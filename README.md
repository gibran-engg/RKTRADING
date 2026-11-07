# RK Trading website

Single-page website for RK Trading, a Mumbai-based import, export and distribution business (FMCG & beverages, botanical raw materials, fresh produce).

It is a **plain static site**: HTML, CSS and vanilla JavaScript. There is no framework, no npm install and no build step. The files in this folder are exactly what gets deployed.

## Run it locally

Pick any one of these.

**Option A: VS Code Live Server (recommended while editing)**

1. Install the *Live Server* extension (by Ritwick Dey) in VS Code.
2. Open this folder in VS Code.
3. Right-click `index.html` → **Open with Live Server**. The page reloads automatically when you save a file.

**Option B: Python's built-in server**

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>. Stop it with `Ctrl+C`.

**Option C: open the file directly**

Double-click `index.html`. Everything works, including the catalogue and the enquiry form; scripts are deliberately loaded as plain scripts (not ES modules) so this works.

Images (Unsplash) and fonts (Google Fonts) load from the internet, so you need a connection for the page to look right.

## Project structure

```
index.html              All page content and markup (one page, anchored sections)
assets/
  css/main.css          All styles: design tokens at the top, then one section per page area
  js/config.js          Site settings: Google Sheets URL for the enquiry form
  js/main.js            Behaviour: mobile menu, active-nav highlight, catalogue, enquiry form
  img/favicon.svg       Browser tab icon
google-sheets-setup.md  How to connect the enquiry form to a Google Sheet
```

Content lives in `index.html` (not in JavaScript), so the page is fully readable without JavaScript and by search engines later on.

## What the page does

| Feature | Where |
| --- | --- |
| Sticky header, mobile menu (closes on link, Escape or outside click), active-section highlight | `main.js` → `initNavigation`, `initActiveSection` |
| Product catalogue: category filters, multi-word search (also searches the product details), empty state with reset | `main.js` → `initCatalogue` |
| Intro-strip verticals jump to the catalogue pre-filtered | `data-filter-link` in `index.html` |
| Expandable "Product details" per card | native `<details>` in `index.html` |
| "Enquire about this category" pre-selects *Product interest* and mentions the product in the message | `main.js` → `initEnquiryForm` |
| Enquiry form: inline validation, honeypot, sending state, timeout, error and success screens | `main.js` → `initEnquiryForm` |
| Demo mode vs. Google Sheets | `config.js` → `enquiryEndpoint` |

## Common edits

**Business details and licence numbers.** Search `index.html` for `PLACEHOLDERS`. The contact address, email and phone are in the Contact section; IEC, GSTIN, FSSAI, APEDA and Spices Board numbers are in the Documentation section. Delete a licence row you don't hold, or the whole `.credentials` block.

**Add or edit a product.** In `index.html`, copy an existing `<article class="product-card">` block inside the portfolio section. Keep these in sync:

- `data-category` on the card must match one of the filter buttons (`data-filter`).
- `data-interest` on the card's "Enquire" link must match an option in the form's *Product interest* dropdown.
- `data-product` on that link is the name that gets written into the enquiry message.

**Add a category.** Add a filter button (`data-filter="…"`), use the same text in the cards' `data-category`, and add it as an option in the *Product interest* dropdown.

**Colours, fonts, spacing.** Change the tokens at the top of `assets/css/main.css` (`:root { … }`).

## Enquiry form

With `enquiryEndpoint: ''` in `assets/js/config.js` (the default) the form is in **demo mode**: it validates, shows "Sending…" briefly and then the success screen, and logs the payload it would have sent to the browser console. A note under the button says it is in demo mode.

To receive real enquiries in a Google Sheet, follow [google-sheets-setup.md](google-sheets-setup.md). It takes about five minutes and only involves pasting one URL into `config.js`.

## Browser support

Current Chrome, Edge, Firefox and Safari (desktop and mobile). The layout is responsive from 320px up, with breakpoints at roughly 1000px (two-column catalogue), 860px (mobile menu), 760px (stacked sections) and 600px (single column).

## Later: production launch

Deliberately **not** done yet, because they depend on the final domain. The structure already leaves room for each, so none of them needs a restructure:

- Canonical URL, production `<meta>` / Open Graph / Twitter tags and structured data: add them to the `<head>` of `index.html`, where a comment marks the spot.
- `robots.txt` and `sitemap.xml`: add as new files in the project root.
- Google Search Console and Google Analytics: add the verification tag and script to `<head>`.
- Cloudflare Pages: connect this GitHub repository with no framework preset, leave the build command empty, and point the build output directory at the repository root. DNS and SSL are configured in Cloudflare once the domain is bought.
- Optionally self-host the images in `assets/img/` instead of loading them from Unsplash.
