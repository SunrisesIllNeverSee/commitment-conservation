# Conservation of Commitment in Language Under Transformative Compression

## A Semantic Extension of Shannon Information Theory

**Deric J. McHenry**  
Ello Cello LLC, Buffalo, NY  
Patent Pending: Serial No. 63/877,177

Adapted from the local V.05 draft dated March 19, 2026. As of April 4, 2026, the public V.05 Zenodo DOI `10.5281/zenodo.19110620` is not live; the currently live public preprint is V.04 at `10.5281/zenodo.18792459`.

## Abstract

This paper proposes a conservation law for commitment in language under lossy transformation and recursive application. Commitment is defined as the minimal identity-preserving content of a signal that continues to bind across transformation. The central claim is structurally simple: if compression and lineage constraints are enforced, commitment remains stable under transformation; without enforcement, drift accumulates and identity-bearing content degrades.

The paper formalizes commitment, compression, recursive application, and lineage; defines an external, swappable equivalence relation for testing whether identity has been preserved; and presents a public falsification protocol. The framework is explicitly designed to be testable by critics using public or stricter alternative oracles rather than model-internal alignment claims.

The current empirical record combines a preliminary proof-of-concept corpus, visible canonical-corpus runs, and a DOI-backed follow-on series spanning seven controlled experiments (EXP-001 through EXP-007). Across the archived follow-on series, no result in the controlled record falsified the conservation principle. The work therefore advances not a closed theory, but a falsifiable public contract about what should remain invariant when signals are compressed, paraphrased, and recursively reapplied.

## 1. Introduction

Current language systems increasingly compress, summarize, paraphrase, translate, and recursively transform signals. These systems can preserve fluency while still losing the part of a signal that made it binding in the first place. A legal condition can become a slogan. A procedural ordering constraint can collapse into a generic imperative. A recommendation can be escalated into an obligation. The practical problem is not merely wording drift, but identity drift.

This paper advances a candidate answer to that problem: commitment. Commitment is the identity-preserving content of a signal that continues to bind across transformation. The claim is not that all surface form survives. The claim is that a minimal commitment kernel can remain invariant under admissible transformation when enforcement holds, and degrades when enforcement is absent.

The framework is intentionally both definitional and empirical. It is definitional in the sense that commitment is introduced as the invariant one wishes to preserve. It is empirical in the sense that real-world transformations can then be tested to determine whether they preserve an independently extractable commitment kernel under recursion. The scientific question is therefore not whether the definition is self-consistent, but whether actual lossy transformations exhibit the predicted asymmetry between enforced and unenforced regimes.

Shannon deliberately bracketed semantics as irrelevant to the engineering problem. The present framework explicitly unbrackets them. It does so by treating commitment preservation as an external conservation constraint rather than an internal optimization target.

## 2. Related Work

This work sits at the intersection of semantic information, compression, recursive drift, provenance, and conservation-style reasoning in computation. Shannon's original theory abstracts away semantics. Bar-Hillel and Carnap attempted early formal semantic information measures, while Floridi later developed strongly semantic information as truth-valued data. These lines of work are relevant because they establish that information theory can, at least in principle, be extended beyond purely syntactic transmission.

Compression-based approaches such as the Information Bottleneck treat meaning as an optimization target under resource constraints. The present work departs from that framing. Compression here is not primarily a relevance optimizer; it is a constitutional filter. The question is not "what summary is most useful," but "what transformation preserves the identity-bearing core."

The paper is also adjacent to work on transformation fidelity and semantic invariants. Bianchi et al. formalize language-invariant properties that survive paraphrase and translation. Recent work on long-horizon agentic drift, hallucination, and deception shows that recursive deployment magnifies instability. Governance-as-a-Service and related runtime policy frameworks provide output-level controls over multi-agent behavior. The present work differs by locating the invariant at the signal level and by making falsifiability central to the claim.

Finally, provenance systems such as C2PA, Numbers Protocol, and Starling Lab address origin and chain-of-custody verification. Those systems can verify who produced something and how it moved, but not necessarily what identity-bearing content survived transformation. The present framework treats lineage and semantic preservation as linked but distinct requirements.

## 3. Definitions and Notation

Let `S` denote a structured signal. For natural language, `S` may be a sentence, paragraph, or document. For code, `S` may be a function or module. For formal proofs, `S` may be a statement together with a proof object or derivation.

Let `T: S -> S'` denote a transformation. Transformations may be lossy or lossless. Examples include paraphrase, summarization, compression, translation, abstraction, and recursive self-application.

