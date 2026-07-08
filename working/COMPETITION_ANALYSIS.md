# The Competition — Who Else Is Doing This?

**Built:** 2026-07-08
**Method:** Six parallel web research agents, each covering one candidate or cluster. Findings cross-checked against CT's specific claim: a conservation law for deontic content with empirical validation, a falsification protocol, and a public harness.

---

## The Bottom Line

**No direct competition exists.** CT is the only work found that combines all four:
1. Conservation law for deontic/commitment content
2. Empirical validation through controlled experiments
3. Explicit falsification protocol
4. Public harness for replication

The field has pieces of this picture but nobody has put them together. The closest approaches each have one or two of the four criteria but not all four.

---

## The Serious Candidates

### 1. Marcolli, Chomsky, Berwick — Conserved Quantity in Syntactic Merge

**This is the closest competitor in mathematical physics approach.**

| Criterion | Status |
|-----------|--------|
| Conservation claim | YES — σ̂ (sigma-hat) is a conserved quantity in Merge operations (∆σ̂ = 0) |
| Empirical validation | NO — mathematical formalization only, no experiments |
| Falsification protocol | NO — no explicit protocol for σ̂ |
| Public harness | NO — no code repository |
| Deontic content | NO — syntactic structure, not semantic/deontic |
| Published where | MIT Press 2025 (book), arXiv:2305.18278, arXiv:2306.10270, arXiv:2311.06189 |

**What they have:** A rigorously defined conserved quantity (σ̂ = b₀(F) + #V(F), the number of leaves in the syntactic forest) that is invariant under Internal and External Merge. The conservation is proven mathematically — Sideward and Countercyclic Merge violate it, which provides a mathematical basis for preferring Internal/External Merge. The work uses Hopf algebras (from QFT renormalization) to formalize the syntax-semantics interface via Birkhoff factorization.

**What they don't have:** No empirical validation of σ̂ conservation in actual language use. No falsification protocol. No public harness. And critically — **they explicitly do NOT claim semantic conservation.** Their framework maintains "autonomy of syntax": Merge is a computational process independent of semantics. The conserved quantity is about syntactic tree structure, not meaning preservation.

**Relationship to CT:** Complement, not competitor. Marcolli has the mathematical physics machinery (Hopf algebras, renormalization, conserved quantities) and the physics pedigree (Connes collaborator, QFT background). CT has the empirical validation, the falsification protocol, and the semantic/deontic focus. The two works operate at different levels: Marcolli at the syntactic-computational level, CT at the semantic-deontic level. A future synthesis is possible — Marcolli's σ̂ could be the syntactic conserved quantity, CT's C(S) the semantic one, and the relationship between them could be the syntax-semantics interface.

**Key citation:** Marcolli, M., Chomsky, N., Berwick, R.C. (2023). "Mathematical Structure of Syntactic Merge." arXiv:2305.18278. MIT Press, 2025.

---

### 2. Kuhn, Farquhar, Gal (Oxford OATML) — Semantic Entropy

**This is the closest competitor in methodology (NLI bidirectional entailment).**

| Criterion | Status |
|-----------|--------|
| Conservation claim | NO — measures uncertainty, not conservation |
| Empirical validation | YES — AUROC 0.83 (TriviaQA), 0.77 (CoQA), extensive ablation |
| Falsification protocol | NO — standard ML evaluation only |
| Public harness | YES — multiple GitHub repos (jlko/semantic_uncertainty, lorenzkuhn/semantic_uncertainty) |
| Deontic content | NO — general semantic content, not deontic |
| Published where | Nature 2024, ICLR 2023 |

**What they have:** A method for measuring semantic uncertainty in LLM outputs by clustering semantically equivalent generations using bidirectional NLI entailment (DeBERTa-v2-xlarge-mnli). Published in Nature. Extensive empirical validation across multiple datasets and models. Public code. Active research group at Oxford.

**What they don't have:** No conservation claim. No falsification protocol. No deontic focus. Their work is about detecting hallucinations, not about whether meaning is conserved under transformation.

**Relationship to CT:** Complement, not competitor. They use the same NLI bidirectional entailment method that CT uses — but for a different purpose. They measure uncertainty (how many distinct meanings does the model produce?); CT measures conservation (does the meaning stay the same under transformation?). The methodological overlap is real and should be cited. Their work validates that NLI bidirectional entailment is a reliable semantic equivalence check (92.7% accuracy on TriviaQA, 95.5% on CoQA), which supports CT's choice of the same method.

**Key citation:** Farquhar, S., Kossen, J., Kuhn, L., & Gal, Y. (2024). "Detecting hallucinations in large language models using semantic entropy." Nature, 630, 625-630.

---

### 3. Tishby Legacy — Information Bottleneck

**This is the closest competitor in information-theoretic framing.**

| Criterion | Status |
|-----------|--------|
| Conservation claim | NO — tradeoff, not conservation |
| Empirical validation | YES (for semantic efficiency, not conservation) |
| Falsification protocol | NO — optimization framework, not a law |
| Public harness | YES — multiple implementations |
| Deontic content | NO — general semantic content |
| Published where | NIPS 1999, ICLR, NeurIPS, Cognitive Science |

**What they have:** The Information Bottleneck (IB) framework formalizes the tradeoff between compression and prediction: minimize I(X;T) while maximizing I(Y;T). Tishby's student Noga Zaslavsky applied IB to semantic systems (color naming, semantic categories) and found that human languages are near-optimal in the IB sense. The "information plane" work (Shwartz-Ziv & Tishby 2017) claimed deep networks compress during training — though this was later contested (Saxe et al. 2018).

**What they don't have:** No conservation claim. IB is explicitly a tradeoff — information is intentionally discarded to achieve compression. No falsification protocol. No deontic focus. The information plane compression claim was partially falsified (activation-function dependent, not causal for generalization).

**Relationship to CT:** Complement, not competitor. IB provides the information-theoretic background for thinking about compression and meaning. CT's conservation law is a different claim: not "find the optimal compression-prediction tradeoff" but "under governed transformation, deontic content is conserved." IB says "compress optimally"; CT says "if you govern the compression, the commitment survives."

**Key citation:** Tishby, N., Pereira, F.C., & Bialek, W. (2000). "The information bottleneck method." arXiv:physics/0004057.

---

### 4. Brandom — Deontic Scorekeeping

**This is the closest competitor in deontic content focus.**

| Criterion | Status |
|-----------|--------|
| Conservation claim | NO — commitments are actively altered through speech acts |
| Empirical validation | NO — philosophical/conceptual only |
| Falsification protocol | NO — hermeneutic, not hypothetico-deductive |
| Public harness | NO |
| Deontic content | YES — core concept (commitments and entitlements) |
| Published where | Harvard University Press (Making It Explicit, 1994), Oxford (Between Saying and Doing, 2008) |

**What they have:** A philosophical framework where discursive practice is a social game of "giving and asking for reasons," and participants track deontic statuses (commitments and entitlements). The framework is explicitly about commitments — the same concept CT measures. Brandom's "conservativeness requirement" for logical vocabulary (following Dummett) says that introducing logical vocabulary should not license new material inferences involving only old vocabulary.

**What they don't have:** No conservation claim (commitments are actively altered — that's the point of the scorekeeping model). No empirical validation. No falsification protocol. No connection to physics or conservation laws. No public harness.

