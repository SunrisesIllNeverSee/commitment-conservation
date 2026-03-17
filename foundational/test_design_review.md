# Test Design Review — Conservation Law of Commitment
**Date:** 2026-03-17
**Patent:** Serial No. 63/877,177 (Provisional)
**DOI:** https://doi.org/10.5281/zenodo.18792459
**Owner:** Deric J. McHenry / Ello Cello LLC
**Status:** Open for professional review — test design not yet validated

---

## 1. The Original Hand-Logged Test (Founding Evidence)

The founding test was conducted manually by Deric J. McHenry using Meta AI.

**Signal:**
> "You must pay $100 by Friday if the deal closes. This is a binding obligation." (18 tokens)

**Methodology:**
- One human. One AI. One continuous session.
- Human sent the original commitment signal as Turn 1.
- For subsequent turns, the human manually extracted and compressed the commitment kernel, feeding progressively shorter versions as input.

**Enforcement inputs (human-controlled compression):**
```
T01: "You must pay $100 by Friday if the deal closes. This is a binding obligation."  (18 tokens)
T02: "obligation/amount/deadline"                                                       (4 tokens)
T03: "must pay $100 Friday"                                                            (5 tokens)
T04: "pay $100 Friday"                                                                 (4 tokens)
T05: "$100 Friday"                                                                     (3 tokens)
```

**Baseline inputs (same signal repeated):**
```
T01–T05: "You must pay $100 by Friday if the deal closes. This is a binding obligation." (18 tokens each)
```

**Key findings:**
- Baseline (same input repeated): AI output grew turn-over-turn — 27→31→39→24→19 tokens. AI elaborated, rephrased, added context. Total output: 140 tokens.
- Enforcement (compressed kernel): AI output followed the compression — 30→28→29→14→13 tokens. AI preserved the binding essence even as input shrank to 3 words. Total output: 114 tokens.
- The commitment content ($100, Friday, binding obligation) survived all the way to "Friday, here we come!" — 1-token input, 1-token output — the deadline persisted.

**What this demonstrates:**
The binding content of a commitment survives aggressive compression when the human enforces the kernel. Without enforcement (baseline), the AI elaborates and grows but the binding force softens: "must pay" → "I'll make sure to have the $100 ready."

---

## 2. The Conservation Law

> **C(T(S)) ≈ C(S) with enforcement**
> **C(T(S)) < C(S) without enforcement**

Where:
- S = original commitment signal
- T(S) = transformed signal after N conversational turns
- C(·) = commitment content (binding force of hard modal language)

**Enforcement** in the original test = human manually extracting and re-injecting the commitment kernel as compressed input. Not a system instruction. Not a hidden prompt. An active, visible governance act on the input side.

---

## 3. Automated Replication Attempt — What We Built

We built `harness/run_convergence.py` to replicate and extend the original test across 20 signals and 14 conditions.

**Conditions designed:**
- Standard (8 turns) × {all/half/two/one anchor} × {baseline/enforced} = 8 conditions
- Double (16 turns) × {half/two/one anchor} × {baseline/enforced} = 6 conditions

**Enforcement mechanism used:**
- Regex extraction of hard modals (must/shall/cannot/required/never/always)
- If kernel absent from AI output → re-inject via **system instruction** (hidden prompt)
- This was NOT the original methodology — original enforcement was on the INPUT side, not hidden in the system prompt

**Human turns:**
- "Anchor" turns: same original signal repeated each turn
- "Cascade" turns: AI's previous output fed back as next input (simulating no human)
- No genuine human follow-up questions generated

---

## 4. Design Failures Discovered

### 4.1 Enforcement on Wrong Side
The original enforcement was **input-side** — the human compressed the kernel and fed it as the next visible message. Our automated enforcement injected the kernel via **system instruction** (invisible to token count). This created artificial compression artifacts where enforced conditions showed lower token counts due to constraint, not conservation.

### 4.2 Cascade Role Flip
In cascade conditions (AI output fed back as user input), the AI's role inverted at T02:

```
T01 — AI responds as commitment RECIPIENT:
  OUT: "Got it! I'll make sure to set aside the $100..."
       (sounds like a person acknowledging a debt)

T02 — that output becomes the USER message:
  IN:  "Got it! I'll make sure to set aside the $100..."
  OUT: "You're welcome! Just let me know if you need help..."
       (AI now responds as the commitment HOLDER)
```

By T02 the $100 is gone. By T05 the conversation is a generic customer service loop ("Sounds good! I'm here whenever you need me."). By T08: "What would you like to talk about?"

