"""
Builds brochure.html for the R.K. Trading product catalogue.

    python build.py            -> writes brochure.html
    python build.py --pdf      -> also prints ../RK-Trading-Food-and-Natural-Products.pdf with Microsoft Edge (headless)

All product lists, specs and copy live in the data blocks below, so a change is a one-line edit
followed by a rebuild. Copy follows the website: no brand names, no Iran, pricing on quotation.
"""
import html
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
e = html.escape

# ---------------------------------------------------------------- contact (same as assets/js/config.js)
PHONE = "+91 70064 01698"
EMAIL = "riyazwani2015@gmail.com"
WHATSAPP = "https://wa.me/917006401698"
ADDRESS = "Flat 15, 3rd Floor, Haji Abdul Majid Apartments, Swami Vivekanand Marg (behind Jasmine Apts), Andheri West, Mumbai – 400058, Maharashtra, India"

# ---------------------------------------------------------------- data
IMPORTS = [
    ("Dates: Dry &amp; Fresh", "img/dates.jpg",
     "Dry and fresh dates, graded and packed by us. Origin and shelf life are confirmed for each product.",
     ["Dry dates", "Fresh dates"]),
    ("Dry Fruits &amp; Nuts", "img/dryfruits.jpg",
     "Dry fruits and nuts for retailers, wholesalers and repackers, graded and packed by us. Origin and shelf life are confirmed for each product.",
     ["Almonds", "Cashews", "Pistachios", "Walnuts", "Raisins", "Dried apricots and figs"]),
    ("Chocolates", "img/chocolates.jpg",
     "Chocolates for retail, wholesale and distribution buyers, supplied by type and specification, not by brand name.",
     ["Bars and blocks", "Filled chocolates", "Assorted boxes"]),
    ("Herbals", "img/herbal.jpg",
     "Herbal raw materials and products, imported for manufacturers, wholesalers and retailers.",
     ["Whole herbs", "Cut herbs", "Herbal powders"]),
    ("Ayurvedic Products", "img/ayurveda.jpg",
     "Ayurvedic raw materials and products, imported for manufacturers, wholesalers and retailers.",
     ["Ayurvedic raw materials", "Ayurvedic products"]),
]
EXPORTS = [
    ("FMCG Products", None,
     "Fast-moving food and beverage products for retail, wholesale and distribution buyers, supplied by product type and specification.",
     ["Packaged food", "Beverages", "Snacks", "Instant mixes"]),
    ("Spices", "img/spices.jpg",
     "Whole and ground spices, graded and packed by us to your specification.",
     ["Whole spices", "Ground spices"]),
    ("Tea", "img/tea.jpg",
     "Tea packed in the grades and pack sizes your market needs.",
     ["Black tea", "Green tea", "Packed tea"]),
    ("Fresh Fruit &amp; Vegetables", "img/produce.jpg",
     "Fresh fruit and vegetables, sized, graded and packed by us for export. Seasonal availability is confirmed at quotation.",
     ["Fresh fruit", "Fresh vegetables"]),
    ("Grains", "img/grains.jpg",
     "Grains graded, sized and packed by us to your specification, for importers, wholesalers and distributors.",
     ["Rice", "Wheat", "Millets", "Corn"]),
]
ORIGINS = ["China", "Turkey", "Afghanistan", "Dubai (UAE)", "Oman", "Italy"]
MARKETS = ["Middle East", "Malaysia", "Sri Lanka"]

