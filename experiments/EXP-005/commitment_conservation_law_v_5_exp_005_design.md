# Commitment Conservation Framework (v6)

**Timestamp:** 2026-03-18 (Post EXP-005)

---

# 🧠 Core Insight (Updated)

Commitment stability is governed by **two coupled transformation bottlenecks**:

1. **Compression (Step A)** — what survives
2. **Extraction (Step B)** — what is representable

A signal can survive compression and still fail conservation if the extraction frame cannot encode its structure.

---

# 🧾 Conservation Law of Commitment (v6)

> A commitment is conserved under recursive transformation when its defining constraints survive compression *and* remain representable within the extraction frame without asymmetric transformation.

---

## 🔬 Conditions

### 1. Compression Preservation (3a)
The signal must remain above the compression resolution threshold.

If compressed below this threshold → collapse to minimal kernel.

---

### 2. Extractability (3b)
All obligation-bearing structure must be representable in the extraction schema.

Failure occurs when:
- ordering constraints ("before", "after") are ignored
- conditional dependencies are dropped
- negation structure is not preserved

---

### 3. Anchor Presence
At least one compression-resistant anchor must exist.

Anchors include:
- modal (must, shall, cannot)
- temporal (Friday, 5pm)
- quantitative ($5000, 90 days)
- definitional

---

### 4. Symmetry Preservation
Transformation must not strengthen or weaken obligation.

S ⇄ T(S)

---

# 🔴 Failure Modes (Refined)

## 1. Resolution Collapse (Step A)
Signal compressed below anchor threshold.

## 2. Representation Blindness (Step B)
Structure survives but is not encoded.

**Example:**
"before proceeding" preserved → ignored by extractor

---

## 3. Asymmetric Reformulation
Obligation becomes stronger or weaker.

---

## 4. Frame Inversion (NEW)
Negation / modality flips semantic direction.

Example:
"shall not sublet" → "must obtain consent"

---

## 5. Escalation Bias
Soft → hard obligation ("should" → "must")

---

## 6. Co-Degraded Invariance
Both reference and output degraded → false stability

---

# 🧩 Mechanisms

## Path A — Enforcement (Gate)
- requires anchor
- sensitive to extraction frame
- fails via collapse or asymmetry

## Path B — Definitional Closure
- self-stabilizing
- fails via contradiction

---

# 📊 EXP-005 Findings (Locked)

From experiment log fileciteturn6file0:

### Key Result

**Primary hypothesis FAILED:**
- procedural_keystone remained at NLI=0.50 under ANCH
- ordering constraint survived Step A but was removed in Step B

→ Step B is a primary bottleneck

---

### Secondary Result

**ESCL generalized beyond expectation:**
- legal_qualifier: 0.50 → 1.00
- prevented prohibition → absolute collapse

→ ESCL controls symmetry, not just modal strength

---

### Critical Discovery

> Preservation ≠ Representability

A signal can survive compression but still fail conservation.

---

### Anchor Behavior

- Quantified temporal → perfect fixpoint
- Passive temporal → stable across all conditions

→ Anchors function as compression-stable invariants

---

# 🌌 System Interpretation

The system is not a single law but a **constrained dynamical system** with identifiable regimes.

Invariance emerges only when all constraints align:

- compression threshold maintained
- structure representable
- anchor present
- symmetry preserved

---

# ⚖️ Clarification on “Law” vs “Conditional Law”

This is not a contradiction — it’s a framing issue.

The law is:

> **Commitment is conserved under transformation.**

The conditions define:

> **when the system satisfies the requirements for conservation to manifest.**

Analog:
- energy conservation always holds
- but observed behavior depends on system constraints

---

# 🧠 Final Position (Checkpoint)

You are not discovering a single rule.

You are mapping:

> **the conditions under which invariance becomes observable in language systems**

---

# 🧾 Status

- Mechanisms separated
- Failure modes classified
- Bottlenecks identified
- Ready for extraction-frame expansion (next phase)

