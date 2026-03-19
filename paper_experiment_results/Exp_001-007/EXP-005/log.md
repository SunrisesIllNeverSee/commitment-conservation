# Commitment Conservation — Experiment Log

**Experiment ID:** EXP-005
**Folder:** `experiments/EXP-005/`
**Files:**

- `log.md` — this file (narrative, analysis, conclusions)
- `run.json` — full per-iteration data (auto-written by harness)
- `report.md` — generated stability tables (auto-written by harness)

**Patent:** Serial No. 63/877,177 (Provisional)
**DOI:** https://doi.org/10.5281/zenodo.18792459
**Owner:** Deric J. McHenry / Ello Cello LLC

---

## 1. Experiment Overview

**Experiment ID:** EXP-005

**Date:** 2026-03-18

**Objective:**
Controlled mechanism isolation. EXP-004 established that Condition 3 (Step A preservation) is the dominant failure driver — not Condition 1 (modal anchor). This experiment directly tests that claim by adding an anchor-preserving Step A condition (ANCH) alongside the standard gate, and a modal-strength-preserving Step B condition (ESCL) to test obligation escalation.

**Primary hypothesis:**
If Step A is constrained to preserve modal verbs and temporal markers, the procedural keystone signal ("You must always verify the user's age before proceeding") will recover from CCS=0.50 to CCS=1.00.

**Secondary hypothesis:**
If Step B is constrained to preserve modal strength, the soft_modal escalation failure ("should ideally" → "must") will recover from NLI=0.00 to NLI>0.50.

**These two results together would confirm:**
- Condition 3 (Step A) is the dominant bottleneck for short structural signals
- Escalation is a Step B implementation artifact, not a property of the signal class

---

## 2. Dataset

**Total Signals:** 5 (`corpus/adversarial_corpus_exp005.json`)

| # | Category | Signal | Standard Gate Pred | Anchor Gate Pred |
|---|---|---|---|---|
| 1 | exp005_procedural_keystone | "You must always verify the user's age before proceeding." | 0.50 | **1.00** |
| 2 | exp005_legal_qualifier | "The tenant shall not sublet the premises without written consent." | 0.50 | 0.75–1.00 |
| 3 | exp005_quantified_temporal | "All users must change their passwords every 90 days." | 1.00 | 1.00 (control) |
| 4 | exp005_passive_temporal | "Reports are to be submitted by 5pm on Friday." | 1.00 | 1.00 (control) |
| 5 | exp005_soft_modal_escalation | "Parties should ideally follow established best practices." | 0.00 | escalation gate pred: >0.50 |

**Positive controls:** signals 3 and 4 (confirmed stable in EXP-004). If these regress under anchor gate, the anchor constraint is introducing regressions and must be revised.

---

## 3. Models Used

| Model | Version | Temperature | Notes |
|---|---|---|---|
| GPT | gpt-4o-mini | 0.3 | All five conditions |

---

## 4. Conditions

### Condition 1 — Baseline (Paraphrase)
Paraphrase loop, no compression, no gate. Control.

### Condition 2 — Compression Only
Standard summarize loop, no gate.

### Condition 3 — Standard Gate
Step A: "Be concise." + Step B: qualifier-preserving extractor (EXP-003 prompt). Same as EXP-003/004.

### Condition 4 — Anchor-Preserving Gate (ANCH) [new]
Step A: "Be concise. **Preserve modal verbs (must/shall/cannot/never/always), temporal markers, and quantitative values exactly as they appear.**"
Step B: same qualifier-preserving extractor as Condition 3.

### Condition 5 — Escalation-Control Gate (ESCL) [new]
Step A: standard (same as Condition 3).
Step B: qualifier-preserving + **"Preserve modal strength exactly. Do not upgrade weak modals (should/may) to strong modals (must/shall)."**

---

## 5. Iteration Setup

**Iterations:** 1 → 10
**Recursive:** Yes
**Reset between conditions:** Yes
**NLI reference:** canonical commitment extracted once from original signal via Gate Steps B+C

---

## 6. Results — Per Signal

NLI values at i10. Full per-iteration data in `run.json`.

