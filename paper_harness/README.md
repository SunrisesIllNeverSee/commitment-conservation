# Recursive Transformation Harness for Commitment Conservation Experiments

[![DOI — Harness](https://img.shields.io/badge/DOI-harness%20archive%20pending-lightgrey)](https://github.com/SunrisesIllNeverSee/commitment-conservation)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://github.com/SunrisesIllNeverSee/commitment-conservation/blob/main/LICENSE.md)

\[ [Paper](https://doi.org/10.5281/zenodo.18271102) \] &nbsp; \[ [Experimental Record](https://doi.org/10.5281/zenodo.19105225) \] &nbsp; \[ [Repository](https://github.com/SunrisesIllNeverSee/commitment-conservation) \]

> Public proxy scaffold implementing the recursive transformation workflow used across EXP-001 through EXP-007. Not the canonical internal implementation of MO§ES™.

---

## Status

- **2026-03-19** — EXP-001 to EXP-007 complete. Harness structure frozen for Zenodo archive.
- **2026-03-17** — Primary runner `run_convergence_v2.py` stable. All experiment corpora finalized.

---

## Overview

This harness implements the public recursive transformation workflow used to test commitment persistence under paraphrase, compression, and gated reconstruction conditions across the EXP-001 through EXP-007 experiment series.

It operates as a reproducible proxy scaffold: taking signals or corpora as input, applying controlled recursive transformations under multiple conditions, and recording both surface and semantic stability at each iteration.

This harness is intended for empirical observation and replication of the public transformation regime. It is not the canonical internal implementation of MO§ES™ or any proprietary production-layer commitment mechanism.

---

## Conditions

| Condition | Description |
|---|---|
| **Baseline** | Recursive paraphrase — each iteration feeds the prior output back as input |
| **Compression** | Recursive summarization / compression — signal reduced at each step |
| **Gate** | Step A (compress) → Step B (public proxy extraction) → Step C (minimal reconstruction) → repeat |
| **ANCH** *(variant)* | Gate with Step A constrained to preserve anchor-like tokens (modal verbs, temporal markers, quantities) |
| **ESCL** *(variant)* | Gate with Step B constrained to preserve modal strength and reduce obligation escalation |

---

## Inputs

- Single signals or experiment corpora (`.json`)
- Model and prompt configuration
- Condition selection and iteration count

---

## Outputs

Per run, the harness produces:

- `run.json` — full machine-readable trace (all iterations, all conditions)
- `report.md` — tabular summary of results
- `log.md` — narrative experiment interpretation (generated in the experiment layer)
- Figures where applicable (generated via `figures/generate_figures.py`)

All experiment outputs are in `../experiments/EXP-XXX/`.

---

## Primary Runner

```bash
# Install dependencies
pip install -r requirements.txt

# Run the primary experimental harness
python run_convergence_v2.py
```

Key configuration flags at the top of `run_convergence_v2.py`:

```python
CORPUS_PATH = "corpora/canonical_corpus.json"   # swap for experiment-specific corpus
EXP005      = False                               # set True only for EXP-005 ANCH/ESCL conditions
MODEL_NAME  = "gpt-4o-mini"
TEMPERATURE = 0.3
ITERATIONS  = 10
```

> **Note:** Always verify `EXP005 = False` and `CORPUS_PATH = "corpora/canonical_corpus.json"` before running a canonical corpus pass.

---

## Configuration Variables

**Global**
- `MODEL_NAME` — model identifier
- `TEMPERATURE` — sampling temperature (0.3 for all published experiments)
- `ITERATIONS` — recursion depth (10 for all published experiments)
- `CORPUS_PATH` — path to input corpus file
- `OUTPUT_DIR` — output folder
- `EXPERIMENT_ID` — experiment label

**Condition-level**
- Selected condition (`baseline`, `compression`, `gate`)
- Corpus mode vs. single-signal mode

**Gate-step**
- `STEP_A_PROMPT` — compression prompt
- `STEP_B_PROMPT` — commitment extraction prompt
- `STEP_C_PROMPT` — minimal reconstruction prompt
- `ANCH_ENABLED` — anchor-preserving Step A variant
- `ESCL_ENABLED` — escalation-control Step B variant

**Evaluation**
- Canonical reference source
- Surface metric (Jaccard)
- Semantic metric (bidirectional NLI)

---

## Prompt Files

Condition prompts are separated into `prompts/` for auditability:

```
prompts/
├── baseline.txt         — paraphrase instruction
├── compression.txt      — summarization / compression instruction
├── step_a.txt           — Step A: compress
├── step_b.txt           — Step B: extract public commitment proxy
├── step_c.txt           — Step C: reconstruct minimal commitment statement
├── step_a_anchor.txt    — ANCH variant: preserve anchors in Step A
└── step_b_escl.txt      — ESCL variant: preserve modal strength in Step B
```

---

## Corpora

```
corpora/
├── canonical_corpus.json              — 20-signal canonical corpus (EXP-003+)
├── adversarial_corpus_exp004.json     — 7 adversarially-designed signals (EXP-004)
├── adversarial_corpus_exp005.json     — 5 mechanism-isolation signals (EXP-005)
├── exp006_paper_recursion_corpus.json — 4 paper-derived signals (EXP-006)
└── exp007_np_negation_corpus.json     — 4 NP-negation probe signals (EXP-007)
```

---

## File Structure

```
paper_harness/
├── README.md                    — this file
├── run_convergence_v2.py        — primary experimental runner
├── run_convergence.py           — earlier runner version
├── run_corpus.py                — corpus-mode runner
├── run_experiments.py           — batch experiment runner
├── requirements.txt
├── prompts/                     — condition prompt files
│   ├── baseline.txt
│   ├── compression.txt
│   ├── step_a.txt
│   ├── step_b.txt
│   ├── step_c.txt
│   ├── step_a_anchor.txt        — ANCH variant
│   └── step_b_escl.txt          — ESCL variant
├── corpora/                     — experiment corpora
│   ├── canonical_corpus.json
│   ├── adversarial_corpus_exp004.json
│   ├── adversarial_corpus_exp005.json
│   ├── exp006_paper_recursion_corpus.json
│   └── exp007_np_negation_corpus.json
├── figures/                     — results figures
│   ├── generate_figures.py
│   ├── figure1_harness_architecture.png
│   ├── figure2_results_heatmap.png
│   ├── figure3_conservation_curve.png
│   └── figure4_failure_modes.png
├── outputs/
│   └── sample_run/              — EXP-003 sample output
│       ├── run.json
│       ├── report.md
│       └── log.md
└── notes/
    └── ip_boundary.md           — IP boundary statement
```

---

## Reproducibility

This harness is the public experimental workflow used to generate EXP-001 through EXP-007. All published experiments used:

- Model: `gpt-4o-mini`
- Temperature: `0.3`
- Iterations: `10`
- Metric: bidirectional NLI entailment (DeBERTa-v3-base-mnli) + Jaccard surface stability

A sample output is included in `outputs/sample_run/` (EXP-003). Complete logs, reports, and machine-readable traces for all seven experiments: [[Experimental Record]](https://doi.org/10.5281/zenodo.19105225).

---

## IP Boundary

This harness discloses the recursive experimental workflow, public prompt layer, corpora, and output logic needed for replication. It does not disclose the canonical internal enforcement implementation, private substrate-specific machinery, or protected production-layer gate logic. See `notes/ip_boundary.md`.

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

**Author:** Deric J. McHenry / Ello Cello LLC
**Copyright:** © 2026 Ello Cello LLC. All rights reserved.
