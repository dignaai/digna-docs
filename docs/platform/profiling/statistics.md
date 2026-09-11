---
title: Profiling Statistics Reference | digna Documentation
description: The complete reference of statistics digna computes while profiling a data source — Row Count, Null Count, Sum, Average, string lengths, distribution counts — which attribute category enables each one, and how each is translated into SQL.
image: /assets/logo_square.png
keywords:
  - digna statistics
  - data profiling metrics
  - null count
  - row count
  - average string length
  - attribute category
  - numerical categorical unspecified
  - data quality metrics
  - quality of data
  - observability of data
  - in-database profiling
lang: en
robots: index, follow
og_title: Profiling Statistics Reference | digna Documentation
og_description: Every statistic digna computes while profiling, which attribute category enables it, and what it means for anomaly detection.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Profiling Statistics Reference

---

## What a Statistic Is

Every digna module is built on the same foundation: a small set of **statistics** computed per dataset and per column, in-database, on each inspection.

Profiling is the one step that always runs — it is not gated behind a module flag. The modules then differ only in what they do with the numbers profiling produced:

| Module | What it does with the statistics |
|---|---|
| **Data Anomalies** | Predicts the next value and compares the observation against it |
| **Data Analytics** | Fits trend and volatility over a window of past values |
| **Data Volume** | Reports row counts at dataset and data source level (always on) |

Because the statistics are shared, enabling a second module costs no extra profiling work on the source.

---

## The Statistics

| Statistic | Group | Level | SQL it becomes |
|---|---|---|---|
| **Row Count** | Data volume | Table | `count(*)` |
| **Null Count** | Missing values | Column | `count(CASE WHEN col IS NULL THEN 1 END)` |
| **Sum** | Numerical metrics | Column | `sum(col)` |
| **Average** | Numerical metrics | Column | `avg(col)` |
| **Minimum String Length** | Text length | Column | `min(length(col))` |
| **Average String Length** | Text length | Column | `avg(length(col))` |
| **Maximum String Length** | Text length | Column | `max(length(col))` |
| **Count** | Distribution | Column | `count(col)`, grouped by the column's own value |
| **Number of Unique Values** | Distribution | Column | `count(distinct col)` |
| **Number of Negative Values** | Distribution | Column | `count(CASE WHEN col < 0 THEN 1 END)` |
| **Number of Zero Values** | Distribution | Column | `count(CASE WHEN col = 0 THEN 1 END)` |
| **Number of Positive Values** | Distribution | Column | `count(CASE WHEN col > 0 THEN 1 END)` |

The SQL above is the PostgreSQL rendering. Each supported technology carries its own template set, so the same statistic is expressed in the dialect of Teradata, Snowflake, Databricks, Oracle, MS SQL Server, Netezza, Hive, or Impala as appropriate — but the meaning is identical across all of them.

!!! note "Count is the distribution statistic"
    **Count** is the only statistic that also groups by the value of the column itself, producing one measured value per distinct category. That is what lets digna learn the *shape* of a categorical column and flag an unexpected member — not just how many non-null values it has.

---

## Attribute Categories Decide the Default Set

When an attribute (column) is added to a data source it is given a **category**, and the category determines which statistics are switched on automatically:

| Category | Typical content | Statistics enabled by default |
|---|---|---|
| **Numerical** | Amounts, quantities, measurements | Null Count, Sum, Average |
| **Categorical** | Discrete labels, types, classifications | Null Count, Count |
| **Unspecified** | Free text, IDs, mixed or unstructured values | Null Count, Average String Length, Number of Unique Values |
| **Custom** | Anything needing a specific set | Exactly the statistics you select — nothing is inferred |

**Unspecified** is the default for a column that is neither clearly numerical nor clearly categorical.

**Row Count** sits outside this table. It is table-level, belongs to no category, and is always computed.

Use **Custom** when the defaults do not fit — for example to add **Minimum** and **Maximum String Length** to a code column where a width change matters, or **Number of Negative Values** to an amount column that should never go below zero.

!!! tip "The column-swap signal"
    A swapped `first_name` / `last_name` pair produces no null, no row-count change, and no rule violation. What moves is **Average String Length** on both columns at once. Categorising those columns as **Unspecified** — or adding the string-length statistics through **Custom** — is what makes that failure visible.

---

## Positive Statistics

Each statistic carries a flag saying whether it can legitimately be negative. All of them are non-negative by construction **except Sum and Average**, which follow the data.

For the non-negative ones, digna floors the whole predicted band at zero, so a prediction interval never suggests that a count could be below zero. For Sum and Average it does not, because a negative total is a real possibility.

---

## Turning Statistics Off

Not every column deserves every statistic. Each combination of **table + column + statistic** is a mapping that can be switched off individually, and switching one off removes it from anomaly detection without removing the profiled value.

The same mapping also carries four optional numeric limits used by [Data Anomalies](../data_anomalies/how_it_works.md):

| Setting | Effect |
|---|---|
| **Lower Limit** / **Upper Limit** | Clamp the predicted value and its bands into a range you know the metric cannot leave |
| **Min Threshold** / **Max Threshold** | Put a floor and a ceiling on the *width* of the tolerance band |

**Min Threshold** is the practical answer to a metric that is almost perfectly stable: without a floor, a series that has been identical for weeks produces a near-zero band, and the first ordinary fluctuation is reported. **Max Threshold** is the opposite guard, for a noisy series whose band would otherwise grow wide enough to hide a genuine problem.

---

## Related Pages

- [Profiling – The Foundation](Introduction.md)
- [How Profiling Works](how_it_works.md)
- [Datasets](datasets.md) — how filters and grouping split a table into monitored subsets
- [Data Anomalies – How It Works](../data_anomalies/how_it_works.md)

---
