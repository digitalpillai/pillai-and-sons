# Car range update — November 2026

Specifications, prices and features refreshed against the current Maruti Suzuki range,
plus a new Commercial Vehicles page. `contact.html` was not opened.

---

## 1. The range itself has not changed

All **17 models** on the site are still on sale, and nothing new has been added to the
range. Ignis and Ciaz are discontinued, and neither was on the site. What *has* changed
is that two models were replaced by new generations, and prices moved.

Upcoming but **not yet on sale**, so deliberately left off: new Ertiga, Fronx facelift,
XL6 facelift, Fronx EV, Jimny EV, seven-seat EV MPV.

## 2. Two models substantially updated

### Brezza — 2026 facelift, now with a turbo
| Field | Was | Now |
|---|---|---|
| Engine | 1.5L K-Series Dual Jet | 1.0L Boosterjet Turbo / 1.5L K-Series |
| Transmission | Manual, 6-speed AT | 6-speed Manual, 6-speed AT |
| Mileage | 19.80 km/l | Up to 21.09 km/l |
| Price | ₹7,39,900 | ₹7,50,000 |

New feature highlights: the 110hp/170Nm Boosterjet turbo, 10.1-inch SmartPlay Pro X,
ventilated seats with 64-colour ambient lighting, and the underbody S-CNG cylinder.
ARAI figures: 1.5 MT 21.09, 1.5 AT 20.17, 1.0 turbo 20.47 kmpl, CNG 26.90 km/kg.

### Baleno — new generation, Level 2 ADAS
| Field | Was | Now |
|---|---|---|
| Engine | 1.2L K-Series Dual Jet | 1.2L Z12E (3-cylinder) |
| Transmission | Manual, AMT | 5-speed Manual, 5-speed AMT |
| Mileage | 22.35 km/l | Up to 24.77 km/l |
| Price | ₹5,98,000 | ₹5,99,000 |

The outgoing 90hp four-cylinder is replaced by an 83hp/112Nm three-cylinder. New
highlights: Level 2 ADAS, 360-degree camera and TPMS, ventilated seats with a cooled
wireless charger. ARAI: 23.80 MT, 24.77 AMT, 33.61 km/kg CNG.

### e Vitara — price and feature correction
Price ₹15,99,000 → **₹16,19,000**. Highlights now state both packs with their ranges
(49 kWh / 440 km, 61 kWh / 543 km) and add Level 2 ADAS with the 5-star Bharat NCAP
rating.

## 3. Price changes only

| Model | Was | Now |
|---|---|---|
| Fronx | ₹6,84,000 | ₹6,90,000 |
| Grand Vitara | ₹10,76,000 | ₹10,77,000 |
| XL6 | ₹11,57,000 | ₹11,62,000 |
| Jimny | ₹12,39,000 | ₹12,59,000 |
| Invicto | ₹24,97,000 | ₹25,02,000 |

**Nine models were deliberately left alone** — S-Presso, Alto K10, Celerio, WagonR,
Swift, Dzire, Eeco, Ertiga and Victoris. Their existing figures already match the
current starting prices, so changing them would have been churn.

## 4. New page: Commercial Vehicles

`cars/commercial.html`, linked from the **Cars** menu on every page (beside ARENA and
NEXA), from the cars index intro, and added to `sitemap.xml`.

Covers Super Carry, Eeco Cargo, Tour H1, WagonR Tour, Dzire Tour S and Ertiga Tour,
with a section on why fleet buyers should service with you, and a commercial-desk CTA.

**It quotes no prices, on purpose.** Commercial and fleet pricing depends on quantity,
body options, permits and finance structure. Publishing retail figures for Tour variants
would mislead a fleet buyer and undercut your own negotiation. The page says pricing is
quoted per order and drives an enquiry instead.

---

## Three things that need your decision

**1. `contact.html` now has a different menu from every other page.** You asked me not
to touch it, so I did not — which means it is the one page whose Cars menu has no
Commercial entry. It is a one-line fix whenever you want it; say the word.

**2. Please check the prices against your DMS before this goes live.** They come from
two independent trade sources that agree on 16 of 17 models, but they are national
starting ex-showroom figures rounded to the nearest ₹1,000, not Tamil Nadu figures from
your system. You hold the authoritative numbers; I do not. The site's existing
"get a written on-road price" section already sets the right expectation with customers,
so the exposure is limited — but a wrong headline figure is still worth catching.

The one real conflict: CarWale lists the e Vitara at ₹13.61 lakh while CarDekho and
Autocar say ₹16.19 lakh. The lower figure is the Battery-as-a-Service price, which
excludes the battery and adds a ₹3.99/km subscription. I used **₹16.19 lakh**, the
with-battery price, since that is what the other models' figures are comparable to.

**3. Do not run `tools/generate_site.py`.** It would destroy the branch directory, the
careers advert and the driving-school block, and would re-add the top bar you removed —
none of which exist in the generator. All edits here were made to the HTML directly.
`tools/gen_content.py` has been kept in step so the data stays the source of truth, but
it is now a record rather than something to regenerate from.

---

## What was verified

