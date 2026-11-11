/**
 * DEUTSCH A1 - ქართულ-გერმანული სასწავლო პლატფორმა
 * Modern Interactive Application Engine (Pro Edition)
 */

(function () {
  'use strict';

  // --- Global State ---
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
    // MC state
    mcIndex: 0,
    mcSelectedAnswer: null,
    mcSubmitted: false,
    mcScore: 0,
    // FIB state
    fibIndex: 0,
    fibUserInput: '',
    fibSubmitted: false,
    fibIsCorrect: false,
    fibScore: 0,
    // Listening state
    lisIndex: 0,
    lisSelectedAnswer: null,
    lisSubmitted: false,
    lisScore: 0,
    lisPlayCount: 0,

    // Dialogue Sequential Player state
    dialoguePlaying: false,
    dialogueLineIndex: 0,
    dialogueTimer: null
  };

  // --- Local Storage Management ---
  const STORAGE_KEY = 'deutsch_a1_pro_v2';

  let userData = loadUserData();

  function loadUserData() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        return JSON.parse(raw);
      }
    } catch (e) {
      console.error('Failed to load user data:', e);
    }
    return {
      xp: 0,
      streak: 1,
      lastActiveDate: new Date().toISOString().split('T')[0],
      completedLessons: [],
      lessonScores: {},
      masteredWords: [],
      favoriteWords: [],
      examPassed: false,
      examScore: null,
      isPro: true,
      subscriptionTier: 'pro_annual'
    };
  }

  function saveUserData() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(userData));
      updateHeaderStats();
    } catch (e) {
      console.error('Failed to save user data:', e);
    }
  }

  function addXP(amount) {
    userData.xp = (userData.xp || 0) + amount;
    saveUserData();
    playChime('success');
    showToast(`+${amount} XP! ⭐`);
  }

  // --- Web Audio API Chimes (Native & Zero Dependencies) ---
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

    // Stop sequential dialogue if switching away
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
        
        <!-- Hero Banner with Goethe-Institut Curriculum Highlights -->
        <div class="relative overflow-hidden bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 rounded-3xl p-8 md:p-10 text-white shadow-2xl">
          <div class="relative z-10 max-w-3xl">
            <div class="flex items-center gap-2 mb-3">
              <span class="px-3 py-1 bg-white/20 backdrop-blur-md rounded-full text-xs font-bold tracking-wider uppercase">
                Schritte International Neu & Menschen აკადემიური პროგრამა
              </span>
              <span class="px-2.5 py-1 bg-amber-400 text-slate-950 font-black rounded-md text-[11px] uppercase tracking-wider">
                💎 PRO PLATFORM
              </span>
            </div>
            <h1 class="text-3xl md:text-5xl font-black mb-4 leading-tight">
              გერმანული ენა ქართველებისთვის • A1 დონე
            </h1>
            <p class="text-blue-100 text-base md:text-lg mb-6 leading-relaxed font-normal">
              10 ყოვლისმომცველი გაკვეთილი, 734 სიტყვიანი ლექსიკონი, დეტალური გრამატიკული ანალიზი ქართულენოვანთათვის, რეალური აუდიო დიალოგები და 3-დონიანი სავარჯიშო ცენტრი.
            </p>
            <div class="flex flex-wrap gap-4 items-center">
              <button onclick="window.DeutschApp.openLesson(1)" class="bg-white text-blue-700 hover:bg-blue-50 font-extrabold px-6 py-3 rounded-2xl shadow-lg transition active:scale-95 flex items-center gap-2 text-sm">
                <span>🚀 Lektion 1-ის დაწყება</span>
              </button>
              <button onclick="window.DeutschApp.setTab('article-trainer')" class="bg-white/10 hover:bg-white/20 text-white font-bold px-5 py-3 rounded-2xl backdrop-blur-md transition flex items-center gap-2 text-sm border border-white/20">
                <span>🎯 der / die / das ტრენერი (431 სიტყვა)</span>
              </button>
              <button onclick="window.DeutschApp.openProModal()" class="bg-amber-400/90 hover:bg-amber-400 text-slate-950 font-bold px-4 py-3 rounded-2xl transition flex items-center gap-1.5 text-sm">
                <span>💎 PRO გამოწერის მართვა</span>
              </button>
            </div>
          </div>

          <!-- Decorative Background Elements -->
          <div class="absolute -right-12 -bottom-12 w-64 h-64 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>
          <div class="absolute right-10 top-10 text-8xl opacity-15 pointer-events-none select-none">🇩🇪</div>
        </div>

        <!-- Lessons Grid -->
        <div>
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-2xl font-black text-slate-900 dark:text-white">A1 სასწავლო მოდულები</h2>
              <p class="text-xs text-slate-500">მიჰყევით გაკვეთილებს ეტაპობრივად თანმიმდევრობით</p>
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
                  <h3 class="text-lg font-extrabold text-slate-900 dark:text-white leading-snug">${l.title_ka}</h3>
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

            <p class="text-sm font-semibold text-blue-700 dark:text-blue-300 italic mb-2">${l.title_de}</p>
            <p class="text-xs text-slate-600 dark:text-slate-400 mb-5 leading-relaxed font-normal">${l.description_ka || ''}</p>

            <!-- Objectives snippet -->
            ${l.objectives_ka && l.objectives_ka.length ? `
              <div class="p-3 bg-slate-50 dark:bg-slate-700/30 rounded-xl mb-4 text-[11px] text-slate-600 dark:text-slate-300 space-y-1">
                <span class="font-bold text-slate-700 dark:text-slate-200 block">🎯 ძირითადი თემები:</span>
                <p class="line-clamp-2">• ${l.objectives_ka.slice(0, 3).join(' • ')}</p>
              </div>
            ` : ''}
          </div>

          <div class="flex items-center justify-between pt-4 border-t border-slate-100 dark:border-slate-700/60">
            <div class="text-[11px] font-bold text-slate-500 flex items-center gap-2">
              <span title="გრამატიკული სექციები">📚 ${l.grammar_sections ? l.grammar_sections.length : 0} თეორია</span>
              <span>•</span>
              <span title="აუდიო დიალოგები">💬 ${l.dialogues ? l.dialogues.length : 0} დიალოგი</span>
              <span>•</span>
              <span title="სავარჯიშოების რაოდენობა" class="text-blue-600 dark:text-blue-400">✍️ ${totalTests} ტესტი</span>
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

    // Filter vocabulary for this lesson (all 734 words have lesson_id)
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
              <h1 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white leading-tight">${lesson.title_ka}</h1>
              <p class="text-slate-500 font-bold text-base mt-0.5">${lesson.title_de}</p>
            </div>
          </div>

          ${lesson.description_ka ? `
            <p class="text-slate-600 dark:text-slate-300 text-sm leading-relaxed mb-6 font-normal">${lesson.description_ka}</p>
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
                    <span>${obj}</span>
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

      html += `
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm">
          <h3 class="text-lg md:text-xl font-black text-slate-900 dark:text-white mb-4 flex items-center gap-2.5">
            <span class="w-2.5 h-6 bg-blue-600 rounded-full inline-block"></span>
            <span>${sec.title}</span>
          </h3>
          <div class="text-slate-700 dark:text-slate-300 text-sm md:text-base leading-relaxed space-y-3 font-normal">
            <p>${formattedContent}</p>
          </div>
        </div>
      `;
    });

    html += `
        </div>

        <!-- TAB CONTENT 2: Dialogues & Sequential Audio Player -->
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

            <div class="space-y-3.5" id="dialogue-lines-container">
    `;

    (lesson.dialogues || []).forEach((line, idx) => {
      const isEven = idx % 2 === 0;
      html += `
        <div id="dialogue-line-${idx}" class="p-4 rounded-2xl transition-all duration-200 ${isEven ? 'bg-blue-50/70 dark:bg-slate-700/30 border border-blue-100 dark:border-slate-700' : 'bg-slate-50 dark:bg-slate-700/20 border border-slate-100 dark:border-slate-700'}">
          <div class="flex items-center justify-between mb-1.5">
            <span class="text-xs font-black uppercase tracking-wider text-blue-700 dark:text-blue-400 flex items-center gap-1.5">
              <span>👤</span> ${line.speaker}
            </span>
            <button onclick="window.DeutschApp.speak('${line.text_de.replace(/'/g, "\\'")}', this)" class="text-xs font-bold text-slate-600 dark:text-slate-300 hover:text-blue-600 flex items-center gap-1 bg-white dark:bg-slate-800 px-3 py-1 rounded-lg shadow-sm border border-slate-200 dark:border-slate-600 transition">
              <span>🔊 მოუსმინე</span>
            </button>
          </div>
          <p class="text-base font-extrabold text-slate-900 dark:text-white mb-1">${line.text_de}</p>
          <p class="text-xs md:text-sm text-slate-600 dark:text-slate-400 font-medium">${line.text_ka}</p>
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
                <h4 class="font-black text-base text-amber-900 dark:text-amber-200">${lesson.cultural_notes.title || 'კულტურული ნიუანსები'}</h4>
                <p class="text-xs md:text-sm text-amber-900 dark:text-amber-300 leading-relaxed font-normal">${lesson.cultural_notes.content_ka}</p>
              </div>
            ` : `
              <p class="text-sm text-slate-500">ამ გაკვეთილის კულტურული ცნობარი მალე განახლდება.</p>
            `}

            <div class="mt-6 p-4 rounded-2xl bg-slate-50 dark:bg-slate-700/30 border border-slate-200 dark:border-slate-700 text-xs text-slate-600 dark:text-slate-300 space-y-2">
              <span class="font-bold text-slate-800 dark:text-slate-200 block">📌 რჩევა ქართველი სტუდენტებისთვის:</span>
              <p>გერმანულენოვან ქვეყნებში მკაცრად დაცულია პუნქტუალურობა (Pünktlichkeit) და ოფიციალური მიმართვის ფორმა (Siezen). არასდროს მიმართოთ უცნობ ადამიანს ან თანამშრომელს "du"-თი, სანამ ის თავად არ შემოგთავაზებთ ამას ("Duzen").</p>
            </div>
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
              ${w.article ? `<span class="text-[11px] font-black px-2 py-0.5 rounded-md ${badgeClass}">${w.article}</span>` : ''}
              <span class="font-extrabold text-sm text-slate-900 dark:text-white truncate">${w.word}</span>
              ${w.plural ? `<span class="text-[11px] text-slate-400 font-normal">(${w.plural})</span>` : ''}
            </div>
            <p class="text-xs font-medium text-slate-600 dark:text-slate-300 truncate">${w.georgian}</p>
            ${w.example_de ? `
              <p class="text-[10px] text-slate-400 italic mt-1 truncate">${w.example_de}</p>
            ` : ''}
          </div>
          <div class="flex items-center gap-1.5 shrink-0">
            <button onclick="window.DeutschApp.toggleFavorite('${w.id}')" class="p-2 rounded-xl text-xs hover:bg-slate-200 dark:hover:bg-slate-700 transition ${isFav ? 'text-amber-500' : 'text-slate-300'}" title="რჩეულებში დამატება">
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
              🎓 Goethe A1 სასერტიფიკატო გამოცდაზე გადასვლა →
            </button>
          `}
        </div>

      </div>
    `;

    container.innerHTML = html;

    // Default init for exercises
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

  // --- Sequential Dialogue Player ---
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

    state.dialoguePlaying = true;
    state.dialogueLineIndex = 0;

    const btn = document.getElementById('btn-play-all-dialogue');
    if (btn) btn.innerHTML = `<span>⏹️ დიალოგის შეჩერება</span>`;

    playNextDialogueLine(lesson);
  }

  function playNextDialogueLine(lesson) {
    if (!state.dialoguePlaying) return;

    if (state.dialogueLineIndex >= lesson.dialogues.length) {
      stopSequentialDialogue();
      showToast('დიალოგის მოსმენა დასრულდა 👏');
      return;
    }

    const currentLine = lesson.dialogues[state.dialogueLineIndex];

    // Highlight current line
    lesson.dialogues.forEach((_, idx) => {
      const el = document.getElementById(`dialogue-line-${idx}`);
      if (el) {
        if (idx === state.dialogueLineIndex) {
          el.classList.add('ring-2', 'ring-blue-500', 'bg-blue-100/50');
        } else {
          el.classList.remove('ring-2', 'ring-blue-500', 'bg-blue-100/50');
        }
      }
    });

    speakGerman(currentLine.text_de, null, () => {
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

    // Remove line highlights
    document.querySelectorAll('[id^="dialogue-line-"]').forEach(el => {
      el.classList.remove('ring-2', 'ring-blue-500', 'bg-blue-100/50');
    });
  }

  // ==========================================================================
  // MULTI-MODE EXERCISE ENGINE (MC, FIB, LISTENING)
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

    // Finished check
    if (state.mcIndex >= list.length) {
      const total = list.length;
      const score = state.mcScore;
      const pct = Math.round((score / total) * 100);
      const passed = pct >= 60;

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
              ? 'შესანიშნავი შედეგია! თქვენ საფუძვლიანად აითვისეთ ამ გაკვეთილის გრამატიკული და ლექსიკური წესები.'
              : 'სასურველია გადახედოთ გაკვეთილის გრამატიკის ნაწილს და სცადოთ ტესტი ხელახლა.'}
          </p>
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
          ${q.question}
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
          <span class="text-xs md:text-sm font-medium">${opt}</span>
        </button>
      `;
    });

    html += `
        </div>

        ${state.mcSubmitted ? `
          <div class="p-4 rounded-2xl ${state.mcSelectedAnswer === q.answer ? 'bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 dark:border-emerald-900/40 text-emerald-900 dark:text-emerald-200' : 'bg-rose-50 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900/40 text-rose-900 dark:text-rose-200'} text-xs md:text-sm animate-fadeIn space-y-1">
            <span class="font-black block">${state.mcSelectedAnswer === q.answer ? 'სწორია! 🎉 (+10 XP)' : 'არასწორია!'}</span>
            <p class="font-normal leading-relaxed">${q.explanation || ''}</p>
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

      container.innerHTML = `
        <div class="p-8 text-center space-y-6 animate-fadeIn bg-slate-50 dark:bg-slate-700/20 rounded-2xl border border-slate-200 dark:border-slate-700">
          <div class="text-6xl">✍️</div>
          <h3 class="text-2xl font-black text-slate-900 dark:text-white">Lückentext სავარჯიშო დასრულდა!</h3>
          <div class="text-4xl font-black text-emerald-600">${score} / ${total} სწორი (${pct}%)</div>
          <p class="text-xs text-slate-600 dark:text-slate-400">თქვენ წარმატებით გაიარეთ გამოტოვებული სიტყვების წერის ტრენერი.</p>
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
            <span>${item.sentence_before || ''}</span>
            <input type="text" id="fib-input" value="${state.fibUserInput}" oninput="window.DeutschApp.onFIBInput(this.value)" onkeydown="if(event.key==='Enter') window.DeutschApp.submitFIBAnswer(${lesson.id})" placeholder="..." class="px-3 py-1.5 rounded-xl border-2 ${state.fibSubmitted ? (state.fibIsCorrect ? 'border-emerald-500 bg-emerald-50 text-emerald-900' : 'border-rose-500 bg-rose-50 text-rose-900') : 'border-blue-500 bg-white dark:bg-slate-800'} text-center font-black text-lg max-w-[160px] focus:outline-none" ${state.fibSubmitted ? 'disabled' : ''}>
            <span>${item.sentence_after || ''}</span>
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
            <p class="text-xs text-slate-500 dark:text-slate-400 font-medium pt-1">💡 მინიშნება: ${item.hint}</p>
          ` : ''}
        </div>

        ${state.fibSubmitted ? `
          <div class="p-4 rounded-2xl ${state.fibIsCorrect ? 'bg-emerald-50 dark:bg-emerald-950/30 border border-emerald-200 text-emerald-900 dark:text-emerald-200' : 'bg-rose-50 dark:bg-rose-950/30 border border-rose-200 text-rose-900 dark:text-rose-200'} text-xs md:text-sm animate-fadeIn">
            <span class="font-black">${state.fibIsCorrect ? 'სწორია! 🎉 (+10 XP)' : 'არასწორია!'}</span>
            ${!state.fibIsCorrect ? `<span class="ml-2 font-bold">სწორი პასუხია: <code class="px-2 py-0.5 bg-white dark:bg-slate-800 rounded font-black text-emerald-600">${item.correct_answer}</code></span>` : ''}
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

      container.innerHTML = `
        <div class="p-8 text-center space-y-6 animate-fadeIn bg-slate-50 dark:bg-slate-700/20 rounded-2xl border border-slate-200 dark:border-slate-700">
          <div class="text-6xl">🎧</div>
          <h3 class="text-2xl font-black text-slate-900 dark:text-white">მოსმენის გაგების ტესტი დასრულდა!</h3>
          <div class="text-4xl font-black text-emerald-600">${score} / ${total} სწორი (${pct}%)</div>
          <p class="text-xs text-slate-600 dark:text-slate-400">თქვენ წარმატებით შეამოწმეთ გერმანული საუბრის აღქმის უნარი.</p>
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
              ტექსტი იყო: "${item.audio_text}"
            </div>
          ` : ''}
        </div>

        <!-- Question based on audio -->
        <h4 class="text-base md:text-lg font-black text-slate-900 dark:text-white leading-snug">
          ${item.question}
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
          <span class="text-xs md:text-sm font-medium">${opt}</span>
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
              <input type="text" id="lexicon-search-input" value="${state.lexiconSearch}" oninput="window.DeutschApp.onLexiconSearch(this.value)" placeholder="ძებნა გერმანულად ან ქართულად..." class="w-full px-4 py-3 pl-11 rounded-2xl bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600 focus:outline-none focus:border-blue-500 text-xs md:text-sm font-medium">
              <span class="absolute left-4 top-3 text-slate-400">🔍</span>
              ${state.lexiconSearch ? `
                <button onclick="window.DeutschApp.clearLexiconSearch()" class="absolute right-4 top-3 text-slate-400 hover:text-slate-600 text-xs">✕</button>
              ` : ''}
            </div>

            <div>
              <select onchange="window.DeutschApp.onLexiconCategory(this.value)" class="w-full px-4 py-3 rounded-2xl bg-slate-50 dark:bg-slate-700/50 border border-slate-200 dark:border-slate-600 focus:outline-none focus:border-blue-500 text-xs font-bold">
                ${categories.map(c => `
                  <option value="${c}" ${state.lexiconCategory === c ? 'selected' : ''}>
                    ${c === 'all' ? 'ყველა თემატიკა (კატეგორია)' : c}
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
              ${w.article ? `<span class="text-[11px] font-black px-2 py-0.5 rounded-md ${badgeClass}">${w.article}</span>` : ''}
              <h3 class="font-extrabold text-base text-slate-900 dark:text-white truncate">${w.word}</h3>
              ${w.plural ? `<span class="text-xs text-slate-400 font-normal">(${w.plural})</span>` : ''}
              ${w.pos ? `<span class="text-[10px] text-slate-400 bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 rounded">${w.pos}</span>` : ''}
            </div>

            <p class="text-xs md:text-sm font-semibold text-blue-700 dark:text-blue-300 mb-2">${w.georgian}</p>

            ${w.example_de ? `
              <div class="p-2.5 rounded-xl bg-slate-50 dark:bg-slate-700/30 text-xs space-y-0.5">
                <p class="font-bold text-slate-800 dark:text-slate-200">${w.example_de}</p>
                <p class="text-slate-500 italic text-[11px]">${w.example_ka || ''}</p>
              </div>
            ` : ''}
          </div>

          <div class="flex flex-col gap-1.5 shrink-0">
            <button onclick="window.DeutschApp.speak('${w.word.replace(/'/g, "\\'")}', this)" class="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 hover:text-blue-600 hover:bg-blue-50 transition" title="გამოთქმის მოსმენა">
              🔊
            </button>
            <button onclick="window.DeutschApp.toggleFavorite('${w.id}')" class="p-2.5 rounded-xl text-base hover:bg-slate-100 dark:hover:bg-slate-700 transition ${isFav ? 'text-amber-500' : 'text-slate-300'}" title="რჩეულებში დამატება">
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
  // TAB 3: FLASHCARDS TRAINER (WITH LESSON SELECTOR)
  // ==========================================================================
  function initFlashcards() {
    let pool = [...window.GERMAN_A1_DATA.dictionary];

    if (state.flashcardLessonFilter !== 'all') {
      if (state.flashcardLessonFilter === 'fav') {
        const favs = new Set(userData.favoriteWords || []);
        pool = pool.filter(w => favs.has(w.id));
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
            <h1 class="text-2xl font-black text-slate-900 dark:text-white">სასწავლო ბარათები</h1>
            <p class="text-xs text-slate-500">დააჭირეთ ბარათს გადასაბრუნებლად</p>
          </div>

          <!-- Lesson Selector Dropdown -->
          <select onchange="window.DeutschApp.onFlashcardLessonFilter(this.value)" class="px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold focus:outline-none">
            <option value="all" ${state.flashcardLessonFilter === 'all' ? 'selected' : ''}>ყველა სიტყვა (734)</option>
            ${window.GERMAN_A1_DATA.lessons.map(l => `
              <option value="${l.id}" ${state.flashcardLessonFilter === String(l.id) ? 'selected' : ''}>გაკვეთილი ${l.id}: ${l.title_ka.substring(0, 20)}...</option>
            `).join('')}
            <option value="fav" ${state.flashcardLessonFilter === 'fav' ? 'selected' : ''}>⭐ მხოლოდ რჩეულები</option>
          </select>
        </div>

        ${total === 0 ? `
          <div class="p-12 text-center text-slate-500 bg-white dark:bg-slate-800 rounded-3xl border border-slate-200 dark:border-slate-700">
            ამ კატეგორიაში ბარათები არ მოიძებნა.
          </div>
        ` : `
          <!-- Progress counter -->
          <div class="flex items-center justify-between text-xs font-extrabold text-slate-400">
            <span>ბარათი ${state.flashcardIndex + 1} / ${total}</span>
            <span class="text-emerald-600">ნასწავლია: ${(userData.masteredWords || []).length} სიტყვა</span>
          </div>

          <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5 overflow-hidden">
            <div class="bg-blue-600 h-1.5 rounded-full transition-all duration-300" style="width: ${((state.flashcardIndex + 1) / total) * 100}%"></div>
          </div>

          <!-- 3D Flippable Card -->
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
                    <span class="text-[10px] font-black uppercase tracking-wider text-slate-400 mb-3">${current.category || 'A1 ლექსიკა'}</span>
                    ${current.article ? `<span class="text-xs font-black px-3 py-1 rounded-full ${badgeClass} mb-2">${current.article}</span>` : ''}
                    <h2 class="text-3xl md:text-4xl font-black text-slate-900 dark:text-white mb-2 text-center">${current.word}</h2>
                    ${current.plural ? `<p class="text-xs text-slate-400 mb-5 font-bold">Plural: ${current.plural}</p>` : '<div class="mb-5"></div>'}

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
                    <h3 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white mb-4 text-center">${current.georgian}</h3>

                    ${current.example_de ? `
                      <div class="p-3.5 rounded-xl bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm border border-blue-100 dark:border-slate-700 text-xs space-y-1 max-w-sm text-center">
                        <p class="font-bold text-slate-800 dark:text-slate-200">${current.example_de}</p>
                        <p class="text-slate-500 italic text-[11px]">${current.example_ka || ''}</p>
                      </div>
                    ` : ''}

                    <span class="absolute bottom-4 text-[11px] text-slate-400 font-medium">დააჭირეთ უკან დასაბრუნებლად ↺</span>
                  </div>
                </div>
              </div>

              <!-- Controls: Repeat vs Know -->
              <div class="grid grid-cols-2 gap-4">
                <button onclick="window.DeutschApp.flashcardAction(false)" class="py-3 px-4 rounded-2xl border border-rose-300 dark:border-rose-900/50 bg-rose-50 dark:bg-rose-950/30 text-rose-700 dark:text-rose-300 font-extrabold text-xs hover:bg-rose-100 transition flex items-center justify-center gap-1.5">
                  <span>❌ გასამეორებელია</span>
                </button>
                <button onclick="window.DeutschApp.flashcardAction(true)" class="py-3 px-4 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-extrabold text-xs shadow-md transition flex items-center justify-center gap-1.5 active:scale-95">
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

        <!-- Score & Streak Banner -->
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

        <!-- Word Card -->
        <div id="trainer-card" class="bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 rounded-3xl p-10 text-center shadow-lg transition-all duration-300">
          <span class="text-[11px] font-black uppercase tracking-widest text-slate-400 mb-2 block">არსებითი სახელი</span>
          <h2 id="trainer-word-display" class="text-4xl md:text-5xl font-black text-slate-900 dark:text-white mb-3">
            ${word.word}
          </h2>
          <p class="text-lg font-bold text-blue-600 dark:text-blue-400 mb-5">
            ${word.georgian}
          </p>
          <button onclick="window.DeutschApp.speak('${word.article} ${word.word}', this)" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-xs font-bold hover:text-blue-600 transition">
            <span>🔊 გამოთქმის მოსმენა</span>
          </button>
        </div>

        <!-- 3 Big Action Buttons -->
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

        <!-- Feedback Box -->
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

        <!-- Target Georgian Sentence -->
        <div class="bg-gradient-to-r from-blue-900 to-indigo-900 rounded-3xl p-6 text-white text-center shadow-lg">
          <span class="text-[10px] font-extrabold uppercase tracking-wider text-blue-300 block mb-1">თარგმნეთ ქართულიდან:</span>
          <h2 class="text-xl md:text-2xl font-black">${challenge.translation_ka}</h2>
          ${challenge.hint ? `<p class="text-xs text-blue-200 mt-2 italic">💡 წესი: ${challenge.hint}</p>` : ''}
        </div>

        <!-- Drop/Build Area -->
        <div class="min-h-[90px] p-4 rounded-3xl border-2 border-dashed ${state.sbChecked ? (state.sbIsCorrect ? 'border-emerald-500 bg-emerald-50/50' : 'border-rose-500 bg-rose-50/50') : 'border-blue-300 dark:border-slate-600 bg-white dark:bg-slate-800'} flex flex-wrap items-center gap-2 transition">
          ${state.sbSelectedWords.length === 0 ? `
            <span class="text-xs text-slate-400 italic mx-auto">დააჭირეთ ქვემოთ მოცემულ სიტყვებს წინადადების ასაწყობად</span>
          ` : state.sbSelectedWords.map((w, idx) => `
            <button onclick="window.DeutschApp.removeSentenceWord(${idx})" class="px-3.5 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-sm transition flex items-center gap-1 active:scale-95">
              <span>${w}</span>
              <span class="text-[10px] opacity-70">✕</span>
            </button>
          `).join('')}
        </div>

        <!-- Word Bank -->
        <div>
          <span class="text-xs font-bold text-slate-400 block mb-2 uppercase">სიტყვების ბანკი:</span>
          <div class="flex flex-wrap gap-2">
            ${state.sbAvailableWords.map((w, idx) => `
              <button onclick="window.DeutschApp.addSentenceWord(${idx})" class="sentence-chip px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-700 text-slate-800 dark:text-slate-100 font-extrabold text-xs hover:bg-blue-100 dark:hover:bg-slate-600 border border-slate-200 dark:border-slate-600 shadow-sm transition active:scale-95">
                ${w}
              </button>
            `).join('')}
          </div>
        </div>

        <!-- Actions -->
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
  // TAB 6: GRAMMAR REFERENCE HANDBOOK
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
            <span class="text-blue-600">📊</span> ${tables.articles.title}
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
                    <td class="font-bold">${c.case_de}</td>
                    <td>${c.maskulin}</td>
                    <td>${c.feminin}</td>
                    <td>${c.neutrum}</td>
                    <td>${c.plural}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- 2. Pronouns Table -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span class="text-indigo-600">👤</span> ${tables.pronouns.title}
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
                    <td class="font-bold">${p.person}</td>
                    <td class="font-extrabold text-blue-600">${p.nom}</td>
                    <td class="font-extrabold text-indigo-600">${p.akk}</td>
                    <td class="font-extrabold text-emerald-600">${p.dat}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- 3. Modal Verbs Table -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span class="text-amber-500">⚙️</span> ${tables.modal_verbs.title}
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
                    <td class="font-black">${v.verb}</td>
                    <td class="font-bold text-blue-600">${v.ich}</td>
                    <td>${v.du}</td>
                    <td>${v.wir}</td>
                    <td>${v.ihr}</td>
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>

        <!-- 4. Irregular Verbs Table -->
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-6 md:p-8 shadow-sm space-y-4">
          <h3 class="text-lg font-black text-slate-900 dark:text-white flex items-center gap-2">
            <span class="text-rose-600">⚡</span> ${tables.irregular_verbs.title}
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
                    <td class="font-extrabold">${v.inf}</td>
                    <td class="text-slate-600 dark:text-slate-300">${v.prasens}</td>
                    <td class="font-extrabold text-blue-600 dark:text-blue-400">${v.perfekt}</td>
                    <td class="font-medium text-slate-600 dark:text-slate-300">${v.georgian}</td>
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
  // TAB 7: GOETHE-INSTITUT A1 CERTIFICATION EXAM SIMULATOR
  // ==========================================================================
  function renderExam(container) {
    const questions = window.GERMAN_A1_DATA.final_exam_questions || [];

    if (state.examSubmitted) {
      renderExamResults(container);
      return;
    }

    let html = `
      <div class="max-w-3xl mx-auto space-y-8 animate-fadeIn pb-16">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl p-8 shadow-2xl">
          <div class="flex items-center gap-2 mb-3">
            <span class="px-3 py-1 bg-yellow-400 text-slate-950 font-black rounded-full text-xs uppercase tracking-wider inline-block">
              Goethe-Zertifikat A1: Start Deutsch 1 სტანდარტი
            </span>
          </div>
          <h1 class="text-2xl md:text-3xl font-black mb-3">A1 დონის სასერტიფიკატო სატესტო გამოცდა</h1>
          <p class="text-slate-300 text-xs md:text-sm leading-relaxed mb-4 font-normal">
            ტესტი მოიცავს ${questions.length} შეკითხვას A1 დონის გრამატიკიდან, საკომუნიკაციო სიტუაციებიდან და ლექსიკიდან.
            ჩასაბარებლად საჭიროა მინიმუმ 60% (${Math.ceil(questions.length * 0.6)} სწორი პასუხი).
          </p>
          <div class="flex items-center gap-4 text-xs text-yellow-300 font-bold">
            <span>⏱️ ${questions.length} შეკითხვა</span> • <span>🎯 გამსვლელი: 60%</span> • <span>📜 ოფიციალური დიპლომი</span>
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
            ${q.question}
          </h3>
          <div class="grid grid-cols-1 gap-2.5">
            ${q.options.map((opt, oIdx) => `
              <label class="flex items-center gap-3 p-3.5 rounded-2xl border border-slate-200 dark:border-slate-700 hover:bg-blue-50/50 dark:hover:bg-slate-700/30 cursor-pointer transition">
                <input type="radio" name="exam_q_${q.id}" value="${oIdx}" ${selected === oIdx ? 'checked' : ''} onchange="window.DeutschApp.onExamAnswer(${q.id}, ${oIdx})" class="w-4 h-4 text-blue-600 focus:ring-blue-500">
                <span class="text-xs md:text-sm font-medium text-slate-800 dark:text-slate-200">${opt}</span>
              </label>
            `).join('')}
          </div>
        </div>
      `;
    });

    html += `
          <div class="flex justify-center pt-4">
            <button type="submit" class="px-8 py-4 rounded-2xl bg-emerald-600 hover:bg-emerald-700 text-white font-black text-base shadow-xl shadow-emerald-600/25 transition active:scale-95">
              გამოცდის დასრულება და სერტიფიკატის მიღება 🚀
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
    const score = state.examScore;
    const pct = Math.round((score / total) * 100);
    const passed = pct >= 60;

    let html = `
      <div class="max-w-3xl mx-auto space-y-8 animate-fadeIn pb-16">
        <div class="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-3xl p-8 text-center space-y-5 shadow-lg">
          <div class="text-7xl">${passed ? '🏆' : '📝'}</div>
          <h1 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">
            ${passed ? 'გილოცავთ! თქვენ წარმატებით ჩააბარეთ A1 გამოცდა!' : 'გამოცდა ვერ ჩაბარდა'}
          </h1>
          <div class="text-5xl font-black ${passed ? 'text-emerald-600' : 'text-rose-600'}">
            ${score} / ${total} (${pct}%)
          </div>
          <p class="text-xs md:text-sm text-slate-600 dark:text-slate-400 max-w-md mx-auto leading-relaxed">
            ${passed
              ? 'თქვენ მიაღწიეთ გერმანული ენის A1 დონის სასერტიფიკატო სტანდარტს! ქვემოთ შეგიძლიათ იხილოთ და ამობეჭდოთ თქვენი ოფიციალური დიპლომი.'
              : 'სამწუხაროდ 60%-იანი ბარიერი ვერ გადაილახა. გირჩევთ კიდევ ერთხელ გაიმეოროთ გაკვეთილები და სცადოთ ხელახლა.'}
          </p>

          <div class="flex justify-center gap-3">
            <button onclick="window.DeutschApp.retakeExam()" class="px-5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-600 font-extrabold text-xs text-slate-700 dark:text-slate-300 hover:bg-slate-100 transition">
              🔄 ხელახლა ჩაბარება
            </button>
            ${passed ? `
              <button onclick="window.print()" class="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-xs shadow-md transition flex items-center gap-2">
                <span>🖨️ დიპლომის ბეჭდვა</span>
              </button>
            ` : ''}
          </div>
        </div>

        ${passed ? `
          <!-- Printable Official Certificate -->
          <div id="certificate-print-area" class="bg-white border-8 border-double border-slate-900 p-10 rounded-2xl text-center space-y-6 shadow-2xl text-slate-900">
            <div class="flex items-center justify-center gap-3">
              <span class="text-3xl">🇩🇪</span>
              <span class="text-xs font-black tracking-widest uppercase text-slate-500">DEUTSCH A1 • ZERTIFIKAT</span>
              <span class="text-3xl">🇬🇪</span>
            </div>

            <div class="space-y-1">
              <h2 class="text-3xl font-black tracking-tight uppercase">სერტიფიკატი</h2>
              <p class="text-xs font-bold text-slate-500 tracking-wider">A1 CEFR საერთაშორისო სტანდარტი</p>
            </div>

            <p class="text-xs text-slate-600 max-w-md mx-auto">
              ეძლევა სტუდენტს, რომელმაც წარმატებით დაასრულა გერმანული ენის A1 დონის სრული კურსი და ჩააბარა სასერტიფიკატო გამოცდა:
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

            <div class="pt-4 flex items-center justify-between max-w-lg mx-auto text-[11px] text-slate-500 font-semibold">
              <div class="text-left">
                <span class="block font-black text-slate-800">აკადემიური მოდული:</span>
                <span>Schritte & Menschen A1</span>
              </div>
              <div class="text-right">
                <span class="block font-black text-slate-800">სტატუსი:</span>
                <span class="text-emerald-600 font-black">VALID CERTIFICATE ✓</span>
              </div>
            </div>
          </div>
        ` : ''}
      </div>
    `;

    container.innerHTML = html;
  }

  // ==========================================================================
  // TAB 8: PROFILE & PROGRESS
  // ==========================================================================
  function renderProfile(container) {
    const completedCount = (userData.completedLessons || []).length;
    const masteredCount = (userData.masteredWords || []).length;
    const favCount = (userData.favoriteWords || []).length;

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
                <p class="text-xs text-slate-500 font-medium">გერმანული A1 • სტატისტიკა, პროგრესი და მიღწევები</p>
              </div>
            </div>

            <button onclick="window.DeutschApp.openProModal()" class="px-4 py-2 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-black text-xs shadow-md transition hover:scale-105 active:scale-95">
              💎 გამოწერის მართვა
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
          <h2 class="text-lg font-black text-slate-900 dark:text-white">გაკვეთილების შეფასებები</h2>
          <div class="space-y-3">
            ${window.GERMAN_A1_DATA.lessons.map(l => {
              const isComp = (userData.completedLessons || []).includes(l.id);
              const score = (userData.lessonScores || {})[l.id];
              return `
                <div class="flex items-center justify-between p-3.5 rounded-2xl border border-slate-100 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-700/20 transition">
                  <div class="flex items-center gap-3">
                    <span class="text-2xl p-2 bg-slate-50 dark:bg-slate-700 rounded-xl">${l.icon}</span>
                    <div>
                      <p class="font-extrabold text-xs md:text-sm text-slate-900 dark:text-white">${l.title_ka}</p>
                      <p class="text-[11px] text-slate-400 italic">${l.title_de}</p>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    ${isComp ? `
                      <span class="text-xs font-black text-emerald-600 bg-emerald-50 dark:bg-emerald-950/40 px-3 py-1 rounded-full">
                        ✓ ${score || 100}%
                      </span>
                    ` : `
                      <span class="text-xs font-bold text-slate-400 bg-slate-100 dark:bg-slate-700 px-3 py-1 rounded-full">
                        გაუვლელი
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
  // PRO SUBSCRIPTION MODAL (COMMERCIAL PRODUCT EXPERIENCE)
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
              💎 Deutsch A1 Pro Subscription
            </span>
            <h2 class="text-2xl md:text-3xl font-black text-slate-900 dark:text-white">
              სრული შეუზღუდავი წვდომა
            </h2>
            <p class="text-xs text-slate-500 font-medium max-w-md mx-auto">
              დაეუფლეთ გერმანულ ენას Goethe-Institut-ისა და გერმანული უნივერსიტეტების სტანდარტით
            </p>
          </div>

          <!-- Subscription Plans Grid -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            
            <!-- Tier 1: Free Starter -->
            <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-700 text-center flex flex-col justify-between">
              <div>
                <span class="text-xs font-bold text-slate-400 block mb-1">Starter</span>
                <div class="text-xl font-black text-slate-900 dark:text-white mb-2">უფასო</div>
                <ul class="text-[11px] text-slate-600 dark:text-slate-400 space-y-1.5 text-left mb-4">
                  <li>✓ 10 გაკვეთილის თეორია</li>
                  <li>✓ საბაზისო ტესტები</li>
                  <li>✓ Web Audio გაჟღერება</li>
                </ul>
              </div>
              <span class="text-[10px] text-slate-400 block font-bold">საბაზისო წვდომა</span>
            </div>

            <!-- Tier 2: Pro Annual (Featured) -->
            <div class="p-4 rounded-2xl border-2 border-amber-400 bg-amber-50/40 dark:bg-amber-950/20 text-center flex flex-col justify-between relative pro-glow">
              <span class="absolute -top-3 left-1/2 -translate-x-1/2 px-2.5 py-0.5 bg-amber-400 text-slate-950 font-black text-[9px] uppercase rounded-full">
                ყველაზე პოპულარული
              </span>
              <div>
                <span class="text-xs font-black text-amber-700 dark:text-amber-300 block mb-1">PRO Premium</span>
                <div class="text-2xl font-black text-slate-900 dark:text-white mb-2">₾29 <span class="text-xs font-normal text-slate-400">/წელი</span></div>
                <ul class="text-[11px] text-slate-700 dark:text-slate-300 space-y-1.5 text-left mb-4 font-medium">
                  <li>✓ 734+ Goethe A1 ლექსიკა</li>
                  <li>✓ Hörverstehen (აუდიო გაგება)</li>
                  <li>✓ Lückentext ჭკვიანი ტრენერი</li>
                  <li>✓ der/die/das ტრენერი (431)</li>
                  <li>✓ Satzbau სინტაქსი</li>
                  <li>✓ ოფიციალური დიპლომი</li>
                </ul>
              </div>
              <button onclick="window.DeutschApp.activatePro('pro_annual')" class="w-full py-2 rounded-xl bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 font-black text-xs shadow-md transition active:scale-95">
                ${userData.isPro ? 'აქტიურია ✓' : 'გააქტიურება ⚡'}
              </button>
            </div>

            <!-- Tier 3: Lifetime Pro -->
            <div class="p-4 rounded-2xl border border-slate-200 dark:border-slate-700 text-center flex flex-col justify-between">
              <div>
                <span class="text-xs font-bold text-purple-600 block mb-1">Lifetime Pro</span>
                <div class="text-xl font-black text-slate-900 dark:text-white mb-2">₾149 <span class="text-xs font-normal text-slate-400">ერთჯერადად</span></div>
                <ul class="text-[11px] text-slate-600 dark:text-slate-400 space-y-1.5 text-left mb-4">
                  <li>✓ სამუდამო სრული წვდომა</li>
                  <li>✓ ყველა A1 მოდული & ტესტი</li>
                  <li>✓ მომავალი A2 მოდულები</li>
                  <li>✓ პრიორიტეტული მხარდაჭერა</li>
                </ul>
              </div>
              <button onclick="window.DeutschApp.activatePro('lifetime')" class="w-full py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs shadow transition active:scale-95">
                ულიმიტო წვდომა
              </button>
            </div>

          </div>

          <!-- Feature comparison footer -->
          <div class="p-4 bg-slate-50 dark:bg-slate-700/30 rounded-2xl border border-slate-100 dark:border-slate-700 text-xs text-slate-600 dark:text-slate-300 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-base">🛡️</span>
              <span>100% გარანტია • მუშაობს ლოკალურად ოფლაინში • შეუზღუდავი გამოყენება</span>
            </div>
            <button onclick="window.DeutschApp.toggleProDemo()" class="text-[11px] font-bold text-blue-600 hover:underline">
              PRO სტატუსის გადართვა (${userData.isPro ? 'ჩართულია' : 'გამორთულია'})
            </button>
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

  function activatePro(tier) {
    userData.isPro = true;
    userData.subscriptionTier = tier;
    saveUserData();
    playChime('fanfare');
    showToast('გილოცავთ! PRO გამოწერა წარმატებით გააქტიურდა! 🌟');
    closeProModal();
    if (state.currentTab === 'profile') {
      renderProfile(document.getElementById('main-content'));
    }
  }

  function toggleProDemo() {
    userData.isPro = !userData.isPro;
    saveUserData();
    showToast(`PRO რეჟიმი: ${userData.isPro ? 'ჩართულია ⭐' : 'გათიშულია'}`);
    closeProModal();
  }

  // --- Global Public Interface for inline HTML events ---
  window.DeutschApp = {
    setTab,
    speak: speakGerman,

    // Pro Modal
    openProModal,
    closeProModal,
    activatePro,
    toggleProDemo,

    // Lessons
    openLesson: function (id) {
      state.selectedLessonId = id;
      setTab('lesson-detail');
    },
    switchLessonSubtab,
    toggleSequentialDialogue,
    trainLessonFlashcards: function (lessonId) {
      state.flashcardLessonFilter = String(lessonId);
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
                ${w.article ? `<span class="text-[11px] font-black px-2 py-0.5 rounded-md ${badgeClass}">${w.article}</span>` : ''}
                <span class="font-extrabold text-sm text-slate-900 dark:text-white truncate">${w.word}</span>
                ${w.plural ? `<span class="text-[11px] text-slate-400 font-normal">(${w.plural})</span>` : ''}
              </div>
              <p class="text-xs font-medium text-slate-600 dark:text-slate-300 truncate">${w.georgian}</p>
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
    // MC handlers
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
        addXP(10);
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

    // FIB handlers
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
        addXP(10);
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

    // Listening handlers
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
        addXP(10);
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

    // Flashcards
    onFlashcardLessonFilter: function (filterVal) {
      state.flashcardLessonFilter = filterVal;
      initFlashcards();
      renderFlashcards(document.getElementById('main-content'));
    },
    flipFlashcard: function () {
      state.flashcardFlipped = !state.flashcardFlipped;
      const el = document.getElementById('flashcard-inner-box');
      if (el) el.classList.toggle('is-flipped', state.flashcardFlipped);
    },
    flashcardAction: function (known) {
      const current = state.flashcardList[state.flashcardIndex];
      if (known) {
        userData.masteredWords = userData.masteredWords || [];
        if (!userData.masteredWords.includes(current.id)) {
          userData.masteredWords.push(current.id);
          addXP(5);
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
        addXP(5);

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
        addXP(15);
        speakGerman(userStr);
        showToast('წინადადება სრულიად სწორია! 🎉');
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

    // Exam
    onExamAnswer: function (qId, ansIdx) {
      state.examUserAnswers[qId] = ansIdx;
    },
    submitExam: function () {
      const questions = window.GERMAN_A1_DATA.final_exam_questions || [];
      let score = 0;
      questions.forEach(q => {
        if (state.examUserAnswers[q.id] === q.answer) {
          score += 1;
        }
      });
      state.examScore = score;
      state.examSubmitted = true;
      const pct = Math.round((score / questions.length) * 100);
      if (pct >= 60) {
        playChime('fanfare');
        addXP(100);
      } else {
        playChime('wrong');
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

    // Profile
    resetAllProgress: function () {
      if (confirm('ნამდვილად გსურთ მთლიანი პროგრესის წაშლა?')) {
        localStorage.removeItem(STORAGE_KEY);
        userData = {
          xp: 0,
          streak: 1,
          completedLessons: [],
          lessonScores: {},
          masteredWords: [],
          favoriteWords: [],
          isPro: true
        };
        saveUserData();
        setTab('profile');
        showToast('პროგრესი გასუფთავდა.');
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