WHOLE_SPICES = [
    "Kashmiri saffron (grade A++)", "Ajwain seeds", "Cardamom granules (green)", "Cardamom whole (black)",
    "Cardamom whole (green)", "Cinnamon stick (flat)", "Cinnamon stick (round)", "Coriander seeds",
    "Cumin seeds", "Curry leaves", "Dagar phool", "Fenugreek seeds", "Ganthoda whole", "Ginger whole",
    "Mace whole", "Mint leaves", "Mustard seeds (black)", "Mustard seeds (brown)", "Nutmeg",
    "Pepper whole (white)", "Pepper whole (black)", "Red chilli (stemless)", "Sesame seeds (black)",
    "Sesame seeds (brown)", "Sesame seeds (hulled)", "Sesame seeds (white)", "Shah jeera", "Turmeric whole",
]
GRAINS = ["Rice", "Bajra", "Corn", "Jav", "Jowar", "Kodri", "Ragi", "Wheat"]
GROCERY = [
    "Amchur powder", "Amchur whole", "Apricot (Zardalu)", "Asariyo (Halim)", "Basil leaves whole (Tulsi)",
    "Black salt powder", "Chana", "Chana dalia (split)", "Chana dalia (whole)", "Char magaz", "Charoli",
    "Chora wadi", "Citric acid (Neemu ke phool)", "Coconut powder", "Coconut (whole)", "Crystal sakar (Misri)",
    "Date (dry)", "Chana dal (regular)", "Chana dal (yellow)", "Edible gum", "Fennel seeds (salted yellow)",
    "Fennel seeds (sugar)", "Gulal", "Isabgol", "Kamal kakdi", "Kasuri methi (whole)", "Khicha papad",
    "Kokam black (Lunawada)", "Kokam phool (white)", "Mahabaleshwari chana",
    "Mahabaleshwari chana (salted yellow)", "Makhana phool", "Makhana sweet (chana)",
    "Makhana sweet (peanut)", "Makhana sweet (plain big)", "Makhana sweet (plain small)", "Mamra basmati",
    "Mamra bhel", "Mamra Kolhapuri", "Mamra moody (Madrasi)", "Moong wadi", "Moraiyo", "Panch puran",
    "Papad kharo", "Patasa", "Peanut salted (skin)", "Poha corn", "Poha medium", "Poha nylon",
    "Poha sabudana", "Poha thick", "Potato wafers grill", "Potato wafers plain", "Potato wafers salted",
    "Punjabi wadi", "Raisins (red draksh)", "Rewadi", "Rice boiled", "Rice chakri", "Sabudana whole",
    "Saji na phool", "Salt", "Samo", "Sesame seeds (salted yellow)", "Sesame seeds (sugar coated)",
    "Sindhav powder", "Soya wadi (chunks)", "Takmaria", "Wheat sev",
]
FLOURS = [
    "Kuttu flour", "Bajra flour", "Mathiya flour", "Corn flour (Punjabi style)", "Bhakhri flour",
    "Moong dal flour", "Corn flour (meal)", "Corn flour (coarse)", "Corn flour (fine)", "Ragi flour",
    "Gram flour (coarse)", "Cracked wheat (regular / small)", "Dhokla flour", "Gram flour (besan)",
    "Roasted upma suji mix", "Jowari flour", "Idli rava (par boiled)", "Idli rava (raw) / cream of rice",
    "Haandwa flour", "Rajgaro flour", "Rice flour", "Semolina (suji coarse)", "Semolina (suji fine)",
    "Singoda flour", "Udad flour", "Wheat flour (maida)", "Whole wheat flour (atta)",
]
KHAKHRA = [
    "Bajra khakhara", "Jeera khakhara", "Jeera khari", "Jeera toast", "Masala khakhara", "Methi khakhara",
    "Plain khakhara", "Plain khari", "Plain toast",
]
CHUTNEYS = [
    "Garlic paste", "Ginger garlic paste", "Ginger paste", "Green chilli chutney", "Green coriander chutney",
    "Mint chutney", "Pani puri chutneys", "Sandwich chutney", "Tamarind chutney",
]
PAPAD = [
    "Double pepper papad", "Garlic papad", "Green chilli papad", "Jeera mari papad", "Moong papad",
    "Punjabi papad", "Red chilli papad", "Single pepper papad", "Udad plain papad",
]
INSTANT = [
    "Basudi", "Dahiwad", "Dakor gota", "Dalwada", "Dosa", "Gujarati dal", "Gulab jamun", "Handwo", "Jalebi",
    "Khaman", "Khatta dhokla", "Meduvada", "Methi gota", "Rava dosa", "Rava idli", "Sambhar", "Idli",
]
SNACKS = [
    "Bhavnagari ghatiya", "Bombay bhel", "Bombay puri", "Chanadal", "Chanajor", "Dalmoth", "Diet bhel",
    "Dry fruit kachori", "Dry fruit samosa", "Farali chiwda", "Phoolwadi", "Garlic sev mumra",
    "Green chilli kichiya", "Jamnagari ghatiya", "Jeera kichiya", "Kabuli chana", "Khatta meetha",
    "Makai chiwda", "Manglori mix", "Masala banana", "Methi puri", "Mini bhakarwadi", "Moongdal", "Murukku",
    "Navratna mix", "Nylon chiwda", "Nylon papdi ghatiya", "Nylon sev", "Onion pakoda", "Palak chiwda",
    "Papad bhel", "Pepper banana", "Plain kichiya", "Pudina moong masala", "Ratlami sev",
    "Red chilli garlic kichiya", "Salted boondi", "Sandwich bhakarwadi", "Sing bhujiya", "Soft chakli",
    "Soya sticks", "Spicy hot mix", "Sweet sakkarpara", "Tea time puri", "Tumtum",
]

# name, photo, colour, variety, size, shelf life, packing
CONFIRM = "Confirmed at quotation"
PRODUCE_A = [
    ("Red Onion", "Dark red", "img/produce-onion-dark.jpg", "Dark red", "Agrifound Dark Red", "25 mm – 60 mm+",
     "35 days from packing", "5 kg to 50 kg red mesh bags or jute bags"),
    ("Red Onion", "Light red", "img/produce-onion-light.jpg", "Light red", "Agrifound Light Red", "25 mm – 60 mm+",
     "55 days from packing", "5 kg to 50 kg red mesh bags or jute bags"),
    ("White Onion", "", "img/produce-onion-white.jpg", "White", "Common", "40 mm – 60 mm+",
     "60 days from packing", "10 kg to 50 kg white mesh bags"),
    ("Garlic", "", "img/produce-garlic.jpg", "White", "", "35 mm+",
     "55 days from packing", "5 kg to 50 kg jute bag and 5 to 7 kg box"),
    ("Potato", "", "img/produce-potato.jpg", "Yellow", "Pukhraj, LR, Lokar", "35 mm – 60 mm+",
     "45 days from packing", "5 kg to 50 kg jute bag"),
    ("Lemon", "", "img/produce-lemon.jpg", "Green to natural yellow", "", "40 mm+",
     "30 days from packing", "7 kg to 7.5 kg gross weight"),
]
PRODUCE_B = [
    ("Pomegranate", "", "img/produce-pomegranate.jpg", "Red", "Bhagwa", CONFIRM,
     "25 days from packing", "2.7 kg net and 3.5 kg gross box"),
    ("Banana", "", "img/produce-banana.jpg", "Green to natural yellow", "G9", "8 inch+",
     "28 days in summer and 35 days in other months, from packing", "7 kg, 13 kg or 16 kg box"),
    ("Cherry Tomato", "", "img/produce-tomato.jpg", "Green to natural red", "Cherry tomato", "40 mm+",
     "25 – 28 days from packing", "7 kg net weight and 20 kg crate"),
    ("Green Chilli", "", "img/produce-chilli.jpg", "Green", "G4", CONFIRM,
     "30 days from packing", "4 kg net and 4.5 kg gross box"),
]

