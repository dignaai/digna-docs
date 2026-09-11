# Data Validation – How It Works

---

## Three Kinds of Rule

Every validation rule is one of three kinds. They exist separately because each becomes a different shape of SQL, and each answers a different question.

| Kind | Question it answers |
|---|---|
| **Rule** | Does each row satisfy this condition? |
| **Uniqueness** | Is this key actually unique? |
| **Referential Integrity** | Does every value here exist in that other table? |

All three are evaluated **per row**, inside the source database, and all three report a count of passing and failing records.

!!! warning "Uniqueness and Referential Integrity skip NULLs"
    Both checks are executed **only on populated (non-`NULL`) values**. A key column full of nulls will not fail a uniqueness check, and null foreign keys will not fail referential integrity. If a value being present is itself a requirement, that is a **Rule** — `col IS NOT NULL` — and it belongs in a rule of its own.

---

## Rule Expressions

A rule is built in the **Rule Builder** rather than typed as SQL, which is what lets a business user author one. It compares a left-hand side with a right-hand side, each of which may be a simple value or a calculated expression, and conditions can be nested with parentheses to any depth.

Whatever you build is translated into SQL and shown in the **Expression** field, so the rule stays reviewable. The builder supports:

| Element | Available |
|---|---|
| **Comparison** | `=`, `<>`, `<`, `<=`, `>`, `>=`, `IS`, `IS NOT`, `IN`, `NOT IN`, `LIKE`, `NOT LIKE` |
| **Logic** | `AND`, `OR`, nested to any depth |
| **Arithmetic** | `+`, `−`, `×`, `÷` |
| **Operands** | An **Attribute** (column), **Number**, **String**, **Boolean**, **Null**, **Enumeration**, or **Custom** — a SQL expression executed on the source, e.g. `length(mycolumn)` |

```sql
price > 0                                    -- simple comparison
status IN ('active', 'pending')              -- allowed values
delivery_date IS NOT NULL                    -- presence
(revenue / customers) >= (cost / items)      -- calculated on both sides
discount > 0.2 OR (quantity > 0 AND price > 0)
(region = 'EU' AND (revenue > 1000 OR discount > 0.1))
  OR (region = 'US' AND revenue > 5000)      -- different thresholds per region
```

Every one of these is assembled by selecting rather than typing.

The escape hatch is the **Custom** operand, which passes SQL through untouched — useful for a source-specific function, and the one operand that ties a rule to a particular technology.

### Enumerations

A reference list — currencies, country codes, product categories, status values — is stored once as an **enumeration** and referenced by rules rather than being retyped into each one. Changing the list changes every rule that uses it, which is what keeps "valid currency" meaning the same thing across a project.

### Rule templates

A **template** is a rule expression with a placeholder where the column goes. "Must not be null", "must be positive", "must match this pattern" are written once and then applied to as many columns as needed. Each application is a real rule with its own thresholds and its own results — the template only supplies the shape.

---

## Uniqueness

Given one or more columns, digna groups the snapshot by them and keeps only the groups occurring exactly once. Rows that join to that set pass; everything else fails.

The consequence worth knowing: **every row of a duplicated key is counted as failing**, not just the surplus copies. A key appearing three times contributes three failed records. That is the honest count — you cannot tell which of the three is the right one — but it matters when setting an absolute threshold.

Multiple columns make a composite key. The check is on the combination, not on each column separately.

---

## Referential Integrity

Given a set of columns here and a matching set on another table, digna keeps the distinct values from the other table and fails any row that does not join.

The two column lists must be the same length. A mismatch is rejected outright rather than silently checking a weaker condition — a two-column key compared against one column would let through records the full key would have caught.

---

## Thresholds

Counting failures is not the same as deciding whether the run is acceptable. Each rule carries its own thresholds in one of two modes:

| Mode | Compared quantity | Suits |
|---|---|---|
| **Absolute** | The number of failed records | Rules where any breach matters, and small fixed tolerances |
| **Relative** | Failed records ÷ records evaluated | Rules applied across tables of very different sizes |

Each mode has two levels:

| Condition | Status |
|---|---|
| Above the **Warn threshold** | **Failed** |
| Above the **Info threshold** | **Uncertain** |
| Otherwise | **Passed** |

Both default to zero, so a new rule fails on a single bad record until you say otherwise. That is the right default for a compliance rule and the wrong one for a rule over data with a known, accepted tail of exceptions — set the **Info threshold** to that tail and the **Warn threshold** above it.

!!! warning "Relative thresholds are fractions, not percentages"
    A relative threshold of `0.01` means one per cent. It is compared directly against `failed ÷ (passed + failed)`.

---

## Inspecting Failures

An aggregate count tells you a rule broke; it does not tell you what to fix. For every rule digna can return **the failing records themselves** — the same query, with the pass condition negated instead of counted.

This is how a finding becomes actionable: the process owner receives the rows, not the number. Results are exportable, which is also what makes them usable as audit evidence rather than only as an operational signal.

---

## Portability

From **Release 2026.06**, validation rules can be exported and imported. That turns a rule set into something you can promote between environments, keep in version control, and reuse across projects — see the [Release 2026.06 changelog](../../changelog/Release_202606.md).

---

## Where It Runs

Like every digna module, validation executes **inside the source database**. digna sends SQL and receives counts, plus the failing rows when you ask for them. No table is copied out to be checked.

Validation is also **independent of the other modules**. It reads none of the [profiling statistics](../profiling/Introduction.md) — its rules are evaluated row by row against the same snapshot, in the same pass, but the two produce entirely separate results. A data source can therefore run validation with anomaly detection switched off, and its statuses roll up the same way: check → attribute → dataset → data source, worst result winning.

---

## Related Pages

- [Data Validation – Introduction](Introduction.md)
- [Data Validation – Use Cases](use_cases.md)
- [Datasets](../profiling/datasets.md)
- [Changelog – Release 2026.06](../../changelog/Release_202606.md)

---