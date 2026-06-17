# Contributions

Contributions are welcome when they keep this plugin focused, portable, and
useful for scientific-computing repository work.

## Scope

This repository packages Codex skills for scientific software engineering:
build systems, CI, benchmarking, profiling, numerical review, testing,
documentation, reproducibility, package management, data formats, and parallel
debugging.

Support skills are acceptable when they directly improve real scientific
repository work. Current examples are Git refactor hygiene and repository
baseline setup.

Out of scope:

- site-specific HPC login, scheduler, filesystem, account, or allocation
  workflows;
- private cluster facts, hostnames, credentials, or local machine paths;
- broad general-productivity skills that do not materially support scientific
  codebase work;
- generated caches, build products, bytecode, logs, or local environment files.

## Skill Changes

Each skill lives under:

```text
skills/<skill-name>/SKILL.md
```

When adding or changing a skill:

- keep the skill boundary narrow and triggerable;
- prefer portable guidance over site-specific examples;
- respect repository `AGENTS.md` instructions when the skill says they take
  precedence;
- update `skills/<skill-name>/agents/openai.yaml` when the user-facing summary
  or default prompt should change;
- update `README.md` when the public skill list or boundary guidance changes.

## Repository Hygiene

Keep branches single-purpose and commits atomic. A branch should be easy to
summarize as one fix, feature, refactor, documentation update, release chore, or
validation change. Split unrelated work into separate commits or branches.

Before starting implementation, inspect the current branch and worktree:

```bash
git status --short --branch
```

Create a focused branch from the intended integration branch for the new
concern unless you are already on an appropriate topic branch. This repository
currently targets `development`; in other projects the target might be `main`,
`trunk`, or a release branch:

```bash
git switch development
git pull --ff-only
git switch -c <short-topic-branch>
```

If the work starts to drift from the branch's intent, pause before adding the
second concern. Either keep the current branch focused or start another branch
for the new concern.

Use Git rename hygiene for reorganizations:

```bash
git status --short
git mv <old-path> <new-path>
git status --short
```

If a plain move already happened, stage the affected paths and verify Git
detects renames rather than unrelated delete/add noise:

```bash
git add -A <paths>
git diff --cached --summary
```

Keep generated files out of commits. In particular, do not commit
`__pycache__/`, `*.pyc`, virtual environments, build directories, logs, or local
secret/config files.

Before opening a pull request, inspect the diff for unrelated themes, generated
artifacts, large mechanical changes mixed with semantic edits, or changes that
cross multiple skill boundaries without one clear purpose.

## Validation

Run the same checks used by CI before opening a pull request:

```bash
python3 tools/validate_plugin.py .
python3 tools/validate_skills.py skills
python3 tools/validate_docs.py .
python3 -m py_compile skills/scientific-cli-benchmark/scripts/simple_benchmark.py tools/bump_version.py tools/validate_plugin.py tools/validate_skills.py tools/validate_docs.py
```

If you add new Python scripts, include them in the compile command and the
GitHub Actions workflow.

## Attribution and Licensing

By contributing, you agree that your contribution is provided under the Apache
License, Version 2.0, unless explicitly stated otherwise in the contribution.

Preserve attribution notices in `NOTICE` where applicable. If you use or derive
work from this project, cite it using `CITATION.cff`.

## Pull Request Checklist

- The skill or support-skill boundary is clear.
- The branch has one purpose, and commits are atomic enough to review or revert
  independently.
- Public documentation is updated when users need to know about the change.
- Validation commands pass locally.
- No generated artifacts or local-only files are included.
- No private hostnames, credentials, API tokens, local paths, or allocation
  details are included.
