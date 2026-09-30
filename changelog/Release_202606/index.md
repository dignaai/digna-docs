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

The model behind anomaly detection now weighs competing explanations of each series — a pattern combined with a reading of the most recent observations — and blends their forecasts by how strongly each is supported. A single extreme value can no longer leak into the following predictions.

Two settings on the data source's new **Model** tab steer it, each from `0.0` to `1.0` with `0.5` as the default:

- **Break Sensitivity** – how quickly a jump to a new level or a turning trend is believed rather than treated as outliers
- **Model Complexity** – how much structure the model looks for, from calendar effects and a single level shift up to unknown cycles, month-day effects and monthly resets

Both can be restored to their defaults at any time. See [Model Settings](../platform/data_anomalies/how_it_works.md#model-settings) for how each one acts.

**Impact:** Gives users control over the prediction model itself, alongside the existing Sensitivity and Memory settings on the tolerance band, now on the **Thresholds** tab.

---

### Anomaly Notification Controls

- New **Notifications** tab on the data source's anomaly settings:
  - **Minimum Alerts** – how many failed checks (not uncertain ones) an inspection needs before a notification is sent (default `1`)
  - **Pause After Notification (Days)** – how long a subscription stays silent after notifying about the data source (default `0`, no pause)
- Subscribers are now notified when an inspection fails outright (**Notify Inspection Errors**)
- Every notification links straight to the page it is about — the failed checks of the inspection, or the Schema Tracker and Timeliness views
- Clearer subscription switches: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

**How notifications work:** notifications are sent through **notification channels** – Email (via an SMTP connection), Slack or Jira – which administrators set up and can check with **Test Notification Channel**. A **subscription** connects a channel to a project: it covers all data sources or selected ones, and its switches choose what it reports – each module (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker and data volume checks), inspections that fail outright, and optionally passed inspections as well.

**Impact:** Fewer, more actionable notifications — isolated deviations and persisting anomalies no longer flood the channel.

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