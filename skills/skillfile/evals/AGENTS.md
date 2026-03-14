# Evals

Agent context for the test suite.

## Structure

```
evals/
├── evals.json      — test case definitions
└── fixtures/       — YAML files used as test inputs
    └── install/    — Install feature fixtures
```

## evals.json format

Each eval has the same user prompt. What varies is the fixture files and expected behavior.

```json
{
  "id": 1,
  "prompt": "Install my skills",
  "expected_output": "Description of correct agent behavior",
  "files": ["evals/fixtures/file.yaml"],
  "expectations": ["Verifiable assertion"]
}
```

## Adding tests

1. Design the case: what files exist + what should happen
2. Create fixture files in `fixtures/`
3. Add the case to `evals.json`

## Running tests

0. Show the user a summary of selected evals and wait for approval — see [examples/test-run-plan.md](examples/test-run-plan.md)
1. Read `skill-creator` SKILL.md and list its evaluation workflow steps
2. Execute using skill-creator's steps as your checklist
3. Before saying "done", verify every step is marked done and viewer shown to user

## Report

The eval workflow must produce a report the user can review. The report format is defined by `skill-creator` — do not invent a custom format.

## Feature Inventory

| Feature | Evals | Status |
|---------|-------|--------|
| Install | #1-16 | defined |
| Check | — | pending |
| Update | — | pending |
| List | — | pending |
| Remove | — | pending |
| Search | — | pending |
| Standards Review | — | pending |
