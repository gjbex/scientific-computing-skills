#!/usr/bin/env python3
"""Validate documentation cross-references that prevent workflow drift."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate repository docs.")
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.repo_root)
    errors = validate_docs(root)
    if errors:
        print("Documentation validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Documentation validation passed: {root.resolve()}")


def validate_docs(root: Path) -> list[str]:
    errors: list[str] = []
    readme = read_required(root / "README.md", errors)
    contributions = read_required(root / "CONTRIBUTIONS.md", errors)
    agents = read_required(root / "AGENTS.md", errors)

    if readme is not None:
        require_section(readme, "Development", "README.md", errors)
        require_section(readme, "Validation", "README.md", errors)
        require_text(
            readme,
            "python3 tools/validate_docs.py .",
            "README.md must document the docs validator",
            errors,
        )

    if contributions is not None:
        require_section(contributions, "Repository Hygiene", "CONTRIBUTIONS.md", errors)
        require_section(contributions, "Validation", "CONTRIBUTIONS.md", errors)

    if agents is not None:
        require_section(
            agents,
            "Development And Installation Checkouts",
            "AGENTS.md",
            errors,
        )
        require_text(
            agents,
            "Follow `README.md`",
            "AGENTS.md must point to README.md as the workflow source of truth",
            errors,
        )
        require_text(
            agents,
            "Follow `CONTRIBUTIONS.md`",
            "AGENTS.md must point to CONTRIBUTIONS.md as the hygiene source of truth",
            errors,
        )
        require_text(
            agents,
            "python3 tools/validate_docs.py .",
            "AGENTS.md must include the docs validator in validation commands",
            errors,
        )
        section = extract_section(agents, "Development And Installation Checkouts")
        if section is not None:
            for duplicated in (
                "~/plugins/scientific-computing-skills",
                "git switch development",
                "origin/development",
            ):
                if duplicated in section:
                    errors.append(
                        "AGENTS.md should reference README/CONTRIBUTIONS instead "
                        f"of duplicating workflow detail: {duplicated}"
                    )

    return errors


def read_required(path: Path, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"missing {path.name}")
    except OSError as exc:
        errors.append(f"could not read {path.name}: {exc}")
    return None


def require_section(text: str, heading: str, filename: str, errors: list[str]) -> None:
    if not re.search(rf"(?m)^## {re.escape(heading)}$", text):
        errors.append(f"{filename} must contain a '## {heading}' section")


def require_text(text: str, needle: str, message: str, errors: list[str]) -> None:
    if needle not in text:
        errors.append(message)


def extract_section(text: str, heading: str) -> str | None:
    match = re.search(
        rf"(?ms)^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        text,
    )
    if match is None:
        return None
    return match.group("body")


if __name__ == "__main__":
    main()
