---
name: scientific-cli-design
description: Design and review command-line interfaces for scientific-computing
  and HPC software, especially when parameter validation, configuration files,
  logging, output naming, reproducibility, and batch-friendly behavior matter.
---

# Scientific CLI Design

Use this skill when editing or reviewing a scientific, numerical, or parallel
program's command-line interface and run semantics, especially when the CLI is
part of a reproducible workflow or batch pipeline.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- clear CLI arguments and subcommands;
- robust parameter validation and error messages;
- config-file and command-line override behavior;
- predictable output, logging, and exit conventions;
- batch-friendly and reproducible scientific runs.

## When To Use

Use this skill when:

- the user asks to add or improve a CLI for a scientific code;
- parameter names, defaults, or validation rules are unclear;
- outputs, logs, or checkpoint paths need predictable conventions;
- both interactive runs and batch/scheduler runs must work cleanly;
- command lines should be easy to document, rerun, and benchmark.

Do not use this skill to replace GUI design or domain-specific workflow engines.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the primary run modes and the smallest useful default command.
3. Make required inputs, optional tuning knobs, and output destinations explicit.
4. Validate arguments early and fail with actionable messages.
5. Keep CLI behavior compatible with scripting, CI, and batch schedulers.
6. State what command syntax, defaults, and output behavior changed.

Prefer extending the repository's existing CLI style rather than inventing a new
interface shape unless the current one is clearly a maintenance problem.

## Argument Design

- Prefer descriptive option names over cryptic abbreviations.
- Use positional arguments only for a small number of obvious required inputs.
- Keep performance tuning options separate from scientific model parameters when
  possible.
- Document defaults and avoid hidden behavior changes triggered by unrelated
  flags.
- Prefer explicit units in option names or help text when ambiguity is likely.

For booleans, use clear positive flags and avoid flag pairs that can contradict
each other.

## Config Files and Overrides

- Support config files when many parameters must be reproducible or rerun often.
- Make precedence between config values, CLI overrides, and defaults explicit.
- Prefer printing or recording the resolved configuration for each run.
- Avoid silently ignoring unknown config keys or malformed values.
- Keep config formats human-editable unless the repository already requires
  another convention.

CLI and config handling should make reruns easier, not create two subtly
different configuration paths.

## Validation and Error Handling

- Reject invalid parameter combinations before expensive computation starts.
- Check file existence, writable output locations, and numeric ranges early.
- Fail with nonzero exit codes and concise, actionable messages.
- Distinguish user-input errors from internal failures when practical.
- Avoid silently clamping or correcting scientific parameters unless that
  behavior is documented and justified.

For long batch runs, early validation is usually cheaper than discovering a bad
setting after scheduling and startup overhead.

## Output and Logging Conventions

- Make output paths explicit and avoid surprising writes to the current working
  directory unless that is the project convention.
- Prefer stable filenames or structured run directories for generated artifacts.
- Separate human-readable logs from machine-readable outputs when practical.
- Include enough metadata in logs or manifests to identify the run configuration.
- Support controllable verbosity without hiding important warnings.

For parallel runs, include rank or thread context in logs when it aids debugging
without creating unmanageable noise.

## Batch and HPC Friendliness

- Avoid mandatory interactivity for normal runs.
- Respect environment variables and scheduler-provided paths only when that
  behavior is explicit and documented.
- Make thread counts, rank counts, and affinity-relevant settings easy to pass
  or record.
- Avoid progress output patterns that flood logs or break parsers at scale.
- Prefer deterministic exit behavior suitable for shell scripts and CI.

Batch users should be able to rerun a job from one command and a saved config.

## Reproducibility and Benchmarking

- Make command lines self-describing enough to reproduce reported runs.
- Prefer printing version, config, seed, and major runtime settings when useful.
- Keep benchmark-relevant options explicit rather than hidden in source edits.
- Avoid changing output formats or default parameter semantics without calling
  that out clearly.

A good scientific CLI should be easy to paste into documentation, tests, and
benchmark scripts.

## Anti-Patterns

- dozens of undocumented flags with unclear precedence;
- silent fallback to defaults after parsing errors;
- hidden writes, hidden randomness, or hidden environment-dependent behavior;
- output filenames that overwrite prior runs by accident;
- progress output that becomes unusable under MPI or many threads;
- one CLI path for local use and a different undocumented path for batch jobs.

## Validation Defaults

- Run help output and at least one representative command when practical.
- Test invalid arguments and confirm the error messages are useful.
- Verify output locations, exit codes, and logging behavior for changed paths.
- Check that documented examples still match the implemented CLI.
- State explicitly which command forms were validated and which were not.

## Output Expectations

When using this skill, briefly note:

- which CLI arguments, defaults, or config rules were added or changed;
- how invalid inputs and output paths are handled;
- whether logging, metadata, or batch behavior was improved;
- which CLI commands or help paths were tested;
- which usability or reproducibility concerns remain.
