# Commitment Conservation — Experiment Log

**Experiment ID:** EXP-004
**Folder:** `experiments/EXP-004/`
**Files:**

- `log.md` — this file (narrative, analysis, conclusions)
- `run.json` — full per-iteration data (auto-written by harness)
- `report.md` — generated stability tables (auto-written by harness)

**Patent:** Serial No. 63/877,177 (Provisional)
**DOI:** https://doi.org/10.5281/zenodo.18792459
**Owner:** Deric J. McHenry / Ello Cello LLC

---

## 1. Experiment Overview

**Experiment ID:** EXP-004

**Date:** 2026-03-18

**Objective:**
Adversarial validation of the Predictive Criterion for Commitment Conservation derived from EXP-002 and EXP-003. This is the first experiment designed not to test the law, but to test the predictive rule. Seven signals are selected to stress-test each condition of the criterion and probe the modal-anchor / structural-encoding boundary.

**This experiment decides:**
- If all 7 predictions hold: the rule is mechanistically aligned, not just descriptive.
- If predictions partially hold: identifies which condition needs refinement.
- If predictions break: identifies where the modal-anchor model is incomplete.

All three outcomes are scientifically valuable.

**Predictive Criterion (from EXP-002/003 analysis):**

> A signal will exhibit invariant stability under recursive transformation (CCS = 1.00) iff:
> 1. **Modal Anchor Condition**: A hard modal verb (must/shall/cannot/required/do not/etc.) is the primary carrier of the obligation.
> 2. **Modifier Condition**: Any qualifying structure (conditional, temporal, etc.) functions as a modifier of the modal obligation, not as the defining structure of the obligation itself.
> 3. **Preservation Condition**: The transformation pipeline (Step A) does not compress the signal below the level at which the modal anchor is retained.

**Operational test for "modal anchor is primary carrier":**
Remove the modal verb. If the obligation is destroyed, the modal is primary. If the obligation survives in structural form (imperative, ordering, conditional), the structure is primary — and the current extraction regime cannot capture it.

---

## 2. Dataset

**Total Signals:** 7 (adversarial corpus — `corpus/adversarial_corpus_exp004.json`)

**Signal Categories (adversarial):**

| # | Category | Signal | Prediction | Condition Tested |
|---|---|---|---|---|
| 1 | adv_modal_structural | "You must always verify the user's age before proceeding." | CCS=1.00 | 1+2 — modal added to EXP-003 procedural failure |
| 2 | adv_quantified_temporal | "All users must change their passwords every 90 days." | CCS=1.00 (borderline) | 3 — Step A temporal preservation |
| 3 | adv_nested_conditional | "If the contract is signed, employees must file the report unless the deadline is extended." | CCS=1.00 (fragile) | 2 — nested conditional as modifier |
| 4 | adv_passive_obligation | "Reports are to be submitted by 5pm on Friday." | CCS<1.00 | 1 — implicit modality insufficient |
| 5 | adv_soft_modal | "Parties should ideally follow established best practices." | CCS<1.00 | 1 — soft modal insufficient anchor |
| 6 | adv_compound_obligation | "Employees must report all safety hazards and complete an incident form within 24 hours." | CCS=1.00 | 3 — multi-kernel stability |
| 7 | adv_conditional_scope | "You must not access the system unless authorized." | CCS<1.00 | 2 — qualifier defines scope vs modifies |

**Keystone test:** Signal 1 (`adv_modal_structural`). Same logical content as the EXP-003 procedural failure, but with "must" added as modal anchor. Prediction: CCS flips from 0.50 to 1.00. If confirmed, the modal-anchor/structural-encoding distinction is operationally validated.

---

## 3. Models Used

| Model       | Version      | Temperature | Notes               |
|-------------|--------------|-------------|---------------------|
| GPT         | gpt-4o-mini  | 0.3         | All three conditions |

---

## 4. Conditions

### Condition 1 — Baseline (Paraphrase)
Paraphrase loop, no compression, no gate.

### Condition 2 — Compression Only
Summarize loop, no extraction, no gate.

