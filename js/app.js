/**
 * DEUTSCH A1 PRO - ქართულ-გერმანული სასწავლო პლატფორმა
 * Modern Interactive Application Engine (Enterprise Educational Edition)
 * Includes: Core Labs (Hören, Lesen, Schreiben, Sprechen), SM-2 Spaced Repetition,
 * Robust State Persistence, Native Audio Synthesizer & Speech Recognition/MediaRecorder.
 */

(function () {
  'use strict';

  // --- Sanitization & XSS Prevention Helper ---
  function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  // --- Global Application State ---
  const state = {
    currentTab: 'lessons',
    selectedLessonId: 1,
    speechRate: 0.85,
    isDark: false,

    // Lexicon state
    lexiconSearch: '',
    lexiconCategory: 'all',
    lexiconGender: 'all',

    // Flashcard state
    flashcardList: [],
    flashcardIndex: 0,
    flashcardFlipped: false,
    flashcardLessonFilter: 'all',
    flashcardMode: 'normal', // 'normal' or 'srs'

    // Article Trainer state
    trainerActiveMode: 'articles', // 'articles' | 'plurals' | 'verbs' | 'matching'
    trainerIndex: 0,
    trainerScore: 0,
    trainerStreak: 0,
    trainerCurrentWord: null,

    // Plural Trainer state
    pluralIndex: 0,
    pluralScore: 0,
    pluralStreak: 0,
    pluralCurrentWord: null,
    pluralFeedback: null,

    // Verb Conjugation Trainer state
    verbIndex: 0,
    verbScore: 0,
    verbStreak: 0,
    verbCurrentDrill: null,
    verbFeedback: null,

    // Preposition & Case Trainer state
    caseIndex: 0,
    caseScore: 0,
    caseStreak: 0,
    caseCurrentDrill: null,
    caseFeedback: null,
    caseFilterType: 'all', // 'all', 'dativ', 'akkusativ', 'wechsel'

    // Trennbare Verben Trainer state
    trennbarIndex: 0,
    trennbarScore: 0,
    trennbarStreak: 0,
    trennbarCurrentDrill: null,
    trennbarFeedback: null,
    trennbarFilterType: 'all', // 'all', 'praesens', 'modal', 'imperativ_perfekt'

    // Matching Pairs Game state
    matchCards: [],
    matchFlipped: [],
    matchMatchedIds: [],
    matchMoves: 0,
    matchCompleted: false,

    // Mini-Stories Lab state
    storyActiveId: 'story_1',
    storyAnswers: {},
    storySubmitted: false,
    storyScore: 0,
    storyShowTranslations: {},

    // Hör-Diktat Lab state
    labDiktatIndex: 0,
    labDiktatUserInput: '',
    labDiktatSubmitted: false,
    labDiktatScore: 0,
    labDiktatCategory: 'all',

    // Sentence Builder state
    sbIndex: 0,
    sbAvailableWords: [],
    sbSelectedWords: [],
    sbChecked: false,
    sbIsCorrect: false,

    // Final Exam state
    examIndex: 0,
    examUserAnswers: {},
    examSubmitted: false,
    examScore: 0,
    examFilterModule: 'all',
    examModuleBreakdown: null,

    // Multi-Mode Lesson Exercises state
    exerciseActiveMode: 'mc', // 'mc', 'fib', 'listening'
    mcIndex: 0,
    mcSelectedAnswer: null,
    mcSubmitted: false,
    mcScore: 0,

    fibIndex: 0,
    fibUserInput: '',
    fibSubmitted: false,
    fibIsCorrect: false,
    fibScore: 0,

    lisIndex: 0,
    lisSelectedAnswer: null,
    lisSubmitted: false,
    lisScore: 0,
    lisPlayCount: 0,

    // Dialogue Sequential Player state
    dialoguePlaying: false,
    dialogueAllLines: [],
    dialogueLineIndex: 0,
    dialogueTimer: null,

    // Language Labs state
    labActiveTab: 'hoeren', // 'hoeren', 'lesen', 'schreiben', 'sprechen'
    // Hoeren Lab
    labHoerenIndex: 0,
    labHoerenSelectedAnswer: null,
    labHoerenSubmitted: false,
    labHoerenScore: 0,
    // Lesen Lab
    labLesenIndex: 0,
    labLesenAnswers: {},
    labLesenSubmitted: false,
    // Schreiben Lab
    labSchreibenTaskIndex: 0,
    labSchreibenFormInputs: {},
    labSchreibenText: '',
    labSchreibenFormSubmitted: false,
    labSchreibenDrafts: {},
    labSchreibenSubmittedTasks: {},
    labSchreibenRubricChecks: {},
    // Sprechen Lab
    labSprechenPromptIndex: 0,
    isRecording: false,
    mediaRecorder: null,
    recordedAudioChunks: [],
    recordedAudioUrl: null,
    // Live Pronunciation Evaluation (Speech AI)
    speechEvaluatingId: null,
    speechEvalResults: {},
    isEvaluatingSpeech: false,
    // Grammar CCQ state (Stage 9)
    lessonGrammarAnswers: {},
    lessonGrammarSubmitted: {},
    // Vocabulary active session state (Stage 9)
    lessonVocabSession: null,
    // Daily SRS state
    isDailySRSActive: false,
    dailySRSTotal: 0,
    dailySRSCompleted: 0,
    // Roleplay Chat Simulator (Stage 10 Part 3)
    labRoleplayIndex: 0,
    roleplayStep: 0,
    roleplayHistory: [],
    roleplayPoints: 0,
    roleplayShowTranslations: {},
    roleplayCompleted: false
  };

  // --- Local Calendar Date & Streak Calculations ---
  function getLocalDateString(d = new Date()) {
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  function getCalendarDaysDiff(dateStr1, dateStr2) {
    if (!dateStr1 || !dateStr2) return 0;
    const [y1, m1, d1] = dateStr1.split('-').map(Number);
    const [y2, m2, d2] = dateStr2.split('-').map(Number);
    const utc1 = Date.UTC(y1, m1 - 1, d1);
    const utc2 = Date.UTC(y2, m2 - 1, d2);
    return Math.round((utc2 - utc1) / (1000 * 60 * 60 * 24));
  }

  function updateDailyStreak(data) {
    const todayStr = getLocalDateString();
    if (data.dailyXpDate !== todayStr) {
      data.dailyXpDate = todayStr;
      data.dailyXpEarned = 0;
    }
    if (!data.lastActiveDate) {
      data.lastActiveDate = todayStr;
      data.streak = 1;
      return;
    }
    if (data.lastActiveDate === todayStr) {
      return; // Already recorded activity today
    }
    const diffDays = getCalendarDaysDiff(data.lastActiveDate, todayStr);
    if (diffDays === 1) {
      data.streak = (data.streak || 0) + 1;
      data.lastActiveDate = todayStr;
    } else if (diffDays === 2 && (data.streakFreezes || 0) > 0) {
      // Protect 1 missed day using a Streak Freeze
      data.streakFreezes -= 1;
      data.streakFrozenDates = Array.isArray(data.streakFrozenDates) ? data.streakFrozenDates : [];
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      data.streakFrozenDates.push(getLocalDateString(yesterday));
      data.streak = (data.streak || 0) + 1;
      data.lastActiveDate = todayStr;
    } else if (diffDays > 1) {
      data.streak = 1;
      data.lastActiveDate = todayStr;
    }
  }

  function getCleanDefaultUserData() {
    return {
      xp: 0,
      streak: 1,
      lastActiveDate: getLocalDateString(),
      completedLessons: [],
      lessonScores: {},
      lessonSkillProgress: {}, // lessonId -> { grammarReviewed, vocabPracticed, mcScore, mcPassed, fibScore, fibPassed, lisScore, lisPassed }
      masteredWords: [],
      favoriteWords: [],
      srsItems: {}, // wordId -> { interval, repetition, efactor, nextReviewDate }
      mistakeWords: [],
      claimedRewards: {}, // rewardKey -> timestamp
      labScores: { hoeren: {}, lesen: {}, schreiben: {}, sprechen: {}, roleplay: {} },
      writingDrafts: {}, // taskId -> draftText (Stage 9.1: Draft Persistence)
      learnerName: 'საქართველოს გერმანული ენის სტუდენტი',
      examHistory: [], // [{ attempt, date, score, total, pct, passed }]
      examPassed: false,
      examScore: null,
      examDate: null,
      completedStories: [], // story IDs
      completedDiktat: [], // diktat IDs
      dailyXpGoal: 50,
      dailyXpEarned: 0,
      dailyXpDate: getLocalDateString(),
      weeklyXpHistory: {}, // YYYY-MM-DD -> xp
      streakFreezes: 1,
      streakFrozenDates: [],
      isPro: true,
      subscriptionTier: 'pro_annual'
    };
  }

  // --- Local Storage Management & State Persistence (Stage 8 & Stage 9.1) ---
  const STORAGE_KEY = 'deutsch_a1_pro_v3';
  const RESET_SENTINEL = 'deutsch_a1_reset_marker_v3';
  const WRITING_DRAFTS_KEY = 'deutsch_a1_writing_drafts_v1';

  let userData = null;
  userData = loadUserData();

  function loadUserData() {
    try {
      const wasReset = localStorage.getItem(RESET_SENTINEL);
      let raw = localStorage.getItem(STORAGE_KEY);

      // Only migrate legacy if user never explicitly clicked "Reset All Progress"
      if (!raw && !wasReset) {
        const v2 = localStorage.getItem('deutsch_a1_pro_v2') || localStorage.getItem('deutsch_a1_user_data_v1');
        if (v2) {
          raw = v2;
          localStorage.removeItem('deutsch_a1_pro_v2');
          localStorage.removeItem('deutsch_a1_user_data_v1');
        }
      }

      let data = raw ? JSON.parse(raw) : null;
      if (!data || typeof data !== 'object') {
        data = getCleanDefaultUserData();
      } else {
        // Enforce strict schema validation & defaults
        data.xp = (typeof data.xp === 'number' && !isNaN(data.xp)) ? Math.max(0, data.xp) : 0;
        data.streak = (typeof data.streak === 'number' && !isNaN(data.streak)) ? Math.max(1, data.streak) : 1;
        data.completedLessons = Array.isArray(data.completedLessons) ? data.completedLessons.filter(n => typeof n === 'number') : [];
        data.lessonScores = (typeof data.lessonScores === 'object' && data.lessonScores !== null) ? data.lessonScores : {};
        data.lessonSkillProgress = (typeof data.lessonSkillProgress === 'object' && data.lessonSkillProgress !== null) ? data.lessonSkillProgress : {};
        data.masteredWords = Array.isArray(data.masteredWords) ? data.masteredWords : [];
        data.favoriteWords = Array.isArray(data.favoriteWords) ? data.favoriteWords : [];
        data.srsItems = (typeof data.srsItems === 'object' && data.srsItems !== null) ? data.srsItems : {};
        data.mistakeWords = Array.isArray(data.mistakeWords) ? data.mistakeWords : [];
        data.claimedRewards = (typeof data.claimedRewards === 'object' && data.claimedRewards !== null) ? data.claimedRewards : {};
        data.labScores = (typeof data.labScores === 'object' && data.labScores !== null) ? data.labScores : { hoeren: {}, lesen: {}, schreiben: {}, sprechen: {}, roleplay: {} };
        data.labScores.roleplay = (typeof data.labScores.roleplay === 'object' && data.labScores.roleplay !== null) ? data.labScores.roleplay : {};
        data.writingDrafts = (typeof data.writingDrafts === 'object' && data.writingDrafts !== null && !Array.isArray(data.writingDrafts)) ? data.writingDrafts : {};
        data.learnerName = (typeof data.learnerName === 'string' && data.learnerName.trim()) ? data.learnerName : 'საქართველოს გერმანული ენის სტუდენტი';
        data.examHistory = Array.isArray(data.examHistory) ? data.examHistory : [];
        data.examPassed = Boolean(data.examPassed);
        data.examScore = typeof data.examScore === 'number' ? data.examScore : null;
        data.examDate = typeof data.examDate === 'string' ? data.examDate : null;
        data.completedStories = Array.isArray(data.completedStories) ? data.completedStories : [];
        data.completedDiktat = Array.isArray(data.completedDiktat) ? data.completedDiktat : [];
        data.dailyXpGoal = (typeof data.dailyXpGoal === 'number' && [20, 50, 100, 150].includes(data.dailyXpGoal)) ? data.dailyXpGoal : 50;
        data.dailyXpEarned = (typeof data.dailyXpEarned === 'number' && !isNaN(data.dailyXpEarned)) ? Math.max(0, data.dailyXpEarned) : 0;
        data.dailyXpDate = (typeof data.dailyXpDate === 'string') ? data.dailyXpDate : getLocalDateString();
        data.weeklyXpHistory = (typeof data.weeklyXpHistory === 'object' && data.weeklyXpHistory !== null && !Array.isArray(data.weeklyXpHistory)) ? data.weeklyXpHistory : {};
        data.streakFreezes = (typeof data.streakFreezes === 'number' && !isNaN(data.streakFreezes)) ? Math.max(0, Math.min(3, data.streakFreezes)) : 1;
        data.streakFrozenDates = Array.isArray(data.streakFrozenDates) ? data.streakFrozenDates : [];
        data.isPro = true;

        // Versioned Writing Drafts Safe Recovery (Stage 9.1: Draft Persistence)
        try {
          const rawDrafts = localStorage.getItem(WRITING_DRAFTS_KEY);
          if (rawDrafts) {
            const parsedDrafts = JSON.parse(rawDrafts);
            if (parsedDrafts && typeof parsedDrafts === 'object' && !Array.isArray(parsedDrafts)) {
              data.writingDrafts = Object.assign({}, data.writingDrafts, parsedDrafts);
            }
          }
        } catch (eDraft) {
          console.warn('Recovered safely from corrupted writing drafts storage:', eDraft);
          data.writingDrafts = {};
        }

        updateDailyStreak(data);
      }
      userData = data;
      return data;
    } catch (e) {
      console.error('Failed to load user data, restoring safe defaults:', e);
      userData = getCleanDefaultUserData();
      return userData;
    }
  }

  function saveUserData() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userData));
      updateHeaderStats();
    } catch (e) {
      console.error('Failed to save user data:', e);
    }
  }

  function saveWritingDraft(taskId, text) {
    if (!taskId) return;
    userData.writingDrafts = userData.writingDrafts || {};
    userData.writingDrafts[taskId] = text;
    try {
      localStorage.setItem(WRITING_DRAFTS_KEY, JSON.stringify(userData.writingDrafts));
    } catch (e) {
      console.warn('Failed to persist writing draft to localStorage:', e);
    }
    saveUserData();
  }

  function recordDailyXpProgress(amount) {
    const todayStr = getLocalDateString();
    if (userData.dailyXpDate !== todayStr) {
      userData.dailyXpDate = todayStr;
      userData.dailyXpEarned = 0;
    }
    const prevEarned = userData.dailyXpEarned || 0;
    const goal = userData.dailyXpGoal || 50;
    userData.dailyXpEarned = prevEarned + amount;
    userData.weeklyXpHistory = userData.weeklyXpHistory || {};
    userData.weeklyXpHistory[todayStr] = (userData.weeklyXpHistory[todayStr] || 0) + amount;

    if (prevEarned < goal && userData.dailyXpEarned >= goal) {
      showToast(`🎯 დღიური მიზანი (${goal} XP) შესრულებულია!`);
    }
  }

  // --- Idempotent Reward Management (Fixes Priority 0 Defect 1: XP Exploits) ---
  function grantRewardXP(rewardKey, amount, successMessage) {
    userData.claimedRewards = userData.claimedRewards || {};

    if (userData.claimedRewards[rewardKey]) {
      // Reward already claimed: do not grant duplicate XP
      if (successMessage) {
        showToast(successMessage + ' (XP უკვე მიღებულია)');
      }
      saveUserData();
      return false;
    }

    userData.claimedRewards[rewardKey] = new Date().toISOString();
    userData.xp = (userData.xp || 0) + amount;
    recordDailyXpProgress(amount);
    saveUserData();
    playChime('success');
    showToast((successMessage ? successMessage + ' ' : '') + `+${amount} XP! ⭐`);
    updateHeaderStats();
    return true;
  }

  function addXP(amount) {
    userData.xp = (userData.xp || 0) + amount;
    recordDailyXpProgress(amount);
    saveUserData();
    playChime('success');
    showToast(`+${amount} XP! ⭐`);
  }

  // --- Multi-Skill Lesson Mastery Tracker (Fixes Priority 0 Defect 3) ---
  function recordSkillProgress(lessonId, skillKey, scorePct, passed) {
    userData.lessonSkillProgress = userData.lessonSkillProgress || {};
    userData.lessonScores = userData.lessonScores || {};
    
    let p = userData.lessonSkillProgress[lessonId] || {
      grammarReviewed: false,
      vocabPracticed: false,
      mcScore: 0,
      mcPassed: false,
      fibScore: 0,
      fibPassed: false,
      lisScore: 0,
      lisPassed: false
    };

    if (skillKey === 'grammar') {
      p.grammarScore = Math.max(p.grammarScore || 0, scorePct || 0);
      if (passed) p.grammarReviewed = true;
    } else if (skillKey === 'vocab') {
      p.vocabScore = Math.max(p.vocabScore || 0, scorePct || 0);
      if (passed) p.vocabPracticed = true;
    } else if (skillKey === 'mc') {
      p.mcScore = Math.max(p.mcScore || 0, scorePct);
      if (passed) p.mcPassed = true;
    } else if (skillKey === 'fib') {
      p.fibScore = Math.max(p.fibScore || 0, scorePct);
      if (passed) p.fibPassed = true;
    } else if (skillKey === 'lis') {
      p.lisScore = Math.max(p.lisScore || 0, scorePct);
      if (passed) p.lisPassed = true;
    }

    userData.lessonSkillProgress[lessonId] = p;

    // Overall composite lesson score (average of passed skills)
    const testedSkills = [p.mcScore, p.fibScore, p.lisScore].filter(s => s > 0);
    const avgScore = testedSkills.length ? Math.round(testedSkills.reduce((a, b) => a + b, 0) / testedSkills.length) : 0;
    if (avgScore > (userData.lessonScores[lessonId] || 0)) {
      userData.lessonScores[lessonId] = avgScore;
    }

    checkAndAwardLessonMastery(lessonId);
  }

  function checkAndAwardLessonMastery(lessonId) {
    userData.completedLessons = userData.completedLessons || [];
    const p = (userData.lessonSkillProgress && userData.lessonSkillProgress[lessonId]) || {};
    
    // Strict pedagogical criteria: Grammar reviewed, Vocab trained, and MC, FIB, Listening passed (>= 70%)
    const isMastered = Boolean(
      p.grammarReviewed &&
      p.vocabPracticed &&
      p.mcPassed &&
      p.fibPassed &&
      p.lisPassed
    );

    if (isMastered && !userData.completedLessons.includes(lessonId)) {
      userData.completedLessons.push(lessonId);
      userData.completedLessons.sort((a, b) => a - b);
      grantRewardXP('lesson_mastery_' + lessonId, 50, `გილოცავთ! გაკვეთილი ${lessonId} სრულად ათვისებულია (5-ვე უნარი)! 🎓`);
      playChime('fanfare');
    } else {
      saveUserData();
    }
    updateHeaderStats();
  }

  // --- SM-2 Spaced Repetition Algorithm (SuperMemo-2) ---
  function updateSM2Item(wordId, quality) {
    userData.srsItems = userData.srsItems || {};
    let item = userData.srsItems[wordId] || {
      interval: 1,
      repetition: 0,
      efactor: 2.5,
      nextReviewDate: getLocalDateString()
    };

    if (quality >= 3) {
      if (item.repetition === 0) {
        item.interval = 1;
      } else if (item.repetition === 1) {
        item.interval = 6;
      } else {
        item.interval = Math.round(item.interval * item.efactor);
      }
      item.repetition += 1;
      // Remove from mistakes if successfully remembered
      if (userData.mistakeWords) {
        userData.mistakeWords = userData.mistakeWords.filter(id => id !== wordId);
      }
    } else {
      item.repetition = 0;
      item.interval = 1;
      // Add to mistakes queue
      userData.mistakeWords = userData.mistakeWords || [];
      if (!userData.mistakeWords.includes(wordId)) {
        userData.mistakeWords.push(wordId);
      }
    }

    // Calculate next ease factor
    item.efactor = item.efactor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
    if (item.efactor < 1.3) item.efactor = 1.3;

    // Calculate next local review date
    const nextDate = new Date();
    nextDate.setDate(nextDate.getDate() + item.interval);
    item.nextReviewDate = getLocalDateString(nextDate);

    userData.srsItems[wordId] = item;
    saveUserData();
  }

  // --- Smart Daily SRS Review Queue (Stage 10) ---
  function getDueSRSWords() {
    const todayStr = getLocalDateString();
    const srs = userData.srsItems || {};
    const dict = (window.GERMAN_A1_DATA && window.GERMAN_A1_DATA.dictionary) ? window.GERMAN_A1_DATA.dictionary : [];
    
    // 1. Due today or overdue
    const dueIds = Object.keys(srs).filter(id => {
      const it = srs[id];
      return it && it.nextReviewDate && it.nextReviewDate <= todayStr;
    }).map(Number);

    let dueWords = dict.filter(w => dueIds.includes(w.id));

    // 2. Mistakes queue
    const mistakeIds = (userData.mistakeWords || []).filter(id => !dueIds.includes(id));
    const mistakeWords = dict.filter(w => mistakeIds.includes(w.id));
    dueWords = dueWords.concat(mistakeWords);

    // 3. If fewer than 10 words, supplement with unpracticed words
    if (dueWords.length < 10) {
      const existingIds = new Set(dueWords.map(w => w.id).concat(Object.keys(srs).map(Number)));
      const candidates = dict.filter(w => !existingIds.has(w.id));
      dueWords = dueWords.concat(candidates.slice(0, 10 - dueWords.length));
    }

    return dueWords;
  }

  // --- Web Audio API Chimes (Pure Native Acoustics) ---
  function playChime(type) {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (!AudioContext) return;
      const ctx = new AudioContext();

      if (type === 'success') {
        const osc1 = ctx.createOscillator();
        const osc2 = ctx.createOscillator();
        const gain = ctx.createGain();

        osc1.type = 'sine';
        osc2.type = 'sine';
        osc1.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
        osc2.frequency.setValueAtTime(659.25, ctx.currentTime + 0.1); // E5

        gain.gain.setValueAtTime(0.12, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);

        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(ctx.destination);

        osc1.start(ctx.currentTime);
        osc1.stop(ctx.currentTime + 0.12);
        osc2.start(ctx.currentTime + 0.1);
        osc2.stop(ctx.currentTime + 0.35);
      } else if (type === 'wrong') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = 'triangle';
        osc.frequency.setValueAtTime(260, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(180, ctx.currentTime + 0.25);

        gain.gain.setValueAtTime(0.15, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(ctx.currentTime);
        osc.stop(ctx.currentTime + 0.3);
      } else if (type === 'fanfare') {
        const notes = [523.25, 659.25, 783.99, 1046.5]; // C5, E5, G5, C6
        notes.forEach((freq, i) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, ctx.currentTime + i * 0.1);
          gain.gain.setValueAtTime(0.15, ctx.currentTime + i * 0.1);
          gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.1 + 0.35);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(ctx.currentTime + i * 0.1);
          osc.stop(ctx.currentTime + i * 0.1 + 0.35);
        });
      }
    } catch (e) {
      // AudioContext blocked or silent error
    }
  }

  // --- Native Web Speech Audio Engine ---
  function speakGerman(text, buttonElement, onEndCallback, customRate) {
    if (!('speechSynthesis' in window)) {
      showToast('ხმის გაჟღერების მხარდაჭერა არ არის ბრაუზერში');
      if (onEndCallback) onEndCallback();
      return;
    }
    window.speechSynthesis.cancel();

    const cleanText = text
      .replace(/[()]/g, '')
      .replace(/,\s*-[a-zäöüß]+/gi, '')
      .replace(/•/g, '')
      .trim();

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = 'de-DE';
    utterance.rate = (typeof customRate === 'number') ? customRate : state.speechRate;

    const voices = window.speechSynthesis.getVoices();
    const deVoice = voices.find(v => v.lang.startsWith('de') || v.lang.includes('DE'));
    if (deVoice) utterance.voice = deVoice;

    if (buttonElement) {
      buttonElement.classList.add('speaking-active');
      utterance.onend = () => {
        buttonElement.classList.remove('speaking-active');
        if (onEndCallback) onEndCallback();
      };
      utterance.onerror = () => {
        buttonElement.classList.remove('speaking-active');
        if (onEndCallback) onEndCallback();
      };
    } else {
      utterance.onend = () => {
        if (onEndCallback) onEndCallback();
      };
      utterance.onerror = () => {
        if (onEndCallback) onEndCallback();
      };
    }

    window.speechSynthesis.speak(utterance);
  }

  function speakSlow(text, buttonElement, onEndCallback) {
    speakGerman(text, buttonElement, onEndCallback, 0.65);
  }

  function speakNormal(text, buttonElement, onEndCallback) {
    speakGerman(text, buttonElement, onEndCallback, 0.90);
  }

  // --- Toast Notifications ---
  function showToast(message) {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none';
      document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    toast.className = 'bg-slate-900 text-white dark:bg-slate-100 dark:text-slate-900 px-4 py-2.5 rounded-xl shadow-xl text-sm font-medium animate-fadeIn flex items-center gap-2 pointer-events-auto border border-slate-700 dark:border-slate-300';
    toast.innerHTML = message;
    container.appendChild(toast);
    setTimeout(() => {
      toast.classList.add('opacity-0', 'transition-opacity', 'duration-300');
      setTimeout(() => toast.remove(), 300);
    }, 2500);
  }

  // --- Tab Navigation Engine ---
  function setTab(tabName) {
    state.currentTab = tabName;

    // Stop sequential dialogue if running
    stopSequentialDialogue();

    // Update active state in nav buttons
    document.querySelectorAll('.nav-tab').forEach(btn => {
      if (btn.dataset.tab === tabName) {
        btn.classList.add('active');
        btn.classList.remove('text-slate-600', 'dark:text-slate-300');
      } else {
        btn.classList.remove('active');
        btn.classList.add('text-slate-600', 'dark:text-slate-300');
      }
    });

    const content = document.getElementById('main-content');
    if (!content) return;
    content.innerHTML = '';
    window.scrollTo({ top: 0, behavior: 'smooth' });

    switch (tabName) {
      case 'lessons':
        renderLessonsList(content);
        break;
      case 'lesson-detail':
        renderLessonDetail(content, state.selectedLessonId);
        break;
      case 'lexicon':
        renderLexicon(content);
        break;
      case 'flashcards':
        initFlashcards();
        renderFlashcards(content);
        break;
      case 'article-trainer':
        initArticleTrainer();
        renderArticleTrainer(content);
        break;
      case 'sentence-builder':
        initSentenceBuilder();
        renderSentenceBuilder(content);
        break;
      case 'labs':
        renderLanguageLabs(content);
        break;
      case 'grammar':
        renderGrammarHandbook(content);
        break;
      case 'exam':
        renderExam(content);
        break;
      case 'profile':
        renderProfile(content);
        break;
      default:
        renderLessonsList(content);
    }
  }

  function updateHeaderStats() {
    const elStreak = document.getElementById('stat-streak');
    const elXP = document.getElementById('stat-xp');
    const elBar = document.getElementById('stat-progress-bar');
    const elText = document.getElementById('stat-progress-text');

    if (elStreak) elStreak.textContent = userData.streak || 1;
    if (elXP) elXP.textContent = userData.xp || 0;

    // Progress = (completedLessons / 10) * 70% + (masteredWords / 734) * 30%
    const compLessons = (userData.completedLessons || []).length;
    const mastWords = (userData.masteredWords || []).length;
    const pct = Math.min(100, Math.round((compLessons / 10) * 70 + (mastWords / 734) * 30));

    if (elBar) elBar.style.width = `${pct}%`;
    if (elText) elText.textContent = `${pct}%`;
  }

  // ==========================================================================
  // TAB 1: LESSONS LIST VIEW
  // ==========================================================================
  function renderLessonsList(container) {
    const lessons = window.GERMAN_A1_DATA.lessons;
    let html = `
      <div class="max-w-6xl mx-auto space-y-8 animate-fadeIn">
        
        <!-- Hero Banner with Schritte & Menschen Reference -->
        <div class="relative overflow-hidden bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 rounded-3xl p-8 md:p-10 text-white shadow-2xl">
          <div class="relative z-10 max-w-3xl">
            <div class="flex items-center gap-2 mb-3">
              <span class="px-3 py-1 bg-white/20 backdrop-blur-md rounded-full text-xs font-bold tracking-wider uppercase">
                Schritte International Neu & Menschen აკადემიური პროგრამა
              </span>
              <span class="px-2.5 py-1 bg-amber-400 text-slate-950 font-black rounded-md text-[11px] uppercase tracking-wider">
                💎 A1 სრული პლატფორმა
              </span>
            </div>
            <h1 class="text-3xl md:text-5xl font-black mb-4 leading-tight">
              გერმანული ენა ქართველებისთვის • A1 დონე
            </h1>
            <p class="text-blue-100 text-base md:text-lg mb-6 leading-relaxed font-normal">
              10 ყოვლისმომცველი გაკვეთილი, 734 სიტყვიანი ლექსიკონი, დეტალური გრამატიკული შედარებითი ანალიზი ქართულენოვანთათვის, რეალური აუდიო დიალოგები და 3-დონიანი სავარჯიშო ცენტრი.
            </p>
            <div class="flex flex-wrap gap-4 items-center">
              <button onclick="window.DeutschApp.openLesson(1)" class="bg-white text-blue-700 hover:bg-blue-50 font-extrabold px-6 py-3 rounded-2xl shadow-lg transition active:scale-95 flex items-center gap-2 text-sm">
                <span>🚀 Lektion 1-ის დაწყება</span>
              </button>
              <button onclick="window.DeutschApp.setTab('labs')" class="bg-white/10 hover:bg-white/20 text-white font-bold px-5 py-3 rounded-2xl backdrop-blur-md transition flex items-center gap-2 text-sm border border-white/20">
                <span>🎙️ 7 ენობრივი ლაბორატორია (Labs)</span>
              </button>
              <button onclick="window.DeutschApp.openProModal()" class="bg-amber-400/90 hover:bg-amber-400 text-slate-950 font-bold px-4 py-3 rounded-2xl transition flex items-center gap-1.5 text-sm">
                <span>💎 PRO რეჟიმის მართვა</span>
              </button>
            </div>
          </div>

          <div class="absolute -right-12 -bottom-12 w-64 h-64 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>
          <div class="absolute right-10 top-10 text-8xl opacity-15 pointer-events-none select-none">🇩🇪</div>
        </div>

        <!-- Smart Daily SRS Review Queue (Stage 10) -->
        ${(() => {
          const dueWords = getDueSRSWords();
          const dueCount = dueWords.length;
          return `
            <div class="bg-gradient-to-r from-indigo-900 via-blue-900 to-slate-900 rounded-3xl p-6 md:p-8 text-white shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-6 border border-blue-800/40 animate-fadeIn">
              <div class="space-y-2 max-w-xl">
                <div class="flex items-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/30 text-emerald-300 font-extrabold text-[10px] uppercase tracking-wider">
                    🧠 SM-2 Spaced Repetition სისტემა
                  </span>
                  <span class="text-xs text-blue-200">
                    • ინტერვალური გამეორება
                  </span>
                </div>
                <h2 class="text-xl md:text-2xl font-black">დღევანდელი 5-წუთიანი გამეორება</h2>
                <p class="text-xs md:text-sm text-blue-200 leading-relaxed font-normal">
                  ${dueCount > 0 
                    ? `თქვენ გაქვთ <strong class="text-amber-400 font-black">${dueCount} სიტყვა</strong> განმეორებისთვის ოპტიმალურ დროს. რეგულარული 5-წუთიანი სესია გარანტირებულად გადაიტანს სიტყვებს გრძელვადიან მეხსიერებაში.`
                    : `დღევანდელი ყველა ბარათი წარმატებით გამეორებულია! შემდეგი დაგეგმილი გამეორება გაიხსნება ხვალ.`}
                </p>
              </div>

              <div class="flex flex-col sm:flex-row items-center gap-3 w-full md:w-auto">
                <button onclick="window.DeutschApp.startDailySRSReview()" class="w-full sm:w-auto px-6 py-3.5 rounded-2xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-xs shadow-lg transition active:scale-95 flex items-center justify-center gap-2 whitespace-nowrap">
                  <span>🚀 ${dueCount > 0 ? `გამეორების დაწყება (${dueCount} სიტყვა)` : 'დამატებითი ვარჯიში'}</span>
                  <span class="px-2 py-0.5 rounded-full bg-slate-950/10 text-[10px] font-black">+15 XP</span>
                </button>
              </div>
            </div>
          `;
        })()}

        <!-- Lessons Grid -->
        <div>
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-2xl font-black text-slate-900 dark:text-white">A1 სასწავლო მოდულები</h2>
              <p class="text-xs text-slate-500">გაიარეთ გაკვეთილები ეტაპობრივად და დააგროვეთ ქულები</p>
            </div>
            <span class="text-xs font-bold px-3 py-1 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-full">
              სულ 10 გაკვეთილი
            </span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    `;

    lessons.forEach(l => {
      const isCompleted = (userData.completedLessons || []).includes(l.id);
      const score = (userData.lessonScores || {})[l.id];
      const ex = l.exercises || {};
      const mcCount = (ex.multiple_choice || []).length;
      const fibCount = (ex.fill_in_blank || []).length;
      const lisCount = (ex.listening || []).length;
      const totalTests = mcCount + fibCount + lisCount;

      html += `
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 hover:shadow-xl hover:border-blue-500/40 transition-all duration-300 flex flex-col justify-between group">
          <div>
            <div class="flex items-start justify-between mb-4">
              <div class="flex items-center gap-3.5">
                <span class="text-4xl p-3 bg-blue-50 dark:bg-slate-700/60 rounded-2xl group-hover:scale-105 transition-transform">${l.icon}</span>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="text-xs font-black text-blue-600 dark:text-blue-400 tracking-wider uppercase">LEKTION ${l.id}</span>
                    <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300">${l.level || 'A1'}</span>
                  </div>
                  <h3 class="text-lg font-extrabold text-slate-900 dark:text-white leading-snug">${escapeHtml(l.title_ka)}</h3>
                </div>
              </div>
              ${isCompleted ? `
                <span class="bg-emerald-100 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-400 text-xs font-extrabold px-3 py-1 rounded-full flex items-center gap-1 shadow-sm">
                  ✓ ჩაბარებულია (${score || 100}%)
                </span>
              ` : `
                <span class="bg-slate-100 dark:bg-slate-700 text-slate-500 text-xs font-bold px-3 py-1 rounded-full">
                  გასავლელია
                </span>
              `}
            </div>

            <p class="text-sm font-semibold text-blue-700 dark:text-blue-300 italic mb-2">${escapeHtml(l.title_de)}</p>
            <p class="text-xs text-slate-600 dark:text-slate-400 mb-5 leading-relaxed font-normal">${escapeHtml(l.description_ka || '')}</p>

            ${l.objectives_ka && l.objectives_ka.length ? `
              <div class="p-3 bg-slate-50 dark:bg-slate-700/30 rounded-xl mb-4 text-[11px] text-slate-600 dark:text-slate-300 space-y-1">
                <span class="font-bold text-slate-700 dark:text-slate-200 block">🎯 ძირითადი თემები:</span>
                <p class="line-clamp-2">• ${l.objectives_ka.slice(0, 3).map(escapeHtml).join(' • ')}</p>
              </div>
            ` : ''}
          </div>

          <div class="flex items-center justify-between pt-4 border-t border-slate-100 dark:border-slate-700/60">
            <div class="text-[11px] font-bold text-slate-500 flex items-center gap-2">
              <span>📚 ${l.grammar_sections ? l.grammar_sections.length : 0} თეორია</span>
              <span>•</span>
              <span>💬 ${l.dialogues ? l.dialogues.length : 0} დიალოგი</span>
              <span>•</span>
              <span class="text-blue-600 dark:text-blue-400">✍️ ${totalTests} ტესტი</span>
            </div>
            <button onclick="window.DeutschApp.openLesson(${l.id})" class="text-xs font-extrabold bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-xl shadow-sm transition-all group-hover:translate-x-0.5 flex items-center gap-1">
              <span>გახსნა</span>
              <span>→</span>
            </button>
          </div>
        </div>
      `;
    });

    html += `
          </div>
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 1.1: DEEP LESSON DETAIL VIEW
  // ==========================================================================
  function renderLessonDetail(container, lessonId) {
    const lesson = window.GERMAN_A1_DATA.lessons.find(l => l.id === lessonId);
    if (!lesson) return;

    const lessonVocab = window.GERMAN_A1_DATA.dictionary.filter(w => w.lesson_id === lessonId);
    const ex = lesson.exercises || {};
    const mcCount = (ex.multiple_choice || []).length;
    const fibCount = (ex.fill_in_blank || []).length;
    const lisCount = (ex.listening || []).length;

    let html = `
      <div class="max-w-4xl mx-auto space-y-8 animate-fadeIn pb-16">
        
        <!-- Back Navigation & Lesson Tracker -->
        <div class="flex items-center justify-between">
          <button onclick="window.DeutschApp.setTab('lessons')" class="text-xs font-extrabold text-slate-600 dark:text-slate-400 hover:text-blue-600 dark:hover:text-blue-400 flex items-center gap-1.5 px-3 py-2 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 transition">
            <span>← ყველა გაკვეთილზე დაბრუნება</span>
          </button>
          <div class="flex items-center gap-2">
            <span class="text-xs font-bold px-3 py-1 rounded-full bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300">
              A1 მოდული ${lesson.id} / 10
            </span>
            <button onclick="window.DeutschApp.openProModal()" class="text-xs font-black px-2.5 py-1 bg-amber-400 text-slate-950 rounded-lg shadow-sm">
              💎 PRO
            </button>
          </div>
        </div>

        <!-- Lesson Header Card -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-8 shadow-sm">
          <div class="flex items-center gap-4 mb-4">
            <span class="text-5xl p-3 bg-blue-50 dark:bg-slate-700/60 rounded-2xl">${lesson.icon}</span>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-black uppercase tracking-wider text-blue-600 dark:text-blue-400">LEKTION ${lesson.id}</span>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300">${lesson.level || 'A1'}</span>
              </div>
              <h1 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white leading-tight">${escapeHtml(lesson.title_ka)}</h1>
              <p class="text-slate-500 font-bold text-base mt-0.5">${escapeHtml(lesson.title_de)}</p>
            </div>
          </div>

          ${lesson.description_ka ? `
            <p class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed mb-6 font-normal">${escapeHtml(lesson.description_ka)}</p>
          ` : ''}

          <!-- Learning Objectives Checklist -->
          ${lesson.objectives_ka && lesson.objectives_ka.length ? `
            <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-700/30 border border-slate-100 dark:border-slate-700/60">
              <h3 class="text-xs font-extrabold uppercase tracking-wider text-slate-700 dark:text-slate-300 mb-2 flex items-center gap-1.5">
                <span>🎯 რა ვისწავლით ამ გაკვეთილში:</span>
              </h3>
              <ul class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs text-slate-600 dark:text-slate-300 font-medium">
                ${lesson.objectives_ka.map(obj => `
                  <li class="flex items-start gap-2">
                    <span class="text-blue-600 dark:text-blue-400 font-bold">✓</span>
                    <span>${escapeHtml(obj)}</span>
                  </li>
                `).join('')}
              </ul>
            </div>
          ` : ''}
        </div>

        <!-- Lesson Sub-tabs Bar -->
        <div class="flex border-b border-slate-200 dark:border-slate-700 space-x-1 md:space-x-2 overflow-x-auto pb-1 scrollbar-none">
          <button onclick="window.DeutschApp.switchLessonSubtab('grammar')" id="lsub-grammar" class="lesson-subtab px-4 py-2.5 font-bold text-xs md:text-sm border-b-2 border-blue-600 text-blue-600 dark:text-blue-400 transition whitespace-nowrap">
            📚 გრამატიკა & თეორია
          </button>
          <button onclick="window.DeutschApp.switchLessonSubtab('dialogues')" id="lsub-dialogues" class="lesson-subtab px-4 py-2.5 font-semibold text-xs md:text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 transition whitespace-nowrap">
            💬 დიალოგები & მოსმენა
          </button>
          <button onclick="window.DeutschApp.switchLessonSubtab('culture')" id="lsub-culture" class="lesson-subtab px-4 py-2.5 font-semibold text-xs md:text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 transition whitespace-nowrap">
            💡 კულტურა & DACH
          </button>
          <button onclick="window.DeutschApp.switchLessonSubtab('vocab')" id="lsub-vocab" class="lesson-subtab px-4 py-2.5 font-semibold text-xs md:text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 transition whitespace-nowrap">
            🔤 ლექსიკონი (${lessonVocab.length})
          </button>
          <button onclick="window.DeutschApp.switchLessonSubtab('exercises')" id="lsub-exercises" class="lesson-subtab px-4 py-2.5 font-semibold text-xs md:text-sm border-b-2 border-transparent text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 transition whitespace-nowrap">
            ✍️ სავარჯიშოების ცენტრი (${mcCount + fibCount + lisCount})
          </button>
        </div>

        <!-- TAB CONTENT 1: Grammar & Theory -->
        <div id="lesson-panel-grammar" class="space-y-6">
    `;

    (lesson.grammar_sections || []).forEach((sec) => {
      let formattedContent = (sec.content_ka || '')
        .replace(/\*\*(.*?)\*\*/g, '<strong class="font-black text-slate-900 dark:text-white">$1</strong>')
        .replace(/\*(.*?)\*/g, '<em class="italic text-blue-700 dark:text-blue-300 font-semibold">$1</em>')
        .replace(/\n\n/g, '</p><p class="mt-3">')
        .replace(/\n• /g, '<li class="ml-4 list-disc mt-1.5 font-medium">')
        .replace(/^> (.*$)/gim, '<div class="border-l-4 border-amber-500 bg-amber-50 dark:bg-amber-950/30 p-3.5 rounded-r-xl my-3 text-amber-900 dark:text-amber-200 text-xs md:text-sm font-medium">$1</div>');

      const savedCheck = (userData.grammarChecks && userData.grammarChecks[lesson.id]) || {};
      let userAns = state.lessonGrammarAnswers[sec.id];
      if (userAns === undefined && savedCheck.answers && savedCheck.answers[sec.id] !== undefined) {
        userAns = savedCheck.answers[sec.id];
      }
      const isSubmitted = Boolean(state.lessonGrammarSubmitted[lesson.id] || savedCheck.passed);
      const isCorrect = isSubmitted && sec.check && (userAns === sec.check.answer);

      html += `
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm">
          <h3 class="text-lg md:text-xl font-black text-slate-900 dark:text-white mb-4 flex items-center gap-2.5">
            <span class="w-2.5 h-6 bg-blue-600 rounded-full inline-block"></span>
            <span>${escapeHtml(sec.title)}</span>
          </h3>
          <div class="text-slate-700 dark:text-slate-300 text-sm md:text-base leading-relaxed space-y-3 font-normal">
            <p>${formattedContent}</p>
          </div>

          ${sec.check ? `
            <div class="mt-6 pt-4 border-t border-slate-100 dark:border-slate-700 space-y-3">
              <div class="flex items-center justify-between text-xs font-bold">
                <span class="text-blue-700 dark:text-blue-400 flex items-center gap-1.5">
                  <span>🧠</span> <strong>თეორიის გაგების შემოწმება:</strong>
                </span>
                ${isSubmitted ? (isCorrect ? `
                  <span class="text-emerald-600 font-extrabold flex items-center gap-1">✓ სწორია</span>
                ` : `
                  <span class="text-rose-600 font-extrabold flex items-center gap-1">✕ შეცდომა</span>
                `) : `
                  <span class="text-slate-400 text-[11px]">აირჩიეთ სწორი პასუხი</span>
                `}
              </div>
              <p class="text-xs md:text-sm font-black text-slate-900 dark:text-white">${escapeHtml(sec.check.question)}</p>
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
                ${sec.check.options.map((opt, oIdx) => {
                  let btnCls = "bg-slate-50 dark:bg-slate-700/40 text-slate-700 dark:text-slate-200 border-slate-200 dark:border-slate-600 hover:bg-blue-50 dark:hover:bg-slate-600";
                  if (userAns === oIdx) {
                    btnCls = "bg-blue-600 text-white border-blue-600 shadow-sm font-bold";
                  }
                  if (isSubmitted) {
                    if (oIdx === sec.check.answer) {
                      btnCls = "bg-emerald-600 text-white border-emerald-600 font-black shadow-sm";
                    } else if (userAns === oIdx && !isCorrect) {
                      btnCls = "bg-rose-600 text-white border-rose-600 font-bold";
                    } else {
                      btnCls = "opacity-50 border-slate-200 dark:border-slate-700";
                    }
                  }
                  return `
                    <button onclick="window.DeutschApp.onSelectGrammarCheckOption('${sec.id}', ${oIdx}, ${lesson.id})" class="p-2.5 rounded-xl border text-xs text-left transition ${btnCls}" ${isSubmitted ? 'disabled' : ''}>
                      ${String.fromCharCode(65 + oIdx)}. ${escapeHtml(opt)}
                    </button>
                  `;
                }).join('')}
              </div>
              ${isSubmitted ? `
                <p class="text-[11px] text-slate-500 dark:text-slate-400 italic mt-1 font-medium">💡 ${escapeHtml(sec.check.explanation)}</p>
              ` : ''}
            </div>
          ` : ''}
        </div>
      `;
    });

    const grammarStatus = (userData.lessonSkillProgress && userData.lessonSkillProgress[lesson.id]) || {};
    const grammarPassed = grammarStatus.grammarReviewed === true;

    html += `
        <!-- Grammar Comprehension Mastery Bar (Stage 9) -->
        <div class="p-6 rounded-3xl bg-gradient-to-r from-blue-900 to-indigo-900 text-white space-y-4 shadow-lg animate-fadeIn">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div class="flex items-center gap-2 mb-1">
                <span class="px-2.5 py-0.5 rounded-full bg-blue-500/30 text-blue-200 text-[10px] font-black uppercase tracking-wider">
                  CEFR A1 თეორიის ათვისება
                </span>
                ${grammarPassed ? `
                  <span class="px-2.5 py-0.5 rounded-full bg-emerald-500 text-slate-950 text-[10px] font-black">
                    ✓ ჩათვლილია (${grammarStatus.grammarScore || 100}%)
                  </span>
                ` : `
                  <span class="px-2.5 py-0.5 rounded-full bg-amber-400 text-slate-950 text-[10px] font-black">
                    საჭიროა შემოწმება (მინ. 70%)
                  </span>
                `}
              </div>
              <h4 class="text-base md:text-lg font-black">გაკვეთილის გრამატიკული დაუფლების შემოწმება</h4>
              <p class="text-xs text-blue-200">
                ${grammarPassed ? 'შესანიშნავია! ამ გაკვეთილის გრამატიკული წესები წარმატებით ათვისებულია.' : 'უპასუხეთ ზემოთ მოცემულ ყველა შეკითხვას და დააჭირეთ შემოწმებას.'}
              </p>
            </div>

            <div class="flex items-center gap-2">
              <button onclick="window.DeutschApp.submitGrammarCheck(${lesson.id})" class="px-6 py-3 rounded-2xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs shadow-md transition active:scale-95 flex items-center gap-1.5 whitespace-nowrap">
                <span>თეორიის შემოწმება ✓</span>
              </button>
            </div>
          </div>
        </div>
      </div>

        <!-- TAB CONTENT 2: Dialogues (Fixed BUG-01) -->
        <div id="lesson-panel-dialogues" class="hidden space-y-6">
          <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 class="text-xl font-black text-slate-900 dark:text-white">რეალური გერმანული დიალოგები</h3>
                <p class="text-xs text-slate-500 font-medium">გაავარჯიშეთ რეალური მეტყველება და ინტონაცია ქართულ თარგმანთან შედარებით:</p>
              </div>
              <div class="flex items-center gap-2">
                <button id="btn-play-all-dialogue" onclick="window.DeutschApp.toggleSequentialDialogue(${lesson.id})" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl text-xs font-extrabold shadow-md transition flex items-center gap-2">
                  <span>▶️ მთლიანი დიალოგის მოსმენა</span>
                </button>
              </div>
            </div>

            <div class="space-y-6" id="dialogue-lines-container">
    `;

    // Flatten lines for sequential player tracking
    state.dialogueAllLines = [];

    (lesson.dialogues || []).forEach((dlg, dIdx) => {
      html += `
        <div class="p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-700 pb-2">
            <h4 class="font-black text-sm text-blue-700 dark:text-blue-400">${escapeHtml(dlg.title || `დიალოგი ${dIdx + 1}`)}</h4>
            ${dlg.context ? `<span class="text-[11px] text-slate-500 italic">${escapeHtml(dlg.context)}</span>` : ''}
          </div>
          <div class="space-y-3">
      `;

      (dlg.lines || []).forEach((line, lIdx) => {
        const lineId = `dlg-line-${dIdx}-${lIdx}`;
        state.dialogueAllLines.push({ line, id: lineId });
        const isEven = lIdx % 2 === 0;

        html += `
          <div id="${lineId}" class="p-3.5 rounded-xl transition-all duration-200 ${isEven ? 'bg-blue-50/70 dark:bg-slate-700/30' : 'bg-slate-50 dark:bg-slate-700/20'} border border-slate-100 dark:border-slate-700">
            <div class="flex items-center justify-between mb-1.5">
              <span class="text-xs font-black uppercase tracking-wider text-blue-700 dark:text-blue-400 flex items-center gap-1.5">
                <span>👤</span> ${escapeHtml(line.speaker)}
              </span>
              <button onclick="window.DeutschApp.speak('${line.text_de.replace(/'/g, "\\'")}', this)" class="text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-blue-600 flex items-center gap-1 bg-white dark:bg-slate-800 px-3 py-1 rounded-lg shadow-sm border border-slate-200 dark:border-slate-600 transition">
                <span>🔊 მოუსმინე</span>
              </button>
            </div>
            <p class="text-sm md:text-base font-extrabold text-slate-900 dark:text-white mb-1">${escapeHtml(line.text_de)}</p>
            <p class="text-xs md:text-sm text-slate-600 dark:text-slate-400 font-medium">${escapeHtml(line.text_ka)}</p>
          </div>
        `;
      });

      html += `
          </div>
        </div>
      `;
    });

    html += `
            </div>
          </div>
        </div>

        <!-- TAB CONTENT 3: Cultural Notes (DACH) -->
        <div id="lesson-panel-culture" class="hidden space-y-6">
          <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm">
            <div class="flex items-center gap-3 mb-4">
              <span class="text-4xl">💡</span>
              <div>
                <h3 class="text-xl font-black text-slate-900 dark:text-white">კულტურული ცნობარი: D-A-CH რეგიონი</h3>
                <p class="text-xs text-slate-500 font-medium">გერმანია (D) • ავსტრია (A) • შვეიცარია (CH) — წეს-ჩვეულებები და ეტიკეტი</p>
              </div>
            </div>

            ${lesson.cultural_notes ? `
              <div class="p-6 rounded-2xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200/80 dark:border-amber-900/40 space-y-3">
                <h4 class="font-black text-base text-amber-900 dark:text-amber-200">${escapeHtml(lesson.cultural_notes.title || 'კულტურული ნიუანსები')}</h4>
                <p class="text-xs md:text-sm text-amber-900 dark:text-amber-300 leading-relaxed font-normal">${escapeHtml(lesson.cultural_notes.content_ka)}</p>
              </div>
            ` : `
              <p class="text-sm text-slate-500">ამ გაკვეთილის კულტურული ცნობარი მალე განახლდება.</p>
            `}
          </div>
        </div>

        <!-- TAB CONTENT 4: Vocabulary List -->
        <div id="lesson-panel-vocab" class="hidden space-y-6">
          <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 class="text-xl font-black text-slate-900 dark:text-white">ამ გაკვეთილის ლექსიკონი</h3>
                <p class="text-xs text-slate-500 font-medium">სულ: ${lessonVocab.length} სიტყვა გამოთქმებით, არტიკლებითა და მაგალითებით</p>
              </div>
              <button onclick="window.DeutschApp.trainLessonFlashcards(${lesson.id})" class="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-xl text-xs font-black shadow-md transition flex items-center gap-1.5 active:scale-95">
                <span>🗂️ გაკვეთილის ბარათების გავარჯიშება</span>
              </button>
            </div>

            <!-- Search inside lesson -->
            <div class="relative mb-4">
              <input type="text" id="lesson-vocab-search" oninput="window.DeutschApp.filterLessonVocab(${lesson.id}, this.value)" placeholder="ძებნა ამ გაკვეთილის სიტყვებში..." class="w-full px-4 py-2.5 pl-10 rounded-xl bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600 text-xs font-medium focus:outline-none focus:border-blue-500">
              <span class="absolute left-3.5 top-2.5 text-slate-400 text-xs">🔍</span>
            </div>

            <div id="lesson-vocab-grid" class="grid grid-cols-1 md:grid-cols-2 gap-3">
    `;

    lessonVocab.forEach(w => {
      let badgeClass = 'bg-slate-100 text-slate-700';
      if (w.gender === 'm') badgeClass = 'badge-der';
      else if (w.gender === 'f') badgeClass = 'badge-die';
      else if (w.gender === 'n') badgeClass = 'badge-das';
      else if (w.gender === 'pl') badgeClass = 'badge-pl';

      const isFav = (userData.favoriteWords || []).includes(w.id);

      html += `
        <div class="p-3.5 border border-slate-200 dark:border-slate-700 rounded-2xl bg-slate-50/50 dark:bg-slate-700/20 flex items-center justify-between gap-3 hover:border-blue-400 transition">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              ${w.article ? `<span class="text-[11px] font-black px-2 py-0.5 rounded-md ${badgeClass}">${escapeHtml(w.article)}</span>` : ''}
              <span class="font-extrabold text-sm text-slate-900 dark:text-white truncate">${escapeHtml(w.word)}</span>
              ${w.plural ? `<span class="text-[11px] text-slate-400 font-normal">(${escapeHtml(w.plural)})</span>` : ''}
            </div>
            <p class="text-xs font-medium text-slate-600 dark:text-slate-300 truncate">${escapeHtml(w.georgian)}</p>
            ${w.example_de ? `
              <p class="text-[10px] text-slate-400 italic mt-1 truncate">${escapeHtml(w.example_de)}</p>
            ` : ''}
          </div>
          <div class="flex items-center gap-1.5 shrink-0">
            <button onclick="window.DeutschApp.toggleFavorite('${escapeHtml(w.id)}')" class="p-2 rounded-xl text-xs hover:bg-slate-200 dark:hover:bg-slate-700 transition ${isFav ? 'text-amber-500' : 'text-slate-300'}" title="რჩეულებში დამატება">
              ⭐
            </button>
            <button onclick="window.DeutschApp.speak('${w.word.replace(/'/g, "\\'")}', this)" class="p-2 rounded-xl bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:text-blue-600 shadow-sm border border-slate-200 dark:border-slate-600 transition" title="გამოთქმის მოსმენა">
              🔊
            </button>
          </div>
        </div>
      `;
    });

    html += `
            </div>
          </div>
        </div>

        <!-- TAB CONTENT 5: Multi-Mode Interactive Exercise Hub -->
        <div id="lesson-panel-exercises" class="hidden space-y-6">
          <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm">
            
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 class="text-xl font-black text-slate-900 dark:text-white">ინტერაქტიული სავარჯიშო ცენტრი</h3>
                <p class="text-xs text-slate-500 font-medium">აირჩიეთ სავარჯიშოს ფორმატი ცოდნის საფუძვლიანად შესამოწმებლად:</p>
              </div>
              <span class="text-xs font-extrabold px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300">
                სულ: ${mcCount + fibCount + lisCount} დავალება
              </span>
            </div>

            <!-- Exercise Mode Selector Pills -->
            <div class="flex flex-wrap gap-2 mb-6 p-1.5 bg-slate-100 dark:bg-slate-700/50 rounded-2xl text-xs font-bold">
              <button onclick="window.DeutschApp.switchExerciseMode(${lesson.id}, 'mc')" id="exmode-btn-mc" class="exercise-tab-btn flex-1 py-2.5 px-3 rounded-xl transition text-center active">
                🎯 ტესტი (MC) • ${mcCount}
              </button>
              <button onclick="window.DeutschApp.switchExerciseMode(${lesson.id}, 'fib')" id="exmode-btn-fib" class="exercise-tab-btn flex-1 py-2.5 px-3 rounded-xl transition text-center text-slate-600 dark:text-slate-300">
                ✍️ გამოტოვებული სიტყვა • ${fibCount}
              </button>
              <button onclick="window.DeutschApp.switchExerciseMode(${lesson.id}, 'lis')" id="exmode-btn-lis" class="exercise-tab-btn flex-1 py-2.5 px-3 rounded-xl transition text-center text-slate-600 dark:text-slate-300">
                🎧 მოსმენის გაგება • ${lisCount}
              </button>
            </div>

            <!-- Dynamic Exercise Container -->
            <div id="exercise-content-container">
              <!-- Rendered dynamically by switchExerciseMode -->
            </div>

          </div>
        </div>

        <!-- Bottom Lesson Navigator -->
        <div class="flex items-center justify-between pt-6 border-t border-slate-200 dark:border-slate-700">
          ${lesson.id > 1 ? `
            <button onclick="window.DeutschApp.openLesson(${lesson.id - 1})" class="font-extrabold text-xs md:text-sm text-slate-600 dark:text-slate-300 hover:text-blue-600 flex items-center gap-2">
              ← წინა: გაკვეთილი ${lesson.id - 1}
            </button>
          ` : '<div></div>'}

          ${lesson.id < 10 ? `
            <button onclick="window.DeutschApp.openLesson(${lesson.id + 1})" class="font-extrabold text-xs md:text-sm bg-blue-600 text-white px-5 py-2.5 rounded-xl hover:bg-blue-700 shadow-md transition flex items-center gap-2 active:scale-95">
              შემდეგი: გაკვეთილი ${lesson.id + 1} →
            </button>
          ` : `
            <button onclick="window.DeutschApp.setTab('exam')" class="font-extrabold text-xs md:text-sm bg-emerald-600 text-white px-5 py-2.5 rounded-xl hover:bg-emerald-700 shadow-md transition flex items-center gap-2 active:scale-95">
              🎓 A1 სადიაგნოსტიკო გამოცდაზე გადასვლა →
            </button>
          `}
        </div>

      </div>
    `;

    container.innerHTML = html;
    initLessonExercises(lesson.id);
  }

  function switchLessonSubtab(tab) {
    document.querySelectorAll('.lesson-subtab').forEach(btn => {
      btn.classList.remove('border-blue-600', 'text-blue-600', 'dark:text-blue-400');
      btn.classList.add('border-transparent', 'text-slate-500');
    });
    const activeBtn = document.getElementById(`lsub-${tab}`);
    if (activeBtn) {
      activeBtn.classList.remove('border-transparent', 'text-slate-500');
      activeBtn.classList.add('border-blue-600', 'text-blue-600', 'dark:text-blue-400');
    }

    // Critical Fix 1 (Stage 9.1): Do NOT automatically award grammar mastery on tab switch.
    // Grammar mastery is only granted by passing submitGrammarCheck() CCQs with >= 70% score.

    ['grammar', 'dialogues', 'culture', 'vocab', 'exercises'].forEach(t => {
      const panel = document.getElementById(`lesson-panel-${t}`);
      if (panel) {
        if (t === tab) panel.classList.remove('hidden');
        else panel.classList.add('hidden');
      }
    });

    if (tab !== 'dialogues') {
      stopSequentialDialogue();
    }
  }

  // --- Sequential Dialogue Player (Fixed BUG-01) ---
  function toggleSequentialDialogue(lessonId) {
    if (state.dialoguePlaying) {
      stopSequentialDialogue();
    } else {
      startSequentialDialogue(lessonId);
    }
  }

  function startSequentialDialogue(lessonId) {
    const lesson = window.GERMAN_A1_DATA.lessons.find(l => l.id === lessonId);
    if (!lesson || !lesson.dialogues || lesson.dialogues.length === 0) return;

    // Collect all lines across dialogues
    state.dialogueAllLines = [];
    lesson.dialogues.forEach((dlg, dIdx) => {
      (dlg.lines || []).forEach((line, lIdx) => {
        state.dialogueAllLines.push({ line, id: `dlg-line-${dIdx}-${lIdx}` });
      });
    });

    if (state.dialogueAllLines.length === 0) return;

    state.dialoguePlaying = true;
    state.dialogueLineIndex = 0;

    const btn = document.getElementById('btn-play-all-dialogue');
    if (btn) btn.innerHTML = `<span>⏹️ დიალოგის შეჩერება</span>`;

    playNextDialogueLine(lesson);
  }

  function playNextDialogueLine(lesson) {
    if (!state.dialoguePlaying) return;

    if (state.dialogueLineIndex >= state.dialogueAllLines.length) {
      stopSequentialDialogue();
      showToast('დიალოგის მოსმენა დასრულდა 👏');
      return;
    }

    const currentItem = state.dialogueAllLines[state.dialogueLineIndex];

    // Highlight current line element
    state.dialogueAllLines.forEach((item, idx) => {
      const el = document.getElementById(item.id);
      if (el) {
        if (idx === state.dialogueLineIndex) {
          el.classList.add('ring-2', 'ring-blue-500', 'bg-blue-100/60');
          el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
          el.classList.remove('ring-2', 'ring-blue-500', 'bg-blue-100/60');
        }
      }
    });

    speakGerman(currentItem.line.text_de, null, () => {
      if (!state.dialoguePlaying) return;
      state.dialogueLineIndex += 1;
      state.dialogueTimer = setTimeout(() => {
        playNextDialogueLine(lesson);
      }, 700);
    });
  }

  function stopSequentialDialogue() {
    state.dialoguePlaying = false;
    if (state.dialogueTimer) clearTimeout(state.dialogueTimer);
    window.speechSynthesis.cancel();

    const btn = document.getElementById('btn-play-all-dialogue');
    if (btn) btn.innerHTML = `<span>▶️ მთლიანი დიალოგის მოსმენა</span>`;

    (state.dialogueAllLines || []).forEach(item => {
      const el = document.getElementById(item.id);
      if (el) el.classList.remove('ring-2', 'ring-blue-500', 'bg-blue-100/60');
    });
  }

  // ==========================================================================
  // MULTI-MODE EXERCISE ENGINE (MC, FIB, LISTENING) + COMPLETION HOOKS
  // ==========================================================================
  function initLessonExercises(lessonId) {
    state.exerciseActiveMode = 'mc';
    state.mcIndex = 0;
    state.mcSelectedAnswer = null;
    state.mcSubmitted = false;
    state.mcScore = 0;

    state.fibIndex = 0;
    state.fibUserInput = '';
    state.fibSubmitted = false;
    state.fibIsCorrect = false;
    state.fibScore = 0;

    state.lisIndex = 0;
    state.lisSelectedAnswer = null;
    state.lisSubmitted = false;
    state.lisScore = 0;
    state.lisPlayCount = 0;

    renderExerciseConsole(lessonId);
  }

  function switchExerciseMode(lessonId, mode) {
    state.exerciseActiveMode = mode;

    document.querySelectorAll('.exercise-tab-btn').forEach(btn => {
      btn.classList.remove('active');
      btn.classList.add('text-slate-600', 'dark:text-slate-300');
    });
    const activeBtn = document.getElementById(`exmode-btn-${mode}`);
    if (activeBtn) {
      activeBtn.classList.add('active');
      activeBtn.classList.remove('text-slate-600', 'dark:text-slate-300');
    }

    renderExerciseConsole(lessonId);
  }

  function renderExerciseConsole(lessonId) {
    const lesson = window.GERMAN_A1_DATA.lessons.find(l => l.id === lessonId);
    if (!lesson) return;
    const container = document.getElementById('exercise-content-container');
    if (!container) return;

    if (state.exerciseActiveMode === 'mc') {
      renderMCMode(container, lesson);
    } else if (state.exerciseActiveMode === 'fib') {
      renderFIBMode(container, lesson);
    } else if (state.exerciseActiveMode === 'lis') {
      renderListeningMode(container, lesson);
    }
  }

  // --- MODE A: MULTIPLE CHOICE ---
  function renderMCMode(container, lesson) {
    const list = (lesson.exercises && lesson.exercises.multiple_choice) || [];
    if (list.length === 0) {
      container.innerHTML = `<p class="text-xs text-slate-500">ამ რეჟიმში დავალებები არ მოიძებნა.</p>`;
      return;
    }

    if (state.mcIndex >= list.length) {
      const total = list.length;
      const score = state.mcScore;
      const pct = Math.round((score / total) * 100);
      const passed = pct >= 70;

      // Track MC Skill Progress (Strict Pedagogical Criteria: >= 70%)
      recordSkillProgress(lesson.id, 'mc', pct, passed);
      const skillStatus = (userData.lessonSkillProgress && userData.lessonSkillProgress[lesson.id]) || {};
      const lessonMastered = (userData.completedLessons || []).includes(lesson.id);

      container.innerHTML = `
        <div class="p-8 text-center space-y-6 animate-fadeIn bg-slate-50 dark:bg-slate-700/20 rounded-2xl border border-slate-200 dark:border-slate-700">
          <div class="text-6xl">${passed ? '🎉' : '📖'}</div>
          <h3 class="text-2xl font-black text-slate-900 dark:text-white">
            ${passed ? 'ტესტი წარმატებით დასრულდა!' : 'გაიმეორეთ მასალა და სცადეთ თავიდან'}
          </h3>
          <div class="text-4xl font-black ${passed ? 'text-emerald-600' : 'text-amber-600'}">
            ${score} / ${total} სწორი პასუხი (${pct}%)
          </div>
          <p class="text-xs md:text-sm text-slate-600 dark:text-slate-300 max-w-md mx-auto">
            ${passed
              ? 'შესანიშნავი შედეგია! ტესტის ნაწილი ჩათვლილია (მინ. 70%).'
              : 'სასურველია გადახედოთ გაკვეთილის გრამატიკის ნაწილს და სცადოთ ტესტი ხელახლა (გამსვლელია 70%).'}
          </p>

          <!-- 5-Skill Lesson Mastery Checklist -->
          <div class="p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-left text-xs space-y-2 max-w-lg mx-auto">
            <div class="flex items-center justify-between font-bold text-slate-800 dark:text-slate-200">
              <span>გაკვეთილის 5-უნარის სტატუსი:</span>
              <span class="${lessonMastered ? 'text-emerald-600 font-black' : 'text-slate-500'}">
                ${lessonMastered ? '✓ გაკვეთილი სრულად ათვისებულია (+50 XP)' : 'საჭიროა 5-ვე უნარის ჩაბარება'}
              </span>
            </div>
            <div class="grid grid-cols-5 gap-1.5 text-center text-[10px] font-bold">
              <div class="p-1.5 rounded-lg ${skillStatus.grammarReviewed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">თეორია ${skillStatus.grammarReviewed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.vocabPracticed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">ლექსიკა ${skillStatus.vocabPracticed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.mcPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">ტესტი (${skillStatus.mcScore || 0}%) ${skillStatus.mcPassed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.fibPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">შევსება (${skillStatus.fibScore || 0}%) ${skillStatus.fibPassed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.lisPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">აუდიო (${skillStatus.lisScore || 0}%) ${skillStatus.lisPassed ? '✓' : '⏳'}</div>
            </div>
          </div>

          <div class="flex flex-wrap justify-center gap-3 pt-2">
            <button onclick="window.DeutschApp.restartMC(${lesson.id})" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 font-extrabold text-xs text-slate-700 dark:text-slate-300 hover:bg-slate-100 transition">
              🔄 თავიდან გავლა
            </button>
            <button onclick="window.DeutschApp.switchExerciseMode(${lesson.id}, 'fib')" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition">
              შემდეგი: გამოტოვებული სიტყვები (Lückentext) →
            </button>
          </div>
        </div>
      `;
      return;
    }

    const q = list[state.mcIndex];

    let html = `
      <div class="space-y-6 animate-fadeIn">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>შეკითხვა ${state.mcIndex + 1} / ${list.length}</span>
          <span class="text-blue-600 dark:text-blue-400">ქულა: ${state.mcScore}</span>
        </div>

        <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
          <div class="bg-blue-600 h-1.5 rounded-full transition-all duration-300" style="width: ${((state.mcIndex + 1) / list.length) * 100}%"></div>
        </div>

        <h4 class="text-base md:text-lg font-black text-slate-900 dark:text-white leading-snug">
          ${escapeHtml(q.question)}
        </h4>

        <div class="grid grid-cols-1 gap-3">
    `;

    q.options.forEach((opt, idx) => {
      let optionClass = 'border-slate-200 dark:border-slate-700 hover:border-blue-400 bg-white dark:bg-slate-800';
      let icon = `<span class="w-6 h-6 rounded-lg bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-xs font-extrabold text-slate-500">${String.fromCharCode(65 + idx)}</span>`;

      if (state.mcSubmitted) {
        if (idx === q.answer) {
          optionClass = 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 font-bold';
          icon = `<span class="w-6 h-6 rounded-lg bg-emerald-600 text-white flex items-center justify-center text-xs font-bold">✓</span>`;
        } else if (idx === state.mcSelectedAnswer) {
          optionClass = 'border-rose-500 bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 font-bold';
          icon = `<span class="w-6 h-6 rounded-lg bg-rose-600 text-white flex items-center justify-center text-xs font-bold">✗</span>`;
        } else {
          optionClass = 'opacity-40 border-slate-200 dark:border-slate-700';
        }
      } else if (state.mcSelectedAnswer === idx) {
        optionClass = 'border-blue-600 bg-blue-50/70 dark:bg-blue-900/30 text-blue-900 dark:text-blue-100 font-bold';
        icon = `<span class="w-6 h-6 rounded-lg bg-blue-600 text-white flex items-center justify-center text-xs font-bold">●</span>`;
      }

      html += `
        <button onclick="window.DeutschApp.onSelectMCAnswer(${lesson.id}, ${idx})" class="p-3.5 rounded-2xl border text-left flex items-center gap-3 transition-all ${optionClass}" ${state.mcSubmitted ? 'disabled' : ''}>
          ${icon}
          <span class="text-xs md:text-sm font-medium">${escapeHtml(opt)}</span>
        </button>
      `;
    });

    html += `
        </div>

        ${state.mcSubmitted ? `
          <div class="p-4 rounded-2xl ${state.mcSelectedAnswer === q.answer ? 'bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900/40 text-emerald-900 dark:text-emerald-200' : 'bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/40 text-rose-900 dark:text-rose-200'} text-xs md:text-sm animate-fadeIn space-y-1">
            <span class="font-black block">${state.mcSelectedAnswer === q.answer ? 'სწორია! 🎉 (+10 XP)' : 'არასწორია!'}</span>
            <p class="font-normal leading-relaxed">${escapeHtml(q.explanation || '')}</p>
          </div>
        ` : ''}

        <div class="flex justify-end pt-2">
          ${!state.mcSubmitted ? `
            <button onclick="window.DeutschApp.submitMCAnswer(${lesson.id})" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition disabled:opacity-50" ${state.mcSelectedAnswer === null ? 'disabled' : ''}>
              შემოწმება ✓
            </button>
          ` : `
            <button onclick="window.DeutschApp.nextMCQuestion(${lesson.id})" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition">
              შემდეგი შეკითხვა →
            </button>
          `}
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // --- MODE B: LÜCKENTEXT (FILL IN THE BLANK) ---
  function renderFIBMode(container, lesson) {
    const list = (lesson.exercises && lesson.exercises.fill_in_blank) || [];
    if (list.length === 0) {
      container.innerHTML = `<p class="text-xs text-slate-500">ამ რეჟიმში დავალებები არ მოიძებნა.</p>`;
      return;
    }

    if (state.fibIndex >= list.length) {
      const total = list.length;
      const score = state.fibScore;
      const pct = Math.round((score / total) * 100);
      const passed = pct >= 70;

      // Track FIB Skill Progress (Strict Pedagogical Criteria: >= 70%)
      recordSkillProgress(lesson.id, 'fib', pct, passed);
      const skillStatus = (userData.lessonSkillProgress && userData.lessonSkillProgress[lesson.id]) || {};
      const lessonMastered = (userData.completedLessons || []).includes(lesson.id);

      container.innerHTML = `
        <div class="p-8 text-center space-y-6 animate-fadeIn bg-slate-50 dark:bg-slate-700/20 rounded-2xl border border-slate-200 dark:border-slate-700">
          <div class="text-6xl">✍️</div>
          <h3 class="text-2xl font-black text-slate-900 dark:text-white">Lückentext სავარჯიშო დასრულდა!</h3>
          <div class="text-4xl font-black ${passed ? 'text-emerald-600' : 'text-amber-600'}">${score} / ${total} სწორი (${pct}%)</div>
          <p class="text-xs text-slate-600 dark:text-slate-400">
            ${passed ? 'შესანიშნავია! ტექსტის შევსების ნაწილი ჩათვლილია (მინ. 70%).' : 'გამსვლელი ზღვარია 70%. სცადეთ თავიდან.'}
          </p>

          <!-- 5-Skill Lesson Mastery Checklist -->
          <div class="p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-left text-xs space-y-2 max-w-lg mx-auto">
            <div class="flex items-center justify-between font-bold text-slate-800 dark:text-slate-200">
              <span>გაკვეთილის 5-უნარის სტატუსი:</span>
              <span class="${lessonMastered ? 'text-emerald-600 font-black' : 'text-slate-500'}">
                ${lessonMastered ? '✓ გაკვეთილი სრულად ათვისებულია (+50 XP)' : 'საჭიროა 5-ვე უნარის ჩაბარება'}
              </span>
            </div>
            <div class="grid grid-cols-5 gap-1.5 text-center text-[10px] font-bold">
              <div class="p-1.5 rounded-lg ${skillStatus.grammarReviewed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">თეორია ${skillStatus.grammarReviewed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.vocabPracticed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">ლექსიკა ${skillStatus.vocabPracticed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.mcPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">ტესტი (${skillStatus.mcScore || 0}%) ${skillStatus.mcPassed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.fibPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">შევსება (${skillStatus.fibScore || 0}%) ${skillStatus.fibPassed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.lisPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">აუდიო (${skillStatus.lisScore || 0}%) ${skillStatus.lisPassed ? '✓' : '⏳'}</div>
            </div>
          </div>

          <div class="flex flex-wrap justify-center gap-3 pt-2">
            <button onclick="window.DeutschApp.restartFIB(${lesson.id})" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 font-extrabold text-xs text-slate-700 dark:text-slate-300 hover:bg-slate-100 transition">
              🔄 თავიდან გავლა
            </button>
            <button onclick="window.DeutschApp.switchExerciseMode(${lesson.id}, 'lis')" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition">
              შემდეგი: მოსმენის გაგება (Hörverstehen) →
            </button>
          </div>
        </div>
      `;
      return;
    }

    const item = list[state.fibIndex];

    let html = `
      <div class="space-y-6 animate-fadeIn">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>დავალება ${state.fibIndex + 1} / ${list.length}</span>
          <span class="text-blue-600 dark:text-blue-400">ქულა: ${state.fibScore}</span>
        </div>

        <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
          <div class="bg-blue-600 h-1.5 rounded-full transition-all duration-300" style="width: ${((state.fibIndex + 1) / list.length) * 100}%"></div>
        </div>

        <div class="p-6 rounded-2xl bg-slate-50 dark:bg-slate-700/30 border border-slate-200 dark:border-slate-700 text-center space-y-4">
          <span class="text-[11px] font-extrabold uppercase tracking-wider text-slate-400 block">ჩაწერეთ გამოტოვებული სიტყვა</span>
          
          <div class="text-lg md:text-2xl font-black text-slate-900 dark:text-white flex flex-wrap items-center justify-center gap-2">
            <span>${escapeHtml(item.sentence_before || '')}</span>
            <input type="text" id="fib-input" value="${escapeHtml(state.fibUserInput)}" oninput="window.DeutschApp.onFIBInput(this.value)" onkeydown="if(event.key==='Enter') window.DeutschApp.submitFIBAnswer(${lesson.id})" placeholder="..." class="px-3 py-1.5 rounded-xl border-2 ${state.fibSubmitted ? (state.fibIsCorrect ? 'border-emerald-500 bg-emerald-50 text-emerald-900' : 'border-rose-500 bg-rose-50 text-rose-900') : 'border-blue-500 bg-white dark:bg-slate-800'} text-center font-black text-lg max-w-[160px] focus:outline-none" ${state.fibSubmitted ? 'disabled' : ''}>
            <span>${escapeHtml(item.sentence_after || '')}</span>
          </div>

          <!-- German Special Characters Helper Keys -->
          ${!state.fibSubmitted ? `
            <div class="flex flex-wrap items-center justify-center gap-1.5 pt-2">
              <span class="text-[10px] text-slate-400 mr-1 font-bold">გერმანული კლავიშები:</span>
              <button onclick="window.DeutschApp.appendGermanChar('ä')" class="german-key">ä</button>
              <button onclick="window.DeutschApp.appendGermanChar('ö')" class="german-key">ö</button>
              <button onclick="window.DeutschApp.appendGermanChar('ü')" class="german-key">ü</button>
              <button onclick="window.DeutschApp.appendGermanChar('ß')" class="german-key">ß</button>
              <button onclick="window.DeutschApp.appendGermanChar('Ä')" class="german-key">Ä</button>
              <button onclick="window.DeutschApp.appendGermanChar('Ö')" class="german-key">Ö</button>
              <button onclick="window.DeutschApp.appendGermanChar('Ü')" class="german-key">Ü</button>
            </div>
          ` : ''}

          ${item.hint ? `
            <p class="text-xs text-slate-500 dark:text-slate-400 font-medium pt-1">💡 მინიშნება: ${escapeHtml(item.hint)}</p>
          ` : ''}
        </div>

        ${state.fibSubmitted ? `
          <div class="p-4 rounded-2xl ${state.fibIsCorrect ? 'bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 text-emerald-900 dark:text-emerald-200' : 'bg-rose-50 dark:bg-rose-950/30 border border-rose-200 text-rose-900 dark:text-rose-200'} text-xs md:text-sm animate-fadeIn">
            <span class="font-black">${state.fibIsCorrect ? 'სწორია! 🎉 (+10 XP)' : 'არასწორია!'}</span>
            ${!state.fibIsCorrect ? `<span class="ml-2 font-bold">სწორი პასუხია: <code class="px-2 py-0.5 bg-white dark:bg-slate-800 rounded font-black text-emerald-600">${escapeHtml(item.correct_answer)}</code></span>` : ''}
          </div>
        ` : ''}

        <div class="flex justify-end pt-2">
          ${!state.fibSubmitted ? `
            <button onclick="window.DeutschApp.submitFIBAnswer(${lesson.id})" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition disabled:opacity-50" ${!state.fibUserInput.trim() ? 'disabled' : ''}>
              შემოწმება (Enter) ✓
            </button>
          ` : `
            <button onclick="window.DeutschApp.nextFIBQuestion(${lesson.id})" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition">
              შემდეგი დავალება →
            </button>
          `}
        </div>
      </div>
    `;

    container.innerHTML = html;

    if (!state.fibSubmitted) {
      setTimeout(() => {
        const inp = document.getElementById('fib-input');
        if (inp) inp.focus();
      }, 50);
    }
  }

  // --- MODE C: HÖRVERSTEHEN (LISTENING COMPREHENSION) ---
  function renderListeningMode(container, lesson) {
    const list = (lesson.exercises && lesson.exercises.listening) || [];
    if (list.length === 0) {
      container.innerHTML = `<p class="text-xs text-slate-500">ამ რეჟიმში დავალებები არ მოიძებნა.</p>`;
      return;
    }

    if (state.lisIndex >= list.length) {
      const total = list.length;
      const score = state.lisScore;
      const pct = Math.round((score / total) * 100);
      const passed = pct >= 70;

      // Track Listening Skill Progress (Strict Pedagogical Criteria: >= 70%)
      recordSkillProgress(lesson.id, 'lis', pct, passed);
      const skillStatus = (userData.lessonSkillProgress && userData.lessonSkillProgress[lesson.id]) || {};
      const lessonMastered = (userData.completedLessons || []).includes(lesson.id);

      container.innerHTML = `
        <div class="p-8 text-center space-y-6 animate-fadeIn bg-slate-50 dark:bg-slate-700/20 rounded-2xl border border-slate-200 dark:border-slate-700">
          <div class="text-6xl">🎧</div>
          <h3 class="text-2xl font-black text-slate-900 dark:text-white">მოსმენის გაგების ტესტი დასრულდა!</h3>
          <div class="text-4xl font-black ${passed ? 'text-emerald-600' : 'text-amber-600'}">${score} / ${total} სწორი (${pct}%)</div>
          <p class="text-xs text-slate-600 dark:text-slate-400">
            ${passed ? 'შესანიშნავია! მოსმენის გაგების ნაწილი ჩათვლილია (მინ. 70%).' : 'გამსვლელი ზღვარია 70%. მოუსმინეთ აუდიოებს კიდევ ერთხელ და სცადეთ თავიდან.'}
          </p>

          <!-- 5-Skill Lesson Mastery Checklist -->
          <div class="p-4 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-left text-xs space-y-2 max-w-lg mx-auto">
            <div class="flex items-center justify-between font-bold text-slate-800 dark:text-slate-200">
              <span>გაკვეთილის 5-უნარის სტატუსი:</span>
              <span class="${lessonMastered ? 'text-emerald-600 font-black' : 'text-slate-500'}">
                ${lessonMastered ? '✓ გაკვეთილი სრულად ათვისებულია (+50 XP)' : 'საჭიროა 5-ვე უნარის ჩაბარება'}
              </span>
            </div>
            <div class="grid grid-cols-5 gap-1.5 text-center text-[10px] font-bold">
              <div class="p-1.5 rounded-lg ${skillStatus.grammarReviewed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">თეორია ${skillStatus.grammarReviewed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.vocabPracticed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">ლექსიკა ${skillStatus.vocabPracticed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.mcPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">ტესტი (${skillStatus.mcScore || 0}%) ${skillStatus.mcPassed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.fibPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">შევსება (${skillStatus.fibScore || 0}%) ${skillStatus.fibPassed ? '✓' : '⏳'}</div>
              <div class="p-1.5 rounded-lg ${skillStatus.lisPassed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-500'}">აუდიო (${skillStatus.lisScore || 0}%) ${skillStatus.lisPassed ? '✓' : '⏳'}</div>
            </div>
          </div>

          <div class="flex justify-center pt-2">
            <button onclick="window.DeutschApp.restartListening(${lesson.id})" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 font-extrabold text-xs text-slate-700 dark:text-slate-300 hover:bg-slate-100 transition">
              🔄 თავიდან გავლა
            </button>
          </div>
        </div>
      `;
      return;
    }

    const item = list[state.lisIndex];

    let html = `
      <div class="space-y-6 animate-fadeIn">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>მოსმენის დავალება ${state.lisIndex + 1} / ${list.length}</span>
          <span class="text-blue-600 dark:text-blue-400">ქულა: ${state.lisScore}</span>
        </div>

        <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
          <div class="bg-blue-600 h-1.5 rounded-full transition-all duration-300" style="width: ${((state.lisIndex + 1) / list.length) * 100}%"></div>
        </div>

        <!-- Listening Audio Card -->
        <div class="bg-gradient-to-r from-blue-900 via-indigo-950 to-slate-900 rounded-3xl p-8 text-white text-center space-y-4 shadow-xl">
          <span class="text-[11px] font-extrabold uppercase tracking-wider text-blue-300 block">🎧 Hörverstehen • აუდიო ფრაგმენტი</span>
          
          <div class="flex justify-center items-center gap-3">
            <div class="sound-wave text-blue-400">
              <span></span><span></span><span></span><span></span>
            </div>
            <p class="text-sm text-slate-300 font-medium">დააჭირეთ ღილაკს და ყურადღებით მოუსმინეთ გერმანულ რეპლიკას:</p>
            <div class="sound-wave text-blue-400">
              <span></span><span></span><span></span><span></span>
            </div>
          </div>

          <div class="flex justify-center gap-3 pt-2">
            <button onclick="window.DeutschApp.playListeningAudio('${item.audio_text.replace(/'/g, "\\'")}', this)" class="px-6 py-3 rounded-2xl bg-blue-600 hover:bg-blue-500 text-white font-black text-sm shadow-lg shadow-blue-500/30 transition active:scale-95 flex items-center gap-2">
              <span>🔊 მოუსმინე აუდიოს</span>
            </button>
            <button onclick="window.DeutschApp.playListeningAudioSlow('${item.audio_text.replace(/'/g, "\\'")}', this)" class="px-4 py-3 rounded-2xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs backdrop-blur-md transition flex items-center gap-1.5">
              <span>🐢 ნელა (0.7x)</span>
            </button>
          </div>

          ${state.lisSubmitted ? `
            <div class="pt-3 border-t border-white/10 text-xs text-blue-200 italic">
              ტექსტი იყო: "${escapeHtml(item.audio_text)}"
            </div>
          ` : ''}
        </div>

        <!-- Question based on audio -->
        <h4 class="text-base md:text-lg font-black text-slate-900 dark:text-white leading-snug">
          ${escapeHtml(item.question)}
        </h4>

        <div class="grid grid-cols-1 gap-3">
    `;

    item.options.forEach((opt, idx) => {
      let optionClass = 'border-slate-200 dark:border-slate-700 hover:border-blue-400 bg-white dark:bg-slate-800';
      let icon = `<span class="w-6 h-6 rounded-lg bg-slate-100 dark:bg-slate-700 flex items-center justify-center text-xs font-extrabold text-slate-500">${String.fromCharCode(65 + idx)}</span>`;

      if (state.lisSubmitted) {
        if (idx === item.answer) {
          optionClass = 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-900 dark:text-emerald-200 font-bold';
          icon = `<span class="w-6 h-6 rounded-lg bg-emerald-600 text-white flex items-center justify-center text-xs font-bold">✓</span>`;
        } else if (idx === state.lisSelectedAnswer) {
          optionClass = 'border-rose-500 bg-rose-50 dark:bg-rose-950/40 text-rose-900 dark:text-rose-200 font-bold';
          icon = `<span class="w-6 h-6 rounded-lg bg-rose-600 text-white flex items-center justify-center text-xs font-bold">✗</span>`;
        } else {
          optionClass = 'opacity-40 border-slate-200 dark:border-slate-700';
        }
      } else if (state.lisSelectedAnswer === idx) {
        optionClass = 'border-blue-600 bg-blue-50/70 dark:bg-blue-900/30 text-blue-900 dark:text-blue-100 font-bold';
        icon = `<span class="w-6 h-6 rounded-lg bg-blue-600 text-white flex items-center justify-center text-xs font-bold">●</span>`;
      }

      html += `
        <button onclick="window.DeutschApp.onSelectListeningAnswer(${lesson.id}, ${idx})" class="p-3.5 rounded-2xl border text-left flex items-center gap-3 transition-all ${optionClass}" ${state.lisSubmitted ? 'disabled' : ''}>
          ${icon}
          <span class="text-xs md:text-sm font-medium">${escapeHtml(opt)}</span>
        </button>
      `;
    });

    html += `
        </div>

        <div class="flex justify-end pt-2">
          ${!state.lisSubmitted ? `
            <button onclick="window.DeutschApp.submitListeningAnswer(${lesson.id})" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition disabled:opacity-50" ${state.lisSelectedAnswer === null ? 'disabled' : ''}>
              შემოწმება ✓
            </button>
          ` : `
            <button onclick="window.DeutschApp.nextListeningQuestion(${lesson.id})" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition">
              შემდეგი შეკითხვა →
            </button>
          `}
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 2: FULL LEXICON (734 WORDS)
  // ==========================================================================
  function renderLexicon(container) {
    const dict = window.GERMAN_A1_DATA.dictionary;
    const categories = ['all', ...new Set(dict.map(w => w.category).filter(Boolean))];

    const q = state.lexiconSearch.toLowerCase().trim();
    const filtered = dict.filter(w => {
      if (state.lexiconCategory !== 'all' && w.category !== state.lexiconCategory) return false;
      if (state.lexiconGender === 'der' && w.gender !== 'm') return false;
      if (state.lexiconGender === 'die' && (w.gender !== 'f' && w.gender !== 'pl')) return false;
      if (state.lexiconGender === 'das' && w.gender !== 'n') return false;
      if (state.lexiconGender === 'verbs' && w.pos !== 'ზმნა') return false;
      if (state.lexiconGender === 'favorites' && !(userData.favoriteWords || []).includes(w.id)) return false;

      if (!q) return true;
      return (
        w.word.toLowerCase().includes(q) ||
        w.georgian.toLowerCase().includes(q) ||
        (w.example_de && w.example_de.toLowerCase().includes(q)) ||
        (w.example_ka && w.example_ka.toLowerCase().includes(q))
      );
    });

    let html = `
      <div class="max-w-6xl mx-auto space-y-6 animate-fadeIn pb-16">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
            <div>
              <div class="flex items-center gap-2">
                <h1 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">A1 სრული ლექსიკონი</h1>
                <span class="px-2 py-0.5 text-[10px] font-black bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-md">734 სიტყვა</span>
              </div>
              <p class="text-xs text-slate-500 font-medium">აკადემიური გერმანულ-ქართული ლექსიკონი აუდიო გამოთქმითა და მაგალითებით</p>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold px-3 py-1.5 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-xl">
                ნაპოვნია: ${filtered.length} სიტყვა
              </span>
            </div>
          </div>

          <!-- Search & Filter Controls -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4">
            <div class="md:col-span-2 relative">
              <input type="text" id="lexicon-search-input" value="${escapeHtml(state.lexiconSearch)}" oninput="window.DeutschApp.onLexiconSearch(this.value)" placeholder="ძებნა გერმანულად ან ქართულად..." class="w-full px-4 py-3 pl-11 rounded-2xl bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600 focus:outline-none focus:border-blue-500 text-xs md:text-sm font-medium">
              <span class="absolute left-4 top-3 text-slate-400">🔍</span>
              ${state.lexiconSearch ? `
                <button onclick="window.DeutschApp.clearLexiconSearch()" class="absolute right-4 top-3 text-slate-400 hover:text-slate-600 text-xs">✕</button>
              ` : ''}
            </div>

            <div>
              <select onchange="window.DeutschApp.onLexiconCategory(this.value)" class="w-full px-4 py-3 rounded-2xl bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600 focus:outline-none focus:border-blue-500 text-xs font-bold">
                ${categories.map(c => `
                  <option value="${escapeHtml(c)}" ${state.lexiconCategory === c ? 'selected' : ''}>
                    ${c === 'all' ? 'ყველა თემატიკა (კატეგორია)' : escapeHtml(c)}
                  </option>
                `).join('')}
              </select>
            </div>
          </div>

          <!-- Quick Gender & Type Filter Buttons -->
          <div class="flex flex-wrap gap-2 pt-2 border-t border-slate-100 dark:border-slate-700/60">
            <button onclick="window.DeutschApp.onLexiconGender('all')" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition ${state.lexiconGender === 'all' ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
              ყველა
            </button>
            <button onclick="window.DeutschApp.onLexiconGender('der')" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition ${state.lexiconGender === 'der' ? 'bg-blue-600 text-white shadow' : 'badge-der'}">
              der (მამრობითი)
            </button>
            <button onclick="window.DeutschApp.onLexiconGender('die')" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition ${state.lexiconGender === 'die' ? 'bg-rose-600 text-white shadow' : 'badge-die'}">
              die (მდედრობითი/მრ.)
            </button>
            <button onclick="window.DeutschApp.onLexiconGender('das')" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition ${state.lexiconGender === 'das' ? 'bg-emerald-600 text-white shadow' : 'badge-das'}">
              das (საშუალო)
            </button>
            <button onclick="window.DeutschApp.onLexiconGender('verbs')" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition ${state.lexiconGender === 'verbs' ? 'bg-amber-600 text-white shadow' : 'bg-amber-50 text-amber-700 border border-amber-200'}">
              ზმნები
            </button>
            <button onclick="window.DeutschApp.onLexiconGender('favorites')" class="px-3.5 py-1.5 rounded-xl text-xs font-extrabold transition ${state.lexiconGender === 'favorites' ? 'bg-yellow-500 text-white shadow' : 'bg-yellow-50 text-yellow-700 border border-yellow-200'}">
              ⭐ რჩეულები (${(userData.favoriteWords || []).length})
            </button>
            <button onclick="window.DeutschApp.trainFavoritesFlashcards()" class="sm:ml-auto px-3.5 py-1.5 rounded-xl text-xs font-black bg-gradient-to-r from-amber-500 to-yellow-500 hover:from-amber-600 hover:to-yellow-600 text-white shadow-sm flex items-center gap-1.5 transition active:scale-95">
              <span>⚡ რჩეულების გავარჯიშება (Flashcards)</span>
            </button>
          </div>
        </div>

        <!-- Dictionary Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
    `;

    filtered.forEach(w => {
      let badgeClass = 'bg-slate-100 text-slate-700';
      if (w.gender === 'm') badgeClass = 'badge-der';
      else if (w.gender === 'f') badgeClass = 'badge-die';
      else if (w.gender === 'n') badgeClass = 'badge-das';
      else if (w.gender === 'pl') badgeClass = 'badge-pl';

      const isFav = (userData.favoriteWords || []).includes(w.id);

      html += `
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-4 hover:shadow-md transition flex items-start justify-between gap-4">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              ${w.article ? `<span class="text-[11px] font-black px-2 py-0.5 rounded-md ${badgeClass}">${escapeHtml(w.article)}</span>` : ''}
              <h3 class="font-extrabold text-base text-slate-900 dark:text-white truncate">${escapeHtml(w.word)}</h3>
              ${w.plural ? `<span class="text-xs text-slate-400 font-normal">(${escapeHtml(w.plural)})</span>` : ''}
              ${w.pos ? `<span class="text-[10px] text-slate-400 bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 rounded">${escapeHtml(w.pos)}</span>` : ''}
            </div>

            <p class="text-xs md:text-sm font-semibold text-blue-700 dark:text-blue-300 mb-2">${escapeHtml(w.georgian)}</p>

            ${w.example_de ? `
              <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-700/30 text-xs space-y-0.5">
                <p class="font-bold text-slate-800 dark:text-slate-200">${escapeHtml(w.example_de)}</p>
                <p class="text-slate-500 italic text-[11px]">${escapeHtml(w.example_ka || '')}</p>
              </div>
            ` : ''}
          </div>

          <div class="flex flex-col gap-1.5 shrink-0">
            <button onclick="window.DeutschApp.speak('${w.word.replace(/'/g, "\\'")}', this)" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-blue-600 hover:bg-blue-50 transition" title="გამოთქმის მოსმენა">
              🔊
            </button>
            <button onclick="window.DeutschApp.toggleFavorite('${escapeHtml(w.id)}')" class="p-2.5 rounded-xl text-base hover:bg-slate-100 dark:hover:bg-slate-700 transition ${isFav ? 'text-amber-500' : 'text-slate-300'}" title="რჩეულებში დამატება">
              ⭐
            </button>
          </div>
        </div>
      `;
    });

    html += `
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 3: FLASHCARDS (WITH SM-2 SPACED REPETITION ENGINE - STAGE 3)
  // ==========================================================================
  function initFlashcards() {
    let pool = [...window.GERMAN_A1_DATA.dictionary];

    if (state.flashcardMode === 'srs') {
      const today = new Date().toISOString().split('T')[0];
      const srsMap = userData.srsItems || {};
      pool = pool.filter(w => {
        const item = srsMap[w.id];
        return !item || item.nextReviewDate <= today || (userData.mistakeWords || []).includes(w.id);
      });
      if (pool.length === 0) {
        pool = [...window.GERMAN_A1_DATA.dictionary].slice(0, 30);
      }
    } else if (state.flashcardLessonFilter !== 'all') {
      if (state.flashcardLessonFilter === 'fav') {
        const favs = new Set(userData.favoriteWords || []);
        pool = pool.filter(w => favs.has(w.id));
      } else if (state.flashcardLessonFilter === 'mistakes') {
        const mistakes = new Set(userData.mistakeWords || []);
        pool = pool.filter(w => mistakes.has(w.id));
      } else {
        const lid = parseInt(state.flashcardLessonFilter, 10);
        pool = pool.filter(w => w.lesson_id === lid);
      }
    }

    state.flashcardList = pool.sort(() => Math.random() - 0.5);
    state.flashcardIndex = 0;
    state.flashcardFlipped = false;
  }

  function renderFlashcards(container) {
    const total = state.flashcardList.length;

    let html = `
      <div class="max-w-xl mx-auto space-y-6 animate-fadeIn pb-16">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h1 class="text-2xl font-black text-slate-900 dark:text-white">სასწავლო ბარათები & SM-2</h1>
            <p class="text-xs text-slate-500">ინტერვალური გამეორება (Spaced Repetition)</p>
          </div>

          <div class="flex items-center gap-2">
            <button onclick="window.DeutschApp.toggleFlashcardSRSMode()" class="px-3 py-2 rounded-xl text-xs font-black transition ${state.flashcardMode === 'srs' ? 'bg-purple-600 text-white shadow-md' : 'bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-300'}">
              🧠 SM-2 რიგი
            </button>
            <select onchange="window.DeutschApp.onFlashcardLessonFilter(this.value)" class="px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold focus:outline-none">
              <option value="all" ${state.flashcardLessonFilter === 'all' ? 'selected' : ''}>ყველა სიტყვა (734)</option>
              ${window.GERMAN_A1_DATA.lessons.map(l => `
                <option value="${l.id}" ${state.flashcardLessonFilter === String(l.id) ? 'selected' : ''}>გაკვეთილი ${l.id}</option>
              `).join('')}
              <option value="fav" ${state.flashcardLessonFilter === 'fav' ? 'selected' : ''}>⭐ რჩეულები</option>
              <option value="mistakes" ${state.flashcardLessonFilter === 'mistakes' ? 'selected' : ''}>⚠️ შეცდომები (${(userData.mistakeWords || []).length})</option>
            </select>
          </div>
        </div>

        ${total === 0 ? `
          <div class="p-12 text-center text-slate-500 bg-white dark:bg-slate-800 rounded-3xl border border-slate-200 dark:border-slate-700">
            ამ კატეგორიაში ბარათები არ მოიძებნა.
          </div>
        ` : `
          <div class="flex items-center justify-between text-xs font-extrabold text-slate-400">
            <span>ბარათი ${state.flashcardIndex + 1} / ${total}</span>
            <span class="text-emerald-600">ნასწავლია: ${(userData.masteredWords || []).length} სიტყვა</span>
          </div>

          <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
            <div class="bg-blue-600 h-1.5 rounded-full transition-all duration-300" style="width: ${((state.flashcardIndex + 1) / total) * 100}%"></div>
          </div>

          ${state.lessonVocabSession && state.lessonVocabSession.lessonId ? (() => {
            const sess = state.lessonVocabSession;
            const reviewed = sess.reviewedIds.length;
            const minReq = Math.min(5, total);
            const acc = reviewed > 0 ? Math.round((sess.correctCount / reviewed) * 100) : 0;
            const isPassed = reviewed >= minReq && acc >= 70;
            return `
              <div class="p-3 rounded-2xl bg-white dark:bg-slate-800 border ${isPassed ? 'border-emerald-500 bg-emerald-50/50' : 'border-blue-200'} text-xs flex items-center justify-between shadow-sm animate-fadeIn">
                <span class="font-extrabold ${isPassed ? 'text-emerald-700 dark:text-emerald-300' : 'text-blue-700 dark:text-blue-300'} flex items-center gap-1.5">
                  <span>🎯 გაკვეთილი ${sess.lessonId} ლექსიკა:</span>
                  <span>${reviewed} / ${minReq} სიტყვა (სიზუსტე: ${acc}%)</span>
                </span>
                <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black ${isPassed ? 'bg-emerald-600 text-white' : 'bg-slate-100 text-slate-600'}">
                  ${isPassed ? '✓ ათვისებულია' : 'მინ. 5 სიტყვა (≥70%)'}
                </span>
              </div>
            `;
          })() : ''}

          ${(() => {
            const current = state.flashcardList[state.flashcardIndex];
            let badgeClass = 'bg-slate-100 text-slate-700';
            if (current.gender === 'm') badgeClass = 'badge-der';
            else if (current.gender === 'f') badgeClass = 'badge-die';
            else if (current.gender === 'n') badgeClass = 'badge-das';
            else if (current.gender === 'pl') badgeClass = 'badge-pl';

            return `
              <div class="perspective-1000 w-full h-84">
                <div id="flashcard-inner-box" onclick="window.DeutschApp.flipFlashcard()" class="flashcard-inner ${state.flashcardFlipped ? 'is-flipped' : ''} bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl">
                  <!-- FRONT: German -->
                  <div class="flashcard-front bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700">
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-3">${escapeHtml(current.category || 'A1 ლექსიკა')}</span>
                    ${current.article ? `<span class="text-xs font-black px-3 py-1 rounded-full ${badgeClass} mb-2">${escapeHtml(current.article)}</span>` : ''}
                    <h2 class="text-3xl md:text-4xl font-black text-slate-900 dark:text-white mb-2 text-center">${escapeHtml(current.word)}</h2>
                    ${current.plural ? `<p class="text-xs text-slate-400 mb-5 font-bold">Plural: ${escapeHtml(current.plural)}</p>` : '<div class="mb-5"></div>'}

                    <div class="flex items-center gap-2">
                      <button onclick="event.stopPropagation(); window.DeutschApp.speak('${current.word.replace(/'/g, "\\'")}', this)" class="px-4 py-2 rounded-xl bg-blue-50 dark:bg-blue-900/40 text-blue-600 dark:text-blue-300 font-extrabold text-xs flex items-center gap-1.5 hover:bg-blue-100 transition shadow-sm">
                        <span>🔊 მოუსმინე</span>
                      </button>
                    </div>

                    <span class="absolute bottom-4 text-[11px] text-slate-400 font-medium">დააჭირეთ გადასაბრუნებლად ↺</span>
                  </div>

                  <!-- BACK: Georgian & Examples -->
                  <div class="flashcard-back bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-slate-800 dark:to-slate-900 border border-blue-200 dark:border-slate-700">
                    <span class="text-[10px] font-black uppercase tracking-wider text-blue-600 dark:text-blue-400 mb-2">ქართული თარგმანი</span>
                    <h3 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white mb-4 text-center">${escapeHtml(current.georgian)}</h3>

                    ${current.example_de ? `
                      <div class="p-3.5 rounded-xl bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border border-blue-100 dark:border-slate-700 text-xs space-y-1 max-w-sm text-center">
                        <p class="font-bold text-slate-800 dark:text-slate-200">${escapeHtml(current.example_de)}</p>
                        <p class="text-slate-500 italic text-[11px]">${escapeHtml(current.example_ka || '')}</p>
                      </div>
                    ` : ''}

                    <span class="absolute bottom-4 text-[11px] text-slate-400 font-medium">დააჭირეთ უკან დასაბრუნებლად ↺</span>
                  </div>
                </div>
              </div>

              <!-- Controls: SM-2 Weighted Rating -->
              <div class="grid grid-cols-3 gap-3">
                <button onclick="window.DeutschApp.flashcardSM2Action(1)" class="py-3 px-2 rounded-2xl border border-rose-300 dark:border-rose-900/50 bg-rose-50 dark:bg-rose-950/30 text-rose-700 dark:text-rose-300 font-extrabold text-xs hover:bg-rose-100 transition flex items-center justify-center gap-1">
                  <span>❌ რთული (1დღე)</span>
                </button>
                <button onclick="window.DeutschApp.flashcardSM2Action(3)" class="py-3 px-2 rounded-2xl border border-amber-300 dark:border-amber-900/50 bg-amber-50 dark:bg-amber-950/30 text-amber-700 dark:text-amber-300 font-extrabold text-xs hover:bg-amber-100 transition flex items-center justify-center gap-1">
                  <span>🤔 საშუალო</span>
                </button>
                <button onclick="window.DeutschApp.flashcardSM2Action(5)" class="py-3 px-2 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-xs shadow-md transition flex items-center justify-center gap-1 active:scale-95">
                  <span>✓ ვიცი (+5 XP)</span>
                </button>
              </div>
            `;
          })()}
        `}
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 4: PRACTICE TRAINERS HUB (ARTICLES • PLURALS • VERBS • KASUS • MATCHING)
  // ==========================================================================
  function initArticleTrainer() {
    if (!state.trainerCurrentWord) pickNextTrainerWord();
    if (!state.pluralCurrentWord) pickNextPluralWord();
    if (!state.verbCurrentDrill) pickNextVerbDrill();
    if (!state.caseCurrentDrill) pickNextCaseDrill();
    if (state.matchCards.length === 0) initMatchingGame();
  }

  function pickNextTrainerWord() {
    const words = window.GERMAN_A1_DATA.article_trainer_words || [];
    if (words.length === 0) return;
    const randomWord = words[Math.floor(Math.random() * words.length)];
    state.trainerCurrentWord = randomWord;
  }

  function pickNextPluralWord() {
    const list = window.GERMAN_A1_DATA.plural_trainer_words || [];
    if (list.length === 0) return;
    state.pluralIndex = (state.pluralIndex + 1) % list.length;
    state.pluralCurrentWord = list[state.pluralIndex];
    state.pluralFeedback = null;
  }

  function pickNextVerbDrill() {
    const list = window.GERMAN_A1_DATA.verb_conjugations || [];
    if (list.length === 0) return;
    state.verbIndex = (state.verbIndex + 1) % list.length;
    state.verbCurrentDrill = list[state.verbIndex];
    state.verbFeedback = null;
  }

  function pickNextCaseDrill() {
    const all = window.GERMAN_A1_DATA.preposition_cases || [];
    let list = all;
    if (state.caseFilterType !== 'all') {
      list = all.filter(d => d.type === state.caseFilterType);
    }
    if (list.length === 0) list = all;
    if (list.length === 0) return;

    state.caseIndex = (state.caseIndex + 1) % list.length;
    state.caseCurrentDrill = list[state.caseIndex];
    state.caseFeedback = null;
  }

  function pickNextTrennbareDrill() {
    const all = window.GERMAN_A1_DATA.trennbare_verben || [];
    let list = all;
    if (state.trennbarFilterType !== 'all') {
      list = all.filter(d => d.type === state.trennbarFilterType);
    }
    if (list.length === 0) list = all;
    if (list.length === 0) return;

    state.trennbarIndex = (state.trennbarIndex + 1) % list.length;
    state.trennbarCurrentDrill = list[state.trennbarIndex];
    state.trennbarFeedback = null;
  }

  function initMatchingGame() {
    const dict = window.GERMAN_A1_DATA.dictionary || [];
    if (dict.length < 5) return;

    // Pick 5 random words
    const sample = [...dict].sort(() => Math.random() - 0.5).slice(0, 5);
    const cards = [];
    sample.forEach((item, idx) => {
      cards.push({
        id: `pair_${idx}_de`,
        pairId: idx,
        type: 'de',
        text: (item.article ? item.article + ' ' : '') + item.word,
        audio: (item.article ? item.article + ' ' : '') + item.word
      });
      cards.push({
        id: `pair_${idx}_ka`,
        pairId: idx,
        type: 'ka',
        text: item.georgian,
        audio: null
      });
    });

    state.matchCards = cards.sort(() => Math.random() - 0.5);
    state.matchFlipped = [];
    state.matchMatchedIds = [];
    state.matchMoves = 0;
    state.matchCompleted = false;
  }

  function renderPluralTrainerView() {
    const list = window.GERMAN_A1_DATA.plural_trainer_words || [];
    if (!state.pluralCurrentWord && list.length > 0) {
      state.pluralCurrentWord = list[state.pluralIndex % list.length];
    }
    const item = state.pluralCurrentWord;
    if (!item) return `<div class="p-8 text-center text-slate-500">მონაცემები არ არის.</div>`;

    return `
      <div class="space-y-6 animate-fadeIn pb-16">
        <div class="text-center space-y-1">
          <span class="inline-block px-3 py-1 bg-indigo-100 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300 rounded-full text-xs font-black tracking-wider uppercase">
            A1 მრავლობითი რიცხვი • 60 მაღალი სიხშირის არსებითი სახელი
          </span>
          <h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">Plural: მრავლობითი რიცხვის ტრენერი</h2>
          <p class="text-xs text-slate-500 font-medium">შეარჩიეთ არსებითი სახელის სწორი მრავლობითი ფორმა (მოდელები: -er, -e, -(e)n, -s, -)</p>
        </div>

        <div class="grid grid-cols-2 gap-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-4 shadow-sm text-center">
          <div>
            <span class="text-xs font-bold text-slate-400 block uppercase">სწორი პასუხები</span>
            <span class="text-2xl font-black text-indigo-600 dark:text-indigo-400">${state.pluralScore}</span>
          </div>
          <div>
            <span class="text-xs font-bold text-slate-400 block uppercase">სერია (Streak)</span>
            <span class="text-2xl font-black text-amber-500">🔥 ${state.pluralStreak}</span>
          </div>
        </div>

        <div class="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-3xl p-8 text-center shadow-lg transition-all duration-300">
          <span class="text-[11px] font-black uppercase tracking-widest text-slate-400 mb-2 block">მხოლობითი რიცხვი (Singular)</span>
          <h3 class="text-4xl font-black text-slate-900 dark:text-white mb-2">
            ${escapeHtml(item.singular)}
          </h3>
          <p class="text-base font-bold text-indigo-600 dark:text-indigo-400 mb-4">
            ${escapeHtml(item.translation_ka)}
          </p>
          <div class="flex justify-center gap-2">
            <button onclick="window.DeutschApp.speak('${item.singular}', this)" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-bold hover:text-indigo-600 transition">
              <span>🔊 1.0x</span>
            </button>
            <button onclick="window.DeutschApp.speakSlow('${item.singular}', this)" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-bold hover:text-indigo-600 transition">
              <span>🐢 0.7x</span>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
          ${item.options.map(opt => `
            <button onclick="window.DeutschApp.guessPlural('${escapeHtml(opt)}')" class="p-4 rounded-2xl bg-white dark:bg-slate-800 hover:bg-indigo-50 dark:hover:bg-indigo-950/40 border-2 border-slate-200 dark:border-slate-700 hover:border-indigo-500 font-black text-base text-slate-800 dark:text-white shadow-sm active:scale-95 transition text-center">
              ${escapeHtml(opt)}
            </button>
          `).join('')}
        </div>

        <div id="plural-feedback" class="min-h-[50px] text-center font-bold text-xs md:text-sm">
          ${state.pluralFeedback || ''}
        </div>
      </div>
    `;
  }

  function renderVerbTrainerView() {
    const list = window.GERMAN_A1_DATA.verb_conjugations || [];
    if (!state.verbCurrentDrill && list.length > 0) {
      state.verbCurrentDrill = list[state.verbIndex % list.length];
    }
    const drill = state.verbCurrentDrill;
    if (!drill) return `<div class="p-8 text-center text-slate-500">მონაცემები არ არის.</div>`;

    return `
      <div class="space-y-6 animate-fadeIn pb-16">
        <div class="text-center space-y-1">
          <span class="inline-block px-3 py-1 bg-amber-100 dark:bg-amber-900/40 text-amber-800 dark:text-amber-300 rounded-full text-xs font-black tracking-wider uppercase">
            A1 ზმნის უღლება • არარეგულარული & მოდალური ზმნები
          </span>
          <h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">Verben: ზმნის უღლების ტრენერი</h2>
          <p class="text-xs text-slate-500 font-medium">შეარჩიეთ ზმნის სწორი ფორმა მოცემული პირისთვის (Präsens / Vokalwechsel)</p>
        </div>

        <div class="grid grid-cols-2 gap-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-4 shadow-sm text-center">
          <div>
            <span class="text-xs font-bold text-slate-400 block uppercase">სწორი პასუხები</span>
            <span class="text-2xl font-black text-amber-600 dark:text-amber-400">${state.verbScore}</span>
          </div>
          <div>
            <span class="text-xs font-bold text-slate-400 block uppercase">სერია (Streak)</span>
            <span class="text-2xl font-black text-amber-500">🔥 ${state.verbStreak}</span>
          </div>
        </div>

        <div class="bg-gradient-to-br from-slate-900 to-indigo-950 text-white rounded-3xl p-7 text-center shadow-lg space-y-3">
          <div class="flex items-center justify-center gap-2">
            <span class="text-xs font-extrabold uppercase px-2.5 py-1 rounded-lg bg-blue-500/20 text-blue-300 border border-blue-400/30">
              ინფინიტივი: ${escapeHtml(drill.infinitive)}
            </span>
            <span class="text-xs font-black uppercase px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-400/30">
              პირი: ${escapeHtml(drill.pronoun)}
            </span>
            ${drill.shift ? `
              <span class="text-[11px] font-bold px-2 py-0.5 rounded-md bg-purple-500/30 text-purple-200">
                ${escapeHtml(drill.shift)}
              </span>
            ` : ''}
          </div>

          <h3 class="text-2xl md:text-3xl font-black tracking-wide text-white">
            ${escapeHtml(drill.sentence)}
          </h3>

          <p class="text-xs text-slate-300 italic font-medium">
            ${escapeHtml(drill.translation_ka)}
          </p>

          <div class="pt-1 flex justify-center gap-2">
            <button onclick="window.DeutschApp.speak('${drill.infinitive}', this)" class="inline-flex items-center gap-1 px-3 py-1 bg-white/10 hover:bg-white/20 rounded-xl text-xs font-bold transition">
              <span>🔊 ზმნა</span>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          ${drill.options.map(opt => `
            <button onclick="window.DeutschApp.guessVerb('${escapeHtml(opt)}')" class="p-4 rounded-2xl bg-white dark:bg-slate-800 hover:bg-amber-50 dark:hover:bg-amber-950/40 border-2 border-slate-200 dark:border-slate-700 hover:border-amber-500 font-black text-lg text-slate-800 dark:text-white shadow-sm active:scale-95 transition text-center">
              ${escapeHtml(opt)}
            </button>
          `).join('')}
        </div>

        <div id="verb-feedback" class="min-h-[50px] text-center font-bold text-xs md:text-sm">
          ${state.verbFeedback || ''}
        </div>
      </div>
    `;
  }

  function renderMatchingGameView() {
    if (state.matchCards.length === 0) {
      initMatchingGame();
    }

    const matchedPairsCount = Math.floor(state.matchMatchedIds.length / 2);

    return `
      <div class="space-y-6 animate-fadeIn pb-16">
        <div class="text-center space-y-1">
          <span class="inline-block px-3 py-1 bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 rounded-full text-xs font-black tracking-wider uppercase">
            A1 ლექსიკური მეხსიერება • Wort-Paare
          </span>
          <h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">Wort-Paare: წყვილების თამაში</h2>
          <p class="text-xs text-slate-500 font-medium">დააკავშირეთ გერმანული სიტყვა და მისი შესაბამისი ქართული თარგმანი</p>
        </div>

        <div class="flex items-center justify-between bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-4 shadow-sm text-xs font-bold">
          <div class="flex items-center gap-2">
            <span class="text-slate-400 uppercase">ნაპოვნია:</span>
            <span class="text-emerald-600 dark:text-emerald-400 font-black text-base">${matchedPairsCount} / 5</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-slate-400 uppercase">სვლები:</span>
            <span class="text-blue-600 dark:text-blue-400 font-black text-base">${state.matchMoves}</span>
          </div>
          <button onclick="window.DeutschApp.resetMatchingGame()" class="px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 font-extrabold text-xs transition">
            🔄 ახალი თამაში
          </button>
        </div>

        ${state.matchCompleted ? `
          <div class="bg-gradient-to-r from-emerald-500 to-teal-600 rounded-3xl p-8 text-white text-center shadow-xl space-y-4 animate-fadeIn">
            <div class="text-5xl">🎉 🏆</div>
            <h3 class="text-2xl font-black">შესანიშნავია! ყველა წყვილი ნაპოვნია!</h3>
            <p class="text-xs text-emerald-100">თქვენ წარმატებით დააკავშირეთ 5-ვე სიტყვა ${state.matchMoves} სვლაში (+15 XP).</p>
            <button onclick="window.DeutschApp.resetMatchingGame()" class="px-6 py-3 rounded-2xl bg-white text-emerald-800 font-black text-sm shadow-lg hover:bg-emerald-50 transition active:scale-95">
              კვლავ თამაში ↺
            </button>
          </div>
        ` : `
          <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
            ${state.matchCards.map((card, idx) => {
              const isMatched = state.matchMatchedIds.includes(card.id);
              const isSelected = state.matchFlipped.includes(idx);

              let cardClass = "min-h-[90px] p-3 rounded-2xl font-black text-xs md:text-sm shadow-sm transition-all duration-200 flex flex-col items-center justify-center text-center cursor-pointer select-none ";
              if (isMatched) {
                cardClass += "bg-emerald-100 dark:bg-emerald-950/60 border-2 border-emerald-500 text-emerald-800 dark:text-emerald-200 opacity-80 cursor-default";
              } else if (isSelected) {
                cardClass += "bg-blue-600 border-2 border-blue-400 text-white scale-105 shadow-md shadow-blue-500/30";
              } else {
                cardClass += "bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 hover:border-blue-400 dark:hover:border-blue-500 text-slate-800 dark:text-slate-100 active:scale-95";
              }
              return `
                <div onclick="window.DeutschApp.onMatchCardClick(${idx})" class="${cardClass}">
                  <span class="text-[9px] font-bold uppercase tracking-wider block opacity-70 mb-1">
                    ${card.type === 'de' ? '🇩🇪 DE' : '🇬🇪 GE'}
                  </span>
                  <span>${escapeHtml(card.text)}</span>
                </div>
              `;
            }).join('')}
          </div>
        `}
      </div>
    `;
  }

  function renderCaseTrainerView() {
    const all = window.GERMAN_A1_DATA.preposition_cases || [];
    let list = all;
    if (state.caseFilterType !== 'all') {
      list = all.filter(d => d.type === state.caseFilterType);
    }
    if (list.length === 0) list = all;
    if (!state.caseCurrentDrill && list.length > 0) {
      state.caseCurrentDrill = list[state.caseIndex % list.length];
    }
    const drill = state.caseCurrentDrill;
    if (!drill) return `<div class="p-8 text-center text-slate-500">მონაცემები არ არის.</div>`;

    const sampleAudio = drill.sentence.replace('_______', drill.correct);

    return `
      <div class="space-y-6 animate-fadeIn pb-16">
        <div class="text-center space-y-1">
          <span class="inline-block px-3 py-1 bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 rounded-full text-xs font-black tracking-wider uppercase">
            A1 ბრუნვები & წინდებულები • 40 სავარჯიშო წესებით
          </span>
          <h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">Kasus: ბრუნვები & წინდებულები</h2>
          <p class="text-xs text-slate-500 font-medium">შეარჩიეთ სწორი არტიკლი/ნაცვალსახელი წინდებულის მოთხოვნის მიხედვით (Akkusativ, Dativ, Wechsel)</p>
        </div>

        <!-- Filter Sub-Tabs -->
        <div class="flex flex-wrap gap-2 justify-center text-xs font-bold">
          <button onclick="window.DeutschApp.setCaseFilter('all')" class="px-3.5 py-1.5 rounded-xl transition ${state.caseFilterType === 'all' ? 'bg-purple-600 text-white shadow' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
            ყველა (40)
          </button>
          <button onclick="window.DeutschApp.setCaseFilter('dativ')" class="px-3.5 py-1.5 rounded-xl transition ${state.caseFilterType === 'dativ' ? 'bg-purple-600 text-white shadow' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
            Dativ (mit, nach, aus, zu...)
          </button>
          <button onclick="window.DeutschApp.setCaseFilter('akkusativ')" class="px-3.5 py-1.5 rounded-xl transition ${state.caseFilterType === 'akkusativ' ? 'bg-purple-600 text-white shadow' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
            Akkusativ (für, ohne, durch...)
          </button>
          <button onclick="window.DeutschApp.setCaseFilter('wechsel')" class="px-3.5 py-1.5 rounded-xl transition ${state.caseFilterType === 'wechsel' ? 'bg-purple-600 text-white shadow' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
            Wechsel (Wo? / Wohin?)
          </button>
        </div>

        <div class="grid grid-cols-2 gap-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-4 shadow-sm text-center">
          <div>
            <span class="text-xs font-bold text-slate-400 block uppercase">სწორი პასუხები</span>
            <span class="text-2xl font-black text-purple-600 dark:text-purple-400">${state.caseScore}</span>
          </div>
          <div>
            <span class="text-xs font-bold text-slate-400 block uppercase">სერია (Streak)</span>
            <span class="text-2xl font-black text-amber-500">🔥 ${state.caseStreak}</span>
          </div>
        </div>

        <div class="bg-gradient-to-br from-purple-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-7 text-center shadow-lg space-y-3">
          <div class="flex items-center justify-center gap-2">
            <span class="text-xs font-extrabold uppercase px-2.5 py-1 rounded-lg bg-purple-500/20 text-purple-300 border border-purple-400/30">
              წინდებული: ${escapeHtml(drill.preposition)}
            </span>
            <span class="text-xs font-black uppercase px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-400/30">
              ${escapeHtml(drill.hint)}
            </span>
          </div>

          <h3 class="text-2xl md:text-3xl font-black tracking-wide text-white">
            ${escapeHtml(drill.sentence)}
          </h3>

          <p class="text-xs text-slate-300 italic font-medium">
            ${escapeHtml(drill.translation_ka)}
          </p>

          <div class="pt-1 flex justify-center gap-2">
            <button onclick="window.DeutschApp.speak('${sampleAudio.replace(/'/g, "\\'")}', this)" class="inline-flex items-center gap-1 px-3 py-1 bg-white/10 hover:bg-white/20 rounded-xl text-xs font-bold transition">
              <span>🔊 1.0x</span>
            </button>
            <button onclick="window.DeutschApp.speakSlow('${sampleAudio.replace(/'/g, "\\'")}', this)" class="inline-flex items-center gap-1 px-3 py-1 bg-white/10 hover:bg-white/20 rounded-xl text-xs font-bold transition">
              <span>🐢 0.7x</span>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          ${drill.options.map(opt => `
            <button onclick="window.DeutschApp.guessCase('${escapeHtml(opt)}')" class="p-4 rounded-2xl bg-white dark:bg-slate-800 hover:bg-purple-50 dark:hover:bg-purple-950/40 border-2 border-slate-200 dark:border-slate-700 hover:border-purple-500 font-black text-lg text-slate-800 dark:text-white shadow-sm active:scale-95 transition text-center">
              ${escapeHtml(opt)}
            </button>
          `).join('')}
        </div>

        <div id="case-feedback" class="min-h-[50px] text-center font-bold text-xs md:text-sm">
          ${state.caseFeedback || ''}
        </div>
      </div>
    `;
  }

  function renderTrennbareTrainerView() {
    const all = window.GERMAN_A1_DATA.trennbare_verben || [];
    let list = all;
    if (state.trennbarFilterType !== 'all') {
      list = all.filter(d => d.type === state.trennbarFilterType);
    }
    if (list.length === 0) list = all;
    if (!state.trennbarCurrentDrill && list.length > 0) {
      state.trennbarCurrentDrill = list[state.trennbarIndex % list.length];
    }
    const drill = state.trennbarCurrentDrill;
    if (!drill) return `<div class="p-8 text-center text-slate-500">მონაცემები არ არის.</div>`;

    const sampleAudio = drill.full_sentence || drill.sentence.replace('_______', drill.correct);

    return `
      <div class="space-y-6 animate-fadeIn pb-16">
        <div class="text-center space-y-1">
          <span class="inline-block px-3 py-1 bg-rose-100 dark:bg-rose-900/40 text-rose-700 dark:text-rose-300 rounded-full text-xs font-black tracking-wider uppercase">
            A1 თავსართმოცილებადი ზმნები & Satzklammer • 35 სავარჯიშო
          </span>
          <h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">Trennbare Verben: ზმნური ჩარჩო</h2>
          <p class="text-xs text-slate-500 font-medium">ისწავლეთ ზმნის თავსართის გაყოფა აწმყოში, მოდალურ ზმნებში, ბრძანებითსა და Perfekt-ში</p>
        </div>

        <!-- Filter Sub-Tabs -->
        <div class="flex flex-wrap gap-2 justify-center text-xs font-bold">
          <button onclick="window.DeutschApp.setTrennbareFilter('all')" class="px-3.5 py-1.5 rounded-xl transition ${state.trennbarFilterType === 'all' ? 'bg-rose-600 text-white shadow' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
            ყველა (35)
          </button>
          <button onclick="window.DeutschApp.setTrennbareFilter('praesens')" class="px-3.5 py-1.5 rounded-xl transition ${state.trennbarFilterType === 'praesens' ? 'bg-rose-600 text-white shadow' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
            Präsens (15)
          </button>
          <button onclick="window.DeutschApp.setTrennbareFilter('modal')" class="px-3.5 py-1.5 rounded-xl transition ${state.trennbarFilterType === 'modal' ? 'bg-rose-600 text-white shadow' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
            Modalverben (10)
          </button>
          <button onclick="window.DeutschApp.setTrennbareFilter('imperativ_perfekt')" class="px-3.5 py-1.5 rounded-xl transition ${state.trennbarFilterType === 'imperativ_perfekt' ? 'bg-rose-600 text-white shadow' : 'bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300'}">
            Imperativ & Perfekt (10)
          </button>
        </div>

        <div class="grid grid-cols-2 gap-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-4 shadow-sm text-center">
          <div>
            <span class="text-xs font-bold text-slate-400 block uppercase">სწორი პასუხები</span>
            <span class="text-2xl font-black text-rose-600 dark:text-rose-400">${state.trennbarScore}</span>
          </div>
          <div>
            <span class="text-xs font-bold text-slate-400 block uppercase">სერია (Streak)</span>
            <span class="text-2xl font-black text-amber-500">🔥 ${state.trennbarStreak}</span>
          </div>
        </div>

        <div class="bg-gradient-to-br from-rose-900 via-slate-900 to-slate-950 text-white rounded-3xl p-7 text-center shadow-lg space-y-3">
          <div class="flex items-center justify-center gap-2 flex-wrap">
            <span class="text-xs font-extrabold uppercase px-2.5 py-1 rounded-lg bg-rose-500/20 text-rose-300 border border-rose-400/30">
              ზმნა: <strong class="text-amber-300">${escapeHtml(drill.prefix)}</strong>${escapeHtml(drill.stem)}
            </span>
            <span class="text-xs font-black uppercase px-2.5 py-1 rounded-lg bg-amber-500/20 text-amber-300 border border-amber-400/30">
              ${escapeHtml(drill.hint)}
            </span>
          </div>

          <h3 class="text-2xl md:text-3xl font-black tracking-wide text-white">
            ${escapeHtml(drill.sentence)}
          </h3>

          <p class="text-xs text-slate-300 italic font-medium">
            ${escapeHtml(drill.translation_ka)}
          </p>

          <div class="pt-1 flex justify-center gap-2">
            <button onclick="window.DeutschApp.speak('${sampleAudio.replace(/'/g, "\\'")}', this)" class="inline-flex items-center gap-1 px-3 py-1 bg-white/10 hover:bg-white/20 rounded-xl text-xs font-bold transition">
              <span>🔊 1.0x</span>
            </button>
            <button onclick="window.DeutschApp.speakSlow('${sampleAudio.replace(/'/g, "\\'")}', this)" class="inline-flex items-center gap-1 px-3 py-1 bg-white/10 hover:bg-white/20 rounded-xl text-xs font-bold transition">
              <span>🐢 0.7x</span>
            </button>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-3">
          ${drill.options.map(opt => `
            <button onclick="window.DeutschApp.guessTrennbare('${escapeHtml(opt)}')" class="p-4 rounded-2xl bg-white dark:bg-slate-800 hover:bg-rose-50 dark:hover:bg-rose-950/40 border-2 border-slate-200 dark:border-slate-700 hover:border-rose-500 font-black text-base md:text-lg text-slate-800 dark:text-white shadow-sm active:scale-95 transition text-center">
              ${escapeHtml(opt)}
            </button>
          `).join('')}
        </div>

        <div id="trennbar-feedback" class="min-h-[50px] text-center font-bold text-xs md:text-sm">
          ${state.trennbarFeedback || ''}
        </div>
      </div>
    `;
  }

  function renderArticleTrainer(container) {
    if (!container) container = document.getElementById('main-content');
    if (!container) return;

    const mode = state.trainerActiveMode || 'articles';

    const navBar = `
      <div class="flex flex-wrap gap-2 p-1.5 bg-slate-100 dark:bg-slate-800 rounded-2xl text-xs font-black max-w-4xl mx-auto mb-6">
        <button onclick="window.DeutschApp.setTrainerMode('articles')" class="flex-1 py-2.5 px-2 rounded-xl transition text-center ${mode === 'articles' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300 hover:text-blue-600'}">
          🛡️ der / die / das (431)
        </button>
        <button onclick="window.DeutschApp.setTrainerMode('plurals')" class="flex-1 py-2.5 px-2 rounded-xl transition text-center ${mode === 'plurals' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300 hover:text-indigo-600'}">
          👥 Plural (60)
        </button>
        <button onclick="window.DeutschApp.setTrainerMode('verbs')" class="flex-1 py-2.5 px-2 rounded-xl transition text-center ${mode === 'verbs' ? 'bg-amber-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300 hover:text-amber-600'}">
          ⚡ Verben (50)
        </button>
        <button onclick="window.DeutschApp.setTrainerMode('cases')" class="flex-1 py-2.5 px-2 rounded-xl transition text-center ${mode === 'cases' ? 'bg-purple-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300 hover:text-purple-600'}">
          🎯 Kasus (40)
        </button>
        <button onclick="window.DeutschApp.setTrainerMode('trennbare')" class="flex-1 py-2.5 px-2 rounded-xl transition text-center ${mode === 'trennbare' ? 'bg-rose-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300 hover:text-rose-600'}">
          ✂️ Trennbare (35)
        </button>
        <button onclick="window.DeutschApp.setTrainerMode('matching')" class="flex-1 py-2.5 px-2 rounded-xl transition text-center ${mode === 'matching' ? 'bg-emerald-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300 hover:text-emerald-600'}">
          🧩 Wort-Paare
        </button>
      </div>
    `;

    if (mode === 'plurals') {
      container.innerHTML = `<div class="max-w-2xl mx-auto">${navBar}${renderPluralTrainerView()}</div>`;
      return;
    }
    if (mode === 'verbs') {
      container.innerHTML = `<div class="max-w-2xl mx-auto">${navBar}${renderVerbTrainerView()}</div>`;
      return;
    }
    if (mode === 'cases') {
      container.innerHTML = `<div class="max-w-2xl mx-auto">${navBar}${renderCaseTrainerView()}</div>`;
      return;
    }
    if (mode === 'trennbare') {
      container.innerHTML = `<div class="max-w-2xl mx-auto">${navBar}${renderTrennbareTrainerView()}</div>`;
      return;
    }
    if (mode === 'matching') {
      container.innerHTML = `<div class="max-w-2xl mx-auto">${navBar}${renderMatchingGameView()}</div>`;
      return;
    }

    // Default: 'articles'
    const word = state.trainerCurrentWord;
    if (!word) {
      pickNextTrainerWord();
    }
    const currentWord = state.trainerCurrentWord;
    if (!currentWord) return;

    let html = `
      <div class="max-w-2xl mx-auto pb-16">
        ${navBar}
        <div class="max-w-xl mx-auto space-y-8 animate-fadeIn">
          <div class="text-center space-y-2">
            <span class="inline-block px-3 py-1 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-full text-xs font-black tracking-wider uppercase">
              A1 გრამატიკული ტრენერი • 431 არსებითი სახელი
            </span>
            <h1 class="text-3xl font-black text-slate-900 dark:text-white">არტიკლების ტრენერი</h1>
            <p class="text-xs text-slate-500 font-medium">გამოიცანით სწორი არტიკლი: der (მამრ.), die (მდედრ.) თუ das (საშუალო)?</p>
          </div>

          <div class="grid grid-cols-2 gap-4 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-5 shadow-sm text-center">
            <div>
              <span class="text-xs font-bold text-slate-400 block uppercase">სწორი პასუხები</span>
              <span class="text-2xl font-black text-blue-600 dark:text-blue-400">${state.trainerScore}</span>
            </div>
            <div>
              <span class="text-xs font-bold text-slate-400 block uppercase">სერია (Streak)</span>
              <span class="text-2xl font-black text-amber-500">🔥 ${state.trainerStreak}</span>
            </div>
          </div>

          <div id="trainer-card" class="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-3xl p-10 text-center shadow-lg transition-all duration-300">
            <span class="text-[11px] font-black uppercase tracking-widest text-slate-400 mb-2 block">არსებითი სახელი</span>
            <h2 id="trainer-word-display" class="text-4xl md:text-5xl font-black text-slate-900 dark:text-white mb-3">
              ${escapeHtml(currentWord.word)}
            </h2>
            <p class="text-lg font-bold text-blue-600 dark:text-blue-400 mb-5">
              ${escapeHtml(currentWord.georgian)}
            </p>
            <div class="flex justify-center gap-2">
              <button onclick="window.DeutschApp.speak('${currentWord.article} ${currentWord.word}', this)" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-bold hover:text-blue-600 transition">
                <span>🔊 1.0x</span>
              </button>
              <button onclick="window.DeutschApp.speakSlow('${currentWord.article} ${currentWord.word}', this)" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-bold hover:text-blue-600 transition">
                <span>🐢 0.7x</span>
              </button>
            </div>
          </div>

          <div class="grid grid-cols-3 gap-3 md:gap-4">
            <button onclick="window.DeutschApp.guessArticle('der')" class="py-5 px-3 rounded-2xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xl md:text-2xl shadow-lg shadow-blue-500/20 active:scale-95 transition flex flex-col items-center">
              <span>DER</span>
              <span class="text-[11px] font-medium opacity-80 mt-1">მამრობითი</span>
            </button>
            <button onclick="window.DeutschApp.guessArticle('die')" class="py-5 px-3 rounded-2xl bg-rose-600 hover:bg-rose-700 text-white font-black text-xl md:text-2xl shadow-lg shadow-rose-500/20 active:scale-95 transition flex flex-col items-center">
              <span>DIE</span>
              <span class="text-[11px] font-medium opacity-80 mt-1">მდედრობითი</span>
            </button>
            <button onclick="window.DeutschApp.guessArticle('das')" class="py-5 px-3 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xl md:text-2xl shadow-lg shadow-emerald-500/20 active:scale-95 transition flex flex-col items-center">
              <span>DAS</span>
              <span class="text-[11px] font-medium opacity-80 mt-1">საშუალო</span>
            </button>
          </div>

          <div id="trainer-feedback" class="min-h-[50px] text-center font-bold text-sm"></div>
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 5: SENTENCE BUILDER (SATZBAU)
  // ==========================================================================
  function initSentenceBuilder() {
    loadSentenceChallenge(0);
  }

  function loadSentenceChallenge(index) {
    const list = window.GERMAN_A1_DATA.sentence_builders || [];
    state.sbIndex = index % list.length;
    const challenge = list[state.sbIndex];

    state.sbAvailableWords = [...challenge.words].sort(() => Math.random() - 0.5);
    state.sbSelectedWords = [];
    state.sbChecked = false;
    state.sbIsCorrect = false;
  }

  function renderSentenceBuilder(container) {
    const challenge = window.GERMAN_A1_DATA.sentence_builders[state.sbIndex];
    const total = window.GERMAN_A1_DATA.sentence_builders.length;

    let html = `
      <div class="max-w-2xl mx-auto space-y-6 animate-fadeIn pb-16">
        <div class="text-center space-y-1">
          <span class="inline-block px-3 py-1 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-full text-xs font-black tracking-wider uppercase">
            A1 სინტაქსი და სიტყვათწყობა
          </span>
          <h1 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">Satzbau: წინადადების კონსტრუქტორი</h1>
          <p class="text-xs text-slate-500">დაალაგეთ სიტყვები სწორი გერმანული სინტაქსით (V2 წესი / Satzklammer)</p>
        </div>

        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>დონე ${state.sbIndex + 1} / ${total}</span>
        </div>

        <div class="bg-gradient-to-r from-blue-900 to-indigo-900 rounded-3xl p-6 text-white text-center shadow-lg">
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-blue-300 block mb-1">თარგმნეთ ქართულიდან:</span>
          <h2 class="text-xl md:text-2xl font-black">${escapeHtml(challenge.translation_ka)}</h2>
          ${challenge.hint ? `<p class="text-xs text-blue-200 mt-2 italic">💡 წესი: ${escapeHtml(challenge.hint)}</p>` : ''}
        </div>

        <div class="min-h-[90px] p-4 rounded-3xl border-2 border-dashed ${state.sbChecked ? (state.sbIsCorrect ? 'border-emerald-500 bg-emerald-50/50' : 'border-rose-500 bg-rose-50/50') : 'border-blue-300 dark:border-slate-600 bg-white dark:bg-slate-800'} flex flex-wrap items-center gap-2 transition">
          ${state.sbSelectedWords.length === 0 ? `
            <span class="text-xs text-slate-400 italic mx-auto">დააჭირეთ ქვემოთ მოცემულ სიტყვებს წინადადების ასაწყობად</span>
          ` : state.sbSelectedWords.map((w, idx) => `
            <button onclick="window.DeutschApp.removeSentenceWord(${idx})" class="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-sm transition flex items-center gap-1 active:scale-95">
              <span>${escapeHtml(w)}</span>
              <span class="text-[10px] opacity-70">✕</span>
            </button>
          `).join('')}
        </div>

        <div>
          <span class="text-xs font-bold text-slate-400 block mb-2 uppercase">სიტყვების ბანკი:</span>
          <div class="flex flex-wrap gap-2">
            ${state.sbAvailableWords.map((w, idx) => `
              <button onclick="window.DeutschApp.addSentenceWord(${idx})" class="sentence-chip px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-100 font-extrabold text-xs hover:bg-blue-100 dark:hover:bg-slate-600 border border-slate-200 dark:border-slate-600 shadow-sm transition active:scale-95">
                ${escapeHtml(w)}
              </button>
            `).join('')}
          </div>
        </div>

        <div class="flex items-center justify-between pt-2">
          <button onclick="window.DeutschApp.resetSentence()" class="px-4 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 text-xs font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 transition">
            🔄 გასუფთავება
          </button>

          ${!state.sbChecked || !state.sbIsCorrect ? `
            <button onclick="window.DeutschApp.checkSentence()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition disabled:opacity-50" ${state.sbSelectedWords.length === 0 ? 'disabled' : ''}>
              შემოწმება ✓
            </button>
          ` : `
            <button onclick="window.DeutschApp.nextSentence()" class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-xs shadow-md transition">
              შემდეგი დონე →
            </button>
          `}
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 6: CORE LANGUAGE LABS (HÖREN, LESEN, SCHREIBEN, SPRECHEN & DIALOG-CHAT)
  // ==========================================================================
  function renderLanguageLabs(container) {
    const labs = window.GERMAN_A1_DATA.language_labs || {};
    const active = state.labActiveTab;

    let html = `
      <div class="max-w-4xl mx-auto space-y-8 animate-fadeIn pb-16">
        
        <div class="text-center space-y-2">
          <span class="inline-block px-3 py-1 bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 rounded-full text-xs font-black tracking-wider uppercase">
            CEFR A1 ენობრივი ლაბორატორიები & ინტერაქტიული სიმულატორი
          </span>
          <h1 class="text-3xl font-black text-slate-900 dark:text-white">ენობრივი ლაბორატორიები & დიალოგ-ჩატი</h1>
          <p class="text-xs text-slate-500">Hören (მოსმენა), Lesen (კითხვა), Schreiben (წერა), Sprechen (საუბარი), Dialog-Chat (სასაუბრო სიმულატორი)</p>
        </div>

        <!-- Labs Navigation Pills -->
        <div class="flex flex-wrap gap-2 p-1.5 bg-slate-100 dark:bg-slate-800 rounded-2xl text-xs font-black">
          <button onclick="window.DeutschApp.switchLabTab('hoeren')" class="flex-1 py-3 px-2 rounded-xl transition text-center ${active === 'hoeren' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            🎧 1. HÖREN
          </button>
          <button onclick="window.DeutschApp.switchLabTab('lesen')" class="flex-1 py-3 px-2 rounded-xl transition text-center ${active === 'lesen' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            📖 2. LESEN
          </button>
          <button onclick="window.DeutschApp.switchLabTab('schreiben')" class="flex-1 py-3 px-2 rounded-xl transition text-center ${active === 'schreiben' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            ✍️ 3. SCHREIBEN
          </button>
          <button onclick="window.DeutschApp.switchLabTab('sprechen')" class="flex-1 py-3 px-2 rounded-xl transition text-center ${active === 'sprechen' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            🗣️ 4. SPRECHEN
          </button>
          <button onclick="window.DeutschApp.switchLabTab('roleplay')" class="flex-1 py-3 px-2 rounded-xl transition text-center ${active === 'roleplay' ? 'bg-purple-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            💬 5. DIALOG-CHAT
          </button>
          <button onclick="window.DeutschApp.switchLabTab('stories')" class="flex-1 py-3 px-2 rounded-xl transition text-center ${active === 'stories' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            📚 6. KURZGESCHICHTEN
          </button>
          <button onclick="window.DeutschApp.switchLabTab('diktat')" class="flex-1 py-3 px-2 rounded-xl transition text-center ${active === 'diktat' ? 'bg-amber-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            🎙️ 7. HÖR-DIKTAT
          </button>
        </div>

        <div id="lab-tab-content">
    `;

    if (active === 'hoeren') {
      html += renderHoerenLab(labs.hoeren || []);
    } else if (active === 'lesen') {
      html += renderLesenLab(labs.lesen || []);
    } else if (active === 'schreiben') {
      html += renderSchreibenLab(labs.schreiben || []);
    } else if (active === 'sprechen') {
      html += renderSprechenLab(labs.sprechen || []);
    } else if (active === 'roleplay') {
      html += renderRoleplayLab(labs.roleplay || []);
    } else if (active === 'stories') {
      html += renderStoriesLab(labs.stories || window.GERMAN_A1_DATA.mini_stories || []);
    } else if (active === 'diktat') {
      html += renderDiktatLab(labs.diktat || window.GERMAN_A1_DATA.diktat || []);
    }

    html += `
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // --- 1. HÖREN LAB ---
  function renderHoerenLab(tasks) {
    if (tasks.length === 0) return `<p class="text-xs text-slate-500">დავალებები არ არის.</p>`;
    const item = tasks[state.labHoerenIndex % tasks.length];

    let html = `
      <div class="space-y-6 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm animate-fadeIn">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>დავალება ${state.labHoerenIndex + 1} / ${tasks.length} • ${escapeHtml(item.category)}</span>
          <span class="text-blue-600">ქულა: ${state.labHoerenScore}</span>
        </div>

        <h3 class="text-xl font-black text-slate-900 dark:text-white">${escapeHtml(item.title)}</h3>

        <!-- Audio Player Box -->
        <div class="bg-gradient-to-r from-blue-900 to-indigo-950 p-6 rounded-2xl text-white text-center space-y-4">
          <div class="sound-wave text-blue-400">
            <span></span><span></span><span></span><span></span>
          </div>
          <p class="text-xs text-blue-200 font-medium">მოუსმინეთ განცხადებას ყურადღებით (ტექსტი დამალულია):</p>
          <div class="flex justify-center gap-3">
            <button onclick="window.DeutschApp.speak('${item.audio_text.replace(/'/g, "\\'")}', this)" class="px-5 py-2.5 bg-blue-600 hover:bg-blue-500 rounded-xl text-xs font-black shadow-md flex items-center gap-1.5 transition">
              <span>🔊 მოუსმინე</span>
            </button>
            <button onclick="window.DeutschApp.speakSlow('${item.audio_text.replace(/'/g, "\\'")}', this)" class="px-4 py-2.5 bg-white/10 hover:bg-white/20 rounded-xl text-xs font-bold transition">
              <span>🐢 0.7x ნელა</span>
            </button>
          </div>
        </div>

        <!-- Question -->
        <h4 class="text-base font-black text-slate-900 dark:text-white">${escapeHtml(item.question)}</h4>

        <div class="grid grid-cols-1 gap-2.5">
          ${item.options.map((opt, idx) => {
            let cls = 'border-slate-200 dark:border-slate-700 hover:border-blue-400';
            if (state.labHoerenSubmitted) {
              if (idx === item.answer) cls = 'border-emerald-500 bg-emerald-50 dark:bg-emerald-950/40 font-bold text-emerald-900 dark:text-emerald-200';
              else if (idx === state.labHoerenSelectedAnswer) cls = 'border-rose-500 bg-rose-50 dark:bg-rose-950/40 font-bold text-rose-900 dark:text-rose-200';
              else cls = 'opacity-40';
            } else if (state.labHoerenSelectedAnswer === idx) {
              cls = 'border-blue-600 bg-blue-50 dark:bg-blue-900/30 font-bold';
            }

            return `
              <button onclick="window.DeutschApp.onSelectLabHoeren(${idx})" class="p-3.5 rounded-xl border text-left text-xs md:text-sm font-medium transition ${cls}" ${state.labHoerenSubmitted ? 'disabled' : ''}>
                ${String.fromCharCode(65 + idx)}. ${escapeHtml(opt)}
              </button>
            `;
          }).join('')}
        </div>

        ${state.labHoerenSubmitted ? `
          <div class="p-4 rounded-xl bg-slate-50 dark:bg-slate-700/30 border border-slate-200 dark:border-slate-700 text-xs space-y-1.5 animate-fadeIn">
            <span class="font-bold text-slate-700 dark:text-slate-200 block">📜 აუდიოს სრული ტრანსკრიფცია და თარგმანი:</span>
            <p class="font-bold text-slate-900 dark:text-white">"${escapeHtml(item.audio_text)}"</p>
            <p class="text-slate-600 dark:text-slate-400 italic">${escapeHtml(item.transcript_ka)}</p>
          </div>
        ` : ''}

        <div class="flex justify-between items-center pt-2">
          <button onclick="window.DeutschApp.nextLabHoeren(${tasks.length})" class="text-xs font-bold text-slate-500 hover:text-slate-700">
            სხვა დავალებაზე გადასვლა →
          </button>

          ${!state.labHoerenSubmitted ? `
            <button onclick="window.DeutschApp.submitLabHoeren()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-md transition disabled:opacity-50" ${state.labHoerenSelectedAnswer === null ? 'disabled' : ''}>
              შემოწმება ✓
            </button>
          ` : `
            <button onclick="window.DeutschApp.nextLabHoeren(${tasks.length})" class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs shadow-md transition">
              შემდეგი აუდიო →
            </button>
          `}
        </div>
      </div>
    `;

    return html;
  }

  // --- 2. LESEN LAB ---
  function renderLesenLab(tasks) {
    if (tasks.length === 0) return `<p class="text-xs text-slate-500">დავალებები არ არის.</p>`;
    const item = tasks[state.labLesenIndex % tasks.length];

    let html = `
      <div class="space-y-6 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm animate-fadeIn">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>ტექსტი ${state.labLesenIndex + 1} / ${tasks.length} • ${escapeHtml(item.category)}</span>
        </div>

        <h3 class="text-xl font-black text-slate-900 dark:text-white">${escapeHtml(item.title)}</h3>

        <!-- Realia Text Box -->
        <div class="p-6 rounded-2xl bg-slate-50 dark:bg-slate-700/40 border border-slate-200 dark:border-slate-600 font-mono text-xs md:text-sm text-slate-800 dark:text-slate-100 whitespace-pre-line leading-relaxed shadow-inner">
${escapeHtml(item.text_de)}
        </div>

        <!-- Questions on text -->
        <div class="space-y-5">
          ${item.questions.map((q, qIdx) => {
            const userAns = state.labLesenAnswers[qIdx];
            return `
              <div class="p-4 rounded-xl border border-slate-100 dark:border-slate-700 space-y-2">
                <h5 class="text-xs md:text-sm font-extrabold text-slate-900 dark:text-white">${qIdx + 1}. ${escapeHtml(q.q)}</h5>
                <div class="grid grid-cols-1 gap-2">
                  ${q.options.map((opt, oIdx) => {
                    let cls = 'border-slate-200 dark:border-slate-700 hover:bg-slate-50';
                    if (state.labLesenSubmitted) {
                      if (oIdx === q.answer) cls = 'border-emerald-500 bg-emerald-50 font-bold text-emerald-800';
                      else if (userAns === oIdx) cls = 'border-rose-500 bg-rose-50 font-bold text-rose-800';
                      else cls = 'opacity-40';
                    } else if (userAns === oIdx) {
                      cls = 'border-blue-600 bg-blue-50 font-bold text-blue-900';
                    }
                    return `
                      <button onclick="window.DeutschApp.onSelectLabLesen(${qIdx}, ${oIdx})" class="p-2.5 rounded-lg border text-left text-xs transition ${cls}" ${state.labLesenSubmitted ? 'disabled' : ''}>
                        ${String.fromCharCode(65 + oIdx)}. ${escapeHtml(opt)}
                      </button>
                    `;
                  }).join('')}
                </div>
                ${state.labLesenSubmitted ? `<p class="text-[11px] text-slate-500 mt-1 italic font-medium">💡 ${escapeHtml(q.explanation)}</p>` : ''}
              </div>
            `;
          }).join('')}
        </div>

        <div class="flex justify-between items-center pt-2">
          <button onclick="window.DeutschApp.nextLabLesen(${tasks.length})" class="text-xs font-bold text-slate-500 hover:text-slate-700">
            სხვა ტექსტზე გადასვლა →
          </button>

          ${!state.labLesenSubmitted ? `
            <button onclick="window.DeutschApp.submitLabLesen()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-md transition">
              შემოწმება ✓
            </button>
          ` : `
            <button onclick="window.DeutschApp.nextLabLesen(${tasks.length})" class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs shadow-md transition">
              შემდეგი ტექსტი →
            </button>
          `}
        </div>
      </div>
    `;

    return html;
  }

  // --- 3. SCHREIBEN LAB ---
  function renderSchreibenLab(tasks) {
    if (tasks.length === 0) return `<p class="text-xs text-slate-500">დავალებები არ არის.</p>`;
    const item = tasks[state.labSchreibenTaskIndex % tasks.length];

    let html = `
      <div class="space-y-6 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm animate-fadeIn">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>დავალება ${state.labSchreibenTaskIndex + 1} / ${tasks.length} • ტიპი: ${item.type === 'form' ? 'სარეგისტრაციო ფორმა' : 'წერითი დავალება'}</span>
        </div>

        <h3 class="text-xl font-black text-slate-900 dark:text-white">${escapeHtml(item.title)}</h3>
        <p class="text-xs text-slate-600 dark:text-slate-400 whitespace-pre-line leading-relaxed">${escapeHtml(item.instructions_ka)}</p>
    `;

    if (item.type === 'form') {
      html += `
        <form onsubmit="event.preventDefault(); window.DeutschApp.submitSchreibenForm();" class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          ${item.fields.map(f => `
            <div class="space-y-1">
              <label class="text-xs font-bold text-slate-700 dark:text-slate-200 flex justify-between">
                <span>${escapeHtml(f.label_de)}</span>
                <span class="text-slate-400 font-normal">(${escapeHtml(f.label_ka)})</span>
              </label>
              <input type="text" value="${escapeHtml(state.labSchreibenFormInputs[f.id] || '')}" oninput="window.DeutschApp.onSchreibenFormInput('${f.id}', this.value)" placeholder="${escapeHtml(f.placeholder)}" class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 text-xs font-medium focus:outline-none focus:border-blue-500 bg-slate-50 dark:bg-slate-700">
            </div>
          `).join('')}

          <div class="md:col-span-2 pt-3 flex justify-end">
            <button type="submit" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-md transition">
              ფორმის ჩაბარება (+15 XP) ✓
            </button>
          </div>
        </form>

        ${state.labSchreibenFormSubmitted ? `
          <div class="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 text-emerald-900 dark:text-emerald-200 text-xs animate-fadeIn space-y-1">
            <span class="font-bold">✓ ფორმა წარმატებით შეივსო!</span>
            <p>გერმანიის სასტუმროებსა და უწყებებში ფორმები ივსება ზუსტად ამ ფორმატით.</p>
          </div>
        ` : ''}
      `;
    } else {
      // Stage 9.1: Restore persistent draft if current text is empty
      if (!state.labSchreibenText) {
        state.labSchreibenText = (userData.writingDrafts && userData.writingDrafts[item.id]) || state.labSchreibenDrafts[item.id] || '';
        state.labSchreibenDrafts[item.id] = state.labSchreibenText;
      }

      const isSubmitted = Boolean(state.labSchreibenSubmittedTasks[item.id]);
      const savedScore = (userData.labScores && userData.labScores.schreiben && userData.labScores.schreiben[item.id]) || {};
      const isSelfReviewed = savedScore.state === 'self_reviewed' || savedScore.completed === true;
      const rubricsState = state.labSchreibenRubricChecks[item.id] || {};
      const wordsCount = (state.labSchreibenText.trim().match(/\S+/g) || []).length;

      html += `
        <!-- German character helper keys -->
        <div class="flex flex-wrap gap-1.5 pt-2">
          <span class="text-[10px] text-slate-400 mr-1 font-bold">გერმანული სიმბოლოები:</span>
          <button onclick="window.DeutschApp.appendSchreibenChar('ä')" class="german-key">ä</button>
          <button onclick="window.DeutschApp.appendSchreibenChar('ö')" class="german-key">ö</button>
          <button onclick="window.DeutschApp.appendSchreibenChar('ü')" class="german-key">ü</button>
          <button onclick="window.DeutschApp.appendSchreibenChar('ß')" class="german-key">ß</button>
          <button onclick="window.DeutschApp.appendSchreibenChar('Ä')" class="german-key">Ä</button>
          <button onclick="window.DeutschApp.appendSchreibenChar('Ö')" class="german-key">Ö</button>
          <button onclick="window.DeutschApp.appendSchreibenChar('Ü')" class="german-key">Ü</button>
        </div>

        <div class="relative">
          <textarea id="schreiben-textarea" rows="6" oninput="window.DeutschApp.onSchreibenTextInput(this.value)" placeholder="დაწერეთ თქვენი გერმანული ტექსტი აქ..." class="w-full p-4 rounded-2xl border border-slate-200 dark:border-slate-600 bg-slate-50 dark:bg-slate-700 text-xs md:text-sm font-medium focus:outline-none focus:border-blue-500">${escapeHtml(state.labSchreibenText)}</textarea>
          <span class="absolute bottom-3 right-3 text-[11px] font-bold text-slate-400">
            სიტყვების რაოდენობა: <strong class="text-blue-600">${wordsCount}</strong> (სასურველი: ${escapeHtml(item.suggested_length)})
          </span>
        </div>

        <!-- 4-Stage Pedagogical Audit Disclaimer -->
        <div class="p-3 bg-blue-50/70 dark:bg-slate-700/40 rounded-xl text-xs text-blue-900 dark:text-blue-200 font-medium">
          ℹ️ <strong>პედაგოგიური სტანდარტი (Stage 9):</strong> წერითი დავალების გაგზავნა ხსნის ეტალონურ ნიმუშს. ქულა (+15 XP) გაიცემა მხოლოდ მას შემდეგ, რაც დაასრულებთ 4-პუნქტიან თვითშეფასების რუბრიკას. სისტემა არ გასცემს შეფასებას მხოლოდ სიმბოლოების რაოდენობაზე დაყრდნობით.
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
          <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-700/30 border border-slate-200 dark:border-slate-700 text-xs space-y-2">
            <span class="font-bold text-slate-700 dark:text-slate-200 block">📋 შეფასების კრიტერიუმები (Rubric):</span>
            <ul class="space-y-1 text-slate-600 dark:text-slate-400">
              ${(item.rubrics || []).map(r => `<li>• ${escapeHtml(r)}</li>`).join('')}
            </ul>
          </div>

          <div class="p-4 rounded-2xl bg-amber-50/70 dark:bg-amber-950/20 border border-amber-200 text-xs space-y-2">
            <span class="font-bold text-amber-900 dark:text-amber-200 block">💡 ეტალონური ნიმუში (Musterlösung):</span>
            ${(isSubmitted || isSelfReviewed) ? `
              <p class="text-amber-900 dark:text-amber-300 font-mono whitespace-pre-line text-[11px] animate-fadeIn">${escapeHtml(item.model_solution)}</p>
            ` : `
              <p class="text-slate-400 italic text-[11px]">ეტალონური ნიმუში გაიხსნება თქვენი წერილის გაგზავნის (მინ. ${item.min_words || 15} სიტყვა) შემდეგ.</p>
            `}
          </div>

          ${(isSubmitted || isSelfReviewed) ? `
            <!-- Interactive 4-Point Self-Assessment Rubric (Stage 9) -->
            <div class="md:col-span-2 p-4 rounded-2xl bg-blue-50/70 dark:bg-slate-700/30 border border-blue-200 dark:border-slate-700 text-xs space-y-3 animate-fadeIn">
              <div class="flex items-center justify-between">
                <span class="font-extrabold text-blue-900 dark:text-blue-200 block">
                  📋 თვითშეფასების რუბრიკა (შეადარეთ თქვენი ტექსტი ეტალონურ ნიმუშს):
                </span>
                ${isSelfReviewed ? `
                  <span class="px-2.5 py-0.5 rounded-full bg-emerald-600 text-white font-black text-[10px]">
                    ✓ თვითშეფასება დადასტურებულია (+15 XP)
                  </span>
                ` : `
                  <span class="px-2.5 py-0.5 rounded-full bg-amber-400 text-slate-950 font-black text-[10px]">
                    საჭიროებს რუბრიკის მონიშვნას (მინ. 3 პუნქტი)
                  </span>
                `}
              </div>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                ${(item.rubrics || []).map((r, rIdx) => {
                  const isChecked = Boolean(rubricsState[rIdx] || isSelfReviewed);
                  return `
                    <label class="flex items-start gap-2.5 p-2.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 cursor-pointer hover:border-blue-400 transition">
                      <input type="checkbox" onchange="window.DeutschApp.onToggleSchreibenRubric('${item.id}', ${rIdx})" ${isChecked ? 'checked' : ''} ${isSelfReviewed ? 'disabled' : ''} class="mt-0.5 rounded text-blue-600">
                      <span class="text-slate-700 dark:text-slate-200 font-medium">${escapeHtml(r)}</span>
                    </label>
                  `;
                }).join('')}
              </div>

              ${!isSelfReviewed ? `
                <div class="flex justify-end pt-2">
                  <button onclick="window.DeutschApp.confirmSchreibenSelfReview('${item.id}')" class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs shadow-md transition active:scale-95">
                    თვითშეფასების დადასტურება (+15 XP) ✓
                  </button>
                </div>
              ` : ''}
            </div>
          ` : ''}
        </div>
      `;
    }

    html += `
        <div class="flex justify-between items-center pt-2">
          <button onclick="window.DeutschApp.nextLabSchreiben(${tasks.length})" class="text-xs font-bold text-slate-500 hover:text-slate-700">
            სხვა დავალებაზე გადასვლა →
          </button>

          ${item.type !== 'form' ? `
            ${!state.labSchreibenSubmittedTasks[item.id] && !(userData.labScores && userData.labScores.schreiben && userData.labScores.schreiben[item.id] && userData.labScores.schreiben[item.id].completed) ? `
              <button onclick="window.DeutschApp.submitSchreibenLetter()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-md transition">
                წერილის გაგზავნა თვითშეფასებისთვის →
              </button>
            ` : `
              <button onclick="window.DeutschApp.nextLabSchreiben(${tasks.length})" class="px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-xs shadow-md transition">
                შემდეგი წერითი დავალება →
              </button>
            `}
          ` : ''}
        </div>
      </div>
    `;

    return html;
  }

  // --- 4. SPRECHEN LAB (MICROPHONE RECORDING & MODEL VOICE) ---
  function renderSprechenLab(tasks) {
    if (tasks.length === 0) return `<p class="text-xs text-slate-500">დავალებები არ არის.</p>`;
    const item = tasks[state.labSprechenPromptIndex % tasks.length];

    let html = `
      <div class="space-y-6 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm animate-fadeIn">
        <div class="flex items-center justify-between text-xs font-bold text-slate-400">
          <span>მოდული ${state.labSprechenPromptIndex + 1} / ${tasks.length}</span>
        </div>

        <h3 class="text-xl font-black text-slate-900 dark:text-white">${escapeHtml(item.title)}</h3>
        <p class="text-xs text-slate-500">${escapeHtml(item.instructions_ka)}</p>

        <div class="p-3 bg-purple-50/70 dark:bg-slate-700/40 rounded-xl text-xs text-purple-900 dark:text-purple-200 font-medium">
          ℹ️ <strong>პედაგოგიური შენიშვნა:</strong> მიკროფონის ჩანაწერი განკუთვნილია თვითშეფასებისთვის — მოუსმინეთ საკუთარ ხმას და შეადარეთ გერმანულ მოდელს. Deutsch A1 Pro არ იგონებს ცრუ AI ქულებს.
        </div>

        <!-- Recording & Playback Studio Card -->
        <div class="bg-gradient-to-r from-purple-900 via-indigo-950 to-slate-900 rounded-3xl p-6 text-white text-center space-y-4 shadow-xl">
          <span class="text-[10px] font-black uppercase tracking-wider text-purple-300 block">🎙️ ხმის ჩამწერი სტუდია</span>
          
          <div class="flex justify-center items-center gap-3">
            <div class="sound-wave text-purple-400">
              <span></span><span></span><span></span><span></span>
            </div>
            <p class="text-xs text-slate-300 font-medium">ჩაიწერეთ თქვენი საუბარი, მოუსმინეთ საკუთარ ხმას და შეადარეთ ეტალონს:</p>
            <div class="sound-wave text-purple-400">
              <span></span><span></span><span></span><span></span>
            </div>
          </div>

          <div class="flex justify-center gap-3 pt-2">
            ${!state.isRecording ? `
              <button onclick="window.DeutschApp.startVoiceRecording()" class="px-6 py-3 rounded-2xl bg-rose-600 hover:bg-rose-500 text-white font-black text-xs shadow-lg transition flex items-center gap-2 active:scale-95">
                <span>🔴 ჩაწერის დაწყება</span>
              </button>
            ` : `
              <button onclick="window.DeutschApp.stopVoiceRecording()" class="px-6 py-3 rounded-2xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs shadow-lg transition flex items-center gap-2 animate-pulse">
                <span>⏹️ ჩაწერის დასრულება</span>
              </button>
            `}

            ${item.full_sample_de ? `
              <button onclick="window.DeutschApp.speak('${item.full_sample_de.replace(/'/g, "\\'")}', this)" class="px-5 py-3 rounded-2xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs backdrop-blur-md transition flex items-center gap-1.5">
                <span>🔊 ეტალონური აუდიო</span>
              </button>
            ` : ''}
          </div>

          <!-- Playback of user recording -->
          <div id="user-recording-playback-area" class="pt-2">
            ${state.recordedAudioUrl ? `
              <div class="p-3 rounded-xl bg-white/10 backdrop-blur-sm max-w-sm mx-auto flex items-center justify-between gap-3">
                <span class="text-xs font-bold text-emerald-300">✓ თქვენი ჩანაწერი:</span>
                <audio controls src="${state.recordedAudioUrl}" class="h-8 max-w-[200px]"></audio>
              </div>
            ` : ''}
          </div>
        </div>

        <!-- Prompts / Situations list with Live Pronunciation Evaluation -->
        <div class="space-y-3">
          ${(item.prompts || []).map((p, pIdx) => {
            const pId = 'p_' + item.id + '_' + pIdx;
            const isEvaluating = state.speechEvaluatingId === pId;
            const evalRes = state.speechEvalResults[pId];
            return `
            <div class="p-4 rounded-2xl border border-slate-100 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-700/20 space-y-2">
              <div class="flex items-center justify-between gap-3">
                <div>
                  <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block">${escapeHtml(p.point)}</span>
                  <p class="font-extrabold text-xs md:text-sm text-slate-900 dark:text-white">${escapeHtml(p.phrase_de)}</p>
                </div>
                <div class="flex items-center gap-1.5 flex-shrink-0">
                  <button onclick="window.DeutschApp.speak('${p.phrase_de.replace(/'/g, "\\'")}', this)" class="p-2 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-blue-600 text-xs font-bold transition active:scale-95" title="ეტალონის მოსმენა">
                    🔊
                  </button>
                  <button onclick="window.DeutschApp.evaluatePronunciation('${pId}', '${p.phrase_de.replace(/'/g, "\\'")}')" class="px-3 py-2 rounded-xl ${isEvaluating ? 'bg-amber-500 text-slate-950 font-black mic-pulse' : 'bg-blue-600 hover:bg-blue-700 text-white font-bold'} text-xs shadow-sm transition flex items-center gap-1 active:scale-95" title="გამოთქმის შემოწმება">
                    <span>${isEvaluating ? '🎙️ გისმენთ...' : '🎤 გამოთქმის ტესტი'}</span>
                  </button>
                </div>
              </div>

              ${evalRes ? `
                <div class="pt-2 border-t border-slate-200/60 dark:border-slate-600/60 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs animate-fadeIn">
                  <div class="flex flex-wrap items-center gap-1">
                    <span class="text-[10px] font-bold text-slate-400 mr-1">ანალიზი:</span>
                    ${evalRes.wordStatus.map(w => `
                      <span class="px-2 py-0.5 rounded-md font-bold text-[11px] ${w.matched ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950/80 dark:text-rose-300'}">
                        ${escapeHtml(w.word)} ${w.matched ? '✓' : '✗'}
                      </span>
                    `).join('')}
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="px-2.5 py-0.5 rounded-full font-black text-[10px] ${evalRes.passed ? 'bg-emerald-600 text-white' : 'bg-amber-400 text-slate-950'}">
                      ${evalRes.score}% • ${evalRes.passed ? '✓ ჩათვლილია (+10 XP)' : 'საჭიროებს ვარჯიშს'}
                    </span>
                    ${evalRes.transcript ? `<span class="text-[10px] text-slate-400 italic">("${escapeHtml(evalRes.transcript)}")</span>` : ''}
                  </div>
                </div>
              ` : ''}
            </div>
            `;
          }).join('')}

          ${(item.situations || []).map((s, sIdx) => {
            const sId = 's_' + item.id + '_' + sIdx;
            const isEvaluating = state.speechEvaluatingId === sId;
            const evalRes = state.speechEvalResults[sId];
            return `
            <div class="p-4 rounded-2xl border border-slate-100 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-700/20 space-y-2">
              <span class="text-xs font-bold text-slate-500">${escapeHtml(s.situation_ka)}</span>
              <div class="flex items-center justify-between gap-3">
                <div>
                  <p class="font-extrabold text-sm text-slate-900 dark:text-white">${escapeHtml(s.phrase_de)}</p>
                  <p class="text-xs text-slate-400 italic">${escapeHtml(s.phrase_ka)}</p>
                </div>
                <div class="flex items-center gap-1.5 flex-shrink-0">
                  <button onclick="window.DeutschApp.speak('${s.phrase_de.replace(/'/g, "\\'")}', this)" class="p-2 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-blue-600 text-xs font-bold transition active:scale-95" title="ეტალონის მოსმენა">
                    🔊
                  </button>
                  <button onclick="window.DeutschApp.evaluatePronunciation('${sId}', '${s.phrase_de.replace(/'/g, "\\'")}')" class="px-3 py-2 rounded-xl ${isEvaluating ? 'bg-amber-500 text-slate-950 font-black mic-pulse' : 'bg-blue-600 hover:bg-blue-700 text-white font-bold'} text-xs shadow-sm transition flex items-center gap-1 active:scale-95" title="გამოთქმის შემოწმება">
                    <span>${isEvaluating ? '🎙️ გისმენთ...' : '🎤 გამოთქმის ტესტი'}</span>
                  </button>
                </div>
              </div>

              ${evalRes ? `
                <div class="pt-2 border-t border-slate-200/60 dark:border-slate-600/60 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs animate-fadeIn">
                  <div class="flex flex-wrap items-center gap-1">
                    <span class="text-[10px] font-bold text-slate-400 mr-1">ანალიზი:</span>
                    ${evalRes.wordStatus.map(w => `
                      <span class="px-2 py-0.5 rounded-md font-bold text-[11px] ${w.matched ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-950/80 dark:text-rose-300'}">
                        ${escapeHtml(w.word)} ${w.matched ? '✓' : '✗'}
                      </span>
                    `).join('')}
                  </div>
                  <div class="flex items-center gap-2">
                    <span class="px-2.5 py-0.5 rounded-full font-black text-[10px] ${evalRes.passed ? 'bg-emerald-600 text-white' : 'bg-amber-400 text-slate-950'}">
                      ${evalRes.score}% • ${evalRes.passed ? '✓ ჩათვლილია (+10 XP)' : 'საჭიროებს ვარჯიშს'}
                    </span>
                    ${evalRes.transcript ? `<span class="text-[10px] text-slate-400 italic">("${escapeHtml(evalRes.transcript)}")</span>` : ''}
                  </div>
                </div>
              ` : ''}
            </div>
            `;
          }).join('')}
        </div>

        <div class="flex justify-end pt-2">
          <button onclick="window.DeutschApp.nextLabSprechen(${tasks.length})" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-100 transition">
            შემდეგი სასაუბრო მოდული →
          </button>
        </div>
      </div>
    `;

    return html;
  }

  // --- 5. ROLEPLAY LAB (Stage 10 Part 3 - Chat Simulator) ---
  function renderRoleplayLab(scenarios) {
    if (!scenarios || scenarios.length === 0) {
      return `<p class="text-xs text-slate-500">სასაუბრო სცენარები არ მოიძებნა.</p>`;
    }

    const scIdx = state.labRoleplayIndex % scenarios.length;
    const sc = scenarios[scIdx];
    const totalSteps = (sc.steps && sc.steps.length) || 0;
    const maxPoints = totalSteps * 10;
    const isCompleted = state.roleplayCompleted || state.roleplayStep >= totalSteps;
    const savedScore = (userData.labScores && userData.labScores.roleplay && userData.labScores.roleplay[sc.id]) ? userData.labScores.roleplay[sc.id] : null;

    let html = `
      <div class="space-y-6 bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm animate-fadeIn">
        
        <!-- Scenarios Selection Bar -->
        <div class="space-y-2">
          <div class="flex items-center justify-between text-xs font-bold text-slate-400">
            <span>სასაუბრო სცენარები (${scenarios.length} თემა)</span>
            <span class="text-purple-600 dark:text-purple-400 font-bold">A1 რეალური ყოველდღიური დიალოგები</span>
          </div>
          <div class="flex flex-wrap gap-2">
            ${scenarios.map((s, idx) => {
              const isActive = (idx === scIdx);
              const rec = (userData.labScores && userData.labScores.roleplay && userData.labScores.roleplay[s.id]);
              return `
                <button onclick="window.DeutschApp.switchRoleplayScenario(${idx})" class="flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-bold transition ${isActive ? 'bg-purple-600 text-white shadow-md' : 'bg-slate-100 dark:bg-slate-700/60 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'}">
                  <span>${s.avatar || '💬'}</span>
                  <span class="truncate max-w-[150px]">${escapeHtml(s.title.split('(')[0].trim())}</span>
                  ${rec ? `<span class="px-1.5 py-0.2 rounded-full text-[10px] ${rec.score >= 60 ? 'bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 font-black' : 'bg-amber-500/20 text-amber-600 font-bold'}">✓ ${rec.score}%</span>` : ''}
                </button>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Scenario Context Banner -->
        <div class="p-4 md:p-5 rounded-2xl bg-gradient-to-r from-purple-900 via-indigo-950 to-slate-900 text-white space-y-3 shadow-md">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <span class="text-3xl">${sc.avatar || '🤵'}</span>
              <div>
                <h3 class="font-black text-base md:text-lg">${escapeHtml(sc.title)}</h3>
                <p class="text-xs text-purple-200">${escapeHtml(sc.partner_name)} • ${escapeHtml(sc.partner_role)}</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span class="px-3 py-1 rounded-full text-xs font-black bg-purple-500/30 text-purple-200 border border-purple-400/30">
                ${isCompleted ? 'სტატუსი: დასრულებული' : `ნაბიჯი: ${Math.min(state.roleplayStep + 1, totalSteps)} / ${totalSteps}`}
              </span>
              <span class="px-3 py-1 rounded-full text-xs font-black bg-white/10 text-white">
                ქულა: ${state.roleplayPoints} / ${maxPoints}
              </span>
              <button onclick="window.DeutschApp.restartRoleplayScenario()" class="px-3 py-1 rounded-xl bg-white/10 hover:bg-white/20 text-xs font-bold text-white transition" title="თავიდან დაწყება">
                🔄 თავიდან
              </button>
            </div>
          </div>
          <p class="text-xs text-slate-300 leading-relaxed border-t border-purple-500/20 pt-2.5">
            📍 <strong>სიტუაცია:</strong> ${escapeHtml(sc.situation_ka)}
          </p>
        </div>

        <!-- Chat Stream Area -->
        <div id="roleplay-chat-stream" class="space-y-4 max-h-[520px] overflow-y-auto p-4 md:p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700/80">
          
          <div class="text-center">
            <span class="inline-block px-3 py-1 rounded-full text-[11px] font-bold bg-slate-200 dark:bg-slate-800 text-slate-500 dark:text-slate-400">
              💬 საუბრის დასაწყისი • გაესაუბრეთ პარტნიორს გერმანულად
            </span>
          </div>

          <!-- History items -->
          ${state.roleplayHistory.map((h, hIdx) => {
            const showTranslation = state.roleplayShowTranslations['hist_' + hIdx];
            return `
              <!-- Partner Turn -->
              <div class="flex items-start gap-3 max-w-[85%] md:max-w-[75%]">
                <span class="text-2xl flex-shrink-0">${sc.avatar || '🤵'}</span>
                <div class="space-y-1">
                  <span class="text-[11px] font-bold text-slate-400">${escapeHtml(sc.partner_name)}</span>
                  <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl rounded-tl-sm p-3.5 shadow-sm space-y-2">
                    <p class="text-sm font-bold text-slate-900 dark:text-white leading-relaxed">${escapeHtml(h.partner_de)}</p>
                    <div class="flex items-center gap-2 pt-1 border-t border-slate-100 dark:border-slate-700">
                      <button onclick="window.DeutschApp.speak('${h.partner_de.replace(/'/g, "\\'")}', this)" class="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-purple-600 text-xs font-bold transition flex items-center gap-1" title="მოსმენა">
                        <span>🔊 მოუსმინე</span>
                      </button>
                      <button onclick="window.DeutschApp.toggleRoleplayTranslation('hist_${hIdx}')" class="px-2 py-1 rounded-lg text-xs font-bold text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-950/40 transition">
                        💡 ${showTranslation ? 'თარგმანის დამალვა' : 'ქართულად'}
                      </button>
                    </div>
                    ${showTranslation ? `<p class="text-xs text-purple-800 dark:text-purple-300 italic pt-1">${escapeHtml(h.partner_ka)}</p>` : ''}
                  </div>
                </div>
              </div>

              <!-- User Response -->
              <div class="flex items-start justify-end gap-3 max-w-[85%] md:max-w-[75%] ml-auto">
                <div class="space-y-1 text-right w-full">
                  <div class="flex items-center justify-end gap-2">
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-black ${h.chosen.points >= 9 ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300' : (h.chosen.points >= 6 ? 'bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-300' : 'bg-rose-100 dark:bg-rose-950 text-rose-700 dark:text-rose-300')}">
                      +${h.chosen.points} / 10 ქულა
                    </span>
                    <span class="text-[11px] font-bold text-slate-400">თქვენ</span>
                  </div>
                  <div class="bg-purple-600 text-white rounded-2xl rounded-tr-sm p-3.5 shadow-sm text-left">
                    <p class="text-sm font-bold leading-relaxed">${escapeHtml(h.chosen.text_de)}</p>
                  </div>
                  <!-- Pedagogical Feedback Card -->
                  <div class="bg-purple-50 dark:bg-slate-800/90 border border-purple-200 dark:border-purple-900/60 rounded-xl p-2.5 text-left text-xs space-y-1">
                    <p class="text-purple-950 dark:text-purple-200 font-medium">💡 <strong>შეფასება:</strong> ${escapeHtml(h.chosen.feedback_ka)}</p>
                    <p class="text-slate-500 dark:text-slate-400 text-[11px] italic">ქართულად: "${escapeHtml(h.chosen.text_ka)}"</p>
                  </div>
                </div>
                <span class="text-2xl flex-shrink-0">🧑‍🎓</span>
              </div>
            `;
          }).join('')}

          <!-- Current Active Step (Partner prompt) -->
          ${(!isCompleted && sc.steps && sc.steps[state.roleplayStep]) ? (() => {
            const curStep = sc.steps[state.roleplayStep];
            const showTranslation = state.roleplayShowTranslations['cur_' + state.roleplayStep];
            return `
              <div class="flex items-start gap-3 max-w-[85%] md:max-w-[75%] animate-fadeIn">
                <span class="text-2xl flex-shrink-0">${sc.avatar || '🤵'}</span>
                <div class="space-y-1">
                  <span class="text-[11px] font-bold text-slate-400">${escapeHtml(sc.partner_name)}</span>
                  <div class="bg-white dark:bg-slate-800 border-2 border-purple-200 dark:border-purple-800/60 rounded-2xl rounded-tl-sm p-3.5 shadow-sm space-y-2">
                    <p class="text-sm font-bold text-slate-900 dark:text-white leading-relaxed">${escapeHtml(curStep.partner_de)}</p>
                    <div class="flex items-center gap-2 pt-1 border-t border-slate-100 dark:border-slate-700">
                      <button onclick="window.DeutschApp.speak('${curStep.partner_de.replace(/'/g, "\\'")}', this)" class="p-1.5 rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-purple-600 text-xs font-bold transition flex items-center gap-1" title="მოსმენა">
                        <span>🔊 მოუსმინე</span>
                      </button>
                      <button onclick="window.DeutschApp.toggleRoleplayTranslation('cur_${state.roleplayStep}')" class="px-2 py-1 rounded-lg text-xs font-bold text-purple-600 dark:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-950/40 transition">
                        💡 ${showTranslation ? 'თარგმანის დამალვა' : 'ქართულად'}
                      </button>
                    </div>
                    ${showTranslation ? `<p class="text-xs text-purple-800 dark:text-purple-300 italic pt-1">${escapeHtml(curStep.partner_ka)}</p>` : ''}
                  </div>
                </div>
              </div>
            `;
          })() : ''}

        </div>

        <!-- Reply / Completion Section -->
        ${!isCompleted && sc.steps && sc.steps[state.roleplayStep] ? (() => {
          const curStep = sc.steps[state.roleplayStep];
          return `
            <div class="space-y-3 pt-2 animate-fadeIn">
              <div class="flex items-center justify-between text-xs font-black text-slate-500">
                <span>💬 თქვენი ჯერია — აირჩიეთ საუკეთესო პასუხი (ნაბიჯი ${state.roleplayStep + 1}/${totalSteps}):</span>
                <span class="text-[11px] text-purple-600 dark:text-purple-400 font-bold">ყურადღება მიაქციეთ ეტიკეტსა და გრამატიკას</span>
              </div>
              <div class="space-y-2.5">
                ${curStep.options.map((opt, oIdx) => `
                  <div onclick="window.DeutschApp.chooseRoleplayOption(${oIdx})" class="w-full text-left p-4 rounded-2xl border-2 border-slate-200 dark:border-slate-700 hover:border-purple-500 dark:hover:border-purple-400 bg-white dark:bg-slate-800 hover:bg-purple-50/50 dark:hover:bg-purple-950/20 transition cursor-pointer group shadow-sm flex items-start justify-between gap-3 active:scale-[0.99]">
                    <div class="space-y-1 flex-1">
                      <p class="font-extrabold text-sm text-slate-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-300 transition">
                        ${escapeHtml(opt.text_de)}
                      </p>
                      <p class="text-xs text-slate-500 dark:text-slate-400">
                        ${escapeHtml(opt.text_ka)}
                      </p>
                    </div>
                    <button onclick="event.stopPropagation(); window.DeutschApp.speak('${opt.text_de.replace(/'/g, "\\'")}', this)" class="p-2 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-500 hover:text-purple-600 hover:bg-purple-100 text-xs font-bold transition flex-shrink-0" title="გამოთქმის მოსმენა">
                      🔊
                    </button>
                  </div>
                `).join('')}
              </div>
            </div>
          `;
        })() : ''}

        <!-- Completed Scenario Summary Card -->
        ${isCompleted ? (() => {
          const pct = Math.round((state.roleplayPoints / maxPoints) * 100);
          const stars = (pct >= 85) ? '⭐⭐⭐' : ((pct >= 60) ? '⭐⭐' : '⭐');
          const claimedKey = 'roleplay_' + sc.id;
          const claimed = (userData.claimedRewards && userData.claimedRewards[claimedKey]);
          return `
            <div class="space-y-5 p-6 rounded-3xl bg-gradient-to-br from-purple-50 via-indigo-50 to-white dark:from-slate-800 dark:via-slate-850 dark:to-slate-900 border border-purple-200 dark:border-purple-800 text-center animate-fadeIn">
              <div class="space-y-2">
                <span class="text-3xl">${stars}</span>
                <h3 class="text-xl font-black text-slate-900 dark:text-white">სასაუბრო სცენარი წარმატებით დასრულდა!</h3>
                <p class="text-xs text-slate-500 font-medium">თქვენ მიიღეთ <strong>${state.roleplayPoints}</strong> ქულა <strong>${maxPoints}</strong>-დან (${pct}%)</p>
              </div>

              <div class="inline-flex items-center gap-2 px-4 py-2 rounded-2xl ${pct >= 60 ? 'bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300' : 'bg-amber-100 text-amber-800'} text-xs font-black shadow-sm">
                <span>${pct >= 60 ? '✓ დიალოგი წარმატებით ჩაითვალა' : 'საჭიროებს გამეორებას'}</span>
                <span>•</span>
                <span>${claimed ? 'XP უკვე მიღებულია (+25 XP)' : '+25 XP დაგერიცხათ!'}</span>
              </div>

              <!-- Cultural Tip Card (Landeskunde) -->
              <div class="bg-white dark:bg-slate-800 p-5 rounded-2xl border border-amber-300/80 dark:border-amber-700/60 shadow-sm text-left space-y-2">
                <div class="flex items-center gap-2 text-xs font-black text-amber-700 dark:text-amber-400">
                  <span>🇩🇪</span>
                  <span>გერმანული ეტიკეტი და კულტურა (Landeskunde):</span>
                </div>
                <p class="text-xs md:text-sm text-slate-700 dark:text-slate-200 leading-relaxed">
                  ${escapeHtml(sc.cultural_tip)}
                </p>
              </div>

              <div class="flex flex-wrap items-center justify-center gap-3 pt-2">
                <button onclick="window.DeutschApp.restartRoleplayScenario()" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition">
                  🔄 სცენარის თავიდან გავლა
                </button>
                <button onclick="window.DeutschApp.switchRoleplayScenario(${(scIdx + 1) % scenarios.length})" class="px-6 py-2.5 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-xs font-black shadow-md transition">
                  შემდეგი სასაუბრო სცენარი →
                </button>
              </div>
            </div>
          `;
        })() : ''}

      </div>
    `;

    return html;
  }

  // --- 6. KURZGESCHICHTEN LAB (A1 MINI-STORIES & COMPREHENSION CHECK) ---
  function renderStoriesLab(stories) {
    if (!stories || stories.length === 0) {
      return `<p class="text-xs text-slate-500">ისტორიები არ მოიძებნა.</p>`;
    }

    let activeStory = stories.find(s => s.id === state.storyActiveId);
    if (!activeStory) {
      activeStory = stories[0];
      state.storyActiveId = activeStory.id;
    }

    const isMastered = (userData.completedStories || []).includes(activeStory.id);

    return `
      <div class="space-y-6 animate-fadeIn">
        <!-- Story Selection Pills -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
          ${stories.map((st, sIdx) => {
            const isCurrent = (st.id === state.storyActiveId);
            const done = (userData.completedStories || []).includes(st.id);
            return `
              <button onclick="window.DeutschApp.selectStory('${st.id}')" class="p-3.5 rounded-2xl border text-left transition ${isCurrent ? 'bg-indigo-600 text-white border-indigo-600 shadow-md' : 'bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 hover:border-indigo-400'}">
                <div class="flex items-center justify-between text-[10px] font-black uppercase mb-1">
                  <span>მოთხრობა ${sIdx + 1}</span>
                  ${done ? '<span class="text-emerald-400 font-extrabold">✓</span>' : ''}
                </div>
                <div class="text-xs font-black truncate">${escapeHtml(st.title_de)}</div>
                <div class="text-[10px] opacity-75 truncate">${escapeHtml(st.title_ka)}</div>
              </button>
            `;
          }).join('')}
        </div>

        <!-- Story Reader Card -->
        <div class="bg-gradient-to-r from-indigo-900 via-indigo-950 to-slate-900 rounded-3xl p-6 md:p-8 text-white shadow-lg space-y-4">
          <div class="flex items-center justify-between">
            <span class="px-3 py-1 bg-white/20 rounded-full text-xs font-black uppercase tracking-wider">
              CEFR A1 • ${escapeHtml(activeStory.level || 'A1')}
            </span>
            ${isMastered ? `
              <span class="px-3 py-1 bg-emerald-500/30 border border-emerald-400 text-emerald-300 rounded-xl text-xs font-black">
                ✓ ათვისებულია (+20 XP)
              </span>
            ` : ''}
          </div>
          <div>
            <h2 class="text-2xl md:text-3xl font-black">${escapeHtml(activeStory.title_de)}</h2>
            <p class="text-sm text-indigo-200 font-medium">${escapeHtml(activeStory.title_ka)}</p>
          </div>
          <div class="flex flex-wrap items-center gap-3 pt-3 border-t border-indigo-700/50">
            <span class="text-xs text-indigo-200 font-bold">სრული აუდიო:</span>
            <button onclick="window.DeutschApp.speak('${activeStory.audio_text.replace(/'/g, "\\'")}', this)" class="px-4 py-2 bg-indigo-500 hover:bg-indigo-400 rounded-xl text-xs font-black shadow flex items-center gap-1.5 transition">
              <span>🔊 1.0x მოუსმინე</span>
            </button>
            <button onclick="window.DeutschApp.speakSlow('${activeStory.audio_text.replace(/'/g, "\\'")}', this)" class="px-4 py-2 bg-white/10 hover:bg-white/20 rounded-xl text-xs font-bold transition">
              <span>🐢 0.7x ნელა</span>
            </button>
          </div>
        </div>

        <!-- Story Paragraphs with Translation and Vocabulary Toggles -->
        <div class="space-y-4">
          ${activeStory.paragraphs.map((p, pIdx) => {
            const showTrans = Boolean(state.storyShowTranslations[pIdx]);
            return `
              <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-5 shadow-sm space-y-3">
                <div class="flex items-start justify-between gap-4">
                  <p class="text-base font-bold text-slate-800 dark:text-slate-100 leading-relaxed">
                    ${escapeHtml(p.de)}
                  </p>
                  <div class="flex items-center gap-1.5 shrink-0">
                    <button onclick="window.DeutschApp.speak('${p.de.replace(/'/g, "\\'")}', this)" class="p-2 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-indigo-600 text-xs transition" title="1.0x მოსმენა">
                      🔊
                    </button>
                    <button onclick="window.DeutschApp.speakSlow('${p.de.replace(/'/g, "\\'")}', this)" class="p-2 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-indigo-600 text-xs transition" title="0.7x ნელა">
                      🐢
                    </button>
                    <button onclick="window.DeutschApp.toggleStoryTranslation(${pIdx})" class="px-2.5 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-xs font-extrabold hover:bg-slate-100 dark:hover:bg-slate-700 transition">
                      🇬🇪 ${showTrans ? 'დამალვა' : 'თარგმანი'}
                    </button>
                  </div>
                </div>

                ${showTrans ? `
                  <div class="p-3.5 bg-indigo-50/70 dark:bg-indigo-950/40 rounded-xl text-xs font-medium text-slate-700 dark:text-slate-300 border border-indigo-100 dark:border-indigo-900/40 animate-fadeIn">
                    ${escapeHtml(p.ka)}
                  </div>
                ` : ''}

                ${(p.glossary && p.glossary.length > 0) ? `
                  <div class="pt-2 border-t border-slate-100 dark:border-slate-700/60">
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block mb-1.5">საკვანძო ლექსიკა (Glossary):</span>
                    <div class="flex flex-wrap gap-1.5">
                      ${p.glossary.map(g => `
                        <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-700 dark:text-slate-200 text-xs font-semibold">
                          ${g.article ? `<strong class="text-indigo-600 dark:text-indigo-400">${escapeHtml(g.article)}</strong>` : ''}
                          <span>${escapeHtml(g.word)}:</span>
                          <span class="text-slate-500 dark:text-slate-400">${escapeHtml(g.ka)}</span>
                        </span>
                      `).join('')}
                    </div>
                  </div>
                ` : ''}
              </div>
            `;
          }).join('')}
        </div>

        <!-- Comprehension Check (გაგების შემოწმება) -->
        <div class="bg-white dark:bg-slate-800 border-2 border-indigo-100 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-6">
          <div class="flex items-center justify-between">
            <div>
              <span class="text-[10px] font-black uppercase tracking-wider text-indigo-600 dark:text-indigo-400 block">ტესტი გაგებაზე (Comprehension Check)</span>
              <h3 class="text-xl font-black text-slate-900 dark:text-white">შეამოწმეთ რამდენად კარგად გაიგეთ ისტორია</h3>
            </div>
            ${state.storySubmitted ? `
              <span class="text-xs font-black px-3 py-1 rounded-xl ${state.storyScore >= 2 ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-300' : 'bg-rose-100 text-rose-700 dark:bg-rose-950/50 dark:text-rose-300'}">
                შედეგი: ${state.storyScore} / ${activeStory.quiz.length}
              </span>
            ` : ''}
          </div>

          <div class="space-y-6">
            ${activeStory.quiz.map((q, qIdx) => {
              const userAns = state.storyAnswers[qIdx];
              const isSubmitted = state.storySubmitted;
              const isCorrect = (userAns === q.answer);

              return `
                <div class="p-4 rounded-2xl bg-slate-50 dark:bg-slate-900/40 border border-slate-200 dark:border-slate-700 space-y-3">
                  <div class="flex items-center justify-between text-xs font-black">
                    <span class="text-slate-500 uppercase">კითხვა ${qIdx + 1}</span>
                    ${isSubmitted ? (isCorrect ? '<span class="text-emerald-600 font-black">✓ სწორია</span>' : '<span class="text-rose-600 font-black">✗ არასწორია</span>') : ''}
                  </div>
                  <h4 class="text-sm font-black text-slate-800 dark:text-slate-100">${escapeHtml(q.question)}</h4>

                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                    ${q.options.map((opt, oIdx) => {
                      const isSelected = (userAns === oIdx);
                      let optClass = "p-3 rounded-xl text-xs font-bold text-left border transition ";
                      if (isSubmitted) {
                        if (oIdx === q.answer) {
                          optClass += "bg-emerald-100 dark:bg-emerald-950/60 border-emerald-500 text-emerald-800 dark:text-emerald-200 font-black";
                        } else if (isSelected) {
                          optClass += "bg-rose-100 dark:bg-rose-950/60 border-rose-500 text-rose-800 dark:text-rose-200";
                        } else {
                          optClass += "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 opacity-60";
                        }
                      } else {
                        if (isSelected) {
                          optClass += "bg-indigo-600 text-white border-indigo-600 shadow-sm";
                        } else {
                          optClass += "bg-white dark:bg-slate-800 border-slate-200 dark:border-slate-700 text-slate-800 dark:text-slate-200 hover:border-indigo-400";
                        }
                      }

                      return `
                        <button ${isSubmitted ? 'disabled' : `onclick="window.DeutschApp.selectStoryAnswer(${qIdx}, ${oIdx})"`} class="${optClass}">
                          ${escapeHtml(opt)}
                        </button>
                      `;
                    }).join('')}
                  </div>

                  ${isSubmitted ? `
                    <div class="p-2.5 rounded-xl bg-white dark:bg-slate-800 text-xs text-slate-600 dark:text-slate-300 font-medium border border-slate-200 dark:border-slate-700">
                      💡 <strong>განმარტება:</strong> ${escapeHtml(q.explanation)}
                    </div>
                  ` : ''}
                </div>
              `;
            }).join('')}
          </div>

          <div class="flex items-center justify-between pt-2 border-t border-slate-200 dark:border-slate-700">
            ${!state.storySubmitted ? `
              <button onclick="window.DeutschApp.submitStoryQuiz()" class="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-black rounded-xl shadow transition">
                შემოწმება ✓
              </button>
            ` : `
              <div class="flex items-center gap-3">
                <button onclick="window.DeutschApp.retryStoryQuiz()" class="px-4 py-2 border border-slate-300 dark:border-slate-600 text-slate-600 dark:text-slate-300 text-xs font-bold rounded-xl hover:bg-slate-100 transition">
                  🔄 თავიდან გავლა
                </button>
                <button onclick="window.DeutschApp.nextStory()" class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-black rounded-xl shadow transition">
                  შემდეგი ისტორია →
                </button>
              </div>
            `}
          </div>
        </div>
      </div>
    `;
  }

  // --- 7. HÖR-DIKTAT LAB (A1 AUDIO DICTATION WORKBENCH - 15 TASKS) ---
  function isDiktatInputCorrect(userInput, item) {
    if (!userInput || typeof userInput !== 'string') return false;
    const clean = s => String(s).trim().toLowerCase().replace(/[.!?]+$/, '').replace(/\s+/g, ' ');
    const userClean = clean(userInput);
    if (!userClean) return false;

    if (userClean === clean(item.expected)) return true;
    if (Array.isArray(item.accepted)) {
      for (const acc of item.accepted) {
        if (userClean === clean(acc)) return true;
      }
    }
    const userDecimal = userClean.replace(/,/g, '.');
    if (userDecimal === clean(item.expected).replace(/,/g, '.')) return true;
    if (Array.isArray(item.accepted)) {
      for (const acc of item.accepted) {
        if (userDecimal === clean(acc).replace(/,/g, '.')) return true;
      }
    }
    return false;
  }

  function renderDiktatLab(tasks) {
    if (!tasks || tasks.length === 0) {
      return `<p class="text-xs text-slate-500">აუდიო-კარნახის დავალებები არ მოიძებნა.</p>`;
    }

    const categories = [
      { key: 'all', label: 'ყველა (15)', icon: '🌟' },
      { key: 'buchstabieren', label: 'მართლწერა (4)', icon: '🔤' },
      { key: 'nummern', label: 'ნომრები (4)', icon: '🔢' },
      { key: 'uhrzeit', label: 'საათი (3)', icon: '⏰' },
      { key: 'preise', label: 'ფასები (2)', icon: '💶' },
      { key: 'saetze', label: 'წინადადებები (2)', icon: '💬' }
    ];

    const filter = state.labDiktatCategory || 'all';
    const filteredTasks = (filter === 'all')
      ? tasks
      : tasks.filter(t => t.category === filter);

    const safeTasks = filteredTasks.length > 0 ? filteredTasks : tasks;
    const currentIdx = state.labDiktatIndex % safeTasks.length;
    const item = safeTasks[currentIdx];

    const completedDiktatList = userData.completedDiktat || [];
    const isCompleted = completedDiktatList.includes(item.id);
    const completedCountInFilter = safeTasks.filter(t => completedDiktatList.includes(t.id)).length;

    // Evaluate correctness if submitted
    const isCorrect = state.labDiktatSubmitted && isDiktatInputCorrect(state.labDiktatUserInput, item);

    return `
      <div class="space-y-6 animate-fadeIn">
        <!-- Category Filter Pills -->
        <div class="flex flex-wrap gap-2">
          ${categories.map(c => `
            <button onclick="window.DeutschApp.switchDiktatCategory('${c.key}')" class="px-3.5 py-2 rounded-xl text-xs font-black transition flex items-center gap-1.5 ${filter === c.key ? 'bg-amber-500 text-slate-950 shadow-md' : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700 hover:border-amber-400'}">
              <span>${c.icon}</span>
              <span>${c.label}</span>
            </button>
          `).join('')}
        </div>

        <!-- Dictation Workbench Card -->
        <div class="bg-white dark:bg-slate-800 border-2 border-amber-200 dark:border-amber-900/40 rounded-3xl p-6 md:p-8 shadow-sm space-y-6">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-700/60 pb-4">
            <div class="flex items-center gap-2.5">
              <span class="px-3 py-1 rounded-full text-[11px] font-black uppercase tracking-wider bg-amber-100 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300">
                ${escapeHtml(item.category_ka || 'Hör-Diktat')}
              </span>
              <span class="text-xs font-bold text-slate-400">
                დავალება ${currentIdx + 1} / ${safeTasks.length}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-slate-500 dark:text-slate-400">
                ათვისებული: <strong class="text-amber-600 dark:text-amber-400">${completedCountInFilter} / ${safeTasks.length}</strong>
              </span>
              ${isCompleted ? `
                <span class="px-2.5 py-0.5 rounded-lg text-[10px] font-black bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300">
                  ✓ ჩათვლილია (+10 XP)
                </span>
              ` : ''}
            </div>
          </div>

          <div>
            <h3 class="text-xl md:text-2xl font-black text-slate-900 dark:text-white mb-1.5">${escapeHtml(item.title)}</h3>
            <p class="text-xs md:text-sm text-slate-600 dark:text-slate-300 font-medium">${escapeHtml(item.prompt_ka)}</p>
          </div>

          <!-- Audio Listening Section -->
          <div class="bg-gradient-to-r from-amber-500/10 via-amber-400/5 to-transparent border border-amber-300/40 dark:border-amber-800/40 rounded-2xl p-5 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <div class="w-12 h-12 rounded-xl bg-amber-500 text-slate-950 flex items-center justify-center text-2xl font-black shadow-md">
                🎧
              </div>
              <div>
                <p class="text-xs font-black text-slate-900 dark:text-white uppercase tracking-wider">Hör-Diktat (აუდიო-კარნახი) • Goethe A1 Hören</p>
                <p class="text-[11px] text-slate-500">მოუსმინეთ რამდენჯერაც გჭირდებათ ჩაწერამდე</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="window.DeutschApp.speak('${item.audio_text.replace(/'/g, "\\'")}', this)" class="px-4 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 rounded-xl text-xs font-black shadow transition flex items-center gap-1.5 active:scale-95">
                <span>🔊 1.0x მოუსმინე</span>
              </button>
              <button onclick="window.DeutschApp.speakSlow('${item.audio_text.replace(/'/g, "\\'")}', this)" class="px-4 py-2.5 bg-white dark:bg-slate-700 hover:bg-slate-100 dark:hover:bg-slate-600 text-slate-800 dark:text-slate-200 border border-slate-200 dark:border-slate-600 rounded-xl text-xs font-bold transition flex items-center gap-1.5 active:scale-95">
                <span>🐢 0.7x ნელა</span>
              </button>
            </div>
          </div>

          <!-- Input Workbench & Character Keyboard Chips -->
          <div class="space-y-3">
            <div class="flex items-center justify-between flex-wrap gap-2">
              <label for="diktat-input" class="text-xs font-black text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                ჩაწერეთ ტექსტი გერმანულად:
              </label>
              <div class="flex items-center gap-1">
                <span class="text-[10px] text-slate-400 font-bold mr-1">გერმანული ასოები:</span>
                ${['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü', '€'].map(ch => `
                  <button type="button" onclick="window.DeutschApp.insertDiktatChar('${ch}')" class="w-7 h-7 rounded-lg bg-slate-100 dark:bg-slate-700 hover:bg-amber-400 hover:text-slate-950 text-slate-800 dark:text-slate-200 font-mono font-black text-xs transition border border-slate-200 dark:border-slate-600">
                    ${ch}
                  </button>
                `).join('')}
              </div>
            </div>

            <div class="relative">
              <input
                id="diktat-input"
                type="text"
                autocomplete="off"
                spellcheck="false"
                ${state.labDiktatSubmitted ? 'disabled' : ''}
                value="${escapeHtml(state.labDiktatUserInput)}"
                oninput="window.DeutschApp.onDiktatInput(this.value)"
                onkeydown="if(event.key==='Enter') window.DeutschApp.submitDiktat()"
                placeholder="მაგ. ჩაწერეთ აქ მოსმენილი სიტყვა ან წინადადება..."
                class="w-full px-5 py-4 rounded-2xl border-2 text-base font-bold bg-white dark:bg-slate-900 text-slate-900 dark:text-white placeholder-slate-400 transition focus:outline-none focus:ring-2 ${state.labDiktatSubmitted ? (isCorrect ? 'border-emerald-500 bg-emerald-50/20' : 'border-rose-500 bg-rose-50/20') : 'border-slate-200 dark:border-slate-700 focus:border-amber-500 focus:ring-amber-400'}"
              />
              ${!state.labDiktatSubmitted && state.labDiktatUserInput ? `
                <button onclick="window.DeutschApp.clearDiktatInput()" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 text-xs font-bold p-1">
                  ✕
                </button>
              ` : ''}
            </div>
          </div>

          <!-- Feedback & Explanation (on submit) -->
          ${state.labDiktatSubmitted ? `
            <div class="p-5 rounded-2xl border space-y-3 animate-fadeIn ${isCorrect ? 'bg-emerald-50 dark:bg-emerald-950/40 border-emerald-300 dark:border-emerald-800 text-emerald-950 dark:text-emerald-100' : 'bg-rose-50 dark:bg-rose-950/40 border-rose-300 dark:border-rose-800 text-rose-950 dark:text-rose-100'}">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2">
                  <span class="text-xl">${isCorrect ? '🎉' : '⚠️'}</span>
                  <strong class="text-sm font-black">${isCorrect ? 'სწორია! შესანიშნავი მართლწერა და სმენა!' : 'ცოტა დაგაკლდათ. შეადარეთ ეტალონს:'}</strong>
                </div>
                ${isCorrect ? `<span class="px-2.5 py-0.5 rounded-lg text-xs font-black bg-emerald-200 dark:bg-emerald-800 text-emerald-900 dark:text-emerald-100">+10 XP</span>` : ''}
              </div>

              <div class="p-3 bg-white/70 dark:bg-slate-900/60 rounded-xl text-xs space-y-1 border border-black/5 dark:border-white/10">
                <div class="flex items-center gap-2">
                  <span class="text-slate-500 dark:text-slate-400">გერმანული ეტალონი:</span>
                  <strong class="font-mono text-slate-900 dark:text-white font-black text-sm">${escapeHtml(item.expected)}</strong>
                </div>
                ${item.hint ? `
                  <div class="text-[11px] text-slate-600 dark:text-slate-300">
                    💡 <strong>მინიშნება:</strong> ${escapeHtml(item.hint)}
                  </div>
                ` : ''}
                <div class="text-[11px] text-slate-600 dark:text-slate-300">
                  📚 <strong>წესი & განმარტება:</strong> ${escapeHtml(item.explanation)}
                </div>
              </div>
            </div>
          ` : ''}

          <!-- Action Buttons Bar -->
          <div class="flex flex-wrap items-center justify-between gap-3 pt-3 border-t border-slate-100 dark:border-slate-700/60">
            ${!state.labDiktatSubmitted ? `
              <button onclick="window.DeutschApp.submitDiktat()" class="px-6 py-3 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-black rounded-xl shadow-md transition active:scale-95 flex items-center gap-2">
                <span>🎯 შემოწმება</span>
              </button>
            ` : `
              <div class="flex flex-wrap items-center gap-2.5">
                ${!isCorrect ? `
                  <button onclick="window.DeutschApp.retryDiktat()" class="px-4 py-2.5 border border-slate-300 dark:border-slate-600 text-slate-700 dark:text-slate-300 text-xs font-black rounded-xl hover:bg-slate-100 dark:hover:bg-slate-700 transition">
                    🔄 თავიდან ცდა
                  </button>
                ` : ''}
                <button onclick="window.DeutschApp.nextDiktat()" class="px-6 py-2.5 bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-black rounded-xl shadow-md transition flex items-center gap-1.5 active:scale-95">
                  <span>შემდეგი დავალება →</span>
                </button>
              </div>
            `}

            <!-- Task direct selector numbers -->
            <div class="flex items-center gap-1 overflow-x-auto py-1 max-w-full">
              ${safeTasks.map((t, idx) => {
                const isCur = idx === currentIdx;
                const isDone = completedDiktatList.includes(t.id);
                return `
                  <button
                    onclick="window.DeutschApp.selectDiktatTask(${idx})"
                    class="w-7 h-7 rounded-lg text-[10px] font-black transition ${isCur ? 'bg-amber-500 text-slate-950 ring-2 ring-amber-400 ring-offset-1' : (isDone ? 'bg-emerald-100 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-300 border border-emerald-300 dark:border-emerald-800' : 'bg-slate-100 dark:bg-slate-800 text-slate-500 border border-slate-200 dark:border-slate-700')}"
                    title="${escapeHtml(t.title)}"
                  >
                    ${idx + 1}
                  </button>
                `;
              }).join('')}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  // ==========================================================================
  // TAB 7: GRAMMAR REFERENCE HANDBOOK
  // ==========================================================================
  function renderGrammarHandbook(container) {
    const tables = window.GERMAN_A1_DATA.grammar_tables || {};

    let html = `
      <div class="max-w-4xl mx-auto space-y-8 animate-fadeIn pb-16">
        <div class="text-center space-y-2">
          <span class="inline-block px-3 py-1 bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 rounded-full text-xs font-black tracking-wider uppercase">
            A1 გრამატიკული ცნობარი
          </span>
          <h1 class="text-3xl font-black text-slate-900 dark:text-white">გრამატიკის შემაჯამებელი ცხრილები</h1>
          <p class="text-xs text-slate-500">არტიკლები, პირის ნაცვალსახელები, მოდალური ზმნები და 35 უწესო ზმნის მე-3 ფორმა (Partizip II)</p>
        </div>

        <!-- 1. Articles Table -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span class="text-blue-600">📊</span> ${escapeHtml(tables.articles.title)}
          </h3>
          <div class="overflow-x-auto">
            <table class="grammar-table text-xs md:text-sm">
              <thead>
                <tr>
                  <th>ბრუნვა</th>
                  <th class="text-blue-600">Maskulin (der)</th>
                  <th class="text-rose-600">Feminin (die)</th>
                  <th class="text-emerald-600">Neutrum (das)</th>
                  <th class="text-purple-600">Plural (die)</th>
                </tr>
              </thead>
              <tbody>
                ${tables.articles.cases.map(c => `
                  <tr>
                    <td class="font-bold">${escapeHtml(c.case_de)}</td>
                    <td>${escapeHtml(c.maskulin)}</td>
                    <td>${escapeHtml(c.feminin)}</td>
                    <td>${escapeHtml(c.neutrum)}</td>
                    <td>${escapeHtml(c.plural)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- 2. Pronouns Table -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span class="text-indigo-600">👤</span> ${escapeHtml(tables.pronouns.title)}
          </h3>
          <div class="overflow-x-auto">
            <table class="grammar-table text-xs md:text-sm">
              <thead>
                <tr>
                  <th>პირი</th>
                  <th>Nominativ (ვინ?)</th>
                  <th>Akkusativ (ვის?)</th>
                  <th>Dativ (ვისთვის?)</th>
                </tr>
              </thead>
              <tbody>
                ${tables.pronouns.list.map(p => `
                  <tr>
                    <td class="font-bold">${escapeHtml(p.person)}</td>
                    <td class="font-extrabold text-blue-600">${escapeHtml(p.nom)}</td>
                    <td class="font-extrabold text-indigo-600">${escapeHtml(p.akk)}</td>
                    <td class="font-extrabold text-emerald-600">${escapeHtml(p.dat)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- 3. Modal Verbs Table -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span class="text-amber-500">⚙️</span> ${escapeHtml(tables.modal_verbs.title)}
          </h3>
          <div class="overflow-x-auto">
            <table class="grammar-table text-xs md:text-sm">
              <thead>
                <tr>
                  <th>ზმნა</th>
                  <th>ich / er,sie,es</th>
                  <th>du</th>
                  <th>wir / sie,Sie</th>
                  <th>ihr</th>
                </tr>
              </thead>
              <tbody>
                ${tables.modal_verbs.verbs.map(v => `
                  <tr>
                    <td class="font-black">${escapeHtml(v.verb)}</td>
                    <td class="font-bold text-blue-600">${escapeHtml(v.ich)}</td>
                    <td>${escapeHtml(v.du)}</td>
                    <td>${escapeHtml(v.wir)}</td>
                    <td>${escapeHtml(v.ihr)}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- 4. Irregular Verbs Table -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span class="text-rose-600">⚡</span> ${escapeHtml(tables.irregular_verbs.title)}
          </h3>
          <div class="overflow-x-auto">
            <table class="grammar-table text-xs">
              <thead>
                <tr>
                  <th>ინფინიტივი</th>
                  <th>Präsens (აწმყო)</th>
                  <th>Perfekt (Partizip II)</th>
                  <th>ქართული თარგმანი</th>
                  <th>აუდიო</th>
                </tr>
              </thead>
              <tbody>
                ${tables.irregular_verbs.list.map(v => `
                  <tr>
                    <td class="font-extrabold">${escapeHtml(v.inf)}</td>
                    <td class="text-slate-600 dark:text-slate-300">${escapeHtml(v.prasens)}</td>
                    <td class="font-extrabold text-blue-600 dark:text-blue-400">${escapeHtml(v.perfekt)}</td>
                    <td class="font-medium text-slate-600 dark:text-slate-300">${escapeHtml(v.georgian)}</td>
                    <td>
                      <button onclick="window.DeutschApp.speak('${v.perfekt}', this)" class="text-xs p-1 rounded hover:bg-slate-100">
                        🔊
                      </button>
                    </td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 8: A1 COMPREHENSIVE MULTI-SKILL EXAM (HÖREN, LESEN, SATZBAU, SCHREIBEN)
  // ==========================================================================
  function renderExam(container) {
    const questions = window.GERMAN_A1_DATA.final_exam_questions || [];

    if (state.examSubmitted || userData.examPassed) {
      renderExamResults(container);
      return;
    }

    const currentFilter = state.examFilterModule || 'all';
    const filteredQuestions = currentFilter === 'all'
      ? questions
      : questions.filter(q => q.module === currentFilter);

    const hoerenCount = questions.filter(q => q.module === 'hoeren').length;
    const lesenCount = questions.filter(q => q.module === 'lesen').length;
    const satzbauCount = questions.filter(q => q.module === 'satzbau').length;
    const schreibenCount = questions.filter(q => q.module === 'schreiben').length;

    const answeredCount = Object.keys(state.examUserAnswers).length;

    let html = `
      <div class="max-w-3xl mx-auto space-y-8 animate-fadeIn pb-16">
        <!-- Exam Hero Banner (Objective Assessment, No False Certificate Promises) -->
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-6 md:p-8 shadow-2xl relative overflow-hidden">
          <div class="flex items-center gap-2 mb-3">
            <span class="px-3 py-1 bg-yellow-400 text-slate-950 font-black rounded-full text-[10px] md:text-xs uppercase tracking-wider inline-block">
              CEFR A1 კომპლექსური საგამოცდო სისტემა
            </span>
            <span class="px-2.5 py-1 bg-blue-600/80 text-white font-bold rounded-full text-[10px] uppercase">
              ${answeredCount} / ${questions.length} შესრულებული
            </span>
          </div>
          <h1 class="text-2xl md:text-3xl font-black mb-3">A1 დონის შემაჯამებელი საგამოცდო ტესტი</h1>
          <p class="text-slate-300 text-xs md:text-sm leading-relaxed mb-4 font-normal">
            ტესტი მოიცავს 26 კომპლექსურ დავალებას 4 ძირითად კომპეტენციაში: <strong>Hören (მოსმენა)</strong>, <strong>Lesen & Grammatik (კითხვა და გრამატიკა)</strong>, <strong>Satzbau (სინტაქსი და სიტყვათწყობა)</strong> და <strong>Schreiben (წერა და ფორმულარები)</strong>.
            ჩასაბარებლად აუცილებელია მინიმუმ 60% (${Math.ceil(questions.length * 0.6)} სწორი პასუხი).
          </p>
          <div class="flex flex-wrap items-center gap-2 md:gap-4 text-xs text-yellow-300 font-bold">
            <span>⏱️ 4 მოდული (${questions.length} დავალება)</span> • <span>🎧 Hören (${hoerenCount}) • 📖 Lesen (${lesenCount}) • 🧩 Satzbau (${satzbauCount}) • ✍️ Schreiben (${schreibenCount})</span> • <span>🎯 გამსვლელი: 60%</span>
          </div>
        </div>

        <!-- Module Filter Tabs -->
        <div class="flex flex-wrap items-center gap-2 p-1.5 bg-slate-100 dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700">
          <button type="button" onclick="window.DeutschApp.setExamFilterModule('all')" class="px-3.5 py-2 rounded-xl text-xs font-black transition ${currentFilter === 'all' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'}">
            ყველა (${questions.length})
          </button>
          <button type="button" onclick="window.DeutschApp.setExamFilterModule('hoeren')" class="px-3.5 py-2 rounded-xl text-xs font-black transition ${currentFilter === 'hoeren' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'}">
            🎧 Hören (${hoerenCount})
          </button>
          <button type="button" onclick="window.DeutschApp.setExamFilterModule('lesen')" class="px-3.5 py-2 rounded-xl text-xs font-black transition ${currentFilter === 'lesen' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'}">
            📖 Lesen (${lesenCount})
          </button>
          <button type="button" onclick="window.DeutschApp.setExamFilterModule('satzbau')" class="px-3.5 py-2 rounded-xl text-xs font-black transition ${currentFilter === 'satzbau' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'}">
            🧩 Satzbau (${satzbauCount})
          </button>
          <button type="button" onclick="window.DeutschApp.setExamFilterModule('schreiben')" class="px-3.5 py-2 rounded-xl text-xs font-black transition ${currentFilter === 'schreiben' ? 'bg-blue-600 text-white shadow-sm' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900'}">
            ✍️ Schreiben (${schreibenCount})
          </button>
        </div>

        <form id="final-exam-form" onsubmit="event.preventDefault(); window.DeutschApp.submitExam();" class="space-y-6">
    `;

    filteredQuestions.forEach((q) => {
      const selected = state.examUserAnswers[q.id];
      const isAnswered = selected !== undefined && selected !== null;

      let moduleHeader = '';
      if (q.module === 'hoeren') {
        moduleHeader = `
          <div class="flex items-center justify-between text-xs font-bold text-blue-600 dark:text-blue-400 mb-2">
            <span class="flex items-center gap-1.5"><span class="text-sm">🎧</span> Modul 1: Hören (მოსმენა)</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-black ${isAnswered ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 dark:bg-slate-700 text-slate-500'}">
              ${isAnswered ? 'შევსებულია ✓' : 'პასუხგაუცემელი'}
            </span>
          </div>
          <div class="text-[11px] font-black text-slate-500 uppercase tracking-wider mb-2">
            📍 ${escapeHtml(q.scenario || 'საკომუნიკაციო სიტუაცია')}
          </div>
          <div class="flex flex-wrap items-center justify-between gap-2 p-3.5 bg-blue-50/70 dark:bg-slate-700/50 rounded-2xl border border-blue-200 dark:border-blue-900/50 mb-3">
            <div class="flex items-center gap-3">
              <button type="button" onclick="window.DeutschApp.speakGerman('${escapeHtml(q.audio_text || '')}')" class="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white font-black text-xs rounded-xl shadow-md transition flex items-center gap-2 active:scale-95">
                <span>🔊 მოუსმინე აუდიოს</span>
              </button>
              <span class="text-[11px] text-blue-900 dark:text-blue-200 font-bold">Standard Deutsch • გერმანული წარმოთქმა</span>
            </div>
            <button type="button" onclick="window.DeutschApp.toggleAudioTranscript(${q.id})" class="text-[11px] font-bold text-blue-600 dark:text-blue-400 hover:underline">
              👁️ ტრანსკრიპტი
            </button>
          </div>
          <div id="audio-transcript-${q.id}" class="hidden p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl text-xs text-slate-700 dark:text-slate-300 mb-3 font-mono">
            „${escapeHtml(q.audio_text || '')}“
          </div>
        `;
      } else if (q.module === 'lesen') {
        moduleHeader = `
          <div class="flex items-center justify-between text-xs font-bold text-emerald-600 dark:text-emerald-400 mb-2">
            <span class="flex items-center gap-1.5"><span class="text-sm">📖</span> Modul 2: Lesen & Grammatik (კითხვა და გრამატიკა)</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-black ${isAnswered ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 dark:bg-slate-700 text-slate-500'}">
              ${isAnswered ? 'შევსებულია ✓' : 'პასუხგაუცემელი'}
            </span>
          </div>
          <div class="text-[11px] font-black text-slate-500 uppercase tracking-wider mb-2">
            📄 ${escapeHtml(q.scenario || 'ტექსტის გაანალიზება')}
          </div>
          ${q.reading_text ? `
            <div class="p-4 bg-amber-50/70 dark:bg-slate-900/70 border border-amber-200 dark:border-amber-900/50 rounded-2xl text-xs text-slate-800 dark:text-slate-200 whitespace-pre-line mb-3 font-mono shadow-inner">
              ${escapeHtml(q.reading_text)}
            </div>
          ` : ''}
        `;
      } else if (q.module === 'satzbau') {
        moduleHeader = `
          <div class="flex items-center justify-between text-xs font-bold text-purple-600 dark:text-purple-400 mb-2">
            <span class="flex items-center gap-1.5"><span class="text-sm">🧩</span> Modul 3: Satzbau & Syntax (სინტაქსი და სიტყვათწყობა)</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-black ${isAnswered ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 dark:bg-slate-700 text-slate-500'}">
              ${isAnswered ? 'შევსებულია ✓' : 'პასუხგაუცემელი'}
            </span>
          </div>
          <div class="text-[11px] font-black text-purple-700 dark:text-purple-300 bg-purple-50 dark:bg-purple-950/40 p-2 rounded-xl mb-2.5 border border-purple-200 dark:border-purple-900/50">
            📌 წესი: ${escapeHtml(q.syntax_rule || 'გერმანული წინადადების სტრუქტურა')}
          </div>
        `;
      } else if (q.module === 'schreiben') {
        moduleHeader = `
          <div class="flex items-center justify-between text-xs font-bold text-rose-600 dark:text-rose-400 mb-2">
            <span class="flex items-center gap-1.5"><span class="text-sm">✍️</span> Modul 4: Schreiben (წერა და ფორმულარები)</span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-black ${isAnswered ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950 dark:text-emerald-300' : 'bg-slate-100 dark:bg-slate-700 text-slate-500'}">
              ${isAnswered ? 'შევსებულია ✓' : 'პასუხგაუცემელი'}
            </span>
          </div>
          <div class="text-[11px] font-black text-slate-500 uppercase tracking-wider mb-2">
            📝 ${escapeHtml(q.scenario || 'საგამოცდო წერის დავალება')}
          </div>
        `;
      }

      html += `
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 shadow-sm space-y-3.5">
          ${moduleHeader}
          <div class="flex items-center justify-between text-xs font-bold text-slate-400">
            <span>დავალება #${q.id} (საერთო: ${q.id} / ${questions.length})</span>
          </div>
          <h3 class="text-sm md:text-base font-black text-slate-900 dark:text-white leading-snug">
            ${escapeHtml(q.question)}
          </h3>
          <div class="grid grid-cols-1 gap-2.5 pt-1">
            ${q.options.map((opt, oIdx) => `
              <label class="flex items-center gap-3 p-3.5 rounded-2xl border border-slate-200 dark:border-slate-700 hover:bg-blue-50/50 dark:hover:bg-slate-700/30 cursor-pointer transition ${selected === oIdx ? 'bg-blue-50/70 dark:bg-slate-700/60 border-blue-500 dark:border-blue-500 ring-2 ring-blue-500/20' : ''}">
                <input type="radio" name="exam_q_${q.id}" value="${oIdx}" ${selected === oIdx ? 'checked' : ''} onchange="window.DeutschApp.onExamAnswer(${q.id}, ${oIdx})" class="w-4 h-4 text-blue-600 focus:ring-blue-500">
                <span class="text-xs md:text-sm font-medium text-slate-800 dark:text-slate-200">${escapeHtml(opt)}</span>
              </label>
            `).join('')}
          </div>
        </div>
      `;
    });

    // If viewing all or schreiben, render the interactive Writing Practice Workbench
    if (currentFilter === 'all' || currentFilter === 'schreiben') {
      html += `
        <!-- Interactive Writing Sandbox -->
        <div class="bg-gradient-to-br from-slate-900 to-indigo-950 text-white rounded-3xl p-6 md:p-8 space-y-6 shadow-xl border border-indigo-900/50">
          <div class="flex items-center gap-3">
            <span class="text-3xl">✍️</span>
            <div>
              <h3 class="text-lg font-black">A1 წერის პრაქტიკული სიმულატორი (Schreiben Labor)</h3>
              <p class="text-xs text-slate-300">ოფიციალური Goethe A1 Start Deutsch 1 სტილის ანკეტა და წერილის რედაქტორი</p>
            </div>
          </div>

          <!-- Teil 1: Anmeldeformular -->
          <div class="bg-white/5 border border-white/10 rounded-2xl p-5 space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-black uppercase tracking-wider text-amber-400">Teil 1: Anmeldeformular (სარეგისტრაციო ანკეტა)</span>
              <span class="text-[10px] text-slate-400 font-medium">სიტუაცია: Lukas Meier, Kantstraße 24, 10623 Berlin</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div>
                <label class="block text-slate-400 text-[10px] uppercase font-bold mb-1">Familienname (გვარი):</label>
                <input id="exam-form-nachname" type="text" placeholder="მაგ. Meier" class="w-full px-3 py-2 rounded-xl bg-white/10 border border-white/20 text-white placeholder-slate-500 font-bold focus:outline-none focus:border-amber-400">
              </div>
              <div>
                <label class="block text-slate-400 text-[10px] uppercase font-bold mb-1">Vorname (სახელი):</label>
                <input id="exam-form-vorname" type="text" placeholder="მაგ. Lukas" class="w-full px-3 py-2 rounded-xl bg-white/10 border border-white/20 text-white placeholder-slate-500 font-bold focus:outline-none focus:border-amber-400">
              </div>
              <div>
                <label class="block text-slate-400 text-[10px] uppercase font-bold mb-1">Wohnort (ქალაქი):</label>
                <input id="exam-form-stadt" type="text" placeholder="მაგ. Berlin" class="w-full px-3 py-2 rounded-xl bg-white/10 border border-white/20 text-white placeholder-slate-500 font-bold focus:outline-none focus:border-amber-400">
              </div>
              <div>
                <label class="block text-slate-400 text-[10px] uppercase font-bold mb-1">Postleitzahl / PLZ:</label>
                <input id="exam-form-plz" type="text" placeholder="მაგ. 10623" class="w-full px-3 py-2 rounded-xl bg-white/10 border border-white/20 text-white placeholder-slate-500 font-bold focus:outline-none focus:border-amber-400">
              </div>
              <div class="sm:col-span-2">
                <label class="block text-slate-400 text-[10px] uppercase font-bold mb-1">Beruf (პროფესია):</label>
                <input id="exam-form-beruf" type="text" placeholder="მაგ. Programmierer" class="w-full px-3 py-2 rounded-xl bg-white/10 border border-white/20 text-white placeholder-slate-500 font-bold focus:outline-none focus:border-amber-400">
              </div>
            </div>
            <div class="flex items-center justify-between pt-2">
              <button type="button" onclick="window.DeutschApp.checkExamFormular()" class="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs transition active:scale-95 shadow">
                ანკეტის გადამოწმება ✓
              </button>
              <div id="exam-form-feedback" class="text-xs font-bold text-slate-300"></div>
            </div>
          </div>

          <!-- Teil 2: Kurze Mitteilung (Email) -->
          <div class="bg-white/5 border border-white/10 rounded-2xl p-5 space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-xs font-black uppercase tracking-wider text-emerald-400">Teil 2: Kurze Nachricht (მოკლე წერილი მასწავლებელს)</span>
              <span id="exam-email-word-count" class="text-[10px] text-slate-400 font-medium">0 სიტყვა (რეკომენდებული: 20-30)</span>
            </div>
            <p class="text-xs text-slate-300 leading-relaxed">
              დაწერეთ ელ-ფოსტა ქალბატონ მიულერს (Frau Müller): აცნობეთ, რომ ავად ხართ (krank), ვერ მიდიხართ გაკვეთილზე, ითხოვეთ საშინაო დავალება (Hausaufgabe) და დაემშვიდობეთ თავაზიანად.
            </p>
            <textarea id="exam-email-input" rows="4" oninput="window.DeutschApp.updateExamEmailCount(this.value)" placeholder="Sehr geehrte Frau Müller, leider kann ich morgen nicht kommen..." class="w-full px-4 py-3 rounded-xl bg-white/10 border border-white/20 text-white placeholder-slate-500 font-mono text-xs focus:outline-none focus:border-emerald-400"></textarea>
            
            <div class="flex flex-wrap items-center justify-between gap-3 pt-1">
              <button type="button" onclick="window.DeutschApp.checkExamEmail()" class="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black text-xs transition active:scale-95 shadow">
                წერილის შეფასება (Rubrik) ✓
              </button>
              <div id="exam-email-feedback" class="text-xs font-bold text-slate-300"></div>
            </div>
          </div>
        </div>
      `;
    }

    html += `
          <div class="flex justify-center pt-4">
            <button type="submit" class="px-8 py-4 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-base shadow-xl shadow-emerald-600/25 transition active:scale-95">
              გამოცდის დასრულება და შეფასება 🚀
            </button>
          </div>
        </form>
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 8: FINAL EXAM & OFFICIAL CERTIFICATE SUITE (STAGE 10 PART 4)
  // ==========================================================================
  function getCertificateId() {
    const name = userData.learnerName || 'Student';
    const date = userData.examDate || '2026-01-01';
    const score = (userData.examScore !== null && userData.examScore !== undefined) ? userData.examScore : 25;
    let hash = 0;
    const str = name + '_' + date + '_' + score;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash |= 0;
    }
    const hex = Math.abs(hash).toString(16).toUpperCase().padStart(6, '0').slice(-6);
    return `DA1P-2026-${hex}`;
  }

  function renderCertificateHtml(options = {}) {
    const showInput = options.showInput !== false;
    const total = (window.GERMAN_A1_DATA.final_exam_questions || []).length || 25;
    const score = (userData.examScore !== null && userData.examScore !== undefined) ? userData.examScore : 25;
    const pct = Math.round((score / total) * 100);
    const issueDate = userData.examDate || new Date().toLocaleDateString('ka-GE');
    const certId = getCertificateId();
    
    let gradeDe = 'Bestanden (ჩაბარებული)';
    if (pct >= 90) gradeDe = 'Sehr gut (ფრიადი)';
    else if (pct >= 80) gradeDe = 'Gut (კარგი)';
    else if (pct >= 70) gradeDe = 'Befriedigend (დამაკმაყოფილებელი)';

    return `
      <div id="certificate-print-area" class="bg-white border-8 border-double border-slate-900 p-8 md:p-12 rounded-3xl text-center space-y-6 shadow-2xl text-slate-900 max-w-3xl mx-auto relative overflow-hidden">
        
        <!-- Header -->
        <div class="flex items-center justify-between border-b-2 border-slate-900 pb-4">
          <div class="flex items-center gap-2">
            <span class="text-3xl">🇩🇪</span>
            <span class="text-[11px] font-black uppercase tracking-widest text-slate-700">BUNDESREPUBLIK DEUTSCHLAND</span>
          </div>
          <div class="text-center">
            <span class="text-xs font-black tracking-widest uppercase text-blue-900 block">DEUTSCH A1 PRO</span>
            <span class="text-[9px] font-extrabold text-slate-500 uppercase tracking-widest">AKADEMISCHES SPRACHZERTIFIKAT</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-[11px] font-black uppercase tracking-widest text-slate-700">GEORGIEN</span>
            <span class="text-3xl">🇬🇪</span>
          </div>
        </div>

        <!-- Main Title -->
        <div class="space-y-1.5 pt-2">
          <span class="text-xs font-black uppercase tracking-widest text-blue-700">GEMEINSAMER EUROPÄISCHER REFERENZRAHMEN (GER / CEFR A1)</span>
          <h2 class="text-3xl md:text-4xl font-black tracking-tight text-slate-950 uppercase">ABSCHLUSSZERTIFIKAT</h2>
          <p class="text-sm font-bold text-slate-600">გერმანული ენის A1 დონის დამამთავრებელი სერტიფიკატი</p>
        </div>

        <!-- Recipient -->
        <div class="space-y-3 py-2">
          <p class="text-xs text-slate-500 uppercase tracking-wider font-bold">
            Dieser Leistungsnachweis wird offiziell verliehen an: / ეს სერტიფიკატი გადაეცემა:
          </p>

          ${showInput ? `
            <div class="max-w-md mx-auto no-print">
              <label class="text-[11px] font-bold text-slate-500 block mb-1">თქვენი სახელი და გვარი სერტიფიკატისთვის:</label>
              <input type="text" value="${escapeHtml(userData.learnerName || '')}" oninput="window.DeutschApp.updateLearnerName(this.value)" placeholder="ჩაწერეთ თქვენი სახელი და გვარი..." class="w-full text-center px-4 py-2 rounded-xl border border-slate-300 font-extrabold text-base text-blue-800 focus:outline-none focus:border-blue-600 bg-slate-50">
            </div>
          ` : ''}

          <div id="cert-learner-name-display" class="text-2xl md:text-3xl font-black border-b-2 border-slate-900 max-w-md mx-auto pb-1 text-blue-900 uppercase tracking-wide">
            ${escapeHtml(userData.learnerName || 'საქართველოს გერმანული ენის სტუდენტი')}
          </div>

          <p class="text-xs text-slate-600 max-w-lg mx-auto leading-relaxed">
            რომელმაც წარმატებით დაასრულა გერმანული ენის A1 დონის სრული საუნივერსიტეტო პროგრამა (10 თემატური გაკვეთილი, ლექსიკა, გრამატიკა, 7 ენობრივი ლაბორატორია) და დაადასტურა ცოდნა შემაჯამებელ გამოცდაზე.
          </p>
        </div>

        <!-- Competencies -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-left max-w-xl mx-auto p-3 bg-slate-50 rounded-2xl border border-slate-200 text-[11px]">
          <div class="space-y-0.5">
            <span class="font-black text-slate-900 block">🎧 Hörverstehen:</span>
            <span class="text-slate-500 text-[10px]">A1 აუდიო გაგება ✓</span>
          </div>
          <div class="space-y-0.5">
            <span class="font-black text-slate-900 block">📖 Leseverstehen:</span>
            <span class="text-slate-500 text-[10px]">A1 ტექსტის ანალიზი ✓</span>
          </div>
          <div class="space-y-0.5">
            <span class="font-black text-slate-900 block">✍️ Schreiben:</span>
            <span class="text-slate-500 text-[10px]">A1 წერილები & ფორმები ✓</span>
          </div>
          <div class="space-y-0.5">
            <span class="font-black text-slate-900 block">🗣️ Sprechen & Dialog:</span>
            <span class="text-slate-500 text-[10px]">A1 სასაუბრო კომუნიკაცია ✓</span>
          </div>
        </div>

        <!-- Results Table -->
        <div class="grid grid-cols-3 gap-4 max-w-xl mx-auto text-xs py-3 border-y-2 border-slate-900">
          <div>
            <span class="text-slate-500 block font-bold text-[10px] uppercase">საერთო შედეგი</span>
            <span class="font-black text-emerald-700 text-base">${pct}% (${score}/${total})</span>
          </div>
          <div>
            <span class="text-slate-500 block font-bold text-[10px] uppercase">აკადემიური შეფასება</span>
            <span class="font-black text-blue-900 text-sm md:text-base">${gradeDe}</span>
          </div>
          <div>
            <span class="text-slate-500 block font-bold text-[10px] uppercase">გაცემის თარიღი</span>
            <span class="font-black text-slate-900 text-sm md:text-base">${issueDate}</span>
          </div>
        </div>

        <!-- Signatures & Seal -->
        <div class="pt-4 flex items-center justify-between max-w-xl mx-auto text-[10px] text-slate-600">
          <div class="text-left space-y-1">
            <div class="w-28 border-b border-slate-800 font-serif italic text-xs text-slate-800">Prof. Dr. Weber</div>
            <span class="block font-black text-slate-800">სასწავლო ხელმძღვანელი</span>
            <span class="text-slate-400 text-[9px]">Akademische Leitung</span>
          </div>

          <div class="flex flex-col items-center">
            <div class="w-16 h-16 rounded-full border-2 border-amber-600/80 bg-amber-50 flex flex-col items-center justify-center p-1 shadow-sm text-center">
              <span class="text-xs">🏆</span>
              <span class="text-[7px] font-black uppercase text-amber-900 leading-tight">DEUTSCH A1 PRO</span>
              <span class="text-[6px] font-bold text-amber-700">VERIFIZIERT</span>
            </div>
            <span class="text-[8px] font-black text-slate-400 mt-1 uppercase tracking-widest">${certId}</span>
          </div>

          <div class="text-right space-y-1">
            <div class="w-28 border-b border-slate-800 font-serif italic text-xs text-slate-800 ml-auto">Dr. K. Schneider</div>
            <span class="block font-black text-slate-800">საგამოცდო კომისია</span>
            <span class="text-slate-400 text-[9px]">Prüfungskommission</span>
          </div>
        </div>

        <!-- Disclaimer -->
        <div class="pt-3 border-t border-slate-100 text-[9px] text-slate-400 max-w-lg mx-auto leading-normal">
          * ეს სერტიფიკატი ადასტურებს Deutsch A1 Pro პლატფორმის CEFR A1 სტანდარტის სრული კურსის და შემაჯამებელი გამოცდის წარმატებით ჩაბარებას (სერიული N: ${certId}).
        </div>
      </div>
    `;
  }

  function renderExamResults(container) {
    const questions = window.GERMAN_A1_DATA.final_exam_questions || [];
    const total = questions.length;
    const score = state.examSubmitted ? state.examScore : (userData.examScore || 0);
    const pct = Math.round((score / total) * 100);
    const passed = userData.examPassed || (pct >= 60);

    // Calculate module breakdown
    const modScores = {
      hoeren: { score: 0, total: 0, name: 'Hörverstehen (მოსმენა)', icon: '🎧' },
      lesen: { score: 0, total: 0, name: 'Lesen & Grammatik (კითხვა)', icon: '📖' },
      satzbau: { score: 0, total: 0, name: 'Satzbau & Syntax (სინტაქსი)', icon: '🧩' },
      schreiben: { score: 0, total: 0, name: 'Schreiben (წერა & ანკეტა)', icon: '✍️' }
    };

    questions.forEach(q => {
      const m = q.module || 'lesen';
      if (!modScores[m]) modScores[m] = { score: 0, total: 0, name: m, icon: '📝' };
      modScores[m].total += 1;
      if (state.examUserAnswers && state.examUserAnswers[q.id] === q.answer) {
        modScores[m].score += 1;
      }
    });

    let html = `
      <div class="max-w-3xl mx-auto space-y-8 animate-fadeIn pb-16">
        <!-- Hero Result Card -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-8 text-center space-y-5 shadow-lg">
          <div class="text-7xl">${passed ? '🏆' : '📝'}</div>
          <h1 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">
            ${passed ? 'გილოცავთ! თქვენ წარმატებით ჩააბარეთ A1 კომპლექსური გამოცდა!' : 'გამოცდა ვერ ჩაბარდა'}
          </h1>
          <div class="text-5xl font-black ${passed ? 'text-emerald-600' : 'text-rose-600'}">
            ${score} / ${total} (${pct}%)
          </div>
          <p class="text-xs md:text-sm text-slate-600 dark:text-slate-400 max-w-md mx-auto leading-relaxed">
            ${passed
              ? 'გილოცავთ! თქვენ წარმატებით დაადასტურეთ A1 დონის კომპეტენციები (Hören, Lesen, Satzbau, Schreiben). ქვემოთ მოცემულია თქვენი ოფიციალური საგამოცდო შეფასების უწყისი.'
              : 'სამწუხაროდ 60%-იანი ბარიერი ვერ გადაილახა. გირჩევთ კიდევ ერთხელ გაიმეოროთ გაკვეთილები და სცადოთ ხელახლა.'}
          </p>

          <!-- 4 Competencies Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-left pt-2">
            ${Object.keys(modScores).map(k => {
              const item = modScores[k];
              const mPct = item.total > 0 ? Math.round((item.score / item.total) * 100) : 0;
              return `
                <div class="p-3.5 bg-slate-50 dark:bg-slate-700/50 rounded-2xl border border-slate-200 dark:border-slate-600">
                  <div class="flex items-center gap-1.5 text-xs font-bold text-slate-500 mb-1">
                    <span>${item.icon}</span>
                    <span class="truncate">${item.name}</span>
                  </div>
                  <div class="text-lg font-black text-slate-900 dark:text-white">
                    ${item.score} / ${item.total}
                  </div>
                  <div class="text-[11px] font-bold ${mPct >= 60 ? 'text-emerald-600 dark:text-emerald-400' : 'text-rose-600 dark:text-rose-400'}">
                    ${mPct}% ${mPct >= 60 ? '✓' : '⚠️'}
                  </div>
                </div>
              `;
            }).join('')}
          </div>

          <div class="flex justify-center gap-3 pt-2">
            <button onclick="window.DeutschApp.retakeExam()" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 font-extrabold text-xs text-slate-700 dark:text-slate-300 hover:bg-slate-100 transition">
              🔄 ხელახლა ჩაბარება
            </button>
            ${passed ? `
              <button onclick="window.DeutschApp.printCertificate()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition flex items-center gap-2">
                <span>🖨️ შეფასების ბეჭდვა / PDF</span>
              </button>
            ` : ''}
          </div>
        </div>

        ${passed ? renderCertificateHtml({ showInput: true }) : ''}

        <!-- Question-by-Question Detailed Review -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <h3 class="text-base font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span>📝</span> დავალებების დეტალური ანალიზი და განმარტებები:
          </h3>
          <div class="space-y-4 text-xs">
            ${questions.map((q) => {
              const userAns = state.examUserAnswers ? state.examUserAnswers[q.id] : undefined;
              const isCorrect = userAns === q.answer;
              return `
                <div class="p-4 rounded-2xl border ${isCorrect ? 'border-emerald-200 dark:border-emerald-900/40 bg-emerald-50/30 dark:bg-emerald-950/20' : 'border-rose-200 dark:border-rose-900/40 bg-rose-50/30 dark:bg-rose-950/20'} space-y-2">
                  <div class="flex items-center justify-between font-bold">
                    <span class="text-slate-500">დავალება #${q.id} • ${q.module.toUpperCase()}</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-black ${isCorrect ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-900 dark:text-rose-300'}">
                      ${isCorrect ? 'სწორია ✓ (+1)' : 'შეცდომა ✕ (0)'}
                    </span>
                  </div>
                  <div class="font-extrabold text-slate-900 dark:text-white text-sm">
                    ${escapeHtml(q.question)}
                  </div>
                  <div class="space-y-1 pt-1">
                    <div class="${isCorrect ? 'text-emerald-700 dark:text-emerald-400 font-bold' : 'text-rose-600 dark:text-rose-400 font-bold'}">
                      თქვენი პასუხი: ${userAns !== undefined ? escapeHtml(q.options[userAns] || 'არ იყო არჩეული') : 'არ იყო არჩეული'}
                    </div>
                    ${!isCorrect ? `
                      <div class="text-emerald-700 dark:text-emerald-300 font-bold">
                        სწორი პასუხი: ${escapeHtml(q.options[q.answer])}
                      </div>
                    ` : ''}
                  </div>
                  ${q.explanation ? `
                    <div class="p-2.5 rounded-xl bg-blue-50/60 dark:bg-slate-700/40 border border-blue-100 dark:border-blue-900/30 text-slate-700 dark:text-slate-300 text-[11px] leading-relaxed">
                      💡 <strong>განმარტება:</strong> ${escapeHtml(q.explanation)}
                    </div>
                  ` : ''}
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Examination Attempt History -->
        ${(userData.examHistory && userData.examHistory.length) ? `
          <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 shadow-sm space-y-4">
            <h3 class="text-sm font-black text-slate-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
              <span>📊 საგამოცდო მცდელობების ისტორია:</span>
            </h3>
            <div class="divide-y divide-slate-100 dark:divide-slate-700 text-xs">
              ${userData.examHistory.slice().reverse().map(h => `
                <div class="py-2.5 flex items-center justify-between">
                  <span class="font-extrabold text-slate-700 dark:text-slate-200">მცდელობა #${h.attempt} • ${h.localDate || (h.date ? h.date.split('T')[0] : '')}</span>
                  <div class="flex items-center gap-3">
                    <span class="font-black text-slate-900 dark:text-white">${h.score} / ${h.total || total} (${h.pct}%)</span>
                    <span class="px-2 py-0.5 rounded text-[10px] font-black ${h.passed ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-rose-100 text-rose-800 dark:bg-rose-900/40 dark:text-rose-300'}">
                      ${h.passed ? 'ჩაბარებულია' : 'ვერ ჩაბარდა'}
                    </span>
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
        ` : ''}
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 9: PROFILE & PROGRESS (WITH SM-2 RETENTION STATS)
  // ==========================================================================
  function renderProfile(container) {
    const completedCount = (userData.completedLessons || []).length;
    const masteredCount = (userData.masteredWords || []).length;
    const mistakesCount = (userData.mistakeWords || []).length;
    const diktatCount = (userData.completedDiktat || []).length;

    const todayStr = getLocalDateString();
    const dailyGoal = userData.dailyXpGoal || 50;
    const dailyEarned = (userData.dailyXpDate === todayStr) ? (userData.dailyXpEarned || 0) : 0;
    const dailyPct = Math.min(100, Math.round((dailyEarned / Math.max(1, dailyGoal)) * 100));
    const freezesCount = typeof userData.streakFreezes === 'number' ? userData.streakFreezes : 1;
    const frozenDates = userData.streakFrozenDates || [];
    const weeklyHistory = userData.weeklyXpHistory || {};

    const last7Days = [];
    const kaWeekdays = ['კვ', 'ორ', 'სამ', 'ოთხ', 'ხუთ', 'პარ', 'შაბ'];
    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      const dStr = getLocalDateString(d);
      const dayXp = weeklyHistory[dStr] || (dStr === todayStr ? dailyEarned : 0);
      last7Days.push({
        dateStr: dStr,
        label: kaWeekdays[d.getDay()],
        xp: dayXp,
        isToday: i === 0,
        isFrozen: frozenDates.includes(dStr)
      });
    }
    const maxWeekXp = Math.max(dailyGoal, ...last7Days.map(x => x.xp), 1);

    let html = `
      <div class="max-w-4xl mx-auto space-y-8 animate-fadeIn pb-16">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-8 shadow-sm">
          <div class="flex items-center justify-between mb-6">
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-600 to-indigo-600 text-white text-2xl font-black flex items-center justify-center shadow-lg">
                GE
              </div>
              <div>
                <div class="flex items-center gap-2">
                  <h1 class="text-2xl font-black text-slate-900 dark:text-white">ჩემი სასწავლო პროფილი</h1>
                  <span class="px-2.5 py-0.5 text-[10px] font-black uppercase tracking-wider bg-amber-400 text-slate-950 rounded-md">
                    ${userData.isPro ? 'PRO ACTIVE ⭐' : 'BASIC'}
                  </span>
                </div>
                <p class="text-xs text-slate-500 font-medium">გერმანული A1 • სტატისტიკა, პროგრესი და SM-2 რეიტინგი</p>
              </div>
            </div>

            <button onclick="window.DeutschApp.openProModal()" class="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black text-xs shadow-md transition hover:scale-105 active:scale-95">
              💎 რეჟიმის მართვა
            </button>
          </div>

          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div class="p-4 rounded-2xl bg-blue-50 dark:bg-slate-700/40">
              <span class="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase block mb-1">სულ XP ქულა</span>
              <span class="text-2xl font-black text-slate-900 dark:text-white">${userData.xp || 0} ⭐</span>
            </div>
            <div class="p-4 rounded-2xl bg-amber-50 dark:bg-slate-700/40">
              <span class="text-xs font-bold text-amber-600 dark:text-amber-400 uppercase block mb-1">დღიური სერია</span>
              <span class="text-2xl font-black text-slate-900 dark:text-white">${userData.streak || 1} 🔥</span>
            </div>
            <div class="p-4 rounded-2xl bg-emerald-50 dark:bg-slate-700/40">
              <span class="text-xs font-bold text-emerald-600 dark:text-emerald-400 uppercase block mb-1">გავლილი მოდულები</span>
              <span class="text-2xl font-black text-slate-900 dark:text-white">${completedCount} / 10 📚</span>
            </div>
            <div class="p-4 rounded-2xl bg-purple-50 dark:bg-slate-700/40">
              <span class="text-xs font-bold text-purple-600 dark:text-purple-400 uppercase block mb-1">ნასწავლი სიტყვები</span>
              <span class="text-2xl font-black text-slate-900 dark:text-white">${masteredCount} / 734 🔤</span>
            </div>
          </div>
        </div>

        <!-- Weekly Goal & Streak Freeze System -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-6">
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 class="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
                <span>🎯</span> დღიური მიზანი, კვირის გრაფიკი & Streak Freeze
              </h2>
              <p class="text-xs text-slate-500">აირჩიეთ დღიური XP გეგმა და დაიცავით სერია გაყინვის ბარათებით</p>
            </div>
            <div class="flex items-center gap-1.5 bg-slate-100 dark:bg-slate-700/60 p-1 rounded-xl text-xs font-black">
              ${[20, 50, 100, 150].map(g => `
                <button onclick="window.DeutschApp.setDailyXpGoal(${g})" class="px-3 py-1.5 rounded-lg transition ${dailyGoal === g ? 'bg-blue-600 text-white shadow' : 'text-slate-600 dark:text-slate-300 hover:text-blue-600'}">
                  ${g} XP
                </button>
              `).join('')}
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
            <!-- Daily Progress & 7-Day Chart -->
            <div class="space-y-4">
              <div class="space-y-2">
                <div class="flex items-center justify-between text-xs font-black">
                  <span class="text-slate-700 dark:text-slate-300">დღევანდელი პროგრესი</span>
                  <span class="${dailyEarned >= dailyGoal ? 'text-emerald-600 dark:text-emerald-400' : 'text-blue-600 dark:text-blue-400'}">
                    ${dailyEarned} / ${dailyGoal} XP (${dailyPct}%) ${dailyEarned >= dailyGoal ? '✓' : ''}
                  </span>
                </div>
                <div class="w-full h-3 bg-slate-100 dark:bg-slate-700 rounded-full overflow-hidden">
                  <div class="h-full rounded-full transition-all duration-500 ${dailyEarned >= dailyGoal ? 'bg-emerald-500' : 'bg-blue-600'}" style="width: ${dailyPct}%"></div>
                </div>
              </div>

              <div class="pt-2">
                <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block mb-2">ბოლო 7 დღის აქტივობა:</span>
                <div class="grid grid-cols-7 gap-2 items-end h-20 pt-2">
                  ${last7Days.map(day => {
                    const barPct = Math.max(8, Math.round((day.xp / maxWeekXp) * 100));
                    return `
                      <div class="flex flex-col items-center gap-1 h-full justify-end" title="${day.dateStr}: ${day.xp} XP">
                        <div class="w-full max-w-[28px] rounded-t-lg transition-all ${day.isFrozen ? 'bg-cyan-400' : (day.xp >= dailyGoal ? 'bg-emerald-500' : (day.isToday ? 'bg-blue-600' : 'bg-slate-300 dark:bg-slate-600'))}" style="height: ${barPct}%"></div>
                        <span class="text-[10px] font-black ${day.isToday ? 'text-blue-600 dark:text-blue-400' : 'text-slate-400'}">
                          ${day.isFrozen ? '❄️' : day.label}
                        </span>
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>
            </div>

            <!-- Streak Freeze Card -->
            <div class="p-5 rounded-2xl bg-gradient-to-br from-cyan-50 to-blue-50 dark:from-cyan-950/30 dark:to-slate-900 border border-cyan-200 dark:border-cyan-800/40 space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center gap-2.5">
                  <span class="text-3xl">❄️</span>
                  <div>
                    <h3 class="text-sm font-black text-slate-900 dark:text-white">Streak Freeze (სერიის დაცვა)</h3>
                    <p class="text-[11px] text-slate-500 dark:text-slate-400">ავტომატურად იცავს სერიას 1 გამოტოვებული დღისგან</p>
                  </div>
                </div>
                <span class="px-3 py-1 rounded-xl bg-cyan-500/20 text-cyan-800 dark:text-cyan-300 font-black text-xs">
                  ${freezesCount} / 3
                </span>
              </div>

              <div class="flex items-center justify-between pt-2 border-t border-cyan-200/60 dark:border-cyan-800/30">
                <span class="text-[11px] font-bold text-slate-600 dark:text-slate-300">
                  ${freezesCount >= 3 ? 'მაქსიმალური მარაგი შევსებულია ✓' : 'შეიძინეთ დამატებითი დაცვა 50 XP-ით'}
                </span>
                <button onclick="window.DeutschApp.buyStreakFreeze()" ${freezesCount >= 3 || (userData.xp || 0) < 50 ? 'disabled' : ''} class="px-3.5 py-2 rounded-xl text-xs font-black transition ${freezesCount >= 3 || (userData.xp || 0) < 50 ? 'bg-slate-200 dark:bg-slate-700 text-slate-400 cursor-not-allowed' : 'bg-cyan-600 hover:bg-cyan-500 text-white shadow active:scale-95'}">
                  ❄️ დამატება (50 XP)
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Official Certificate Showcase in Profile (Stage 10 Part 4) -->
        ${userData.examPassed ? `
          <div class="bg-gradient-to-r from-blue-900 via-indigo-950 to-slate-900 rounded-3xl p-6 md:p-8 text-white space-y-4 shadow-xl animate-fadeIn">
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div class="flex items-center gap-3">
                <span class="text-4xl">🎓</span>
                <div>
                  <div class="flex items-center gap-2">
                    <h2 class="text-xl font-black">A1 დამამთავრებელი სერტიფიკატი</h2>
                    <span class="px-2 py-0.5 rounded-md text-[10px] font-black bg-emerald-500 text-slate-950">ჩაბარებულია ✓</span>
                  </div>
                  <p class="text-xs text-slate-300">CEFR A1 Abschlusszertifikat • სერიული N: ${getCertificateId()}</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="window.DeutschApp.openCertificateModal()" class="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-black text-xs shadow-md transition flex items-center gap-1.5 active:scale-95">
                  <span>📜 სერტიფიკატის ნახვა</span>
                </button>
                <button onclick="window.DeutschApp.printCertificate()" class="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-black text-xs border border-white/20 transition flex items-center gap-1.5 active:scale-95">
                  <span>🖨️ ბეჭდვა / PDF</span>
                </button>
              </div>
            </div>

            <div class="p-4 rounded-2xl bg-white/5 border border-white/10 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
              <div class="flex items-center gap-2">
                <span class="text-slate-400">სტუდენტი:</span>
                <strong class="text-white text-sm">${escapeHtml(userData.learnerName || 'საქართველოს გერმანული ენის სტუდენტი')}</strong>
              </div>
              <div class="flex items-center gap-3">
                <span class="text-slate-400">შედეგი: <strong class="text-emerald-400">${userData.examScore !== null ? Math.round((userData.examScore / ((window.GERMAN_A1_DATA.final_exam_questions || []).length || 26)) * 100) : 100}%</strong></span>
                <span class="text-slate-400">•</span>
                <span class="text-slate-400">თარიღი: <strong class="text-white">${userData.examDate || new Date().toLocaleDateString('ka-GE')}</strong></span>
              </div>
            </div>
          </div>
        ` : `
          <div class="bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 space-y-4">
            <div class="flex flex-wrap items-center justify-between gap-4">
              <div class="flex items-center gap-3">
                <span class="text-4xl opacity-50">🎓</span>
                <div>
                  <h2 class="text-lg font-black text-slate-900 dark:text-white">A1 შემაჯამებელი გამოცდა (დაბლოკილია / ჩასაბარებელია)</h2>
                  <p class="text-xs text-slate-500">გაიარეთ 4-მოდულიანი კომპლექსური გამოცდა: Hören, Lesen, Satzbau და Schreiben (გამსვლელი ბარიერი: 60%)</p>
                </div>
              </div>
              <button onclick="window.DeutschApp.setTab('exam')" class="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-black text-xs shadow-md transition flex items-center gap-1.5 active:scale-95">
                <span>🚀 გამოცდაზე გადასვლა</span>
              </button>
            </div>
          </div>
        `}

        <!-- Lessons Progress Breakdown -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <div class="flex items-center justify-between">
            <h2 class="text-lg font-black text-slate-900 dark:text-white">გაკვეთილების შეფასებები & პროგრესი</h2>
            ${mistakesCount > 0 ? `
              <button onclick="window.DeutschApp.trainMistakesFlashcards()" class="text-xs font-bold px-3 py-1 bg-rose-50 text-rose-700 rounded-xl border border-rose-200">
                ⚠️ ${mistakesCount} შეცდომის გამეორება
              </button>
            ` : ''}
          </div>

          <div class="space-y-3">
            ${window.GERMAN_A1_DATA.lessons.map(l => {
              const isComp = (userData.completedLessons || []).includes(l.id);
              const score = (userData.lessonScores || {})[l.id];
              return `
                <div class="flex items-center justify-between p-3.5 rounded-2xl border border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/20 transition">
                  <div class="flex items-center gap-3">
                    <span class="text-2xl p-2 bg-slate-50 dark:bg-slate-700 rounded-xl">${l.icon}</span>
                    <div>
                      <p class="font-extrabold text-xs md:text-sm text-slate-900 dark:text-white">${escapeHtml(l.title_ka)}</p>
                      <p class="text-[11px] text-slate-400 italic">${escapeHtml(l.title_de)}</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    ${isComp ? `
                      <span class="text-xs font-black text-emerald-600 bg-emerald-50 dark:bg-emerald-950/40 px-3 py-1 rounded-full">
                        ✓ ჩაბარებულია (${score || 100}%)
                      </span>
                    ` : `
                      <span class="text-xs font-bold text-slate-400 bg-slate-100 dark:bg-slate-700 px-3 py-1 rounded-full">
                        გასავლელია
                      </span>
                    `}
                    <button onclick="window.DeutschApp.openLesson(${l.id})" class="text-xs font-black text-blue-600 hover:underline">
                      გახსნა →
                    </button>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- Data Backup & Sync: JSON Export / Import -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
              <span class="text-3xl p-2.5 bg-blue-50 dark:bg-slate-700 rounded-2xl">💾</span>
              <div>
                <h2 class="text-lg font-black text-slate-900 dark:text-white">პროგრესის სარეზერვო ასლი (Backup & Sync)</h2>
                <p class="text-xs text-slate-500">ექსპორტი და იმპორტი JSON ფორმატში მოწყობილობებს შორის მონაცემების გადასატანად</p>
              </div>
            </div>
            <div class="flex flex-wrap items-center gap-2.5">
              <button onclick="window.DeutschApp.exportUserDataJSON()" class="px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-black text-xs shadow-md transition flex items-center gap-2 active:scale-95">
                <span>📥 ექსპორტი (JSON)</span>
              </button>
              <label class="px-4 py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 text-slate-800 dark:text-slate-200 font-black text-xs cursor-pointer shadow-sm transition flex items-center gap-2 active:scale-95">
                <span>📤 იმპორტი (JSON)</span>
                <input type="file" accept=".json" class="hidden" onchange="window.DeutschApp.importUserDataJSON(event)" />
              </label>
            </div>
          </div>
          <p class="text-[11px] text-slate-400">
            ინახავს: XP ქულებს, გავლილ გაკვეთილებს, SM-2 გამეორების ინტერვალებს, შეცდომების სიას, შენახულ სიტყვებს, კარნახებს (${diktatCount}/15), ესეების მონახაზებს და ჩაბარებულ სერტიფიკატს.
          </p>
        </div>

        <!-- Danger zone: Reset -->
        <div class="p-6 border border-rose-200 dark:border-rose-900/40 bg-rose-50/50 dark:bg-rose-950/20 rounded-3xl flex items-center justify-between">
          <div>
            <h3 class="text-xs md:text-sm font-black text-rose-800 dark:text-rose-300">მონაცემების გასუფთავება</h3>
            <p class="text-[11px] text-rose-600 dark:text-rose-400">თქვენი მთლიანი პროგრესი, ქულები და ტესტის შედეგები წაიშლება.</p>
          </div>
          <button onclick="window.DeutschApp.resetAllProgress()" class="px-4 py-2 rounded-xl bg-rose-600 hover:bg-rose-700 text-white font-extrabold text-xs shadow-sm transition active:scale-95">
            წაშლა 🗑️
          </button>
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // PRO SUBSCRIPTION MODAL (TRANSPARENT STUDY MODE - FIXES BIZ-01)
  // ==========================================================================
  function openProModal() {
    let container = document.getElementById('modal-container');
    if (!container) return;

    let html = `
      <div class="modal-overlay animate-fadeIn" onclick="if(event.target===this) window.DeutschApp.closeProModal()">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl max-w-2xl w-full p-6 md:p-8 shadow-2xl relative animate-popIn max-h-[90vh] overflow-y-auto">
          
          <button onclick="window.DeutschApp.closeProModal()" class="absolute top-5 right-5 text-slate-400 hover:text-slate-600 text-lg">✕</button>

          <div class="text-center space-y-2 mb-6">
            <span class="inline-block px-3 py-1 bg-amber-400 text-slate-950 rounded-full text-xs font-black tracking-wider uppercase">
              💎 Deutsch A1 Pro • სასწავლო & დემო რეჟიმი
            </span>
            <h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">
              სრული ფუნქციონალი აქტიურია
            </h2>
            <p class="text-xs text-slate-500 font-medium max-w-md mx-auto">
              ლოკალურ ვერსიაში ყველა პროფესიონალური ფუნქცია ხელმისაწვდომია უფასოდ სტუდენტებისთვის
            </p>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            
            <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-700 text-center flex flex-col justify-between">
              <div>
                <span class="text-xs font-bold text-slate-400 block mb-1">საბაზისო</span>
                <div class="text-xl font-black text-slate-900 dark:text-white mb-2">Starter</div>
                <ul class="text-[11px] text-slate-600 dark:text-slate-400 space-y-1.5 text-left mb-4">
                  <li>✓ 10 გაკვეთილის თეორია</li>
                  <li>✓ საბაზისო ტესტები</li>
                  <li>✓ Web Audio გაჟღერება</li>
                </ul>
              </div>
              <span class="text-[10px] text-slate-400 block font-bold">უფასო წვდომა</span>
            </div>

            <div class="p-4 rounded-2xl border-2 border-amber-400 bg-amber-50/40 dark:bg-amber-950/20 text-center flex flex-col justify-between relative pro-glow">
              <span class="absolute -top-3 left-1/2 -translate-x-1/2 px-2.5 py-0.5 bg-amber-400 text-slate-950 font-black text-[9px] uppercase rounded-full">
                აქტიური რეჟიმი
              </span>
              <div>
                <span class="text-xs font-black text-amber-700 dark:text-amber-300 block mb-1">PRO Study Mode</span>
                <div class="text-2xl font-black text-slate-900 dark:text-white mb-2">ყველაფერი ჩართულია</div>
                <ul class="text-[11px] text-slate-700 dark:text-slate-300 space-y-1.5 text-left mb-4 font-medium">
                  <li>✓ 734+ A1 ლექსიკონი</li>
                  <li>✓ 7 ენობრივი ლაბორატორია</li>
                  <li>✓ SM-2 ინტერვალური გამეორება</li>
                  <li>✓ der / die / das ტრენერი (431)</li>
                  <li>✓ Satzbau სინტაქსი</li>
                  <li>✓ A1 შემაჯამებელი გამოცდა (4 მოდული)</li>
                </ul>
              </div>
              <button onclick="window.DeutschApp.closeProModal()" class="w-full py-2 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black text-xs shadow-md transition active:scale-95">
                სწავლის გაგრძელება 🚀
              </button>
            </div>

            <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-700 text-center flex flex-col justify-between">
              <div>
                <span class="text-xs font-bold text-purple-600 block mb-1">Future A2</span>
                <div class="text-xl font-black text-slate-900 dark:text-white mb-2">მომავალი დონე</div>
                <ul class="text-[11px] text-slate-600 dark:text-slate-400 space-y-1.5 text-left mb-4">
                  <li>✓ A2.1 & A2.2 მოდულები</li>
                  <li>✓ გაფართოებული ლაბორატორიები</li>
                  <li>✓ გერმანული B1 მომზადება</li>
                </ul>
              </div>
              <span class="text-[10px] text-purple-600 font-bold">მომავალში</span>
            </div>

          </div>

          <div class="p-4 bg-slate-50 dark:bg-slate-700/30 rounded-2xl border border-slate-100 dark:border-slate-700 text-xs text-slate-600 dark:text-slate-300">
            <span class="font-bold text-slate-800 dark:text-slate-200 block mb-1">ℹ️ გამჭვირვალობის შენიშვნა:</span>
            <p>ეს არის ადგილობრივი (offline) სასწავლო პლატფორმა. აქ არ ხდება საბანკო ტრანზაქციების შესრულება — ყველა ხელსაწყო სრულიად ღიაა თქვენი განათლებისთვის.</p>
          </div>

        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  function closeProModal() {
    const container = document.getElementById('modal-container');
    if (container) container.innerHTML = '';
  }

  // --- Certificate Modal & Print Handlers (Stage 10 Part 4) ---
  function openCertificateModal() {
    let container = document.getElementById('modal-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'modal-container';
      document.body.appendChild(container);
    }

    const certHtml = renderCertificateHtml({ showInput: true, isModal: true });

    const html = `
      <div class="modal-overlay animate-fadeIn" onclick="if(event.target===this) window.DeutschApp.closeCertificateModal()">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl max-w-4xl w-full p-4 md:p-8 shadow-2xl relative animate-popIn max-h-[92vh] overflow-y-auto">
          
          <div class="flex items-center justify-between pb-4 border-b border-slate-200 dark:border-slate-700 mb-6 no-print">
            <div class="flex items-center gap-2">
              <span class="text-2xl">🎓</span>
              <div>
                <h3 class="font-black text-base md:text-lg text-slate-900 dark:text-white">A1 დამამთავრებელი სერტიფიკატი</h3>
                <p class="text-xs text-slate-500">ოფიციალური აკადემიური დოკუმენტი (CEFR A1)</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="window.DeutschApp.printCertificate()" class="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-black text-xs shadow-md transition flex items-center gap-1.5 active:scale-95">
                <span>🖨️ ბეჭდვა / PDF შენახვა</span>
              </button>
              <button onclick="window.DeutschApp.closeCertificateModal()" class="p-2 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-white text-base">✕</button>
            </div>
          </div>

          <div class="certificate-wrapper">
            ${certHtml}
          </div>
        </div>
      </div>
    `;

    container.innerHTML = html;
  }

  function closeCertificateModal() {
    const container = document.getElementById('modal-container');
    if (container) container.innerHTML = '';
  }

  function printCertificate() {
    if (!document.getElementById('certificate-print-area')) {
      openCertificateModal();
    }
    setTimeout(() => {
      window.print();
    }, 150);
  }

  // --- Public Interface for inline HTML events ---
  window.DeutschApp = {
    state,
    setTab,
    speak: speakGerman,
    recordSkillProgress,
    getLocalDateString,
    getCalendarDaysDiff,
    loadUserData,
    getCertificateId,
    openCertificateModal,
    closeCertificateModal,
    printCertificate,
    speakSlow: function (text, btn) {
      speakSlow(text, btn);
    },
    speakNormal: function (text, btn) {
      speakNormal(text, btn);
    },

    // Pro Modal
    openProModal,
    closeProModal,

    // Lessons
    openLesson: function (id) {
      state.selectedLessonId = id;
      setTab('lesson-detail');
    },
    switchLessonSubtab,
    toggleSequentialDialogue,
    trainLessonFlashcards: function (lessonId) {
      state.flashcardMode = 'normal';
      state.flashcardLessonFilter = String(lessonId);
      state.lessonVocabSession = {
        lessonId: Number(lessonId),
        ratings: {}, // wordId -> latestQuality (Stage 9.1: Latest-attempt policy per unique word)
        reviewedIds: [],
        correctCount: 0
      };
      setTab('flashcards');
    },
    trainMistakesFlashcards: function () {
      state.flashcardMode = 'normal';
      state.flashcardLessonFilter = 'mistakes';
      setTab('flashcards');
    },
    filterLessonVocab: function (lessonId, q) {
      const container = document.getElementById('lesson-vocab-grid');
      if (!container) return;
      const lessonVocab = window.GERMAN_A1_DATA.dictionary.filter(w => w.lesson_id === lessonId);
      const query = (q || '').toLowerCase().trim();

      const matched = lessonVocab.filter(w => {
        if (!query) return true;
        return (
          w.word.toLowerCase().includes(query) ||
          w.georgian.toLowerCase().includes(query) ||
          (w.example_de && w.example_de.toLowerCase().includes(query))
        );
      });

      let html = '';
      matched.forEach(w => {
        let badgeClass = 'bg-slate-100 text-slate-700';
        if (w.gender === 'm') badgeClass = 'badge-der';
        else if (w.gender === 'f') badgeClass = 'badge-die';
        else if (w.gender === 'n') badgeClass = 'badge-das';
        else if (w.gender === 'pl') badgeClass = 'badge-pl';

        html += `
          <div class="p-3.5 border border-slate-200 dark:border-slate-700 rounded-2xl bg-slate-50/50 dark:bg-slate-700/20 flex items-center justify-between gap-3 hover:border-blue-400 transition">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                ${w.article ? `<span class="text-[11px] font-black px-2 py-0.5 rounded-md ${badgeClass}">${escapeHtml(w.article)}</span>` : ''}
                <span class="font-extrabold text-sm text-slate-900 dark:text-white truncate">${escapeHtml(w.word)}</span>
                ${w.plural ? `<span class="text-[11px] text-slate-400 font-normal">(${escapeHtml(w.plural)})</span>` : ''}
              </div>
              <p class="text-xs font-medium text-slate-600 dark:text-slate-300 truncate">${escapeHtml(w.georgian)}</p>
            </div>
            <button onclick="window.DeutschApp.speak('${w.word.replace(/'/g, "\\'")}', this)" class="p-2 rounded-xl bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:text-blue-600 shadow-sm border border-slate-200 dark:border-slate-600 transition">
              🔊
            </button>
          </div>
        `;
      });
      container.innerHTML = html;
    },

    // Multi-Mode Exercise Hub Controls
    switchExerciseMode,
    onSelectMCAnswer: function (lessonId, idx) {
      if (state.mcSubmitted) return;
      state.mcSelectedAnswer = idx;
      renderExerciseConsole(lessonId);
    },
    submitMCAnswer: function (lessonId) {
      if (state.mcSelectedAnswer === null) return;
      state.mcSubmitted = true;
      const lesson = window.GERMAN_A1_DATA.lessons.find(l => l.id === lessonId);
      const q = lesson.exercises.multiple_choice[state.mcIndex];

      if (state.mcSelectedAnswer === q.answer) {
        state.mcScore += 1;
        playChime('success');
        grantRewardXP('mc_' + lessonId + '_' + (q.id || state.mcIndex), 10);
      } else {
        playChime('wrong');
      }
      renderExerciseConsole(lessonId);
    },
    nextMCQuestion: function (lessonId) {
      state.mcIndex += 1;
      state.mcSelectedAnswer = null;
      state.mcSubmitted = false;
      renderExerciseConsole(lessonId);
    },
    restartMC: function (lessonId) {
      state.mcIndex = 0;
      state.mcSelectedAnswer = null;
      state.mcSubmitted = false;
      state.mcScore = 0;
      renderExerciseConsole(lessonId);
    },

    onFIBInput: function (val) {
      state.fibUserInput = val;
    },
    appendGermanChar: function (char) {
      state.fibUserInput = (state.fibUserInput || '') + char;
      const inp = document.getElementById('fib-input');
      if (inp) {
        inp.value = state.fibUserInput;
        inp.focus();
      }
    },
    submitFIBAnswer: function (lessonId) {
      if (!state.fibUserInput.trim()) return;
      state.fibSubmitted = true;
      const lesson = window.GERMAN_A1_DATA.lessons.find(l => l.id === lessonId);
      const item = lesson.exercises.fill_in_blank[state.fibIndex];

      const cleanUser = state.fibUserInput.trim().toLowerCase();
      const cleanCorrect = item.correct_answer.trim().toLowerCase();

      state.fibIsCorrect = (cleanUser === cleanCorrect);

      if (state.fibIsCorrect) {
        state.fibScore += 1;
        playChime('success');
        grantRewardXP('fib_' + lessonId + '_' + (item.id || state.fibIndex), 10);
      } else {
        playChime('wrong');
      }
      renderExerciseConsole(lessonId);
    },
    nextFIBQuestion: function (lessonId) {
      state.fibIndex += 1;
      state.fibUserInput = '';
      state.fibSubmitted = false;
      state.fibIsCorrect = false;
      renderExerciseConsole(lessonId);
    },
    restartFIB: function (lessonId) {
      state.fibIndex = 0;
      state.fibUserInput = '';
      state.fibSubmitted = false;
      state.fibIsCorrect = false;
      state.fibScore = 0;
      renderExerciseConsole(lessonId);
    },

    playListeningAudio: function (text, btn) {
      speakGerman(text, btn);
      state.lisPlayCount += 1;
    },
    playListeningAudioSlow: function (text, btn) {
      const orig = state.speechRate;
      state.speechRate = 0.7;
      speakGerman(text, btn, () => {
        state.speechRate = orig;
      });
    },
    onSelectListeningAnswer: function (lessonId, idx) {
      if (state.lisSubmitted) return;
      state.lisSelectedAnswer = idx;
      renderExerciseConsole(lessonId);
    },
    submitListeningAnswer: function (lessonId) {
      if (state.lisSelectedAnswer === null) return;
      state.lisSubmitted = true;
      const lesson = window.GERMAN_A1_DATA.lessons.find(l => l.id === lessonId);
      const item = lesson.exercises.listening[state.lisIndex];

      if (state.lisSelectedAnswer === item.answer) {
        state.lisScore += 1;
        playChime('success');
        grantRewardXP('lis_' + lessonId + '_' + (item.id || state.lisIndex), 10);
      } else {
        playChime('wrong');
      }
      renderExerciseConsole(lessonId);
    },
    nextListeningQuestion: function (lessonId) {
      state.lisIndex += 1;
      state.lisSelectedAnswer = null;
      state.lisSubmitted = false;
      state.lisPlayCount = 0;
      renderExerciseConsole(lessonId);
    },
    restartListening: function (lessonId) {
      state.lisIndex = 0;
      state.lisSelectedAnswer = null;
      state.lisSubmitted = false;
      state.lisScore = 0;
      state.lisPlayCount = 0;
      renderExerciseConsole(lessonId);
    },

    // Lexicon
    onLexiconSearch: function (val) {
      state.lexiconSearch = val;
      renderLexicon(document.getElementById('main-content'));
    },
    clearLexiconSearch: function () {
      state.lexiconSearch = '';
      renderLexicon(document.getElementById('main-content'));
    },
    onLexiconCategory: function (cat) {
      state.lexiconCategory = cat;
      renderLexicon(document.getElementById('main-content'));
    },
    onLexiconGender: function (g) {
      state.lexiconGender = g;
      renderLexicon(document.getElementById('main-content'));
    },
    toggleFavorite: function (wordId) {
      userData.favoriteWords = userData.favoriteWords || [];
      const idx = userData.favoriteWords.indexOf(wordId);
      if (idx > -1) {
        userData.favoriteWords.splice(idx, 1);
        showToast('წაიშალა რჩეულებიდან');
      } else {
        userData.favoriteWords.push(wordId);
        showToast('დაემატა რჩეულებში ⭐');
      }
      saveUserData();
      if (state.currentTab === 'lexicon') {
        renderLexicon(document.getElementById('main-content'));
      }
    },
    trainFavoritesFlashcards: function () {
      const favs = userData.favoriteWords || [];
      if (favs.length === 0) {
        showToast('ჯერ მონიშნეთ სიტყვები ვარსკვლავით (⭐) ლექსიკონში');
        return;
      }
      state.flashcardLessonFilter = 'fav';
      state.flashcardMode = 'normal';
      initFlashcards();
      setTab('flashcards');
    },

    // Flashcards & SM-2
    onFlashcardLessonFilter: function (filterVal) {
      state.flashcardLessonFilter = filterVal;
      initFlashcards();
      renderFlashcards(document.getElementById('main-content'));
    },
    toggleFlashcardSRSMode: function () {
      state.flashcardMode = state.flashcardMode === 'srs' ? 'normal' : 'srs';
      initFlashcards();
      renderFlashcards(document.getElementById('main-content'));
      showToast(state.flashcardMode === 'srs' ? '🧠 SM-2 ინტერვალური გამეორება ჩაირთო' : 'ჩვეულებრივი რეჟიმი');
    },
    flipFlashcard: function () {
      state.flashcardFlipped = !state.flashcardFlipped;
      const el = document.getElementById('flashcard-inner-box');
      if (el) el.classList.toggle('is-flipped', state.flashcardFlipped);
    },
    flashcardSM2Action: function (quality) {
      const current = state.flashcardList[state.flashcardIndex];
      if (quality >= 3) {
        userData.masteredWords = userData.masteredWords || [];
        if (!userData.masteredWords.includes(current.id)) {
          userData.masteredWords.push(current.id);
          grantRewardXP('mastered_word_' + current.id, 5);
        }
      }
      updateSM2Item(current.id, quality);

      // Track active lesson vocabulary mastery session with Latest-Attempt Policy per Unique Word (Stage 9.1)
      if (state.lessonVocabSession && state.lessonVocabSession.lessonId) {
        const sess = state.lessonVocabSession;
        sess.ratings = sess.ratings || {};
        sess.ratings[current.id] = quality; // Latest rating for this unique word

        const uniqueWordIds = Object.keys(sess.ratings);
        const uniqueCount = uniqueWordIds.length;
        const uniqueCorrect = uniqueWordIds.filter(id => sess.ratings[id] >= 3).length;

        // Maintain backward compatibility for state inspection
        sess.reviewedIds = uniqueWordIds.map(Number);
        sess.correctCount = uniqueCorrect;

        const lessonWords = window.GERMAN_A1_DATA.dictionary.filter(w => w.lesson_id === sess.lessonId);
        // Scaled requirement reflecting deck size (Stage 9.1):
        // Minimum 8 words (or full deck if < 8), 20% of deck, capped at 25 words
        const minRequired = Math.min(lessonWords.length, Math.max(8, Math.min(25, Math.ceil(lessonWords.length * 0.2))));
        const accuracy = uniqueCount > 0 ? Math.round((uniqueCorrect / uniqueCount) * 100) : 0;

        if (uniqueCount >= minRequired && accuracy >= 70) {
          recordSkillProgress(sess.lessonId, 'vocab', accuracy, true);
          grantRewardXP('vocab_mastery_' + sess.lessonId, 20, 'ლექსიკის ბარათები ჩათვლილია (+20 XP)!');
        }
      }

      state.flashcardFlipped = false;
      state.flashcardIndex = (state.flashcardIndex + 1) % state.flashcardList.length;
      renderFlashcards(document.getElementById('main-content'));
    },

    // Article Trainer
    guessArticle: function (chosenArticle) {
      const word = state.trainerCurrentWord;
      const feedbackEl = document.getElementById('trainer-feedback');
      const cardEl = document.getElementById('trainer-card');

      if (chosenArticle === word.article) {
        state.trainerScore += 1;
        state.trainerStreak += 1;
        playChime('success');
        grantRewardXP('art_guess_' + word.word, 5);

        speakGerman(`${word.article} ${word.word}`);

        if (feedbackEl) {
          feedbackEl.innerHTML = `<span class="text-emerald-600 animate-fadeIn font-black text-base">✓ სწორია! ${word.article} ${word.word} (+5 XP)</span>`;
        }
        if (cardEl) {
          cardEl.classList.remove('border-slate-200', 'border-rose-500');
          cardEl.classList.add('border-emerald-500');
        }
      } else {
        state.trainerStreak = 0;
        playChime('wrong');
        if (feedbackEl) {
          feedbackEl.innerHTML = `<span class="text-rose-600 animate-fadeIn font-black text-base">✗ არასწორია! სწორია: <strong class="text-lg uppercase underline">${word.article}</strong> ${word.word}</span>`;
        }
        if (cardEl) {
          cardEl.classList.remove('border-slate-200', 'border-emerald-500');
          cardEl.classList.add('border-rose-500');
        }
      }

      setTimeout(() => {
        pickNextTrainerWord();
        renderArticleTrainer(document.getElementById('main-content'));
      }, 1200);
    },

    // Practice Trainers Hub Mode Switch
    setTrainerMode: function (mode) {
      state.trainerActiveMode = mode;
      renderArticleTrainer(document.getElementById('main-content'));
    },

    // Plural Trainer
    guessPlural: function (chosen) {
      const item = state.pluralCurrentWord;
      if (!item) return;
      const feedbackEl = document.getElementById('plural-feedback');

      if (chosen === item.plural) {
        state.pluralScore += 1;
        state.pluralStreak += 1;
        playChime('success');
        grantRewardXP('plural_' + item.word, 5);
        speakGerman(item.plural);
        state.pluralFeedback = `<span class="text-emerald-600 animate-fadeIn font-black text-sm">✓ სწორია! ${escapeHtml(item.plural)}<br><span class="text-xs font-normal text-slate-500">${escapeHtml(item.rule_explanation)}</span></span>`;
      } else {
        state.pluralStreak = 0;
        playChime('wrong');
        state.pluralFeedback = `<span class="text-rose-600 animate-fadeIn font-black text-sm">✗ არასწორია! სწორია: <strong class="underline">${escapeHtml(item.plural)}</strong><br><span class="text-xs font-normal text-slate-500">${escapeHtml(item.rule_explanation)}</span></span>`;
      }

      if (feedbackEl) feedbackEl.innerHTML = state.pluralFeedback;

      setTimeout(() => {
        pickNextPluralWord();
        renderArticleTrainer(document.getElementById('main-content'));
      }, 1600);
    },

    nextPluralWord: function () {
      pickNextPluralWord();
      renderArticleTrainer(document.getElementById('main-content'));
    },

    // Verb Conjugation Trainer
    guessVerb: function (chosen) {
      const drill = state.verbCurrentDrill;
      if (!drill) return;
      const feedbackEl = document.getElementById('verb-feedback');

      if (chosen === drill.correct) {
        state.verbScore += 1;
        state.verbStreak += 1;
        playChime('success');
        grantRewardXP('verb_' + drill.id, 5);
        const fullSentence = drill.sentence.replace('_______', drill.correct);
        speakGerman(fullSentence);
        state.verbFeedback = `<span class="text-emerald-600 animate-fadeIn font-black text-sm">✓ სწორია! „${escapeHtml(fullSentence)}“<br><span class="text-xs font-normal text-slate-500">${escapeHtml(drill.rule)}</span></span>`;
      } else {
        state.verbStreak = 0;
        playChime('wrong');
        state.verbFeedback = `<span class="text-rose-600 animate-fadeIn font-black text-sm">✗ არასწორია! სწორია: <strong class="underline">${escapeHtml(drill.correct)}</strong><br><span class="text-xs font-normal text-slate-500">${escapeHtml(drill.rule)}</span></span>`;
      }

      if (feedbackEl) feedbackEl.innerHTML = state.verbFeedback;

      setTimeout(() => {
        pickNextVerbDrill();
        renderArticleTrainer(document.getElementById('main-content'));
      }, 1600);
    },

    nextVerbDrill: function () {
      pickNextVerbDrill();
      renderArticleTrainer(document.getElementById('main-content'));
    },

    // Preposition & Case Trainer
    setCaseFilter: function (filterType) {
      state.caseFilterType = filterType;
      state.caseIndex = 0;
      pickNextCaseDrill();
      renderArticleTrainer(document.getElementById('main-content'));
    },

    guessCase: function (chosen) {
      const drill = state.caseCurrentDrill;
      if (!drill) return;
      const feedbackEl = document.getElementById('case-feedback');

      if (chosen === drill.correct) {
        state.caseScore += 1;
        state.caseStreak += 1;
        playChime('success');
        grantRewardXP('case_' + drill.id, 5);
        const fullSentence = drill.sentence.replace('_______', drill.correct);
        speakGerman(fullSentence);
        state.caseFeedback = `<span class="text-emerald-600 animate-fadeIn font-black text-sm">✓ სწორია! „${escapeHtml(fullSentence)}“<br><span class="text-xs font-normal text-slate-500">${escapeHtml(drill.rule_ka)}</span></span>`;
      } else {
        state.caseStreak = 0;
        playChime('wrong');
        state.caseFeedback = `<span class="text-rose-600 animate-fadeIn font-black text-sm">✗ არასწორია! სწორია: <strong class="underline">${escapeHtml(drill.correct)}</strong><br><span class="text-xs font-normal text-slate-500">${escapeHtml(drill.rule_ka)}</span></span>`;
      }

      if (feedbackEl) feedbackEl.innerHTML = state.caseFeedback;

      setTimeout(() => {
        pickNextCaseDrill();
        renderArticleTrainer(document.getElementById('main-content'));
      }, 1600);
    },

    nextCaseDrill: function () {
      pickNextCaseDrill();
      renderArticleTrainer(document.getElementById('main-content'));
    },

    // Trennbare Verben & Satzklammer Trainer
    setTrennbareFilter: function (filterType) {
      state.trennbarFilterType = filterType;
      state.trennbarIndex = 0;
      pickNextTrennbareDrill();
      renderArticleTrainer(document.getElementById('main-content'));
    },

    guessTrennbare: function (chosen) {
      const drill = state.trennbarCurrentDrill;
      if (!drill) return;
      const feedbackEl = document.getElementById('trennbar-feedback');

      if (chosen === drill.correct) {
        state.trennbarScore += 1;
        state.trennbarStreak += 1;
        playChime('success');
        grantRewardXP('trennbar_' + drill.id, 5);
        const fullSentence = drill.full_sentence || drill.sentence.replace('_______', drill.correct);
        speakGerman(fullSentence);
        state.trennbarFeedback = `<span class="text-emerald-600 animate-fadeIn font-black text-sm">✓ სწორია! „${escapeHtml(fullSentence)}“<br><span class="text-xs font-normal text-slate-500">${escapeHtml(drill.rule_ka)}</span></span>`;
      } else {
        state.trennbarStreak = 0;
        playChime('wrong');
        state.trennbarFeedback = `<span class="text-rose-600 animate-fadeIn font-black text-sm">✗ არასწორია! სწორია: <strong class="underline">${escapeHtml(drill.correct)}</strong><br><span class="text-xs font-normal text-slate-500">${escapeHtml(drill.rule_ka)}</span></span>`;
      }

      if (feedbackEl) feedbackEl.innerHTML = state.trennbarFeedback;

      setTimeout(() => {
        pickNextTrennbareDrill();
        renderArticleTrainer(document.getElementById('main-content'));
      }, 1600);
    },

    nextTrennbareDrill: function () {
      pickNextTrennbareDrill();
      renderArticleTrainer(document.getElementById('main-content'));
    },

    // Wort-Paare (Matching Game)
    onMatchCardClick: function (idx) {
      if (state.matchCompleted) return;
      if (state.matchFlipped.length >= 2) return;
      const card = state.matchCards[idx];
      if (!card || state.matchMatchedIds.includes(card.id)) return;
      if (state.matchFlipped.includes(idx)) return;

      state.matchFlipped.push(idx);
      renderArticleTrainer(document.getElementById('main-content'));

      if (state.matchFlipped.length === 2) {
        state.matchMoves += 1;
        const card1 = state.matchCards[state.matchFlipped[0]];
        const card2 = state.matchCards[state.matchFlipped[1]];

        if (card1.pairId === card2.pairId && card1.type !== card2.type) {
          playChime('success');
          state.matchMatchedIds.push(card1.id, card2.id);
          const deCard = (card1.type === 'de') ? card1 : card2;
          speakGerman(deCard.audio || deCard.text);
          state.matchFlipped = [];

          if (state.matchMatchedIds.length === state.matchCards.length) {
            state.matchCompleted = true;
            playChime('levelup');
            grantRewardXP('match_pairs_' + Date.now(), 15, 'წყვილების თამაში მოგებულია (+15 XP)!');
          }
          setTimeout(() => {
            renderArticleTrainer(document.getElementById('main-content'));
          }, 300);
        } else {
          playChime('wrong');
          setTimeout(() => {
            state.matchFlipped = [];
            renderArticleTrainer(document.getElementById('main-content'));
          }, 700);
        }
      }
    },

    resetMatchingGame: function () {
      initMatchingGame();
      renderArticleTrainer(document.getElementById('main-content'));
    },

    // Sentence Builder
    addSentenceWord: function (idx) {
      const word = state.sbAvailableWords.splice(idx, 1)[0];
      state.sbSelectedWords.push(word);
      renderSentenceBuilder(document.getElementById('main-content'));
    },
    removeSentenceWord: function (idx) {
      const word = state.sbSelectedWords.splice(idx, 1)[0];
      state.sbAvailableWords.push(word);
      renderSentenceBuilder(document.getElementById('main-content'));
    },
    resetSentence: function () {
      loadSentenceChallenge(state.sbIndex);
      renderSentenceBuilder(document.getElementById('main-content'));
    },
    checkSentence: function () {
      const challenge = window.GERMAN_A1_DATA.sentence_builders[state.sbIndex];
      const targetStr = challenge.words.join(' ');
      const userStr = state.sbSelectedWords.join(' ');

      state.sbChecked = true;
      state.sbIsCorrect = (targetStr === userStr);

      if (state.sbIsCorrect) {
        playChime('success');
        grantRewardXP('sb_' + (challenge.id || state.sbIndex), 15, 'წინადადება სრულიად სწორია!');
        speakGerman(userStr);
      } else {
        playChime('wrong');
        showToast('სცადეთ თავიდან!');
      }

      renderSentenceBuilder(document.getElementById('main-content'));
    },
    nextSentence: function () {
      loadSentenceChallenge(state.sbIndex + 1);
      renderSentenceBuilder(document.getElementById('main-content'));
    },

    // Language Labs Handlers (Stage 2)
    switchLabTab: function (tab) {
      state.labActiveTab = tab;
      renderLanguageLabs(document.getElementById('main-content'));
    },
    onSelectLabHoeren: function (idx) {
      if (state.labHoerenSubmitted) return;
      state.labHoerenSelectedAnswer = idx;
      renderLanguageLabs(document.getElementById('main-content'));
    },
    submitLabHoeren: function () {
      if (state.labHoerenSelectedAnswer === null) return;
      state.labHoerenSubmitted = true;
      const tasks = (window.GERMAN_A1_DATA.language_labs || {}).hoeren || [];
      const item = tasks[state.labHoerenIndex % tasks.length];
      if (state.labHoerenSelectedAnswer === item.answer) {
        state.labHoerenScore += 1;
        playChime('success');
        grantRewardXP('lab_hoeren_' + item.id, 15, 'მოსმენის გაგება: სწორია!');
      } else {
        playChime('wrong');
      }
      renderLanguageLabs(document.getElementById('main-content'));
    },
    nextLabHoeren: function (total) {
      state.labHoerenIndex = (state.labHoerenIndex + 1) % total;
      state.labHoerenSelectedAnswer = null;
      state.labHoerenSubmitted = false;
      renderLanguageLabs(document.getElementById('main-content'));
    },
    onSelectLabLesen: function (qIdx, oIdx) {
      if (state.labLesenSubmitted) return;
      state.labLesenAnswers[qIdx] = oIdx;
      renderLanguageLabs(document.getElementById('main-content'));
    },
    submitLabLesen: function () {
      const tasks = (window.GERMAN_A1_DATA.language_labs || {}).lesen || [];
      const item = tasks[state.labLesenIndex % tasks.length];
      if (!item) return;

      const totalQuestions = item.questions.length;
      const answeredCount = Object.keys(state.labLesenAnswers).length;

      if (answeredCount < totalQuestions) {
        showToast(`გთხოვთ უპასუხოთ ყველა (${totalQuestions}) კითხვას შემოწმებამდე. დარჩენილია ${totalQuestions - answeredCount}.`);
        return;
      }

      state.labLesenSubmitted = true;
      let correctCount = 0;
      item.questions.forEach((q, idx) => {
        if (state.labLesenAnswers[idx] === q.answer) {
          correctCount += 1;
        }
      });

      const pct = Math.round((correctCount / totalQuestions) * 100);
      const passed = (pct >= 66);

      userData.labScores = userData.labScores || {};
      userData.labScores.lesen = userData.labScores.lesen || {};
      userData.labScores.lesen[item.id] = {
        score: correctCount,
        total: totalQuestions,
        pct: pct,
        passed: passed,
        date: getLocalDateString()
      };

      if (passed) {
        playChime('success');
        grantRewardXP('lab_lesen_' + item.id, 15, `წაკითხულის გაგება: ${correctCount}/${totalQuestions} სწორია (${pct}%)!`);
      } else {
        playChime('wrong');
        showToast(`შედეგი: ${correctCount}/${totalQuestions} სწორია (${pct}%). გადახედეთ განმარტებებს და სცადეთ თავიდან.`);
        saveUserData();
      }

      renderLanguageLabs(document.getElementById('main-content'));
    },
    nextLabLesen: function (total) {
      state.labLesenIndex = (state.labLesenIndex + 1) % total;
      state.labLesenAnswers = {};
      state.labLesenSubmitted = false;
      renderLanguageLabs(document.getElementById('main-content'));
    },
    onSchreibenFormInput: function (fieldId, val) {
      state.labSchreibenFormInputs[fieldId] = val;
    },
    submitSchreibenForm: function () {
      const tasks = (window.GERMAN_A1_DATA.language_labs || {}).schreiben || [];
      const item = tasks[state.labSchreibenTaskIndex % tasks.length];
      if (!item || item.type !== 'form') return;

      const requiredFields = (item.fields || []).filter(f => f.required !== false);
      const missingFields = requiredFields.filter(f => !state.labSchreibenFormInputs[f.id] || !state.labSchreibenFormInputs[f.id].trim());

      if (missingFields.length > 0) {
        showToast(`გთხოვთ შეავსოთ ყველა სავალდებულო ველი ფორმაში (დარჩენილია ${missingFields.length})`);
        return;
      }

      state.labSchreibenFormSubmitted = true;
      userData.labScores = userData.labScores || {};
      userData.labScores.schreiben = userData.labScores.schreiben || {};
      userData.labScores.schreiben[item.id] = {
        completed: true,
        date: getLocalDateString()
      };

      grantRewardXP('lab_schreiben_' + item.id, 15, 'სასტუმროს სარეგისტრაციო ბარათი წარმატებით ჩაბარდა!');
      renderLanguageLabs(document.getElementById('main-content'));
    },
    submitSchreibenLetter: function () {
      const tasks = (window.GERMAN_A1_DATA.language_labs || {}).schreiben || [];
      const item = tasks[state.labSchreibenTaskIndex % tasks.length];
      if (!item) return;

      const minWords = item.min_words || 15;
      const wordsCount = (state.labSchreibenText.trim().match(/\S+/g) || []).length;

      if (wordsCount < minWords) {
        showToast(`გთხოვთ დაწეროთ მინიმუმ ${minWords} სიტყვა სანიმუშო პასუხის ნახვამდე (ამჟამად: ${wordsCount})`);
        return;
      }

      state.labSchreibenSubmittedTasks[item.id] = true;
      state.labSchreibenFormSubmitted = true;
      state.labSchreibenDrafts[item.id] = state.labSchreibenText;
      saveWritingDraft(item.id, state.labSchreibenText);

      showToast('წერილი გაიგზავნა! შეადარეთ ნიმუშს და შეავსეთ თვითშეფასების რუბრიკა.');
      renderLanguageLabs(document.getElementById('main-content'));
    },
    onToggleSchreibenRubric: function (taskId, rubricIdx) {
      state.labSchreibenRubricChecks[taskId] = state.labSchreibenRubricChecks[taskId] || {};
      state.labSchreibenRubricChecks[taskId][rubricIdx] = !state.labSchreibenRubricChecks[taskId][rubricIdx];
      renderLanguageLabs(document.getElementById('main-content'));
    },
    confirmSchreibenSelfReview: function (taskId) {
      const checks = state.labSchreibenRubricChecks[taskId] || {};
      const checkedCount = Object.values(checks).filter(Boolean).length;

      if (checkedCount < 3) {
        showToast('გთხოვთ მონიშნოთ მინიმუმ 3 რუბრიკის კრიტერიუმი თვითშეფასების დასადასტურებლად.');
        return;
      }

      userData.labScores = userData.labScores || {};
      userData.labScores.schreiben = userData.labScores.schreiben || {};
      const wordsCount = (state.labSchreibenText.trim().match(/\S+/g) || []).length;
      userData.labScores.schreiben[taskId] = {
        state: 'self_reviewed',
        wordsCount: wordsCount,
        checkedRubrics: checkedCount,
        completed: true,
        date: getLocalDateString()
      };

      grantRewardXP('lab_schreiben_' + taskId, 15, 'თვითშეფასება წარმატებით დასრულდა (+15 XP)!');
      renderLanguageLabs(document.getElementById('main-content'));
    },
    onSelectGrammarCheckOption: function (secId, optionIdx, lessonId) {
      if (state.lessonGrammarSubmitted[lessonId]) return;
      state.lessonGrammarAnswers[secId] = optionIdx;
      renderLessonDetail(document.getElementById('main-content'), lessonId);
    },
    submitGrammarCheck: function (lessonId) {
      const lesson = window.GERMAN_A1_DATA.lessons.find(l => l.id === lessonId);
      if (!lesson) return;

      const sections = lesson.grammar_sections || [];
      const sectionsWithChecks = sections.filter(s => s.check);
      const totalChecks = sectionsWithChecks.length;

      const answeredCount = sectionsWithChecks.filter(s => state.lessonGrammarAnswers[s.id] !== undefined).length;
      if (answeredCount < totalChecks) {
        showToast(`გთხოვთ უპასუხოთ ყველა (${totalChecks}) გრამატიკულ შეკითხვას შემოწმებამდე.`);
        return;
      }

      let correctCount = 0;
      sectionsWithChecks.forEach(s => {
        if (state.lessonGrammarAnswers[s.id] === s.check.answer) {
          correctCount += 1;
        }
      });

      const pct = Math.round((correctCount / totalChecks) * 100);
      const passed = pct >= 70;

      userData.grammarChecks = userData.grammarChecks || {};
      userData.grammarChecks[lessonId] = {
        passed: passed,
        score: pct,
        answers: { ...state.lessonGrammarAnswers },
        date: getLocalDateString()
      };

      recordSkillProgress(lessonId, 'grammar', pct, passed);

      if (passed) {
        state.lessonGrammarSubmitted[lessonId] = true;
        playChime('success');
        grantRewardXP('grammar_mastery_' + lessonId, 20, `თეორიის გაგება დადასტურებულია: ${correctCount}/${totalChecks} სწორია (${pct}%)!`);
      } else {
        state.lessonGrammarSubmitted[lessonId] = false;
        playChime('wrong');
        showToast(`შედეგი: ${correctCount}/${totalChecks} (${pct}%). გამსვლელი ზღვარია 70%. გადახედეთ წესებს და სცადეთ თავიდან.`);
        saveUserData();
      }

      renderLessonDetail(document.getElementById('main-content'), lessonId);
    },
    onSchreibenTextInput: function (val) {
      state.labSchreibenText = val;
      const tasks = (window.GERMAN_A1_DATA.language_labs || {}).schreiben || [];
      const item = tasks[state.labSchreibenTaskIndex % tasks.length];
      if (item && item.type !== 'form') {
        state.labSchreibenDrafts[item.id] = val;
        saveWritingDraft(item.id, val);
      }
      const wordsCount = (val.trim().match(/\S+/g) || []).length;
      const cntEl = document.querySelector('#schreiben-textarea + span strong');
      if (cntEl) cntEl.textContent = wordsCount;
    },
    appendSchreibenChar: function (char) {
      state.labSchreibenText = (state.labSchreibenText || '') + char;
      const ta = document.getElementById('schreiben-textarea');
      if (ta) {
        ta.value = state.labSchreibenText;
        ta.focus();
        window.DeutschApp.onSchreibenTextInput(ta.value);
      }
    },
    nextLabSchreiben: function (total) {
      const tasks = (window.GERMAN_A1_DATA.language_labs || {}).schreiben || [];
      const curItem = tasks[state.labSchreibenTaskIndex % tasks.length];
      if (curItem && curItem.type !== 'form' && state.labSchreibenText) {
        saveWritingDraft(curItem.id, state.labSchreibenText);
      }
      state.labSchreibenTaskIndex = (state.labSchreibenTaskIndex + 1) % total;
      const nextItem = tasks[state.labSchreibenTaskIndex % tasks.length];
      if (nextItem && nextItem.type !== 'form') {
        state.labSchreibenText = (userData.writingDrafts && userData.writingDrafts[nextItem.id]) || state.labSchreibenDrafts[nextItem.id] || '';
      } else {
        state.labSchreibenText = '';
      }
      state.labSchreibenFormInputs = {};
      state.labSchreibenFormSubmitted = false;
      renderLanguageLabs(document.getElementById('main-content'));
    },

    // MediaRecorder Audio Recording (Sprechen Lab)
    startVoiceRecording: async function () {
      try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          showToast('მიკროფონის მხარდაჭერა არ არის ბრაუზერში');
          return;
        }
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        state.recordedAudioChunks = [];
        
        let mrOptions = {};
        if (typeof MediaRecorder.isTypeSupported === 'function') {
          if (MediaRecorder.isTypeSupported('audio/webm;codecs=opus')) {
            mrOptions = { mimeType: 'audio/webm;codecs=opus' };
          } else if (MediaRecorder.isTypeSupported('audio/webm')) {
            mrOptions = { mimeType: 'audio/webm' };
          } else if (MediaRecorder.isTypeSupported('audio/mp4')) {
            mrOptions = { mimeType: 'audio/mp4' };
          }
        }
        
        state.mediaRecorder = new MediaRecorder(stream, mrOptions);
        state.mediaRecorder.ondataavailable = (e) => {
          if (e.data.size > 0) state.recordedAudioChunks.push(e.data);
        };
        state.mediaRecorder.onstop = () => {
          const recMime = (state.mediaRecorder && state.mediaRecorder.mimeType) ? state.mediaRecorder.mimeType : 'audio/webm';
          const blob = new Blob(state.recordedAudioChunks, { type: recMime });
          if (state.recordedAudioUrl) URL.revokeObjectURL(state.recordedAudioUrl);
          state.recordedAudioUrl = URL.createObjectURL(blob);
          renderLanguageLabs(document.getElementById('main-content'));
          playChime('success');
          grantRewardXP('lab_sprechen_rec', 10, 'ჩანაწერი შენახულია! შეგიძლიათ მოუსმინოთ 🎧');
        };
        state.mediaRecorder.start();
        state.isRecording = true;
        renderLanguageLabs(document.getElementById('main-content'));
      } catch (err) {
        console.error('Microphone access denied:', err);
        showToast('მიკროფონზე წვდომა უარყოფილია ან მიუწვდომელია');
      }
    },
    stopVoiceRecording: function () {
      if (state.mediaRecorder && state.isRecording) {
        state.mediaRecorder.stop();
        state.isRecording = false;
        state.mediaRecorder.stream.getTracks().forEach(t => t.stop());
      }
    },
    nextLabSprechen: function (total) {
      state.labSprechenPromptIndex = (state.labSprechenPromptIndex + 1) % total;
      state.isRecording = false;
      state.recordedAudioUrl = null;
      renderLanguageLabs(document.getElementById('main-content'));
    },

    // Speech AI & Live Pronunciation Evaluation (Stage 10)
    evaluatePronunciation: function (phraseId, targetPhrase) {
      const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
      if (!SpeechRec) {
        showToast('თქვენს ბრაუზერში ხმის ამოცნობა მიუწვდომელია. გთხოვთ გამოიყენოთ Chrome, Safari ან Edge.');
        return;
      }

      state.speechEvaluatingId = phraseId;
      state.isEvaluatingSpeech = true;
      renderLanguageLabs(document.getElementById('main-content'));

      try {
        const recognition = new SpeechRec();
        recognition.lang = 'de-DE';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;

        recognition.onresult = function (event) {
          state.isEvaluatingSpeech = false;
          const transcript = (event.results[0] && event.results[0][0]) ? event.results[0][0].transcript : '';

          const cleanTarget = targetPhrase.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?]/g, "").trim();
          const cleanSpoken = transcript.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()?]/g, "").trim();

          const targetWords = cleanTarget.split(/\s+/).filter(Boolean);
          const spokenWords = cleanSpoken.split(/\s+/).filter(Boolean);

          let matched = 0;
          const wordStatus = targetWords.map(tw => {
            const isMatch = spokenWords.includes(tw);
            if (isMatch) matched += 1;
            return { word: tw, matched: isMatch };
          });

          const score = targetWords.length > 0 ? Math.round((matched / targetWords.length) * 100) : 0;
          const passed = score >= 70;

          state.speechEvalResults[phraseId] = {
            score: score,
            transcript: transcript,
            wordStatus: wordStatus,
            passed: passed
          };

          if (passed) {
            playChime('success');
            grantRewardXP('speech_eval_' + phraseId, 10, `შესანიშნავი გამოთქმაა (${score}%)! +10 XP`);
          } else {
            playChime('wrong');
            showToast(`გამოთქმის შედეგი: ${score}%. მოუსმინეთ ეტალონს და სცადეთ თავიდან.`);
          }

          state.speechEvaluatingId = null;
          renderLanguageLabs(document.getElementById('main-content'));
        };

        recognition.onerror = function (event) {
          state.isEvaluatingSpeech = false;
          state.speechEvaluatingId = null;
          console.warn('Speech recognition event notice:', event.error);
          showToast(`ხმის ამოცნობის შეტყობინება: ${event.error}`);
          renderLanguageLabs(document.getElementById('main-content'));
        };

        recognition.onend = function () {
          if (state.isEvaluatingSpeech) {
            state.isEvaluatingSpeech = false;
            state.speechEvaluatingId = null;
            renderLanguageLabs(document.getElementById('main-content'));
          }
        };

        recognition.start();
      } catch (err) {
        state.isEvaluatingSpeech = false;
        state.speechEvaluatingId = null;
        console.error('Speech recognition initiation failed:', err);
        showToast('მიკროფონზე წვდომა ვერ განხორციელდა');
        renderLanguageLabs(document.getElementById('main-content'));
      }
    },

    // Daily SRS Launcher (Stage 10)
    startDailySRSReview: function () {
      const dueWords = getDueSRSWords();
      state.flashcardMode = 'srs';
      state.flashcardLessonFilter = 'all';
      state.flashcardList = dueWords.length > 0 ? dueWords : [...window.GERMAN_A1_DATA.dictionary].slice(0, 15);
      state.flashcardIndex = 0;
      state.flashcardFlipped = false;
      state.isDailySRSActive = true;
      state.dailySRSTotal = state.flashcardList.length;
      state.dailySRSCompleted = 0;
      setTab('flashcards');
      showToast(`🧠 დღიური გამეორების სესია გააქტიურდა (${state.flashcardList.length} სიტყვა)`);
    },

    // Roleplay Chat Simulator Handlers (Stage 10 Part 3)
    chooseRoleplayOption: function (optionIdx) {
      const scenarios = (window.GERMAN_A1_DATA && window.GERMAN_A1_DATA.language_labs && window.GERMAN_A1_DATA.language_labs.roleplay) || [];
      if (scenarios.length === 0) return;
      const sc = scenarios[state.labRoleplayIndex % scenarios.length];
      if (!sc || !sc.steps || state.roleplayCompleted || state.roleplayStep >= sc.steps.length) return;

      const curStep = sc.steps[state.roleplayStep];
      const opt = curStep.options[optionIdx];
      if (!opt) return;

      state.roleplayPoints += (opt.points || 0);
      state.roleplayHistory.push({
        stepIdx: state.roleplayStep,
        partner_de: curStep.partner_de,
        partner_ka: curStep.partner_ka,
        chosen: opt
      });

      state.roleplayStep += 1;

      if (state.roleplayStep >= sc.steps.length) {
        state.roleplayCompleted = true;
        const maxPoints = sc.steps.length * 10;
        const pct = Math.round((state.roleplayPoints / maxPoints) * 100);

        userData.labScores = userData.labScores || {};
        userData.labScores.roleplay = userData.labScores.roleplay || {};
        userData.labScores.roleplay[sc.id] = {
          completed: true,
          score: pct,
          points: state.roleplayPoints,
          maxPoints: maxPoints,
          date: getLocalDateString()
        };

        if (pct >= 60) {
          playChime('success');
          grantRewardXP('roleplay_' + sc.id, 25, `სასაუბრო სცენარი წარმატებით გაიარეთ (${pct}%)!`);
        } else {
          playChime('wrong');
          showToast(`სცენარი დასრულდა (${pct}%). სასურველია კიდევ ერთხელ გავლა.`);
        }
        saveUserData();
      } else {
        playChime('click');
        const nextStep = sc.steps[state.roleplayStep];
        if (nextStep && nextStep.partner_de) {
          speakGerman(nextStep.partner_de);
        }
      }

      renderLanguageLabs(document.getElementById('main-content'));
      setTimeout(() => {
        const chatBox = document.getElementById('roleplay-chat-stream');
        if (chatBox) chatBox.scrollTop = chatBox.scrollHeight;
      }, 50);
    },

    switchRoleplayScenario: function (scIdx) {
      const scenarios = (window.GERMAN_A1_DATA && window.GERMAN_A1_DATA.language_labs && window.GERMAN_A1_DATA.language_labs.roleplay) || [];
      if (scenarios.length === 0) return;
      state.labRoleplayIndex = scIdx % scenarios.length;
      state.roleplayStep = 0;
      state.roleplayHistory = [];
      state.roleplayPoints = 0;
      state.roleplayShowTranslations = {};
      state.roleplayCompleted = false;

      const sc = scenarios[state.labRoleplayIndex];
      if (sc && sc.steps && sc.steps[0] && sc.steps[0].partner_de) {
        speakGerman(sc.steps[0].partner_de);
      }
      renderLanguageLabs(document.getElementById('main-content'));
    },

    restartRoleplayScenario: function () {
      const scenarios = (window.GERMAN_A1_DATA && window.GERMAN_A1_DATA.language_labs && window.GERMAN_A1_DATA.language_labs.roleplay) || [];
      if (scenarios.length === 0) return;
      state.roleplayStep = 0;
      state.roleplayHistory = [];
      state.roleplayPoints = 0;
      state.roleplayShowTranslations = {};
      state.roleplayCompleted = false;

      const sc = scenarios[state.labRoleplayIndex % scenarios.length];
      if (sc && sc.steps && sc.steps[0] && sc.steps[0].partner_de) {
        speakGerman(sc.steps[0].partner_de);
      }
      renderLanguageLabs(document.getElementById('main-content'));
    },

    toggleRoleplayTranslation: function (key) {
      state.roleplayShowTranslations[key] = !state.roleplayShowTranslations[key];
      renderLanguageLabs(document.getElementById('main-content'));
    },

    // Mini-Stories Lab Handlers
    selectStory: function (id) {
      state.storyActiveId = id;
      state.storyAnswers = {};
      state.storySubmitted = false;
      state.storyScore = 0;
      state.storyShowTranslations = {};
      renderLanguageLabs(document.getElementById('main-content'));
    },
    selectStoryAnswer: function (qIdx, oIdx) {
      if (state.storySubmitted) return;
      state.storyAnswers[qIdx] = oIdx;
      renderLanguageLabs(document.getElementById('main-content'));
    },
    toggleStoryTranslation: function (pIdx) {
      state.storyShowTranslations[pIdx] = !state.storyShowTranslations[pIdx];
      renderLanguageLabs(document.getElementById('main-content'));
    },
    submitStoryQuiz: function () {
      const stories = window.GERMAN_A1_DATA.mini_stories || (window.GERMAN_A1_DATA.language_labs || {}).stories || [];
      const activeStory = stories.find(s => s.id === state.storyActiveId) || stories[0];
      if (!activeStory) return;

      const answered = Object.keys(state.storyAnswers).length;
      if (answered < activeStory.quiz.length) {
        showToast(`გთხოვთ უპასუხოთ ყველა (${activeStory.quiz.length}) შეკითხვას შემოწმებამდე.`);
        return;
      }

      let score = 0;
      activeStory.quiz.forEach((q, idx) => {
        if (state.storyAnswers[idx] === q.answer) {
          score += 1;
        }
      });

      state.storyScore = score;
      state.storySubmitted = true;

      userData.completedStories = userData.completedStories || [];
      if (!userData.completedStories.includes(activeStory.id) && score >= 2) {
        userData.completedStories.push(activeStory.id);
        grantRewardXP('story_' + activeStory.id, 20, `მოთხრობა #${activeStory.id} წარმატებით ათვისებულია (+20 XP)!`);
        playChime('fanfare');
      } else if (score >= 2) {
        playChime('success');
      } else {
        playChime('wrong');
      }

      saveUserData();
      renderLanguageLabs(document.getElementById('main-content'));
    },
    retryStoryQuiz: function () {
      state.storyAnswers = {};
      state.storySubmitted = false;
      state.storyScore = 0;
      renderLanguageLabs(document.getElementById('main-content'));
    },
    nextStory: function () {
      const stories = window.GERMAN_A1_DATA.mini_stories || (window.GERMAN_A1_DATA.language_labs || {}).stories || [];
      if (stories.length === 0) return;
      const curIdx = stories.findIndex(s => s.id === state.storyActiveId);
      const nextIdx = (curIdx >= 0 ? (curIdx + 1) % stories.length : 0);
      window.DeutschApp.selectStory(stories[nextIdx].id);
    },

    // Hör-Diktat Lab Handlers
    switchDiktatCategory: function (cat) {
      state.labDiktatCategory = cat;
      state.labDiktatIndex = 0;
      state.labDiktatUserInput = '';
      state.labDiktatSubmitted = false;
      renderLanguageLabs(document.getElementById('main-content'));
    },
    onDiktatInput: function (val) {
      state.labDiktatUserInput = val;
    },
    clearDiktatInput: function () {
      state.labDiktatUserInput = '';
      const el = document.getElementById('diktat-input');
      if (el) { el.value = ''; el.focus(); }
    },
    insertDiktatChar: function (ch) {
      const el = document.getElementById('diktat-input');
      if (el) {
        const start = el.selectionStart || el.value.length;
        const end = el.selectionEnd || el.value.length;
        const oldVal = el.value;
        const newVal = oldVal.substring(0, start) + ch + oldVal.substring(end);
        el.value = newVal;
        state.labDiktatUserInput = newVal;
        el.focus();
        const newPos = start + ch.length;
        try { el.setSelectionRange(newPos, newPos); } catch (e) {}
      } else {
        state.labDiktatUserInput = (state.labDiktatUserInput || '') + ch;
      }
    },
    submitDiktat: function () {
      if (state.labDiktatSubmitted) return;
      const tasks = window.GERMAN_A1_DATA.diktat || (window.GERMAN_A1_DATA.language_labs || {}).diktat || [];
      const filter = state.labDiktatCategory || 'all';
      const safeTasks = (filter === 'all') ? tasks : tasks.filter(t => t.category === filter);
      if (safeTasks.length === 0) return;
      const currentIdx = state.labDiktatIndex % safeTasks.length;
      const item = safeTasks[currentIdx];

      state.labDiktatSubmitted = true;
      const isCorrect = isDiktatInputCorrect(state.labDiktatUserInput, item);

      userData.completedDiktat = userData.completedDiktat || [];
      if (isCorrect) {
        playChime('success');
        if (!userData.completedDiktat.includes(item.id)) {
          userData.completedDiktat.push(item.id);
          grantRewardXP('diktat_' + item.id, 10, 'კარნახი წარმატებით ჩაბარდა (+10 XP)! 🎙️');
        }
      } else {
        playChime('wrong');
      }
      saveUserData();
      renderLanguageLabs(document.getElementById('main-content'));
    },
    retryDiktat: function () {
      state.labDiktatSubmitted = false;
      renderLanguageLabs(document.getElementById('main-content'));
      const el = document.getElementById('diktat-input');
      if (el) { el.focus(); el.select(); }
    },
    nextDiktat: function () {
      const tasks = window.GERMAN_A1_DATA.diktat || (window.GERMAN_A1_DATA.language_labs || {}).diktat || [];
      const filter = state.labDiktatCategory || 'all';
      const safeTasks = (filter === 'all') ? tasks : tasks.filter(t => t.category === filter);
      if (safeTasks.length === 0) return;

      state.labDiktatIndex = (state.labDiktatIndex + 1) % safeTasks.length;
      state.labDiktatUserInput = '';
      state.labDiktatSubmitted = false;
      renderLanguageLabs(document.getElementById('main-content'));
      const el = document.getElementById('diktat-input');
      if (el) el.focus();
    },
    selectDiktatTask: function (idx) {
      state.labDiktatIndex = idx;
      state.labDiktatUserInput = '';
      state.labDiktatSubmitted = false;
      renderLanguageLabs(document.getElementById('main-content'));
      const el = document.getElementById('diktat-input');
      if (el) el.focus();
    },

    // Learner Name Update for Certificate (Stage 10)
    updateLearnerName: function (name) {
      userData.learnerName = name;
      saveUserData();
      const el = document.getElementById('cert-learner-name-display');
      if (el) el.textContent = name || 'საქართველოს გერმანული ენის სტუდენტი';
    },

    // Exam Handlers (Stage 10 Multi-Skill CEFR A1 Examination)
    onExamAnswer: function (qId, ansIdx) {
      state.examUserAnswers[qId] = ansIdx;
    },
    setExamFilterModule: function (mod) {
      state.examFilterModule = mod;
      renderExam(document.getElementById('main-content'));
    },
    toggleAudioTranscript: function (qId) {
      const el = document.getElementById('audio-transcript-' + qId);
      if (el) el.classList.toggle('hidden');
    },
    checkExamFormular: function () {
      const nachname = (document.getElementById('exam-form-nachname') ? document.getElementById('exam-form-nachname').value : '').trim().toLowerCase();
      const vorname = (document.getElementById('exam-form-vorname') ? document.getElementById('exam-form-vorname').value : '').trim().toLowerCase();
      const stadt = (document.getElementById('exam-form-stadt') ? document.getElementById('exam-form-stadt').value : '').trim().toLowerCase();
      const plz = (document.getElementById('exam-form-plz') ? document.getElementById('exam-form-plz').value : '').trim();
      const beruf = (document.getElementById('exam-form-beruf') ? document.getElementById('exam-form-beruf').value : '').trim().toLowerCase();

      const feedback = document.getElementById('exam-form-feedback');
      if (!nachname || !vorname || !stadt || !plz || !beruf) {
        if (feedback) feedback.innerHTML = '<span class="text-amber-400">⚠️ გთხოვთ შეავსოთ ყველა ველი.</span>';
        return;
      }

      let correct = 0;
      if (nachname === 'meier') correct++;
      if (vorname === 'lukas') correct++;
      if (stadt === 'berlin') correct++;
      if (plz === '10623') correct++;
      if (beruf.indexOf('programm') !== -1) correct++;

      if (feedback) {
        if (correct === 5) {
          feedback.innerHTML = '<span class="text-emerald-400">✓ შესანიშნავია! ყველა ველი (5/5) სწორად არის შევსებული!</span>';
        } else {
          feedback.innerHTML = `<span class="text-amber-400">⚠️ სწორია: ${correct}/5 ველი. გადაამოწმეთ ქალაქი, ინდექსი და სახელები.</span>`;
        }
      }
    },
    updateExamEmailCount: function (text) {
      const words = (text || '').trim().split(/\s+/).filter(Boolean);
      const counter = document.getElementById('exam-email-word-count');
      if (counter) counter.textContent = `${words.length} სიტყვა (რეკომენდებული: 20-30)`;
    },
    checkExamEmail: function () {
      const text = (document.getElementById('exam-email-input') ? document.getElementById('exam-email-input').value : '').toLowerCase();
      const feedback = document.getElementById('exam-email-feedback');
      if (!text || text.length < 10) {
        if (feedback) feedback.innerHTML = '<span class="text-amber-400">⚠️ გთხოვთ დაწეროთ წერილი შეფასებამდე.</span>';
        return;
      }

      const hasAnrede = (text.indexOf('sehr geehrte') !== -1 || text.indexOf('liebe frau müller') !== -1 || text.indexOf('guten tag') !== -1);
      const hasGrund = (text.indexOf('krank') !== -1 || text.indexOf('kann nicht') !== -1 || text.indexOf('nicht kommen') !== -1);
      const hasAufgabe = (text.indexOf('hausaufgabe') !== -1 || text.indexOf('aufgabe') !== -1 || text.indexOf('schicken') !== -1 || text.indexOf('woche') !== -1);
      const hasGruss = (text.indexOf('mit freundlichen grüßen') !== -1 || text.indexOf('viele grüße') !== -1 || text.indexOf('herzliche grüße') !== -1 || text.indexOf('grüße') !== -1);

      let score = 0;
      if (hasAnrede) score++;
      if (hasGrund) score++;
      if (hasAufgabe) score++;
      if (hasGruss) score++;

      if (feedback) {
        if (score >= 3) {
          feedback.innerHTML = `<span class="text-emerald-400">✓ რუბრიკა: ${score}/4 პუნქტი დაკმაყოფილებულია! A1 სტანდარტი მიღწეულია.</span>`;
        } else {
          feedback.innerHTML = `<span class="text-amber-400">⚠️ რუბრიკა: ${score}/4 პუნქტი. დაამატეთ თავაზიანი მიმართვა, მიზეზი (krank) ან დამშვიდობება.</span>`;
        }
      }
    },
    submitExam: function () {
      const questions = window.GERMAN_A1_DATA.final_exam_questions || [];
      const total = questions.length;
      const answeredCount = Object.keys(state.examUserAnswers).length;

      if (answeredCount < total) {
        showToast(`გთხოვთ უპასუხოთ ყველა (${total}) კითხვას გამოცდის დასრულებამდე. დარჩენილია ${total - answeredCount}.`);
        return;
      }

      let score = 0;
      const modules = {
        hoeren: { score: 0, total: 0 },
        lesen: { score: 0, total: 0 },
        satzbau: { score: 0, total: 0 },
        schreiben: { score: 0, total: 0 }
      };

      questions.forEach(q => {
        const modKey = q.module || 'lesen';
        if (!modules[modKey]) modules[modKey] = { score: 0, total: 0 };
        modules[modKey].total += 1;

        if (state.examUserAnswers[q.id] === q.answer) {
          score += 1;
          modules[modKey].score += 1;
        }
      });

      const pct = Math.round((score / total) * 100);
      const passed = (pct >= 60);

      state.examScore = score;
      state.examSubmitted = true;
      state.examModuleBreakdown = modules;

      userData.examHistory = userData.examHistory || [];
      const attemptRecord = {
        attempt: userData.examHistory.length + 1,
        date: new Date().toISOString(),
        localDate: getLocalDateString(),
        score: score,
        total: total,
        pct: pct,
        passed: passed,
        modules: modules
      };
      userData.examHistory.push(attemptRecord);
      userData.examScore = score;
      userData.examPassed = passed;
      userData.examDate = attemptRecord.date;

      if (passed) {
        playChime('fanfare');
        grantRewardXP('exam_first_passing_score', 100, `A1 კომპლექსური გამოცდა წარმატებით ჩაბარდა (${score}/${total}, ${pct}%)!`);
      } else {
        playChime('wrong');
        showToast(`გამოცდა არ ჩაითვალა: ${score}/${total} (${pct}%). მინიმალური ზღვარია 60%.`);
        saveUserData();
      }

      renderExamResults(document.getElementById('main-content'));
      window.scrollTo({ top: 0, behavior: 'smooth' });
    },
    retakeExam: function () {
      state.examSubmitted = false;
      state.examUserAnswers = {};
      state.examScore = 0;
      state.examFilterModule = 'all';
      state.examModuleBreakdown = null;
      renderExam(document.getElementById('main-content'));
    },

    // Profile JSON Backup & Sync (Data Export / Import)
    exportUserDataJSON: function () {
      const jsonStr = JSON.stringify(userData, null, 2);
      try {
        if (typeof Blob !== 'undefined' && typeof document !== 'undefined') {
          const blob = new Blob([jsonStr], { type: 'application/json' });
          const url = (typeof URL !== 'undefined' && URL.createObjectURL) ? URL.createObjectURL(blob) : null;
          if (url) {
            const a = document.createElement('a');
            const dateStr = new Date().toISOString().slice(0, 10);
            a.href = url;
            a.download = `deutsch_a1_backup_${dateStr}.json`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(() => {
              try { URL.revokeObjectURL(url); } catch (e) {}
            }, 1000);
          }
        }
      } catch (err) {
        console.warn('Backup export download fallback:', err);
      }
      showToast('პროგრესის სარეზერვო ასლი ჩამოტვირთულია (JSON) 💾');
      return jsonStr;
    },
    importUserDataJSON: function (event) {
      const file = event && event.target && event.target.files && event.target.files[0];
      if (!file) return;

      if (typeof FileReader === 'undefined') {
        alert('FileReader მხარდაჭერილი არ არის ამ ბრაუზერში.');
        return;
      }

      const reader = new FileReader();
      reader.onload = function (evt) {
        try {
          const raw = evt.target.result;
          const parsed = JSON.parse(raw);
          if (!parsed || typeof parsed !== 'object') {
            alert('არასწორი JSON მონაცემები. გთხოვთ ატვირთოთ ვალიდური ფაილი.');
            return;
          }
          localStorage.setItem(STORAGE_KEY, JSON.stringify(parsed));
          userData = loadUserData();
          showToast('პროგრესი წარმატებით აღდგა სარეზერვო ასლიდან! 🎉');
          setTab('profile');
        } catch (err) {
          alert('შეცდომა სარეზერვო ფაილის წაკითხვისას: ' + err.message);
        }
      };
      reader.readAsText(file);
    },

    // Weekly Goal & Streak Freeze Handlers
    setDailyXpGoal: function (goal) {
      if (![20, 50, 100, 150].includes(goal)) return;
      userData.dailyXpGoal = goal;
      saveUserData();
      showToast(`დღიური მიზანი განახლდა: ${goal} XP/დღეში 🎯`);
      if (state.currentTab === 'profile') {
        renderProfile(document.getElementById('main-content'));
      }
    },

    buyStreakFreeze: function () {
      const currentFreezes = typeof userData.streakFreezes === 'number' ? userData.streakFreezes : 0;
      if (currentFreezes >= 3) {
        showToast('მაქსიმუმ 3 Streak Freeze შეგიძლიათ გქონდეთ ❄️');
        return false;
      }
      if ((userData.xp || 0) < 50) {
        showToast('საჭიროა მინიმუმ 50 XP Streak Freeze-ის შესაძენად.');
        return false;
      }
      userData.xp -= 50;
      userData.streakFreezes = currentFreezes + 1;
      saveUserData();
      updateHeaderStats();
      playChime('success');
      showToast('Streak Freeze დაემატა! სერია დაცულია ❄️');
      if (state.currentTab === 'profile') {
        renderProfile(document.getElementById('main-content'));
      }
      return true;
    },

    // Profile & Reset (Fixed Defect 8.6 & Stage 9.1 Drafts Purge)
    resetAllProgress: function () {
      if (confirm('ნამდვილად გსურთ მთლიანი პროგრესის წაშლა? ეს ქმედება შეუქცევადია.')) {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem(WRITING_DRAFTS_KEY);
        localStorage.removeItem('deutsch_a1_pro_v2');
        localStorage.removeItem('deutsch_a1_user_data_v1');
        localStorage.setItem(RESET_SENTINEL, 'true');

        userData = getCleanDefaultUserData();
        userData.writingDrafts = {};
        state.labSchreibenDrafts = {};
        state.labSchreibenText = '';
        saveUserData();
        setTab('profile');
        showToast('მთლიანი პროგრესი და ისტორია გასუფთავდა.');
      }
    },

    // Audio Speed
    setSpeed: function (speed) {
      state.speechRate = speed;
      document.querySelectorAll('.speed-btn').forEach(btn => {
        if (parseFloat(btn.dataset.speed) === speed) {
          btn.classList.add('bg-blue-600', 'text-white');
          btn.classList.remove('bg-slate-100', 'text-slate-700', 'dark:bg-slate-700', 'dark:text-slate-300');
        } else {
          btn.classList.remove('bg-blue-600', 'text-white');
          btn.classList.add('bg-slate-100', 'text-slate-700', 'dark:bg-slate-700', 'dark:text-slate-300');
        }
      });
      showToast(`გამოთქმის სიჩქარე: ${speed}x`);
    },

    // Theme Toggle
    toggleTheme: function () {
      state.isDark = !state.isDark;
      if (state.isDark) {
        document.documentElement.classList.add('dark');
        localStorage.setItem('theme', 'dark');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('theme', 'light');
      }
    }
  };

  // --- Initial Launch ---
  window.addEventListener('DOMContentLoaded', () => {
    // Restore Theme
    if (localStorage.getItem('theme') === 'dark' || (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      state.isDark = true;
      document.documentElement.classList.add('dark');
    }

    // Set initial stats and open Tab
    updateHeaderStats();
    setTab('lessons');
  });

})();
