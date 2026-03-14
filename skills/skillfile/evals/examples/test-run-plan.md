# Test Run Plan

> Generated before execution. User must approve before evals run.

## Scope

- **Source**: `evals/evals.json`
- **Total evals available**: 16
- **Evals selected**: #2, #12, #13, #14, #16 (5 evals)
- **Reason for subset**: remaining untested evals from Install feature

## Selected evals

| # | Case | Fixtures | Expected |
|---|------|----------|----------|
| 2 | Multi-repo install | `multi-repo-skills.yaml` + `multi-repo-lock.yaml` | All 3 repos installed at exact commits |
| 12 | Same repo, 2 branches | `same-repo-two-branches-skills.yaml` | Both branches install independently |
| 13 | Idempotent reinstall | `valid-skills.yaml` + `valid-skills-lock.yaml` | Reinstalls cleanly, no changes |
| 14 | Partial failure | `partial-failure-skills.yaml` | First repo ok, second fails, reports error |
| 16 | Empty config | (empty skills.yaml) | Validation fails, hard stop |

## Checklist (from skill-creator)

- [ ] Execute each selected eval
- [ ] Save output per eval
- [ ] Grade expectations
- [ ] Generate report
- [ ] Show viewer to user

## Approve?

Reply to proceed with execution or adjust the scope.
