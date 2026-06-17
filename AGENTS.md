# AGENTS.md

## Scope

This repository is a Codex plugin distribution for scientific-computing skills.
Keep the package focused on portable scientific-software engineering workflows.

Core skills use the `scientific-*` namespace. General workflow helpers belong
under support skills and must be documented separately in `README.md`.

## Development And Installation Checkouts

Use this repository as the active development checkout. Feature work should
happen here on short-lived feature branches based on the repository's current
integration branch. For this repository, that branch is `development` unless
the maintainer says otherwise. Run validation before merging or publishing.

Before implementing a new fix, feature, refactor, or documentation concern,
inspect `git status --short --branch` and create a focused branch from
the intended integration branch unless the user explicitly asks to work
directly on the current branch. Keep that branch to one concern.

While working, watch for drift from the branch's stated intent. If a requested
or discovered change would add a second concern to the branch or pull request,
pause and warn the user. Propose either staying focused on the current concern
or moving the new concern to a separate branch.

Treat `~/plugins/scientific-computing-skills` as the Codex plugin installation
checkout. It should normally stay on `main`, be updated from the released or
merged state, and then be used for `codex plugin add
scientific-computing-skills@personal`.

Only install from a feature branch in `~/plugins/scientific-computing-skills`
when intentionally testing unreleased skill behavior. Switch it back to `main`
after that test so new Codex sessions do not accidentally load unfinished
changes.

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
