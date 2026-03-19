# Minimal Python Test Harness for Commitment Conservation Protocol
# This script implements the falsification protocol from Section 3 of the preprint.
# It applies transformations (T_i), extracts hard commitments, computes Jaccard fidelity/drift, and plots results.
# Requires: transformers, spacy, matplotlib, numpy
# Run: python test_harness.py

import os
import json
from transformers import pipeline
import spacy
import matplotlib.pyplot as plt
from typing import List, Set
import numpy as np
from datetime import datetime
from .extraction import extract_hard_commitments
from .metrics import jaccard, hybrid_fidelity

# Load models
nlp = spacy.load("en_core_web_sm")
# Use lighter distilbart model for more faithful extraction-based summarization
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
translator_en_de = pipeline("translation", model="Helsinki-NLP/opus-mt-en-de")
translator_de_en = pipeline("translation", model="Helsinki-NLP/opus-mt-de-en")

# Config
SIGMA_GRID = [120, 80, 40, 20, 10, 5]
RECURSION_DEPTH = 8
SAMPLE_SIGNALS = [
    "You must pay $100 by Friday if the deal closes; it's likely rainy, so plan accordingly.",
    "This function must return an integer.",
    "Always verify the user's age before proceeding.",
    "You must do this task immediately.",  # Simpler, direct commitment
    # "Your custom text with commitments here."
]

def extract_hard_commitments(text: str) -> Set[str]:
    """Extract hard commitments using rule-based spaCy parsing."""
    doc = nlp(text)
    commitments = set()
    for sent in doc.sents:
        # Split on semicolons to handle multiple clauses in one sentence
        clauses = [c.strip() for c in sent.text.split(';')]
        for clause in clauses:
            clause_lower = clause.lower()
            if any(modal in clause_lower for modal in ["must", "shall", "cannot", "required"]):
                # Normalize: strip trailing punctuation, extra spaces
                normalized = clause.strip().rstrip('.!?').strip()
                commitments.add(normalized)
    return commitments

def apply_transformations(signal: str) -> List[str]:
    """Apply k=3 transformations: summarization, paraphrase (back-translation), abstraction."""
    # Summarization
    summ = summarizer(signal, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
    
    # Paraphrase via back-translation
    de = translator_en_de(signal, max_length=400, do_sample=False)[0]['translation_text']
    para = translator_de_en(de, max_length=400, do_sample=False)[0]['translation_text']
    
    # Abstraction: first sentence
    abstract = signal.split(".")[0].strip()
    
    return [summ, para, abstract]

def compute_intersection_commitments(signal: str) -> Set[str]:
    """Compute C_hard,op as intersection of transformed extractions."""
    transforms = apply_transformations(signal)
    all_commitments = [extract_hard_commitments(t) for t in transforms]
    
    # Debug output
    print(f"\n[DEBUG] Transform commitments:")
    for i, (t, c) in enumerate(zip(transforms, all_commitments)):
        print(f"  Transform {i+1}: {t[:60]}... -> {len(c)} commitments: {c}")
    
    if all_commitments:
        intersection = set.intersection(*all_commitments)
        print(f"  Intersection: {intersection}")
        return intersection
    return set()

def jaccard(a: Set[str], b: Set[str]) -> float:
    """Jaccard index."""
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)

def compress_with_enforcement(signal: str, max_length: int) -> str:
    """
    Compress with commitment enforcement.
    1. Extract commitments from original
    2. Compress
    3. Check if commitments preserved
    4. If not, append missing commitments (truncate summary if needed)
    """
    # Extract original commitments
    original_commitments = extract_hard_commitments(signal)
    
    # Compress normally
    compressed = summarizer(signal, max_length=max_length, min_length=5, do_sample=False)[0]['summary_text']
    
    # Check what's preserved
    compressed_commitments = extract_hard_commitments(compressed)
    missing = original_commitments - compressed_commitments
    
    # If commitments missing, enforce by appending
    if missing:
        # Append missing commitments
        enforcement_text = " " + " ".join(missing)
        # Truncate if needed to fit in max_length (rough token estimate: 4 chars per token)
        estimated_tokens = len(compressed + enforcement_text) // 4
        if estimated_tokens > max_length:
            # Truncate summary to make room
            available_chars = max_length * 4 - len(enforcement_text)
            compressed = compressed[:max(0, available_chars)] + "..."
        compressed = compressed + enforcement_text
    
    return compressed

