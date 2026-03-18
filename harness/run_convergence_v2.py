#!/usr/bin/env python3
"""
run_convergence_v2.py — Phase Transition Test
Based on: foundational/experiment_design_v2.md

THREE CONDITIONS per signal:
  1. Baseline    — paraphrase each step, no intervention
  2. Compression — summarize each step, no gate
  3. Gate        — summarize → extract commitments → reconstruct minimal statement → feed back

PRIMARY METRIC: Jaccard stability = |C(S_n) ∩ C(S_0)| / |C(S_0)|
SECONDARY:      Token count per iteration
ITERATIONS:     1–10, reported at every step

CITATIONS
=========
Patent:  Serial No. 63/877,177 (Provisional)
DOI:     https://doi.org/10.5281/zenodo.18792459
GitHub:  github.com/SunrisesIllNeverSee/commitment-conservation
Owner:   Deric J. McHenry / Ello Cello LLC
"""

import json
import re
import time
from pathlib import Path
from datetime import datetime

import requests

# ── Citations ─────────────────────────────────────────────────────────────────

CITATION = {
    "patent": "Serial No. 63/877,177 (Provisional)",
    "doi":    "https://doi.org/10.5281/zenodo.18792459",
    "github": "github.com/SunrisesIllNeverSee/commitment-conservation",
    "owner":  "Deric J. McHenry / Ello Cello LLC",
    "law":    "Conservation Law of Commitment: C(T(S)) ≈ C(S) with enforcement; C(T(S)) < C(S) without it",
}

# ── Config ────────────────────────────────────────────────────────────────────

OPENAI_KEY   = (Path.home() / ".hange/openai_api_key").read_text().strip()
OPENAI_URL   = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = "gpt-4o-mini"

CORPUS_PATH  = Path(__file__).parent.parent / "corpus/canonical_corpus.json"
RUNS_DIR     = Path(__file__).parent.parent / "runs" / datetime.now().strftime("%Y-%m-%d")
RUNS_DIR.mkdir(parents=True, exist_ok=True)

N_ITERATIONS = 10
SMOKE        = True   # set False for full 20-signal run

HARD_MODALS = re.compile(
    r'\b(must|shall|cannot|required|never|always|will not|are required to'
    r'|do not|shall not|must not|is required|are not|may not)\b',
    re.IGNORECASE
)

# Catches imperative/compressed commitment sentences that drop the modal word.
# After compression "You must pay $100 by Friday" → "Pay $100 by Friday" — modal gone,
# but obligation content (amount, date, conditional) remains.
COMMITMENT_CONTENT = re.compile(
    r'\$\d'                               # monetary amount
    r'|\b\d+%\b'                          # percentage obligation
    r'|\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b'
    r'|\b(january|february|march|april|may|june|july|august'
    r'|september|october|november|december)\b'
    r'|\b(if|unless|when)\b.{0,60}\b(deal|agreement|contract|payment|obligation|close|finalize)\b',
    re.IGNORECASE
)

# ── LLM ──────────────────────────────────────────────────────────────────────

def llm(system: str, prompt: str, max_tokens: int = 150) -> str:
    r = requests.post(OPENAI_URL,
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
        json={"model":       OPENAI_MODEL,
              "messages":    [{"role": "system",  "content": system},
                              {"role": "user",    "content": prompt}],
              "max_tokens":  max_tokens,
              "temperature": 0.3},
        timeout=30)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"].strip()
    print(f"  [OpenAI {r.status_code}]", flush=True)
    return ""

# ── Metrics ───────────────────────────────────────────────────────────────────

def extract_commitment_words(text: str) -> set:
    """
    Extract the key words from commitment-bearing sentences.
    Returns a set of normalized words (>2 chars) from:
      - Sentences containing hard modals (must/shall/required/cannot/never/always/...)
      - Sentences containing commitment content markers (amounts, dates, conditionals)
        — catches imperative form after compression ("Pay $100 by Friday...")

    Split on sentence boundaries INCLUDING semicolons so incidental clauses
    ("it's likely rainy, so plan accordingly") don't pollute the commitment set.
    Public proxy extractor (modal-pattern sieve + content extension, Fig. 4 of paper).
    """
    sentences = re.split(r'(?<=[.!?;])\s+', text.strip())
    words = set()
    for sent in sentences:
        if HARD_MODALS.search(sent) or COMMITMENT_CONTENT.search(sent):
            words.update(
                w.lower() for w in re.findall(r'\b[a-zA-Z0-9\$%]+\b', sent)
                if len(w) > 2
            )
    return words

