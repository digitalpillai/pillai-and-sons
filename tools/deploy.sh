#!/usr/bin/env bash
#
# deploy.sh  —  V2
# Publishes this site to GitHub Pages in one command.
#
#   bash tools/deploy.sh <your-github-username> <repository-name>
#
# Example:
#   bash tools/deploy.sh yourusername pillai-and-sons
#
# It works out your live URL from those two values, writes it into the
# spreadsheet and regenerates the pages (so canonical tags, sitemap.xml and the
# 404 base path are all correct), then commits and pushes.
#
# Re-run it any time to publish later changes — it only creates the repository
# and the first commit once.

set -euo pipefail

# ---------------------------------------------------------------- arguments --
if [ $# -lt 2 ]; then
  cat <<'USAGE'
Usage:  bash tools/deploy.sh <github-username> <repository-name>

  <github-username>   your GitHub account name, exactly as it appears in
                      github.com/<username>
  <repository-name>   what you want the repository called. It becomes part of
                      the web address, so keep it lowercase with hyphens:
                      pillai-and-sons

Example:
  bash tools/deploy.sh yourusername pillai-and-sons
USAGE
  exit 1
fi

USER="$1"
REPO="$2"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

SITE_URL="https://${USER}.github.io/${REPO}"

echo
echo "================================================================"
echo "  Publishing to:  ${SITE_URL}/"
echo "================================================================"
echo

# ------------------------------------------------------------ sanity checks --
if ! command -v git >/dev/null 2>&1; then
  echo "git is not installed."
  echo "  macOS   : xcode-select --install"
  echo "  Windows : https://git-scm.com/download/win"
  echo "  Linux   : sudo apt install git"
  exit 1
fi

if [ ! -f index.html ]; then
  echo "index.html is not here. Run this from inside the website folder:"
  echo "   cd /path/to/pillai-and-sons && bash tools/deploy.sh $USER $REPO"
  exit 1
fi

if [ ! -f .nojekyll ]; then
  echo "  .nojekyll was missing — recreating it (GitHub Pages needs it)."
  touch .nojekyll
fi

# ------------------------------------------- point the site at its real URL --
if command -v python3 >/dev/null 2>&1 && python3 -c "import openpyxl" >/dev/null 2>&1; then
  echo "-> Setting site_url in the spreadsheet and rebuilding the pages"
  python3 - "$SITE_URL" <<'PY'
import sys
from openpyxl import load_workbook
url = sys.argv[1]
wb = load_workbook("config/site-config.xlsx")
ws = wb["Business"]
for row in ws.iter_rows(min_row=2):
    if row[0].value == "site_url":
        row[1].value = url
        break
wb.save("config/site-config.xlsx")
print("   spreadsheet updated ->", url)
PY
  python3 tools/build_config.py
  python3 tools/generate_site.py
  if [ -f tools/check_site.py ]; then
    python3 tools/check_site.py || echo "   (check_site reported issues — see above)"
  fi
else
  echo "!  Python or openpyxl not found, so the pages were not regenerated."
  echo "   The site will still work, but canonical tags, sitemap.xml and the"
  echo "   404 page will point at the old address. To fix later:"
  echo "     pip install openpyxl"
  echo "     python3 tools/build_config.py && python3 tools/generate_site.py"
fi
echo

# ------------------------------------------------------------------- commit --
if [ ! -d .git ]; then
  echo "-> Creating a git repository here"
  git init -q
  git branch -M main
fi

git add -A
if git diff --cached --quiet 2>/dev/null; then
  echo "-> Nothing has changed since the last publish"
else
  git -c user.name="${GIT_AUTHOR_NAME:-Site Owner}" \
      -c user.email="${GIT_AUTHOR_EMAIL:-site@example.com}" \
      commit -q -m "Publish website" || true
  echo "-> Changes committed"
fi

# ------------------------------------------------------------------- remote --
REMOTE="https://github.com/${USER}/${REPO}.git"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE"
else
  git remote add origin "$REMOTE"
fi
echo "-> Remote set to ${REMOTE}"

# Create the repository automatically if the GitHub CLI is available
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  if ! gh repo view "${USER}/${REPO}" >/dev/null 2>&1; then
    echo "-> Creating the repository on GitHub (public — required for free Pages)"
    gh repo create "${USER}/${REPO}" --public --source=. --remote=origin >/dev/null
  fi
fi

echo "-> Pushing"
echo
git push -u origin main

# -------------------------------------------------------------- turn on Pages --
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  echo
  echo "-> Turning on GitHub Pages"
  gh api -X POST "repos/${USER}/${REPO}/pages" \
     -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
   || gh api -X PUT "repos/${USER}/${REPO}/pages" \
        -f "source[branch]=main" -f "source[path]=/" >/dev/null 2>&1 \
   || echo "   Could not set it automatically — switch it on in Settings > Pages."
fi

cat <<EOF

================================================================
  Done.

  If Pages is not on yet:
    github.com/${USER}/${REPO}  ->  Settings  ->  Pages
    Source: "Deploy from a branch",  Branch: main,  Folder: / (root)
    Save.

  Your site (allow a minute for the first build):
    ${SITE_URL}/

  The editor:
    ${SITE_URL}/admin/index.html

  To publish future changes, run this same command again.
================================================================
EOF
