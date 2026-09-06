# What changed in this update

## 1. Careers page — rebuilt as the job application page
`careers.html`

- Heading: **Job Application — Car Sales / Service / Accounts / Backoffice / Telecallers**, with a **50+ openings** eyebrow.
- Highlight box (built from the site's own `note-card` component): an
  **Immediate placement** pill, then, set large, **Hiring Freshers / Experienced
  (Training Will be Provided)**.
- Application form with the **14 fields from your Google Form**, in the same
  order, nothing added:

  | # | Question | Control |
  |---|---|---|
  | 1 | For Which Position you want to apply for Job? | Dropdown (4 options) |
  | 2 | Name | Text |
  | 3 | Mobile Number | Tel, 10 digits |
  | 4 | Age | Number |
  | 5 | Education Qualification? | Text |
  | 6 | Do you have Car Driving License? | Yes / No |
  | 7 | Are you Fresher or Experienced | Fresher / Experienced |
  | 8 | Do you have experience in Car/Bike Sales or Service? | Yes / No |
  | 9 | In which City you want Job? | Dropdown (19 cities) |
  | 10 | Your Current living city/Town? | Text |
  | 11 | Present Company Name | Text |
  | 12 | Current Monthly Takehome Salary? | Text |
  | 13 | Expected Monthly Takehome Salary? | Text |
  | 14 | Attach your Resume (Optional) | File upload |

- The form uses your existing `form-card` / `form-grid` / `form-field` markup, so
  it inherits your styling and is already responsive. Page-specific CSS is a
  dozen lines in the page head, using your `--c-*` tokens.
- **The previous careers content was replaced** — the six Thanjavur job cards
  ("Work somewhere people stay", "How we hire") are gone. The original is
  recoverable from git history if you want any of it back.

## 2. Driving school section — upgraded
`driving-school.html`

- The block inserted earlier was **V1**; it is now **V3**.
- Two real responsive bugs fixed: media queries were in the wrong order
  (640px before 900px), and the photo grid could overflow on narrow phones.
- Type sizes raised — contact details and buttons are now 16px.
- The scoped CSS is now bound to **your** design tokens rather than my
  fallbacks — it picks up `--c-ch-school` (the green school channel colour),
  `--c-heading`, `--c-text`, `--c-border` and `--r-card`.

## 3. Navigation — Careers moved to "More"
All 49 pages that carry the nav.

- Careers was under **About**; it is now under **More**, between
  "News and Advice" and "Privacy Policy", as you asked.
- The breadcrumb and its JSON-LD on `careers.html` were updated to match
  (Home → Careers, no longer Home → About → Careers).

---

# Before you publish — one required step

The careers form is **not connected yet**. It will load and validate, but every
submission will fail until you do this:

1. Open your sheet:
   `https://docs.google.com/spreadsheets/d/1X7oDATxdpm1nnzK_jc7Su0k718QEk2wfKMnn7s0cWEU/edit`
2. **Extensions → Apps Script**, delete what is there, paste in `Code.gs`
   (in the `careers-form-backend/` folder), **Save**.
3. Function dropdown → **setupSheet** → **Run**. Authorise when asked
   (your account → Advanced → Go to project → Allow). It needs Drive access
   because resumes are saved there.
4. **Deploy → New deployment → Web app**
   - Execute as: **Me**
   - Who has access: **Anyone**  ← must be "Anyone", or the site cannot post
   - Deploy, then copy the URL ending in `/exec`.
5. In `careers.html`, find:

   ```js
   var CAREERS_ENDPOINT = "PASTE_YOUR_APPS_SCRIPT_URL_HERE";
   ```

   and paste your `/exec` URL in place of the placeholder.

Then test locally before pushing:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000/careers.html`, submit one test application with a
small PDF, confirm the row lands in the sheet and the file in the Drive folder
"Pillai & Sons — Resumes", then delete the test row and file.

---

# Two things worth your judgement

1. **Your Google Form's two city lists disagree.** The form description lists
   Kuthalam, Thiruvaiyaru, Needamangalam, Udayarpalayam and Lalgudi, but the
   dropdown offers Peravurani, Velankanni, Pondicherry, Chengalpet and
   Chidambaram instead. The page uses the **dropdown** list, since that is what
   applicants actually select. Worth reconciling on the form itself.

2. **"Present Company Name" and "Current Monthly Takehome Salary" are required**,
   yet the ad invites freshers, who have neither. Freshers will have to type
   "NA". Tell me and I will make those two optional in one line.

Separately, and not something I changed: your site's form inputs are set to 15px
in `assets/css/main.css`. Anything under 16px makes iOS Safari zoom in when a
field is tapped. It affects every form on the site, not just this one. A
one-line change fixes it, but it is your stylesheet, so I left it alone.
