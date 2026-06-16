---
name: developer-tool-installation-policy
description: Decide whether developer and scientific workflow tools belong in
  project-local environments, pre-commit or CI configuration, or isolated global
  installs such as pipx, uv tool, or pixi global.
---

# Developer Tool Installation Policy

Use this skill when deciding where small command-line tools should live:
project metadata, local developer environments, pre-commit hooks, CI jobs, or
isolated global tool installs.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a consistent split for tools such as:

- `ruff`, `black`, `mypy`, `pytest`, `pre-commit`;
- `dvc`, `git-lfs`, data and workflow utilities;
- `hpccm`, `apptainer`, `docker`, `podman`;
- `quarto`, `jupyter`, `nbval`, `nbstripout`;
- `nextflow`, `snakemake`, `tox`, `nox`, `hatch`, `twine`;
- other small CLIs used across many repositories.

The goal is to avoid both dependency sprawl and hidden global assumptions.

## Default Policy

Use a split policy:

- Put project contract tools in the project environment, repository metadata,
  pre-commit configuration, or CI configuration.
- Put personal convenience tools in isolated global installs such as `pipx`,
  `uv tool install`, or `pixi global install`.

A tool is part of the project contract when the repository depends on it for
correctness, generated files, contributor workflow, CI, release artifacts, or
reproducible scientific outputs.

A tool is personal convenience when it is only used interactively, across many
unrelated repositories, or as a launcher/bootstrapper whose exact version does
not define repository outputs.

## Project-Local Tools

Prefer a project-local or repository-pinned tool when:

- CI runs it;
- pre-commit enforces it;
- contributors must run it to make valid changes;
- it generates committed files;
- it affects scientific results, figures, containers, notebooks, data
  pipelines, or release artifacts;
- documented commands assume it is available;
- the exact version affects behavior or output stability.

Project-local placement can mean `pyproject.toml`, `pixi.toml`, `environment.yml`,
`requirements-dev.txt`, `.pre-commit-config.yaml`, `tox.ini`, `noxfile.py`, a
language-specific lockfile, or CI setup steps. Match the repository's existing
tooling rather than adding a second environment manager without a reason.

## Global Isolated Tools

Use isolated global installs for tools that are useful across many projects but
are not part of a specific repository's validated contract.

Appropriate examples:

- `pipx install pre-commit` as a user-level launcher;
- `uv tool install ruff` for ad hoc formatting or inspection;
- `pixi global install hpccm` for drafting container recipes;
- global `dvc` for read-only inspection across repositories;
- global `quarto` or `nextflow` only when repository documentation and CI do
  not rely on a hidden unpinned version.

Avoid `pip install --user` into an unscoped Python environment for shared CLI
tools. Prefer isolated tool environments so dependencies do not conflict across
projects.

## Decision Table

| Situation | Default placement |
| --- | --- |
| CI or pre-commit runs the tool | project config plus CI setup |
| Tool generates committed files | project-pinned version and freshness check |
| Tool affects scientific outputs | project environment or documented lockfile |
| Tool is only used for ad hoc inspection | isolated global install |
| Tool bootstraps project environments | isolated global install plus project docs |
| Contributors must run it | project docs and reproducible install path |
| Exact version is irrelevant | isolated global install is acceptable |

When in doubt, treat reproducibility-sensitive tools as project contract tools.

## Tool-Specific Guidance

### Ruff and Similar Linters

Use a global isolated `ruff` for quick cross-repository inspection. Pin or
configure `ruff` in the project when formatting, linting, pre-commit, or CI
depends on it. Keep configuration in version control.

### DVC

Use global `dvc` for casual inspection. Treat DVC as project-local policy when
the repository contains `.dvc` files, `dvc.yaml`, `dvc.lock`, documented
`dvc pull`, `dvc status`, or `dvc repro` workflows. Do not rely on undocumented
local DVC remotes or private credentials.

### HPCCM

Use global `hpccm` for drafting recipes. Pin HPCCM in the project or CI when an
HPCCM recipe generates committed Apptainer/Singularity definition files. Add a
freshness check that regenerates `.def` files and fails on diffs.

### Pre-Commit

Installing the `pre-commit` launcher globally is fine. Hook versions and hook
configuration belong in `.pre-commit-config.yaml` and should align with CI.

### Nextflow and Quarto

Global installs are acceptable for personal use, but repository workflows should
document expected versions and CI setup when pipelines or rendered documents are
part of the project contract.

## CI and Documentation

For any project contract tool:

- document the supported setup path in the README or contribution docs;
- make CI install the tool explicitly instead of relying on runner state;
- pin versions when generated output stability matters;
- expose one documented local command that exercises the same checks as CI when
  practical;
- state when a globally installed launcher is only a convenience, not a
  substitute for project configuration.

## Anti-Patterns

- requiring hidden global tools for CI-equivalent local checks;
- letting global `ruff`, `dvc`, `hpccm`, or `quarto` versions define committed
  outputs without a project pin;
- installing every small CLI into every project when it is only a personal
  launcher;
- mixing multiple environment managers without a clear boundary;
- committing generated outputs without documenting the tool and command that
  produced them;
- assuming `pipx`, `uv`, or `pixi global` installs are visible inside CI,
  containers, or HPC batch jobs.

## Output Expectations

When using this skill, state:

- which tools are project contract tools and why;
- which tools are personal convenience tools and where to install them;
- which repository files should pin or configure project tools;
- which CI, pre-commit, or documentation updates are needed;
- any validation that could not be performed because a tool is unavailable.
