#!/usr/bin/env python3
"""Generate grading.json files from run_evals.py output for skill-creator compatibility."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
EVALS_FILE = SKILL_DIR / "evals" / "evals.json"

# Import from run_evals
sys.path.insert(0, str(SKILL_DIR / "evals"))
from run_evals import setup_fixture, check_expectations


def main():
    workspace = Path(sys.argv[1]) if len(sys.argv) > 1 else SKILL_DIR.parent.parent / "skillfile-workspace" / "iteration-1"
    workspace.mkdir(parents=True, exist_ok=True)

    with open(EVALS_FILE) as f:
        evals_data = json.load(f)

    eval_names = {
        1: "valid-both-files",
        2: "valid-skills-no-lockfile",
        3: "invalid-skills-bad-url",
        4: "invalid-lock-short-hash",
        5: "empty-skills-file",
        6: "missing-skills-file",
        7: "unquoted-timestamp",
        8: "missing-required-field",
    }

    all_results = []

    for eval_case in evals_data["evals"]:
        eval_id = eval_case["id"]
        eval_name = eval_names.get(eval_id, f"eval-{eval_id}")
        eval_dir = workspace / eval_name / "with_skill"
        eval_dir.mkdir(parents=True, exist_ok=True)
        (eval_dir / "outputs").mkdir(exist_ok=True)

        # Write eval_metadata.json
        metadata = {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "prompt": eval_case["prompt"],
            "assertions": eval_case.get("expectations", []),
        }
        with open(eval_dir.parent / "eval_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        # Execute the eval
        with tempfile.TemporaryDirectory(prefix=f"skillfile-eval-{eval_id}-") as tmpdir:
            workdir = Path(tmpdir)
            shutil.copytree(SKILL_DIR / "scripts", workdir / "scripts")
            shutil.copytree(SKILL_DIR / "schemas", workdir / "schemas")
            setup_fixture(workdir, eval_case)

            result = subprocess.run(
                [sys.executable, "scripts/validate_skills.py"],
                cwd=workdir,
                capture_output=True,
                text=True,
                timeout=30,
            )

            output = result.stdout + result.stderr
            (eval_dir / "outputs" / "stdout.txt").write_text(output)

            exp_results = check_expectations(
                eval_case.get("expectations", []),
                result.returncode,
                output,
            )

        # Write grading.json
        passed = sum(1 for r in exp_results if r["passed"])
        total = len(exp_results)

        grading = {
            "expectations": exp_results,
            "summary": {
                "passed": passed,
                "failed": total - passed,
                "total": total,
                "pass_rate": passed / total if total > 0 else 0,
            },
        }
        with open(eval_dir / "grading.json", "w") as f:
            json.dump(grading, f, indent=2)

        all_results.append({
            "eval_id": eval_id,
            "eval_name": eval_name,
            "passed": passed,
            "total": total,
            "pass_rate": passed / total if total > 0 else 0,
        })

        icon = "✅" if passed == total else "❌"
        print(f"{icon} {eval_name}: {passed}/{total}")

    # Write benchmark.json
    benchmark = {
        "metadata": {
            "skill_name": "skillfile",
            "skill_path": str(SKILL_DIR),
            "timestamp": "2026-03-14T13:30:00+01:00",
            "evals_run": [r["eval_name"] for r in all_results],
            "runs_per_configuration": 1,
        },
        "runs": [
            {
                "eval_id": r["eval_id"],
                "eval_name": r["eval_name"],
                "configuration": "with_skill",
                "run_number": 1,
                "result": {
                    "pass_rate": r["pass_rate"],
                    "passed": r["passed"],
                    "failed": r["total"] - r["passed"],
                    "total": r["total"],
                    "time_seconds": 0,
                    "tokens": 0,
                    "tool_calls": 0,
                    "errors": 0,
                },
                "expectations": [],
                "notes": [],
            }
            for r in all_results
        ],
        "run_summary": {
            "with_skill": {
                "pass_rate": {
                    "mean": sum(r["pass_rate"] for r in all_results) / len(all_results),
                    "stddev": 0,
                    "min": min(r["pass_rate"] for r in all_results),
                    "max": max(r["pass_rate"] for r in all_results),
                },
            },
        },
        "notes": [
            f"{sum(1 for r in all_results if r['passed'] == r['total'])}/{len(all_results)} evals passed all expectations",
        ],
    }
    with open(workspace / "benchmark.json", "w") as f:
        json.dump(benchmark, f, indent=2)

    total_evals = len(all_results)
    total_passed = sum(1 for r in all_results if r["passed"] == r["total"])
    print(f"\n{total_passed}/{total_evals} evals passed")
    print(f"Workspace: {workspace}")

    if total_passed < total_evals:
        sys.exit(1)


if __name__ == "__main__":
    main()
