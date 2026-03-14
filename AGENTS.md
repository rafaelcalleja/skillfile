# AGENTS.md

## Project overview

Skillfile is a skill for AI coding agents that manages the installation and versioning of other skills from external git repositories. It uses a declarative YAML config and a lockfile with commit hashes for reproducibility.

## Directory structure

```
skills/skillfile/
├── SKILL.md           — main skill instructions
├── STANDARDS.md        — patterns for building workflows/skills
├── schemas/            — JSON schemas for YAML validation
└── scripts/            — Python validation script
```

## How to work on this project

- **SKILL.md** is written in natural language for LLM agents. It is NOT a script.
- **STANDARDS.md** is a living document — add new patterns when discovered.
- All YAML config files must have a corresponding JSON Schema in `schemas/`.
- All changes to YAML schemas must keep the validation script working.

## Testing changes

Run the validation script to check schemas are correct:

```bash
python3 skills/skillfile/scripts/validate_skills.py
```

Requires `pyyaml` and `jsonschema` Python packages.

## Before committing

1. Verify the validation script runs without errors
2. Review STANDARDS.md — does this change introduce a new pattern?
3. Ensure SKILL.md stays in natural language, no bash scripts embedded
