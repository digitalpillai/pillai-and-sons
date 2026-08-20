"""
gen_og_image.py  —  V3
Renders assets/images/og-default.png, the 1200x630 card that Facebook, LinkedIn,
WhatsApp and X show when someone shares a link to the site.

Every page's <meta property="og:image"> points at this file. Without it a shared
link renders as a bare grey box, which for a dealership is the difference
between a WhatsApp forward that looks legitimate and one that does not.

It is drawn from the same tokens as the site — the logo, the brand red, Poppins
and Montserrat — so the card and the site cannot drift apart.

V2: uses the client's supplied logo file as-is. The mark carries its own cream
field, so on the dark card it reads as a logo tile rather than a knocked-out
wordmark; the company name sits beside it in the site's own type.

V3: the drawn silhouette on the right is replaced by the Grand Vitara studio
photograph the site now ships.

Run:  python3 tools/gen_og_image.py

Needs a headless Chromium. Playwright is used when it is installed, because it
gives an exact 1200x630 viewport. Otherwise the script falls back to driving
Chromium directly — and there it has to probe first: `--window-size=1200,630`
produces a 1200x630 *screenshot* but only a 1200x543 *viewport*, because the
window furniture is counted in the requested size and not in the capture. The
probe measures that difference, the window is enlarged by it, and the extra rows
are cropped off. Getting this wrong is what silently cut the bottom line off the
first version of this card.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import gen_parts as P  # noqa: E402  (needs ROOT on the path first)
from gen_cars import car_art  # noqa: E402  (fallback only)

W, H = 1200, 630


def find_chromium():
    env = os.environ.get("CHROMIUM")
    if env and os.path.exists(env):
        return env
    for pattern in ("/opt/pw-browsers/chromium*/chrome-linux/chrome",
                    "/opt/pw-browsers/chromium*/chrome-linux64/chrome"):
        hits = sorted(glob.glob(pattern))
        if hits:
            return hits[-1]
    for name in ("chromium", "chromium-browser", "google-chrome"):
        path = shutil.which(name)
        if path:
            return path
    return None


def car_html():
    """The flagship car for the share card: the real photograph when it is in
    the build, the drawing otherwise."""
    rel = os.path.join(ROOT, "assets", "images", "cars", "grand-vitara.webp")
    if os.path.exists(rel):
        return '<img src="file://%s" alt="">' % rel
    return car_art("mid-suv")


def build_html():
    biz = P.BIZ
    colors = P.CFG["colors"]
    fonts_dir = os.path.join(ROOT, "assets", "fonts")

    def font_face(family, weight, filename):
        return ("@font-face{font-family:%s;font-weight:%d;font-style:normal;"
                "src:url('file://%s') format('woff2')}"
                % (family, weight, os.path.join(fonts_dir, filename)))

    faces = "".join([
        font_face("Poppins", 700, "poppins-700.woff2"),
        font_face("Poppins", 600, "poppins-600.woff2"),
        font_face("Montserrat", 400, "montserrat-400.woff2"),
        font_face("Montserrat", 600, "montserrat-600.woff2"),
    ])

    logo = os.path.join(ROOT, "assets", "images", "logo.png")
    channels = " &nbsp;·&nbsp; ".join(c["short"] for c in
                                      __import__("gen_content").CHANNELS)

    return """<!doctype html><html><head><meta charset="utf-8"><style>
%(faces)s
*{box-sizing:border-box;margin:0}
html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{background:%(dark)s;color:#fff;font-family:Montserrat,sans-serif;
  position:relative;display:flex;flex-direction:column;justify-content:space-between;
  padding:52px 64px 44px}
.glow{position:absolute;inset:0;
  background:radial-gradient(760px 420px at 84%% 4%%, %(brand)s55, transparent 62%%),
             radial-gradient(560px 360px at 2%% 100%%, %(blue)s3d, transparent 60%%)}