def paraphrase_with_enforcement(signal: str) -> str:
    """
    Paraphrase via back-translation with commitment enforcement.
    """
    original_commitments = extract_hard_commitments(signal)
    
    # Back-translate
    de = translator_en_de(signal, max_length=400, do_sample=False)[0]['translation_text']
    paraphrased = translator_de_en(de, max_length=400, do_sample=False)[0]['translation_text']
    
    # Check preservation
    para_commitments = extract_hard_commitments(paraphrased)
    missing = original_commitments - para_commitments
    
    # Append missing
    if missing:
        paraphrased = paraphrased + " " + " ".join(missing)
    
    return paraphrased

def compression_sweep(signal: str, enforce: bool = False):
    """Test Prediction 1: Compression invariance."""
    # Use original signal commitments as base, not intersection
    base = extract_hard_commitments(signal)
    mode = "ENFORCED" if enforce else "BASELINE"
    print(f"\n{'='*80}")
    print(f"Testing signal ({mode}): {signal}")
    print(f"Base commitments (from original): {base}")
    print(f"{'='*80}")
    fid_vals = []
    for sigma in SIGMA_GRID:
        if enforce:
            compressed = compress_with_enforcement(signal, sigma)
        else:
            compressed = summarizer(signal, max_length=sigma, min_length=5, do_sample=False)[0]['summary_text']
        comp_commitments = extract_hard_commitments(compressed)
        fid = hybrid_fidelity(base, comp_commitments)
        print(f"  σ={sigma:3d} | Compressed: {compressed[:60]:<60} | Commitments: {len(comp_commitments):2d} | Fidelity: {fid:.3f}")
        fid_vals.append(fid)
    
    # Plot
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.figure(figsize=(10, 6))
    plt.plot(SIGMA_GRID, fid_vals, marker='o', linewidth=2, markersize=8)
    plt.xlabel("Compression Threshold (σ)", fontsize=12)
    plt.ylabel("Fid_hard(σ)", fontsize=12)
    mode_str = "ENFORCED" if enforce else "BASELINE"
    plt.title(f"{mode_str} Fidelity vs σ for: {signal[:50]}...\n{timestamp}", fontsize=11)
    plt.gca().invert_xaxis()
    plt.grid(alpha=0.3)
    plt.ylim(-0.05, 1.05)
    plt.tight_layout()
    mode_file = mode_str.lower()
    plt.savefig(f"fid_plot_{mode_file}_{hash(signal)}.png", dpi=150)
    plt.close()  # Use close() instead of show() to avoid blocking in tests
    
    return SIGMA_GRID, fid_vals

def recursion_test(signal: str, depth: int = RECURSION_DEPTH, enforce: bool = False):
    """Test Prediction 2: Recursive drift."""
    # Use original signal commitments as base
    base = extract_hard_commitments(signal)
    mode = "ENFORCED" if enforce else "BASELINE"
    deltas = []
    current = signal
    for n in range(depth + 1):
        cur_commitments = extract_hard_commitments(current)
        delta = 1.0 - jaccard(base, cur_commitments)
        deltas.append(delta)
        # Recursive transformation: paraphrase
        if enforce:
            current = paraphrase_with_enforcement(current)
        else:
            current = apply_transformations(current)[1]  # Use paraphrase
    
    # Plot
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    plt.figure(figsize=(10, 6))
    plt.plot(range(depth + 1), deltas, marker='o', linewidth=2, markersize=8)
    plt.xlabel("Recursion Step (n)", fontsize=12)
    plt.ylabel("Δ_hard(n)", fontsize=12)
    mode_str = "ENFORCED" if enforce else "BASELINE"
    plt.title(f"{mode_str} Drift vs n for: {signal[:50]}...\n{timestamp}", fontsize=11)
    plt.grid(alpha=0.3)
    plt.ylim(-0.05, 1.05)
    plt.tight_layout()
    mode_file = mode_str.lower()
    plt.savefig(f"delta_plot_{mode_file}_{hash(signal)}.png", dpi=150)
    plt.close()  # Use close() instead of show() to avoid blocking in tests
    
    return deltas

if __name__ == "__main__":
    # Run on sample signals
    for signal in SAMPLE_SIGNALS:
        print(f"\nTesting signal: {signal}")
        compression_sweep(signal)
        # Skip recursion_test for now (uses slow translation models)
        # recursion_test(signal)
        print("Compression sweep plot saved.")