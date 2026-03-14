# AGENTS.md

> **This file is an index.** Read only what you need. Load referenced files on demand.

## Development Pipeline (MANDATORY)

Any modification to this skill MUST follow this pipeline:

1. **Design tests** → see [evals/README.md](skills/skillfile/evals/README.md)
2. **Implement** the change
3. **Run evals** → read `skill-creator` SKILL.md, list its steps, use them as your checklist
4. **Verify** → every step from skill-creator marked done, viewer shown to user
5. **Commit** only after evals pass

## References

| What | Where | When to load |
|------|-------|-------------|
| Skill instructions | [SKILL.md](skills/skillfile/SKILL.md) | When executing any skill operation |
| Development patterns | [STANDARDS.md](skills/skillfile/STANDARDS.md) | After completing any operation |
| Test cases | [evals/evals.json](skills/skillfile/evals/evals.json) | When designing or running tests |
| Test fixtures | [evals/fixtures/](skills/skillfile/evals/fixtures/) | When running tests |
| Eval workflow | `skill-creator` SKILL.md | When running evals (step 3) |

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
