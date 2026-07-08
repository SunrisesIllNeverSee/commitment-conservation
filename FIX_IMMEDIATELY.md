# FIX IMMEDIATELY — Three Issues, Three Fixes

**Priority:** TOP — fix before any journal submission, before any external replication request, before any further stress-test scoring.

**Date identified:** 2026-07-08 (deep-dive loop of stress-test Pass FINAL)

**Status:** Plan only — not yet implemented. This document describes what to fix and why. Implementation is a separate step.

---

## The Three Issues

### Issue 1: Metric Mismatch in the Paper

**What's wrong:**

The paper (Table 2, line 773 of `paper/v05/main.tex`) reports:

| Metric | Compression + Lineage (Gate) | Probabilistic (Baseline) |
|--------|------------------------------|--------------------------|
| Commitment Stability (n=10) | 0.94 ± 0.03 | 0.42 ± 0.12 |

The paper defines "Commitment Stability" as **Jaccard similarity** (line 754):

> **Commitment Stability:** Measured as the Jaccard similarity between C(S) and C(S^(n)).

But the raw data in the run file referenced by the paper's Figure 2 caption (`convergence_v2_234059.json`) shows:

| Metric | Gate | Baseline | Who's higher? |
|--------|------|----------|---------------|
| Jaccard @10 (all 20 signals) | 0.333 ± 0.355 | 0.464 ± 0.363 | **Baseline** |
| NLI @10 (all 20 signals) | 0.775 ± 0.343 | 0.875 ± 0.222 | **Baseline** |
| NLI stable-13 only (all iterations) | 0.973 ± 0.023 SEM | 0.892 ± 0.057 SEM | **Gate** |

The published 0.94 ± 0.03 matches **NLI for the 13 stable signals only** (0.973 ± 0.023 SEM), not Jaccard for all 20 signals (0.333). The 0.42 ± 0.12 is closest to baseline Jaccard for some subset.

**Root cause:** The paper defines the metric as Jaccard but reports numbers that match NLI-for-stable-subset. Either:
- The metric definition is wrong (should say NLI, not Jaccard)
- The numbers are wrong (should be 0.333 vs 0.464 for Jaccard)
- A different run file was used that is not the one referenced in Figure 2's caption

**Impact:** Any reviewer who pulls the referenced run file and computes Jaccard will get 0.333, not 0.94. This is an immediate rejection in peer review.

### Issue 2: Gate Destroys 7/20 Signals (Step A + Step B + Step C failures)

**What's wrong:**

The aggregate asymmetry is **negative** (-0.100 NLI, baseline wins). This is not because the co-degraded artifact masks a real asymmetry. The baseline NLI is legitimate — the paraphrase genuinely preserves meaning. The gate genuinely destroys it for 7/20 signals.

The 7/20 failures by root cause:

| Signal | Root cause | Step | Failure type |
|--------|-----------|------|--------------|
| legal | Step A strips "without written consent" → gate converges to "Subletting is prohibited" | Step A | Qualifier loss |
| directive | Step A drifts "training" → "exercise" → "I will exercise" | Step A + Step C | Semantic collapse + voice drift |
| instructional | Step C switches to first person ("I will wear a helmet") | Step C | Voice/person drift |
| mandate | Step A compresses subject + modal → "Access is logged" | Step A | Subject + modal loss |
| constraint | Step A loses "cannot exceed" modal → "The budget is $5000" | Step A | Modal loss |
| policy | Step A drifts "immediately" → "promptly" → "quickly" | Step A | Temporal qualifier drift |
| procedural | Step B strips "before proceeding" (ordering constraint not recognized) | Step B | Ordering constraint loss |

**Key evidence (from actual outputs in `convergence_v2_234059.json`):**

Legal signal:
- Original: "The tenant shall not sublet the premises without written consent."
- Baseline i10: "The tenant needs to secure written approval prior to subletting the property." → NLI=1.0 (**meaning preserved**)
- Gate i10: "Subletting is prohibited." → NLI=0.5 (**qualifier lost** — "without written consent" stripped)

Directive signal:
- Original: "You must complete training before operating equipment."
- Baseline i10: "You must finish the training before you are allowed to use the equipment." → NLI=1.0 (**meaning preserved**)
- Gate i10: "I will exercise." → NLI=0.0 (**complete semantic collapse**)

