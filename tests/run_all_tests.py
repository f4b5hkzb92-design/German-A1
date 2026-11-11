#!/usr/bin/env python3
"""
DEUTSCH A1 PRO - Master Test Runner
Executes curriculum integrity tests and WebKit JavaScriptCore runtime tests.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_suite(name, script_path):
    print(f"\n>>> Running: {name} ({script_path.name})...")
    res = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("STDERR:\n" + res.stderr)
    return res.returncode == 0

def main():
    print("="*65)
    print("       DEUTSCH A1 PRO — COMPREHENSIVE QA & TEST SUITE")
    print("="*65)

    test1 = BASE_DIR / "tests" / "test_curriculum_integrity.py"
    test2 = BASE_DIR / "tests" / "test_runtime_jscore.py"
    test3 = BASE_DIR / "tests" / "test_stage8_verification.py"

    p1 = run_suite("Curriculum & Data Integrity Suite", test1)
    p2 = run_suite("Safari / WebKit JavaScriptCore Runtime Suite", test2)
    p3 = run_suite("Stage 8 Verification & QA Harness", test3)

    print("\n" + "="*65)
    if p1 and p2 and p3:
        print("  🎉 ALL TEST SUITES PASSED PERFECTLY (100% SUCCESS)!")
        print("="*65)
        sys.exit(0)
    else:
        print("  ❌ ONE OR MORE TEST SUITES FAILED")
        print("="*65)
        sys.exit(1)

if __name__ == "__main__":
    main()
