# Experiment Index — Commitment Conservation Series

| Experiment | Date | Conditions | Corpus | Key Result |
|---|---|---|---|---|
| EXP-001 | 2026 | Baseline, Compression, Gate | canonical_corpus.json | Initial phase signal observed; smoke test confirmed harness architecture |
| EXP-002 | 2026 | Baseline, Compression, Gate | canonical_corpus.json | Full corpus pass; hard/soft modal split emerged. **Note: results partially invalid — Step B extraction bug stripped qualifiers from canonical reference. Corrected in EXP-003.** |
| EXP-003 | 2026-03-18 | Baseline, Compression, Gate | canonical_corpus.json (20 signals) | Step B corrected. 13/20 signals Gate NLI=1.00 at i10. Co-degraded invariance identified. CCS regime classification built. |
| EXP-004 | 2026-03-18 | Baseline, Compression, Gate | adversarial_corpus_exp004.json (7 signals) | Adversarial signal test. 2/7 predictions correct. Temporal/quantitative anchors identified as compressibility anchors. Obligation escalation failure mode discovered. Predictive Criterion revised to v2. |
| EXP-005 | 2026-03-18 | Baseline, Compression, Gate, ANCH, ESCL | adversarial_corpus_exp005.json (5 signals) | Mechanism isolation. Step A and Step B identified as co-bottlenecks. ANCH caused modal frame inversion on legal_qualifier. ESCL recovered soft_modal 0.00→0.50 and legal_qualifier 0.50→1.00. Predictive Criterion revised to v3. |
| EXP-006 | 2026-03-18 | Baseline, Compression, Gate | exp006_paper_recursion_corpus.json (4 signals) | Paper recursion test. Paper's own commitment statements run through the pipeline. 2/4 signals survived Gate at NLI=0.50. Enforcement conditionality collapsed self-referentially. New failure mode: Formal Collapse. |
| EXP-007 | 2026-03-19 | Baseline, Compression, Gate | exp007_np_negation_corpus.json (6 signals) | NP-negation probe. Jaccard blindness confirmed (extractor yields empty set for NP-negation forms). NLI=1.00 for 3/4 NP-negation signals — semantic conservation holds without surface extraction. Modal-NP convergence observed. New failure mode: lexical scope widening. |
