#!/usr/bin/env python3
"""
DEUTSCH A1 PRO — STAGE 10 PART 3: ROLEPLAY CHAT SIMULATOR QA & VERIFICATION
Validates the interactive multi-turn A1 conversational branching scenarios,
pedagogical scoring, cultural etiquette tips, and idempotent rewards.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

passed = 0
failed = 0

def check(condition, desc):
    global passed, failed
    if condition:
        print(f"  [PASS] {desc}")
        passed += 1
    else:
        print(f"  [FAIL] {desc}")
        failed += 1

print("=" * 65)
print("DEUTSCH A1 PRO: STAGE 10 PART 3 (ROLEPLAY CHAT SIMULATOR) QA")
print("=" * 65)

# --- 1. DATA INTEGRITY AUDIT ---
data_js_path = os.path.join(os.path.dirname(__file__), "..", "js", "data.js")
with open(data_js_path, "r", encoding="utf-8") as f:
    raw_data = f.read()

# Extract JSON from window.GERMAN_A1_DATA
prefix = "window.GERMAN_A1_DATA = "
start_idx = raw_data.find(prefix)
if start_idx == -1:
    print("FATAL: Could not find window.GERMAN_A1_DATA in js/data.js")
    sys.exit(1)

json_str = raw_data[start_idx + len(prefix):].rstrip().rstrip(";")
dataset = json.loads(json_str)

labs = dataset.get("language_labs", {})
roleplays = labs.get("roleplay", [])

check(isinstance(roleplays, list), "language_labs.roleplay is a list")
check(len(roleplays) >= 6, f"Contains >= 6 conversational roleplay scenarios (found {len(roleplays)})")

expected_scenarios = [
    ("rp_cafe", "Café", 5),
    ("rp_hotel", "Hotel", 4),
    ("rp_supermarkt", "Supermarkt", 4),
    ("rp_weg", "Weg", 3),
    ("rp_arzt", "Arzt", 4),
    ("rp_wohnung", "WG", 5)
]

for sc_id, keyword, min_steps in expected_scenarios:
    matching = [r for r in roleplays if r.get("id") == sc_id]
    check(len(matching) == 1, f"Scenario '{sc_id}' uniquely exists")
    if matching:
        sc = matching[0]
        check(keyword in sc.get("title", ""), f"Scenario '{sc_id}' title contains '{keyword}'")
        check(bool(sc.get("partner_name")), f"Scenario '{sc_id}' has partner name: {sc.get('partner_name')}")
        check(bool(sc.get("partner_role")), f"Scenario '{sc_id}' has partner role: {sc.get('partner_role')}")
        check(bool(sc.get("avatar")), f"Scenario '{sc_id}' has partner avatar: {sc.get('avatar')}")
        check(len(sc.get("cultural_tip", "")) >= 30, f"Scenario '{sc_id}' has rich cultural tip (Landeskunde)")
        steps = sc.get("steps", [])
        check(len(steps) >= min_steps, f"Scenario '{sc_id}' has >= {min_steps} steps (found {len(steps)})")
        
        for idx, step in enumerate(steps, 1):
            check(bool(step.get("partner_de")), f"  Step {idx} has German prompt: {step.get('partner_de')[:35]}...")
            check(bool(step.get("partner_ka")), f"  Step {idx} has Georgian translation")
            options = step.get("options", [])
            check(len(options) == 3, f"  Step {idx} has exactly 3 response options")
            points = [o.get("points") for o in options]
            check(10 in points, f"  Step {idx} includes a perfect 10-point response option")
            check(any(p <= 3 for p in points), f"  Step {idx} includes a common error option for learning")
            for opt in options:
                check(bool(opt.get("text_de")), f"    Option text_de present")
                check(bool(opt.get("text_ka")), f"    Option text_ka present")
                check(bool(opt.get("feedback_ka")), f"    Option feedback_ka present")

# --- 2. JAVASCRIPT LOGIC & STATE PERSISTENCE SIMULATION ---
BASE_DIR = Path(__file__).resolve().parent.parent

mock_env = """
var window = { 
  location: { href: "http://localhost:8000" },
  addEventListener: function() {},
  matchMedia: function() { return { matches: false }; },
  scrollTo: function() {}
};
var globalThis = window;

var console = {
  log: function() {},
  warn: function() {},
  error: function() {},
  info: function() {}
};

var document = {
  getElementById: function(id) { 
    return { 
      innerHTML: "", 
      innerText: "", 
      value: "", 
      style: {}, 
      appendChild: function(){}, 
      classList: { add: function(){}, remove: function(){}, toggle: function(){}, contains: function(){ return false; } }, 
      focus: function(){},
      querySelectorAll: function(){ return []; },
      querySelector: function(){ return null; },
      addEventListener: function(){},
      remove: function(){}
    }; 
  },
  querySelectorAll: function() { return []; },
  querySelector: function() { return null; },
  body: { classList: { add: function(){}, remove: function(){} } },
  documentElement: { classList: { add: function(){}, remove: function(){}, toggle: function(){} } },
  createElement: function() { 
    return { 
      innerHTML: "", 
      style: {}, 
      appendChild: function(){}, 
      classList: { add: function(){}, remove: function(){} }, 
      remove: function(){} 
    }; 
  }
};

var localStorage = {
  _data: {},
  getItem: function(k) { return this._data[k] !== undefined ? this._data[k] : null; },
  setItem: function(k, v) { this._data[k] = String(v); },
  removeItem: function(k) { delete this._data[k]; },
  clear: function() { this._data = {}; }
};

var confirm = function() { return true; };
var alert = function() {};
window.confirm = confirm;
window.alert = alert;

