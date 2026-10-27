---
title: Profiling Location – Source Database or digna Engine | digna Documentation
description: Choose where digna profiles your data. By default, profiling runs in the source database. With the digna Engine, digna exports the inspected data and profiles it inside your digna installation, which also enables referential integrity checks between different database connections and technologies.
image: /assets/logo_square.png
keywords:
  - digna engine
  - profiling location
  - in-database profiling
  - data profiling
  - cross-connection referential integrity
  - data quality
  - digna profiling
lang: en
robots: index, follow
og_title: Profiling Location – Source Database or digna Engine | digna Documentation
og_description: Profile data where it lives, in the source database, or export it and profile it in the digna Engine inside your digna installation.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Profiling Location – Source Database or digna Engine

Every database connection has a **Profiling Location**. It decides where digna calculates the statistics and checks of the data sources that read through that connection:

| Profiling Location | Where the work happens |
|---|---|
| **Source Database** (default) | In your database. digna sends SQL and receives aggregated results. |
| **digna Engine** | In digna. digna exports the inspected data and profiles it in the digna Engine. |

The **digna Engine** was introduced in [Release 2026.11](../../changelog/Release_202611.md). It is optional: profiling in the source database remains the default and works as before.

---

## Source Database {: #source-database }

digna profiles data where it lives. Every statistic and every check is a query that runs in your database, and only aggregates come back: a count, a sum, a count per category. See [How Profiling Works](how_it_works.md).

With this location, the connection's **Profiling Mode** (Standard, Permanent or Session) decides whether digna works on the source tables directly or on a copy in a work table inside your database. See [Profiling Mode and Work Schema](../../databases/overview.md#profiling-mode-and-work-schema).

---

## digna Engine {: #digna-engine }

For the case you'd rather export the data and profile it outside the source database, digna profiles it in the **digna Engine**, an engine built into digna:

1. For each data source and inspected date, digna reads the inspected data with **one query** on the source database.
2. It loads the result into the digna Engine.
3. Profiling and the checks run in the digna Engine.
4. When the data source's inspection is done, the copy is discarded. Only the results are stored, as with the source database.

The data leaves the source database, but not your environment: the digna Engine runs inside your digna installation, on-premises or in your private cloud.

What runs where:

| Module | With the digna Engine |
|---|---|
| Profiling, Data Anomalies, Data Analytics | In the digna Engine |
| Data Validation rules and uniqueness checks | In the digna Engine |
| Referential integrity within one connection | In the source database |
| Referential integrity across connections | In the digna Engine (see below) |
| Timeliness, Schema Tracker | Unchanged: they read metadata, not the data |

Things to know:

- The **Profiling Mode** is not used with the digna Engine, and a connection that profiles in the digna Engine can be saved without one.
- Dataset definitions and validation rule conditions are written in the source database's SQL dialect, as before. digna evaluates them on the source, as part of the one query.
- The digna Engine works with memory and, when a data source doesn't fit, with temporary files on the digna host. Plan memory and disk space on that host for the largest inspected date of the data sources that use it. If the data doesn't fit even then, the inspection of that data source fails rather than falling back to the source database.
- The digna Engine is available for every supported database technology.

---

## Referential Integrity Across Connections {: #referential-integrity-across-connections }

Some checks need data from two places. A [referential integrity check](../data_validation/how_it_works.md#referential-integrity) whose two data sources are on **different database connections**, possibly on different database technologies (e.g. Oracle and PostgreSQL), can't run as one query in either database.

The digna Engine makes these checks possible, whatever the connection's Profiling Location:

- With **digna Engine**, the check runs on the exported data, together with the other checks.
- With **Source Database**, everything else still runs in the source database. Only for the cross-connection checks, digna exports the **key columns** of both data sources into the digna Engine and runs those checks there.

The dashboard shows a note on such a check. The failing records of a cross-connection check can't be listed.

---

## Choosing a Location {: #choosing-a-location }

| Choose | When |
|---|---|
| **Source Database** | Data must not leave the source database, or digna has read-only access and the database handles the profiling queries well |
| **digna Engine** | You'd rather export the data and profile it in digna, e.g. to keep the profiling work off the source database |

Cross-connection referential integrity works with both, so it is no reason to change the location.

The location is set per database connection, in **Admin → DB Connections**. Changing it applies from the next inspection of the data sources that use the connection.

---

## Related Pages

- [How Profiling Works](how_it_works.md)
- [Database Connections Overview](../../databases/overview.md)
- [Data Validation – How It Works](../data_validation/how_it_works.md)
- [Changelog – Release 2026.11](../../changelog/Release_202611.md)
