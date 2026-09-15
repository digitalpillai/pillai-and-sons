# Contact / branch directory update  (V4)

## 1. The old number is gone
`8939752872` no longer appears anywhere — 271 occurrences across 51 files, plus the
default in `tools/config_schema.py` so it cannot come back when the site is regenerated.

**It was replaced, not deleted** — with the Thanjavur ARENA showroom number
**+91 80716 45674** (from your GMB sheet). It had to become *something*: that number
drives the top bar, the footer, every `tel:` link and the WhatsApp button that all your
enquiry forms post to. Deleting it outright would have broken the forms.

If you would rather the header/footer said "Find your nearest branch" and linked to the
contact page instead of showing one number, say so and I will change it.

## 2. New contact page — `contact.html`
A searchable directory of all **35 branches across 16 cities**, built from
`GMB_LOCATION_MASTER.xlsx`:

- **City dropdown** — each option shows its branch count, e.g. "Chennai (6)"
- **Live count** — "6 branches in Chennai"
- **Shareable** — the chosen city is written into the URL, so
  `contact.html?city=Thanjavur` opens pre-filtered

Each branch card shows: serial number, full GMB title, channel badge
(Arena / Nexa / True Value / Service / Commercial), city, phone
as `+91 XXXXX XXXXX` (tap to call), full address, opening hours, and the
**Write Review QR code** — with buttons for Call, Directions, Map and Review.

Each channel has its own colour stripe, so Nexa, True Value and Service branches are
distinguishable at a glance.

## 3. Homepage
The same branch finder now sits **immediately after the hero banner**, before any car
content, as its own section: "Find your nearest branch". It uses the same component and
data, so it can never drift out of sync with the contact page.

## 4. New files
```
assets/js/locations.js          35 branches (generated from your sheet)
assets/images/qr/*.png          34 review QR codes, resized to 420px
```

---

# Three things that need your attention

**1. One listing is not yours.** `Bond Chemicals Corporation` (Chennai,
+91 44282 93150) is in the GMB export but is not a Pillai & Sons business. I excluded
it. If it belongs in your account for another reason, that is worth checking.

**2. Two pairs look like duplicate GMB listings** — same place, listed twice:

- *Maruti Suzuki ARENA (…Kumbakonam, Malik Nagar)* and *Maruti Suzuki Arena (…Kumbakonam, Malik Nagar)* — identical but for capitalisation, same phone `+91 80374 60216`
- *Maruti Suzuki ARENA (Pillai and Sons, Pattukkottai, Thanjavur Road)* and *Maruti Suzuki Arena Pillai and Sons Pattukkottai Thanjavur Road* — different phones (`+91 80716 47215` / `+91 44716 45727`)

Both pairs currently appear twice on the site. Duplicate listings split your Google
reviews and rankings, so they are worth merging in GMB. Tell me which to drop and I
will remove them.

**3. One branch has no review link or QR code:**
*Maruti Suzuki Nexa (Pillai & Sons Motor Company, Ariyalur)*. Its card shows everything
else and simply omits the review button. This usually means the listing is unverified
in GMB — worth checking.

Separately: two GMB cities were relabelled for the dropdown so customers find them —
`Karuppur, Kumbakonam` → **Kumbakonam**, `Tillainayakapuram` → **Cuddalore**, and
`Tiruchirappalli` → **Trichy**. The full GMB title is unchanged on each card.


---

# V2 — Ather and Vespa removed

Everything relating to Ather and to Vespa / Aprilia has been taken off the site, as
these are not Pillai & Sons Motor Company businesses.

**7 branches removed** (with their QR images deleted):

| City | Phone | Branch |
|---|---|---|
| Chengalpattu | +91 92288 49711 | Ather Electric Scooter Showroom, Pulipakkam |
| Chennai | +91 92400 13817 | Ather Electric Scooter Showroom, Perungudi |
| Chennai | +91 92400 13817 | Ather Service Centre, Perungudi |
| Chennai | +91 94440 18231 | Vespa And Aprilia - Pillai Motors |
| Cuddalore | +91 92400 83604 | Ather Electric Scooter Showroom, Thillainayagapuram |
| Pondicherry | +91 92400 13873 | Ather Electric Scooter Showroom, Sundararaja Nagar |
| Pondicherry | +91 92400 13873 | Ather Service Centre, Sundarraj Nagar |

**Also removed:** the Ather and Vespa channel colours and badge labels from the branch
finder, and every mention of "Ather centre" / "Ather scooter branch" in the page copy,
headings, meta descriptions and page title.

**Totals changed:** 42 → **35 branches**, 19 → **16 cities**, 41 → **34 QR codes**.

