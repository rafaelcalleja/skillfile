# Running Test Suite — Lessons Learned

Patterns discovered while building and executing the eval pipeline. Follow these to avoid common mistakes.

## Always announce before executing

Each step must be verbalized before it runs. Say "Step N: [what]" → do it → print result. This prevents skipping steps. If you didn't announce it, you didn't do it.

## Step 0 is a gate

Before executing anything, show the user a summary table of selected evals. Wait for explicit approval. Do not proceed without it.

## Delegate to skill-creator

Do not reinvent the eval workflow. Do not write custom grading scripts, custom viewers, or custom report formats. Skill-creator defines how evals run — read it, follow it.

## Do not hardcode skill-creator internals

If skill-creator changes its format, our instructions should still work. Reference skill-creator by name, not by its current implementation details.

## Subsets are valid

You don't have to run all evals every time. A subset is fine, but every skill-creator step must complete for every eval in the subset.

## Determinism comes from measurement

LLM instruction-following is probabilistic. You cannot force an agent to follow steps 100% of the time. What you can do is run the evals multiple times and measure consistency. If pass rate drops, the instructions need improvement.

## Don't duplicate content

Each piece of information lives in exactly one file. Reference it, don't copy it. If two files say the same thing, one of them is wrong (or will be soon).