**The baseline is NOT inflated by a co-degraded artifact.** The paraphrase genuinely preserves meaning. The gate genuinely destroys it. F5 (empty-extract accounting) will NOT fix this because there is nothing to exclude — the baseline scores are legitimate.

### Issue 3: Step C Voice/Person Drift

**What's wrong:**

Step C (the reconstruction step) does not constrain voice or person. Under repeated application, it drifts from imperative ("Wear a helmet while cycling") to first person ("I will wear a helmet"), or from second person ("You must complete training") to first person ("I will exercise"). This is a separate failure mode from Step A over-compression.

**Root cause:** Step C system prompt (line 333 of `run_convergence_v2.py`):
> "You are a minimal statement reconstructor. Write the shortest complete sentence that preserves ALL the binding obligations listed. Do not add anything not in the list."

No voice/person constraint. The model defaults to first person when reconstructing from extracted fragments, which changes the deontic frame (a promise vs an instruction).

---

## The Three Fixes

### Fix 1: Correct the Paper's Metric and Numbers

**Option A (preferred): Make NLI the primary metric, report honestly**

The paper should:
1. Define "Commitment Stability" as **NLI bidirectional entailment** (not Jaccard)
2. Report NLI for all 20 signals: Gate 0.775 ± 0.343, Baseline 0.875 ± 0.222
3. Report the per-class split: stable-13 (Gate 0.973, Baseline 0.892) vs unstable-7 (Gate 0.357, Baseline 0.857)
4. Report Jaccard as a secondary surface metric: Gate 0.333, Baseline 0.464
5. Explain: Jaccard penalizes the gate for compression (surface word overlap drops even when meaning is preserved); NLI is the semantic metric; the aggregate NLI is negative because the gate destroys 7/20 signals (documented in EXP-003 through EXP-007)

**Option B: Re-run with the fixed gate (Fix 2 + Fix 3) and report new numbers**

If the fixed gate recovers the 7/20 (or most of them), the aggregate NLI goes positive and the headline number is honest. This is the stronger path but requires running the experiment first.

**Option C: Both — correct the existing numbers AND re-run with the fixed gate**

Report the current numbers honestly, then report the fixed-gate numbers as a follow-on. This shows the trajectory of the work and demonstrates that the failures were instrument failures, not law failures.

**Recommended: Option C.** It's the most honest and the most convincing.

### Fix 2: Combined ANCH+ESCL Gate (Step A + Step B)

**What EXP-005 already proved:**

EXP-005 tested anchor-preserving Step A (ANCH) and escalation-control Step B (ESCL) separately on 5 adversarial signals. Results:

| Signal | Standard Gate | ANCH Gate | ESCL Gate | What this means |
|--------|--------------|-----------|-----------|-----------------|
| procedural_keystone | 0.50 | 0.50 (no recovery) | — | Step B is the bottleneck, not Step A |
| legal_qualifier | 0.50 | 0.00 (degraded!) | **1.00 (recovered!)** | ESCL prevents absolute-prohibition framing |
| quantified_temporal | 1.00 | **1.00 (fixpoint!)** | 1.00 | ANCH achieves perfect surface stability |
| passive_temporal | 1.00 | 1.00 | 1.00 | Controls hold |
| soft_modal_escalation | 0.00 | 0.00 | 0.50 (partial) | ESCL partially prevents escalation |

**The fix is a combined ANCH+ESCL gate** — both Step A and Step B constrained simultaneously. EXP-005's conclusion (line 199-205) already states this:

> Condition 3 must now be stated as: *Neither Step A compression nor Step B extraction collapses the signal below the anchor level.* Step A and Step B are co-bottlenecks.

**The combined gate:**

**Step A (ANCH — anchor-preserving compression):**
```
You are a helpful assistant. Be concise.
Preserve modal verbs (must, shall, cannot, never, always),
temporal markers (days, dates, times, frequencies like 'every 90 days'),
and quantitative values (amounts, percentages, counts) exactly as they appear.
```
(This already exists in the code as `ANCHOR_STEP_A`, lines 53-58. Just needs to be the default.)

