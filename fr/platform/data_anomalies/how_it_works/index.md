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

The model is a **robust regression** fitted to the history of that series. It always carries an intercept and a level-shift term for each detected structural break; beyond that, it selects its own structure from a set of candidates — a linear trend, the previous one or two observations, weekday effects, within-month and within-year seasonality, and month-boundary spikes.

Candidates are admitted only when the data genuinely supports them, so a series with no weekly pattern does not get weekday terms, and a short series does not get seasonality at all. Below five usable observations no model is fitted and the median is used instead.

Robustness is what keeps a single bad day from poisoning the following ones: observations are reweighted across several passes, so a spike is downweighted rather than fitted, and a downweighted observation can be replaced by its fitted value before it becomes the *previous observation* of the next prediction.

Up to two structural breaks may be absorbed. That is what lets the model follow a genuine step change — a migration, a new source system, a business change — instead of averaging across it indefinitely.

See [Anomaly Tuning](../reference/tuning.md) for the seven dials that shape this.

---

## Step 3 – The Tolerance Band

digna does not compare the observation to the prediction directly. It compares it against a band derived from **how wrong recent predictions have been on this very series**:

```
bound  =  multiplier  ×  weighted mean absolute error of recent predictions
```

- The **multiplier** comes from [Sensitivity](../reference/tuning.md#sensitivity) — a tail probability from 1 % to 10 %.
- The **weighting** comes from [Memory](../reference/tuning.md#memory) — flat, linear decay, or quadratic decay over a rolling window of just over a year.

This is why a genuinely noisy series is not permanently red: its band is wide because its predictions have genuinely been that wrong. A precise series gets a narrow band, and a real deviation on it is caught early.

### Clamps

Four optional limits on the statistic mapping constrain the result:

| Setting | Applied to |
|---|---|
| `min_threshold` / `max_threshold` | The **width** of the bound |
| `lower_limit` / `upper_limit` | The **prediction and its bands** |

In addition, statistics that cannot be negative have their whole band floored at zero — a count is never predicted to go below zero. Only **Sum** and **Average** are exempt, because they legitimately can.

---

## Step 4 – Status and Rollup

The band gives four edges, and the observation falls into one of five regions:

| Observed value | Status |
|---|---|
| Below `predicted − 2 × bound` | **Failed** |
| Between `−2 ×` and `−1 × bound` | **Uncertain** |
| Within `± 1 × bound` | **Passed** |
| Between `+1 ×` and `+2 × bound` | **Uncertain** |
| Above `predicted + 2 × bound` | **Failed** |

Statuses then roll up — **check → attribute → dataset → data source** — with the worst status winning at each level, alongside the count of checks that passed, were uncertain, and failed.

Checks whose mapping has anomaly detection switched off are excluded from the rollup entirely, which is what makes disabling a noisy statistic effective rather than merely cosmetic.

---

## What Is Stored

For every check and every inspection date, digna records the observed value, the predicted value, all four band edges, and the resulting status. Nothing about a finding has to be reconstructed later — the expectation it was judged against is stored beside it.

Re-inspecting a date is safe: an inspection cleans up its own previous results for that date range before writing new ones, so a data source can be re-run without duplicating history.

---

## Related Pages

- [Data Anomalies – Introduction](Introduction.md)
- [Data Anomalies – Use Cases](use_cases.md)
- [Profiling – The Foundation](../profiling/Introduction.md)
- [Statistics](../profiling/statistics.md)
- [Datasets](../profiling/datasets.md)
- [Anomaly Tuning](../reference/tuning.md)
- [Statuses and Alerts](../reference/statuses.md)

---