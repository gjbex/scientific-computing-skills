---
name: scientific-cli-benchmark
description: Benchmark command-line applications for scientific computing and
  HPC workloads. Use this skill when measuring runtime, scaling, or placement
  effects for serial or multithreaded executables, especially when thread
  counts, OpenMP affinity, correctness checks, or repeatable benchmarking with
  hyperfine matter.
---

# Scientific CLI Benchmark

## Overview

Use this skill to benchmark command-line applications in a way that is
appropriate for scientific computing workloads. Prefer reproducible runs,
explicit runtime settings, lightweight sanity checks before timing, and
reporting that distinguishes single-thread baselines from multithreaded
scaling and placement effects. This skill is for performance measurement,
not for full functional or scientific verification.

## When to Use It

Use this skill when the user asks to:

- benchmark a CLI executable or script;
- compare serial and parallel runtime;
- measure OpenMP or thread-count scaling;
- study socket placement, affinity, or memory locality effects;
- collect repeatable timing data for a report, table, or plot.

This skill is a poor fit for microbenchmarks inside a programming
language runtime. It is meant for end-to-end command execution.

## Useful Tools

Useful tools for this skill include:

- `hyperfine` for repeated end-to-end timing with warmups and summary
  statistics;
- `STREAM` for sustained memory-bandwidth measurements;
- `lmbench`, especially `lat_mem_rd`, for memory-latency probes;
- `LIKWID` for topology-aware bandwidth-style microbenchmarks and
  hardware-counter workflows on Linux HPC systems;
- `lscpu` and `nproc` for basic CPU and topology information;
- `hwloc` tools such as `lstopo` for richer topology inspection;
- `numactl` for NUMA policy control and hardware layout queries;
- `taskset` for lightweight CPU affinity control on Linux;
- `perf stat` and `perf record` for hardware-counter diagnosis and
  hotspot investigation;
- `OMP_DISPLAY_ENV` for confirming the OpenMP runtime configuration that
  the program actually sees.

## Workflow

1. Identify the benchmark target and how it is built or launched.
2. Build an optimized executable before timing, usually a release build.
3. Establish a benchmark sanity check:
   run a small or representative case first and verify a checksum,
   residual, output file hash, or other stable signal sufficient to
   ensure the timed cases are comparable.
4. Inspect hardware and runtime constraints that affect performance:
   core counts, sockets, SMT, cache hierarchy and cache sizes, memory
   bandwidth, allocator, CPU frequency policy, and scheduler placement
   if running under Slurm or similar systems.
5. Choose the timing method:
   prefer `hyperfine`; use the bundled fallback script when `hyperfine`
   is unavailable or when the benchmark needs more custom control.
6. Run warmups before recording data.
7. Sweep the relevant parameters:
   problem size, thread count, affinity policy, tile sizes, input files,
   and build variants.
8. Report the exact command line and all relevant environment variables.
9. Summarize results with mean runtime, variability, and derived metrics
   such as speedup and efficiency when thread scaling is measured.

## Benchmark Design Rules

- Keep the benchmark focused on one question at a time.
- Use wall-clock time for end-to-end application performance.
- Record the machine and scheduler context when available.
- Separate benchmark sanity checks from timing runs if validation adds
  material overhead.
- Keep correctness work minimal in this skill:
  only do enough to ensure benchmark results are meaningful. Full
  program verification belongs in a different workflow or skill.
- Avoid comparing runs with different problem sizes unless the goal is a
  weak-scaling or throughput study.
- For multithreaded runs, always record:
  `OMP_NUM_THREADS`, `OMP_PROC_BIND`, `OMP_PLACES`, and any affinity
  variables such as `GOMP_CPU_AFFINITY` or `KMP_AFFINITY`.
- Treat first-run effects explicitly:
  filesystem cache, JIT compilation, page faults, and data staging can
  distort a single timing.
- Prefer at least 5 measured runs for stable executables. Increase run
  counts when jitter is high or runtime is short.
- Long-running benchmark scripts should emit progress updates through
  `logging`, typically at `INFO` level, for build, correctness checks,
  and each major sweep dimension so the user can see which case is
  currently running and suppress output easily when needed.

## Timing with Hyperfine

When `hyperfine` is available, prefer it for simple repeated command
timing. Common pattern:

