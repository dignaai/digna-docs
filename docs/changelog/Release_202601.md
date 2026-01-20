---
title: digna Release 2026.01 | Logical Datasources, Global Connections & Advanced Data Validation
description: Learn what’s new in digna Release 2026.01. This version introduces global database connections, logical datasources, anomaly relevance conditions, CSV exports, and advanced data validation including referential integrity checks.
keywords: digna Release 2026.01, digna changelog, digna datasource, digna database connections, digna Data Anomalies, digna Data Validation, referential integrity validation, data quality rules, data observability, digna CSV export
image: /assets/logo_square.png
---

# Changelog – Release 2026.01  

With Release 2026.01, digna introduces major improvements to datasource modeling, connection management, and inspection usability.  
This release enhances flexibility across all modules and significantly extends **data quality and validation coverage**.

---

## 🚀 New Features  

### Global Database Connections  
- Database connections are now configured on a **global level**.  
- Global connections can be reused across **all projects**, simplifying configuration and maintenance.  
- **Impact:** Reduces operational overhead and ensures consistent connectivity across environments.

### Multiple Source Connections per Project  
- Projects can now reference **multiple source connection configurations**.  
- Enables more flexible setups for complex data landscapes project.  
- **Impact:** Supports realistic enterprise architectures with heterogeneous data sources.

### Logical Datasources  
- Datasources now represent a **logical layer** within a project.  
- Each datasource can be backed by:
   - a **database table**
   - a **database view**
   - a **custom SQL statement**  
- This separation improves reuse, clarity, and inspection modeling across modules.  
- **Impact:** Decouples inspections and data quality rules from physical storage, improving maintainability and reuse.

### Anomaly Relevance Condition  
- An **Anomaly Relevance Condition** can now be defined to control anomaly status evaluation on level of dataset.  
- Statistics are calculated independently of whether the condition is set or met.  
- If the condition is **not met**, **digna Data Anomalies** does not provide anomaly status (green / yellow / red).  
- **Example:** Exclude the dataset from anomaly evaluation when the record count is below 10.
- **Impact:** Ensures anomalies are evaluated only in relevant business contexts.

### Per-Module Notification Configuration  
- Notifications can now be configured **per module** directly in digna.  
- Allows independent control of alerting behavior for **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation**, and other modules.  
- **Impact:** Enables precise alerting strategies aligned with team responsibilities and criticality.

### Inspection Results Export (CSV)  
- Users can now **download inspection results as CSV files**.  
- Enables offline analysis, reporting, and integration with external tools.  
- **Impact:** Simplifies audits, reporting, and downstream data quality analysis.

---

## 🧪 Extended Data Validation Capabilities  

With this release, **digna Data Validation** now supports a comprehensive set of data quality rules:

- **Row-level validation rules**  
- **Multi-column uniqueness checks**  
- **Referential integrity validation across datasources**

Together, these checks enable enforcement of **structural and relational data quality rules** across complex data landscapes.

### Uniqueness Checks for Multiple Columns
- Introduced **Uniqueness Checks** for a configurable **set of columns**.  
- Enables validation of compound keys and business-level uniqueness constraints.  
- **Impact:** Detects duplicate business entities that cannot be identified with single-column checks.

### Referential Integrity Checks
- Introduced **Referential Integrity Checks** to validate relationships between datasources.  
- Ensures that **foreign key values** in a source datasource exist in a referenced target datasource.  
- Supports validation across:
  - different tables or views  
  - different schemas  
  - different database connections within the same project  
- Helps detect orphaned records, broken relationships, and data consistency issues early.  
- Designed to work with **logical datasources**, including views and custom SQL.  
- **Use cases:** data warehouse integrity, regulatory reporting, master data consistency, and reliable downstream analytics.

---

## 🎯 Who Benefits from This Release  

- **Data Engineers:** More flexible datasource modeling and reusable database connections  
- **Data Quality & Governance Teams:** Expanded validation coverage including relational integrity rules  
- **Analytics & BI Teams:** Cleaner inputs and exportable inspection results  
- **Platform Owners:** Reduced configuration complexity and improved operational maintainability

---

## 🛠 CLI Updates  
- No changes

---
