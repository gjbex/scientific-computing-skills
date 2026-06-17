#!/usr/bin/env python3
"""Update plugin and citation version metadata together."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?"
    r"(?:\+[0-9A-Za-z.-]+)?$"
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update .codex-plugin/plugin.json and CITATION.cff versions."
    )
    parser.add_argument("version", help="Semantic version, for example 0.2.0")
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Release date in YYYY-MM-DD format. Default: today.",
    )
    parser.add_argument("plugin_root", nargs="?", default=".")
    args = parser.parse_args()

    if not SEMVER_RE.fullmatch(args.version):
        raise SystemExit("version must use semantic versioning, for example 0.2.0")
    if not DATE_RE.fullmatch(args.date):
        raise SystemExit("--date must use YYYY-MM-DD format")

    root = Path(args.plugin_root)
    update_plugin_manifest(root / ".codex-plugin" / "plugin.json", args.version)
    update_citation(root / "CITATION.cff", args.version, args.date)
    print(f"Updated release metadata to {args.version} ({args.date})")


def update_plugin_manifest(path: Path, version: str) -> None:
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path} is not valid JSON: {exc}") from exc

    if not isinstance(manifest, dict):
        raise SystemExit(f"{path} must contain a JSON object")

    manifest["version"] = version
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def update_citation(path: Path, version: str, release_date: str) -> None:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise SystemExit(f"missing {path}") from exc

    text, version_count = re.subn(r"(?m)^version: .*$", f"version: {version}", text)
    text, date_count = re.subn(
        r"(?m)^date-released: .*$", f"date-released: {release_date}", text
    )
    if version_count != 1:
        raise SystemExit(f"{path} must contain exactly one version field")
    if date_count != 1:
        raise SystemExit(f"{path} must contain exactly one date-released field")

    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