```bash
hyperfine \
    --warmup 2 \
    --runs 8 \
    --export-json benchmark.json \
    'OMP_NUM_THREADS=1 ./my_solver input.dat' \
    'OMP_NUM_THREADS=16 OMP_PROC_BIND=spread OMP_PLACES=cores ./my_solver input.dat'
```

For parameter sweeps, keep one varying dimension per loop so the output
stays interpretable. For example:

```bash
for threads in 1 2 4 8 16 32; do
    echo "=== threads=${threads} ==="
    OMP_NUM_THREADS="${threads}" \
    OMP_PROC_BIND=spread \
    OMP_PLACES=cores \
    hyperfine --warmup 1 --runs 6 './my_solver -n 4000'
done
```

Use `--prepare` only when the preparation step is intentionally excluded
from the measurement.

If `hyperfine` is missing and the user wants it, use
`scripts/install_hyperfine.sh` to install a private copy without root
access. By default it installs into `./tools/hyperfine`, which is useful
for project-local workflows and shared cluster environments.

Example:

```bash
skills/scientific-cli-benchmark/scripts/install_hyperfine.sh \
    --prefix ./tools/hyperfine
export PATH="$PWD/tools/hyperfine/bin:$PATH"
```

The installer prefers `cargo install --root ...` when `cargo` is
available. Otherwise it downloads a prebuilt release tarball for common
Linux architectures.

## Fallback Timing

If `hyperfine` is not installed, use
`scripts/simple_benchmark.py`. It runs warmups, repeats the command,
captures wall-clock timings, and can emit either a plain-text table or
JSON.

Example:

```bash
python3 skills/scientific-cli-benchmark/scripts/simple_benchmark.py \
    --warmup 2 \
    --runs 8 \
    --threads 1,2,4,8,16 \
    --env OMP_PROC_BIND=spread \
    --env OMP_PLACES=cores \
    --command ./my_solver -- -n 4000 -t 100
```

The `--threads` option expands into multiple runs by setting
`OMP_NUM_THREADS` for each requested value.

## Multithreading and Affinity

For OpenMP or thread-pool based programs:

- start from a 1-thread baseline;
- sweep meaningful thread counts, not just powers of two;
- check whether SMT should be disabled or excluded;
- test placement policies such as `close` and `spread`;
- distinguish one-socket from full-node runs on multisocket machines.

If the user asks for scaling results, compute:

- speedup = `T1 / Tp`;
- parallel efficiency = `speedup / p`.

When the machine topology matters, gather context with commands such as:

```bash
lscpu
numactl --hardware
```

If running under a scheduler, also record the allocation details.

## Interpreting Results

In scientific computing, benchmark interpretation should connect the
timings to workload characteristics:

- gather basic hardware context before drawing conclusions;
- compute-bound kernels may scale until core or vector limits dominate;
- memory-bound kernels often saturate bandwidth early;
- placement sensitivity often indicates NUMA or bandwidth effects;
- high variance can indicate oversubscription, thermal throttling,
  interference from other jobs, or unstable I/O.

Useful system-characterization tools include:

- `lscpu` for CPU topology, sockets, cores, threads, cache sizes, and
  NUMA layout;
- `nproc` for the visible logical CPU count;
- Intel `mlc` when available to estimate sustained memory bandwidth and
  latency, which is often valuable when interpreting memory-bound
  kernels.

Cache and memory-hierarchy context matters when interpreting benchmark
results:

- tile-size effects often reflect cache-capacity and cache-line reuse
  behavior rather than only algorithmic changes;
- runtime jumps can occur when the working set stops fitting in a given
  cache level;
- a result that looks compute-bound at small `n` may become memory-bound
  once the footprint exceeds the relevant cache capacity.

Avoid claiming a speedup without stating the baseline, problem size, and
thread placement.

## Outputs

When reporting results, include:

- the tested command;
- build type and compiler when relevant;
- machine or node description;
- hostname and basic CPU topology from tools such as `nproc` or `lscpu`;
- git remote and commit hash when the benchmark was run from a clean
  worktree;
- thread and affinity settings;
- number of warmups and measured runs;
- mean runtime and variability;
- speedup and efficiency for scaling studies;
- any benchmark sanity signal used before timing.

## Deliverables

When the user wants a finished benchmark artifact, produce one or more of
the following:

- a reproducible shell script;
- a scheduler job script for cluster runs;
- a markdown summary table;
- a CSV or JSON file with raw timing data.
