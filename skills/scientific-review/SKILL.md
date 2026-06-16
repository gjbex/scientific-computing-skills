---
name: scientific-review
description: Review scientific-computing repositories, pull requests, or code
  changes for correctness, validation, reproducibility, maintainability,
  documentation, and performance risks beyond ordinary software review.
---

# Scientific Review

Use this skill when reviewing scientific-computing code, repositories, pull
requests, or design changes where the main goal is to identify scientific,
engineering, reproducibility, and maintainability risks.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for reviewing:

- scientific correctness and assumption risks;
- missing or weak validation;
- reproducibility and provenance gaps;
- performance, portability, and scalability side effects;
- documentation and usability gaps;
- repository hygiene and release-readiness issues.

## When To Use

Use this skill when:

- the user asks for a review of a scientific repository, PR, or code change;
- changes affect scientific results, validation, performance, or workflow
  behavior;
- the review needs to prioritize actionable risks over style preferences;
- ordinary software review would miss domain-specific reproducibility or
  scientific-correctness concerns;
- a broad review is needed before choosing narrower skills.

Use `scientific-numerics-review` instead when the task is specifically about
floating-point behavior, numerical stability, convergence, tolerances,
conditioning, or mathematical invariants.

## Review Mindset

Findings come first. Prioritize concrete bugs, regressions, missing validation,
scientific correctness risks, and release-blocking ambiguity. Keep summaries
secondary.

Prefer evidence-backed findings with file and line references. Distinguish
confirmed defects from plausible risks and open questions.

Do not turn a scientific review into a broad style cleanup unless style directly
affects correctness, maintainability, or reproducibility.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the scientific purpose, expected outputs, and validation contract.
3. Inspect changed code, tests, documentation, and workflow entry points
   together.
4. Review correctness and validation before style and polish.
5. Check whether results can be reproduced from documented inputs and commands.
6. Report findings ordered by severity, then residual risks and test gaps.

For PR review, focus on the diff and nearby affected code. For repository
review, identify the highest-risk workflows rather than trying to inspect
everything equally.

## Review Areas

### Scientific Correctness

- Are assumptions, units, coordinate systems, dimensions, and conventions clear?
- Do outputs match the stated scientific quantity or claim?
- Are edge cases, invalid inputs, and boundary conditions handled deliberately?
- Are approximations or model limitations documented where users need them?
- Could a code change silently alter scientific interpretation?

Use `scientific-numerics-review` for deeper numerical analysis when needed.

### Validation and Tests

- Are there tests for the most important scientific behavior?
- Do tests use meaningful tolerances and reference data?
- Is there coverage for small examples, edge cases, stochastic behavior, and
  parallel consistency where relevant?
- Are benchmark or optimization changes protected by correctness checks?
- Are large or expensive validations separated from fast smoke tests?

Tests should explain what scientific behavior they protect, not only exercise
code paths.

### Reproducibility

- Can a user rerun the documented workflow from checked-in instructions?
- Are inputs, parameters, random seeds, environment details, and versions
  captured when they matter?
- Are generated outputs separated from source and traceable to commands?
- Is dirty-tree or commit information recorded for reported results?
- Are notebooks, scripts, and workflow engines using the same source of truth?

Use `scientific-reproducibility` for implementation work on run metadata and
rerun contracts.

### Performance and Portability

- Does a performance change preserve correctness?
- Does an optimization overfit to one CPU, compiler, GPU, dataset, filesystem,
  or scheduler configuration?
- Are thread counts, MPI ranks, affinity, memory use, and I/O behavior handled
  explicitly where they affect results?
- Are fallback paths maintained for non-ideal hardware or missing accelerators?
- Are benchmark claims supported by reproducible measurements?

Use `scientific-profiling`, `scientific-cli-benchmark`, or
`scientific-performance-portability` for deeper follow-up.

### Workflow and Repository Structure

- Are build, test, run, and validation commands discoverable?
- Are CI and local commands aligned?
- Are generated files, caches, and large artifacts kept out of source layout?
- Are dependency and container boundaries explicit?
- Are workflow orchestration files separated from scientific implementation
  logic?

Use `project-repository-setup`, `scientific-workflow-automation`, or
`scientific-container-workflows` for implementation work.

### Documentation and Release Readiness

- Does the README explain purpose, installation, a minimal run, validation, and
  expected outputs?
- Are assumptions, input formats, output formats, and limitations documented?
- Is citation, license, and attribution metadata present when public reuse is
  expected?
- Are private hostnames, local paths, credentials, or site-specific details
  absent from public materials?
- Are examples small, runnable, and consistent with current code?

Use `scientific-documentation` or `scientific-release-and-publication` for
follow-up edits.

## Severity Guidance

Treat as high severity:

- wrong scientific results or silent result corruption;
- tests that pass while validating the wrong quantity;
- irreproducible published or release-critical results;
- performance changes that break correctness or portability guarantees;
- public release artifacts containing secrets or private infrastructure details.

Treat as medium severity:

- missing validation for important behavior;
- unclear assumptions that could lead users to misuse results;
- fragile workflow or environment dependencies;
- documentation that prevents correct installation or rerun.

Treat as low severity:

- style or naming issues that do not affect correctness;
- documentation polish;
- optional cleanup that does not block reliable use.

## Anti-Patterns

- listing style nits before correctness findings;
- claiming a result is valid without checking the validation path;
- treating a successful benchmark as proof of scientific correctness;
- ignoring documentation and workflow files in scientific review;
- failing to distinguish confirmed bugs from plausible risks;
- asking for broad rewrites when a narrow fix would address the risk.

## Output Expectations

When using this skill for a review:

- list findings first, ordered by severity;
- include file and line references where possible;
- explain why each finding matters scientifically or operationally;
- include open questions or assumptions after findings;
- summarize residual risks or missing validation even if no findings are found.

If no findings are discovered, say so explicitly and state what was not
validated.
