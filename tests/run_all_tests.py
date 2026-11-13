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
    test4 = BASE_DIR / "tests" / "test_stage9_verification.py"
    test5 = BASE_DIR / "tests" / "test_stage9_1_verification.py"
    test6 = BASE_DIR / "tests" / "test_stage10_part3_roleplay.py"
    test7 = BASE_DIR / "tests" / "test_stage10_part4_certificate.py"
    test8 = BASE_DIR / "tests" / "test_multiskill_exam.py"
    test9 = BASE_DIR / "tests" / "test_upgrades.py"

    p1 = run_suite("Curriculum & Data Integrity Suite", test1)
    p2 = run_suite("Safari / WebKit JavaScriptCore Runtime Suite", test2)
    p3 = run_suite("Stage 8 Verification & QA Harness", test3)
    p4 = run_suite("Stage 9 Verification & QA Harness", test4)
    p5 = run_suite("Stage 9.1 Verification & QA Harness", test5)
    p6 = run_suite("Stage 10 Part 3 (Roleplay Chat Simulator) Suite", test6)
    p7 = run_suite("Stage 10 Part 4 & 5 (Certificate & PWA) Suite", test7)
    p8 = run_suite("Multi-Skill CEFR A1 Examination Suite", test8)
    p9 = run_suite("Practice Trainers Hub & Mini-Stories Suite", test9)

    print("\n" + "="*65)
    if p1 and p2 and p3 and p4 and p5 and p6 and p7 and p8 and p9:
        print("  🎉 ALL TEST SUITES PASSED PERFECTLY (100% SUCCESS)!")
        print("="*65)
        sys.exit(0)
    else:
        print("  ❌ ONE OR MORE TEST SUITES FAILED")
        print("="*65)
        sys.exit(1)

if __name__ == "__main__":
    main()
