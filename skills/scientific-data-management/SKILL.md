---
name: scientific-data-management
description: Manage scientific data, reference inputs, generated outputs,
  checksums, provenance, large artifacts, and Git boundaries, with optional DVC
  usage when it is available and appropriate.
---

# Scientific Data Management

Use this skill when a scientific repository needs clear boundaries for raw
data, processed data, generated outputs, reference fixtures, large artifacts, or
provenance.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- separating source code from raw data, derived data, and generated artifacts;
- deciding which data should be tracked by Git;
- managing large files, checksums, manifests, and provenance;
- keeping reference data useful without bloating the repository;
- using DVC when it is available and materially improves data versioning.

## When To Use

Use this skill when:

- a project mixes source files, raw data, processed data, results, and caches;
- reference inputs or golden outputs need to be organized;
- generated outputs or checkpoints are at risk of being committed accidentally;
- data provenance, checksums, or retention policy is unclear;
- large data files need a versioning or storage strategy;
- DVC, Git LFS, object storage, or external archives are being considered.

Do not use this skill to replace scientific file-format design. Use
`scientific-io-and-data-formats` when the structure of a file format or schema
is the main issue.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify data classes: raw inputs, immutable references, processed data,
   generated outputs, caches, checkpoints, fixtures, and release artifacts.
3. Decide what belongs in Git, what belongs in external storage, and what is
   reproducible from commands.
4. Add or update manifests, checksums, README files, or ignore rules where they
   reduce ambiguity.
5. Prefer small representative fixtures over large hidden datasets in tests.
6. State what data are durable, generated, ignored, externally stored, or
   intentionally tracked.

Do not move or delete user data without explicit confirmation.

## Data Classes

Use explicit names and documentation for common categories:

- raw data: original inputs that should not be edited in place;
- reference data: small trusted inputs or outputs used for tests or examples;
- processed data: derived data that may be reproducible from raw inputs;
- generated results: outputs from simulations, analyses, benchmarks, or
  workflows;
- checkpoints: restart state, usually large and runtime-specific;
- caches and scratch: reproducible or temporary tool outputs;
- release artifacts: curated files distributed with a versioned release.

The goal is to make it obvious what humans edit, what tools generate, and what
must be preserved.

## Git Boundaries

- Keep source code, small fixtures, schemas, manifests, and documentation in
  Git.
- Keep large datasets, checkpoints, caches, and bulk generated outputs out of
  Git unless there is a deliberate release reason.
- Track small reference datasets only when they are stable, documented, and
  useful for tests or examples.
- Use `.gitignore` for reproducible outputs, local downloads, work directories,
  and cache files.
- Avoid broad ignore rules that hide source files or important metadata.

If generated files are committed, document why they are part of the repository
contract and how to regenerate them.

## Provenance and Manifests

For important data, capture:

- source or origin;
- date or version;
- license or access constraints;
- checksum or content hash;
- preprocessing command or workflow;
- software version or commit used to generate derived data;
- units, schema, dimensions, and important conventions.

A lightweight `data/README.md`, manifest file, or checksums file is often enough
for small projects.

## Checksums

- Use checksums for externally stored data, downloaded inputs, and release
  artifacts.
- Prefer stable algorithms such as SHA-256 for new manifests.
- Store checksums next to data manifests or download instructions.
- Verify checksums before running expensive analyses when data corruption would
  waste compute or invalidate results.

Checksums prove identity, not scientific correctness.

## DVC Usage

DVC is a good option when it is available and the project needs reproducible
large-data tracking, external storage, or data-aware pipeline stages.

Use DVC when:

- data are too large or too changeable for Git;
- multiple data versions must be tied to code commits;
- remote storage can be configured for collaborators or CI;
- pipeline stages and outputs need explicit dependency tracking;
- users can reasonably install and use DVC in the target environment.

Do not require DVC for a project with only small fixtures or simple downloaded
example data. DVC should reduce ambiguity, not add ceremony.

## DVC Patterns

When DVC is appropriate:

- track large data or generated artifacts with DVC, not Git;
- commit `.dvc` metadata and `dvc.lock` or pipeline metadata when they define
  the project contract;
- keep DVC remotes documented but do not commit private credentials;
- make `dvc pull`, `dvc repro`, and `dvc status` behavior clear in the README;
- verify `.gitignore` entries generated by DVC do not hide source files;
- document what data are required for tests, examples, and full workflows.

Useful checks:

```bash
dvc status
dvc doctor
dvc repro --dry
```

Use the exact commands supported by the repository's DVC version. If DVC is not
installed, inspect DVC metadata and state that runtime validation was not
performed.

## Alternatives to DVC

Consider alternatives when they fit better:

- Git LFS for moderately large files that should behave like repository
  artifacts;
- package or release assets for curated versioned examples;
- object storage with checksummed download scripts for large public datasets;
- institutional archives, Zenodo, or domain repositories for citable datasets;
- workflow-managed scratch or project storage for generated production outputs.

Choose the lightest mechanism that preserves reproducibility and access.

## Test Fixtures and Reference Data

- Prefer tiny, interpretable fixtures for automated tests.
- Keep golden outputs small and provenance-documented.
- Record how reference outputs were generated.
- Avoid large opaque binary golden files unless they are unavoidable.
- Separate correctness fixtures from benchmark datasets.

Test data should make failures diagnosable.

## Workflow Outputs and Checkpoints

- Keep workflow work directories, caches, and checkpoints out of Git by
  default.
- Use stable output directories for durable results.
- Avoid overwriting results without an explicit run identifier or output path.
- Store summaries, manifests, or hashes when full outputs are too large for
  review.
- Document retention expectations for expensive generated data.

Use `scientific-workflow-automation` and `scientific-reproducibility` for
workflow-level implementation details.

## Validation Defaults

- Inspect tracked large files and generated artifacts before finishing changes.
- Check `.gitignore` does not hide source files that should be tracked.
- Verify small fixtures or manifests are readable and documented.
- Run checksum or DVC status checks when the repository uses them.
- Run a tiny workflow or test that consumes the managed data when practical.

If validation requires external data access, state whether access was available.

## Anti-Patterns

- committing raw production datasets without a deliberate policy;
- mixing raw data, processed data, generated results, and caches in one
  directory;
- tracking huge checkpoints in Git;
- ignoring all data files so fixtures silently disappear;
- using DVC without documenting remotes or pull/repro commands;
- committing private DVC remote credentials or local storage paths;
- treating generated data as source without regeneration instructions.

## Output Expectations

When using this skill, briefly note:

- which data classes were identified;
- which files are tracked by Git, DVC, Git LFS, external storage, or ignored;
- what manifests, checksums, README notes, or ignore rules changed;
- which data validation, checksum, DVC, or workflow checks were run;
- what data access, retention, or provenance questions remain.
