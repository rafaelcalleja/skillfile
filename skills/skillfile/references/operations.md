# Operations Reference

Detailed procedures for each skillfile operation. Read the relevant section when performing an operation.

## Install

Install skills from the lockfile, filtered by agent.

Before installing, check if the user specified which agent to install for. If they said something like "Install my skills for claude-code", use that agent. If they just said "Install my skills" without specifying, ask them which agent — the `agents` field in `skills.yaml` shows what's available. If they say "all", install everything.

**With lockfile:** Read each matching entry. For each one:
1. Clone the repository
2. Checkout the exact commit hash from the lockfile
3. Run `npx -y skills@1.4.5 add <local-path> --agent <agent> --skill '*' -y`
4. Clean up the temporary directory

**Without lockfile (first-time):** Read `skills.yaml`, install the latest from each branch, and generate the lockfile (see Update for lockfile generation format).

**New repos in skills.yaml:** If `skills.yaml` has repos not yet in the lockfile, install those at latest and add them to the lockfile. This is the only case where Install touches the lockfile — existing entries stay unchanged.

## Check for Updates

For each repository in the lockfile, run `git ls-remote <repo-url> refs/heads/<branch>` to get the latest commit hash. Compare against the `commit` field in the lockfile. Report which repositories have updates, showing current vs latest hashes.

This never modifies the lockfile.

## Update

This is the only operation that modifies the lockfile. Ask the user for confirmation before proceeding — updating changes pinned versions, which affects reproducibility.

Read each entry from `skills.yaml`. For each one:
1. Clone the repository at the specified branch
2. Run `npx -y skills@1.4.5 add <local-path> --agent <agents> --skill '*' -y` where `<agents>` comes from the entry's `agents` field
3. Clean up the temporary directory

After installing, regenerate `skills-lock.yaml` with:
- repo URL
- branch
- new commit hash (from the cloned repo)
- installation timestamp
- list of skill names installed

Timestamps must be quoted strings (e.g. `"2026-03-14T07:18:30+01:00"`) — YAML silently converts unquoted ISO dates into datetime objects, which breaks schema validation downstream.

## List Installed Skills

Read and display `skills-lock.yaml`. Shows all installed skills with source repository, branch, commit hash, and installation date.

## Remove a Skill

Run `npx -y skills@1.4.5 remove <skill-name> --all` to remove a specific skill. Then remove its entry from `skills-lock.yaml`.

## Search for New Skills

Browse https://skills.sh or run `npx -y skills@1.4.5 find <query>` to discover new skill packages.
