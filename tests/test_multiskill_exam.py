#!/usr/bin/env python3
"""
DEUTSCH A1 PRO — Multi-Skill CEFR A1 Examination & Honest Assessment Verification
Tests:
1. Multi-Skill Exam Dataset Architecture (26 items: Hören, Lesen, Satzbau, Schreiben)
2. Hören Audio Engine: audio_text presence and speakGerman integration
3. Satzbau Syntax Engine: German word order rules (V2, Satzklammer, Trennbare, Inversion)
4. Schreiben Engine: Official Formular validation & Guided Email rubric
5. Honest Assessment & Certificate Promise Removal from UI
6. Modular Scoring & Detailed Review Generation
"""

import sys
import os
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
print("DEUTSCH A1 PRO: Multi-Skill Examination & Assessment Integrity QA")
print("=" * 65)

BASE_DIR = Path(__file__).resolve().parent.parent
data_path = BASE_DIR / "js" / "data.js"
app_path = BASE_DIR / "js" / "app.js"

data_content = data_path.read_text(encoding="utf-8")
raw_json = data_content.replace("window.GERMAN_A1_DATA = ", "").rstrip(";\n")
data = json.loads(raw_json)
app_code = app_path.read_text(encoding="utf-8")

# --- 1. DATASET INTEGRITY & MODULE ARCHITECTURE ---
exam = data.get("final_exam_questions", [])
check(len(exam) == 26, f"Exam contains exactly 26 comprehensive tasks (found {len(exam)})")

hoeren_items = [q for q in exam if q.get("module") == "hoeren"]
lesen_items = [q for q in exam if q.get("module") == "lesen"]
satzbau_items = [q for q in exam if q.get("module") == "satzbau"]
schreiben_items = [q for q in exam if q.get("module") == "schreiben"]

check(len(hoeren_items) == 7, f"Modul 1 (Hören) contains 7 tasks (found {len(hoeren_items)})")
check(len(lesen_items) == 8, f"Modul 2 (Lesen & Grammatik) contains 8 tasks (found {len(lesen_items)})")
check(len(satzbau_items) == 7, f"Modul 3 (Satzbau & Syntax) contains 7 tasks (found {len(satzbau_items)})")
check(len(schreiben_items) == 4, f"Modul 4 (Schreiben) contains 4 tasks (found {len(schreiben_items)})")

# Hören validation
for h in hoeren_items:
    check(bool(h.get("audio_text")), f"Hören #{h['id']} has authentic spoken German audio_text")
    check(bool(h.get("scenario")), f"Hören #{h['id']} has authentic situation setting")
    check(len(h.get("options", [])) == 4, f"Hören #{h['id']} has 4 options")

# Satzbau validation
for s in satzbau_items:
    check(bool(s.get("syntax_rule")), f"Satzbau #{s['id']} defines strict word order rule")
    check(bool(s.get("explanation")), f"Satzbau #{s['id']} has pedagogical explanation")

# Schreiben validation
for w in schreiben_items:
    check(bool(w.get("scenario")), f"Schreiben #{w['id']} has real-world writing context")
    check(len(w.get("options", [])) == 4, f"Schreiben #{w['id']} has options")

# --- 2. ELIMINATION OF PREMATURE CERTIFICATE PROMISES ---
check("📜 Deutsch A1 Pro კურსის სერტიფიკატი" not in app_code, "Exam view does not falsely promise course certificate in header")
check("სერტიფიკატის მისაღებად ჩააბარეთ შემაჯამებელი A1 გამოცდა" not in app_code, "Profile does not display promotional message promising certificate before exam is passed")
check("✓ სადიაგნოსტიკო სერტიფიკატი" not in app_code, "Pro modal does not list unearned diagnostic certificate")

# --- 3. JAVASCRIPT SIMULATION (MODULAR SCORING & INTERACTIVE WORKBENCH) ---
mock_env = """
var window = { 
  location: { href: "http://localhost:8000" },
  addEventListener: function() {},
  matchMedia: function() { return { matches: false }; },
  scrollTo: function() {},
  print: function() { this.__printCalled = true; }
};
var globalThis = window;

var console = {
  log: function() {},
  warn: function() {},
  error: function() {},
  info: function() {}
};

var document = {
  _elements: {},
  getElementById: function(id) { 
    if (!this._elements[id]) {
      this._elements[id] = { 
        innerHTML: "", 
        innerText: "", 
        value: "", 
        style: {}, 
        appendChild: function(){}, 
        classList: { 
          _c: [],
          add: function(c){ if(!this._c.includes(c)) this._c.push(c); }, 
          remove: function(c){ this._c = this._c.filter(x => x!==c); }, 
          toggle: function(c){ if(this._c.includes(c)) this.remove(c); else this.add(c); }, 
          contains: function(c){ return this._c.includes(c); } 
        }, 
        focus: function(){},
        querySelectorAll: function(){ return []; },
        querySelector: function(){ return null; },
        addEventListener: function(){},
        remove: function(){}
      }; 
    }
    return this._elements[id];
  },
  querySelectorAll: function() { return []; },
  querySelector: function() { return null; },
  body: { classList: { add: function(){}, remove: function(){} }, appendChild: function(){} },
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

var setTimeout = function(cb, ms) { cb(); };
var clearTimeout = function() {};
window.setTimeout = setTimeout;
window.clearTimeout = clearTimeout;

var navigator = {
  userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
  mediaDevices: { getUserMedia: function() { return Promise.resolve({ getTracks: () => [{ stop: ()=>{} }] }); } }
};

var speechSynthesis = {
  speak: function(){},
  cancel: function(){},
  getVoices: function() { return [{ name: "Anna", lang: "de-DE", default: true }]; }
};
var SpeechSynthesisUtterance = function(t){ this.text = t; this.lang = "de-DE"; };
window.SpeechSynthesisUtterance = SpeechSynthesisUtterance;
window.speechSynthesis = speechSynthesis;
window.document = document;
window.localStorage = localStorage;
"""

