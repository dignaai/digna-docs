# Data Anomalies – Use Cases

---

## When to Reach for This Module

*digna Data Anomalies* is the right module when **you cannot describe in advance what "wrong" looks like**.

It learns the natural patterns in your data and alerts you whenever something looks implausible — with **no thresholds and no rules to maintain**. That makes it the default starting point for any table you have just onboarded, and the only practical option for environments where hand-written checks would run into the hundreds.

The same engine covers two purposes that are usually split across separate tools:

- **Data quality** — is this delivery complete, well-formed, and consistent with every delivery before it?
- **Business and operational KPIs** — has a number that the business steers by moved in a way nobody expected?

Both are computed from the same column metrics, in-database, so adding KPI monitoring on top of quality monitoring costs no extra profiling run.

!!! tip "Rules still have their place"
    Use *Data Anomalies* for the unknown unknowns and [*Data Validation*](../data_validation/Introduction.md) for the requirements you can write down — a mandatory VAT code, a currency in `{EUR, USD}`, an amount that must be positive. Most production projects run both.

---

## Banking and Financial Services

### Incomplete overnight loads before risk reporting

A core banking table normally receives around 500 000 transaction records per night. One morning the load completes without error, but only 50 000 rows arrived — an upstream extract silently truncated.

| | |
|---|---|
| **Metric that moves** | Record count |
| **What digna does** | Compares the value against the learned range for that weekday and flags the deviation with a confidence score |
| **Why it matters** | Risk and regulatory reports are built before anyone opens the source table; a short load becomes a wrong submission |

### Balances and exposure drifting out of range

Average account balance, total exposure per segment, or the sum of a position column shifts gradually rather than breaking. Because *digna* tracks `sum`, `avg`, `min`, and `max` per column over time, the drift is visible as an anomaly long before it is visible in a quarterly report.

### Swapped or misaligned columns after an ETL change

A pipeline change reverses `first_name` and `last_name`. No job fails, no null appears, and row counts are perfect. What changes is the **average string length and value distribution** of each column — which is exactly what *digna* profiles, so the swap surfaces as a paired anomaly on both columns.

### Unexpected categorical values

A `city` column that has only ever contained Austrian cities suddenly contains *Zurich*. *digna* classifies the column as **categorical**, learns its value distribution, and flags the new member as unexpected.

---

## Healthcare

### Clinical and claims data completeness

Patient, encounter, and claims tables are assembled from many feeder systems, each with its own release cycle. A missing-value ratio that jumps from 0.2 % to 11 % on a diagnosis code column is not a schema break and not a rule violation — it is a change in behaviour, and it is what this module is built to catch.

### Reference data that quietly changes meaning

Code lists (diagnosis, procedure, department) are updated by external bodies. When the distribution across a coded column reshapes after such an update, *digna* reports it, giving analytics teams a chance to check whether historical comparisons are still valid.

!!! note "No data leaves your environment"
    All profiling and detection run **inside your database**. *digna* reads and stores metrics, never patient records — which is what makes the module usable on regulated clinical data at all.

---

## Telecommunications

Telecommunications teams move high volumes of customer and operational data through distributed pipelines, so a small change at one source can create widespread downstream errors.

- **CDR and usage volumes** — call, message, and data-usage counts have strong daily and weekly seasonality. *digna* learns that shape, so a genuine drop on a Tuesday is flagged while the normal Sunday dip is not.
- **Per-region deliveries** — with metrics defined on **filtered subsets (Datasets)**, each region, product line, or network element is monitored on its own baseline instead of disappearing into a national total.
- **Churn and activation KPIs** — the same profiling run that guards data quality also watches the operational numbers built from it.

---

## Retail and E-Commerce

- **Sales and order volumes** per store, channel, or SKU group, each with its own learned pattern.
- **Rising NULL rates after a migration** — a classic post-cutover failure where the job succeeds and the content degrades.
- **Duplicate batch loads** — an ingestion replay doubles a day's revenue; the record count and the sum of the amount column both move together, which reads unmistakably as a duplicated load rather than a good day.

---

## Public Sector

Public sector agencies typically need **traceability across systems** rather than speed alone. *digna Data Anomalies* contributes the audit trail: every flagged anomaly carries the metric, the observed value, the learned expected range, a timestamp, and a confidence score, so a data issue raised months later can be reconstructed rather than argued about.

Register and case-management data also tends to be **irregular by nature** — filing peaks at deadlines, quiet periods between them. Learned seasonality handles this without an analyst maintaining a calendar of exceptions.

---

## Choosing What to Monitor

Broad coverage is the point of this module, but not every column deserves attention. *digna* lets you **disable metrics per column, per table, or per project**, which keeps profiling fast and the alert list credible.

A practical starting point:

| Priority | What to keep monitored |
|---|---|
| **Always** | Record counts on every fact and transaction table |
| **Always** | Missing-value ratios on business-critical columns |
| **High** | Sums and averages of columns that feed reported KPIs |
| **High** | Distributions of categorical columns used as report dimensions |
| **Selective** | Free-text and technical columns — usually noise, disable unless a swap risk exists |

---

## Where This Module Fits

| Question | Module |
|---|---|
| Did something change that nobody expected? | **Data Anomalies** |
| Is that change part of a longer trend, or a one-off? | [Data Analytics](../data_analytics/Introduction.md) |
| Does every row still satisfy the rules we wrote down? | [Data Validation](../data_validation/Introduction.md) |
| Did the data arrive at all, and on time? | [Data Timeliness](../data_timeliness/Introduction.md) |
| Did the structure change underneath us? | [Schema Tracker](../schema_tracker/Introduction.md) |

---

## Related Pages

- [Data Anomalies – Introduction](Introduction.md)
- [Data Anomalies – How It Works](how_it_works.md)
- [digna Modules – Technical Overview](../overview.md)
- [How to add a datasource to a project](../../getting_started/how_to_add_a_datasource_to_project.md)

---