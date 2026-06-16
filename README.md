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
- `scientific-documentation`: user and developer documentation for algorithms,
  assumptions, parameters, workflows, reproducibility, and performance context.
- `scientific-io-and-data-formats`: scientific file layout, metadata,
  checkpointing, portability, reproducibility, and I/O performance tradeoffs.
- `scientific-numerics-review`: numerical stability, conditioning,
  convergence, tolerances, invariants, and scientific correctness risks.
- `scientific-package-management`: Python-first scientific package layout and
  environment management, with lighter guidance for R and Julia projects.
- `scientific-parallel-debugging`: debugging races, deadlocks,
  nondeterminism, halo exchange, load imbalance, and serial/parallel drift.
- `scientific-performance-portability`: preserving performance across
  compilers, CPUs, node layouts, and cluster environments.
- `scientific-profiling`: profiling CPU, memory, cache, synchronization,
  vectorization, scaling, and Python/native numerical workloads.
- `scientific-reproducibility`: capturing seeds, environments, toolchains,
  inputs, configs, and run metadata needed for repeatable results.
- `scientific-testing`: numerical, stochastic, regression, and
  parallel-consistency tests for scientific software.

## Skill Boundary Guide

Use `scientific-testing` for correctness tests and regression protection.
Use `scientific-cli-benchmark` for measured runtime comparisons.
Use `scientific-profiling` when benchmark results need root-cause diagnosis.
Use `scientific-numerics-review` for mathematical and floating-point risks.
Use `scientific-performance-portability` when an optimization must generalize
beyond one machine or compiler.
Use `scientific-reproducibility` when results need to be rerunnable and
auditable.

## Layout

```text
scientific-computing-skills/
  .codex-plugin/plugin.json
  skills/
    scientific-*/
      SKILL.md
```

## Validation

Validate the plugin manifest with:

```bash
python3 ~/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

Validate individual skills with:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py \
  skills/scientific-testing
```

## Publication Notes

This project is licensed under the Apache License, Version 2.0. Redistributed
copies and derivative distributions must preserve the license and attribution
notices required by that license, including the notices in `NOTICE` where
applicable.

If you use this project or derive work from it, please cite it using the
metadata in `CITATION.cff`.
