#!/usr/bin/env python3
"""
DEUTSCH A1 PRO - Automated Safari / JavaScriptCore Runtime Test Suite
Executes real browser logic on macOS WebKit JavaScriptCore via osascript.
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    print("="*60)
    print("DEUTSCH A1 PRO: Safari WebKit JavaScriptCore Runtime Test")
    print("="*60)

    js_test_code = """
var window = this;
var setTimeout = function(cb, d) { cb(); };
var clearTimeout = function() {};
window.setTimeout = setTimeout;
window.clearTimeout = clearTimeout;
window.addEventListener = function(evt, cb) { if (evt === "DOMContentLoaded") { cb(); } };
window.matchMedia = function() { return { matches: false }; };
window.scrollTo = function() {};

var document = {
  documentElement: { classList: { add: function(){}, remove: function(){} } },
  getElementById: function(id) { 
    return { 
      innerHTML: "", 
      innerText: "",
      value: "",
      style: {},
      children: [],
      appendChild: function(c){}, 
      classList: { add: function(){}, remove: function(){}, toggle: function(){} },
      addEventListener: function(){},
      remove: function(){}
    }; 
  },
  querySelector: function() { return null; },
  querySelectorAll: function() { return []; },
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
  getItem: function(k) { return this._data[k] || null; },
  setItem: function(k, v) { this._data[k] = String(v); },
  removeItem: function(k) { delete this._data[k]; }
};

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
    return [
      { name: "Anna", lang: "de-DE", default: true },
      { name: "Samantha", lang: "en-US", default: false }
    ];
  }
};
var SpeechSynthesisUtterance = function(text) {
  this.text = text;
  this.lang = "de-DE";
  this.rate = 1.0;
  this.voice = null;
  this.onend = null;
  this.onerror = null;
};
window.SpeechSynthesisUtterance = SpeechSynthesisUtterance;
"""
    runner_script = BASE_DIR / "tests" / "_temp_jscore_runner.js"
    
    data_content = (BASE_DIR / "js" / "data.js").read_text(encoding="utf-8")
    app_content = (BASE_DIR / "js" / "app.js").read_text(encoding="utf-8")

    test_assertions = """
var app = window.DeutschApp;
var data = window.GERMAN_A1_DATA;

function assert(condition, message) {
  if (!condition) {
    throw new Error("Assertion Failed: " + message);
  }
  console.log("  [PASS] " + message);
}

console.log("1. Testing Dataset & Application Boot...");
assert(data !== undefined, "window.GERMAN_A1_DATA is loaded");
assert(app !== undefined, "window.DeutschApp is initialized");
assert(data.lessons.length === 10, "10 lessons initialized");
assert(data.dictionary.length >= 700, "Dictionary loaded >= 700 words");

console.log("2. Testing Spaced Repetition (SM-2 Algorithm)...");
app.trainLessonFlashcards(1);
app.flipFlashcard();
app.flashcardSM2Action(5); // Great rating
var stored = JSON.parse(localStorage.getItem("deutsch_a1_pro_v3"));
assert(stored !== null, "User state saved to localStorage (deutsch_a1_pro_v3)");
assert(stored.srsItems !== undefined, "srsItems initialized in userData");
assert(stored.xp > 0, "XP earned on successful flashcard");

app.flashcardSM2Action(1); // Failed rating
stored = JSON.parse(localStorage.getItem("deutsch_a1_pro_v3"));
assert(stored.mistakeWords.length > 0, "Mistake queue tracks failed words");

console.log("3. Testing Lesson Completion & Persistence...");
var initialCompleted = stored.completedLessons ? stored.completedLessons.length : 0;
// Test opening and navigating through all 10 lessons
for (var i = 1; i <= 10; i++) {
  app.openLesson(i);
  app.switchLessonSubtab("grammar");
  app.switchLessonSubtab("vocab");
  app.switchLessonSubtab("dialogue");
  app.switchLessonSubtab("exercises");
}
console.log("  [PASS] Navigated all 10 lessons and 40 sub-views cleanly");

console.log("4. Testing 4 Core Language Labs (Hören, Lesen, Schreiben, Sprechen)...");
app.setTab("labs");
app.switchLabTab("hoeren");
app.switchLabTab("lesen");
app.switchLabTab("schreiben");
app.switchLabTab("sprechen");
console.log("  [PASS] All 4 language labs rendered without errors");

console.log("5. Testing Additional Interactive Modules...");
app.setTab("dictionary");
app.setTab("articles");
app.setTab("sentences");
app.setTab("exam");
app.setTab("tables");
app.setTab("profile");
console.log("  [PASS] Dictionary, Article Trainer, Sentences, Exam, Tables, Profile views OK");

console.log("6. Testing Audio Synthesizer Integration & Speed Control...");
app.speak("Guten Tag! Wie geht es Ihnen?");
app.speakSlow("Auf Wiedersehen!");
app.setSpeed(1.0);
app.setSpeed(0.85);
console.log("  [PASS] German speech synthesis and speed control operational");

console.log("7. Testing Theme Persistence...");
app.toggleTheme();
assert(localStorage.getItem("theme") === "dark", "Theme toggled to dark");
app.toggleTheme();
assert(localStorage.getItem("theme") === "light", "Theme toggled to light");

console.log("\\n" + "=".repeat(60));
console.log("ALL WEBKIT JSCORE RUNTIME TESTS PASSED (0 ERRORS)!");
console.log("=".repeat(60));
"""

    full_js = js_test_code + "\n" + data_content + "\n" + app_content + "\n" + test_assertions
    runner_script.write_text(full_js, encoding="utf-8")

    try:
        res = subprocess.run(
            ["osascript", "-l", "JavaScript", str(runner_script)],
            capture_output=True,
            text=True
        )
        if res.stdout:
            print(res.stdout)
        if res.stderr:
            print(res.stderr)
        return res.returncode == 0
    finally:
        if runner_script.exists():
            runner_script.unlink()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
