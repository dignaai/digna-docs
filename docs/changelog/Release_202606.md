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

## Watch the Release

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — a walkthrough of this release on the digna YouTube channel.*

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

### Configurable Prediction Model

The model behind anomaly detection is now configurable. Seven parameters steer how the prediction is fitted:

- Break Sensitivity
- Outlier Sensitivity
- Memory
- Ridge Strength
- Gap Tolerance
- Outlier Correction
- Plausible Range Tightness

The defaults suit the great majority of series, and each parameter can be restored to its default at any time.

**Impact:** Gives users control over the prediction model itself, alongside the existing Sensitivity and Memory settings on the tolerance band. For guidance on when to reach for one and how to set it, contact digna.

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
