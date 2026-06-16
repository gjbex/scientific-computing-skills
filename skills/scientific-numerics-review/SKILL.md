---
name: scientific-numerics-review
description: Review scientific-computing and HPC code for numerical stability,
  conditioning, convergence logic, tolerance choices, invariants, and
  scientifically meaningful correctness risks that ordinary software review may
  miss.
---

# Scientific Numerics Review

Use this skill when reviewing or changing scientific, numerical, or parallel
code where the main risk is not syntax or style, but mathematically unsound or
scientifically misleading behavior.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for reviewing:

- floating-point-sensitive computations;
- iterative methods and convergence criteria;
- discretizations, approximations, and conservation properties;
- tolerance choices and error metrics;
- changes that may alter scientific meaning without obviously breaking the code.

## When To Use

Use this skill when:

- the user asks for a review of numerical or scientific code;
- a solver, integrator, optimizer, or reduction path is being changed;
- tolerances, stopping conditions, or precision choices are being modified;
- performance work may have changed numerical behavior;
- results drift and it is unclear whether the change is acceptable.

Do not use this skill as a substitute for full mathematical verification or
domain-specific theoretical review beyond what the code and task require.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the numerical quantity or scientific claim the code is meant to preserve.
3. Review algorithmic assumptions before line-level style details.
4. Distinguish implementation noise from scientifically meaningful result drift.
5. Prefer concrete failure modes over vague statements about instability.
6. State what is known, what is inferred, and what would need stronger validation.

Prefer findings that connect code changes to likely numerical consequences.

## Core Review Questions

Ask questions such as:

- Is the computation stable for the expected input range?
- Is the problem well-conditioned enough for the chosen method and precision?
- Are stopping criteria tied to meaningful error or residual measures?
- Are tolerances justified by scale, conditioning, or discretization error?
- Does the code preserve known invariants, bounds, or monotonic properties?
- Could reordering operations materially change the result?
- Is the reported metric aligned with the actual scientific objective?

## Floating-Point Risks

Review for:

- catastrophic cancellation;
- loss of significance in subtraction of near-equal values;
- unstable summation or reduction order;
- overflow or underflow risks;
- avoidable conversion between precisions;
- hidden dependence on exact equality of floating-point values.

Parallel reductions, vectorization, and compiler optimization can change
operation order enough to expose these issues.

## Convergence and Stopping Logic

- Check whether residuals, errors, or objective changes are the right stopping
  signal.
- Distinguish absolute and relative stopping criteria.
- Ensure the chosen norm or metric matches the mathematical claim.
- Review maximum-iteration fallbacks and non-convergence handling.
- Be cautious when iteration count is treated as a quality measure by itself.

A solver that stops consistently is not necessarily a solver that stops
correctly.

## Tolerances and Error Metrics

- Review whether tolerances scale with the problem and quantity being measured.
- Avoid one global tolerance for unrelated variables without justification.
- Distinguish discretization error, solver error, and floating-point noise.
- Check whether comparisons near zero use an appropriate absolute tolerance.
- Treat unexplained tolerance widening as a likely defect until justified.

Tolerance choices should reflect the mathematics of the problem, not only the
desire to pass tests.

## Discretization and Invariants

- Check whether discrete operators are consistent with the intended model.
- Review boundary-condition handling and edge-cell logic carefully.
- Look for violated conservation, symmetry, positivity, monotonicity, or mass
  balance properties when those should hold.
- Treat indexing changes, halo logic, and stencil rewrites as numerically
  significant even when they look mechanically small.

Small implementation changes can alter the scientific meaning of a method.

## Precision Choices

- Review whether `float`, `double`, or mixed precision is appropriate for the
  algorithm and scale.
- Identify accumulations or solves that may need higher precision than storage.
- Check whether conversions are deliberate and localized.
- Treat precision reductions made for performance as numerically meaningful
  changes, not only engineering optimizations.

## Parallel and Performance-Driven Changes

- Review whether threading, SIMD, fusion, tiling, or reordering changed the
  numerical contract.
- Expect non-associative reductions to produce some drift, but not arbitrary
  drift.
- Distinguish acceptable roundoff variation from evidence of instability.
- Check whether determinism requirements changed silently.

Performance improvements should not quietly rewrite the scientific claim.

## Anti-Patterns

- exact equality reasoning for generic floating-point paths;
- convergence checks that do not reflect solution quality;
- widening tolerances without explaining the source of the drift;
- assuming faster code is equivalent because outputs "look similar";
- treating previous outputs as unquestionable ground truth;
- dismissing all numerical differences as floating-point noise.

## Review Output Style

When this skill is used for review, prioritize:

- concrete numerical risks and likely consequences;
- file and line references when possible;
- clear distinction between confirmed defects, plausible concerns, and open
  questions;
- brief mention of missing validation that would resolve uncertainty.

If no clear findings are present, say so explicitly and mention any residual
numerical risks that remain hard to assess without stronger tests or reference
data.

## Output Expectations

When using this skill, briefly note:

- what numerical quantity, invariant, or convergence behavior was reviewed;
- which risks appear confirmed versus inferred;
- whether precision, reduction order, or tolerance choices are involved;
- what additional tests or reference comparisons would reduce uncertainty;
- which scientific or numerical risks remain open.
