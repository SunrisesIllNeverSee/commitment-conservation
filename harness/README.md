# Commitment Conservation Test Harness

This directory contains the test harness for validating the commitment conservation law under compression and recursive application.

## Overview

The harness implements a falsification framework that operationalizes commitment invariance using:

- Compression-based stress tests
- Lineage-aware evaluation
- Model-agnostic testing infrastructure

## Structure

- **src/** - Core harness implementation
  - `harness.py` - Main test harness
  - `test_harness.py` - Test framework
  - `extraction.py` - Commitment extraction
  - `metrics.py` - Evaluation metrics
  - `samples.py` - Sample data management
  - `plotting.py` - Visualization utilities
  - `config.py` - Configuration management
  - `deterministic_pipeline.py` - Deterministic testing pipeline
  - `advanced_extractor.py` - Advanced extraction methods

- **tests/** - Unit and integration tests
  - `test_harness.py` - Harness tests
  - `test_full_harness.py` - Full integration tests

## Configuration Files

- `requirements.txt` - Python dependencies
- `pyproject.toml` - Project configuration
- `environment.yml` - Conda environment specification
- `Harnesstest.ini` - Harness configuration

## Running the Harness

```bash
# Install dependencies
pip install -r requirements.txt

# Run the harness
cd src && python harness.py

# Run tests
pytest tests/
```

## Purpose

This harness is designed to test whether commitment content is conserved under:

1. **Compression** - Reduction to essential structure
2. **Recursion** - Repeated self-application with lineage tracking

The framework is model-agnostic and can be applied to both human and machine-generated language.

### Environment Notes

This harness specifies the structure and invariants of the evaluation.
Exact dependency resolution may vary across systems (OS, Python, backend).
Environment-related failures should be distinguished from invariant violations.

## Citation

If you use this harness, please cite the original paper:

```text
McHenry, D. J. (2026). A Conservation Law for Commitment in Language Under 
Transformative Compression and Recursive Application. Zenodo. 
DOI: 10.5281/zenodo.18267279
```
