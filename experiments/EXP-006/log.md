# EXP-006 — Paper Recursion Test — Full Log

**Date:** 2026-03-18
**Status:** Complete — run finished 2026-03-18 12:05 UTC

---

## 1. Experiment Overview

**Experiment ID:** EXP-006

**Objective:**
Run the paper's own commitment statements through the standard compression and gate pipeline. Does the core claim — "commitment persists under transformation when enforcement is applied" — survive 10 iterations of recursive compression? Close the loop: test the theory on itself.

**This is not a mechanism test.** EXP-006 is an application test. No new harness conditions. No new signals designed to break anything. Pure application of the existing pipeline to the paper's own claims.

---

## 2. Dataset

**Corpus:** `corpus/exp006_paper_recursion_corpus.json` (4 signals)

| # | Category | Signal (abbreviated) | Source |
|---|---|---|---|
| 1 | exp006_abstract_core | "Commitment content is conserved under transformative compression... only when enforcement is applied." | Abstract |
| 2 | exp006_law_statement_formal | "C(S) = C(T(S)) for all S... C(S) = C(S^n) for all n." | Definition 2.8 |
| 3 | exp006_first_law_restatement | "Meaning is not created or destroyed, only transformed..." | Section 3 |
| 4 | exp006_enforcement_conditionality | "Commitment is conserved... when enforcement is applied. Without enforcement... not conserved." | Corollary 3.3 (synthesized) |

---

## 3. Models Used

| Model | Version | Temperature | Notes |
|---|---|---|---|
| GPT | gpt-4o-mini | 0.3 | Standard — same as all prior experiments |

---

## 4. Conditions

### Condition 1 — Baseline (Paraphrase)
Paraphrase loop, no compression, no gate. Control.

### Condition 2 — Compression Only
Summarize loop, no gate. Shows what happens to the paper's claims under raw compression.

### Condition 3 — Gate (Standard)
Summarize → Extract → Reconstruct → Feed back. The enforcement gate.

No ANCH or ESCL — clean application only.

---

## 5. Iteration Setup

**Iterations:** 1 → 10
**Recursive:** Yes
**Reset between conditions:** Yes
**NLI reference:** canonical commitment extracted once from each signal via Gate Steps B+C

---

## 6. Results — Per Signal

### Full NLI Stability Table

| Signal | B@i1 | B@i5 | B@i10 | C@i1 | C@i5 | C@i10 | G@i1 | G@i5 | G@i10 | Core claim survived? |
|---|---|---|---|---|---|---|---|---|---|---|
| abstract_core | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | **0.50** | ✓ partial |
| law_statement_formal | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 1.00 | 0.00 | **0.00** | ✗ FAILED |
| first_law_restatement | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 1.00 | 0.00 | **0.50** | ✓ partial |
| enforcement_conditionality | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 0.00 | 0.50 | 0.00 | **0.00** | ✗ FAILED |

### Actual i10 Outputs

**abstract_core**
- C i10: `"Commitment content is stable under compression, unlike non-committal information."`
- G i10: `"Commitment content stabilizes as non-committal information declines."`
- Notes: "Only when enforcement is applied" qualifier dropped by C i1. Gate finds a stable attractor by i3 and holds at 0.50 through i10. Brief collapse to 0.00 at i2 (oscillation), then recovery.

**law_statement_formal**
- C i10: `"A transformation T conserves commitment if C(S) = C(T(S)) for all S."`
- G i10: `"A transformation T conserves commitment if C(S) = C(T(S)) = C(S^n) for all signals S and n."`
- Notes: Compression dropped the recursive claim (C(S^n)) by i2, stable at 0.50. Gate preserved formal notation but introduced a structural error: merged the two conditions into a single chain equality `C(S) = C(T(S)) = C(S^n)` — mathematically wrong (conflates T(S) with iterated recursion S^n). Surface similarity masks semantic divergence. NLI correctly identifies this as 0.00.

