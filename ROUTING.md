# Skill Routing

Use this file to choose the most specific skill for a scientific-computing
task. When multiple skills apply, start with the skill that matches the user's
primary intent, then use secondary skills for follow-up implementation details.

## Quick Router

| User intent | Primary skill |
| --- | --- |
| Review a scientific repository, pull request, or code change broadly | `scientific-review` |
| Review numerical stability, convergence, tolerances, or floating-point behavior | `scientific-numerics-review` |
| Add or review scientific tests and validation cases | `scientific-testing` |
| Collect timing, scaling, or placement measurements | `scientific-cli-benchmark` |
| Diagnose why code is slow | `scientific-profiling` |
| Judge whether an optimization generalizes across machines or compilers | `scientific-performance-portability` |
| Improve GPU or accelerator portability | `scientific-accelerator-portability` |
| Configure CMake, compiler warnings, build types, or sanitizers | `scientific-build-systems` |
| Design or improve CI jobs, matrices, artifacts, or GitHub Actions workflows | `scientific-ci` |
| Design a scientific command-line interface | `scientific-cli-design` |
| Apply coding conventions when repository guidance is absent | `scientific-code-style` |
| Improve README, usage docs, algorithm docs, or workflow docs | `scientific-documentation` |
| Organize Python/R/Julia package metadata and environments | `scientific-package-management` |
| Manage containers, Apptainer/Singularity, Docker/Podman, or HPCCM recipes | `scientific-container-workflows` |
| Turn ad hoc shell steps into a reproducible Nextflow-first workflow | `scientific-workflow-automation` |
| Manage raw data, fixtures, generated outputs, checksums, large artifacts, or DVC | `scientific-data-management` |
| Design file formats, schemas, metadata layout, checkpoints, or I/O paths | `scientific-io-and-data-formats` |
| Analyze results, generate figures/tables, or summarize scientific outputs | `scientific-data-analysis-and-visualization` |
| Maintain notebooks, output policy, notebook CI, or report/demo notebooks | `scientific-notebook-workflows` |
| Make experiments or results rerunnable and auditable | `scientific-reproducibility` |
| Prepare public release, citation metadata, DOI, tags, or release notes | `scientific-release-and-publication` |
| Set up repository baseline, local hooks, layout, and developer commands | `project-repository-setup` |
| Move or rename tracked files while preserving Git history | `git-refactor-hygiene` |

## Boundary Rules

### Review

Use `scientific-review` for broad scientific repository or PR review. Use
`scientific-numerics-review` when the main risk is mathematical or numerical:
stability, conditioning, convergence, tolerances, precision, or invariants.

### Performance

Use `scientific-cli-benchmark` to collect runtime and scaling data. Use
`scientific-profiling` to explain a slowdown or identify bottlenecks. Use
`scientific-performance-portability` to evaluate whether a measured or proposed
optimization will remain robust across compilers, CPUs, node layouts, or
clusters.

### Accelerators

Use `scientific-accelerator-portability` for CUDA, HIP, SYCL, OpenACC, Kokkos,
RAJA, OpenCL, OpenMP offload, GPU containers, device selection, fallback paths,
and accelerator-specific correctness risks.

Use `scientific-performance-portability` for broader non-accelerator
performance portability questions.

### Data and I/O

Use `scientific-data-management` when the question is where data lives, what is
tracked, what is generated, how large artifacts are managed, or whether DVC,
Git LFS, checksums, or external storage are appropriate.

Use `scientific-io-and-data-formats` when the question is how scientific data
should be represented inside files: schema, metadata, checkpoints, HDF5/NetCDF
layout, portability, and I/O performance.

Use `scientific-data-analysis-and-visualization` when the question is how to
turn results into defensible figures, tables, summaries, or comparison reports.

### Reproducibility and Release

Use `scientific-reproducibility` when runs, experiments, benchmarks, or results
need to be rerunnable and auditable.

Use `scientific-release-and-publication` when the repository or artifact is
being prepared for public release, citation, archival, DOI workflows, tags, or
release notes.

### Packaging, Containers, and Workflows

Use `scientific-package-management` for language-level dependency metadata,
virtual environments, `pyproject.toml`, R/Julia project layout, and package
structure.

Use `scientific-container-workflows` for full runtime environments,
Apptainer/Singularity, Docker/Podman, HPCCM-generated definition files, and
container smoke tests.

Use `scientific-workflow-automation` for multi-step scientific pipelines,
especially Nextflow-first workflows that should scale from laptops to HPC or
cloud executors.

### Repository Baseline and CI

Use `project-repository-setup` for repository layout, root-file hygiene,
`.gitignore`, local validation commands, and pre-commit hooks.

Use `scientific-ci` for CI job design, build/test matrices, GitHub Actions,
artifacts, sanitizer jobs, documentation checks, and scientific validation in
CI.

### Notebooks

Use `scientific-notebook-workflows` for notebook structure, output policy,
notebook execution checks, GitHub-preview report/demo notebooks, and factoring
reusable logic out of cells.

Use `scientific-data-analysis-and-visualization` when the main task is
interpreting results or producing figures and tables, even if the current
implementation happens to be in a notebook.

## Out Of Scope For This Package

Site-specific HPC operations are intentionally excluded:

- cluster login setup;
- Slurm account, partition, reservation, or allocation choices;
- queue monitoring and job submission operations;
- shared filesystem quota and site storage discovery;
- cluster-specific probe submission workflows.

Those belong in a separate HPC operations package.
