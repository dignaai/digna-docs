---
title: Data Validation – Rule-Based Checks for Compliance & Auditability | digna Documentation
description: Discover how digna Data Validation enforces deterministic, rule-based checks with thresholds, ranges, and reference lists. Ensure compliance, auditability, and regulatory reporting in finance, healthcare, and other data-sensitive industries.
image: /assets/logo_square.png
keywords:
  - data validation
  - rule-based data checks
  - data quality
  - quality of data
  - data observability
  - thresholds and ranges
  - reference list validation
  - auditability
  - compliance monitoring
  - digna data validation
lang: en
robots: index, follow
og_title: Data Validation – Rule-Based Checks for Compliance & Auditability | digna Documentation
og_description: digna Data Validation enforces deterministic, rule-based checks with thresholds, ranges, and reference lists. Designed for regulated industries, it ensures compliance, transparency, and auditability.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Rule-Based Checks
<h1 style="display:none;">AI-Driven Data Validation Module for Data Quality and Observability – digna</h1>

---

## Purpose

The **Data Validation** module ensures the **quality of data** through precise, rule-based checks.  
It allows organizations to define deterministic business and technical validation logic, ensuring that data meets compliance standards, contractual SLAs, and regulatory requirements.

By combining *in-database rule execution*, *complete audit trails*, and *integration with other digna modules*, **Data Validation** guarantees consistent and traceable **Data Quality and Observability** across complex enterprise environments.

---

## Technical Overview

### Supported Validation Types

- **Equality Checks**  
  Confirm that values match expected results (e.g., reference codes, Boolean flags, categorical mappings).

- **Thresholds & Ranges**  
  Validate numeric measures or KPIs against defined limits — static or dynamically derived.

- **Reference Lists & Lookups**  
  Check whether field values exist within approved master data sets (e.g., VAT codes, ISO country lists, product catalogs).

- **Cross-Column Consistency**  
  Ensure relational correctness (e.g., currency aligns with region, risk category matches asset type).

- **Null Handling Rules**  
  Detect unexpected null or empty values in critical columns.

### Execution and Logging

- **In-Database Processing** – All validation rules execute directly in your database (Teradata, Snowflake, Databricks, PostgreSQL, etc.).  
- **No Data Extraction** – digna never transfers raw data outside your environment.  
- **Full Traceability** – Each rule result is logged with timestamp, responsible dataset, record counts, and pass/fail outcomes.  
- **Audit**