.road{position:absolute;left:0;right:0;bottom:0;height:6px;
  background:repeating-linear-gradient(to right, #ffffff33 0 56px, transparent 56px 112px)}
.top,.mid,.bot{position:relative}
.lockup{display:flex;align-items:center;gap:16px}
.logo{height:76px;width:auto;display:block}
.lockup .nm{font-family:Poppins,sans-serif;font-weight:700;font-size:26px;line-height:1.1;letter-spacing:-.01em;color:#fff}
.lockup .tg{font-size:12px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#ffffff99;margin-top:4px}
h1{font-family:Poppins,sans-serif;font-weight:700;font-size:46px;line-height:1.08;
  letter-spacing:-.02em;max-width:15ch}
h1 em{font-style:normal;color:%(brand)s}
p{margin-top:16px;font-size:21px;line-height:1.45;color:#ffffffcc;max-width:30ch}
.bot{display:flex;align-items:flex-end;justify-content:space-between;gap:40px}
.chan{font-family:Poppins,sans-serif;font-weight:600;font-size:17px;letter-spacing:.06em;
  text-transform:uppercase;color:#ffffffb3}
.meta{margin-top:10px;font-size:20px;color:#fff}
.car{position:absolute;right:-10px;top:225px;width:560px}
.car svg{width:100%%;height:auto;color:#fff}
.car img{width:100%%;height:auto;display:block}
</style></head><body>
<div class="glow"></div>
<div class="top"><div class="lockup"><img class="logo" src="file://%(logo)s" alt=""><div><div class="nm">%(name)s</div><div class="tg">%(tagline)s</div></div></div></div>
<div class="car">%(car)s</div>
<div class="mid">
  <h1>Authorised <em>Maruti Suzuki</em> dealer in Thanjavur</h1>
  <p>New cars, certified pre-owned, an authorised workshop and the driving school &mdash; one address.</p>
</div>
<div class="bot">
  <div>
    <div class="chan">%(channels)s</div>
    <div class="meta">%(phone)s &nbsp;·&nbsp; Medical College Road, Thanjavur</div>
  </div>
</div>
<div class="road"></div>
</body></html>""" % {
        "faces": faces, "w": W, "h": H,
        "dark": colors["secondary"], "brand": colors["primary"], "blue": colors["tertiary"],
        "logo": logo, "car": car_html(), "channels": channels,
        "phone": biz["phone_display"],
        "name": biz["business_name"], "tagline": biz["tagline"],
    }


def render_with_playwright(html_path, out):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False
    launch = {}
    chrome = find_chromium()
    if chrome:
        launch["executable_path"] = chrome
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(**launch)
            page = browser.new_page(viewport={"width": W, "height": H},
                                    device_scale_factor=1)
            page.goto("file://" + html_path)
            page.wait_for_timeout(400)
            page.screenshot(path=out)
            browser.close()
        return True
    except Exception as exc:                      # noqa: BLE001
        print("Playwright render failed (%s); falling back to raw Chromium." % exc)
        return False


PROBE = ("<!doctype html><meta charset=utf-8><title>x</title>"
         "<script>document.title = innerWidth + 'x' + innerHeight;</script>")


def viewport_offset(chrome, tmp):
    """How many pixels of the requested window size never reach the viewport."""
    probe = os.path.join(tmp, "probe.html")
    with open(probe, "w", encoding="utf-8") as fh:
        fh.write(PROBE)
    res = subprocess.run(
        [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
         "--window-size=%d,%d" % (W, H), "--dump-dom", "file://" + probe],
        capture_output=True)
    dom = res.stdout.decode("utf-8", "replace")
    m = re.search(r"<title>(\d+)x(\d+)</title>", dom)
    if not m:
        return 0
    return H - int(m.group(2))


def render_with_chromium(chrome, html_path, out, tmp):
    dy = viewport_offset(chrome, tmp)
    raw = os.path.join(tmp, "raw.png")
    cmd = [chrome, "--headless", "--disable-gpu", "--no-sandbox",
           "--hide-scrollbars", "--allow-file-access-from-files",
           "--force-device-scale-factor=1",
           "--window-size=%d,%d" % (W, H + dy),
           "--screenshot=" + raw, "file://" + html_path]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0 or not os.path.exists(raw):
        print("Chromium failed:\n" + res.stderr.decode("utf-8", "replace")[-800:])
        return False

    if dy == 0:
        shutil.move(raw, out)
        return True

    try:
        from PIL import Image
    except ImportError:
        print("Rendered at %dx%d but Pillow is not installed to crop it back to "
              "%dx%d. Install Pillow, or install Playwright, and re-run."
              % (W, H + dy, W, H))
        return False
    Image.open(raw).crop((0, 0, W, H)).save(out)
    return True


def main():
    out = os.path.join(ROOT, "assets", "images", "og-default.png")
    tmp = tempfile.mkdtemp(prefix="og-")
    html = os.path.join(tmp, "og.html")
    with open(html, "w", encoding="utf-8") as fh:
        fh.write(build_html())

    done = render_with_playwright(html, out)
    if not done:
        chrome = find_chromium()
        if not chrome:
            print("No Chromium found — leaving og-default.png as it is.\n"
                  "Set CHROMIUM=/path/to/chrome and re-run.")
            shutil.rmtree(tmp, ignore_errors=True)
            return 1
        done = render_with_chromium(chrome, html, out, tmp)

    shutil.rmtree(tmp, ignore_errors=True)
    if not done:
        return 1
    print("assets/images/og-default.png  %d x %d, %.0f KB"
          % (W, H, os.path.getsize(out) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(main())