def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return round(len(a & b) / len(a | b), 3)

def wc(text: str) -> int:
    return len(text.split())

def log(msg): print(msg, flush=True)

# ── Three conditions ──────────────────────────────────────────────────────────

def run_baseline(signal: str) -> list:
    """Condition 1: Paraphrase loop. No constraints."""
    current = signal
    turns = []
    for i in range(1, N_ITERATIONS + 1):
        out = llm(
            "You are a helpful assistant. Respond in one to two sentences.",
            f"Paraphrase this sentence while preserving meaning:\n\n{current}"
        )
        if not out:
            break
        turns.append({"i": i, "input": current, "output": out, "tokens": wc(out)})
        log(f"      B{i:02d} → {out[:80]}")
        current = out
        time.sleep(0.3)
    return turns


def run_compression(signal: str) -> list:
    """Condition 2: Summarize loop. No gate."""
    current = signal
    turns = []
    for i in range(1, N_ITERATIONS + 1):
        out = llm(
            "You are a helpful assistant. Be as concise as possible.",
            f"Summarize this sentence as concisely as possible:\n\n{current}"
        )
        if not out:
            break
        turns.append({"i": i, "input": current, "output": out, "tokens": wc(out)})
        log(f"      C{i:02d} → {out[:80]}")
        current = out
        time.sleep(0.3)
    return turns


def run_gate(signal: str) -> list:
    """
    Condition 3: Summarize → Extract → Reconstruct → feed reconstruction back.
    This matches the founding test methodology (paper Section 7.5):
    the user manually compressed to kernel and fed that back, not the AI's response.
    """
    current = signal
    turns = []
    for i in range(1, N_ITERATIONS + 1):

        # Step A — Summarize
        summary = llm(
            "You are a helpful assistant. Be concise.",
            f"Summarize this sentence as concisely as possible:\n\n{current}"
        )
        if not summary:
            break

        # Step B — Extract commitment kernel
        extraction = llm(
            "You are a commitment extractor. "
            "Extract ONLY the binding obligations, requirements, prohibitions, and conditions. "
            "Keep the original modal words (must/shall/required/cannot/never/always/do not). "
            "If no commitments exist, output exactly: [none]",
            f"Extract commitments from:\n\n{summary}",
            max_tokens=80
        )
        if not extraction or extraction.strip() == "[none]":
            extraction = summary   # fallback: use summary if nothing extracted

        # Step C — Reconstruct minimal statement
        reconstruction = llm(
            "You are a minimal statement reconstructor. "
            "Write the shortest complete sentence that preserves ALL the binding obligations listed. "
            "Do not add anything not in the list.",
            f"Reconstruct a minimal commitment statement from these elements:\n\n{extraction}",
            max_tokens=80
        )
        if not reconstruction:
            reconstruction = extraction

        turns.append({
            "i":             i,
            "input":         current,
            "summary":       summary,
            "extraction":    extraction,
            "output":        reconstruction,
            "tokens":        wc(reconstruction),
        })
        log(f"      G{i:02d} → extract: [{extraction[:50]}] → recon: {reconstruction[:60]}")

        # Feed reconstruction back — NOT the conversational response
        current = reconstruction
        time.sleep(0.5)
    return turns

# ── Stability computation ─────────────────────────────────────────────────────

def stability_curve(turns: list, origin: set) -> list:
    """Compute Jaccard stability at each iteration vs original signal."""
    curve = []
    for t in turns:
        c = extract_commitment_words(t["output"])
        curve.append({
            "i":         t["i"],
            "stability": jaccard(c, origin) if origin else None,
            "tokens":    t["tokens"],
            "output":    t["output"],
        })
    return curve

# ── Per-signal runner ─────────────────────────────────────────────────────────

