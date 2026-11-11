# DEUTSCH A1 PRO — COMPLETE PROJECT SPECIFICATION & CONTEXT FOR CHATGPT

> **Note for ChatGPT:**
> This document provides the complete architectural, functional, pedagogical, and code context for the **Deutsch A1 Pro** local web application. Use this document to understand the codebase, help the user debug, add new lessons (A1 or A2), create additional exercises, integrate backends, or modify features.

---

## 1. PROJECT OVERVIEW
- **Project Name:** Deutsch A1 Pro (გერმანული ენის სრული სასწავლო პლატფორმა)
- **Target Audience:** Georgian native speakers learning German at the CEFR A1 level.
- **Academic Standards:** Modeled after textbooks used in Georgian universities (TSU, Iliauni) and Goethe-Institut Georgien:
  - *Schritte International Neu A1.1 & A1.2* (Hueber)
  - *Menschen A1* (Hueber)
  - *Netzwerk Neu A1* (Klett)
- **Language Policy:** 
  - Interface, pedagogical grammar explanations, cultural notes, and exercise feedbacks are **100% in Georgian**.
  - Target language content (vocabulary, dialogue utterances, exercises, example sentences) is authentic **German (Standarddeutsch)**.
- **Deployment Mode:** Runs locally via a lightweight Python 3 HTTP server at `http://localhost:8000`. Offline-first, zero external cloud dependencies.
- **Local Directory:** `/Users/shotachitaishvili/Documents/German A1/`

---

## 2. TECH STACK & ARCHITECTURAL DECISIONS
1. **Frontend Architecture:** Single-Page Application (SPA) built with vanilla ES6+ JavaScript, HTML5, and Tailwind CSS (via CDN).
2. **Audio System:**
   - **Pronunciation Engine:** Native browser Web Speech API (`SpeechSynthesisUtterance`) configured for `de-DE`. Includes speech rate controls (`1.0x`, `0.85x`, `0.7x` slow audio for beginners).
   - **Sound Effects (FX):** Web Audio API acoustic synthesizer generating real-time sine/triangle chimes for correct answers, gentle error tones, and celebration fanfares without external audio files.
3. **Data Layer:** Pre-compiled static master dataset (`js/data.js`, ~553 KB) exposing `window.GERMAN_A1_DATA`.
4. **State Management & Persistence:** Browser `localStorage` (`deutsch_a1_pro_v2` key) tracking:
   - XP Points & Streak counter (Gamification)
   - Completed lessons and per-lesson test scores
   - Mastered flashcard words & Favorite words (⭐)
   - Final exam score and pass certificate status
   - PRO Subscription status (`isPro: true/false`, subscription tier)
5. **Server:** Built-in Python 3 HTTP server (`server.py`) serving UTF-8 headers, no-cache directives, and correct MIME types.

---

## 3. FILE SYSTEM & CODEBASE STRUCTURE

```
/Users/shotachitaishvili/Documents/German A1/
├── index.html                   # Main HTML layout, navigation, and modal containers
├── server.py                    # Python 3 local HTTP server (Port 8000, UTF-8, No-Cache)
├── start.sh                     # Bash launch script
├── README.md                    # Comprehensive Georgian user documentation
├── CHATGPT_PROJECT_BRIEF.md     # This comprehensive context file for ChatGPT
├── css/
│   └── style.css                # Custom glassmorphic styling, animations, gender colors, 3D flipcards
├── js/
│   ├── data.js                  # Master dataset (553 KB: 734 words, 10 lessons, tables, exam)
│   └── app.js                   # Main application engine (1,400+ lines, tab router, test engine)
├── build_full_suite.py          # Master compiler script (builds js/data.js from modular generators)
├── update_deep_exercises.py     # 3-tier exercises database for Lessons 2–10
├── data_deep_lessons.py         # Expanded Lesson 1 module with detailed theory & tests
├── data_deep_lessons_part2.py   # Expanded Lesson 2 module
├── data_lexicon_part1.py        # Lexicon: Lesson 1 (123 words)
├── data_lexicon_part2.py        # Lexicon: Lesson 2 (62 words)
├── data_lexicon_part3.py        # Lexicon: Lesson 3 (120 words)
├── data_lexicon_part4.py        # Lexicon: Lesson 4 (130 words)
├── data_lexicon_part5.py        # Lexicon: Lessons 5–10 (293 words)
└── data_lexicon_part6.py        # Lexicon: Adjectives, colors, clothing (103 words)
```

---

## 4. MASTER DATA SCHEMA (`window.GERMAN_A1_DATA`)