**Relationship to CT:** Foundation, not competitor. Brandom provides the philosophical vocabulary for deontic content (commitments, entitlements, normative statuses). CT takes that vocabulary and makes it empirical and computational. Brandom says "commitments exist and are tracked"; CT says "commitments are conserved under governed transformation, and here's the measurement." The recent work connecting Brandom to LLMs (Barth 2025, "Do LLMs Advocate for Inferentialism?" 2024, "LLMs and the Logical Space of Reasons" 2025) suggests the field is moving toward exactly the kind of empirical deontic analysis CT already does.

**Key citation:** Brandom, R.B. (1994). Making It Explicit: Reasoning, Representing, and Discursive Commitment. Harvard University Press.

---

### 5. Floridi — Philosophy of Information

**Not a competitor — different domain entirely.**

| Criterion | Status |
|-----------|--------|
| Conservation claim | NO — only ethical "conservation" (respect for information) |
| Empirical validation | NO — purely conceptual |
| Falsification protocol | NO — philosophical analysis |
| Public harness | NO |
| Deontic content | NO — general semantic information |
| Published where | Minds and Machines, Synthese, Erkenntnis |

**What he has:** A theory of semantic information as "well-formed, meaningful, and truthful data" (the veridicality thesis). The Method of Levels of Abstraction. Informational Structural Realism. Currently at Yale (Digital Ethics Center), focused on AI ethics.

**What he doesn't have:** No conservation claim. No empirical validation. No falsification protocol. Explicitly rejects "digital physics" and "it from bit." No connection between semantic information and physical conservation laws.

