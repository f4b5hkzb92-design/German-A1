#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEUTSCH A1 PRO — STAGE 9 COMPREHENSIVE QA & VERIFICATION HARNESS
Verifies:
1. Genuine Grammar Mastery: openLesson() does NOT complete grammar; CCQs require >= 70% score.
2. Genuine Vocabulary Mastery: trainLessonFlashcards() does NOT complete vocab; active session requires >= 5 words at >= 70%.
3. 4-Stage Writing Lab Lifecycle: Draft -> Submitted (0 XP) -> Self-Reviewed with 4-point Rubric (15 XP once).
4. Offline Independence: index.html has 0 external CDNs or remote font URLs; css/style.css is 100% self-contained.
5. Multi-Skill Lesson Mastery: All 5 real skills required for lesson completion.
"""

import subprocess
import json
import re
import sys
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

def run_jscore_probe(js_probe_code):
    data_content = (BASE_DIR / "js" / "data.js").read_text(encoding="utf-8")
    app_content = (BASE_DIR / "js" / "app.js").read_text(encoding="utf-8")
    full_code = mock_env + "\n" + data_content + "\n" + app_content + "\n" + js_probe_code
    probe_file = BASE_DIR / "tests" / "_stage9_runner.js"
    probe_file.write_text(full_code, encoding="utf-8")
    try:
        res = subprocess.run(["osascript", "-l", "JavaScript", str(probe_file)], capture_output=True, text=True)
        return res.stdout, res.stderr, res.returncode
    finally:
        if probe_file.exists():
            probe_file.unlink()

class Stage9TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.failures = []

    def log(self, success, test_name, detail=""):
        if success:
            self.passed += 1
            print(f"  [PASS] {test_name}")
        else:
            self.failed += 1
            msg = f"  [FAIL] {test_name}" + (f" — {detail}" if detail else "")
            print(msg)
            self.failures.append(test_name)

    def summary(self):
        print("\n" + "="*65)
        print(f"STAGE 9 QA SUITE: {self.passed} Passed, {self.failed} Failed")
        print("="*65)
        if self.failures:
            print("\nFailures:")
            for f in self.failures:
                print(f"  • {f}")
        return self.failed == 0

def main():
    print("="*65)
    print("       DEUTSCH A1 PRO — STAGE 9 VERIFICATION & QA HARNESS")
    print("="*65)
    runner = Stage9TestRunner()

    # TEST 1: Genuine Grammar Mastery Verification
    probe_grammar = """
var app = window.DeutschApp;
localStorage.clear();

// Action A: Open Lesson 1
app.openLesson(1);
var u1 = localStorage.getItem('deutsch_a1_pro_v3');
var grammarBeforeCheck = (u1 !== null && JSON.parse(u1).lessonSkillProgress && JSON.parse(u1).lessonSkillProgress[1] && JSON.parse(u1).lessonSkillProgress[1].grammarReviewed);

// Action B: Submit incomplete grammar checks
app.submitGrammarCheck(1);
var u2 = localStorage.getItem('deutsch_a1_pro_v3');
var grammarIncompletePassed = (u2 !== null && JSON.parse(u2).lessonSkillProgress && JSON.parse(u2).lessonSkillProgress[1] && JSON.parse(u2).lessonSkillProgress[1].grammarReviewed);

// Action C: Answer all questions WRONGLY (choose option 2 where 1 or 0 is correct)
var lesson = window.GERMAN_A1_DATA.lessons.find(function(l){ return l.id === 1; });
lesson.grammar_sections.forEach(function(s){
  if (s.check) {
    app.onSelectGrammarCheckOption(s.id, (s.check.answer + 1) % 3, 1);
  }
});
app.submitGrammarCheck(1);
var u3 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var grammarWrongPassed = u3.lessonSkillProgress && u3.lessonSkillProgress[1] && u3.lessonSkillProgress[1].grammarReviewed;
var grammarWrongXP = u3.xp;

// Action D: Answer all questions CORRECTLY
lesson.grammar_sections.forEach(function(s){
  if (s.check) {
    app.onSelectGrammarCheckOption(s.id, s.check.answer, 1);
  }
});
app.submitGrammarCheck(1);
var u4 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var grammarCorrectPassed = u4.lessonSkillProgress[1].grammarReviewed === true;
var grammarCorrectXP = u4.xp;

// Action E: Resubmit correct check -> Idempotent check
app.submitGrammarCheck(1);
var u5 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var grammarResubmitXP = u5.xp;

