#!/usr/bin/env python3
"""
apply_overrides.py  —  V1
Adds (or removes) the <script src=".../content-overrides.js"> tag on every page.

Run it once after you download content-overrides.js from the admin panel and
drop the file into assets/js/ :

    python3 tools/apply_overrides.py            # add the tag everywhere
    python3 tools/apply_overrides.py --remove   # take it back out

The tag is inserted immediately after the existing content.js tag, which is
where assets/js/main.js expects to find the published overrides.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET = "assets/js/content-overrides.js"

CONTENT_RE = re.compile(r'(<script src="((?:\.\./)*)assets/js/content\.js"></script>)')
OVERRIDE_RE = re.compile(r'\n?<script src="(?:\.\./)*assets/js/content-overrides\.js"></script>')


def pages():
    out = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in (".git", "tools", "config", "__pycache__")]
        for fn in filenames:
            if fn.endswith(".html"):
                out.append(os.path.join(dirpath, fn))
    return sorted(out)


def main():
    remove = "--remove" in sys.argv
    if not remove and not os.path.exists(os.path.join(ROOT, TARGET)):
        raise SystemExit(
            "Cannot find %s\n"
            "Download it from the 'Save & publish' tab in admin/index.html first." % TARGET)

    changed = 0
    for path in pages():
        with open(path, "r", encoding="utf-8") as fh:
            src = fh.read()
        original = src

        src = OVERRIDE_RE.sub("", src)
        if not remove:
            def add(m):
                return m.group(1) + '\n<script src="%sassets/js/content-overrides.js"></script>' % m.group(2)
            src = CONTENT_RE.sub(add, src, count=1)

        if src != original:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(src)
            changed += 1

    print("%s the overrides tag on %d page(s)" % ("Removed" if remove else "Added", changed))


if __name__ == "__main__":
    main()
