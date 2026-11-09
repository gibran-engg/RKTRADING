/*
 * R.K. Trading: site behaviour (vanilla JavaScript, no build step)
 * ------------------------------------------------------------------
 * 1. Header & mobile navigation
 * 2. Contact details from config.js (top bar, footer, Contact page, WhatsApp button)
 * 3. Enquiry forms: validation, demo mode, Google Sheets submission, product pre-fill
 * 4. Footer year
 *
 * Page content lives in the HTML files, so pages are readable without JavaScript.
 * Language switching is in i18n.js. User-facing strings here go through t() so they can be translated.
 */
(function () {
  'use strict';

  var config = window.RK_CONFIG || {};

  function t(key, fallback) {
    return window.RK_I18N ? window.RK_I18N.t(key, fallback) : fallback;
  }

  initNavigation();
  initContactDetails();
  initForms();
  initFooterYear();
  initReveal();

  /* 5. Scroll reveal ------------------------------------------------------ */
  // Content fades up as it enters the screen. Skipped for visitors who prefer reduced
  // motion. The .reveal classes are removed once an element has finished, so hover
  // effects on it behave normally afterwards.
  function initReveal() {
    if (reducedMotion() || !('IntersectionObserver' in window)) return;

    // [container, children]: children appear one after another
    var groups = [
      ['.card-grid', '.card-cat'], ['.why-grid', '.why-card'], ['.process-grid', '.process-card'],
      ['.steps-row', 'li'], ['.badge-row', '.badge'], ['.trust-grid', '.trust-item'], ['.faq', '.faq-item']
    ];
    // single elements
    var singles = ['.section-heading', '.subhead', '.quote-section .prose', '.quote-card', '.trade-map', '.trade-lists',
      '.cat', '.owner-card', '.reg-table', '.next-steps', '.contact-details', '.form-panel', '.split > .prose',
      '.reg-split > div', '.cta-inner', '.footer-main > div'];

    var targets = [];
    function mark(el, delay) {
      if (el.classList.contains('reveal') || el.closest('.reveal') || el.closest('.hero')) return;
      el.classList.add('reveal');
      el.style.setProperty('--d', delay + 'ms');
      targets.push(el);
    }
    groups.forEach(function (g) {
      document.querySelectorAll(g[0]).forEach(function (box) {
        Array.prototype.forEach.call(box.querySelectorAll(':scope > ' + g[1]), function (el, i) { mark(el, Math.min(i, 6) * 80); });
      });
    });
    singles.forEach(function (sel) {
      document.querySelectorAll(sel).forEach(function (el, i) { mark(el, 0); });
    });
    if (!targets.length) return;

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        observer.unobserve(el);
        el.classList.add('is-in');
        var wait = 900 + (parseInt(el.style.getPropertyValue('--d'), 10) || 0);
        setTimeout(function () {
          el.classList.remove('reveal', 'is-in');
          el.style.removeProperty('--d');
        }, wait);
      });
    }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
    targets.forEach(function (el) { observer.observe(el); });
  }

  /* 1. Header & mobile navigation ---------------------------------------- */
  function initNavigation() {
    var header = document.querySelector('[data-header]');
    var toggle = document.querySelector('[data-menu-toggle]');
    var nav = document.querySelector('[data-nav]');
    if (!header || !toggle || !nav) return;

    function isOpen() { return nav.classList.contains('is-open'); }
    function setOpen(open) {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? t('nav.menuClose', 'Close menu') : t('nav.menuOpen', 'Open menu'));
    }

    toggle.addEventListener('click', function () { setOpen(!isOpen()); });

    // Close after choosing a link, on Escape, on a click outside the header, and when the
    // window grows back to the desktop layout. (The language buttons keep the menu open.)
    nav.addEventListener('click', function (event) {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && isOpen()) { setOpen(false); toggle.focus(); }
    });
    document.addEventListener('click', function (event) {
      if (isOpen() && !header.contains(event.target)) setOpen(false);
    });
    window.matchMedia('(max-width: 980px)').addEventListener('change', function () { setOpen(false); });
    document.addEventListener('rk:langchange', function () { setOpen(isOpen()); });

    // Soft shadow under the sticky header once the page has scrolled, plus a thin progress line.
    var ticking = false;
    function updateShadow() {
      ticking = false;
      header.classList.toggle('is-scrolled', window.scrollY > 8);
      var max = document.documentElement.scrollHeight - window.innerHeight;
      header.style.setProperty('--scroll', max > 0 ? Math.min(1, window.scrollY / max).toFixed(4) : 0);
    }
    updateShadow();
    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(updateShadow); }
    }, { passive: true });
  }

  /* 2. Contact details ---------------------------------------------------- */
  function initContactDetails() {
    var contact = config.contact || {};

    function hrefFor(key, value) {
      if (key === 'phone') return 'tel:' + value.replace(/[^\d+]/g, '');
      if (key === 'email') return 'mailto:' + value;
      if (key === 'whatsapp') return 'https://wa.me/' + value.replace(/\D/g, '');
      if (key === 'address') return 'https://www.google.com/maps/search/?api=1&query=' + encodeURIComponent(value);
      return null;
    }

    document.querySelectorAll('[data-contact]').forEach(function (el) {
      var key = el.getAttribute('data-contact');
      var value = String(contact[key] || '').trim();

      if (!value) {
        // Not provided yet: elements marked data-hide-empty stay hidden; others keep their placeholder text.
        var li = el.closest('li');
        if (el.hasAttribute('data-hide-empty') && li && li.children.length === 1) li.hidden = true;
        return;
      }

      el.hidden = false;
      var textEl = el.hasAttribute('data-contact-text') ? el : el.querySelector('[data-contact-text]');
      if (textEl) {
        textEl.removeAttribute('data-i18n'); // a real value is not translated
        textEl.textContent = key === 'whatsapp' ? '+' + value.replace(/\D/g, '') : value;
      }
      if (el.tagName === 'A') {
        var href = hrefFor(key, value);
        if (href) el.setAttribute('href', href);
        if (key === 'whatsapp' || key === 'address') { el.setAttribute('target', '_blank'); el.setAttribute('rel', 'noopener'); }
      }
    });

    // Placeholders such as the generic "Mumbai, India" line give way to the real value.
    document.querySelectorAll('[data-hide-if-contact]').forEach(function (el) {
      if (String(contact[el.getAttribute('data-hide-if-contact')] || '').trim()) el.hidden = true;
    });
  }

  /* 3. Enquiry forms ------------------------------------------------------ */
  function initForms() {
    var endpoint = String(config.enquiryEndpoint || '').trim();
    // Option A: Apps Script URL (enquiryEndpoint). Option B: a Google Form (googleForm). Form wins if both are set.
    var gform = config.googleForm || {};
    var gformAction = String(gform.action || '').trim();
    var useGoogleForm = gformAction !== '' && !!gform.fields;
    var demoMode = endpoint === '' && !useGoogleForm;
    // No endpoint yet AND the site is on a real host: never fake a success (that would silently lose
    // the enquiry). Show no "demo" wording and point the visitor to phone / WhatsApp / email instead.
    var onDevHost = /^(localhost|127\.0\.0\.1|\[::1\]|)$/.test(location.hostname) || /\.(localhost|test)$/.test(location.hostname);
    var unconfigured = demoMode && !onDevHost;
    var timeoutMs = Number(config.requestTimeoutMs) || 20000;

    // Sent to Google Sheets, plus "page". Must match FIELDS in the Apps Script (google-sheets-setup.md).
    var FIELDS = ['name', 'email', 'company', 'country', 'phone', 'type', 'interest', 'quantity', 'message', 'language'];
    var EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    document.querySelectorAll('[data-enquiry-wrap]').forEach(setUp);

    function setUp(wrap) {
      var form = wrap.querySelector('[data-enquiry-form]');
      var success = wrap.querySelector('[data-enquiry-success]');
      if (!form || !success) return;

      var submitButton = form.querySelector('[data-submit]');
      var submitLabel = form.querySelector('[data-submit-label]');
      var errorBox = form.querySelector('[data-form-error]');
      var privacyNote = form.querySelector('[data-form-note]');
      var demoNote = form.querySelector('[data-demo-note]');
      var demoSuccess = success.querySelector('[data-demo-success]');
      var successTitle = success.querySelector('[data-success-title]');
      var againButton = success.querySelector('[data-enquiry-again]');
      var interest = form.elements.namedItem('interest');
      var message = form.elements.namedItem('message');
      var nameField = form.elements.namedItem('name');
      var checked = Array.prototype.slice.call(form.querySelectorAll('input[required], input[type="email"]'));
      var sending = false;

      // Demo mode: no endpoint set yet, so nothing is sent. Say so, on the form and on the success screen.
      if (demoMode && !unconfigured) {
        if (privacyNote) privacyNote.hidden = true;
        if (demoNote) demoNote.hidden = false;
        if (demoSuccess) demoSuccess.hidden = false;
      }

      /* Validation: inline messages instead of the browser's default bubbles. */
      function errorFor(input) {
        var value = input.value.trim();
        if (input.required && value === '') {
          if (input.name === 'name') return t('js.err.name', 'Please enter your name.');
          if (input.name === 'email') return t('js.err.email', 'Please enter your business email.');
          if (input.name === 'country') return t('js.err.country', 'Please enter your country.');
          return t('js.err.required', 'This field is required.');
        }
        if (input.type === 'email' && value !== '' && !EMAIL_PATTERN.test(value)) {
          return t('js.err.emailFormat', 'Please enter a valid email address, e.g. you@company.com.');
        }
        return '';
      }

      function setFieldError(input, text) {
        var field = input.closest('.field');
        var el = field ? field.querySelector('.field-error') : null;
        if (text) {
          if (!el && field) {
            el = document.createElement('p');
            el.className = 'field-error';
            el.id = input.id + '-error';
            field.appendChild(el);
          }
          if (el) { el.textContent = text; input.setAttribute('aria-describedby', el.id); }
          input.setAttribute('aria-invalid', 'true');
        } else {
          if (el) el.remove();
          input.removeAttribute('aria-invalid');
          input.removeAttribute('aria-describedby');
        }
      }

      function validate() {
        var firstInvalid = null;
        checked.forEach(function (input) {
          input.value = input.value.trim();
          var text = errorFor(input);
          setFieldError(input, text);
          if (text && !firstInvalid) firstInvalid = input;
        });
        if (firstInvalid) firstInvalid.focus();
        return firstInvalid === null;
      }

      checked.forEach(function (input) {
        // Check a field once the visitor leaves it, then re-check live while they fix it.
        input.addEventListener('blur', function () {
          if (input.value.trim() !== '' || input.hasAttribute('aria-invalid')) setFieldError(input, errorFor(input));
        });
        input.addEventListener('input', function () {
          if (input.hasAttribute('aria-invalid')) setFieldError(input, errorFor(input));
        });
      });

      /* "Request a quote" links on category cards arrive as contact.html?interest=<slug> */
      if (wrap.hasAttribute('data-prefill')) prefillFromUrl();
      function prefillFromUrl() {
        var slug = new URLSearchParams(location.search).get('interest');
        if (!slug || !interest) return;
        var option = Array.prototype.find.call(interest.options, function (o) { return o.getAttribute('data-slug') === slug; });
        if (!option) return;
        interest.value = option.value;
        if (message && slug !== 'other' && message.value.trim() === '') {
          message.value = "I'm interested in: " + option.value + '.\n';
        }
        var field = interest.closest('.field');
        if (field) {
          field.classList.add('is-highlighted');
          interest.addEventListener('animationend', function () { field.classList.remove('is-highlighted'); }, { once: true });
        }
      }

      /* Submission */
      form.addEventListener('submit', function (event) {
        event.preventDefault();
        if (sending) return;
        hideError();
        if (!validate()) return;

        var data = new FormData(form);

        // Honeypot filled in: almost certainly a bot. Show success, send nothing.
        if (String(data.get('website') || '').trim() !== '') { showSuccess(); return; }

        var payload = new URLSearchParams();
        FIELDS.forEach(function (name) {
          var value = name === 'language' ? document.documentElement.lang || 'en' : String(data.get(name) || '').trim();
          payload.append(name, value);
        });
        payload.append('page', window.location.href);

        if (unconfigured) { showError(unconfiguredMessage()); return; }

        setSending(true);
        var request;
        if (demoMode) {
          console.info('[R.K. Trading] Demo mode: enquiry NOT sent. This is what would go to Google Sheets:', Object.fromEntries(payload));
          request = new Promise(function (resolve) { setTimeout(resolve, 600); }); // lets you see the "Sending…" state
        } else if (useGoogleForm) {
          request = postWithTimeout(gformAction, toGoogleForm(payload), timeoutMs);
        } else {
          request = postWithTimeout(endpoint, payload, timeoutMs);
        }
        request.then(showSuccess).catch(function () {
          showError(t('js.err.send', 'Sorry, we could not send your enquiry. Please check your connection and try again.'));
        }).then(function () { setSending(false); });
      });

      if (againButton) againButton.addEventListener('click', function () { showForm(true); });

      // Rename our field names to the form's entry.NNNN ids. Text starting with = + - @ gets a leading
      // apostrophe so it cannot run as a formula in the responses sheet.
      function toGoogleForm(p) {
        var out = new URLSearchParams();
        Object.keys(gform.fields).forEach(function (key) {
          var id = gform.fields[key];
          if (!id || !p.has(key)) return;
          var v = p.get(key);
          out.append(id, /^[=+\-@]/.test(v) ? "'" + v : v);
        });
        return out;
      }

      function unconfiguredMessage() {
        var c = config.contact || {};
        var how = [c.phone, c.email].filter(Boolean).join(' · ');
        return t('js.err.unconfigured', 'Online enquiries are temporarily unavailable. Please contact us directly:') + (how ? ' ' + how : '');
      }

      function postWithTimeout(url, body, ms) {
        var controller = new AbortController();
        var timer = setTimeout(function () { controller.abort(); }, ms);
        // mode "no-cors": Apps Script sends no CORS headers, so the reply is opaque. A resolved
        // fetch means the request left the browser; check the sheet to confirm it arrived.
        return fetch(url, { method: 'POST', mode: 'no-cors', body: body, signal: controller.signal })
          .then(function (r) { clearTimeout(timer); return r; }, function (e) { clearTimeout(timer); throw e; });
      }

      function setSending(isSending) {
        sending = isSending;
        if (submitButton) submitButton.disabled = isSending;
        if (submitLabel) submitLabel.textContent = isSending ? t('form.sending', 'Sending…') : t('form.send', 'Send enquiry');
        form.setAttribute('aria-busy', String(isSending));
      }

      function showSuccess() {
        form.reset();
        checked.forEach(function (input) { setFieldError(input, ''); });
        form.hidden = true;
        success.hidden = false;
        if (successTitle) successTitle.focus({ preventScroll: true });
        success.scrollIntoView({ block: 'nearest', behavior: reducedMotion() ? 'auto' : 'smooth' });
      }

      function showForm(moveFocus) {
        success.hidden = true;
        form.hidden = false;
        hideError();
        if (moveFocus && nameField) nameField.focus();
      }

      function showError(text) {
        if (!errorBox) return;
        errorBox.textContent = text;
        errorBox.hidden = false;
      }

      function hideError() { if (errorBox) errorBox.hidden = true; }
    }
  }

  /* 4. Footer year -------------------------------------------------------- */
  function initFooterYear() {
    var year = String(new Date().getFullYear());
    document.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = year; });
  }

  function reducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
})();
