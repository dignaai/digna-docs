---
title: digna Release 2025.09 | Modular Design, Five New Modules, MFA via OIDC
description: Learn what’s new in digna Release 2025.09. This version introduces a modular architecture, five new modules, MFA via OIDC, and per-module notifications.
keywords: digna Release 2025.09, digna changelog, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modular design, digna OIDC MFA
image: /assets/logo_square.png
---

# Changelog – Release 2025.09  

With Release 2025.09, digna introduces a new **modular architecture** and launches **five specialized modules** for Data Quality and Observability.  
This release also strengthens authentication and improves notification handling across the platform.  

---

## 🚀 New Features  

### Modular Design  
- digna now follows a **modular architecture**.  
- Customers can enable only the modules they need and add more as requirements grow.  
- Previous functionality is now part of **digna Data Anomalies**.  

### New Modules  
- **digna Data Anomalies** – AI-powered detection of anomalies in data volumes, distributions, and missing values.  
- **digna Data Analytics** – Time-series evaluation of observability metrics to detect long-term trends and volatility.  
- **digna Data Timeliness** – Monitoring of expected data arrival times, both AI-based and rule-based.  
- **digna Data Validation** – Rule-based record-level checks to ensure compliance with business rules.  
- **digna Data Schema Tracker** – Detection of schema changes (DDL modifications) in monitored databases.  

### MFA via OIDC  
- Support for **Multi-Factor Authentication (MFA)** with OIDC Single Sign-On.  
- Provides enterprise-grade security for all user logins.  

### Per-Module Notification Emails  
- Notifications are now sent **per module**, making it easier to separate alerts from Data Anomalies, Data Analytics, and other modules.  

---

## 🛠 CLI Updates  

- **New command: `inspect-cancel`** – Cancel inspections by request ID or terminate all active requests.  
- **New command: `check-config`** – Validate configuration files before startup.  
- **New command: `remove-orphans`** – Clean up orphaned repository entries.  
- **Enhanced `inspect` command** – New option `--bypass-backend` (`-bb`) and standardized return codes (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Documentation  
- New guides:  
  - Single Sign-On Integration Guide  
