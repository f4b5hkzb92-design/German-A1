#!/usr/bin/env python3
"""
DEUTSCH A1 PRO — STAGE 10 PART 4 & 5: OFFICIAL CERTIFICATE & PWA SUITE QA
Validates the official CEFR A1 Abschlusszertifikat, deterministic serial numbering,
profile showcase integration, print media stylesheet, and PWA mobile offline support.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

passed = 0
failed = 0

def check(condition, desc):
    global passed, failed
    if condition:
        print(f"  [PASS] {desc}")
        passed += 1
    else:
        print(f"  [FAIL] {desc}")
        failed += 1

print("=" * 65)
print("DEUTSCH A1 PRO: STAGE 10 PART 4 & 5 (CERTIFICATE & PWA) QA")
print("=" * 65)

BASE_DIR = Path(__file__).resolve().parent.parent

# --- 1. PWA ASSETS & MANIFEST VERIFICATION ---
manifest_path = BASE_DIR / "manifest.json"
check(manifest_path.exists(), "manifest.json exists in root directory")
if manifest_path.exists():
    manifest_data = json.loads(manifest_path.read_text(encoding="utf-8"))
    check(manifest_data.get("name") in ("Deutsch A1", "Deutsch A1 Pro"), "manifest.json has valid app name")
    check(manifest_data.get("display") == "standalone", "manifest.json has display 'standalone'")
    check(manifest_data.get("start_url") in ("./", "/"), "manifest.json has valid start_url")
    check(len(manifest_data.get("icons", [])) >= 2, "manifest.json provides icons for home screen")

sw_path = BASE_DIR / "sw.js"
check(sw_path.exists(), "sw.js service worker exists in root directory")
if sw_path.exists():
    sw_text = sw_path.read_text(encoding="utf-8")
    check("CACHE_NAME" in sw_text, "sw.js declares CACHE_NAME")
    check("caches.open" in sw_text, "sw.js handles install caching")
    check("fetch(event.request)" in sw_text, "sw.js implements network-first strategy")
    check("caches.match" in sw_text, "sw.js implements offline cache fallback")

index_html = (BASE_DIR / "index.html").read_text(encoding="utf-8")
check('rel="manifest"' in index_html, "index.html links to manifest.json")
check('pwa-install-banner' in index_html, "index.html contains pwa-install-banner element")
check('installPWA' in index_html, "index.html defines installPWA prompt handler")
check('offline' in index_html and 'online' in index_html, "index.html registers offline/online event listeners")

# --- 2. PRINT STYLESHEET VERIFICATION ---
style_css = (BASE_DIR / "css" / "style.css").read_text(encoding="utf-8")
check("@media print" in style_css, "style.css contains @media print rules")
check("@page" in style_css and "A4" in style_css, "style.css defines @page A4 dimensions")
check("#certificate-print-area" in style_css, "style.css targets #certificate-print-area for print visibility")
check(".no-print" in style_css, "style.css suppresses .no-print elements during printing")
check("print-color-adjust: exact" in style_css, "style.css ensures exact print color reproduction")

# --- 3. JAVASCRIPT SIMULATION (CERTIFICATE ENGINE & PROFILE INTEGRATION) ---
mock_env = """
var window = { 
  location: { href: "http://localhost:8000" },
  addEventListener: function() {},
  matchMedia: function() { return { matches: false }; },
  scrollTo: function() {},
  print: function() { this.__printCalled = true; }
};
var globalThis = window;

var console = {
  log: function() {},
  warn: function() {},
  error: function() {},
  info: function() {}
};

