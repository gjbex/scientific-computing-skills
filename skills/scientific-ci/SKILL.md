---
name: scientific-ci
description: Design and maintain continuous-integration workflows for
  scientific-computing and HPC software, especially when build matrices,
  compiler warnings, numerical validation, artifacts, and pragmatic test
  selection must balance confidence, cost, and portability.
---

# Scientific CI

Use this skill when editing or reviewing CI configuration for scientific,
numerical, or parallel software where automated checks must validate builds,
tests, and workflow integrity without assuming a full HPC environment.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- build and test workflows in scientific repositories;
- compiler and platform coverage that catches meaningful regressions;
- CI-friendly validation for numerical and parallel code;
- artifact and log handling that helps diagnose failures efficiently.

## When To Use

Use this skill when:

- the user asks to add or improve CI for a scientific project;
- build or test coverage is inconsistent across compilers or configurations;
- numerical regressions should be caught automatically;
- sanitizers, warnings, or linting should run in a controlled way;
- documentation, examples, or reproducibility paths need automated smoke checks.

Do not use this skill to assume that CI should replicate a full cluster or
production environment when the repository only needs practical automated
coverage.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the smallest CI set that catches the most likely regressions.
3. Separate fast required checks from slower or more environment-specific ones.
4. Prefer reproducible commands already used locally by the repository.
5. Keep matrix size proportional to actual risk and maintenance cost.
6. State what CI validates, what it deliberately skips, and what remains manual.

Prefer extending the repository's current CI system rather than introducing a
second workflow layer without clear value.

## Core Coverage

Scientific CI usually benefits from some combination of:

- at least one clean configure and build path;
- automated tests or validation commands;
- warning-clean builds where practical;
- documentation or example smoke checks when examples are important;
- one stricter path such as sanitizers, static analysis, or an additional
  compiler.

The goal is confidence per minute, not maximal job count.

## Build Matrix Guidance

- Start with one primary compiler and one representative build mode.
- Add a second compiler when toolchain diversity regularly reveals defects.
- Use separate jobs for debug-like validation and release-like build assurance.
- Keep optional accelerators or heavyweight dependencies out of the default path
  unless they are central to the project.
- Avoid exploding the matrix across every compiler, OS, and dependency version
  unless the repository genuinely supports them all.

For scientific code, compiler diversity is often more valuable than broad OS
fan-out.

## Numerical and Scientific Validation

- Prefer small, deterministic tests that still exercise meaningful scientific
  behavior.
- Use tolerances and acceptance criteria that match the algorithm.
- Keep large reference datasets out of the default CI path unless they are
  unavoidable.
- Distinguish correctness checks from performance checks.
- If exact reproducibility is not expected, document the allowed variation.

CI should catch real scientific regressions without becoming flaky.

## Parallel and HPC Concerns

- Keep CI parallel tests modest in scale and resource assumptions.
- Use low-rank or low-thread-count checks to catch obvious parallel defects.
- Avoid assuming specialized interconnects, filesystems, or schedulers in
  general-purpose CI runners.
- Treat MPI, OpenMP, and thread-affinity checks as smoke coverage unless the
  environment supports more.
- Mark cluster-only validation separately from standard CI.

CI should validate portability and basic correctness, not pretend to be a full
performance lab.

## Warnings, Sanitizers, and Analysis

- Include a warning-focused build when warnings are part of project policy.
- Add sanitizer jobs as opt-in or non-default required checks when runtime cost
  is acceptable.
- Keep stricter analysis paths isolated so failures are easy to interpret.
- Prefer one or two well-maintained strict jobs over many rarely trusted ones.

If a job is noisy or flaky, fix the cause or narrow its scope rather than
teaching people to ignore it.

## Artifacts and Diagnostics

- Upload logs, test reports, or small failure artifacts when they aid triage.
- Prefer compact machine-readable outputs when tooling already supports them.
- Preserve enough context to debug a failure without rerunning blindly.
- Avoid artifact sprawl that nobody inspects.

Artifacts should reduce diagnosis time, not just consume storage.

## Performance and Benchmark Checks

- Keep full benchmarks out of default CI unless the repository has stable,
  meaningful performance gates.
- Prefer performance smoke tests or regression sentinels only when variance is
  controlled.
- Record environment assumptions clearly if any timing-based check exists.

Most scientific repositories should separate CI correctness from serious
benchmarking.

## Reproducibility and Documentation Hooks

- Run documented build or example commands when those paths are part of normal
  user workflows.
- Prefer checked-in configs or scripts over ad hoc command duplication in CI.
- Ensure CI commands align with the repository's published instructions.

When examples or docs drift from the code, CI is a useful backstop.

## Anti-Patterns

- CI matrices so large that failures are ignored;
- performance gates on unstable runners;
- tests that require hidden external data or machine-local paths;
- warning or sanitizer jobs that are permanently red;
- duplicating local build logic in CI instead of reusing scripts or presets;
- assuming cluster-specific infrastructure in generic hosted CI.

## Validation Defaults

- Run the smallest affected workflow locally when practical before editing CI.
- Validate CI syntax or configuration structure if tooling is available.
- Confirm that referenced scripts, presets, and paths exist.
- State explicitly which CI paths were tested locally and which were not.
- If jobs could not be exercised end-to-end, say what remains unverified.

## Output Expectations

When using this skill, briefly note:

- which CI files or jobs were added or changed;
- which build, test, or analysis paths are now covered;
- whether matrix, sanitizer, artifact, or documentation checks were introduced;
- which workflow commands were validated locally;
- which portability, flakiness, or environment risks remain.
