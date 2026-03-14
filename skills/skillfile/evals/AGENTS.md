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

Use `skill-creator` — follow its evaluation workflow. See root [AGENTS.md](../../AGENTS.md) for the full pipeline.

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
