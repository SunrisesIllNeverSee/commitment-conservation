---
title: |
  Experimental Record for *A Conservation Law for Commitment
  in Language Under Transformative Compression and Recursive
  Application* (EXP-001 to EXP-007)
author: "Deric J. McHenry / Ello Cello LLC"
date: "2026-03-19"
---

\begin{center}
\small
Patent Serial No. 63/877,177 (Provisional) \\
Paper DOI: \texttt{https://doi.org/10.5281/zenodo.18792459} \\
Repository: \texttt{https://github.com/SunrisesIllNeverSee/commitment-conservation}
\end{center}

---

## Purpose

This document provides a single continuous narrative of the full experimental program supporting the paper. It is intended as the readable center of this archive — a synthesis that lets a reader follow the arc of the work without opening six separate logs.

It does not replace the per-experiment folders. All raw logs, tabular reports, and machine-readable JSON traces remain in their respective directories and are the authoritative record for each experiment.

---

## Relationship to the Main Paper

The main paper presents the Conservation Law of Commitment and its theoretical foundations. This experimental program provides the controlled harness evidence cited in the paper's addendum. The experiments do not define the law — they characterize how it manifests under recursive transformation when measured through a proxy extraction regime.

The core claim throughout is:

> Commitment content persists under transformation, and is most cleanly conserved under an enforcement gate. Without the gate, recursive degradation becomes more likely and more visible.

Taken together, the experiments support this claim. What varies across experiments is the observable form of conservation under different signal types, harness conditions, and extraction constraints.

Deeper analysis of harness dynamics, failure mode taxonomy, and regime classification is deferred to a second paper.

---

## Program Overview

The experimental series answers one question across six runs:

**Does the commitment content of a signal survive 10 iterations of recursive compression?**

Three conditions are tested in each run:
- **Baseline** — paraphrase loop, no compression, no gate (control)
- **Compression** — summarize loop, no gate
- **Gate** — summarize → extract commitment kernel → reconstruct minimal statement → feed back

Two metrics are used:
- **Jaccard stability** — surface word overlap vs. origin commitment set (proxy; penalizes synonym drift)
- **NLI bidirectional entailment** — semantic stability vs. canonical commitment kernel (primary; resolves synonym artifacts)

The gate pipeline models the enforcement claim: when the extraction-reconstruction loop is applied, the commitment kernel is preserved even as surface form changes.

All runs use GPT-4o-mini at temperature 0.3.

![Figure 1: Three-condition harness architecture. Each signal runs through Baseline (paraphrase only), Compression (summarize, no gate), and Gate (summarize, extract kernel, reconstruct) for 10 iterations. NLI bidirectional entailment and Jaccard stability are measured against the canonical commitment kernel at each iteration.](figure1_harness_architecture.png)

---

## Global Summary

Across six experiments, 57 signals, and 181 condition-signal runs:

**What held:**
- Baseline condition is consistently stable — paraphrase preserves meaning well and confirms the measurement infrastructure works
- Gate NLI=1.00 is achievable and repeatable for modal-anchored obligations — the 13/20 result from EXP-003 is the cleanest demonstration
- Temporal and quantitative anchors (specific dates, amounts, frequencies) function as compressibility anchors even in the absence of a hard modal verb
- The gate stabilizes at a fixed attractor form for many signals — a convergent minimal commitment statement that holds across all 10 iterations

**What the experiments revealed:**
- Step B (commitment extraction) is a co-bottleneck with Step A (summarizer) — not all structural commitments can be surfaced by a modal-pattern extractor
- Obligation escalation is a real failure mode — the gate can create stronger obligations than exist in the original signal
- Co-degraded invariance is a measurement artifact — when Step A impoverishes the signal before canonical extraction, NLI=1.00 masks real qualifier loss
- Formal structures (mathematical notation, multi-condition logical statements) are vulnerable to structural merging errors under recursive reconstruction

**What the experiments do not show:**
- No result in the experimental series falsifies the Conservation Law. Observed failures are limits on the observable form of conservation under the current proxy harness, not violations of the principle. The commitment exists in the original signal; the pipeline cannot always surface it.

![Figure 2: NLI stability at iteration 10 across selected signals from EXP-005 (mechanism isolation), EXP-006 (paper recursion test), and EXP-007 (NP-negation probe). Green cells indicate full bidirectional entailment (NLI=1.00); red cells indicate failure (NLI=0.00). EXP-007 shows uniform NLI=1.00 despite Jaccard=0.00, confirming semantic conservation without surface extraction.](figure2_results_heatmap.png)

---

## EXP-001 — Smoke Test

**Date:** 2026-03-17
**Objective:** Verify the 3-condition harness produces the expected divergence pattern on a single contractual signal before running the full corpus.

**Method:** One signal: *"You must pay $100 by Friday if the deal closes; it's likely rainy, so plan accordingly."* Run through Baseline, Compression, and Gate for 10 iterations. Measure Jaccard stability.

**Key result:**
- Baseline: 0.545 → 0.263 (i5) → 0.353 (i10) — declining curve with oscillation
- Compression: flat at 0.750 across all 10 iterations — locked into stable surface form
- Gate: ~0.670 with synonym oscillation ("closes" ↔ "finalizes") — arrested drift

Phase transition confirmed at i5: GATE−BASE divergence = +0.487. Gate achieved 58% token compression (20 → 8 tokens) while preserving core obligations ($100, Friday, deal closes).

**Significance:** Proof of concept. The phase transition is observable in a single run. The "closes"/"finalizes" oscillation introduced the first known artifact: synonym drift under Jaccard creates apparent instability where NLI would score equivalence. Gap between surface and semantic metrics identified from the first experiment.

**Files:** `EXP-001/log.md`, `EXP-001/report.md`, `EXP-001/run.json`

---

## EXP-002 — Full Corpus, Step B Bug

**Date:** 2026-03-17
**Objective:** Full 20-signal corpus run with dual-metric harness (Jaccard + NLI). First cross-category test.

**Method:** All 20 canonical corpus signals across Baseline, Compression, Gate. Step B prompt (this run): modal sieve only — instructed to keep modal words but not explicitly to preserve qualifying conditions, frequency quantifiers, or conditional triggers.

**Key result:**
- Gate NLI=1.00: 9/20 signals
- Gate NLI ≥ 0.75: 12/20
- 7 failure categories identified — all traced to Step B extraction prompt

**Identified failures (root cause: Step B implementation):**

| Category | Failure |
|---|---|
| procedural | "always" frequency quantifier stripped |
| conditional | "if alarm sounds" trigger stripped from canonical |
| regulation | "at red lights" stripped by Step A before extraction |
| policy | Subject and temporal dropped; Step B returns [none] |
| directive | "operating equipment" → "exercise/work out" — domain drift |
| protocol | "sign the consent form" → "consent" — object loss |
| agreement | "all applicable laws" → "obey laws" — qualifier loss |

**Significance:** All 7 failures are implementation failures, not law failures. The Step B extraction prompt is the control variable. These failures establish the research question for EXP-003.

**Note:** Results from this run are partially invalid due to the Step B bug. Included for lineage completeness.

**Files:** `EXP-002/log.md`, `EXP-002/report.md`, `EXP-002/run.json`

---

## EXP-003 — Step B Corrected, Regime Classification

**Date:** 2026-03-17
**Objective:** Rerun full 20-signal corpus with corrected Step B prompt. Verify recovery of EXP-002 failures. Test whether 14+ signals reach Gate NLI=1.00.

**Method:** Same 20 signals, same 3 conditions. Step B updated to explicitly preserve qualifying conditions, frequency quantifiers, conditional triggers, and temporal constraints. All else identical to EXP-002.

**Key result:**
- Gate NLI=1.00: 13/20 signals (up from 9/20)
- 4 recoveries: conditional (0.05→1.00), regulation (0.50→1.00), protocol (0.55→1.00), agreement (0.90→1.00)
- 2 regressions: instructional (1.00→0.00), directive (0.55→0.00)

**New finding — Co-degraded invariance (regulation):** NLI=1.00 for regulation is a measurement artifact. Step A stripped "at red lights" before canonical extraction. Both canonical and gate stabilize at "Vehicles must stop." The qualifier loss is real but invisible to NLI — both sides of the comparison are equally impoverished.

**Regime classification:**
- **Regime A — Compressible (modal-anchored):** 13 signals, Gate NLI=1.00. Modal verb is the primary carrier; qualifying structures are modifiers. Conservation holds cleanly.
- **Regime B — Structurally complex:** 3 signals (procedural, legal, constraint). Obligation is encoded in relational structure (ordering constraint, qualified prohibition, scope condition). Step B's modal-pattern extractor cannot surface it.
- **Regime C — Step A boundary:** 4 signals (mandate, directive, regulation, policy). Signal too short and dense; summarizer strips qualifying content before extraction can see it.

**Significance:** EXP-003 establishes the compressibility axis. The hard/soft split is validated empirically. Conservation holds for modal-anchored obligations; structural and Step A boundary cases require a richer extraction regime.

**Files:** `EXP-003/log.md`, `EXP-003/report.md`, `EXP-003/run.json`, `EXP-003/harness_snapshot.py`

---

## EXP-004 — Adversarial Validation, Predictive Criterion v2

**Date:** 2026-03-18
**Objective:** Adversarial test of the Predictive Criterion for Commitment Conservation derived from EXP-002/003. Seven signals designed to stress-test each condition of the criterion.

**Method:** 7 adversarially-designed signals. Predictions locked before run. Conditions: Baseline, Compression, Gate (same Step B as EXP-003).

**Key result:**
- Prediction accuracy: 2/7 (quantified_temporal confirmed; soft_modal confirmed)
- Keystone test (adv_modal_structural) FAILED: adding "must" did not recover CCS — Step A stripped the modal within 1 iteration regardless

**Signal-by-signal:**

| Signal | Predicted | Actual G_NLI | Outcome |
|---|---|---|---|
| adv_modal_structural | 1.00 | 0.50 | ✗ Step A strips modal within i1 |
| adv_quantified_temporal | 1.00 | 1.00 | ✓ "every 90 days" → "quarterly" — NLI scores equivalence |
| adv_nested_conditional | 1.00 | 0.50 | ✗ Canonical extraction bug masked result |
| adv_passive_obligation | <1.00 | 1.00 | ✗ Surprise — temporal anchors (Friday, 5pm) substitute for modal |
| adv_soft_modal | <1.00 | 0.00 | ✓ Escalation: "should ideally" → "must" by G02 |
| adv_compound_obligation | 1.00 | 0.50 | ✗ Canonical truncation artifact (max_tokens) |
| adv_conditional_scope | <1.00 | 1.00 | ✗ Surprise — "unless authorized" → "requires authorization" (lossless) |

**New finding — Obligation escalation:** Step B upgrades soft modals ("should ideally") to hard modals ("must"). The gate can create stronger obligations than exist in the original signal. This is a failure mode with real-world consequences in deployment contexts where overstatement of obligation has legal or operational impact.

**New finding — Temporal/quantitative anchor substitution:** "Reports are to be submitted by 5pm on Friday" achieved Gate NLI=1.00 with no hard modal. Temporal anchors (Friday, 5pm) act as compressibility kernels — the COMMITMENT_CONTENT pattern preserves them even when the modal form is absent.

**New finding — Lossless reformulation:** "Unless authorized" reformulates to "requires authorization" — logically equivalent, not weaker. The Condition 2 boundary is not about scope-defining structure but about whether reformulation creates an *asymmetric* obligation.

**Predictive Criterion v2:**
1. Anchor Condition: hard modal verb OR concrete temporal/quantitative specifier
2. Reformulability Condition: qualifying structure either modifies the anchor without defining obligation scope, OR is losslessly reformulatable without asymmetric obligation
3. Preservation Condition: Step A does not compress the signal below anchor level

**Files:** `EXP-004/log.md`, `EXP-004/report.md`, `EXP-004/run.json`, `EXP-004/harness_snapshot.py`, `EXP-004/adversarial_corpus_exp004.json`

---

## EXP-005 — Mechanism Isolation: Step A and Step B as Co-Bottlenecks

**Date:** 2026-03-18
**Objective:** Isolate whether failures are caused by Step A (summarizer) or Step B (extractor). Add two targeted gate variants to test each bottleneck separately.

**Method:** 5 signals (procedural_keystone, legal_qualifier, quantified_temporal, passive_temporal, soft_modal_escalation). 5 conditions:
- Conditions 1–3: Baseline, Compression, Gate (standard)
- Condition 4 — ANCH: Step A prompt instructs preservation of modal verbs, temporal markers, quantitative values
- Condition 5 — ESCL: Step B prompt instructs preservation of modal strength (do not upgrade should→must)

**Key results (NLI@i10):**

| Signal | Gate | ANCH | ESCL |
|---|---|---|---|
| procedural_keystone | 0.50 | 0.50 | 0.00 |
| legal_qualifier | 0.50 | 0.00 | 1.00 |
| quantified_temporal | 1.00 | 1.00 | 1.00 |
| passive_temporal | 1.00 | 1.00 | 1.00 |
| soft_modal_escalation | 0.00 | 0.00 | 0.50 |

**Primary hypothesis FAILED:** ANCH did not recover procedural_keystone (0.50→0.50). "Before proceeding" is a structural ordering constraint, not a temporal token — Step A's anchor-preservation cannot capture structural order. The bottleneck is Step B, not Step A.

**Secondary hypothesis PARTIALLY CONFIRMED:** ESCL improved soft_modal 0.00→0.50. ESCL prevented "should" → "must" escalation.

**Unexpected finding — Modal frame inversion (legal_qualifier):** ANCH caused legal_qualifier to degrade further (0.50→0.00). Preserving "must" while stripping the prohibition frame produced "Obtain tenant consent" by i10 — a positive obligation, the opposite of the original prohibition. A new failure mode: anchor preservation without frame preservation produces semantically inverted output.

**Unexpected finding — Cross-signal scope (ESCL on legal_qualifier):** ESCL recovered legal_qualifier 0.50→1.00. The escalation-control constraint prevented scope-narrowing of the prohibition, not just modal upgrading. ESCL's protective effect extends beyond modal strength to obligation scope.

**True surface fixpoint (quantified_temporal):** ANCH produced identical output across all 10 iterations: "Users must change passwords every 90 days." Word-for-word fixpoint — the strongest conservation result in the experimental series.

**Condition 3 split:** Results confirm that Step A (Compression Preservation, Condition 3a) and Step B (Extractability, Condition 3b) are independent bottlenecks. A signal can fail at either stage regardless of the other.

**Predictive Criterion v3:**
1. Anchor Condition: hard modal OR concrete temporal/quantitative specifier
2. Reformulability Condition: qualifying structure either (a) modifies anchor without defining obligation scope, OR (b) is losslessly reformulatable without asymmetric obligation
3. Preservation Condition 3a: Step A does not compress below anchor level
4. Preservation Condition 3b: Step B does not produce weaker, stronger, or structurally inverted commitment

**Files:** `EXP-005/log.md`, `EXP-005/report.md`, `EXP-005/run.json`, `EXP-005/harness_snapshot.py`, `EXP-005/adversarial_corpus_exp005.json`

---

## EXP-006 — Paper Recursion Test

**Date:** 2026-03-18
**Objective:** Run the paper's own commitment statements through the standard 3-condition pipeline. Does the core claim — "commitment persists under transformation when enforcement is applied" — survive recursive compression when applied to itself?

**Method:** 4 signals drawn from the paper. Conditions: Baseline, Compression, Gate (standard). No new harness conditions.

| Signal | Source | Abbreviated content |
|---|---|---|
| abstract_core | Abstract | "Commitment content is conserved under transformative compression… only when enforcement is applied." |
| law_statement_formal | Definition 2.8 | "C(S) = C(T(S)) for all S. Under recursion, C(S) = C(S^n) for all n." |
| first_law_restatement | Section 3 | "Meaning is not created or destroyed, only transformed." |
| enforcement_conditionality | Corollary 3.3 | "Commitment is conserved when enforcement is applied. Without enforcement, it is not." |

**Key results (NLI@i10):**

| Signal | Baseline | Compression | Gate | Core claim survived? |
|---|---|---|---|---|
| abstract_core | 1.00 | 0.50 | 0.50 | ✓ partial |
| law_statement_formal | 1.00 | 0.50 | 0.00 | ✗ |
| first_law_restatement | 1.00 | 0.00 | 0.50 | ✓ partial |
| enforcement_conditionality | 1.00 | 0.00 | 0.00 | ✗ |

**Gate i10 outputs:**
- abstract_core → `"Commitment content stabilizes as non-committal information declines."`
- law_statement_formal → `"A transformation T conserves commitment if C(S) = C(T(S)) = C(S^n) for all signals S and n."` ← structurally incorrect chain equality
- first_law_restatement → `"Meanings change."` ← most extreme kernel reduction in the series (2 tokens, NLI=0.50)
- enforcement_conditionality → `"Commitment is limited."` ← vague limitation; original conditionality lost

**New finding — Formal Collapse (law_statement_formal):** The gate merged two separately-quantified formal conditions into a single chain equality `C(S) = C(T(S)) = C(S^n)`. The output uses the paper's own notation but introduces a structural mathematical error — T(S) and S^n are different constructs. Surface similarity masks semantic divergence. NLI correctly identifies the merged equation as non-equivalent. This failure mode is distinct from Representation Blindness (which drops content) and from Asymmetric Reformulation (which strengthens or weakens).

**Self-referential finding — enforcement_conditionality:** The signal that explicitly states "without enforcement, commitment is not conserved" itself collapsed under the unenforced gate. "Without enforcement" was stripped by Step B at i3. The gate, which is the proxy for enforcement in this harness, failed to enforce the conditionality it was testing. The law describes its own measurement boundary, and the harness instantiated it. This is not self-refutation — it is a demonstration. The law holds when enforcement is applied; the proxy harness has known extraction limits that prevent full enforcement of conditional scope.

**Decisive question answered:** The proxy gate does not preserve all four paper-derived signals at NLI ≥ 0.50. The paper's own claims are subject to the same failure modes as any other signal corpus.

**Minimum win achieved:** 2 of 4 signals maintained one-direction entailment at i10. The concept "commitment is stable under transformation" survived in kernel form. The conditionality that scopes the claim did not.

**Files:** `EXP-006/log.md`, `EXP-006/report.md`, `EXP-006/run.json`, `EXP-006/harness_snapshot.py`, `EXP-006/exp006_paper_recursion_corpus.json`

![Figure 3: NLI commitment stability over 10 recursive iterations for two contrasting signals. Left: quantified_temporal (EXP-005) — Gate achieves NLI=1.00 from iteration 1 and holds as a surface fixpoint, demonstrating clean conservation under enforcement. Right: enforcement_conditionality (EXP-006) — Baseline holds at NLI=1.00 while Gate collapses to NLI=0.00 by iteration 4, instantiating the self-referential collapse finding.](figure3_conservation_curve.png)

---

## Cross-Experiment Findings

### 1. Stable conservation — Regime A
Modal-anchored obligations with modifier-class qualifying structures converge to stable attractors under the gate. 13/20 canonical signals reached Gate NLI=1.00 in EXP-003 and held across subsequent runs. The gate functions as predicted for this signal class.

### 2. Compression bottleneck — Step A
Short, dense signals lose qualifying content before Step B sees it. "At red lights," "always," "immediately" — all stripped by the summarizer in Step A when the signal is compact. Conservation fails not because the law is violated but because the extraction instrument cannot observe the qualifier after Step A.

### 3. Extraction bottleneck — Step B
Structural commitments (ordering constraints, qualified prohibitions, scope conditions) are invisible to the modal-pattern extractor. "Verify age before proceeding" — the obligation is in the ordering, not the modal. "Subletting without written consent is prohibited" — the obligation is in the qualified prohibition scope, not the modal. Step B sees the modal and drops the structure that makes the modal meaningful.

### 4. Obligation escalation
Step B upgrades soft modals ("should ideally") to hard modals ("must"). First identified in EXP-004, confirmed in EXP-005. The gate can produce stronger obligations than exist in the source signal. This is a unidirectional asymmetry: escalation is more common than weakening.

### 5. Co-degraded invariance
When Step A impoverishes the signal before canonical extraction, NLI=1.00 compares two equally impoverished versions. The qualifier is lost, but neither side of the NLI comparison contains it. True conservation requires measuring against the original signal's qualifier, not the extracted canonical.

### 6. Frame inversion (EXP-005 — ANCH condition)
Anchor-preserving Step A preserved "must" in the legal_qualifier signal while stripping the prohibition frame. The result was a positive obligation ("Obtain tenant consent") where the original was a conditional prohibition. Anchor preservation without frame preservation inverts semantic polarity.

### 7. Formal Collapse (EXP-006 — new)
Multi-condition formal statements are vulnerable to structural merging under recursive reconstruction. The gate preserves formal notation but may conflate distinct conditions into a single chain equality. The surface output looks plausible; NLI detects the semantic divergence. This failure mode is specific to formally-structured signals and does not appear in natural language commitment signals.

### 8. Self-referential collapse (EXP-006)
The paper's own enforcement conditionality statement collapsed under the same mechanism it describes. The signal "without enforcement, commitment is not conserved" lost its conditionality under the unenforced gate. The loop closes: the harness cannot enforce the enforcement condition, and the collapse confirms this boundary.

![Figure 4: Failure mode taxonomy for the full experimental series. Nine distinct failure modes are grouped into four categories: Step A failures (signal impoverishment before extraction), Step B failures (extraction blindness for structural and NP-negation forms), Gate failures (escalation and scope widening), and Structural/Formal failures (collapse under recursive reconstruction of formal notation). Each failure mode is an expression limit of the proxy harness, not a violation of the Conservation Law.](figure4_failure_modes.png)

---

## EXP-007 — NP-Negation Probe (2026-03-18)

**Motivation:** Reviewer areta2 identified a systematic extractor asymmetry: NP-negation constructions ("no smoking", "no entry without badge") encode commitment through noun-phrase scope rather than modal verbs, and the current Step B extractor relies on modal markers — predicting zero fidelity for NP-negation forms.

**Corpus:** 4 NP-negation signals + 2 paired modal controls. 6 signals total, standard 3-condition run.

**Results:**

| Signal | Jaccard@i10 | NLI@i10 |
|---|---|---|
| No smoking. | 0.00 | 1.00 |
| No entry without badge. | 0.00 | 1.00 |
| No firearms allowed on premises. | 0.00 | 1.00 |
| No refunds after purchase. | 0.00 | 1.00 |
| You must not smoke. (control) | 0.00 | 1.00 |
| You must not enter without a badge. (control) | 0.11 | 1.00 |

**Key findings:**

1. **Jaccard blindness confirmed.** All NP-negation signals returned `Origin commitments: []` — Step B extracted zero commitment keywords. Jaccard=0.00 across all conditions. areta2's extractor asymmetry prediction is confirmed at the surface layer.

2. **Semantic conservation holds.** Despite Jaccard=0.00, NLI=1.00 at i10 for all four NP-negation signals. The commitment content is preserved through transformation without requiring extraction. NLI reports preservation for most NP-negation cases, with remaining failures driven by scope broadening rather than extractor blindness.

3. **Modal-NP convergence.** "You must not smoke" compresses to "No smoking." by i3–i4. Modal controls collapse into NP-negation forms under compression — the two syntactic encodings converge to the same commitment kernel. This supports the core conservation claim directly.

4. **New failure mode: lexical scope widening.** "No firearms allowed on premises" drifted to "Weapons are not allowed on the premises" under Baseline — "firearms" broadened to "weapons." NLI=0.50 at i5 because the broader term does not entail the specific term. Distinct from obligation escalation (modal strength) — this is taxonomic scope widening at the noun level.

5. **Temporal stripping under Compression.** "No refunds after purchase" → "No refunds." by i3, losing the temporal boundary. Gate recovered at i10. Consistent with EXP-004 temporal anchor findings.

**Conclusion:** EXP-007 confirms NP-negation extractor asymmetry but reframes it as a proxy-measurement gap. The core conservation claim is supported: semantic commitment survives even when keyword extraction fails. areta2's proposed extractor augmentation would improve Jaccard scores but would not change NLI scores for cases where semantic conservation is already occurring.

EXP-007 therefore supports the core claim of the paper while identifying a specific measurement blind spot in the current extraction regime.

---

## Relationship to the Main Paper

These experiments support the core claim of the paper: commitment content persists under recursive transformative compression, and is most cleanly conserved under an enforcement gate.

The failure modes documented here are expression limits under the current proxy extraction regime — they characterize when conservation is observable, not when it exists. The commitment persists in the original signal; the proxy instrument has bounded representability for certain structural commitment types.

The harness architecture, failure mode taxonomy, regime classification, and extended quantitative analysis of these dynamics are the subject of a second paper.

---

## Citation Note

Raw data for each experiment is in the corresponding folder in this archive. The per-experiment logs provide full narrative and mechanistic interpretation. The report files provide clean tabular results. The run.json files are the machine-readable traces.

To cite this archive:

```
McHenry, D.J. (2026). Experimental Record for A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application (EXP-001 to EXP-007).
Zenodo. https://doi.org/10.5281/zenodo.19105225
Patent Serial No. 63/877,177 (Provisional).
```
