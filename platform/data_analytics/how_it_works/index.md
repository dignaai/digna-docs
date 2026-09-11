# Data Analytics – How It Works

---

## The Idea

[Data Anomalies](../data_anomalies/how_it_works.md) asks whether *today* deviates from expectation. **Data Analytics asks what the last N observations, taken together, are doing** — and answers it with a straight line fitted through them.

Two properties of that line matter:

- Its **slope** is the trend — where the metric is heading.
- The **scatter around it** is the volatility — how consistently it gets there.

Both are computed from statistics [profiling](../profiling/Introduction.md) has already collected, so the module adds analytical depth without a second pass over your data.

---

## Defining an Analytics Rule

A rule names four things:

| Part | Meaning |
|---|---|
| **The series** | Which table, column, and statistic to analyse |
| **The metric** | Absolute change, relative change, absolute volatility, or relative volatility |
| **The window** | A range and a unit — how much history the line is fitted through |
| **The limits** | Optional lower and upper bounds on the resulting value |

### Window units

| Unit | Meaning |
|---|---|
| **DAY** | The last *N* days |
| **WEEK** | The last *N* weeks |
| **MONTH** | The last *N* months |
| **OBSERVATION** | The last *N* observations, whenever they happened |

**OBSERVATION** is the one to use for irregular series. A monthly delivery analysed over "the last 30 days" has one or two points; analysed over "the last 12 observations" it has a year of behaviour. Calendar units are the better choice when the *rate* matters — a source whose delivery frequency itself is changing tells you more per day than per observation.

---

## The Four Metrics

A regression is fitted with time on the x-axis, scaled so the window spans the unit interval. That scaling is what makes the metrics comparable: a slope is expressed **per window**, not per second, so the same limit means the same thing on a 30-day and a 90-day rule.

| Metric | Definition | Reads as |
|---|---|---|
| **Absolute Change** | The slope of the fitted line | How much the metric moves across the window, in its own units |
| **Relative Change** | Slope ÷ intercept, as a percentage | The same movement as a percentage of where the window started |
| **Absolute Volatility** | Mean absolute deviation from the fitted line | Typical distance between observation and trend, in the metric's own units |
| **Relative Volatility** | That deviation ÷ the mean of the series, as a percentage | Scatter as a percentage of the typical level |

### Choosing absolute or relative

**Relative** metrics are what you want in almost every case where series are compared or one rule is applied across many columns — a 5 % drift means the same thing on a table of 500 rows and one of 5 million. **Absolute** metrics are right when the quantity itself has meaning: "this null count must not grow by more than 100 per month" is an absolute statement, and expressing it as a percentage would be an awkward way to say it.

Relative metrics are guarded against a near-zero denominator: when the intercept, or the mean of the series, is effectively zero, the relative value is reported as zero rather than exploding. A metric that spends time near zero should be monitored with its absolute counterpart.

---

## Evaluation

Each computed value is compared against the rule's limits:

| Condition | Status |
|---|---|
| Below the lower limit, or above the upper limit | **Failed** |
| Otherwise | **Passed** |

A limit left empty is simply not evaluated, so a rule with neither limit set records the value and never fails. That is a legitimate configuration — it gives you the trend series in the interface without alerting on it, which is a good way to observe a metric's normal range before deciding what the limit should be.

There is no Uncertain status here. Unlike anomaly detection, whose band is learned and therefore has a natural inner and outer edge, an analytics limit is a line a person drew.

Statuses roll up the same way as everywhere else — **check → attribute → dataset → data source**, worst result winning.

---

## Practical Setup

1. **Create the rule with no limits.** Let it run for a few weeks and watch what the metric actually does on your data.
2. **Set the limit outside the observed range**, not at the edge of it. A limit set to the highest value you have seen will fire on the next ordinary week.
3. **Prefer one-sided limits where only one direction is a problem.** A rising null rate is a defect; a falling one is a fix, and does not need an alert.
4. **Use volatility for pipeline health, trend for data health.** Rising volatility on a stable metric is usually an infrastructure story — retries, contention, an unreliable upstream job. A moving trend is usually a data or business story.

!!! tip "Read the two together"
    Flat trend with rising volatility means instability, not change. A moving trend with low volatility is an orderly change — growth, a migration, a decommissioning. A moving trend *and* rising volatility is usually a defect: partial loads, duplicated batches, a source in transition.

---

## Related Pages

- [Data Analytics – Introduction](Introduction.md)
- [Data Analytics – Use Cases](use_cases.md)
- [Profiling – The Foundation](../profiling/Introduction.md)
- [Statistics](../profiling/statistics.md)

---