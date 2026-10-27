# Changelog – Release 2026.11  

Release 2026.11 is built around three major additions:

- **digna Data Reconciliation (Beta)**: checks that data stays consistent as it moves between systems  
- **digna Agentic (Beta)**: opens digna to AI agents through the digna MCP Server  
- **digna Engine**: optionally profiles data inside digna, and enables referential integrity checks between different database technologies  

---

## New Features  

### digna Data Reconciliation (Beta) – Source-to-Target Consistency  
Data often passes through several systems before it reaches a report. digna Data Reconciliation (Beta) compares a **target** data source with the **sources** it was built from, and alerts when they no longer match.

- Configured as named rules on the new **Data Reconciliation** tab of the target data source  
- Any data source of the project with Data Reconciliation switched on can be a source  
- Use cases include standard reconciliation procedures and validating the results of ETL processes  
- Two types of rules: **Exact** and **AI**  

**Exact Rules – Reconciliation as a Data Quality Rule**: You define exactly what must match between one source and one target, like a data quality rule.

  - Compare one source data source with one target data source  
  - Pair a target check with a source check by statistic and attribute, e.g. row counts or the sum of an amount column  
  - Allow a difference with an **absolute** tolerance (e.g. ± 10) or a **relative** one (e.g. ± 0.5 % of the source)  
  - The timeline shows each day's difference against the tolerance  

**AI Rules – Reconciliation as Data Observability**: digna learns how a target follows its sources, in the way digna observes data in other modules, and alerts when the relationship breaks.

  - Combine checks from several source data sources with the checks of one target  
  - No need to know or write down the logic between them (joins, filters, aggregations)  
  - A model learns from the history how the target follows its sources on the same day  
  - Each target check is predicted from the day's source values, and digna alerts when the target leaves the band of the rule's own past errors  
  - Each rule has its own **Model settings**: **Sensitivity**, **Memory** and **Model Complexity**  

Reconciliation checks appear on the Dashboard with a timeline per rule. They count towards the overall inspection status and trigger notifications.

**Impact:** Covers both sides of reconciliation. Exact rules enforce known controls between source and target, and AI rules monitor complex flows such as ETL processes, so data lost or changed on the way is caught without hand-written reconciliation SQL.

---

### digna Agentic (Beta) – digna for AI Agents  
The first version of digna Agentic (Beta). AI agents can now work with digna, answer business questions about your data, and help improve your configuration.

**digna MCP Server**: Lets Claude and other AI agents work with digna through the Model Context Protocol.

  - Manage projects, data sources, rules, inspection schedules and subscriptions  
  - Read inspection statuses down to the single check, to investigate alerts  

**Descriptions on Data Sources and Attributes**: Describe in plain language what a data source or attribute contains.

  - AI agents use the descriptions to interpret your data  
  - Ask business questions about your data, and AI agents answer them from what digna monitors  
  - If digna's current configuration can't answer a question, the AI agent suggests changes to the data source and its attributes where possible, e.g. adding a new dataset  

**Impact:** Lets you ask business questions about your data in plain language, and lets AI agents help configure digna and investigate data quality issues.

---

### digna Engine – Profile Where You Choose  
By default, digna profiles data where it lives, in the source database. The digna Engine adds an option: digna exports the data from the source and profiles it inside the digna Engine.

- Optional, not mandatory: profiling in the source database remains available  
- Selected per database connection as its **profiling location**: **Source Database** or **digna Engine**  
- Available for every supported source technology  

**Cross-Connection Referential Integrity**: Some checks need data to be exported. The digna Engine extends **digna Data Validation** for these cases.

  - **Referential Integrity Checks** between data sources on **different database connections**, including different database technologies (e.g. Oracle and PostgreSQL)  
  - Works with both profiling locations: for the Source Database, only the key columns are exported to the digna Engine  
  - The dashboard shows when a check runs across two connections  

**Impact:** Lets you choose where data is profiled, and enforces relationships between systems that run on different database technologies.

---

## Profiling Enhancements  

This release also gives users more control over what is profiled and how.

### Query Attributes – User-Defined Columns  
- Define artificial columns: a SQL expression over one or more columns of the data source  
- Each query attribute has its own name  
- Profiled and checked like any other attribute  

### DATE Column Category  
- New **Date** category for attributes  
- Metrics relative to the inspected date  

### On-Demand Profiling  
- Profile any attribute against one date's full snapshot, without running an inspection  
- Helps set the attribute's column type: **Numerical**, **Categorical**, **Date** or **Unspecified**  

---

## Who Benefits from This Release  

- **Data Engineers:** Validation of ETL results with digna Data Reconciliation (Beta)  
- **Finance, Risk & Controlling Teams:** Standard reconciliation procedures as exact rules in digna Data Reconciliation (Beta)  
- **Data Quality & Governance Teams:** Referential integrity across database technologies with the digna Engine  
- **Business Users:** Business questions about data answered by AI agents with digna Agentic (Beta)  
- **AI & Automation Teams:** AI agents working with digna through digna Agentic (Beta)  

---

## CLI Updates  
- No changes  

---