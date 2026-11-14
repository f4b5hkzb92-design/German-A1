(function (global) {
  'use strict';

  const STORAGE_KEY = 'deutsch_a1_subscription_v1';
  const USAGE_KEY = 'deutsch_a1_daily_usage_v1';
  const DAILY_FREE_LIMIT = 20;

  const PLAN = {
    id: 'deutsch_a1_premium_monthly',
    title: 'Deutsch A1 Premium',
    priceGel: 5,
    priceLabel: '5 ₾ / თვეში',
    periodLabel: 'ყოველთვიური გამოწერა'
  };

  function getTodayKey() {
    return new Date().toISOString().slice(0, 10);
  }

  function loadSubscription() {
    try {
      const raw = global.localStorage ? global.localStorage.getItem(STORAGE_KEY) : null;
      if (!raw) return { active: false, expiresAt: 0, source: 'free' };
      const parsed = JSON.parse(raw);
      if (parsed && parsed.expiresAt && parsed.expiresAt > Date.now()) {
        return { active: true, expiresAt: parsed.expiresAt, source: parsed.source || 'store' };
      }
      return { active: false, expiresAt: 0, source: 'free' };
    } catch (e) {
      return { active: false, expiresAt: 0, source: 'free' };
    }
  }

  function saveSubscription(sub) {
    try {
      if (global.localStorage) {
        global.localStorage.setItem(STORAGE_KEY, JSON.stringify(sub));
      }
    } catch (e) {}
  }

  function loadUsage() {
    const today = getTodayKey();
    try {
      const raw = global.localStorage ? global.localStorage.getItem(USAGE_KEY) : null;
      if (raw) {
        const parsed = JSON.parse(raw);
        if (parsed && parsed.date === today) {
          return { date: today, count: Number(parsed.count) || 0 };
        }
      }
    } catch (e) {}
    return { date: today, count: 0 };
  }

  function saveUsage(usage) {
    try {
      if (global.localStorage) {
        global.localStorage.setItem(USAGE_KEY, JSON.stringify(usage));
      }
    } catch (e) {}
  }

  function isNativeApp() {
    return Boolean(global.Capacitor && typeof global.Capacitor.isNativePlatform === 'function' && global.Capacitor.isNativePlatform());
  }

  function isPremiumActive() {
    if (global.CapacitorBilling && typeof global.CapacitorBilling.isSubscribed === 'function') {
      return Boolean(global.CapacitorBilling.isSubscribed(PLAN.id));
    }
    return loadSubscription().active;
  }

  function shouldShowAds() {
    return !isPremiumActive();
  }

  function getRemainingFreeActions() {
    if (isPremiumActive()) return Infinity;
    const usage = loadUsage();
    return Math.max(0, DAILY_FREE_LIMIT - usage.count);
  }

  function consumeFreeAction() {
    if (isPremiumActive()) return { allowed: true, remaining: Infinity };
    const usage = loadUsage();
    if (usage.count >= DAILY_FREE_LIMIT) {
      return { allowed: false, remaining: 0 };
    }
    usage.count += 1;
    saveUsage(usage);
    renderAdBanner();
    return { allowed: true, remaining: Math.max(0, DAILY_FREE_LIMIT - usage.count) };
  }

  function getSubscriptionSummary() {
    const sub = loadSubscription();
    const active = isPremiumActive();
    const remaining = getRemainingFreeActions();
    return {
      plan: PLAN,
      active,
      expiresAt: sub.expiresAt,
      expiresFormatted: sub.expiresAt ? new Date(sub.expiresAt).toLocaleDateString('ka-GE') : null,
      dailyLimit: DAILY_FREE_LIMIT,
      remainingToday: remaining,
      adsEnabled: !active,
      isNative: isNativeApp()
    };
  }

  async function subscribeMonthly() {
    // Native StoreKit / Google Play Billing hook when wrapped in Capacitor
    if (global.CapacitorBilling && typeof global.CapacitorBilling.purchase === 'function') {
      const ok = await global.CapacitorBilling.purchase(PLAN.id);
      if (ok) {
        const nextMonth = Date.now() + 30 * 24 * 60 * 60 * 1000;
        saveSubscription({ active: true, expiresAt: nextMonth, source: 'native-store' });
        syncAdVisibility();
        return { ok: true, mode: 'native' };
      }
      return { ok: false, mode: 'native' };
    }

    // Web/preview mode activation (for testing UX before Capacitor store build)
    const nextMonth = Date.now() + 30 * 24 * 60 * 60 * 1000;
    saveSubscription({ active: true, expiresAt: nextMonth, source: 'web-preview' });
    syncAdVisibility();
    return { ok: true, mode: 'preview' };
  }

  async function restorePurchases() {
    if (global.CapacitorBilling && typeof global.CapacitorBilling.restore === 'function') {
      const restored = await global.CapacitorBilling.restore(PLAN.id);
      if (restored) {
        const nextMonth = Date.now() + 30 * 24 * 60 * 60 * 1000;
        saveSubscription({ active: true, expiresAt: nextMonth, source: 'native-restore' });
        syncAdVisibility();
        return { ok: true, restored: true };
      }
      return { ok: true, restored: false };
    }
    syncAdVisibility();
    return { ok: true, restored: isPremiumActive() };
  }

  function resetToFreeTier() {
    saveSubscription({ active: false, expiresAt: 0, source: 'free' });
    syncAdVisibility();
  }

  function syncAdVisibility() {
    if (global.CapacitorAdMob) {
      if (isPremiumActive() && typeof global.CapacitorAdMob.hideBanner === 'function') {
        global.CapacitorAdMob.hideBanner();
      } else if (!isPremiumActive() && typeof global.CapacitorAdMob.showBanner === 'function') {
        global.CapacitorAdMob.showBanner();
      }
    }
    renderAdBanner();
  }

  function renderAdBanner() {
    if (typeof document === 'undefined') return;
    const slot = document.getElementById('ad-banner-slot');
    if (!slot) return;

    if (!shouldShowAds()) {
      slot.classList.add('hidden');
      slot.innerHTML = '';
      return;
    }

    const remaining = getRemainingFreeActions();
    slot.classList.remove('hidden');
    slot.innerHTML = `
      <div class="max-w-7xl mx-auto px-4 py-2 flex flex-wrap items-center justify-between gap-2 text-xs">
        <div class="flex items-center gap-2 text-slate-600 dark:text-slate-300">
          <span class="px-1.5 py-0.5 rounded bg-slate-200 dark:bg-slate-700 text-[10px] font-black uppercase">AD</span>
          <span>უფასო რეჟიმი • დღიური ლიმიტი: <strong>${remaining}/${DAILY_FREE_LIMIT}</strong></span>
        </div>
        <button onclick="window.DeutschApp && window.DeutschApp.openProModal()" class="px-3 py-1 rounded-lg bg-amber-400 hover:bg-amber-300 text-slate-950 font-black text-[11px] transition">
          💎 Premium (5 ₾/თვე) — რეკლამის გარეშე
        </button>
      </div>
    `;
  }

  if (typeof document !== 'undefined') {
    document.addEventListener('DOMContentLoaded', () => {
      syncAdVisibility();
    });
  }

  global.DeutschBilling = {
    PLAN,
    DAILY_FREE_LIMIT,
    isPremiumActive,
    shouldShowAds,
    getRemainingFreeActions,
    consumeFreeAction,
    getSubscriptionSummary,
    subscribeMonthly,
    restorePurchases,
    resetToFreeTier,
    syncAdVisibility,
    renderAdBanner
  };
})(typeof window !== 'undefined' ? window : globalThis);