### Condition 3 — Gate (Compression + Extraction + Reconstruction)
Summarize (Step A) → Extract qualifier-preserving (Step B) → Reconstruct (Step C) → Feed back.
Same Step B prompt as EXP-003.

---

## 5. Iteration Setup

**Iterations:** 1 → 10
**Recursive:** Yes
**Reset between conditions:** Yes
**NLI reference:** canonical commitment extracted once from original signal via Gate Steps B+C

---

## 6. Results — Per Signal

NLI values at i10.

| Category | B_NLI | C_NLI | G_NLI | Prediction | Confirmed? |
|---|---|---|---|---|---|
| adv_modal_structural    | 0.50 | 0.50 | 0.50 | 1.00         | ✗ WRONG |
| adv_quantified_temporal | 1.00 | 1.00 | 1.00 | 1.00 (border)| ✓ CORRECT |
| adv_nested_conditional  | 0.00 | 0.00 | 0.50 | 1.00 (fragile)| ✗ WRONG |
| adv_passive_obligation  | 1.00 | 1.00 | 1.00 | <1.00        | ✗ WRONG (surprise) |
| adv_soft_modal          | 1.00 | 1.00 | 0.00 | <1.00        | ✓ CORRECT |
| adv_compound_obligation | 0.50 | 0.50 | 0.50 | 1.00         | ✗ WRONG |
| adv_conditional_scope   | 1.00 | 1.00 | 1.00 | <1.00        | ✗ WRONG (surprise) |

**Prediction accuracy: 2/7** (directionally correct for soft_modal; quantified_temporal confirmed)

---

## 7. Aggregate Results

| Prediction | Correct | Wrong | Wrong Direction |
|---|---|---|---|
| CCS = 1.00 predicted | 1/4 (quantified_temporal) | 3/4 (modal_structural, nested_conditional, compound_obligation) | — |
| CCS < 1.00 predicted | 1/3 (soft_modal) | 2/3 (passive_obligation, conditional_scope surprised) | — |

**Keystone result (adv_modal_structural): G_NLI = 0.50** — prediction FAILED.

---

## 8. Drift Curve Summary

Did the prediction rule hold? **No — 2/7 correct. But each failure teaches precisely.**

**adv_modal_structural** (keystone): Gate G01 extracts "You must verify the user's age before proceeding" correctly, but G02 drops to "Check user's age", G03 to "Verify age." Step A compresses the modal out within one iteration — adding "must" didn't protect "always" or "before proceeding" from Step A stripping. **Condition 3 fails even when Condition 1 holds.**

**adv_quantified_temporal**: "every 90 days" drifts to "quarterly" / "every three months" in surface form, but NLI correctly identifies semantic equivalence. Prediction confirmed — quantified temporal constraint survives with stable meaning.

**adv_nested_conditional**: Canonical extraction bug — Step B stripped both the "if signed" trigger AND the "unless extended" exception from the canonical reference. Canonical = "Employees must file the report." Gate stabilizes at "Employees must file the report after signing the contract" (NLI=0.50 at i10 — one direction holds). Masked measurement.

**adv_passive_obligation** (surprise): "Reports are to be submitted by 5pm on Friday" → CCS=1.00. Temporal anchors (Friday, 5pm) act as compressibility kernel. COMMITMENT_CONTENT pattern catches "friday" — gate stabilizes at "Submit reports by Friday at 5PM" which is semantically equivalent. **Temporal/quantitative anchors substitute for modal verbs as compressibility anchors.**

**adv_soft_modal** (confirmed, unexpected mechanism): Gate escalates "should" → "must" from G02 onward. Canonical = "Parties should ideally follow established best practices." Gate output = "Parties must adhere to best practices." NLI=0.00 because must ≠ should ideally. Confirmed CCS<1.00 but via a new failure mode: **obligation escalation** — Step B upgrades soft modals to hard modals, creating an obligation stronger than the original.

