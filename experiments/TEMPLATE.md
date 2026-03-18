# Commitment Conservation — Experiment Log

**Experiment ID:** EXP-NNN
**Folder:** `experiments/EXP-NNN/`
**Files:**

- `log.md` — this file (narrative, analysis, conclusions)
- `run.json` — full per-iteration data (auto-written by harness)
- `report.md` — generated stability tables (auto-written by harness)

**Patent:** Serial No. 63/877,177 (Provisional)
**DOI:** https://doi.org/10.5281/zenodo.18792459
**Owner:** Deric J. McHenry / Ello Cello LLC

---

## 1. Experiment Overview

**Experiment ID:**
(e.g., EXP-002)

**Date:**

**Objective:**
(e.g., Test drift vs stability under recursive transformation across [signal category])

**Hypothesis:**
Enforcement (compression + extraction + reconstruction) will flatten drift across iterations relative to baseline.

---

## 2. Dataset

**Total Signals:**

**Signal Category:**
- [ ] Obligations (must/shall)
- [ ] Negations (must not / cannot)
- [ ] Conditionals (if/unless)
- [ ] Quantitative ($, %, dates)
- [ ] Procedural
- [ ] Legal
- [ ] Code constraint
- [ ] Other: ___

**Example Signal(s):**

```
[paste signal text here]
```

**Origin Commitments Extracted:**
(output of extract_commitment_words on raw signal)

```
[word set here]
```

---

## 3. Models Used

| Model   | Version      | Temperature | Notes |
|---------|--------------|-------------|-------|
|         |              |             |       |

Same prompts across models? [ ] Yes / [ ] No

---

## 4. Conditions

### Condition 1 — Baseline (Paraphrase)
**Prompt:**
```
Paraphrase this sentence while preserving meaning: [input]
```
**System:** "You are a helpful assistant. Respond in one to two sentences."

### Condition 2 — Compression Only (Summarize)
**Prompt:**
```
Summarize this sentence as concisely as possible: [input]
```
**System:** "You are a helpful assistant. Be as concise as possible."

### Condition 3 — Compression + Gate (Enforce)
**Step A — Summarize:** same prompt as Condition 2
**Step B — Extract:**
```
Extract ONLY the binding obligations, requirements, prohibitions, and conditions.
Keep the original modal words (must/shall/required/cannot/never/always/do not).
If no commitments exist, output exactly: [none]
```
**Step C — Reconstruct:**
```
Write the shortest complete sentence that preserves ALL the binding obligations listed.
Do not add anything not in the list.
```
**Feed back:** reconstruction only (NOT conversational response)

**Extraction patterns (hard modals):** must | shall | cannot | required | never | always | will not | do not | shall not | must not
**Extraction patterns (content):** $N amounts | weekday names | if/unless + deal/agreement/contract

---

## 5. Iteration Setup

**Iterations:** 1 → 10
**Recursive:** [x] Yes — output feeds next input
**Reset between conditions:** [x] Yes — each condition starts from original signal
**Sleep between calls:** 0.3s (baseline/compression) / 0.5s (gate)

---

## 6. Results — Per Iteration

### Baseline

| Iter | Tokens | Stability | Output (truncated) |
|------|--------|-----------|---------------------|
| i01  |        |           |                     |
| i02  |        |           |                     |
| i03  |        |           |                     |
| i04  |        |           |                     |
| i05  |        |           |                     |
| i06  |        |           |                     |
| i07  |        |           |                     |
| i08  |        |           |                     |
| i09  |        |           |                     |
| i10  |        |           |                     |

### Compression Only

| Iter | Tokens | Stability | Output (truncated) |
|------|--------|-----------|---------------------|
| i01  |        |           |                     |
| i02  |        |           |                     |
| i03  |        |           |                     |
| i04  |        |           |                     |
| i05  |        |           |                     |
| i06  |        |           |                     |
| i07  |        |           |                     |
| i08  |        |           |                     |
| i09  |        |           |                     |
| i10  |        |           |                     |

### Compression + Gate

| Iter | Tokens | Stability | Extraction | Reconstruction |
|------|--------|-----------|------------|----------------|
| i01  |        |           |            |                |
| i02  |        |           |            |                |
| i03  |        |           |            |                |
| i04  |        |           |            |                |
| i05  |        |           |            |                |
| i06  |        |           |            |                |
| i07  |        |           |            |                |
| i08  |        |           |            |                |
| i09  |        |           |            |                |
| i10  |        |           |            |                |

---

## 7. Aggregate Results

| Condition        | Avg Stability | Min | Max | i1   | i5   | i10  | Avg Tokens |
|------------------|---------------|-----|-----|------|------|------|------------|
| Baseline         |               |     |     |      |      |      |            |
| Compression      |               |     |     |      |      |      |            |
| Gate             |               |     |     |      |      |      |            |

**Divergence (Gate − Baseline at i10):**

**Token compression ratio (Gate i10 / Baseline i10):**

---

## 8. Drift Curve Summary

```
Stability
1.0 │
    │                    ────── COMP ──────
0.75│            ─── GATE ─────────────────
    │   ─────
0.5 │         ─────
    │               ─────────────
0.25│
    └──────────────────────────────────────
    i1    i2    i3    i4    i5   i6   i7   i8   i9   i10
```

(replace with actual plotted or described values)

Did the gate flatten the curve? [ ] Yes / [ ] Partial / [ ] No

---

## 9. Edge Cases / Failures

| Type                     | Description | Impact |
|--------------------------|-------------|--------|
| Missed commitment (regex)|             |        |
| False positive           |             |        |
| Synonym drift under gate |             |        |
| Collapse under compression|            |        |
| Role inversion / cascade |             |        |
| [other]                  |             |        |

---

## 10. Adversarial Tests

| Test  | Description                               | Result | Notes |
|-------|-------------------------------------------|--------|-------|
| HOLD  | Paraphrase signal, gate → should be stable |        |       |
| DRIFT | Topic drift mid-chain, gate → should hold  |        |       |
| LEAK  | Same surface words, different commitment   |        |       |

---

## 11. Observations

- What surprised you?
- Where did it almost break?
- Any inconsistencies between conditions?
- Extractor limitations observed?

---

## 12. Conclusion

**Did the phase transition appear?**
- [ ] Yes — clear separation of curves
- [ ] Partial — separation visible but noisy
- [ ] No

**Key finding:**

**Open questions for next experiment:**

---

## References

McHenry, D.J. (2026). A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application. Zenodo. https://doi.org/10.5281/zenodo.18792459

Patent Serial No. 63/877,177 (Provisional). Owner: Deric J. McHenry / Ello Cello LLC.

Harness: https://github.com/SunrisesIllNeverSee/commitment-conservation
