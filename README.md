# Pillai &amp; Sons Motor Company — website

A complete static website for an authorised Maruti Suzuki dealership in
Thanjavur. Plain HTML5, CSS3 and vanilla JavaScript — no framework, no build
step, no server, no database, no monthly bill.

**49 pages** covering all five sides of the business: ARENA and NEXA new cars,
True Value pre-owned, the authorised workshop, the Maruti Driving School, plus
the usual company, legal and contact pages.

---

## The two ways in

There is one website here, and two front doors to it.

| | Who it is for | Where |
|---|---|---|
| **The website** | Customers | `index.html` |
| **The editor** | You | `admin/index.html` |

Open `admin/index.html` in any browser — from the folder on your computer, or on
the live site — change what you like, press **Save changes**, then refresh a page
of the website. Your edit is there.

There is nothing to install and nothing to log into.

---

## Quick start

1. Double-click `index.html` to see the site.
2. Open `admin/index.html` to change anything on it.
3. When you are ready to go live, follow **DEPLOY.md**.

---

## What you can change, and where

### Everything at once — the spreadsheet

`config/site-config.xlsx` holds every business detail, colour and font setting
in five sheets:

| Sheet | Holds |
|---|---|
| **Business** | Name, both phone numbers, WhatsApp number, email, address, opening hours, Google Map, counters, the dealer disclaimer |
| **Colors** | 25 colours, including one for each of the five channels |
| **Fonts** | Font families, every heading size for desktop, tablet and mobile, weights, letter spacing, corner radius, page width |
| **Social** | Facebook, Instagram, YouTube, LinkedIn, X, Pinterest, IndiaMART, JustDial, WhatsApp — with a yes/no switch for each |
| **Themes** | The five palettes a visitor can choose from using the paint button |

Edit it in Excel, Numbers or Google Sheets, then either:

- **No Python:** open `admin/index.html` → **Excel config** → drop the file in.
  It shows you exactly what changed before you apply it.
- **With Python:** `python3 tools/build_config.py`

Both routes end up writing `assets/js/site-config.js`, which is the file the
website actually reads.

### Page by page — the editor

`admin/index.html` has six sections:

- **Business details** — the same fields as the Business sheet
- **Page content** — 306 editable headings, paragraphs and labels, grouped by
  part of the site
- **Images &amp; video** — every photograph on the site: the 17 cars and the page
  banners, each replaceable with your own
- **Colours** — every colour with a picker and a live preview of the home page
- **Fonts &amp; sizes** — typography, radius and page width
- **Social &amp; directory links** — the profile URLs

**Save changes** writes to your browser's storage, so you see your edits
immediately on your own machine. To make them live for everyone, go to
**Save &amp; publish** and follow the two steps there — it hands you the two files
to upload.

Also on that tab: **Download a backup** (one JSON file with everything) and
**Restore from a backup**. Take one before you make big changes.

---

## About the logo

`assets/images/logo.png` is your file, byte for byte as you supplied it — not
recoloured, not cropped, no background removed, no rounded corners. It is used
in the header, in the footer, as the browser tab icon, in the editor and on the
share card that appears when someone posts a link to the site.

Because the mark carries no lettering, it sits beside the company name set in
the site's own type. That keeps "Pillai & Sons Motor Company" in the header for
readers and for search engines without touching the artwork. Both lines come
from the **Business** sheet (`business_name` and `tagline`), so renaming the
business updates them everywhere.

To swap the logo later, replace `assets/images/logo.png` with a file of the same
name. Nothing else needs to change.

---

## About the pictures

Every photograph on this site came from your own Maruti Suzuki media folders —
NEXA, ARENA, True Value and the Driving School — and each one was chosen for the
page it sits on rather than picked at random. Sixty files in all: seventeen car
photographs, twenty-seven page banners and section images, and sixteen icons.

Two things had to be fixed on the way in, and both would have broken the site
silently if they had not been:

- **Most of those files were not the format their name claimed.** Around 4,200 of
  the roughly 5,000 images were AVIF carrying a `.png` or `.jpg` extension.
  Copied across untouched they would have been served as `image/png` and would
  not have displayed. Everything used here was decoded, re-encoded and re-named
  to match what it actually is.
