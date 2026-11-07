/*
 * RK Trading: site behaviour (vanilla JavaScript, no build step)
 * ------------------------------------------------------------------
 * 1. Header & mobile navigation
 * 2. Active-section highlighting in the nav
 * 3. Product catalogue: category filters, search, enquiry shortcuts
 * 4. Enquiry form: validation, demo mode, Google Sheets submission
 * 5. Footer year
 *
 * All content lives in index.html, so the page is fully readable without
 * JavaScript; this file only adds interaction on top.
 */
(function () {
  'use strict';

  const config = window.RK_CONFIG || {};

  initNavigation();
  initActiveSection();
  initCatalogue();
  initEnquiryForm();
  initFooterYear();

  /* 1. Header & mobile navigation ---------------------------------------- */
  function initNavigation() {
    const header = document.querySelector('[data-header]');
    const toggle = document.querySelector('[data-menu-toggle]');
    const nav = document.querySelector('[data-nav]');
    if (!header || !toggle || !nav) return;

    const isOpen = () => nav.classList.contains('is-open');
    const setOpen = (open) => {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };

    toggle.addEventListener('click', () => setOpen(!isOpen()));

    // Close after choosing a link, on Escape, on a click outside the header,
    // and when the window grows back to the desktop layout.
    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && isOpen()) {
        setOpen(false);
        toggle.focus();
      }
    });
    document.addEventListener('click', (event) => {
      if (isOpen() && !header.contains(event.target)) setOpen(false);
    });
    window.matchMedia('(max-width: 860px)').addEventListener('change', () => setOpen(false));

    // Soft shadow under the sticky header once the page has scrolled.
    const updateShadow = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
    updateShadow();
    window.addEventListener('scroll', updateShadow, { passive: true });
  }

  /* 2. Active-section highlighting --------------------------------------- */
  function initActiveSection() {
    const links = Array.from(document.querySelectorAll('[data-nav] a[href^="#"]:not(.nav-cta)'));
    const sections = Array.from(document.querySelectorAll('main > section'));
    if (!links.length || !sections.length || !('IntersectionObserver' in window)) return;

    const linkById = new Map(links.map((link) => [link.getAttribute('href').slice(1), link]));

    const setActive = (id) => {
      const activeLink = linkById.get(id);
      links.forEach((link) => {
        const active = link === activeLink;
        link.classList.toggle('is-active', active);
        if (active) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    };

    // A thin band across the middle of the viewport: whichever section crosses
    // it is "current". Sections without a nav link clear the highlight.
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) setActive(entry.target.id);
      });
    }, { rootMargin: '-45% 0px -50% 0px' });

    sections.forEach((section) => observer.observe(section));
  }

  /* 3. Product catalogue ------------------------------------------------- */
  function initCatalogue() {
    const grid = document.querySelector('[data-product-grid]');
    if (!grid) return;

    const cards = Array.from(grid.querySelectorAll('.product-card'));
    const filterButtons = Array.from(document.querySelectorAll('[data-filter]'));
    const searchInput = document.querySelector('[data-search]');
    const emptyState = document.querySelector('[data-catalog-empty]');
    const status = document.querySelector('[data-catalog-status]');
    const resetButton = document.querySelector('[data-catalog-reset]');

    // Searchable text per card: everything a buyer might type, including the
    // collapsed "Product details" list, but not button labels.
    const SEARCHABLE = '.product-tag, .origin, h3, .product-desc, .chips, .examples, dl';
    const searchIndex = cards.map((card) =>
      normalise(Array.from(card.querySelectorAll(SEARCHABLE), (el) => el.textContent).join(' '))
    );

    let activeCategory = 'All';

    function applyFilters(announce) {
      // Every word must match somewhere in the card, so "red onion" and
      // "onion red" both work.
      const terms = normalise(searchInput ? searchInput.value : '').split(' ').filter(Boolean);
      let visibleCount = 0;

      cards.forEach((card, i) => {
        const inCategory = activeCategory === 'All' || card.dataset.category === activeCategory;
        const matchesSearch = terms.every((term) => searchIndex[i].includes(term));
        const visible = inCategory && matchesSearch;
        card.hidden = !visible;
        if (visible) visibleCount += 1;
      });

      if (emptyState) emptyState.hidden = visibleCount > 0;
      if (status && announce) {
        status.textContent = visibleCount === 0
          ? 'No matching products.'
          : `Showing ${visibleCount} of ${cards.length} product categories.`;
      }
    }

    function setCategory(category) {
      const known = filterButtons.some((button) => button.dataset.filter === category);
      activeCategory = known ? category : 'All';
      filterButtons.forEach((button) => {
        const active = button.dataset.filter === activeCategory;
        button.classList.toggle('is-active', active);
        button.setAttribute('aria-pressed', String(active));
      });
      applyFilters(true);
    }

    filterButtons.forEach((button) => {
      button.addEventListener('click', () => setCategory(button.dataset.filter));
    });

    if (searchInput) {
      searchInput.addEventListener('input', () => applyFilters(true));
      searchInput.addEventListener('search', () => applyFilters(true)); // native clear (×) button
    }

    if (resetButton) {
      resetButton.addEventListener('click', () => {
        if (searchInput) searchInput.value = '';
        setCategory('All');
        if (searchInput) searchInput.focus();
      });
    }

    // The three verticals in the intro strip jump to the portfolio pre-filtered.
    document.querySelectorAll('[data-filter-link]').forEach((link) => {
      link.addEventListener('click', () => {
        if (searchInput) searchInput.value = '';
        setCategory(link.dataset.filterLink);
      });
    });

    // Respect any value the browser restored into the search box.
    applyFilters(false);
  }

  function normalise(text) {
    return String(text)
      .toLowerCase()
      .normalize('NFD').replace(/[̀-ͯ]/g, '') // é -> e
      .replace(/['‘’]/g, '')                  // "lays" matches "Lay’s"
      .replace(/\s+/g, ' ')
      .trim();
  }

  /* 4. Enquiry form ------------------------------------------------------ */
  function initEnquiryForm() {
    const form = document.querySelector('[data-enquiry-form]');
    const success = document.querySelector('[data-enquiry-success]');
    if (!form || !success) return;

    const endpoint = String(config.enquiryEndpoint || '').trim();
    const demoMode = endpoint === '';
    const timeoutMs = Number(config.requestTimeoutMs) || 20000;

    // Sent to Google Sheets in this order, plus "page". Must match FIELDS in
    // the Apps Script (see google-sheets-setup.md).
    const FIELDS = ['name', 'email', 'company', 'country', 'phone', 'type', 'interest', 'quantity', 'message'];

    const REQUIRED_MESSAGES = {
      name: 'Please enter your name.',
      email: 'Please enter your business email.',
      country: 'Please enter the destination country.'
    };
    const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    const submitButton = form.querySelector('[data-submit]');
    const submitLabel = form.querySelector('[data-submit-label]');
    const errorBox = form.querySelector('[data-form-error]');
    const note = form.querySelector('[data-form-note]');
    const interestSelect = form.elements.namedItem('interest');
    const messageField = form.elements.namedItem('message');
    const nameField = form.elements.namedItem('name');
    const validatedInputs = Array.from(form.querySelectorAll('input[required], input[type="email"]'));

    const successLabel = success.querySelector('[data-success-label]');
    const successTitle = success.querySelector('[data-success-title]');
    const successText = success.querySelector('[data-success-text]');
    const againButton = success.querySelector('[data-enquiry-again]');

    if (demoMode) {
      if (note) {
        note.textContent = 'Demo mode: enquiries are not sent anywhere yet. Connect Google Sheets to start receiving them.';
        note.classList.add('is-demo');
      }
      if (successLabel) successLabel.textContent = 'Demo enquiry captured';
      if (successText) successText.textContent = 'The front-end form is working. Connect Google Sheets to receive enquiries.';
    }

    /* Validation: inline messages instead of the browser's default bubbles. */
    function errorFor(input) {
      const value = input.value.trim();
      if (input.required && value === '') return REQUIRED_MESSAGES[input.name] || 'This field is required.';
      if (input.type === 'email' && value !== '' && !EMAIL_PATTERN.test(value)) {
        return 'Please enter a valid email address, e.g. you@company.com.';
      }
      return '';
    }

    function setFieldError(input, message) {
      const field = input.closest('.field');
      let errorEl = field ? field.querySelector('.field-error') : null;

      if (message) {
        if (!errorEl && field) {
          errorEl = document.createElement('p');
          errorEl.className = 'field-error';
          errorEl.id = `${input.id}-error`;
          field.appendChild(errorEl);
        }
        if (errorEl) {
          errorEl.textContent = message;
          input.setAttribute('aria-describedby', errorEl.id);
        }
        input.setAttribute('aria-invalid', 'true');
      } else {
        if (errorEl) errorEl.remove();
        input.removeAttribute('aria-invalid');
        input.removeAttribute('aria-describedby');
      }
    }

    function validateForm() {
      let firstInvalid = null;
      validatedInputs.forEach((input) => {
        input.value = input.value.trim();
        const message = errorFor(input);
        setFieldError(input, message);
        if (message && !firstInvalid) firstInvalid = input;
      });
      if (firstInvalid) firstInvalid.focus();
      return firstInvalid === null;
    }

    validatedInputs.forEach((input) => {
      // Check a field once the visitor leaves it, then re-check live while they fix it.
      input.addEventListener('blur', () => {
        if (input.value.trim() !== '' || input.hasAttribute('aria-invalid')) setFieldError(input, errorFor(input));
      });
      input.addEventListener('input', () => {
        if (input.hasAttribute('aria-invalid')) setFieldError(input, errorFor(input));
      });
    });

    /* "Enquire about this category" on a product card pre-fills the form. */
    let autoMessage = '';
    document.addEventListener('click', (event) => {
      const link = event.target.closest('[data-interest]');
      if (!link) return;

      if (form.hidden) showForm(false);

      const interest = link.dataset.interest;
      if (interestSelect && Array.from(interestSelect.options).some((option) => option.value === interest)) {
        interestSelect.value = interest;
        const field = interestSelect.closest('.field');
        if (field) {
          field.classList.remove('is-highlighted');
          void field.offsetWidth; // restart the highlight animation
          field.classList.add('is-highlighted');
          // Remove it afterwards, or it would replay whenever the form is re-shown.
          interestSelect.addEventListener('animationend', () => field.classList.remove('is-highlighted'), { once: true });
        }
      }

      // Mention the product in the message, unless the visitor has already written something.
      const product = link.dataset.product;
      if (product && messageField && (messageField.value.trim() === '' || messageField.value === autoMessage)) {
        autoMessage = `I'm interested in: ${product}.\n`;
        messageField.value = autoMessage;
      }
    });

    /* Submission */
    let sending = false;

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      if (sending) return;
      hideError();
      if (!validateForm()) return;

      const data = new FormData(form);

      // Honeypot filled in: almost certainly a bot. Show success, send nothing.
      if (String(data.get('website') || '').trim() !== '') {
        showSuccess();
        return;
      }

      const payload = new URLSearchParams();
      FIELDS.forEach((name) => payload.append(name, String(data.get(name) || '').trim()));
      payload.append('page', window.location.href);

      setSending(true);
      try {
        if (demoMode) {
          console.info('[RK Trading] Demo mode: enquiry NOT sent. This is what would go to Google Sheets:', Object.fromEntries(payload));
          await wait(600); // lets you see the "Sending…" state while testing
        } else {
          await postWithTimeout(endpoint, payload, timeoutMs);
        }
        showSuccess();
      } catch (error) {
        showError('Sorry, we could not send your enquiry. Please check your connection and try again.');
      } finally {
        setSending(false);
      }
    });

    if (againButton) againButton.addEventListener('click', () => showForm(true));

    function postWithTimeout(url, body, ms) {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), ms);
      // mode "no-cors": Apps Script sends no CORS headers, so the reply is opaque.
      // A resolved fetch means the request left the browser; check the sheet to confirm.
      return fetch(url, { method: 'POST', mode: 'no-cors', body, signal: controller.signal })
        .finally(() => clearTimeout(timer));
    }

    function setSending(isSending) {
      sending = isSending;
      if (submitButton) submitButton.disabled = isSending;
      if (submitLabel) submitLabel.textContent = isSending ? 'Sending…' : 'Submit enquiry';
      form.setAttribute('aria-busy', String(isSending));
    }

    function showSuccess() {
      form.reset();
      autoMessage = '';
      validatedInputs.forEach((input) => setFieldError(input, ''));
      form.hidden = true;
      success.hidden = false;
      if (successTitle) successTitle.focus({ preventScroll: true });
      success.scrollIntoView({ block: 'nearest', behavior: prefersReducedMotion() ? 'auto' : 'smooth' });
    }

    function showForm(moveFocus) {
      success.hidden = true;
      form.hidden = false;
      hideError();
      if (moveFocus && nameField) nameField.focus();
    }

    function showError(message) {
      if (!errorBox) return;
      errorBox.textContent = message;
      errorBox.hidden = false;
    }

    function hideError() {
      if (errorBox) errorBox.hidden = true;
    }
  }

  /* 5. Footer year ------------------------------------------------------- */
  function initFooterYear() {
    const year = String(new Date().getFullYear());
    document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = year; });
  }

  /* Helpers -------------------------------------------------------------- */
  function wait(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }
})();
