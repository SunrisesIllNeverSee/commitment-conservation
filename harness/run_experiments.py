#!/usr/bin/env python3
"""
Run experiments on canonical corpus and generate summary statistics.
"""
import json
import sys
import os

# Set non-GUI backend
os.environ['MPLBACKEND'] = 'Agg'

sys.path.insert(0, 'harness/src')

from test_harness import recursion_test, compression_sweep

# Test signals from corpus
signals = [
    "This function must return an integer.",
    "The tenant shall not sublet the premises without written consent.",
    "You must wear a helmet while cycling.",
    "All passwords must be at least 8 characters long.",
    "The budget cannot exceed $5000."
]

results = {"recursion": [], "compression": []}

print("Running experiments on 5 signals...")

for i, signal in enumerate(signals, 1):
    print(f"\n[{i}/5] Testing: {signal[:50]}...")
    
    # Recursion test
    print("  - Running recursion test (depth=10)...")
    deltas = recursion_test(signal, depth=10)
    stability = 1.0 - deltas[-1]  # Final stability
    results["recursion"].append({
        "signal": signal,
        "deltas": deltas,
        "final_stability": stability
    })
    print(f"    Stability after 10 iterations: {stability*100:.1f}%")
    
    # Compression test
    print("  - Running compression sweep...")
    sigmas, fids = compression_sweep(signal)
    avg_fidelity = sum(fids) / len(fids)
    results["compression"].append({
        "signal": signal,
        "avg_fidelity": avg_fidelity,
        "fidelities": fids
    })
    print(f"    Average fidelity: {avg_fidelity*100:.1f}%")

# Calculate averages
avg_recursion_stability = sum(r["final_stability"] for r in results["recursion"]) / len(results["recursion"])
avg_compression_fidelity = sum(r["avg_fidelity"] for r in results["compression"]) / len(results["compression"])

print(f"\n{'='*60}")
print(f"RESULTS (n=5 signals, 10 iterations each):")
print(f"{'='*60}")
print(f"  Average commitment stability after 10 recursions: {avg_recursion_stability*100:.1f}%")
print(f"  Average compression fidelity: {avg_compression_fidelity*100:.1f}%")
print(f"{'='*60}\n")

# Save detailed results
os.makedirs('harness/outputs', exist_ok=True)
with open('harness/outputs/experiment_results.json', 'w') as f:
    json.dump({
        "summary": {
            "n_signals": len(signals),
            "recursion_depth": 10,
            "avg_recursion_stability": avg_recursion_stability,
            "avg_compression_fidelity": avg_compression_fidelity
        },
        "detailed_results": results
    }, f, indent=2)
    
print("✓ Detailed results saved to: harness/outputs/experiment_results.json")