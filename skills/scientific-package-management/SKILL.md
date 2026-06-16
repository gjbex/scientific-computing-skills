---
name: scientific-package-management
description: Organize and maintain language-managed scientific projects,
  especially Python-first workflows where dependency management, virtual
  environments, `pyproject.toml`, lockfiles, conda-style environments, and
  practical project layout need reproducible defaults, with lighter guidance
  for R and Julia environments.
---

# Scientific Package Management

Use this skill when editing or reviewing scientific software that depends more
on language-level package managers and project layout than on a compiled build
system.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- dependency declaration and environment isolation;
- project layout for maintainable scientific code;
- reproducible package resolution and lockfile practices;
- separating application code, experiments, tests, and data artifacts;
- clarifying when a project should behave like a package versus a loose script
  collection.

## When To Use

Use this skill when:

- the user asks how to structure a Python, R, or Julia scientific project;
- dependency management or environment reproducibility is unclear;
- a repository mixes scripts, notebooks, and reusable code without a clear
  layout;
- package metadata, optional dependencies, or editable installs need cleanup;
- a Python project needs `pyproject.toml` or a more coherent environment story.

Do not use this skill for compiled build-system work such as compiler flags,
CMake target structure, or sanitizer configuration. Use the build-system skill
for that.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Inspect the existing entry points, packaging metadata, and environment files.
3. Keep one obvious developer workflow for install, test, and run tasks.
4. Prefer reproducible dependency declarations over ad-hoc local instructions.
5. Separate reusable library code from notebooks, experiments, and generated
   outputs.
6. State clearly which package manager or environment tool is the default.

Prefer extending the repository's current package-management approach rather
than migrating tools unless the user asks for a change.

## Scope Boundaries

This skill is primarily about language-managed projects:

- Python packaging and environments;
- R environments and package-oriented project structure;
- Julia environments and module/package layout;
- the boundary between reusable code, scripts, notebooks, and data artifacts.

It is not primarily about:

- compiler or linker configuration;
- cluster module systems beyond recording relevant environment facts;
- experiment metadata capture beyond what is needed to recreate an environment.

## Preferred Defaults

- Prefer one primary dependency-management path per repository.
- Prefer checked-in metadata over undocumented setup commands.
- Prefer isolated environments over global user installs.
- Prefer explicit optional dependency groups for docs, tests, profiling, or
  development tools.
- Prefer layouts that make imports stable and tests easy to run.

For Python-heavy work, read `references/python-projects.md` for concrete
defaults and examples.

## Python Defaults

- Prefer `pyproject.toml` as the canonical project metadata entry point.
- Prefer a `src/` layout when the project is intended to be imported as a
  package.
- Prefer editable installs for active development rather than manipulating
  `PYTHONPATH`.
- Prefer one environment tool chosen explicitly by the repository such as
  `mamba`/`conda`, `uv`, `pip` plus `venv`, or `poetry`.
- Prefer `mamba` or another conda-compatible solver when the Python stack also
  depends on non-Python libraries such as BLAS, MPI, HDF5, CUDA, or vendor math
  libraries that should be managed together with Python packages.
- Prefer extras or dependency groups for `test`, `dev`, `docs`, or `profile`
  dependencies instead of one unstructured dependency list.
- Keep notebooks outside the importable package tree.

Use `references/python-projects.md` when choosing among `mamba`, `uv`, `pip`,
and `poetry`, or when defining a package-oriented layout.

## R Defaults

- Prefer `renv` when environment reproducibility matters.
- Distinguish clearly between one-off analysis scripts and a real R package.
- If the repository exposes reusable analysis functions, consider package-style
  structure rather than keeping all logic in notebooks or flat scripts.
- Keep generated outputs and large datasets outside the package source tree.

Do not add package ceremony to a tiny script-only analysis unless reuse or
distribution actually requires it.

## Julia Defaults

- Prefer checked-in `Project.toml` and `Manifest.toml` for reproducible
  environments.
- Keep reusable code in modules rather than long top-level scripts when the
  project is growing.
- Treat the environment as part of the project, not as an external assumption.
- Separate package code, experiments, and large output artifacts clearly.

## Project Layout

Prefer layouts that make the code's role obvious:

- importable source code in one clear package or module tree;
- tests in a dedicated test directory following repository conventions;
- notebooks in a dedicated `notebooks/` or `analysis/` area;
- scripts or CLIs in a dedicated `scripts/` or package entry-point location;
- data artifacts, caches, and generated outputs outside importable source.

If the project is mostly exploratory, keep the layout lightweight. If it is
used by multiple people or automated systems, prefer stronger package structure.

## Dependencies and Locking

- Keep runtime dependencies separate from developer tooling dependencies.
- Avoid mixing environment bootstrap instructions across multiple tools without
  a clear default.
- If a conda-style environment is the source of truth, keep Python package
  metadata and environment files consistent rather than letting them drift.
- Use lockfiles when the selected tool supports them and the repository needs
  repeatable environments.
- Be explicit about whether dependency versions are minimums, compatible ranges,
  or fully locked.
- Distinguish scientific runtime dependencies from optional accelerators or
  local-only tools.

For scientific projects, document dependencies that materially affect numerical
results or performance, not only import success.

## Notebooks and Scripts

- Keep notebooks as consumers of package code, not the only location of core
  logic.
- Factor reusable functions out of notebooks into importable modules.
- Avoid treating copied notebook cells as the project's API boundary.
- Keep command-line scripts thin when they mostly orchestrate package code.

If a notebook is the only practical interface, still isolate heavy logic in
plain modules where possible so tests and profiling stay feasible.

## Interface With Other Skills

- Use `scientific-build-systems` when native extensions, compilers, or build
  backends need substantial work.
- Use `scientific-testing` for test design and numerical assertions.
- Use `scientific-reproducibility` for run metadata, seeds, and experiment
  provenance beyond environment setup.
- Use `scientific-profiling` when the question is performance diagnosis rather
  than package structure.

## Anti-Patterns

- mixing multiple package managers without naming one source of truth;
- keeping core logic only inside notebooks;
- relying on `PYTHONPATH` hacks or working-directory-sensitive imports;
- global user-level installs as the normal development workflow;
- undeclared dependencies discovered only by import failures;
- package layouts that mix generated outputs into importable source trees.

## Validation Defaults

- Validate the primary install or environment-creation path after changes.
- Run at least one representative import, test, or entry-point command.
- Check that project metadata and lockfiles match the chosen tool.
- State explicitly which toolchain or package-manager paths were not validated.
- Record the environment command users should run first.

## Output Expectations

When using this skill, briefly note:

- which package-management or project-layout files were changed;
- which tool is the repository's default for environments and dependencies;
- whether package structure, extras, or lockfile practices were added or
  clarified;
- which install, import, or test commands were run;
- which environment assumptions remain.
