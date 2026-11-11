#!/usr/bin/env python3
"""
DEUTSCH A1 PRO — STAGE 8 VERIFICATION & REGRESSION SUITE
Comprehensive test harness verifying:
1. Idempotent Rewards & XP exploit prevention
2. Genuine Reading Lab assessment & score validation
3. 5-Skill Lesson Mastery criteria (Grammar, Vocab, MC, FIB, Listening)
4. Local calendar date & midnight boundary streak calculation
5. Exam attempt history, retake independence, and first-pass reward limit
6. Storage migration, reset safety, legacy key purge & corrupt data recovery
7. Offline stylesheets and bilingual typography integrity
"""

import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Stage8TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []

    def log_result(self, ok, test_name, detail=""):
        if ok:
            self.passed += 1
            print(f"  [PASS] {test_name}")
        else:
            self.failed += 1
            msg = f"{test_name} — {detail}" if detail else test_name
            self.failures.append(msg)
            print(f"  [FAIL] {msg}")

    def summary(self):
        print("\n" + "="*65)
        print(f"STAGE 8 QA SUITE: {self.passed} Passed, {self.failed} Failed")
        print("="*65)
        if self.failures:
            print("\nFailures:")
            for f in self.failures:
                print(f"  • {f}")
            return False
        return True

def run_jscore_probe(js_probe_code):
    mock_env = """
var window = this;
if (typeof console === "undefined") {
  var console = { log: function(){}, error: function(){}, warn: function(){} };
} else {
  console.error = console.error || console.log;
  console.warn = console.warn || console.log;
}
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
    return {
      innerHTML: "",
      innerText: "",
      value: "",
      style: {},
      classList: { add: function(){}, remove: function(){}, toggle: function(){} },
      appendChild: function(){},
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
  getItem: function(k) { return this._data[k] !== undefined ? this._data[k] : null; },
  setItem: function(k, v) { this._data[k] = String(v); },
  removeItem: function(k) { delete this._data[k]; },
  clear: function() { this._data = {}; }
};

var confirm = function() { return true; };
var alert = function() {};
window.confirm = confirm;
window.alert = alert;

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
"""
    data_content = (BASE_DIR / "js" / "data.js").read_text(encoding="utf-8")
    app_content = (BASE_DIR / "js" / "app.js").read_text(encoding="utf-8")

    full_code = mock_env + "\n" + data_content + "\n" + app_content + "\n" + js_probe_code
    probe_file = BASE_DIR / "tests" / "_stage8_runner.js"
    probe_file.write_text(full_code, encoding="utf-8")
    try:
        res = subprocess.run(["osascript", "-l", "JavaScript", str(probe_file)], capture_output=True, text=True)
        return res.stdout, res.stderr, res.returncode
    finally:
        if probe_file.exists():
            probe_file.unlink()

def main():
    print("="*65)
    print("       DEUTSCH A1 PRO — STAGE 8 VERIFICATION & QA HARNESS")
    print("="*65)

    runner = Stage8TestRunner()

    # TEST 1: XP Exploit Prevention on Repeated Reading Lab Submissions
    probe_xp_exploit = """
var app = window.DeutschApp;
app.setTab('labs');
app.switchLabTab('lesen');

// Answer question 0 and 1 correctly on reading task 1
app.onSelectLabLesen(0, 0);
app.onSelectLabLesen(1, 0);
app.onSelectLabLesen(2, 0); // 3 of 3 answered correctly

app.submitLabLesen();
var data1 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var xp1 = data1.xp;

// Resubmit same task
app.submitLabLesen();
var data2 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var xp2 = data2.xp;

// Resubmit third time
app.submitLabLesen();
var data3 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var xp3 = data3.xp;

var out = {
  initialXP: xp1,
  afterResubmit1: xp2,
  afterResubmit2: xp3,
  isIdempotent: (xp1 === 15 && xp2 === 15 && xp3 === 15)
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_xp_exploit)
    assert code == 0, f"Probe 1 failed: {stderr}"
    res1 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(res1['isIdempotent'], "XP Exploit Prevention: submitLabLesen awards 15 XP once and 0 on repeated retries", f"XP progression: {res1['initialXP']} -> {res1['afterResubmit1']} -> {res1['afterResubmit2']}")

    # TEST 2: Genuine Reading Lab Grading & Incomplete Submission Guard
    probe_lesen_grading = """
