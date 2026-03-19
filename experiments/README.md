# Experimental Record for A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application (EXP-001 to EXP-007)

**Owner:** Deric J. McHenry / Ello Cello LLC
**Patent:** Serial No. 63/877,177 (Provisional)
**Paper DOI:** https://doi.org/10.5281/zenodo.18792459
**Repository:** https://github.com/SunrisesIllNeverSee/commitment-conservation

---

## Overview

This archive is the DOI-backed empirical record for the follow-on controlled harness studies supporting:

> McHenry, D.J. (2026). *A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application.* Zenodo. https://doi.org/10.5281/zenodo.18792459

The experiments test whether commitment content — obligations, prohibitions, modal constraints — is conserved under recursive transformative compression. Seven experiments are included, progressing from initial signal tests through mechanism isolation, a self-referential paper recursion test, and a targeted NP-negation probe.

All experiments use GPT-4o-mini at temperature 0.3. Primary metric is NLI bidirectional entailment stability vs. a canonical commitment kernel. Secondary metric is Jaccard surface stability.

---

## Quick Start

For a single continuous narrative of the full experimental program, start here:
→ [`combined_experimental_record.md`](combined_experimental_record.md)

For the raw experiment-by-experiment data, open the individual folders.

---

## Relationship to the Main Paper

- The main paper presents the Conservation Law of Commitment and its theoretical foundations.
- This archive provides the follow-on controlled harness results cited in the paper's addendum.
- Harness dynamics, failure mode taxonomy, regime classification, and extended interpretation are deferred to a second paper.

---

## Experiment Summary

| Experiment | Purpose | Key Result |
|---|---|---|
| EXP-001 | Initial smoke test | Phase signal confirmed |
| EXP-002 | Full corpus pass | Hard/soft split; Step B bug identified (see note) |
| EXP-003 | Corrected harness, 20 signals | 13/20 Gate NLI=1.00; co-degraded invariance found |
| EXP-004 | Adversarial signals | Escalation failure mode; Predictive Criterion v2 |
| EXP-005 | Mechanism isolation (ANCH/ESCL) | Step A/Step B co-bottlenecks; Criterion v3 |
| EXP-006 | Paper recursion test | 2/4 paper claims survived; self-referential collapse |
| EXP-007 | NP-negation probe | Jaccard blindness confirmed; NLI=1.00 for 3/4; lexical scope widening identified as new failure mode |

**Note on EXP-002:** Results are partially invalid due to a Step B extraction bug that stripped qualifiers from the canonical reference. The bug was corrected in EXP-003. EXP-002 is included for lineage completeness.

---

## Directory Guide

Each experiment folder contains:

| File | Contents |
|---|---|
| `log.md` | Narrative log: setup, hypotheses, results, mechanistic conclusions |
| `report.md` | Clean tabular results (Jaccard + NLI at i1/i5/i10) |
| `run.json` | Full machine-readable trace (all iterations, all conditions) |
| `harness_snapshot.py` | Exact harness code used for that run *(EXP-003 through EXP-007)* |
| `*_corpus.json` | Corpus used for that experiment *(EXP-004 through EXP-007)* |

`canonical_corpus.json` at the top level is the base corpus used for EXP-003 and the canonical harness.

EXP-001 and EXP-002 predate harness snapshots and do not include `harness_snapshot.py`.

To reproduce any experiment, install dependencies and run the snapshot:

```bash
pip install -r requirements.txt
python3 EXP-00X/harness_snapshot.py
```

---

## Methods / Reproducibility

Experiments were generated through a fixed recursive transformation harness using GPT-4o-mini at temperature 0.3. Each run applies three controlled pipeline conditions — Baseline (paraphrase), Compression (summarize), and Gate (summarize, extract commitment kernel, reconstruct minimal statement) — for 10 iterations per signal. Commitment stability is measured at each iteration via NLI bidirectional entailment against a canonical kernel and Jaccard surface overlap.

Detailed step prompts, extraction logic, and condition-specific variants (ANCH, ESCL) are documented in the per-experiment `harness_snapshot.py` files. Full machine-readable traces are in `run.json`. Corpus files define the signal set and hypotheses for each run.

---

## Citation

```
McHenry, D.J. (2026). Experimental Record for A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application (EXP-001 to EXP-007).
Zenodo. https://doi.org/10.5281/zenodo.19105225
Patent Serial No. 63/877,177 (Provisional).
```
