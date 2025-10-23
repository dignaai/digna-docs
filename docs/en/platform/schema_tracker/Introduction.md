---
title: Data Schema Tracker – Monitor Schema Evolution | digna Documentation
description: Learn how digna Data Schema Tracker monitors column additions/removals, data type changes, and overall schema drift. Receive alerts for both planned and unplanned changes to prevent ETL failures and broken dashboards.
---

# Data Schema Tracker – Monitor Schema Evolution

## Purpose
Track schema evolution and notify teams when changes occur.

## Technical Features
- Monitors:
  - Added or removed columns
  - Data type changes
- Generates alerts for both intentional and unintentional schema changes  
- Prevents **silent schema drift** that could break ETL pipelines or dashboards  

## Example Use Cases
- Detecting data type changes (e.g., `INT` → `VARCHAR`) that may cause downstream errors  
- Notifying data engineers before pipelines fail due to schema mismatches  

## Value
Helps teams stay in control of **fast-moving, evolving datasets**.