---
title: How Profiling Works | digna Documentation
description: The mechanics of digna profiling — the snapshot query and the #date# marker, how dataset filters and grouping are applied, Standard, Session and Permanent work tables, Single and Combined query modes, and the row counts that always run.
image: /assets/logo_square.png
keywords:
  - digna profiling
  - snapshot query
  - profiling mode
  - session permanent work table
  - query mode single combined
  - row count data volume
  - incremental inspection
  - quality of data
  - observability of data
lang: en
robots: index, follow
og_title: How Profiling Works | digna Documentation
og_description: Snapshot queries, work tables, query modes, and the row counts that always run — the mechanics of digna profiling.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# How Profiling Works

---

## One Pass Over the Data

Whatever an inspection ends up reporting, it reads your data **once**:

```
1. Build a snapshot     what rows are in scope for this date
2. Materialise          optionally, into a work table
3. Measure              row counts, then the enabled statistics
4. Store                one value per dataset, column, and statistic
```

The modules then work from what step 3 produced. *Data Anomalies* and *Data Analytics* read the statistics; *Data Validation*, when it is enabled, evaluates its own rules against the same snapshot in the same pass, so it too needs no separate trip to the source.

---

## Step 1 – The Snapshot

The snapshot is the set of rows the inspection considers. How it is built depends on what the data source is:

| Data source kind | Snapshot |
|---|---|
| **TABLE** or **VIEW** | A `SELECT` over the object, restricted to the columns with statistics enabled |
| **QUERY** | The SQL you supplied, used as-is |

For tables and views, an optional **snapshot filter** narrows it further. This is the place to exclude rows that should never count toward any measurement — test records, soft-deleted rows, a partition that is not yet complete.

!!! note "Only the columns in use are read"
    The snapshot selects the columns that actually carry statistics, not `SELECT *`. Adding a column to a table therefore changes nothing until you give that column a category and statistics of its own.

### Snapshot query tags

A snapshot query is a **template**, not a fixed statement. Tags let one query serve every inspection date and stay portable between environments:

| Tag | Resolves to |
|---|---|
| `#db_name#` | The database name from the connection |
| `#schema_name#` | The schema name from the connection |
| `#date#` | The date being inspected, as `YYYY-MM-DD` |
| `#date+N#` | *N* days after the inspected date |
| `#date-N#` | *N* days before it |

```sql
select * from #db_name#.#schema_name#.orders
where load_date = '#date#'
```

The date offsets are what let a source be described whose data lands a day late, or whose window spans a boundary:

```sql
select * from #db_name#.#schema_name#.events
where ts >= date('#date#') and ts < date('#date+1#')
```

An offset that cannot be resolved is reported as an error rather than quietly falling back to the unshifted date — a wrong window would silently measure the wrong rows.

This is what makes inspections **per-date and re-runnable**. Each date is measured on its own, a range can be backfilled, and re-inspecting a date replaces that date's results rather than duplicating them.

!!! note "The inspection offset is a different setting"
    A scheduled job also has an **Offset**, which decides *which* date an inspection run is for. Offset `0` inspects the day the job runs; offset `-1` inspects yesterday. The offset picks the date; the `#date#` tag is how your query receives it.

---

## Step 2 – Work Tables

A snapshot may be read many times in one inspection — once per statistic, or once per dataset. Whether it is materialised first is a property of the database connection:

| Profiling mode | What happens | Suits |
|---|---|---|
| **Standard** | No work table; statistics are computed directly against the snapshot query | Simple sources, cheap snapshots |
| **Session** | The snapshot is written to a connection-scoped temporary table, which disappears when the connection closes | The usual choice where the technology supports it |
| **Permanent** | The snapshot is written to a real table, created and dropped around the profiling run | Technologies where a session-scoped table is not usable |

**Session** is the mode to prefer where it is available: the snapshot is evaluated once instead of being re-evaluated by every statistic, and nothing is left behind afterwards. **Permanent** achieves the same thing on technologies that do not offer a usable temporary table, at the cost of creating and dropping a real object.

The work table is dropped even when profiling fails, so a failed inspection does not leave an object behind that blocks the next one.

---

## Step 3 – Measuring

Each dataset's [filter and grouping expressions](datasets.md) are applied, and every enabled statistic becomes an aggregate over the result:

```sql
SELECT
    <grouping expression>,
    <statistic>
FROM
    (<snapshot>)
WHERE
    <filter expression>
GROUP BY
    <grouping expression>
```

### Query mode

How those aggregates are packed into SQL is set per data source:

| Query mode | Behaviour |
|---|---|
| **Combined** | Every statistic is computed within a single SQL query |
| **Single** | Each statistic is computed by its own dedicated query |

**Combined** reduces the number of queries and the round trips they cost, and is the better fit when the source can comfortably hold the combined query in memory. **Single** issues more queries, each with a smaller memory footprint, which is what large data sources need when a combined query risks running into out-of-memory or spool limits.

Query mode changes only how the work is packaged. The statistics it produces are identical either way, so switching modes on an existing data source does not create a discontinuity in its history.

---

## Row Counts

Row counting is the one measurement that is **not** conditional on any module.

Every inspection counts the rows in each dataset and in the data source as a whole, and stores those counts as statuses at dataset and data source level. This happens with no module enabled, because a data source that delivered no rows is worth knowing about regardless of what else you have configured — and because it is what [Timeliness](../data_timeliness/how_it_works.md) keys off to decide whether a delivery happened at all.

These counts have their own switch in a notification subscription, so they can be routed or silenced separately from anomaly findings.

### Report Empty Datasets

A data source carries a **Report Empty Datasets** option. With it enabled, digna raises an alert when the snapshot query returns no rows at all for the inspected date — the signal of a missing extraction or a failed upstream job, which is otherwise easy to mistake for a quiet day.

!!! note "Row counts and the Row Count statistic"
    The two are related but not the same thing. The always-on count reports the volume that arrived. The **Row Count** [statistic](statistics.md) is the same number treated as a time series, so that [Data Anomalies](../data_anomalies/how_it_works.md) can predict it and flag a short load — which needs the *Data Anomalies* module.

---

## Step 4 – Storage and Re-Running

Each measured value is stored against the dataset, column, statistic, and date it belongs to. Nothing is aggregated away, so any statistic can be read back later as a full time series.

Before writing, an inspection removes its own previous results for the dates in scope. That is what makes a data source safe to re-inspect: running the same date twice leaves one set of results, not two. Delivery history for [Timeliness](../data_timeliness/how_it_works.md) is deliberately exempt — re-inspecting an old date must not erase the record of what was delivered that day.

---

## Getting Profiling Right

1. **Categorise columns deliberately.** The [attribute category](statistics.md#attribute-categories-decide-the-default-set) decides which statistics a column gets. The default set is a reasonable start, not an answer for every column.
2. **Add the statistic that would move.** Work backwards from the failure you want to catch — a swapped column moves string lengths, a truncated load moves row counts, a broken lookup moves the distribution.
3. **Turn off what nobody acts on.** A statistic producing findings nobody investigates makes the whole data source look unhealthy and trains people to ignore the colour.
4. **Use the snapshot filter for rows that should never count**, and [dataset filters](datasets.md) for subsets you want measured separately. They are different tools: the first removes rows from all measurement, the second creates a measurement of its own.

---

## Related Pages

- [Profiling – The Foundation](Introduction.md)
- [Statistics](statistics.md)
- [Datasets](datasets.md)
- [Data Anomalies – How It Works](../data_anomalies/how_it_works.md)

---
