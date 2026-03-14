# Workflow Standards

Patterns and principles for creating workflows, extracted from real construction sessions. Each pattern includes a generic explanation and a concrete example.

## 1. Audience

Workflows are consumed by LLM agents. Write every instruction in natural language. An agent reading the workflow should understand what to do without needing bash scripts or command sequences.

> **Example**: Instead of writing a bash loop to iterate over config entries, write "Read each entry from the config file and run the install command for each one."

## 2. Distributable by Design

Everything a workflow needs must live together in a single folder. Copying that folder to another project must be enough to use it — no external dependencies, no hardcoded paths.

> **Example**: Config files, schemas, validation scripts, and the workflow itself all live inside `.agents/workflows/`. A new project gets the workflow by copying the folder.

## 3. Separation of Instructions and Data

Instructions (what to do) and data (what to operate on) belong in separate files. The workflow describes the process; config files provide the inputs.

> **Example**: The workflow `.md` says "read each repository from the config and install it." The `.yaml` config lists which repositories to install. Changing a repository doesn't require editing the workflow.

## 4. Data Validation

If a workflow consumes configuration files, those files must have a schema and a validation step. This prevents malformed input from causing silent failures downstream.

> **Example**: A `skills.yaml` config has a corresponding `skills.schema.json`. Before any install operation, a Python script validates the YAML against the schema using `jsonschema`.

## 5. Change Propagation

When introducing a new capability, review every step of the workflow to assess whether the change affects it. A feature added to one step often has ripple effects across the entire flow.

> **Example**: Adding `@branch` support to the install step also affected list (doesn't show branches), check for updates (`npx skills check` is branch-unaware), and update (needs re-clone instead of native update). Each step had to be individually reconsidered.

## 6. End-to-End Coherence

Every step must be coherent with the real capabilities and limitations of the tools it uses. Do not write instructions that assume a tool can do something it cannot.

> **Example**: `npx skills update` doesn't know about branches. The workflow cannot say "run update" for branch-pinned repos — it must say "re-run the install step" instead.

## 7. Problem Resolution by Debate

When a problem arises, do not jump to the first solution. Present multiple approaches with their trade-offs and let the user select the best one after discussion.

> **Example**: When `npx skills list` didn't show branch information, four options were presented: (1) combine outputs, (2) use only the YAML, (3) JSON enrichment, (4) lockfile approach. Option 4 was selected after evaluating the alternatives.

## 8. Research Before Building

Before designing a workflow, deeply understand the tools it will use — their capabilities, flags, formats, and limitations. Assumptions lead to rework.

> **Example**: Initially assuming `npx skills` didn't exist led to building a manual `git clone` solution. Actual research revealed a full CLI with `add`, `remove`, `list`, `update`, `check`, and `find` commands.

## 9. Documented Workarounds

When a tool doesn't support something natively, design a workaround and document it explicitly in the workflow. The workaround becomes a first-class part of the instructions.

> **Example**: `npx skills add` doesn't support branch specification. The workflow documents a workaround: clone the repo at the desired branch into a temp directory, then point `npx skills add` at the local clone.

## 10. End-to-End Testing

Writing a workflow is not enough. Execute it end-to-end to prove it works. Issues that look fine on paper often surface only during execution.

> **Example**: The validation script passed linting but failed at runtime because Python 3.10 doesn't support `list[str]` without a future import. The timestamp validation also failed because YAML auto-parses ISO dates as datetime objects.

## 11. Side Effects Documentation

When execution reveals unexpected side effects, document the fix directly in the workflow so future runs don't hit the same problem.

> **Example**: YAML silently converts ISO timestamps into datetime objects, breaking schema validation. The workflow now explicitly instructs: "timestamps must be quoted strings."

## 12. Explicit Over Implicit

Do not assume the agent executing the workflow knows edge cases or conventions. State everything explicitly, even if it seems obvious.

> **Example**: Instead of assuming the agent will quote timestamps in YAML, the workflow states: "Timestamps must be quoted strings (e.g. `"2026-03-14T07:18:30+01:00"`) to prevent YAML from auto-parsing them as datetime objects."

## 13. Continuous Learning

This document is a living standard. After building or modifying a workflow, evaluate whether new patterns, pitfalls, or best practices were discovered. If so, add them here. Each workflow construction session is an opportunity to improve the process for all future workflows.

> **Example**: Building the update-skills workflow revealed 12 patterns that didn't exist before. These were extracted from the construction session and added to this document, making the next workflow better from the start.

## 14. Isolated Testing Contexts

Workflow tests must run in independent agent sessions, not in the same session where the workflow was built. The builder has full context about intentions, edge cases, and workarounds — they will unconsciously fill in gaps that a fresh agent would stumble on. Only a context-free execution reveals whether the workflow is truly self-contained.

> **Example**: Testing the update-skills workflow in the same session where it was built always "passed" because the agent already knew the tools, the workarounds, and the expected behavior. A proper test requires a new conversation where the agent reads the workflow cold and follows it without prior knowledge.

## 15. Errors Are Hard Stops

When any command in a workflow fails — non-zero exit code, syntax error, runtime exception, unexpected output, missing dependency — the agent must stop immediately. Report the exact error to the user and ask how to proceed. Do not continue to the next step. No rationalization ("it's probably fine", "it's a pre-existing issue", "the important part still works") justifies bypassing an error.

This applies to every step: validation, installation, cloning, lockfile generation, cleanup — all of them. A workflow is a chain of trust; one broken link invalidates everything downstream.

> **Example**: A validation script failed with a `SyntaxError` because `python` resolved to Python 2.7 instead of 3.x. The agent noted the failure but continued with the update anyway, rationalizing that "the YAML files were valid when last checked." This violated the workflow's own instruction and let potentially invalid data through unchecked.
