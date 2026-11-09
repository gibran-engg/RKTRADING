/*
 * R.K. Trading: language switching (English, 中文, العربية)
 * ------------------------------------------------------------------
 * English is the source text and lives in the HTML (good for search engines and for anyone
 * with JavaScript off). Chinese and Arabic live in assets/js/lang/zh.js and ar.js as
 * { key: 'translation' } and are loaded only when a visitor asks for them.
 *
 * Markup:
 *   data-i18n="key"                    replaces the element's text
 *   data-i18n-html="key"               replaces its HTML (for headings with <em> or links)
 *   data-i18n-attr="attr:key;attr:key" replaces attributes (placeholder, aria-label, content)
 *
 * A key missing from a dictionary falls back to the English already on the page.
 * The chosen language is remembered in localStorage and can be forced with ?lang=zh|ar|en.
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'rk-lang';
  var SUPPORTED = ['en', 'zh', 'ar'];
  var RTL = { ar: true };
  var root = document.documentElement;
  var script = document.currentScript;
  var base = script && script.src ? script.src.replace(/i18n\.js(\?.*)?$/, '') : 'assets/js/';

  var originals = new Map(); // element -> English text / html / attributes captured on first sight
  var current = 'en';
  var storageWorks = true;

  function stored() {
    try { return localStorage.getItem(STORAGE_KEY); } catch (e) { storageWorks = false; return null; }
  }
  function store(lang) {
    try { localStorage.setItem(STORAGE_KEY, lang); } catch (e) { storageWorks = false; }
  }
  function valid(lang) { return SUPPORTED.indexOf(lang) !== -1 ? lang : null; }
  function dictionary(lang) { return lang !== 'en' && window.RK_LANG ? window.RK_LANG[lang] || null : null; }

  function t(key, fallback) {
    var d = dictionary(current);
    return d && d[key] != null ? d[key] : fallback;
  }

  function pairs(el) {
    return (el.getAttribute('data-i18n-attr') || '').split(';').map(function (p) {
      var i = p.indexOf(':');
      return i > 0 ? { attr: p.slice(0, i).trim(), key: p.slice(i + 1).trim() } : null;
    }).filter(Boolean);
  }

  function collect() {
    document.querySelectorAll('[data-i18n],[data-i18n-html],[data-i18n-attr]').forEach(function (el) {
      if (originals.has(el)) return;
      var rec = {};
      if (el.hasAttribute('data-i18n')) rec.text = el.textContent;
      if (el.hasAttribute('data-i18n-html')) rec.html = el.innerHTML;
      if (el.hasAttribute('data-i18n-attr')) {
        rec.attrs = {};
        pairs(el).forEach(function (p) { rec.attrs[p.attr] = el.getAttribute(p.attr) || ''; });
      }
      originals.set(el, rec);
    });
  }

  function apply(lang) {
    var d = dictionary(lang);
    originals.forEach(function (rec, el) {
      if (!el.isConnected) return;
      var key;
      if (rec.text !== undefined && el.hasAttribute('data-i18n')) {
        key = el.getAttribute('data-i18n');
        el.textContent = d && d[key] != null ? d[key] : rec.text;
      }
      if (rec.html !== undefined && el.hasAttribute('data-i18n-html')) {
        key = el.getAttribute('data-i18n-html');
        el.innerHTML = d && d[key] != null ? d[key] : rec.html;
      }
      if (rec.attrs && el.hasAttribute('data-i18n-attr')) {
        pairs(el).forEach(function (p) {
          var v = d && d[p.key] != null ? d[p.key] : rec.attrs[p.attr];
          if (v !== undefined) el.setAttribute(p.attr, v);
        });
      }
    });

    current = lang;
    root.lang = lang;
    root.dir = RTL[lang] ? 'rtl' : 'ltr';
    document.querySelectorAll('[data-lang-switch] [data-lang]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(btn.getAttribute('data-lang') === lang));
    });
    keepLanguageInLinks(lang);
    root.classList.remove('i18n-pending');
    document.dispatchEvent(new CustomEvent('rk:langchange', { detail: { lang: lang } }));
  }

  // If the browser blocks storage, carry the language between pages in the URL instead.
  function keepLanguageInLinks(lang) {
    if (storageWorks) return;
    document.querySelectorAll('a[href]').forEach(function (a) {
      var href = a.getAttribute('href');
      if (!href || href.charAt(0) === '#' || /^[a-z][a-z0-9+.-]*:/i.test(href)) return;
      var url = new URL(href, location.href);
      url.searchParams.set('lang', lang);
      a.setAttribute('href', url.pathname.split('/').pop() + url.search + url.hash);
    });
  }

  function load(lang, done) {
    if (lang === 'en' || (window.RK_LANG && window.RK_LANG[lang])) { done(); return; }
    var s = document.createElement('script');
    s.src = base + 'lang/' + lang + '.js';
    s.onload = done;
    s.onerror = done; // couldn't load: stay on English text rather than break the page
    document.head.appendChild(s);
  }

  function setLanguage(lang, remember) {
    lang = valid(lang) || 'en';
    collect();
    load(lang, function () {
      if (remember !== false) store(lang);
      apply(lang);
    });
  }

  function init() {
    var fromUrl = valid(new URLSearchParams(location.search).get('lang'));
    var initial = fromUrl || valid(stored()) || 'en';
    collect();
    document.querySelectorAll('[data-lang-switch] [data-lang]').forEach(function (btn) {
      btn.addEventListener('click', function () { setLanguage(btn.getAttribute('data-lang')); });
    });
    if (initial === 'en') { apply('en'); return; }
    load(initial, function () { apply(initial); });
  }

  window.RK_I18N = {
    t: t,
    set: setLanguage,
    get lang() { return current; }
  };

  init();
})();
