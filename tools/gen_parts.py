"""
gen_parts.py  —  V4
Shared HTML building blocks: <head>, top bar, header/nav, page banner, footer,
floating widgets — plus the small CMS registry that keeps assets/js/content.js
in sync with the data-cms attributes in the markup.

V2: retargeted from the interiors build to a Maruti Suzuki dealership. AutoDealer
schema, a second (service) phone line in the top bar, the five-channel strip, the
model card / spec chip / accordion fragments, and a dealer disclaimer in the
footer that has to stay accurate because we are an authorised dealer, not the
manufacturer.

V3: the client's own logo file replaces the drawn wordmark. It is used byte for
byte as supplied — not recoloured, not cropped, no background removed — so the
mark is a square-ish tile with its own cream field. Because that mark carries no
words, it is locked up with the business name set in the site's own type, which
keeps the company name in the header for both readers and search engines without
touching the artwork.

V4: real Maruti Suzuki photography replaces the drawn silhouettes. Each model has
a studio cutout (WebP, alpha preserved so it sits on the card's own gradient) and
each page banner has a photograph chosen for that page's subject. The drawings
are gone from the pages but car_art() is kept: it is the fallback for a model
added later that has no photograph yet.
"""
import html
import json
import os
import re

from gen_cars import body_label, car_art
from gen_icons import icon
from gen_nav import FOOTER_COLUMNS, NAV

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------- config ---
def load_config():
    """Read assets/js/site-config.js (generated from the Excel workbook)."""
    path = os.path.join(ROOT, "assets", "js", "site-config.js")
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    start = src.index("{", src.index("window.SITE_CONFIG ="))
    # Walk the braces so the trailing SITE_CONFIG_META statement is ignored.
    depth, in_str, esc, end = 0, False, False, None
    for i in range(start, len(src)):
        ch = src[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end is None:
        raise SystemExit("Could not parse assets/js/site-config.js")
    return json.loads(src[start:end + 1])


CFG = load_config()
BIZ = CFG["business"]
NAME = BIZ["business_name"]
SITE_URL = BIZ["site_url"].rstrip("/")


# ------------------------------------------------------------- registry ---
# Every editable string/image on the site is registered here while pages are
# generated. generate_site.py then dumps it to assets/js/content.js so the admin
# panel knows exactly what can be edited, and with what default.
REGISTRY = []
_SEEN = set()


def reg(key, kind, value, label, group):
    if key in _SEEN:
        return value
    _SEEN.add(key)
    REGISTRY.append({"k": key, "t": kind, "v": value, "l": label, "g": group})
    return value


def cms_text(key, value, label, group, tag="p", cls="", extra=""):
    reg(key, "rich" if ("<" in value) else "text", value, label, group)
    cls_a = ' class="%s"' % cls if cls else ""
    ex = (" " + extra) if extra else ""
    return '<%s%s%s data-cms="%s">%s</%s>' % (tag, cls_a, ex, key, value, tag)


def cms_img(key, src, alt, w, h, label, group, cls="", lazy=True, extra=""):
    reg(key, "image", src, label, group)
    cls_a = ' class="%s"' % cls if cls else ""
    lz = ' loading="lazy" decoding="async"' if lazy else ""
    ex = (" " + extra) if extra else ""
    return ('<img%s src="%s" alt="%s" width="%d" height="%d"%s%s data-cms-src="%s">'
            % (cls_a, src, html.escape(alt, quote=True), w, h, lz, ex, key))


def cms_val(key, value, label, group, kind="text"):
    """Register a value that is used raw (in an attribute, or as link text)."""
    return reg(key, kind, value, label, group)


# ------------------------------------------------------------ path utils ---
def rel(href, depth):
    """Rewrite a root-relative href for a page nested `depth` folders deep."""
    if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
        return href
    return ("../" * depth) + href


def esc(s):
    return html.escape(s, quote=True)


# ------------------------------------------------------------------ head ---
def site_base_path():
    """Path component of site_url, e.g. https://u.github.io/repo -> /repo/ ."""
    m = re.match(r"^https?://[^/]+(/.*)?$", SITE_URL)
    path = (m.group(1) or "") if m else ""
    path = path.rstrip("/")
    return (path + "/") if path else "/"


def build_head(page, depth):
    p = lambda h: rel(h, depth)
    canonical = SITE_URL + "/" + page["href"]
    og_image = SITE_URL + "/assets/images/" + page.get("og_image", "og-default.png")

    return """<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
{head_first}<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{robots}">
<meta name="theme-color" content="{primary}">
<meta name="author" content="{name}">
<meta property="og:type" content="{ogtype}">
<meta property="og:site_name" content="{name}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{ogimg}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{ogimg}">
<link rel="icon" href="{fav}" type="image/png">
<link rel="apple-touch-icon" href="{fav}">
<link rel="preload" href="{font4}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{font7}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{css}">
<script src="{cfgjs}"></script>
<script src="{contentjs}"></script>
{ld}
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
""".format(
        title=esc(page["title"]),
        desc=esc(page["description"]),
        canonical=canonical,
        robots=page.get("robots", "index, follow"),
        primary=CFG["colors"]["primary"],
        name=esc(NAME),
        ogtype=page.get("og_type", "website"),
        ogimg=og_image,
        fav=p("assets/images/logo.png"),
        font4=p("assets/fonts/montserrat-400.woff2"),
        font7=p("assets/fonts/poppins-700.woff2"),
        css=p("assets/css/main.css"),
        cfgjs=p("assets/js/site-config.js"),
        contentjs=p("assets/js/content.js"),
        ld=json_ld(page),
        head_first=page.get("head_first", ""),
    )


def json_ld(page):
    addr = {
        "@type": "PostalAddress",
        "streetAddress": ", ".join(filter(None, [BIZ["address_line1"], BIZ["address_line2"]])),
        "addressLocality": BIZ["city"],
        "addressRegion": BIZ["state"],
        "postalCode": BIZ["pincode"],
        "addressCountry": "IN",
    }
    phone = "+" + BIZ["phone_country_code"] + BIZ["phone"]
    socials = [s["url"] for s in CFG["social"] if s.get("enabled") and s.get("url")]

    business = {
        "@context": "https://schema.org",
        "@type": ["AutoDealer", "AutomotiveBusiness", "LocalBusiness"],
        "@id": SITE_URL + "/#business",
        "name": NAME,
        "description": BIZ["short_description"],
        "url": SITE_URL + "/",
        "telephone": phone,
        "email": BIZ["email"],
        "image": SITE_URL + "/assets/images/og-default.png",
        "logo": SITE_URL + "/assets/images/logo.png",
        "priceRange": "₹₹",
        "currenciesAccepted": "INR",
        "address": addr,
        "areaServed": [{"@type": "City", "name": c} for c in
                       ("Thanjavur", "Kumbakonam", "Pattukkottai", "Papanasam", "Orathanadu")],
        "brand": {"@type": "Brand", "name": "Maruti Suzuki"},
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification",
             "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
             "opens": "09:00", "closes": "19:30"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday",
             "opens": "10:00", "closes": "17:00"},
        ],
        "sameAs": socials,
    }

    blocks = [business]

    crumbs = page.get("breadcrumb")
    if crumbs:
        items = []
        for i, (label, href) in enumerate(crumbs, start=1):
            entry = {"@type": "ListItem", "position": i, "name": label}
            if href:
                entry["item"] = SITE_URL + "/" + href
            items.append(entry)
        blocks.append({"@context": "https://schema.org", "@type": "BreadcrumbList",
                       "itemListElement": items})

    if page.get("faq_ld"):
        blocks.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": q,
                 "acceptedAnswer": {"@type": "Answer", "text": a}}
                for q, a in page["faq_ld"]
            ],
        })

    # A car model page. Price is indicative ex-showroom, so it is published as a
    # PriceSpecification with the currency and a note rather than a hard offer.
    if page.get("car_ld"):
        c = page["car_ld"]
        blocks.append({
            "@context": "https://schema.org", "@type": "Car",
            "name": "Maruti Suzuki " + c["name"],
            "brand": {"@type": "Brand", "name": "Maruti Suzuki"},
            "model": c["name"],
            "bodyType": c["body"],
            "vehicleSeatingCapacity": c["seats"],
            "fuelType": c["fuel"],
            "vehicleTransmission": c["gearbox"],
            "offers": {
                "@type": "Offer",
                "priceCurrency": "INR",
                "price": c["price_num"],
                "availability": "https://schema.org/InStock",
                "seller": {"@id": SITE_URL + "/#business"},
                "description": "Indicative ex-showroom price. On-road price varies with "
                               "variant, registration, insurance and accessories.",
            },
        })

    if page.get("article_ld"):
        a = page["article_ld"]
        blocks.append({
            "@context": "https://schema.org", "@type": "BlogPosting",
            "headline": a["headline"], "description": page["description"],
            "datePublished": a["date"], "dateModified": a["date"],
            "author": {"@type": "Organization", "name": NAME},
            "publisher": {"@type": "Organization", "name": NAME,
                          "logo": {"@type": "ImageObject",
                                   "url": SITE_URL + "/assets/images/logo.png"}},
            "mainEntityOfPage": SITE_URL + "/" + page["href"],
        })

    return "\n".join('<script type="application/ld+json">%s</script>'
                     % json.dumps(b, ensure_ascii=False, separators=(",", ":"))
                     for b in blocks)


