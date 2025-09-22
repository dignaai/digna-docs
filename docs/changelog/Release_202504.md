---
title: digna Release 2025.04 | Inspection Hub, Multi-language, Module Analytics
description: Learn what’s new in digna Release 2025.04. This version introduces the Inspection Hub, multi-language support (English, German, Polish), import/export of data sources via dignacli, the first release of Module Analytics, and an improved dashboard experience.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna multi-language support, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Changelog – Release 2025.04

With Release 2025.04, digna takes a major step forward in making data quality and observability easier to manage, more transparent for teams, and accessible to users worldwide.  
This release combines **powerful new features**, **workflow automation improvements**, and **user experience refinements**.  

---

## New Features

### Inspection Hub – A New Command Center
The **Inspection Hub** is now available as the central place to manage all your inspection jobs. Instead of jumping between different modules or relying solely on command-line execution, you can now monitor and control your inspections from one streamlined interface.  

Key capabilities include:  
- On-demand inspections: Start new jobs instantly whenever you need fresh results.  
- Inspection history: See a timeline of inspections — what was run, who triggered it, and when.  
- Status tracking: Jobs are clearly marked as completed, in progress, or pending.  
- Invoker insights: Quickly check whether an inspection was triggered by a user, scheduler, or the CLI.  
- Clean-up tools: Delete outdated or unnecessary jobs to keep your workspace clear.  
- Detailed logs: Drill into each job to see how long it took, which sources were included, and how thresholds were applied.  

The Inspection Hub gives teams **end-to-end visibility and control**, making inspections easier to manage across large projects.  

---

### Multi-language Support – digna Speaks Your Language
digna is now ready for international teams with the introduction of **multi-language support**.  

In this release you can set your **preferred interface language** directly in User Preferences. Supported languages include:  
- English (UK, US, CA, AU)  
- German (DE, AT, CH)  
- Polish (PL)  

This makes digna easier to use for multilingual organizations and ensures smoother adoption across teams working in different regions. More languages will be added in upcoming releases.  

---

### Import & Export of Data Sources – Configuration Made Simple
Consistency across environments is essential in enterprise deployments. With 2025.04, digna introduces **import/export of data sources** via **dignacli**, the command-line tool for advanced users.  

Benefits:  
- Export a data source configuration once, then reuse it across Development, Test, and Production.  
- Eliminate manual reconfiguration and avoid costly errors.  
- Support automated workflows and CI/CD pipelines with simple CLI commands (`export-ds` and `import-ds`).  
- Quickly copy data sources between projects for easier collaboration.  

This functionality ensures that teams can deploy with confidence, knowing that configurations are consistent in every environment.  

---

### Module Analytics (v1) – From Detection to Understanding
digna started as a platform for anomaly detection and data quality monitoring. With Release 2025.04, it evolves further with the **first version of Module Analytics**.  

Module Analytics helps users **understand their data** rather than just react to issues. With this new module you can:  
- Track long-term trends in your data sets.  
- Detect and monitor volatility to understand fluctuations.  
- Explore data behavior over time for deeper context.  

For example, digna can automatically highlight that *“Row count increased by 15.8% since the beginning of the year.”*  
No SQL queries, no manual checks — just **actionable insights at a glance**.  

This is the foundation of digna’s journey toward advanced data analytics, enabling data teams to shift from reactive to proactive monitoring.  

---

### Dashboard Improvements – A Smoother User Experience
Beyond the major features, Release 2025.04 includes several **dashboard refinements** designed to make digna more intuitive and enjoyable:  
- Faster navigation between projects and inspections.  
- A cleaner layout for inspection logs and job submissions.  
- Subtle design adjustments that help you find insights more quickly.  

These improvements are based directly on customer feedback and demonstrate our ongoing commitment to making digna **a platform built for daily use**.  

---

## General Improvements
- Performance optimizations for inspection jobs across large data sets.  
- Enhanced error handling in dignacli to provide clearer feedback.  
- Stability improvements for projects with many simultaneous jobs.  
- UI refinements for job log filtering and project management.  

---

## Summary
Release 2025.04 is about **control, accessibility, and insight**.  

- The new **Inspection Hub** gives users full visibility into inspection jobs.  
- **Multi-language support** ensures digna can be used across global teams.  
- **Import/export functionality** simplifies configuration management across environments.  
- **Module Analytics (v1)** shifts the focus from detection to understanding, with trend and volatility tracking.  
- **Dashboard improvements** refine the overall user experience.  

Together, these updates make digna more powerful, user-friendly, and internationally ready than ever before.  