WHY = [
    ("Imports and exports under one roof", "One partner for both directions of trade, so you deal with a single accountable team."),
    ("Graded, sized and packed by us", "We do the grading, sizing and packing ourselves, so what you approve is what ships."),
    ("Origin and shelf life, confirmed", "Origin, shelf life and specifications are confirmed for each product before you commit."),
    ("Registered and documented", "GST, FSSAI, APEDA, Spices Board, Tea and Udyam registrations are held. Numbers on request."),
    ("Straightforward quotations", "Pricing is on quotation. MOQ, lead times and terms are shared on request, by phone."),
    ("Speak to us directly", "Send an enquiry and talk to our team by phone or WhatsApp, not a call centre."),
]
PROCESS = [
    ("Procurement", "img/procurement.jpg", "Products sourced from our suppliers to the agreed specification."),
    ("Labelling", "img/process-labelling.jpg", "Every pack labelled to the buyer's requirements."),
    ("Loading", "img/process-loading.jpg", "Careful loading into containers and trucks."),
    ("Shipping", "img/shipping.jpg", "Shipped to your destination."),
    ("Unloading", "img/unloading.jpg", "Unloaded and handed over at delivery."),
]
STEPS = [
    ("Send an enquiry", "Tell us the product, quantity and destination."),
    ("Get your quotation", "We confirm price, specification, origin and shelf life. MOQ, lead time and terms are shared by phone."),
    ("We pack and ship", "We grade, size, pack, label and load your order and ship it to the destination."),
]

# ---------------------------------------------------------------- extra data
ENQ = {
    "dates": ["Variety and grade", "Dry or fresh", "Pack size, quantity and delivery location"],
    "dryfruits": ["Product and grade", "Pack size and packing style", "Quantity and delivery location"],
    "chocolates": ["Type and pack size", "Labelling language", "Quantity and delivery location"],
    "herbal": ["Product and form (whole, cut or powder)", "Required grade or specification", "Quantity and packing size"],
    "ayurvedic": ["Product and form", "Required grade or specification", "Quantity and packing size"],
    "fmcg": ["Product type and pack size", "Labelling language", "Quantity and destination market"],
    "tea": ["Tea type and grade", "Pack size and packing style", "Quantity and destination market"],
    "spices": ["Spice and form (whole or ground)", "Grade and pack size", "Quantity and destination market"],
    "grains": ["Grain type and grade", "Pack size", "Quantity and destination market"],
    "grocery": ["Product and pack size", "Labelling language", "Quantity and destination market"],
    "produce": ["Fruit or vegetable and variety", "Size, grade and packing", "Quantity, season and destination"],
}

