#!/usr/bin/env python3
"""
Compare baseline vs enforced compression for commitment conservation.
This is the killer experiment: showing enforcement improves stability.
"""
import json
import sys
import os

# Set non-GUI backend
os.environ['MPLBACKEND'] = 'Agg'

# Change to harness directory to make imports work
os.chdir(os.path.dirname(__file__))

from src.test_harness import recursion_test, compression_sweep

# Third set of test signals
signals = [
    "Users must change passwords every 90 days.",
    "The contract terminates after 12 months.",
    "Files must not exceed 10MB in size.",
    "Employees shall work 40 hours per week.",
    "Temperature must remain below 25 degrees Celsius."
]

print("="*70)
print("COMMITMENT CONSERVATION: BASELINE vs ENFORCED COMPARISON")
print("="*70)

results = {
    "baseline": {"recursion": [], "compression": []},
    "enforced": {"recursion": [], "compression": []}
}

for i, signal in enumerate(signals, 1):
    print(f"\n{'#'*70}")
    print(f"[{i}/5] Signal: {signal}")
    print(f"{'#'*70}")
    
    # BASELINE
    print(f"\n--- BASELINE (no enforcement) ---")
    print("  Running recursion test (depth=10)...")
    deltas_base = recursion_test(signal, depth=10, enforce=False)
    stability_base = 1.0 - deltas_base[-1]
    results["baseline"]["recursion"].append({
        "signal": signal,
        "deltas": deltas_base,
        "final_stability": stability_base
    })
    print(f"    ✓ Baseline stability: {stability_base*100:.1f}%")
    
    print("  Running compression sweep...")
    sigmas_base, fids_base = compression_sweep(signal, enforce=False)
    avg_fid_base = sum(fids_base) / len(fids_base)
    results["baseline"]["compression"].append({
        "signal": signal,
        "avg_fidelity": avg_fid_base,
        "fidelities": fids_base
    })
    print(f"    ✓ Baseline avg fidelity: {avg_fid_base*100:.1f}%")
    
    # ENFORCED
    print(f"\n--- ENFORCED (commitment preservation) ---")
    print("  Running recursion test (depth=10)...")
    deltas_enf = recursion_test(signal, depth=10, enforce=True)
    stability_enf = 1.0 - deltas_enf[-1]
    results["enforced"]["recursion"].append({
        "signal": signal,
        "deltas": deltas_enf,
        "final_stability": stability_enf
    })
    print(f"    ✓ Enforced stability: {stability_enf*100:.1f}%")
    
    print("  Running compression sweep...")
    sigmas_enf, fids_enf = compression_sweep(signal, enforce=True)
    avg_fid_enf = sum(fids_enf) / len(fids_enf)
    results["enforced"]["compression"].append({
        "signal": signal,
        "avg_fidelity": avg_fid_enf,
        "fidelities": fids_enf
    })
    print(f"    ✓ Enforced avg fidelity: {avg_fid_enf*100:.1f}%")
    
    # Improvement
    improvement_stability = (stability_enf - stability_base) * 100
    improvement_fidelity = (avg_fid_enf - avg_fid_base) * 100
    print(f"\n  📊 IMPROVEMENTS:")
    print(f"     Stability:  {improvement_stability:+.1f} pp")
    print(f"     Fidelity:   {improvement_fidelity:+.1f} pp")

# Aggregate statistics
avg_stab_base = sum(r["final_stability"] for r in results["baseline"]["recursion"]) / len(signals)
avg_stab_enf = sum(r["final_stability"] for r in results["enforced"]["recursion"]) / len(signals)
avg_fid_base = sum(r["avg_fidelity"] for r in results["baseline"]["compression"]) / len(signals)
avg_fid_enf = sum(r["avg_fidelity"] for r in results["enforced"]["compression"]) / len(signals)

print(f"\n{'='*70}")
print(f"FINAL RESULTS (n=5 signals, 10 iterations each)")
print(f"{'='*70}")
print(f"\nRECURSION STABILITY:")
print(f"  Baseline:  {avg_stab_base*100:5.1f}%")
print(f"  Enforced:  {avg_stab_enf*100:5.1f}%")
print(f"  Gain:      {(avg_stab_enf - avg_stab_base)*100:+5.1f} pp")

print(f"\nCOMPRESSION FIDELITY:")
print(f"  Baseline:  {avg_fid_base*100:5.1f}%")
print(f"  Enforced:  {avg_fid_enf*100:5.1f}%")
print(f"  Gain:      {(avg_fid_enf - avg_fid_base)*100:+5.1f} pp")

print(f"\n{'='*70}")
print(f"KEY FINDING:")
if (avg_stab_enf - avg_stab_base) > 0.4:  # 40+ pp improvement
    print(f"  ✓ Enforcement provides {(avg_stab_enf - avg_stab_base)*100:.0f} pp stability gain")
    print(f"    This validates the core thesis: commitment-aware systems")
    print(f"    dramatically outperform baseline transformers.")
else:
    print(f"  Enforcement improves stability by {(avg_stab_enf - avg_stab_base)*100:.1f} pp")
print(f"{'='*70}\n")

# Save results
os.makedirs('outputs', exist_ok=True)
with open('outputs/enforcement_comparison.json', 'w') as f:
    json.dump({
        "summary": {
            "n_signals": len(signals),
            "recursion_depth": 10,
            "baseline": {
                "avg_stability": avg_stab_base,
                "avg_fidelity": avg_fid_base
            },
            "enforced": {
                "avg_stability": avg_stab_enf,
                "avg_fidelity": avg_fid_enf
            },
            "improvements": {
                "stability_gain_pp": (avg_stab_enf - avg_stab_base) * 100,
                "fidelity_gain_pp": (avg_fid_enf - avg_fid_base) * 100
            }
        },
        "detailed_results": results
    }, f, indent=2)

print("✓ Detailed comparison saved to: outputs/enforcement_comparison.json")
