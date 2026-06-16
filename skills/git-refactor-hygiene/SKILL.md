---
name: git-refactor-hygiene
description: Use when reorganizing, moving, or renaming tracked files/directories in a Git worktree, especially to preserve rename history and avoid delete/add staging noise.
---

# Git Refactor Hygiene

## Workflow

1. Check status first with `git status --short`.
1. For tracked files or directories, use `git mv <old> <new>` rather than plain
   `mv`.
1. If a plain `mv` already happened, stage with `git add -A <paths>` and verify
   Git reports `R` renames, not just `D` plus `A`.
1. Leave unrelated dirty or untracked files untouched unless the user
   explicitly asks otherwise.
1. Verify with `git status --short` and, when needed,
   `git diff --cached --summary`.

## Notes

- Prefer one move-focused commit separate from content edits when practical.
- If files are edited during the move, Git may still detect renames after
  staging, but check explicitly.
