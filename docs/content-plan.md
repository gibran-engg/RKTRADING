# Content plan

What the site says, why it is built this way, and what is still waiting on the client. Updated 9 Nov 2026, after the client's answers.

## 1. Positioning statement (drafted by us, for the client to approve)

> R.K. Trading is a Mumbai-based general trader that connects Indian exporters and international buyers with imported industrial and natural products. Since 2017 we have sourced, graded, packed and shipped, so buyers deal with one accountable partner from enquiry to delivery.

Home headline: **Import & Export Trading from Mumbai to the World.**
Supporting claims (all taken from the client's answers): in business since 2017, two-way trade, graded / sized / packed by us, origin and shelf life confirmed per product, pricing on quotation.

## 2. Sitemap

| Page | Job | Search phrases it is written for |
| --- | --- | --- |
| `index.html` | Convert: quick quote, show the whole range, build trust, answer objections (FAQ) | import export company Mumbai · Mumbai trading company |
| `imports.html` | Rank and convert for what comes into India | boiler / heat pump importer India · PPR pipes importer · WPC flooring importer · dates importer · ayurvedic raw material importer |
| `exports.html` | Rank and convert for what goes out | spices exporter India · tea exporter · fresh fruit and vegetable exporter · grains exporter · FMCG exporter Middle East |
| `about.html` | Credibility: founding year, owner, registrations | R.K. Trading Mumbai |
| `contact.html` | Full enquiry form | (conversion page, not a search target) |

Every product has an anchor (`imports.html#dates`) and a pre-filled quote link (`contact.html?interest=dates`). One page per category can be split out later if one product line needs its own search presence.

## 3. What we learned from other import/export sites, and what we used

Large corporate traders (for example Tata International and Olam) were reviewed and rejected as models: they lead with news carousels and sustainability stories and have no quote flow. The useful patterns came from exporter-focused guidance and from B2B marketplace listings.

| Pattern seen | How it is used here |
| --- | --- |
| Marketplace listings show "price on request" with a "Get quote" button on every product | Pricing is on quotation only (client's rule). Every product has **Request a quote**; the header, hero, sticky mobile bar and a closing band repeat it |
| Exporter guidance: contact details in the header, a short enquiry form, say what happens after it is sent | Phone / email in the top bar (once supplied), quick-quote form in the hero, **What happens next** beside the contact form |
| Show credentials on the home page | Trust bar (since 2017, 6 origin countries, 10 product lines, 6 registrations) and a registrations section; numbers on About |
| Show markets served and the process | Where-we-trade map and lists; From packing to delivery (photos only, as the client asked) |
| Real photos signal authenticity; stock photos do the opposite | Free Unsplash stand-in photos (no visible brand logos) on the ten products, to be replaced by the client's own; designed placeholders for the five process steps |
| Product pages organised around how buyers search, one page per product line | Imports and exports pages with category blocks, anchors and keyword-led titles |
| Fast, light pages; no auto-playing video or pop-ups | No video, no pop-ups, photos lazy-loaded at card size, no web fonts for Chinese / Arabic |
| Multilingual sites need proper language handling; machine-only Arabic hurts credibility | Language switcher with full right-to-left Arabic. Translations are drafts to be reviewed by a native speaker. Per-language URLs and `hreflang` are planned for the SEO phase |
| Standard navigation, not hidden or unusual menus | Four plain links plus a quote button |

Sources (advice from vendor and agency pages, so treated as guidance, not proof):
[Website strategy for export](https://tmrin.pages.dev/academy/lessons/l22) ·
[Export/import website design](https://prateeksha.com/industries/export-import-website-design) ·
[Multilingual vs single-language export sites](https://kolonell.com/en/blog/multilingual-vs-single-language-website-export-dubai-2026) ·
[Multilingual SEO for B2B exporters](https://academy.reevol.com/en/marketing-to-buyers/multilingual-seo-for-b2b-exporters/) ·
marketplace listings such as [Katke's Spices and Beverages](https://www.globallinker.com/seller/katke039s-spices-and-beverages) and [Merry Exim](https://www.indiamart.com/merry-exim-international/).

## 4. How the client's brief was applied

| Client answer | What we did |
| --- | --- |
| General trader, no brand authorisation. Brand and product names must not be displayed | Every brand name from the earlier draft was removed. Products are described by type and specification. A "general trader, not an authorised distributor" statement appears in the footer, About and FAQ |
| Imports: heating equipment, PPR, heat pumps, boilers, building materials (WPC, WPA), herbals and ayurvedic, dry and fresh dates | Five import categories: boilers / heat pumps / heating equipment; PPR pipes and fittings; building and flooring materials; herbals and ayurvedic; dates |
| Exports: FMCG, spices, tea, fresh fruit and vegetables, grains | Five export categories |
| Origins: China, Turkey, Afghanistan, Dubai, Oman, Italy, Iran. Markets: Middle East, Malaysia, Sri Lanka, Iran | Shown, **except Iran** (see open items) |
| Client does all packing, grading and sizing | Stated on every page |
| Pricing on quotation; MOQ, lead times and terms by phone | Stated everywhere; the form asks for a phone / WhatsApp number; FAQ explains it |
| Languages: English, Chinese, Arabic | Switcher on every page, remembered between visits; Arabic is right-to-left |
| Process content as photos only | Five photo slots: procurement, labelling, loading, shipping, unloading. No video |
| Colours: green, white, blue | New palette; the old sand/tan accent is gone |
| Goal: lots of leads; enquiries to Google Sheets; owner will build an n8n workflow | Two forms, sticky quote button on phones, WhatsApp button. Each enquiry records the visitor's language so n8n can answer in it |
| Owner maintains the site alone | Plain HTML/CSS/JS, one `config.js` for details, README with edit recipes |
| No testimonials | None included |

## 5. Still open

From the client's list:

- [ ] Registration numbers (GST, FSSAI, APEDA, Spices Board, Tea, Udyam)
- [x] Address, phone, WhatsApp, email → `assets/js/config.js` (received 9 Nov; the email is a personal Gmail address, so swap it for a domain email once one exists)
- [ ] Owner bio and photo → `about.html`
- [x] Logo: circular seal received 9 Nov and added to header, footer, favicons and 404 (a vector/SVG or transparent original would be sharper than the traced PNG, and the seal's small text is not legible at header size)
- [ ] Photos: products and the five process steps. **Ask first whether visible brand logos may appear**
- [ ] Full form of "WPA" (the site says "WPC and WPA" without expanding it)
- [ ] **Whether Iran may appear publicly** as an origin and a market. Check with the CA / bank. It is left off for now; adding it is a one-line change in the lists on Home, Imports, Exports, About and the FAQ, plus the map
- [ ] Domain name, launch deadline, budget, post-launch support, business email

Found while building:

- [ ] **IEC (Import Export Code)** is not in the client's list of registrations. Every importer and exporter needs one; confirm and add it to About
- [ ] What exactly "PPR" covers (the site assumes pipes and fittings)
- [ ] The exact name of the "tea registration" (shown as "Tea registration")
- [ ] The actual FMCG range and the grain types exported (the site uses broad generic labels)
- [ ] Wording of the process captions (labelling, loading, shipping, unloading); they are neutral drafts
- [ ] Whether the three claims linking registrations to products are right: spices ↔ Spices Board, tea ↔ tea registration, fresh produce and grains ↔ APEDA
- [ ] Native-speaker review of the Chinese and Arabic translations

## 6. Dropped on purpose

The earlier draft had a product search box and category filter buttons for twelve cards. With the catalogue now split into an imports page and an exports page of five categories each, search and filters add nothing, so they were replaced by a sticky category jump bar on each page. If the range grows past about twenty items, bring search back.
