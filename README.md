# Skillfile

A skill for managing agent skills with version pinning and reproducibility.

## What it does

- **Declarative config** — define repos, branches, and target agents in `skills.yaml`
- **Lockfile** — pins exact commit hashes for reproducible installs
- **Agent filtering** — install skills for specific agents (claude-code, cursor, etc.)
- **Validation** — JSON Schema + Python jsonschema for all YAML files
- **Standards** — self-evolving patterns for workflow quality

## Install

```bash
npx skills add rafaelcalleja/skillfile
```

## Usage

Once installed, the skill is available to your AI agent. Ask it to:

- `/skillfile` — install, update, check, list, or remove skills
- Edit `skills.yaml` in the skill's directory to add/remove repositories

## Config format

```yaml
# skills.yaml
superpowers:
  repo: https://github.com/obra/superpowers@main
  agents: [claude-code, cursor]

my-skills:
  repo: https://github.com/user/my-skills@develop
  agents: [antigravity]
```

## License

MIT
