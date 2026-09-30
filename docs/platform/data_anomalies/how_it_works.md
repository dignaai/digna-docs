---
title: Data Anomalies – How It Works | digna Documentation
description: How digna Data Anomalies works end to end — in-database profiling, a prediction per series that weighs competing explanations, a tolerance band derived from recent prediction error, status rollup from check to data source, and anomaly notifications.
image: /assets/logo_square.png
keywords:
  - anomaly detection how it works
  - data profiling
  - prediction model
  - tolerance band
  - conformal thresholds
  - in-database execution
  - quality of data
  - observability of data
  - digna data anomalies
lang: en
robots: index, follow
og_title: Data Anomalies – How It Works | digna Documentation
og_description: The mechanics of digna Data Anomalies — profiling, prediction, tolerance bands, and status rollup.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Anomalies – How It Works

---

## The Pipeline

Each inspection runs the same four steps for every data source:

```
1. Profile     measure the enabled statistics, in-database
2. Predict     fit a model per series and predict the current value
3. Bound       derive a tolerance from how wrong recent predictions were
4. Status      compare, then roll the result up to the data source
```

---

## Step 1 – Profiling

Profiling is what produces the numbers this module reasons about. digna builds a snapshot of the data source, applies each dataset's filter and grouping expressions, and computes every enabled statistic as an aggregate — inside your database, with only the aggregated results coming back.

*Data Anomalies* adds nothing to this step and reads nothing else. Every finding it produces is a statement about a statistic that profiling measured, which is why **the statistics you enable determine what this module is able to see**.

See [How Profiling Works](../profiling/how_it_works.md) for the mechanics, including the snapshot filter, the `#date#` marker, work tables, and query modes.

---

## Step 2 – Prediction

Every combination of dataset, column, and statistic is its own time series, and each gets its own model.

The model reads a series the way a person reading its chart would: it holds **several competing explanations** of the history at once and weighs them against each other. Each explanation combines a *pattern* — a level, a trend, weekly, monthly and yearly calendar effects, settled shifts of level, cycles, days of the month that stand out — with a reading of the *most recent observations*: nothing changed and the odd values are outliers, the level jumped, the trend turned, an episode that is now over, a spike that is fading, a level that wanders.

Every explanation is scored by how well it accounts for the observations, and the prediction is the blend of their forecasts, each weighted by how strongly it is supported. Explanations are admitted only when the data genuinely supports them, so a series with no weekly pattern does not get weekday effects, and a simple series is not made to look complicated.

No explanation predicts from the previous observations directly, which is what keeps a single bad day from poisoning the following ones: a single extreme value stays an outlier, however far off it is, and does not drag the prediction after it.

A **structural break** — a genuine step change such as a migration, a new source system, or a business change — is one of the explanations. Once the evidence for it is strong enough, the model predicts from the new level or slope instead of averaging across the change; until then, it hedges and moves over gradually.

### Model Settings {: #model-settings }

Release 2026.06 opens the model up to configuration. Two settings on the data source's **Model** tab steer the prediction. Both run from `0.0` to `1.0`, and `0.5` is the default the model is tuned at:

| Setting | Effect |
|---|---|
| **Break Sensitivity** | How quickly a fundamental change — a jump to a new level, or a trend that sets in or turns — is believed rather than treated as outliers. Higher believes a change after fewer observations: a clear change takes about seven observations at `0.0`, about three at `0.5`, and one or two at `1.0`. A smaller change, or a change of slope, takes longer to show. |
| **Model Complexity** | How much structure the model looks for, from a glance to a careful study. Lower sticks to a level, a trend, the calendar, a single shift of level and the recent observations. Higher also considers rarer explanations — a cycle the calendar does not know, a change of slope, days of the month that stand out, totals that reset monthly, several shifts of level — and each needs less evidence to be believed. Higher settings take longer to compute. |

Both settings act only on how much an explanation is believed, so the prediction changes gradually as either is turned. Every other quantity the model uses is fixed. The defaults suit the great majority of series, and **Restore Defaults** returns both settings to `0.5` at any time.

---

## Step 3 – The Tolerance Band

digna does not compare the observation to the prediction directly. It compares it against a tolerance band derived from **how wrong recent predictions have been on this very series** — recent errors weighted so that newer ones count for more.

This is why a genuinely noisy series is not permanently red: its band is wide because its predictions have genuinely been that wrong. A precise series gets a narrow band, and a real deviation on it is caught early.

Two settings on the data source's **Thresholds** tab adjust the band:

| Setting | Effect |
|---|---|
| **Sensitivity** | How far an observation may stray before it is reported. Higher reports smaller deviations. |
| **Memory** | How far back the errors behind the band still count. Longer remembers more history. |

Both default to **Moderate**, and both can be restored to their defaults at any time.

### Clamps

Four optional limits on the statistic mapping constrain the result:

| Setting | Applied to |
|---|---|
| `min_threshold` / `max_threshold` | The **width** of the bound |
| `lower_limit` / `upper_limit` | The **prediction and its bands** |

In addition, statistics that cannot be negative have their whole band floored at zero — a count is never predicted to go below zero. Only **Sum** and **Average** are exempt, because they legitimately can.

---

## Step 4 – Status and Rollup

The observation is compared against the band and reported as one of three statuses:

| Observation | Status |
|---|---|
| Within the expected band | **Passed** |
| Outside it, but not far outside | **Uncertain** |
| Well outside it | **Failed** |

**Uncertain** is what makes continuous monitoring usable. Without a middle state every tolerance is a cliff edge, and a metric one unit past the line reads the same as one that collapsed.

Statuses then roll up — **check → attribute → dataset → data source** — with the worst status winning at each level, alongside the count of checks that passed, were uncertain, and failed.

Checks whose mapping has anomaly detection switched off are excluded from the rollup entirely, which is what makes disabling a noisy statistic effective rather than merely cosmetic.

---

## Notifications

When a data source's anomaly status is **Failed**, digna notifies every subscription that covers the data source through its notification channel (Email, Slack or Jira). The message lists the failed checks and links straight to them on the data source's inspection page.

Two settings on the data source's **Notifications** tab decide when such a notification is sent:

| Setting | Effect | Default |
|---|---|---|
| **Minimum Alerts** | How many **Failed** checks an inspection date needs before a notification is sent — **Uncertain** checks do not count. Higher values hold back isolated deviations. At least `1`. | `1` — every failed inspection notifies |
| **Pause After Notification (Days)** | After a notification, how many inspection dates the same subscription stays silent about this data source, so a persisting anomaly is not reported over and over. | `0` — never pauses |

Both apply to data anomaly notifications only, and **Restore Defaults** returns them to their defaults. Which modules a subscription notifies about, and whether it also reports passed inspections and inspection errors, is set on the subscription itself.

---

## What Is Stored

For every check and every inspection date, digna records the observed value, the predicted value, the band it was judged against, and the resulting status. Nothing about a finding has to be reconstructed later — the expectation it was judged against is stored beside it.

Re-inspecting a date is safe: an inspection cleans up its own previous results for that date range before writing new ones, so a data source can be re-run without duplicating history.

---

## Related Pages

- [Data Anomalies – Introduction](Introduction.md)
- [Data Anomalies – Use Cases](use_cases.md)
- [Profiling – The Foundation](../profiling/Introduction.md)
- [Statistics](../profiling/statistics.md)
- [Datasets](../profiling/datasets.md)

---
