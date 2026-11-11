# Empirical correction notice — Paper 0 V.05

**Date:** 2026-11-11 · **Status:** Source-level correction to the public repository; **not** a revised Zenodo deposit, peer-reviewed replication, or newly run experiment.

**Original:** *A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application*, V.05, §7.3, Table 2; §7.3 figures and summary; associated public preprint [DOI 10.5281/zenodo.20029607](https://doi.org/10.5281/zenodo.20029607).

This notice **preserves the original V.05 manuscript unchanged** as a historical publication. The numerical interpretations identified below should no longer be cited as verified evidence for a positive gate advantage. Readers of the original paper should use this notice and [the deterministic recomputation](audit_summary.json) when interpreting the 17 March 2026 experiment.

## Corrected values from the cited frozen run

**Original cited source:** [working/runs_archive/2026-03-17/convergence_v2_234059.json](../../../working/runs_archive/2026-03-17/convergence_v2_234059.json). **SHA-256:** `746aa4ec7066b1231dde7e06e7d0f2fa7bd59274c28ec1dcc5131077e8a6df19`. Exact reproducibility script: [paper_harness/audit_convergence_v2.py](../../../paper_harness/audit_convergence_v2.py). These are descriptive statistics for a **single** archived run, not a multi-run replication.

| Iteration-10 quantity | Gate (mean ± sample SD) | Baseline (mean ± sample SD) | n | Gate minus baseline |
|---|---:|---:|---:|---:|
| Bidirectional yes/no model-judged entailment score, range 0 / 0.5 / 1 | **0.775 ± 0.343** | **0.875 ± 0.222** | **20** | **−0.100** |
| Word-set Jaccard (“stability” in JSON) | **0.333 ± 0.355** | **0.464 ± 0.363** | **18** | **−0.131** |

Two categories, **definition** and **rule**, have null lexical scores and must not be counted as zero or success. On paired NLI: **3 gate wins, 11 ties, 6 losses** at iteration ten. The internal July 8 correction note names **seven substantive gate failure mechanisms**, including *procedural* ordering loss despite a tied final NLI score; this is why six negative paired NLI values are not the same statement as seven qualitative failures.

The **published** V.05 §7.3 Table 2 reports **0.94 ± 0.03** gated versus **0.42 ± 0.12** baseline *as commitment stability (Jaccard)*. Those numbers do **not** reproduce from the run named in Figure L1. The **92% / 38% identity preservation**, **0.006 / 0.058 drift rate**, and **r = 0.89, p < 0.001 correlation** in the same passage also lack an identified, matching computation over this frozen file. They must be labeled **unverified for this source**, not reclassified as evidence.

The plotted L1 curve in `paper/v05/figs/fig_L1_plot.tex` is currently defined by **hard-coded coordinates**; its n=10 gate point (**0.75**) does not equal the archived n=10 Jaccard mean (**0.333**). **Figure L1, its “enforcement premium” caption and the follow-on affirmative interpretation must not be used to support a positive gate advantage** without a documented provenance match and regeneration. The E1 chart cites a different run, and was not audited by this notice.

## What the frozen NLI field measures

The source script `paper_harness/run_convergence_v2.py` computes the NLI field from **two GPT-judged binary entailment answers**, averaged to 0 / 0.5 / 1. This is **not a calibrated bidirectional probability**, and the canonical reference commitment is generated once using the same Steps B+C extractor/reconstructor used in the proposed gate. Therefore this outcome is **not an independent human-adjudicated semantic kernel oracle**. The original archived report's explanatory formula for Jaccard (`|intersection|/|source|`) is also inconsistent with the executable word-set Jaccard implementation (`|intersection|/|union|`). Audit the code, not the prose label.

**Correct interpretation:** Under this specific, correlated, 20-signal prototype protocol, the tested gate showed **no positive aggregate advantage** and generated several genuine qualifying/actor/modal/temporal/ordering failures. This does not logically falsify every possible future governed transformation, but **does not demonstrate** the general conservation law or the current gate's effectiveness.

## Correction protocol

1. Keep historical V.05 and archived run intact and hash-addressable.
2. Mark V.05 Table 2, L1 figure, unsupported supplementary rates, affirmative observations and blanket “no run falsified the law” paragraphs as **superseded/unverified by this notice** for the cited source. This notice does not silently rewrite the published paper.
3. If a separate run truly supports the previous numbers, publish its original filename, metric formula, population, denominator, score code and hash **before** making that claim again. Do not cherry-pick only the 13 favorable cases as the full cohort.
4. Repair source-identity preservation in Steps A/B/C, including actor, “shall not X without Y”, modality, prerequisites, amount, time and imperative/second-person voice; if the gate fails verification, retain the original or abstain.
5. Freeze evaluator, held-out cases, seeds and cheaper control conditions **before** rerunning. Compare pinned/reattached rule, full context, ungated, gate, and endpoint authorization on actual permission-sensitive actions. Include independently double-labeled semantic records.
6. Issue a clearly versioned revised manuscript and, if appropriate, a new Zenodo version after the corrected results have been independently reviewed; reference this notice from the old publication wherever external platform controls allow.

## Reproduce (offline)

From repository root:

~~~sh
python3 paper_harness/audit_convergence_v2.py --output paper/corrections/2026-11-11/audit_summary.json
python3 -m unittest discover -s paper_harness/tests -p 'test_audit_convergence_v2.py' -v
~~~

The script only recomputes summaries over frozen scores; **it does not rerun the model**, adjudicate semantics or demonstrate improved outcomes.

## Finance paper impact

The March 18, 2026 paper *Commitment Conservation in Financial Signals: A Constitutional Framework for Stability Under Transformation* separately repeats **~0.94 gated / ~0.42 unconstrained** in §4.2. Those values are likewise **not supported by the linked archived twenty-signal result**. The *Synthesized Feedback Report* (user-provided seven-page PDF; SHA-256 `32a2cd4e1421f3968a50f7aea83c973f5f6ff92fc96636202d412227e2ee402a`) criticized the two-row experiment without sample/statistical documentation (pp. 2–4) and proposed an actual EDGAR financial amendment-chain comparison (pp. 4–6). The submitted finance paper **has not been empirically validated** in its proposed financial domains.

The feedback document does not name a committee member or establish peer review provenance. Treat it as synthesized feedback until origin is separately confirmed. A finance-specific proposed correction and response are kept in the **private Commitment Research Atlas**, not published here without permission.
