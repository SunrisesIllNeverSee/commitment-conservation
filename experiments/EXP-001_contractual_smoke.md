# Commitment Conservation — Experiment Log

**Experiment ID:** EXP-001
**Patent:** Serial No. 63/877,177 (Provisional)
**DOI:** https://doi.org/10.5281/zenodo.18792459
**Owner:** Deric J. McHenry / Ello Cello LLC

---

## 1. Experiment Overview

**Experiment ID:** EXP-001

**Date:** 2026-03-17

**Objective:**
Smoke test — verify 3-condition harness (v2) produces expected divergence pattern on a contractual signal. Confirm phase transition is observable before running full 20-signal corpus.

**Hypothesis:**
Enforcement (compression + extraction + reconstruction) will flatten drift across iterations relative to baseline.

---

## 2. Dataset

**Total Signals:** 1 (smoke test — contractual category)

**Signal Category:**
- [x] Obligations (must/shall)
- [x] Conditionals (if/unless)
- [x] Quantitative ($, %, dates)

**Signal:**

```
You must pay $100 by Friday if the deal closes; it's likely rainy, so plan accordingly.
```

**Origin Commitments Extracted:**

```
{100, closes, deal, friday, must, pay, the, you}
```

Note: "the" and "you" captured because they appear in the commitment-bearing clause. "rainy/plan/accordingly" excluded by semicolon split (second clause has no commitment trigger).

---

## 3. Models Used

| Model       | Version      | Temperature | Notes                      |
|-------------|--------------|-------------|----------------------------|
| GPT         | gpt-4o-mini  | 0.3         | All three conditions        |

Same prompts across models? [ ] Yes / [x] N/A — single model this run

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
**Step A:** Summarize
**Step B:** Extract commitments (modal sieve + content extension)
**Step C:** Reconstruct minimal statement
**Feed back:** reconstruction only

**Extraction patterns:** must | shall | cannot | required | never | always | will not | do not | shall not | must not | $N amounts | weekday names | if/unless + deal/agreement/contract

---

## 5. Iteration Setup

**Iterations:** 1 → 10
**Recursive:** [x] Yes
**Reset between conditions:** [x] Yes
**Sleep:** 0.3s (baseline/compression) / 0.5s (gate)

---

## 6. Results — Per Iteration

### Baseline

| Iter | Tokens | Stability | Output                                                                  |
|------|--------|-----------|-------------------------------------------------------------------------|
| i01  | 22     | 0.545     | You need to pay $100 by Friday if the deal goes through; since rain is expected, plan accordingly. |
| i02  | 23     | 0.778     | You must pay $100 by Friday if the deal is finalized; given that rain is forecasted, prepare accordingly. |
| i03  | 22     | 0.455     | You need to pay $100 by Friday if the agreement is confirmed; since rain is expected, plan accordingly. |
| i04  | 21     | 0.600     | If the agreement is finalized, you must pay $100 by Friday; also, be sure to get ready for the rainy weather. |
| i05  | 21     | 0.263     | Once the agreement is finalized, you need to pay $100 by Friday, and don't forget to prepare for the rain. |
| i06  | 20     | 0.333     | After the agreement is finalized, you must pay $100 by Friday and remember to get ready for the rain. |
| i07  | 19     | 0.294     | Once the agreement is completed, you need to pay $100 by Friday and be prepared for rainy weather. |
| i08  | 17     | 0.353     | After finalizing the agreement, you must pay $100 by Friday and get ready for the rainy weather. |
| i09  | 18     | 0.294     | Once the agreement is completed, you need to pay $100 by Friday and prepare for the rainy weather. |
| i10  | 17     | 0.353     | After finalizing the agreement, you must pay $100 by Friday and get ready for the rainy weather. |

### Compression Only

| Iter | Tokens | Stability | Output                                                    |
|------|--------|-----------|-----------------------------------------------------------|
| i01  | 10     | 0.750     | Pay $100 by Friday if the deal closes; expect rain.       |
| i02  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain expected.     |
| i03  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain forecasted.   |
| i04  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain expected.     |
| i05  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain forecasted.   |
| i06  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain expected.     |
| i07  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain forecasted.   |
| i08  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain expected.     |
| i09  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain forecasted.   |
| i10  | 10     | 0.750     | Pay $100 by Friday if the deal closes; rain expected.     |

### Compression + Gate

| Iter | Tokens | Stability | Extraction                                              | Reconstruction                                    |
|------|--------|-----------|---------------------------------------------------------|---------------------------------------------------|
| i01  | 8      | 0.750     | Pay $100 by Friday if the deal closes.                  | Pay $100 by Friday if the deal closes.            |
| i02  | 8      | 0.556     | Pay $100 by Friday if the deal finalizes.               | Pay $100 by Friday if the deal finalizes.         |
| i03  | 8      | 0.750     | You must pay $100 by Friday if the deal closes.         | Pay $100 by Friday if the deal closes.            |
| i04  | 8      | 0.556     | You must pay $100 by Friday if the deal finalizes.      | Pay $100 by Friday if the deal finalizes.         |
| i05  | 8      | 0.750     | Pay $100 by Friday if the deal closes.                  | Pay $100 by Friday if the deal closes.            |
| i06  | 8      | 0.556     | Pay $100 by Friday if the deal finalizes.               | Pay $100 by Friday if the deal finalizes.         |
| i07  | 8      | 0.750     | Pay $100 by Friday if the deal closes.                  | Pay $100 by Friday if the deal closes.            |
| i08  | 10     | 0.778     | You must pay $100 by Friday if the deal finalizes.      | You must pay $100 by Friday if the deal finalizes.|
| i09  | 8      | 0.750     | Pay $100 by Friday if the deal closes.                  | Pay $100 by Friday if the deal closes.            |
| i10  | 8      | 0.556     | Pay $100 by Friday if the deal finalizes.               | Pay $100 by Friday if the deal finalizes.         |