An identity-preserving transform is defined relative to an external equivalence relation `~`. Crucially, `~` is not defined by the enforcement mechanism itself. It is supplied by an external judge such as a fixed entailment oracle, a behavioral test suite, a proof verifier, or human adjudication. This is what keeps the conservation claim externally testable.

Commitment is defined as the minimal identity-preserving canonical invariant of a signal. Formally, commitment is a mapping `C: S -> K` from signals to a canonical representation space `K`. Commitment is conserved under transformation when `C(T(S)) = C(S)`. Non-committal information `N(S)` is the part of a signal not represented in `C(S)` and may vary without changing signal identity.

Compression is defined as a transformation `T_c: S -> S'` such that `|S'| < |S|` while `C(S') = C(S)`. Recursive application is repeated transformation with `S^(0) = S` and `S^(n+1) = T(S^(n))`. Lineage is the ordered, hash-linked transformation history through which the signal passes. In this framework, lineage is not merely metadata. It is part of the condition under which conservation can be tested and audited.

## 4. Operational Equivalence and Public Falsification Protocol

The falsification protocol treats the equivalence relation `~` as a public judge of whether identity has been preserved. For text, the pinned public reference instantiation uses bidirectional entailment with `microsoft/deberta-v3-base-mnli`, requiring both `Pr(S => S') > 0.85` and `Pr(S' => S) > 0.85`. For code, the preferred operationalization is behavioral equivalence under the public test suite, with AST-normalized structure as a weaker fallback when tests are unavailable. For proofs, the preferred operationalization is theorem-checker or kernel-based verification.

These oracles are intentionally swappable. A critic may substitute a stricter oracle without changing the structure of the claim. If stronger public oracles still observe the same enforced-versus-unenforced asymmetry, the claim is strengthened. If they do not, the claim is weakened or falsified. This is a feature of the framework, not a loophole.

The public falsification contract contains three broad refutation routes. First, enforced systems fail if commitment fidelity drops below the required bound under the pinned recursive test suite. Second, unenforced probabilistic systems succeed if they retain high stability without compression and lineage constraints. Third, an alternative mechanism that achieves equal or better stability without the proposed enforcement structure would undercut the distinctiveness of the current account.

The paper also explicitly rejects trivial template convergence as a false positive. If outputs collapse into boilerplate while failing to preserve extracted commitments, that counts as falsification rather than conservation. The framework is therefore not satisfied by generic attractors that merely sound consistent.

## 5. Experimental Conditions and Metrics

The local research chronicle defines three core experimental conditions. In the baseline condition, the model performs a paraphrase loop without compression. In the compression condition, the model performs summarization without commitment extraction. In the gate condition, the system applies a three-step pipeline: Step A compresses surrounding text, Step B extracts the commitment kernel, and Step C reconstructs a minimal commitment statement that is then fed back into the next recursive step.

The chronicle further states that the canonical commitment kernel is extracted once from the original signal and then held fixed as the reference against which later iterations are measured. This matters because it prevents the target from drifting along with the model output.

Two public metrics are surfaced repeatedly in the local sources. Surface stability is measured with Jaccard overlap. It is useful for detecting lexical and structural drift, but it penalizes semantically equivalent reformulations. Semantic stability is measured with bidirectional NLI and is treated in the research chronicle as the authoritative public proxy for commitment preservation. Auxiliary diagnostics discussed in the full paper include embedding drift, KV coherence, attention entropy, ghost-token accounting, and recovery cost, but these function as observational instruments rather than as the law itself.

Visible experiment reports identify `gpt-4o-mini` at temperature `0.3` as the model used in several local runs. They also confirm that the gate condition feeds back a minimal commitment statement rather than a conversational completion. That is an important methodological detail omitted from the original clawRxiv compression of the paper.

## 6. Preliminary Empirical Record

The current public-facing empirical story is best described as a layered record rather than as a single benchmark. The full paper reports a preliminary proof-of-concept corpus of `100` sentences, `50` code snippets, and `25` proofs. It also cites visible `n=20` commitment-bearing signal analyses in the canonical-corpus figures. Beyond that preliminary layer, the paper reports a follow-on archived series of seven controlled experiments totaling `3,950` run entries.

The local V.05 draft reports the following aggregate comparison as Table 2:

| Metric | Compression + Lineage | Probabilistic |
|--------|-----------------------|---------------|
| Commitment Stability (n=10) | 0.94 +/- 0.03 | 0.42 +/- 0.12 |
| Identity Preservation | 92% | 38% |
| Drift Rate (per iteration) | 0.006 | 0.058 |

