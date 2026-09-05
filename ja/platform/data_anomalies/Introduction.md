# Data Anomalies – Automated Detection
<h1 style="display:none;">AI駆動のデータ品質と可観測性モジュール – digna Data Anomalies</h1>

---

## Purpose

The **Data Anomalies** module identifies irregularities in your datasets automatically — no rule writing required.  
It continuously monitors  **the quality of data delivery**, learning what “normal” looks like and detecting deviations in real time.

By using AI-based detection, digna recognises *silent data errors* such as missing, duplicated, or corrupted records that can distort reports, ML models, and dashboards.

---

## Technical Overview

### Metrics analyzed

digna continuously profiles the following aspects of your data:

- **Record volume** – total number of rows, daily or batch-based  
- **Missing values** – detection of null or empty fields  
- **Distributions and histograms** – monitoring shape changes in data  
- **Value ranges** – automatic identification of out-of-range or extreme values  
- **Uniqueness** – checks for duplicate keys or repeated entries  

### Intelligent anomaly detection

- Uses **historical learning** to dynamically define expected boundaries  
- Detects deviations in **volume, value distributions, or logical relationships**  
- Employs AI to adapt thresholds automatically based on time-of-day or seasonal patterns  
- Differentiates between **statistical fluctuations** and true anomalies  
- Produces detailed metrics and confidence scores per dataset and column  

---

## Detection Scenarios

Below are examples of real-world problems automatically caught by the **Data Anomalies** module:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Missing half of daily transactions, duplicated batch loads, or sudden data surges |
| **Missing or null values** | Data extractions completed but critical columns left empty |
| **Distribution drifts** | Average purchase amount or transaction count per region changes unexpectedly |
| **Column swaps** | Columns like *first_name* and *last_name* accidentally switched during ETL |
| **Unexpected categorical values** | e.g., “Zurich” appears under Austrian city list |
| **Sudden uniqueness loss** | Previously unique IDs start duplicating due to upstream join errors |

---

## Architecture and Execution

- **In-database execution:** All anomaly detection logic is executed *inside the database engine* (Teradata, Snowflake, Databricks, PostgreSQL, etc.)  
- **No data movement:** digna reads only metrics, never transfers raw data externally  
- **Incremental updates:** Only new data segments are analyzed each run for efficiency  
- **Configurable inspection frequency:** Hourly, daily, or triggered by upstream processes  
- **Result storage:** Metrics and anomaly flags are written back to digna’s observability schema for visualization and alerting  

---

## Benefits

| Area | Benefit |
|------|----------|
| **Automation** | Eliminates hundreds of manual SQL or rule definitions |
| **Precision** | Detects issues that static thresholds often miss |
| **Scalability** | Monitors millions of records per table efficiently |
| **Integration** | Works seamlessly with *digna Data Analytics* for trend analysis |
| **Compliance** | Ensures continuous control over the **quality and observability of data** |
| **Transparency** | Provides confidence scores, timestamps, and reason codes for every anomaly |

---

## How digna Learns “Normal”

1. **Profiling phase:** digna collects metrics from historical datasets.  
2. **Learning phase:** AI models identify recurring patterns (seasonal, weekly, daily).  
3. **Monitoring phase:** Future datasets are compared against dynamically learned thresholds.  
4. **Alerting phase:** Deviations beyond statistical confidence boundaries are raised as anomalies.  

All models are explainable, deterministic, and optimized for enterprise data volumes.

---

## Example Use Cases

- Monitoring data quality in **banking transaction systems**  
- Detecting load failures in **ETL or data warehouse jobs**  
- Identifying abnormal customer activity in **telecommunication records**  
- Observing clinical data consistency in **healthcare analytics pipelines**  
- Preventing broken dashboards in **BI and reporting environments**

---

## Frequently Asked Questions

**Does Data Anomalies require predefined rules?**  
No — the module learns from data behavior automatically.

**Can I still define specific thresholds if needed?**  
Yes. digna allows combining AI-based and rule-based detection (via *Data Validation*).

**How are false positives minimized?**  
The module uses adaptive learning and statistical confidence scoring to ignore normal seasonal variations.

**Where does computation happen?**  
All processing runs within your database — digna never extracts raw data.

**Is it suitable for sensitive or regulated data?**  
Yes. digna runs fully **on-premises or in private cloud** and adheres to European compliance standards.

---