- **They were far too large.** The four folders total 259 MB. The site now uses
  3.5 MB of imagery, resized and compressed, with each car trimmed of its
  transparent margin so it fills the card instead of floating in it.

Car photographs are WebP with transparency, so each car sits on the card's own
background. Banners are JPEG. Every one of them is an editable slot: open the
editor → **Images & video** → find the model or the banner → **Upload new
image**, and yours replaces it everywhere it appears.

If you add an eighteenth model later and have no photograph for it yet, the site
falls back to the drawn silhouette rather than showing a gap. The drawings are
still in `tools/gen_cars.py` for exactly that reason.

---

## Contact forms

Every enquiry form on this site ends in the same place: **WhatsApp**.

There is no server behind a static website, so a form that promises to email you
would quietly fail. Instead the form gathers the details, assembles a tidy
message, and opens it in WhatsApp on the visitor's own phone or desktop. They
press send, and it arrives on the number in the **Business** sheet
(`whatsapp_number`).

The visitor sees the message before it is sent. Nothing is stored on the
website.

Forms on the site:

- General enquiry (home, contact, offers, why-us)
- Model enquiry (one on each of the 17 car pages, pre-filled with that model)
- Test drive booking
- Service booking, and one on each of the four workshop pages
- True Value valuation and sell-your-car
- Driving school enrolment
- Job application
- Review submission

To change the destination number, edit `whatsapp_number` in the Business sheet
(country code + number, digits only — `918939752872`).

---

## Colours

Two separate things, easy to confuse:

**Your palette** — set in the Colors sheet or the editor. This is the site's
real identity, and it is what everyone sees by default.

**The visitor's palette** — the paint button at the bottom right of every page
lets a visitor pick a different palette for themselves. It is remembered on
their device only, changes nothing for anyone else, and resets with one click.
The five choices come from the Themes sheet.

There is a third layer worth knowing about: each of the five business channels
has its own colour, and any section tagged with a channel picks it up
automatically — pills, rules, icons, buttons and all. That is why the workshop
pages read amber and the driving school reads green without anyone maintaining
five copies of the stylesheet.

Colours you pick are darkened automatically where they would carry white text,
so contrast keeps passing WCAG AA even if you choose something light. Every page
is audited against that — see below.

---

## What has been checked

Run against the finished site:

- **200 page/width combinations** (49 pages × 1440, 1024, 768 and 390 px) — no
  horizontal overflow, no broken images, no JavaScript errors, no failed
  requests
- **2,357 internal links** followed — every one resolves
- **51 pages** scanned with axe-core against WCAG 2.1 A and AA plus
  best-practice rules — **zero violations**, including the editor
- Every desktop dropdown hit-tested (not just checked for `visibility`, which
  lies when an ancestor is clipping)
- Every element checked against the container it sits in — `overflow-x: clip`
  keeps the page from scrolling sideways, but it also hides overflow from the
  usual `scrollWidth` test, so containment is measured directly
- The type scale confirmed to shrink at each breakpoint with JavaScript both on
  and off
- The three-level menu walked with the Tab key, top to bottom
- The mobile drawer opened, a submenu expanded, the close button hit-tested and
  the drawer closed — at 390 px
- Both forms paths: valid submission builds the right `wa.me` URL with every
  field; invalid submission is blocked with per-field messages
- The site read with JavaScript disabled — all content present, counters showing
  real figures, FAQ answers readable
- The editor driven end to end: edit → save → refresh → the change is on the
  public page; image upload → the photograph replaces the drawing; backup →
  reset → restore

`python3 tools/check_site.py` re-runs the static half of that (links, assets,
alt text, titles, descriptions, landmarks) any time you change something.

---

## The legal pages

`privacy-policy.html` and `terms-conditions.html` are transcribed from the two
Word documents you supplied. The text lives in `tools/gen_legal.py`, not in the
HTML — edit it there and re-run `python3 tools/generate_site.py`.

