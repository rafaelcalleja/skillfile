# Skillfile

A skill for managing agent skills with version pinning and reproducibility.

## What it does

- **Declarative config** — define repos and branches in `skills.yaml`
- **Lockfile** — pins exact commit hashes for reproducible installs
- **Validation** — JSON Schema + Python jsonschema for all YAML files
- **Standards** — self-evolving patterns for workflow quality

## Install

```bash
npx skills add decolua/skillfile
```

## Usage

Once installed, the skill is available to your AI agent. Ask it to:

- `/skillfile` — install, update, check, list, or remove skills
- Edit `skills.yaml` in the skill's directory to add/remove repositories

## Config format

```yaml
# skills.yaml
superpowers: https://github.com/obra/superpowers@main
my-skills: https://github.com/user/my-skills@develop
```

## License

MIT
