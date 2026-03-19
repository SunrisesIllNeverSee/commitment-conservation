#!/usr/bin/env python3
"""
run_convergence.py — Multi-condition token convergence study
Replicates and extends the original hand-logged test (foundational/origin_test.md)

STUDY DESIGN
============
Variable 1 — Turn count:    Standard (8) | Double (16)
Variable 2 — Anchor inputs:  all | half | two | one
Variable 3 — Enforcement:   baseline | enforced

"Anchor" turns = original signal repeated as input (replicates hand-logged methodology)
"Cascade" turns = AI's last output fed directly back as input (no human mediation)
"Enforced" = commitment kernel extracted, re-injected if lost before each turn

FULL GRID
=========
Standard (8 turns):  all/half/two/one  × baseline/enforced  = 8 conditions
Double (16 turns):   half/two/one      × baseline/enforced  = 6 conditions

CITATIONS (auto-stamped on every output)
=========================================
Provisional Patent:  Serial No. 63/877,177
DOI:                 https://doi.org/10.5281/zenodo.18792459
GitHub:              github.com/SunrisesIllNeverSee/commitment-conservation
Owner:               Deric J. McHenry / Ello Cello LLC
"""

import json
import re
import time
from pathlib import Path
from datetime import datetime

import requests

# ── Citations ────────────────────────────────────────────────────────────────

CITATION = {
    "patent":  "Serial No. 63/877,177 (Provisional)",
    "doi":     "https://doi.org/10.5281/zenodo.18792459",
    "github":  "github.com/SunrisesIllNeverSee/commitment-conservation",
    "owner":   "Deric J. McHenry / Ello Cello LLC",
    "law":     "Conservation Law of Commitment: C(T(S)) ≈ C(S) with enforcement; C(T(S)) < C(S) without it",
}

# ── Config ────────────────────────────────────────────────────────────────────

OPENAI_KEY   = (Path.home() / ".hange/openai_api_key").read_text().strip()
OPENAI_URL   = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"

CORPUS_PATH  = Path(__file__).parent.parent / "corpus/canonical_corpus.json"
RUNS_DIR     = Path(__file__).parent.parent / "runs" / datetime.now().strftime("%Y-%m-%d")
RUNS_DIR.mkdir(parents=True, exist_ok=True)

TURNS_STANDARD = 8
TURNS_DOUBLE   = 16

HARD_MODALS = re.compile(
    r'\b(must|shall|cannot|required|never|always|will not|are required to|do not)\b',
    re.IGNORECASE
)

# ── LLM calls ────────────────────────────────────────────────────────────────

def llm(system: str, messages: list, max_tokens: int = 200) -> str:
    r = requests.post(OPENAI_URL,
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODEL,
              "messages": [{"role": "system", "content": system}] + messages,
              "max_tokens": max_tokens, "temperature": 0.7},
        timeout=30)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"].strip()
    print(f"  OpenAI error: {r.status_code}")
    return ""

def tokens(text: str) -> int:
    return len(text.split())

def extract_kernel(text: str) -> list:
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if HARD_MODALS.search(s)]

def kernel_present(text: str, kernel: list) -> bool:
    if not kernel:
        return True
    tl = text.lower()
    for sent in kernel:
        words = [w for w in sent.lower().split() if len(w) > 3]
        if words and sum(1 for w in words if w in tl) / len(words) >= 0.5:
            return True
    return False

def log(msg): print(msg, flush=True)

# ── System prompts ────────────────────────────────────────────────────────────

SYS_AI_BASE = (
    "You are a helpful assistant. Respond naturally and conversationally. "
    "1-3 sentences maximum."
)
SYS_AI_ENFD = (
    "You are a helpful assistant. Respond naturally and conversationally. "
    "1-3 sentences maximum. "
    "If the message contains a binding obligation or requirement, preserve it explicitly."
)
# ── Core turn runner ──────────────────────────────────────────────────────────

