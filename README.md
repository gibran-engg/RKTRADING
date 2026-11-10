# R.K. Trading website

Website for R.K. Trading, a Mumbai-based general trader (imports and exports, since 2017). Five static pages in English, Chinese (中文) and Arabic (العربية).

It is a **plain static site**: HTML, CSS and vanilla JavaScript. No framework, no npm install, no build step. The files in this folder are exactly what gets deployed.

## Run it locally

Pick any one of these.

**VS Code Live Server (best while editing).** Install the *Live Server* extension, then right-click `index.html` → **Open with Live Server**. It reloads on save.

**Python's built-in server.**

```bash
python -m http.server 8000
```

Then open <http://localhost:8000>. If the port is busy, use another one (`8080`). Stop with `Ctrl+C`. It does not auto-reload; refresh the browser after saving.

**Open the file directly.** Double-click `index.html`. Everything works, including language switching and the forms.

Fonts (Google Fonts) load from the internet, so you need a connection for the page to look right. Chinese and Arabic use fonts already installed on the visitor's device, so they add no download.

## Project structure

```
index.html        Home: hero, trust bar, products, where we trade, why us, process, registrations, FAQ, quick-quote form (bottom)
imports.html      Imports: five categories
exports.html      Exports: five categories
about.html        Story, owner, registrations (numbers go here)
contact.html      Full enquiry form, contact details
404.html          "Page not found"
assets/
  css/main.css    All styles. Design tokens (green / white / blue) at the top
  js/config.js    Settings: Google Sheets URL + phone / WhatsApp / email / address
  js/main.js      Menu, contact details, enquiry forms
  js/i18n.js      Language switching
  js/lang/zh.js   Chinese translations   (loaded only when a visitor picks 中文)
  js/lang/ar.js   Arabic translations    (loaded only when a visitor picks العربية)
  img/logo.png, logo-light.png   Company seal (header; white version for the dark footer)
  img/favicon-32.png, favicon-64.png, apple-touch-icon.png   Browser and phone icons (globe mark / full seal)
  img/world-map.svg   Land for the home-page trade map
  img/brochure-food.jpg, brochure-building.jpg   Cover thumbnails for the catalogue download cards
  brochures/          The two catalogue PDFs offered for download (see "Catalogue PDFs" below)
docs/content-plan.md   Positioning, sitemap, research notes, decisions and open client questions
google-sheets-setup.md How to receive enquiries in a Google Sheet
```

## Everyday edits

### Contact details and Google Sheets: `assets/js/config.js`

When the client sends their phone, WhatsApp, email and address, put them in `config.js`. They appear on every page: top bar, footer, closing banners, the quote section on the home page, the Contact page, and the floating WhatsApp / Call buttons (a tap-to-call bar on phones). The `tel:`, `mailto:`, WhatsApp and Google Maps links are built for you. Anything left empty stays hidden in the top bar and footer and shows a "to follow" placeholder on the Contact page. The WhatsApp button only appears once a number is set.

The same details are also written directly into each page's HTML, so they show without JavaScript, survive caching and are visible to search engines. `config.js` takes over once it loads. **If the phone, email or address changes, update `config.js` and also search the project for the old value and replace it** (about 5 files).

If a change doesn't show up in your browser, do a hard refresh (`Ctrl+F5`): the CSS and script links carry a version suffix (`?v=3`); bump it when you edit those files.

The Google Sheets URL goes in the same file. See [google-sheets-setup.md](google-sheets-setup.md).

### Registration numbers and owner bio: `about.html`

Each registration row says "Available on request" for now. Replace that text with the real number (and remove its `data-i18n` attribute) and delete a row the client does not hold. The owner bio is a one-line factual sentence; extend it (and its `about.owner.bio` key in `zh.js` / `ar.js`) and swap the owner icon for a photo when one arrives.

### Text and translations

English lives in the HTML and is the source of truth. Chinese and Arabic are looked up by key:

```html
<h3 data-i18n="why.2.t">Graded, sized and packed by us</h3>
```

```js
// assets/js/lang/zh.js and ar.js
'why.2.t': '由我们分级、分选和包装',
```

To change a sentence: edit the English in the HTML, then update the same key in `zh.js` and `ar.js`. If you skip a translation, that text simply shows in English. Headings that contain an emphasised phrase use `data-i18n-html` and `<em>…</em>`. Placeholders and labels use `data-i18n-attr="placeholder:key"`.

The translations are a **first draft**. Have a native speaker review them (especially trade terms) before launch.

### Dark / light theme

Every page has a sun/moon button in the header. The site is light by default, whatever the visitor's system setting; once they press the button, their choice is remembered in the browser (`localStorage` key `rk-theme`). The colours live in `assets/css/main.css`: the light values are the tokens at the top (section 1) and the dark values are one block at the very end (section 20). To change a dark colour, edit it there. The tiny script at the top of each page's `<head>` applies the theme before the page paints (this avoids a white flash), so keep it in sync across pages, like the language script next to it.

### Photos