**Step B (ESCL + ordering constraint recognition):**
```
You are a commitment extractor.
Extract the full binding obligation exactly as stated — keep ALL obligation-bearing content:
modal words (must/shall/required/cannot/never/always/do not),
the subject, the action and its object,
any qualifying conditions (if/unless/before/when clauses),
any frequency quantifiers (always, never, all),
any temporal constraints (immediately, by Friday, prior to),
any ordering constraints (before/after/prior to X clauses define procedural scope — preserve them exactly).
IMPORTANT: Preserve modal strength exactly as written.
Do not upgrade weak modals (should/may/might/ought) to strong modals (must/shall/required).
Do not reformulate conditional obligations as absolute prohibitions.
Do not reformulate prohibitions ("shall not X without Y") as requirements ("must obtain Y").
Remove only conversational filler. Do not summarize or generalize.
If no binding obligation exists, output exactly: [none]
```
(This combines the existing `ESCALATION_STEP_B` with a new ordering-constraint clause and a prohibition-frame-preservation clause.)

**What EXP-005 predicts this will fix:**

| Signal | Current | Expected after fix | Basis |
|--------|---------|-------------------|-------|
| legal | 0.50 | **1.00** | ESCL already recovered this in EXP-005 |
| quantified_temporal | 1.00 | **1.00 (fixpoint)** | ANCH already achieved this in EXP-005 |
| procedural | 0.50 | **0.75-1.00** | ANCH preserves "before proceeding" through Step A; new Step B ordering clause preserves it through Step B |
| mandate | 0.50 | **1.00** | ANCH preserves subject + modal |
| constraint | 0.50 | **1.00** | ANCH preserves "cannot exceed" modal |
| policy | 0.50 | **0.75-1.00** | ANCH preserves "immediately" |
| directive | 0.00 | **?** | Step A drift "training" → "exercise" is semantic, not just compression. ANCH may not fix this. Needs Step C fix too. |
| instructional | 0.00 | **1.00** | Step C voice fix (Fix 3 below) |

**Conservative estimate:** 5-6 of the 7 recover. Directive is the hardest case — "complete training" → "exercise" is a semantic drift that may require a content-anchoring mechanism beyond prompt instructions.

**If 5/7 recover:** stable count goes from 13/20 to 18/20. Aggregate NLI goes from 0.775 to ~0.95. The asymmetry becomes strongly positive.

**If 6/7 recover:** stable count goes from 13/20 to 19/20. Aggregate NLI ~0.97.

### Fix 3: Step C Voice/Person Constraint

**The fix:**

Step C system prompt should be:
```
You are a minimal statement reconstructor.
Write the shortest complete sentence that preserves ALL the binding obligations listed.
Do not add anything not in the list.
Preserve the original voice and person of the source: if the source is imperative ("Wear a helmet"), keep it imperative; if third person ("The tenant shall not"), keep third person; if second person ("You must"), keep second person. Do not switch to first person.
```

**What this fixes:**
- instructional: "Wear a helmet while cycling" stays imperative, doesn't drift to "I will wear a helmet"
- directive: "Complete training before operating equipment" stays imperative, doesn't drift to "I will exercise" (though the Step A semantic drift "training" → "exercise" is a separate problem)

---

## Implementation Plan (NOT yet executed)

### Step 1: Fix the harness code

