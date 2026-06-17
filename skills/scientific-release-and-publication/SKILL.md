---
name: scientific-release-and-publication
description: Prepare scientific software for public release and citation,
  including versioning, release notes, archival metadata, DOI workflows, and
  publication-ready repository hygiene.
---

# Scientific Release And Publication

Use this skill when preparing scientific software, workflows, datasets, or
Codex skill/plugin distributions for public release, citation, archival, or
reuse by other researchers and developers.

Repository `AGENTS.md` instructions take precedence over this skill.

## Purpose

Apply a pragmatic default for:

- release readiness checks for scientific software repositories;
- versioning, tags, changelogs, and release notes;
- citation metadata and attribution files;
- archival DOI workflows such as Zenodo;
- packaging release artifacts without generated junk or private details;
- making examples, validation commands, and documentation consistent.

## When To Use

Use this skill when:

- a repository is being made public;
- a versioned release, tag, or GitHub Release is being prepared;
- citation metadata, license files, or attribution notices need to be added or
  updated;
- a DOI or software archive should be created;
- release artifacts must be reviewed for reproducibility and privacy;
- documentation needs to describe installation, validation, and citation.

Do not use this skill as a substitute for legal review, formal publication
policy, or project-governance decisions that require maintainers to choose
licensing or authorship terms.

## Working Approach

When this skill applies:

1. Read the repository `AGENTS.md` first, if present.
2. Identify the intended release audience: users, collaborators, reviewers,
   package consumers, or archival repositories.
3. Check the release contract: install, run, test, cite, and reproduce.
4. Keep source, generated artifacts, release assets, and archival metadata
   clearly separated.
5. Align version, citation, license, README, changelog, and release notes.
6. State what was validated and what remains maintainer policy.

Prefer small, reviewable release-preparation changes over last-minute broad
reorganization.

## Release Metadata

A public scientific release should normally include:

- `README.md` with purpose, installation, usage, validation, and citation
  guidance;
- `LICENSE` with the selected license text;
- `NOTICE` when attribution notices must be preserved;
- `CITATION.cff` for GitHub and citation tooling;
- changelog or release notes when users need to understand changes;
- version metadata in package, plugin, or workflow files;
- repository URL and, when available, DOI metadata.

Keep metadata consistent across files. If the public repository URL changes,
update both human-facing and machine-readable metadata.

## Versioning and Tags

- Use semantic versioning when the project has software-like compatibility
  expectations.
- Keep release tags aligned with package or plugin version fields.
- When a repository provides a release-metadata helper, use it instead of
  hand-editing version fields across multiple files.
- For plugin distributions, keep the plugin manifest version and
  `CITATION.cff` version/date metadata aligned, and add or run a validator that
  fails on drift.
- Do not bump versions only to force local cache invalidation.
- Keep pre-release labels explicit for experimental releases.
- Document breaking changes, new features, fixes, and known limitations.

For research prototypes, the versioning policy may be lightweight, but it
should still be explicit enough that citations can identify a release.

## Citation Metadata

Use `CITATION.cff` for preferred citation information.

At minimum, consider:

- `cff-version`;
- `message`;
- `title`;
- `type`;
- `authors`;
- `version`;
- `date-released`;
- `license`;
- `repository-code`;
- `url`;
- `doi`, once an archival DOI exists.

Do not invent DOI values. Add DOI metadata only after an archive or publisher
has assigned it.

## DOI and Archival Workflows

When using Zenodo or a similar archive:

- connect the public repository to the archive before creating the release when
  possible;
- create a GitHub Release from a clean tag;
- verify the archive captured the intended release;
- add the assigned DOI to `CITATION.cff` and README citation guidance;
- do not archive generated junk, secrets, or oversized files unintentionally.

If the DOI is not yet available, leave a clear follow-up rather than adding a
placeholder.

## Release Artifacts

- Keep generated build outputs and caches out of source control.
- Include generated artifacts only when they are part of the release contract,
  such as generated documentation or checked-in definition files.
- Do not commit large binary images such as `.sif` containers unless there is a
  documented exceptional reason.
- Prefer release assets, registries, archives, or documented external storage
  for large artifacts.
- Verify release artifacts can be traced back to source, recipes, inputs, or
  documented generation commands.

Release artifacts should be reproducible or clearly provenance-tracked.

## Privacy and Public-Readiness Checks

Before publishing or releasing, scan for:

- API keys, tokens, passwords, private keys, and credentials;
- local absolute paths and user-specific scratch directories;
- private hostnames, allocation names, account IDs, or scheduler details;
- generated caches, bytecode, logs, and temporary files;
- large data files that should live outside Git;
- accidental personal information beyond intentional attribution metadata.

For scientific/HPC projects, site-specific examples should be generic unless
the site details are intentionally public documentation.

## Documentation Consistency

Release documentation should answer:

- what the project does;
- who should use it;
- how to install or set it up;
- how to run a minimal example;
- how to validate the installation;
- how to cite the work;
- where limitations, generated artifacts, and external dependencies are
  documented.

Keep README, examples, validation commands, CI, and release notes aligned.

## Validation Defaults

- Run the documented test or validation commands.
- Run packaging, plugin, or metadata validators if the repository provides
  them.
- Check that version fields, tags, and citation metadata agree.
- Inspect `git status --short` before release.
- Scan tracked files for generated artifacts and obvious secrets.
- Confirm public URLs resolve or are at least syntactically correct.

If a release step depends on external services such as GitHub Releases or
Zenodo, state whether it was performed or left for the maintainer.

## Anti-Patterns

- publishing a repository before license and citation metadata are chosen;
- adding placeholder DOI values;
- shipping release notes that do not match the code;
- committing generated caches or large binary artifacts by accident;
- hiding the only validation command in CI logs instead of documenting it;
- changing authorship, license, or governance policy without maintainer input;
- treating a GitHub repository URL as equivalent to an archival DOI.

## Output Expectations

When using this skill, briefly note:

- which release, citation, license, version, or archive metadata changed;
- whether validation and public-readiness checks were run;
- what release artifacts or generated files were included or excluded;
- which steps remain for maintainers, such as creating a tag, GitHub Release,
  or DOI archive.
