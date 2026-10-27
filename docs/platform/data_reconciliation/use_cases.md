---
title: Data Reconciliation – Use Cases | digna Documentation
description: Practical use cases for digna Data Reconciliation. Standard reconciliation procedures in finance and regulatory reporting, validation of ETL processes, data migrations and replications, with exact rules for known controls and AI rules for complex flows.
image: /assets/logo_square.png
keywords:
  - data reconciliation use cases
  - ETL validation
  - financial reconciliation
  - regulatory reporting reconciliation
  - data migration validation
  - data replication monitoring
  - digna data reconciliation
lang: en
robots: index, follow
og_title: Data Reconciliation – Use Cases | digna Documentation
og_description: See how digna Data Reconciliation supports reconciliation procedures, ETL validation, migrations and replications — with exact rules for known controls and AI rules for complex flows.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Reconciliation – Use Cases

---

## When to Reach for This Module

Use **Data Reconciliation** when the question is not "is this table healthy?" but "did this table receive what it should have?". The other modules look at one data source at a time. Reconciliation looks at the step between data sources.

| Situation | Rule type |
|---|---|
| The target should match one source, and you know how | **Exact** |
| A reconciliation control must be documented and auditable | **Exact** |
| The target is built from several sources by logic you don't want to rewrite | **AI** |
| The relationship changes slowly over time, e.g. with growing volumes | **AI** |

---

## Standard Reconciliation Procedures

Finance, risk and controlling teams reconcile data as part of their regular close and reporting processes. These controls are known in advance, which makes them **exact rules**.

### Totals between the ledger and the reporting layer

Compare the sum of booked amounts in the general ledger with the sum in the reporting data mart, per entity or per currency (using [datasets](../profiling/datasets.md)). A relative tolerance of 0 % means every cent must arrive. A small absolute tolerance allows for known rounding.

### Record counts before regulatory submission

Before a regulatory report is submitted, confirm that the number of contracts, positions or transactions in the reporting table matches the source system. A failed check on the day of submission is a reason to stop and investigate, not a finding for next month.

### Evidence for auditors

Each exact check is stored per date with both values, the difference and the tolerance. That history shows that the control was performed every day, and what it found.

---

## Validating ETL Processes

A target table in a data warehouse is often built from several source tables: orders joined with customers, filtered by status, aggregated per day. Rewriting that logic as a reconciliation query duplicates the ETL and breaks whenever the ETL changes. **AI rules** avoid both.

### A fact table built from several sources

Select the row counts and amount sums of the source tables as source checks, and the row count and amount sum of the fact table as target checks. digna learns how the fact table follows its sources. When a join suddenly drops rows or a filter changes, the target no longer matches what today's sources predict, and the check turns **Uncertain** or **Failed**.

### Loads that grow with their sources

When volumes grow, a fixed threshold either alerts constantly or never. An AI rule predicts the target from the same day's source values, so growth in the sources is expected growth in the target. Only a break in the relationship alerts.

---

## Migrations and Replications

### Platform migration

During a migration, the old and the new platform run side by side. An **exact rule** per migrated table compares row counts, sums and distinct counts between the two, with the old platform as the source. Because sources and target can be on different database connections, the old and new platforms don't need to be the same technology.

### Replication between sites

For a replica that should match its primary exactly, an exact rule on the row count with a tolerance of 0 detects replication lag and lost records on the first inspection after they occur.

---

## Designing Rules That Stay Useful

- **Start with exact rules where you can.** If you can write the relationship down, an exact rule is simpler to explain and to audit.
- **Choose a few strong checks.** Row counts and sums of key amounts catch most losses. Comparing every statistic of every column adds noise, not coverage.
- **Segment the target the way the business reads it.** Datasets per region, entity or product line show where a difference is, not just that one exists.
- **Give AI rules time.** A new AI rule needs about a month of shared history before it judges. Use the first weeks to check that the predictions look plausible.
- **Inspect sources before the target.** Reconciliation waits for every source to be inspected for the date, so schedule the target's inspection after its sources'.

---

## Where This Module Fits

- **Data Validation** checks rules inside one data source, and referential integrity between two. Reconciliation compares aggregated values between data sources.
- **Data Anomalies** learns how one series behaves over time. AI reconciliation learns how one data source behaves **relative to others** on the same day.
- **Timeliness** tells you whether the data arrived. Reconciliation tells you whether all of it arrived.

---

## Related Pages

- [Data Reconciliation – Introduction](Introduction.md)
- [Data Reconciliation – How It Works](how_it_works.md)
- [Data Validation – Use Cases](../data_validation/use_cases.md)
- [Changelog – Release 2026.11](../../changelog/Release_202611.md)