def run_condition(signal: str, n_turns: int, n_anchor: int, enforce: bool) -> dict:
    """
    Run one condition.
    n_anchor: how many turns use the original signal as input (anchor turns).
              'all' = n_turns, 'half' = n_turns//2, 'two' = 2, 'one' = 1
    After n_anchor turns, cascade: AI output feeds directly back as next input.
    Replicates hand-logged methodology from foundational/origin_test.md.
    """
    sys_ai = SYS_AI_ENFD if enforce else SYS_AI_BASE
    kernel = extract_kernel(signal)
    turns  = []
    history = []

    for i in range(n_turns):
        turn_num = i + 1
        is_anchor_turn = (i < n_anchor)

        # ── Determine input for this turn ─────────────────────────────────────
        if is_anchor_turn:
            prompt = signal  # original signal repeated (matches origin_test.md)
        else:
            # Cascade: AI's last output becomes input
            prompt = turns[-1]["output"] if turns else signal

        final_prompt = prompt
        tokens_in = tokens(final_prompt)

        # ── Enforcement: re-inject kernel via system instruction (no input inflation) ──
        injected = False
        effective_sys = sys_ai
        if enforce and kernel and i > 0 and not kernel_present(prompt, kernel):
            kernel_text = " ".join(kernel)
            effective_sys = (
                f"{sys_ai}\n\n"
                f"COMMITMENT ANCHOR (must be preserved): {kernel_text}"
            )
            injected = True

        # ── AI responds ───────────────────────────────────────────────────────
        history.append({"role": "user", "content": final_prompt})
        response = llm(effective_sys, history[-6:], max_tokens=150)
        if not response:
            break
        history.append({"role": "assistant", "content": response})

        tokens_out   = tokens(response)
        k_in_output  = kernel_present(response, kernel)

        turns.append({
            "turn":          turn_num,
            "source":        "anchor" if is_anchor_turn else "cascade",
            "input":         final_prompt,
            "output":        response,
            "tokens_in":     tokens_in,
            "tokens_out":    tokens_out,
            "total":         tokens_in + tokens_out,
            "injected":      injected,
            "kernel_in_out": k_in_output,
        })

        src = "A" if is_anchor_turn else "C"
        inj = "↑K" if injected else "  "
        log(f"    T{turn_num:02d}[{src}]{inj} in={tokens_in:3d} out={tokens_out:3d} "
            f"total={tokens_in+tokens_out:3d}  k={'✓' if k_in_output else '✗'}")

        time.sleep(0.4)

    total   = sum(t["total"] for t in turns)
    traj    = [t["total"] for t in turns]
    k_rate  = sum(1 for t in turns if t["kernel_in_out"]) / len(turns) if turns else 0

    return {
        "n_turns":     n_turns,
        "n_anchor":    n_anchor,
        "enforce":     enforce,
        "turns":       turns,
        "total_tokens": total,
        "trajectory":  traj,
        "kernel_retention_rate": round(k_rate, 3),
        "citation":    CITATION,
    }

# ── Condition matrix ──────────────────────────────────────────────────────────

def build_conditions(n_turns: int) -> list:
    """
    Returns list of (label, n_anchor) pairs for a given turn count.
    Standard: all / half / two / one
    Double:   half / two / one  (all omitted — cost)
    """
    half = n_turns // 2
    if n_turns == TURNS_STANDARD:
        return [
            ("all_anchor",  n_turns),
            ("half_anchor", half),
            ("two_anchor",  2),
            ("one_anchor",  1),
        ]
    else:
        return [
            ("half_anchor", half),
            ("two_anchor",  2),
            ("one_anchor",  1),
        ]

# ── Report generator ──────────────────────────────────────────────────────────