# --------------------------------------------------------------- top bar ---
SOCIAL_ICONS = [
    ("facebook", "facebook", "Facebook"),
    ("instagram", "instagram", "Instagram"),
    ("youtube", "youtube", "YouTube"),
    ("linkedin", "linkedin", "LinkedIn"),
    ("twitter", "twitter", "X (Twitter)"),
    ("pinterest", "pinterest", "Pinterest"),
    ("indiamart", "store", "IndiaMART"),
    ("justdial", "book-open", "JustDial"),
]


def social_row(cls="social-row"):
    out = ['<div class="%s">' % cls]
    for platform, ic, label in SOCIAL_ICONS:
        out.append('<a href="#" data-social="%s" target="_blank" rel="noopener" '
                   'aria-label="%s">%s</a>' % (platform, label, icon(ic)))
    out.append("</div>")
    return "".join(out)


def build_topbar():
    """Two numbers, because a dealership gets two completely different calls:
    someone buying a car, and someone whose car is in the workshop."""
    return """<aside class="topbar" aria-label="Contact details and social links">
  <div class="container topbar__inner">
    <div class="topbar__contact">
      <a href="tel:+{cc}{phone}" data-biz-href="tel">{phone_icon}<span class="topbar__tag">Sales</span><span data-biz="phone_display">{phone_display}</span></a>
      <a href="tel:+{cc}{sphone}" data-biz-href="tel_service">{wrench_icon}<span class="topbar__tag">Service</span><span data-biz="phone_service_display">{sphone_display}</span></a>
      <span class="topbar__hours">{clock_icon}<span data-biz="business_hours">{hours}</span></span>
    </div>
    {social}
  </div>
</aside>
""".format(
        phone=BIZ["phone"], cc=BIZ["phone_country_code"],
        phone_display=esc(BIZ["phone_display"]),
        sphone=BIZ["phone_service"], sphone_display=esc(BIZ["phone_service_display"]),
        hours=esc(BIZ["business_hours"]),
        phone_icon=icon("phone"), wrench_icon=icon("wrench"), clock_icon=icon("clock"),
        social=social_row(),
    )


