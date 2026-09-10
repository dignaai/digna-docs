# Profiling – The Foundation

---

## What Profiling Is

**Profiling is the step where digna measures your data.**

It reads each data source and computes a set of numbers describing it — how many rows arrived, how many values were missing, what the totals and averages were, how the values in a categorical column were distributed. Those numbers are called **statistics**, and they are the raw material two of the digna modules are built on.

Profiling is not something you schedule, license, or run separately. **It is part of running the modules that need it.** When *digna Data Anomalies* or *digna Data Analytics* is enabled on a data source, the inspection profiles that data source as part of its work — there is no second job to configure and no extra pass over your data.

---

## Who Reads the Statistics

| Module | Relationship to profiling |
|---|---|
| **[Data Anomalies](../data_anomalies/Introduction.md)** | Built on it — predicts the next value of each statistic and compares the observation against it |
| **[Data Analytics](../data_analytics/Introduction.md)** | Built on it — fits trend and volatility across a window of past statistic values |
| **[Data Validation](../data_validation/Introduction.md)** | Independent — evaluates its own rules row by row and does not read the statistics |
| **[Timeliness](../data_timeliness/Introduction.md)** | Independent — concerned with *when* data arrived, not what is in it |
| **[Schema Tracker](../schema_tracker/Introduction.md)** | Independent — reads the database catalogue, not the data |

This is why understanding profiling is worth the few minutes: it explains what *Data Anomalies* and *Data Analytics* can and cannot see. Both modules are exactly as good as the statistics they were given. A column with no statistics enabled is a column those two modules cannot say anything about — however obviously wrong its contents may be.

The other three modules stand on their own. A data source can run *Data Validation*, *Timeliness*, or *Schema Tracker* without anomaly detection at all.

!!! tip "The practical consequence"
    If *Data Anomalies* is not catching something you expected it to catch, the first question is not "how do I tune it?" but **"is there a statistic that would have moved?"** A swapped `first_name` / `last_name` pair changes no row count and creates no null — it changes string lengths. If the string-length statistics are not enabled on those columns, no amount of tuning will find it.

---

## What Profiling Produces

Every inspection, for every data source, profiling produces:

- **A row count** for each dataset and for the data source as a whole. This always happens, for every data source, with no module enabled at all.
- **The enabled statistics**, computed per dataset and per column, for the data sources whose modules need them.

Both are stored with the date they describe, so each one becomes a point in a time series. A single measurement is not interesting; the series is what allows a prediction, a trend, or a volatility figure.

See [Statistics](statistics.md) for the full list of what can be measured, and [Datasets](datasets.md) for how one table can be split into several independently measured subsets.

---

## Your Data Stays Where It Is

Profiling is executed **inside your database**. digna sends SQL and receives numbers.

What comes back is aggregates — a count, a sum, an average, a count per category. **No rows are copied out, and no raw values are transmitted or stored by digna.** The one exception is deliberate and user-initiated: when a validation rule fails, you can ask to see the records that failed it, because a count alone is not something anyone can act on.

This is the property that makes digna usable on regulated data — clinical records, transaction data, personal data under GDPR — and it is a consequence of the architecture rather than a policy layered on top. digna is installed on-premises or in your private cloud, so there is no external service for data to be sent to.

---

## Related Pages

- [How Profiling Works](how_it_works.md) — the mechanics, and the settings that shape them
- [Statistics](statistics.md) — every statistic digna can compute
- [Datasets](datasets.md) — filters and grouping
- [digna Modules – Technical Overview](../overview.md)

---