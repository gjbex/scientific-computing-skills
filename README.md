# Scientific Computing Skills

`scientific-computing-skills` is a Codex plugin distribution for reusable
scientific-software engineering workflows. It packages focused skills for
building, testing, profiling, benchmarking, documenting, and reviewing
scientific and HPC-oriented codebases.

The package intentionally excludes site-specific HPC operations such as cluster
login setup, Slurm account handling, site filesystems, and probe submission
workflows. Those belong in a separate HPC operations skill package.

## Included Skills

- `scientific-build-systems`: build-system configuration, compiler warnings,
  build types, sanitizers, dependencies, and portable CMake-style workflows.
- `scientific-ci`: CI design for scientific projects, including compiler
  coverage, numerical validation, artifacts, and cost-aware matrices.
- `scientific-cli-benchmark`: repeatable command-line benchmarking for serial,
  threaded, and HPC workloads.
- `scientific-cli-design`: batch-friendly command-line interfaces,
  configuration behavior, validation, logging, and output conventions.
- `scientific-code-style`: reusable coding and validation defaults for
  scientific-computing repositories when project guidance is minimal.
- `scientific-container-workflows`: Apptainer-first scientific container
  workflows, with Docker or Podman as local options and HPCCM recipes as the
  preferred source of truth for non-trivial definition files.
- `scientific-data-analysis-and-visualization`: language-agnostic guidance for
  defensible scientific analysis, figures, tables, summaries, uncertainty,
  comparisons, and reproducible analysis artifacts.
- `scientific-data-management`: scientific data boundaries, reference
  fixtures, generated outputs, checksums, provenance, large artifacts, Git
  hygiene, and optional DVC usage.
- `scientific-documentation`: user and developer documentation for algorithms,
  assumptions, parameters, workflows, reproducibility, and performance context.
- `scientific-io-and-data-formats`: scientific file layout, metadata,
  checkpointing, portability, reproducibility, and I/O performance tradeoffs.
- `scientific-numerics-review`: numerical stability, conditioning,
  convergence, tolerances, invariants, and scientific correctness risks.
- `scientific-notebook-workflows`: reproducible scientific notebook workflows,
  including output policy, CI smoke checks, reusable logic, and intentional
  report/demo notebooks with committed outputs.
- `scientific-package-management`: Python-first scientific package layout and
  environment management, with lighter guidance for R and Julia projects.
- `scientific-parallel-debugging`: debugging races, deadlocks,
  nondeterminism, halo exchange, load imbalance, and serial/parallel drift.
- `scientific-performance-portability`: preserving performance across
  compilers, CPUs, node layouts, and cluster environments.
- `scientific-profiling`: profiling CPU, memory, cache, synchronization,
  vectorization, scaling, and Python/native numerical workloads.
- `scientific-release-and-publication`: public release preparation, versioning,
  citation metadata, DOI workflows, release notes, artifact hygiene, and
  publication-ready repository checks.
- `scientific-reproducibility`: capturing seeds, environments, toolchains,
  inputs, configs, and run metadata needed for repeatable results.
- `scientific-review`: broad scientific-code and repository review for
  correctness, validation, reproducibility, performance, documentation, and
  release-readiness risks.
- `scientific-testing`: numerical, stochastic, regression, and
  parallel-consistency tests for scientific software.
- `scientific-workflow-automation`: Nextflow-first workflow automation for
  reproducible multi-step scientific pipelines that should scale from laptops
  to HPC clusters or cloud executors.

## Support Skills

- `git-refactor-hygiene`: use when scientific-computing work involves moving,
  renaming, or reorganizing tracked files so Git history and staging stay
  clean.
- `project-repository-setup`: use when scientific-computing work needs a sane
  repository baseline, including layout, root-file hygiene, local validation
  commands, pre-commit hooks, and CI alignment.

## Skill Boundary Guide

Use `scientific-testing` for correctness tests and regression protection.
Use `scientific-cli-benchmark` for measured runtime comparisons.
Use `project-repository-setup` for baseline local hooks, repository layout, and
local command entry points. Use `scientific-ci` for CI job design and GitHub
Actions workflow details.
Use `scientific-profiling` when benchmark results need root-cause diagnosis.
Use `scientific-data-analysis-and-visualization` when scientific outputs need
defensible figures, tables, summaries, uncertainty handling, or comparison
reports.
Use `scientific-data-management` when raw data, processed data, fixtures,
generated outputs, large artifacts, checksums, or DVC boundaries need to be
made explicit.
Use `scientific-numerics-review` for mathematical and floating-point risks.
Use `scientific-notebook-workflows` when notebooks need reproducibility,
reviewable output policy, CI smoke checks, or intentional report/demo outputs.
Use `scientific-performance-portability` when an optimization must generalize
beyond one machine or compiler.
Use `scientific-release-and-publication` when a repository is being prepared
for public release, citation, archival, or DOI-backed reuse.
Use `scientific-reproducibility` when results need to be rerunnable and
auditable.
Use `scientific-review` for broad scientific repository or pull-request
reviews. Use `scientific-numerics-review` for deeper numerical stability,
convergence, and tolerance concerns.
Use `scientific-container-workflows` when a scientific runtime needs portable
container recipes, especially for Apptainer/Singularity on HPC systems.
Use `scientific-workflow-automation` when ad hoc shell steps should become a
version-controlled workflow, with Nextflow as the preferred default for
multi-step pipelines.

## Layout

```text
scientific-computing-skills/
  .codex-plugin/plugin.json
  skills/
    git-refactor-hygiene/
      SKILL.md
    project-repository-setup/
      SKILL.md
    scientific-*/
      SKILL.md
```

## Installation

Clone the plugin into the standard local plugin directory:

```bash
mkdir -p ~/plugins
git clone https://github.com/gjbex/scientific-computing-skills.git \
  ~/plugins/scientific-computing-skills
```

Create or update the personal Codex marketplace entry:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/create_basic_plugin.py \
  scientific-computing-skills \
  --path ~/plugins \
  --with-marketplace \
  --force
```

Install the plugin from the personal marketplace:

```bash
codex plugin add scientific-computing-skills@personal
```

Start a new Codex thread after installation so the newly installed skills are
available in the session.

## Updating

Update the local checkout:

```bash
git -C ~/plugins/scientific-computing-skills pull --ff-only
```

Refresh the plugin version cachebuster and reinstall from the personal
marketplace:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/update_plugin_cachebuster.py \
  ~/plugins/scientific-computing-skills

codex plugin add scientific-computing-skills@personal
```

Start a new Codex thread after reinstalling.

## Validation

Validate the plugin manifest with:

```bash
python3 tools/validate_plugin.py .
```

Validate bundled skills with:

```bash
python3 tools/validate_skills.py skills
```

Compile bundled Python scripts:

```bash
python3 -m py_compile skills/scientific-cli-benchmark/scripts/simple_benchmark.py
```

See `CONTRIBUTIONS.md` for contribution scope, repository hygiene, and pull
request expectations.

## Publication Notes

This project is licensed under the Apache License, Version 2.0. Redistributed
copies and derivative distributions must preserve the license and attribution
notices required by that license, including the notices in `NOTICE` where
applicable.

If you use this project or derive work from it, please cite it using the
metadata in `CITATION.cff`.
