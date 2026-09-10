# Data Analytics – Use Cases

---

## When to Reach for This Module

[*Data Anomalies*](../data_anomalies/Introduction.md) answers *"is today unusual?"*. **Data Analytics answers the questions that only make sense over a longer window:**

- Is this metric **trending** in a direction nobody decided on?
- Has this pipeline become **more volatile** than it used to be, even though no single day looks wrong?
- Which parts of the estate are **stable**, and which need attention first?

It calculates higher-level statistics — **trend** and **volatility** — on the core column statistics *digna* already collects: record counts, missing values, min, max, sum, average, and the rest. Nothing extra needs to be configured on the data source; the analytical layer sits on metrics that exist as soon as profiling runs.

The result is **one view for data health and for business and operational KPIs**, which is why the module is aimed at data owners, analysts, and decision-makers rather than only at the engineering team.

---

## Banking and Financial Services

### Volume patterns across departments

Every department loads into the same warehouse, and every department is convinced its own volumes are fine. Trend analysis over record counts makes the comparison objective: which sources are growing, which are flat, and which have been quietly shrinking for six weeks.

### Financial KPI fluctuation

Sums and averages of monetary columns — exposure, provisions, fee income, transaction value — are tracked the same way as quality metrics. A rising **volatility** score on a KPI that used to be steady is an early signal, both for the business and for the team that suspects an upstream process has changed.

### Distinguishing seasonality from decay

Month-end and quarter-end peaks are normal in finance. What matters is whether the *baseline between peaks* is moving. Separating trend from volatility makes that visible instead of leaving it buried under the peaks.

---

## Retail and E-Commerce

### Rising NULL rates after a migration

A platform migration completes and everything passes. Weeks later, the missing-value rate on a handful of columns has climbed steadily from near zero. No single day crossed a threshold; the **trend** is the finding.

### Sales trends and top-performing SKUs

The same statistics that guard data quality also describe the business. Sum and average over order-value columns, sliced by product group or channel, expose which SKUs are carrying growth and which are declining — from the warehouse, without exporting anything to a separate analytics tool.

### Stability comparison between periods

Comparing a promotional period against a normal one shows whether the pipeline coped. High volatility during a peak that did not exist the year before usually means a capacity or scheduling problem, not a demand story.

---

## Healthcare

- **Completeness decay in clinical datasets** — a diagnosis or outcome field whose missing-value ratio creeps upward across releases points at a feeder system that changed, not at a single bad load.
- **Long-horizon comparability** — before a dataset is used for research or reporting across several years, trend and volatility over its key metrics show whether the series is actually comparable end to end.

---

## Telecommunications

- **Network and usage metrics** carry heavy seasonality; volatility scoring separates *noisy but healthy* sources from ones that have genuinely destabilised.
- **Per-region and per-product trends** built on filtered subsets keep a shrinking region visible instead of averaged away in the national figure.
- **Capacity planning** benefits from the same trend series that quality monitoring produces — record-count growth per source is a free by-product of profiling.

---

## Public Sector

- **Register growth and processing backlogs** are naturally slow-moving; trend is the appropriate lens, and the stored metric history provides the evidence trail an audit expects.
- **Cross-agency data sharing** works better when both sides can point at the same stability record for a dataset instead of exchanging assurances.

---

## Reading Trend and Volatility Together

| Trend | Volatility | Typical interpretation |
|---|---|---|
| Flat | Low | Healthy, stable source — safe to monitor lightly |
| Flat | **Rising** | Process instability: retries, contention, an unreliable upstream job |
| **Rising / falling** | Low | A real, orderly change — business growth, decommissioning, a migration |
| **Rising / falling** | **Rising** | Usually a defect: partial loads, duplicated batches, a source in transition |

!!! tip "Configure alerts where the trend matters"
    Flexible alert configuration means you can route trend and volatility findings differently from day-to-day anomalies — a gradual decay rarely needs a night-time page, but it does need to reach the data owner.

---

## Where This Module Fits

*Data Analytics* is the interpretive layer over [*Data Anomalies*](../data_anomalies/Introduction.md). Anomalies tell you a delivery deviated; analytics tells you whether that deviation is an isolated event, the newest point on a trend, or a symptom of a source that has become unstable.

---

## Related Pages

- [Data Analytics – Introduction](Introduction.md)
- [Data Analytics – How It Works](how_it_works.md)
- [Data Anomalies – Use Cases](../data_anomalies/use_cases.md)
- [digna Modules – Technical Overview](../overview.md)

---