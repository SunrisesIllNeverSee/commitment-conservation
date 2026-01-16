# A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application

## Abstract

This repository accompanies a preprint introducing a conservation law for commitment in language under transformative compression and recursive application. We formalize commitment as an information-bearing invariant that must be preserved across paraphrase, summarization, and iterative reuse, even as surface form and representation change.

We propose a falsifiability framework based on compression-driven stress tests and lineage-aware evaluation, distinguishing semantic preservation from mere token retention. The framework is model-agnostic and applies to both human and machine-generated language.

This repository serves as a public, timestamped disclosure of the theoretical law, evaluation criteria, and architectural relationships. Implementation mechanisms are intentionally out of scope.

---

## Core Claims

- **Commitment Conservation:** Meaningful commitments in language obey a conservation constraint under compression and recursive reuse.
- **Dual Stress Regime:** Preservation must hold under both transformative compression and recursive application, exposing failure modes not captured by retrieval benchmarks.
- **Falsifiability:** Commitment preservation can be empirically tested using compression-based stress tests and lineage-aware metrics.

---

## Empirical Results

We tested standard transformer-based compression (baseline) versus commitment-enforced compression on 5 signals over 10 recursive iterations:

| Metric | Baseline | Enforced | Improvement |
|--------|----------|----------|-------------|
| **Recursion Stability** | 20.0% | 60.0% | **+40 pp** |
| **Compression Fidelity** | 63.8% | 78.9% | **+15 pp** |

**Key Finding:** Simple commitment enforcement (extracting obligations before compression and re-appending if lost) triples stability from 20% to 60%. This 40-percentage-point gain demonstrates that commitment-aware systems dramatically outperform baseline transformers.

**Baseline Results:** Only 1 of 5 signals (20%) maintained commitment integrity under standard recursive summarization. Four signals exhibited complete drift after a single transformation cycle.

**Enforcement Results:** With commitment preservation, 3 of 5 signals (60%) maintained full integrity through 10 iterations. This validates that tracking deontic force prevents catastrophic loss.

**Full experimental data:** 
- Baseline: `harness/outputs/experiment_results.json`
- Comparison: `harness/outputs/enforcement_comparison.json`

**Interpretation:** These results empirically validate the paper's core thesis. Probabilistic transformations without commitment enforcement exhibit significant drift (Corollary 3.3). The 40pp improvement demonstrates the value of conservation-aware architectures.

---

## Resources

- **Zenodo (DOI, all versions):** <https://doi.org/10.5281/zenodo.18267278>  
- **Zenodo (current version):** <https://doi.org/10.5281/zenodo.18271102>  
- **GitHub Repository:** <https://github.com/SunrisesIllNeverSee/commitment-conservation>

---

## Licensing & Scope

This work is released under **Creative Commons Attribution 4.0 International (CC BY 4.0)**.

This repository includes an operational evaluation harness and corpus supporting the experiments described in the paper.

Core implementation details related to production deployment, enforcement, and system integration are intentionally out of scope.

---

## Attribution & Contact

**Author:** Deric J. McHenry  
**Copyright:** © 2026 Ello Cello LLC. All rights reserved.  
**Affiliation:** Ello Cello LLC

For academic or research correspondence, please reference the Zenodo DOI above.