CSS = """
@font-face{font-family:'DM Sans';src:url(fonts/dmsans-latin.woff2) format('woff2');font-weight:400 700;font-style:normal}
@font-face{font-family:'Manrope';src:url(fonts/manrope-latin.woff2) format('woff2');font-weight:600 800;font-style:normal}
@page{size:A4;margin:0}
:root{
  --g950:#06241b;--g900:#093527;--g800:#0c4a37;--g700:#126048;--g600:#1a7a5c;--g500:#2a9a74;--g100:#e3f2ea;--g50:#f2f9f5;
  --b950:#071c3a;--b900:#0a2a56;--b800:#0f4a96;--b700:#1559b3;--b600:#2271d1;--b300:#9cc4f4;--b200:#c4dcf8;--b100:#e2eefc;--b50:#f1f7fe;
  --ink:#10251d;--text:#31443c;--muted:#566860;--line:#d3ddd8;--accent:#a8d4ff;
  --display:'Manrope','DM Sans',sans-serif;--body:'DM Sans',sans-serif;
}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#fff}
body{font-family:var(--body);color:var(--text);font-size:9pt;line-height:1.5;-webkit-print-color-adjust:exact;print-color-adjust:exact}
img{display:block;width:100%;height:100%;object-fit:cover}
ul{list-style:none}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;break-after:page;page-break-after:always;background:#fff}
.page:last-child{break-after:auto;page-break-after:auto}
.abs{position:absolute}

/* section band + folio */
.band{position:absolute;left:0;right:0;top:0;height:13mm;display:flex;justify-content:space-between;align-items:center;padding:0 28mm 0 14mm;
  color:#fff;font:700 6.8pt var(--display);letter-spacing:.24em;text-transform:uppercase;z-index:5}
.band.in{background:var(--g800)}.band.out{background:var(--b800)}.band.cat{background:var(--b900)}
.band span:last-child{opacity:.75;letter-spacing:.18em}
.pn{position:absolute;right:14mm;top:4mm;z-index:6;font:800 8.5pt var(--display);color:#fff;letter-spacing:.04em}
.pn.b{top:auto;bottom:7mm;color:var(--g900)}
.ft{position:absolute;left:14mm;right:14mm;bottom:5.5mm;display:flex;justify-content:space-between;align-items:baseline;font-size:6.8pt;color:var(--muted);z-index:5}
.ft b{font:800 8pt var(--display);color:var(--g900)}
.ft.w,.ft.w b{color:#fff}

/* type */
.lbl{font:700 6.8pt var(--display);letter-spacing:.2em;text-transform:uppercase;color:var(--b700)}
.lbl.g{color:var(--g600)}
.lbl.w{color:var(--accent)}
h1{font:800 26pt/1.06 var(--display);color:var(--g900);letter-spacing:-.022em}
h1 em{font-style:normal;color:var(--b700)}
h2{font:800 19pt/1.12 var(--display);color:var(--g900);letter-spacing:-.015em}

/* feature pages: two products per page, photo bleeds to the page edge */
.feat{position:absolute;left:0;right:0;top:13mm;bottom:0;display:flex;flex-direction:column}
.prod{flex:1;display:flex;min-height:0;position:relative}
.prod+.prod{border-top:.2mm solid var(--line)}
.prod.r{flex-direction:row-reverse}
.prod .im{width:98mm;flex:none;position:relative;overflow:hidden}
.prod .tx{flex:1;padding:8mm 14mm 9mm 9mm;display:flex;flex-direction:column;justify-content:center}
.prod.r .tx{padding:8mm 9mm 9mm 14mm}
.prod .num{font:800 30pt/1 var(--display);color:var(--b700);letter-spacing:-.03em}
.prod.in .num{color:var(--g600)}
.prod h2{margin:2mm 0 2.6mm}
.prod p{font-size:9pt;line-height:1.55;color:var(--text)}
.sh{font:700 6.4pt var(--display);letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin:4.2mm 0 1mm}
.plain li{font-size:8.8pt;font-weight:600;color:var(--ink);padding:1.1mm 0;border-bottom:.2mm solid var(--line);line-height:1.3}
.plain.mu li{font-weight:400;color:var(--text)}
.prod.solid{background:var(--g900);color:#fff}
.prod.solid .tx{padding:0 14mm 0 14mm}
.prod.solid .big li{font:800 17pt/1 var(--display);color:#fff;padding:3.1mm 0;border-bottom:.25mm solid rgba(255,255,255,.22);letter-spacing:-.01em}
.prod.solid p{color:#c7d6ce;margin-bottom:5mm;font-size:9.4pt}
.prod.solid h2{color:#fff}
.typeblock{background:var(--b900);color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 10mm 0 14mm}
.typeblock li{font:800 17pt/1.05 var(--display);padding:3.2mm 0;border-bottom:.25mm solid rgba(255,255,255,.22);letter-spacing:-.012em}
.typeblock .lbl{margin-bottom:3mm}

/* catalogue pages */
.flow{position:absolute;left:0;right:0;top:13mm;bottom:11mm}
.hero{position:relative;overflow:hidden}
.hero::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,36,27,0) 40%,rgba(6,36,27,.78))}
.hero .t{position:absolute;left:14mm;right:14mm;bottom:6mm;z-index:2;color:#fff;display:flex;justify-content:space-between;align-items:flex-end}
.hero h1{color:#fff;font-size:30pt}
.hero .n{font:700 7pt var(--display);letter-spacing:.2em;text-transform:uppercase;color:var(--accent);padding-bottom:2mm}
.duo{display:flex}
.duo .hero{flex:1}
.duo .hero .t{left:9mm;right:9mm;flex-direction:column;align-items:flex-start;gap:1mm}
.duo .hero .n{padding-bottom:0}
.duo .hero h1{font-size:21pt}
.body{padding:5mm 14mm 0}
.split{display:flex;height:88mm}
.split .im{width:104mm;flex:none;position:relative;overflow:hidden;background:#fff}
.split .tx{flex:1;padding:0 14mm 0 9mm;display:flex;flex-direction:column;justify-content:center}
.split p{font-size:9.4pt}
.gh{display:flex;justify-content:space-between;align-items:baseline;border-top:.7mm solid var(--g900);padding-top:2mm;margin:6.5mm 0 1.5mm}
.gh:first-child{margin-top:0}
.gh h2{font-size:12.5pt}
.gh span{font:700 6.6pt var(--display);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.list{column-gap:7mm;column-fill:balance}
.list li{break-inside:avoid;font-size:8.7pt;font-weight:600;color:var(--ink);padding:1.45mm 0;border-bottom:.2mm solid var(--line);line-height:1.3}
.c2{column-count:2}.c3{column-count:3}.c4{column-count:4}
.c4 li{font-size:8.2pt}
.enq{margin-top:5mm;font-size:7.8pt;color:var(--muted);line-height:1.55}
.enq b{font:700 6.4pt var(--display);letter-spacing:.18em;text-transform:uppercase;color:var(--b700);margin-right:2mm}
.feature-strip{display:flex;gap:6mm;align-items:center;margin-top:6mm;background:var(--b50);padding:0 6mm 0 0}
.feature-strip .im{width:44mm;height:30mm;flex:none}
.feature-strip h3{font:800 12pt/1.2 var(--display);color:var(--g900);margin:1mm 0 1.2mm}
.feature-strip p{font-size:8.4pt}

/* produce rows */
.ph{padding:8mm 14mm 4mm}
.ph h1{font-size:25pt}
.ph p{margin-top:2mm;font-size:9pt;color:var(--muted);max-width:140mm}
.prow{display:flex;height:46.4mm;border-top:.2mm solid var(--line)}
.prow:last-child{border-bottom:.2mm solid var(--line)}
.prow .im{width:60mm;flex:none}
.prow .tx{flex:1;padding:4.2mm 14mm 3mm 8mm}
.prow h2{font-size:15pt;display:flex;align-items:baseline;gap:3mm}
.prow h2 small{font:600 8pt var(--body);color:var(--b700);letter-spacing:0}
.spec{display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 7mm;margin-top:3mm}
.spec div{border-top:.2mm solid var(--line);padding-top:1.1mm}
.spec dt{font:700 5.8pt var(--display);letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}
.spec dd{font-size:8.3pt;font-weight:600;color:var(--ink);line-height:1.32}
.spec .wide{grid-column:1 / -1}

/* intro */
.side{position:absolute;left:0;top:0;bottom:0;width:66mm;display:flex;flex-direction:column}
.side div{flex:1;min-height:0;position:relative;overflow:hidden}
.side img,.cover .grid img{position:absolute;inset:0}
.intro{position:absolute;left:78mm;right:14mm;top:20mm;bottom:14mm;display:flex;flex-direction:column}
.intro h1{margin:3mm 0 5mm;font-size:30pt}
.intro .lead{font-size:10.4pt;line-height:1.6;color:var(--text)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:9mm}
.kv{margin-top:9mm}
.kv div{display:flex;gap:4mm;border-top:.2mm solid var(--line);padding:2.7mm 0;font-size:8.8pt}
.kv dt{width:25mm;flex:none;font:700 6.2pt var(--display);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);padding-top:.6mm}
.kv dd{font-weight:600;color:var(--ink)}
.small{font-size:7.6pt;color:var(--muted);line-height:1.55;margin-top:auto;padding-top:4mm;border-top:.2mm solid var(--line)}

/* process */
.mosaic{display:grid;grid-template-columns:repeat(3,1fr);grid-auto-rows:88mm}
.mosaic .c{position:relative;overflow:hidden;color:#fff}
.mosaic .c.ph2::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(6,36,27,0) 45%,rgba(6,36,27,.85))}
.mosaic .cap{position:absolute;left:6mm;right:6mm;bottom:5mm;z-index:2}
.mosaic .cap b{display:block;font:800 9pt var(--display);color:var(--accent);letter-spacing:.05em}
.mosaic .cap h3{font:800 13pt/1.15 var(--display);color:#fff;margin:.6mm 0}
.mosaic .cap p{font-size:7.6pt;color:#e6efe9;line-height:1.4}
.mosaic .solid{background:var(--g900);display:flex;flex-direction:column;justify-content:center;padding:0 7mm}
.mosaic .solid h3{font:800 15pt/1.15 var(--display);color:#fff;margin:2mm 0}
.mosaic .solid p{font-size:8.2pt;color:#c7d6ce}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm;margin-top:6mm}
.steps div{border-top:.7mm solid var(--b700);padding-top:3mm}
.steps b{font:800 22pt/1 var(--display);color:var(--b700)}
.steps h3{font:800 10.5pt var(--display);color:var(--g900);margin:2mm 0 1mm}
.steps p{font-size:8.2pt;color:var(--muted);line-height:1.5}
.regline{margin-top:6mm;font-size:8.4pt;color:var(--text);border-top:.2mm solid var(--line);padding-top:3.5mm}
.regline b{font:700 6.4pt var(--display);letter-spacing:.18em;text-transform:uppercase;color:var(--b700);margin-right:2mm}

/* cover + back */
.cover .grid{position:absolute;left:0;right:0;top:0;height:188mm;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1.25fr 1fr 1fr}
.cover .grid .w{grid-column:1 / -1}
.cover .grid>div{position:relative;overflow:hidden;min-height:0}
.cover .stripe{position:absolute;left:0;right:0;top:188mm;height:3.2mm;background:var(--b700)}
.cover .base{position:absolute;left:0;right:0;top:191.2mm;bottom:0;background:var(--g900);color:#fff}
.cover .logo{position:absolute;left:14mm;top:13mm;width:34mm;height:34mm}
.cover .title{position:absolute;left:62mm;right:14mm;top:13mm}
.cover .title .lbl{margin-bottom:3.4mm;display:block}
.cover h1{color:#fff;font-size:38pt;line-height:1.02}
.cover h1 em{color:var(--accent)}
.cover .sub{font-size:9.6pt;color:#c7d6ce;margin-top:4.5mm;max-width:100mm;line-height:1.55}
.cover .cl{position:absolute;left:14mm;right:14mm;bottom:11mm;display:flex;justify-content:space-between;font-size:8.2pt;color:#c7d6ce;border-top:.25mm solid rgba(255,255,255,.22);padding-top:4mm}
.cover .cl b{color:#fff;font-weight:700}
.back .top{position:absolute;left:0;right:0;top:0;height:116mm}
.back .base{position:absolute;left:0;right:0;top:116mm;bottom:0;background:var(--g900);color:#fff}
.back .stripe{position:absolute;left:0;right:0;top:116mm;height:3.2mm;background:var(--b700);z-index:2}
.back .logo{position:absolute;left:14mm;top:132mm;width:26mm;height:26mm}
.back h1{color:#fff;font-size:27pt;position:absolute;left:50mm;right:14mm;top:130mm}
.back h1 em{color:var(--accent)}
.back .sub{position:absolute;left:50mm;right:14mm;top:163mm;font-size:9.6pt;color:#c7d6ce;line-height:1.55}
.back .ct{position:absolute;left:14mm;right:14mm;top:186mm;display:grid;grid-template-columns:1fr 1fr;gap:0 8mm}
.back .ct div{border-top:.25mm solid rgba(255,255,255,.25);padding:3.4mm 0 4mm}
.back .ct small{display:block;font:700 6.4pt var(--display);letter-spacing:.2em;text-transform:uppercase;color:var(--accent);margin-bottom:1.2mm}
.back .ct b{font:800 14pt var(--display);color:#fff;line-height:1.25;display:block}
.back .ct span{font-size:8.6pt;color:#e2ebe6;line-height:1.5;display:block}
.back .ct .wide{grid-column:1 / -1}
.back .fine{position:absolute;left:14mm;right:14mm;bottom:9mm;font-size:7pt;color:#9db4a9;line-height:1.6}
"""