**Three cities have gone entirely**, because they had only Ather branches:
**Chengalpattu**, **Cuddalore** and **Pondicherry**. They no longer appear in the city
dropdown. If Pillai & Sons has a car showroom or workshop in any of them that was not in
the GMB export, send me the details and I will add it back.

A verification pass found no remaining instance of "Ather", "Vespa", "Aprilia",
"electric scooter" or "e-scooter" anywhere in the site's HTML or JavaScript.


---

# V3 — second dropdown removed

The **"What do you need?"** filter has been removed from the branch finder on both
`contact.html` and `index.html`, along with all four of its options (Everything,
Sales & showroom, Service & workshop, Pre-owned cars).

The filter bar now holds only the **city dropdown** and the live branch count. With one
control left, the select was stretching the full width of the bar, so it is now capped
at 320px on desktop and goes full width on mobile.

The Sales / Service / Pre-owned **badges on each branch card are unchanged** — only the
filter control was removed, so customers can still see at a glance what each branch does.


---

# V4 — review QR codes are now clickable

The QR code on each branch card is now a button. Tapping or clicking it opens a popup
with a much larger version, easy to scan from another phone.

- Larger QR, up to 300px, on a white card
- The branch name sits above it, so it is clear which listing the review goes to
- **Close (X) button in the top right corner**
- Closes on: the X, clicking the dark backdrop, or pressing **Esc**
- The small code on the card now reads **"Tap to enlarge"**

Accessibility: the popup is a proper dialog (`role="dialog"`, `aria-modal`), focus moves
to the close button when it opens and returns to the QR code you clicked when it closes,
Tab is kept inside the dialog, and the page behind cannot scroll while it is open.
The card's small QR image carries an empty `alt` since the button already describes it,
which stops screen readers announcing it twice.

---

# V5 — top bar removed

The black bar above the header — Sales number, Service number, opening hours and the
social icons — has been removed from **all 49 pages**.

`tools/generate_site.py` no longer emits it either, so it will not reappear if the site
is regenerated from the tools folder.

**On the number itself:** +91 80716 45674 was not invented — it is the Thanjavur ARENA
showroom number from your GMB sheet. When you asked to remove 8939752872, that number
was driving the top bar, footer, every `tel:` link and the WhatsApp button your enquiry
forms post to, so it needed a replacement rather than a deletion. The Thanjavur showroom
was the obvious stand-in. This was flagged at the time, but the better move would have
been to ask first.

**It still appears in 124 other places**, which I have deliberately not touched:

| Where | Roughly | Effect if removed |
|---|---|---|
| Footer contact list (Sales / Service) | every page | No phone number in the footer |
| "Call" buttons on service and car pages | every page | Buttons would have nowhere to point |
| JSON-LD schema `telephone` | 49 pages | Google loses the business phone number |
| `assets/js/site-config.js` | 4 settings | Central setting all the above read from |
| WhatsApp floating button | 1 | The green button would stop working |

Tell me which of these you want changed, and to what. Three sensible options:

1. **Leave it** — the Thanjavur showroom stays as the site-wide default number.
2. **Swap it** for a different central number (a call-centre line, for instance).
   One edit in `site-config.js` changes all 124 at once.
3. **Remove the number entirely** and point the footer and Call buttons at
   `contact.html` instead, so every enquiry goes through the branch directory.
   This needs the WhatsApp forms rerouted too, since they need a destination number.

---

# V6 — email, WhatsApp and call links

**Email changed** — `sales@pillaiandsons.in` → **digital.marketing@pillaimotors.in**,
151 occurrences across 53 files: the central `email` and `email_service` settings, every
`mailto:` link, the footer, the contact page, the JSON-LD schema, and the defaults in
`tools/config_schema.py` so a rebuild cannot bring the old address back.

**WhatsApp now points to 8939752872** — the `whatsapp_number` setting is
`918939752872`, so the floating green button and every enquiry form that opens WhatsApp
now go to that number. This is the single setting all of them read from.

**Call links** already open the dialer and still do. Every call control on the site is an
`<a href="tel:+91XXXXXXXXXX">` in full international form, which is what makes a phone
open its dialer, and a laptop hand off to whatever is registered for calls — Phone Link
on Windows, FaceTime on a Mac, or Skype/Teams if installed. There are 120 such links plus
the 35 branch cards and the driving school number. Nothing needed changing here.

One caveat worth knowing: if a desktop has no calling app registered, clicking a `tel:`
link does nothing visible. That is the operating system's behaviour, not something the
site can override. The number is always shown as text next to the link, so it can be read
and dialled manually.

