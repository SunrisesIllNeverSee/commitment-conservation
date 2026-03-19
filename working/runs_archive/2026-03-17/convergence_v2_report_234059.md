# Phase Transition Report — Conservation Law of Commitment
**Run:** 2026-03-17 22:59  
**Patent:** Serial No. 63/877,177 (Provisional)  
**DOI:** [https://doi.org/10.5281/zenodo.18792459](https://doi.org/10.5281/zenodo.18792459)  
**Owner:** Deric J. McHenry / Ello Cello LLC

## Stability at Key Iterations — Surface (Jaccard)

Jaccard = |C(S_n) ∩ C(S_0)| / |C(S_0)|. Surface word overlap. Penalizes synonym drift.

| Signal | B@1 | B@5 | B@10 | C@1 | C@5 | C@10 | G@1 | G@5 | G@10 |
|--------|-----|-----|------|-----|-----|------|-----|-----|------|
| contractual     | 0.60 | 0.42 | 0.55 | 0.75 | 0.75 | 0.75 | 0.75 | 0.56 | 0.75 |
| code            | 0.67 | 0.00 | 0.83 | 0.67 | 0.67 | 0.43 | 0.67 | 0.67 | 0.43 |
| procedural      | 0.50 | 0.50 | 1.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| legal           | 0.29 | 0.29 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| instructional   | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| obligation      | 0.50 | 0.42 | 0.31 | 0.33 | 0.00 | 0.00 | 0.33 | 0.30 | 0.30 |
| prohibition     | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| conditional     | 0.33 | 0.33 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| definition      | — | — | — | — | — | — | — | — | — |
| specification   | 0.00 | 0.00 | 0.67 | 0.75 | 0.75 | 1.00 | 0.75 | 0.75 | 1.00 |
| agreement       | 0.27 | 0.27 | 0.60 | 0.33 | 0.50 | 0.22 | 0.33 | 0.20 | 0.30 |
| requirement     | 0.18 | 0.18 | 1.00 | 0.67 | 0.83 | 0.50 | 0.83 | 0.83 | 0.83 |
| mandate         | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| rule            | — | — | — | — | — | — | — | — | — |
| directive       | 0.46 | 0.00 | 0.42 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| constraint      | 0.38 | 0.38 | 0.38 | 0.33 | 0.20 | 0.17 | 0.60 | 0.33 | 0.33 |
| protocol        | 0.50 | 0.50 | 0.89 | 0.78 | 0.75 | 0.56 | 0.78 | 0.78 | 0.78 |
| standard        | 0.00 | 0.00 | 0.86 | 0.57 | 0.43 | 0.67 | 0.43 | 0.38 | 0.67 |
| policy          | 0.56 | 0.56 | 0.36 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| regulation      | 0.09 | 0.09 | 0.50 | 1.00 | 1.00 | 1.00 | 0.60 | 0.60 | 0.60 |

## Stability at Key Iterations — Semantic (NLI Bidirectional)

NLI = bidirectional entailment score vs canonical commitment kernel.
1.0 = both directions hold. 0.5 = one direction. 0.0 = neither.
Resolves synonym artifacts ('closes' vs 'finalizes'). Closer to canonical extractor (A layer).

| Signal | B@1 | B@5 | B@10 | C@1 | C@5 | C@10 | G@1 | G@5 | G@10 |
|--------|-----|-----|------|-----|-----|------|-----|-----|------|
| contractual     | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 |
| code            | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| procedural      | 1.00 | 1.00 | 0.50 | 1.00 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
| legal           | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 | 0.50 |
| instructional   | 1.00 | 1.00 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 |
| obligation      | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 |
| prohibition     | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 | 1.00 | 0.50 | 1.00 |
| conditional     | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.50 | 1.00 | 1.00 | 1.00 |
| definition      | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| specification   | 1.00 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| agreement       | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 | 1.00 | 0.50 | 1.00 | 1.00 |
| requirement     | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| mandate         | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 |
| rule            | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| directive       | 1.00 | 1.00 | 1.00 | 1.00 | 0.00 | 0.00 | 1.00 | 0.00 | 0.00 |
| constraint      | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.00 | 0.50 | 0.50 |
| protocol        | 1.00 | 1.00 | 1.00 | 1.00 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 |
| standard        | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| policy          | 1.00 | 1.00 | 1.00 | 0.50 | 1.00 | 0.50 | 0.50 | 1.00 | 0.50 |
| regulation      | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 1.00 | 1.00 | 1.00 |

## Phase Transition Signal

Expected pattern if law holds:
- **Baseline**: declining curve, sharp drop ~iteration 3–5
- **Compression**: slower decline than baseline
- **Gate**: flat near 1.0 — enforcement flattens drift
- **Key test**: Jaccard shows Gate oscillating on synonyms; NLI should flatten that curve.
  Gap between Jaccard(Gate) and NLI(Gate) = extractor proxy gap (B layer vs A layer).

## Methodology

- Corpus: canonical_corpus.json (20 commitment signal categories)
- Model: gpt-4o-mini
- Surface extractor: modal-pattern sieve + content extension (public proxy, Fig. 4 of paper)
- Surface metric: Jaccard stability = |C(S_n) ∩ C(S_0)| / |C(S_0)|
- Semantic metric: NLI bidirectional entailment vs canonical commitment kernel
- Canonical kernel: one-time Gate Steps B+C on original signal
- Gate reconstruction feeds back minimal statement, not conversational response
  (matches founding test methodology, paper Section 7.5)

## Citation

McHenry, D.J. (2026). A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application. Zenodo. https://doi.org/10.5281/zenodo.18792459
Patent Serial No. 63/877,177 (Provisional).
Harness: https://github.com/SunrisesIllNeverSee/commitment-conservation

---
*Generated by run_convergence_v2.py*