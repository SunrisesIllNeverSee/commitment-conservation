# Reproducibility Receipt

**Zenodo (concept DOI):** `https://doi.org/10.5281/zenodo.18267278`

**Date**: January 16, 2026  
**Status**: ✅ Harness Confirmed Operational

## Test Execution

All 13 tests passing in test suite:

```bash
cd harness
MPLBACKEND=Agg python -m pytest tests/test_full_harness.py -q
```

**Result**: `13 passed, 17 warnings in 21.09s`

### Test Coverage

✅ Commitment extraction (empty/nonempty signals)  
✅ Jaccard index (perfect match / zero overlap)  
✅ Intersection-based commitment computation  
✅ Compression sweep (Prediction 1: σ-invariance)  
✅ Recursion drift (Prediction 2: Δ_hard accumulation)  
✅ Canonical corpus loading  
✅ Transformation pipeline application  
✅ Complex signal processing

## Key Fixes Applied

1. **Blocking issue**: Replaced `plt.show()` → `plt.close()` in plotting functions
2. **Test errors**: Fixed duplicate function names, removed invalid parameters
3. **File paths**: Corrected corpus path from `data/` → `corpus/`
4. **Type checking**: Configured `.vscode/settings.json` to disable strict Pylance checks for research code

## Environment

- **Python**: 3.9.6 (virtual environment at `.venv/`)
- **Key dependencies**: transformers, spacy, matplotlib, pytest
- **Matplotlib backend**: Agg (non-GUI, CI-friendly)

## Running Tests

### Quick run (recommended):
```bash
MPLBACKEND=Agg pytest tests/test_full_harness.py -q
```

### Verbose output:
```bash
MPLBACKEND=Agg pytest tests/test_full_harness.py -v
```

### With minimal warnings:
```bash
MPLBACKEND=Agg pytest tests/test_full_harness.py -q --disable-warnings
```

## Notes

- Tests complete in ~20 seconds (model loading + transformations)
- Plots saved to PNG files, no GUI interaction required
- Warnings from dependencies (urllib3, matplotlib) are non-critical
- Type checking disabled for research flexibility

---

**Harness is research-ready for experimental evaluation.**