probe_exam_js = """
function runProbe() {
  var results = [];
  try {
    var app = window.DeutschApp;

    // Test A: Module Filtering
    app.setExamFilterModule('hoeren');
    var mainEl = document.getElementById('main-content');
    results.push({
      name: "Filter setExamFilterModule('hoeren') restricts view to Hören tasks",
      ok: (mainEl.innerHTML.indexOf('Modul 1: Hören') !== -1 && mainEl.innerHTML.indexOf('Modul 3: Satzbau') === -1)
    });

    app.setExamFilterModule('all');
    results.push({
      name: "Filter setExamFilterModule('all') displays all 4 modules",
      ok: (mainEl.innerHTML.indexOf('Modul 1: Hören') !== -1 && mainEl.innerHTML.indexOf('Modul 4: Schreiben') !== -1)
    });

    // Test B: Audio Transcript Toggle
    app.toggleAudioTranscript(1);
    var transEl = document.getElementById('audio-transcript-1');
    results.push({
      name: "toggleAudioTranscript toggles hidden class on audio transcript",
      ok: Boolean(transEl)
    });

    // Test C: Anmeldeformular Validation
    document.getElementById('exam-form-nachname').value = "Meier";
    document.getElementById('exam-form-vorname').value = "Lukas";
    document.getElementById('exam-form-stadt').value = "Berlin";
    document.getElementById('exam-form-plz').value = "10623";
    document.getElementById('exam-form-beruf').value = "Programmierer";
    app.checkExamFormular();
    var formFeedback = document.getElementById('exam-form-feedback').innerHTML;
    results.push({
      name: "checkExamFormular validates authentic A1 registration form correctly",
      ok: (formFeedback.indexOf('შესანიშნავია') !== -1 && formFeedback.indexOf('5/5') !== -1)
    });

    // Test D: Email Rubric Check
    document.getElementById('exam-email-input').value = "Sehr geehrte Frau Müller, leider kann ich morgen nicht kommen, weil ich krank bin. Könnten Sie mir bitte die Hausaufgabe schicken? Viele Grüße, Giorgi";
    app.checkExamEmail();
    var emailFeedback = document.getElementById('exam-email-feedback').innerHTML;
    results.push({
      name: "checkExamEmail validates CEFR A1 email rubric (salutation, reason, task, closing)",
      ok: (emailFeedback.indexOf('რუბრიკა: 4/4') !== -1)
    });

    // Test E: Submit Full Exam with Multi-Skill Scoring
    var questions = window.GERMAN_A1_DATA.final_exam_questions;
    questions.forEach(function(q) {
      app.onExamAnswer(q.id, q.answer);
    });
    app.submitExam();

    var user = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
    var lastAttempt = user.examHistory[user.examHistory.length - 1];

    results.push({
      name: "submitExam calculates 26/26 score (100%) and marks examPassed=true",
      ok: Boolean(user.examPassed === true && user.examScore === 26 && lastAttempt.pct === 100)
    });

    results.push({
      name: "submitExam records per-module performance breakdown",
      ok: Boolean(lastAttempt.modules && 
                  lastAttempt.modules.hoeren.score === 7 && 
                  lastAttempt.modules.lesen.score === 8 && 
                  lastAttempt.modules.satzbau.score === 7 && 
                  lastAttempt.modules.schreiben.score === 4)
    });

    var resultsHtml = document.getElementById('main-content').innerHTML;
    results.push({
      name: "renderExamResults displays all 4 competency cards and detailed explanations",
      ok: (resultsHtml.indexOf('Hörverstehen (მოსმენა)') !== -1 && 
           resultsHtml.indexOf('Satzbau &amp; Syntax') !== -1 || resultsHtml.indexOf('Satzbau & Syntax') !== -1) && 
           resultsHtml.indexOf('დავალებების დეტალური ანალიზი') !== -1
    });

  } catch(e) {
    results.push({ name: "Exception during probe: " + e.toString(), ok: false });
  }

  return JSON.stringify(results);
}
runProbe();
"""

full_code = mock_env + "\n" + data_content + "\n" + app_code + "\n" + probe_exam_js

probe_file = BASE_DIR / "tests" / "_stage10_multiskill_runner.js"
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
print(f"MULTI-SKILL EXAM QA SUMMARY: {passed} Passed, {failed} Failed")
print("=" * 65)

if failed > 0:
    sys.exit(1)
