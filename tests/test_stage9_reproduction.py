#!/usr/bin/env python3
"""
STAGE 9 DEFECT REPRODUCTION HARNESS
Demonstrates the remaining defects identified in Stage 9 review.
"""

import subprocess
import json
import re
from pathlib import Path

BASE_DIR = Path("/Users/shotachitaishvili/Documents/German A1")

mock_env = """
var window = { 
  location: { href: "http://localhost:8000" },
  addEventListener: function() {},
  matchMedia: function() { return { matches: false }; },
  scrollTo: function() {}
};
var globalThis = window;
var document = {
  getElementById: function(id) { 
    return { 
      innerHTML: "", 
      style: {}, 
      appendChild: function(){}, 
      classList: { add: function(){}, remove: function(){}, contains: function(){ return false; } }, 
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

def run_jscore_probe(js_code):
    data_content = (BASE_DIR / "js" / "data.js").read_text(encoding="utf-8")
    app_content = (BASE_DIR / "js" / "app.js").read_text(encoding="utf-8")
    full_code = mock_env + "\n" + data_content + "\n" + app_content + "\n" + js_code
    probe_file = BASE_DIR / "tests" / "_stage9_repro_runner.js"
    probe_file.write_text(full_code, encoding="utf-8")
    try:
        res = subprocess.run(["osascript", "-l", "JavaScript", str(probe_file)], capture_output=True, text=True)
        return res.stdout, res.stderr, res.returncode
    finally:
        if probe_file.exists():
            probe_file.unlink()

def main():
    print("="*65)
    print("       DEUTSCH A1 PRO — STAGE 9 DEFECT REPRODUCTION")
    print("="*65)

    # 1. Fake grammar completion
    probe_grammar = """
var app = window.DeutschApp;
localStorage.clear();
// Student simply OPENS lesson 1 without reading or answering anything
app.openLesson(1);
var u = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var grammarState = (u.lessonSkillProgress && u.lessonSkillProgress[1]) ? u.lessonSkillProgress[1].grammarReviewed : false;
var out = { fakeGrammarCompleted: (grammarState === true) };
JSON.stringify(out);
"""
    out, err, code = run_jscore_probe(probe_grammar)
    if code != 0:
        print(f"Probe 1 error: {err}")
    res1 = json.loads(out.strip() or "{}")
    if res1.get("fakeGrammarCompleted"):
        print("  [CONFIRMED DEFECT 9.1] Fake Grammar Completion: openLesson(1) automatically marked grammarReviewed = true!")

    # 2. Fake vocabulary completion
    probe_vocab = """
var app = window.DeutschApp;
localStorage.clear();
// Student clicks trainLessonFlashcards(1) but flips ZERO cards
app.trainLessonFlashcards(1);
var u = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var vocabState = (u.lessonSkillProgress && u.lessonSkillProgress[1]) ? u.lessonSkillProgress[1].vocabPracticed : false;
var out = { fakeVocabCompleted: (vocabState === true) };
JSON.stringify(out);
"""
    out, err, code = run_jscore_probe(probe_vocab)
    if code != 0:
        print(f"Probe 2 error: {err}")
    res2 = json.loads(out.strip() or "{}")
    if res2.get("fakeVocabCompleted"):
        print("  [CONFIRMED DEFECT 9.2] Fake Vocabulary Completion: trainLessonFlashcards(1) automatically marked vocabPracticed = true!")

    # 3. Unassessed Writing Lab completion
    probe_writing = """
var app = window.DeutschApp;
localStorage.clear();
app.setTab('labs');
app.switchLabTab('schreiben');
// Student types 15 random words in Task 2 (Letter)
app.onSchreibenTextInput("word word word word word word word word word word word word word word word");
app.submitSchreibenLetter();
var u = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var scoreSaved = u.labScores && u.labScores.schreiben && (u.labScores.schreiben['s_lab_1'] || u.labScores.schreiben['s_lab_2']);
var xpAwarded = u.xp;
var out = { 
  completedWithoutRubric: (scoreSaved && scoreSaved.completed === true),
  xpWithoutRubric: xpAwarded
};
JSON.stringify(out);
"""
    out, err, code = run_jscore_probe(probe_writing)
    if code != 0:
        print(f"Probe 3 error: {err}")
    res3 = json.loads(out.strip() or "{}")
    if res3.get("completedWithoutRubric") and res3.get("xpWithoutRubric", 0) > 0:
        print(f"  [CONFIRMED DEFECT 9.3] Writing Assessment: Writing task completed and awarded {res3['xpWithoutRubric']} XP without any self-review rubric!")
    else:
        print(f"Probe 3 result: {res3}")

    # 4. External CDN and Font Dependencies in index.html
    html_content = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    has_tailwind_cdn = "cdn.tailwindcss.com" in html_content
    has_google_fonts = "fonts.googleapis.com" in html_content or "fonts.gstatic.com" in html_content
    if has_tailwind_cdn or has_google_fonts:
        print(f"  [CONFIRMED DEFECT 9.4] External CDN Dependencies in index.html:")
        if has_tailwind_cdn:
            print("    • cdn.tailwindcss.com script present")
        if has_google_fonts:
            print("    • Google Fonts preconnect/stylesheet links present")

    print("="*65)

if __name__ == "__main__":
    main()
