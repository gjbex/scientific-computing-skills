---
name: scientific-documentation
description: Write and improve documentation for scientific-computing and HPC
  software, especially when algorithms, assumptions, parameters, workflows,
  reproducibility expectations, and performance context must be explained
  clearly to technical users.
---

# Scientific Documentation

Use this skill when editing or reviewing documentation for scientific,
numerical, or parallel software where readers need clear technical guidance on
what the software does, how to run it, and how to interpret its results.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- README and usage documentation for scientific tools and workflows;
- documenting assumptions, inputs, outputs, and parameter meanings;
- explaining algorithms and numerical choices at the right level;
- connecting documentation to validation, reproducibility, and performance work.

## When To Use

Use this skill when:

- the user asks to add or improve project documentation;
- the repository lacks clear instructions for building, running, or validating;
- numerical methods, solver settings, or data products need explanation;
- results are hard to interpret because assumptions or units are undocumented;
- examples or workflow descriptions would materially reduce confusion.

Do not use this skill to replace formal scientific papers or deep domain
theory that belongs in external references.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the target reader: developer, researcher, student, or user.
3. Document what the software does before describing internal structure.
4. Prefer concrete commands, examples, and file paths over abstract prose.
5. Explain assumptions, limits, and output interpretation explicitly.
6. State what was documented, what remains implicit, and what was verified.

Prefer extending existing repository documentation rather than scattering new
facts across many files without a clear entry point.

## Core Topics

Scientific documentation should usually make these easy to find:

- purpose of the code or workflow;
- build and run instructions;
- required inputs and expected outputs;
- units, conventions, and parameter meanings;
- validation or test expectations;
- reproducibility requirements such as seeds, configs, and environment details;
- performance-relevant runtime settings when they matter.

The goal is not maximal prose. The goal is reducing ambiguity for the next
technical reader.

## README Expectations

For project-level documentation, prefer a README that answers:

- what problem the software solves;
- who it is for;
- how to build or install it;
- the simplest command that works;
- where to find examples, tests, or datasets;
- what the major limitations or assumptions are.

If benchmarking or profiling is central to the project, say so explicitly and
link the expected workflow.

## Method and Model Explanations

- Document the numerical method at the level needed to use and maintain it.
- Explain approximations, stability assumptions, discretization choices, or
  solver stopping criteria when they affect results.
- Prefer short, precise descriptions over tutorial-style theory dumps.
- If equations or references are necessary, include only what clarifies the
  implementation or outputs.

Documentation should help readers understand both capability and limitation.

## Inputs, Outputs, and Parameters

- Define input file expectations, schema assumptions, and units.
- Explain output artifacts, formats, and how to interpret important fields.
- Document parameter defaults and which ones materially change results.
- Prefer explicit examples for non-obvious configuration combinations.
- Call out dangerous or expensive settings clearly.

If a parameter affects correctness, performance, or reproducibility, say so.

## Examples

- Include at least one minimal working example when practical.
- Prefer copyable commands with real filenames or realistic placeholders.
- Keep examples aligned with the current CLI, file layout, and defaults.
- Show expected output shape or key lines when that aids verification.
- Avoid examples that are too large, too slow, or dependent on hidden files.

Examples should be easy to rerun, not merely illustrative.

## Reproducibility and Performance Context

- Document seeds, config files, environment variables, and build assumptions
  needed to reproduce published examples or benchmark claims.
- Distinguish normal usage guidance from performance-tuning guidance.
- If thread counts, MPI ranks, affinity, or filesystem setup matter, document
  them near the relevant workflow.
- Avoid presenting one machine's performance as universal behavior.

Scientific documentation should help readers reproduce intent, not just syntax.

## Style Guidance

- Prefer precise technical language over marketing language.
- Use headings that reflect user tasks and concepts.
- Keep definitions close to the first point of use.
- Avoid unexplained acronyms when a short expansion would help.
- Prefer tables or structured lists when documenting many parameters or files.

Clarity matters more than stylistic flourish.

## Anti-Patterns

- README files that describe internals before basic usage;
- undocumented units, coordinate conventions, or assumptions;
- examples that no longer run;
- claims about correctness or performance with no validation context;
- scattering critical usage facts across commit history or issue threads;
- documenting only the happy path when failure modes are common.

## Validation Defaults

- Check that documented commands, paths, and filenames still match the repo.
- Run or partially verify key examples when practical.
- Confirm that parameter names, defaults, and output descriptions match code.
- State explicitly which documentation claims were validated and which were not.
- If examples could not be run, say why.

## Output Expectations

When using this skill, briefly note:

- which documentation files or sections were added or changed;
- which workflows, assumptions, or parameter meanings are now documented;
- whether examples or reproducibility notes were added;
- which documentation examples or commands were validated;
- which gaps remain for future documentation work.
