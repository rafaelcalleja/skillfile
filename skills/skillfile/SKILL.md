---
name: skillfile
description: Use when managing agent skills installation, updates, or version pinning from external git repositories. Use this skill whenever the user mentions installing skills, updating skills, checking for updates, listing installed skills, removing skills, skills.yaml, skills-lock.yaml, /skillfile, or any conversation about managing agent tool packages — even if they don't explicitly ask for 'skillfile'.
---

# Skillfile

Manages agent skills using `npx skills@1.4.5` with a declarative YAML config and a lockfile for reproducibility. Each skill repo targets specific agents (claude-code, cursor, etc.).

> All commands use `npx -y skills@1.4.5`. The skill's behavior depends on this version — using a different one may produce unexpected results.

## Quick Reference

| Operation | What it does | Modifies lockfile? |
|-----------|-------------|-------------------|
| **Install** | Installs from lockfile, filtered by agent | No (except new entries) |
| **Check** | Compares lockfile vs remote HEAD | No |
| **Update** | Installs latest from branch | Yes |
| **List** | Shows lockfile contents | No |
| **Remove** | Removes a skill | Yes |

For detailed step-by-step procedures, read `references/operations.md`.

## Files

| File | Purpose | Schema |
|------|---------|--------|
| `skills.yaml` | Repos, branches, target agents | `references/skills.schema.json` |
| `skills-lock.yaml` | Pinned commit hashes | `references/skills-lock.schema.json` |

Both live in this skill's directory.

## Setup

If `skills.yaml` doesn't exist, create it:

```yaml
# Skills Configuration
superpowers:
  repo: https://github.com/obra/superpowers@main
  agents: [claude-code, cursor]
```

If the project lacks an `AGENTS.md` at root, create one with a Skill Management section pointing to this skill's config.

## Validate

Before any operation, run `python3 scripts/validate_skills.py` from this skill's directory. Validation catches malformed config before it causes silent failures downstream — continuing with bad config wastes time cloning repos that can't install correctly. If validation fails, stop and tell the user what went wrong.

## Operations

Read `references/operations.md` for the detailed procedure of whichever operation the user requested (Install, Check, Update, List, Remove, Search).
