---
title: Statuses and Alerts | digna Documentation
description: How digna turns measured values into Passed, Uncertain, and Failed statuses, how those roll up from check to attribute, dataset, and data source, and how subscriptions route each module's findings to email, Slack, or Jira.
image: /assets/logo_square.png
keywords:
  - digna status model
  - passed uncertain failed
  - data quality alerting
  - notification channel
  - slack jira email alerts
  - status rollup
  - quality of data
  - observability of data
lang: en
robots: index, follow
og_title: Statuses and Alerts | digna Documentation
og_description: The digna status model — Passed, Uncertain, Failed — how statuses roll up across levels, and how alerts are routed to email, Slack, and Jira.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Statuses and Alerts

---

## The Four Statuses

Every check digna evaluates ends in one of four states, and the same vocabulary is used by all five modules:

| Status | Meaning |
|---|---|
| **Not tested** | No result — the check did not run, or there was not enough history to evaluate it |
| **Passed** | The observation is within expectations |
| **Uncertain** | Outside the inner tolerance but inside the outer one — worth a look, not yet a failure |
| **Failed** | Outside the outer tolerance, or a rule was breached beyond its threshold |

**Uncertain** is the status that makes continuous monitoring usable. Without a middle state, every tolerance is a cliff edge: a metric one unit past the line is indistinguishable from one that collapsed. Which modules can produce it differs, and the difference is not arbitrary:

| Module | Can report Uncertain? | Why |
|---|---|---|
| **Data Anomalies** | Yes | The tolerance is a band with an inner and an outer edge |
| **Data Validation** | Yes | Rules carry both an info and a warning threshold |
| **Data Analytics** | No | Limits are user-defined lines — inside or outside |
| **Schema Tracker** | No | The structure either changed or it did not |
| **Timeliness** | No | The delivery either met its deadline or it did not — reported as **In Time** / **Delayed** |

---

## How a Status Is Reached

### Data Anomalies — a band around a prediction

The model predicts the next value and derives a tolerance `bound` from how wrong it has recently been. Four edges follow:

```
       ├──── Failed ────┼─ Uncertain ─┼──────── Passed ────────┼─ Uncertain ─┼──── Failed ────┤
                    predicted        predicted             predicted      predicted
                    − 2 × bound      − 1 × bound           + 1 × bound    + 2 × bound
```

An observation inside ±1 bound passes; between one and two bounds it is uncertain; beyond two it fails. The width of `bound` follows from the recent prediction error on that series, adjusted by the data source's **Sensitivity** and **Memory** settings — see [Data Anomalies – How It Works](../data_anomalies/how_it_works.md#step-3-the-tolerance-band).

### Data Validation — two thresholds on the failure count

Each rule counts passing and failing records, then compares that count against its own thresholds. Two modes are available:

| Threshold mode | Compared quantity |
|---|---|
| **Absolute** | The number of failed records |
| **Relative** | Failed records as a fraction of all records evaluated |

Above the **Info threshold** gives **Uncertain**; above the **Warn threshold** gives **Failed**. Both default to zero, so out of the box a single failing record is a failure — deliberately strict, and easy to relax where a small tail of exceptions is expected.

### Data Analytics — user-defined limits

A trend or volatility value outside its configured lower or upper limit is **Failed**; anything else is **Passed**. A limit left empty is not evaluated, so a rule with neither limit set never fails.

### Schema Tracker and Timeliness — binary by nature

A structural change that matches an enabled event type is **Failed**. A delivery arriving after its deadline is **Delayed**. Neither has a meaningful middle state.

---

## Rollup: Worst Result Wins

Statuses are produced at check level and then aggregated upward:

```
check  →  attribute (column)  →  dataset  →  data source
```

At each level the status is the **worst** of the statuses below it, alongside a count of how many checks passed, were uncertain, and failed. One failing check therefore turns its column, its dataset, and its data source red.

That is the correct default — a data source with a known problem is not healthy — but it is also why disabling irrelevant statistics matters. A noisy check nobody acts on makes the whole data source look broken and trains people to ignore the colour.

---

## Alerts

### Channels

Notifications are delivered through configured channels:

| Channel | Typical use |
|---|---|
| **Email** | Data owners, wide distribution, daily digests |
| **Slack** | The operational channel that handles pipelines |
| **Jira** | Findings that need a tracked ticket and an assignee |

### Subscriptions

A subscription binds a channel to a project and decides what reaches it. It covers either **all tables** in the project or a named list, and each module can be switched on or off independently:

| Subscription setting | Reports |
|---|---|
| Notify Errors | Inspection failures — the job itself did not complete |
| Notify Data Volume | Row-count findings |
| Data anomalies | AI-detected deviations |
| Data validation | Rule breaches |
| Data analytics | Trend and volatility limit breaches |
| Delayed delivery | Missed timeliness deadlines |
| Schema change | Structural changes |

A subscription can also be set to notify on **every** inspection rather than only when something is wrong — useful for a low-volume critical feed where silence is ambiguous, and unhelpful for anything else.

!!! tip "Split the routes by urgency, not by team"
    A missed overnight delivery and a slow upward drift in a null rate are both real findings, and they need different destinations. Route timeliness and inspection errors to the channel someone is watching, and anomalies, analytics, and schema changes to the data owner's queue.

### Missed deliveries are a special case

Every other status is produced by an inspection. A **missing** delivery, by definition, has no inspection to produce it — so a background monitor checks every minute for deadlines that have passed, and raises the alert independently.

Each missed deadline is claimed exactly once before its message is sent, so a delivery that stays missing does not re-alert on every tick.

---

## Related Pages

- [Statistics](../profiling/statistics.md)
- [How Profiling Works](../profiling/how_it_works.md)
- [Data Timeliness – How It Works](../data_timeliness/how_it_works.md)
- [Data Validation – How It Works](../data_validation/how_it_works.md)

---
