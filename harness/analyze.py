#!/usr/bin/env python3
"""
Commitment Conservation Harness CLI

Runs the operational harness via a single command so users don't need to
navigate internal modules. Outputs JSON/CSV receipts.
"""

import os
import json
import argparse
from datetime import datetime

# Force non-GUI plotting backend (prevents macOS blocking)
os.environ.setdefault("MPLBACKEND", "Agg")

def _now_iso() -> str:
    return datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

def main() -> int:
    p = argparse.ArgumentParser(
        prog="commitment-harness",
        description="Run commitment conservation experiments (compression / recursion) and export receipts."
    )

    sub = p.add_subparsers(dest="cmd", required=True)

    # --- compression ---
    pc = sub.add_parser("compression", help="Run compression sweep on a signal.")
    pc.add_argument("--signal", required=True, help="Input signal text.")
    pc.add_argument("--out", default="outputs/compression_receipt.json", help="Output receipt path (json).")

    # --- recursion ---
    pr = sub.add_parser("recursion", help="Run recursion test on a signal.")
    pr.add_argument("--signal", required=True, help="Input signal text.")
    pr.add_argument("--depth", type=int, default=8, help="Recursion depth.")
    pr.add_argument("--enforced", action="store_true", help="Use enforcement mode.")
    pr.add_argument("--out", default="outputs/recursion_receipt.json", help="Output receipt path (json).")

    # --- full run (if you have a pipeline entry) ---
    pf = sub.add_parser("full", help="Run the deterministic pipeline (if available).")
    pf.add_argument("--out", default="outputs/full_receipt.json", help="Output receipt path (json).")

    args = p.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    # Import from your harness implementation
    try:
        from src.deterministic_pipeline import compression_sweep, recursion_test, deterministic_pipeline
    except ImportError:
        # Fallback to test_harness if deterministic_pipeline doesn't exist
        try:
            from src.test_harness import compression_sweep, recursion_test
            deterministic_pipeline = None
        except Exception as e:
            raise SystemExit(f"Import error: {e}\n(Verify you run this from the harness/ directory.)")

    receipt = {
        "timestamp_utc": _now_iso(),
        "command": args.cmd,
        "python": {
            "mpl_backend": os.environ.get("MPLBACKEND"),
        },
    }

    if args.cmd == "compression":
        sigma_vals, fid_vals = compression_sweep(args.signal)
        receipt.update({
            "input_signal": args.signal,
            "n": len(fid_vals),
            "sigma_values": sigma_vals,
            "fidelities": fid_vals,
        })

    elif args.cmd == "recursion":
        deltas = recursion_test(args.signal, depth=args.depth, enforced=args.enforced) if hasattr(recursion_test, '__code__') and 'enforced' in recursion_test.__code__.co_varnames else recursion_test(args.signal, depth=args.depth)
        receipt.update({
            "input_signal": args.signal,
            "depth": args.depth,
            "enforced": args.enforced if hasattr(recursion_test, '__code__') and 'enforced' in recursion_test.__code__.co_varnames else False,
            "deltas": deltas,
        })

    elif args.cmd == "full":
        if deterministic_pipeline is None:
            raise SystemExit("deterministic_pipeline not available. (Missing src/deterministic_pipeline.py import.)")
        result = deterministic_pipeline()
        receipt.update({"result": result})

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(receipt, f, indent=2, ensure_ascii=False)

    print(f"✓ Wrote receipt: {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