# ---------------------------------------------------------------- header ---
_CARET = ('<svg class="nav__caret" viewBox="0 0 12 8" aria-hidden="true">'
          '<path d="M1 1.5 6 6.5l5-5" stroke="currentColor" stroke-width="2" '
          'stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>')

_SUB_TOGGLE = ('<button type="button" class="submenu-toggle" aria-expanded="false" '
               'aria-controls="%s" aria-label="Show submenu for %s">'
               '<svg viewBox="0 0 12 8" aria-hidden="true">'
               '<path d="M1 1.5 6 6.5l5-5" stroke="currentColor" stroke-width="2" '
               'stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg></button>')


def _nav_items(items, depth, current, level=1, path="m"):
    """Every item renders as  <li><div class="nav-item"><a>…</a>[toggle]</div>[<ul>]</li>
    so one CSS selector works at every level and on every breakpoint.

    The toggle button is real markup, not something JS injects at runtime — the
    interiors build learned that the hard way when the CSS selectors and the DOM
    disagreed about where the <a> lived.
    """
    out = []
    for i, item in enumerate(items):
        children = item.get("children")
        sub_id = "%s-%d-%d" % (path, level, i)
        href = rel(item["href"], depth)
        classes = []
        if children:
            classes.append("has-children")
        if _is_current(item, current):
            classes.append("is-current")
        cls = ' class="%s"' % " ".join(classes) if classes else ""
        aria = ' aria-current="page"' if item["href"] == current else ""
        label = html.escape(item["label"])

        out.append("<li%s>" % cls)
        out.append('<div class="nav-item">')
        out.append('<a href="%s"%s><span>%s</span>%s</a>'
                   % (href, aria, label, _CARET if children else ""))
        if children:
            out.append(_SUB_TOGGLE % (sub_id, label))
        out.append("</div>")
        if children:
            out.append('<ul class="submenu" id="%s">' % sub_id)
            out.append(_nav_items(children, depth, current, level + 1, sub_id))
            out.append("</ul>")
        out.append("</li>")
    return "".join(out)


