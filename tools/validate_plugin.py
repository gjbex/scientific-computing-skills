#!/usr/bin/env python3
"""Validate the public plugin manifest with stdlib-only checks."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)\."
    r"(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z.-]+)?"
    r"(?:\+[0-9A-Za-z.-]+)?$"
)
PLUGIN_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")
HEX_COLOR_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a Codex plugin.")
    parser.add_argument("plugin_root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.plugin_root)
    errors = validate_plugin(root)
    if errors:
        print("Plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print(f"Plugin validation passed: {root.resolve()}")


def validate_plugin(root: Path) -> list[str]:
    errors: list[str] = []
    manifest_path = root / ".codex-plugin" / "plugin.json"
    if not manifest_path.is_file():
        return ["missing .codex-plugin/plugin.json"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"plugin.json is not valid JSON: {exc}"]

    if not isinstance(manifest, dict):
        return ["plugin.json must contain a JSON object"]

    reject_todo_markers(manifest, "$", errors)
    validate_manifest(root, manifest, errors)
    validate_citation_metadata(root, manifest, errors)
    return errors


def validate_manifest(root: Path, manifest: dict[str, Any], errors: list[str]) -> None:
    allowed = {
        "name",
        "version",
        "description",
        "author",
        "homepage",
        "repository",
        "license",
        "keywords",
        "skills",
        "interface",
    }
    for key in sorted(set(manifest) - allowed):
        errors.append(f"unexpected plugin.json field: {key}")

    name = require_string(manifest, "name", errors)
    if name and not PLUGIN_NAME_RE.fullmatch(name):
        errors.append("name must be lower-case hyphen-case and at most 64 characters")

    version = require_string(manifest, "version", errors)
    if version and not SEMVER_RE.fullmatch(version):
        errors.append("version must use semantic versioning")

    require_string(manifest, "description", errors)
    validate_author(manifest.get("author"), errors)
    require_string(manifest, "license", errors)
    validate_url_field(manifest, "homepage", errors)
    validate_url_field(manifest, "repository", errors)
    validate_keywords(manifest.get("keywords"), errors)
    validate_skills_path(root, manifest.get("skills"), errors)
    validate_interface(manifest.get("interface"), errors)


def validate_author(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("author must be an object")
        return
    for key in sorted(set(value) - {"name", "email", "url"}):
        errors.append(f"unexpected author field: {key}")
    require_string(value, "name", errors, prefix="author")
    if "email" in value:
        require_string(value, "email", errors, prefix="author")
    if "url" in value:
        validate_url_field(value, "url", errors, prefix="author")


def validate_keywords(value: Any, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append("keywords must be a non-empty array")
        return
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            errors.append(f"keywords[{index}] must be a non-empty string")


def validate_skills_path(root: Path, value: Any, errors: list[str]) -> None:
    if not isinstance(value, str) or not value.strip():
        errors.append("skills must be a non-empty string")
        return
    if value != "./skills/":
        errors.append("skills must be './skills/'")
    if not (root / "skills").is_dir():
        errors.append("skills directory does not exist")


def validate_interface(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("interface must be an object")
        return
    allowed = {
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
        "capabilities",
        "defaultPrompt",
        "brandColor",
    }
    for key in sorted(set(value) - allowed):
        errors.append(f"unexpected interface field: {key}")
    for key in (
        "displayName",
        "shortDescription",
        "longDescription",
        "developerName",
        "category",
    ):
        require_string(value, key, errors, prefix="interface")

    capabilities = value.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append("interface.capabilities must be a non-empty array")
    elif not all(isinstance(item, str) and item.strip() for item in capabilities):
        errors.append("interface.capabilities entries must be non-empty strings")

    prompts = value.get("defaultPrompt")
    if not isinstance(prompts, list) or not prompts:
        errors.append("interface.defaultPrompt must be a non-empty array")
    elif len(prompts) > 3:
        errors.append("interface.defaultPrompt should contain at most 3 entries")
    elif not all(isinstance(item, str) and item.strip() for item in prompts):
        errors.append("interface.defaultPrompt entries must be non-empty strings")

    color = value.get("brandColor")
    if color is not None and (
        not isinstance(color, str) or not HEX_COLOR_RE.fullmatch(color)
    ):
        errors.append("interface.brandColor must use #RRGGBB format")


def require_string(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
    *,
    prefix: str | None = None,
) -> str | None:
    field = f"{prefix}.{key}" if prefix else key
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{field} must be a non-empty string")
        return None
    return value.strip()


def validate_url_field(
    payload: dict[str, Any],
    key: str,
    errors: list[str],
    *,
    prefix: str | None = None,
) -> None:
    value = payload.get(key)
    if value is None:
        return
    field = f"{prefix}.{key}" if prefix else key
    if not isinstance(value, str) or not value.startswith("https://"):
        errors.append(f"{field} must be an https:// URL")


def validate_citation_metadata(
    root: Path, manifest: dict[str, Any], errors: list[str]
) -> None:
    citation_path = root / "CITATION.cff"
    if not citation_path.exists():
        return

    try:
        citation = citation_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"could not read CITATION.cff: {exc}")
        return

    citation_version = extract_cff_scalar(citation, "version", errors)
    if citation_version and manifest.get("version") != citation_version:
        errors.append(
            "CITATION.cff version must match .codex-plugin/plugin.json version"
        )

    release_date = extract_cff_scalar(citation, "date-released", errors)
    if release_date and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", release_date):
        errors.append("CITATION.cff date-released must use YYYY-MM-DD format")


def extract_cff_scalar(text: str, key: str, errors: list[str]) -> str | None:
    matches = re.findall(rf"(?m)^{re.escape(key)}:\s*(.+?)\s*$", text)
    if not matches:
        errors.append(f"CITATION.cff missing {key}")
        return None
    if len(matches) > 1:
        errors.append(f"CITATION.cff contains multiple {key} fields")
        return None
    # Normalize by stripping both single and double quotes from the scalar value
    return matches[0].strip().strip('"\'')



def reject_todo_markers(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, str):
        if "[TODO:" in value:
            errors.append(f"{path} contains a TODO placeholder")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            reject_todo_markers(item, f"{path}[{index}]", errors)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            reject_todo_markers(item, f"{path}.{key}", errors)


if __name__ == "__main__":
    main()
