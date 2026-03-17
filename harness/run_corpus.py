#!/usr/bin/env python3
"""
Full corpus run — all 20 canonical signals, baseline vs enforced.
"""
import json
import os
from datetime import datetime

os.environ['MPLBACKEND'] = 'Agg'
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from src.test_harness import recursion_test, compression_sweep

RECURSION_DEPTH = 20
CORPUS_PATH     = "../corpus/canonical_corpus.json"

with open(CORPUS_PATH) as f:
    corpus = json.load(f)["canonical_signals"]

print(f"{'='*70}")
print(f"FULL CORPUS RUN — {len(corpus)} signals, depth={RECURSION_DEPTH}")
print(f"{'='*70}\n")

results = []

for i, entry in enumerate(corpus, 1):
    cat    = entry["category"]
    signal = entry["signal"]
    print(f"[{i:02d}/{len(corpus)}] [{cat:15s}] {signal[:55]}...")

    # Baseline
    b_deltas    = recursion_test(signal, depth=RECURSION_DEPTH, enforce=False)
    b_stability = 1.0 - b_deltas[-1]
    _, b_fids   = compression_sweep(signal, enforce=False)
    b_fidelity  = sum(b_fids) / len(b_fids)

    # Enforced
    e_deltas    = recursion_test(signal, depth=RECURSION_DEPTH, enforce=True)
    e_stability = 1.0 - e_deltas[-1]
    _, e_fids   = compression_sweep(signal, enforce=True)
    e_fidelity  = sum(e_fids) / len(e_fids)

    gain_stab = e_stability - b_stability
    gain_fid  = e_fidelity  - b_fidelity

    print(f"  Stability  B={b_stability*100:.0f}%  E={e_stability*100:.0f}%  Δ={gain_stab*100:+.0f}pp")
    print(f"  Fidelity   B={b_fidelity*100:.1f}%  E={e_fidelity*100:.1f}%  Δ={gain_fid*100:+.1f}pp\n")

    results.append({
        "category": cat,
        "signal": signal,
        "baseline_stability": b_stability,
        "enforced_stability": e_stability,
        "stability_gain": gain_stab,
        "baseline_fidelity": b_fidelity,
        "enforced_fidelity": e_fidelity,
        "fidelity_gain": gain_fid,
    })

n = len(results)
avg_b_stab = sum(r["baseline_stability"] for r in results) / n
avg_e_stab = sum(r["enforced_stability"]  for r in results) / n
avg_b_fid  = sum(r["baseline_fidelity"]  for r in results) / n
avg_e_fid  = sum(r["enforced_fidelity"]  for r in results) / n

print(f"{'='*70}")
print(f"FINAL — n={n} signals, depth={RECURSION_DEPTH}")
print(f"{'='*70}")
print(f"  RECURSION STABILITY")
print(f"    Baseline: {avg_b_stab*100:.1f}%   Enforced: {avg_e_stab*100:.1f}%   Gain: {(avg_e_stab-avg_b_stab)*100:+.1f}pp")
print(f"  COMPRESSION FIDELITY")
print(f"    Baseline: {avg_b_fid*100:.1f}%   Enforced: {avg_e_fid*100:.1f}%   Gain: {(avg_e_fid-avg_b_fid)*100:+.1f}pp")
print(f"{'='*70}\n")

os.makedirs("outputs", exist_ok=True)
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"outputs/corpus_run_{ts}.json"
with open(out_path, "w") as f:
    json.dump({
        "run_timestamp": ts,
        "parameters": {"recursion_depth": RECURSION_DEPTH},
        "n_signals": n,
        "summary": {
            "avg_baseline_stability": avg_b_stab,
            "avg_enforced_stability": avg_e_stab,
            "stability_gain": avg_e_stab - avg_b_stab,
            "avg_baseline_fidelity": avg_b_fid,
            "avg_enforced_fidelity": avg_e_fid,
            "fidelity_gain": avg_e_fid - avg_b_fid,
        },
        "per_signal": results,
    }, f, indent=2)

print(f"✓ Results saved: {out_path}")
