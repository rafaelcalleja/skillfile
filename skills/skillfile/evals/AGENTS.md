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

0. Show the user a summary and wait for approval:

   ## 🧪 Test Run — [Feature] (subset N/M)

   | # | Case | What happens |
   |---|------|-------------|
   | 1 | Case description | Expected behavior |
   | 2 | Case description | Expected behavior |

   **N evals** → execute + grade + viewer. Approve?
1. Read `skill-creator` SKILL.md
2. List its evaluation workflow steps
3. Use those steps as your checklist — execute each one, mark it done
4. Subsets of evals are valid, but every skill-creator step must be completed for each eval you run
5. Before saying "done", verify every step is marked done and viewer shown to user

## Report

The eval workflow must produce a report the user can review. The report format is defined by `skill-creator` — do not invent a custom format.