# ---------------------------------------------------------------- helpers
def li(items):
    return "".join(f"<li>{e(i)}</li>" for i in items)


def band(kind, left, right="R.K. Trading · Food &amp; Natural Products"):
    return f'<div class="band {kind}"><span>{left}</span><span>{right}</span></div>'


def folio(n, bottom=False):
    return f'<div class="pn{" b" if bottom else ""}">{n:02d}</div>'


def enq(key):
    return f'<p class="enq"><b>Include in your enquiry</b>{e("; ".join(ENQ[key]))}.</p>'


def product(num, kind, name, img, text, supply, key, side="l", pos="50% 50%"):
    cls = "prod in" if kind == "Import" else "prod out"
    if side == "r":
        cls += " r"
    lbl = "lbl g" if kind == "Import" else "lbl"
    return f"""<article class="{cls}"><div class="im"><img src="{img}" alt="" style="object-position:{pos}"></div>
<div class="tx"><div class="num">{num:02d}</div><div class="{lbl}" style="margin-top:1.4mm">{kind}</div><h2>{name}</h2><p>{text}</p>
<div class="sh">What we supply</div><ul class="plain">{li(supply)}</ul>
<div class="sh">Include in your enquiry</div><ul class="plain mu">{li(ENQ[key])}</ul></div></article>"""


