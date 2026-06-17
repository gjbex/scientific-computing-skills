# AGENTS.md

## Scope

This repository is a Codex plugin distribution for scientific-computing skills.
Keep the package focused on portable scientific-software engineering workflows.

Core skills use the `scientific-*` namespace. General workflow helpers belong
under support skills and must be documented separately in `README.md`.

## Editing Rules

- Preserve existing skill boundaries unless the user explicitly asks to split,
  merge, or rename skills.
- Do not add site-specific HPC login, scheduler, filesystem, account,
  allocation, or cluster-host facts to this repository.
- Do not commit generated artifacts such as `__pycache__/`, `*.pyc`, build
  directories, logs, temporary files, or local environment files.
- When moving tracked files, use Git rename hygiene: inspect status first,
  prefer `git mv`, and verify renames before committing.
- If public plugin metadata changes, keep `.codex-plugin/plugin.json`,
  `README.md`, `CITATION.cff`, and `NOTICE` consistent where applicable.

## Validation

Run these before finishing changes:

```bash
python3 tools/validate_plugin.py .
python3 tools/validate_skills.py skills
python3 -m py_compile skills/scientific-cli-benchmark/scripts/simple_benchmark.py tools/bump_version.py tools/validate_plugin.py tools/validate_skills.py
```

Use repo-local validators in `tools/`; do not make CI depend on a local
`~/.codex` installation.
