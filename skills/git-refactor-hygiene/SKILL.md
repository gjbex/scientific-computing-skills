---
name: git-refactor-hygiene
description: Use when reorganizing, moving, renaming, staging, committing, or
  preparing pull requests in a Git worktree, especially to preserve rename
  history and keep branches, commits, and PRs single-purpose.
---

# Git Refactor Hygiene

## Workflow

1. Check status first with `git status --short`.
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
- Keep commits atomic: each commit should explain one coherent reason for the
  changed files and should be revertible without taking unrelated work with it.
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
