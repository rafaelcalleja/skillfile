# AGENTS.md

## Development Pipeline (MANDATORY)

Any modification to this skill MUST follow this pipeline. No exceptions. No skipping steps.

### Before modifying

1. Identify which feature you are changing — see Feature Inventory below
2. Check existing evals in `evals/evals.json` for the affected feature
3. Design new test cases if the change adds behavior or fixes a bug
4. Add them to `evals/evals.json`

### Implement

5. Make the change to SKILL.md, scripts, or schemas

### Run evals

6. Read `skill-creator` SKILL.md
7. Follow skill-creator's evaluation workflow to run ALL evals in `evals/evals.json`

**MANDATORY CHECKLIST — you MUST complete every item before reporting results:**

- [ ] Read `evals/evals.json` — count total evals
- [ ] Execute every eval (not a subset, ALL of them)
- [ ] Save stdout output for each eval to `outputs/stdout.txt`
- [ ] Grade each eval's expectations — write `grading.json`
- [ ] Generate `benchmark.json` with aggregate results
- [ ] Generate `eval_review.html` using `generate_review.py`
- [ ] Report the viewer to the user

**STOP — before saying "done", verify:**

- [ ] How many evals are in `evals.json`? ___
- [ ] How many did you execute? ___
- [ ] How many have `grading.json`? ___
- [ ] Does `benchmark.json` exist? ___
- [ ] Does `eval_review.html` exist? ___
- [ ] Did you show the viewer to the user? ___

If ANY answer is "no" or the counts don't match, you are NOT done. Go back and complete the missing steps.

### After all evals pass

8. Only commit after all evals pass
9. Review `STANDARDS.md` — did this change reveal a new pattern?

---

## Feature Inventory

| Feature | Description | Evals |
|---------|-------------|-------|
| **Install** | Install skills from lockfile or first-time | `evals/evals.json` #1-16 |
| **Check** | Compare lockfile vs remote HEAD | _pending_ |
| **Update** | Install latest + regenerate lockfile | _pending_ |
| **List** | Display lockfile contents | _pending_ |
| **Remove** | Remove skill + lockfile entry | _pending_ |
| **Search** | Find new skills | _pending_ |
| **Standards Review** | Check STANDARDS.md compliance | _pending_ |

---

## Project Structure

```
skills/skillfile/
├── SKILL.md           — skill instructions (what agents execute)
├── STANDARDS.md        — development patterns
├── schemas/            — JSON schemas for YAML validation
├── scripts/            — validation script
└── evals/
    ├── evals.json      — test cases (prompt + fixtures + expectations)
    └── fixtures/       — YAML fixtures for tests
        └── install/    — Install feature fixtures
```