**Relationship to CT:** None directly. Floridi's work is philosophical and conceptual. CT is empirical and computational. If anything, Floridi's rejection of digital physics means he would likely be skeptical of CT's framing — but his Levels of Abstraction method could be used to clarify CT's claims (CT operates at a different LoA than physics, and that's fine).

**Key citation:** Floridi, L. (2004). "Outline of a Theory of Strongly Semantic Information." Minds and Machines, 14(2), 197-221.

---

## The Marginal Candidates

### 6. Determiner Conservativity (Barwise & Cooper 1981)

**Well-established conservation in formal semantics — but a different domain.**

This is the strongest established conservation result in linguistics: all natural-language determiner meanings are conservative (D(A,B) ↔ D(A,A∩B)). It has cross-linguistic evidence, a well-defined logical condition, and counterexamples have been sought. But it's about quantifier semantics, not deontic content. It's a conservation universal in formal semantics, not a conservation law in the physics sense.

**Relationship to CT:** Precedent. If determiner conservativity is a conservation universal in formal semantics, CT's commitment conservation is a conservation law in computational semantics. The existence of determiner conservativity shows that conservation principles in language are not unprecedented — they're established in one domain and CT is extending them to another.

**Key citation:** Barwise, J. & Cooper, R. (1981). "Generalized Quantifiers and Natural Language." Linguistics and Philosophy, 4(2), 159-219.

### 7. Semantic Thermodynamics / Semantodynamics (various Zenodo preprints)

**Claims conservation but lacks rigor.**

Multiple Zenodo preprints claim "Three Laws of Semantic Thermodynamics," "Coherence Conservation," "Semantic Noether Principle," etc. Some claim empirical validation (44-67% degradation on commercial LLMs). But:
- No explicit falsification protocols
- No public harnesses
- Unclear methodology
- Not peer-reviewed
- Not focused on deontic content

**Relationship to CT:** These are parallel attempts at the same idea (physics-informed semantics) but without the rigor. CT has the controlled experiments, the falsification protocol, and the public harness that these works lack. If any of these authors pursue peer review, CT's work would be the benchmark they need to cite and surpass.

### 8. Atkey — Parametricity to Conservation Laws via Noether's Theorem (POPL 2014)

**Conservation laws from type theory — but programming languages, not natural language.**

Derives conservation laws from parametricity in type theory using Noether's theorem. Mathematically sophisticated. But about programming languages, not natural language semantics. No empirical validation. No deontic content.

**Relationship to CT:** Methodological precedent. If Noether's theorem can derive conservation laws in type theory, it can potentially do so in language. CT's lack of a Lagrangian (the weakest point in the stress test) is the gap that Atkey's approach might eventually fill — but for natural language, not programming languages.

**Key citation:** Atkey, R. (2014). "From Parametricity to Conservation Laws, via Noether's Theorem." POPL 2014.

---

## The Competition Matrix

| Candidate | Conservation? | Empirical? | Falsifiable? | Public harness? | Deontic? | Physics-grade? |
|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| **CT (McHenry)** | **YES** | **YES** | **YES** | **YES** | **YES** | **Partial** (no Lagrangian) |
| Marcolli/Chomsky | YES (syntactic) | NO | NO | NO | NO | YES (Hopf algebra) |
| Kuhn/Farquhar | NO | YES | NO | YES | NO | NO |
| Tishby/IB | NO (tradeoff) | YES | NO | YES | NO | Partial |
| Brandom | NO | NO | NO | NO | YES | NO |
| Floridi | NO | NO | NO | NO | NO | NO |
| Determiner Conservativity | YES | YES | YES | YES | NO | NO |
| Semantic Thermodynamics | YES | Claimed | Unclear | NO | NO | NO |
| Atkey | YES | NO | NO | NO | NO | YES |

**CT is the only entry with YES in all five substantive columns.** The only gap is "Physics-grade" (no Lagrangian / no Noether symmetry) — and that's the CAP-001 gap already identified in the stress test.

---

## What This Means for CT

### The field is converging on CT's territory from multiple directions

1. **From mathematics (Marcolli):** Conserved quantities in syntax, Hopf algebra formalism, physics-grade machinery. Missing: empirical validation, semantic focus, falsification protocol.

2. **From NLP (Kuhn/Farquhar):** NLI bidirectional entailment as semantic equivalence, public code, Nature publication. Missing: conservation claim, deontic focus, falsification protocol.

3. **From philosophy (Brandom):** Deontic content as core concept, commitments and entitlements. Missing: empirical validation, conservation claim, computational implementation.

4. **From information theory (Tishby):** Compression-prediction tradeoff, semantic efficiency in language. Missing: conservation claim, deontic focus, falsification protocol.

5. **From formal semantics (Barwise & Cooper):** Conservation universals in language. Missing: physics framing, deontic content, computational harness.

**CT sits at the intersection of all five.** It has the deontic content (from Brandom), the NLI methodology (from Kuhn/Farquhar), the information-theoretic framing (from Tishby), the conservation universal precedent (from Barwise & Cooper), and the physics-grade mathematical machinery is the one thing it's missing (from Marcolli).

### The window is open but closing

The Marcolli/Chomsky/Berwick work (MIT Press 2025) is the most serious threat. If they add empirical validation and extend σ̂ to semantics, they would have a physics-grade conservation law in language with mathematical rigor. They have the physics pedigree, the Chomsky name, the MIT Press venue, and the mathematical machinery. What they don't have is the empirical work — and that's CT's advantage.

The Kuhn/Farquhar Nature 2024 paper shows that NLI bidirectional entailment is publishable in top venues. If they pivot from uncertainty measurement to conservation, they would have the methodology, the code, and the venue. What they don't have is the conservation claim and the deontic focus.

**The priority is clear:** CT needs to fix the paper metric mismatch, run EXP-008, and get the work into a peer-reviewed venue before one of these groups extends their work into CT's territory. The mathematical physics approach (Marcolli) and the NLI methodology (Kuhn/Farquhar) are both one step away from CT's specific claim.

### What to do about each

1. **Marcolli:** Cite as the mathematical physics foundation. Position CT as the empirical complement to her syntactic conservation. The synthesis (syntactic σ̂ + semantic C(S)) is a future paper — possibly a collaboration.

2. **Kuhn/Farquhar:** Cite as the methodological validation of NLI bidirectional entailment. Their 92.7% accuracy number supports CT's choice of the same method. Position CT as extending their method from uncertainty measurement to conservation measurement.

3. **Brandom:** Cite as the philosophical foundation. Position CT as the empirical/computational realization of his deontic scorekeeping framework.

4. **Tishby/IB:** Cite as the information-theoretic background. Position CT as the conservation counterpart to IB's tradeoff — IB says "compress optimally," CT says "govern the compression and the commitment survives."

5. **Determiner Conservativity:** Cite as the precedent for conservation universals in language. Position CT as extending conservation from quantifier semantics to deontic semantics.

6. **Floridi:** Cite sparingly, if at all. His work is too far from CT's to be directly relevant, and his rejection of digital physics suggests he would not be sympathetic.

7. **Semantic Thermodynamics preprints:** Acknowledge as parallel attempts. CT's rigor (controlled experiments, falsification protocol, public harness) is the differentiator.

8. **Atkey:** Cite as the methodological precedent for Noether's theorem in non-physics domains. The Lagrangian gap (CAP-001) is the place where Atkey's approach might eventually help.

---

## The People to Contact

Based on the competition analysis, the people who would be most interested in CT are:

1. **Matilde Marcolli (Caltech)** — Has the physics machinery and the syntactic conservation. Would be interested in the empirical semantic conservation complement. Highest priority — a collaboration could close the Lagrangian gap.

2. **Sebastian Farquhar (Oxford OATML)** — Has the NLI methodology and the Nature publication. Would be interested in the conservation application of bidirectional entailment. Could provide methodological validation and potentially collaborate on a follow-up.

3. **Robert Brandom (Pittsburgh)** — Has the philosophical framework for deontic content. Would be interested in the empirical/computational realization. Probably not a collaborator (different field) but a potential endorser.

4. **Noga Zaslavsky (Max Planck Institute / formerly Tishby's student)** — Has the IB application to semantics. Would be interested in the conservation counterpart to IB's tradeoff. Could provide the information-theoretic perspective.

5. **Noam Chomsky (Arizona/MIT)** — Co-author with Marcolli. If Marcolli is interested, Chomsky's endorsement would be significant. But Chomsky is famously skeptical of statistical/AI approaches to language, so this is a long shot.

---

*This document is the competition analysis for the CT stress test. It should be read alongside `CT_ANSWERS_FINAL.md` (the corrected answers) and `FIX_IMMEDIATELY.md` (the fix plan). The competition analysis confirms that CT's specific claim is novel — no one else has all four criteria — but the field is converging from multiple directions and the window is closing.*