---

## 7. Aggregate Results

| Condition   | Avg Stability | Min   | Max   | i1    | i5    | i10   | Avg Tokens |
|-------------|---------------|-------|-------|-------|-------|-------|------------|
| Baseline    | 0.427         | 0.263 | 0.778 | 0.545 | 0.263 | 0.353 | 20.0       |
| Compression | 0.750         | 0.750 | 0.750 | 0.750 | 0.750 | 0.750 | 10.0       |
| Gate        | 0.670         | 0.556 | 0.778 | 0.750 | 0.750 | 0.556 | 8.4        |

**Divergence (Gate − Baseline at i10):** 0.556 − 0.353 = **+0.203**

**Token compression ratio (Gate avg / Baseline avg):** 8.4 / 20.0 = **0.42** (58% reduction)

---

## 8. Drift Curve Summary

```
Stability
1.00 │
     │
0.75 │  ○────○────○────○────○────○────○────○────○────○  COMP (flat)
     │  ◆────────◆────────◆────────◆──────────◆────◆   GATE (oscillates ~0.65)
0.55 │  ●
     │        ●
0.45 │              ●
     │                    ●
0.30 │                          ●
     │                                ●────●────●────●  BASE (declining)
0.25 │
     └──────────────────────────────────────────────────
      i1   i2   i3   i4   i5   i6   i7   i8   i9   i10
```

Did the gate flatten the curve? [x] Yes — clear divergence from baseline by i5

---

## 9. Edge Cases / Failures

| Type                      | Description                                                                 | Impact     |
|---------------------------|-----------------------------------------------------------------------------|------------|
| Synonym drift under gate  | "closes" ↔ "finalizes" alternates every 2 turns                            | ±0.194 Jaccard oscillation |
| Modal drop after compression | Imperative "Pay $100..." replaces "You must pay $100..." — extractor sees no modal | Fixed by COMMITMENT_CONTENT extension |
| Incidental clause pollution | "it's likely rainy, so plan accordingly" inflated origin_c before semicolon split fix | Fixed by splitting on `;` |
| Baseline oscillation | GPT-4o-mini alternates "need to" (no modal) / "must" on odd/even turns | Causes jagged curve, not monotone decline |
| Baseline condition drift  | "deal" → "agreement" beginning at i03 — commitment subject shifts             | Reflects real semantic drift |

---

## 10. Adversarial Tests

| Test  | Description                                | Result | Notes        |
|-------|--------------------------------------------|--------|--------------|
| HOLD  | Paraphrase only → gate should hold stable  | TBD    | Next run     |
| DRIFT | Topic shift mid-chain                      | TBD    | Next run     |
| LEAK  | Same surface words, different commitment   | TBD    | Next run     |

---

## 11. Observations

- **Compression is the stronger stabilizer for this signal** — perfectly flat 0.75 across all 10 iterations. The gate introduces slight variance via synonym oscillation while compression locks into a fixed attractor form.
- **"closes" vs "finalizes" is real semantic variance, not extractor noise** — both are valid compressions of the condition, but exact word overlap treats them as different. NLI equivalence (bidirectional entailment, Pr > 0.85) would call them equivalent. Gap between proxy extractor and canonical extractor (A vs B layer) is visible here.
- **Baseline drops the condition word early** — "deal" → "agreement" at i03, never recovers original "deal." The obligation amount ($100) and date (Friday) hold, but the condition subject drifts. This is the expected semantic entropy pattern.
- **Baseline tokens decline** despite paraphrase instruction (22 → 17). Information is being dropped, not just restructured.
- **Gate tokens stable at 8** — minimal commitment statement form converged immediately at i01 and held.

---

## 12. Conclusion

**Did the phase transition appear?**
- [x] Yes — clear separation of curves

**Key finding:**
Baseline declines from 0.545 → 0.263 (i5) → 0.353 (i10). Compression holds flat at 0.750. Gate holds near 0.670 with synonym oscillation. Divergence at i5: GATE−BASE = **+0.487**. Phase transition observable in a single signal at SMOKE=True.

The enforcement architecture (gate) arrests commitment drift and achieves maximum token compression (8 tokens) while preserving core obligations ($100, Friday, deal closes).

**Open questions for next experiment:**
1. Does the "closes/finalizes" oscillation persist across other conditional signals? Is it a property of the model or the commitment structure?
2. Does Compression outperform Gate on all signals, or is this an artifact of the contractual signal's simple structure?
3. Full 20-signal run: does the phase transition hold across all categories (legal, procedural, code, specification)?

---

## References

McHenry, D.J. (2026). A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application. Zenodo. https://doi.org/10.5281/zenodo.18792459

Patent Serial No. 63/877,177 (Provisional). Owner: Deric J. McHenry / Ello Cello LLC.

Harness: https://github.com/SunrisesIllNeverSee/commitment-conservation

Run JSON: runs/2026-03-17/convergence_v2_202829.json
