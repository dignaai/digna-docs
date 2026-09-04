---
title: digna Release 2026.06 | Python SDK, Docker Deployment & Enhanced Validation Management
description: Learn what’s new in digna Release 2026.06. This version introduces the new digna Python SDK, Docker deployment support, a redesigned dashboard experience, and extended import/export capabilities for data validation rules.
keywords: digna Release 2026.06, digna Python SDK, digna Docker support, data quality automation, data profiling, validation rule import export, digna dashboard, data observability platform, Python API, metadata automation
image: /assets/logo_square.png
---

# Changelog – Release 2026.06  

With Release 2026.06, digna takes a major step forward in automation, extensibility, and platform usability.  
This release introduces the new **digna Python SDK**, official **Docker deployment support**, a refreshed dashboard experience, and enhanced portability for validation rule management.

---

## New Features  

### digna Python SDK – Automate Everything with Python  
- Install via:
  ```bash
  pip install digna-sdk
  ```
- Programmatically manage and automate digna using Python  
- Create and configure projects via code  
- Trigger inspections and monitoring executions  
- Manage datasets, rules, and configurations programmatically  
- Profile tables and extract metadata insights  
- Export profiling and data quality results to external repositories and systems  
- Integrate with notebooks, orchestration tools, and CI/CD pipelines  

**Impact:** Enables full infrastructure-as-code and deep automation of data quality and observability workflows using Python.

---

### Docker Support – Simplified Deployment & Operations  
- Official Docker image support for digna  
- Fast and consistent setup across environments  
- Simplified onboarding for development, test, and production  
- Easy integration with Kubernetes and container platforms  
- Improved portability and reproducibility of deployments  

**Impact:** Makes digna easier to deploy and operate in modern cloud-native architectures.

---

### QueryMode – Flexible SQL Execution Strategy

Configure query execution strategy: **Single** or **Combined** mode

**Single Mode**: Each statistic is calculated with one dedicated SQL query

  - Ideal for large datasources where memory constraints are a concern
  - Prevents combined query resource exhaustion (out of memory, spool limits)
  - Higher query count but lower per-query memory footprint

**Combined Mode**: All statistics are computed within a single SQL query

  - Reduces total query count and network overhead
  - Optimizes performance when datasources are manageable in memory
  - More efficient for frequent, parallel executions

**Impact:** Gives users fine-grained control over query execution to balance performance, resource usage, and memory safety based on their datasource characteristics.


---

### Redesigned Dashboard Experience  
- Modernized and improved UI/UX design  
- Clearer navigation and structure  
- Better visibility of monitoring results and data quality insights  
- Improved readability of alerts, statistics, and dashboards  
- Faster access to key operational information  

**Impact:** Improves usability and daily productivity for all users.

---

### Extended Import & Export for Validation Rules  
- Enhanced import/export functionality for validation rules  
- Easier migration between environments and projects  
- Improved reuse of standardized rule sets  
- Better governance and rule lifecycle management  
- Simplified collaboration across teams  

**Impact:** Enables scalable and consistent data quality governance across the organization.

---

## Platform Enhancements  

- Full Python SDK integration for automation  
- Containerized deployment via Docker  
- Improved UX through redesigned dashboard  
- Expanded portability of validation logic  

---

## Who Benefits from This Release  

- Data Engineers: automation, SDK usage, pipeline integration  
- Platform Teams: simplified deployment via Docker  
- Data Governance Teams: reusable validation rule management  
- Analytics Teams: improved usability and insights visibility  

---

## CLI Updates  
- Added SDK integration support  
- Improved import/export workflows  
- General stability and performance improvements  