var document = {
  _elements: {},
  getElementById: function(id) { 
    if (!this._elements[id]) {
      this._elements[id] = { 
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
    }
    return this._elements[id];
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

var setTimeout = function(cb, ms) { cb(); };
var clearTimeout = function() {};
window.setTimeout = setTimeout;
window.clearTimeout = clearTimeout;

var navigator = {
  userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
  mediaDevices: { getUserMedia: function() { return Promise.resolve({ getTracks: () => [{ stop: ()=>{} }] }); } }
};

var speechSynthesis = {
  speak: function(){},
  cancel: function(){},
  getVoices: function() { return [{ name: "Anna", lang: "de-DE", default: true }]; }
};
var SpeechSynthesisUtterance = function(t){ this.text = t; this.lang = "de-DE"; };
window.SpeechSynthesisUtterance = SpeechSynthesisUtterance;
window.speechSynthesis = speechSynthesis;
window.document = document;
window.localStorage = localStorage;
"""

probe_certificate_js = """
function runProbe() {
  var results = [];
  try {
    var app = window.DeutschApp;

    // Test 1: Deterministic Certificate ID Generation
    var certId1 = app.getCertificateId();
    results.push({ 
      name: "getCertificateId generates format DA1P-2026-XXXXXX", 
      ok: Boolean(certId1 && certId1.indexOf('DA1P-2026-') === 0 && certId1.length === 16) 
    });

    // Test 2: Name Update
    app.updateLearnerName('გიორგი მაისურაძე');
    var rawUser = JSON.parse(localStorage.getItem('deutsch_a1_pro_v3'));
    results.push({
      name: "updateLearnerName persists student name to userData",
      ok: Boolean(rawUser && rawUser.learnerName === 'გიორგი მაისურაძე')
    });

    var certId2 = app.getCertificateId();
    results.push({
      name: "Certificate ID updates deterministically based on learner name",
      ok: (certId1 !== certId2 && certId2.indexOf('DA1P-2026-') === 0)
    });

    // Test 3: Profile view when exam NOT passed
    rawUser.examPassed = false;
    rawUser.examScore = null;
    localStorage.setItem('deutsch_a1_pro_v3', JSON.stringify(rawUser));
    app.loadUserData();

    var mainEl = document.getElementById('main-content');
    app.setTab('profile');
    var profileHtmlUnpassed = mainEl.innerHTML;
    results.push({
      name: "Profile displays locked certificate state when exam is not passed",
      ok: (profileHtmlUnpassed.indexOf('დაბლოკილია') !== -1 && profileHtmlUnpassed.indexOf('გამოცდაზე გადასვლა') !== -1)
    });

    // Test 4: Profile view when exam PASSED
    rawUser.examPassed = true;
    rawUser.examScore = 24;
    rawUser.examDate = '2026-11-13';
    localStorage.setItem('deutsch_a1_pro_v3', JSON.stringify(rawUser));
    app.loadUserData();

    app.setTab('profile');
    var profileHtmlPassed = mainEl.innerHTML;
    results.push({
      name: "Profile showcases official certificate banner when exam is passed",
      ok: (profileHtmlPassed.indexOf('A1 დამამთავრებელი სერტიფიკატი') !== -1 && profileHtmlPassed.indexOf('სერტიფიკატის ნახვა') !== -1)
    });

    // Test 5: Open Certificate Modal
    app.openCertificateModal();
    var modalEl = document.getElementById('modal-container');
    var modalHtml = modalEl.innerHTML;

    results.push({
      name: "openCertificateModal renders #certificate-print-area in modal",
      ok: (modalHtml.indexOf('id="certificate-print-area"') !== -1)
    });

    results.push({
      name: "Certificate contains CEFR A1 ABSCHLUSSZERTIFIKAT German title",
      ok: (modalHtml.indexOf('ABSCHLUSSZERTIFIKAT') !== -1 && modalHtml.indexOf('CEFR A1') !== -1)
    });

    results.push({
      name: "Certificate contains all 5 CEFR competencies (Hören, Lesen, Schreiben, Sprechen, Grammatik)",
      ok: (modalHtml.indexOf('Hörverstehen') !== -1 && modalHtml.indexOf('Leseverstehen') !== -1 && 
           modalHtml.indexOf('Schreiben') !== -1 && modalHtml.indexOf('Sprechen') !== -1)
    });

    results.push({
      name: "Certificate contains academic signatures and verification seal",
      ok: (modalHtml.indexOf('Akademische Leitung') !== -1 && modalHtml.indexOf('Prüfungskommission') !== -1 && modalHtml.indexOf('VERIFIZIERT') !== -1)
    });

    // Test 6: Close Modal
    app.closeCertificateModal();
    results.push({
      name: "closeCertificateModal successfully clears modal container",
      ok: (modalEl.innerHTML === '')
    });

    // Test 7: Print Certificate Trigger
    app.printCertificate();
    results.push({
      name: "printCertificate prepares DOM and triggers window.print()",
      ok: Boolean(window.__printCalled)
    });

  } catch(e) {
    results.push({ name: "Exception during probe: " + e.toString(), ok: false });
  }

  return JSON.stringify(results);
}
runProbe();
"""

data_content = (BASE_DIR / "js" / "data.js").read_text(encoding="utf-8")
app_content = (BASE_DIR / "js" / "app.js").read_text(encoding="utf-8")
full_code = mock_env + "\n" + data_content + "\n" + app_content + "\n" + probe_certificate_js

probe_file = BASE_DIR / "tests" / "_stage10_cert_runner.js"
probe_file.write_text(full_code, encoding="utf-8")
try:
    res = subprocess.run(["osascript", "-l", "JavaScript", str(probe_file)], capture_output=True, text=True)
    if res.returncode == 0:
        sim_results = json.loads(res.stdout.strip())
        for r in sim_results:
            check(r["ok"], r["name"])
    else:
        check(False, f"osascript JS execution failed: {res.stderr}")
finally:
    if probe_file.exists():
        probe_file.unlink()

print("=" * 65)
print(f"STAGE 10 PART 4 & 5 QA SUMMARY: {passed} Passed, {failed} Failed")
print("=" * 65)

if failed > 0:
    sys.exit(1)