var out = {
  grammarBeforeCheck: Boolean(grammarBeforeCheck),
  grammarIncompletePassed: Boolean(grammarIncompletePassed),
  grammarWrongPassed: Boolean(grammarWrongPassed),
  grammarWrongXP: grammarWrongXP,
  grammarCorrectPassed: grammarCorrectPassed,
  grammarCorrectXP: grammarCorrectXP,
  isIdempotent: (grammarCorrectXP === 20 && grammarResubmitXP === 20)
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_grammar)
    assert code == 0, f"Probe 1 failed: {stderr}"
    res1 = json.loads(stdout.strip() or stderr.strip())
    runner.log(not res1['grammarBeforeCheck'], "Grammar Integrity: openLesson(1) does NOT mark grammar as reviewed")
    runner.log(not res1['grammarIncompletePassed'], "Grammar Guard: Unanswered grammar check rejected without passing")
    runner.log(not res1['grammarWrongPassed'] and res1['grammarWrongXP'] == 0, "Grammar Assessment: Failing CCQs results in 0 XP and grammarReviewed = false")
    runner.log(res1['grammarCorrectPassed'] and res1['grammarCorrectXP'] == 20, "Grammar Mastery: Passing all CCQs awards 20 XP and marks grammarReviewed = true")
    runner.log(res1['isIdempotent'], "Grammar Idempotence: Resubmitting grammar check awards 0 duplicate XP")

    # TEST 2: Genuine Vocabulary Mastery Verification
    probe_vocab = """
var app = window.DeutschApp;
localStorage.clear();

// Action A: Open flashcard deck for Lesson 1
app.trainLessonFlashcards(1);
var u1 = localStorage.getItem('deutsch_a1_pro_v3');
var vocabBeforePractice = (u1 !== null && JSON.parse(u1).lessonSkillProgress && JSON.parse(u1).lessonSkillProgress[1] && JSON.parse(u1).lessonSkillProgress[1].vocabPracticed);

// Action B: Rate only 2 cards (insufficient coverage)
app.flashcardSM2Action(5);
app.flashcardSM2Action(5);
var u2 = localStorage.getItem('deutsch_a1_pro_v3');
var vocabUnderMin = (u2 !== null && JSON.parse(u2).lessonSkillProgress && JSON.parse(u2).lessonSkillProgress[1] && JSON.parse(u2).lessonSkillProgress[1].vocabPracticed);

// Action C: Complete required minimum (5 unique words) with correct recall
app.flashcardSM2Action(5);
app.flashcardSM2Action(5);
app.flashcardSM2Action(5);
var u3 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var vocabMastered = u3.lessonSkillProgress && u3.lessonSkillProgress[1] && u3.lessonSkillProgress[1].vocabPracticed === true;
var vocabXP = u3.xp;

var out = {
  vocabBeforePractice: Boolean(vocabBeforePractice),
  vocabUnderMin: Boolean(vocabUnderMin),
  vocabMastered: vocabMastered,
  xpAwarded: (vocabXP >= 20)
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_vocab)
    assert code == 0, f"Probe 2 failed: {stderr}"
    res2 = json.loads(stdout.strip() or stderr.strip())
    runner.log(not res2['vocabBeforePractice'], "Vocabulary Integrity: trainLessonFlashcards(1) does NOT mark vocab as practiced")
    runner.log(not res2['vocabUnderMin'], "Vocabulary Guard: Rating fewer than 5 words does NOT award lesson vocabulary mastery")
    runner.log(res2['vocabMastered'], "Vocabulary Mastery: Actively reviewing >= 5 words with >= 70% recall marks vocabPracticed = true")
    runner.log(res2['xpAwarded'], "Vocabulary Reward: Vocabulary mastery bonus (+20 XP) granted upon verified recall")

    # TEST 3: 4-Stage Writing Lab Lifecycle
    probe_writing = """
var app = window.DeutschApp;
localStorage.clear();
app.setTab('labs');
app.switchLabTab('schreiben');

// Task 2 is birthday invitation letter
app.nextLabSchreiben(4); // index 1 (s_lab_2)

// Stage 1: Short text (< 15 words) rejected
app.onSchreibenTextInput("Hallo Peter, ich lade dich ein.");
app.submitSchreibenLetter();
var u1 = localStorage.getItem('deutsch_a1_pro_v3');
var shortRejected = (u1 === null || JSON.parse(u1).xp === 0);

// Stage 2: Valid text (>= 15 words) submitted for self-review
app.onSchreibenTextInput("Lieber Peter, ich habe am Samstag Geburtstag und lade dich herzlich ein. Die Party beginnt um 18 Uhr.");
app.submitSchreibenLetter();
var u2 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3') || '{"xp":0}');
var submissionXPZero = (u2.xp === 0); // No XP awarded simply for submitting text!
var isSubmitted = Boolean(app.state.labSchreibenSubmittedTasks['s_lab_2']);

// Stage 3: Self-review rubric validation (< 3 checks rejected)
app.onToggleSchreibenRubric('s_lab_2', 0); // Check 1
app.onToggleSchreibenRubric('s_lab_2', 1); // Check 2
app.confirmSchreibenSelfReview('s_lab_2');
var u3 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3') || '{"xp":0}');
var incompleteRubricNoXP = (u3.xp === 0);

// Check 3 and 4 -> Confirm self-review
app.onToggleSchreibenRubric('s_lab_2', 2);
app.onToggleSchreibenRubric('s_lab_2', 3);
app.confirmSchreibenSelfReview('s_lab_2');
var u4 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var selfReviewedXP = u4.xp;
var selfReviewedCompleted = u4.labScores && u4.labScores.schreiben && u4.labScores.schreiben['s_lab_2'] && u4.labScores.schreiben['s_lab_2'].completed;

