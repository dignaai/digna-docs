---
title: Schema Tracker – How It Works | digna Documentation
description: How digna Schema Tracker works — a stored column baseline compared on every inspection, the three change events it reports, why a rename appears as a removal plus an addition, and how the baseline advances.
image: /assets/logo_square.png
keywords:
  - schema tracker how it works
  - schema drift detection
  - column baseline
  - type change alert
  - new removed column
  - data contract monitoring
  - quality of data
  - observability of data
  - digna schema tracker
lang: en
robots: index, follow
og_title: Schema Tracker – How It Works | digna Documentation
og_description: The mechanics of digna Schema Tracker — baseline comparison, the three change events, and how the baseline advances.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Schema Tracker – How It Works

---

## Baseline and Comparison

Schema Tracker keeps a **baseline**: the set of columns and their data types, as read from the source catalogue.

On every inspection it reads the catalogue again and compares:

```
1. Read the current columns and types from the source catalogue
2. Compare against the stored baseline
3. Report the differences that match an enabled event type
4. Advance the baseline
```

The very first inspection has nothing to compare against. It records the baseline and reports **Passed** — a new data source is never flagged for existing.

The comparison is against the catalogue, not against the data, so it costs one metadata query regardless of how large the table is.

---

## The Three Events

| Event | Raised when |
|---|---|
| **NEW** | A column exists now that was not in the baseline |
| **REMOVED** | A column was in the baseline and is gone |
| **TYPE_CHANGE** | A column exists in both, with a different data type |

Each is recorded with the column name, and a type change additionally stores **both the old and the new type**, so the change history says what it changed from rather than only what it is now.

!!! note "A rename is reported as a removal plus an addition"
    Column identity is the column name. Renaming `is_subscribed` to `subscribed` produces a **REMOVED** event for the old name and a **NEW** event for the new one — digna cannot know they are the same column, and neither can the catalogue.

    This is the right behaviour for the failure that matters: everything downstream referencing the old name is broken either way, and a rename reported as a rename would understate that.

---

## Enabling Events Individually

The three event types are switched on and off independently per data source. That is more useful than it first appears, because the three have very different signal-to-noise ratios in different environments.

| Situation | Suggested configuration |
|---|---|
| A shared table other teams consume | All three on |
| A table under active development where columns are added routinely | **NEW** off, **REMOVED** and **TYPE_CHANGE** on |
| A stable reporting source | All three on |
| A source where only breaking changes matter | **NEW** off |

**TYPE_CHANGE** is the one to keep on almost everywhere. A removed column breaks something loudly and gets found; a `DATE` silently becoming a `STRING` keeps loading, and the reports built on it are quietly wrong.

---

## How the Baseline Advances

This is the part worth understanding, because it decides what happens to a change you have chosen not to watch.

The baseline is updated **only when a reportable change is found** — that is, a difference matching an event type you have enabled.

The consequence: if a column is added while **NEW** is switched off, the baseline is not advanced, and the addition is still pending. Switch **NEW** on later and it will be reported then. A change you are not watching is not discarded; it is deferred.

---

## Status

| Condition | Status |
|---|---|
| No reportable change | **Passed** |
| One or more reportable changes | **Failed** |

There is no middle state — a structure either changed or it did not.

---

## Scope and Timing

**Applies to tables and views only.** A data source defined as a query has no catalogue entry to track, and Schema Tracker skips it.

Schema tracking runs **once per data source per inspection request**, not once per inspected date. It describes the structure as it is right now, which has no per-date meaning — and unlike the date-scoped modules, its history is never removed by re-inspecting a date range.

It also works across every technology digna connects to. The check reads the catalogue through the same metadata layer used for connection setup, so it needs no per-technology configuration of its own — see the [database connector guides](../../databases/snowflake_connector_guide.md).

---

## Using It Well

1. **Track the tables other people consume**, not only the ones you own — the cost of a change is carried downstream.
2. **Check the change history first when an anomaly appears.** A distribution shift on the same day as a type conversion is not two problems.
3. **Route structural alerts to the owning team**, so the person who can explain the change receives it.
4. **Read a REMOVED/NEW pair on the same inspection as a probable rename**, and check the names before assuming a column was dropped.

---

## Related Pages

- [Schema Tracker – Introduction](Introduction.md)
- [Schema Tracker – Use Cases](use_cases.md)
- [How to connect a database to a data project](../../getting_started/how_to_connect_database_to_data_project.md)

---