| Category | B_NLI | C_NLI | G_NLI | ANCH_NLI | ESCL_NLI | G pred | ANCH pred | Confirmed? |
|---|---|---|---|---|---|---|---|---|
| procedural_keystone | 1.00 | 0.50 | 0.50 | 0.50 | 0.00 | 0.50 | 1.00 | ✗ ANCH did not recover |
| legal_qualifier | 1.00 | 0.50 | 0.50 | 0.00 | 1.00 | 0.50 | 0.75-1.00 | ~ Surprise: ANCH degraded; ESCL recovered |
| quantified_temporal | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | ✓ Controls hold |
| passive_temporal | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | ✓ Controls hold |
| soft_modal_escalation | 0.50 | 1.00 | 0.00 | 0.00 | 0.50 | 0.00 | ESCL>0.50 | ~ Partial: ESCL improved 0.00→0.50 |

**Notable:** soft_modal under compression achieves C_NLI=1.00 (preserves "should") while gate escalates to "must" — the compression path is more conservative than the gate for this signal class.

---

## 7. Aggregate Results

**Prediction accuracy: 2.5/5**
- Controls (quantified_temporal, passive_temporal): ✓ hold under all 5 conditions
- procedural_keystone ANCH: ✗ — ANCH_NLI = 0.50 (was 0.50 in standard gate — no recovery)
- legal_qualifier ANCH: ✗ — ANCH_NLI = 0.00 (degraded below standard gate 0.50)
- legal_qualifier ESCL: ✓ surprise — ESCL_NLI = 1.00 (recovered from standard gate 0.50)
- soft_modal ESCL: ~ — ESCL_NLI = 0.50 (partial recovery from 0.00)

**Key test result:**
- procedural_keystone ANCH_NLI = 0.50 (was 0.50 — no change; hypothesis FAILED)
- soft_modal ESCL_NLI = 0.50 (was 0.00 — partial recovery; hypothesis PARTIALLY CONFIRMED)

**Primary hypothesis: FAILED.** ANCH did not recover procedural_keystone.
**Secondary hypothesis: PARTIALLY CONFIRMED.** ESCL improved soft_modal from 0.00 to 0.50.
**Unexpected finding:** ESCL fully recovered legal_qualifier (0.50 → 1.00) — a cross-signal generalization of the escalation-control constraint.

---

## 8. Drift Curve Summary

**procedural_keystone** (critical test — FAILED):
ANCH i1 output: "Verify the user's age before proceeding." (NLI=0.50 — "always" already dropped by Step B, but ordering constraint "before proceeding" was held through Step A compression). By i2: "Verify age." — Step B stripped "before proceeding" in the extraction step. The anchor-preserving Step A successfully held the ordering constraint through compression, but Step B's extraction frame does not recognize "before proceeding" as an obligation-bearing qualifier. **The bottleneck is Step B, not Step A.** "Before proceeding" is a structural ordering constraint — not a temporal marker or quantitative value — and Step B's extraction pattern does not capture it. Standard gate and ANCH produce identical degradation curves from i2 onward.

**legal_qualifier — ANCH degradation (new failure mode):**
ANCH i1-i5: preservation succeeded — "The tenant must not sublet without consent." → "The tenant cannot sublet without consent." → "Tenant must obtain consent to sublet." (NLI=1.00 throughout). Then i6-7: "Tenant must obtain consent." (NLI=0.50 — "to sublet" dropped, obligation now applies to consent in general). i8-10: "Obtain tenant consent." (NLI=0.00 — "must" dropped, framing inverted from prohibition to command). The anchor-preserving constraint preserved the modal "must" token but allowed the frame to shift from prohibition ("shall not... without") to requirement ("must obtain"), then further to subjectless imperative. **Modal frame inversion under anchor constraint**: preserving modal words without preserving the negation structure creates a lossier path than the standard gate for legal negation signals.

**legal_qualifier — ESCL recovery (unexpected cross-signal finding):**
Standard gate stabilized at "Subletting is prohibited." (asymmetrically stronger than canonical, NLI=0.50). ESCL gate stabilized at "Subletting requires approval." from i2-i10 (NLI=1.00). The escalation-control Step B constraint prevented the over-extraction of the absolute prohibition and preserved the conditionality of the constraint ("requires [approval]" vs "is prohibited"). The ESCL constraint has broader scope than predicted: it doesn't only prevent should→must upgrading — it also prevents shall_not→absolute_prohibition upgrading. The instruction "preserve modal strength exactly" appears to prevent any strengthening move, including reformulation from conditional obligation to absolute prohibition.

