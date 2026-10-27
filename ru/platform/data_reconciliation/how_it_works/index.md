# Data Reconciliation – How It Works

---

## Sources and Target

Every reconciliation rule belongs to its **target**: the data source whose correctness you want to confirm. The rule names one or more **sources**, the data sources the target was built from.

- Rules are configured on the target's **Data Reconciliation** tab.
- **Data Reconciliation** must be switched on for the target and for every source. Only data sources with the module switched on can be chosen as sources.
- Sources and target belong to the same project. They can be on different database connections.

A rule compares **checks**: the statistic of an attribute that digna measures in every inspection, such as the row count of the table or the sum of an amount column. Reconciliation reuses these values, so it adds no queries against your databases.

---

## Exact Rules

An exact rule compares **one source** data source with the target. It consists of pairs, and each pair compares one target check with one source check of the same statistic.

| Pair | Example |
|---|---|
| Row count ↔ row count | Every order in the source arrives in the target |
| Sum of `amount` ↔ sum of `amount` | No value is lost or doubled during the load |
| Distinct count of `customer_id` ↔ distinct count of `customer_id` | No customer goes missing |

Each pair has a tolerance:

| Tolerance type | Passes when | Suits |
|---|---|---|
| **Absolute** | `|target − source|` ≤ the tolerance value | Small fixed differences, e.g. ± 10 rows |
| **Relative** | `|target − source|` ≤ the tolerance value, in % of the source | Tables of any size, e.g. ± 0.5 % |

A tolerance of 0 requires an exact match. With a relative tolerance, a source value of 0 passes only when the target is 0 as well.

An exact pair is either **Passed** or **Failed**. A pair also fails when the target or the source has no value for the inspected date.

---

## AI Rules

An AI rule combines checks from **several source** data sources with one or more checks of the target. It needs no description of the logic between them.

### How the prediction works

For each target check, digna learns from history how the target has followed its sources **on the same day**. It then predicts today's target value from today's source values and compares the prediction with the value the target actually has.

- The model learns from the **365 days** before the inspected date.
- It is trained again for every prediction, so it follows changes in the relationship without a separate training step.
- Single days with broken data do not distort it: the model is fitted robustly, so outliers in the history carry little weight.

### The expected range

How far the target may deviate from the prediction is not set by hand. digna stores every prediction it makes and measures how far each one was from the value that followed. The expected range is derived from these past errors: a rule whose sources explain the target well gets a narrow range, a noisy relationship gets a wide one.

| Target value | Status |
|---|---|
| Inside the expected range | **Passed** |
| Outside the inner range | **Uncertain** |
| Outside the outer range | **Failed** |

### History needed

A new AI rule needs history before it can judge:

- at least **30 days** on which the target and its sources all have values, to learn from, and
- at least **10 past predictions**, to derive the expected range.

Until then the rule's checks have no status. digna fills in predictions for past dates over the next inspections, so a rule over sources with existing history becomes active after a few inspections.

### Model settings

Each AI rule has its own **Model settings**:

| Setting | Values | Effect |
|---|---|---|
| **Sensitivity** | Very Low … Very High (default: Moderate) | How readily the rule alerts. Higher sensitivity narrows the expected range. |
| **Memory** | Short, Moderate, Long (default: Moderate) | How fast old history stops counting, both for learning and for the expected range. |
| **Model Complexity** | 0.0 … 1.0 (default: 0.5) | How elaborate a relationship between sources and target the model may assume. |

---

## Matching Datasets

When the target is split into [datasets](../profiling/datasets.md), each target dataset is compared with the source dataset **of the same name**, e.g. the target's `region = 'North'` dataset with the source's `region = 'North'` dataset.

- **Exact rules** need a source dataset with the same name. If there is none, the pair fails.
- **AI rules** can also learn from a source that is not split: if a source has a single whole-table dataset, it feeds every target dataset.

A dataset excluded by its relevance rules gets no reconciliation status.

---

## When Reconciliation Runs

Reconciliation is evaluated in the **target's inspection**, after the target's own checks, and only when every source of the rule has been inspected successfully for the same date. If a source has not been inspected yet, digna writes nothing for that date. This is not a failure: the date simply isn't ready to be reconciled.

- When sources and target are inspected in the same inspection request, digna inspects the sources first.
- Inspecting only a source again does not re-evaluate the target. Inspect the target again to reconcile against the new source values.

---

## Statuses and Notifications

Reconciliation results roll up like every other module's: check → attribute → dataset → data source, and the worst result wins. They count towards the overall inspection status, so a failed reconciliation turns the data source red on the Dashboard.

On the Dashboard, each reconciliation check opens a timeline per rule: for exact rules the source value, the target value and the difference against the tolerance; for AI rules the target value against the prediction and its expected range.

Failed reconciliation checks are notified through your subscriptions, like failures of the other modules.

---

## Related Pages

- [Data Reconciliation – Introduction](Introduction.md)
- [Data Reconciliation – Use Cases](use_cases.md)
- [Datasets](../profiling/datasets.md)
- [Statistics](../profiling/statistics.md)
- [Changelog – Release 2026.11](../../changelog/Release_202611.md)