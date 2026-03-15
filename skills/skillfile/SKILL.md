---
name: skillfile
description: Use when managing agent skills installation, updates, or version pinning from external git repositories
---

# Skillfile

Manages agent skills using `npx skills@1.4.5` with a declarative YAML config and a lockfile for reproducibility.

> **npx version constraint**: All commands in this skill use `npx -y skills@1.4.5`. Do not use a different version — the skill's behavior depends on it.

## Quick Reference

| Operation | What it does | Modifies lockfile? |
|-----------|-------------|-------------------|
| **Install** | Installs what the lockfile says, filtered by agent. If `skills.yaml` has new repos not in the lockfile, adds them | No (except adding new entries) |
| **Check** | Compares lockfile commits against remote HEAD | No |
| **Update** | Installs latest from each branch, asks for confirmation | Yes |
| **List** | Shows lockfile contents | No |
| **Remove** | Removes a skill | Yes (removes entry) |
| **First-time** | If no lockfile exists, installs from `skills.yaml` and creates lockfile | Yes (creation) |

## Files

| File | Purpose | Format | Schema | Edited by |
|------|---------|--------|--------|-----------|
| `skills.yaml` | Declares repositories, branches, and target agents | `name: {repo, agents}` | `schemas/skills.schema.json` | User (manually) |
| `skills-lock.yaml` | Pins the exact commit hash installed | `name: {repo, branch, commit, installed, skills}` | `schemas/skills-lock.schema.json` | Skill only (never manually) |

Both files live in the same directory as this skill and are validated before any operation by running `python3 scripts/validate_skills.py` from this skill's directory.

## Setup

If `skills.yaml` does not exist in this skill's directory, create it with the format:

```yaml
# Skills Configuration
# Format: name: {repo: https://repository_url@branch, agents: [agent1, agent2]}

superpowers:
  repo: https://github.com/obra/superpowers@main
  agents: [claude-code, cursor]
```

If the project does not have an `AGENTS.md` at its root, create one. If it already exists, append the following section. This lets other agents know that skill management is available:

```markdown
## Skill Management

This project uses [skillfile](https://github.com/rafaelcalleja/skillfile) for managing agent skills. Run `/skillfile` to install, update, check, list, or remove skills. Configuration is in `.agents/skills/skillfile/skills.yaml`.
```

## Validate configuration

Before any operation, validate the YAML files against their JSON schemas by running `python3 scripts/validate_skills.py` from this skill's directory.

**Validation is a hard gate.** If the command fails for ANY reason — schema errors, syntax errors, missing dependencies, non-zero exit code — you MUST stop immediately. Do not continue with the operation. Report the exact error to the user and ask how to proceed.

## Install

Install skills from the lockfile, filtered by agent. This is the default operation and never modifies the lockfile.

Before installing, ask the user which agent to install for. If the user specifies an agent (e.g. "Install my skills for claude-code"), filter `skills.yaml` entries to only those whose `agents` list includes the specified agent. If the user says "all", install everything. Do not install without confirming the agent.

If `skills-lock.yaml` exists, read each matching entry and for each one: clone the repository, checkout the exact commit hash from the lockfile, then run `npx -y skills@1.4.5 add <local-path> --agent <agent>`. Clean up the temporary directory afterwards.

If the lockfile does not exist yet, treat this as a first-time install: read `skills.yaml`, install the latest from each branch, and generate the lockfile (see Update for how to generate it).

If `skills.yaml` contains repositories that are not yet in the lockfile, install those as new entries and add them to the lockfile. This is the only case where Install modifies the lockfile — existing entries are never changed.

## Check for updates

For each repository in the lockfile, run `git ls-remote <repo-url> refs/heads/<branch>` to get the latest commit hash. Compare it against the `commit` field in the lockfile. Report which repositories have updates available, showing the current and latest commit hashes.

This operation never modifies the lockfile.

## Update

This is the only operation that modifies the lockfile. Before proceeding, ask the user for confirmation.

Read each entry from `skills.yaml`. For each one, clone the repository at the specified branch, then run `npx -y skills@1.4.5 add <local-path> --agent <agents>` where `<agents>` comes from the entry's `agents` field. Clean up the temporary directory afterwards.

After installing, regenerate `skills-lock.yaml` with: repo URL, branch, the new commit hash (obtained from the cloned repo), installation timestamp, and the list of skill names installed. Timestamps must be quoted strings (e.g. `"2026-03-14T07:18:30+01:00"`) to prevent YAML from auto-parsing them as datetime objects.

## List installed skills

Read and display the contents of `skills-lock.yaml`. This shows all installed skills with their source repository, branch, commit hash, and installation date.

## Remove a skill

Run `npx -y skills@1.4.5 remove <skill-name> --all` to remove a specific skill. Then remove its entry from `skills-lock.yaml`.

## Search for new skills

Browse https://skills.sh or run `npx -y skills@1.4.5 find <query>` to discover new skill packages.

## Standards Review

After completing any operation, read `STANDARDS.md` in this skill's directory and review each pattern point by point. Verify compliance. If new patterns were discovered during this execution, add them to `STANDARDS.md`.
