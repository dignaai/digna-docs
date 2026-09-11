# Datasets – Filters and Grouping

---

## Why Datasets Exist

Monitoring a table as a single whole hides everything that happens inside it. A national total stays healthy while one region delivers nothing; an overall null rate stays flat while one product line degrades.

A **Dataset** is a named subset of a data source that gets its own statistics, its own learned baseline, and its own status. One data source can carry several, and each behaves as an independently monitored series.

---

## The Three Kinds

A dataset is defined by two SQL fragments, and **the kind you choose decides which of them you get**:

| Kind | Fragment(s) | Behaves like |
|---|---|---|
| **Static** | Filter expression | A `WHERE` condition — one series over a chosen subset of rows |
| **Dynamic** | Grouping expression | A `GROUP BY` — one series per distinct value |
| **Hybrid** | Both | Filter first, then group the remainder |

Conceptually, every statistic is computed as:

```sql
SELECT
    <grouping expression>,
    <statistic>
FROM
    (<snapshot of the data source>)
WHERE
    <filter expression>
GROUP BY
    <grouping expression>
```

Both fragments are written in **the SQL dialect of the source database**, without the `WHERE` or `GROUP BY` keyword — digna supplies those.

---

### Static — filter only

```
Kind:   Static
Filter: status <> 'CANCELLED'
```

One series, over the rows that matter. Cancelled orders no longer drag the sums and averages of a dataset that is supposed to describe live business.

Other typical filters:

```sql
type = 'retail'
country = 'AT' AND status = 'active'
created_at >= DATE '2024-01-01'
```

### Dynamic — grouping only

```
Kind:      Dynamic
Grouping:  region_code
```

One series **per region**, each with its own baseline. A region that normally delivers 40 000 rows and delivers 400 is flagged on its own scale, instead of being absorbed by a national figure that barely moves.

A grouping expression does not have to be a bare column:

```sql
country
DATE(created_at)
EXTRACT(YEAR FROM created_at)
```

To group by more than one column, concatenate them into a single expression — `firstname || ' ' || lastname` — since the grouping is a single value.

### Hybrid — both

```
Kind:      Hybrid
Filter:    channel = 'ONLINE'
Grouping:  country_code
```

Online orders, monitored per country.

!!! tip "Preview before you save"
    Both fields have a **Preview** button that runs the expression against the source and shows what comes back. Use it — a filter that silently matches nothing produces an empty dataset, and a grouping expression over the wrong column produces hundreds of series.

!!! warning "The expressions run on your source database"
    Keep them cheap. An expression over an indexed column is free; one wrapping a column in a function may prevent index use on a large table. A grouping expression over a high-cardinality column (an ID, a timestamp to the second) produces one monitored series per distinct value, which is almost never what you want.

---

## Relevance Rules

A dataset can also carry an optional **relevance rule** — a condition that controls whether an anomaly status is produced at all.

The distinction matters:

- **Statistics are always calculated**, whether or not a relevance rule is set and whether or not it is met.
- If the condition is **not met**, [Data Anomalies](../data_anomalies/how_it_works.md) produces **no status** for that dataset — no green, no yellow, no red.

This is the tool for a dataset that is only meaningful some of the time. A partition that is legitimately empty at weekends, a regional feed that is expected only in season, a subset that exists only after a monthly close — each would otherwise generate a failure every time it is correctly absent. A relevance rule suppresses the verdict without suppressing the measurement, so the history stays complete and the status stays honest.

---

## Grouping and the Distribution Statistic

Grouping and the **Count** statistic operate at different levels, and they compose.

- The **grouping expression** of a Dynamic or Hybrid dataset splits the data source into datasets.
- The **Count** statistic additionally groups by the value of the column it is measuring, so a categorical column produces one measured value per distinct category *within* each dataset.

A dataset grouped by `region_code`, with Count on a `customer_type` column, therefore tracks the retail/business mix **per region** — and reports the region whose mix shifted, not just that the national mix moved.

That composition is powerful and multiplies quickly. A high-cardinality grouping expression combined with a high-cardinality categorical column produces a very large number of series; both should stay in the tens, not the thousands.

---

## Practical Guidance

| Situation | Suggested setup |
|---|---|
| Table with a natural partition (region, channel, product line, source system) | **Dynamic**, grouped on that column |
| Table containing rows that should not count (cancelled, test, soft-deleted) | **Static**, filtering them out |
| One segment of a partitioned table, watched on its own | **Hybrid** — filter to the segment, group within it |
| Table serving two purposes with different expectations | Two **Static** datasets, each with its own filter |
| Small, homogeneous table | One dataset with no expressions is enough |
| A dataset that is legitimately empty some of the time | Add a **relevance rule** rather than lowering sensitivity |
| Column with thousands of distinct values | Do **not** group by it |

---

## Related Pages

- [Profiling – The Foundation](Introduction.md)
- [How Profiling Works](how_it_works.md)
- [Statistics](statistics.md)
- [Data Anomalies – How It Works](../data_anomalies/how_it_works.md)
- [How to add a datasource to a project](../../getting_started/how_to_add_a_datasource_to_project.md)

---