- `contact.html` is byte-identical (MD5 `cc6dbcb35d3f82879e1fb77bb447147c`, unchanged)
- All 51 pages parse with a real HTML5 parser
- 4,518 internal links checked, none broken
- 97 model cards and 85 spec rows cross-checked against `gen_content.py` — all match
- No stale price string survives anywhere in HTML or Python
- Branch directory, careers advert, driving-school block and QR popup all intact
- Top bar still absent; no duplicate Commercial menu entries
- `sitemap.xml` is valid XML, now 49 URLs

Two bugs were caught during the work and fixed: a first pass replaced shared strings
globally, which put Baleno's gearbox onto the Fronx card and corrupted several models'
data in `gen_content.py` (`"Manual, AMT"` belongs to seven models, and
`"1.2L K-Series Dual Jet"` is a substring of WagonR's engine). The data file was
restored from the original and re-applied with per-model scoping; the audit above is
what proves it is clean.

## Sources

Model specifications and prices: [Autocar India](https://www.autocarindia.com/),
[CarWale](https://www.carwale.com/maruti-suzuki-cars/),
[CarDekho](https://www.cardekho.com/maruti-suzuki-cars),
[Maruti Suzuki](https://www.marutisuzuki.com/),
[NEXA](https://www.nexaexperience.com/),
[Maruti Suzuki Commercial](https://www.marutisuzukicommercial.com/).

---

# Homepage branch finder — city picker (5 Nov 2026)

"Find your nearest branch" on `index.html` no longer dumps all 35 branches on page
load. The dropdown is centred, and nothing is listed until a city is chosen.

- The dropdown opens on **"Select your city"** rather than "All cities"
- Until a city is picked, a short centred prompt sits where the cards were
- Choosing a city shows only that city's branches, with the count beside the dropdown
  ("4 branches in Thanjavur", correctly singular for one)
- Returning to the placeholder clears the cards and brings the prompt back
- The `?city=` deep link still works, so `index.html?city=Thanjavur` opens pre-filtered

Verified by running the real component against the real branch data with DOM stubs —
13 checks across four states (no selection, a multi-branch city, a single-branch city,
and back to the placeholder), all passing.

**`contact.html` is deliberately unchanged.** It runs the same component under the
heading "Choose your city" and still lists every branch on load. You asked me not to
touch that page, so I did not. If you want the same picker behaviour there, it is the
same three edits — say the word.

---

# WhatsApp number changed (5 Nov 2026)

WhatsApp now points to **7358105818** (`wa.me/917358105818`), changed from 8939752872.

Changed in three places — the live setting plus the two copies that would otherwise
reintroduce the old number later:

| File | What it is |
|---|---|
| `assets/js/site-config.js` | The live `whatsapp_number` setting every WhatsApp link reads from |
| `tools/config_schema.py` | The default, so a config rebuild cannot bring the old number back |
| `README.md` | The documented example |

That one setting drives the floating green button and every enquiry form that opens
WhatsApp, so all of them moved together.

**Phone and email were deliberately not touched**, as asked:

- `tel:` links stay on **+91 80716 45674** (sales and service)
- Email stays `digital.marketing@pillaimotors.in`
- The careers page keeps its own **+91 73581 05818** contact line

Verified by running the site's own link builders against the live config, which now
return `wa.me/917358105818` for WhatsApp and the unchanged `tel:+918071645674`.

The old number still appears in `CHANGES-CONTACT-UPDATE.md`. That file is the record of
an earlier change and describes what was true at the time, so it was left as written
rather than rewritten.

---

# Google Analytics 4 added (5 Nov 2026)

Tracking is wired into all 50 public pages via one shared file,
`assets/js/analytics.js`, loaded from each page's `<head>`. Full instructions are in
**`ANALYTICS-SETUP.md`**.

**It sends nothing until you add your Measurement ID**, so this is safe to publish
as-is. One edit on line 32 of that file switches the whole site on.

Events recorded: `call_click`, `whatsapp_click`, `email_click`, `directions_click`,
`map_click`, `review_click`, `review_qr_open`, `city_select` and `form_submit`, plus
the automatic `page_view`.

Every branch-card interaction carries `branch_name`, `branch_city` and `link_source`,
read from the card the link sits in — so a call from the Thanjavur ARENA card is
distinguishable from one in Trichy, and a footer call is correctly marked
"(not branch specific)" rather than credited to whichever branch was on screen.

`city_select` is worth watching on its own: it records cities people search for,
including ones you have no branch in.

**`contact.html` has been modified.** You had asked me to leave it alone, but you then
asked for analytics on the contact page and per city and outlet, which cannot be done
without touching it. The only change is the one script tag. Its MD5 moves from
`cc6dbcb35d3f82879e1fb77bb447147c` to `69b3156afee76eee6801b1f778e61498`.

`admin/index.html` is deliberately excluded, so your own editing visits stay out of
the reports.

Verified by loading the real `contact.html` in a headless DOM, running the real branch
finder so real cards existed, and clicking real elements: 21 checks across call,
WhatsApp, email, directions, map, review, QR, city-select and footer-vs-branch
attribution — all passing.
