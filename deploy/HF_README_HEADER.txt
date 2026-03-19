---
title: Commitment Conservation Harness
emoji: ⚖️
colorFrom: blue
colorTo: purple
sdk: static
pinned: false
license: cc-by-4.0
tags:
  - nlp
  - evaluation
  - benchmark
  - summarization
  - semantic-preservation
  - commitment-conservation
  - transformers
  - llm
---

# Commitment Conservation Harness

**Open evaluation framework for testing the conservation law proposed in the preprint.**

📄 **Paper**: [A Conservation Law for Commitment in Language Under Transformative Compression (v0.03)](https://doi.org/10.5281/zenodo.18274930)  
🏗️ **Zenodo Record**: https://zenodo.org/records/18274930  
💻 **GitHub**: https://github.com/SunrisesIllNeverSee/commitment-conservation

---

## Quick Start

Run the harness locally:

```bash
# Clone and install
git clone https://huggingface.co/burnmydays/commitment_conservation_harness
cd commitment_conservation_harness/harness
pip install -r requirements.txt

# Run baseline experiments
python run_experiments.py

# Run baseline vs enforced comparison
python compare_enforcement.py
```

Results saved to `harness/outputs/` as JSON files showing baseline vs enforced stability.

---

