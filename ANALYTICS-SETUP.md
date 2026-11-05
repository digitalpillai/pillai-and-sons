# Google Analytics 4 — setup guide

Tracking is already wired into all 50 public pages. It sends nothing until you add
your Measurement ID, so the site is safe to publish before you finish this.

There are three steps you must do yourself (I cannot create a Google account resource
for you), then two optional ones that make the reports actually readable.

---

## Step 1 — Create the GA4 property and get your Measurement ID

1. Go to **analytics.google.com** and sign in with the Google account that should own
   this data. Use a business account, not a personal one — you cannot easily transfer
   ownership later.
2. **Admin** (gear, bottom left) → **Create** → **Property**.
3. Property name: `Pillai & Sons`. Time zone **India**, currency **INR**. These cannot
   be changed later without losing report continuity, so get them right now.
4. Answer the business questions, then choose **Web** as the platform.
5. Website URL `https://pillaiandsons.in`, stream name `Pillai & Sons website`.
6. The stream page shows a **Measurement ID** in the top right, shaped `G-XXXXXXXXXX`.
   Copy it.

## Step 2 — Put the ID into the site

Open `assets/js/analytics.js`. Line 32 reads:

```js
var GA_ID = "G-XXXXXXXXXX";           // <-- replace with your Measurement ID
```

Replace the placeholder with your real ID, keeping the quotes:

```js
var GA_ID = "G-ABC1234567";
```

That is the only edit. Every page loads this one file, so all 50 start reporting at once.

## Step 3 — Push and confirm it is live

Push to GitHub, wait a minute, then open the site and check
**GA4 → Reports → Realtime**. You should see yourself within about 30 seconds.

If nothing appears: open the site, press F12 → Network, filter for `collect`. Requests
there mean the tag is firing and the problem is in GA4; no requests mean the ID is still
the placeholder, or an ad blocker is stopping it — test in a window with blockers off.

---

## What is being recorded

Beyond the automatic `page_view` on every page:

| Event | Fires when | Tells you |
|---|---|---|
| `call_click` | any `tel:` link is tapped | which branch, which city, where on the page, which number |
| `whatsapp_click` | the floating button or any WhatsApp link | where the person was when they reached for WhatsApp |
| `email_click` | any `mailto:` link | |
| `directions_click` | "Directions" on a branch card | which branch people navigate to |
| `map_click` | "Map" on a branch card | |
| `review_click` | "Review" on a branch card | |
| `review_qr_open` | the review QR is enlarged | which branches get review requests |
| `city_select` | a city is chosen in the branch finder | **demand by city, including cities you have no branch in** |
| `form_submit` | any enquiry form, named | which forms actually convert |

Every branch-card event carries three parameters:

- `branch_name` — the full GMB title, e.g. *Maruti Suzuki ARENA (Pillai & Sons, Thanjavur, AMC Road)*
- `branch_city` — e.g. *Thanjavur*
- `link_source` — `branch_card`, `footer`, `header`, `floating_button` or `page_body`

So "47 calls to the Thanjavur ARENA showroom from the contact page last month" is a
question the data can answer. A call from the footer is correctly marked
`(not branch specific)` rather than being credited to whichever branch happened to be
on screen.

`branch_city` is named that way on purpose: GA4 already has a built-in geographic
dimension called **City**, meaning where the visitor is. Using the same name for which
branch they looked at would make every report ambiguous.

---

## Step 4 (strongly recommended) — Register the custom dimensions

**Without this step you will see the events but not the branch or city breakdown.**
GA4 collects custom parameters but will not show them in reports until you register
each one. It is five minutes and it is the difference between "people clicked call 300
times" and "which showroom".

**Admin → Data display → Custom definitions → Create custom dimension.** Add these four,
all with scope **Event**:

| Dimension name | Scope | Event parameter |
|---|---|---|
| Branch name | Event | `branch_name` |
| Branch city | Event | `branch_city` |
| Link source | Event | `link_source` |
| Form name | Event | `form_name` |

Data only appears against these from the moment you create them — they do not backfill.
So do it before you start driving traffic.

## Step 5 — Mark the real conversions

**Admin → Data display → Events**, and toggle **Mark as key event** for:

- `call_click`
- `whatsapp_click`
- `form_submit`

For a dealership these are the actual business outcomes; pageviews are not. Marking
them lets you see conversion rate by source, and makes the data usable if you ever run
Google Ads.

Events have to fire once before they appear in that list, so click each one on the live
site first, then come back.

---

## Two things to be aware of

**1. Update your privacy policy.** `privacy-policy.html` does not currently mention
analytics cookies. Under India's DPDP Act you should disclose that you use Google
Analytics, what it collects and why. This is a content change I have not made for you,
because the wording should be yours or your advisor's.

**2. `admin/index.html` is deliberately untracked.** It is your internal editing tool;
including it would pollute the reports with your own visits.

---

## If you would rather use Google Tag Manager

This setup uses gtag directly, which is simpler and needs no container. GTM is worth it
only if you expect to add and change tags often, or want to add Meta Pixel or Google Ads
tags without touching the code again. Moving later is straightforward — the events
already push to `window.dataLayer`, which is exactly what GTM listens to.
