#!/usr/bin/env python3
"""Deterministic, offline audit of the original 2026-03-17 convergence v2 run.

Never calls an LLM and never recomputes semantic judgments. It only aggregates
the frozen outputs that are in the archived JSON. It intentionally does not
assert the validity of those scores as independent semantic ground truth.

Run: python3 paper_harness/audit_convergence_v2.py --output paper/corrections/2026-11-11/audit_summary.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RAW = ROOT / "working/runs_archive/2026-03-17/convergence_v2_234059.json"
REGIMES = ("baseline", "compression", "gate")
T_ENTRIES = {"baseline": "baseline_nli", "compression": "compression_nli", "gate": "gate_nli"}


def sample_stats(xs):
    if not xs:
        return {"n": 0, "mean": None, "sample_sd": None}
    return {
        "n": len(xs),
        "mean": round(statistics.mean(xs), 9),
        "sample_sd": round(statistics.stdev(xs), 9) if len(xs) > 1 else None,
    }


def extract_step(record, group, step, field):
    arr = record.get(group)
    if not isinstance(arr, list):
        raise ValueError(f"Expected {group} list for {record.get('category')}")
    matches = [obj for obj in arr if obj.get("i") == step]
    if len(matches) != 1:
        raise ValueError(f"Expected one step {step} in {group}/{record.get('category')}, got {len(matches)}")
    return matches[0].get(field)


def audit_data(data, *, step=10):
    if not isinstance(data, list):
        raise ValueError("Raw data is not a list")
    categories = [d.get("category") for d in data]
    if len(categories) != 20 or len(set(categories)) != len(categories):
        raise ValueError("Expected 20 distinct original signal categories")
    for d in data:
        for regime in REGIMES:
            for field in (regime, T_ENTRIES[regime]):
                vals = d.get(field)
                if not isinstance(vals, list) or set(x.get("i") for x in vals) != set(range(1, 11)):
                    raise ValueError(f"Expected steps 1..10 for {d['category']}/{field}")
    columns = {}
    coverage = {}
    for metric, (field, groups) in {
        "nli_judgment": ("nli_stability", T_ENTRIES),
        "lexical_stability": ("stability", {r: r for r in REGIMES}),
    }.items():
        by_regime = {}
        available = {}
        for regime, group in groups.items():
            vals = {
                d["category"]: extract_step(d, group, step, field)
                for d in data
            }
            invalid = [k for k,v in vals.items() if v is not None and (not isinstance(v, (int,float)) or not 0 <= v <= 1)]
            if invalid:
                raise ValueError(f"Invalid {metric} values for {invalid}")
            non_null = [float(v) for v in vals.values() if v is not None]
            by_regime[regime] = sample_stats(non_null)
            available[regime] = vals
        pairs = [(cat, available["gate"][cat], available["baseline"][cat])
                 for cat in categories if available["gate"][cat] is not None and available["baseline"][cat] is not None]
        differences = [float(g)-float(b) for cat,g,b in pairs]
        by_regime["gate_minus_baseline_paired"] = {
            **sample_stats(differences),
            "gate_wins": sum(d > 0 for d in differences),
            "ties": sum(d == 0 for d in differences),
            "gate_losses": sum(d < 0 for d in differences),
            "negative_categories": [cat for (cat,g,b),d in zip(pairs,differences) if d < 0],
        }
        columns[metric] = by_regime
        coverage[metric] = {
            "missing_by_regime": {
                regime: [k for k,v in vals.items() if v is None]
                for regime,vals in available.items()
            },
            "non_null_paired": len(pairs),
        }
    return {
        "step": step, "signals_total": len(data), "categories": categories,
        "metrics": columns, "coverage": coverage,
        "limitations": [
            "Descriptive statistics over a single frozen 20-signal, 10-step run, not independent replications.",
            "NLI field is the mean of two yes/no GPT entailment responses (possible values 0, 0.5, 1), not a calibrated probability.",
            "Canonical reference is created by the same extractor/reconstructor family being evaluated, not an independent human oracle.",
            "The lexical 'stability' field derives from word-set Jaccard in run_convergence_v2.py; the archived report mistakenly prints intersection/origin as its formula.",
            "Two categories have null lexical values; they are excluded from lexical means (not counted as zero or success).",
            "No statistical inference or model generalization is warranted from this single correlated run.",
        ],
    }


def run(raw_path=DEFAULT_RAW, step=10):
    data_bytes = Path(raw_path).read_bytes()
    data = json.loads(data_bytes)
    out = audit_data(data, step=step)
    out["source"] = {
        "path": str(Path(raw_path).relative_to(ROOT)) if Path(raw_path).is_relative_to(ROOT) else str(raw_path),
        "sha256": hashlib.sha256(data_bytes).hexdigest(),
        "kind": "frozen_archived_trace",
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", type=Path, default=DEFAULT_RAW)
    ap.add_argument("--step", type=int, default=10)
    ap.add_argument("--output", type=Path, help="Optional JSON output (does not touch original run)")
    args = ap.parse_args()
    result = run(args.source, args.step)
    body = json.dumps(result, indent=2, ensure_ascii=False)+"\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf8")
        print("Wrote", args.output)
    else:
        print(body)


if __name__ == "__main__":
    main()
