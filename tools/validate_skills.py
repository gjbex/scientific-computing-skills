#!/usr/bin/env python3
"""Validate bundled skill frontmatter without external dependencies."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate bundled Codex skills.")
    parser.add_argument("skills_root", nargs="?", default="skills")
    args = parser.parse_args()

    skills_root = Path(args.skills_root)
    errors = validate_skills(skills_root)
    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Skill validation passed: {skills_root.resolve()}")


def validate_skills(skills_root: Path) -> list[str]:
    if not skills_root.is_dir():
        return [f"{skills_root} is not a directory"]

    errors: list[str] = []
    skill_dirs = sorted(path for path in skills_root.iterdir() if path.is_dir())
    if not skill_dirs:
        return [f"{skills_root} contains no skill directories"]

    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return [f"{skill_md}: frontmatter must start at first byte"]

    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if match is None:
        return [f"{skill_md}: invalid frontmatter delimiters"]

    frontmatter = parse_frontmatter(match.group(1), skill_md, errors)
    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if name is None:
        errors.append(f"{skill_md}: missing name")
    elif not NAME_RE.fullmatch(name):
        errors.append(f"{skill_md}: invalid skill name {name!r}")
    elif name != skill_dir.name:
        errors.append(f"{skill_md}: name {name!r} does not match directory")

    if description is None:
        errors.append(f"{skill_md}: missing description")
    elif len(description) > 1024:
        errors.append(f"{skill_md}: description exceeds 1024 characters")
    elif "<" in description or ">" in description:
        errors.append(f"{skill_md}: description must not contain angle brackets")

    return errors


def parse_frontmatter(
    frontmatter: str,
    skill_md: Path,
    errors: list[str],
) -> dict[str, str]:
    values: dict[str, str] = {}
    current_key: str | None = None

    for line_number, line in enumerate(frontmatter.splitlines(), start=2):
        if not line.strip():
            continue
        if line.startswith(" ") or line.startswith("\t"):
            if current_key is None:
                errors.append(f"{skill_md}:{line_number}: orphan continuation line")
                continue
            values[current_key] = f"{values[current_key]} {line.strip()}".strip()
            continue

        if ":" not in line:
            errors.append(f"{skill_md}:{line_number}: expected key: value")
            current_key = None
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key not in {"name", "description", "license", "allowed-tools", "metadata"}:
            errors.append(f"{skill_md}:{line_number}: unexpected key {key!r}")
        values[key] = value
        current_key = key

    return values


if __name__ == "__main__":
    main()
