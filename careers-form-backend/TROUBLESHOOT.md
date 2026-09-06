# "Sorry, something went wrong" — how to find the cause

That message means the browser reached Google but the request failed.
Work through these in order; the first two cause most cases.

## 1. Is the deployment open to "Anyone"?

Apps Script editor → **Deploy → Manage deployments** → pencil icon.
"Who has access" must read **Anyone** — not "Anyone with Google account",
not "Only myself". Change it, set **Version: New version**, then **Deploy**.

Quick test: open your `/exec` URL in a **private/incognito window**. If you see
a Google sign-in page instead of `{"result":"ok"...}`, this is your problem.

## 2. Did you redeploy after pasting the code?

Saving the script is not enough. Every code change needs
**Deploy → Manage deployments → pencil → Version: New version → Deploy**.
Without this, the live endpoint still runs the old (or empty) code.

## 3. Turn on the real error message

In `careers.html`, find:

```js
var DEBUG           = false;
```

Change it to `true`, reload, and submit again. The page will now show the
technical reason in brackets. Common ones:

| Shown | Meaning |
|---|---|
| `HTTP 401` / `HTTP 403` | Deployment is not set to "Anyone" (see step 1) |
| `Endpoint did not return JSON` | Same as above — Google served a login page |
| `HTTP 404` | The `/exec` URL is wrong or the deployment was deleted |
| `Cannot read ... getRange` | `setupSheet` was never run |
| `Bad row reference` | Sheet has no header row — run `setupSheet` |

Set `DEBUG` back to `false` before you publish.

## 4. Check the script's own log

Apps Script editor → **Executions** (left sidebar). Each attempt appears there
with its error. This shows what actually failed inside Google.

## 5. Check the URL itself

It must end in `/exec`, not `/dev`. A `/dev` URL only works while you are
signed in, which is why it fails for real visitors.

---

# What changed in V3 / V2

The attachment no longer travels with the application. The form now:

1. Saves the application row first, then
2. Uploads each file in its own request.

So a file problem can no longer lose someone's application — the row is
already saved, and the page says which attachment failed.

## Attachment limits

- Up to **10 files** per application
- **25 MB** per file
- **100 MB** total

These are set at the top of the script block in `careers.html`:

```js
var MAX_FILES       = 10;
var MAX_PER_FILE_MB = 25;
var MAX_TOTAL_MB    = 100;
```

**A caution about large files.** Apps Script is not built as a file-transfer
service. Uploads in the low megabytes are reliable; as files approach 25 MB
they get slow and may time out, and the script has a hard 6-minute execution
limit. The limits above are permitted, not guaranteed. Since real resumes are
almost always under 5 MB, this matters only if applicants attach photos or
scans. If you genuinely need reliable 100 MB uploads, Apps Script is the wrong
backend and you would want a dedicated file service instead — worth telling me
if that is the actual requirement.
