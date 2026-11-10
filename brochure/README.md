# Brochures

Two catalogues, built from the same layout system. Each folder holds its PDF and a `source/` folder.

| Catalogue | PDF | Pages |
| --- | --- | --- |
| Food & Natural Products | `food-and-natural-products/RK-Trading-Food-and-Natural-Products.pdf` | 15 |
| Building & Heating Supplies | `building-and-heating-supplies/RK-Trading-Building-and-Heating-Supplies.pdf` | 6 |

`original/RK-Trading-Brochure-original.pdf` is the untouched copy of the old brochure.

## Rebuild after an edit

All copy, product lists and specs are in the data blocks of each `source/build.py`. After editing, from that `source` folder:

```bash
python build.py --pdf
```

This needs Python and Microsoft Edge (the PDF is printed with Edge in headless mode). `python build.py` alone only rewrites `brochure.html`.

## Food & Natural Products

Imports: dates, dry fruits and nuts, chocolates, herbals, ayurvedic products. Exports: FMCG (packaged food, beverages, snacks, instant mixes), spices, tea, grains, fresh produce, plus the full product lists.

Open points:
- The "What we supply" lines for dry fruits, chocolates, herbals and ayurvedic are placeholders from common product types (the `IMPORTS` list in `build.py`). Confirm with the client.
- Photos for the new lines and the FMCG shop-aisle photo are free stock photos. The aisle photo may show brand logos on the shelves, so swap it for a brand-free one.
- Pomegranate and green chilli sizes in the old brochure read "150 mm – 450 mm+", which cannot be right. They say "Confirmed at quotation".

## Building & Heating Supplies

Imports only: boilers, heat pumps and heating equipment; PPR pipes and fittings; WPC and WPA flooring and other building materials. Content comes from the website; it is short because the client has not yet given specifications.

Open points:
- No models, capacities, sizes, pressure ratings or dimensions yet. Ask the client for them and add a detail page per product line.
- The pipe photo is a stock photo of grey pipes, not PPR. The flooring photo is wood decking, not WPC. Replace both with the client's own.
- Photos of the boilers, stove and heat pump are from the website or stock. Check the equipment for visible brand labels before sending.
- "WPA" is not expanded anywhere (the website has the same gap).
- Only GST and Udyam are listed as registrations, as on the website. The IEC (Import Export Code) is still unconfirmed.

## Both

- Contact details match the website. The old brochure listed two more phone numbers (+91 76780 16898 and +91 96180 87826). Keep or drop?
- Registration numbers are still pending.
- English only for now.
