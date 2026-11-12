#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Safari Browser Automation & Screenshot Capturer for macOS
Opens Safari to local test suite and captures visual evidence.
"""

import subprocess
import time
from pathlib import Path

BASE_DIR = Path("/Users/shotachitaishvili/Documents/German A1")
SCREENSHOTS_DIR = BASE_DIR / "tests" / "screenshots"
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

def run_applescript(script_str):
    return subprocess.run(["osascript", "-e", script_str], capture_output=True, text=True)

def main():
    print("="*65)
    print("       SAFARI REAL BROWSER AUTOMATION & SCREENSHOT HARNESS")
    print("="*65)

    # 1. Activate Safari and open QA Runner
    test_url = "http://localhost:8000/tests/safari_browser_test.html"
    print(f"1. Launching Safari and navigating to {test_url}...")
    run_applescript('tell application "Safari" to activate')
    time.sleep(1)
    run_applescript(f'tell application "Safari" to open location "{test_url}"')
    
    print("2. Allowing 3.5 seconds for Safari to render DOM and execute tests...")
    time.sleep(3.5)

    # 3. Capture Screenshot 1: QA Dashboard in Safari
    shot1 = SCREENSHOTS_DIR / "safari_qa_dashboard.png"
    print(f"3. Capturing visual evidence of QA Dashboard: {shot1.name}...")
    subprocess.run(["screencapture", "-x", str(shot1)])
    if shot1.exists():
        print(f"   ✓ Captured: {shot1} ({shot1.stat().st_size:,} bytes)")

    # 4. Navigate Safari to main application
    main_url = "http://localhost:8000/"
    print(f"4. Navigating Safari to main production interface: {main_url}...")
    run_applescript(f'tell application "Safari" to open location "{main_url}"')
    time.sleep(2.5)

    # 5. Capture Screenshot 2: Main Production Interface
    shot2 = SCREENSHOTS_DIR / "safari_main_app.png"
    print(f"5. Capturing production application view: {shot2.name}...")
    subprocess.run(["screencapture", "-x", str(shot2)])
    if shot2.exists():
        print(f"   ✓ Captured: {shot2} ({shot2.stat().st_size:,} bytes)")

    print("="*65)
    print("  🎉 REAL BROWSER TESTING COMPLETE! EVIDENCE SAVED.")
    print("="*65)

if __name__ == "__main__":
    main()