def hero(img, title, count, h, pos="50% 50%", cls=""):
    n = f'<span class="n">{count}</span>' if count else ""
    return f'<div class="hero {cls}" style="height:{h}mm"><img src="{img}" alt="" style="object-position:{pos}"><div class="t"><h1>{title}</h1>{n}</div></div>'


def group(title, items, cols, count=True):
    c = f"{len(items)} products" if count else ""
    return f'<div class="gh"><h2>{title}</h2><span>{c}</span></div><ul class="list c{cols}">{li(items)}</ul>'


def prow(p):
    name, sub, img, colour, variety, size, shelf, packing = p
    s = f"<small>{e(sub)}</small>" if sub else ""
    items = [("Colour", colour)]
    if variety:
        items.append(("Variety", variety))
    items += [("Size", size), ("Shelf life", shelf)]
    dl = "".join(f'<div{" class=wide" if (i == len(items) - 1 and len(items) % 2) else ""}><dt>{k}</dt><dd>{e(v)}</dd></div>' for i, (k, v) in enumerate(items))
    dl += f'<div class="wide"><dt>Packing</dt><dd>{e(packing)}</dd></div>'
    return f'<article class="prow"><div class="im"><img src="{img}" alt=""></div><div class="tx"><h2>{e(name)}{s}</h2><dl class="spec">{dl}</dl></div></article>'


# ---------------------------------------------------------------- pages
pages = []

# 1 cover
pages.append(f"""<section class="page cover">
<div class="grid">
<div class="w"><img src="img/spices.jpg" alt="" style="object-position:50% 38%"></div>
<div><img src="img/dates.jpg" alt=""></div><div><img src="img/produce.jpg" alt=""></div>
<div><img src="img/dryfruits.jpg" alt=""></div><div><img src="img/tea.jpg" alt="" style="object-position:50% 40%"></div></div>
<div class="stripe"></div>
<div class="base">
<img class="logo" src="img/logo-light-lg.png" alt="R.K. Trading seal" style="object-fit:contain">
<div class="title"><span class="lbl w">Mumbai · India · Since 2017</span><h1>Food &amp; Natural<br>Products<br><em>Catalogue</em></h1>
<p class="sub">Import and export trading from Mumbai to the world. Dates, dry fruits, chocolates, herbals and ayurvedic products in. Spices, tea, grains, fresh produce and FMCG out.</p></div>
<div class="cl"><span><b>{e(PHONE)}</b> &nbsp;·&nbsp; {e(EMAIL)}</span><span>Pricing on quotation</span></div></div>
</section>""")

