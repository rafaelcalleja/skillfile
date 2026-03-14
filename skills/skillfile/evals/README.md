# Evals

Test cases for the skillfile skill. Each eval is a user prompt + fixture files + expectations.

## Structure

```
evals/
├── evals.json          — test case definitions
└── fixtures/
    ├── valid-skills.yaml
    ├── valid-skills-lock.yaml
    ├── invalid-skills-bad-url.yaml
    ├── invalid-lock-short-hash.yaml
    ├── invalid-lock-missing-field.yaml
    └── install/        — Install feature fixtures
```

## How to run

Use `skill-creator` — read its SKILL.md and follow the evaluation workflow.

## Adding tests

1. Design the test case: user prompt + what files exist + what should happen
2. Create any needed fixture files in `fixtures/`
3. Add the case to `evals.json`
4. Run evals to verify

## evals.json format

```json
{
  "skill_name": "skillfile",
  "evals": [
    {
      "id": 1,
      "prompt": "User's request",
      "expected_output": "What the agent should do",
      "files": ["evals/fixtures/file.yaml"],
      "expectations": ["Verifiable assertion 1", "Verifiable assertion 2"]
    }
  ]
}
```
