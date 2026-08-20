# Putting this site on GitHub

Two routes. Pick one.

**Before either one, choose the repository name.** It becomes part of your web
address — `https://<username>.github.io/<repository-name>/` — so keep it
lowercase with hyphens. `pillai-and-sons` is a good choice.

> **Free GitHub accounts must make the repository public** for Pages to work.
> Private repositories need a paid plan. Nothing in this folder is secret — the
> whole site is public once it's live anyway — so public is fine.

---

## Route A — one command (recommended)

Unzip the folder, open a terminal inside it, and run:

```bash
bash tools/deploy.sh <your-github-username> pillai-and-sons
```

For example:

```bash
bash tools/deploy.sh yourusername pillai-and-sons
```

That script does all of this for you:

1. Works out your live URL from the username and repository name.
2. Writes it into `site_url` on the Business sheet of the spreadsheet.
3. Rebuilds all 49 pages so the canonical tags, `sitemap.xml`, `robots.txt` and
   the 404 page all point at the right address. **This is the step people forget,
   and it's the one that quietly breaks SEO and the 404 page.**
4. Runs the pre-launch check.
5. Creates the git repository, commits everything, and pushes.
6. Switches on GitHub Pages, if you have the GitHub CLI installed.

Run the same command again any time you want to publish later changes.

### What you need first

- **git** — `git --version` to check.
  macOS: `xcode-select --install` · Windows: <https://git-scm.com/download/win>
  · Linux: `sudo apt install git`
- **Python with openpyxl**, for step 2–4: `pip install openpyxl`.
  Without it the site still publishes, it just skips the URL rewrite.
- Optional but nice: the **GitHub CLI** (<https://cli.github.com>), then run
  `gh auth login` once. With it, the script creates the repository and turns on
  Pages by itself. Without it, do those two things by hand — see below.

### If you don't have the GitHub CLI

Create the repository first at <https://github.com/new> — name it exactly what
you passed to the script, set it to **Public**, and do **not** tick "Add a README".
Then run the script.

Afterwards, turn Pages on:

**Settings → Pages → Source: "Deploy from a branch" → Branch: `main`, Folder:
`/ (root)` → Save.**

---

## Route B — the GitHub website, no software at all

Workable, but there are two traps.

1. Go to <https://github.com/new>. Name it `pillai-and-sons`, set **Public**,
   click **Create repository**.
2. Click **uploading an existing file**.
3. Unzip the delivered file, open the `pillai-and-sons` folder, and drag its
   **contents** — not the folder itself — into the browser.

   > **Trap 1: GitHub only accepts 100 files per upload, and this site has
   > more than that.** Drag the loose files plus the `assets` folder first,
   > commit, then click **Add file → Upload files** again and drag `cars`,
   > `service`, `true-value`, `blog`, `admin`, `config` and `tools`.

4. Commit each batch.
5. **Trap 2: `.nojekyll` starts with a dot, so your file manager probably hides
   it and it won't get uploaded.** Without it GitHub may not serve the site
   correctly. Create it by hand: **Add file → Create new file**, type
   `.nojekyll` as the name, leave the body empty, commit.
6. **Settings → Pages → Source: "Deploy from a branch" → Branch: `main`,
   Folder: `/ (root)` → Save.**
7. Finally, fix the URLs. Open `config/site-config.xlsx`, put your live address
   in the **site_url** row, and either run
   `python3 tools/build_config.py && python3 tools/generate_site.py`, or open
   `admin/index.html`, drop the spreadsheet on the **Excel config** tab, and
   upload the downloaded `site-config.js` back into `assets/js/`.

---

## After it's live

Give it about a minute for the first build, then:

| | Address |
|---|---|
| Website | `https://<username>.github.io/pillai-and-sons/` |
| Editor | `https://<username>.github.io/pillai-and-sons/admin/index.html` |

A few things worth knowing:

- **The editor is reachable by anyone who guesses the URL.** It cannot change
  your live site on its own — edits live in that person's browser until someone
  with repository access commits the exported files — but if you would rather it
  weren't public, delete the `admin` folder from the repository and keep it on
  your own computer. It works perfectly well opened from disk.
- `robots.txt` already tells search engines to skip `/admin/`.
- To publish later edits, run `bash tools/deploy.sh <username> pillai-and-sons`
  again, or commit through the GitHub website.

## Using your own domain instead

1. In your domain registrar, point a `CNAME` record for `www` at
   `<username>.github.io`.
2. **Settings → Pages → Custom domain**, enter `www.yourdomain.com`, Save, then
   tick **Enforce HTTPS** once the certificate is issued.
3. Set `site_url` in the spreadsheet to `https://www.yourdomain.com` and
   regenerate — on a custom domain the site sits at the root rather than in a
   `/repository-name/` subfolder, and the 404 page needs to know that.

---

## If something goes wrong

| Symptom | Cause |
|---|---|
| Page loads but has no styling | `.nojekyll` missing, or Pages is pointing at the wrong folder |
| 404 on every page | Pages source is set to `/docs` instead of `/ (root)`, or the first build hasn't finished |
| Site works, but a wrong-URL page is unstyled | `site_url` doesn't match reality — set it and regenerate |
| `git push` asks for a password | GitHub stopped accepting passwords; use `gh auth login`, or create a personal access token and use that as the password |
| Pages tab says it needs a paid plan | The repository is private on a free account — make it public |
