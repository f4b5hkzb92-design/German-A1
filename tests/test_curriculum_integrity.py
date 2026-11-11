#!/usr/bin/env python3
"""
DEUTSCH A1 PRO - Automated Curriculum Integrity & Quality Assurance Test Suite
Verifies CEFR A1 coverage, structural completeness, Georgian translations, and exercise integrity.
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_JS = BASE_DIR / "js" / "data.js"

class TestSuite:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def assert_true(self, condition, msg):
        if condition:
            self.passed += 1
            print(f"  [PASS] {msg}")
        else:
            self.failed += 1
            self.errors.append(msg)
            print(f"  [FAIL] {msg}")

    def summary(self):
        print("\n" + "="*60)
        print(f"TEST SUMMARY: {self.passed} Passed, {self.failed} Failed")
        print("="*60)
        if self.errors:
            print("\nFailures:")
            for e in self.errors:
                print(f"  - {e}")
            return False
        return True

def load_dataset():
    assert DATA_JS.exists(), f"data.js not found at {DATA_JS}"
    content = DATA_JS.read_text(encoding="utf-8")
    start = content.find("{")
    end = content.rfind("}") + 1
    return json.loads(content[start:end])

def main():
    print("="*60)
    print("DEUTSCH A1 PRO: Curriculum & Data Integrity Verification")
    print("="*60)

    runner = TestSuite()
    data = load_dataset()

    # 1. Top-Level Keys
    required_keys = ['lessons', 'dictionary', 'article_trainer_words', 'sentence_builders', 'final_exam_questions', 'grammar_tables', 'language_labs']
    for k in required_keys:
        runner.assert_true(k in data, f"Key '{k}' exists in master dataset")

    # 2. Lessons Coverage (10 Lessons)
    lessons = data.get('lessons', [])
    runner.assert_true(len(lessons) == 10, f"Exactly 10 comprehensive lessons present (got {len(lessons)})")

    for idx, l in enumerate(lessons, 1):
        lid = l.get('id')
        runner.assert_true(lid == idx, f"Lesson {idx} has correct ID {idx}")
        runner.assert_true(bool(l.get('title_de')), f"Lesson {idx} has German title: {l.get('title_de')}")
        runner.assert_true(bool(l.get('title_ka')), f"Lesson {idx} has Georgian title: {l.get('title_ka')}")
        
        objectives = l.get('objectives_ka', [])
        runner.assert_true(len(objectives) >= 3, f"Lesson {idx} has >= 3 Georgian CEFR outcomes (found {len(objectives)})")

        grammar_secs = l.get('grammar_sections', [])
        runner.assert_true(len(grammar_secs) >= 2, f"Lesson {idx} has >= 2 deep grammar modules (found {len(grammar_secs)})")
        for g_idx, g in enumerate(grammar_secs, 1):
            runner.assert_true(bool(g.get('title')), f"Lesson {idx} grammar {g_idx} has title: {g.get('title')[:40]}...")
            runner.assert_true(len(g.get('content_ka', '')) > 80, f"Lesson {idx} grammar {g_idx} has comprehensive content (>80 chars)")

        dialogues = l.get('dialogues', [])
        runner.assert_true(len(dialogues) >= 1, f"Lesson {idx} has authentic dialogues (found {len(dialogues)})")
        for d_idx, d in enumerate(dialogues, 1):
            lines = d.get('lines', [])
            runner.assert_true(len(lines) >= 2, f"Lesson {idx} dialogue {d_idx} has >= 2 turns (found {len(lines)})")
            for line in lines:
                runner.assert_true(bool(line.get('speaker')), f"Lesson {idx} dialogue line has speaker")
                runner.assert_true(bool(line.get('text_de')), f"Lesson {idx} dialogue line has German text")
                runner.assert_true(bool(line.get('text_ka')), f"Lesson {idx} dialogue line has Georgian translation")

        exercises = l.get('exercises', {})
        mc_list = exercises.get('multiple_choice', [])
        fib_list = exercises.get('fill_in_blank', [])
        listen_list = exercises.get('listening', [])
        runner.assert_true(len(mc_list) >= 3, f"Lesson {idx} has >= 3 MC exercises (found {len(mc_list)})")
        runner.assert_true(len(fib_list) >= 3, f"Lesson {idx} has >= 3 Fill-in-Blank exercises (found {len(fib_list)})")
        runner.assert_true(len(listen_list) >= 2, f"Lesson {idx} has >= 2 Listening exercises (found {len(listen_list)})")

    # 3. Vocabulary & Lexicon Coverage
    dictionary = data.get('dictionary', [])
    runner.assert_true(len(dictionary) >= 700, f"Master dictionary has >= 700 A1 words (found {len(dictionary)})")
    
    sample_word = dictionary[0]
    for prop in ['id', 'word', 'georgian', 'pos']:
        runner.assert_true(prop in sample_word, f"Dictionary words include property '{prop}'")

    # 4. Article Trainer Word Bank
    article_words = data.get('article_trainer_words', [])
    runner.assert_true(len(article_words) >= 400, f"Article trainer noun pool has >= 400 words (found {len(article_words)})")
    valid_articles = {'der', 'die', 'das'}
    invalid_articles = [w for w in article_words if w.get('article') not in valid_articles]
    runner.assert_true(len(invalid_articles) == 0, f"All article trainer words have valid gender ('der', 'die', 'das')")

    # 5. Sentence Builders
    sentence_builders = data.get('sentence_builders', [])
    runner.assert_true(len(sentence_builders) >= 10, f"Sentence builders count >= 10 (found {len(sentence_builders)})")
    for s_idx, sb in enumerate(sentence_builders, 1):
        runner.assert_true(len(sb.get('words', [])) >= 3, f"Sentence builder {s_idx} has >= 3 chunks")
        runner.assert_true(bool(sb.get('translation_ka')), f"Sentence builder {s_idx} has Georgian translation")

    # 6. Final Exam Specification
    exam_questions = data.get('final_exam_questions', [])
    runner.assert_true(len(exam_questions) >= 20, f"Final diagnostic exam has >= 20 questions (found {len(exam_questions)})")
    for q_idx, q in enumerate(exam_questions, 1):
        runner.assert_true(bool(q.get('question')), f"Exam question {q_idx} has prompt in Georgian/German")
        runner.assert_true(len(q.get('options', [])) >= 3, f"Exam question {q_idx} has >= 3 options")
        runner.assert_true(isinstance(q.get('answer'), int), f"Exam question {q_idx} has valid answer index")
        runner.assert_true(0 <= q.get('answer') < len(q.get('options', [])), f"Exam question {q_idx} answer index within range")

    # 7. Four Language Labs
    labs = data.get('language_labs', {})
    for skill in ['hoeren', 'lesen', 'schreiben', 'sprechen']:
        runner.assert_true(skill in labs, f"Language lab '{skill}' exists in dataset")
        tasks = labs.get(skill, [])
        runner.assert_true(len(tasks) >= 2, f"Language lab '{skill}' has >= 2 authentic tasks (found {len(tasks)})")

    # Hören Lab Check
    for h in labs.get('hoeren', []):
        runner.assert_true(bool(h.get('audio_text')), f"Hören task '{h.get('id')}' has authentic German script")
        runner.assert_true(bool(h.get('transcript_ka')), f"Hören task '{h.get('id')}' has Georgian transcript translation")

    # Lesen Lab Check
    for les in labs.get('lesen', []):
        runner.assert_true(bool(les.get('text_de')), f"Lesen task '{les.get('id')}' has authentic German realia text")
        runner.assert_true(len(les.get('questions', [])) >= 1, f"Lesen task '{les.get('id')}' has questions")

    # Schreiben Lab Check
    for sch in labs.get('schreiben', []):
        if sch.get('type') == 'form':
            runner.assert_true(len(sch.get('fields', [])) >= 3, f"Schreiben form '{sch.get('id')}' has form fields")
        else:
            runner.assert_true(bool(sch.get('model_solution')), f"Schreiben free-text '{sch.get('id')}' has model German answer")
            runner.assert_true(len(sch.get('rubrics', [])) >= 2, f"Schreiben free-text '{sch.get('id')}' has Georgian grading rubric")

    # Sprechen Lab Check
    for sp in labs.get('sprechen', []):
        has_prompts = bool(sp.get('prompts')) or bool(sp.get('situations'))
        runner.assert_true(has_prompts, f"Sprechen lab '{sp.get('id')}' has guided speaking prompts/situations")

    success = runner.summary()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
