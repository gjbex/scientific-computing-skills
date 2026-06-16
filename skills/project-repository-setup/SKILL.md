---
name: project-repository-setup
description: Set up or review a language-agnostic software repository baseline,
  especially when project layout, root-file hygiene, pre-commit hooks,
  formatting/linting entry points, local developer commands, and CI alignment
  need a sane default structure.
---

# Project Repository Setup

Use this skill when creating, reorganizing, or reviewing a software repository's
baseline structure and developer workflow, independent of any one programming
language or domain.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- top-level project layout and repo-root hygiene;
- baseline developer documentation and metadata files;
- pre-commit, formatting, and linting entry points;
- consistent local commands for build, test, and quality checks;
- keeping generated files, caches, and large artifacts out of source layout.

## When To Use

Use this skill when:

- the user asks to scaffold or clean up repository structure;
- a project has ad hoc scripts, scattered generated outputs, or unclear entry
  points;
- baseline files such as `.gitignore`, `.editorconfig`, `README`, or
  `CONTRIBUTING` need to be added or rationalized;
- pre-commit hooks or standard local validation commands should be introduced;
- CI and local developer workflows should use the same project entry points.

Do not use this skill to override a framework's required layout or an existing
repository convention that is already intentional and working.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Inspect existing top-level directories, scripts, and generated outputs.
3. Identify which project files are source, tests, docs, automation, examples,
   or generated artifacts.
4. Prefer small, conventional layout improvements before large migrations.
5. Keep local developer commands and CI entry points aligned.
6. State what was reorganized, what was left unchanged, and what follow-up
   cleanup remains.

Prefer incremental structure changes unless the user explicitly asks for a broad
repository reorganization.

## Top-Level Layout

A practical language-agnostic baseline is:

- `src/` or a project-specific source directory for primary implementation code;
- `tests/` for automated tests;
- `docs/` for user or developer documentation beyond the README;
- `examples/` for runnable examples or small sample projects;
- `scripts/` for maintenance or developer automation;
- `benchmarks/` for benchmark drivers or performance experiments when relevant.

Only create directories that have a clear near-term use. Avoid empty layout
theater.

## Repo Root Hygiene

Keep the repository root focused on discoverability:

- `README.md` for project purpose and common workflows;
- `LICENSE` or equivalent licensing file;
- `CONTRIBUTING.md` when contribution workflow matters;
- `.gitignore` for generated artifacts, caches, build trees, and local-only files;
- `.editorconfig` when basic editor consistency is useful;
- one or a few project-level build/config entry points.

Avoid dumping generated outputs, one-off scratch files, or many unrelated helper
scripts into the root.

## Pre-Commit and Quality Hooks

- Use pre-commit hooks to run fast, deterministic checks that catch common
  formatting and hygiene issues before commit.
- Keep hooks fast enough that developers do not routinely bypass them.
- Prefer repository-local config files and pinned tool versions where practical.
- Avoid hooks that depend on machine-local state or hidden external services.
- Make hook behavior consistent with CI checks so the same issues are caught in
  both places.

Treat expensive tests, flaky integration checks, or environment-specific
validation as poor pre-commit defaults.

Use `developer-tool-installation-policy` when deciding whether tools used by
hooks, local commands, or CI should be project-pinned or installed as isolated
global CLIs.

## Local Developer Commands

- Provide one obvious command path for setup, test, format, and lint when the
  project supports those actions.
- Prefer checked-in scripts, task runners, or documented commands over ad hoc
  shell snippets hidden in docs.
- Keep command names and behavior stable enough for CI and contributors.
- Avoid duplicating near-identical logic across local scripts and CI workflows.

If the repository spans multiple tools or languages, make the top-level command
surface clear even if internals remain tool-specific.

## Generated Files and Artifacts

- Keep build directories, caches, temporary outputs, and generated artifacts out
  of source directories when practical.
- Add ignore rules for files that are reproducible and not meant for review.
- Commit generated files only when there is a clear reason, such as vendored
  lockfiles, generated documentation intended for publication, or checked-in
  golden references.
- Store large data artifacts outside the normal source tree unless they are
  truly part of the repository contract.

Repository structure should make it obvious what humans edit and what tools
produce.

## Configuration Files

- Place tool configuration where the tool and repository conventions expect it.
- Prefer one canonical config per tool rather than scattered duplicates.
- Keep shared settings in version-controlled files and local overrides in
  ignored machine-specific files.
- Document non-obvious config interactions in the README or contribution docs.

Avoid configuration sprawl that makes it unclear which file actually controls a
tool.

## CI Alignment

- Reuse the same scripts, presets, or task-runner targets locally and in CI when
  practical.
- Keep CI jobs pointed at documented project entry points rather than bespoke
  one-off command sequences.
- Make pre-commit, lint, test, and build expectations visible from the repo
  itself, not only from CI logs.

Local and CI workflows should validate the same contract unless there is an
explicit reason to split them.

For GitHub-hosted projects, GitHub Actions is a practical default CI target.
Keep workflow files under `.github/workflows/`, run documented local commands
inside jobs, avoid broad permissions, and keep release or deployment automation
separate from ordinary validation unless the repository deliberately uses CI/CD.

Use `scientific-ci` for scientific CI design details such as build matrices,
numerical validation, artifacts, GitHub Actions job structure, and portability
tradeoffs.

## Anti-Patterns

- creating many empty directories with no current purpose;
- mixing source files, generated artifacts, and scratch outputs in one tree;
- maintaining separate undocumented commands for local development and CI;
- adding pre-commit hooks so slow or flaky that they get ignored;
- hardcoding machine-local paths in repository automation;
- moving large parts of the tree purely for aesthetics without improving
  discoverability or workflow.

## Validation Defaults

- Check that moved or newly referenced scripts and config files exist.
- Run the lightweight local quality or test entry point when practical.
- Verify that ignore rules do not hide source files that should be tracked.
- State explicitly which setup, hook, or validation paths were exercised.
- If a proposed layout change was not applied, note the reason and migration
  risk.

## Output Expectations

When using this skill, briefly note:

- which top-level layout, metadata, or automation files were added or changed;
- whether pre-commit, lint, format, or test entry points were introduced;
- how generated artifacts and local-only files are handled;
- which local validation commands were run;
- which repository-structure tradeoffs or follow-up cleanup remain.
