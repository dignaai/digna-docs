# *digna* Modules — Technical Overview

*digna* is an AI-powered **Data Quality & Observability Platform** designed for **in-database execution**.  
It operates directly inside your data environment and ensures **trust in your data** — without requiring manual rule coding or data movement.

By combining automated anomaly detection, rule-based validation, and data structure monitoring, digna continuously improves both **data quality** and **observability of data pipelines**.

---

## Module Summary

| Module | Focus Area | Key Capabilities |
|--------|-------------|------------------|
| **Data Anomalies** | Automated anomaly detection | Learns “normal” data behavior, detects deviations in **volume, distribution, or value patterns**, and flags abnormal data movement or gaps |
| **Data Analytics** | Trends & volatility | Analyzes long-term **metrics, stability, and change patterns** to detect drifts in data quality over time |
| **Data Validation** | Rule-based checks | Enforces **exact values, ranges, thresholds, or reference lists** — with full audit trail and reproducibility |
| **Timeliness** | Delivery monitoring | Uses AI-learned **expected arrival times** and user-defined schedules to detect **late or missing data** |
| **Schema Tracker** | Structural monitoring | Detects **schema drift**, such as new or removed columns, renamed fields, or datatype changes |
| **[Data Reconciliation](data_reconciliation/Introduction.md)** | Source-to-target consistency | Compares a target with the data sources it was built from — **exact rules** for known controls, **AI rules** for complex flows such as ETL processes |
| **[digna Agentic](agentic/Introduction.md)** | AI agents | Lets Claude and other AI agents **answer business questions**, investigate alerts and configure digna through the **digna MCP Server** |

---

## How the Modules Work Together

Each digna module addresses a specific dimension of the **quality of data** and **observability of data systems**, yet they integrate seamlessly into a single platform.  

- **Data Anomalies** and **Data Analytics** provide AI-driven insights and trend awareness.  
- **Data Validation** ensures correctness through rule enforcement.  
- **Timeliness** safeguards data delivery and freshness.  
- **Schema Tracker** protects structure and metadata integrity.  
- **Data Reconciliation** confirms that data arrived completely between systems.  
- **digna Agentic** opens all of the above to AI agents — see [Connect an AI Agent](agentic/connect_ai_agent.md).  

By default, all modules profile data in the source database. A database connection can instead use the [digna Engine](profiling/profiling_location.md).

Together, they create a complete **Data Observability and Quality Control Framework** operating entirely within your environment — **on-premises or private cloud**.

---

## Benefits of the Modular Approach

- **Scalable** – start with one module and expand as needed  
- **Unified Interface** – same UI and API for all modules  
- **AI-Assisted Configuration** – minimal setup effort, fast onboarding  
- **Cross-Module Insights** – detect relationships between timeliness, schema drift, and anomalies  
- **Enterprise Integration** – works with Teradata, Snowflake, Databricks, and other enterprise data platforms  

---

**digna** delivers a **modular, AI-driven framework for Data Quality and Data Observability** —  
built in Europe for organizations that demand **data sovereignty**, **performance**, and **trust**.  
All modules work together to provide complete visibility into your data ecosystem, ensuring that every insight is **accurate, explainable, and reliable**.

---

## Frequently Asked Questions

**Do I need all modules to start?**  
No — each module can be licensed and deployed independently. 

**How does digna detect anomalies?**  
Through AI models that learn from historical patterns in data volume, distribution, and value ranges.

**Can digna validate both technical and business rules?**  
Yes — the Data Validation module supports both types of checks with audit-ready reports.

**Does digna require external services or SaaS?**  
No. All digna modules operate inside your own infrastructure for full data control and compliance.

---