def _is_current(item, current):
    if item["href"] == current:
        return True
    for child in item.get("children", []):
        if _is_current(child, current):
            return True
    return False


def build_header(depth, current):
    p = lambda h: rel(h, depth)
    return """<header class="site-header">
  <div class="container">
    <div class="header-bar">
      <a class="brand" href="{home}" aria-label="{name} — home">
        <img class="brand__mark" src="{logo}" alt="" width="1024" height="831">
        <span class="brand__text">
          <span class="brand__name" data-biz="business_name">{name}</span>
          <span class="brand__tag" data-biz="tagline">{tagline}</span>
        </span>
      </a>
      <nav class="nav" id="site-nav" aria-label="Main navigation">
        <div class="nav__bar">
          <span class="nav__bar-title">Menu</span>
          <button type="button" class="nav__close" aria-label="Close menu">{close}</button>
        </div>
        <ul class="nav__list">{items}</ul>
      </nav>
      <div class="header-cta">
        <a class="btn btn--sm" href="{drive}"><span class="sr-only">Book a </span>Test Drive {arrow}</a>
        <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Open menu"><span></span></button>
      </div>
    </div>
  </div>
</header>
<div class="nav-backdrop"></div>
""".format(
        home=p("index.html"), logo=p("assets/images/logo.png"),
        name=esc(NAME), tagline=esc(BIZ["tagline"]),
        close=icon("close"), arrow=icon("arrow-right"),
        drive=p("test-drive.html"),
        items=_nav_items(NAV, depth, current),
    )


# ---------------------------------------------------------------- banner ---
def build_banner(page, depth, group):
    """Page banner. There is no photograph here on purpose — a coloured field
    carrying the channel colour is honest and loads instantly, where a stock
    photo of somebody else's car would not be either."""
    p = lambda h: rel(h, depth)
    key = page["key"]
    crumbs = page.get("breadcrumb") or [("Home", "index.html"), (page["nav_title"], None)]

    items = []
    for i, (label, href) in enumerate(crumbs):
        sep = icon("chevron-right") if i else ""
        if href and i < len(crumbs) - 1:
            items.append('<li>%s<a href="%s">%s</a></li>' % (sep, p(href), html.escape(label)))
        else:
            items.append('<li>%s<span aria-current="page">%s</span></li>'
                         % (sep, html.escape(label)))

    head_html = page["banner_heading"]
    reg("%s.banner.heading" % key, "rich", head_html, "Banner heading", group)
    reg("%s.banner.text" % key, "text", page["banner_text"], "Banner text", group)
    channel = page.get("channel", "")

    # A photograph behind the heading, where one fits the page. The scrim in the
    # stylesheet is what keeps the white heading legible over it; without a photo
    # the banner falls back to the channel-coloured field.
    banner_img = ""
    slug = page.get("banner_image")
    if slug:
        src = "assets/images/banners/%s.jpg" % slug
        if os.path.exists(os.path.join(ROOT, src)):
            bw, bh = image_size(src)
            banner_img = ('<div class="page-banner__media">%s</div>'
                          % cms_img("%s.banner.photo" % key, rel(src, depth),
                                    page.get("banner_alt", page["nav_title"]),
                                    bw, bh, "Banner photograph", group,
                                    lazy=False))

    return """<section class="page-banner{chcls}{imgcls}"{chattr}>
  {media}
  <div class="container page-banner__inner">
    <div class="page-banner__copy">
      {eyebrow}
      <h1 data-cms="{key}.banner.heading">{heading}</h1>
      <p data-cms="{key}.banner.text">{text}</p>
    </div>
    <nav aria-label="Breadcrumb">
      <ol class="breadcrumb">{crumbs}</ol>
    </nav>
  </div>
</section>
""".format(
        chcls=" page-banner--channel" if channel else "",
        imgcls=" page-banner--photo" if banner_img else "",
        media=banner_img,
        chattr=' data-channel="%s"' % channel if channel else "",
        eyebrow=('<span class="eyebrow">%s</span>' % html.escape(page["banner_eyebrow"]))
                if page.get("banner_eyebrow") else "",
        key=key, heading=head_html, text=html.escape(page["banner_text"]),
        crumbs="".join(items),
    )