```javascript
window.GERMAN_A1_DATA = {
  lessons: [
    {
      id: 1, // 1 to 10
      title_de: "Lektion 1: Erste Kontakte, Begrüßung & Alphabet",
      title_ka: "გაკვეთილი 1: პირველი კონტაქტი, გაცნობა და ანბანი",
      icon: "👋",
      level: "A1.1",
      description_ka: "...",
      objectives_ka: ["...", "..."],
      grammar_sections: [
        {
          id: "1.1",
          title: "1.1 მისალმება და დამშვიდობება...",
          content_ka: "Markdown formatted string with Georgian explanation and contrastive notes..."
        }
      ],
      dialogues: [
        {
          speaker: "Anna",
          text_de: "Guten Tag! Wie heißen Sie?",
          text_ka: "გამარჯობა! რა გქვიათ თქვენ?"
        }
      ],
      cultural_notes: {
        title: "💡 კულტურული ცნობარი: D-A-CH რეგიონი...",
        content_ka: "..."
      },
      exercises: {
        multiple_choice: [
          {
            id: "mc1_1",
            question: "რომელია სწორი ფორმა: 'Ich _______ Giorgi.'?",
            options: ["heiße", "heißt", "heißen", "bin heißen"],
            answer: 0,
            explanation: "Ich პირთან ზმნის დაბოლოებაა -e: ich heiße."
          }
        ],
        fill_in_blank: [
          {
            id: "fib1_1",
            sentence_before: "Ich ",
            sentence_after: " aus Georgien. (kommen)",
            correct_answer: "komme",
            hint: "ზმნა kommen ich პირთან იღებს დაბოლოებას -e"
          }
        ],
        listening: [
          {
            id: "lis1_1",
            audio_text: "Guten Tag, mein Name ist Lukas Weber.",
            question: "რა არის მოსაუბრის გვარი?",
            options: ["Lukas", "Weber", "Müller", "Schneider"],
            answer: 1
          }
        ]
      }
    }
    // Lessons 2 to 10 follow the same schema
  ],

  // Full 734-word lexicon
  dictionary: [
    {
      id: "hallo",
      word: "Hallo",
      article: "", // "der", "die", "das" or ""
      gender: "none", // "m", "f", "n", "pl", "none"
      plural: "",
      pos: "შორისდებული", // Part of speech in Georgian
      georgian: "გამარჯობა (არაფორმალური)",
      example_de: "Hallo Giorgi! Wie geht's?",
      example_ka: "გამარჯობა გიორგი! როგორ ხარ?",
      category: "მისალმება & ზრდილობა",
      lesson_id: 1 // 1 to 10
    }
  ],

  // 431 nouns with der/die/das for Article Trainer
  article_trainer_words: [
    { word: "Tisch", article: "der", georgian: "მაგიდა", gender: "m" }
  ],

  // 12 Sentence Builder syntax challenges
  sentence_builders: [
    {
      id: 1,
      words: ["Ich", "komme", "aus", "Georgien."],
      translation_ka: "მე საქართველოდან ვარ.",
      hint: "ქვემდებარე -> ზმნა (V2) -> aus -> ქვეყანა."
    }
  ],

  // 25 Final Diagnostic Exam questions
  final_exam_questions: [
    {
      id: 1,
      question: "'Woher kommen Sie?' - რომელია სწორი პასუხი?",
      options: ["Ich heiße David.", "Ich komme aus Georgien.", "Ich wohne in Tiflis.", "Ja, ich spreche Deutsch."],
      answer: 1,
      explanation: "Woher (საიდან) ითხოვს პასუხს წარმოშობაზე: aus + ქვეყანა."
    }
  ],

  // Grammar summary tables
  grammar_tables: {
    articles: { cases: [...] },
    pronouns: { list: [...] },
    modal_verbs: { verbs: [...] },
    irregular_verbs: { list: [...] } // 35 irregular verbs with Partizip II
  }
};
```

---

## 5. CORE FEATURES & FUNCTIONAL MODULES

### Module 1: Lessons System (10 Modules)
- **Lesson 1:** Erste Kontakte, Begrüßung, Alphabet, Verben (sein, heißen, kommen, sprechen) in Präsens, W-Fragen.
- **Lesson 2:** Familie & Freunde, Possessivpronomen (mein/dein), Zahlen 20–100.
- **Lesson 3:** Essen, Trinken & Einkaufen, unbestimmter Artikel, Negation (kein vs. nicht), Pluralformen.
- **Lesson 4:** Wohnung & Möbel, Räume, Akkusativ (den/die/das/die), Adjektive.
- **Lesson 5:** Tagesablauf, Uhrzeit (offiziell/umgangssprachlich), trennbare Verben (aufstehen, einkaufen).
- **Lesson 6:** Freizeit & Hobbys, Modalverben (können, wollen, möchten), Wochentage.
- **Lesson 7:** In der Stadt, Orientierung, Verkehrsmittel, Dativ (dem/der/dem/den), Präpositionen mit Dativ.
- **Lesson 8:** Beruf & Arbeit, Modalverben (müssen, dürfen - Verbot), Präpositionen als/bei.
- **Lesson 9:** Gesundheit & Körper, Schmerzen, Imperativ (du/ihr/Sie), Empfehlungen (sollen).
- **Lesson 10:** Urlaub & Reisen, Vergangenheit (Das Perfekt mit haben und sein + Partizip II).

