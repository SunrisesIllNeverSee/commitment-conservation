# CLAUDE.md — commitment-conservation

## What This Repo Is

Research repository for the **Conservation Law of Commitment** — the claim that commitment content (obligations, prohibitions, modal constraints) persists under recursive transformative compression, and is most cleanly conserved under an enforcement gate.

**Owner:** Deric J. McHenry / Ello Cello LLC
**Patent:** Serial No. 63/877,177 (Provisional)
**Paper DOI:** https://doi.org/10.5281/zenodo.18271102
**Experimental Record DOI:** https://doi.org/10.5281/zenodo.19105225

---

## Law Statement

> C(T(S)) ≈ C(S) with enforcement; C(T(S)) < C(S) without it

**Never call this "McHenry's Law."** The user explicitly prohibits personal name attribution.

---

## File Structure

```
paper/              — main paper drafts (primary deliverable)
experiments/        — EXP-001 through EXP-007
  EXP-00X/
    log.md          — narrative: setup, hypotheses, results, conclusions
    report.md       — clean tabular results (Jaccard + NLI at i1/i5/i10)
    run.json        — full machine-readable trace
    harness_snapshot.py — exact harness at time of run (EXP-003+)
    *_corpus.json   — corpus used (EXP-004+)
harness/            — active harness code
  run_convergence_v2.py  ← PRIMARY harness file
corpus/             — canonical_corpus.json (20 signals) + experiment corpora
foundational/       — theoretical documents
releases/           — versioned release artifacts
working/            — internal planning docs (NOT for public commit)
deploy/             — HF and other deployment artifacts
```

---

## Harness Setup

```bash
cd harness
source ../.venv/bin/activate   # or: python3 -m venv .venv && pip install -r requirements.txt
python3 run_convergence_v2.py
```

**Critical flags in run_convergence_v2.py:**
- `CORPUS_PATH` — must point to `canonical_corpus.json` for standard runs; change for specific experiment corpora
- `EXP005` flag — must be `False` for standard canonical runs; `True` enables ANCH/ESCL conditions

---

## Experiment State

| Experiment | Status | Notes |
|---|---|---|
| EXP-001 | Complete | Smoke test; Jaccard only |
| EXP-002 | Complete | Partially invalid — Step B bug. Included for lineage. |
| EXP-003 | Complete | Canonical 20-signal run; regime classification |
| EXP-004 | Complete | Adversarial signals; Predictive Criterion v2 |
| EXP-005 | Complete | ANCH/ESCL mechanism isolation; Criterion v3 |
| EXP-006 | Complete | Paper recursion test; Formal Collapse failure mode |
| EXP-007 | Complete | NP-negation probe; Jaccard blindness confirmed |

**CORPUS_PATH is currently:** `canonical_corpus.json` (restored after EXP-007 run)

---

## Key Metrics

- **NLI bidirectional entailment** — primary; 1.00=both directions, 0.50=one direction, 0.00=neither
- **Jaccard stability** — secondary; surface keyword overlap vs. origin commitment set (blind to NP-negation forms — confirmed in EXP-007)

---

## Failure Mode Registry

| Mode | Discovered | Description |
|---|---|---|
| Step A Boundary | EXP-002/003 | Summarizer strips qualifying content before extraction |
| Structural Blindness | EXP-003/005 | Modal extractor cannot surface ordering constraints |
| Obligation Escalation | EXP-004/005 | Step B upgrades "should" → "must" |
| Co-degraded Invariance | EXP-003 | NLI=1.00 masks real qualifier loss when both sides are impoverished |
| Modal Frame Inversion | EXP-005 (ANCH) | Anchor preservation without frame preservation inverts polarity |
| Formal Collapse | EXP-006 | Multi-condition formal statement merged into structurally incorrect chain equality |
| Self-referential Collapse | EXP-006 | Conditionality statement collapsed under the mechanism it describes |
| Lexical Scope Widening | EXP-007 | Taxonomic broadening at noun level ("firearms" → "weapons") |
| NP-negation Blindness | EXP-007 | Noun-phrase negation yields empty extraction; Jaccard=0.00 despite NLI=1.00 |

---

## Pending Work

- [ ] Update main paper (addendum with EXP-007 reference)
- [ ] Abstract for second paper (harness dynamics, failure mode taxonomy)
- [ ] GitHub push — EXP-006/007 corpus + snapshots
- [ ] Cross-model replication (Claude, Llama, GPT-4)
- [ ] GitHub release tag to match Zenodo versions

---

## IP Boundaries

- The **law statement** and **theoretical framework** are in the paper — public under CC BY 4.0
- The **MO§ES™ core** (SCS, S³, Mediator, SigEconomy) is **proprietary** — never expose in this repo
- The **harness** is a proxy measurement tool, not the production enforcement implementation
- Patent Serial No. 63/877,177 (Provisional) covers the operational system

---

## Brand Voice

**Never use:** "magic", "intelligent", "smart AI", "revolutionary", "disruptive"
**Use:** sovereign, lineage, invariants, compression, verifiable signal, entropy cost, commitment conservation