# ---------------------------------------------------------------- footer ---
def build_footer(depth):
    p = lambda h: rel(h, depth)

    cols = []
    for title, links in FOOTER_COLUMNS:
        lis = "".join('<li><a href="%s">%s</a></li>' % (p(h), html.escape(l)) for l, h in links)
        cols.append('<div class="footer-col"><h3>%s</h3><ul>%s</ul></div>' % (title, lis))

    return """<section class="newsletter" aria-labelledby="newsletter-title">
  <div class="container newsletter__inner">
    <div>
      <h2 id="newsletter-title">Offers, before they expire</h2>
      <p>Monthly consumer offers, exchange bonuses and service camps. One email a month, no more.</p>
    </div>
    <form data-demo-form novalidate>
      <label class="sr-only" for="nl-email">Email address</label>
      <input id="nl-email" type="email" name="email" placeholder="Your email address" required>
      <button class="btn" type="submit">Subscribe {arrow}</button>
    </form>
    <div class="form-status" role="status" aria-live="polite"></div>
  </div>
</section>

<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-col footer-brand">
        <div class="brand brand--footer">
          <img class="brand__mark" src="{logo}" alt="" width="1024" height="831">
          <span class="brand__text">
            <span class="brand__name" data-biz="business_name">{name}</span>
            <span class="brand__tag" data-biz="tagline">{tagline}</span>
          </span>
        </div>
        <p data-biz="short_description">{desc}</p>
        {social}
      </div>
      {cols}
      <div class="footer-col">
        <h3>Reach Us</h3>
        <ul class="footer-contact">
          <li>{pin}<span data-biz="address_block">{addr}</span></li>
          <li>{ph}<a href="tel:+{cc}{phone}" data-biz-href="tel">Sales <span data-biz="phone_display">{phone_display}</span></a></li>
          <li>{wr}<a href="tel:+{cc}{sphone}" data-biz-href="tel_service">Service <span data-biz="phone_service_display">{sphone_display}</span></a></li>
          <li>{ml}<a href="mailto:{email}" data-biz-href="mail"><span data-biz="email">{email}</span></a></li>
          <li>{cl}<span data-biz="business_hours">{hours}</span></li>
        </ul>
      </div>
    </div>
    <p class="footer-disclaimer" data-biz="dealer_disclaimer">{disclaimer}</p>
    <div class="footer-bottom">
      <p>&copy; <span data-year>{year}</span> <span data-biz="copyright_line">{copy}</span></p>
      <div class="legal-links">
        <a href="{privacy}">Privacy Policy</a>
        <a href="{terms}">Terms &amp; Conditions</a>
        <a href="{sitemapp}">Sitemap</a>
      </div>
    </div>
  </div>
</footer>

<aside class="fab-stack" aria-label="Quick actions">
  <button type="button" class="fab fab--theme" id="theme-fab" aria-expanded="false" aria-controls="theme-panel" aria-label="Change site colours">{paint}</button>
  <a class="fab fab--whatsapp" href="#" data-biz-href="wa" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{wa}</a>
  <button type="button" class="fab fab--top" id="back-to-top" aria-label="Back to top">{up}</button>
</aside>

<aside class="theme-panel" id="theme-panel" aria-label="Colour theme picker">
  <h5>Colour theme</h5>
  <p>Prefer a different palette? Pick one — your choice is remembered on this device.</p>
  <div class="theme-panel__grid"></div>
  <div class="theme-panel__custom">
    <label for="tp-primary">Primary <input type="color" id="tp-primary" value="{c1}"></label>
    <label for="tp-secondary">Secondary <input type="color" id="tp-secondary" value="{c2}"></label>
    <label for="tp-tertiary">Accent <input type="color" id="tp-tertiary" value="{c3}"></label>
    <div class="theme-panel__actions">
      <button type="button" class="btn btn--outline btn--sm" id="theme-reset">Reset</button>
      <button type="button" class="btn btn--sm" id="theme-close">Done</button>
    </div>
  </div>
</aside>

<script src="{js}"></script>
</body>
</html>
""".format(
        arrow=icon("arrow-right"),
        logo=p("assets/images/logo.png"),
        name=esc(NAME), tagline=esc(BIZ["tagline"]),
        desc=html.escape(BIZ["short_description"]),
        social=social_row(),
        cols="".join(cols),
        pin=icon("map-pin"), ph=icon("phone"), ml=icon("mail"),
        cl=icon("clock"), wr=icon("wrench"),
        addr=html.escape(", ".join(filter(None, [
            BIZ["address_line1"], BIZ["address_line2"],
            "%s - %s" % (BIZ["city"], BIZ["pincode"]), BIZ["state"]]))),
        cc=BIZ["phone_country_code"], phone=BIZ["phone"],
        phone_display=esc(BIZ["phone_display"]),
        sphone=BIZ["phone_service"], sphone_display=esc(BIZ["phone_service_display"]),
        email=esc(BIZ["email"]),
        hours=esc(BIZ["business_hours"]),
        disclaimer=html.escape(BIZ["dealer_disclaimer"]),
        year="2026", copy=html.escape(BIZ["copyright_line"]),
        privacy=p("privacy-policy.html"), terms=p("terms-conditions.html"),
        sitemapp=p("sitemap.xml"),
        paint=icon("palette"), wa=icon("whatsapp"), up=icon("arrow-up"),
        c1=CFG["colors"]["primary"], c2=CFG["colors"]["secondary"],
        c3=CFG["colors"]["tertiary"],
        js=p("assets/js/main.js"),
    )


