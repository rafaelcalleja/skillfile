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
7. List every step in skill-creator's evaluation workflow
8. Use that list as your checklist — execute each step, mark it done
9. Do NOT skip any step. If you chose a subset of evals, that's fine, but every step of the workflow must be completed for each eval you run

**Before saying "done", verify against your checklist:**

- [ ] Every step from skill-creator's workflow is marked done
- [ ] Evals executed = evals chosen
- [ ] Viewer/report shown to the user

If anything is missing, go back and complete it.

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