### Module 2: Multi-Mode Interactive Exercise Hub
Inside every lesson:
1. **Multiple Choice:** 4–8 questions per lesson, animated feedback, linguistic rule explanation in Georgian, Web Audio API sound chimes, score tracking, XP reward (+30 XP).
2. **Lückentext (Fill-in-the-blank):** Interactive text input, on-screen German special character helper buttons (`ä`, `ö`, `ü`, `ß`, `Ä`, `Ö`, `Ü`), hint button, Enter key checking, case-insensitive comparison, XP reward (+20 XP).
3. **Hörverstehen (Listening Comprehension):** Real-time German speech synthesis (`de-DE`), animated sound wave equalizer, normal (1.0x) and slow (0.7x) speed toggles, comprehension question with 4 options, XP reward (+20 XP).

### Module 3: Sequential Dialogue Player
- Auto-plays dialogue lines in sequence with configurable pauses (`700ms`).
- Highlights the current speaking character and utterance in real time.
- Stop/Pause capability.

### Module 4: 734-Word Lexicon & Flashcards
- Search in Georgian and German with instant filtering.
- Filter by gender: `der`, `die`, `das`, `verbs`, or `favorites` (⭐).
- Dedicated Flashcard Trainer with lesson filter dropdown: practice all 734 words or drill down into a specific lesson (e.g. Lesson 1's 123 words).
- 3D CSS flip animations with "Repeat" vs. "Known (+5 XP)" buttons.

### Module 5: Article Trainer (der / die / das)
- Rapid-fire drill using 431 German nouns extracted from the lexicon.
- Color-coded: `der` (Blue), `die` (Red), `das` (Green).
- Tracks streaks and high scores, plays pronunciation upon correct answer.

### Module 6: Satzbau (Sentence Builder)
- 12 levels of German syntax puzzles.
- Word chips arranged by clicking, validating V2 word order and modal verb sentence brackets (*Satzklammer*).

### Module 7: Grammar Handbook
- Summary tables for Definite, Indefinite, and Negative articles in Nominativ, Akkusativ, and Dativ.
- Personal pronouns in all 3 cases.
- Modal verbs present tense conjugation table.
- 35 Most frequent irregular verbs with Partizip II and audio pronunciation.

### Module 8: Goethe-Institut A1 Probetest & Official Diploma
- 25-question comprehensive diagnostic exam covering all 10 lessons.
- 60% pass threshold (15 correct).
- Generates an official printable Certificate of Completion (`window.print()`) styled according to Goethe CEFR A1 standards.

### Module 9: Commercial PRO Subscription System
- Subscription tier modal accessible via header badge or profile:
  - **Starter (Free):** Basic lessons & quizzes.
  - **PRO Premium (₾29/year):** All 734 words, Hörverstehen, Lückentext, Article trainer, Satzbau, Exam Certificate.
  - **Lifetime Pro (₾149 one-time):** Lifetime access and upcoming A2 modules.
- Includes a live Demo Mode activation switch that instantly grants full PRO features and celebration fanfare sound.

---

## 6. HOW TO RUN THE PROJECT LOCALLY

```bash
# 1. Navigate to the project directory
cd "/Users/shotachitaishvili/Documents/German A1"

# 2. Start the local server
python3 server.py
# (Or run: ./start.sh)

# 3. Open in any modern web browser
# Open: http://localhost:8000
```

---

## 7. READY-TO-USE PROMPTS FOR CHATGPT ASSISTANCE

If the user wants you (ChatGPT) to continue developing this project, here are example tasks and how to approach them:

### Prompt A: "Add Lesson 11 (A2.1 Kickoff)"
To add a new lesson:
1. Follow the schema in Section 4.
2. Create grammar sections with Georgian explanations and contrastive notes.
3. Provide authentic dialogues with German/Georgian text.
4. Add 5 Multiple Choice, 3 Lückentext, and 2 Listening exercises.
5. Add 50+ new vocabulary items tagged with `lesson_id: 11`.

### Prompt B: "Connect Real Payments (Stripe / LemonSqueezy / Georgian Bank Pay)"
To make the PRO subscription commercial:
1. Replace the mock activation in `activatePro()` with a checkout webhook or payment link.
2. Store user licenses in a lightweight backend (FastAPI / Node / Supabase / Firebase).

### Prompt C: "Export / Deploy to the Web"
Since this application uses vanilla HTML5/JS/CSS without Node build steps, it can be hosted instantly on **GitHub Pages**, **Vercel**, **Netlify**, or **Cloudflare Pages** by simply dragging and dropping the project folder.
