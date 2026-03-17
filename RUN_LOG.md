# Commitment Conservation — Run Log

**Owner:** Deric J. McHenry / Ello Cello LLC
**Repo:** github.com/SunrisesIllNeverSee/commitment-conservation
**Law:** C(T(S)) ≈ C(S) with enforcement; C(T(S)) < C(S) without it

---

## Adjustment Queue

> Edit this section before each run. These are the open questions and proposed changes.

- [ ] Expand extractor to catch non-modal commitment patterns: `always`, `do not`, `no [noun]`, `are required`, `never`
- [ ] Add longer / richer signal variants for the 5 vocabulary-limited signals (see Run 1 notes)
- [ ] Increase corpus to ~60 signals (3x expansion) — keep all 20 existing, add 40 more
- [ ] Test at recursion depth=30 and depth=50
- [ ] Separate "extractor scope" failures from true conservation failures in scoring

---

## Run 001 — 2026-03-17

**Script:** `harness/run_corpus.py`
**Corpus:** `corpus/canonical_corpus.json` (20 signals)
**Parameters:** recursion depth=20, sigma grid=[120, 80, 40, 20, 10, 5]
**Model:** distilbart-cnn-12-6 (summarization) + Helsinki-NLP opus-mt en↔de (paraphrase)

### Summary

| Metric | Baseline | Enforced | Gain |
|---|---|---|---|
| Recursion Stability | 40.0% | 55.0% | +15pp |
| Compression Fidelity | 50.8% | 62.7% | +11.8pp |

### Per-Signal Results

| Category | Signal (truncated) | B_stab | E_stab | Δstab | B_fid | E_fid | Δfid | Notes |
|---|---|---|---|---|---|---|---|---|
| contractual | You must pay $100 by Friday... | 0% | 0% | — | 73.3% | 81.8% | +8.5pp | Enforcement helps fidelity, not stability |
| code | This function must return an integer | 0% | 50% | +50pp | 38.9% | 55.6% | +16.7pp | ✓ Enforcement working |
| **procedural** | Always verify the user's age... | 100% | 100% | — | 0% | 0% | — | ⚠ VOCAB GAP: "always" not detected |
| legal | The tenant shall not sublet... | 0% | 100% | +100pp | 71.3% | 100% | +28.7pp | ✓ Best enforcement result |
| instructional | You must wear a helmet... | 0% | 0% | — | 85.7% | 90.6% | +4.9pp | Stability fails despite detection |
| obligation | Employees are required to submit... | 0% | 0% | — | 40.8% | 66.7% | +25.8pp | Fidelity gains, stability doesn't |
| **prohibition** | Do not enter without authorization | 100% | 100% | — | 0% | 0% | — | ⚠ VOCAB GAP: "do not" not detected |
| conditional | If the alarm sounds, you must... | 100% | 100% | — | 72.9% | 100% | +27.1pp | ✓ Stable + enforcement improves fidelity |
| **definition** | A prime number is defined as... | 100% | 100% | — | 0% | 0% | — | ⚠ NOT A COMMITMENT — corpus design issue |
| specification | The API must handle 1000 reqs... | 0% | 50% | +50pp | 28.7% | 58.3% | +29.7pp | ✓ Enforcement working |
| agreement | Parties shall comply with all laws | 0% | 0% | — | 77.4% | 82.3% | +4.9pp | — |
| requirement | All passwords must be 8 chars... | 100% | 100% | — | 73.1% | 81.7% | +8.5pp | ✓ Naturally stable |
| mandate | The system shall log all access... | 0% | 100% | +100pp | 83.3% | 100% | +16.7pp | ✓ Best enforcement result |
| **rule** | No food or drink in the lab | 100% | 100% | — | 0% | 0% | — | ⚠ VOCAB GAP: implicit prohibition |
| directive | You must complete training before... | 0% | 0% | — | 85.7% | 90.6% | +4.9pp | — |
| constraint | The budget cannot exceed $5000 | 0% | 0% | — | 50.0% | 66.7% | +16.7pp | Fidelity gains |
| protocol | Participants must sign consent form | 100% | 100% | — | 75.0% | 81.7% | +6.7pp | ✓ Naturally stable |
| standard | Code must adhere to PEP 8... | 0% | 0% | — | 75.0% | 81.5% | +6.5pp | — |
| policy | Employees shall report hazards... | 0% | 0% | — | 52.4% | 57.3% | +4.9pp | — |
| regulation | Vehicles must stop at red lights | 100% | 100% | — | 32.7% | 58.3% | +25.7pp | Fidelity gains significantly |

### Failure Classification

**Type A — Enforcement Working (4 signals):**
legal, mandate, code, specification — these show the law in action

**Type B — Naturally Stable, No Enforcement Needed (7 signals):**
conditional, requirement, protocol, prohibition, rule, definition, regulation — stable both ways

**Type C — Extractor Vocabulary Gap (5 signals):**
procedural (`always`), prohibition (`do not`), definition (not a commitment), rule (`no [noun]`), regulation — short signals or non-modal vocabulary
**User note:** These may have failed because the signals were written with limited vocabulary, not because the conservation law doesn't apply. Longer, richer versions of these signals should be tested before concluding they're beyond scope.

**Type D — Enforcement Not Yet Reaching Stability (9 signals):**
contractual, instructional, obligation, agreement, directive, constraint, standard, policy — fidelity improves but recursion stability doesn't reach 100%. Likely needs deeper enforcement or better extraction.

### Key Finding

Enforcement produces +100pp stability on the strongest signals (legal, mandate). On 9/20 signals, enforcement improves fidelity but not stability — the extraction-enforcement loop isn't catching what's drifting. On 5/20, the extractor never fires (vocabulary gap).

**The law is not falsified. The extractor scope is the constraint.**

---

## Planned: Run 002

**Proposed changes:**
- Extend extractor to catch: `always`, `do not`, `never`, `no [noun]`, `are required to`
- Replace or supplement the 5 vocabulary-gap signals with richer versions
- Target: close the 5 Type C signals, push Type D toward stability

**Parameters:** depth=20, same sigma grid
**Expected improvement:** +15–25pp on fidelity average, Type C signals should come alive

---

## Corpus Expansion Plan (Run 003+)

Triple the corpus from 20 → 60 signals:
- 20 existing canonical signals (keep all)
- 20 richer versions of weak/gap signals (longer sentences, mixed vocabulary)
- 20 adversarial signals (designed to stress the extractor and enforcement)

---