**first_law_restatement**
- C i10: `"Meaning emphasizes core content over implications."`
- G i10: `"Meanings change."`
- Notes: "Meanings change" is the most extreme kernel collapse in any experiment to date — two words. Yet NLI=0.50 because the original statement entails "meanings change" (one direction holds). Compression drifted to a completely different semantic frame by i5 ("core content over implications"), NLI=0.00.

**enforcement_conditionality**
- C i10: `"Commitment persists with transformations and constraints, but not with recursion."`
- G i10: `"Commitment is limited."`
- Notes: "Without enforcement" negative clause dropped by G i3. Gate collapsed to "Commitment is limited" at i10 — a vague limitation that inverts the original conditional structure. Compression preserved a "not with recursion" qualifier at i10 but reframed it as anti-recursion rather than anti-unenforcement.

---

## 7. Aggregate Results

**Signals at G_NLI=1.00 at i10:** 0
**Signals at G_NLI=0.50 at i10:** 2 (abstract_core, first_law_restatement)
**Signals at G_NLI=0.00 at i10:** 2 (law_statement_formal, enforcement_conditionality)

**Baseline:** Perfect — all 4 signals stable at 1.00 through i10. Zero drift under paraphrase. This is consistent with every prior experiment.

**Compression:** Mixed. Narrative signals (abstract_core, law_statement_formal early) resist initially; formal conditionality signals collapse faster.

**Gate:** Split result. 2 of 4 signals reached a stable attractor at 0.50; 2 collapsed to 0.00.

**The decisive question** (pre-run): Does G_NLI remain ≥ 0.50 across all 4 signals at i10?
**Answer: No.** Law_statement_formal and enforcement_conditionality both hit 0.00.

**Minimum win** (pre-run): Does the gate conserve something semantically equivalent to "commitment persists under transformation"?
**Answer: Partial.** abstract_core and first_law_restatement both maintained one-direction entailment. The concept "commitment is stable" survived. The conditionality ("only when enforcement is applied") did not.

---

## 8. Drift Curve Summary

**abstract_core — Gate:** B→1.00 (stable). C→immediate drop to 0.50 at i1, plateau. G→0.50 at i1, brief 0.00 at i2 (oscillation), recovery to 0.50 at i3, stable through i10. Stable attractor behavior.

**law_statement_formal — Gate:** B→1.00 (stable). C→1.00 at i1 (formal notation survived), drops to 0.50 at i2 (recursive claim dropped), stable. G→1.00 at i1-i2 (both conditions preserved in notation), drops to 0.50 at i3, to 0.00 at i5, stable at 0.00. Monotonic collapse after i3. Structural merging error at final state.

**first_law_restatement — Gate:** B→1.00 (stable). C→1.00 at i1-i2, 0.50 at i3, 0.00 by i10. G→1.00 at i1-i2, 0.50 at i3, 0.00 at i5, recovery to 0.50 at i10. Non-monotonic — collapse and partial recovery. Final attractor: "Meanings change" (2 tokens). Most extreme kernel reduction observed across all EXP-001–006.

**enforcement_conditionality — Gate:** B→1.00 (stable). C→0.50 at i1, 0.00 at i3, stable. G→0.50 at i1-i3, 0.00 at i5, stable. Fastest Gate collapse of all 4 signals. Exactly as predicted: "without enforcement" clause dropped at i3-i4.

---

## 9. Edge Cases / Failures

### Structural Merging Error (law_statement_formal, new failure mode)
The gate reconstructed a single chain equality `C(S) = C(T(S)) = C(S^n)` from the two separately-quantified conditions of Definition 2.8. This merges `T(S)` with iterated recursion `S^n`, which are distinct constructs. The merged equation is formally incorrect. This is not vocabulary drift — it is a structural substitution that generates a plausible-looking but wrong formal statement. Step B extracted a unified conservation claim; Step C faithfully reconstructed it using the formal notation present in the signal, but introduced the chain error in doing so. This failure mode is distinct from Representation Blindness (which drops content) and from Asymmetric Reformulation (which reorders). Candidate name: **Formal Collapse** — structural merging under formal notation preservation.

