---
name: scientific-workflow-automation
description: Design and maintain reproducible scientific workflows, with
  Nextflow as the preferred default for multi-step pipelines that should scale
  from laptops to HPC clusters or cloud executors.
---

# Scientific Workflow Automation

Use this skill when a scientific project needs an explicit, reproducible
workflow for running multi-step analyses, simulations, postprocessing, or data
pipelines.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- turning ad hoc shell history into version-controlled workflow entry points;
- choosing when Nextflow is the right orchestration layer;
- separating workflow orchestration from scientific application code;
- defining inputs, outputs, parameters, profiles, and run directories clearly;
- making small local runs and larger HPC or cloud runs share one workflow
  contract.

## When To Use

Use this skill when:

- a project has several dependent run, transform, analysis, or reporting steps;
- a workflow should run locally and scale to batch schedulers or cloud
  executors;
- reruns, caching, or resume behavior matter;
- containerized execution should be part of the reproducibility story;
- users need one documented command path instead of many manual shell steps.

Do not use this skill to replace ordinary build, test, or lint commands. Use
`project-repository-setup`, `scientific-build-systems`, or `scientific-ci` for
those concerns.

## Default Position

Prefer Nextflow for multi-step scientific workflows that need to scale from
laptops to HPC clusters or cloud environments, especially when the workflow
benefits from containers, caching, executor profiles, and clean failure
diagnostics.

Use `make` only for small local developer tasks such as `make test`,
`make format`, or `make clean`. Do not make a large scientific pipeline depend
on a fragile `Makefile` when Nextflow's process model, executor support, and
resume semantics are a better fit.

Do not force Nextflow onto a one-command script or a simple repository quality
workflow. The orchestration layer should earn its complexity.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the scientific workflow steps, data dependencies, parameters, and
   expected outputs.
3. Decide whether the workflow is simple enough for scripts or needs Nextflow.
4. Keep scientific code in scripts, modules, or executables; keep Nextflow
   responsible for orchestration.
5. Define a tiny local test input before scaling to larger data or HPC runs.
6. State what the workflow runs, how to resume it, and which profiles were
   validated.

Prefer incremental workflow extraction over rewriting the whole project at
once.

## Recommended Layout

A practical Nextflow-oriented layout is:

```text
main.nf
nextflow.config
bin/
  helper-script
conf/
  local.config
  hpc.config
data/
  README.md
examples/
  tiny/
results/
  .gitignore
```

Adjust to existing repository conventions. Do not create empty directories
without near-term use.

## Nextflow Structure

- Keep `main.nf` readable and focused on high-level workflow structure.
- Put executor, container, resource, and profile settings in
  `nextflow.config` or included config files.
- Expose scientific parameters through `params`, not hardcoded paths.
- Use named processes with clear input and output contracts.
- Keep process scripts small; move reusable logic into version-controlled
  scripts or package code.
- Prefer explicit `publishDir` behavior over unclear output side effects.

The workflow should make it obvious which files are inputs, intermediates,
published results, and logs.

## Profiles and Portability

- Provide a small `local` profile for laptop or CI smoke tests.
- Add HPC or cloud profiles only when the project has a real execution target.
- Keep site-specific account, partition, queue, reservation, and filesystem
  details out of public generic defaults.
- Document which profile was tested and which values users must adapt.
- Keep resource requests conservative for example profiles.

Profile names should describe execution context, not one user's machine.

## Containers and Environments

- Prefer containers for workflow-level portability when dependencies are
  non-trivial.
- Keep container image names, tags, or digests explicit.
- Separate container build instructions from workflow execution instructions.
- Document when host modules, MPI, GPU drivers, or filesystem mounts remain
  outside the container boundary.
- Avoid relying on unpinned `latest` images for reproducible workflows.

Container guidance should align with `scientific-container-workflows` if that
skill is added later.

## Inputs, Outputs, and Resume Behavior

- Provide a tiny input set that exercises the workflow quickly.
- Avoid overwriting durable results without an explicit output directory.
- Explain how `-resume` is expected to work and when users should not use it.
- Keep temporary work directories separate from published outputs.
- Record command line, profile, config, code version, and key parameters when
  outputs are meant to be auditable.

Nextflow's cache is useful, but it is not a substitute for clear provenance.

## Validation and CI

- Add a tiny local smoke test when the workflow is part of the repository
  contract.
- Keep CI workflow tests small enough to run on generic hosted runners.
- Validate syntax and a minimal execution path before claiming the workflow is
  usable.
- Do not put full scientific production runs in default CI.
- Capture enough logs to diagnose failed processes without rerunning the whole
  workflow blindly.

For larger workflows, CI should prove structure and basic behavior, not
scientific completeness.

## Failure Diagnostics

- Preserve Nextflow logs and failed process command files when diagnosing.
- Inspect `.command.sh`, `.command.err`, `.command.out`, and trace reports when
  available before changing resource settings.
- Distinguish workflow wiring errors from scientific-code failures.
- Change one dimension at a time: input, container, profile, resource request,
  or process script.
- Prefer fixing the smallest reproducible failing example before scaling out.

Clear failure diagnosis is one of the reasons to prefer Nextflow over a large
chain of shell scripts.

## Anti-Patterns

- encoding the main scientific workflow as a long, fragile `Makefile`;
- putting substantial scientific logic directly inside process heredocs;
- hardcoding user-local absolute paths;
- committing Nextflow work directories, caches, or generated results;
- publishing example configs with real private accounts or allocations;
- adding many profiles that nobody has tested;
- treating `-resume` as a provenance mechanism.

## Validation Defaults

- Run the smallest available workflow example locally when practical.
- Run `nextflow run main.nf -profile local` or the repository's documented
  equivalent for smoke validation.
- Check that generated outputs land in documented output directories.
- Verify `.gitignore` excludes work directories, caches, and generated results.
- If Nextflow is unavailable, validate the file structure and state that runtime
  validation was not performed.

## Output Expectations

When using this skill, briefly note:

- which workflow steps, parameters, profiles, or outputs were added or changed;
- whether Nextflow is now the primary workflow engine or only one option;
- which tiny local run or syntax checks were validated;
- what remains site-specific, large-scale, or untested.