# ------------------------------------------------------------- fragments ---
def section_head(key, eyebrow, title, group, text=None, align="center"):
    cls = "section-head" + ("" if align == "center" else " section-head--left")
    parts = ['<div class="%s reveal">' % cls]
    if eyebrow:
        parts.append(cms_text(key + ".eyebrow", eyebrow, "Eyebrow", group, "span", "eyebrow"))
    parts.append(cms_text(key + ".title", title, "Heading", group, "h2"))
    if text:
        parts.append(cms_text(key + ".text", text, "Intro text", group, "p"))
    parts.append("</div>")
    return "".join(parts)


def checklist(items, cls="checklist"):
    lis = "".join('<li>%s<span>%s</span></li>' % (icon("check-square"), html.escape(i))
                  for i in items)
    return '<ul class="%s">%s</ul>' % (cls, lis)


def btn(label, href, cls="btn", arrow=True):
    ic = (" " + icon("arrow-right")) if arrow else ""
    return '<a class="%s" href="%s">%s%s</a>' % (cls, href, html.escape(label), ic)


def wa_button(label, message, cls="btn btn--wa"):
    return ('<a class="%s" href="#" data-biz-href="wa" data-wa-message="%s" '
            'target="_blank" rel="noopener">%s %s</a>'
            % (cls, esc(message), html.escape(label), icon("whatsapp")))


def stars(n=5):
    # role="img" is required for aria-label to be permitted on a plain div.
    return ('<div class="quote-card__stars" role="img" aria-label="%d out of 5 stars">%s</div>'
            % (n, icon("star") * n))


# --- automotive fragments ---------------------------------------------------
SPEC_ICONS = [
    ("seats", "users", "Seats"),
    ("fuel", "fuel", "Fuel"),
    ("gearbox", "gearbox", "Transmission"),
    ("mileage", "gauge", "Mileage"),
    ("engine", "cog", "Engine"),
]


def spec_chips(model, keys=("seats", "fuel", "gearbox", "mileage")):
    """The small icon+value row under a model name. `title` carries the label so
    the icon is never the only thing conveying meaning."""
    out = ['<ul class="spec-chips">']
    for key, ic, label in SPEC_ICONS:
        if key not in keys:
            continue
        out.append('<li><span class="spec-chips__icon" title="%s">%s</span>'
                   '<span class="sr-only">%s: </span>%s</li>'
                   % (label, icon(ic), label, html.escape(model[key])))
    out.append("</ul>")
    return "".join(out)


