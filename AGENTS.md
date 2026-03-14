# AGENTS.md

> Index file — load referenced files on demand.

## Project Overview

Skillfile manages agent skills using a declarative YAML config (`skills.yaml`) and a lockfile (`skills-lock.yaml`) for reproducibility. Skills are installed from git repositories.

## Testing

Test cases are in [evals/evals.json](skills/skillfile/evals/evals.json). Run evals using `skill-creator`:

1. Read `skill-creator` SKILL.md
2. List its evaluation workflow steps
3. Use those steps as your checklist — execute each one, mark it done
4. Subsets of evals are valid

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
| Test cases & context | [evals/AGENTS.md](skills/skillfile/evals/AGENTS.md) | When designing or running tests |
| Eval workflow | `skill-creator` SKILL.md | When running evals |
