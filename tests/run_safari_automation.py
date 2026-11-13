#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Safari Browser Automation & Screenshot Capturer for macOS (Stage 9.1)
Opens Safari to local test suite, retrieves machine-readable test results,
asserts 100% pass rate, and exits with a non-zero code on any test failure.
"""

import subprocess
import time
import json
import sys
from pathlib import Path

BASE_DIR = Path("/Users/shotachitaishvili/Documents/German A1")
SCREENSHOTS_DIR = BASE_DIR / "tests" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_FILE = BASE_DIR / "tests" / "_safari_qa_results.json"

def run_applescript(script_str):
    return subprocess.run(["osascript", "-e", script_str], capture_output=True, text=True)

def main():
    print("="*65)
    print("  SAFARI REAL BROWSER AUTOMATION & MACHINE-READABLE QA (Stage 9.1)")
    print("="*65)

    # 0. Clean prior machine-readable results
    if RESULTS_FILE.exists():
        try:
            RESULTS_FILE.unlink()
        except Exception:
            pass

    # 1. Activate Safari and open QA Runner
    test_url = "http://localhost:8000/tests/safari_browser_test.html"
    print(f"1. Launching Safari and navigating to {test_url}...")
    run_applescript('tell application "Safari" to activate')
    time.sleep(1)
    run_applescript(f'tell application "Safari" to open location "{test_url}"')

    # 2. Poll for machine-readable results posted by safari_browser_test.html
    print("2. Waiting for Safari test execution and machine-readable results...")
    max_wait = 25.0
    start_time = time.time()
    qa_results = None

    while (time.time() - start_time) < max_wait:
        if RESULTS_FILE.exists():
            try:
                content = RESULTS_FILE.read_text(encoding="utf-8")
                if content.strip():
                    qa_results = json.loads(content)
                    break
            except Exception:
                pass
        time.sleep(0.5)

    # 3. Capture Screenshot 1: QA Dashboard in Safari
    shot1 = SCREENSHOTS_DIR / "safari_qa_dashboard.png"
    print(f"3. Capturing visual evidence of QA Dashboard: {shot1.name}...")
    subprocess.run(["screencapture", "-x", str(shot1)])
    if shot1.exists():
        print(f"   ✓ Captured: {shot1} ({shot1.stat().st_size:,} bytes)")

    # 4. Navigate Safari to main application
    main_url = "http://localhost:8000/"
    print(f"4. Navigating Safari to main production interface: {main_url}...")
    run_applescript('tell application "Safari" to activate')
    time.sleep(0.5)
    run_applescript(f'tell application "Safari" to open location "{main_url}"')
    time.sleep(2.5)

    # 5. Capture Screenshot 2: Main Production Interface
    shot2 = SCREENSHOTS_DIR / "safari_main_app.png"
    print(f"5. Capturing production application view: {shot2.name}...")
    subprocess.run(["screencapture", "-x", str(shot2)])
    if shot2.exists():
        print(f"   ✓ Captured: {shot2} ({shot2.stat().st_size:,} bytes)")

    # 6. Verify machine-readable results and enforce exit code
    print("\n" + "="*65)
    if not qa_results:
        print("  ❌ ERROR: No machine-readable QA results received from Safari!")
        print("  Safari browser test timed out or failed to reach the server.")
        print("="*65)
        sys.exit(1)

    passed = qa_results.get("passed", 0)
    failed = qa_results.get("failed", 0)
    success = qa_results.get("success", False)
    details = qa_results.get("details", [])

    print(f"  SAFARI TEST RESULTS: {passed} PASSED, {failed} FAILED (Success: {success})")
    for item in details:
        status_tag = "[PASS]" if item.get("ok") else "[FAIL]"
        print(f"    {status_tag} {item.get('title')}")
    print("="*65)

    if not success or failed > 0 or passed == 0:
        print(f"  ❌ SAFARI QA FAILED: {failed} test(s) failed!")
        print("  Exiting with non-zero status code.")
        sys.exit(1)

    print("  🎉 ALL REAL SAFARI BROWSER TESTS PASSED (100% SUCCESS)!")
    print("="*65)
    sys.exit(0)

if __name__ == "__main__":
    main()
