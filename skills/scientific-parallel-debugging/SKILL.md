---
name: scientific-parallel-debugging
description: Debug parallel scientific-computing and HPC software, especially
  when races, deadlocks, nondeterminism, halo-exchange mistakes, load imbalance,
  affinity issues, or serial-versus-parallel correctness drift must be isolated
  and explained.
---

# Scientific Parallel Debugging

Use this skill when debugging scientific, numerical, or parallel software where
failures depend on thread count, rank count, scheduling, communication, or
runtime placement rather than purely serial logic.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- isolating parallel-only correctness failures;
- debugging thread, task, OpenMP, or MPI behavior;
- separating communication, synchronization, and numerical drift issues;
- reporting actionable root-cause hypotheses instead of vague nondeterminism.

## When To Use

Use this skill when:

- the bug appears only with multiple threads, tasks, or ranks;
- serial and parallel results diverge unexpectedly;
- the program hangs, deadlocks, or stalls under parallel execution;
- output depends suspiciously on scheduling, affinity, or launch configuration;
- race conditions, halo exchanges, reductions, or partitioning logic are suspect.

Do not use this skill as a substitute for general serial debugging when the bug
does not depend on parallel execution.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Reduce the failure to the smallest thread or rank count that still reproduces it.
3. Compare serial and parallel behavior on the same input.
4. Change one dimension at a time: threads, ranks, affinity, schedule, or input.
5. Distinguish crash, hang, wrong answer, and performance-pathology cases.
6. State what is observed, what is inferred, and what remains unverified.

Prefer reproducible minimal cases over large production runs while debugging.

## Common Failure Classes

Look for:

- data races and unsafely shared state;
- deadlocks, missed notifications, or mismatched barriers;
- reduction mistakes and non-associative drift beyond expected roundoff;
- halo or ghost-cell exchange errors;
- partitioning and boundary-condition mistakes;
- rank- or thread-local initialization mismatches;
- affinity, oversubscription, or placement-induced misbehavior.

Parallel bugs often combine logic, runtime, and numerical effects.

## Reproduction Strategy

- Start from a known-good serial baseline.
- Reproduce on the smallest input that still exercises the bug.
- Sweep low thread or rank counts before testing larger scales.
- Record launch commands and environment variables exactly.
- Prefer deterministic seeds and stable inputs while isolating the issue.

If the bug disappears under logging or debugging, say so explicitly and treat
that as a clue rather than a contradiction.

## Wrong-Answer Debugging

- Compare serial and parallel outputs at multiple granularities.
- Check whether divergence starts at boundaries, reductions, or exchanged data.
- Validate invariants such as conservation, positivity, or residual behavior.
- Distinguish acceptable reduction-order roundoff from real algorithmic drift.
- Inspect data ownership and update ordering before widening tolerances.

Wrong answers in parallel code are often communication or ownership bugs before
they are "just floating-point noise."

## Hangs and Deadlocks

- Check for mismatched send/receive patterns, collectives, or barriers.
- Look for code paths where one rank or thread can skip required synchronization.
- Inspect lock acquisition order and nested critical sections.
- Reduce concurrency to the smallest case that still hangs.
- Use timeouts, progress logging, or coarse checkpoints to locate the stall.

A hang is usually easier to localize when you first determine which participant
stops making forward progress.

## OpenMP and Threading Issues

- Review shared versus private data clauses carefully.
- Check reductions, `nowait` regions, task dependencies, and loop schedules.
- Test whether `OMP_NUM_THREADS=1` matches the serial code path.
- Record `OMP_NUM_THREADS`, `OMP_PROC_BIND`, `OMP_PLACES`, and any runtime
  affinity settings.
- Watch for false sharing, oversubscription, and thread-unsafe library calls.

Thread count changes that alter correctness often point to hidden shared state.

## MPI and Distributed Issues

- Verify message sizes, tags, communicators, and collective participation.
- Check decomposition logic and off-by-one errors at subdomain boundaries.
- Confirm that all ranks agree on global dimensions and iteration structure.
- Separate communication bugs from local-kernel bugs by validating local states
  before and after exchange points.
- Treat rank-dependent file I/O and restart logic as potential correctness
  hazards, not just infrastructure details.

## Affinity and Runtime Configuration

- Record launcher arguments, rank counts, thread counts, and placement settings.
- Test whether binding, rank mapping, or oversubscription changes the failure.
- Distinguish correctness bugs from performance-sensitive scheduling behavior.
- Expect shared cluster environments to amplify timing-sensitive issues.

Runtime configuration is part of the bug report, not just execution trivia.

## Useful Tools

Useful tools for this skill include:

- `gdb` or `lldb` for process-level debugging;
- `valgrind` tools when slowdown is acceptable;
- compiler sanitizers such as ThreadSanitizer or AddressSanitizer when
  supported by the toolchain and runtime;
- MPI launcher options and runtime diagnostics;
- strategic logging with rank or thread identifiers;
- `perf` or profiler support only when a stall or slowdown may hide the bug.

Choose the lightest tool that can confirm or refute the current hypothesis.

## Anti-Patterns

- debugging only at large scale when the bug reproduces at small scale;
- widening tolerances before checking communication or ownership logic;
- assuming nondeterminism means the bug is impossible to localize;
- changing thread and rank counts at the same time during diagnosis;
- ignoring environment variables and launcher configuration in bug reports;
- treating a hang as a performance issue without first finding the blocked phase.

## Output Expectations

When using this skill, briefly note:

- what parallel configuration reproduces the issue;
- whether the failure is a crash, hang, wrong answer, or configuration-sensitive
  pathology;
- which thread, rank, reduction, exchange, or synchronization hypotheses were
  tested;
- what observations support the leading diagnosis;
- which uncertainty remains and what next isolation step is most justified.
