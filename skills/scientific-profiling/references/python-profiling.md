# Python Profiling Reference

Use this reference when the slowdown is in a Python scientific workflow or when
it is unclear whether the bottleneck is Python code, native libraries, or
memory behavior.

## Tool Choice

Pick the lightest tool that answers the current question:

- `cProfile` when you need a fast first pass over a reproducible local run.
- `py-spy` when you want sampling without editing code or when attaching to a
  running process.
- `line_profiler` when one or two Python functions are already suspect and the
  question is which lines dominate.
- `scalene` when you need per-line CPU, native, and memory attribution.
- `tracemalloc` when the question is allocation growth, object retention, or
  where Python heap memory is coming from.
- `memray` when a stronger memory profile is needed, especially for allocation
  traces and native-backed memory behavior.
- `perf` or native profilers when most time is already known to be inside
  compiled extensions.

## Baseline Capture

Before profiling, record:

- interpreter and environment:
  `python --version`, package manager, and virtual environment if present;
- main numerical packages and versions;
- the exact command line or test target;
- thread-related environment variables used by BLAS, OpenMP, or PyTorch.

Prefer a script or module entry point over ad-hoc notebook cells. If the hot
path currently lives in a notebook, factor it into an importable function or a
small script first.

## cProfile

Use `cProfile` for the first pass when overhead is acceptable and the workload
is easy to rerun.

Collect:

```bash
python -m cProfile -o profile.pstats path/to/script.py --arg1 value
```

Or for a module entry point:

```bash
python -m cProfile -o profile.pstats -m package.module --arg1 value
```

Inspect sorted by cumulative time:

```bash
python - <<'PY'
import pstats
stats = pstats.Stats("profile.pstats")
stats.strip_dirs().sort_stats("cumulative").print_stats(30)
PY
```

Interpretation:

- cumulative time shows where end-to-end time is spent;
- internal time helps separate local work from child-call dominated wrappers;
- many cheap Python calls often indicate dispatch or data-conversion overhead;
- if heavy time disappears into a small number of extension calls, move to
  library-specific or native profiling.

## py-spy

Use `py-spy` when you want sampling with low intrusion.

Top-style live view:

```bash
py-spy top -- python path/to/script.py --arg1 value
```

Record a flame graph:

```bash
py-spy record -o profile.svg -- python path/to/script.py --arg1 value
```

Attach to a running process:

```bash
py-spy top --pid 12345
```

Interpretation:

- stacks that repeatedly end in Python loops indicate interpreter overhead;
- stacks dominated by extension frames suggest the real hotspot is below
  Python;
- flat, noisy samples can indicate a workload that is too short or too
  irregular for stable conclusions.

## line_profiler

Use `line_profiler` only after narrowing the search to a small set of Python
functions.

Typical pattern:

```python
from line_profiler import profile

@profile
def step(state):
    ...
```

Run:

```bash
kernprof -lb path/to/script.py --arg1 value
```

Use it for:

- Python loops that may need vectorization or batching;
- dataframe-style transformations with suspicious per-row logic;
- glue code around native kernels where data motion may dominate.

Avoid decorating many functions at once. The output becomes noisy and the
instrumentation overhead increases quickly.

## Scalene

Use `scalene` when you need to separate Python time from native time and also
want memory signals.

Example:

```bash
scalene --reduced-profile --cpu --memory path/to/script.py --arg1 value
```

Use it when:

- the boundary between Python and extension time is unclear;
- allocation churn may be part of the slowdown;
- you need per-line evidence before rewriting code.

Interpretation:

- high Python CPU time points to interpreter-side work;
- high native time with low Python time suggests library calls or extensions;
- memory-heavy lines often indicate repeated temporary arrays, dataframe copies,
  or object churn.

## tracemalloc

Use `tracemalloc` when memory growth or allocation hotspots matter more than
CPU time.

Minimal pattern:

```python
import tracemalloc

tracemalloc.start()
run_workload()
snapshot = tracemalloc.take_snapshot()
for stat in snapshot.statistics("lineno")[:20]:
    print(stat)
```

Use it for:

- unexpected growth during iterative solvers or data pipelines;
- identifying which files and lines allocate the most Python-managed memory;
- comparing snapshots before and after a specific phase.

`tracemalloc` does not fully explain memory held only in native libraries, so
switch to `memray` or a native tool when the picture remains incomplete.

## Memray

Use `memray` when memory behavior needs a more complete trace.

Collect:

```bash
memray run -o memray.bin path/to/script.py --arg1 value
```

Inspect:

```bash
memray summary memray.bin
memray flamegraph memray.bin
```

Use it when:

- peak memory matters;
- allocations may come from both Python and native code paths;
- you need a richer artifact than `tracemalloc` provides.

## Mixed Python and Native Workloads

When Python orchestrates native kernels:

- profile Python first to see whether orchestration overhead is material;
- if the hot path is a small number of heavy extension calls, switch to native
  profilers rather than over-instrumenting Python;
- check thread counts for MKL, OpenBLAS, OpenMP, NumExpr, and PyTorch before
  concluding that Python is the scaling bottleneck;
- watch for repeated conversions between arrays, tensors, dataframes, and
  Python containers.

Common signals:

- many tiny calls around native kernels:
  batching or vectorization is likely more valuable than micro-optimizing one
  line;
- most time in imports or setup:
  separate startup from steady-state measurements;
- memory churn from temporary arrays:
  reduce copies, fuse operations, or reuse buffers.

## Reporting

When summarizing a Python profile, include:

- the entry point and representative input;
- the profiler and invocation used;
- whether the hotspot is in Python, native extensions, allocations, or
  synchronization;
- the top one or two optimizations that the profile actually justifies.