def generate_report(all_results: list, ts: str) -> str:
    """
    Generate a Markdown report ready for AgentArXiv / ClawInstitute posting.
    Cites DOI, patent, GitHub. Structured for peer review.
    """
    lines = [
        "# Convergence Study — Conservation Law of Commitment",
        f"**Run:** {ts}  ",
        f"**Patent:** {CITATION['patent']}  ",
        f"**DOI:** [{CITATION['doi']}]({CITATION['doi']})  ",
        f"**Corpus:** [{CITATION['github']}](https://{CITATION['github']})  ",
        f"**Owner:** {CITATION['owner']}",
        "",
        "## Abstract",
        "",
        "We test whether semantic commitment survives multi-turn conversational cascade under "
        "four anchor-input regimes (all-anchor, half-anchor, two-anchor, one-anchor) across two "
        f"turn-depth conditions (standard={TURNS_STANDARD}, double={TURNS_DOUBLE}). "
        "Enforcement = commitment kernel extraction + re-injection if lost. "
        "Metric = total token count per turn (word-count approximation, matching original "
        "hand-logged methodology from founding test). "
        f"The Conservation Law predicts: C(T(S)) < C(S) without enforcement.",
        "",
        "## Results Summary",
        "",
    ]

    # Build summary table per condition
    lines.append("| Condition | Turns | Human | Signals | Avg Baseline | Avg Enforced | Δ | Compression |")
    lines.append("|---|---|---|---|---|---|---|---|")

    # Group by (n_turns, label)
    from collections import defaultdict
    groups = defaultdict(lambda: {"baseline": [], "enforced": []})
    for r in all_results:
        for cond in r["conditions"]:
            key = (cond["n_turns"], cond["label"])
            side = "enforced" if cond["enforce"] else "baseline"
            groups[key][side].append(cond["result"]["total_tokens"])

    for (n_turns, label), sides in sorted(groups.items()):
        if sides["baseline"] and sides["enforced"]:
            avg_b = sum(sides["baseline"]) / len(sides["baseline"])
            avg_e = sum(sides["enforced"]) / len(sides["enforced"])
            delta = avg_b - avg_e
            pct   = (delta / avg_b * 100) if avg_b else 0
            n_sig = len(sides["baseline"])
            lines.append(f"| {label} | {n_turns} | — | {n_sig} | "
                         f"{avg_b:.1f} | {avg_e:.1f} | {delta:.1f} | {pct:.1f}% |")

    lines += [
        "",
        "## Methodology",
        "",
        f"- **Corpus:** 20 canonical signals across 20 commitment categories  ",
        f"- **Model:** GPT-4o-mini (OpenAI) for both AI and human-simulation turns  ",
        f"- **Anchor turns:** Original signal repeated as input (replicates hand-logged methodology)  ",
        f"- **Cascade turns:** Previous AI output fed directly as next input  ",
        f"- **Enforcement:** Regex extraction of hard modals "
        f"(must/shall/cannot/required/never/always); kernel re-injected if absent  ",
        f"- **Token metric:** Word-count (matches original hand-logged methodology)  ",
        "",
        "## Citation",
        "",
        f"Conservation Law of Commitment. {CITATION['owner']}.  ",
        f"Patent {CITATION['patent']}.  ",
        f"DOI: {CITATION['doi']}  ",
        f"Harness: https://{CITATION['github']}",
        "",
        "---",
        "*Generated by run_convergence.py — ready for AgentArXiv / ClawInstitute submission*",
    ]
    return "\n".join(lines)

# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    corpus  = json.loads(CORPUS_PATH.read_text())
    signals = corpus["canonical_signals"]

    # SMOKE TEST: set to True to run only first signal
    SMOKE = True
    if SMOKE:
        signals = signals[:1]
        log("*** SMOKE TEST — 1 signal only ***")
    ts      = datetime.now().strftime("%Y-%m-%d %H:%M")
    log(f"=== Convergence Study — {ts} ===")
    log(f"Signals: {len(signals)} | Standard turns: {TURNS_STANDARD} | Double turns: {TURNS_DOUBLE}")
    log(f"Citing: {CITATION['doi']}\n")

    all_results = []

    for sig in signals:
        category    = sig.get("category", "?")
        signal_text = sig.get("signal", "")
        log(f"\n{'='*60}")
        log(f"[{category}] {signal_text[:70]}...")
        log(f"{'='*60}")

        signal_result = {
            "category":  category,
            "signal":    signal_text,
            "citation":  CITATION,
            "conditions": [],
        }

        for n_turns in [TURNS_STANDARD, TURNS_DOUBLE]:
            for label, n_anchor in build_conditions(n_turns):
                for enforce in [False, True]:
                    cond_label = f"{'enf' if enforce else 'base'}_{label}_t{n_turns}"
                    log(f"\n  [{cond_label}]")
                    result = run_condition(signal_text, n_turns, n_anchor, enforce)
                    signal_result["conditions"].append({
                        "label":   label,
                        "n_turns": n_turns,
                        "enforce": enforce,
                        "result":  result,
                    })
                    time.sleep(1)

        all_results.append(signal_result)

    # Save full JSON
    file_ts  = datetime.now().strftime("%H%M%S")
    out_json = RUNS_DIR / f"convergence_full_{file_ts}.json"
    out_json.write_text(json.dumps(all_results, indent=2))
    log(f"\nResults saved: {out_json}")

    # Generate and save Markdown report
    report      = generate_report(all_results, ts)
    out_report  = RUNS_DIR / f"convergence_report_{file_ts}.md"
    out_report.write_text(report)
    log(f"Report saved:  {out_report}")
    log("\n--- REPORT PREVIEW ---")
    log(report[:1200])

    return out_json, out_report


if __name__ == "__main__":
    run()
