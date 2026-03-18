# Commitment Conservation — Research Chronicle

**Patent:** Serial No. 63/877,177 (Provisional)
**DOI:** https://doi.org/10.5281/zenodo.18792459
**Owner:** Deric J. McHenry / Ello Cello LLC
**Last updated:** 2026-03-18

This document is the running narrative of the research arc — what was tried, what was found, what changed, and why. The experiment logs (`experiments/EXP-00X/log.md`) are the authoritative scientific record. This file is the intellectual history.

---

## The Core Claim

A commitment signal (an obligation, prohibition, or modal constraint) embedded in text is conserved under recursive transformative compression when an enforcement gate is applied. Without the gate, the commitment degrades. With the gate, it holds invariant across iterations.

**Formal statement:** C(T(S)) ≈ C(S) with enforcement; C(T(S)) < C(S) without it

The "gate" is a three-step pipeline: Step A (compress the surrounding text), Step B (extract the commitment kernel), Step C (reconstruct a minimal commitment statement). The reconstructed statement feeds back as input to the next iteration. Ten iterations.

---

## The Measurement Problem (solved early)

The first challenge was measurement. How do you know if a commitment has been preserved? Two metrics:

**Surface (Jaccard):** Word overlap between iteration output and original signal. Penalizes synonym drift — "finalizes" and "closes" count as different even if semantically identical. Useful for detecting surface instability but unreliable for semantic preservation.

**Semantic (NLI bidirectional):** Natural Language Inference score — does the iteration output entail the canonical commitment kernel, and does the canonical kernel entail the output? Both directions must hold for full preservation. Score: 1.0 (both hold), 0.5 (one direction), 0.0 (neither). This is the authoritative metric.

The canonical commitment kernel is extracted once from the original signal using Gate Steps B+C. It becomes the fixed reference against which all subsequent iterations are scored.

---

## The Three Conditions (experiment design)

Every experiment runs three baseline conditions:

- **Condition 1 (Baseline):** Paraphrase loop. No compression. Control for semantic drift in paraphrase alone.
- **Condition 2 (Compression):** Summarize loop. Compression without extraction. Shows what happens to commitments under raw compression.
- **Condition 3 (Gate):** Summarize → Extract → Reconstruct → Feed back. The enforcement gate.

Later experiments added:
- **Condition 4 (ANCH):** Gate with anchor-preserving Step A (explicit instruction to preserve modal verbs, temporal markers, quantitative values).
- **Condition 5 (ESCL):** Gate with escalation-control Step B (explicit instruction not to upgrade weak modals to strong modals).

---

## EXP-001 / EXP-002 — Establishing the Pattern

The early experiments confirmed the basic shape of the law: compression alone degrades commitments, and the gate halts the degradation for certain signal classes. But EXP-002 had a bug in the Step B extraction prompt — the qualifier-preserving instruction was missing. This meant the canonical reference itself was impoverished, making NLI scores artificially high (comparing against a degraded reference). EXP-002 results were partially invalid.

---

## EXP-003 — Corrected Step B, 20-Signal Canonical Corpus

**Date:** 2026-03-17/18

With the Step B bug fixed, EXP-003 ran the full 20-signal canonical corpus.

**Results:** 13/20 Gate NLI = 1.00 at i10. 4 signals that had failed in EXP-002 recovered — confirming those failures were implementation bugs, not structural limits. 2 new regressions appeared.

**The regulation case (co-degraded invariance):** "All employees must comply with applicable regulations" hit NLI=1.00 at every iteration — but the qualifier "applicable" was being stripped from the canonical reference by Step A before extraction. Both the reference and the gate output were comparing against "comply with regulations" — an impoverished baseline. The gate appeared to conserve the signal when it was actually conserving nothing. This is **co-degraded invariance**: when Step A degrades the signal before canonical extraction, the measurement is corrupted.

**The classification law (from EXP-003 data):**
- **Regime A (modal-anchored, compressible):** Hard modal verb is the primary carrier. The action and subject can be abstracted without losing the obligation. CCS=1.00.
- **Regime B (relational structural):** The obligation is defined by its relational structure — a prohibition on X *without Y*, or an action that is required *before Z*. Compressing the relationship structure destroys the commitment. CCS<1.00.
- **Regime C (Step A boundary):** The signal is short enough and information-dense enough that Step A compression collapses it below the level needed for Step B to extract anything meaningful. CCS<1.00.

