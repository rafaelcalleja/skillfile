# Operations Reference

Detailed procedures for each skillfile operation. Read the relevant section when performing an operation.

## Install

**Goal**: All skills from the lockfile are installed for the requested agent. New repos in `skills.yaml` not yet in the lockfile get installed at latest and added to the lockfile.

Determine which agent to install for: check if the user specified one, if `config.json` has a `default_agent`, or ask the user. The `agents` field in `skills.yaml` shows what's available.

**With lockfile**: For each entry matching the requested agent, clone the repo, checkout the pinned commit, and run `npx -y skills@1.4.5 add <local-path> --agent <agent> --skill '*' -y`. Clean up each clone after installation.

**Without lockfile (first-time)**: Install the latest from each branch and generate the lockfile (see Update for lockfile format).

**New repos in skills.yaml**: If `skills.yaml` has repos not in the lockfile, install those at latest and add them to the lockfile. Existing entries stay unchanged.

If a clone fails, retry by converting the URL to the alternate protocol (`https://` ↔ `git@`).

After installing, log each operation to `operations.log`.

## Check for Updates

**Goal**: Report which repos have newer commits on their branch than what the lockfile pins.

For each lockfile entry, run `git ls-remote <repo-url> refs/heads/<branch>` and compare against the `commit` field. Report differences with current vs latest hashes.

This never modifies the lockfile.

## Update

**Goal**: All skills are installed at the latest commit from their branch, and the lockfile reflects the new state.

> Ask the user for confirmation before proceeding — updating changes pinned versions, which affects reproducibility.

For each `skills.yaml` entry, clone at the branch head, install with `npx -y skills@1.4.5 add <local-path> --agent <agents> --skill '*' -y`, and clean up.

After all installations, regenerate `skills-lock.yaml` with:
- repo URL
- branch
- new commit hash (from the cloned repo)
- installation timestamp (must be a quoted string, e.g. `"2026-03-14T07:18:30+01:00"`)
- list of skill names installed

Log each operation to `operations.log`.

## List Installed Skills

**Goal**: Display all installed skills with their source, branch, commit, and install date.

Read `skills-lock.yaml` and present its contents.

## Remove a Skill

**Goal**: The named skill is uninstalled and removed from the lockfile.

Run `npx -y skills@1.4.5 remove <skill-name> --all`, then remove its entry from `skills-lock.yaml`. Log the operation to `operations.log`.

## Search for New Skills

**Goal**: Help the user discover new skill packages.

Browse https://skills.sh or run `npx -y skills@1.4.5 find <query>`.
