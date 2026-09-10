---
title: Data Timeliness – Use Cases by Industry | digna Documentation
description: Real-world use cases for digna Timeliness. Detect late and missing deliveries across large multi-source landscapes — with AI-learned arrival patterns and user-defined schedules for strict data contracts.
image: /assets/logo_square.png
keywords:
  - data timeliness use cases
  - data freshness monitoring
  - late data detection
  - missing data load
  - data contract sla
  - pipeline monitoring
  - quality of data
  - observability of data
  - multi source data warehouse
  - digna timeliness
lang: en
robots: index, follow
og_title: Data Timeliness – Use Cases by Industry | digna Documentation
og_description: See how digna Timeliness detects late and missing deliveries across banking, healthcare, telecommunications, mobility, and public sector data landscapes.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – Use Cases

---

## When to Reach for This Module

Every other quality check assumes the data is there. *Timeliness* is the module that checks that assumption.

It **automatically learns delivery patterns whenever data is delivered** and detects when data arrives late or does not arrive at all — with no configuration for the ordinary case. Where a delivery is governed by a **strict data contract**, you define the exact expectation instead and let the schedule be the authority.

Most landscapes need both, and the two combine per source:

| Approach | Use it when |
|---|---|
| **AI-learned arrival patterns** | Delivery time varies naturally, or there are too many sources to schedule by hand |
| **User-defined schedules** | A contractual or regulatory window exists and "usually on time" is not the standard |

The two failures it reports:

- **Late** — the delivery arrives, but after its deadline.
- **Missing** — the deadline passed and nothing arrived; a background monitor raises this one, since there is no inspection to report it.

An **early** delivery counts as on time. If upstream re-processing is a concern, the signal to watch is a duplicate-load anomaly in [Data Anomalies](../data_anomalies/use_cases.md), where row count and column sums move together.

---

## Large Multi-Source Warehouses

This is the module's home ground. The published *ITSV* deployment monitors the **timeliness and freshness of around 50 GB of data from 30 different sources in 500 different structures**, loaded daily into their data warehouse.

At that scale the problem is not detecting a single delay, it is **triage**: nobody can hand-schedule 500 structures, and an alert list that treats every source as equally urgent is ignored within a week. Learned patterns give each structure its own baseline, so only genuine deviations surface, and defined schedules are reserved for the deliveries that carry a contract.

### Prioritising remediation across regions

A mobility data hub ingests from several regional sources. Timeliness monitoring shows the state of each one side by side — one region delivering on time, another sitting on a **five-day backlog**. The value is not only the alert; it is knowing which region to fix first, and being able to show that the others are healthy.

---

## Banking and Financial Services

- **Overnight batch windows** — end-of-day feeds have to land before risk, treasury, and regulatory processing begins. A schedule-based expectation makes a missed window an incident rather than something discovered by a failed downstream job.
- **Market and reference data** — rates, prices, and reference files sourced from external providers, where the provider's punctuality is outside your control but very much your problem.
- **Reporting deadlines** — supervisory submissions depend on a chain of upstream deliveries; monitoring the chain gives the reporting team time to react rather than to explain.

---

## Healthcare

- **Clinical feeds from multiple systems** — laboratory results, admissions, and device data arrive on different cadences, each learned separately instead of forced onto a common assumption.
- **Freshness of decision-support datasets** — if a dashboard informs clinical or operational decisions, stale data is more dangerous than an empty dashboard, because nothing signals that it is stale.
- **External reporting obligations** — registry and authority submissions with fixed windows, monitored as strict schedules.

---

## Telecommunications

- **Distributed collection points** — usage and network data arrives from many nodes; learned patterns per node keep a single silent collector from disappearing into an otherwise healthy total.
- **Billing cycle inputs** — a feed that misses the billing run has direct revenue and customer consequences.
- **Re-processing detection** — a collector that replays a period delivers the same data twice; the duplicate shows up in [Data Anomalies](../data_anomalies/use_cases.md) as row count and usage sums moving together, before it reaches aggregation.

---

## Public Sector

- **Statutory reporting windows** — deliveries between agencies with dates set by law, best expressed as explicit schedules.
- **Cross-agency dependencies** — where one agency's output is another's input, timeliness monitoring makes the handover observable to both sides.
- **Evidence of compliance** — the arrival record is itself the proof that a delivery obligation was met, and when it was met.

---

## Practical Rollout

1. **Start with learning.** Onboard sources and let *digna* learn their arrival behaviour; you get coverage across the whole landscape immediately, with no schedule design.
2. **Promote the critical few.** For deliveries with a contract or a deadline, replace the learned expectation with an explicit schedule.
3. **Separate the alert routes.** A missing overnight load needs someone awake; a source drifting half an hour later each week needs the data owner in the morning.
4. **Match the expectation to your inspection cadence.** A delivery is timestamped when digna observed the rows, not when they landed, so a source inspected once a day supports day-level expectations rather than hour-level ones.

!!! note "Runs where your data is"
    Like every *digna* module, timeliness monitoring operates within your infrastructure — nothing is sent out to determine whether a delivery arrived.

---

## Where This Module Fits

*Timeliness* answers **"did it arrive, and when?"** before the other modules ask whether the content is right. A missing delivery reported as a record-count anomaly is a confusing way to learn that a pipeline is down; reported as a missing delivery, it is unambiguous.

---

## Related Pages

- [Data Timeliness – Introduction](Introduction.md)
- [Data Timeliness – How It Works](how_it_works.md)
- [How to schedule a daily job](../../getting_started/how_to_schedule_a_daily_job.md)
- [How to use crontab definition](../../getting_started/how_to_use_crontab.md)
- [digna Modules – Technical Overview](../overview.md)

---
