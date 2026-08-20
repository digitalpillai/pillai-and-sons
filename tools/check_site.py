#!/usr/bin/env python3
"""
check_site.py  —  V1
Pre-launch checks. Run from the project root:

    python3 tools/check_site.py

Verifies:
  * every internal href resolves to a file that exists
  * every img/iframe/script/link asset exists
  * every <img> carries alt, width and height
  * every page has a unique <title> and meta description of a sane length
  * no page is missing the skip link, nav or footer
  * ids referenced by aria-controls exist
"""
import os
import re
import sys
from collections import defaultdict
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_PREFIX = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:", "#")

problems = []
warnings = []


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.assets, self.imgs = [], [], []
        self.ids, self.aria_controls = set(), []
        self.title, self.desc = "", ""
        self._in_title = False
        self.has_skip = self.has_nav = self.has_footer = self.has_main = False
        self.h1 = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if a.get("aria-controls"):
            self.aria_controls.append(a["aria-controls"])
        if tag == "a":
            if a.get("href"):
                self.links.append(a["href"])
            if "skip-link" in (a.get("class") or ""):
                self.has_skip = True
        elif tag == "img":
            self.imgs.append(a)
            if a.get("src"):
                self.assets.append(a["src"])
        elif tag in ("script", "iframe") and a.get("src"):
            self.assets.append(a["src"])
        elif tag == "link" and a.get("href") and a.get("rel") in ("stylesheet", "icon", "apple-touch-icon", "preload"):
            self.assets.append(a["href"])
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name") == "description":
            self.desc = a.get("content", "")
        elif tag == "nav":
            self.has_nav = True
        elif tag == "footer":
            self.has_footer = True
        elif tag == "main":
            self.has_main = True
        elif tag == "h1":
            self.h1 += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def all_pages():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # admin/ is the owner's editor, not a public page — it has its own rules
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "tools", "config", "admin", "__pycache__")]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(os.path.relpath(os.path.join(dirpath, fn), ROOT))
    return sorted(out)


def main():
    pages = all_pages()
    titles, descs = defaultdict(list), defaultdict(list)

    for rel_page in pages:
        full = os.path.join(ROOT, rel_page)
        with open(full, "r", encoding="utf-8") as fh:
            src = fh.read()
        p = Page()
        p.feed(src)
        base = os.path.dirname(full)
        tag = rel_page

        titles[p.title.strip()].append(rel_page)
        if p.desc:
            descs[p.desc.strip()].append(rel_page)
        else:
            problems.append("%s: no meta description" % tag)

        if not (110 <= len(p.desc) <= 175):
            warnings.append("%s: meta description is %d chars (aim 120-160)" % (tag, len(p.desc)))
        if p.h1 != 1:
            problems.append("%s: found %d <h1> (expected exactly 1)" % (tag, p.h1))
        for flag, label in ((p.has_skip, "skip link"), (p.has_nav, "<nav>"),
                            (p.has_footer, "<footer>"), (p.has_main, "<main>")):
            if not flag:
                problems.append("%s: missing %s" % (tag, label))

        for href in p.links:
            if href.startswith(SKIP_PREFIX):
                continue
            target = href.split("#")[0].split("?")[0]
            if not target:
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, target))):
                problems.append("%s: broken link -> %s" % (tag, href))

        for src_url in p.assets:
            if src_url.startswith(SKIP_PREFIX):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(base, src_url.split("?")[0]))):
                problems.append("%s: missing asset -> %s" % (tag, src_url))

        for img in p.imgs:
            if img.get("alt") is None:
                problems.append("%s: <img> without alt (%s)" % (tag, img.get("src")))
            if not img.get("width") or not img.get("height"):
                warnings.append("%s: <img> without width/height (%s)" % (tag, img.get("src")))

        for cid in p.aria_controls:
            if cid not in p.ids:
                problems.append("%s: aria-controls=\"%s\" has no matching id" % (tag, cid))

    for t, where in titles.items():
        if len(where) > 1:
            problems.append("duplicate <title> %r on: %s" % (t, ", ".join(where)))
    for d, where in descs.items():
        if len(where) > 1:
            problems.append("duplicate meta description on: %s" % ", ".join(where))

    for required in (".nojekyll", "robots.txt", "sitemap.xml", "README.md",
                     "assets/css/main.css", "assets/js/main.js",
                     "assets/js/site-config.js", "assets/js/content.js",
                     "config/site-config.xlsx", "admin/index.html"):
        if not os.path.exists(os.path.join(ROOT, required)):
            problems.append("missing required file: %s" % required)

    print("checked %d pages" % len(pages))
    if warnings:
        print("\n%d warning(s):" % len(warnings))
        for w in warnings[:40]:
            print("  ~ %s" % w)
        if len(warnings) > 40:
            print("  ... and %d more" % (len(warnings) - 40))
    if problems:
        print("\n%d PROBLEM(S):" % len(problems))
        for pr in problems[:60]:
            print("  ! %s" % pr)
        if len(problems) > 60:
            print("  ... and %d more" % (len(problems) - 60))
        sys.exit(1)
    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
