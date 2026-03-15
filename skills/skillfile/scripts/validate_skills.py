#!/usr/bin/env python3
"""Validate skills YAML files against their JSON schemas."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import validate, ValidationError

WORKFLOWS_DIR = Path(__file__).resolve().parent.parent
SCHEMAS_DIR = WORKFLOWS_DIR / "references"

FILES_TO_VALIDATE = [
    ("skills.yaml", "skills.schema.json", True),       # required
    ("skills-lock.yaml", "skills-lock.schema.json", False),  # optional (first-time install)
]


def validate_file(yaml_file: Path, schema_file: Path) -> list[str]:
    errors = []

    if not yaml_file.exists():
        errors.append(f"{yaml_file.name}: file not found")
        return errors

    if not schema_file.exists():
        errors.append(f"{schema_file.name}: schema not found")
        return errors

    with open(schema_file) as f:
        schema = json.load(f)

    with open(yaml_file) as f:
        data = yaml.safe_load(f)

    if data is None:
        errors.append(f"{yaml_file.name}: file is empty")
        return errors

    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        errors.append(f"{yaml_file.name}: {e.message}")

    return errors


def main():
    all_errors = []

    for yaml_name, schema_name, required in FILES_TO_VALIDATE:
        yaml_path = WORKFLOWS_DIR / yaml_name
        schema_path = SCHEMAS_DIR / schema_name

        if not yaml_path.exists() and not required:
            print(f"⏭️  {yaml_name} not found (optional, skipped)")
            continue

        errors = validate_file(yaml_path, schema_path)
        all_errors.extend(errors)

        if not errors and yaml_path.exists():
            print(f"✅ {yaml_name} is valid")

    if all_errors:
        for error in all_errors:
            print(f"❌ {error}")
        sys.exit(1)

    print("\nAll files valid.")


if __name__ == "__main__":
    main()
