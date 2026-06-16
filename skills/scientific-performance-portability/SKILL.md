---
name: scientific-performance-portability
description: Review and improve scientific-computing and HPC code so it remains
  performant across compilers, CPUs, node layouts, and cluster environments,
  especially when avoiding one-machine tuning, vendor lock-in, and fragile
  assumptions matters.
---

# Scientific Performance Portability

Use this skill when editing or reviewing scientific, numerical, or parallel
software where the goal is good performance on more than one machine or
toolchain, not maximum tuning for a single host.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- avoiding overfitting to one compiler, CPU, socket topology, or cluster;
- separating portable optimizations from machine-specific tuning;
- reviewing data layout, threading, and vectorization choices for robustness;
- documenting performance assumptions and fallback paths.

## When To Use

Use this skill when:

- the user asks whether an optimization will generalize across machines;
- code is being tuned on one platform but must stay usable elsewhere;
- architecture-specific flags, intrinsics, or affinity assumptions are proposed;
- performance regressions appear only on some compilers or node types;
- fallback behavior for non-ideal hardware needs to be preserved.

Do not use this skill as a substitute for benchmarking or profiling. Use those
skills to measure and diagnose, then use this one to assess portability tradeoffs.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify which performance assumptions are truly portable and which are not.
3. Prefer algorithmic and layout improvements before machine-specific tuning.
4. Keep architecture-specific code behind clear feature checks or options.
5. Preserve a correct, maintainable fallback path.
6. State what hardware/compiler context was considered and what remains untested.

Prefer portable wins first, then isolate unavoidable specialization.

## Portability Questions

Ask questions such as:

- Does this optimization depend on one cache size, vector width, or NUMA layout?
- Will another compiler still optimize this code reasonably?
- Is `-march=native`, a vendor intrinsic, or a runtime binding assumption leaking
  into default behavior?
- Does the code degrade safely when SMT, NUMA, SIMD width, or accelerator support
  differs?
- Is the performance claim tied to one input shape or one machine balance?

## Preferred Optimization Patterns

- Favor better algorithms, reduced memory traffic, and improved locality before
  narrow hardware tuning.
- Prefer data layouts and loop structures that compilers can optimize reliably.
- Use blocking or tiling parameters that can be configured or auto-selected when
  one fixed value is unlikely to fit every platform.
- Keep threading choices explicit and test at more than one core count.
- Separate correctness logic from optimization-specific dispatch when practical.

## Architecture-Specific Code

- Avoid making vendor-specific intrinsics the only implementation path.
- Keep specialized kernels isolated behind capability checks, build options, or
  runtime dispatch.
- Document the baseline path and the specialized path.
- Make sure tests cover both paths when feasible.
- Treat assumptions about alignment, SIMD width, page size, or cache geometry as
  explicit constraints, not implicit truths.

Machine-specific optimization is acceptable when it is opt-in, localized, and
backed by a portable fallback.

## Threading, NUMA, and Placement

- Avoid hardcoding thread counts, socket counts, or rank/thread mappings unless
  the workflow is explicitly machine-specific.
- Prefer exposing placement and thread controls through runtime settings.
- Review whether first-touch, allocation strategy, or memory placement assumptions
  hold on different NUMA systems.
- Expect one "best" affinity policy on one machine to be suboptimal elsewhere.

Portable performance often requires making placement tunable rather than fixed.

## Compiler and Build Concerns

- Avoid relying on one compiler's undocumented optimization behavior.
- Prefer standard language constructs before non-portable extensions.
- Keep architecture-specific flags out of broad default builds.
- Test at least one alternate compiler or build mode when portability is a goal.
- Document any minimum compiler, SIMD, or ISA assumptions introduced by a change.

If the build system already provides opt-in tuning knobs, preserve that structure.

## Measuring Portability

- Compare performance across at least two relevant machine or compiler contexts
  when practical.
- Normalize conclusions by workload size and hardware characteristics.
- Distinguish "slower but acceptable fallback" from "unusable off the tuned
  platform."
- Report exact build flags, runtime settings, and benchmark inputs.

One-machine speedup is not enough evidence for a broadly useful optimization.

## Anti-Patterns

- hardcoding `-march=native` or one CPU's tuning assumptions into defaults;
- deleting a generic implementation after adding one specialized kernel;
- selecting tile sizes, thread counts, or affinity policies that only fit one
  benchmark host;
- assuming benchmark wins on one compiler imply wins everywhere;
- mixing portability-sensitive dispatch logic with core numerical code until it
  becomes hard to maintain.

## Output Expectations

When using this skill, briefly note:

- what performance-portability assumption was reviewed or changed;
- whether the solution is portable by default, specialized behind a guard, or
  machine-specific by design;
- which compiler, hardware, or runtime contexts were considered;
- which measurements or build checks were run;
- which portability risks or untested environments remain.