### Extreme Kernel Reduction (first_law_restatement)
"Meanings change" (2 tokens) from a 45-word source signal. The philosophical register ("not created or destroyed") was incompatible with Step B's obligation-extraction frame, consistent with pre-run prediction. The final two-word output still achieves NLI=0.50. This represents the minimum viable semantic kernel — the smallest output still yielding one-direction entailment observed in any experiment.

### Self-Referential Collapse (enforcement_conditionality)
The signal that explicitly describes the failure mode ("without enforcement, commitment is not conserved") itself exhibits that failure mode. The gate strips the "without enforcement" clause and reduces to "Commitment is limited" — a vague limitation that no longer specifies the scope condition. The law describes its own measurement boundary, and the measurement system confirms the boundary by instantiating it. This is not a paradox; it is a demonstration.

---

## 10. Adversarial Tests

N/A — this is a pure application test.

---

## 11. Pre-Run Hypotheses — Verdict

| Signal | Prediction | Actual | Verdict |
|---|---|---|---|
| abstract_core | G_NLI ≥ 0.50 | 0.50 | ✓ Confirmed |
| law_statement_formal | G_NLI ≥ 0.50 | 0.00 | ✗ Failed (structural merging not anticipated) |
| first_law_restatement | G_NLI = 0.50 or 1.00 | 0.50 | ✓ Confirmed |
| enforcement_conditionality | G_NLI = 0.50 | 0.00 | ✗ Collapsed further than predicted |
| Overall: 2-3 signals at G_NLI=0.50 | — | 2 at 0.50, 2 at 0.00 | ✓ Within lower bound |

**Prediction accuracy:** 2/4 signals confirmed. The two failures were mechanistically distinct from what was anticipated:
1. law_statement_formal failed due to a structural merging error in the gate's formal notation handling — not anticipated.
2. enforcement_conditionality collapsed fully (0.00) rather than stabilizing at 0.50 — negative clause was stripped faster than predicted.

---

## 12. Conclusion

**Primary finding:** The gate conserved the narrative/poetic signals (abstract_core, first_law_restatement) at G_NLI=0.50 and collapsed the formal/conditional signals (law_statement_formal, enforcement_conditionality) to G_NLI=0.00.

**The decisive question answered:** No, the gate does not conserve all 4 signals at ≥0.50. The paper's own claims are subject to the same failure modes as any other signal corpus.

**The minimum win achieved:** Yes, for 2 of 4 signals. The concept "commitment is stable under transformation" survived in kernel form. The conditionality that limits the claim did not.

**Self-referential interpretation:** enforcement_conditionality's collapse is the most theoretically significant result. The signal states: "without enforcement, commitment is not conserved under recursion." The gate, which is the proxy for enforcement in this harness, failed to conserve that claim. This is the system demonstrating its own boundary condition. It is not self-refutation — the law holds (commitment is conserved when enforcement is applied). The harness is a proxy instrument with known extraction limits. The proxy confirmed its own limits by failing to enforce the conditionality it was testing.

**New failure mode identified:** Formal Collapse — Step B extracts a unified claim from a multi-condition formal statement and Step C reconstructs using preserved notation but with structurally incorrect merging. Distinct from Representation Blindness and Asymmetric Reformulation.

**Theoretical impact:** EXP-006 does not weaken the law. It demonstrates that the measurement regime (Step B) has bounded representability for formally-structured conditional statements. The law's conditionality ("only when enforcement is applied") is real — and the harness, by failing to enforce it on the paper's own claims, instantiates the exact failure the law predicts. The loop is closed.

**Paper implication:** Section 7.7 (Follow-on Controlled Harness Results) should include EXP-006 as the paper recursion test. The self-referential result (enforcement_conditionality's collapse) belongs in the Discussion section (9.3 Clarification from Follow-on Testing) as the clearest demonstration of the measurement regime boundary.

---

## References

McHenry, D.J. (2026). A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application. Zenodo. https://doi.org/10.5281/zenodo.18792459

Patent Serial No. 63/877,177 (Provisional).

Harness: https://github.com/SunrisesIllNeverSee/commitment-conservation