Three sets of corrections were made to the Privacy Policy, all agreed first:

- **"Toyota/Hero" → "Maruti Suzuki"**, six places. The document had been adapted
  from another dealer's template and those had been missed.
- **"Pillai & Sos" → "Pillai & Sons"**, two places.
- **`".ord"` → `".org"`** in the guidance on enthusiast domain names.

One formatting repair in the Terms: the definitions of *Website* and *You* had
run together into one paragraph in the source file, so they are separated here.

Nothing else was reworded, reordered or removed.

Two things in the supplied text describe practices this site does not currently
have — worth a look before launch, though neither is an error on our side:

- The Privacy Policy has sections on **cookies** and on sharing data with a
  **third-party advertising company**. As built, this site sets no cookies and
  loads no advertising or analytics scripts at all. The clauses are harmless if
  you intend to add those later; if you do not, they over-describe what happens.
- The Terms cap liability at **100 USD** and carry **EU** and **US** compliance
  sections. That is standard template wording; your lawyer may want it in rupees.

---

## Files

```
index.html                  Home
about.html  why-us.html  team.html  testimonials.html  careers.html
cars/index.html             All 17 models, filterable
cars/arena.html  cars/nexa.html
cars/<model>.html           17 model pages
true-value/                 Buy, sell, how we certify
service/                    Overview, booking, and 4 workshop services
driving-school.html
offers.html  finance.html  faqs.html
blog.html  blog/<post>.html
contact.html  test-drive.html  locations.html
privacy-policy.html  terms-conditions.html
404.html
sitemap.xml  robots.txt  .nojekyll

admin/                      The editor (index.html, admin.css, admin.js)
config/site-config.xlsx     The spreadsheet
assets/css/main.css         One stylesheet
assets/js/main.js           One script
assets/js/site-config.js    Generated from the spreadsheet
assets/js/content.js        Generated list of every editable field
assets/fonts/               Poppins and Montserrat, self-hosted
assets/images/              logo.png (as supplied), share card, car drawings
tools/                      The generators (see below)
```

### tools/

You do not need these to run or edit the site. They are here so the site can be
rebuilt from source rather than hand-patched.

| File | What it does |
|---|---|
| `generate_site.py` | Builds all 49 pages. **Run this after editing any tool.** |
| `gen_content.py` | Every word of copy: models, services, courses, FAQs, posts, jobs |
| `gen_nav.py` | The menu tree and the footer columns |
| `gen_parts.py` | Shared markup: head, header, banner, footer, cards |
| `gen_cars.py` | The car drawings |
| `gen_icons.py` | The inline icon set |
| `gen_legal.py` | The Privacy Policy and Terms text, transcribed from the client's Word documents |
| `gen_og_image.py` | Renders the WhatsApp/Facebook share card |
| `config_schema.py` | What lives in the spreadsheet |
| `make_config_xlsx.py` | Writes a fresh spreadsheet from that schema |
| `build_config.py` | Spreadsheet → `assets/js/site-config.js` |
| `apply_overrides.py` | Folds published editor changes back into the source |
| `check_site.py` | Pre-launch validation |
| `deploy.sh` | One-command publish to GitHub Pages |

Rebuild everything:

```bash
python3 tools/build_config.py     # spreadsheet -> site-config.js
python3 tools/generate_site.py    # -> all 49 pages
python3 tools/check_site.py       # verify
```

Only `build_config.py` and `make_config_xlsx.py` need anything installed
(`pip install openpyxl`). Everything else is the standard library.

---

## Browser support

Current Chrome, Edge, Firefox and Safari, on desktop, tablet and phone,
including every current iPhone size. The layout is tested at 1440, 1024, 768 and
390 px, and the menu becomes a drawer on anything narrow or touch-operated.

Two modern CSS features are used deliberately: `color-mix()` for the channel
tints and `overflow: clip` for the off-canvas drawer. Both have a fallback path,
and both are supported everywhere the site is tested.

---

## Going live

See **DEPLOY.md**. Short version: it is a folder of files, so any static host
works. GitHub Pages is free and there is a one-command script for it.