# 2 intro
pages.append(f"""<section class="page">
<div class="side"><div><img src="img/dryfruits.jpg" alt=""></div><div><img src="img/spices.jpg" alt="" style="object-position:50% 30%"></div><div><img src="img/dates.jpg" alt=""></div></div>
<div class="intro">
<span class="lbl">About R.K. Trading</span>
<h1>One trader, <em>both directions.</em></h1>
<p class="lead">R.K. Trading is a Mumbai-based general trader of food and natural products. Dates, dry fruits, chocolates, herbals and ayurvedic products come in; spices, tea, grains, fresh produce and FMCG go out. Since 2017 we have sourced, graded, packed and shipped, so buyers deal with one accountable partner from enquiry to delivery.</p>
<div class="two">
<div><div class="sh" style="margin-top:0">We import</div><ul class="plain">{li(["Dates, dry and fresh", "Dry fruits and nuts", "Chocolates", "Herbals", "Ayurvedic products"])}</ul></div>
<div><div class="sh" style="margin-top:0">We export</div><ul class="plain">{li(["FMCG products", "Spices", "Tea", "Fresh fruit and vegetables", "Grains"])}</ul></div></div>
<dl class="kv">
<div><dt>Imports from</dt><dd>{e(", ".join(ORIGINS))}</dd></div>
<div><dt>Exports to</dt><dd>{e(", ".join(MARKETS))}</dd></div>
<div><dt>Founded</dt><dd>September 2017, Mumbai</dd></div>
<div><dt>Proprietor</dt><dd>Riyaz Ahmed Wani</dd></div>
<div><dt>How we work</dt><dd>Graded, sized and packed by us. Origin and shelf life confirmed for each product.</dd></div>
<div><dt>Registrations</dt><dd>GST, FSSAI, APEDA, Spices Board, Tea and Udyam. Numbers on request.</dd></div></dl>
<p class="small">R.K. Trading is a general trader. We source from manufacturers and growers and supply to buyers. We are not an authorised distributor or agent of any brand, so every product in this catalogue is described by type and specification, not by brand name.</p>
</div>{folio(2, True)}</section>""")

# 3-5 imports
dts, dry, choc, herb, ayu = IMPORTS
pages.append(f"""<section class="page">{band("in", "Imports")}<div class="feat">
{product(1, "Import", dts[0], dts[1], dts[2], dts[3], "dates", "l")}
{product(2, "Import", dry[0], dry[1], dry[2], dry[3], "dryfruits", "r", "50% 45%")}</div>{folio(3)}</section>""")
pages.append(f"""<section class="page">{band("in", "Imports")}<div class="feat">
{product(3, "Import", choc[0], choc[1], choc[2], choc[3], "chocolates", "l", "50% 50%")}
{product(4, "Import", herb[0], herb[1], herb[2], herb[3], "herbal", "r", "50% 40%")}</div>{folio(4)}</section>""")
origins = "".join(f"<li>{e(o)}</li>" for o in ORIGINS)
pages.append(f"""<section class="page">{band("in", "Imports")}<div class="feat">
{product(5, "Import", ayu[0], ayu[1], ayu[2], ayu[3], "ayurvedic", "l", "50% 50%")}
<article class="prod solid"><div class="tx"><span class="lbl w">Origins</span><h2 style="margin:2mm 0 2.6mm">Where we import from</h2>
<p>We source from six countries for buyers in India. Need a different origin? Ask us and we will tell you what is possible.</p>
<ul class="big" style="columns:2;column-gap:9mm">{origins}</ul></div></article></div>{folio(5)}</section>""")

# 6 exports: FMCG + tea
fm, sp, tea, prod_, gr = EXPORTS
pages.append(f"""<section class="page">{band("out", "Exports")}<div class="feat">
{product(1, "Export", fm[0], "img/fmcg.jpg", fm[2] + " Products are described by type and specification, not by brand name.", fm[3], "fmcg", "l", "50% 50%")}
{product(2, "Export", tea[0], tea[1], tea[2], tea[3], "tea", "r", "50% 45%")}</div>{folio(6)}</section>""")

# 7 spices
pages.append(f"""<section class="page">{band("cat", "Export range · Spices")}<div class="flow">
{hero("img/spices.jpg", "Whole spices", f"{len(WHOLE_SPICES)} products", 140, "50% 40%")}
<div class="body"><ul class="list c3">{li(WHOLE_SPICES[1:])}</ul>
<div class="feature-strip" style="margin-top:7mm"><div class="im"><img src="img/saffron.jpg" alt=""></div><div><span class="lbl">Featured</span><h3>Kashmiri saffron, grade A++</h3><p>Whole threads, graded and packed by us. Pack size and quantity are confirmed at quotation.</p></div></div>
{enq("spices")}</div></div>{folio(7)}</section>""")

# 8 grains + flours
pages.append(f"""<section class="page">{band("cat", "Export range · Grains &amp; flours")}<div class="flow">
<div class="duo">{hero("img/grains.jpg", "Grains", f"{len(GRAINS)} products", 118, "50% 50%")}{hero("img/flour-spoons.jpg", "Flours", f"{len(FLOURS)} products", 118, "50% 45%")}</div>
<div class="body">{group("Grains", GRAINS, 4, False)}{group("Flours", FLOURS, 3)}
{enq("grains")}</div></div>{folio(8)}</section>""")

# 9 grocery
pages.append(f"""<section class="page">{band("cat", "Export range · General grocery")}<div class="flow">
{hero("img/dates.jpg", "General grocery", f"{len(GROCERY)} products", 62, "50% 55%")}
<div class="body"><ul class="list c3">{li(GROCERY)}</ul>
<p class="enq" style="margin-top:4mm">Product names follow common trade usage. Specification, grade and pack size for any item are confirmed at quotation.</p>
{enq("grocery")}</div></div>{folio(9)}</section>""")