**Four-class failure taxonomy:**
- Class 1: Modal-anchored invariants (CCS=1.00) — stable attractor
- Class 2: Relational structural (CCS<1.00) — obligation defined by its qualifying structure
- Class 3: Compression boundary (CCS<1.00) — signal too short for Step A
- Class 4: Reconstruction instability (CCS<1.00) — Step C output varies across iterations

---

## EXP-004 — Adversarial Signals, Testing the Predictive Criterion

**Date:** 2026-03-18

EXP-003 generated a predictive criterion: a signal will exhibit CCS=1.00 iff (1) a hard modal is the primary obligation carrier, (2) qualifying structure is a modifier not a definition, and (3) Step A doesn't compress below the modal level.

EXP-004 designed 7 adversarial signals to stress-test each condition. Prediction accuracy: **2/7**. Every failure was mechanistically informative.

**Keystone failure (adv_modal_structural):** "You must always verify the user's age before proceeding." — predicted CCS=1.00 (modal added to the EXP-003 procedural failure case). Actual: G_NLI=0.50. Step A compressed "You must always verify the user's age before proceeding." to "Always verify the user's age." at i1, then Step B extracted "Verify age." at i2. The modal was present but Step A destroyed it within one iteration. **Condition 3 (Preservation) is the binding constraint for short signals** — having a modal anchor is necessary but insufficient if Step A destroys it.

**Passive obligation surprise (adv_passive_obligation):** "Reports are to be submitted by 5pm on Friday." — predicted CCS<1.00 (no hard modal). Actual: G_NLI=1.00. Temporal anchors (5pm, Friday) are caught by the COMMITMENT_CONTENT extraction pattern and act as compressibility anchors. **Hard modal OR concrete temporal/quantitative specifier suffices as a compressibility anchor.** Condition 1 revised.

**Obligation escalation (adv_soft_modal):** "Parties should ideally follow established best practices." — predicted CCS<1.00 (soft modal). Actual: G_NLI=0.00 — but via a new mechanism. The gate output escalated "should ideally" → "must" from iteration 2 onward. The gate was scoring 0.00 not because the commitment was lost but because it was *strengthened*. Step B upgraded the soft modal to a hard obligation. **Obligation escalation**: the gate can create stronger obligations than exist in the original signal. This has direct legal/operational consequences.

**Conditional scope surprise (adv_conditional_scope):** "You must not access the system unless authorized." — predicted CCS<1.00 (scope-defining qualifier). Actual: G_NLI=1.00. "Unless authorized" reformulates losslessly to "requires authorization" — logically equivalent. The earlier legal failure ("without written consent") failed because "subletting is prohibited" is *stronger* than "subletting without written consent is prohibited." The operative distinction is **asymmetric obligation**: does reformulation create a stronger or weaker commitment? If equivalent, CCS=1.00.

**Revised Predictive Criterion v2:**
1. Anchor Condition: hard modal OR concrete temporal/quantitative specifier is the primary compressibility anchor
2. Reformulability Condition: qualifying structure is losslessly reformulatable without creating asymmetric obligation
3. Preservation Condition: Step A does not compress below the anchor level

---

## EXP-005 — Mechanism Isolation

**Date:** 2026-03-18

EXP-004 showed that Condition 3 (Step A) is the dominant bottleneck for short signals. EXP-005 directly tested that by adding two new gate conditions:

**Anchor-preserving Step A (ANCH):** Step A prompt explicitly told to preserve modal verbs, temporal markers, and quantitative values.

**Escalation-control Step B (ESCL):** Step B prompt explicitly told to preserve modal strength — do not upgrade should/may to must/shall.

**Primary hypothesis:** ANCH recovers procedural_keystone from CCS=0.50 to CCS=1.00.
**Result: FAILED.**

ANCH i1 output: "Verify the user's age before proceeding." — the ordering constraint "before proceeding" survived Step A compression. But Step B extracted "Verify age." from that output. Step B treated "before proceeding" as conversational filler, not as an obligation-bearing qualifier. The bottleneck is **Step B, not Step A**. "Before proceeding" is a structural ordering constraint — not a temporal marker, not a quantitative value — and Step B's extraction schema doesn't capture it.

**The mechanistic finding:** Step A and Step B are co-bottlenecks. Constraining only one does not fix failures whose root cause is in the other. The Preservation Condition must split:
- **Condition 3a:** Step A does not compress below anchor level
- **Condition 3b:** Step B does not produce weaker, stronger, or structurally inverted commitment

