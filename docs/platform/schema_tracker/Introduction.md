---
title: Data Schema Tracker – Monitor Schema Evolution | digna Documentation
description: Learn how digna Data Schema Tracker monitors column changes, datatype updates, and schema drift. Detect and alert on both intentional and unintentional schema changes to prevent ETL failures, broken dashboards, and loss of data observability.
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - data schema tracker
  - schema drift detection
  - schema evolution monitoring
  - metadata observability
  - data observability
  - quality of data
  - data structure monitoring
  - database metadata
  - etl pipeline stability
  - digna data schema tracker
lang: en
robots: index, follow
og_title: Data Schema Tracker – Monitor Schema Evolution | digna Documentation
og_description: digna Data Schema Tracker monitors schema drift, datatype changes, and column updates. Receive alerts before ETL pipelines or dashboards fail due to unexpected structure changes.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Monitor Schema Evolution
<h1 style="display:none;">AI-Driven Module for Metadata Observability and Data Quality – digna Data Schema Tracker</h1>

---

## Purpose

The **Data Schema Tracker** keeps you informed about how your database structures evolve.  
It continuously monitors **table schemas, columns, and datatypes** to detect **schema drift** — intentional or unintentional structural changes that can disrupt pipelines, ETL jobs, or BI dashboards.

By ensuring transparency in schema evolution, digna helps organizations maintain **trust in the quality of data**, uphold **observability of data systems**, and avoid costly production incidents caused by undetected schema changes.

---

## Technical Overview

### What It Monitors

- **Added or Removed Columns** – Detects newly introduced, renamed, or deleted columns.  
- **Datatype Modifications** – Identifies changes such as `INT → VARCHAR` or `DATE → TIMESTAMP`.  
- **Table and View Modifications** – Tracks creation, renaming, or removal of tables and views.  
- **Cross-Environment Differences** – Compares schema versions between Dev, Test, and Production environments.  

### Detection & Alerting

- Scans **database metadata** or **system catalogs** directly within your data platform.  
- Compares each schema snapshot with the previously known version stored in digna’s observability schema.  
- Generates **real-time alerts** in the dashboard, via API, or external notification channels (email, Slack, webhook).  
- Logs every schema version for **historical tracking and audit readiness**.

---

## Architecture and Execution

- **In-Database Execution:** digna runs entirely within your environment, querying metadata views without extracting any data.  
- **Lightweight Scanning:** accesses only structural information — never user data.  
- **Centralized Storage:** schema metadata and drift records are stored in the digna observability schema for visualization and analytics.  
- **Automation:** supports scheduled or event-based scans via digna Core or external orchestration tools.  

---

## Example Use Cases

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Detect upstream structure changes before pipelines fail due to schema mismatches. |
| **Business Intelligence Reliability** | Prevent broken dashboards caused by renamed or missing columns. |
| **Data Warehouse Governance** | Maintain an auditable history of schema evolution for compliance and impact analysis. |
| **Integration Oversight** | Ensure that data lake and warehouse schemas remain synchronized after structural updates. |

---

## Benefits

| Area | Benefit |
|------|----------|
| **Data Quality** | Prevents undetected schema drift that can corrupt or invalidate data pipelines. |
| **Observability** | Adds structural monitoring to the overall observability of data ecosystems. |
| **Compliance** | Maintains versioned schema history for audit, traceability, and change control. |
| **Prevention** | Detects structural issues before they cascade into reporting or production errors. |

---

## How It Works

1. **Snapshot Collection** – digna captures the current schema metadata.  
2. **Comparison** – the new snapshot is compared
