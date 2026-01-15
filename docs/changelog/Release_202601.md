---
title: digna Release 2026.01 | Logical Datasources, Global Connections, CSV Export
description: Learn what’s new in digna Release 2026.01. This version introduces global database connections, logical datasources, anomaly relevance conditions, CSV exports, and enhanced data validation checks.
keywords: digna Release 2026.01, digna changelog, digna datasource, digna database connections, digna Data Anomalies, digna Data Validation, digna CSV export, digna notifications
image: /assets/logo_square.png
---

# Changelog – Release 2026.01  

With Release 2026.01, digna introduces major improvements to datasource modeling, connection management, and inspection usability.  
This release enhances flexibility across all modules and extends validation capabilities.

---

## 🚀 New Features  

### Global Database Connections  
- Database connections are now configured on a **global level**.  
- Global connections can be reused across **all projects**, simplifying configuration and maintenance.  

### Multiple Source Connections per Project  
- Projects can now reference **multiple source connection configurations**.  
- Enables more flexible setups for complex data landscapes within a single project.  

### Logical Datasources  
- Datasources now represent a **logical layer** within a project.  
- Each datasource can be backed by:
  - a **database table**
  - a **database view**
  - or a **custom SQL statement**  
- This separation improves reuse, clarity, and inspection modeling across modules.

### Anomaly Relevance Condition  
- An **Anomaly Relevance Condition** can now be defined to control anomaly status evaluation.  
- Statistics are calculated independently of whether the condition is set or met.  
- If the condition is **not met**, **digna Data Anomalies** does not provide anomaly status (green / yellow / red).

### Per-Module Notification Configuration  
- Notifications can now be configured **per module** directly in digna.  
- Allows independent control of alerting behavior for Data Anomalies, Data Timeliness, Data Validation, and other modules.

### Inspection Results Export (CSV)  
- Users can now **download inspection results as CSV files**.  
- Enables offline analysis, reporting, and integration with external tools.

## 🛠 CLI Updates  

---

## ✅ digna Data Validation  

### Uniqueness Checks for Multiple Columns  
- Introduced **Uniqueness Checks** for a configurable **set of columns**.  
- Enables validation of compound keys and business-level uniqueness rules.

---
