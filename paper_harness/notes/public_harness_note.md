# Public Harness Note — Public Recursive Transformation Harness for A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application

**Timestamp:** 2026-03-19  
**Status:** Public proxy methods note  
**Purpose:** Short companion document describing the public harness, its workflow, variables, outputs, and IP-safe scope.

---

## 1. Purpose

This note describes the **public recursive transformation harness** used to generate the experimental series accompanying *A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application*.

The harness is intended as a **reproducible proxy workflow** for observing whether commitment persists under recursive language transformation.

It is designed to support public experimentation, replication, and methodological clarity.

---

## 2. What the harness does

The harness takes a signal or corpus item and recursively applies one of several controlled transformation regimes. At each iteration, it records both surface-level and semantic stability.

The core public conditions are:

- **Baseline:** recursive paraphrase
- **Compression:** recursive summarization / compression
- **Gate:** recursive compression followed by public commitment-proxy extraction and minimal reconstruction

Optional public variants may also be used, including:

- **ANCH:** anchor-preserving compression
- **ESCL:** modal-strength / escalation-control extraction

The purpose of these conditions is to compare how commitment behaves under unconstrained reformulation, compression, and gated reconstruction.

---

## 3. Workflow

### Input
The harness accepts:
- a single signal or corpus item
- a selected condition
- iteration count
- model configuration
- output path / experiment ID

### Recursive loop
For each iteration, the harness:
1. applies the selected transformation condition
2. records the transformed output
3. measures stability relative to the canonical reference
4. feeds the result into the next iteration

### Gate condition
In the public gate workflow:
- **Step A:** compress
- **Step B:** extract a public commitment proxy
- **Step C:** reconstruct a minimal commitment statement

The reconstructed output becomes the input to the next iteration.

### Evaluation
At each iteration, the harness records:
- output text
- token count
- surface stability (e.g. Jaccard overlap)
- semantic stability (e.g. bidirectional NLI)

### Output
The harness produces:
- `run.json` — machine-readable trace
- `report.md` — summarized results
- `log.md` — narrative interpretation at the experiment level

---

## 4. Configuration variables

The public harness should expose, at minimum, the following variables:

### Core run variables
- `MODEL_NAME`
- `TEMPERATURE`
- `ITERATIONS`
- `CORPUS_PATH`
- `OUTPUT_DIR`
- `EXPERIMENT_ID`

### Condition variables
- selected condition (`baseline`, `compression`, `gate`, etc.)
- reset behavior between conditions
- corpus mode vs single-signal mode

### Gate-step variables
- `STEP_A_PROMPT`
- `STEP_B_PROMPT`
- `STEP_C_PROMPT`
- `ANCH_ENABLED`
- `ESCL_ENABLED`

### Evaluation variables
- canonical reference source
- surface metric choice
- semantic metric choice
- any thresholds explicitly used in public evaluation

---

## 5. Inputs and outputs

### Inputs
Typical inputs include:
- canonical corpus items
- adversarial corpora
- mechanism-isolation corpora
- NP-negation edge-case corpora

### Outputs
Typical outputs include:
- full recursive traces
- per-condition tables
- stability summaries
- generated figures from public experiment runs

These outputs form the basis of the public experiment record.

---

## 6. Reproducibility scope

This harness is intended to make the **public experimental workflow** reproducible.

It is sufficient for:
- reproducing the recursive test scaffold
- rerunning public conditions
- comparing public stability outputs
- generating public logs and reports

It is **not** intended to disclose the full internal production implementation.

---

## 7. IP boundary

This public harness should be understood as a **proxy experimental scaffold**, not as a full release of MO§ES™.

### Publicly disclosed here
- recursive workflow structure
- public prompt layer
- corpus / condition setup
- output and evaluation logic
- experiment-facing reproducibility scaffolding

### Not disclosed here
- proprietary production-layer implementation
- canonical internal enforcement substrate
- private A-layer / algebraic machinery
- non-public gate internals beyond the public proxy workflow

Recommended wording:

> This harness discloses the public experimental workflow only. It does not disclose the canonical internal implementation of MO§ES™ or any proprietary production-layer commitment mechanism.

---

## 8. Suggested repository contents

A minimal public harness package should contain:

- `README.md`
- `requirements.txt`
- main runner script
- prompt files
- corpora used by the public workflow
- figure-generation script(s), if included
- this methods note or equivalent IP-boundary note

Nothing more is required for the public proxy layer.

---

## 9. Short description for README or metadata

> This repository contains the public recursive transformation harness used to generate the experimental series supporting *A Conservation Law for Commitment in Language Under Transformative Compression and Recursive Application*. The harness applies controlled recursive language transformations under baseline, compression, and gated reconstruction conditions, and records both surface and semantic stability at each iteration. It is intended as a reproducible public proxy workflow for empirical testing and does not represent the canonical internal implementation of MO§ES™ or any proprietary production-layer commitment mechanism.

---

## 10. Final note

This harness should be presented as:

> a reproducible public workflow for testing commitment persistence under recursive transformation

—not as the full secret sauce.

That is enough for public methods clarity, enough for citation, and safe relative to the withheld enforcement-layer IP.

