# AGENTS.md

> Index file — load referenced files on demand.

## Project Overview

Skillfile manages agent skills using a declarative YAML config (`skills.yaml`) and a lockfile (`skills-lock.yaml`) for reproducibility. Skills are installed from git repositories.

## Development Pipeline

Any modification to this skill MUST follow this order:

1. **Design tests** → see [evals/AGENTS.md](skills/skillfile/evals/AGENTS.md)
2. **Implement** the change
3. **Run evals** → see Testing above
4. **Verify** → every skill-creator step marked done, viewer shown to user
5. **Commit** only after evals pass
6. **Review standards** → see [STANDARDS.md](skills/skillfile/STANDARDS.md)

## References

| What | Where | When to load |
|------|-------|-------------|
| Skill instructions | [SKILL.md](skills/skillfile/SKILL.md) | When executing any skill operation |
| Development patterns | [STANDARDS.md](skills/skillfile/STANDARDS.md) | After completing any operation |
| Testing | [evals/AGENTS.md](skills/skillfile/evals/AGENTS.md) | When designing or running tests |
