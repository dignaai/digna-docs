# Anomaly Tuning

---

## Two Questions, Two Sets of Dials

Anomaly detection asks two separate questions, and they are tuned separately:

| Question | Answered by | Where |
|---|---|---|
| **What should this value be?** | The prediction model | **Model Configuration** — seven dials |
| **How far may it stray before we say something?** | The tolerance band | **Threshold Configuration** — Sensitivity and Memory |

Reaching for the wrong set is the most common tuning mistake. If the *expected* value is wrong — the model missed a step change, or is still averaging across a migration — widening the band only hides the problem. If the expected value is right and ordinary noise keeps being reported, the band is what needs adjusting.

Both sets live on the data source's **Data Anomalies** configuration, under the **Model Configuration** and **Threshold Configuration** tabs, and each has a **Restore Defaults** action. **A data source that has never been configured behaves exactly as one explicitly set to the defaults.**

---

## The Tolerance Band

The band is `predicted ± bound`, where the bound is the recent prediction error, weighted and scaled:

```
bound  =  multiplier  ×  weighted mean absolute error of recent predictions
```

### Sensitivity

Sensitivity sets the multiplier. It is expressed as the tail probability the band is drawn at:

| Setting | Tail probability | Band width | Effect |
|---|---|---|---|
| **very low** | 1 % | ≈ 4.6 × error | Only severe deviations are reported |
| **low** | 2.5 % | ≈ 3.7 × error | Quiet |
| **moderate** *(default)* | 5 % | ≈ 3.0 × error | Balanced |
| **high** | 7.5 % | ≈ 2.6 × error | Eager |
| **very high** | 10 % | ≈ 2.3 × error | Reports small deviations |

Remember that the band has two edges: an observation past **one** bound is Uncertain, past **two** it is Failed. Raising sensitivity narrows both.

### Memory

Memory decides how quickly an old prediction error stops counting toward the bound. Errors are weighted over a rolling window of just over a year:

| Setting | Weighting | Best for |
|---|---|---|
| **short** | Fades quadratically — the last few weeks dominate | Series that legitimately change character; recent behaviour is the only relevant reference |
| **moderate** *(default)* | Fades linearly over the year | Most data sources |
| **long** | Flat — an error from a year ago counts as much as yesterday's | Stable, seasonal series where a full year of behaviour is the right reference |

!!! tip "The quiet-series trap"
    A metric that has been perfectly steady produces a near-zero bound, and the first ordinary fluctuation is reported as a failure. The fix is not a lower sensitivity — it is a **`min_threshold`** on the statistic mapping, which puts a floor on how narrow the band may become. See [Profiling Statistics](../profiling/statistics.md#turning-statistics-off).

---

## The Prediction Model

Before the band is applied, digna predicts what the value should be. The model is a robust regression fitted per series, and it selects its own structure:

- **Always in the design:** an intercept, plus a level-shift dummy for each detected structural break.
- **Candidates that must earn their place:** a linear trend, the previous observation, the one before that, weekday effects, within-month seasonality, month-boundary spikes, and within-year seasonality.

Candidates are admitted by forward selection under a penalised criterion, so a weekly pattern enters the model only when the data genuinely shows one. A seasonal category is estimated only when at least three observations fall into it, and a series with fewer than five usable observations gets no model at all — its median is used instead.

The fit is robust: observations are reweighted over several passes so a single spike cannot drag the line, and up to two structural breaks may be absorbed.

---

## The Seven Prediction Dials

Every dial runs from `0.0` to `1.0` and defaults to `0.5`, which is the setting the model was tuned and backtested at. **Higher always means more sensitive** — quicker to see a regime change, quicker to call something an outlier, tighter around the recent level.

| Dial | What it decides | Low `0.0` | High `1.0` |
|---|---|---|---|
| **Break Sensitivity** | How readily a level shift is accepted as a structural break, after which the model predicts from the new level instead of averaging across the step | Only extreme jumps qualify | Ordinary noise starts being split into regimes |
| **Outlier Sensitivity** | How readily a single observation is dismissed rather than fitted | Essentially a plain least-squares fit that any spike drags with it | A good share of clean data is discarded |
| **Memory** | How quickly older observations fade from the fit | Short memory — recent behaviour only | Long memory — years of history still counts |
| **Ridge Strength** | How hard the fit is stabilised when its features tell nearly the same story | Safety net effectively off; a degenerate fit fails outright | Coefficients shrunk harder |
| **Gap Tolerance** | How stale the previous observation may be before the model stops reading anything into it | Even regular observations are rejected; nothing is carried over | The last value is trusted no matter how old |
| **Outlier Correction** | When a downweighted observation is replaced by its fitted value, so an outlier cannot leak into the next prediction by being the previous observation | Nothing is ever corrected | Nearly the whole series is fed back as fitted values |
| **Plausible Range Tightness** | How tightly the prediction is held to the range the series has recently occupied — the last guard against a trend running away | A wide band lets an extrapolation run | Little beyond what has already been observed is allowed |

**Ridge Strength** is a safety net rather than a modelling choice; it keeps the solution well defined and is rarely the right dial to turn.

---

## Which Dial to Reach For

| Symptom | Likely cause | First thing to try |
|---|---|---|
| Every day after a migration or replatform is flagged | The model is averaging across a step change | Raise **Break Sensitivity** |
| A one-off spike causes alerts for days afterwards | The spike entered the fit and became the previous observation | Raise **Outlier Sensitivity**, then **Outlier Correction** |
| A source with weekend gaps alerts every Monday | The gap is being treated as a stale value | Raise **Gap Tolerance** |
| Predictions drift far above anything the series has done | An extrapolating trend | Raise **Plausible Range Tightness** |
| The model is still using behaviour from before a permanent change | Too much history in the fit | Lower **Memory** |
| A perfectly steady metric alerts on trivial movement | The bound collapsed to near zero | Set a **`min_threshold`** on the mapping |
| Too many small deviations reported across the board | The band is too narrow for this source | Lower **Sensitivity** |

!!! warning "Change one dial at a time"
    The dials interact — Break Sensitivity and Memory in particular both change what the model considers current. Move one, let a few inspections run, and judge the result before moving another. If several are off the defaults and the behaviour is worse than when you started, reset them and change one.

---

## Related Pages

- [Statuses and Alerts](statuses.md)
- [Statistics](../profiling/statistics.md)
- [Data Anomalies – How It Works](../data_anomalies/how_it_works.md)
- [Data Timeliness – How It Works](../data_timeliness/how_it_works.md) — the same band machinery applied to arrival times

---