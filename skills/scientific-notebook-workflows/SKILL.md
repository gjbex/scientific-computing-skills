---
name: scientific-notebook-workflows
description: Maintain reproducible scientific notebook workflows, including
  notebook structure, output policy, CI smoke checks, conversion to scripts or
  modules, and intentional report/demo notebooks with committed outputs.
---

# Scientific Notebook Workflows

Use this skill when scientific work uses Jupyter, Quarto, R Markdown, Pluto, or
similar notebooks for exploration, reporting, demos, documentation, or
reproducible analysis.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- keeping notebooks reproducible, reviewable, and useful;
- deciding when notebook outputs should be stripped or committed;
- separating reusable logic from exploratory cells;
- adding small execution or smoke-test paths for important notebooks;
- documenting data, environment, and artifact expectations.

## When To Use

Use this skill when:

- notebooks are part of a scientific workflow, report, demo, tutorial, or
  analysis artifact;
- notebook outputs cause review noise or reproducibility concerns;
- reusable logic is trapped inside notebook cells;
- notebooks need CI execution, smoke checks, or conversion to scripts;
- GitHub preview of notebook outputs is intentionally useful.

Do not use this skill to replace project packaging or workflow orchestration.
Use `scientific-package-management` for package layout and
`scientific-workflow-automation` for multi-step pipelines.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the notebook role: exploration, report, demo, tutorial,
   documentation, or workflow step.
3. Decide the output policy based on that role.
4. Factor reusable logic into scripts, modules, or package code when practical.
5. Keep data paths, parameters, environment assumptions, and generated outputs
   explicit.
6. State what was made reproducible, what remains exploratory, and how the
   notebook should be reviewed.

Avoid treating all notebooks the same. Exploration notebooks, report notebooks,
and CI-executed notebooks have different contracts.

## Notebook Roles

- exploration: scratch or early-stage investigation, often not release-critical;
- analysis: reproducible computation over known inputs;
- report: narrative result presentation intended for readers;
- demo: runnable or previewable example of project behavior;
- tutorial: teaching material with explanatory output;
- workflow step: notebook is part of an automated or documented pipeline.

The role determines whether outputs, execution order, and CI expectations need
to be strict.

## Output Policy

Strip outputs by default when notebooks are primarily source artifacts and the
outputs are reproducible, noisy, large, or irrelevant to review.

Commit outputs intentionally when they are part of the repository contract, for
example:

- report notebooks where GitHub preview is useful to readers;
- demo notebooks where rendered output shows expected behavior;
- tutorial notebooks where outputs are instructional;
- publication or release artifacts where the rendered result is reviewed.

When committing outputs:

- document that outputs are intentionally committed;
- keep outputs small enough for review and repository size;
- avoid embedding secrets, private paths, large binary blobs, or unstable random
  output;
- record the environment and command used to regenerate the notebook;
- rerun from a clean kernel before committing if the notebook is meant to be
  reproducible.

Do not commit outputs merely because they happened to be present after an
interactive session.

## Structure and Reusable Logic

- Keep reusable functions in importable modules or scripts.
- Keep notebooks as consumers of project code, not the only implementation.
- Use clear sections for setup, parameters, data loading, analysis, and results.
- Avoid hidden state across non-linear execution order.
- Prefer explicit parameters over editing cells before each run.
- Keep long-running or expensive steps behind documented switches or cached
  inputs.

Notebook cells should tell a readable story without becoming the project's API.

## Data and Artifacts

- Use small example data or documented subsets for notebooks intended to run in
  CI or by new users.
- Keep generated figures, tables, and exports in documented output locations.
- Do not rely on user-local absolute paths.
- Record data provenance, checksums, filters, and preprocessing where they
  affect interpretation.
- Keep large datasets, caches, and generated outputs out of Git unless they are
  intentional release artifacts.

Use `scientific-data-management` for large data and fixture policy.

## Environment and Dependencies

- Document the kernel, language version, and key packages.
- Prefer using the repository's normal environment setup instead of notebook-only
  installation cells.
- Avoid installing packages inside notebooks unless the notebook is explicitly a
  self-contained tutorial and the tradeoff is documented.
- Keep environment setup consistent with `pyproject.toml`, environment files,
  lockfiles, or project documentation.

Use `scientific-package-management` when dependency structure needs cleanup.

## CI and Smoke Checks

- Execute important notebooks in CI only with small inputs and stable outputs.
- Prefer smoke checks for tutorials and demos rather than full production runs.
- Fail clearly when a notebook cannot run from a clean checkout.
- Consider checking execution with tools such as `nbclient`, `pytest`,
  `nbval`, Quarto render, or framework-native commands when they are already
  part of the project.
- Keep notebook CI separate from heavyweight analysis unless the repository
  deliberately validates full reports.

If notebook execution is too expensive for CI, document the manual validation
command and expected runtime.

## Review Hygiene

- Minimize irrelevant metadata churn.
- Avoid committing execution-order chaos when the notebook is meant to be
  readable.
- For output-stripped notebooks, verify the notebook still runs after stripping.
- For output-committed notebooks, ensure the output diff is meaningful and not
  just stale execution noise.
- Treat large base64-encoded images or widgets as generated artifacts unless
  there is a clear reporting/demo reason.

Reviewers should be able to distinguish source changes from generated output
changes.

## Converting Notebooks

Factor notebook logic out when:

- multiple notebooks copy the same code;
- tests need to cover notebook logic;
- a workflow depends on notebook internals;
- performance profiling or packaging requires a script/module boundary;
- notebooks are too large or fragile to review.

Prefer small helper modules or scripts over a large migration unless the project
is ready for that change.

## Validation Defaults

- Open or inspect the notebook metadata when output policy changes.
- Run the smallest representative notebook execution when practical.
- If outputs are committed, rerun from a clean kernel or state why that was not
  done.
- If outputs are stripped, verify no required report/demo output was removed.
- Check `.gitignore` and repository policy for generated figures, data, and
  notebook checkpoints.

## Anti-Patterns

- keeping the only implementation of a workflow inside notebook cells;
- committing huge outputs or private paths by accident;
- stripping outputs from report/demo notebooks where preview is the point;
- relying on hidden kernel state;
- adding notebook-only dependency installation that diverges from the project
  environment;
- treating a rendered notebook as validated when it was not rerun cleanly.

## Output Expectations

When using this skill, briefly note:

- the notebook role and chosen output policy;
- whether outputs were stripped, retained, regenerated, or intentionally
  committed;
- which reusable logic, data paths, environment assumptions, or generated
  artifacts changed;
- which notebook execution or render checks were run;
- what remains exploratory, manual, or too expensive to validate.
