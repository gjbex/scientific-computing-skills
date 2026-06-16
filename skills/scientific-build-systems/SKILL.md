---
name: scientific-build-systems
description: Configure and maintain build systems for scientific-computing and
  HPC software, especially when compiler warnings, build types, optimization
  flags, sanitizers, dependencies, and portable CMake-style workflows need
  pragmatic defaults.
---

# Scientific Build Systems

Use this skill when editing or reviewing build configuration for scientific,
numerical, or parallel software and the repository needs practical defaults for
correctness, portability, and performance-oriented development.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- CMake-style project structure and target-scoped settings;
- warning profiles and language-standard choices;
- debug, release, and sanitizer-oriented build types;
- dependency handling in research and HPC environments;
- portable optimization settings that avoid overfitting to one machine.

## When To Use

Use this skill when:

- the user asks to add or clean up build-system configuration;
- compiler flags, warnings, or language standards need a consistent baseline;
- the project needs clearer debug versus release behavior;
- sanitizers or analysis builds should be added without disrupting normal use;
- a scientific codebase must build across laptops, clusters, or CI machines.

Do not use this skill to override explicit repository policy or cluster-specific
toolchain constraints that are already documented.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Inspect the existing build entry points before introducing new structure.
3. Prefer target-scoped settings over global flags.
4. Separate developer-friendly defaults from machine-specific tuning.
5. Keep release, debug, and sanitizer workflows explicit.
6. State what was changed, what was validated, and what remains environment-specific.

Prefer extending the repository's current build system rather than migrating it
unless the user explicitly asks for that change.

## Preferred Defaults

- Prefer CMake for compiled scientific projects when the build system is open to
  choice.
- Use modern target-based CMake patterns rather than directory-wide global state.
- Prefer explicit language standards such as C11, C17, or C++20 when supported
  by the repository toolchain.
- Keep warning configuration reusable and target-scoped.
- Reserve machine-specific flags such as `-march=native` for opt-in builds, not
  broad defaults.

## Build Types

Distinguish build intents clearly:

- `Debug` for diagnostics, assertions, and source-level debugging;
- `Release` for optimized production-style performance work;
- `RelWithDebInfo` as a practical default for profiling and many scientific
  development tasks;
- sanitizer-oriented builds for memory and undefined-behavior diagnosis.

Do not weaken warnings in optimized builds merely to keep them quiet.

## Compiler Warnings

- Start from a practical warning baseline such as `-Wall -Wextra -Wpedantic`
  where supported.
- Add stricter warnings incrementally when the codebase is ready for them.
- Treat new warnings as issues to fix rather than noise to suppress.
- Prefer narrow suppressions with clear rationale when suppression is necessary.
- Keep warning helpers target-scoped so third-party code is not affected by
  project policies.

For numerically sensitive code, consider `-Wshadow`, `-Wconversion`,
`-Wsign-conversion`, or `-Wdouble-promotion` only when the cleanup cost is
understood.

## Optimization Flags

- Prefer portable baseline optimization such as `-O2` or `-O3` through the
  build type rather than hand-appending flags everywhere.
- Avoid enabling architecture-specific tuning globally unless the repository is
  explicitly single-machine or single-cluster.
- Use link-time optimization only when the toolchain and dependency stack are
  known to support it cleanly.
- Document any non-default flags added for performance investigation.

If users want per-machine tuning, expose it as an option rather than making it
the default behavior for everyone.

## Sanitizers and Analysis Builds

- Add AddressSanitizer and UndefinedBehaviorSanitizer as opt-in developer tools
  when the compiler supports them.
- Keep sanitizer flags out of normal release builds.
- Disable or adjust incompatible optimizations only as needed for usable reports.
- Document runtime caveats such as MPI launcher interaction or unsupported
  vendor libraries.

When practical, keep sanitizer configuration behind a dedicated option or build
preset instead of mixing it into unrelated build modes.

## Dependencies

- Prefer discovered packages through the repository's existing mechanism.
- Keep dependency declarations explicit and version expectations clear.
- Avoid hardcoding machine-local paths unless the environment requires it.
- Distinguish required dependencies from optional accelerators or tooling.
- Make it easy to build a minimal feature set when full HPC dependencies are
  unavailable on a developer machine.

For HPC-style environments, expect variation across module systems, compilers,
MPI stacks, and BLAS implementations.

## CMake Patterns

Prefer patterns like:

- target-specific compile features and compile options;
- small helper functions for warnings or sanitizer flags;
- `option()` for opt-in features and heavyweight dependencies;
- `find_package()` or repository-native discovery rather than manual include
  path duplication;
- `ctest` integration when tests exist.

Avoid pushing project policy into global variables when target properties are
enough.

## Presets and Reproducibility

- Prefer `CMakePresets.json` when the repository already uses presets or when
  multiple repeatable developer configurations are needed.
- Use presets to separate common workflows such as debug, release, profiling,
  and sanitizer builds.
- Keep host-specific values out of shared presets unless they are intentionally
  local-only.

Presets are useful when the same build modes must be reproduced across local
development, CI, and cluster login nodes.

## Anti-Patterns

- forcing one developer's machine-specific flags on all users;
- mixing debug, release, and sanitizer concerns into one opaque flag set;
- global include and compile flag mutations when target-scoped settings suffice;
- silently disabling warnings to get a build through;
- hardcoding dependency paths that should be discovered or configured;
- adding build-system complexity before confirming the repository needs it.

## Validation Defaults

- Configure from a clean build directory when practical.
- Validate at least one normal developer build after changing build logic.
- If build options were added, test the affected configuration paths directly.
- Record which compiler, generator, and important options were used.
- State explicitly what could not be validated in the current environment.

## Output Expectations

When using this skill, briefly note:

- which build-system files and targets were changed;
- which warning, standard, or build-type policies were introduced or preserved;
- whether sanitizer, preset, or dependency logic was added;
- which build commands were run;
- which portability or toolchain risks remain.