var app = window.DeutschApp;
localStorage.clear();
var data = window.GERMAN_A1_DATA;
app.setTab('labs');
app.switchLabTab('lesen');

// Case A: Submit with ZERO answers
app.submitLabLesen();
var stateAfterEmpty = localStorage.getItem('deutsch_a1_pro_v3');
var emptyBlocked = (stateAfterEmpty === null || JSON.parse(stateAfterEmpty).xp === 0);

// Case B: Answer all WRONGLY (choose option 3 where 0 is correct)
app.onSelectLabLesen(0, 3);
app.onSelectLabLesen(1, 3);
app.onSelectLabLesen(2, 3);
app.submitLabLesen();
var stateAfterFail = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var failBlockedFromXP = (stateAfterFail.xp === 0);
var taskScoreSaved = stateAfterFail.labScores && stateAfterFail.labScores.lesen && stateAfterFail.labScores.lesen['l_lab_1'];
var failRecorded = taskScoreSaved && taskScoreSaved.score === 0 && taskScoreSaved.passed === false;

var out = {
  emptyBlocked: emptyBlocked,
  failBlockedFromXP: failBlockedFromXP,
  failRecorded: failRecorded
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_lesen_grading)
    assert code == 0, f"Probe 2 failed: {stderr}"
    res2 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(res2['emptyBlocked'], "Reading Lab Guard: Unanswered submission rejected without awarding XP")
    runner.log_result(res2['failBlockedFromXP'], "Reading Lab Grading: All-wrong answers receive 0 XP and failed status")
    runner.log_result(res2['failRecorded'], "Reading Lab Persistence: Task performance recorded with score 0/3, passed=false")

    # TEST 3: 5-Skill Lesson Mastery (60% MC does NOT complete lesson)
    probe_lesson_mastery = """
var app = window.DeutschApp;
localStorage.clear();

// Case A: User only passes MC (e.g. 100%)
app.openLesson(1);
// Simulate MC completion
app.recordSkillProgress(1, 'mc', 100, true);
var userA = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var completedA = (userA.completedLessons || []).includes(1);

// Case B: Complete all 5 skills (Grammar, Vocab, MC, FIB, Listening)
app.recordSkillProgress(1, 'grammar', 100, true);
app.recordSkillProgress(1, 'vocab', 100, true);
app.recordSkillProgress(1, 'fib', 100, true);
app.recordSkillProgress(1, 'lis', 100, true);
var userB = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var completedB = (userB.completedLessons || []).includes(1);
var completionXP = userB.xp >= 50; // Completion bonus +50 XP granted

var out = {
  mcAloneCompleted: completedA,
  allSkillsCompleted: completedB,
  completionXPGiven: completionXP
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_lesson_mastery)
    assert code == 0, f"Probe 3 failed: {stderr}"
    res3 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(not res3['mcAloneCompleted'], "Lesson Mastery Integrity: 100% MC alone does NOT complete the lesson")
    runner.log_result(res3['allSkillsCompleted'], "Lesson Mastery Integrity: Lesson marks completed only when all 5 skills pass")
    runner.log_result(res3['completionXPGiven'], "Lesson Mastery Bonus: +50 XP completion bonus awarded upon full mastery")

    # TEST 4: Streak Date & Midnight Boundary Math
    probe_streak_math = """
var app = window.DeutschApp;
var d1 = "2026-11-11";
var d2 = "2026-11-12";
var d3 = "2026-11-14";

var diffConsecutive = app.getCalendarDaysDiff(d1, d2);
var diffMissed = app.getCalendarDaysDiff(d1, d3);
var diffSameDay = app.getCalendarDaysDiff(d1, d1);

