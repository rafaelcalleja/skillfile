# Designing Test Cases — Lessons Learned

Patterns discovered while creating the Install evals. Follow these when designing test cases for a new feature.

## The prompt is what a user would say

Every eval uses the same prompt — the instruction a real user would give. Don't write technical descriptions as prompts. "Install my skills" is a prompt. "Validate YAML then clone at commit hash" is not.

## What varies is the file state

The prompt stays the same. What changes between evals is the fixture files: which files exist, what they contain, and what's missing. The fixture defines the scenario, not the prompt.

## Organize fixtures by feature

```
fixtures/
└── install/
    ├── multi-repo-skills.yaml
    ├── partial-failure-skills.yaml
    └── ...
```

Each fixture file name describes the scenario it creates.

## Cover three categories

1. **Happy path** — normal operation works correctly (install, first-time, multi-repo)
2. **Error handling** — bad input, missing repos, failures (validation fails, clone fails, npx fails)
3. **Edge cases** — unusual but valid scenarios (idempotent, same repo two branches, orphaned lockfile entries)

## Only test what you can simulate

If you can't reliably reproduce a scenario in the test environment, don't write an eval for it. "Network unavailable" requires cutting network access — that's invasive and flaky. Remove it.

## Expectations must be verifiable

Write expectations that can be checked by reading the output. "Agent handles the error gracefully" is not verifiable. "Agent reports the error to the user" is — you can grep for the error message.

## One scenario per eval

Each eval tests exactly one thing. Don't combine "multi-repo install + validation failure" into one eval. Separate them so you know exactly what broke.

## Regression testing works

Remove a behavior from the skill instructions → run the eval → it fails. This proves the evals are actually testing the skill, not just passing by default.