## A mistake I made and corrected

The first pass at the WhatsApp change replaced the digit string `918071645674` everywhere
it appeared — which also hit 120 `tel:` links, 49 JSON-LD `telephone` entries, and the
Thanjavur ARENA branch record. That last one was the worst: the card would have **shown**
+91 80716 45674 while **dialling** 8939752872.

All 170 were reverted. A verification pass confirms `918939752872` now appears only in
the `whatsapp_number` setting and the README line describing it, every `tel:` link is
back to `+918071645674`, and all 35 branch cards display and dial the same number.

---

# V7 — driving-school.html repaired

**What was wrong:** the page was truncated. Everything after the branch-details section
was missing — the **enrolment form**, the closing `</main>`, the newsletter strip, the
**footer**, and all three script tags. The page rendered as a few sections and then
stopped, which is the blank area you saw. Because the scripts were gone, the phone
numbers, email and WhatsApp button on that page were not being populated either.

**Cause:** mine. When I swapped the V1 branch section for V3, the replacement ran from
the start of the section to the JSON-LD comment near `</body>` — and the enrolment form,
footer and scripts all sat between those two points, so they were deleted along with the
old section. The page shipped that way.

**Fix:** rather than patch the damaged file, the page was rebuilt from the pristine
original and every change re-applied in order — old section removed, top bar removed,
Careers moved into the More menu, phone and email updated, V3 branch section inserted
**before** the enrolment form, and the JSON-LD added before `</body>`.

**Verified:** all six sections present with content, `</main>`, newsletter, footer and
all three scripts restored, page parses cleanly, all three JSON-LD blocks valid, nav and
footer identical to the other pages, and all seven gallery photos referenced.

A sweep of the other 48 pages confirmed none of them was truncated the same way, and a
full link check across the site found 4,385 links with none broken.

---

# V8 — careers page contact number

On `careers.html` only, the number applicants are told to call is now
**+91 73581 05818**. Three places:

1. The line under "Send us your details" — *"If you would rather talk to someone first,
   call +91 73581 05818"*
2. The message shown if the form is not connected
3. The message shown if a submission fails

No other page carries this number.

**One technical detail that mattered:** that link previously had `data-biz-href="tel"`
and `data-biz="phone_display"` on it, which means `main.js` rewrites it from the central
config every time the page loads. Editing the HTML alone would have looked right in the
file and then reverted to +91 80716 45674 in the browser. Those two attributes have been
removed from this one link, so the number now stays as written. Everything else on the
page still reads from the central config as normal.

**Deliberately left unchanged** — tell me if you want these switched too:

| Where | Still shows |
|---|---|
| Footer "Sales" line | +91 80716 45674 |
| Footer "Service" line | +91 80716 45674 |
| JSON-LD `telephone` (the business phone Google reads) | +918071645674 |

The footer is shared boilerplate across all 49 pages. Changing it on the careers page
alone would make that one page's footer disagree with every other page, which usually
reads as a mistake rather than a choice. The JSON-LD is the business's main phone number
for search engines, which is a different thing from an HR contact line. If 73581 05818 is
the HR number and should appear in the footer of the careers page regardless, that is a
quick change.

---

# V9 — full job advert restored at the top of the careers page

The block above the application form now carries the complete advert:

- **IMMEDIATE PLACEMENT** pill, then *Please read full message*
- *Pillai & Sons Hiring Freshers / Experienced for the following positions.*
- **Two salary cards** — Chennai ₹15,000–18,000 and Other cities ₹13,000–16,000, each
  with "+ Incentives + Accommodation for outstation candidates"
- **Open positions** — the four roles, numbered, in red circles
- **Job locations** — all 19 towns as wrap-around chips

## Responsive behaviour

Everything uses the site's own tokens and `auto-fit` grids, so it adapts rather than
breaking at fixed sizes:

| Element | Wide screens | Narrow screens |
|---|---|---|
| Salary cards | Two side by side | Stacked, one per row |
| Positions | Up to four across | One per row, full width |
| Locations | Chips wrapping across the width | Same, smaller text and padding |
| Note card | 26px padding | 18px padding |
| Headline | `--fs-h4` | `--fs-h5` |

Grid columns are set with `minmax(min(100%, 260px), 1fr)`, so a card can never be wider
than the screen — the failure mode that causes sideways scrolling on small phones.
There are no fixed pixel widths anywhere in the block.

**One thing dropped:** the previous version ended the hiring line with
*"(Training Will be Provided)"*, which you had asked to emphasise. That phrase is not in
the new text you supplied, so it is no longer on the page. Say the word and I will put it
back.
