# A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18267278.svg)](https://doi.org/10.5281/zenodo.18267278)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](LICENSE.md)

\[ [Paper](https://doi.org/10.5281/zenodo.18271102) \] &nbsp; \[ [Experimental Record](https://doi.org/10.5281/zenodo.19105225) \] &nbsp; \[ [Patent No. 63/877,177](https://github.com/SunrisesIllNeverSee/commitment-conservation) \]

> Commitment content persists under transformation, and is most cleanly conserved under an enforcement gate. Without the gate, recursive degradation becomes more likely and more visible.

---

## Status

- **2026-03-19** — EXP-007 complete (NP-negation probe). Experimental series EXP-001 to EXP-007 finalized and archived on Zenodo.
- **2026-03-18** — EXP-006 complete (paper recursion test). Formal Collapse failure mode identified.
- **2026-03-18** — EXP-003 through EXP-005 complete. Regime classification built; mechanism isolation confirmed Step A/B co-bottlenecks.
- **2026-03-17** — Preprint published. Harness and canonical corpus released.

---

## Abstract

This repository accompanies a preprint introducing a conservation law for commitment in language under transformative compression and recursive application. We formalize commitment as an information-bearing invariant that must be preserved across paraphrase, summarization, and iterative reuse, even as surface form and representation change.

We propose a falsifiability framework based on compression-driven stress tests and lineage-aware evaluation, distinguishing semantic preservation from mere token retention. The framework is model-agnostic and applies to both human and machine-generated language.

---

## Key Results

Seven controlled harness experiments (EXP-001 through EXP-007) across a 20-signal canonical corpus plus targeted adversarial and structural probes. All runs: GPT-4o-mini, temperature 0.3, 10 recursive iterations, NLI bidirectional entailment + Jaccard surface stability.

| Experiment | Focus | Key Result |
|---|---|---|
| EXP-001/002 | Smoke test, full corpus | Phase signal confirmed; Step B extraction bug identified |
| EXP-003 | Corrected harness, 20 signals | 13/20 Gate NLI=1.00; regime classification built |
| EXP-004 | Adversarial signals | Escalation failure mode; Predictive Criterion v2 |
| EXP-005 | Mechanism isolation (ANCH/ESCL) | Step A/B co-bottlenecks confirmed; Criterion v3 |
| EXP-006 | Paper recursion test | 2/4 paper claims survived; Formal Collapse identified |
| EXP-007 | NP-negation probe | Jaccard blindness confirmed; NLI=1.00 for 3/4 despite zero extraction |

Full logs, tabular reports, and machine-readable traces are in `experiments/`. Complete narrative: [[Experimental Record]](https://doi.org/10.5281/zenodo.19105225).

---

## Core Claims

- **Commitment Conservation:** Meaningful commitments in language obey a conservation constraint under compression and recursive reuse.
- **Dual Stress Regime:** Preservation must hold under both transformative compression and recursive application, exposing failure modes not captured by retrieval benchmarks.
- **Falsifiability:** Commitment preservation can be empirically tested using compression-based stress tests and lineage-aware metrics.

---

## Reproduce

```bash
git clone https://github.com/SunrisesIllNeverSee/commitment-conservation
cd commitment-conservation
pip install -r harness/requirements.txt
python3 experiments/EXP-003/harness_snapshot.py
```

Each experiment folder (`EXP-001` through `EXP-007`) contains `log.md`, `report.md`, `run.json`, and `harness_snapshot.py` (EXP-003+).

---

## Repository Structure

```
├── paper/          — main paper drafts and versions
├── experiments/    — EXP-001 through EXP-007
├── harness/        — recursive transformation harness
├── corpus/         — canonical corpus + experiment corpora
├── foundational/   — theoretical foundations
├── figures/        — visual assets
├── scripts/        — utility and reproduction scripts
└── releases/       — versioned release artifacts
```

---

## Licensing & Scope

Released under **CC BY 4.0**. This repository includes the evaluation harness and corpus supporting the experiments described in the paper.

Core implementation details related to production deployment, enforcement, and system integration are intentionally out of scope. Patent Serial No. 63/877,177 (Provisional).

---

## Attribution

**Author:** Deric J. McHenry / Ello Cello LLC
**Copyright:** © 2026 Ello Cello LLC. All rights reserved.

For academic or research correspondence, please reference the Zenodo DOI.

---

## Citation

```bibtex
@misc{mchenry2026commitment,
  title     = {A Conservation Law for Commitment in Language Under
               Transformative Compression and Recursive Application},
  author    = {McHenry, Deric J.},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18271102},
  url       = {https://doi.org/10.5281/zenodo.18271102},
  note      = {Patent Serial No. 63/877,177 (Provisional). Ello Cello LLC.}
}
```
