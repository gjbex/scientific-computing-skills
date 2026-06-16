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

## Validation

Run the same checks used by CI before opening a pull request:

```bash
python3 tools/validate_plugin.py .
python3 tools/validate_skills.py skills
python3 -m py_compile skills/scientific-cli-benchmark/scripts/simple_benchmark.py
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
- Public documentation is updated when users need to know about the change.
- Validation commands pass locally.
- No generated artifacts or local-only files are included.
- No private hostnames, credentials, API tokens, local paths, or allocation
  details are included.
