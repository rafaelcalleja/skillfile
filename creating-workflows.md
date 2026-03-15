# Creating Workflows — Lessons Learned

Patterns discovered while building the skillfile workflow. Follow these when creating new agent workflows.

## Schema first, code second

Define JSON schemas before writing validation scripts or implementation code. Schemas are the source of truth — everything else derives from them.

## Validation is a hard gate

Validate inputs before any operation. If validation fails, stop immediately. Don't silently proceed with bad data. Non-zero exit code = hard stop.

## Lockfiles for reproducibility

Pin exact versions (commit hashes, not branches). The lockfile captures the state that was actually installed, not the intent. Only the update operation modifies the lockfile.

## AGENTS.md is for agents, README is for humans

These are different documents with different audiences. Don't mix them. AGENTS.md follows the agents.md spec — it's an index with progressive disclosure. README is for humans reading GitHub.

## Progressive disclosure

AGENTS.md is an index. It tells the agent what files exist and when to load them. The details live in the referenced files. If AGENTS.md is longer than a screen, it has too much content.

## One fact, one place

Every piece of information lives in exactly one file. Reference it from elsewhere, never copy it. If two files say the same thing, they will eventually diverge and one will be wrong.

## Don't hardcode external tool behavior

If your workflow depends on an external tool (like skill-creator), reference the tool by name. Don't paste its steps into your files — if the tool changes, your copy is stale.

## Verbalize each step

Agents skip steps they don't announce. Force the agent to say "Step N: [what]" before executing. Print the result before moving to the next step. If it wasn't announced, it wasn't done.

## Step 0 is a gate

Before executing anything, show the user what will happen. Wait for explicit approval. This makes the process predictable and gives the user control over scope.

## Every feature must update all affected files

When a feature changes a format, behavior, or instruction, check every file in the repo that references it. Update or delete stale content. Files to check: SKILL.md, AGENTS.md, STANDARDS.md, README, schemas, fixtures, evals.json, validation scripts. If you changed a format, every example of the old format is now wrong.