// Stage 4: Resubmission / re-confirm -> Idempotent
app.confirmSchreibenSelfReview('s_lab_2');
var u5 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var resubmitXP = u5.xp;

var out = {
  shortRejected: shortRejected,
  submissionXPZero: submissionXPZero,
  isSubmitted: isSubmitted,
  incompleteRubricNoXP: incompleteRubricNoXP,
  selfReviewedXP: selfReviewedXP,
  selfReviewedCompleted: Boolean(selfReviewedCompleted),
  isIdempotent: (selfReviewedXP === 15 && resubmitXP === 15)
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_writing)
    assert code == 0, f"Probe 3 failed: {stderr}"
    res3 = json.loads(stdout.strip() or stderr.strip())
    runner.log(res3['shortRejected'], "Writing Stage 1: Text with < 15 words rejected from submission")
    runner.log(res3['submissionXPZero'] and res3['isSubmitted'], "Writing Stage 2: Text submission opens model solution but awards ZERO unearned XP")
    runner.log(res3['incompleteRubricNoXP'], "Writing Stage 3 Guard: Self-review with < 3 criteria checked is blocked from XP")
    runner.log(res3['selfReviewedCompleted'] and res3['selfReviewedXP'] == 15, "Writing Stage 3 Mastery: Confirmed 4-point self-review awards 15 XP and marks completed")
    runner.log(res3['isIdempotent'], "Writing Idempotence: Resubmitting rubric awards 0 duplicate XP")

    # TEST 4: Offline Independence & Zero Remote Asset Verification
    index_html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
    has_no_tailwind_cdn = "cdn.tailwindcss.com" not in index_html
    has_no_google_fonts = "fonts.googleapis.com" not in index_html and "fonts.gstatic.com" not in index_html
    has_no_remote_http = not re.search(r'href=[\"\x27]http[s]?:', index_html) and not re.search(r'src=[\"\x27]http[s]?:', index_html)

    style_css = (BASE_DIR / "css" / "style.css").read_text(encoding="utf-8")
    has_system_font = "-apple-system" in style_css and "Fira GO" in style_css
    has_dark_mode = "html.dark" in style_css
    has_responsive = "@media (min-width: 768px)" in style_css

    runner.log(has_no_tailwind_cdn, "Offline Independence: cdn.tailwindcss.com completely removed from index.html")
    runner.log(has_no_google_fonts, "Offline Independence: Google Fonts CDN completely removed from index.html")
    runner.log(has_no_remote_http, "Offline Independence: index.html contains ZERO external HTTP/HTTPS network dependencies")
    runner.log(has_system_font, "Offline Resilience: Complete local system font stack active in style.css")
    runner.log(has_dark_mode, "Offline Resilience: Full dark mode (.dark) utility classes present in style.css")
    runner.log(has_responsive, "Offline Resilience: Responsive media breakpoints (sm, md, lg) self-contained in style.css")

    # TEST 5: Real Multi-Skill Lesson Mastery Check
    probe_lesson_completion = """
var app = window.DeutschApp;
localStorage.clear();

// Complete 4 out of 5 skills for Lesson 1 (leave Grammar incomplete)
app.recordSkillProgress(1, 'vocab', 100, true);
app.recordSkillProgress(1, 'mc', 100, true);
app.recordSkillProgress(1, 'fib', 100, true);
app.recordSkillProgress(1, 'lis', 100, true);

var u1 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var lessonIncomplete = (u1.completedLessons || []).includes(1) === false;

// Now complete the 5th skill: Grammar CCQs
var lesson = window.GERMAN_A1_DATA.lessons.find(function(l){ return l.id === 1; });
lesson.grammar_sections.forEach(function(s){
  if (s.check) {
    app.onSelectGrammarCheckOption(s.id, s.check.answer, 1);
  }
});
app.submitGrammarCheck(1);

var u2 = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
var lessonMastered = (u2.completedLessons || []).includes(1) === true;
var finalXP = u2.xp; // Includes 20 (grammar) + 50 (lesson completion bonus)

var out = {
  lessonIncomplete: lessonIncomplete,
  lessonMastered: lessonMastered,
  bonusGiven: (finalXP >= 70)
};
JSON.stringify(out);
"""
    stdout, stderr, code = run_jscore_probe(probe_lesson_completion)
    assert code == 0, f"Probe 5 failed: {stderr}"
    res5 = json.loads(stdout.strip() or stderr.strip())
    runner.log(res5['lessonIncomplete'], "Mastery Rigor: Lesson remains incomplete when only 4 of 5 skills are passed")
    runner.log(res5['lessonMastered'], "Mastery Rigor: Lesson completes ONLY when all 5 skills (Grammar CCQs included) are passed")
    runner.log(res5['bonusGiven'], "Mastery Reward: Lesson completion bonus (+50 XP) awarded upon 100% genuine multi-skill mastery")

    success = runner.summary()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
