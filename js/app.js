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
    trainerIndex: 0,
    trainerScore: 0,
    trainerStreak: 0,
    trainerCurrentWord: null,

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
    // Grammar CCQ state (Stage 9)
    lessonGrammarAnswers: {},
    lessonGrammarSubmitted: {},
    // Vocabulary active session state (Stage 9)
    lessonVocabSession: null
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
      labScores: { hoeren: {}, lesen: {}, schreiben: {}, sprechen: {} },
      examHistory: [], // [{ attempt, date, score, total, pct, passed }]
      examPassed: false,
      examScore: null,
      examDate: null,
      isPro: true,
      subscriptionTier: 'pro_annual'
    };
  }

  // --- Local Storage Management & State Persistence (Stage 8) ---
  const STORAGE_KEY = 'deutsch_a1_pro_v3';
  const RESET_SENTINEL = 'deutsch_a1_reset_marker_v3';

  let userData = loadUserData();

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
        data.labScores = (typeof data.labScores === 'object' && data.labScores !== null) ? data.labScores : { hoeren: {}, lesen: {}, schreiben: {}, sprechen: {} };
        data.examHistory = Array.isArray(data.examHistory) ? data.examHistory : [];
        data.examPassed = Boolean(data.examPassed);
        data.examScore = typeof data.examScore === 'number' ? data.examScore : null;
        data.examDate = typeof data.examDate === 'string' ? data.examDate : null;
        data.isPro = true;

        updateDailyStreak(data);
      }
      return data;
    } catch (e) {
      console.error('Failed to load user data, restoring safe defaults:', e);
      return getCleanDefaultUserData();
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
    saveUserData();
    playChime('success');
    showToast((successMessage ? successMessage + ' ' : '') + `+${amount} XP! ⭐`);
    updateHeaderStats();
    return true;
  }

  function addXP(amount) {
    userData.xp = (userData.xp || 0) + amount;
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
  function speakGerman(text, buttonElement, onEndCallback) {
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
    utterance.rate = state.speechRate;

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
                <span>🎙️ 4 ენობრივი ლაბორატორია (Labs)</span>
              </button>
              <button onclick="window.DeutschApp.openProModal()" class="bg-amber-400/90 hover:bg-amber-400 text-slate-950 font-bold px-4 py-3 rounded-2xl transition flex items-center gap-1.5 text-sm">
                <span>💎 PRO რეჟიმის მართვა</span>
              </button>
            </div>
          </div>

          <div class="absolute -right-12 -bottom-12 w-64 h-64 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>
          <div class="absolute right-10 top-10 text-8xl opacity-15 pointer-events-none select-none">🇩🇪</div>
        </div>

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

    if (tab === 'grammar' && state.selectedLessonId) {
      recordSkillProgress(state.selectedLessonId, 'grammar', 100, true);
    }

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
  // TAB 4: ARTICLE TRAINER (DER / DIE / DAS - 431 WORDS)
  // ==========================================================================
  function initArticleTrainer() {
    pickNextTrainerWord();
  }

  function pickNextTrainerWord() {
    const words = window.GERMAN_A1_DATA.article_trainer_words || [];
    if (words.length === 0) return;
    const randomWord = words[Math.floor(Math.random() * words.length)];
    state.trainerCurrentWord = randomWord;
  }

  function renderArticleTrainer(container) {
    const word = state.trainerCurrentWord;
    if (!word) return;

    let html = `
      <div class="max-w-xl mx-auto space-y-8 animate-fadeIn pb-16">
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
            ${escapeHtml(word.word)}
          </h2>
          <p class="text-lg font-bold text-blue-600 dark:text-blue-400 mb-5">
            ${escapeHtml(word.georgian)}
          </p>
          <button onclick="window.DeutschApp.speak('${word.article} ${word.word}', this)" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-bold hover:text-blue-600 transition">
            <span>🔊 გამოთქმის მოსმენა</span>
          </button>
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
  // TAB 6: FOUR CORE LANGUAGE LABS (HÖREN, LESEN, SCHREIBEN, SPRECHEN - STAGE 2)
  // ==========================================================================
  function renderLanguageLabs(container) {
    const labs = window.GERMAN_A1_DATA.language_labs || {};
    const active = state.labActiveTab;

    let html = `
      <div class="max-w-4xl mx-auto space-y-8 animate-fadeIn pb-16">
        
        <div class="text-center space-y-2">
          <span class="inline-block px-3 py-1 bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 rounded-full text-xs font-black tracking-wider uppercase">
            CEFR A1 ოთხი ძირითადი უნარი
          </span>
          <h1 class="text-3xl font-black text-slate-900 dark:text-white">4 ენობრივი ლაბორატორია</h1>
          <p class="text-xs text-slate-500">Hören (მოსმენა), Lesen (კითხვა), Schreiben (წერა), Sprechen (საუბარი)</p>
        </div>

        <!-- Labs Navigation Pills -->
        <div class="flex flex-wrap gap-2 p-1.5 bg-slate-100 dark:bg-slate-800 rounded-2xl text-xs font-black">
          <button onclick="window.DeutschApp.switchLabTab('hoeren')" class="flex-1 py-3 px-3 rounded-xl transition text-center ${active === 'hoeren' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            🎧 1. HÖREN (მოსმენა)
          </button>
          <button onclick="window.DeutschApp.switchLabTab('lesen')" class="flex-1 py-3 px-3 rounded-xl transition text-center ${active === 'lesen' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            📖 2. LESEN (კითხვა)
          </button>
          <button onclick="window.DeutschApp.switchLabTab('schreiben')" class="flex-1 py-3 px-3 rounded-xl transition text-center ${active === 'schreiben' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            ✍️ 3. SCHREIBEN (წერა)
          </button>
          <button onclick="window.DeutschApp.switchLabTab('sprechen')" class="flex-1 py-3 px-3 rounded-xl transition text-center ${active === 'sprechen' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-600 dark:text-slate-300'}">
            🗣️ 4. SPRECHEN (საუბარი)
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

        <!-- Prompts / Situations list -->
        <div class="space-y-3">
          ${(item.prompts || []).map(p => `
            <div class="p-3.5 rounded-xl border border-slate-100 dark:border-slate-700 flex items-center justify-between gap-3">
              <div>
                <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 block">${escapeHtml(p.point)}</span>
                <p class="font-extrabold text-xs md:text-sm text-slate-900 dark:text-white">${escapeHtml(p.phrase_de)}</p>
              </div>
              <button onclick="window.DeutschApp.speak('${p.phrase_de.replace(/'/g, "\\'")}', this)" class="p-2 rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-blue-600 text-xs">
                🔊
              </button>
            </div>
          `).join('')}

          ${(item.situations || []).map(s => `
            <div class="p-3.5 rounded-xl border border-slate-100 dark:border-slate-700 space-y-1">
              <span class="text-xs font-bold text-slate-500">${escapeHtml(s.situation_ka)}</span>
              <div class="flex items-center justify-between gap-2">
                <div>
                  <p class="font-extrabold text-sm text-slate-900 dark:text-white">${escapeHtml(s.phrase_de)}</p>
                  <p class="text-xs text-slate-400 italic">${escapeHtml(s.phrase_ka)}</p>
                </div>
                <button onclick="window.DeutschApp.speak('${s.phrase_de.replace(/'/g, "\\'")}', this)" class="p-2 rounded-lg bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-blue-600 text-xs">
                  🔊
                </button>
              </div>
            </div>
          `).join('')}
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
  // TAB 8: A1 DIAGNOSTIC SIMULATION EXAM (Compliant & Honest Certification)
  // ==========================================================================
  function renderExam(container) {
    const questions = window.GERMAN_A1_DATA.final_exam_questions || [];

    if (state.examSubmitted || userData.examPassed) {
      renderExamResults(container);
      return;
    }

    let html = `
      <div class="max-w-3xl mx-auto space-y-8 animate-fadeIn pb-16">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-8 shadow-2xl">
          <div class="flex items-center gap-2 mb-3">
            <span class="px-3 py-1 bg-yellow-400 text-slate-950 font-black rounded-full text-xs uppercase tracking-wider inline-block">
              A1 სადიაგნოსტიკო საგამოცდო სიმულატორი
            </span>
          </div>
          <h1 class="text-2xl md:text-3xl font-black mb-3">A1 დონის შემაჯამებელი საგამოცდო ტესტი</h1>
          <p class="text-slate-300 text-xs md:text-sm leading-relaxed mb-4 font-normal">
            ტესტი მოიცავს ${questions.length} შეკითხვას A1 დონის გრამატიკიდან, საკომუნიკაციო სიტუაციებიდან და ლექსიკიდან.
            ჩასაბარებლად საჭიროა მინიმუმ 60% (${Math.ceil(questions.length * 0.6)} სწორი პასუხი).
          </p>
          <div class="flex items-center gap-4 text-xs text-yellow-300 font-bold">
            <span>⏱️ ${questions.length} შეკითხვა</span> • <span>🎯 გამსვლელი: 60%</span> • <span>📜 Deutsch A1 Pro კურსის სერტიფიკატი</span>
          </div>
        </div>

        <form id="final-exam-form" onsubmit="event.preventDefault(); window.DeutschApp.submitExam();" class="space-y-5">
    `;

    questions.forEach((q, idx) => {
      const selected = state.examUserAnswers[q.id];
      html += `
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 shadow-sm space-y-3.5">
          <div class="flex items-center justify-between text-xs font-bold text-slate-400">
            <span>შეკითხვა ${idx + 1} / ${questions.length}</span>
          </div>
          <h3 class="text-sm md:text-base font-black text-slate-900 dark:text-white leading-snug">
            ${escapeHtml(q.question)}
          </h3>
          <div class="grid grid-cols-1 gap-2.5">
            ${q.options.map((opt, oIdx) => `
              <label class="flex items-center gap-3 p-3.5 rounded-2xl border border-slate-200 dark:border-slate-700 hover:bg-blue-50/50 dark:hover:bg-slate-700/30 cursor-pointer transition">
                <input type="radio" name="exam_q_${q.id}" value="${oIdx}" ${selected === oIdx ? 'checked' : ''} onchange="window.DeutschApp.onExamAnswer(${q.id}, ${oIdx})" class="w-4 h-4 text-blue-600 focus:ring-blue-500">
                <span class="text-xs md:text-sm font-medium text-slate-800 dark:text-slate-200">${escapeHtml(opt)}</span>
              </label>
            `).join('')}
          </div>
        </div>
      `;
    });

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

  function renderExamResults(container) {
    const questions = window.GERMAN_A1_DATA.final_exam_questions || [];
    const total = questions.length;
    const score = state.examSubmitted ? state.examScore : (userData.examScore || 0);
    const pct = Math.round((score / total) * 100);
    const passed = userData.examPassed || (pct >= 60);

    let html = `
      <div class="max-w-3xl mx-auto space-y-8 animate-fadeIn pb-16">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-8 text-center space-y-5 shadow-lg">
          <div class="text-7xl">${passed ? '🏆' : '📝'}</div>
          <h1 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">
            ${passed ? 'გილოცავთ! თქვენ წარმატებით ჩააბარეთ A1 სადიაგნოსტიკო გამოცდა!' : 'გამოცდა ვერ ჩაბარდა'}
          </h1>
          <div class="text-5xl font-black ${passed ? 'text-emerald-600' : 'text-rose-600'}">
            ${score} / ${total} (${pct}%)
          </div>
          <p class="text-xs md:text-sm text-slate-600 dark:text-slate-400 max-w-md mx-auto leading-relaxed">
            ${passed
              ? 'თქვენ მიაღწიეთ გერმანული ენის A1 დონის სასერტიფიკატო სტანდარტს! ქვემოთ შეგიძლიათ იხილოთ და ამობეჭდოთ თქვენი შიდა სადიაგნოსტიკო სერტიფიკატი.'
              : 'სამწუხაროდ 60%-იანი ბარიერი ვერ გადაილახა. გირჩევთ კიდევ ერთხელ გაიმეოროთ გაკვეთილები და სცადოთ ხელახლა.'}
          </p>

          <div class="flex justify-center gap-3">
            <button onclick="window.DeutschApp.retakeExam()" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 font-extrabold text-xs text-slate-700 dark:text-slate-300 hover:bg-slate-100 transition">
              🔄 ხელახლა ჩაბარება
            </button>
            ${passed ? `
              <button onclick="window.print()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition flex items-center gap-2">
                <span>🖨️ სერტიფიკატის ბეჭდვა</span>
              </button>
            ` : ''}
          </div>
        </div>

        ${passed ? `
          <!-- Printable Internal Course Certificate (Fixed SEC-01) -->
          <div id="certificate-print-area" class="bg-white border-8 border-double border-slate-900 p-10 rounded-2xl text-center space-y-6 shadow-2xl text-slate-900">
            <div class="flex items-center justify-center gap-3">
              <span class="text-3xl">🇩🇪</span>
              <span class="text-xs font-black tracking-widest uppercase text-slate-500">DEUTSCH A1 PRO • COURSE COMPLETION CERTIFICATE</span>
              <span class="text-3xl">🇬🇪</span>
            </div>

            <div class="space-y-1">
              <h2 class="text-3xl font-black tracking-tight uppercase">სერტიფიკატი</h2>
              <p class="text-xs font-bold text-slate-500 tracking-wider">A1 დონის სრული კურსის წარმატებით დასრულება</p>
            </div>

            <p class="text-xs text-slate-600 max-w-md mx-auto">
              ეძლევა სტუდენტს, რომელმაც წარმატებით დაასრულა გერმანული ენის A1 დონის საუნივერსიტეტო პროგრამა (10 მოდული) და ჩააბარა შემაჯამებელი სადიაგნოსტიკო გამოცდა:
            </p>

            <div class="text-2xl font-black border-b-2 border-slate-900 max-w-sm mx-auto pb-1 text-blue-700">
              საქართველოს გერმანული ენის სტუდენტი
            </div>

            <div class="grid grid-cols-3 gap-4 max-w-lg mx-auto text-xs py-4 border-y border-slate-200">
              <div>
                <span class="text-slate-400 block font-bold">შედეგი</span>
                <span class="font-black text-emerald-600 text-sm">${pct}% (${score}/${total})</span>
              </div>
              <div>
                <span class="text-slate-400 block font-bold">შეფასება</span>
                <span class="font-black text-blue-600 text-sm">${pct >= 90 ? 'Sehr Gut (ფრიადი)' : (pct >= 80 ? 'Gut (კარგი)' : 'Bestanden (ჩაბარებულია)')}</span>
              </div>
              <div>
                <span class="text-slate-400 block font-bold">თარიღი</span>
                <span class="font-black text-slate-800 text-sm">${new Date().toLocaleDateString('ka-GE')}</span>
              </div>
            </div>

            <div class="pt-4 flex flex-col md:flex-row items-center justify-between max-w-lg mx-auto text-[10px] text-slate-500 font-medium space-y-2 md:space-y-0">
              <div class="text-left">
                <span class="block font-black text-slate-800">შეფასებული უნარები:</span>
                <span>Hören, Lesen, Wortschatz, Grammatik</span>
              </div>
              <div class="text-right">
                <span class="block font-black text-slate-800">სტატუსი:</span>
                <span class="text-emerald-600 font-black">COURSE COMPLETED ✓</span>
              </div>
            </div>

            <!-- Transparent Disclaimer (Compliant with SEC-01) -->
            <div class="pt-4 border-t border-slate-100 text-[9px] text-slate-400 max-w-md mx-auto leading-normal">
              * ეს სერტიფიკატი ადასტურებს Deutsch A1 Pro პლატფორმის შიდა სადიაგნოსტიკო ტესტის წარმატებით ჩაბარებას და წარმოადგენს პერსონალურ საგანმანათლებლო შეფასებას.
            </div>
          </div>
        ` : ''}

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
                    <span class="font-black text-slate-900 dark:text-white">${h.score} / ${h.total || 25} (${h.pct}%)</span>
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
                  <li>✓ 4 ენობრივი ლაბორატორია</li>
                  <li>✓ SM-2 ინტერვალური გამეორება</li>
                  <li>✓ der / die / das ტრენერი (431)</li>
                  <li>✓ Satzbau სინტაქსი</li>
                  <li>✓ სადიაგნოსტიკო სერტიფიკატი</li>
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

  // --- Public Interface for inline HTML events ---
  window.DeutschApp = {
    state,
    setTab,
    speak: speakGerman,
    recordSkillProgress,
    getLocalDateString,
    getCalendarDaysDiff,
    loadUserData,
    speakSlow: function (text, btn) {
      const orig = state.speechRate;
      state.speechRate = 0.7;
      speakGerman(text, btn, () => {
        state.speechRate = orig;
      });
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

      // Track active lesson vocabulary mastery session (Stage 9)
      if (state.lessonVocabSession && state.lessonVocabSession.lessonId) {
        const sess = state.lessonVocabSession;
        if (!sess.reviewedIds.includes(current.id)) {
          sess.reviewedIds.push(current.id);
        }
        if (quality >= 3) {
          sess.correctCount += 1;
        }
        const lessonWords = window.GERMAN_A1_DATA.dictionary.filter(w => w.lesson_id === sess.lessonId);
        const minRequired = Math.min(5, lessonWords.length);
        const accuracy = Math.round((sess.correctCount / sess.reviewedIds.length) * 100);

        if (sess.reviewedIds.length >= minRequired && accuracy >= 70) {
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
      state.labSchreibenTaskIndex = (state.labSchreibenTaskIndex + 1) % total;
      state.labSchreibenText = '';
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

    // Exam Handlers (Fixed Defect 8.5)
    onExamAnswer: function (qId, ansIdx) {
      state.examUserAnswers[qId] = ansIdx;
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
      questions.forEach(q => {
        if (state.examUserAnswers[q.id] === q.answer) {
          score += 1;
        }
      });

      const pct = Math.round((score / total) * 100);
      const passed = (pct >= 60);

      state.examScore = score;
      state.examSubmitted = true;

      userData.examHistory = userData.examHistory || [];
      const attemptRecord = {
        attempt: userData.examHistory.length + 1,
        date: new Date().toISOString(),
        localDate: getLocalDateString(),
        score: score,
        total: total,
        pct: pct,
        passed: passed
      };
      userData.examHistory.push(attemptRecord);
      userData.examScore = score;
      userData.examPassed = passed;
      userData.examDate = attemptRecord.date;

      if (passed) {
        playChime('fanfare');
        grantRewardXP('exam_first_passing_score', 100, `სადიაგნოსტიკო გამოცდა წარმატებით ჩაბარდა (${score}/${total}, ${pct}%)!`);
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
      renderExam(document.getElementById('main-content'));
    },

    // Profile & Reset (Fixed Defect 8.6)
    resetAllProgress: function () {
      if (confirm('ნამდვილად გსურთ მთლიანი პროგრესის წაშლა? ეს ქმედება შეუქცევადია.')) {
        localStorage.removeItem(STORAGE_KEY);
        localStorage.removeItem('deutsch_a1_pro_v2');
        localStorage.removeItem('deutsch_a1_user_data_v1');
        localStorage.setItem(RESET_SENTINEL, 'true');

        userData = getCleanDefaultUserData();
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
