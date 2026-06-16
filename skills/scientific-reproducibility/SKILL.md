---
name: scientific-reproducibility
description: Improve reproducibility for scientific-computing and HPC workflows,
  especially when runs depend on seeds, environments, toolchains, input sets,
  configuration files, or experiment metadata that must be captured to make
  results repeatable and auditable.
---

# Scientific Reproducibility

Use this skill when editing or reviewing scientific, numerical, or parallel
software where results must be reproducible across reruns, machines, or
collaborators.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- capturing the information needed to reproduce a run;
- separating scientific outputs from run metadata and environment details;
- reducing accidental nondeterminism in experiments and validation workflows;
- reporting what was controlled, what was recorded, and what still varies.

## When To Use

Use this skill when:

- the user asks to make experiments or validation runs reproducible;
- benchmark or profiling results should be traceable to exact inputs and builds;
- random seeds, configuration files, or solver settings affect results;
- outputs depend on toolchain, libraries, hardware, or runtime placement;
- the repository lacks a consistent run-recording convention.

Do not use this skill as a substitute for correctness testing or for deep
environment packaging work beyond the repository's actual needs.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the smallest set of metadata required to reproduce the result.
3. Prefer explicit inputs, configuration, and seeds over hidden defaults.
4. Separate immutable artifacts from transient logs and scratch files.
5. Record environment and toolchain facts that materially affect outcomes.
6. State clearly what is reproducible, to what level, and under what assumptions.

Prefer lightweight, repository-native mechanisms before introducing heavier
experiment-management infrastructure.

## What To Capture

At minimum, consider recording:

- command line and subcommands used;
- input file names or dataset identifiers;
- configuration files and relevant parameter values;
- random seeds or deterministic-mode settings;
- code version such as commit hash or dirty-tree status;
- compiler, interpreter, or toolchain version when it affects behavior;
- key runtime environment variables;
- output locations and artifact names.

Capture only what materially affects rerunning or interpreting the result.

## Determinism and Seeds

- Fix random seeds when exact reruns matter.
- If multiple random streams exist, record all seed sources, not just one.
- Prefer exposing seed control through CLI flags or config rather than hidden
  constants.
- When strict determinism is impossible or too expensive, document the expected
  variability and acceptance criteria.

Do not claim reproducibility if the workflow still depends on unrecorded
randomness or scheduling-sensitive behavior.

## Environment and Toolchain

- Record compiler, MPI, BLAS, Python, or other major dependency versions when
  they materially affect outputs or performance.
- Note machine or node characteristics when hardware changes interpretation,
  especially for benchmarking and profiling.
- Record important runtime settings such as `OMP_NUM_THREADS`,
  `OMP_PROC_BIND`, affinity, rank counts, or precision modes.
- Distinguish environment facts that affect correctness from those that affect
  only performance.

For HPC workflows, expect cluster modules, scheduler settings, and launcher
arguments to matter.

## Inputs, Config, and Artifacts

- Keep configuration in explicit files or structured arguments when practical.
- Prefer stable, human-readable metadata formats unless the repository already
  uses something else.
- Keep generated artifacts organized by run or experiment identifier.
- Avoid overwriting prior outputs without a clear reason.
- Store summaries or hashes when full outputs are too large for routine review.

If a run consumes external data, record where that data came from and which
version or snapshot was used.

## Benchmarking and Performance Context

- Tie runtime results to the exact build, input, placement, and environment.
- Record thread counts, rank counts, and affinity settings with every reported
  timing.
- Separate scientific-result reproducibility from performance reproducibility.
- Expect low-level timing variation even when the command and environment match.

For performance work, reproducible setup is often more realistic than identical
wall-clock numbers.

## Practical Patterns

- Add a run manifest, metadata file, or structured log for key experiments.
- Stamp outputs with version and parameter metadata when that does not create
  clutter.
- Expose configuration through checked-in config files for important workflows.
- Prefer deterministic test fixtures and small reproducible benchmark inputs.
- Keep one obvious command path for rerunning a published example or regression.

## Anti-Patterns

- undocumented default parameters;
- results reported without command lines or input provenance;
- hidden machine-local paths inside scripts or configs;
- claiming exact reproducibility when only approximate reproducibility exists;
- overwriting artifacts in place without preserving run context;
- mixing scratch data and important outputs in the same opaque directory.

## Validation Defaults

- Rerun at least one representative workflow from recorded inputs and metadata.
- Verify that the recorded command and configuration are sufficient to rerun it.
- Check that required files live in stable locations or are described clearly.
- State explicitly what could not be reproduced in the current environment.
- If deterministic reruns are not expected, validate the allowed variation.

## Output Expectations

When using this skill, briefly note:

- what metadata or manifesting mechanism was added or updated;
- which inputs, seeds, versions, and environment details are now captured;
- whether reproducibility is exact, bounded, or approximate;
- which rerun or validation steps were executed;
- which external dependencies or environment assumptions remain.
