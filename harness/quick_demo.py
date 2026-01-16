#!/usr/bin/env python3
"""
Quick demo: Show baseline vs enforced on ONE signal.
This proves the concept without waiting for full experiment.
"""
import os
os.environ['MPLBACKEND'] = 'Agg'
os.chdir(os.path.dirname(__file__))

from src.test_harness import recursion_test, compression_sweep

# Single test signal
signal = "The tenant shall not sublet the premises without written consent."

print("="*70)
print("QUICK DEMO: Baseline vs Enforced (1 signal)")
print("="*70)
print(f"\nSignal: {signal}\n")

# BASELINE RECURSION
print("--- BASELINE Recursion Test ---")
deltas_base = recursion_test(signal, depth=5, enforce=False)
stab_base = (1.0 - deltas_base[-1]) * 100
print(f"✓ Baseline stability after 5 iterations: {stab_base:.1f}%\n")

# ENFORCED RECURSION  
print("--- ENFORCED Recursion Test ---")
deltas_enf = recursion_test(signal, depth=5, enforce=True)
stab_enf = (1.0 - deltas_enf[-1]) * 100
print(f"✓ Enforced stability after 5 iterations: {stab_enf:.1f}%\n")

# BASELINE COMPRESSION
print("--- BASELINE Compression Sweep ---")
_, fids_base = compression_sweep(signal, enforce=False)
avg_base = sum(fids_base) / len(fids_base) * 100
print(f"✓ Baseline avg fidelity: {avg_base:.1f}%\n")

# ENFORCED COMPRESSION
print("--- ENFORCED Compression Sweep ---")
_, fids_enf = compression_sweep(signal, enforce=True)
avg_enf = sum(fids_enf) / len(fids_enf) * 100
print(f"✓ Enforced avg fidelity: {avg_enf:.1f}%\n")

# RESULTS
print("="*70)
print("RESULTS:")
print("="*70)
print(f"Recursion Stability:")
print(f"  Baseline:  {stab_base:5.1f}%")
print(f"  Enforced:  {stab_enf:5.1f}%")
print(f"  Gain:      {stab_enf - stab_base:+5.1f} pp\n")
print(f"Compression Fidelity:")
print(f"  Baseline:  {avg_base:5.1f}%")
print(f"  Enforced:  {avg_enf:5.1f}%")
print(f"  Gain:      {avg_enf - avg_base:+5.1f} pp\n")
print("="*70)