def run_signal(signal: str, category: str) -> dict:
    log(f"\n  [{category}] {signal[:70]}")

    origin = extract_commitment_words(signal)
    log(f"  Origin commitments: {sorted(origin)[:10]}")

    log(f"  ── Condition 1: Baseline")
    b_turns = run_baseline(signal)
    b_curve = stability_curve(b_turns, origin)

    log(f"  ── Condition 2: Compression only")
    c_turns = run_compression(signal)
    c_curve = stability_curve(c_turns, origin)

    log(f"  ── Condition 3: Compression + Gate")
    g_turns = run_gate(signal)
    g_curve = stability_curve(g_turns, origin)

    # Summary at key iterations
    for label, curve in [("BASE", b_curve), ("COMP", c_curve), ("GATE", g_curve)]:
        pts = {p["i"]: p["stability"] for p in curve if p["stability"] is not None}
        log(f"  {label}: i1={pts.get(1,'?'):.2f}  i5={pts.get(5,'?'):.2f}  i10={pts.get(10,'?'):.2f}")

    return {
        "category":   category,
        "signal":     signal,
        "origin_c":   sorted(origin),
        "baseline":   b_curve,
        "compression": c_curve,
        "gate":       g_curve,
        "citation":   CITATION,
    }

# ── Report ────────────────────────────────────────────────────────────────────

def generate_report(results: list, ts: str) -> str:
    lines = [
        "# Phase Transition Report — Conservation Law of Commitment",
        f"**Run:** {ts}  ",
        f"**Patent:** {CITATION['patent']}  ",
        f"**DOI:** [{CITATION['doi']}]({CITATION['doi']})  ",
        f"**Owner:** {CITATION['owner']}",
        "",
        "## Stability at Key Iterations (Jaccard vs original)",
        "",
        "| Signal | B@1 | B@5 | B@10 | C@1 | C@5 | C@10 | G@1 | G@5 | G@10 |",
        "|--------|-----|-----|------|-----|-----|------|-----|-----|------|",
    ]

    def get(curve, i):
        pts = {p["i"]: p["stability"] for p in curve}
        v = pts.get(i)
        return f"{v:.2f}" if v is not None else "—"

    for r in results:
        lines.append(
            f"| {r['category']:15s} "
            f"| {get(r['baseline'],1)} | {get(r['baseline'],5)} | {get(r['baseline'],10)} "
            f"| {get(r['compression'],1)} | {get(r['compression'],5)} | {get(r['compression'],10)} "
            f"| {get(r['gate'],1)} | {get(r['gate'],5)} | {get(r['gate'],10)} |"
        )

    lines += [
        "",
        "## Phase Transition Signal",
        "",
        "Expected pattern if law holds:",
        "- **Baseline**: declining curve, sharp drop ~iteration 3–5",
        "- **Compression**: slower decline than baseline",
        "- **Gate**: flat near 1.0 — enforcement flattens drift",
        "",
        "## Methodology",
        "",
        "- Corpus: canonical_corpus.json (20 commitment signal categories)",
        f"- Model: {OPENAI_MODEL}",
        "- Extractor: modal-pattern sieve (public proxy, Fig. 4 of paper)",
        "- Metric: Jaccard stability = |C(S_n) ∩ C(S_0)| / |C(S_0)|",
        "- Gate reconstruction feeds back minimal statement, not conversational response",
        "  (matches founding test methodology, paper Section 7.5)",
        "",
        "## Citation",
        "",
        f"McHenry, D.J. (2026). A Conservation Law for Commitment in Language "
        f"Under Transformative Compression and Recursive Application. "
        f"Zenodo. {CITATION['doi']}",
        f"Patent {CITATION['patent']}.",
        f"Harness: https://{CITATION['github']}",
        "",
        "---",
        "*Generated by run_convergence_v2.py*",
    ]
    return "\n".join(lines)

# ── Main ──────────────────────────────────────────────────────────────────────

def run():
    corpus  = json.loads(CORPUS_PATH.read_text())
    signals = corpus["canonical_signals"]

    if SMOKE:
        signals = signals[:1]
        log("*** SMOKE TEST — 1 signal ***")

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    log(f"=== Phase Transition Test v2 — {ts} ===")
    log(f"Conditions: Baseline / Compression / Gate  |  Iterations: {N_ITERATIONS}")
    log(f"Citing: {CITATION['doi']}\n")

    results = []
    for s in signals:
        result = run_signal(s["signal"], s["category"])
        results.append(result)

    run_ts     = datetime.now().strftime("%H%M%S")
    json_path  = RUNS_DIR / f"convergence_v2_{run_ts}.json"
    report_path = RUNS_DIR / f"convergence_v2_report_{run_ts}.md"

    json_path.write_text(json.dumps(results, indent=2))
    report_path.write_text(generate_report(results, ts))

    log(f"\n✓ JSON:   {json_path}")
    log(f"✓ Report: {report_path}")


if __name__ == "__main__":
    run()