# 10 khakhra / papad / chutneys
pages.append(f"""<section class="page">{band("cat", "Export range · Bakery, papad &amp; chutneys")}<div class="flow">
<div class="duo">{hero("img/papad.jpg", "Papad", f"{len(PAPAD)} products", 122, "50% 50%")}{hero("img/chutney.jpg", "Chutneys &amp; pastes", f"{len(CHUTNEYS)} products", 122, "50% 50%")}</div>
<div class="body">{group("Papad", PAPAD, 3)}{group("Chutneys &amp; pastes", CHUTNEYS, 3)}{group("Khakhra &amp; bakery", KHAKHRA, 3)}</div></div>{folio(10)}</section>""")

# 11 instant mix + snacks
pages.append(f"""<section class="page">{band("cat", "Export range · Instant mixes &amp; snacks")}<div class="flow">
<div class="split"><div class="im"><img src="img/snacks.jpg" alt=""></div><div class="tx"><span class="lbl">Export range</span><h1 style="margin:2mm 0 3mm">Instant mixes <em>&amp; snacks.</em></h1><p>Ready-to-cook mixes and traditional snacks, packed and labelled to the buyer's requirements. Ask us about pack size and labelling language.</p></div></div>
<div class="body">{group("Instant mix", INSTANT, 4)}{group("Namkeen &amp; snacks", SNACKS, 4)}
<p class="enq">All packs are labelled to the buyer's requirements. Ask us about labelling language and pack size.</p></div></div>{folio(11)}</section>""")

# 12-13 fresh produce
def produce_page(rows, n, title, lead):
    return f"""<section class="page">{band("cat", "Export range · Fresh produce")}<div class="flow">
<div class="ph"><span class="lbl">Fresh produce specifications</span><h1 style="margin-top:2mm">{title}</h1><p>{lead}</p></div>
{"".join(prow(p) for p in rows)}</div>{folio(n)}</section>"""


allp = PRODUCE_A + PRODUCE_B
order = {p[0] + p[1]: p for p in allp}
rows1 = [order[k] for k in ("Red OnionDark red", "Red OnionLight red", "White Onion", "Garlic", "Potato")]
rows2 = [order[k] for k in ("Lemon", "Pomegranate", "Banana", "Cherry Tomato", "Green Chilli")]
pages.append(produce_page(rows1, 12, "Onions, garlic <em>and potato.</em>", "Shelf life is counted from the date of packing. Seasonal availability is confirmed at quotation."))
pages.append(produce_page(rows2, 13, "Lemon, fruit, tomato <em>and chilli.</em>", "Every lot is sized and graded by us before it is packed."))

# 14 how we work
pc = ""
for i, (t, img, d) in enumerate(PROCESS):
    pc += f'<div class="c ph2"><img src="{img}" alt=""><div class="cap"><b>0{i + 1}</b><h3>{t}</h3><p>{d}</p></div></div>'
pc += '<div class="c solid"><span class="lbl w">How we work</span><h3>One team, start to finish.</h3><p>We grade, size, pack, label and load every order ourselves, so you deal with one accountable partner.</p></div>'
steps = "".join(f"<div><b>{i + 1}</b><h3>{t}</h3><p>{d}</p></div>" for i, (t, d) in enumerate(STEPS))
pages.append(f"""<section class="page">{band("out", "How we work")}<div class="flow" style="bottom:0">
<div class="mosaic">{pc}</div>
<div class="body" style="padding-top:8mm"><span class="lbl">How buying works</span><div class="steps">{steps}</div>
<p class="regline"><b>Registrations</b>GST, FSSAI, APEDA, Spices Board, Tea and Udyam. Registration numbers are available on request.</p></div></div>{folio(14)}</section>""")

# 15 back
pages.append(f"""<section class="page back">
<div class="top"><img src="img/shipping.jpg" alt="" style="object-position:50% 52%"></div>
<div class="base"></div><div class="stripe"></div>
<img class="logo" src="img/logo-light-lg.png" alt="R.K. Trading seal" style="object-fit:contain">
<h1>Tell us what you need to <em>import or export.</em></h1>
<p class="sub">Send an enquiry and we will come back to you with a quotation. MOQ, lead times and terms are shared by phone.</p>
<div class="ct"><div><small>Phone &amp; WhatsApp</small><b>{e(PHONE)}</b></div><div><small>Email</small><b>{e(EMAIL)}</b></div>
<div class="wide"><small>Office</small><span>{e(ADDRESS)}</span></div></div>
<p class="fine">R.K. Trading is a general trader and is not an authorised distributor or agent of any brand. Products are described by type and specification. Origin, shelf life and specifications are confirmed for each product at quotation. Images are for illustration.</p>
</section>""")

DOC = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>R.K. Trading — Food &amp; Natural Products Catalogue</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head>
<body>{"".join(pages)}</body></html>"""

(HERE / "brochure.html").write_text(DOC, encoding="utf-8")
print("wrote brochure.html,", len(pages), "pages")

if "--pdf" in sys.argv:
    import time
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    out = HERE.parent / "RK-Trading-Food-and-Natural-Products.pdf"
    started = time.time()
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", (HERE / "brochure.html").as_uri()], check=True, timeout=180)
    while not (out.exists() and out.stat().st_mtime >= started and out.stat().st_size > 0):
        if time.time() - started > 120:
            raise SystemExit("Edge did not write the PDF")
        time.sleep(1)
    time.sleep(2)
    print("wrote", out)
