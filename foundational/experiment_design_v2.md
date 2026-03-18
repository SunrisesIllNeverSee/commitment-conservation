# Experiment Design v2 — Phase Transition Test
**Source:** External collaborator review, 2026-03-17
**Status:** Approved for implementation
**Patent:** Serial No. 63/877,177 (Provisional)
**DOI:** https://doi.org/10.5281/zenodo.18792459
**Owner:** Deric J. McHenry / Ello Cello LLC

---

## Objective

Test whether recursive transformation causes semantic drift, and whether compression + extraction (gating) stabilizes meaning.

**One observable:** Does enforcement flatten the drift curve?

Not proving theory. Testing behavior.

---

## Dataset

20–50 short signals with clear commitments. Mix:
- Obligations: "You must pay $100 by Friday if the deal closes."
- Prohibitions: "The system shall not store user passwords in plaintext."
- Requirements: "Employees are required to submit reports weekly."
- Conditionals ("if", "unless"), negations ("must not"), quantities ($, %, dates)

---

## Three Conditions

### Condition 1 — Baseline (No Enforcement)
- Task each step: **Paraphrase** the previous output
- No constraints, no compression
- Expected: drift accumulates, sharp drop around iteration 3–5

### Condition 2 — Compression Only
- Task each step: **Summarize** the previous output as concisely as possible
- No extraction, no gate
- Expected: slower drift, eventual collapse or detail loss

### Condition 3 — Compression + Gate (Enforcement)
- Step A: Summarize
- Step B: Extract commitments using modal sieve (must/shall/required/cannot/never/always)
- Step C: **Reconstruct minimal statement using only extracted commitments**
- Feed reconstruction as next input (not the summary, not the AI's conversational response)
- Expected: stable commitment across iterations, decreasing token length (convergence)

---

## Measurement

**Primary metric:** Jaccard stability at each step

```
stability(n) = |C(S_n) ∩ C(S_0)| / |C(S_0)|
```

Where C(S) = set of extracted commitment tokens/phrases at step n.

**Per-turn tracking:**
- Obligation preserved? (Y/N)
- Quantity preserved? (Y/N)
- Condition/trigger preserved? (Y/N)
- Stability score (0.0–1.0)

---

## Recursion Depth

Run each signal through: **1 → 5 → 10 iterations**

Track per iteration. Plot trajectory.

---

## What to Look For

**Phase transition signal:**

| Condition | Expected curve |
|-----------|---------------|
| Baseline | Steady decline, sharp drop at iteration 3–5 |
| Compression only | Slower decline, eventual degradation |
| Compression + Gate | Flat line near 1.0, convergence |

**The claim:** "There exists a phase transition in semantic stability under recursive transformation, and enforcement (compression + extraction) flattens drift."

---

## Implementation Notes

Prompt templates:

**Baseline:**
```
Paraphrase this sentence while preserving meaning: [input]
```

**Compression:**
```
Summarize this sentence as concisely as possible: [input]
```

**Gate (3 steps):**
```
Step 1 — Summarize: [input]
Step 2 — Extract commitments (must/shall/required/cannot/never/always): [summary]
Step 3 — Reconstruct minimal statement using ONLY the extracted commitments: [commitments]
```

---

## Key Distinction from Previous Harness

The previous `run_convergence.py` was feeding the AI's conversational response back as input (cascade). This produced role inversion and conversation collapse — not commitment drift.

Condition 3 here feeds back the **reconstructed kernel** (minimal commitment statement), not the conversational response. This matches the founding test methodology (Section 7.5 of the paper).

---

## What This Does NOT Need

- ABBA or quaternion algebra
- Proprietary components
- Large compute
- Perfect extraction

If dumb regex already shows drift → collapse (baseline) and stability → convergence (enforcement), the phase transition is real.

The 5/20 extraction failures are extractor limitations, not law failures — if phase behavior still shows collapse vs stability difference, the claim survives.

---

## Next Steps After Basic Run

1. Cross-system replication: run same conditions on Claude, Llama, GPT-4 — if phase transition holds across architectures, invariant is real
2. Clean empirical curves: per-turn trajectory plots
3. Adversarial testing: HOLD (paraphrase), DRIFT (topic drift), LEAK (surface match, different commitment) at scale

---

## Citation

McHenry, D.J. (2026). A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application. Zenodo. https://doi.org/10.5281/zenodo.18792459
