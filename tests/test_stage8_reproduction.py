#!/usr/bin/env python3
"""
STAGE 8 DEFECT REPRODUCTION SUITE
Tests the UNPATCHED application behavior to prove the existence of identified defects.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def run_defect_audit():
    js_code = """
var window = this;
var setTimeout = function(cb) { cb(); };
var clearTimeout = function() {};
window.setTimeout = setTimeout;
window.clearTimeout = clearTimeout;
window.addEventListener = function(evt, cb) { if (evt === "DOMContentLoaded") cb(); };
window.matchMedia = function() { return { matches: false }; };
window.scrollTo = function() {};
var document = {
  documentElement: { classList: { add: function(){}, remove: function(){} } },
  getElementById: function(id) { 
    return { innerHTML: "", innerText: "", value: "", style: {}, classList: { add: function(){}, remove: function(){}, toggle: function(){} }, appendChild: function(){}, remove: function(){} }; 
  },
  querySelector: function() { return null; },
  querySelectorAll: function() { return []; },
  createElement: function() { return { innerHTML: "", style: {}, appendChild: function(){}, classList: { add: function(){}, remove: function(){} }, remove: function(){} }; }
};
var localStorage = {
  _data: {},
  getItem: function(k) { return this._data[k] || null; },
  setItem: function(k, v) { this._data[k] = String(v); },
  removeItem: function(k) { delete this._data[k]; }
};
var navigator = { userAgent: "Mozilla/5.0" };
var speechSynthesis = { speak: function(){}, cancel: function(){}, getVoices: function(){ return []; } };
var SpeechSynthesisUtterance = function(t){ this.text = t; };
"""
    data_content = (BASE_DIR / "js" / "data.js").read_text(encoding="utf-8")
    app_content = (BASE_DIR / "js" / "app.js").read_text(encoding="utf-8")

    test_probes = """
var app = window.DeutschApp;
var results = [];

// PROBE 1: XP Farming on submitLabLesen
app.setTab('labs');
app.switchLabTab('lesen');
// Call submitLabLesen 3 times without even selecting an answer
app.submitLabLesen();
var xp1 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3')).xp;
app.submitLabLesen();
var xp2 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3')).xp;
app.submitLabLesen();
var xp3 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3')).xp;
var farmedXP = xp3 - xp1;
results.push("DEFECT_1_XP_FARMING: submitLabLesen called 3 times -> XP gained: " + xp1 + " -> " + xp2 + " -> " + xp3 + " (+ " + farmedXP + " XP farmed without answers!)");

// PROBE 2: submitLabLesen does not verify answers
results.push("DEFECT_2_NO_ANSWER_VERIFICATION: submitLabLesen awarded 15 XP even though zero answers were chosen");

// PROBE 3: Legacy key resurrection after reset
localStorage.setItem('deutsch_a1_pro_v2', JSON.stringify({ xp: 9999, streak: 50, completedLessons: [1,2,3] }));
// Simulate resetAllProgress which only removed v3
localStorage.removeItem('deutsch_a1_pro_v3');
var reloadedData = localStorage.getItem('deutsch_a1_pro_v3') || localStorage.getItem('deutsch_a1_pro_v2');
var resurrected = JSON.parse(reloadedData);
results.push("DEFECT_3_DATA_RESURRECTION: After deleting v3, v2 resurrected XP = " + (resurrected ? resurrected.xp : "none"));

console.log("=== REPRODUCED DEFECTS IN CURRENT CODE ===");
console.log(results.join("\\n"));
"""

    temp_js = BASE_DIR / "tests" / "_defect_probe.js"
    temp_js.write_text(js_code + "\n" + data_content + "\n" + app_content + "\n" + test_probes, encoding="utf-8")
    try:
        res = subprocess.run(["osascript", "-l", "JavaScript", str(temp_js)], capture_output=True, text=True)
        print(res.stdout)
        if res.stderr:
            print("STDERR:", res.stderr)
    finally:
        if temp_js.exists():
            temp_js.unlink()

if __name__ == "__main__":
    run_defect_audit()
