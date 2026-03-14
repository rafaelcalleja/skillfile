# AGENTS.md

## Development Pipeline (MANDATORY)

Any modification to this skill must follow this pipeline. No exceptions.

### Before modifying

1. **Identify which feature you are changing** — see Feature Inventory below
2. **Check existing evals** — read `evals/evals.json` for the affected feature
3. **Design new test cases** if the change adds behavior or fixes a bug. Add them to `evals/evals.json`
4. **Get user confirmation** on the new test cases before proceeding

### Implement

5. **Make the change** to SKILL.md, scripts, or schemas
6. **Run validation** — `python3 scripts/validate_skills.py` must pass

### Verify

7. **Run ALL evals** using `skill-creator` — not just the ones for your change, ALL of them
8. **If any eval fails** — fix and re-run. Do not commit with failing evals
9. **Only commit after all evals pass**

### After committing

10. **Review STANDARDS.md** — did this change reveal a new pattern? If so, add it

---

## Feature Inventory

| Feature | Description | Evals |
|---------|-------------|-------|
| **Validate** | Run schemas against YAML files | `evals/evals.json` #1-8 |
| **Install (lockfile)** | Checkout exact commit, install | _pending_ |
| **Install (first-time)** | No lockfile → install from skills.yaml, generate lockfile | _pending_ |
| **Install (new repo)** | New repo in skills.yaml not in lockfile | _pending_ |
| **Check** | Compare lockfile commits vs remote HEAD | _pending_ |
| **Update** | Install latest, ask confirmation, regenerate lockfile | _pending_ |
| **List** | Display lockfile contents | _pending_ |
| **Remove** | Remove skill + lockfile entry | _pending_ |
| **Search** | Find new skills | _pending_ |
| **Standards Review** | Check STANDARDS.md compliance | _pending_ |

---

## Project Structure

```
skills/skillfile/
├── SKILL.md           — skill instructions (what agents execute)
├── STANDARDS.md        — development patterns (loaded on standards review)
├── schemas/            — JSON schemas for YAML validation
├── scripts/            — validation script
└── evals/              — test infrastructure
    ├── evals.json      — test cases per feature
    └── fixtures/       — YAML fixtures for tests
```

## Testing

### Run all evals

```bash
cd skills/skillfile && python3 evals/run_evals.py
```

### Run specific evals

```bash
cd skills/skillfile && python3 evals/run_evals.py 1 3 5
```

### Run validation only

```bash
cd skills/skillfile && python3 scripts/validate_skills.py
```

All evals must pass (exit code 0) before committing.
