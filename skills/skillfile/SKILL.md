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

## Preferences

If `config.json` exists in this skill's directory, read it for default preferences:

```json
{
  "default_agent": "",
  "temp_dir": "/tmp"
}
```

- **`default_agent`**: Skip asking the user which agent on Install if set (e.g., `"claude-code"`)
- **`temp_dir`**: Where to create temporary clone directories

If `config.json` doesn't exist, ask the user when needed and offer to save their preference.

## Validate

Before any operation, run `python3 scripts/validate_skills.py` from this skill's directory. Validation catches malformed config before it causes silent failures downstream — continuing with bad config wastes time cloning repos that can't install correctly. If validation fails, stop and tell the user what went wrong.

## Gotchas

- ❌ **Unquoted timestamps** break YAML silently — `installed: 2026-03-14T07:18:30+01:00` gets auto-parsed as a datetime object. Always quote: `installed: "2026-03-14T07:18:30+01:00"`
- ❌ **Clone cuelga o falla** — el protocolo viene de la URL en `repo:`. Si el clone falla (HTTPS sin credenciales, SSH sin clave), reintenta convirtiendo al protocolo alternativo: `https://github.com/org/repo` ↔ `git@github.com:org/repo.git`
- ❌ **Wrong `npx skills` version** produces unexpected results — always use `npx -y skills@1.4.5`, never skip the version pin
- ❌ **Install doesn't update** — it only adds new repos to the lockfile. Users expecting Install to fetch latest are often looking for Update
- ❌ **`npx skills add` doesn't support branches** — you must clone the repo at the desired branch first, then point `add` at the local clone
- ✅ **Always validate before any operation** — malformed YAML causes silent failures downstream
- ✅ **Always clean up temp directories** after cloning, even on failure

## Helper Script

The `scripts/install-repo.sh` script handles the clone → install → cleanup cycle for a single repo. Use it to avoid reconstructing the workflow each time:

```bash
scripts/install-repo.sh <repo-url> <branch> <commit|latest> <agent> [temp-dir]
```

This is optional — the operations in `references/operations.md` describe the same workflow in natural language.

## Operation Log

After every Install, Update, or Remove operation, append an entry to `operations.log` in this skill's directory:

```
2026-03-18T16:30:00+01:00  install  anthropic-skills  claude-code  b0cbd3d
2026-03-18T16:31:00+01:00  update   skill-writing-guide  cursor  5464062
```

Format: `timestamp  operation  skill-name  agent  commit`

This lets you review past operations ("what did I install last time?") and debug issues ("when was this skill last updated?").

## Operations

Read `references/operations.md` for the detailed procedure of whichever operation the user requested (Install, Check, Update, List, Remove, Search).
