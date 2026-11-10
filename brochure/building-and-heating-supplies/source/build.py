"""
Builds brochure.html for the R.K. Trading Building & Heating Supplies catalogue.

    python build.py            -> writes brochure.html
    python build.py --pdf      -> also prints ../RK-Trading-Building-and-Heating-Supplies.pdf with Microsoft Edge (headless)

Copy follows the website: no brand names, pricing on quotation. Same layout system as the
Food & Natural Products catalogue (../../food-and-natural-products/source/build.py).
"""
import html
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
e = html.escape

PHONE = "+91 70064 01698"
EMAIL = "riyazwani2015@gmail.com"
ADDRESS = "Flat 15, 3rd Floor, Haji Abdul Majid Apartments, Swami Vivekanand Marg (behind Jasmine Apts), Andheri West, Mumbai – 400058, Maharashtra, India"

ORIGINS = ["China", "Turkey", "Afghanistan", "Dubai (UAE)", "Oman", "Italy"]

IMPORTS = [
    ("Boilers, Heat Pumps &amp; Heating Equipment", "img/pellet-boiler-1.jpg",
     "Boilers, heat pumps and heating equipment for homes, commercial buildings and industrial sites. Tell us the capacity and fuel or power source you need and we will source to match.",
     ["Boilers", "Heat pumps", "Heating equipment"]),
    ("PPR Pipes &amp; Fittings", "img/ppr.jpg",
     "PPR pipes and fittings for hot and cold water systems, imported in the sizes and pressure ratings your project needs.",
     ["PPR pipes", "PPR fittings"]),
    ("Building &amp; Flooring Materials", "img/building.jpg",
     "WPC and WPA flooring and other building and construction materials for contractors, builders and distributors.",
     ["WPC flooring", "WPA products", "Building materials", "Construction materials"]),
]

PROCESS = [
    ("Procurement", "img/building.jpg", "Products sourced from our suppliers to the agreed specification."),
    ("Labelling", "img/process-labelling.jpg", "Every pack labelled to the buyer's requirements."),
    ("Loading", "img/process-loading.jpg", "Careful loading into containers and trucks."),
    ("Shipping", "img/shipping.jpg", "Shipped to your destination."),
    ("Unloading", "img/unloading.jpg", "Unloaded and handed over at delivery."),
]
STEPS = [
    ("Send an enquiry", "Tell us the product, quantity and destination."),
    ("Get your quotation", "We confirm price, specification and origin. MOQ, lead time and terms are shared by phone."),
    ("We pack and ship", "We pack, label and load your order and ship it to the destination."),
]

