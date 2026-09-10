# Data Timeliness – How It Works

---

## What Counts as a Delivery

A **delivery** is any inspection of this data source that profiled rows — whether it was started by the scheduler, through the API, from the CLI, or as a backfill. The only gate is that the Timeliness module is enabled on the data source.

Two consequences follow, and both matter in practice:

!!! warning "digna records when it *observed* the rows, not when they landed"
    The delivery timestamp is the moment the inspection ran. A job scheduled at 06:00 cannot see that the data actually arrived at 03:00 — it can only report that by 06:00 it was there. **The precision of timeliness monitoring is therefore bounded by your inspection cadence.** A source inspected once a day supports day-level expectations, not hour-level ones.

!!! warning "Manual runs and re-inspections move the expectation"
    Because the timestamp is a clock reading, a delivery cannot be deduplicated. Re-inspecting an old date, or triggering a run by hand outside the normal window, records a delivery at *that* moment and carries the expectation with it. Expect a manual run at an unusual hour to disturb the learned pattern.

Delivery history is retained for three years.

---

## Two Modes

Each data source is judged in one of two modes.

### AI Based

digna learns the arrival pattern from the delivery history and predicts the next one. Two quantities are predicted separately:

- **The gap** — how many days until the next delivery.
- **The minute of day** — what time within that day it should land.

Both use the same modelling machinery as [Data Anomalies](../data_anomalies/how_it_works.md), so a source that delivers Monday to Friday learns that Friday means three days rather than one, without anyone configuring it.

Gaps are indexed forward — the days from each delivery to the *next* one are attached to the earlier date — which is what lets the weekday effects be learned at all.

### Rule Based

The expectation is stated rather than learned. Four shapes are available:

| Rule mode | Configuration | Describes |
|---|---|---|
| **Daily** | A time and a time zone | "Every day by 06:00 Europe/Vienna" |
| **Weekly** | A time, a set of weekdays, a time zone | "Mondays and Thursdays by 22:00" |
| **Monthly** | A time, a set of days of the month (including **Last day**), a time zone | "The 1st and the 15th by 09:00", or "the last day of the month" |
| **Time Between** | A value and a **Window Type** — hour, day, week, or month | "At most 4 hours between deliveries" |

The first three are calendar deadlines and honour the configured time zone, including its daylight-saving transitions. **Time Between** is different in kind: it has no calendar at all, only a maximum interval since the last delivery, which is what makes it the right choice for a source that delivers many times a day.

A rule that no schedule can honour — an empty weekday list, an unrecognised time zone — is rejected loudly when it is used, rather than leaving a data source silently unmonitored.

!!! tip "Which mode to pick"
    Use **Rule Based** where a contract, an SLA, or a regulation states the deadline — there, "usually on time" is not the standard, and a learned expectation would drift toward whatever actually happens. Use **AI Based** everywhere else, especially across a large landscape where hand-scheduling every source is not realistic.

---

## The Alert Margin

The predicted arrival time and the deadline are deliberately two different things:

```
deadline  =  expected delivery time  +  alert margin
```

The expectation is the bare point prediction. The margin is the slack allowed on top of it before a delivery counts as late.

- In **Rule Based** mode the margin is zero — the rule states its deadline outright.
- In **AI Based** mode the margin is fitted to how late past deliveries actually were, using the same [sensitivity and memory](../reference/tuning.md#the-tolerance-band) settings as anomaly detection.

Keeping the two apart is what stops the deadline from inflating. If each margin were folded into the stored expectation, the next margin would be fitted to deviations from the previous *deadline* rather than from a prediction, and the slack would compound on every delivery.

The margin also has floors and ceilings, because a fitted value alone is not safe at the extremes:

| Guard | Purpose |
|---|---|
| At least a tenth of the predicted gap | A source that has been landing exactly on time would otherwise get a near-zero margin — and a monthly source needs more slack than a daily one |
| One hour on an empty history | The very first prediction has no gap to take a fraction of |
| Capped at the length of the error window it was fitted over | A margin wider than its own reference window is not a meaningful margin |

---

## Sub-Daily Deliveries in AI Based Mode

The prediction model is indexed by calendar date, so a source delivering several times a day cannot be represented directly. AI Based mode collapses each date to **the last delivery of that date**, which is the conservative choice — the deadline should cover the latest arrival that is still normal.

If a source genuinely delivers many times a day and each one matters, that is what **Time Between** is for.

---

## Status

Timeliness reads the shared status scale with its own vocabulary, and it has no middle ground:

| Condition | Status |
|---|---|
| The delivery arrived on or before its deadline | **In Time** |
| It arrived after | **Delayed** |
| The module is not enabled on this data source | **Not Tracked** |

An **early** delivery is In Time. digna does not flag data that arrives ahead of schedule — if a re-processing upstream is a concern for you, the signal to watch is a duplicate-load anomaly in [Data Anomalies](../data_anomalies/how_it_works.md), where row count and column sums move together.

Every recorded delivery stores the timestamp, the expectation it was judged against, the next expectation, and the margin — so a status can be explained later without re-deriving anything.

---

## A Delivery That Never Arrives

Every other finding in digna is produced by an inspection. A **missing** delivery has no inspection to produce it, so it is handled separately.

A background monitor checks **every minute** for data sources whose deadline has passed with no delivery recorded, and raises the alert. Each missed deadline is claimed exactly once before its message is sent, so a source that stays missing alerts once rather than every minute.

A data source whose inspection ran but whose tasks all failed reaches the same place: nothing was profiled, so nothing was delivered, and the monitor reports it as missed — which is what it is.

### Viewing the past

The timeliness overview supports **time travel**: setting an *as of* point shows the status of every data source as it stood at that moment, rather than as it stands now. That is how you reconstruct what was actually late on the morning a report went out, instead of inferring it from the current state.

### Skipping a delivery

When you know no delivery is coming — a holiday, a planned outage, a source retired for a period — a delivery can be declared skipped. The expectation advances to the next slot without a missed-delivery alert being raised.

---

## Configuration Caveat on Import

!!! warning "Project import resets some rule-mode settings"
    Exporting a project and importing it elsewhere carries the timeliness **mode**, and the **TIME_BETWEEN** value and unit. It does **not** carry the rule mode, rule time, weekdays, days of month, or time zone — those return to their defaults on the imported side (`DAILY`, `00:00`, `UTC`, empty day sets).

    After importing a project, re-check the timeliness configuration of any data source that used a **Daily**, **Weekly**, or **Monthly** rule.

---

## Related Pages

- [Data Timeliness – Introduction](Introduction.md)
- [Data Timeliness – Use Cases](use_cases.md)
- [Statuses and Alerts](../reference/statuses.md)
- [Anomaly Tuning](../reference/tuning.md)
- [How to schedule a daily job](../../getting_started/how_to_schedule_a_daily_job.md)

---