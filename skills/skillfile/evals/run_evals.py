#!/usr/bin/env python3
"""Run evals for the skillfile skill.

Reads evals/evals.json, sets up fixtures, executes the validation script,
and checks expectations (exit code + stdout patterns).

Usage:
    python3 evals/run_evals.py           # run all evals
    python3 evals/run_evals.py 1 3 5     # run specific eval IDs
"""
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


def setup_fixture(workdir: Path, eval_case: dict) -> None:
    """Copy fixture files into the working directory."""
    # Clean any previous skills.yaml / skills-lock.yaml
    for f in ["skills.yaml", "skills-lock.yaml"]:
        target = workdir / f
        if target.exists():
            target.unlink()

    prompt = eval_case["prompt"].lower()

    # Parse the prompt to determine which fixtures to copy
    for fixture_file in eval_case.get("files", []):
        src = SKILL_DIR / fixture_file
        if not src.exists():
            print(f"    ⚠ Fixture not found: {fixture_file}")
            continue

        # Determine target name based on the fixture filename
        name = src.name
        if "lock" in name:
            target_name = "skills-lock.yaml"
        elif "skills" in name:
            target_name = "skills.yaml"
        else:
            target_name = name

        shutil.copy2(src, workdir / target_name)

    # Handle special setup from prompt
    if "empty skills.yaml" in prompt or "0 bytes" in prompt:
        (workdir / "skills.yaml").write_text("")

    if "no skills.yaml" in prompt or "no skills.yaml file" in prompt:
        target = workdir / "skills.yaml"
        if target.exists():
            target.unlink()

    if "no skills-lock.yaml" in prompt:
        target = workdir / "skills-lock.yaml"
        if target.exists():
            target.unlink()

    if "ensure there is no skills-lock.yaml" in prompt:
        target = workdir / "skills-lock.yaml"
        if target.exists():
            target.unlink()

    if "unquoted timestamp" in prompt:
        lock_content = (
            "superpowers:\n"
            "  repo: https://github.com/obra/superpowers\n"
            "  branch: main\n"
            "  commit: a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2\n"
            "  installed: 2026-03-14T07:18:30+01:00\n"
            "  skills:\n"
            "    - test-driven-development\n"
        )
        (workdir / "skills-lock.yaml").write_text(lock_content)


def check_expectations(expectations: list[str], exit_code: int, output: str) -> list[dict]:
    """Check expectations against actual results. Returns list of {text, passed, evidence}."""
    results = []
    output_lower = output.lower()

    for exp in expectations:
        exp_lower = exp.lower()

        if exp_lower.startswith("exit code is "):
            expected_code = int(exp_lower.split("exit code is ")[1])
            passed = exit_code == expected_code
            evidence = f"Exit code was {exit_code}"

        elif "does not contain" in exp_lower or "does not" in exp_lower:
            # Extract the pattern after "does NOT contain"
            pattern = exp.split("'")[1] if "'" in exp else exp.split("contain ")[-1].strip("'\"")
            passed = pattern.lower() not in output_lower
            evidence = f"Pattern '{pattern}' {'not found (correct)' if passed else 'WAS found (unexpected)'}"

        elif "contains" in exp_lower:
            # Handle "or" patterns: "contains X or Y"
            if "' or '" in exp_lower:
                parts = exp_lower.split("contains ")[1]
                patterns = [p.strip("' \"") for p in parts.split(" or ")]
                passed = any(p in output_lower for p in patterns)
                evidence = f"Checked patterns {patterns}: {'found' if passed else 'none found'}"
            elif "' and '" in exp_lower:
                parts = exp_lower.split("contains ")[1]
                patterns = [p.strip("' \"") for p in parts.split(" and ")]
                passed = all(p in output_lower for p in patterns)
                evidence = f"Checked patterns {patterns}: {'all found' if passed else 'not all found'}"
            else:
                pattern = exp.split("'")[1] if "'" in exp else exp.split("contains ")[1].strip("'\"")
                passed = pattern.lower() in output_lower
                evidence = f"Pattern '{pattern}' {'found' if passed else 'NOT found'}"
        else:
            passed = False
            evidence = f"Unknown expectation format: {exp}"

        results.append({"text": exp, "passed": passed, "evidence": evidence})

    return results


def run_eval(eval_case: dict) -> dict:
    """Run a single eval case. Returns grading results."""
    eval_id = eval_case["id"]
    prompt = eval_case["prompt"]

    print(f"\n{'='*60}")
    print(f"Eval #{eval_id}: {eval_case.get('expected_output', '')[:80]}")
    print(f"{'='*60}")

    # Create a temporary working directory that mirrors the skill structure
    with tempfile.TemporaryDirectory(prefix=f"skillfile-eval-{eval_id}-") as tmpdir:
        workdir = Path(tmpdir)

        # Copy scripts and schemas into the temp dir
        shutil.copytree(SKILL_DIR / "scripts", workdir / "scripts")
        shutil.copytree(SKILL_DIR / "schemas", workdir / "schemas")

        # Setup fixtures
        setup_fixture(workdir, eval_case)

        # List what's in the workdir for debugging
        files = list(workdir.glob("*.yaml"))
        print(f"  Setup: {[f.name for f in files]}")

        # Run the validation script
        result = subprocess.run(
            [sys.executable, "scripts/validate_skills.py"],
            cwd=workdir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = result.stdout + result.stderr
        print(f"  Exit code: {result.returncode}")
        print(f"  Output: {output.strip()}")

        # Check expectations
        exp_results = check_expectations(
            eval_case.get("expectations", []),
            result.returncode,
            output,
        )

        passed = sum(1 for r in exp_results if r["passed"])
        total = len(exp_results)

        for r in exp_results:
            icon = "✅" if r["passed"] else "❌"
            print(f"  {icon} {r['text']}")
            if not r["passed"]:
                print(f"     → {r['evidence']}")

        print(f"\n  Result: {passed}/{total} expectations passed")

        return {
            "eval_id": eval_id,
            "passed": passed,
            "total": total,
            "all_passed": passed == total,
            "expectations": exp_results,
        }


def main():
    with open(EVALS_FILE) as f:
        evals_data = json.load(f)

    # Filter by IDs if specified
    ids_to_run = None
    if len(sys.argv) > 1:
        ids_to_run = [int(x) for x in sys.argv[1:]]

    evals = evals_data["evals"]
    if ids_to_run:
        evals = [e for e in evals if e["id"] in ids_to_run]

    print(f"Running {len(evals)} evals for skill: {evals_data['skill_name']}")

    results = []
    for eval_case in evals:
        result = run_eval(eval_case)
        results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")

    total_passed = sum(1 for r in results if r["all_passed"])
    total_evals = len(results)

    for r in results:
        icon = "✅" if r["all_passed"] else "❌"
        print(f"  {icon} Eval #{r['eval_id']}: {r['passed']}/{r['total']} expectations")

    print(f"\n  {total_passed}/{total_evals} evals passed")

    if total_passed < total_evals:
        sys.exit(1)


if __name__ == "__main__":
    main()