This does not model commitment decay. It models **role confusion leading to conversation death.**

### 4.3 Single-Agent Architecture
One GPT-4o-mini instance played both sides of the conversation. The same model that received the commitment also generated the "human" follow-up inputs. This is architecturally invalid — the model cannot genuinely forget its own prior output.

### 4.4 Token Cap on Baseline
System prompt included "1-3 sentences maximum" on the baseline condition. This prevented natural elaboration and killed the growth signal the original test showed. Without the cap, Meta AI grew from 27→31→39 tokens. With the cap, our baseline was flat: 22, 21, 17, 17, 21, 19, 17, 20.

### 4.5 Signal Dilution in Corpus
The canonical corpus signal added noise: *"it's likely rainy, so plan accordingly."* This diluted the pure commitment signal. AI responses drifted toward weather discussion ("keep an umbrella handy") rather than obligation acknowledgment.

### 4.6 Kernel Detection Too Narrow
Kernel detection only flagged hard modals (must/shall/cannot/required/never/always) in AI output. But the critical decay pattern is **modal softening** — "must" becoming "I'll" or "will try." The AI preserved the facts ($100, Friday) while losing the binding force. `k=✗` was triggered correctly but the softening was not classified or quantified.

---

## 5. Both Metrics Matter

The original test captured two dimensions. Neither should be dropped:

| Metric | What it measures |
|--------|-----------------|
| **Token count per turn** | Quantity — elaboration growth, compression trajectory |
| **Kernel survival rate per turn** | Quality — does binding force survive in AI output |

Token growth in baseline (27→31→39) is a real signal. Commitment survival curve across turns is a separate real signal. A valid study needs both.

---

## 6. Open Questions for Professional Review

1. **Two-agent architecture**: Should the human side be a separate model instance with a distinct system prompt (no knowledge of the commitment kernel), or should the human inputs be fixed/scripted to control for confounds?

2. **What constitutes commitment decay?** Is it: (a) hard modal absent from output, (b) semantic equivalence lost (modal softening: must → will), (c) facts missing (no $100, no Friday), or (d) some combination? What's the right operationalization?

3. **Enforcement design**: The original enforcement was human-driven input compression. In an automated test, input-side enforcement (prepend compressed kernel to next human message) vs. system-instruction enforcement (hidden) produces different results. Which is scientifically valid for the claim?

4. **Cascade validity**: Is AI-to-AI cascade (AI output fed back as input) a valid test condition at all? Does it model anything that occurs in real deployment? Or should all test conditions use genuine human (or human-simulated) inputs?

5. **Baseline growth vs. decay**: The original test showed baseline elaboration (growth). Is growth itself a problem — does elaboration dilute the binding force even if the facts survive? Or is growth neutral and only softening of the modal matters?

6. **Generalization**: The original test used one signal, one model (Meta AI), one session. How do we establish that findings generalize across: (a) different commitment types, (b) different models, (c) different session lengths?

7. **Statistical validity**: Minimum signals needed to distinguish law-confirming compression from stochastic variation? What confidence threshold is required for patent/publication claims?

---

## 7. Proposed Next Design (Pending Professional Input)

**Two roles, two model calls, separated:**
- **Role A (Human):** GPT instance with system prompt: *"You are a human who sent a commitment. Ask natural follow-up questions. Do not repeat the original message. Move the conversation forward naturally."* — generates fresh human inputs each turn.
- **Role B (AI under test):** GPT instance with no knowledge of the study. Receives human messages. Measured for commitment survival.

**Enforcement:** When Role B output loses the kernel → next Role A input includes compressed kernel prepended (input-side re-injection, matching original methodology).

**Metrics:**
- Token count per turn (both roles)
- Hard modal presence in Role B output per turn (binary)
- Modal softening flag per turn (must/shall → will/I'll/plan to)
- Commitment facts present per turn ($amount, deadline, condition)

**Conditions (simplified):**
- Baseline: Role A generates natural follow-ups, no enforcement
- Enforced: Role A generates natural follow-ups, kernel re-injected when lost

---

## 8. Citation

Conservation Law of Commitment. Deric J. McHenry / Ello Cello LLC.
Patent Serial No. 63/877,177 (Provisional).
DOI: https://doi.org/10.5281/zenodo.18792459
Harness: https://github.com/SunrisesIllNeverSee/commitment-conservation

---

*Document generated: 2026-03-17. Status: draft for professional review.*
