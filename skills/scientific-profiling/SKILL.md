---
name: scientific-profiling
description: Profile scientific-computing and HPC software to identify CPU,
  memory, cache, synchronization, vectorization, and scaling bottlenecks,
  including Python workloads that call numerical libraries or native kernels,
  especially when benchmark results show a slowdown but the root cause is still
  unknown.
---

# Scientific Profiling

Use this skill when investigating why scientific, numerical, or parallel code is
slow and the next step is diagnosis rather than another timing sweep, including
Python pipelines, scripts, and notebooks that drive native numerical code.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- choosing the right profiling method for the performance question;
- distinguishing CPU, memory, I/O, and synchronization bottlenecks;
- interpreting hotspots in serial, threaded, or MPI-style workloads;
- separating Python interpreter overhead from time spent in native extensions;
- reporting actionable findings instead of raw profiler dumps.

## When To Use

Use this skill when:

- benchmark results reveal an unexpected slowdown or scaling limit;
- the user asks where time is going in a solver, kernel, or pipeline;
- a Python workflow is slow and it is unclear whether the cost is in Python
  code, NumPy-style library calls, or native extensions;
- a multithreaded code stops scaling and the cause is unclear;
- cache misses, bandwidth limits, or vectorization efficiency may matter;
- the goal is performance diagnosis, not only runtime measurement.

Do not use this skill as a substitute for correctness testing or for final
benchmark reporting. Use it to explain observed performance behavior.

## Working Approach

When this skill applies:

1. Confirm the target build and command line being profiled.
2. Reproduce the slowdown on a representative but manageable case.
3. Start with the lightest profiler that can answer the question.
4. For Python, first decide whether whole-program, function-level, line-level,
   or memory profiling is needed.
5. Separate collection from interpretation.
6. Prefer one performance question at a time.
7. Report both the hotspot and the likely limiting resource.

Prefer repository-native build and run workflows. Add profiler-specific build
changes only when the existing setup does not already support them.

## Profiling Questions

First decide which question matters most:

- where wall time is spent;
- whether the code is compute-bound or memory-bound;
- whether threading or MPI introduces imbalance or synchronization cost;
- whether vectorization is missing;
- whether I/O, allocation, or setup dominates runtime.

The tool choice should follow the question, not the other way around.

## Tool Selection

Useful tools for this skill include:

- `perf stat` for high-level hardware-counter context;
- `perf record` and `perf report` for Linux CPU hotspot analysis;
- `cProfile` and `pstats` for low-overhead whole-program Python call profiling;
- `py-spy` for sampling Python processes with low intrusion, including
  production-like runs where code changes are undesirable;
- `line_profiler` for line-level Python hotspot analysis after a function-level
  hotspot is already known;
- `scalene` for mixed CPU, native, and memory attribution in Python workloads;
- `tracemalloc` or `memray` for Python allocation and memory-growth diagnosis;
- `valgrind --tool=callgrind` for deterministic call-graph profiling when
  runtime overhead is acceptable;
- `gprof` only for older toolchains or simple CPU-bound code when better tools
  are unavailable;
- compiler vectorization reports for missed SIMD opportunities;
- `time` and lightweight logging when a full profiler is unnecessary;
- MPI or OpenMP runtime summaries when the code already exposes them.

Use hardware-counter and sampling tools first when the workload is large enough
that instrumentation overhead would distort the result.

For Python, prefer this progression:

- `cProfile` for an initial whole-program view when the slowdown is reproducible
  in a local run;
- `py-spy` when sampling an existing process or when instrumentation would be
  too invasive;
- `line_profiler` only after identifying a small set of suspect functions;
- `scalene`, `tracemalloc`, or `memray` when allocation behavior or Python
  versus native time needs to be separated.

For concrete command patterns and quick interpretation notes, see
`references/python-profiling.md`.

## Build Guidance

- Prefer an optimized build for realistic hotspots.
- Keep debug symbols enabled when practical so call stacks are readable.
- Avoid profiling only debug builds unless the release build is unavailable.
- Rebuild with frame pointers or profiler-friendly flags only when the tool
  requires them.
- Document any changes to optimization flags, symbols, or inlining settings.
- For Python, record the interpreter version, environment manager, key package
  versions, and whether major libraries are using optimized native backends.

For CMake-style projects, a practical default is a release-like build with debug
symbols rather than a pure debug build.

For Python projects, prefer the repository's native runner such as
`python -m ...`, `pytest`, `uv run`, or a notebook-exported script rather than
ad-hoc command rewrites that change import or startup behavior.

