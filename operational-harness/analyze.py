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

def simple_extraction(text: str, quiet: bool = False, as_json: bool = False) -> int:
    """Simple commitment extraction (default mode)."""
    try:
        from src.extraction import extract_hard_commitments
        import spacy
    except ImportError as e:
        print(f"Import error: {e}", file=__import__('sys').stderr)
        return 1
    
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Error: spaCy model 'en_core_web_sm' not found.", file=__import__('sys').stderr)
        print("Install with: python -m spacy download en_core_web_sm", file=__import__('sys').stderr)
        return 1
    
    commitments = extract_hard_commitments(text, nlp)
    
    if as_json:
        import json
        print(json.dumps({"input": text, "commitments": sorted(list(commitments))}, indent=2))
    elif quiet:
        for c in sorted(commitments):
            print(c)
    else:
        print(f"Extracted {len(commitments)} commitment(s) from: \"{text[:60]}{'...' if len(text) > 60 else ''}\"")
        if commitments:
            for i, c in enumerate(sorted(commitments), 1):
                print(f"  {i}. {c}")
        else:
            print("  (none)")
    
    return 0

def main() -> int:
    import sys
    
    # Check if this is a 'run' subcommand or simple extraction
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        # Experimental mode
        return run_experiment()
    else:
        # Simple extraction mode
        return run_simple_extraction()

def run_simple_extraction() -> int:
    """Simple extraction CLI."""
    import sys
    p = argparse.ArgumentParser(
        prog="commitment-harness",
        description="Extract commitments from text.",
        epilog="For full experiments, use: python analyze.py run {compression|recursion|full}"
    )
    p.add_argument("text", help="Text to analyze")
    p.add_argument("--quiet", "-q", action="store_true", help="Output only commitments (no headers)")
    p.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = p.parse_args()
    return simple_extraction(args.text, quiet=args.quiet, as_json=args.json)

def run_experiment() -> int:
    """Experimental harness CLI."""
    import sys
    p = argparse.ArgumentParser(
        prog="commitment-harness run",
        description="Run commitment conservation experiments and export receipts."
    )

    sub = p.add_subparsers(dest="experiment", required=True)

    # compression experiment
    pc = sub.add_parser("compression", help="Run compression sweep on a signal.")
    pc.add_argument("--signal", required=True, help="Input signal text.")
    pc.add_argument("--out", default="outputs/compression_receipt.json", help="Output receipt path (json).")

    # recursion experiment
    pr = sub.add_parser("recursion", help="Run recursion test on a signal.")
    pr.add_argument("--signal", required=True, help="Input signal text.")
    pr.add_argument("--depth", type=int, default=8, help="Recursion depth.")
    pr.add_argument("--enforced", action="store_true", help="Use enforcement mode.")
    pr.add_argument("--out", default="outputs/recursion_receipt.json", help="Output receipt path (json).")

    # full pipeline
    pf = sub.add_parser("full", help="Run the deterministic pipeline (if available).")
    pf.add_argument("--out", default="outputs/full_receipt.json", help="Output receipt path (json).")

    # Remove 'run' from argv so argparse sees the subcommand correctly
    sys.argv.pop(1)
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
        "experiment": args.experiment,
        "python": {
            "mpl_backend": os.environ.get("MPLBACKEND"),
        },
    }

    if args.experiment == "compression":
        sigma_vals, fid_vals = compression_sweep(args.signal)
        receipt.update({
            "input_signal": args.signal,
            "n": len(fid_vals),
            "sigma_values": sigma_vals,
            "fidelities": fid_vals,
        })

    elif args.experiment == "recursion":
        deltas = recursion_test(args.signal, depth=args.depth, enforced=args.enforced) if hasattr(recursion_test, '__code__') and 'enforced' in recursion_test.__code__.co_varnames else recursion_test(args.signal, depth=args.depth)
        receipt.update({
            "input_signal": args.signal,
            "depth": args.depth,
            "enforced": args.enforced if hasattr(recursion_test, '__code__') and 'enforced' in recursion_test.__code__.co_varnames else False,
            "deltas": deltas,
        })

    elif args.experiment == "full":
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
