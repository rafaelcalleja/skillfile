# AGENTS.md

> Index file — load referenced files on demand.

## Project Overview

Skillfile manages agent skills using a declarative YAML config (`skills.yaml`) and a lockfile (`skills-lock.yaml`) for reproducibility. Skills are installed from git repositories, filtered by target agent (claude-code, cursor, etc.).

## Development Pipeline

Any modification to this skill MUST follow this order:

1. **Design tests** → see [evals/AGENTS.md](skills/skillfile/evals/AGENTS.md)
2. **Implement** the change
3. **Run evals** → see [evals/AGENTS.md](skills/skillfile/evals/AGENTS.md)
4. **Verify** → every skill-creator step marked done, viewer shown to user
5. **Commit** only after evals pass
6. **Review standards** → see [STANDARDS.md](skills/skillfile/STANDARDS.md)
7. **After npx version bump** → run agent sync: `npx -y skills@X.Y.Z --help` to verify flags, update SKILL.md if behavior changed

## References

| What | Where | When to load |
|------|-------|-------------|
| Skill instructions | [SKILL.md](skills/skillfile/SKILL.md) | When executing any skill operation |
| Development patterns | [STANDARDS.md](skills/skillfile/STANDARDS.md) | After completing any operation |
| Testing | [evals/AGENTS.md](skills/skillfile/evals/AGENTS.md) | When designing or running tests |
| Eval execution patterns | [running-test-suite.md](skills/skillfile/running-test-suite.md) | When running evals for the first time |
| Workflow creation patterns | [creating-workflows.md](skills/skillfile/creating-workflows.md) | When building new agent workflows |
| Test case design patterns | [designing-test-cases.md](skills/skillfile/designing-test-cases.md) | When designing evals for a new feature |
