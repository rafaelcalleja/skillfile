# AGENTS.md

> Index file — load referenced files on demand.

## Project Overview

Skillfile manages agent skills using a declarative YAML config (`skills.yaml`) and a lockfile (`skills-lock.yaml`) for reproducibility. Skills are installed from git repositories, filtered by target agent (claude-code, cursor, etc.).

## Development Pipeline

Any modification to this skill follows this order:

1. **Design tests** → use skill-creator workflow
2. **Implement** the change
3. **Run evals** → use skill-creator workflow
4. **Verify** → skill-creator steps complete, viewer shown to user
5. **Commit** only after evals pass
6. **Review standards** → see [STANDARDS.md](STANDARDS.md)
7. **After npx version bump** → run agent sync: `npx -y skills@X.Y.Z --help` to verify flags, update SKILL.md if behavior changed

## References

| What | Where | When to load |
|------|-------|-------------|
| Skill instructions | [SKILL.md](skills/skillfile/SKILL.md) | When executing any skill operation |
| Operations reference | [operations.md](skills/skillfile/references/operations.md) | When performing Install/Update/Remove/Check |
| Development patterns | [STANDARDS.md](STANDARDS.md) | After completing any operation |
| Eval execution patterns | [running-test-suite.md](running-test-suite.md) | When running evals |
| Workflow creation patterns | [creating-workflows.md](creating-workflows.md) | When building new workflows |
| Test case design patterns | [designing-test-cases.md](designing-test-cases.md) | When designing evals |
