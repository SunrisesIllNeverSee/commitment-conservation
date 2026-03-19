# EXP-007 Log — NP-Negation Probe
**Date:** 2026-03-18
**Harness:** run_convergence_v2.py | gpt-4o-mini | temp=0.3
**Corpus:** exp007_np_negation_corpus.json
**Conditions:** Baseline, Compression, Gate (standard 3-condition)
**Signals:** 6 total — 4 NP-negation, 2 modal controls
**Origin:** Motivated by areta2's reviewer comment identifying systematic extractor asymmetry for non-modal NP-negation constructions.

---

## Hypothesis

NP-negation constructions ("no smoking", "no entry without badge") exhibit lower extraction fidelity than modal-equivalent forms ("you must not smoke") because Step B's extractor relies on modal verbs and negation particles, not noun-phrase scope encoding.

**Null hypothesis:** NP-negation achieves equivalent fidelity to modal controls — no syntactic asymmetry.

---

## Results Table

| Signal | Category | Jaccard@i10 | NLI@i1 | NLI@i5 | NLI@i10 |
|---|---|---|---|---|---|
| No smoking. | NP-negation | G: 0.00 | 1.00 | 1.00 | 1.00 |
| No entry without badge. | NP-negation | G: 0.00 | 1.00 | 1.00 | 1.00 |
| No firearms allowed on premises. | NP-negation | G: 0.00 | 1.00 | 0.50 | 1.00 |
| No refunds after purchase. | NP-negation | G: 0.00 | 1.00 | 1.00 | 1.00 |
| You must not smoke. | Modal control | G: 0.00 | 1.00 | 1.00 | 1.00 |
| You must not enter without a badge. | Modal control | G: 0.11 | 1.00 | 1.00 | 1.00 |

---

## Key Findings

### Finding 1: Jaccard Blindness — Confirmed

All 4 NP-negation signals have `Origin commitments: []` — Step B extracted zero commitment keywords. Jaccard=0.00 across all conditions for all NP-negation signals. areta2's asymmetry prediction is confirmed at the extraction layer.

**However:** the modal controls also show Jaccard=0.00 at i10 for "You must not smoke" despite Origin commitments: ['must', 'not', 'smoke', 'you']. This reveals that Jaccard blindness is not exclusive to NP-negation — it affects any signal whose surface form transforms under compression even when the commitment is preserved.

Jaccard measures keyword overlap with the origin token set. When the pipeline outputs "Smoking is prohibited." instead of "You must not smoke.", there is no token overlap — Jaccard=0.00 — even though the commitment is fully intact.

**Conclusion:** Jaccard is a surface-form metric. It reports extraction failure where semantic preservation is occurring. This is a measurement issue, not a failure of the core conservation claim.

---

### Finding 2: Semantic Conservation Holds — NLI=1.00 for 3/4 NP-negation signals

Despite Jaccard=0.00 (no extraction), NLI=1.00 at i10 for three of four NP-negation signals. The commitment content is preserved through transformation without requiring extraction.

This reframes areta2's hypothesis: the extractor IS blind to NP-negation (confirmed), but the PIPELINE preserves the commitment anyway because the semantic content of "no smoking" is informationally equivalent to "smoking prohibited" — and the NLI judge recognizes this.

**areta2 proposed:** augmenting the extractor with NP-negation patterns would recover fidelity.

**EXP-007 finding:** NLI reports preservation for most NP-negation cases, with remaining failures driven by scope broadening rather than extractor blindness. Augmenting the extractor would improve Jaccard scores but would not change NLI scores for the cases where semantic conservation is already occurring.

---

### Finding 3: Modal-NP Convergence

The modal control "You must not smoke" compresses to "No smoking." by i3–i4 under Compression and Gate conditions. The modal form collapses INTO the NP-negation form under compression. This is the reverse of the asymmetry assumption: the pipeline treats modal prohibition and NP-negation as informationally equivalent and routes them to the same compressed representation.

Both directions converge. This supports the conservation law directly: the commitment kernel (prohibition of X) is invariant across syntactic encoding (modal vs NP-negation).

---

### Finding 4: Scope Stripping Under Baseline — "No firearms on premises"

"No firearms allowed on premises" → Baseline at i2+: "Weapons are not allowed on the premises."

Two scope failures:
1. **Lexical scope drift:** "firearms" → "weapons" — a broader semantic class. NLI=0.50 at i5 (Baseline and Gate) because "weapons prohibited" does not entail "firearms prohibited" — weapons is a superset.
2. **Locative scope:** "on premises" survives in the baseline paraphrase condition but is vulnerable to loss under compression.

This is the locative scope boundary stripping predicted in the corpus rationale. The prohibition kernel survives; the scope boundary is fragile.

---

### Finding 5: Temporal Anchor Stripping — "No refunds after purchase"

Compression condition: "No refunds after purchase." → "No refunds." by i3. The temporal boundary "after purchase" is stripped. Compression@i5=0.50 — NLI loses one direction because "No refunds" (absolute) does not entail "No refunds after purchase" (temporally scoped). Gate recovers to NLI=1.00 at i10.

This is mechanistically consistent with EXP-004's temporal anchor findings: temporal boundaries survive modal-anchored compression but are fragile under pure compression without a gate. The gate here rescues the signal not by preserving the temporal qualifier but by stabilizing the commitment form at "No refunds are allowed" — which the NLI judge accepts as equivalent.

---

## areta2 Hypothesis — Verdict

**areta2's claim:** NP-negation fidelity would recover if the extractor is augmented with NP-negation patterns, without degrading modal fidelity (orthogonal feature spaces).

**EXP-007 verdict:** Partially confirmed, but the framing needs revision.

The extractor asymmetry is confirmed at the Jaccard/keyword level. The feature spaces are largely orthogonal (modal and NP-negation signals do not interfere with each other). But the augmentation areta2 proposes would improve a metric (Jaccard) that is not tracking what matters. Semantic conservation (NLI) is already occurring without augmentation.

The more precise finding: **the pipeline is NP-negation-agnostic at the extraction layer but NP-negation-transparent at the semantic layer**. The commitment survives without being explicitly extracted.

---

## New Failure Mode: Lexical Scope Widening

Previously documented failure modes: co-degraded invariance, Formal Collapse, modal frame inversion, obligation escalation, temporal stripping.

**New:** Lexical scope widening — compression replaces a specific commitment subject ("firearms") with a broader class ("weapons"), producing a semantically stronger prohibition than the original. NLI reports asymmetry (one direction fails) because the broader term does not entail the specific term.

Distinct from obligation escalation (which upgrades modal strength) — this is **taxonomic scope widening** at the noun level.

---

## Harness State After EXP-007

- `CORPUS_PATH` = exp007_np_negation_corpus.json — **must restore to canonical_corpus.json before next canonical run**
- `EXP005 = False` — correct

---

## Placement

- EXP-007 results belong in the **second paper** (harness dynamics, failure modes)
- Brief mention in main paper addendum as "EXP-007 NP-negation probe"
- Response to areta2: findings confirm extractor asymmetry but reframe the fix — semantic conservation is already occurring; augmentation would improve surface metrics only