def price_line(model, cls="price"):
    return ('<p class="%s"><span class="price__from">From</span> '
            '<span class="price__value">&#8377;%s</span> '
            '<span class="price__note">ex-showroom</span></p>'
            % (cls, html.escape(model["price"])))


def channel_pill(channel):
    return ('<span class="pill pill--channel" data-channel="%s">%s</span>'
            % (channel["colour"], html.escape(channel["short"])))


def art_slot(model, depth, group):
    """Register the model's illustration as an editable image and return its key.

    One key per model, shared by the card and the model page, so the owner
    uploads official Maruti media-kit photography once and it appears in both
    places. The registered default points at the standalone SVG of the drawing
    so the admin panel can show what is currently in use.
    """
    key = "model.%s.art" % model["key"]
    # Root-relative: the admin panel resolves image values from one fixed place.
    reg(key, "image", "assets/images/cars/%s.webp" % model["key"],
        "%s — photograph" % model["name"], group)
    return key


_DIMS = {}


def image_size(rel):
    """Real pixel size of a file in the build, cached. Emitting the true
    width/height means the browser reserves the right box before the image
    arrives, so nothing jumps as the page loads."""
    if rel not in _DIMS:
        path = os.path.join(ROOT, rel)
        try:
            with open(path, "rb") as fh:
                head = fh.read(64)
            if head[:4] == b"RIFF" and head[8:12] == b"WEBP":
                # VP8X / VP8L / VP8 all carry the canvas size in the first chunk.
                if head[12:16] == b"VP8X":
                    w = int.from_bytes(head[24:27], "little") + 1
                    h = int.from_bytes(head[27:30], "little") + 1
                elif head[12:16] == b"VP8 ":
                    w = int.from_bytes(head[26:28], "little") & 0x3FFF
                    h = int.from_bytes(head[28:30], "little") & 0x3FFF
                else:                                    # VP8L
                    bits = int.from_bytes(head[21:25], "little")
                    w = (bits & 0x3FFF) + 1
                    h = ((bits >> 14) & 0x3FFF) + 1
                _DIMS[rel] = (w, h)
            else:
                _DIMS[rel] = _jpeg_size(path)
        except Exception:
            _DIMS[rel] = (1600, 900)
    return _DIMS[rel]


def _jpeg_size(path):
    with open(path, "rb") as fh:
        data = fh.read()
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1; continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h = int.from_bytes(data[i + 5:i + 7], "big")
            w = int.from_bytes(data[i + 7:i + 9], "big")
            return (w, h)
        i += 2 + int.from_bytes(data[i + 2:i + 4], "big")
    return (1600, 900)


def car_photo(model, depth, cls="", lazy=True):
    """The model's studio photograph. Falls back to the drawn silhouette if no
    photograph has been supplied for that model."""
    rel = "assets/images/cars/%s.webp" % model["key"]
    if not os.path.exists(os.path.join(ROOT, rel)):
        return car_art(model["body"], "Maruti Suzuki " + model["name"])
    w, h = image_size(rel)
    lz = ' loading="lazy" decoding="async"' if lazy else ' decoding="async"'
    cls_a = ' class="%s"' % cls if cls else ""
    return ('<img%s src="%s" alt="Maruti Suzuki %s" width="%d" height="%d"%s>'
            % (cls_a, rel_url(rel, depth), esc(model["name"]), w, h, lz))


def rel_url(href, depth):
    return ("../" * depth) + href


