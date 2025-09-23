---
title: Data Schema Tracker – Monitor Schema Evolution | digna Documentation
description: Learn how digna Data Schema Tracker monitors column changes, datatype updates, and schema drift. Get alerts for intentional and unintentional changes to prevent ETL failures and dashboard errors.
---

# Data Schema Tracker – Monitor Schema Evolution

## Purpose
Track and alert on schema evolution.

## Technical Features
- Monitors:
  - Added or removed columns
  - Datatype changes
- Alerts on both intentional and unintentional schema changes  
- Prevents **silent schema drift** that can break ETL pipelines or dashboards  

## Example Use Cases
- Identifying datatype changes (e.g., `INT` → `VARCHAR`) that may cause downstream errors  
- Alerting data engineers before pipelines fail due to schema mismatches  

## Value
Keeps teams in control of **fast-moving, evolving datasets**.
