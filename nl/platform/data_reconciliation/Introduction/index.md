# Data Reconciliation – Source-to-Target Consistency

**digna Data Reconciliation** was introduced in [Release 2026.11](../../changelog/Release_202611.md) as a beta version.

---

## Purpose

Data rarely stays in one place. It is loaded from operational systems into a staging area, transformed into a data warehouse, aggregated into data marts, migrated to new platforms and replicated between sites. Every step can lose rows, duplicate them or change values, and each table can still look perfectly healthy on its own.

**Data Reconciliation** checks the step between tables. It compares a **target** data source with the **sources** it was built from, and alerts when they no longer match.

---

## Two Types of Rules

Reconciliation is configured as named rules on the target data source. Each rule is one of two types.

### Exact rules – reconciliation as a data quality rule

You define exactly what must match between **one source and one target**: the row count of a replicated table, the sum of an amount column before and after a load, the number of distinct customers in two systems. Each pair is compared with a tolerance, either absolute (e.g. ± 10) or relative to the source (e.g. ± 0.5 %).

Exact rules are deterministic. They suit reconciliation procedures that a controller, an auditor or a regulator expects to see written down.

### AI rules – reconciliation as data observability

For a target built from **several sources** by joins, filters and aggregations, the relationship is often unknown or too complex to write down. An AI rule learns it instead. digna observes how the target has followed its sources in the past, predicts what the target should be today from the sources' values of the same day, and alerts when the target leaves the expected range.

AI rules suit ETL processes and other flows where you know which tables feed the target, but not the exact logic between them.

---

## Technical Overview

- **Built on profiling** – Reconciliation compares the statistics digna already measures for each data source, such as row counts, sums and distinct counts. It sends no extra queries to compare tables.
- **Segment by segment** – When the target is split into [datasets](../profiling/datasets.md), each dataset is compared with the source dataset of the same name, e.g. region by region.
- **Part of the inspection** – Reconciliation runs in the target's inspection, once every source has been inspected for the same date. Its results count towards the inspection status and trigger notifications like every other module.
- **Timeline per rule** – The Dashboard shows each reconciliation check over time: the compared values, the difference and the tolerance or expected range.

---

## Related Pages

- [Data Reconciliation – How It Works](how_it_works.md)
- [Data Reconciliation – Use Cases](use_cases.md)
- [Data Validation – Introduction](../data_validation/Introduction.md)
- [Changelog – Release 2026.11](../../changelog/Release_202611.md)