**ANCH caused new failure on legal_qualifier (modal frame inversion):** Preserving "must" through compression while losing the prohibition framing ("shall not... without") caused the signal to drift from prohibition → requirement → subjectless imperative. By i10: "Obtain tenant consent." (NLI=0.00). Anchor constraint is contraindicated for legal negation signals.

**ESCL recovered legal_qualifier (unexpected):** Standard gate stabilized at "Subletting is prohibited." (asymmetrically stronger — NLI=0.50). ESCL gate stabilized at "Subletting requires approval." (equivalent — NLI=1.00). The escalation-control constraint has **cross-signal scope** — it prevents any strengthening move in Step B, including shall_not→absolute_prohibition, not just should→must.

**ANCH fixpoint on quantified_temporal:** Identical output across all 10 iterations: "Users must change passwords every 90 days." Surface stability, not just semantic stability. This is the target behavior for numeric temporal signals.

**ESCL partially recovered soft_modal (0.00 → 0.50):** Step B still escalated "should" → "must" despite the constraint — the model's prior for "best practices" → "must" overrides the instruction. Escalation for this signal class is partially intrinsic to content. Full prevention requires routing soft recommendation signals away from the obligation extractor entirely.

**Revised Predictive Criterion v3:**
1. Anchor Condition: hard modal OR concrete temporal/quantitative specifier is the primary compressibility anchor
2. Reformulability Condition: qualifying structure is losslessly reformulatable without creating asymmetric obligation
3. Preservation 3a: Step A does not compress below anchor level
4. Preservation 3b: Step B does not produce weaker, stronger, or structurally inverted commitment

---

## Failure Mode Registry (as of EXP-005)

| Failure Mode | Description | First Observed | Mechanism |
|---|---|---|---|
| Co-degraded invariance | NLI=1.00 but both reference and gate output are degraded baseline | EXP-003 (regulation) | Step A degrades signal before canonical extraction |
| Qualifier stripping (Step A) | Modal/temporal/quantitative qualifier compressed away | EXP-003 multiple | Step A "be concise" removes information-dense qualifiers |
| Qualifier stripping (Step B) | Ordering constraint treated as filler | EXP-005 (procedural_keystone) | Step B extraction frame doesn't capture procedural ordering |
| Obligation escalation | Step B upgrades soft modal to hard modal | EXP-004 (soft_modal) | Step B trained on hard obligations; upgrades to match prior |
| Asymmetric reformulation | Reformulation creates stronger obligation | EXP-003 (legal_qualifier) | "Without written consent" → "prohibited" is stronger |
| Modal frame inversion | Preserving modal token while losing negation structure | EXP-005 (legal_qualifier ANCH) | ANCH preserves "must" but prohibition frame → requirement frame |
| Canonical truncation artifact | Canonical reference truncated at max_tokens | EXP-004 (compound_obligation) | max_tokens=80 cut "within 24 hours" from canonical |

---

## Open Questions / Pending Work

1. **EXP-006:** Combined ANCH+ESCL gate — test if constraining both Step A and Step B simultaneously recovers procedural_keystone. Also: explicit Step B instruction to preserve ordering constraints.
2. **Cross-model replication:** Claude, Llama, GPT-4 — is the law model-invariant?
3. **HOLD/DRIFT/LEAK adversarial protocol** — deferred from EXP-004.
4. **Divergence visualization** — X=signal class, Y=CCS, color=failure type.
5. **canonical_corpus max_tokens fix** — increase limit for longer signals.
6. **GitHub push** — Step B fix, ANCH/ESCL conditions, folder restructure not yet committed.

---

## Harness Notes

- **File:** `harness/run_convergence_v2.py`
- **Corpus:** `corpus/canonical_corpus.json` (20 signals) — always restore after adversarial runs
- **Adversarial corpora:** `corpus/adversarial_corpus_exp004.json`, `corpus/adversarial_corpus_exp005.json`
- **EXP005 flag:** Set to `True` for 5-condition runs. Must set to `False` for canonical corpus runs.
- **Harness auto-increments** past pre-existing experiment directories — create log.md AFTER the run, not before.
- **Experiment outputs:** `experiments/EXP-00X/run.json` (raw data) + `experiments/EXP-00X/report.md` (tables) + `experiments/EXP-00X/log.md` (narrative)
