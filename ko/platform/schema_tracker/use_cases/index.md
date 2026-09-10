# Schema Tracker – Use Cases

---

## When to Reach for This Module

Schema changes are different from every other data problem: they are usually **someone's intentional work**, made in one place, that turns into an unintended failure somewhere else entirely. The person who dropped the column had no list of who depended on it.

*Schema Tracker* continuously monitors database structure and reports **added columns, removed columns, and data type changes** — whether intentional or accidental. Every change is **timestamped, attributed, and stored**, so the question "when did this change and who changed it" has an answer instead of a discussion.

A rename appears as a removal plus an addition, because a column is identified by its name — see [How It Works](how_it_works.md#the-three-events).

Two distinct failure shapes make this worth monitoring on its own:

- **Loud breaks** — a removed or renamed column; the job fails, and the only cost is the time spent finding out why.
- **Silent breaks** — a type change that still loads. `DATE` becomes `STRING`, sorting and date arithmetic quietly change behaviour, and reports are wrong for weeks before anyone notices. These are the **invisible errors** that cost the most.

---

## The Canonical Example

A `customer_profiles` table changes overnight:

| Change | Type | Consequence |
|---|---|---|
| `is_subscribed` removed | Removed column | **12 downstream reports** reference the field |
| `signup_date` converted `DATE` → `STRING` | Risky type conversion | Loads succeed; cohort and retention calculations silently degrade |

The removal is discovered eventually, because something fails. The conversion is the dangerous one: nothing fails, and the numbers stay plausible. *Schema Tracker* surfaces both at the moment they happen, with the timestamp and the attribution that make the follow-up conversation short.

---

## Banking and Financial Services

- **Core banking and risk models** — a datatype narrowing on an amount or identifier column can truncate values without an error; the resulting figures are wrong but not obviously wrong.
- **Regulatory reporting lineage** — supervisory submissions are built on a fixed structural contract. A stored, attributed change history is the evidence that the structure was stable across a reporting period, or the record of exactly when it was not.
- **Change control across environments** — structural differences between development, test, and production are a recurring cause of "it worked in test"; drift detection makes the divergence visible rather than inferred.

---

## Healthcare

- **Feeder system upgrades** — clinical source systems are updated on their own schedule and vendors add or rename fields as part of routine releases. The receiving warehouse learns about it from *Schema Tracker*, not from a broken nightly load.
- **Coded field type changes** — a code column changing type or width can silently truncate or reformat values that must match a national code list exactly.
- **Auditability** — for regulated clinical data, knowing when a structure changed is part of being able to defend the data derived from it.

---

## Telecommunications

Telecommunications landscapes have the exact profile this module protects against: **high-volume data through distributed pipelines, where a small source change creates widespread downstream errors**.

- A field added by a network element vendor propagates into ingestion jobs that were not expecting it.
- A rename in a customer or subscription source breaks joins across several domains at once, and surfaces as a removal and an addition on the same inspection.
- Type changes on usage counters affect billing aggregation before they affect anything visible.

---

## Retail and E-Commerce

- **Platform migrations and replatforming** — the period with the highest structural churn and the lowest tolerance for broken reporting.
- **Third-party and marketplace feeds** — external partners change their export structure without a release note; the change arrives as data.
- **Seasonal readiness** — a structural check before a peak trading period is cheap; discovering drift during it is not.

---

## Public Sector

- **Shared data contracts between agencies** — where several consumers depend on one structure, *Schema Tracker* keeps the contract observable to the provider and the consumers alike.
- **Long-lived registers** — datasets maintained across decades accumulate structural changes; a stored change history is what keeps historical comparisons defensible.
- **Traceability requirements** — timestamped, attributed change records are the form of evidence public sector audits expect.

---

## Making It Actionable

1. **Track the tables other people consume**, not just your own. The cost of a change is carried downstream.
2. **Treat type changes as findings in their own right.** They will not announce themselves in a job log.
3. **Route structural alerts to the owning team**, so the person who can explain the change is the person who receives it.
4. **Check the change history first when an anomaly appears.** A distribution shift on the same day as a type conversion is not two problems.

!!! tip "Pair it with anomaly detection"
    *Schema Tracker* tells you the structure changed; [*Data Anomalies*](../data_anomalies/Introduction.md) tells you the content changed. Together they usually explain each other, and having both turns a two-day investigation into a two-minute one.

---

## Coverage

Structural monitoring works across the data platforms *digna* connects to — Teradata, Snowflake, Databricks, Oracle, PostgreSQL, MS SQL Server, Azure Synapse, and the rest of the supported list. See the [database connector guides](../../databases/snowflake_connector_guide.md) for connection setup.

---

## Where This Module Fits

| Question | Module |
|---|---|
| Did the structure change? | **Schema Tracker** |
| Did the content change unexpectedly? | [Data Anomalies](../data_anomalies/Introduction.md) |
| Is a metric trending or destabilising? | [Data Analytics](../data_analytics/Introduction.md) |
| Does every row satisfy our rules? | [Data Validation](../data_validation/Introduction.md) |
| Did the data arrive on time? | [Data Timeliness](../data_timeliness/Introduction.md) |

---

## Related Pages

- [Schema Tracker – Introduction](Introduction.md)
- [Schema Tracker – How It Works](how_it_works.md)
- [digna Modules – Technical Overview](../overview.md)
- [How to connect a database to a data project](../../getting_started/how_to_connect_database_to_data_project.md)

---