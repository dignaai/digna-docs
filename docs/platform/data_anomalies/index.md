---
title: digna Data Anomalies | AI-Powered Observability of Data
description: digna Data Anomalies is part of the digna Data Observability Platform. It automatically learns patterns in your data and detects anomalies to improve the quality of data and observability across databases, data lakes, and warehouses.
tags:
  - data quality
  - data observability
  - quality of data
  - observability of data
  - AI-driven monitoring
  - anomaly detection
  - digna
  - digna platform
hide:
  - toc                # optional: hide the small top-level TOC if you use inline nav
  - navigation         # optional: hide side navigation for standalone pages
image: /assets/logo_square.png
---


# digna Data Anomalies – AI-Based Detection of Data Quality Issues

**AI-powered observability for always-on data trust**

digna Data Anomalies is part of the **digna Data Observability Platform** — a modular solution that improves the **quality of data** by continuously analyzing how datasets behave over time.

It automatically learns what “normal” looks like for your data and alerts you when behavior changes — without defining static thresholds or writing a single rule.  
The module runs directly inside your database, so data never leaves your environment.

---

## Purpose of digna Data Anomalies

The **digna Data Anomalies** module provides continuous **observability of data** by calculating and tracking predefined statistical metrics such as:

- Data volume and record counts  
- Missing value ratios  
- Value distributions and histograms  
- Numeric ranges and averages  
- Column uniqueness and text length  

These metrics are collected automatically for every dataset.  
Using them, digna builds models that represent the typical behavior of each metric — learning daily, weekly, or seasonal patterns.  
Once trained, the module predicts expected values for new data and detects deviations that may indicate quality issues, process failures, or upstream changes.

---

## Key capabilities

- Learns expected data behavior automatically using AI — no configuration of thresholds.  
- Detects sudden drops, spikes, or drifts in data volume and distributions.  
- Identifies swapped columns or incorrect mappings between attributes.  
- Highlights unexpected categorical values (e.g., new regions or codes).  
- Supports all column types: numerical, categorical, or unspecified.  
- Operates entirely in the customer environment — no data movement.  
- Integrates with **digna Data Analytics** for long-term trend analysis.

---

## How it works

### Step 1 – Metric calculation
digna computes a set of profile metrics for each table and column.  
These metrics describe the structure and statistical behavior of your data and are stored for further analysis.

### Step 2 – Model training
Based on historical metric values, digna trains compact machine-learning models (signature models) that capture the normal range of each metric.

### Step 3 – Automatic thresholding
Using *conformal inference*, digna calculates adaptive confidence intervals (auto-thresholds) that evolve with your data.  
If new metric values fall outside the predicted range, they are flagged as anomalies.

This continuous feedback loop ensures that monitoring stays relevant even when data volumes or patterns naturally grow.

---

## Example scenarios

### Unexpected drop in record volume
A dataset typically contains around 500 000 records per day.  
When a new delivery includes only 50 000 records, digna flags an anomaly and shows how far the value deviates from its learned range.

### Swapped columns detected
The average string length of `last_name` suddenly matches that of `first_name`.  
digna recognizes the deviation in metric patterns and signals a potential column swap.

### Unexpected category detected
A column listing Austrian cities suddenly contains “Zurich”.  
Based on historical distributions, digna marks the new value as unexpected and alerts the user.

---

## Integration with other modules

- **digna Data Analytics** — aggregates anomaly history and volatility metrics to reveal long-term trends.  
- **digna Data Validation** — enforces explicit business rules for deterministic quality checks.  
- **digna Data Timeliness** — monitors arrival times of data and correlates delays with anomaly occurrences.  
- **digna Data Schema Tracker** — detects structural changes that may explain new anomalies.

---

## Typical use cases

- Detecting missing or duplicate data loads.  
- Identifying swapped or truncated columns.  
- Detecting distribution drift in numeric or categorical features.  
- Finding unexpected reference values or codes.  
- Monitoring continuous ingestion pipelines for irregularities.  
- Tracking the overall **quality and observability of data** across domains.

---

## Benefits

- Immediate detection of abnormal data behavior.  
- Eliminates manual threshold tuning.  
- Reduces operational effort for large data environments.  
- Builds confidence in analytics and reporting systems.  
- Strengthens the **quality of data** and end-to-end **data observability**.

---

## Related digna Modules

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trend and volatility metrics.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — rule-based data verification.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — monitoring data delivery schedules.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — schema change detection.

---

## Summary

The **digna Data Anomalies** module forms the core of digna’s AI-driven **Data Observability Platform**.  
By continuously monitoring key metrics, learning patterns, and identifying deviations, it helps organizations ensure that the **quality of data** remains trustworthy, stable, and explainable — without manual configuration.