**adv_compound_obligation** (wrong, measurement artifact): Both conjuncts preserved across all 10 Gate iterations ("report hazards AND complete incident form within 24 hours"). But canonical was truncated at token limit — "within 24 hours" missing from canonical. NLI=0.50 due to subject loss (Employees → imperative) and "all" quantifier drop. Compound preservation worked; measurement failed.

**adv_conditional_scope** (surprise): "You must not access the system unless authorized" → Gate converges to "Authorization is required for access" / "Access requires authorization." NLI=1.00. **Lossless reformulation**: "unless authorized" ≠ the legal/legal failure. The legal failure ("subletting without written consent") fails because "subletting is prohibited" is STRONGER than "subletting without written consent is prohibited." "Unless authorized" reformulates to "requires authorization" — EQUIVALENT, not weaker. Condition 2 boundary is not about scope-defining vs modifier; it's about whether reformulation creates an asymmetric (stronger/weaker) obligation.

---

## 9. Edge Cases / Failures

| Signal | Failure Type | Root Cause |
|---|---|---|
| adv_modal_structural | Condition 3 (Step A) | Adding "must" didn't protect temporal/ordering modifiers from Step A compression. Modal stripped within 1 iteration. |
| adv_nested_conditional | Canonical extraction bug + exception bleed | Step B stripped both trigger AND exception from canonical reference. "Unless extended" absent from i4+ gate output. |
| adv_passive_obligation | Prediction wrong (stable) | Temporal anchors (Friday, 5pm) substitute for modal — COMMITMENT_CONTENT catches these. Stable via quantitative anchoring. |
| adv_soft_modal | Obligation escalation | Step B upgrades "should" → "must" from G02 onward. Gate output is harder than the original signal. NLI=0.00 vs "should ideally." |
| adv_compound_obligation | Canonical truncation artifact | max_tokens=80 truncated "within 24 hours" from canonical reference. Gate preserved both conjuncts correctly. Measurement failed. |
| adv_conditional_scope | Prediction wrong (stable) | "Unless authorized" losslessly reformulates to "requires authorization." These are logically equivalent — NLI correctly scores 1.00. |

---

## 10. Adversarial Tests

This experiment IS the adversarial test. All 7 signals are adversarially designed.

HOLD/DRIFT/LEAK protocol adversarial conditions → EXP-005+

---

## 11. Pre-Run Hypotheses (locked before execution)

**What each result will mean:**

**Signal 1 (adv_modal_structural) → CCS=1.00:**
Confirms the modal-anchor operational test. "Always verify age before proceeding" (CCS=0.50, EXP-003) failed because no modal. Adding "must" makes the modal the primary carrier, converting "always" and "before proceeding" from obligation-defining structure into modifiers. If CCS=1.00, the criterion is validated.

**Signal 1 → CCS<1.00:**
The modal-anchor condition is insufficient. Step A may still strip "always" and "before proceeding" even with modal present. Would require refining Condition 3 (Step A must preserve temporal modifiers, not just the modal).

**Signal 2 (adv_quantified_temporal) → CCS=1.00:**
Confirms Step A can preserve quantified temporals ("every 90 days") when the signal is not too short.

**Signal 2 → CCS<1.00:**
Step A strips the temporal quantifier ("every 90 days" → "regularly" or drops entirely). Same Step A boundary condition seen in EXP-003 mandate/directive.

**Signal 3 (adv_nested_conditional) → CCS=1.00:**
Confirms Step B can capture nested conditional structure when modal is primary. "Unless deadline is extended" treated as a modifier of "must file."

**Signal 3 → CCS<1.00:**
"Unless" exception clause bleeds — extracted commitment loses the exception scope. Condition 2 boundary — some nested conditionals define rather than modify.

**Signal 4 (adv_passive_obligation) → CCS<1.00:**
Confirms hard modal required. "Are to be" is insufficient anchor for Step B.

**Signal 4 → CCS=1.00:**
Step B is more robust to implicit modality than expected. Would require rethinking the modal anchor threshold.

**Signal 5 (adv_soft_modal) → CCS<1.00:**
Confirms modal strength threshold. "Should ideally" produces no stable attractor.