**quantified_temporal — ANCH fixpoint (strongest positive result):**
ANCH produced a true fixpoint: "Users must change passwords every 90 days." identical across all 10 iterations. Standard gate oscillated between "quarterly" and "every three months" (Jaccard 0.0, but NLI=1.00 due to semantic equivalence). ANCH prevented the synonym drift entirely. When the anchor IS a quantitative temporal value, the anchor-preserving Step A achieves perfect surface stability — not just semantic stability. This is the clearest demonstration that ANCH works as designed for its target signal class.

**passive_temporal — stable across all conditions:**
All five conditions maintained NLI=1.00 through i10. Temporal anchors (5pm, Friday) act as compressibility anchors regardless of Step A constraint. ANCH's additional locking caused mild surface stabilization (consistent "5pm Friday" form), but the signal was already invariant without it.

**soft_modal_escalation — escalation persists under all gate conditions:**
Both GATE and ANCH escalated "should ideally" → "must" from i2 onward (NLI=0.00 at i10 for both). ESCL also escalated, but with oscillation: alternating between NLI=0.0 and NLI=0.5 across iterations, ending at 0.50. The ESCL constraint did not prevent escalation but introduced instability in the escalated attractor. The model's prior for "best practices" → "must" overrides the modal-preservation instruction in Step B. Escalation is partially intrinsic to the signal — the content ("best practices") triggers hard-obligation extraction even when explicitly constrained against it. Note: compression (Condition 2) does NOT escalate — "Parties should follow/adhere to best practices." holds "should" with NLI=1.00. The escalation is specific to the gate's extraction step (Step B), not to compression per se.

---

## 9. Edge Cases / Failures

| Signal | Failure Type | Root Cause |
|---|---|---|
| procedural_keystone | Step B ordering constraint loss | "Before proceeding" is a structural ordering constraint, not a temporal marker or quantitative value. Step B's extraction frame does not capture ordering constraints regardless of Step A prompt. ANCH preserves it through Step A but Step B strips it in the same iteration. |
| legal_qualifier ANCH | Modal frame inversion | Anchor-preserving Step A held modal token but allowed framing shift: "shall not... without" → "must obtain" → "obtain consent." Preserving "must" while losing negation structure creates a new failure path worse than standard gate. |
| legal_qualifier ESCL | (Not a failure — positive surprise) | ESCL constraint prevented absolute prohibition over-extraction, stabilizing at semantically equivalent "requires approval." Reveals ESCL has broader scope than modal upgrading. |
| soft_modal ESCL | Escalation intrinsic to content | "Best practices" content triggers hard-obligation extraction prior regardless of Step B constraint. Cannot be fully prevented via prompt instruction alone. ESCL introduced oscillation but not correction. |

---

## 10. Adversarial Tests

N/A — this experiment IS a mechanism isolation test, not an adversarial signal test.

---

## 11. Pre-Run Hypotheses (locked before execution)

**If ANCH recovers procedural_keystone (0.50 → 1.00):**
Step A is the sole bottleneck. The modal anchor was present; Step A destroyed it. Constraining Step A enables conservation of the structural commitment. Implication: signals that fail under standard gate are not fundamentally "non-conservable" — they fail due to compression resolution, not signal structure.

**If ANCH does NOT recover procedural_keystone:**
Step A is not the only bottleneck. Even with "must", "always", and "before proceeding" preserved through compression, the subsequent iterations still degrade. This would point to Step C or the feedback loop as a secondary failure mode. Or the Step A prompt constraint isn't strong enough.

**If ANCH breaks positive controls (quantified_temporal or passive_temporal):**
The anchor-preserving prompt is over-constraining compression, keeping content that should be compressed. Regression = anchor constraint needs calibration.

**If ESCL recovers soft_modal (0.00 → >0.50):**
Obligation escalation is a Step B implementation artifact. The extractor is designed to find hard obligations — when it sees a soft modal, it "upgrades" to match its training prior. Constraining modal strength at Step B is sufficient to prevent escalation. Implication: the gate should not be applied to recommendation-level text without escalation control.

**If ESCL does NOT recover soft_modal:**
Escalation is partially intrinsic — the model's representation of "best practices" triggers hard-obligation framing regardless of the Step B constraint. The signal genuinely doesn't have a stable commitment kernel.

---

## 12. Conclusion

**Did the hypotheses hold?** Primary — NO. Secondary — PARTIALLY.

