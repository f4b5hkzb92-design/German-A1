#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEUTSCH A1 PRO: Practice Trainers Hub & Mini-Stories Verification Suite
Tests:
1. Plural Trainer (60 nouns, 5 patterns, rule explanations)
2. Verb Conjugation Trainer (50 drills, irregulars, modals)
3. Matching Pairs Game (Wort-Paare memory game)
4. A1 Graded Mini-Stories (Kurzgeschichten with audio, glossary, 3-question checks)
5. Dual-Speed Audio Engine (1.0x & 0.7x)
6. Starred Words (Favorites) Flashcard Trainer
"""

import json
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

passed_count = 0
failed_count = 0

def check(condition, message):
    global passed_count, failed_count
    if condition:
        print(f"  [PASS] {message}")
        passed_count += 1
    else:
        print(f"  [FAIL] {message}")
        failed_count += 1

def main():
    print("=" * 65)
    print("DEUTSCH A1 PRO: Practice Trainers & Mini-Stories QA Suite")
    print("=" * 65)

    # -------------------------------------------------------------
    # 1. Dataset Integrity & Schema Checks
    # -------------------------------------------------------------
    data_file = BASE_DIR / "js" / "data.js"
    check(data_file.exists(), "js/data.js exists on disk")

    raw_text = data_file.read_text(encoding="utf-8")
    json_start = raw_text.find("{")
    json_end = raw_text.rfind("}") + 1
    data = json.loads(raw_text[json_start:json_end])

    # Plural Trainer dataset
    plurals = data.get("plural_trainer_words", [])
    check(len(plurals) == 60, f"Plural Trainer contains exactly 60 high-yield nouns (got {len(plurals)})")

    patterns = set(p.get("pattern") for p in plurals)
    has_all_patterns = {"-er", "-e", "-s", "-"}.issubset(patterns) and any("n" in p for p in patterns)
    check(has_all_patterns, f"All 5 plural patterns represented across dataset (patterns: {patterns})")

    for idx, p in enumerate(plurals[:5]):
        check(bool(p.get("singular") and p.get("plural") and p.get("rule_explanation")), f"Plural #{p.get('id', idx)} has complete grammatical rule explanation")
        check(p.get("plural") in p.get("options", []), f"Plural #{p.get('id', idx)} options contain correct plural answer")

    # Verb Conjugation dataset
    verbs = data.get("verb_conjugations", [])
    check(len(verbs) == 50, f"Verb Conjugation Trainer contains exactly 50 drills (got {len(verbs)})")

    for idx, v in enumerate(verbs[:5]):
        check(bool(v.get("infinitive") and v.get("pronoun") and v.get("correct") and v.get("sentence")), f"Verb Drill #{v.get('id', idx)} has complete sentence context")
        check(v.get("correct") in v.get("options", []), f"Verb Drill #{v.get('id', idx)} options contain correct conjugation")

    # Mini-Stories dataset
    stories = data.get("mini_stories", [])
    check(len(stories) == 4, f"Mini-Stories collection contains 4 authentic A1 stories (got {len(stories)})")

    for st in stories:
        check(bool(st.get("title_de") and st.get("title_ka") and st.get("audio_text")), f"Story '{st.get('title_de')}' has bilingual title and audio narration")
        check(len(st.get("paragraphs", [])) >= 2, f"Story '{st.get('title_de')}' has >= 2 paragraphs (got {len(st.get('paragraphs', []))})")
        check(len(st.get("quiz", [])) == 3, f"Story '{st.get('title_de')}' has exactly 3 comprehension check questions (got {len(st.get('quiz', []))})")

    # -------------------------------------------------------------
    # 2. Runtime Behavior & Interactive Verification (OSA / JSC)
    # -------------------------------------------------------------
    mock_env = """
    const storage = {};
    const localStorage = {
        getItem: function(k) { return storage[k] || null; },
        setItem: function(k, v) { storage[k] = String(v); },
        removeItem: function(k) { delete storage[k]; }
    };

    const elementMap = {};
    function getOrCreateElement(id) {
        if (!elementMap[id]) {
            elementMap[id] = {
                id: id,
                innerHTML: '',
                textContent: '',
                classList: {
                    classes: [],
                    add: function(c) { if (!this.classes.includes(c)) this.classes.push(c); },
                    remove: function(c) { this.classes = this.classes.filter(x => x !== c); },
                    contains: function(c) { return this.classes.includes(c); },
                    toggle: function(c, force) {
                        if (force === undefined) force = !this.contains(c);
                        if (force) this.add(c); else this.remove(c);
                    }
                },
                style: {},
                dataset: {},
                value: '',
                appendChild: function() {},
                querySelectorAll: function() { return []; }
            };
        }
        return elementMap[id];
    }

    const document = {
        getElementById: function(id) { return getOrCreateElement(id); },
        querySelectorAll: function() { return []; },
        createElement: function(tag) { return getOrCreateElement('elem_' + Math.random()); },
        body: { appendChild: function() {} },
        documentElement: { classList: getOrCreateElement('docEl').classList }
    };

    function SpeechSynthesisUtterance(text) {
        this.text = text;
        this.lang = 'de-DE';
    }

    const window = {
        localStorage: localStorage,
        document: document,
        location: { reload: function() {} },
        scrollTo: function() {},
        matchMedia: function() { return { matches: false }; },
        addEventListener: function() {},
        setTimeout: function(fn) { try { fn(); } catch(e){} },
        clearTimeout: function() {},
        SpeechSynthesisUtterance: SpeechSynthesisUtterance,
        speechSynthesis: {
            cancel: function() {},
            speak: function() {},
            getVoices: function() { return [{ lang: 'de-DE' }]; }
        }
    };

    globalThis.SpeechSynthesisUtterance = SpeechSynthesisUtterance;
    globalThis.setTimeout = window.setTimeout;
    globalThis.clearTimeout = window.clearTimeout;
    globalThis.window = window;
    globalThis.document = document;
    globalThis.localStorage = localStorage;
    """

    data_code = (BASE_DIR / "js" / "data.js").read_text(encoding="utf-8")
    app_code = (BASE_DIR / "js" / "app.js").read_text(encoding="utf-8")

    probe_js = """
    function runProbe() {
        const app = window.DeutschApp;
        const results = [];

        try {
            // Test 1: Hub Trainer Mode Switch
            app.setTrainerMode('plurals');
            const pluralEl = document.getElementById('main-content');
            results.push({
                name: 'setTrainerMode switches to Plural Trainer view',
                ok: pluralEl.innerHTML.indexOf('Plural: მრავლობითი რიცხვის ტრენერი') !== -1
            });

            // Test 2: Plural Guess Correct
            const pluralItem = app.state.pluralCurrentWord;
            const initialPluralScore = app.state.pluralScore;
            app.guessPlural(pluralItem.plural);
            results.push({
                name: 'guessPlural correct increments score and streak',
                ok: app.state.pluralScore === initialPluralScore + 1 && app.state.pluralStreak === 1
            });

            // Test 3: Plural Guess Incorrect
            app.guessPlural('fake_wrong_plural');
            results.push({
                name: 'guessPlural incorrect resets streak to 0',
                ok: app.state.pluralStreak === 0
            });

            // Test 4: Verb Trainer Mode
            app.setTrainerMode('verbs');
            const verbItem = app.state.verbCurrentDrill;
            const initialVerbScore = app.state.verbScore;
            results.push({
                name: 'setTrainerMode switches to Verb Trainer view',
                ok: app.state.trainerActiveMode === 'verbs' && Boolean(verbItem)
            });

            // Test 5: Verb Guess Correct
            app.guessVerb(verbItem.correct);
            results.push({
                name: 'guessVerb correct increments score and streak',
                ok: app.state.verbScore === initialVerbScore + 1 && app.state.verbStreak === 1
            });

            // Test 6: Matching Game Initialization
            app.setTrainerMode('matching');
            results.push({
                name: 'Matching Game initializes 10 cards (5 pairs)',
                ok: app.state.matchCards.length === 10 && app.state.matchCompleted === false
            });

            // Test 7: Matching Game Pair Match
            const card0 = app.state.matchCards[0];
            const matchingIdx = app.state.matchCards.findIndex((c, i) => i !== 0 && c.pairId === card0.pairId && c.type !== card0.type);
            app.onMatchCardClick(0);
            app.onMatchCardClick(matchingIdx);
            results.push({
                name: 'onMatchCardClick correctly pairs German and Georgian words',
                ok: app.state.matchMatchedIds.includes(card0.id) && app.state.matchMoves === 1
            });

            // Test 8: Backwards Compatibility with Der/Die/Das Tab
            app.setTrainerMode('articles');
            const cardEl = document.getElementById('trainer-card');
            const wordEl = document.getElementById('trainer-word-display');
            results.push({
                name: 'Articles mode preserves #trainer-card and #trainer-word-display',
                ok: Boolean(cardEl) && Boolean(wordEl)
            });

            // Test 9: Mini-Stories Lab Navigation
            app.setTab('labs');
            app.switchLabTab('stories');
            const labsContent = document.getElementById('main-content');
            results.push({
                name: 'Language Labs renders Kurzgeschichten sub-tab',
                ok: labsContent.innerHTML.indexOf('KURZGESCHICHTEN') !== -1 && labsContent.innerHTML.indexOf('მოთხრობა 1') !== -1
            });

            // Test 10: Mini-Stories Quiz Submission
            app.selectStory('story_1');
            app.selectStoryAnswer(0, 1);
            app.selectStoryAnswer(1, 2);
            app.selectStoryAnswer(2, 1);
            app.submitStoryQuiz();
            const userStored = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3') || '{}');
            results.push({
                name: 'submitStoryQuiz records completion and awards XP',
                ok: app.state.storySubmitted === true && (userStored.completedStories || []).includes('story_1')
            });

            // Test 11: Paragraph Translation Toggle
            app.toggleStoryTranslation(0);
            results.push({
                name: 'toggleStoryTranslation toggles translation visibility state',
                ok: app.state.storyShowTranslations[0] === true
            });

            // Test 12: Dual-Speed Audio Helpers
            results.push({
                name: 'speakSlow and speakNormal audio helper functions exist',
                ok: typeof app.speakSlow === 'function' && typeof app.speakNormal === 'function'
            });

            // Test 13: Starred Words Flashcards Practice
            app.toggleFavorite(1);
            app.toggleFavorite(2);
            app.trainFavoritesFlashcards();
            results.push({
                name: 'trainFavoritesFlashcards launches flashcards filtered by favorites',
                ok: app.state.currentTab === 'flashcards' && app.state.flashcardLessonFilter === 'fav'
            });
        } catch (e) {
            results.push({ name: 'Exception in probe: ' + e.toString(), ok: false });
        }

        return JSON.stringify(results);
    }
    runProbe();
    """

    full_runner = mock_env + "\n" + data_code + "\n" + app_code + "\n" + probe_js
    runner_file = BASE_DIR / "tests" / "_stage10_upgrades_runner.js"
    runner_file.write_text(full_runner, encoding="utf-8")

    try:
        proc = subprocess.run(["osascript", "-l", "JavaScript", str(runner_file)], capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"  [FAIL] JavaScript Execution failed:\n{proc.stderr}")
            check(False, "JavaScript runner executed without errors")
        else:
            runtime_results = json.loads(proc.stdout.strip())
            for res in runtime_results:
                check(res["ok"], res["name"])
    finally:
        runner_file.unlink(missing_ok=True)

    print("=" * 65)
    print(f"UPGRADES QA SUMMARY: {passed_count} Passed, {failed_count} Failed")
    print("=" * 65)

    if failed_count > 0:
        sys.exit(1)
    sys.exit(0)

if __name__ == "__main__":
    main()
