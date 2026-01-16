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
