---
name: scientific-testing
description: Design and implement tests for scientific-computing and HPC
  software, especially when numerical tolerances, reference data, stochastic
  behavior, parallel consistency, and regression protection matter more than
  exact bitwise equality.
---

# Scientific Testing

Use this skill when adding or reviewing tests for scientific, numerical, or
parallel software where correctness must be established with domain-appropriate
checks rather than naive exact equality.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- numerical assertions and tolerance choices;
- regression tests for scientific outputs;
- deterministic and stochastic test design;
- parallel correctness checks;
- lightweight test reporting that explains what was and was not validated.

## When To Use

Use this skill when:

- outputs are floating-point, iterative, or otherwise numerically sensitive;
- the user asks for tests, validation, or regression protection;
- a benchmark or optimization task still needs a correctness backstop;
- serial and parallel implementations should agree within a justified margin;
- exact output equality is unstable or misleading.

Do not use this skill to replace formal verification, large-scale scientific
validation campaigns, or performance benchmarking.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the smallest stable signal that demonstrates correctness.
3. Prefer fast tests that isolate one numerical property at a time.
4. Use exact equality only for inherently discrete outputs.
5. Choose tolerances that reflect the algorithm, scale, and conditioning of the
   problem.
6. State what the test proves and what it does not prove.

Prefer repository-native test runners and layout. Add new test helpers only when
they reduce duplication or clarify numerical intent.

## Test Selection

Prefer a mix of:

- smoke tests for basic execution and output shape;
- regression tests against trusted reference outputs;
- property tests for invariants such as conservation, monotonicity, symmetry,
  or bounded residuals;
- edge-case tests for small inputs, degenerate geometry, empty data, and
  boundary conditions;
- parallel-consistency tests comparing thread counts, schedules, or ranks.

Keep expensive end-to-end cases sparse. Cover most behavior with small,
interpretable inputs.

## Numerical Assertions

- Prefer `abs(a - b) <= atol + rtol * abs(b)` or the testing framework's
  equivalent.
- Use `atol` for quantities expected near zero.
- Use `rtol` when magnitude scales with the input or reference solution.
- Avoid reusing one global tolerance for every variable.
- Tighten tolerances only when the algorithm and platform justify them.
- Loosen tolerances only with a concrete reason such as conditioning,
  non-associative reductions, or vendor-library variation.

When choosing a tolerance, consider:

- floating-point precision;
- accumulation order and reduction structure;
- iterative solver stopping criteria;
- mesh size, discretization error, or sampling noise;
- cross-platform differences from BLAS, MPI, OpenMP, or math libraries.

## Reference Data

- Prefer analytically solvable cases when available.
- Otherwise use trusted baseline outputs generated from a known-good version.
- Record how the reference data was produced.
- Keep reference inputs and outputs small enough for routine test runs.
- Store derived summaries when full outputs are too large, such as norms,
  residuals, checksums, or key observables.

Do not treat a previous buggy implementation as ground truth simply because it
is older.

## Stochastic and Iterative Workloads

- Fix random seeds when the goal is deterministic regression protection.
- When randomness is intrinsic, assert distribution-level or range-based
  properties instead of single exact values.
- For iterative methods, assert convergence behavior, residual thresholds, or
  invariant preservation rather than internal iteration-by-iteration identity.
- If a solver may converge in different iteration counts across platforms, test
  the achieved quality of the solution rather than the exact count alone.

## Parallel Correctness

- Compare serial and parallel outputs on the same input.
- Test more than one thread or rank count when practical.
- Expect small floating-point differences from non-associative reductions.
- Check for invariants that should hold regardless of scheduling.
- Add at least one test designed to catch partitioning or halo-exchange errors
  when the code is domain-decomposed.

If bitwise reproducibility is a user requirement, treat it as a separate goal
and document the runtime and compiler constraints needed to maintain it.

## Anti-Patterns

- exact equality for generic floating-point arrays without justification;
- tolerances so loose that major regressions still pass;
- tests that only check that a file exists;
- benchmarking without a correctness guardrail;
- asserting implementation details instead of scientific properties;
- large golden files with no provenance.

## Validation Defaults

- Run the smallest relevant test slice first before broader suites.
- Prefer framework-native assertions over hand-rolled comparison code.
- When a tolerance is non-obvious, explain it in the test or commit message.
- If a test is flaky, identify whether the cause is randomness, concurrency, I/O,
  or an invalid assertion before widening the tolerance.
- Prefer CI-friendly tests that finish quickly and avoid machine-specific
  assumptions unless the repository explicitly supports heavier validation tiers.
- State explicitly which test commands were run and which could not be run.

## Framework Patterns

For Python, prefer `pytest` with `pytest.approx` or `numpy.testing` helpers.

For C++, prefer the repository's existing framework. When options are open,
Google Test with helper functions for vector, norm, or residual checks is a
practical default.

For CMake-based projects, prefer registering tests with `ctest` when that is the
existing project pattern.

For array-style comparisons, prefer norms or elementwise comparisons with clear
absolute and relative tolerances instead of custom loops unless the framework
is unavailable.

## Output Expectations

When using this skill, briefly note:

- what numerical property or invariant each added test checks;
- how tolerances or acceptance criteria were chosen;
- whether reference data, seeds, or parallel comparisons were used;
- which validation commands were run;
- which correctness risks remain untested.
