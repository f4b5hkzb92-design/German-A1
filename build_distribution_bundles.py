#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generates distribution bundles for Deutsch A1 Pro (Stage 9.1):
1. Deutsch_A1_All_Code.txt (Single consolidated text file)
2. Deutsch_A1_Full.zip
3. German_A1_Project_Bundle.zip
Copies bundles to Desktop and project root.
"""

import os
import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path("/Users/shotachitaishvili/Documents/German A1")
DESKTOP_DIR = Path("/Users/shotachitaishvili/Desktop")

CODE_FILES = [
    "README.md",
    "STAGE_9_1_AUDIT.md",
    "STAGE_9_1_TEST_RESULTS.md",
    "index.html",
    "css/style.css",
    "server.py",
    "js/app.js",
    "tests/safari_browser_test.html",
    "tests/run_safari_automation.py",
    "tests/test_stage9_1_verification.py",
    "tests/test_stage9_verification.py",
    "tests/test_stage8_verification.py",
    "tests/run_all_tests.py",
    "data_grammar_checks.py",
    "data_language_labs.py",
    "data_upgrades.py",
    "build_full_suite.py"
]

def generate_consolidated_code_file():
    target = BASE_DIR / "Deutsch_A1_All_Code.txt"
    print(f"Generating {target.name}...")
    with open(target, "w", encoding="utf-8") as out:
        out.write("="*80 + "\n")
        out.write("DEUTSCH A1 PRO — COMPLETE SOURCE CODE & SPECIFICATION (STAGE 9.1)\n")
        out.write("="*80 + "\n\n")

        for rel_path in CODE_FILES:
            fpath = BASE_DIR / rel_path
            if fpath.exists():
                out.write("\n" + "#"*80 + "\n")
                out.write(f"### FILE: {rel_path}\n")
                out.write("#"*80 + "\n\n")
                out.write(fpath.read_text(encoding="utf-8"))
                out.write("\n\n")
    print(f"  ✓ {target.name} created ({target.stat().st_size:,} bytes)")
    return target

def generate_zip_bundle(zip_name):
    zip_path = BASE_DIR / zip_name
    print(f"Generating {zip_name}...")
    
    # Excluded patterns
    excluded_names = {".git", "__pycache__", ".DS_Store", "Deutsch_A1_Full.zip", "German_A1_Project_Bundle.zip"}

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in excluded_names and not d.startswith(".")]
            for file in files:
                if file in excluded_names or file.endswith(".pyc") or file == zip_name:
                    continue
                full_path = Path(root) / file
                arc_name = full_path.relative_to(BASE_DIR)
                zf.write(full_path, arc_name)

    print(f"  ✓ {zip_name} created ({zip_path.stat().st_size:,} bytes)")
    return zip_path

def main():
    print("="*65)
    print("   DEUTSCH A1 PRO — STAGE 9.1 BUNDLE & ARCHIVE GENERATOR")
    print("="*65)

    all_code = generate_consolidated_code_file()
    zip1 = generate_zip_bundle("Deutsch_A1_Full.zip")
    zip2 = generate_zip_bundle("German_A1_Project_Bundle.zip")

    # Copy to Desktop
    print("\nCopying distribution artifacts to Desktop...")
    for item in [all_code, zip1, zip2]:
        dest = DESKTOP_DIR / item.name
        shutil.copy2(item, dest)
        print(f"  ✓ Copied to Desktop: {dest} ({dest.stat().st_size:,} bytes)")

    print("\n" + "="*65)
    print("  🎉 ALL STAGE 9.1 ARTIFACTS GENERATED & DEPLOYED SUCCESSFULLY!")
    print("="*65)

if __name__ == "__main__":
    main()