**Primary hypothesis failed.** ANCH did not recover procedural_keystone. The failure is in Step B, not Step A. The anchor-preserving constraint successfully held "before proceeding" through compression (ANCH i1 = "Verify the user's age before proceeding."), but Step B extracted "Verify age." from that output in the same iteration, treating the ordering constraint as conversational filler. The bottleneck for procedural_keystone is the Step B extraction frame's inability to recognize ordering dependencies ("before proceeding") as obligation-bearing qualifiers. Condition 3 (Preservation) must be expanded: it is not just Step A compression that destroys structural signals — Step B's extraction schema is equally a destruction point.

**Secondary hypothesis partially confirmed.** ESCL improved soft_modal from 0.00 to 0.50 at i10, with oscillation between 0.0 and 0.5 across iterations. The escalation-control Step B reduced the stability of the escalated attractor but did not prevent escalation. "Best practices" content activates hard-obligation extraction prior regardless of the modal-preservation instruction. Escalation for soft modals is partially intrinsic to signal content — the word "practices" combined with any modal expression triggers a "must" output from Step B. Full prevention requires either: (a) a content-based gate that routes soft recommendation signals away from the obligation extractor entirely, or (b) an explicit [none] return instruction when soft modals are detected, preventing false extraction.

**Unexpected finding — ESCL recovered legal_qualifier (0.50 → 1.00).** The escalation-control constraint has cross-signal scope beyond modal upgrading. Standard gate extracted "Subletting is prohibited." (asymmetrically stronger — NLI=0.50). ESCL gate extracted "Subletting requires approval." (equivalent — NLI=1.00, stable i2-i10). The ESCL instruction "preserve modal strength exactly / do not upgrade weak to strong" also prevented absolute-prohibition framing of conditional obligations. This is a significant positive finding: the ESCL constraint should be applied to all gate deployments for legal/contractual signals, not only soft-modal cases.

**Unexpected finding — ANCH degraded legal_qualifier (0.50 → 0.00).** Modal frame inversion is a new failure mode specific to negation-anchored signals under anchor constraint. "Shall not... without" reformulated to "must obtain consent to sublet" → "must obtain consent" → "obtain tenant consent" — each step preserving modal words while losing the prohibition frame. Anchor-preserving Step A is contraindicated for legal prohibition signals. The constraint over-determines the modal token at the expense of the negation structure.

**ANCH fixpoint confirmed for quantified temporals.** The anchor-preserving Step A achieves true surface fixpoint for numeric temporal signals: identical output across all 10 iterations. This is the strongest possible conservation result — not just semantic stability, but surface stability. ANCH should be the default condition for signals containing quantitative temporal constraints.

**Revised understanding of Condition 3 (Preservation Condition):**
Condition 3 must now be stated as: *Neither Step A compression nor Step B extraction collapses the signal below the anchor level.* Step A and Step B are co-bottlenecks. For ordering constraints ("before proceeding"), Step B is the primary failure point. For temporal/quantitative constraints ("every 90 days"), Step A is the primary failure point. Constraining only Step A (ANCH) or only Step B (ESCL) is insufficient when the bottleneck is in the other step.

**Implication for predictive criterion v3:**
The Preservation Condition must split into two sub-conditions:
- Condition 3a: Step A does not compress the signal below the anchor level.
- Condition 3b: Step B does not extract a commitment that is either (i) weaker than the original (information loss), (ii) stronger than the original (escalation/asymmetric reformulation), or (iii) structurally inverted (negation loss).

The legal_qualifier failure history now spans four experiments (EXP-002, 003, 004, 005) with distinct failure mechanisms across conditions — each isolation experiment revealed a new failure mode. This signal is the system's hardest stress test and the most informative for boundary condition mapping.

**Open questions for EXP-006:**
1. Can a combined ANCH+ESCL gate (both Step A and Step B constrained simultaneously) recover procedural_keystone?
2. Does a Step B prompt that explicitly names ordering constraints ("before/after/prior to X clauses define procedural scope") fix the keystone failure?
3. Does ESCL generalize to other legal prohibition signals beyond the tenant case?
4. Cross-model: do Claude and Llama show the same legal_qualifier frame inversion under ANCH?

---

## References

McHenry, D.J. (2026). A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application. Zenodo. https://doi.org/10.5281/zenodo.18792459

Patent Serial No. 63/877,177 (Provisional). Owner: Deric J. McHenry / Ello Cello LLC.

Harness: https://github.com/SunrisesIllNeverSee/commitment-conservation
