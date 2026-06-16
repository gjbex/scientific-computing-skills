---
name: scientific-code-style
description: Apply reusable coding, validation, documentation, and compiler
  warning conventions to scientific-computing and HPC repositories when
  project-specific `AGENTS.md` guidance is absent or intentionally minimal.
---

# Scientific Code Style

Use this skill when editing scientific-computing or HPC code and the repository
does not already define stricter conventions in `AGENTS.md`.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a consistent reusable default for:

- coding style
- language features to prefer or avoid
- validation habits
- testing expectations
- documentation quality

## When To Use

Use this skill when:

- the task is in a scientific, numerical, or HPC codebase
- the user wants reusable scientific-computing conventions applied
- repository instructions are absent, minimal, or intentionally high-level

Do not use this skill to override explicit repository conventions.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Follow repository-specific rules where they exist.
3. Use this skill only for gaps that are still unspecified.
4. Keep changes pragmatic and aligned with the existing codebase.

## General Conventions

- Prefer modern coding styles, idioms, and best practices.
- Keep source lines to 79 characters when practical.
- Use descriptive names.
- Avoid unnecessary dependencies, imports, and includes.
- Prefer straightforward code that is easy to benchmark, validate, and review.

## Python Conventions

- Use type hints and docstrings for functions and classes.
- Follow PEP 8.
- Prefer f-strings over `%` formatting and `str.format()`.
- Prefer list comprehensions and generator expressions when they improve
  clarity.
- Prefer context managers for resource management.
- Prefer `pathlib` over `os.path`.
- Use descriptive snake case for variables and functions.
- Define constants at module scope with uppercase names.
- Prefer single quotes for string literals unless the string contains a single
  quote.
- Group imports as standard library, third-party, and local imports.
- Separate import groups with a blank line and alphabetize within each group.

## C++ Conventions

- Prefer C++20 or later when practical.
- Prefer smart pointers over raw owning pointers.
- Prefer range-based `for` loops when they improve clarity.
- Prefer `auto` when it removes redundant type noise.
- Use `nullptr` instead of `NULL` or `0`.
- Prefer `constexpr` for compile-time constants.
- Prefer `std::string` over C-style strings.
- Use descriptive snake case names.
- Define constants with `constexpr` or `const` using uppercase names.
- Group headers as corresponding header, standard library, third-party, and
  project headers.
- Separate header groups with a blank line and alphabetize within each group.

## Compiler Warnings

- Enable a useful baseline of compiler warnings for C and C++ builds.
- Prefer `-Wall -Wextra -Wpedantic` as a practical default when supported.
- Treat new warnings as defects to fix, not noise to ignore.
- Use `-Werror` only when the repository already relies on it or the toolchain
  is stable enough that it will not create avoidable churn.
- If a warning must be suppressed, prefer the narrowest possible suppression and
  document why it is necessary.
- Avoid disabling broad warning groups just to silence one issue.

## Recommended Warning Flags

- Start with `-Wall -Wextra -Wpedantic` for GCC and Clang.
- Consider adding `-Wshadow` when variable shadowing is likely to hide defects.
- Consider adding `-Wconversion` and `-Wsign-conversion` for numerically
  sensitive code, but expect some cleanup effort before enabling them broadly.
- Consider adding `-Wdouble-promotion` for floating-point-heavy code when the
  toolchain supports it.
- Consider adding `-Wformat=2` for stricter format-string checking in C code.
- Prefer enabling additional warnings incrementally and fixing the resulting
  issues rather than turning on a large set all at once.

## Build-Type Guidance

- In debug builds, prefer strong warnings and debug symbols so problems are easy
  to diagnose.
- In release builds, keep the same warning baseline unless there is a
  repository-specific reason to differ.
- Do not weaken warnings in release builds merely to keep optimized builds
  quiet.
- If `-Werror` is used, prefer enabling it in CI or in well-controlled
  toolchains rather than assuming it is safe everywhere.

## CMake Pattern

Use a target-scoped warning helper rather than global flags when the repository
uses CMake:

```cmake
function(enable_project_warnings target_name)
    target_compile_options(${target_name} PRIVATE
        $<$<AND:$<COMPILE_LANGUAGE:C>,$<C_COMPILER_ID:GNU,Clang>>:
            -Wall
            -Wextra
            -Wpedantic
            -Wshadow
            -Wformat=2
        >
        $<$<AND:$<COMPILE_LANGUAGE:CXX>,$<CXX_COMPILER_ID:GNU,Clang>>:
            -Wall
            -Wextra
            -Wpedantic
            -Wshadow
        >
    )
endfunction()
```

Then apply it per target:

```cmake
add_executable(example example.cpp)
enable_project_warnings(example)
```

For numerically sensitive targets, consider a second stricter helper that adds
flags such as `-Wconversion`, but only after the repository is ready to address
the extra findings.

## Validation Defaults

- Run static analysis tools appropriate to the language when available.
- For Python, prefer `pylint`, `flake8`, and `mypy`.
- For C++, prefer `clang-tidy` and `cppcheck`.
- For compiled languages, check whether warning flags are enabled and add them
  when the build system does not already define a reasonable baseline.
- If tools are unavailable, state that explicitly rather than assuming
  compliance.

Use `developer-tool-installation-policy` when deciding whether formatters,
linters, or static-analysis tools should be project-pinned through repository
configuration or installed globally for ad hoc inspection.

## Testing Defaults

- Add automated tests for major functionality when feasible.
- Keep tests independent of execution order.
- Cover normal behavior and meaningful edge cases.
- For Python, prefer `pytest`.
- For C++, prefer Google Test.

## Documentation Defaults

- Document nontrivial functions, classes, and modules.
- Add usage examples when they materially help understanding.
- For Python docstrings, prefer `numpy` or `scipy` style.
- Prefer single quotes for Python docstrings.
- Use doctest format for Python examples when examples are useful.
- For C++, prefer Doxygen-style comments.

## Output Expectations

When using this skill, briefly note:

- whether repository rules overrode any part of this skill
- which validation or test steps were run
- which checks could not be run