var out = {
  diffConsecutive: diffConsecutive,
  diffMissed: diffMissed,
  diffSameDay: diffSameDay,
  localDateValid: /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/.test(app.getLocalDateString())
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_streak_math)
    assert code == 0, f"Probe 4 failed: {stderr}"
    res4 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(res4['diffConsecutive'] == 1, "Streak Engine: Consecutive days return exact diff = 1")
    runner.log_result(res4['diffMissed'] == 3, "Streak Engine: Skipped days return diff = 3 (triggers streak reset to 1)")
    runner.log_result(res4['diffSameDay'] == 0, "Streak Engine: Same day actions return diff = 0 (prevents duplicate streak increment)")
    runner.log_result(res4['localDateValid'], "Streak Engine: getLocalDateString returns valid YYYY-MM-DD local calendar date")

    # TEST 5: Exam Attempt History & Retake Independence
    probe_exam_reliability = """
var app = window.DeutschApp;
localStorage.clear();
var questions = window.GERMAN_A1_DATA.final_exam_questions;

// Answer all 25 questions correctly
questions.forEach(function(q) {
  app.onExamAnswer(q.id, q.answer);
});

// Submit Attempt 1
app.submitExam();
var state1 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var xpAttempt1 = state1.xp;
var history1Len = (state1.examHistory || []).length;

// Retake and submit Attempt 2
app.retakeExam();
questions.forEach(function(q) {
  app.onExamAnswer(q.id, q.answer);
});
app.submitExam();
var state2 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var xpAttempt2 = state2.xp;
var history2Len = (state2.examHistory || []).length;

var out = {
  firstPassXP: xpAttempt1,
  secondPassXP: xpAttempt2,
  noRetakeXPFarm: (xpAttempt1 === 100 && xpAttempt2 === 100),
  historyMaintained: (history1Len === 1 && history2Len === 2),
  attempt2RecordedCorrectly: state2.examHistory[1].attempt === 2
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_exam_reliability)
    assert code == 0, f"Probe 5 failed: {stderr}"
    res5 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(res5['firstPassXP'] == 100, "Exam Reliability: First passing attempt awards 100 XP")
    runner.log_result(res5['noRetakeXPFarm'], "Exam Reliability: Retaking the exam does NOT grant duplicate +100 XP")
    runner.log_result(res5['historyMaintained'], "Exam Reliability: Each attempt is independently appended to examHistory")

    # TEST 6: State Reset & Legacy Data Resurrection Prevention
    probe_reset_safety = """
var app = window.DeutschApp;
localStorage.clear();

// Put legacy v2 and v1 data into storage
localStorage.setItem('deutsch_a1_pro_v2', JSON.stringify({ xp: 8888, streak: 30 }));
localStorage.setItem('deutsch_a1_user_data_v1', JSON.stringify({ xp: 7777 }));

// Perform full reset
app.resetAllProgress();

var v3Clean = localStorage.getItem('deutsch_a1_pro_v3');
var v2Clean = localStorage.getItem('deutsch_a1_pro_v2');
var v1Clean = localStorage.getItem('deutsch_a1_user_data_v1');
var sentinelSet = localStorage.getItem('deutsch_a1_reset_marker_v3');

// Reload user data as if page reloaded
var reloaded = app.loadUserData();

var out = {
  v2Removed: (v2Clean === null),
  v1Removed: (v1Clean === null),
  sentinelSet: (sentinelSet === 'true'),
  noResurrection: (reloaded.xp === 0 && reloaded.streak === 1)
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_reset_safety)
    assert code == 0, f"Probe 6 failed: {stderr}"
    res6 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(res6['v2Removed'], "Reset Safety: Legacy key deutsch_a1_pro_v2 permanently purged on reset")
    runner.log_result(res6['v1Removed'], "Reset Safety: Legacy key deutsch_a1_user_data_v1 permanently purged on reset")
    runner.log_result(res6['noResurrection'], "Reset Safety: Legacy progress does NOT resurrect after reset and reload")

    # TEST 7: Corrupted Storage Recovery
    probe_corrupt_recovery = """
var app = window.DeutschApp;
localStorage.clear();
// Inject corrupted, non-JSON garbage string
localStorage.setItem('deutsch_a1_pro_v3', '{corrupt:not-json');
var recovered = app.loadUserData();

var out = {
  didNotCrash: true,
  safeDefaultsRestored: (recovered.xp === 0 && recovered.streak === 1 && Array.isArray(recovered.completedLessons))
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_corrupt_recovery)
    assert code == 0, f"Probe 7 failed: {stderr}"
    res7 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(res7['safeDefaultsRestored'], "Corrupt Storage Recovery: Invalid JSON handled gracefully without crashing")

    # TEST 8: Writing Lab Validation & Rubrics
    probe_writing_lab = """