ENQ = {
    "heating": ["Type and capacity (kW or output)", "Fuel or power source", "Quantity and delivery location"],
    "ppr": ["Pipe diameters and pressure rating", "Fittings required", "Quantity and delivery location"],
    "building": ["Product (WPC, WPA or other) and dimensions", "Thickness, finish and colour", "Quantity and delivery location"],
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


def band(kind, left, right="R.K. Trading · Building &amp; Heating Supplies"):
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



CSS += """
.trio{display:grid;grid-template-columns:repeat(3,1fr);gap:1.4mm}
.trio figure{position:relative;height:68mm;overflow:hidden}
.trio figcaption{position:absolute;left:0;right:0;bottom:0;padding:6mm 4mm 2.4mm;color:#fff;font:700 6.8pt var(--display);letter-spacing:.16em;text-transform:uppercase;background:linear-gradient(180deg,rgba(6,36,27,0),rgba(6,36,27,.8))}
.tcols{display:grid;grid-template-columns:repeat(3,1fr);gap:8mm}
.tcols.two{grid-template-columns:1fr 1fr}
.tcols p{font-size:9pt;line-height:1.55}
.tcols p{margin-bottom:1mm}
.tcols>div>.sh:first-child{margin-top:0}
.tcols .t{font:800 11.5pt/1.2 var(--display);color:var(--g900);margin-bottom:2mm}
.origins{position:absolute;left:0;right:0;bottom:0;height:62mm;background:var(--g900);color:#fff;padding:7mm 14mm 0}
.origins h2{color:#fff;font-size:14pt;margin:1.6mm 0 1.4mm}
.origins p{font-size:8.6pt;color:#c7d6ce;margin-bottom:3mm;max-width:130mm}
.origins ul{columns:3;column-gap:8mm}
.origins li{font:800 12pt/1 var(--display);padding:2.3mm 0;border-bottom:.25mm solid rgba(255,255,255,.22);break-inside:avoid}
"""


# ---------------------------------------------------------------- pages
pages = []
heat, ppr, bld = IMPORTS

# 1 cover
pages.append(f"""<section class="page cover">
<div class="grid">
<div class="w"><img src="img/pellet-boiler-1.jpg" alt="" style="object-position:50% 40%"></div>
<div><img src="img/pellet-stove.jpg" alt=""></div><div><img src="img/ppr.jpg" alt=""></div>
<div><img src="img/building.jpg" alt=""></div><div><img src="img/heatpump.jpg" alt="" style="object-position:50% 60%"></div></div>
<div class="stripe"></div>
<div class="base">
<img class="logo" src="img/logo-light-lg.png" alt="R.K. Trading seal" style="object-fit:contain">
<div class="title"><span class="lbl w">Mumbai · India · Since 2017</span><h1>Building &amp; Heating<br>Supplies<br><em>Catalogue</em></h1>
<p class="sub">Import trading from Mumbai. Boilers, heat pumps and heating equipment, PPR pipes and fittings, and building and flooring materials, sourced to your specification.</p></div>
<div class="cl"><span><b>{e(PHONE)}</b> &nbsp;·&nbsp; {e(EMAIL)}</span><span>Pricing on quotation</span></div></div>
</section>""")

# 2 about
pages.append(f"""<section class="page">
<div class="side"><div><img src="img/pellet-boiler-2.jpg" alt="" style="object-position:55% 50%"></div><div><img src="img/ppr.jpg" alt=""></div><div><img src="img/building.jpg" alt=""></div></div>
<div class="intro">
<span class="lbl">About R.K. Trading</span>
<h1>Sourced to <em>your specification.</em></h1>
<p class="lead">R.K. Trading is a Mumbai-based general trader. We import heating equipment, PPR pipes and fittings, and building and flooring materials from six countries for buyers in India. Since 2017 we have sourced, packed and shipped, so buyers deal with one accountable partner from enquiry to delivery.</p>
<div class="two">
<div><div class="sh" style="margin-top:0">We import</div><ul class="plain">{li(["Boilers, heat pumps and heating equipment", "PPR pipes and fittings", "WPC and WPA flooring", "Building and construction materials"])}</ul></div>
<div><div class="sh" style="margin-top:0">We supply to</div><ul class="plain">{li(["Homes", "Commercial buildings", "Industrial sites", "Contractors, builders and distributors"])}</ul></div></div>
<dl class="kv">
<div><dt>Imports from</dt><dd>{e(", ".join(ORIGINS))}</dd></div>
<div><dt>Founded</dt><dd>September 2017, Mumbai</dd></div>
<div><dt>Proprietor</dt><dd>Riyaz Ahmed Wani</dd></div>
<div><dt>How we work</dt><dd>Sourced to the agreed specification. Origin and specifications confirmed for each product.</dd></div>
<div><dt>Registrations</dt><dd>GST and Udyam. Numbers on request.</dd></div></dl>
<p class="small">R.K. Trading is a general trader. We source from manufacturers and supply to buyers. We are not an authorised distributor or agent of any brand, so every product in this catalogue is described by type and specification, not by brand name.</p>
</div>{folio(2, True)}</section>""")

# 3 heating
pages.append(f"""<section class="page">{band("in", "Imports · Heating equipment")}<div class="flow">
{hero("img/pellet-boiler-1.jpg", "Heating equipment", "Boilers · Heat pumps · Stoves", 124, "50% 35%")}
<div class="trio">
<figure><img src="img/pellet-boiler-2.jpg" alt=""><figcaption>Pellet boiler</figcaption></figure>
<figure><img src="img/pellet-stove.jpg" alt="" style="object-position:50% 40%"><figcaption>Pellet stove</figcaption></figure>
<figure><img src="img/heatpump.jpg" alt="" style="object-position:55% 60%"><figcaption>Heat pump</figcaption></figure></div>
<div class="body" style="padding-top:7mm">
<p class="lead" style="margin:0 0 6mm;max-width:none">Boilers, heat pumps and heating equipment for homes, commercial buildings and industrial sites. Tell us the capacity and fuel or power source you need and we will source to match.</p>
<div class="tcols">
<div><div class="sh">What we supply</div><ul class="plain">{li(heat[3])}</ul></div>
<div><div class="sh">Used in</div><ul class="plain">{li(["Homes", "Commercial buildings", "Industrial sites"])}</ul></div>
<div><div class="sh">Include in your enquiry</div><ul class="plain mu">{li(ENQ["heating"])}</ul></div></div></div></div>{folio(3)}</section>""")

# 4 ppr + building + origins
origins = "".join(f"<li>{e(o)}</li>" for o in ORIGINS)
pages.append(f"""<section class="page">{band("in", "Imports · PPR &amp; building materials")}<div class="flow" style="bottom:0">
<div class="duo">{hero("img/ppr.jpg", "PPR pipes &amp; fittings", "", 84, "50% 50%")}{hero("img/building.jpg", "Building materials", "", 84, "50% 50%")}</div>
<div class="body" style="padding-top:7mm"><div class="tcols two">
<div><p>{ppr[2]}</p>
<div class="sh">What we supply</div><ul class="plain">{li(ppr[3])}</ul>
<div class="sh">Used for</div><ul class="plain">{li(["Hot water systems", "Cold water systems"])}</ul>
<div class="sh">Include in your enquiry</div><ul class="plain mu">{li(ENQ["ppr"])}</ul></div>
<div><p>{bld[2]}</p>
<div class="sh">What we supply</div><ul class="plain">{li(bld[3])}</ul>
<div class="sh">Supplied to</div><ul class="plain">{li(["Contractors", "Builders", "Distributors"])}</ul>
<div class="sh">Include in your enquiry</div><ul class="plain mu">{li(ENQ["building"])}</ul></div></div></div>
<div class="origins"><span class="lbl w">Origins</span><h2>Where we import from</h2>
<p>We source from six countries for buyers in India. Need a different origin? Ask us and we will tell you what is possible.</p><ul>{origins}</ul></div></div>{folio(4)}</section>""")

# 5 how we work
pc = ""
for i, (t, img, d) in enumerate(PROCESS):
    pc += f'<div class="c ph2"><img src="{img}" alt=""><div class="cap"><b>0{i + 1}</b><h3>{t}</h3><p>{d}</p></div></div>'
pc += '<div class="c solid"><span class="lbl w">How we work</span><h3>One team, start to finish.</h3><p>We source, pack, label and load every order ourselves, so you deal with one accountable partner.</p></div>'
steps = "".join(f"<div><b>{i + 1}</b><h3>{t}</h3><p>{d}</p></div>" for i, (t, d) in enumerate(STEPS))
pages.append(f"""<section class="page">{band("out", "How we work")}<div class="flow" style="bottom:0">
<div class="mosaic">{pc}</div>
<div class="body" style="padding-top:8mm"><span class="lbl">How buying works</span><div class="steps">{steps}</div>
<p class="regline"><b>Registrations</b>GST and Udyam. Registration numbers are available on request.</p></div></div>{folio(5)}</section>""")

# 6 back
pages.append(f"""<section class="page back">
<div class="top"><img src="img/shipping.jpg" alt="" style="object-position:50% 52%"></div>
<div class="base"></div><div class="stripe"></div>
<img class="logo" src="img/logo-light-lg.png" alt="R.K. Trading seal" style="object-fit:contain">
<h1>Tell us what you need to <em>import.</em></h1>
<p class="sub">Send an enquiry and we will come back to you with a quotation. MOQ, lead times and terms are shared by phone.</p>
<div class="ct"><div><small>Phone &amp; WhatsApp</small><b>{e(PHONE)}</b></div><div><small>Email</small><b>{e(EMAIL)}</b></div>
<div class="wide"><small>Office</small><span>{e(ADDRESS)}</span></div></div>
<p class="fine">R.K. Trading is a general trader and is not an authorised distributor or agent of any brand. Products are described by type and specification. Origin and specifications are confirmed for each product at quotation. Images are for illustration.</p>
</section>""")

DOC = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>R.K. Trading — Building &amp; Heating Supplies Catalogue</title>
<meta name="viewport" content="width=device-width,initial-scale=1"><style>{CSS}</style></head>
<body>{"".join(pages)}</body></html>"""

(HERE / "brochure.html").write_text(DOC, encoding="utf-8")
print("wrote brochure.html,", len(pages), "pages")

if "--pdf" in sys.argv:
    import time
    edge = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    out = HERE.parent / "RK-Trading-Building-and-Heating-Supplies.pdf"
    started = time.time()
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out}", (HERE / "brochure.html").as_uri()], check=True, timeout=180)
    while not (out.exists() and out.stat().st_mtime >= started and out.stat().st_size > 0):
        if time.time() - started > 120:
            raise SystemExit("Edge did not write the PDF")
        time.sleep(1)
    time.sleep(2)
    print("wrote", out)