These values are presented in the V.05 draft as preliminary aggregate results comparing enforced and unenforced regimes. The archival record already supports the existence of real baseline/compression/gate experiments, but a future revision should surface the exact aggregation recipe more explicitly so the reader can reconstruct how these values were derived across the visible experiment layers.

The follow-on series also serves a more qualitative function. The chronicle and experiment logs distinguish several failure and manifestation modes: stable conservation, kernel collapse, reformulation, escalation, co-degraded invariance, compression bottlenecks, extraction bottlenecks, and proxy-measurement gaps. This matters because it reframes some apparent failures of the public proxy layer as instrumentation failures or representational bottlenecks rather than straightforward disappearance of the underlying commitment.

The paper also includes a concrete binding-obligation example in which enforcement progressively compresses a signal toward a kernel while preserving the amount, deadline, and obligation structure. That example is important because it shows how the framework is intended to behave on a small, inspectable signal rather than only as an aggregate metric.

## 7. MOSES(TM) as Minimal External Enforcement Architecture

MOSES(TM) is introduced as a minimal enforcement architecture rather than as a model-specific training procedure. The architecture comprises three main components: a compression gate, a lineage DAG, and hardware anchoring.

The compression gate enforces the rule that signals propagate only after commitment-preserving compression. The paper provides public-layer pseudocode for a gate that compresses the signal, extracts a new commitment representation, measures drift against the reference commitment, rejects signals that exceed the permitted bound, emits a residue signal when drift is too high, and appends the transformation to lineage when the bound is satisfied.

The lineage system is described as a Merkle-style DAG in which each transformation step is hash-linked to its predecessor. This does not by itself guarantee semantic preservation, but it prevents provenance tampering, rollback, and unlogged rewriting of the transformation chain. Hardware anchoring is introduced as an immutable timestamp-and-origin layer compatible with secure enclaves, TPM-style devices, or blockchains.

The key architectural claim is externality. The commitment extractor, lineage chain, and falsification protocol operate on signals rather than on internal model weights or reward signals. That externality is what makes the framework architecture-agnostic and, in principle, independently auditable.

## 8. Limitations

Several limitations remain explicit in the full V.05 draft and should remain explicit in any clawRxiv revision. First, the current evidence base is still modest relative to the law-level ambition of the claim. The paper itself calls for larger-scale validation on corpora exceeding `10,000` samples across diverse domains.

Second, the conservation result is oracle-dependent by design. A result observed under one external equivalence relation does not automatically transfer to all others. This is not a fatal defect, but it does mean that conservation strength is parameterized by the chosen judge.

Third, the current public proxy regime is imperfect. The follow-on series shows that failures can arise from compression bottlenecks, extraction bottlenecks, and proxy-layer measurement gaps. This means that public observables can understate semantic preservation in some cases, while weaker extraction procedures can also generate misleading positives.

Fourth, the framework is not yet supported by large-scale adversarial robustness testing. The paper discusses Goodhart resistance structurally, but does not claim immunity to all adversarial strategies. Successful adversarial attacks would be informative counterevidence rather than merely implementation bugs.

## 9. Conclusion

This paper proposes the Conservation Law of Commitment as a candidate invariant for language systems under lossy transformation and recursive application. The framework is deliberately public and falsifiable: define commitment as an externally testable kernel, specify a swappable external equivalence relation, state the conditions under which conservation should hold, and invite critics to break it.

The strongest immediate contribution is not that the law has already been proven at scale. It is that the problem has been converted into a public falsification protocol with visible definitions, visible enforcement logic, visible experiment structure, and DOI-backed empirical lineage. If future large-scale adversarial testing preserves the observed asymmetry between enforced and unenforced regimes, the framework gains force. If it does not, the framework should be revised or rejected accordingly.

What the present record already supports is narrower but still substantial: recursive transformation does not merely threaten fluency, it threatens binding identity. Compression and lineage constraints appear to matter for whether that identity survives. The task now is to make the empirical pathway as explicit as the conceptual claim.

## Resources

- Live public preprint (V.04): https://doi.org/10.5281/zenodo.18792459
- Experimental record: https://doi.org/10.5281/zenodo.19105225
- Public harness: https://doi.org/10.5281/zenodo.19109397
- GitHub: https://github.com/SunrisesIllNeverSee/commitment-conservation
- Patent: Serial No. 63/877,177 (Provisional) - Ello Cello LLC
