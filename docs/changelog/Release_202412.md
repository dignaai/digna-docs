---
title: digna Release 2024.12 | Changelog & New Features
description: Discover what’s new in digna Release 2024.12. This version introduces a built-in scheduler, PDF reporting, flexible custom columns, dynamic snapshot query placeholders, and smarter threshold optimization to improve anomaly detection and data quality monitoring.
keywords: digna Release 2024.12, digna changelog, release notes, built-in scheduler, PDF reports, custom column type, snapshot query placeholders, threshold optimization, data observability, data quality monitoring, anomaly detection
image: /assets/logo_square.png
---



# Changelog – Release 2024.12

The 2024.12 release delivers a new set of features and improvements that make digna more automated, flexible, and business-ready.  
This version enhances scheduling, reporting, query handling, and anomaly detection accuracy.  

---

## New Features

### Built-in Scheduler
Inspections no longer depend solely on the command line or API calls.  
With the **new digna Scheduler**, inspections can be executed automatically at defined times.  

- Supports **Cron expressions** for recurring schedules (daily, weekly, or custom intervals).  
- Offers precise control through **offsets**, **start dates**, and **end dates**.  
- Enables teams to ensure all critical data sources are inspected consistently and without manual effort.  

---

### Reports in PDF Format
Teams can now easily share results with stakeholders through **PDF exports**.  

- Charts, metrics, and anomaly results can be exported in a professional PDF format.  
- Reports combine **visualizations** and **underlying data** to serve both technical and business users.  
- Eliminates the need for external tools for report creation.  

---

### New Column Type: `CUSTOM`
To provide more flexibility, digna introduces a new **`CUSTOM` column type**.  

- Users can define exactly which **statistics and metrics** are applied to specific attributes.  
- Perfect for special cases that don’t fit into standard categories such as NUMERICAL or CATEGORICAL.  
- Helps keep analyses focused and results relevant to business context.  

---

### New Placeholders in Snapshot Queries
Snapshot queries are now simpler and less error-prone with **dynamic placeholders**.  

- Tokens like `#date+n#` or `#date-n#` automatically adjust dates in queries.  
- Example:  
  - `#date+1#` → tomorrow  
  - `#date-2#` → two days ago  
- Eliminates manual date calculations and ensures consistency across teams.  

---

### Threshold Optimization
Anomaly thresholds are now more intelligent and context-aware.  

- For metrics such as **NULL COUNT**, lower thresholds are automatically capped at **0**.  
- Prevents invalid or meaningless thresholds.  
- Results in fewer false positives and more reliable anomaly detection.  

---

## General Improvements
- Refined **UI components** in project and attribute configuration views.  
- Improved **dashboard performance** for large data volumes.  
- Enhanced **logging and error messages** for troubleshooting.  

---

## Summary
Release 2024.12 strengthens digna as a platform for **data quality, anomaly detection, and observability**.  
With automation through scheduling, shareable PDF reports, customizable columns, simplified snapshot queries, and smarter thresholds, digna becomes even more valuable for both technical users and business stakeholders.  