## Serial Hotspots

- Start with inclusive wall-time hotspots.
- Confirm whether the hottest function is self-time or child-time dominated.
- Distinguish true computation from allocation, dispatch, and conversion work.
- Check whether the hotspot is expected from the algorithm.
- If the top hotspot is surprising, verify that input size and code path are
  representative.

For Python, also distinguish:

- interpreter overhead from time spent inside NumPy, SciPy, PyTorch, or other
  native libraries;
- repeated small allocations, conversions, or dataframe operations from the
  actual numerical kernel;
- import, startup, and JIT warmup costs from steady-state runtime.

## Memory and Cache Behavior

- Use counter data when available to distinguish compute saturation from memory
  stalls.
- Watch for bandwidth saturation, cache-thrashing, poor locality, and excessive
  temporary allocations.
- Relate cache effects to working-set size, tile size, and access pattern.
- Treat sudden performance cliffs as potential cache-capacity or NUMA effects.

If the benchmark skill already established scaling curves, use those results as
context instead of repeating the entire sweep.

## Python-Specific Workflow

If the task is primarily Python performance diagnosis, read
`references/python-profiling.md` for command templates and tool-selection
examples before collecting profiles.

- Start with a representative script entry point rather than an interactive
  notebook cell when possible so runs are reproducible.
- For notebook-heavy workflows, export or factor the slow path into a script or
  module before collecting serious profiles.
- Use `python -m cProfile -o profile.pstats ...` for the first pass when a
  simple call profile is enough.
- Inspect `pstats` output sorted by cumulative time before switching tools.
- Use `py-spy top` or `py-spy record` when you need sampling with minimal code
  changes.
- Add `line_profiler` decorators sparingly and only on already-suspect
  functions.
- Use `scalene` when time may be split across Python, native extensions, and
  memory allocation.
- Use `tracemalloc` or `memray` when memory growth, churn, or unexpected object
  retention is part of the slowdown.

For NumPy-style workloads, check whether vectorized library calls already
dominate runtime before spending time micro-optimizing surrounding Python loops.

## Mixed Python and Native Stacks

- If most time is in compiled libraries, switch from Python profilers to native
  profilers or library-specific diagnostics.
- If profiles show many short Python calls around native kernels, investigate
  batching, vectorization, and data-layout conversions first.
- When Python launches multithreaded native kernels, interpret results in terms
  of both Python overhead and underlying thread or BLAS behavior.
- Be explicit about whether the observed bottleneck is Python code, extension
  code, library dispatch, data movement, or synchronization.

## Threading and Parallel Overheads

- Compare one-thread and many-thread profiles on the same input.
- Look for time lost to barriers, critical sections, reductions, task overhead,
  idle threads, or load imbalance.
- Check whether thread placement or NUMA policy changes the hotspot mix.
- Expect reduction order and scheduling to affect both performance and minor
  floating-point behavior.
- Profile representative thread counts rather than every possible count.

For MPI-style programs, distinguish computation, communication, waiting, and
rank imbalance before optimizing local kernels.

## Vectorization

- Use compiler optimization reports when the question is missed SIMD rather than
  runtime hotspot distribution.
- Check alignment assumptions, loop-carried dependencies, aliasing, and data
  layout when vectorization fails.
- Confirm that vectorization matters for the observed hotspot before rewriting
  large sections of code.

## Anti-Patterns

- profiling an unrepresentative toy case and generalizing from it;
- drawing conclusions from a debug build alone;
- collecting large profiler outputs without a clear question;
- optimizing a hotspot before confirming it materially affects end-to-end
  runtime;
- confusing sampling percentages with absolute speedup potential;
- treating profiler output as ground truth without hardware and workload context.

## Validation Defaults

- Run a small sanity check before profiling to confirm the code path is correct.
- Record the exact command, input, environment variables, and build type.
- Prefer repeatable profiling conditions with stable placement and low system
  noise.
- State clearly whether findings came from sampling, instrumentation, counters,
  or compiler reports.
- For Python, record the interpreter, virtual environment or package manager,
  and profiler invocation.
- If the profiling environment is constrained, say what could not be measured.

## Output Expectations

When using this skill, briefly note:

- what workload and build were profiled;
- which tools and counters were used;
- for Python, whether findings came from call profiling, sampling, line-level
  instrumentation, or memory profiling;
- the main hotspots or bottlenecks found;
- whether the likely limit is compute, memory, synchronization, communication,
  or I/O;
- which follow-up optimization or experiment is most justified.