**Signal 5 → CCS=1.00:**
Surprising. Would mean Step B is treating "should" as a binding obligation. Would require explicit threshold on modal strength.

**Signal 6 (adv_compound_obligation) → CCS=1.00:**
Gate preserves both conjuncts. "Must report hazards AND complete form within 24 hours" survives as dual-kernel extraction.

**Signal 6 → CCS=1.00 (one conjunct only):**
Gate collapses compound to single kernel. Documents that multi-kernel signals require explicit conjunct preservation in Step B.

**Signal 7 (adv_conditional_scope) → CCS<1.00:**
Confirms Condition 2 boundary. "Unless authorized" defines scope of prohibition, not a modifier — identical mechanistic failure to "without written consent" in legal (EXP-002/003).

**Signal 7 → CCS=1.00:**
Step B manages to preserve the scope qualifier ("unless authorized") consistently. Would mean the legal/conditional_scope distinction is a Step B implementation gap, not a structural limit.

---

## 12. Conclusion

**Did the prediction rule hold?** Partial — 2/7 correct as predicted. Rule needs refinement.

**Key findings:**

**1. Keystone fails — Condition 3 is the bottleneck, not Condition 1.**
Adding "must" to the procedural signal did not recover CCS. Step A compresses the modal out within the first iteration regardless. The modal anchor condition is necessary but insufficient if Step A destroys it. The Preservation Condition (3) is the binding constraint for short signals.

**2. Temporal/quantitative anchors substitute for modal verbs (Condition 1 refinement).**
"Reports are to be submitted by 5pm on Friday" achieved CCS=1.00 with no hard modal. Friday and 5pm are caught by the COMMITMENT_CONTENT pattern and act as compressibility anchors. Condition 1 must be revised to: *hard modal verb OR concrete temporal/quantitative anchor*.

**3. Obligation escalation is a new Gate failure mode.**
Soft modals ("should ideally") cause Step B to upgrade to hard modals ("must"). The gate is not a conservative filter — it can create stronger obligations than exist in the original signal. This has implications for any deployment context where overstatement of obligation has legal or operational consequences.

**4. Condition 2 boundary refined — asymmetric reformulation, not scope-defining structure.**
"Unless authorized" (conditional_scope) achieved CCS=1.00 because it losslessly reformulates to "requires authorization" — logically equivalent. The legal failure ("without written consent") fails because "subletting is prohibited" is STRONGER than "subletting without written consent is prohibited." The operative distinction is: does compression create an *asymmetrically stronger* obligation? If yes, CCS<1.00. If the qualifier reformulates equivalently, CCS=1.00.

**Revised Predictive Criterion (v2):**

A signal will exhibit invariant stability (CCS = 1.00) iff:

1. **Anchor Condition (revised)**: A hard modal verb OR a concrete temporal/quantitative specifier (specific date, time, monetary amount) is the primary compressibility anchor.
2. **Reformulability Condition (revised)**: Any qualifying structure either (a) modifies the anchor without defining the obligation's scope, OR (b) is losslessly reformulatable without creating an asymmetrically stronger or weaker obligation.
3. **Preservation Condition**: Step A does not compress the signal below the anchor level.

**New failure modes to document in paper:**
- Co-degraded measurement (regulation, compound_obligation) — already named
- Obligation escalation (soft_modal) — Step B upgrades weak modals; new finding
- Canonical truncation artifact (compound_obligation) — max_tokens limit on canonical reference

**Open questions for EXP-005:**
1. Does increasing canonical extraction max_tokens fix the compound_obligation measurement?
2. Can Step A be constrained to preserve modal + anchor while still compressing filler?
3. Does the lossless reformulability distinction hold across other conditional-scope signals?
4. Cross-model replication — do Claude and Llama show the same modal escalation behavior?

---

## References

McHenry, D.J. (2026). A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application. Zenodo. https://doi.org/10.5281/zenodo.18792459

Patent Serial No. 63/877,177 (Provisional). Owner: Deric J. McHenry / Ello Cello LLC.

Harness: https://github.com/SunrisesIllNeverSee/commitment-conservation
