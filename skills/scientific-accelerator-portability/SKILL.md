---
name: scientific-accelerator-portability
description: Review and improve GPU and accelerator scientific code for
  portability across CUDA, HIP, SYCL, OpenACC, Kokkos, OpenMP offload, hardware
  generations, drivers, compilers, and fallback paths.
---

# Scientific Accelerator Portability

Use this skill when scientific code targets GPUs or other accelerators and must
remain correct, maintainable, and reasonably portable across hardware,
compilers, drivers, and execution environments.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- separating portable accelerator abstractions from backend-specific code;
- preserving CPU or non-accelerated fallback paths where practical;
- documenting hardware, driver, compiler, and runtime assumptions;
- testing correctness across backend and precision differences;
- avoiding overfitting to one GPU generation, vendor, or cluster.

## When To Use

Use this skill when:

- code uses CUDA, HIP, SYCL, OpenACC, OpenMP offload, Kokkos, RAJA, OpenCL, or
  accelerator-specific libraries;
- a CPU implementation is being ported to GPU or accelerator hardware;
- code must run on more than one accelerator backend or hardware generation;
- performance changes alter data movement, precision, launch shape, or memory
  layout;
- CI, containers, or workflows need accelerator-aware smoke tests.

Do not use this skill as a substitute for benchmarking or profiling. Use
`scientific-cli-benchmark` and `scientific-profiling` to measure behavior, then
use this skill to reason about portability and fallback tradeoffs.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the accelerator backend, target hardware, compiler, driver, and
   runtime assumptions.
3. Find the baseline implementation and expected scientific outputs.
4. Preserve or document fallback behavior before specializing.
5. Review correctness, data movement, memory layout, precision, and launch
   assumptions together.
6. State which backends or devices were considered, tested, and left untested.

Prefer portable abstractions and explicit backend boundaries before adding
vendor-specific special cases.

## Backend Strategy

- Use a portability layer such as Kokkos, RAJA, SYCL, OpenMP offload, or
  OpenACC when the project already depends on it or needs multi-vendor support.
- Use CUDA or HIP directly when the project deliberately targets that backend
  and the maintenance cost is accepted.
- Keep backend-specific code isolated behind capability checks, build options,
  or narrow implementation files.
- Avoid mixing unrelated accelerator models in one code path without a clear
  abstraction boundary.
- Document which backend is primary and which are best-effort.

Portability should be a design choice, not an accidental collection of compiler
branches.

## Fallback Paths

- Preserve a CPU or serial fallback when practical.
- Make fallback selection explicit through build options, runtime detection, or
  documented configuration.
- Ensure tests cover fallback paths, not only the fastest accelerator path.
- Avoid silently changing scientific behavior when falling back to CPU or a
  different precision.
- Document when no fallback exists and why.

A slow correct fallback is often valuable for validation and portability.

## Data Movement and Memory

- Minimize host-device transfers in hot paths.
- Keep ownership and lifetime of device data explicit.
- Avoid hidden synchronization unless it is required for correctness.
- Check that memory layout matches access patterns for the target backend.
- Be explicit about unified memory, pinned memory, managed memory, and device
  allocations.
- Treat out-of-memory behavior and allocation failures as expected failure
  modes, not impossible states.

Data movement mistakes can dominate performance and obscure correctness bugs.

## Precision and Numerical Behavior

- Check whether the accelerator path changes precision, reduction order,
  math-library implementation, or fused operations.
- Use tolerances justified by algorithm, scale, backend, and reduction behavior.
- Compare accelerator and CPU outputs on small deterministic cases.
- Avoid assuming bitwise equality across GPU models, compiler versions, or math
  libraries unless the project explicitly enforces it.
- Document when backend-specific numerical drift is expected.

Use `scientific-numerics-review` for deeper numerical stability and tolerance
analysis.

## Build and Configuration

- Keep accelerator backend selection explicit in CMake, package metadata, or
  build scripts.
- Avoid hardcoding one CUDA architecture, GPU name, compiler path, or SDK
  install location as a global default.
- Support architecture lists or configurable target capabilities when
  reasonable.
- Separate required accelerator dependencies from optional acceleration.
- Fail clearly when a requested backend is unavailable.

Use `scientific-build-systems` for implementation details in compiled build
configuration.

## Containers and Workflows

- Document host driver and runtime requirements for GPU containers.
- Do not assume the container fully owns the GPU software stack.
- For Apptainer/Singularity, document GPU flags such as `--nv` or `--rocm`
  where relevant.
- Keep workflow profiles explicit about accelerator requirements.
- Provide tiny accelerator smoke tests before large GPU runs.

Use `scientific-container-workflows` and `scientific-workflow-automation` for
container and workflow integration.

## CI and Testing

- Keep CPU/fallback tests in ordinary CI when accelerator runners are
  unavailable.
- Add accelerator smoke tests only when suitable runners or self-hosted
  infrastructure are available.
- Mark GPU-specific tests clearly so they can be skipped or selected.
- Test small deterministic inputs before performance-sized workloads.
- Check both correctness and device selection behavior.

CI should not pretend to validate accelerator support if no accelerator is
available.

## Performance Portability

- Do not overfit launch dimensions, block sizes, vector widths, or tile sizes to
  one GPU generation without measurement.
- Prefer tunable parameters when one fixed value is unlikely to generalize.
- Distinguish occupancy, bandwidth, latency, transfer, and synchronization
  bottlenecks.
- Record hardware model, driver, compiler, runtime, and input shape for
  benchmark claims.
- Preserve maintainability unless the specialization has measured value.

Use `scientific-performance-portability` for broader non-accelerator
portability tradeoffs.

## Anti-Patterns

- making the accelerator path the only tested implementation;
- hiding backend selection in local environment variables;
- hardcoding one user's CUDA, ROCm, or compiler install path;
- assuming all GPUs support the same precision, atomics, memory, or libraries;
- committing code that only works on one cluster without documenting why;
- treating a successful kernel launch as proof of scientific correctness;
- using GPU timing without synchronizing or accounting for data transfer.

## Validation Defaults

- Build or configure the requested backend when practical.
- Run a tiny correctness case on CPU/fallback and accelerator paths when
  available.
- Check device discovery or backend-selection output.
- Compile or run tests for fallback behavior.
- Record which hardware, compiler, driver, and backend were actually tested.
- If no accelerator is available, state that only static/build-level checks were
  performed.

## Output Expectations

When using this skill, briefly note:

- which backend, hardware, compiler, driver, and runtime assumptions were
  considered;
- whether CPU/fallback behavior exists and was tested;
- what correctness, tolerance, data-movement, or configuration risks were
  addressed;
- which accelerator smoke tests, builds, or benchmarks were run;
- what remains backend-specific, hardware-specific, or untested.
