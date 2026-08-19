# Migration Map — commitment-conservation

**Installed:** 2026-08-19
**Mode:** migrate
**Profile:** research

## Existing structure preserved

All existing root directories declared in `allowed_root_dirs_extra`:
- `paper/` — main paper drafts (primary deliverable)
- `experiments/` — EXP-001 through EXP-007
- `operational-harness/`, `paper_harness/` — harness code
- `paper_experiment_results/` — experiment result artifacts
- `corpus/` — canonical corpus and experiment corpora
- `working/` — internal planning docs (added to archive_roots)
- `.firecrawl/` — tool cache (gitignored)

All existing root files declared in `allowed_root_files_extra`:
- `CITATION.cff`, `CLAUDE.md`, `FIX_IMMEDIATELY.md`, `QUICKNOTES.md`,
  `REPRODUCIBILITY.md`, `RESEARCH_CHRONICLE.md`, `RUN_LOG.md`, `paper.zip`

## Canon context

- Authority role: `evidence_source`
- Canon contexts: `commitment-theory`, `conservation_law`
- Authority owner: `search_authority`

## Migration steps (before enforce)

1. [ ] Run `repo_check.py --ci` until clean (currently clean)
2. [ ] Verify GitHub ruleset application (solo-fast)
3. [ ] Switch REPO.yaml mode from `migrate` → `enforce`

## Enforce readiness

Ready after ruleset verification — no structural defects.