def model_card(model, depth, channels, group, reveal=True):
    """One car in a grid. The silhouette is a CMS image slot too, so the client
    can drop official Maruti media-kit photography in later without touching a
    line of markup."""
    p = lambda h: rel(h, depth)
    ch = channels[model["channel"]]
    href = p("cars/%s.html" % model["key"])
    key = "model.%s.card" % model["key"]
    art_key = art_slot(model, depth, "Cars")
    reg(key + ".pitch", "text", model["pitch"], "%s — card text" % model["name"], group)
    return """<article class="model-card{rev}" data-channel="{colour}">
  <a class="model-card__media" href="{href}" tabindex="-1" aria-hidden="true">
    <span class="model-card__art" data-cms-art="{art_key}" data-art-alt="Maruti Suzuki {name}">{art}</span>
  </a>
  <div class="model-card__body">
    <div class="model-card__top">
      {pill}
      <span class="model-card__body-type">{body}</span>
    </div>
    <h3><a href="{href}">{name}</a></h3>
    <p data-cms="{key}.pitch">{pitch}</p>
    {chips}
    {price}
    <span class="model-card__link">View {name} {arrow}</span>
  </div>
</article>""".format(
        rev=" reveal" if reveal else "",
        colour=ch["colour"], href=href, key=key, art_key=art_key,
        art=car_photo(model, depth, cls="model-card__photo"),
        pill=channel_pill(ch),
        body=html.escape(body_label(model["body"])),
        name=html.escape(model["name"]), pitch=html.escape(model["pitch"]),
        chips=spec_chips(model), price=price_line(model),
        arrow=icon("arrow-right"),
    )


def accordion(items, key, group, open_first=True):
    """items: list of (question, answer). Native <details> so it works with JS
    disabled and is keyboard-operable for free."""
    out = ['<div class="accordion">']
    for i, (q, a) in enumerate(items):
        reg("%s.%d.q" % (key, i), "text", q, "Question %d" % (i + 1), group)
        reg("%s.%d.a" % (key, i), "text", a, "Answer %d" % (i + 1), group)
        out.append('<details class="accordion__item"%s>' % (" open" if (i == 0 and open_first) else ""))
        out.append('<summary><span data-cms="%s.%d.q">%s</span>%s</summary>'
                   % (key, i, html.escape(q), icon("plus")))
        out.append('<div class="accordion__body"><p data-cms="%s.%d.a">%s</p></div>'
                   % (key, i, html.escape(a)))
        out.append("</details>")
    out.append("</div>")
    return "".join(out)


def indian_group(n):
    """18000 -> 18,000 and 1650000 -> 16,50,000. Mirrors format() in main.js."""
    s = str(int(n))
    if len(s) <= 3:
        return s
    head, tail = s[:-3], s[-3:]
    out = []
    while len(head) > 2:
        out.insert(0, head[-2:])
        head = head[:-2]
    if head:
        out.insert(0, head)
    return ",".join(out) + "," + tail


def stat_row(stats, group, key="stats"):
    """stats: list of (value, suffix, label).

    The final number is baked into the markup, not "0". The count-up animation
    zeroes it at the moment it starts, so a visitor without JavaScript — or one
    whose IntersectionObserver never fires because the element is already past —
    reads the real figure instead of a row of zeros.
    """
    out = ['<div class="stat-row reveal">']
    for i, (value, suffix, label) in enumerate(stats):
        reg("%s.%d.label" % (key, i), "text", label, "Stat %d label" % (i + 1), group)
        out.append('<div class="stat"><span class="stat__value">'
                   '<span data-count="%s">%s</span>%s</span>'
                   '<span class="stat__label" data-cms="%s.%d.label">%s</span></div>'
                   % (value, indian_group(value), html.escape(suffix),
                      key, i, html.escape(label)))
    out.append("</div>")
    return "".join(out)


def step_list(steps, cls="steps"):
    """steps: list of (title, text). Numbered, because these are sequences."""
    out = ['<ol class="%s">' % cls]
    for i, (title, text) in enumerate(steps, start=1):
        out.append('<li class="steps__item reveal"><span class="steps__num">%02d</span>'
                   '<div><h3>%s</h3><p>%s</p></div></li>'
                   % (i, html.escape(title), html.escape(text)))
    out.append("</ol>")
    return "".join(out)


def icon_card(ic, title, text, cls="icon-card", channel=""):
    ch = ' data-channel="%s"' % channel if channel else ""
    return ('<article class="%s reveal"%s><span class="icon-card__icon">%s</span>'
            '<h3>%s</h3><p>%s</p></article>'
            % (cls, ch, icon(ic), html.escape(title), html.escape(text)))


def map_embed(depth, cls="map-embed"):
    return ('<div class="%s"><iframe src="%s" title="Map to %s on Google Maps" '
            'width="600" height="450" style="border:0" loading="lazy" '
            'referrerpolicy="no-referrer-when-downgrade" '
            'allowfullscreen data-biz-src="map"></iframe></div>'
            % (cls, esc(BIZ["map_embed_url"]), esc(NAME)))
