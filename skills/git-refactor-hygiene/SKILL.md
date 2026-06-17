---
name: git-refactor-hygiene
description: Use when reorganizing, moving, renaming, staging, committing, or
  preparing pull requests in a Git worktree, especially to preserve rename
  history and keep branches, commits, and PRs single-purpose.
---

# Git Refactor Hygiene

## Workflow

1. Check status first with `git status --short`.
1. Fetch remote refs before branch or pull-request decisions when network
   access is available, so comparisons use current `origin/*` state rather than
   stale local tracking refs.
1. Before implementation starts, confirm the work is on a focused branch for
   the requested concern. If it is still on the project's target branch, such
   as `main`, `trunk`, or `development`, update that intended base with
   `git pull --ff-only` and create a short-lived topic branch from it unless
   the user explicitly wants to work in place.
1. Check the current branch and compare it with its base when practical before
   committing or preparing a pull request.
1. For tracked files or directories, use `git mv <old> <new>` rather than plain
   `mv`.
1. If a plain `mv` already happened, stage with `git add -A <paths>` and verify
   Git reports `R` renames, not just `D` plus `A`.
1. Leave unrelated dirty or untracked files untouched unless the user
   explicitly asks otherwise.
1. Stage by path or hunk so each commit represents one purpose.
1. Verify with `git status --short` and, when needed,
   `git diff --cached --summary`.

## Branch and Commit Scope

- Keep branches single-purpose: one bug fix, feature, refactor, documentation
  update, release chore, or validation change.
- Use the repository's documented pull-request target as the base branch. Some
  projects use trunk-based development with PRs into `main`; others use
  `trunk`, `development`, or temporary release branches. Do not assume
  `development` is universal.
- A short-lived topic branch is the default for new implementation work, but a
  tiny mechanical release chore can be committed directly on an integration
  branch when the maintainer explicitly chooses that path and the diff is
  limited to the release metadata.
- Treat remote tracking branches as the source of truth for pull-request scope.
  Before opening or updating a PR, check the commit list and diff against the
  actual target branch, for example `git log --oneline origin/main..HEAD` or
  `git diff --stat origin/development...HEAD`.
- Keep commits atomic: each commit should explain one coherent reason for the
  changed files and should be revertible without taking unrelated work with it.
- Watch for scope drift while working. If the branch's diff starts to include a
  second concern, warn the user and propose either staying focused on the
  current concern or moving the new concern to a separate branch.
- Separate mechanical moves or generated refreshes from semantic edits when
  practical.
- If a change touches unrelated skill boundaries, build files, documentation,
  and release metadata at once, pause and explain whether those changes form one
  contract or should be split.
- Do not stage unrelated dirty files just because they are present in the
  worktree.

## Warning Triggers

Before committing, pushing, opening a pull request, or summarizing a branch,
warn the user when:

- `git status --short` shows unrelated modified or untracked files;
- the branch diff mixes independent concerns that could be reviewed or reverted
  separately;
- the branch includes commits already intended for the target branch because it
  was created from a local integration branch that was ahead of `origin/*`;
- a commit would combine file moves with substantial content changes;
- generated artifacts, caches, logs, or local environment files appear in the
  diff;
- the diff spans many directories or skill boundaries without a clear single
  purpose;
- the pull request would include cleanup, feature work, release metadata, and
  validation changes that are not part of the same repository contract.

When warning, name the files or themes causing the concern and suggest a split
such as separate commits, a follow-up branch, or leaving unrelated files
unstaged.

## Notes

- Prefer one move-focused commit separate from content edits when practical.
- If files are edited during the move, Git may still detect renames after
  staging, but check explicitly.
- Keep persistent scratch notes either ignored intentionally or outside the
  repository; do not stage them by accident.
- Ignored caches such as `__pycache__/` do not need to be removed for normal Git
  hygiene. Use `git status --short --ignored` or `git check-ignore -v <path>` if
  you need to verify that generated files are safely ignored.