var app = window.DeutschApp;
localStorage.clear();
app.setTab('labs');
app.switchLabTab('schreiben');

// Case A: Form with missing fields
app.submitSchreibenForm();
var formState1 = localStorage.getItem('deutsch_a1_pro_v3');
var formBlocked = (formState1 === null || JSON.parse(formState1).xp === 0);

// Case B: Form filled completely
app.onSchreibenFormInput('fn', 'Giorgi');
app.onSchreibenFormInput('ln', 'Beridze');
app.onSchreibenFormInput('bd', '15.05.1998');
app.onSchreibenFormInput('nat', 'georgisch');
app.onSchreibenFormInput('addr', 'Rustaveli 10');
app.onSchreibenFormInput('city', 'Tiflis');
app.submitSchreibenForm();
var formState2 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var formPassedXP = (formState2.xp === 15);

// Resubmit same form -> idempotent check
app.submitSchreibenForm();
var formState3 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var formIdempotent = (formState3.xp === 15);

var out = {
  formBlocked: formBlocked,
  formPassedXP: formPassedXP,
  formIdempotent: formIdempotent
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_writing_lab)
    assert code == 0, f"Probe 8 failed: {stderr}"
    res8 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(res8['formBlocked'], "Writing Lab Guard: Incomplete hotel form rejected with 0 XP")
    runner.log_result(res8['formPassedXP'], "Writing Lab Assessment: Fully filled form awarded 15 XP once")
    runner.log_result(res8['formIdempotent'], "Writing Lab Idempotence: Resubmitting form grants 0 duplicate XP")

    # TEST 9: Sentence Builder Idempotence
    probe_sentence_builder = """
var app = window.DeutschApp;
localStorage.clear();
app.setTab('sentence-builder');

// Solve sentence 0 by picking words in target order
var challenge = window.GERMAN_A1_DATA.sentence_builders[app.state.sbIndex];
challenge.words.forEach(function(targetWord) {
  var idx = app.state.sbAvailableWords.indexOf(targetWord);
  if (idx !== -1) {
    app.addSentenceWord(idx);
  }
});
app.checkSentence();

var sbState1 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var sbXP1 = sbState1 ? sbState1.xp : 0;

// Re-check sentence 0
app.checkSentence();
var sbState2 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var sbXP2 = sbState2 ? sbState2.xp : 0;

var out = {
  firstSolvedXP: sbXP1,
  recheckedXP: sbXP2,
  isIdempotent: (sbXP1 === 15 && sbXP2 === 15)
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_sentence_builder)
    assert code == 0, f"Probe 9 failed: {stderr}"
    res9 = json.loads(stdout.strip() or stderr.strip())
    runner.log_result(res9['isIdempotent'], "Sentence Builder: Repeatedly checking a solved sentence grants 0 duplicate XP", f"XP: {res9['firstSolvedXP']} -> {res9['recheckedXP']}")

    # TEST 10: Offline Stylesheet Completeness & Local System Fonts
    css_file = BASE_DIR / "css" / "style.css"
    css_text = css_file.read_text(encoding="utf-8")
    has_layout_rules = ".max-w-4xl" in css_text and ".grid-cols-1" in css_text and ".flex" in css_text
    has_system_font = "-apple-system" in css_text or "system-ui" in css_text
    no_blocking_imports = "@import url('https://fonts.googleapis.com" not in css_text

    runner.log_result(has_layout_rules, "Offline Resilience: Complete local CSS utility classes present in style.css")
    runner.log_result(has_system_font, "Offline Resilience: Local system font fallback stack active for Georgian/German")
    runner.log_result(no_blocking_imports, "Offline Resilience: Remote blocking @import fonts removed from stylesheet")

    success = runner.summary()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