The twelve product photos are free stock photos from [Unsplash](https://unsplash.com/license) loaded straight from their servers (no attribution required). They are **stand-ins** for the client's own photos, and each was checked for visible brand logos. To swap one, change the `src` of its `<img class="media">` in `index.html`, `imports.html` or `exports.html` to a file in `assets/img/`, for example:

```html
<img class="media" src="assets/img/dates.jpg" alt="Dry dates packed in cartons" width="900" height="720" loading="lazy">
```

Export photos at about 1200px wide as WebP or compressed JPEG (under 200 KB each). **Do not use photos that show visible brand logos** until the client confirms that is allowed. Before launch, host the photos yourself rather than relying on Unsplash.

The five process cards (Procurement, Labelling, Loading, Shipping, Unloading) use free Unsplash stand-in photos, checked for visible brand logos. Labelling and Loading are cropped copies kept in `assets/img/` (`process-labelling.jpg`, `process-loading.jpg`) so that the logos in the original frames are cut out. The client wants **photos only, no video**. To swap one, change the `src` of its `<img class="media">` in `index.html` to a file in `assets/img/`.

The trade map on the home page draws land from `assets/img/world-map.svg` (Natural Earth, public domain) with the routes and labels on top. The overlay uses the same 900x470 box as the map: `x = (lon + 25) * 5.294`, `y = (62.7 - lat) * 5.294`. To add a country, work out its x, y that way and add a node, an arc and a label in `index.html`.

Each product photo carries a small arrow badge: **inward arrow = import, outward arrow = export**. It is part of the `<div class="photo">` wrapper around the image; keep the wrapper when swapping photos.

### Adding or changing a product

Each category exists in these places. Keep them in step:

1. `imports.html` or `exports.html`: copy a `<article class="cat" id="…">` block.
2. `index.html`: the matching `<article class="card-cat">` and the entry in the hero quick-quote *Product interest* list.
3. `contact.html`: the *Product interest* option. Give it `data-slug="…"` equal to the block's `id`; links like `contact.html?interest=dates` use it to pre-select the product.
4. Footer links on all pages, and the jump bar at the top of the imports/exports page.
5. Translation keys `cat.<id>.*` in `zh.js` and `ar.js`.

### Navigation and footer

The header and footer are repeated in each page so they work without JavaScript. To change a menu item, edit it in all five pages (search for `data-header`).

### Catalogue PDFs

Two catalogues are offered for download: **Food & Natural Products** and **Building & Heating Supplies**. The PDFs are in `assets/brochures/`; the cover thumbnails are `assets/img/brochure-food.jpg` and `brochure-building.jpg`. Each is linked from a "Download our product catalogues" section (id `catalogues`) on the home, imports, exports and about pages, and from the footer on every page except 404. Texts are under the `brochure.*` keys in `zh.js` and `ar.js`; the PDFs themselves are English only.

To update one: rebuild it in the `brochure/` folder (see `brochure/README.md`), copy the new PDF over the one in `assets/brochures/` under the same name, and update the file size shown on its download button (search for `brochure-meta`) and the thumbnail if the cover changed. If the page count changes, update "15 pages" or "6 pages" in the card text (`brochure.food.p`, `brochure.bld.p`) in the HTML and both language files.

**Before deploying:** Cloudflare Pages publishes the whole repository root, so the `brochure/` folder (build sources and the old brochure in `brochure/original/`) would be public. The old brochure names brands and lists Iranian saffron. Remove or ignore `brochure/` for the deployment, or move it out of this repository.

## The enquiry forms

There are two forms: a short quick-quote at the bottom of the home page and the full form on the Contact page. Both validate inline, block double-sends, drop bot submissions (hidden honeypot field), time out after 20 seconds, and keep the visitor's typing if sending fails.

With `enquiryEndpoint: ''` (the default) they run in **demo mode**: on a local address (localhost, 127.0.0.1, a file opened from disk) they show a "Demo mode" note, simulate sending, and log the payload to the browser console. On any other address with no endpoint set, the form does **not** fake a success: it shows "Online enquiries are temporarily unavailable" with the phone and email from `config.js`, so no enquiry is silently lost. Set the Apps Script URL in `config.js` to go live. Each enquiry also records the visitor's **language** (`en`, `zh` or `ar`), so the client's n8n workflow can reply in the right language.

## Browser support

Current Chrome, Edge, Firefox and Safari on desktop and mobile. Responsive from 320px up. Arabic uses a full right-to-left layout.

## Later: production launch

Deliberately **not done yet**; each needs the final domain. Nothing below needs a restructure:

- Canonical URLs, Open Graph / Twitter tags, structured data (Organization / LocalBusiness), `robots.txt`, `sitemap.xml`, Search Console, analytics: a comment in each page's `<head>` marks the spot.
- **Search engines and languages.** Today there is one URL per page and Chinese / Arabic are applied by JavaScript, so search engines index the English text. When the SEO phase starts, generate real `/zh/` and `/ar/` pages (with `hreflang`) from the same HTML and dictionaries. No content needs rewriting.
- Cloudflare Pages: connect this repository with no framework preset, an empty build command and the repository root as the output directory. DNS and SSL are configured once the domain is bought. `404.html` is picked up automatically.
- Replace the Unsplash stand-in photos and the process placeholders with the client's photos, hosted in `assets/img/`.
- Business email on the new domain, then add it to `config.js`.
- A privacy policy page, because the forms collect personal data.