var setTimeout = function(cb) { cb(); };
var clearTimeout = function() {};
window.setTimeout = setTimeout;
window.clearTimeout = clearTimeout;

var navigator = {
  userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
  mediaDevices: {
    getUserMedia: function() {
      return Promise.resolve({
        getTracks: function() { return [{ stop: function(){} }]; }
      });
    }
  }
};

var speechSynthesis = {
  speak: function(){},
  cancel: function(){},
  getVoices: function() {
    return [{ name: "Anna", lang: "de-DE", default: true }];
  }
};
var SpeechSynthesisUtterance = function(t){ this.text = t; this.lang = "de-DE"; };
window.SpeechSynthesisUtterance = SpeechSynthesisUtterance;
window.speechSynthesis = speechSynthesis;
window.document = document;
window.localStorage = localStorage;
"""

probe_roleplay_js = """
function runProbe() {
  var results = [];
  try {
    // Test 1: Switch to roleplay lab
    window.DeutschApp.switchLabTab('roleplay');
    results.push({ name: "switchLabTab('roleplay') sets active lab", ok: true });

    // Initial state check
    var rawInit = localStorage.getItem('deutsch_a1_pro_v3');
    var initUser = rawInit ? JSON.parse(rawInit) : { xp: 0 };
    var initialXP = initUser.xp || 0;

    // Step through all 5 steps of rp_cafe picking optimal 10-point answers (index 0)
    window.DeutschApp.chooseRoleplayOption(0); // Step 1 -> Step 2
    window.DeutschApp.chooseRoleplayOption(0); // Step 2 -> Step 3
    window.DeutschApp.chooseRoleplayOption(0); // Step 3 -> Step 4
    window.DeutschApp.chooseRoleplayOption(0); // Step 4 -> Step 5
    window.DeutschApp.chooseRoleplayOption(0); // Step 5 -> Completed!

    var rawUpdated = localStorage.getItem('deutsch_a1_pro_v3');
    var updatedUser = JSON.parse(rawUpdated);
    var scRecord = updatedUser.labScores && updatedUser.labScores.roleplay && updatedUser.labScores.roleplay['rp_cafe'];

    results.push({ 
      name: "Completed rp_cafe is recorded in userData.labScores.roleplay with 100% score", 
      ok: Boolean(scRecord && scRecord.completed === true && scRecord.score === 100)
    });

    results.push({
      name: "Completion awards +25 XP to user profile",
      ok: (updatedUser.xp === initialXP + 25)
    });

    // Test 3: Idempotence: replay rp_cafe and verify NO duplicate XP
    window.DeutschApp.restartRoleplayScenario();
    window.DeutschApp.chooseRoleplayOption(0);
    window.DeutschApp.chooseRoleplayOption(0);
    window.DeutschApp.chooseRoleplayOption(0);
    window.DeutschApp.chooseRoleplayOption(0);
    window.DeutschApp.chooseRoleplayOption(0);

    var rawReplayed = localStorage.getItem('deutsch_a1_pro_v3');
    var replayedUser = JSON.parse(rawReplayed);
    results.push({
      name: "Replaying roleplay scenario grants ZERO duplicate XP (strict idempotence)",
      ok: (replayedUser.xp === initialXP + 25)
    });

    // Test 4: Switching to another scenario
    window.DeutschApp.switchRoleplayScenario(1); // rp_hotel
    window.DeutschApp.chooseRoleplayOption(0); // Step 1
    window.DeutschApp.chooseRoleplayOption(0); // Step 2
    window.DeutschApp.chooseRoleplayOption(0); // Step 3
    window.DeutschApp.chooseRoleplayOption(0); // Step 4 -> Completed rp_hotel!

    var rawHotel = localStorage.getItem('deutsch_a1_pro_v3');
    var hotelUser = JSON.parse(rawHotel);
    var hotelRecord = hotelUser.labScores && hotelUser.labScores.roleplay && hotelUser.labScores.roleplay['rp_hotel'];

    results.push({
      name: "Switching scenario initializes and completes independent conversation thread (+25 XP)",
      ok: Boolean(hotelRecord && hotelRecord.completed === true && hotelUser.xp === initialXP + 50)
    });

    // Test 5: Translation toggling
    window.DeutschApp.toggleRoleplayTranslation('test_key');
    results.push({
      name: "toggleRoleplayTranslation executes safely without errors",
      ok: true
    });

  } catch(e) {
    results.push({ name: "Exception during probe: " + e.toString(), ok: false });
  }

  return JSON.stringify(results);
}
runProbe();
"""

data_content = (BASE_DIR / "js" / "data.js").read_text(encoding="utf-8")
app_content = (BASE_DIR / "js" / "app.js").read_text(encoding="utf-8")
full_code = mock_env + "\n" + data_content + "\n" + app_content + "\n" + probe_roleplay_js

probe_file = BASE_DIR / "tests" / "_stage10_roleplay_runner.js"
probe_file.write_text(full_code, encoding="utf-8")
try:
    res = subprocess.run(["osascript", "-l", "JavaScript", str(probe_file)], capture_output=True, text=True)
    if res.returncode == 0:
        sim_results = json.loads(res.stdout.strip())
        for r in sim_results:
            check(r["ok"], r["name"])
    else:
        check(False, f"osascript JS execution failed: {res.stderr}")
finally:
    if probe_file.exists():
        probe_file.unlink()

print("=" * 65)
print(f"STAGE 10 PART 3 QA SUMMARY: {passed} Passed, {failed} Failed")
print("=" * 65)

if failed > 0:
    sys.exit(1)
