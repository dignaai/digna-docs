# Data Validation – Use Cases

---

## When to Reach for This Module

Use *Data Validation* whenever **the requirement can be written down**. Not "does this look unusual", but:

> `invoice_amount` must be positive.
> `currency_code` must be in `{EUR, USD}`.
> `vat_code` must be present.

These are not statistical questions and should not be answered statistically. *Data Validation* checks **every single row** against rules you define, and reports exactly which records failed and how many — deterministically, with no assumptions and no learning period.

Rules can be created by **technical or business users** through the interface, which matters more than it sounds: the person who knows the regulation is usually not the person who writes SQL.

The module **works independently of the other modules**. A project can run validation alone, or run it alongside AI-based detection.

!!! info "The complementary pairing"
    [*Data Anomalies*](../data_anomalies/Introduction.md) catches what you did not think to check. *Data Validation* proves what you are required to check. Compliance work needs the second; it is not satisfied by "the model saw nothing unusual".

---

## Finance and Regulatory Reporting

### Invoice and transaction compliance

A typical invoice dataset is validated with a small set of rules:

| Rule | Type |
|---|---|
| `vat_code` must be present | Null / presence check |
| `currency_code` must be in `{EUR, USD}` | Reference list |
| `invoice_amount` must be positive | Threshold |
| `invoice_amount` must not exceed the approval limit | Threshold |
| `invoice_date` must fall in the reporting period | Range |

A run against a real month's data returns not just a pass/fail but the **count of non-compliant records and the records themselves** — for example, 31 rows failing across the five rules. That list is what gets handed to the process owner; the aggregate number alone is not actionable.

### Pre-submission checks before risk reporting

A financial services team validates transaction records against business rules **before** risk reporting is published, rather than discovering the breach in a regulator's response. Because validation results are inspectable and exportable, the same run doubles as the evidence that the check was performed.

### Reference data integrity

Country codes, currency codes, product codes, counterparty classifications — all natural reference-list rules. A value outside the list is unambiguously wrong, and treating it as an anomaly to be scored would only add doubt.

---

## Healthcare

- **Mandatory clinical fields** — a diagnosis code, an admission date, or a consent flag that must never be null on a submitted record.
- **Coded value conformance** — procedure and diagnosis columns validated against the official code list in force, so a retired or mistyped code is caught at the row rather than in aggregate.
- **Plausibility ranges** — dates of birth, admission and discharge ordering, and measurement ranges that must hold for a record to be usable.

---

## Telecommunications

- **Billing correctness** — usage quantities and charged amounts constrained to sensible ranges before an invoice run, since a billing error reaches customers directly.
- **Contract and tariff conformance** — tariff codes validated against the active catalogue, catching records created against a plan that no longer exists.
- **High-volume, distributed sources** — where a small change at one source creates widespread downstream errors, explicit rules at the entry point stop the error spreading rather than merely reporting it later.

---

## Public Sector

Public sector work typically requires **traceability across systems**. *Data Validation* is the module that supplies it directly: **every rule run logs its results**, including how many records failed and which ones, and all outcomes are **inspectable, exportable, and easy to trace**.

That makes it suitable for statutory reporting, eligibility and entitlement checks, and any process where "the data was correct" has to be demonstrable months later.

---

## Governing Rules Across Environments

From **Release 2026.06**, validation rules can be **imported and exported**, which changes how rule sets are managed at scale:

- Promote a rule set from development to test to production without re-entering it.
- Reuse a standard set — mandatory fields, currency and country lists, sign conventions — across projects.
- Keep rule definitions in version control alongside the rest of your configuration.
- Share a curated set between teams so that "compliant" means the same thing in each of them.

See the [Release 2026.06 changelog](../../changelog/Release_202606.md) for the details.

---

## Designing a Rule Set That Stays Useful

| Do | Instead of |
|---|---|
| Write one rule per requirement, named after the requirement | One large rule that fails for several unrelated reasons |
| Encode the regulation or contract that motivates the rule in its description | Leaving future readers to infer the intent |
| Use reference lists for closed value sets | Chains of exact-value comparisons |
| Reserve validation for stated requirements | Re-implementing anomaly detection as thresholds you have to keep tuning |

---

## Where This Module Fits

| Question | Module |
|---|---|
| Does every row satisfy a rule we can state? | **Data Validation** |
| Did something change that nobody expected? | [Data Anomalies](../data_anomalies/Introduction.md) |
| Is a metric trending or destabilising? | [Data Analytics](../data_analytics/Introduction.md) |
| Did the data arrive on time? | [Data Timeliness](../data_timeliness/Introduction.md) |
| Did a column or type change? | [Schema Tracker](../schema_tracker/Introduction.md) |

---

## Related Pages

- [Data Validation – Introduction](Introduction.md)
- [Data Validation – How It Works](how_it_works.md)
- [digna Modules – Technical Overview](../overview.md)
- [Changelog – Release 2026.06](../../changelog/Release_202606.md)

---