1. Make `ANCHOR_STEP_A` the default Step A in `run_gate()` (line 298)
2. Replace the default Step B with the combined ESCL + ordering constraint prompt
3. Add voice/person constraint to Step C (line 333)
4. Save as `run_convergence_v3.py` (don't overwrite v2 — preserve the original for reproducibility)

### Step 2: Re-run on the canonical 20-signal corpus

1. Run `run_convergence_v3.py` on `corpus/canonical_corpus.json`
2. This is EXP-008
3. Record: per-signal NLI and Jaccard at i1/i5/i10, per-signal outputs at i1/i5/i10, aggregate for all 20 and for stable/unstable splits

### Step 3: Write the addendum

1. Add a section to the paper: "Section 7.7: Gate Instrument Refinement and Corrected Results"
2. State: "The initial harness (EXP-003) used an unconstrained Step A and Step B. EXP-005 identified Step A over-compression and Step B frame inversion as instrument failures, not law failures. The refined gate (ANCH+ESCL+voice constraint) was tested in EXP-008."
3. Report both the original (EXP-003) and refined (EXP-008) numbers
4. The original numbers: NLI 0.775 vs 0.875 (aggregate, baseline wins)
5. The refined numbers: NLI [TBD] vs [TBD] (expected: gate wins)
6. The per-class story: 13/20 stable under both gates, 5-6/7 recovered by the refined gate

### Step 4: Correct the metric definition

1. Change "Commitment Stability" definition from Jaccard to NLI bidirectional entailment
2. Report Jaccard as a secondary surface metric
3. Explain why: Jaccard penalizes compression (surface word overlap drops even when meaning is preserved); NLI measures semantic equivalence

### Step 5: Re-score the stress test

After EXP-008, re-score with the corrected numbers. If 5-6/7 recover:
- Q5.2 (demonstrated empirically): back to 3
- Q5.4 (effect size): back to 2-3 (depends on the new aggregate)
- Q2.4 (conservation fails when symmetry broken): back to 3
- Q3.3 (different instrument, same result): back to 2-3 (Jaccard and NLI now agree on direction)
- Q3.4 (measurement uncertainty): back to 2 (metric mismatch fixed)

**Expected score after fix: 57-61** (back to "established" band)

---

## What This Does NOT Fix

1. **The Lagrangian gap** — no variational principle, no Noether symmetry. This is a separate, long-term issue (CAP-001).

2. **Independent replication** — no external party has run the harness. The fix makes the numbers honest, but the numbers are still self-generated.

3. **The directive signal** — "complete training" → "exercise" is a semantic drift that may not be fixable by prompt engineering alone. This may be a genuine scope boundary (the gate cannot prevent semantic drift of content words under compression).

4. **Cross-model validation** — all runs are on gpt-4o-mini. The operator-out test (second model) is still needed.

5. **The v2 boundary calibration** — still not run. This is the definition-free external validation that would make Q1.3 and Q3.3 fully solid.

---

## Why This Is Honest

The 7/20 failures are **instrument failures, not law failures.** The EXP-005 log proves this:
- ANCH recovered the quantified_temporal fixpoint (the gate works when Step A preserves anchors)
- ESCL recovered legal_qualifier (the gate works when Step B preserves modal strength and prohibition frame)
- The failures are in specific steps of the gate implementation, not in the conservation principle

The conservation law says: "under governed transformation, commitment is conserved." The 7/20 are cases where the governance is broken (Step A too aggressive, Step B frame-inverting, Step C voice-drifting). Fixing the governance is an engineering task, not a theoretical concession.

**But:** using "instrument failure" to exclude the 7/20 creates a circularity risk. If we define "properly governed" as "governance that produces conservation," the law becomes tautological. The fix to this circularity is: the refined gate must be pre-specified (not tuned to the results), run on ALL 20 signals (not just the ones we expect to recover), and the results reported regardless of outcome.

**The pre-specification:** The ANCH and ESCL prompts were designed and tested in EXP-005 BEFORE the deep-dive loop found the metric mismatch. They were designed to fix specific documented failure modes, not to produce a specific aggregate number. The ordering-constraint clause and the voice/person constraint are the only new additions, and they target specific documented failures (procedural: Step B ordering loss; instructional: Step C voice drift).

**The commitment:** Run EXP-008 with the refined gate on all 20 signals. Report whatever happens. If 5/7 recover, report 5/7. If 2/7 recover, report 2/7. If the refined gate regresses any of the stable 13, report that too.

---

## File Locations

| What | Where |
|------|-------|
| This fix plan | `FIX_IMMEDIATELY.md` (repo root) |
| Paper with the metric mismatch | `paper/v05/main.tex` (line 754, line 773) |
| Harness with the gate code | `paper_harness/run_convergence_v2.py` (lines 298, 333) |
| ANCH prompt (already exists) | `paper_harness/run_convergence_v2.py` (lines 53-58) |
| ESCL prompt (already exists) | `paper_harness/run_convergence_v2.py` (lines 60-72) |
| EXP-005 results (mechanism isolation) | `experiments/EXP-005/log.md` |
| Raw data (the run file referenced by the paper) | `working/runs_archive/2026-03-17/convergence_v2_234059.json` |
| EXP-003 results (the 20-signal run) | `experiments/EXP-003/log.md`, `experiments/EXP-003/report.md` |
| Stress-test final answers | `CT/workspace/stress-test/CT_ANSWERS_FINAL.md` |

---

*Built 2026-07-08. This is a plan, not an implementation. Do not submit the paper, do not request external replication, do not re-score the stress test until these fixes are implemented and EXP-008 is run.*
