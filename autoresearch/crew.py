#!/usr/bin/env python3
"""
autoresearch/crew.py — Convergence Study Analysis Crew
Agents: Theorist → Adversary → Reporter
Run: python3 crew.py [path/to/convergence_full_*.json]

Loads the latest (or specified) convergence run, analyzes it against the
Conservation Law of Commitment, and generates a structured research report.

CITATIONS
=========
Provisional Patent:  Serial No. 63/877,177
DOI:                 https://doi.org/10.5281/zenodo.18792459
GitHub:              github.com/SunrisesIllNeverSee/commitment-conservation
Owner:               Deric J. McHenry / Ello Cello LLC
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime

import requests

# ── Config ────────────────────────────────────────────────────────────────────

OPENAI_KEY = (Path.home() / ".hange/openai_api_key").read_text().strip()
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
MODEL      = "gpt-4o-mini"

RUNS_DIR   = Path(__file__).parent.parent / "runs"
REF_README = Path(__file__).parent.parent / "README.md"
ORIGIN     = Path(__file__).parent.parent / "foundational/origin_test.md"

CITATION = {
    "patent": "Serial No. 63/877,177 (Provisional)",
    "doi":    "https://doi.org/10.5281/zenodo.18792459",
    "github": "github.com/SunrisesIllNeverSee/commitment-conservation",
    "owner":  "Deric J. McHenry / Ello Cello LLC",
    "law":    "Conservation Law of Commitment: C(T(S)) ≈ C(S) with enforcement; C(T(S)) < C(S) without it",
}

# ── LLM ──────────────────────────────────────────────────────────────────────

def llm(system: str, user: str, max_tokens: int = 600) -> str:
    r = requests.post(OPENAI_URL,
        headers={"Authorization": f"Bearer {OPENAI_KEY}", "Content-Type": "application/json"},
        json={"model": MODEL,
              "messages": [{"role": "system", "content": system},
                           {"role": "user",   "content": user}],
              "max_tokens": max_tokens, "temperature": 0.3},
        timeout=60)
    if r.status_code == 200:
        return r.json()["choices"][0]["message"]["content"].strip()
    print(f"  OpenAI error: {r.status_code} — {r.text[:200]}")
    return ""

def log(msg): print(msg, flush=True)

# ── Data loader ───────────────────────────────────────────────────────────────

def load_latest_run() -> tuple[dict, Path]:
    """Find the most recent convergence_full_*.json across all run dates."""
    jsons = sorted(RUNS_DIR.glob("*/convergence_full_*.json"))
    if not jsons:
        raise FileNotFoundError(f"No convergence_full_*.json found under {RUNS_DIR}")
    path = jsons[-1]
    return json.loads(path.read_text()), path

def summarize_results(data: list) -> str:
    """Build a compact results table for agent context."""
    from collections import defaultdict
    groups = defaultdict(lambda: {"baseline": [], "enforced": []})
    for sig in data:
        for cond in sig["conditions"]:
            key  = (cond["n_turns"], cond["label"])
            side = "enforced" if cond["enforce"] else "baseline"
            groups[key][side].append(cond["result"]["total_tokens"])

    lines = ["Condition | Turns | N_signals | Avg_Baseline | Avg_Enforced | Delta | Compression%"]
    for (n_turns, label), sides in sorted(groups.items()):
        if sides["baseline"] and sides["enforced"]:
            avg_b = sum(sides["baseline"]) / len(sides["baseline"])
            avg_e = sum(sides["enforced"]) / len(sides["enforced"])
            delta = avg_b - avg_e
            pct   = (delta / avg_b * 100) if avg_b else 0
            n_sig = len(sides["baseline"])
            lines.append(f"{label} | {n_turns} | {n_sig} | {avg_b:.1f} | {avg_e:.1f} | {delta:.1f} | {pct:.1f}%")

    # Per-signal kernel retention rates
    lines.append("\nKernel Retention Rates (enforced conditions):")
    for sig in data[:3]:  # sample first 3 signals
        cat = sig["category"]
        for cond in sig["conditions"]:
            if cond["enforce"]:
                kr = cond["result"]["kernel_retention_rate"]
                lines.append(f"  [{cat}] {cond['label']} t{cond['n_turns']}: {kr:.1%}")

    return "\n".join(lines)

# ── Agents ────────────────────────────────────────────────────────────────────

SYS_THEORIST = """You are the theoretical architect of the Conservation Law of Commitment.
The law states: C(T(S)) ≈ C(S) with enforcement; C(T(S)) < C(S) without it.
Where:
  - S = original signal containing commitment (hard modals: must/shall/cannot/never/always)
  - T(S) = transformation of S through n conversational turns
  - C(·) = commitment content (semantic weight of binding language)
  - Anchor turns = original signal repeated as input (matches hand-logged founding test)
  - Cascade turns = AI's last output fed as next input

