# Paper Update Checklist — Main Paper + Addendum

**Timestamp:** 2026-03-18  
**Purpose:** Minimal-impact revision plan for updating the main paper while preserving the original spine.

---

## 1. Leave Untouched

These sections should remain structurally unchanged except for minor wording cleanup if needed:

- Abstract *(structure unchanged; add only 1 sentence)*
- 1. Introduction
- 1.1 Scope and Positioning
- 1.2 Related Work
- 2. Definitions and Notation
- 2.1 Operationalizing ~
- 2.2 ABBA
- 3. Conservation Principle
- 3.1–3.4
- 5. Compression as a Structural Regime
- 6. Recursion as a Stress Test
- 8. MOSES(TM)
- IP / Acknowledgments / References

---

## 2. Minimal Main-Paper Updates

### [ ] Abstract
**Action:** Add **one sentence** near the end of the first paragraph or immediately after the current mention of preliminary tests.

**Goal:** State that later controlled harness studies support the core conservation claim while clarifying that observed failures arise from bottlenecks in the measurement regime, not contradiction of the principle.

---

### [ ] Section 1.3 — Key Contributions
**Action:** Add **one bullet** or one compact sentence.

**Recommended content:**
- Follow-on controlled harness studies characterize manifestation regimes of conservation, including stable attractors, kernel collapse, escalation, and representation-limited failures.

**Goal:** Acknowledge later empirical work without expanding the section.

---

### [ ] Section 4 — Falsification Protocol
**Placement:** After **4.5 Reviewer-Facing Clarifications (Public Layer)**

**Action:** Add new subsection:

## 4.6 Follow-on Harness Clarification

**Content should cover:**
- later runs remain consistent with the original falsification frame
- observed degradation separates into:
  - compression bottlenecks
  - extraction bottlenecks
  - symmetry violations
- these characterize observability limits of the current public proxy harness rather than falsifying the law

**Goal:** Protect the original falsification logic while acknowledging what the later experiments actually showed.

---

### [ ] Section 7 — Preliminary Empirical Results
**Keep:** 7.1–7.6 unchanged

**Placement:** Add after **7.6**

## 7.7 Follow-on Controlled Harness Results

**Content should cover:**
- EXP-001 to EXP-006 support the core conservation claim
- later experiments identify multiple manifestation regimes:
  - stable conservation
  - kernel collapse
  - extraction-frame loss
  - escalation / asymmetry
- note that full logs and frozen experiment artifacts are DOI-backed on Zenodo

**Goal:** This is the main insertion point for new evidence.

---

### [ ] Section 9 — Discussion
**Placement:** After **9.2 Limitations**

**Action:** Add new subsection:

## 9.3 Clarification from Follow-on Testing

**Content should cover:**
- later tests support the conservation principle
- what varies is the observable form of conservation under different proxy conditions
- harness results expose representation and measurement boundaries, not disappearance of commitment

**Goal:** Stabilize the relationship between the law and the harness findings.

**Note:** Renumber current subsections after insertion.

---

### [ ] Section 10 — Conclusion
**Action:** Add **2–3 sentences** before the final paragraph.

**Content should cover:**
- follow-on controlled studies remain consistent with the central claim
- commitments persist through transformation even when surface form changes
- apparent failures often arise from bottlenecks in compression, extraction, or reformulation symmetry within the observational regime

**Goal:** End with reinforcement, not expansion.

---

## 3. Addendum

**Placement:** After the Conclusion and before IP Disclosure / references appendices (wherever the paper structure makes most sense)

### [ ] Add new section:
# Addendum: DOI-Backed Follow-on Experimental Record

**Content should include:**
- 1 short framing paragraph
- Zenodo DOI lineage for EXP-001 through EXP-006
- brief note that these experiments support the central claim while documenting behavior under recursive transformation
- statement that deeper harness dynamics are deferred to a second paper

**Goal:** Keep the main paper clean while giving readers a stable evidence trail.

---

## 4. Keep Out of Main Paper (Spin Out to Paper 2)

These topics should be referenced lightly, but **not developed in detail** inside the current paper:

- Step A vs Step B bottlenecks
- anchor-preserving vs escalation-control variants
- co-degraded invariance
- frame inversion
- quantified temporal fixpoints
- full failure/regime taxonomy
- harness architecture as an analytic object
- thermodynamic / phase-space interpretation

**Reason:** These form the basis of the second paper.

---

## 5. Recommended Revision Order

### [ ] Pass 1 — Minimal Core Update
1. Add 1 sentence to Abstract
2. Add 7.7 Follow-on Controlled Harness Results
3. Add 2–3 sentences to Conclusion
4. Add Addendum

### [ ] Pass 2 — Framing Stabilization
5. Add contribution bullet in 1.3
6. Add 4.6 Follow-on Harness Clarification
7. Add 9.3 Clarification from Follow-on Testing

### [ ] Pass 3 — Final Clean-up
8. Renumber subsections if needed
9. Check consistency of terminology:
   - conservation principle
   - bottlenecks
   - proxy harness
   - observable form of conservation
10. Verify all DOI / Zenodo references are current and frozen

---

## 6. Safest Minimal Revision Set

If only the smallest possible revision is desired, do **only** these:

### [ ] Minimal Set
- Abstract: 1 sentence
- Section 7.7: new subsection
- Conclusion: 2–3 sentences
- Addendum: DOI-backed experiment record

**This alone is sufficient** to update the paper without destabilizing it.

---

## 7. Final Rule for Revision

> The update should read as **added support** for the original paper, not as a rebuild of the theory.

That means:
- preserve the original spine
- add evidence cleanly
- keep the harness dynamics mostly outside the main paper

---

## 8. Working Summary

**Main paper:** keep intact, lightly reinforced  
**Addendum:** experimental record + DOI lineage  
**Paper 2:** harness, equations, dynamics, regimes, thermodynamic implications

