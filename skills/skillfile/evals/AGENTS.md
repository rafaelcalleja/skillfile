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

Each step MUST print its name and result before proceeding to the next. Do NOT batch steps. Do NOT skip announcing a step.

0. Show the user a summary and wait for approval:

   ## 🧪 Test Run — [Feature] (subset N/M)

   | # | Case | What happens |
   |---|------|-------------|
   | 1 | Case description | Expected behavior |
   | 2 | Case description | Expected behavior |

   **N evals** → execute + grade + viewer. Approve?

1. Say "Step 1: Reading skill-creator SKILL.md" → read it → list the steps found
2. Say "Step 2: Listing workflow steps" → print them numbered
3. Say "Step 3: Executing eval #N" → execute → print result. Repeat for each eval
4. Say "Step 4: Grading" → grade each eval → print pass/fail per eval
5. Say "Step 5: Generating viewer" → generate → show to user

## Report

The eval workflow must produce a report the user can review. The report format is defined by `skill-creator` — do not invent a custom format.