Analyze empirical data with precision. Flag confirmations and contradictions of the law.
Be brief and rigorous. No hype."""

SYS_ADVERSARY = """You are a red-team researcher testing the Conservation Law of Commitment.
Your job is to find weaknesses in the methodology, the metric, or the findings.
Be adversarial but honest. If data contradicts the law, say so clearly.
Focus on: metric validity, confounds, conditions that break the pattern, alternative explanations.
No filler. Every claim must be tied to specific data."""

SYS_REPORTER = """You write research reports for AgentArXiv and ClawInstitute submission.
Precise, minimal, structured for peer review.
Every claim is grounded in data. Limitations are named explicitly.
Format: clean Markdown with sections. No hype. No filler."""

# ── Run ───────────────────────────────────────────────────────────────────────

def run(run_path: Path = None):
    if run_path:
        data = json.loads(run_path.read_text())
        source = run_path
    else:
        data, source = load_latest_run()

    log(f"\n=== CONVERGENCE ANALYSIS CREW ===")
    log(f"Source: {source}")
    log(f"Signals: {len(data)} | Conditions per signal: {len(data[0]['conditions']) if data else 0}")
    log(f"Citing: {CITATION['doi']}\n")

    results_summary = summarize_results(data)
    readme_excerpt  = REF_README.read_text()[:3000]
    origin_excerpt  = ORIGIN.read_text()[:2000] if ORIGIN.exists() else ""

    # ── Agent 1: Theorist ─────────────────────────────────────────────────────
    log("--- Theorist ---")
    theory_prompt = f"""CONSERVATION LAW CONTEXT:
{readme_excerpt}

FOUNDING TEST (hand-logged):
{origin_excerpt}

CONVERGENCE RESULTS:
{results_summary}

Answer:
1. Which conditions confirm C(T(S)) < C(S) without enforcement? (baseline > enforced in token total)
2. Which conditions contradict the law? Explain why.
3. Does the anchor-then-cascade design correctly replicate the founding test methodology?
4. What does the kernel retention rate tell us about enforcement effectiveness?
5. What is the strongest empirical signal in this data for the Conservation Law?"""

    theory = llm(SYS_THEORIST, theory_prompt, max_tokens=700)
    log(theory)
    time.sleep(1)

    # ── Agent 2: Adversary ────────────────────────────────────────────────────
    log("\n--- Adversary ---")
    adversary_prompt = f"""RESULTS:
{results_summary}

THEORIST'S ANALYSIS:
{theory}

Red-team this study. Address:
1. Is word-count a valid proxy for commitment content? Name the failure cases.
2. Could compression in enforced conditions be an artifact of the enforcement constraint (shorter = tighter = not conservation)?
3. For conditions where enforcement loses to baseline — is that noise or a systematic problem?
4. What would falsify the Conservation Law using this methodology?
5. What is the minimum change to the harness that would make results interpretable?"""

    adversary = llm(SYS_ADVERSARY, adversary_prompt, max_tokens=700)
    log(adversary)
    time.sleep(1)

    # ── Agent 3: Reporter ─────────────────────────────────────────────────────
    log("\n--- Reporter ---")
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    reporter_prompt = f"""Write a structured research findings report for inclusion in the
Conservation Law of Commitment paper (Patent {CITATION['patent']}).

RESULTS TABLE:
{results_summary}

THEORETICAL ANALYSIS:
{theory}

ADVERSARIAL REVIEW:
{adversary}

Structure:
## Study Design
## Results Summary (include full table)
## Confirmations of Conservation Law
## Contradictions and Open Questions
## Adversarial Findings
## Methodology Notes
## Next Steps
## Citation

Keep under 900 words. Clean Markdown. Cite: Patent {CITATION['patent']}, DOI {CITATION['doi']}"""

    report = llm(SYS_REPORTER, reporter_prompt, max_tokens=1000)
    log("\n--- FINAL REPORT ---")
    log(report)

    # Save
    ts_file = datetime.now().strftime("%H%M%S")
    date_dir = source.parent
    out_path = date_dir / f"crew_analysis_{ts_file}.md"
    header = (
        f"# Convergence Analysis — Conservation Law of Commitment\n"
        f"**Run:** {ts}  \n"
        f"**Source:** {source.name}  \n"
        f"**Patent:** {CITATION['patent']}  \n"
        f"**DOI:** [{CITATION['doi']}]({CITATION['doi']})  \n"
        f"**Owner:** {CITATION['owner']}\n\n"
        f"---\n\n"
    )
    out_path.write_text(header + report)
    log(f"\nReport saved: {out_path}")
    return out_path


if __name__ == "__main__":
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    run(path)
