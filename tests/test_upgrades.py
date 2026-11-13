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

    # Preposition & Case dataset
    cases = data.get("preposition_cases", [])
    check(len(cases) == 40, f"Preposition & Case Trainer contains exactly 40 drills (got {len(cases)})")
    case_types = set(c.get("type") for c in cases)
    check(case_types == {"dativ", "akkusativ", "wechsel"}, f"All 3 A1 case categories represented (found {case_types})")

    for idx, c in enumerate(cases[:5]):
        check(bool(c.get("sentence") and c.get("correct") and c.get("rule_ka")), f"Case Drill #{c.get('id', idx)} has complete sentence and rule")
        check(c.get("correct") in c.get("options", []), f"Case Drill #{c.get('id', idx)} options contain correct answer")

    # Hör-Diktat Lab dataset
    diktat = data.get("diktat", [])
    check(len(diktat) == 15, f"Hör-Diktat Lab contains exactly 15 tasks (got {len(diktat)})")
    diktat_cats = set(d.get("category") for d in diktat)
    check(diktat_cats == {"buchstabieren", "nummern", "uhrzeit", "preise", "saetze"}, f"All 5 Hör-Diktat categories represented (found {diktat_cats})")

    for idx, d in enumerate(diktat[:5]):
        check(bool(d.get("audio_text") and d.get("expected") and d.get("prompt_ka") and d.get("explanation")), f"Diktat #{d.get('id', idx)} has complete audio, expected answer, prompt, and explanation")

    # Trennbare Verben & Satzklammer dataset
    trennbar = data.get("trennbare_verben", [])
    check(len(trennbar) == 35, f"Trennbare Verben Trainer contains exactly 35 drills (got {len(trennbar)})")
    trennbar_types = set(t.get("type") for t in trennbar)
    check(trennbar_types == {"praesens", "modal", "imperativ_perfekt"}, f"All 3 Trennbare Verben categories represented (found {trennbar_types})")

    for idx, t in enumerate(trennbar[:5]):
        check(bool(t.get("infinitive") and t.get("sentence") and t.get("correct") and t.get("rule_ka")), f"Trennbare Drill #{t.get('id', idx)} has complete sentence and rule")
        check(t.get("correct") in t.get("options", []), f"Trennbare Drill #{t.get('id', idx)} options contain correct answer")

    # Zahlen, Uhrzeit & Datum dataset
    zahlen = data.get("zahlen_uhrzeit_drills", [])
    check(len(zahlen) == 36, f"Zahlen & Uhrzeit Trainer contains exactly 36 drills (got {len(zahlen)})")
    zahlen_cats = set(z.get("category") for z in zahlen)
    check(zahlen_cats == {"zahlen", "uhrzeit", "datum"}, f"All 3 Zahlen & Zeit categories represented (found {zahlen_cats})")
    for idx, z in enumerate(zahlen[:5]):
        check(bool(z.get("prompt_ka") and z.get("prompt_display") and z.get("correct") and z.get("rule_ka")), f"Zahlen Drill #{z.get('id', idx)} has complete prompt and rule")
        check(z.get("correct") in z.get("options", []), f"Zahlen Drill #{z.get('id', idx)} options contain correct answer")

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

            // Test 5b: Kasus & Preposition Trainer Mode
            app.setTrainerMode('cases');
            const caseItem = app.state.caseCurrentDrill;
            const initialCaseScore = app.state.caseScore;
            const caseEl = document.getElementById('main-content');
            results.push({
                name: 'setTrainerMode switches to Kasus & Preposition Trainer view',
                ok: app.state.trainerActiveMode === 'cases' && caseEl.innerHTML.indexOf('Kasus: ბრუნვები & წინდებულები') !== -1
            });

            // Test 5c: Kasus Guess Correct
            app.guessCase(caseItem.correct);
            results.push({
                name: 'guessCase correct increments score and streak',
                ok: app.state.caseScore === initialCaseScore + 1 && app.state.caseStreak === 1
            });

            // Test 5d: Kasus Guess Incorrect
            app.guessCase('fake_wrong_case');
            results.push({
                name: 'guessCase incorrect resets streak to 0',
                ok: app.state.caseStreak === 0
            });

            // Test 5e: Kasus Filter Change
            app.setCaseFilter('dativ');
            results.push({
                name: 'setCaseFilter filters drills by Dativ',
                ok: app.state.caseFilterType === 'dativ' && app.state.caseCurrentDrill.type === 'dativ'
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

            // Test 14: Hör-Diktat Lab Navigation & Rendering
            app.setTab('labs');
            app.switchLabTab('diktat');
            const mainHtml = document.getElementById('main-content').innerHTML;
            results.push({
                name: 'Language Labs renders Hör-Diktat sub-tab and workbench',
                ok: app.state.labActiveTab === 'diktat' && (mainHtml.indexOf('Hör-Diktat') !== -1 || mainHtml.indexOf('HÖR-DIKTAT') !== -1)
            });

            // Test 15: Hör-Diktat Interaction & Completion Tracking
            app.switchDiktatCategory('buchstabieren');
            app.onDiktatInput('Schneider');
            app.submitDiktat();
            const uAfterDiktat = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3') || '{}');
            results.push({
                name: 'submitDiktat verifies correct transcription and awards completion',
                ok: app.state.labDiktatSubmitted === true && (uAfterDiktat.completedDiktat || []).includes('dik_1')
            });

            // Test 16: Profile JSON Export
            const exportedJSON = app.exportUserDataJSON();
            const parsedExport = JSON.parse(exportedJSON);
            results.push({
                name: 'exportUserDataJSON creates valid JSON backup with user progress',
                ok: typeof exportedJSON === 'string' && parsedExport && parsedExport.xp >= 0 && Array.isArray(parsedExport.completedDiktat)
            });

            // Test 17: Trennbare Verben Trainer Mode & Guess
            app.setTab('article-trainer');
            app.setTrainerMode('trennbare');
            const trennDrill = app.state.trennbarCurrentDrill;
            results.push({
                name: 'setTrainerMode switches to Trennbare Verben Trainer view',
                ok: app.state.trainerActiveMode === 'trennbare' && trennDrill !== null && document.getElementById('main-content').innerHTML.indexOf('Trennbare Verben') !== -1
            });

            const prevTrennScore = app.state.trennbarScore;
            app.guessTrennbare(trennDrill.correct);
            results.push({
                name: 'guessTrennbare correct increments score and streak',
                ok: app.state.trennbarScore === prevTrennScore + 1 && app.state.trennbarStreak === 1
            });

            app.setTrennbareFilter('modal');
            results.push({
                name: 'setTrennbareFilter filters drills by modal category',
                ok: app.state.trennbarFilterType === 'modal' && app.state.trennbarCurrentDrill && app.state.trennbarCurrentDrill.type === 'modal'
            });

            // Test 18: Weekly Goal & Streak Freeze System
            app.setTab('profile');
            app.setDailyXpGoal(100);
            const uAfterGoal = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3') || '{}');
            const freezeRes = app.buyStreakFreeze();
            const uAfterFreeze = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3') || '{}');
            results.push({
                name: 'Weekly Goal & Streak Freeze update dailyXpGoal and track dailyXpEarned',
                ok: uAfterGoal.dailyXpGoal === 100 && typeof uAfterGoal.dailyXpEarned === 'number' && uAfterGoal.dailyXpEarned > 0 && document.getElementById('main-content').innerHTML.indexOf('Streak Freeze') !== -1
            });
            results.push({
                name: 'buyStreakFreeze spends 50 XP when available or enforces XP threshold safely',
                ok: (uAfterGoal.xp >= 50) ? (freezeRes === true && uAfterFreeze.streakFreezes === 2 && uAfterFreeze.xp === uAfterGoal.xp - 50) : (freezeRes === false)
            });

            // Test 19: Zahlen, Uhrzeit & Datum Trainer
            app.setTab('article-trainer');
            app.setTrainerMode('zahlen');
            const zahlenDrill = app.state.zahlenCurrentDrill;
            results.push({
                name: 'setTrainerMode switches to Zahlen, Uhrzeit & Datum Trainer view',
                ok: app.state.trainerActiveMode === 'zahlen' && zahlenDrill !== null && document.getElementById('main-content').innerHTML.indexOf('Zahlen, Uhrzeit & Datum') !== -1
            });

            const prevZahlenScore = app.state.zahlenScore;
            app.guessZahlen(zahlenDrill.correct);
            results.push({
                name: 'guessZahlen correct increments score and streak',
                ok: app.state.zahlenScore === prevZahlenScore + 1 && app.state.zahlenStreak === 1
            });

            app.setZahlenFilter('uhrzeit');
            results.push({
                name: 'setZahlenFilter filters drills by uhrzeit category',
                ok: app.state.zahlenFilterType === 'uhrzeit' && app.state.zahlenCurrentDrill && app.state.zahlenCurrentDrill.category === 'uhrzeit'
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
