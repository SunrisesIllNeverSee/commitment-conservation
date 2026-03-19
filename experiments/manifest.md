# Manifest — Commitment Conservation Experimental Record

**Version:** 1.0
**Date:** 2026-03-18
**Experiments:** EXP-001 through EXP-007

---

## Top-Level Files

| File | Purpose |
|---|---|
| `README.md` | Overview, relationship to paper, directory guide, citation |
| `manifest.md` | This file — complete inventory |
| `experiment_index.md` | One-page summary of all seven experiments |
| `CITATION.cff` | Machine-readable citation metadata |
| `requirements.txt` | Python dependency for harness reproduction (`requests`) |
| `canonical_corpus.json` | Base corpus (20 signals) used by EXP-003 and canonical harness |

---

## EXP-001

| File | Purpose |
|---|---|
| `log.md` | Experiment log |
| `report.md` | Tabular results |
| `run.json` | Full machine-readable trace |

---

## EXP-002

| File | Purpose |
|---|---|
| `log.md` | Experiment log (includes Step B bug disclosure) |
| `report.md` | Tabular results |
| `run.json` | Full machine-readable trace |

**Note:** Results partially invalid — Step B extraction bug. Corrected in EXP-003.

---

## EXP-003

| File | Purpose |
|---|---|
| `log.md` | Experiment log |
| `report.md` | Tabular results |
| `run.json` | Full machine-readable trace |
| `harness_snapshot.py` | Exact harness at time of run (canonical_corpus, 3 conditions) |

---

## EXP-004

| File | Purpose |
|---|---|
| `log.md` | Experiment log |
| `report.md` | Tabular results |
| `run.json` | Full machine-readable trace |
| `harness_snapshot.py` | Exact harness at time of run (adversarial corpus, 3 conditions) |
| `adversarial_corpus_exp004.json` | 7 adversarially-designed signals |

---

## EXP-005

| File | Purpose |
|---|---|
| `log.md` | Experiment log |
| `report.md` | Tabular results |
| `run.json` | Full machine-readable trace |
| `harness_snapshot.py` | Exact harness at time of run (5 conditions: Baseline, Compression, Gate, ANCH, ESCL) |
| `adversarial_corpus_exp005.json` | 5 signals for mechanism isolation |

---

## EXP-006

| File | Purpose |
|---|---|
| `log.md` | Experiment log |
| `report.md` | Tabular results |
| `run.json` | Full machine-readable trace |
| `harness_snapshot.py` | Exact harness at time of run (paper recursion corpus, 3 conditions) |
| `exp006_paper_recursion_corpus.json` | 4 signals drawn from the main paper |

---

## EXP-007

| File | Purpose |
|---|---|
| `log.md` | Experiment log |
| `report.md` | Tabular results |
| `run.json` | Full machine-readable trace |
| `harness_snapshot.py` | Exact harness at time of run (NP-negation corpus, 3 conditions) |
| `exp007_np_negation_corpus.json` | 6 signals: 4 NP-negation + 2 paired modal controls |
