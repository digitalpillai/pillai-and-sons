"""
generate_site.py  —  V1
Builds every page of the Pillai & Sons Motor Company site.

Run:  python3 tools/generate_site.py

Reads
  gen_content.py   all copy: models, services, courses, FAQs, posts, jobs
  gen_nav.py       the navigation tree and footer columns
  gen_parts.py     shared markup (head/header/banner/footer) + the CMS registry
  gen_cars.py      the car silhouettes
  gen_icons.py     the inline icon set
  assets/js/site-config.js   business details, colours, fonts (from the Excel)

Writes
  *.html                       50 pages
  assets/js/content.js         the editable-content manifest the admin panel reads
  sitemap.xml, robots.txt, .nojekyll

Nothing here runs in the browser. The output is plain static HTML that works
from file:// as well as over HTTP.
"""
import html
import json
import os
import re
import shutil

import gen_content as C
import gen_legal as L
import gen_parts as P
from gen_cars import body_label, car_art
from gen_icons import check_required, icon
from gen_nav import NAV

ROOT = P.ROOT
BIZ = P.BIZ
CFG = P.CFG
NAME = P.NAME

e = html.escape
esc = P.esc
reg = P.reg
cms_text = P.cms_text
section_head = P.section_head
checklist = P.checklist
btn = P.btn
wa_button = P.wa_button
stars = P.stars
accordion = P.accordion
model_card = P.model_card
spec_chips = P.spec_chips
price_line = P.price_line
channel_pill = P.channel_pill
icon_card = P.icon_card
step_list = P.step_list
stat_row = P.stat_row
map_embed = P.map_embed

CH = C.CHANNEL_BY_KEY
PAGES = []


# ---------------------------------------------------------------------------
#  GitHub Pages base-path shim.
#
#  A 404 served from a deep path (/cars/swift-typo.html) is rendered by GitHub
#  at that URL, so every relative asset href in 404.html resolves one directory
#  too low and the page arrives unstyled. Injecting a <base> as the very first
#  thing in <head> fixes it without hard-coding the repository name — the name
#  is read back out of the URL when the configured site_url does not match.
# ---------------------------------------------------------------------------
# The <base> tag written into 404.html. It is filled in twice: once as a real
# attribute (so Chromium's preload scanner, which starts fetching CSS and fonts
# before it reaches an inline script, gets the right answer immediately) and once
# inside the script that corrects it if the page turns out to be served from
# somewhere other than the configured site_url.
BASE_SHIM = """%s<script>
(function () {
  var el = document.querySelector("base[data-auto]");
  if (!el) {
    el = document.createElement("base");
    el.setAttribute("data-auto", "");
    document.head.insertBefore(el, document.head.firstChild);
  }

  if (location.protocol === "file:") {
    // Opened straight off disk. The published base is meaningless here; this
    // file sits at the site root, so point at its own folder.
    el.href = location.href.replace(/[^/]*$/, "");
    return;
  }

  var BASE = %s;
  var path = location.pathname;
  if (path.indexOf(BASE) !== 0) {
    // Served from somewhere other than the configured site_url. On a
    // *.github.io project site the first path segment is the repository name;
    // anywhere else, assume the domain root.
    var seg = path.split("/").filter(Boolean);
    BASE = (/\\.github\\.io$/.test(location.hostname) && seg.length > 1) ? "/" + seg[0] + "/" : "/";
  }
  if (el.getAttribute("href") !== BASE) el.href = BASE;

  document.addEventListener("DOMContentLoaded", function () {
    // <base> also retargets bare fragment links, which would otherwise jump to
    // the home page instead of scrolling.
    var here = location.pathname + location.search;
    Array.prototype.forEach.call(document.querySelectorAll('a[href^="#"]'), function (a) {
      a.setAttribute("href", here + a.getAttribute("href"));
    });
  });
}());
</script>
"""


# ===========================================================================
#  FORMS
# ===========================================================================
def field(name, label, kind="text", required=False, placeholder="", options=None,
          value="", extra=""):
    req = ' required aria-required="true"' if required else ""
    star = ' <span class="req" aria-hidden="true">*</span>' if required else ""
    fid = "f-" + re.sub(r"[^a-z0-9]+", "-", (extra or name + label).lower()).strip("-")
    ph = ' placeholder="%s"' % esc(placeholder) if placeholder else ""

    if kind == "select":
        opts = "".join('<option value="%s"%s>%s</option>'
                       % (esc(o), " selected" if o == value else "", e(o or placeholder or "Select"))
                       for o in ([""] + list(options or [])))
        control = '<select id="%s" name="%s"%s>%s</select>' % (fid, name, req, opts)
    elif kind == "textarea":
        control = '<textarea id="%s" name="%s"%s%s>%s</textarea>' % (fid, name, req, ph, e(value))
    elif kind == "checkbox":
        return ('<div class="form-field form-field--full"><label class="form-consent" for="%s">'
                '<input id="%s" type="checkbox" name="%s"%s> <span>%s</span></label>'
                '<span class="field-error" aria-live="polite"></span></div>'
                % (fid, fid, name, req, label))
    else:
        control = ('<input id="%s" type="%s" name="%s"%s%s value="%s">'
                   % (fid, kind, name, req, ph, esc(value)))

    full = ' form-field--full' if kind == "textarea" else ""
    return ('<div class="form-field%s"><label for="%s">%s%s</label>%s'
            '<span class="field-error" aria-live="polite"></span></div>'
            % (full, fid, e(label), star, control))


def form_block(fid, heading, fields, submit="Send on WhatsApp", intro=None,
               hidden=None, note=None):
    """Every enquiry form ends in a WhatsApp click-to-chat URL. There is no
    server behind this site, so a mail-to form would silently fail; WhatsApp
    delivers the message to a number the business actually watches."""
    hid = "".join('<input type="hidden" name="%s" value="%s" data-label="%s">'
                  % (k, esc(v), esc(l)) for k, v, l in (hidden or []))
    return """<form class="form-card" data-wa-form data-wa-heading="%(head)s" id="%(id)s" novalidate>
  <h2>%(title)s</h2>
  %(intro)s
  %(hidden)s
  <div class="form-grid">%(fields)s</div>
  <div class="mt-32"><button class="btn btn--block" type="submit">%(submit)s %(wa)s</button></div>
  <div class="form-status" role="status" aria-live="polite"></div>
  %(note)s
</form>""" % {
        "head": esc(heading), "id": fid, "title": e(heading),
        "intro": '<p>%s</p>' % e(intro) if intro else "",
        "hidden": hid, "fields": "".join(fields),
        "submit": e(submit), "wa": icon("whatsapp"),
        "note": '<p class="form-note">%s</p>' % e(note) if note else
                '<p class="form-note">Your details open in WhatsApp so you can '
                'check them before sending. Nothing is stored on this website.</p>',
    }


MODEL_NAMES = [m["name"] for m in C.MODELS]
CITY_LIST = ["Thanjavur", "Kumbakonam", "Pattukkottai", "Orathanadu", "Papanasam", "Other"]


def enquiry_fields(with_model=True, model_value=""):
    f = [field("name", "Your name", required=True, placeholder="Full name", extra="enq-name"),
         field("phone", "Phone", "tel", required=True, placeholder="10-digit mobile", extra="enq-phone"),
         field("email", "Email", "email", placeholder="you@example.com", extra="enq-email"),
         field("city", "City", "select", options=CITY_LIST, extra="enq-city")]
    if with_model:
        f.append(field("model", "Model of interest", "select", options=MODEL_NAMES,
                       value=model_value, extra="enq-model"))
        f.append(field("finance", "Do you need finance?", "select",
                       options=["Yes, please arrange it", "No, paying outright", "Not decided"],
                       extra="enq-finance"))
    f.append(field("message", "Anything else we should know?", "textarea",
                   placeholder="Variant, colour, timeline, exchange car…", extra="enq-msg"))
    return f


# ===========================================================================
#  SHARED SECTION BUILDERS
# ===========================================================================
def cta_band(title, text, actions, group, key):
    reg(key + ".title", "text", title, "CTA heading", group)
    reg(key + ".text", "text", text, "CTA text", group)
    return """<section class="section section--tight"><div class="container">
  <div class="cta-band reveal">
    <div><h2 data-cms="%s.title">%s</h2><p data-cms="%s.text">%s</p></div>
    <div class="cta-band__actions">%s</div>
  </div>
</div></section>""" % (key, e(title), key, e(text), "".join(actions))


def channel_cards(depth, group):
    p = lambda h: P.rel(h, depth)
    hrefs = {"arena": "cars/arena.html", "nexa": "cars/nexa.html",
             "true-value": "true-value/index.html", "service": "service/index.html",
             "driving-school": "driving-school.html"}
    out = ['<div class="channel-grid">']
    for c in C.CHANNELS:
        reg("channel.%s.blurb" % c["key"], "text", c["blurb"], "%s blurb" % c["short"], group)
        out.append("""<article class="channel-card reveal" data-channel="%s">
  <span class="channel-card__icon">%s</span>
  <span class="channel-card__tag">%s</span>
  <h3>%s</h3>
  <p data-cms="channel.%s.blurb">%s</p>
  <a class="link-more" href="%s">Explore %s %s</a>
</article>""" % (c["colour"], icon(c["icon"]), e(c["tag"]), e(c["name"]),
                 c["key"], e(c["blurb"]), p(hrefs[c["key"]]), e(c["short"]),
                 icon("arrow-right")))
    out.append("</div>")
    return "".join(out)


def why_us_grid(group):
    out = ['<div class="grid grid--4">']
    for ic, title, text in C.WHY_US:
        reg("why.%s.text" % re.sub(r"\W+", "-", title.lower()), "text", text, title, group)
        out.append(icon_card(ic, title, text))
    out.append("</div>")
    return "".join(out)


def testimonial_grid(items, group, cols=3):
    out = ['<div class="grid grid--%d">' % cols]
    for name, meta, initials, rating, quote in items:
        out.append("""<article class="quote-card reveal">
  %s
  <blockquote>%s</blockquote>
  <div class="quote-card__who">
    <span class="quote-card__avatar" aria-hidden="true">%s</span>
    <span><span class="quote-card__name">%s</span><span class="quote-card__meta">%s</span></span>
  </div>
</article>""" % (stars(rating), e(quote), e(initials), e(name), e(meta)))
    out.append("</div>")
    return "".join(out)


def model_grid(models, depth, group, cols=3, filterable=False):
    cls = "model-grid" if cols == 3 else "model-grid model-grid--4"
    out = ['<div class="%s" id="model-grid">' % cls]
    for m in models:
        card = model_card(m, depth, CH, group)
        if filterable:
            cat = "%s %s" % (m["channel"], m["body"])
            card = card.replace('<article class="model-card reveal"',
                                '<article class="model-card reveal" data-cat="%s"' % cat, 1)
        out.append(card)
    out.append("</div>")
    if filterable:
        out.append('<p class="filter-empty" hidden>No models match that filter. '
                   '<button type="button" class="filter-chip" data-filter="all">Show all</button></p>')
    return "".join(out)


PRICE_DISCLAIMER = (
    "Prices shown are indicative ex-showroom prices for the base variant and move "
    "with variant, colour and manufacturer revisions. The on-road price adds road "
    "tax, registration, insurance and any accessories. Ask us for a written on-road "
    "quotation before you book — ours does not change between the estimate and the "
    "invoice.")


def price_note():
    return '<div class="price-note">%s <strong>%s</strong></div>' % (
        icon("info"), e(PRICE_DISCLAIMER))


# ===========================================================================
#  PAGE BODIES
# ===========================================================================
def page_home(pg):
    g = "Home"
    d = 0
    hero_models = [C.MODEL_BY_KEY[k] for k in ("brezza", "swift", "grand-vitara",
                                               "ertiga", "fronx", "dzire")]
    return """
<section class="hero hero--photo">
  <div class="hero__media">%(heroimg)s</div>
  <div class="hero__scrim" aria-hidden="true"></div>
  <div class="container hero__inner">
    <div>
      <span class="eyebrow">Authorised Maruti Suzuki dealer &middot; Thanjavur</span>
      <h1 data-cms="home.hero.title">%(h1)s</h1>
      <p class="hero__lead" data-cms="home.hero.text">%(lead)s</p>
      <div class="hero__actions">
        %(b1)s
        %(b2)s
      </div>
      <div class="hero__badges">
        <span>%(i1)s ARENA and NEXA under one roof</span>
        <span>%(i2)s Maruti-trained workshop</span>
        <span>%(i3)s True Value certified pre-owned</span>
        <span>%(i4)s 17 models, hatchback to seven-seat SUV</span>
      </div>
    </div>

  </div>
</section>

<div class="container quick-strip">
  <div class="quick-strip__grid">
    <a href="test-drive.html">%(q1)s<span><strong>Book a test drive</strong><small>At the showroom or your home</small></span></a>
    <a href="service/book-service.html" data-channel="service">%(q2)s<span><strong>Book a service</strong><small>Free pick-up in the city</small></span></a>
    <a href="true-value/sell-your-car.html" data-channel="truevalue">%(q3)s<span><strong>Value your car</strong><small>Free written valuation</small></span></a>
    <a href="finance.html">%(q4)s<span><strong>Finance and EMI</strong><small>Nine lenders, one form</small></span></a>
  </div>
</div>

<section class="section" id="main">
  <div class="container">
    %(ch_head)s
    %(channels)s
  </div>
</section>

<section class="section section--smoke">
  <div class="container">
    %(m_head)s
    %(models)s
    <div class="center-actions">%(all_models)s</div>
    %(pnote)s
  </div>
</section>

<section class="section">
  <div class="container">
    %(w_head)s
    %(why)s
  </div>
</section>

<section class="section section--dark">
  <div class="container">
    %(s_head)s
    %(stats)s
  </div>
</section>

<section class="section">
  <div class="container">
    %(b_head)s
    <ol class="steps steps--3 steps--flow">%(steps)s</ol>
  </div>
</section>

<section class="section section--smoke">
  <div class="container">
    %(t_head)s
    %(tests)s
    <div class="center-actions">%(all_tests)s</div>
  </div>
</section>

<section class="section">
  <div class="container grid--split grid">
    <div>
      <span class="eyebrow">Ask us anything</span>
      <h2>Tell us what you need. We will tell you what it costs.</h2>
      <p>Not sure whether you want the hatchback or the compact SUV, whether CNG makes
         sense for your running, or what your current car is worth against it? That is
         the conversation, and it is free.</p>
      %(cl)s
      <div class="hero__actions" style="margin-top:26px">%(wa)s</div>
    </div>
    %(form)s
  </div>
</section>

<section class="section section--smoke">
  <div class="container">
    %(p_head)s
    <div class="grid grid--3">%(posts)s</div>
  </div>
</section>
""" % {
        "heroimg": P.cms_img("home.hero.photo", "assets/images/banners/home.jpg",
                             "Maruti Suzuki cars in the showroom", 1600, 672,
                             "Hero photograph", "Home", lazy=False),
        "h1": reg("home.hero.title", "rich",
                  "Every Maruti Suzuki you need, and everything after you buy it.",
                  "Hero heading", g),
        "lead": reg("home.hero.text", "text",
                    "Thirty years selling, servicing and standing behind Maruti Suzuki cars "
                    "in Thanjavur. New cars from ARENA and NEXA, certified pre-owned through "
                    "True Value, an authorised workshop, and the Maruti Driving School — all "
                    "at one address.",
                    "Hero text", g),
        "b1": btn("See all 17 models", "cars/index.html"),
        "b2": '<a class="btn btn--ghost" href="test-drive.html">Book a test drive %s</a>' % icon("steering"),
        "i1": icon("store"), "i2": icon("wrench"), "i3": icon("certificate"),
        "i4": icon("car"),
        "q1": icon("steering"), "q2": icon("wrench"), "q3": icon("exchange"), "q4": icon("rupee"),
        "ch_head": section_head("home.channels", "What we do",
                                "Five businesses, one address", g,
                                "Buying, owning and eventually replacing a car — we are set "
                                "up for the whole cycle, not just the sale."),
        "channels": channel_cards(d, g),
        "m_head": section_head("home.models", "The range", "Popular right now", g,
                               "Six of the seventeen models we sell. Prices are indicative "
                               "ex-showroom for the base variant."),
        "models": model_grid(hero_models, d, g),
        "all_models": btn("View the full range", "cars/index.html"),
        "pnote": price_note(),
        "w_head": section_head("home.why", "Why us", "What you get by buying here", g),
        "why": why_us_grid(g),
        "s_head": section_head("home.stats", "Since 1996",
                               "Three decades in Thanjavur", g),
        "stats": stat_row([(v, s, l) for v, s, l in C.HOME_STATS], g, "home.stats"),
        "b_head": section_head("home.buy", "How it works",
                               "Six steps from first question to keys", g),
        "steps": "".join(
            '<li class="steps__item reveal"><span class="steps__num">%02d</span>'
            '<div><h3>%s</h3><p>%s</p></div></li>' % (i, e(t), e(x))
            for i, (t, x) in enumerate(C.BUY_STEPS, start=1)),
        "t_head": section_head("home.tests", "Customer stories",
                               "What people say afterwards", g),
        "tests": testimonial_grid(C.TESTIMONIALS[:3], g),
        "all_tests": btn("Read more stories", "testimonials.html", "btn btn--outline"),
        "cl": checklist([
            "A written on-road quotation, itemised, that does not move",
            "Free valuation of your current car against the new one",
            "Finance from nine lenders compared side by side",
            "Delivery across Thanjavur district",
        ]),
        "wa": wa_button("Chat on WhatsApp", BIZ["whatsapp_greeting"]),
        "form": form_block("home-enquiry", "Send us an enquiry", enquiry_fields(),
                           intro="We reply the same working day."),
        "p_head": section_head("home.posts", "News and advice",
                               "Worth reading before you buy", g),
        "posts": "".join(post_card(p, 0) for p in C.POSTS),
    }


def post_card(post, depth):
    p = lambda h: P.rel(h, depth)
    return """<article class="post-card reveal">
  <span class="pill pill--muted">%s</span>
  <h3><a href="%s">%s</a></h3>
  <p>%s</p>
  <div class="article-meta"><span>%s %s</span><span>%s %s</span></div>
</article>""" % (e(post["tag"]), p("blog/" + post["slug"]), e(post["title"]),
                 e(post["excerpt"]), icon("calendar"), e(post["date_h"]),
                 icon("clock"), e(post["read"]))


# --------------------------------------------------------------------- cars
def page_cars_index(pg):
    g = "Cars"
    bodies = []
    for m in C.MODELS:
        if m["body"] not in bodies:
            bodies.append(m["body"])
    chips = ['<button type="button" class="filter-chip" data-filter="all" aria-pressed="true">All 17 models</button>',
             '<button type="button" class="filter-chip" data-filter="arena" aria-pressed="false">ARENA</button>',
             '<button type="button" class="filter-chip" data-filter="nexa" aria-pressed="false">NEXA</button>']
    for b in bodies:
        chips.append('<button type="button" class="filter-chip" data-filter="%s" aria-pressed="false">%s</button>'
                     % (b, e(body_label(b))))
    return """
<section class="section" id="main"><div class="container">
  %(head)s
  <div class="filter-bar" data-filter-target="#model-grid" role="group" aria-label="Filter models">%(chips)s</div>
  %(grid)s
  %(pnote)s
</div></section>
%(cta)s
""" % {
        "head": section_head("cars.head", "New cars",
                             "The full Maruti Suzuki range", g,
                             "Seventeen models across the ARENA and NEXA channels. "
                             "Filter by showroom or by body type.", align="left"),
        "chips": "".join(chips),
        "grid": model_grid(C.MODELS, 1, g, cols=3, filterable=True),
        "pnote": price_note(),
        "cta": cta_band("Not sure which one?",
                        "Tell us your budget, your monthly running and how many people "
                        "usually travel. We will shortlist two or three and arrange test drives.",
                        [btn("Book a test drive", "../test-drive.html"),
                         wa_button("Ask on WhatsApp", "Hello, please help me choose a Maruti Suzuki model.",
                                   "btn btn--ghost")],
                        g, "cars.cta"),
    }


def page_channel(pg):
    ch = CH[pg["channel_key"]]
    g = ch["short"]
    models = C.ARENA_MODELS if ch["key"] == "arena" else C.NEXA_MODELS
    return """
<section class="section" id="main"><div class="container">
  %(head)s
  <div class="grid grid--split grid" style="margin-bottom:52px">
    <div>
      <p class="lead">%(blurb)s</p>
      %(cl)s
    </div>
    <div class="channel-band__art" data-channel="%(colour)s" aria-hidden="true">%(art)s</div>
  </div>
  %(grid)s
  %(pnote)s
</div></section>
%(cta)s
""" % {
        "head": section_head("%s.head" % ch["key"], ch["tag"], pg["section_title"], g, align="left"),
        "blurb": e(ch["blurb"]),
        "cl": checklist(pg["points"]),
        "colour": ch["colour"],
        "art": P.car_photo(C.MODEL_BY_KEY[pg["art_model"]], 1, lazy=False),
        "grid": model_grid(models, 1, g),
        "pnote": price_note(),
        "cta": cta_band("See it in person",
                        "Every model here can be brought to your home or office for a test drive.",
                        [btn("Book a test drive", "../test-drive.html"),
                         btn("Talk to us", "../contact.html", "btn btn--ghost")],
                        g, "%s.cta" % ch["key"]),
    }


def page_model(pg):
    m = pg["model"]
    ch = CH[m["channel"]]
    g = "Cars"
    related = [x for x in C.MODELS if x["channel"] == m["channel"] and x["key"] != m["key"]][:3]
    key = "model." + m["key"]

    specs = [("users", "Seats", m["seats"]), ("fuel", "Fuel", m["fuel"]),
             ("gearbox", "Transmission", m["gearbox"]), ("gauge", "Mileage (ARAI)", m["mileage"]),
             ("cog", "Engine", m["engine"]), ("car", "Body type", body_label(m["body"]))]

    return """
<section class="model-hero" data-channel="%(colour)s" id="main"><div class="container model-hero__inner">
  <div>
    <div class="model-hero__meta">%(pill)s<span class="pill pill--muted">%(body)s</span></div>
    <h1>Maruti Suzuki %(name)s</h1>
    <p class="lead" data-cms="%(key)s.pitch">%(pitch)s</p>
    %(price)s
    <div class="model-hero__actions">
      <a class="btn" href="#enquire">Enquire about the %(name)s %(ar)s</a>
      <a class="btn btn--outline" href="../test-drive.html?model=%(slug)s">Book a test drive %(st)s</a>
    </div>
  </div>
  <div class="model-hero__art"><span data-cms-art="%(art_key)s" data-art-alt="Maruti Suzuki %(name)s">%(art)s</span></div>
</div></section>

<section class="section"><div class="container">
  <div class="grid grid--sidebar">
    <div>
      <h2>Specifications</h2>
      <ul class="spec-list">%(specs)s</ul>
      %(pnote)s

      <h2 class="mt-48">What stands out</h2>
      %(high)s

      <h2 class="mt-48">Owning it in Thanjavur</h2>
      <p>%(own1)s</p>
      <p>%(own2)s</p>
    </div>
    <aside class="sidebar">
      <div class="sidebar-card">
        <h3>At a glance</h3>
        <ul>
          <li><strong>Showroom:</strong> %(chname)s</li>
          <li><strong>Body type:</strong> %(body)s</li>
          <li><strong>Seats:</strong> %(seats)s</li>
          <li><strong>Fuel:</strong> %(fuel)s</li>
          <li><strong>Transmission:</strong> %(gearbox)s</li>
        </ul>
      </div>
      <div class="sidebar-card sidebar-card--dark">
        <h3>Prefer to just call?</h3>
        <p>Sales desk, Monday to Saturday.</p>
        <p><a class="btn btn--ghost btn--sm" href="tel:+%(cc)s%(phone)s" data-biz-href="tel">%(ph)s <span data-biz="phone_display">%(phone_display)s</span></a></p>
      </div>
      <div class="sidebar-card">
        <h3>Other %(chshort)s models</h3>
        <ul>%(rellinks)s</ul>
      </div>
    </aside>
  </div>
</div></section>

<section class="section section--smoke" id="enquire"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Enquire</span>
      <h2>Get a written on-road price for the %(name)s</h2>
      <p>Tell us the variant you are looking at, or leave it blank and we will send the
         full variant list with on-road prices for each. Either way the quotation is
         itemised and it does not change between the estimate and the invoice.</p>
      %(cl2)s
    </div>
    %(form)s
  </div>
</div></section>

<section class="section"><div class="container">
  %(rhead)s
  %(rgrid)s
</div></section>
""" % {
        "colour": ch["colour"], "pill": channel_pill(ch), "body": e(body_label(m["body"])),
        "name": e(m["name"]), "key": key,
        "pitch": reg(key + ".pitch", "text", m["pitch"], "%s — intro" % m["name"], g),
        "price": price_line(m, "price price--lg"),
        "ar": icon("arrow-right"), "st": icon("steering"),
        "slug": m["key"], "art": P.car_photo(m, 1, lazy=False),
        "art_key": P.art_slot(m, 1, g),
        "specs": "".join(
            '<li>%s<span><span class="spec-list__label">%s</span>'
            '<span class="spec-list__value">%s</span></span></li>' % (icon(ic), e(lbl), e(val))
            for ic, lbl, val in specs),
        "pnote": price_note(),
        "high": checklist(m["highlights"]),
        "own1": e("Every %s we sell is serviced by our own Maruti-trained technicians two "
                  "minutes from the showroom, on Maruti equipment, with genuine parts and "
                  "part numbers printed on your invoice." % m["name"]),
        "own2": e("Periodic maintenance follows the published Maruti Suzuki schedule, we "
                  "collect and drop within Thanjavur city limits at no charge, and nothing "
                  "is added to the job card without a phone call first."),
        "chname": e(ch["name"]), "chshort": e(ch["short"]),
        "seats": e(m["seats"]), "fuel": e(m["fuel"]), "gearbox": e(m["gearbox"]),
        "cc": BIZ["phone_country_code"], "phone": BIZ["phone"],
        "phone_display": e(BIZ["phone_display"]), "ph": icon("phone"),
        "rellinks": "".join('<li><a href="%s.html">%s</a></li>' % (x["key"], e(x["name"]))
                            for x in related),
        "cl2": checklist(["Ex-showroom, tax, registration, insurance and accessories, listed separately",
                          "Exchange value for your current car, if you have one",
                          "EMI options from nine lenders, compared on one sheet",
                          "The realistic delivery date, not the optimistic one"]),
        "form": form_block("model-enquiry-" + m["key"],
                           "Enquiry — Maruti Suzuki " + m["name"],
                           enquiry_fields(model_value=m["name"]),
                           hidden=[("model_page", m["name"], "Model")]),
        "rhead": section_head(key + ".related", "Also consider",
                              "Other %s models" % ch["short"], g, align="left"),
        "rgrid": model_grid(related, 1, g),
    }


# --------------------------------------------------------------- true value
def page_true_value(pg):
    g = "True Value"
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Certified pre-owned</span>
      <h2>A used car with a paper trail</h2>
      <p class="lead">Maruti Suzuki True Value exists because the pre-owned market has a
         trust problem. Every car we sell under it goes through a documented inspection,
         arrives with a clear title, and carries a warranty you can hold us to.</p>
      <p>We do not sell cars we would not put a family member in. If a car fails the
         inspection it goes to auction, not to the front of the yard with a polish.</p>
      <div class="hero__actions" style="margin-top:26px">
        %(b1)s %(b2)s
      </div>
    </div>
    <div class="channel-band__art" data-channel="truevalue">%(art)s</div>
  </div>
</div></section>

<section class="section section--smoke"><div class="container">
  %(ihead)s
  <div class="grid grid--2">
    <div>%(cl1)s</div>
    <div>%(cl2)s</div>
  </div>
  <div class="center-actions">%(b3)s</div>
</div></section>

<section class="section"><div class="container">
  %(shead)s
  <ol class="steps steps--4 steps--flow">%(steps)s</ol>
</div></section>

<section class="section section--smoke"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Buying or selling</span>
      <h2>Both directions, same yard</h2>
      <p>Most people arrive wanting to do both at once: sell what they have and drive
         away in something newer. That is one conversation, one valuation and one
         invoice, and the exchange figure reduces what you need to finance.</p>
      %(cl3)s
    </div>
    %(form)s
  </div>
</div></section>
""" % {
        "b1": btn("How we certify", "certification.html"),
        "b2": btn("Sell your car", "sell-your-car.html", "btn btn--outline"),
        "art": P.cms_img("tv.index.photo", "../assets/images/banners/tv-countless.jpg",
                         "Certified pre-owned cars at a Maruti Suzuki True Value outlet",
                         1100, 493, "True Value photograph", "True Value"),
        "ihead": section_head("tv.checks", "The inspection",
                              "What gets checked before a car is listed", g),
        "cl1": checklist(C.TRUE_VALUE_CHECKS[:4]),
        "cl2": checklist(C.TRUE_VALUE_CHECKS[4:]),
        "b3": btn("Read the full certification process", "certification.html", "btn btn--outline"),
        "shead": section_head("tv.steps", "Selling to us", "Four steps, about a week", g),
        "steps": "".join(
            '<li class="steps__item reveal"><span class="steps__num">%02d</span>'
            '<div><h3>%s</h3><p>%s</p></div></li>' % (i, e(t), e(x))
            for i, (t, x) in enumerate(C.TRUE_VALUE_STEPS, start=1)),
        "cl3": checklist(["Free valuation, in writing, valid for seven days",
                          "Any make or model — not only Maruti Suzuki",
                          "We handle the RC transfer and the paperwork",
                          "Payment before the car leaves your name"]),
        "form": form_block("tv-enquiry", "Get your car valued", [
            field("name", "Your name", required=True, extra="tv-name"),
            field("phone", "Phone", "tel", required=True, extra="tv-phone"),
            field("current_car", "Car to value", required=True,
                  placeholder="e.g. 2018 Swift VXi", extra="tv-car"),
            field("km_driven", "Kilometres driven", placeholder="e.g. 62,000", extra="tv-km"),
            field("message", "Anything we should know?", "textarea", extra="tv-msg"),
        ], submit="Send for valuation"),
    }


def page_tv_sell(pg):
    g = "True Value"
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--sidebar">
    <div>
      <h2>What your car is worth, in writing</h2>
      <p class="lead">A verbal figure is worth nothing when you get home and think about
         it. Ours comes on paper, it is valid for seven days, and it is the figure that
         appears on the invoice if you go ahead.</p>
      <p>We buy any make and any model, not only Maruti Suzuki. The valuation takes about
         forty minutes at our Thanjavur yard, covers the same inspection points we apply
         to cars we sell, and you leave with the number whether or not you sell to us.</p>

      <h2 class="mt-48">How the valuation works</h2>
      <ol class="steps steps--flow" style="grid-template-columns:1fr">%(steps)s</ol>

      <h2 class="mt-48">Bring these with you</h2>
      %(cl)s

      <div class="note-card mt-32" data-channel="truevalue">
        <h3>Selling against a new car?</h3>
        <p>Say so at the start. The exchange figure is set against the new car on the same
           invoice, which reduces the amount you finance and the interest you pay on it.</p>
      </div>
    </div>
    <aside class="sidebar">%(form)s</aside>
  </div>
</div></section>
""" % {
        "steps": "".join(
            '<li class="steps__item reveal"><span class="steps__num">%02d</span>'
            '<div><h3>%s</h3><p>%s</p></div></li>' % (i, e(t), e(x))
            for i, (t, x) in enumerate(C.TRUE_VALUE_STEPS, start=1)),
        "cl": checklist(["Registration certificate (RC)", "Valid insurance policy",
                         "Service history, if you have it", "PUC certificate",
                         "Both sets of keys", "Loan closure letter, if the car was financed"]),
        "form": form_block("sell-form", "Book a free valuation", [
            field("name", "Your name", required=True, extra="sell-name"),
            field("phone", "Phone", "tel", required=True, extra="sell-phone"),
            field("current_car", "Make and model", required=True, extra="sell-car"),
            field("year", "Year of purchase", placeholder="e.g. 2018", extra="sell-year"),
            field("km_driven", "Kilometres driven", extra="sell-km"),
            field("preferred_date", "Preferred date", "date", extra="sell-date"),
        ], submit="Book the valuation"),
    }


def page_tv_cert(pg):
    g = "True Value"
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--sidebar">
    <div>
      <h2>What certification actually means</h2>
      <p class="lead">"Certified" is a word that gets used loosely. Here is precisely
         what it means on a car in our yard, so you can compare it against whatever
         else you are being offered.</p>
      <p>Every True Value car passes a documented inspection covering the mechanical
         condition, the structure, the electricals and the paperwork. The report is
         yours to read before you buy, not after.</p>

      <h2 class="mt-48">The inspection points</h2>
      %(cl)s

      <h2 class="mt-48">The paperwork we verify</h2>
      %(cl2)s

      <h2 class="mt-48">What you get on delivery</h2>
      %(cl3)s

      <div class="note-card mt-32" data-channel="truevalue">
        <h3>If a car fails</h3>
        <p>It does not get listed. Cars that fail the inspection go to trade auction and
           are never sold to a retail customer from this yard. That is the point of the
           process — a certification that lets everything through certifies nothing.</p>
      </div>
    </div>
    <aside class="sidebar">
      <div class="sidebar-card">
        <h3>On this page</h3>
        <ul>
          <li><a href="index.html">Buy pre-owned</a></li>
          <li><a href="sell-your-car.html">Sell your car</a></li>
          <li><a href="../finance.html">Finance for pre-owned</a></li>
        </ul>
      </div>
      %(form)s
    </aside>
  </div>
</div></section>
""" % {
        "cl": checklist(C.TRUE_VALUE_CHECKS),
        "cl2": checklist(["Registration certificate and chassis number match",
                          "Single-owner or multi-owner history, stated plainly",
                          "Hypothecation cleared and recorded",
                          "Insurance status and claim history",
                          "No outstanding challans against the vehicle"]),
        "cl3": checklist(["The written inspection report",
                          "Warranty on engine and transmission",
                          "Free first service at our workshop",
                          "RC transfer handled by us, tracked to completion"]),
        "form": form_block("cert-form", "Ask about a car", [
            field("name", "Your name", required=True, extra="cert-name"),
            field("phone", "Phone", "tel", required=True, extra="cert-phone"),
            field("message", "Which car?", "textarea", extra="cert-msg"),
        ], submit="Send enquiry"),
    }


# ------------------------------------------------------------------ service
def page_service_index(pg):
    g = "Service"
    cards = []
    for s in C.SERVICES:
        cards.append("""<article class="icon-card reveal" data-channel="service">
  <span class="icon-card__icon">%s</span>
  <h3>%s</h3>
  <p>%s</p>
  <a class="link-more" href="%s.html">%s %s</a>
</article>""" % (icon(s["icon"]), e(s["name"]), e(s["blurb"]), s["key"],
                 e(s["lead"]), icon("arrow-right")))
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Authorised workshop</span>
      <h2>Servicing that keeps the warranty and the resale value intact</h2>
      <p class="lead">Maruti-trained technicians, Maruti equipment, Maruti Genuine Parts,
         and an estimate you approve before anything is touched.</p>
      <p>The complaint people bring us most often about other workshops is not the price.
         It is finding items on the bill that nobody mentioned. Our job card is digital,
         itemised and approved by you — and if we find something once the car is on the
         lift, we call you and wait.</p>
      <div class="hero__actions" style="margin-top:26px">%(b1)s %(b2)s</div>
    </div>
    <div class="channel-band__art" data-channel="service">%(art)s</div>
  </div>
</div></section>

<section class="section section--smoke"><div class="container">
  %(head)s
  <div class="grid grid--4">%(cards)s</div>
</div></section>

<section class="section"><div class="container">
  %(whead)s
  <div class="grid grid--4">%(why)s</div>
</div></section>

%(cta)s
""" % {
        "b1": btn("Book a service", "book-service.html"),
        "b2": '<a class="btn btn--outline" href="tel:+%s%s" data-biz-href="tel_service">%s Call the workshop</a>'
              % (BIZ["phone_country_code"], BIZ["phone_service"], icon("phone")),
        "art": P.cms_img("service.index.photo", "../assets/images/banners/svc-accessories.jpg",
                         "Maruti Genuine Parts and accessories", 1100, 560,
                         "Service photograph", "Service"),
        "head": section_head("service.head", "What we do", "Four workshops in one", g),
        "cards": "".join(cards),
        "whead": section_head("service.why", "How we work", "What is different here", g),
        "why": "".join([
            icon_card("clipboard", "Estimate first, always",
                      "You see and approve the figure before a spanner moves. Additions "
                      "need a phone call and a yes.", channel="service"),
            icon_card("truck", "Free pick-up and drop",
                      "Within Thanjavur city limits, at no charge. Tell us a window and "
                      "we work around it.", channel="service"),
            icon_card("certificate", "Genuine parts, part numbers printed",
                      "Maruti Genuine Parts only, with the numbers on your invoice so you "
                      "can verify them.", channel="service"),
            icon_card("screen", "Digital job card",
                      "You can see what was done, what it cost, and photographs of "
                      "anything we flagged.", channel="service"),
        ]),
        "cta": cta_band("Car due for a service?",
                        "Book online and we will confirm a slot the same day. Free pick-up "
                        "and drop within the city.",
                        [btn("Book a service", "book-service.html"),
                         wa_button("Ask the workshop", "Hello, I would like to book a service.",
                                   "btn btn--ghost")],
                        g, "service.cta"),
    }


def page_service_detail(pg):
    s = pg["service"]
    g = "Service"
    others = [x for x in C.SERVICES if x["key"] != s["key"]]
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--sidebar">
    <div>
      <h2>%(lead)s</h2>
      %(intro)s

      <h2 class="mt-48">What you get</h2>
      %(points)s

      <h2 class="mt-48">Common questions</h2>
      %(faqs)s
    </div>
    <aside class="sidebar">
      <div class="sidebar-card">
        <h3>Other workshop services</h3>
        <ul>%(others)s</ul>
      </div>
      %(form)s
      <div class="sidebar-card sidebar-card--dark">
        <h3>Workshop hours</h3>
        <p data-biz="service_hours">%(hours)s</p>
        <p><a class="btn btn--ghost btn--sm" href="tel:+%(cc)s%(sp)s" data-biz-href="tel_service">%(ph)s <span data-biz="phone_service_display">%(spd)s</span></a></p>
      </div>
    </aside>
  </div>
</div></section>
""" % {
        "lead": e(s["lead"]),
        "intro": "".join("<p>%s</p>" % e(x) for x in s["intro"]),
        "points": checklist(s["points"]),
        "faqs": accordion(s["faqs"], "service.%s.faq" % s["key"], g),
        "others": "".join('<li><a href="%s.html">%s</a></li>' % (x["key"], e(x["name"]))
                          for x in others),
        "form": form_block("svc-" + s["key"], "Book this service", [
            field("name", "Your name", required=True, extra="svc-name-" + s["key"]),
            field("phone", "Phone", "tel", required=True, extra="svc-phone-" + s["key"]),
            field("reg_no", "Registration number", placeholder="TN 49 ...",
                  extra="svc-reg-" + s["key"]),
            field("preferred_date", "Preferred date", "date", extra="svc-date-" + s["key"]),
            field("message", "Describe the problem", "textarea", extra="svc-msg-" + s["key"]),
        ], submit="Send booking request",
            hidden=[("service_type", s["name"], "Service")]),
        "hours": e(BIZ["service_hours"]),
        "cc": BIZ["phone_country_code"], "sp": BIZ["phone_service"],
        "spd": e(BIZ["phone_service_display"]), "ph": icon("phone"),
    }


def page_book_service(pg):
    g = "Service"
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Workshop booking</span>
      <h2>Book a slot in about a minute</h2>
      <p class="lead">Fill this in and it opens in WhatsApp with your details already
         written out. We confirm the slot the same working day.</p>
      %(cl)s
      <div class="note-card mt-32" data-channel="service">
        <h3>Free pick-up and drop</h3>
        <p>Within Thanjavur city limits, at no charge. Tick the box below and tell us a
           window that suits you — we will confirm the driver's time when we confirm
           the slot.</p>
      </div>
      <h2 class="mt-48">Before you bring the car in</h2>
      %(cl2)s
    </div>
    %(form)s
  </div>
</div></section>
""" % {
        "cl": checklist(["Estimate before work starts, approved by you",
                         "Maruti Genuine Parts with part numbers on the invoice",
                         "Digital job card and vehicle health report",
                         "Same-day delivery on standard periodic services"]),
        "cl2": checklist(["Remove valuables and personal documents",
                          "Tell us about noises even if they are intermittent",
                          "Bring the service booklet if you have it",
                          "Leave a number you will actually answer during the day"]),
        "form": form_block("book-service", "Book a service", [
            field("name", "Your name", required=True, extra="bs-name"),
            field("phone", "Phone", "tel", required=True, extra="bs-phone"),
            field("reg_no", "Registration number", required=True, placeholder="TN 49 ...",
                  extra="bs-reg"),
            field("model", "Model", "select", options=MODEL_NAMES + ["Other Maruti Suzuki model"],
                  extra="bs-model"),
            field("service_type", "Type of service", "select",
                  options=[s["name"] for s in C.SERVICES] + ["Not sure — please advise"],
                  required=True, extra="bs-type"),
            field("preferred_date", "Preferred date", "date", required=True, extra="bs-date"),
            field("message", "Describe the problem", "textarea",
                  placeholder="Noises, warning lights, anything unusual", extra="bs-msg"),
            field("pickup", "I would like free pick-up and drop within Thanjavur city",
                  "checkbox", extra="bs-pickup"),
        ], submit="Send booking request"),
    }


# ----------------------------------------------------------- driving school
def page_driving_school(pg):
    g = "Driving School"
    cards = []
    for c in C.DRIVING_COURSES:
        # Excluded items are shown rather than hidden — a course that lists what
        # it does *not* cover is easier to choose between than one that doesn't.
        rows = "".join(
            '<li%s>%s<span>%s</span><span class="sr-only">%s</span></li>'
            % ("" if ok else ' class="is-off"',
               icon("check-square") if ok else icon("close"), e(t),
               "included" if ok else "not included")
            for t, ok in c["includes"])
        cards.append("""<article class="icon-card reveal" data-channel="school">
  <div class="model-card__top">
    <span class="pill pill--channel">%s</span>
    <span class="model-card__body-type">%s</span>
  </div>
  <h3>%s</h3>
  <p class="price"><span class="price__value">&#8377;%s</span> <span class="price__note">%s</span></p>
  <p>%s</p>
  <ul class="checklist" style="margin-top:6px">%s</ul>
  <a class="btn btn--channel btn--sm" href="#enrol">Enrol in %s %s</a>
</article>""" % (e(c["name"]), e(c["duration"]), e(c["name"] + " course"),
                 e(c["price"]), e(c["sessions"]), e("For: " + c["for"]), rows,
                 e(c["name"]), icon("arrow-right")))
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Maruti Driving School</span>
      <h2>Learn properly, not just enough to pass</h2>
      <p class="lead">Dual-control cars, certified instructors, simulator sessions and a
         syllabus that covers highway behaviour, night driving and what to do when
         something goes wrong — not only the test route.</p>
      <p>The licence is the easy part. Confidence in traffic on a Thanjavur market
         morning is the part that takes real teaching, and that is what we are set up
         to give you.</p>
      <div class="hero__actions" style="margin-top:26px">%(b1)s %(b2)s</div>
    </div>
    <div class="channel-band__art" data-channel="school">%(art)s</div>
  </div>
</div></section>

<section class="section section--smoke"><div class="container">
  %(chead)s
  <div class="grid grid--3">%(cards)s</div>
  <p class="form-note text-center mt-32">Course fees include the training car and fuel.
     Government fees for the learner's licence and the driving licence test are paid
     directly to the RTO and are not included.</p>
</div></section>

<section class="section"><div class="container">
  %(whead)s
  <div class="grid grid--4">%(why)s</div>
</div></section>

<section class="section section--smoke" id="enrol"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Enrol</span>
      <h2>Start with a phone call</h2>
      <p>Tell us which course suits you and we will confirm the next available batch,
         the timings, and exactly what the RTO fees will come to.</p>
      %(cl)s
    </div>
    %(form)s
  </div>
</div></section>
""" % {
        "b1": '<a class="btn btn--channel" href="#enrol">Enrol now %s</a>' % icon("arrow-right"),
        "b2": btn("Talk to us", "contact.html", "btn btn--outline"),
        "art": P.cms_img("school.photo", "assets/images/banners/ds-learning.jpg",
                         "Learning to drive at the Maruti Driving School", 1100, 227,
                         "Driving school photograph", "Driving School"),
        "chead": section_head("school.courses", "Courses", "Three courses, one syllabus", g),
        "cards": "".join(cards),
        "whead": section_head("school.why", "How we teach", "What a session looks like", g),
        "why": "".join([
            icon_card("steering", "Dual-control cars",
                      "The instructor has a second brake and clutch. Nothing you do in "
                      "the first week can go badly wrong.", channel="school"),
            icon_card("screen", "Simulator first",
                      "Clutch control, gear changes and hazard response practised before "
                      "you are in live traffic.", channel="school"),
            icon_card("road", "Real roads, real conditions",
                      "Market streets, the bypass, night driving and rain — the "
                      "situations that actually make people nervous.", channel="school"),
            icon_card("clipboard", "Licence paperwork handled",
                      "We help with the learner's licence application and prepare you for "
                      "the RTO test.", channel="school"),
        ]),
        "cl": checklist(["Batches start every fortnight",
                         "Morning, afternoon and evening timings",
                         "Female instructors available on request",
                         "Refresher sessions for licensed drivers who have not driven in years"]),
        "form": form_block("school-form", "Enrol at the driving school", [
            field("name", "Your name", required=True, extra="ds-name"),
            field("phone", "Phone", "tel", required=True, extra="ds-phone"),
            field("course", "Course", "select",
                  options=[c["name"] for c in C.DRIVING_COURSES] + ["Not sure — please advise"],
                  required=True, extra="ds-course"),
            field("preferred_time", "Preferred timing", "select",
                  options=["Morning", "Afternoon", "Evening"], extra="ds-time"),
            field("message", "Anything we should know?", "textarea", extra="ds-msg"),
        ], submit="Send enrolment enquiry"),
    }


# -------------------------------------------------------------------- about
def page_about(pg):
    g = "About"
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--sidebar">
    <div>
      <h2>Thirty years, one address, one family</h2>
      <p class="lead">Pillai &amp; Sons Motor Company has been selling and servicing Maruti
         Suzuki cars in Thanjavur since the mid-nineties. The business is still run by the
         family whose name is on the board.</p>
      <p>That matters more than it sounds. A dealership is a long relationship: you buy a
         car once and then come back for servicing, for parts, for the next car and often
         for your children's first car. We are still here to be found if something goes
         wrong, and the person who signed off your price is usually in the building.</p>

      <h2 class="mt-48">What we grew into</h2>
      <p>We started with a single ARENA showroom. Today the same address carries the NEXA
         premium range, a True Value pre-owned yard, an authorised workshop with a body
         and paint shop, and the Maruti Driving School. Five businesses, because a car
         owner needs all five and should not have to drive to five different towns.</p>

      <h2 class="mt-48">How we price</h2>
      <p>One thing we do differently, and it is the thing customers mention most: the
         written quotation does not change. Ex-showroom, road tax, registration, insurance
         and accessories are listed as separate lines on day one. If a line moves, it is
         because a government rate moved, and we show you the notification.</p>

      <div class="note-card mt-32">
        <h3>Authorised, and what that means</h3>
        <p data-biz="dealer_disclaimer">%(disc)s</p>
      </div>
    </div>
    <aside class="sidebar">
      <div class="sidebar-card">
        <h3>More about us</h3>
        <ul>
          <li><a href="why-us.html">Why choose us</a></li>
          <li><a href="team.html">Our team</a></li>
          <li><a href="testimonials.html">Customer stories</a></li>
          <li><a href="careers.html">Careers</a></li>
          <li><a href="locations.html">Find us</a></li>
        </ul>
      </div>
      <div class="sidebar-card sidebar-card--dark">
        <h3>Visit the showroom</h3>
        <p data-biz="address_block">%(addr)s</p>
        <p><a class="btn btn--ghost btn--sm" href="#" data-biz-href="map" target="_blank" rel="noopener">%(pin)s Get directions</a></p>
      </div>
    </aside>
  </div>
</div></section>

<section class="section section--dark"><div class="container">
  %(shead)s
  %(stats)s
</div></section>

<section class="section"><div class="container">
  %(whead)s
  %(why)s
</div></section>

%(cta)s
""" % {
        "disc": e(BIZ["dealer_disclaimer"]),
        "addr": e(", ".join(filter(None, [BIZ["address_line1"], BIZ["address_line2"],
                                          BIZ["city"] + " - " + BIZ["pincode"], BIZ["state"]]))),
        "pin": icon("map-pin"),
        "shead": section_head("about.stats", "By the numbers", "Where we are today", g),
        "stats": stat_row(list(C.HOME_STATS), g, "about.stats"),
        "whead": section_head("about.why", "Why us", "What you get by buying here", g),
        "why": why_us_grid(g),
        "cta": cta_band("Come and see for yourself",
                        "The showroom is on Medical College Road. No appointment needed, "
                        "and nobody will follow you around the floor.",
                        [btn("Get directions", "locations.html"),
                         btn("Book a test drive", "test-drive.html", "btn btn--ghost")],
                        g, "about.cta"),
    }


def page_why_us(pg):
    g = "About"
    return """
<section class="section" id="main"><div class="container">
  %(head)s
  %(why)s
</div></section>

<section class="section section--smoke"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">The pricing promise</span>
      <h2>The quotation you get on day one is the invoice you sign</h2>
      <p>Almost every complaint about car buying comes down to the same thing: the number
         moved. Here is how we stop that happening.</p>
      %(cl)s
    </div>
    <div>
      <div class="note-card">
        <h3>What is in a written on-road quotation</h3>
        <p>Ex-showroom price &middot; TN road tax &middot; registration and RTO charges
           &middot; insurance (own damage and third party, shown separately)
           &middot; extended warranty, if you choose it &middot; accessories, itemised
           &middot; logistics and handling. Nothing else appears later.</p>
      </div>
      <div class="note-card mt-32">
        <h3>What we cannot control</h3>
        <p>Road tax and registration are government charges calculated on the ex-showroom
           price. No dealer can discount them, and anyone offering to is either absorbing
           it elsewhere on the invoice or is not telling you the truth.</p>
      </div>
    </div>
  </div>
</div></section>

<section class="section"><div class="container">
  %(bhead)s
  <ol class="steps steps--3 steps--flow">%(steps)s</ol>
</div></section>

<section class="section section--smoke"><div class="container">
  %(thead)s
  %(tests)s
</div></section>

%(cta)s
""" % {
        "head": section_head("why.head", "Why choose us",
                             "Four reasons people drive past two other dealers to get here", g),
        "why": why_us_grid(g),
        "cl": checklist([
            "Every charge is a separate line, written down, on the first visit",
            "Accessories are optional and priced individually — never a compulsory bundle",
            "Insurance is quoted from multiple insurers, and you may bring your own",
            "Any deviation from a quoted price needs the Managing Director's signature",
            "The delivery date we give you is the realistic one",
        ]),
        "bhead": section_head("why.steps", "How it works",
                              "Six steps from first question to keys", g),
        "steps": "".join(
            '<li class="steps__item reveal"><span class="steps__num">%02d</span>'
            '<div><h3>%s</h3><p>%s</p></div></li>' % (i, e(t), e(x))
            for i, (t, x) in enumerate(C.BUY_STEPS, start=1)),
        "thead": section_head("why.tests", "In their words", "Customers on the difference", g),
        "tests": testimonial_grid(C.TESTIMONIALS[:3], g),
        "cta": cta_band("Get a written quotation",
                        "Tell us the model and variant. We will send the full on-road "
                        "breakdown, itemised, with nothing hidden in a bundle.",
                        [btn("Send an enquiry", "contact.html"),
                         wa_button("Ask on WhatsApp", "Hello, I would like a written on-road quotation.",
                                   "btn btn--ghost")],
                        g, "why.cta"),
    }


def page_team(pg):
    g = "About"
    cards = "".join("""<article class="team-card reveal">
  <span class="team-card__avatar" aria-hidden="true">%s</span>
  <h3>%s</h3>
  <span class="team-card__role">%s</span>
  <p>%s</p>
</article>""" % (e(ini), e(name), e(role), e(bio)) for name, role, ini, bio in C.TEAM)
    return """
<section class="section" id="main"><div class="container">
  %(head)s
  <div class="grid grid--3">%(cards)s</div>
</div></section>

<section class="section section--smoke"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Working here</span>
      <h2>We hire for temperament, then train for product</h2>
      <p>Product knowledge is teachable in six weeks. Patience with a customer who is
         asking the same question for the third time is not. We hire for the second and
         train the first, which is why our sales floor turns over far less than the
         industry average.</p>
      %(cl)s
      <div class="hero__actions" style="margin-top:26px">%(b)s</div>
    </div>
    <div class="note-card">
      <h3>Photographs</h3>
      <p>We have used initials rather than stock photographs of people who do not work
         here. Real team photographs can be uploaded from the admin panel and will appear
         in place of the initials.</p>
    </div>
  </div>
</div></section>
""" % {
        "head": section_head("team.head", "Our team",
                             "The people you will actually deal with", g,
                             "Small floor, long service. Most of the names below have "
                             "been here more than a decade."),
        "cards": cards,
        "cl": checklist(["Average tenure on the sales floor: over eight years",
                         "Every technician Maruti-trained and certified",
                         "Instructors at the driving school hold RTO-recognised certification",
                         "Nobody here is paid a commission that depends on selling you accessories"]),
        "b": btn("See open positions", "careers.html"),
    }


def page_testimonials(pg):
    g = "About"
    return """
<section class="section" id="main"><div class="container">
  %(head)s
  %(tests)s
</div></section>

<section class="section section--smoke"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Reviews</span>
      <h2>Where these come from</h2>
      <p>These are drawn from customers who bought or serviced with us and agreed to be
         quoted. We have not edited them into advertising copy, and we have not removed
         the ones that mention what went wrong before it was put right.</p>
      <p>If you have bought from us and would like to add yours — good or bad — send it
         through and we will publish it as written.</p>
      <div class="hero__actions" style="margin-top:26px">%(wa)s</div>
    </div>
    %(form)s
  </div>
</div></section>

%(cta)s
""" % {
        "head": section_head("tests.head", "Customer stories",
                             "What people say afterwards", g,
                             "The test of a dealership is not the day you buy. It is the "
                             "third service, two years later."),
        "tests": testimonial_grid(C.TESTIMONIALS, g),
        "wa": wa_button("Send yours on WhatsApp", "Hello, I would like to share my experience."),
        "form": form_block("review-form", "Share your experience", [
            field("name", "Your name", required=True, extra="rev-name"),
            field("phone", "Phone", "tel", extra="rev-phone"),
            field("model", "Car you bought or serviced", "select",
                  options=MODEL_NAMES + ["Other"], extra="rev-model"),
            field("message", "Your experience", "textarea", required=True, extra="rev-msg"),
        ], submit="Send your review"),
        "cta": cta_band("Ready to talk to us?",
                        "Book a test drive, or just come in and ask questions. Neither "
                        "commits you to anything.",
                        [btn("Book a test drive", "test-drive.html"),
                         btn("Contact us", "contact.html", "btn btn--ghost")],
                        g, "tests.cta"),
    }


def page_careers(pg):
    g = "Careers"
    cards = "".join("""<article class="job-card reveal">
  <div>
    <h3>%s</h3>
    <div class="job-card__meta">
      <span>%s %s</span><span>%s %s</span><span>%s %s</span>
    </div>
    <p>%s</p>
  </div>
  <a class="btn btn--outline btn--sm" href="#apply">Apply %s</a>
</article>""" % (e(title), icon("map-pin"), e(loc), icon("clock"), e(kind),
                 icon("briefcase"), e(exp), e(desc), icon("arrow-right"))
                    for title, loc, kind, exp, desc in C.JOBS)
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Careers</span>
      <h2>Work somewhere people stay</h2>
      <p class="lead">Six open positions across the showroom, the workshop and the driving
         school. Product training is provided; what we cannot train is patience and
         straight dealing.</p>
      %(cl)s
    </div>
    <div class="note-card">
      <h3>How we hire</h3>
      <p>One conversation with the department head, one with the Managing Director, and
         a day on the floor so you can see what the job actually is before you accept it.
         We tell you the salary band in the first conversation.</p>
    </div>
  </div>
</div></section>

<section class="section section--smoke"><div class="container">
  %(head)s
  <div class="stack">%(cards)s</div>
</div></section>

<section class="section" id="apply"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Apply</span>
      <h2>Send us your details</h2>
      <p>Tell us which role you are interested in and roughly what you have done before.
         We read everything that comes in and reply either way.</p>
      %(cl2)s
    </div>
    %(form)s
  </div>
</div></section>
""" % {
        "cl": checklist(["Provident fund and ESI from day one",
                         "Maruti Suzuki training programmes, fully paid",
                         "Sunday off for workshop staff on a rota",
                         "Internal promotion first — three of our department heads started on the floor"]),
        "head": section_head("careers.head", "Open positions", "Six roles open now", g),
        "cards": cards,
        "cl2": checklist(["We reply to every application, including the unsuccessful ones",
                          "Freshers considered for sales and driving school roles",
                          "Walk-ins welcome on weekday afternoons"]),
        "form": form_block("careers-form", "Job application", [
            field("name", "Your name", required=True, extra="job-name"),
            field("phone", "Phone", "tel", required=True, extra="job-phone"),
            field("email", "Email", "email", extra="job-email"),
            field("role", "Applying for", "select",
                  options=[j[0] for j in C.JOBS] + ["Something else"], required=True,
                  extra="job-role"),
            field("experience", "Years of experience", "select",
                  options=["Fresher", "1-3 years", "3-5 years", "5-10 years", "10+ years"],
                  extra="job-exp"),
            field("message", "Tell us about yourself", "textarea", required=True, extra="job-msg"),
        ], submit="Send application"),
    }


# ------------------------------------------------------------------- offers
def page_offers(pg):
    g = "Offers"
    cards = "".join(icon_card(ic, title, text) for title, ic, text in C.OFFER_KINDS)
    return """
<section class="section" id="main"><div class="container">
  %(head)s
  <div class="grid grid--4">%(cards)s</div>
  <div class="price-note mt-32">%(info)s <strong>Offers change every month and vary by
    model, variant and stock position. Rather than publish a figure that is stale by the
    time you read it, we will tell you exactly what is live on the model you want, on the
    day you ask.</strong></div>
</div></section>

<section class="section section--smoke"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">This month</span>
      <h2>Ask what is running right now</h2>
      <p>Consumer offers come from Maruti Suzuki and change monthly. Exchange bonuses,
         corporate discounts and rural offers stack differently depending on the model
         and the variant, and some cannot be combined.</p>
      <p>Send us the model you are looking at and we will come back with everything you
         qualify for, in writing, with the conditions attached to each.</p>
      %(cl)s
    </div>
    %(form)s
  </div>
</div></section>

%(cta)s
""" % {
        "head": section_head("offers.head", "Offers",
                             "Four kinds of benefit, and how they stack", g,
                             "Most buyers qualify for more than one. Here is what exists "
                             "and what the conditions actually are."),
        "cards": cards, "info": icon("info"),
        "cl": checklist(["Exchange bonus applies to any make, not only Maruti Suzuki",
                         "Corporate offer needs an employee ID or salary slip",
                         "Rural offer needs proof of a rural address",
                         "Some offers cannot be combined — we will tell you which"]),
        "form": form_block("offers-form", "What offers apply to me?", enquiry_fields(),
                           submit="Ask about offers"),
        "cta": cta_band("Finance changes the maths",
                        "A larger exchange value reduces the loan, which reduces the "
                        "interest. Often that is worth more than the discount.",
                        [btn("See finance options", "finance.html"),
                         btn("Value your car", "true-value/sell-your-car.html", "btn btn--ghost")],
                        g, "offers.cta"),
    }


def page_finance(pg):
    g = "Finance"
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--sidebar">
    <div>
      <h2>Finance and insurance, compared on one sheet</h2>
      <p class="lead">We work with nine lenders. You see all of them side by side — rate,
         tenure, processing fee, foreclosure terms — and choose. We are not paid more to
         push one of them.</p>

      <h2 class="mt-48">What affects your rate</h2>
      %(cl)s

      <h2 class="mt-48">What you will need</h2>
      <div class="grid grid--2">
        <div>
          <h3>Salaried</h3>
          %(cl2)s
        </div>
        <div>
          <h3>Self-employed</h3>
          %(cl3)s
        </div>
      </div>

      <h2 class="mt-48">Insurance</h2>
      <p>Third-party cover is compulsory by law. Own-damage cover is not, but skipping it
         on a new car is a bad trade — and any lender financing the car will require it.
         We quote from several insurers and you are free to bring your own policy.</p>
      %(cl4)s

      <h2 class="mt-48">Common questions</h2>
      %(faq)s
    </div>
    <aside class="sidebar">
      %(form)s
      <div class="sidebar-card">
        <h3>Related</h3>
        <ul>
          <li><a href="offers.html">Current offers</a></li>
          <li><a href="true-value/sell-your-car.html">Value your current car</a></li>
          <li><a href="cars/index.html">Browse the range</a></li>
        </ul>
      </div>
    </aside>
  </div>
</div></section>
""" % {
        "cl": checklist(["Your credit score — check it before you apply, not after",
                         "The down payment: more down usually means a lower rate",
                         "Tenure: a longer loan lowers the EMI and raises the total interest",
                         "Whether the car is new or pre-owned",
                         "Existing relationship with the lender"]),
        "cl2": checklist(["Aadhaar and PAN", "Three months of salary slips",
                          "Six months of bank statements", "Form 16 or the latest return"]),
        "cl3": checklist(["Aadhaar and PAN", "Two years of income tax returns",
                          "Twelve months of bank statements", "Business registration proof"]),
        "cl4": checklist(["Own damage and third party quoted separately, never bundled",
                          "Zero-depreciation add-on explained rather than assumed",
                          "You may bring your own policy — it will not affect your price",
                          "Claims support through our body shop, which is cashless with most insurers"]),
        "faq": accordion([
            ("Can I get finance approved before choosing a car?",
             "Yes, and it is the better order. A pre-approval tells you your real budget "
             "including the on-road price, so you are choosing a car you can actually "
             "drive away rather than one you can nearly afford."),
            ("Do you charge for arranging finance?",
             "No. The lender pays a standard commission and it does not change your rate. "
             "We show you every offer we receive, including the ones that pay us less."),
            ("Can I foreclose the loan early?",
             "Terms vary by lender. Some allow it free after twelve EMIs, others charge a "
             "percentage of the outstanding. It is on the comparison sheet — read that "
             "column before you sign, not after."),
            ("Is finance available on True Value cars?",
             "Yes, though rates are typically higher than on a new car and the maximum "
             "tenure is shorter. We will show you both so you can compare properly."),
        ], "finance.faq", g),
        "form": form_block("finance-form", "Check your EMI options", [
            field("name", "Your name", required=True, extra="fin-name"),
            field("phone", "Phone", "tel", required=True, extra="fin-phone"),
            field("model", "Model", "select", options=MODEL_NAMES, extra="fin-model"),
            field("budget", "Comfortable monthly EMI", "select",
                  options=["Under 10,000", "10,000 - 15,000", "15,000 - 25,000",
                           "25,000 - 40,000", "Above 40,000"], extra="fin-emi"),
            field("message", "Anything else?", "textarea", extra="fin-msg"),
        ], submit="Send finance enquiry"),
    }


def page_faqs(pg):
    g = "FAQs"
    cats = "".join(icon_card(ic, name, blurb) for name, ic, blurb in C.FAQ_CATEGORIES)
    groups = []
    for i, (title, items) in enumerate(C.FAQ_GROUPS):
        groups.append('<h2 class="mt-48">%s</h2>%s'
                      % (e(title), accordion(items, "faq.%d" % i, g, open_first=(i == 0))))
    return """
<section class="section" id="main"><div class="container">
  %(head)s
  <div class="grid grid--4">%(cats)s</div>
</div></section>

<section class="section section--smoke"><div class="container">
  <div class="grid grid--sidebar">
    <div class="article-body">%(groups)s</div>
    <aside class="sidebar">
      <div class="sidebar-card sidebar-card--dark">
        <h3>Question not here?</h3>
        <p>Send it over. We answer the same working day, and if it is a good question we
           add it to this page.</p>
        <p>%(wa)s</p>
      </div>
      <div class="sidebar-card">
        <h3>Useful pages</h3>
        <ul>
          <li><a href="finance.html">Finance and insurance</a></li>
          <li><a href="service/index.html">Servicing</a></li>
          <li><a href="true-value/certification.html">True Value certification</a></li>
          <li><a href="contact.html">Contact us</a></li>
        </ul>
      </div>
    </aside>
  </div>
</div></section>
""" % {
        "head": section_head("faq.head", "FAQs", "The questions we actually get asked", g,
                             "Grouped by what you are trying to do."),
        "cats": cats,
        "groups": "".join(groups),
        "wa": wa_button("Ask on WhatsApp", "Hello, I have a question:", "btn btn--ghost btn--sm"),
    }


# --------------------------------------------------------------------- blog
def page_blog(pg):
    g = "Blog"
    return """
<section class="section" id="main"><div class="container">
  %(head)s
  <div class="grid grid--3">%(posts)s</div>
</div></section>

%(cta)s
""" % {
        "head": section_head("blog.head", "News and advice",
                             "Things worth knowing before you sign", g,
                             "Written by the people who deal with these questions every "
                             "day, not by a marketing agency."),
        "posts": "".join(post_card(p, 0) for p in C.POSTS),
        "cta": cta_band("Have a question we have not covered?",
                        "Send it in. If it is something several people are asking, it "
                        "becomes the next article.",
                        [btn("Contact us", "contact.html"),
                         wa_button("Ask on WhatsApp", "Hello, I have a question:", "btn btn--ghost")],
                        g, "blog.cta"),
    }


def page_post(pg):
    post = pg["post"]
    g = "Blog"
    body = []
    for kind, text in post["body"]:
        if kind == "p":
            body.append("<p>%s</p>" % e(text))
        elif kind == "h2":
            body.append("<h2>%s</h2>" % e(text))
        elif kind == "h3":
            body.append("<h3>%s</h3>" % e(text))
        elif kind == "ul":
            body.append("<ul>%s</ul>" % "".join("<li>%s</li>" % e(x) for x in text))
        elif kind == "quote":
            body.append("<blockquote>%s</blockquote>" % e(text))
    others = [x for x in C.POSTS if x["key"] != post["key"]]
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--sidebar">
    <article class="article-body">
      <div class="article-meta">
        <span>%(cal)s %(date)s</span><span>%(clk)s %(read)s</span><span class="pill pill--muted">%(tag)s</span>
      </div>
      %(body)s
      <div class="note-card mt-48">
        <h3>Want this applied to a specific car?</h3>
        <p>Send us the model and variant and we will put the actual numbers against it,
           in writing, with every line itemised.</p>
        <p class="mt-32">%(wa)s</p>
      </div>
    </article>
    <aside class="sidebar">
      <div class="sidebar-card">
        <h3>More reading</h3>
        <ul>%(others)s</ul>
      </div>
      <div class="sidebar-card">
        <h3>Useful pages</h3>
        <ul>
          <li><a href="../cars/index.html">All 17 models</a></li>
          <li><a href="../finance.html">Finance and insurance</a></li>
          <li><a href="../faqs.html">FAQs</a></li>
        </ul>
      </div>
    </aside>
  </div>
</div></section>
""" % {
        "cal": icon("calendar"), "date": e(post["date_h"]),
        "clk": icon("clock"), "read": e(post["read"]), "tag": e(post["tag"]),
        "body": "".join(body),
        "wa": wa_button("Ask on WhatsApp", "Hello, I read your article and have a question:"),
        "others": "".join('<li><a href="%s">%s</a></li>' % (x["slug"], e(x["title"]))
                          for x in others),
    }


# ------------------------------------------------------------------ contact
def page_contact(pg):
    g = "Contact"
    return """
<section class="section" id="main"><div class="container">
  <div class="contact-grid">
    <div>
      <span class="eyebrow">Get in touch</span>
      <h2>Two numbers, because there are two kinds of call</h2>
      <p>One for buying a car, one for the workshop. Both are answered by a person during
         opening hours, and neither of them is a call centre.</p>
      <ul class="contact-list">
        <li>
          <span class="contact-list__icon">%(pin)s</span>
          <div><h3>Showroom and workshop</h3><p data-biz="address_block">%(addr)s</p></div>
        </li>
        <li>
          <span class="contact-list__icon">%(ph)s</span>
          <div><h3>Sales</h3><p><a href="tel:+%(cc)s%(phone)s" data-biz-href="tel"><span data-biz="phone_display">%(phd)s</span></a></p></div>
        </li>
        <li>
          <span class="contact-list__icon">%(wr)s</span>
          <div><h3>Service</h3><p><a href="tel:+%(cc)s%(sphone)s" data-biz-href="tel_service"><span data-biz="phone_service_display">%(sphd)s</span></a></p></div>
        </li>
        <li>
          <span class="contact-list__icon">%(ml)s</span>
          <div><h3>Email</h3><p><a href="mailto:%(email)s" data-biz-href="mail"><span data-biz="email">%(email)s</span></a></p></div>
        </li>
        <li>
          <span class="contact-list__icon">%(cl)s</span>
          <div><h3>Opening hours</h3>
            <p><span data-biz="business_hours">%(hours)s</span><br>
               <span data-biz="business_hours_sun">%(hsun)s</span><br>
               Workshop: <span data-biz="service_hours">%(shours)s</span></p></div>
        </li>
      </ul>
      <div class="hero__actions" style="margin-top:28px">%(wa)s %(dir)s</div>
    </div>
    %(form)s
  </div>
</div></section>

<section class="section section--smoke"><div class="container">
  %(mhead)s
  %(map)s
</div></section>
""" % {
        "pin": icon("map-pin"), "ph": icon("phone"), "wr": icon("wrench"),
        "ml": icon("mail"), "cl": icon("clock"),
        "addr": e(", ".join(filter(None, [BIZ["address_line1"], BIZ["address_line2"],
                                          BIZ["city"] + " - " + BIZ["pincode"], BIZ["state"]]))),
        "cc": BIZ["phone_country_code"], "phone": BIZ["phone"], "phd": e(BIZ["phone_display"]),
        "sphone": BIZ["phone_service"], "sphd": e(BIZ["phone_service_display"]),
        "email": e(BIZ["email"]),
        "hours": e(BIZ["business_hours"]), "hsun": e(BIZ["business_hours_sun"]),
        "shours": e(BIZ["service_hours"]),
        "wa": wa_button("Chat on WhatsApp", BIZ["whatsapp_greeting"]),
        "dir": '<a class="btn btn--outline" href="#" data-biz-href="map" target="_blank" rel="noopener">%s Get directions</a>' % icon("map-pin"),
        "form": form_block("contact-form", "Send us a message", enquiry_fields()),
        "mhead": section_head("contact.map", "Find us", "Medical College Road, Thanjavur", g),
        "map": map_embed(0),
    }


def page_test_drive(pg):
    g = "Contact"
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--split grid">
    <div>
      <span class="eyebrow">Test drive</span>
      <h2>At the showroom, or at your door</h2>
      <p class="lead">Every model we sell can be brought to your home or office anywhere
         in Thanjavur city, and to most of the district by arrangement. No charge, and no
         obligation at the end of it.</p>
      %(cl)s

      <h2 class="mt-48">Bring your licence</h2>
      <p>A valid driving licence is required by law and by the insurer — no licence, no
         drive, however far you have come. If someone else in the family will be the main
         driver, bring them and their licence too. It is their opinion that matters.</p>

      <div class="note-card mt-32">
        <h3>What to actually test</h3>
        <p>Reversing into a real parking space, the boot with your pram or your luggage in
           it, the rear seat with the front seat set where you drive it, and a rough road.
           Ten minutes on a smooth bypass tells you almost nothing.</p>
      </div>
    </div>
    %(form)s
  </div>
</div></section>

<section class="section section--smoke"><div class="container">
  %(head)s
  %(grid)s
  <div class="center-actions">%(all)s</div>
</div></section>
""" % {
        "cl": checklist(["Home or office test drives across Thanjavur city",
                         "Both ARENA and NEXA models available",
                         "Weekend slots, booked in advance",
                         "No pressure to sit down with a salesperson afterwards"]),
        "form": form_block("test-drive-form", "Book a test drive", [
            field("name", "Your name", required=True, extra="td-name"),
            field("phone", "Phone", "tel", required=True, extra="td-phone"),
            field("model", "Model", "select", options=MODEL_NAMES, required=True, extra="td-model"),
            field("city", "Where?", "select", options=CITY_LIST, extra="td-city"),
            field("preferred_date", "Preferred date", "date", required=True, extra="td-date"),
            field("preferred_time", "Preferred time", "select",
                  options=["Morning", "Afternoon", "Evening"], extra="td-time"),
            field("message", "Anything else?", "textarea", extra="td-msg"),
        ], submit="Request a test drive"),
        "head": section_head("td.models", "Popular choices",
                             "Six people ask for these most often", g),
        "grid": model_grid([C.MODEL_BY_KEY[k] for k in
                            ("swift", "brezza", "ertiga", "fronx", "grand-vitara", "baleno")],
                           0, g),
        "all": btn("See all 17 models", "cars/index.html", "btn btn--outline"),
    }


def page_locations(pg):
    g = "Contact"
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--sidebar">
    <div>
      <h2>One address, five businesses</h2>
      <p class="lead">The ARENA showroom, the NEXA lounge, the True Value yard, the
         workshop and the driving school are all at the same Medical College Road
         address in Thanjavur.</p>
      <p>That is deliberate. A car owner should not have to drive across town to service
         what they bought, or to a different district to have a pre-owned car valued.</p>

      <h2 class="mt-48">Getting here</h2>
      %(cl)s

      <h2 class="mt-48">Areas we cover</h2>
      <p>We deliver and register across Thanjavur district and the surrounding towns —
         Kumbakonam, Pattukkottai, Orathanadu, Papanasam, Thiruvaiyaru and Peravurani
         among them. Registration can be arranged for your home RTO rather than ours.</p>

      %(map)s
    </div>
    <aside class="sidebar">
      <div class="sidebar-card">
        <h3>Address</h3>
        <p data-biz="address_block">%(addr)s</p>
        <p class="mt-32">%(dir)s</p>
      </div>
      <div class="sidebar-card">
        <h3>Hours</h3>
        <ul>
          <li><strong>Showroom:</strong> <span data-biz="business_hours">%(hours)s</span></li>
          <li><span data-biz="business_hours_sun">%(hsun)s</span></li>
          <li><strong>Workshop:</strong> <span data-biz="service_hours">%(shours)s</span></li>
        </ul>
      </div>
      <div class="sidebar-card sidebar-card--dark">
        <h3>Call ahead</h3>
        <p>Especially if you want a specific model ready for a test drive.</p>
        <p><a class="btn btn--ghost btn--sm" href="tel:+%(cc)s%(phone)s" data-biz-href="tel">%(ph)s <span data-biz="phone_display">%(phd)s</span></a></p>
      </div>
    </aside>
  </div>
</div></section>
""" % {
        "cl": checklist(["On Medical College Road, near Rajjappa Nagar",
                         "About ten minutes from Thanjavur Junction railway station",
                         "Customer parking on site",
                         "Wheelchair-accessible showroom entrance"]),
        "map": map_embed(0),
        "addr": e(", ".join(filter(None, [BIZ["address_line1"], BIZ["address_line2"],
                                          BIZ["city"] + " - " + BIZ["pincode"], BIZ["state"]]))),
        "dir": '<a class="btn btn--sm" href="#" data-biz-href="map" target="_blank" rel="noopener">%s Get directions</a>' % icon("map-pin"),
        "hours": e(BIZ["business_hours"]), "hsun": e(BIZ["business_hours_sun"]),
        "shours": e(BIZ["service_hours"]),
        "cc": BIZ["phone_country_code"], "phone": BIZ["phone"], "phd": e(BIZ["phone_display"]),
        "ph": icon("phone"),
    }


# ------------------------------------------------------------------- legal
# The text itself lives in tools/gen_legal.py, transcribed from the client's
# Word documents. Only the rendering lives here.

def _linkify(text):
    """Turn bare URLs, email addresses and phone numbers into real links.

    The source documents were written for print, so a reader on the site would
    otherwise be looking at a web address they cannot click."""
    out = e(text)
    out = re.sub(r"(https?://[^\s,)]+[^\s.,)])",
                 lambda m: '<a href="%s">%s</a>' % (m.group(1), m.group(1)), out)
    out = re.sub(r"\b([\w.+-]+@[\w-]+\.[\w.]+)\b",
                 lambda m: '<a href="mailto:%s" data-biz-href="mail">%s</a>'
                           % (m.group(1), m.group(1)), out)
    return out


def render_legal(blocks):
    out = []
    for kind, val in blocks:
        if kind == "meta":
            out.append('<p class="muted legal-updated"><strong>%s</strong></p>' % e(val))
        elif kind == "h2":
            out.append("<h2>%s</h2>" % e(val))
        elif kind == "h3":
            out.append("<h3>%s</h3>" % e(val))
        elif kind == "dl":
            rows = "".join("<dt>%s</dt><dd>%s</dd>" % (e(t), _linkify(b)) for t, b in val)
            out.append('<dl class="legal-defs">%s</dl>' % rows)
        else:
            out.append("<p>%s</p>" % _linkify(val))
    return "".join(out)


def page_legal(pg):
    return """
<section class="section" id="main"><div class="container">
  <div class="grid grid--sidebar">
    <div class="legal-body">
      %(body)s
    </div>
    <aside class="sidebar">
      <div class="sidebar-card">
        <h3>Legal</h3>
        <ul>
          <li><a href="privacy-policy.html">Privacy Policy</a></li>
          <li><a href="terms-conditions.html">Terms &amp; Conditions</a></li>
          <li><a href="contact.html">Contact us</a></li>
        </ul>
      </div>
      <div class="sidebar-card sidebar-card--dark">
        <h3>Questions about this?</h3>
        <p>Write to us and a person will answer, not a template.</p>
        <p><a class="btn btn--ghost btn--sm" href="mailto:%(email)s" data-biz-href="mail">%(ml)s Email us</a></p>
      </div>
    </aside>
  </div>
</div></section>
""" % {
        "body": render_legal(pg["blocks"]),
        "email": esc(BIZ["email"]), "ml": icon("mail"),
    }


def page_404(pg):
    return """
<section class="section text-center" id="main"><div class="container">
  <span class="eyebrow" style="justify-content:center">Error 404</span>
  <h1>That page has moved on</h1>
  <p class="lead">The link you followed does not exist any more — or never did. Nothing
     is broken on your side.</p>
  <div class="center-actions">
    %(b1)s %(b2)s %(b3)s
  </div>
  <h2 class="mt-48">Where you might have been going</h2>
  <div class="grid grid--4">%(cards)s</div>
</div></section>
""" % {
        "b1": btn("Back to the home page", "index.html"),
        "b2": btn("See all 17 models", "cars/index.html", "btn btn--outline"),
        "b3": btn("Contact us", "contact.html", "btn btn--outline"),
        "cards": "".join([
            icon_card("car", "New cars", "The full ARENA and NEXA range with indicative prices."),
            icon_card("exchange", "True Value", "Certified pre-owned cars, and free valuations."),
            icon_card("wrench", "Service", "Book a workshop slot with free pick-up and drop."),
            icon_card("steering", "Driving School", "Three courses on dual-control cars."),
        ]),
    }


# ===========================================================================
#  PAGE TABLE
# ===========================================================================
def add(key, href, title, description, nav_title, banner_heading, banner_text,
        render, group="General", **extra):
    pg = {
        "key": key, "href": href, "title": title, "description": description,
        "nav_title": nav_title, "banner_heading": banner_heading,
        "banner_text": banner_text, "render": render, "group": group,
    }
    pg.update(extra)
    PAGES.append(pg)
    return pg


def build_page_table():
    T = " | " + NAME

    # ---- home -------------------------------------------------------------
    add("home", "index.html",
        "Maruti Suzuki Dealer in Thanjavur — ARENA, NEXA, True Value, Service" + T,
        "Authorised Maruti Suzuki dealer in Thanjavur: ARENA and NEXA new cars, True "
        "Value pre-owned, an authorised workshop and the Maruti Driving School. "
        "Call +91 89397 52872.",
        "Home", "", "", page_home, "Home", no_banner=True)

    # ---- cars -------------------------------------------------------------
    add("cars", "cars/index.html", "All Maruti Suzuki Models and Prices" + T,
        "Every Maruti Suzuki model we sell in Thanjavur, across ARENA and NEXA, with "
        "indicative ex-showroom prices, seating, fuel and transmission options.",
        "All Models", "All 17 Maruti Suzuki models",
        "Filter by showroom or body type. Prices are indicative ex-showroom for the "
        "base variant.", page_cars_index, "Cars", banner_image="cars", banner_alt='The Maruti Suzuki ARENA showroom frontage at dusk',
        banner_eyebrow="New cars",
        breadcrumb=[("Home", "index.html"), ("Cars", None)])

    add("arena", "cars/arena.html", "Maruti Suzuki ARENA Cars in Thanjavur" + T,
        "The Maruti Suzuki ARENA range at Pillai & Sons, Thanjavur — hatchbacks, sedans, "
        "SUVs, MPVs and vans with indicative ex-showroom prices.",
        "ARENA", "Maruti Suzuki ARENA",
        "The everyday range: ten models built for Indian roads and Indian running costs.",
        page_channel, "ARENA", banner_image="arena", banner_alt='A Maruti Suzuki ARENA showroom lit up in the evening',
        channel="arena", channel_key="arena", art_model="swift",
        section_title="Ten models, hatchback to seven-seat MPV",
        banner_eyebrow="New cars",
        points=["Ten models from the S-Presso to the Ertiga",
                "Factory-fitted S-CNG on most of the range",
                "The widest service network in the country",
                "Lowest running costs in almost every segment"],
        breadcrumb=[("Home", "index.html"), ("Cars", "cars/index.html"), ("ARENA", None)])

    add("nexa", "cars/nexa.html", "NEXA Cars in Thanjavur — Baleno, Fronx, Grand Vitara" + T,
        "The NEXA premium range at Pillai & Sons, Thanjavur — Baleno, Fronx, Jimny, "
        "Grand Vitara, Invicto, XL6 and e Vitara with indicative ex-showroom prices.",
        "NEXA", "NEXA",
        "Maruti Suzuki's premium channel: a quieter showroom and a different class of car.",
        page_channel, "NEXA", banner_image="nexa", banner_alt='NEXA cars lined up inside a NEXA showroom',
        channel="nexa", channel_key="nexa", art_model="grand-vitara",
        section_title="Seven models, and a different way of buying",
        banner_eyebrow="Premium cars",
        points=["Seven models including the Grand Vitara and Jimny",
                "Strong hybrid and turbo-petrol options",
                "Relationship manager assigned from first visit to delivery",
                "Separate NEXA service bays"],
        breadcrumb=[("Home", "index.html"), ("Cars", "cars/index.html"), ("NEXA", None)])

    for m in C.MODELS:
        ch = CH[m["channel"]]
        add("model-" + m["key"], "cars/%s.html" % m["key"],
            "Maruti Suzuki %s Price in Thanjavur, Mileage and Specs%s" % (m["name"], T),
            "Maruti Suzuki %s in Thanjavur from Rs %s ex-showroom. %s seats, %s, %s. "
            "Written on-road quotation and a test drive at your door."
            % (m["name"], m["price"], m["seats"], m["fuel"].split(",")[0].strip(),
               m["mileage"]),
            m["name"], "", "", page_model, "Cars",
            model=m, channel=ch["colour"], no_banner=True,
            car_ld={"name": m["name"], "body": body_label(m["body"]), "seats": m["seats"],
                    "fuel": m["fuel"], "gearbox": m["gearbox"],
                    "price_num": m["price"].replace(",", "")},
            breadcrumb=[("Home", "index.html"), ("Cars", "cars/index.html"),
                        (ch["short"], "cars/%s.html" % ch["key"]), (m["name"], None)])

    # ---- true value -------------------------------------------------------
    add("true-value", "true-value/index.html",
        "True Value Certified Pre-Owned Cars in Thanjavur" + T,
        "Maruti Suzuki True Value at Pillai & Sons, Thanjavur. Certified pre-owned cars "
        "with a documented inspection, a clear title and a warranty. Free valuations.",
        "Buy Pre-Owned", "Maruti Suzuki True Value",
        "Certified pre-owned cars with a documented inspection, a clear title and a "
        "warranty you can hold us to.",
        page_true_value, "True Value", banner_image="true-value", banner_alt='Rows of certified pre-owned cars at a Maruti Suzuki True Value outlet',
        channel="truevalue", banner_eyebrow="Pre-owned",
        breadcrumb=[("Home", "index.html"), ("True Value", None)])

    add("tv-sell", "true-value/sell-your-car.html",
        "Sell Your Car in Thanjavur — Free Valuation" + T,
        "Sell any make or model at Pillai & Sons True Value, Thanjavur. Free written "
        "valuation valid for seven days, RC transfer handled, payment before transfer.",
        "Sell Your Car", "Sell your car",
        "Any make, any model. A free written valuation that is valid for seven days.",
        page_tv_sell, "True Value", banner_image="tv-sell", banner_alt='A Maruti Suzuki True Value outlet where cars are valued',
        channel="truevalue", banner_eyebrow="True Value",
        breadcrumb=[("Home", "index.html"), ("True Value", "true-value/index.html"),
                    ("Sell Your Car", None)])

    add("tv-cert", "true-value/certification.html",
        "How True Value Certification Works" + T,
        "What Maruti Suzuki True Value certification actually covers at Pillai & Sons, "
        "Thanjavur: the inspection points, the paperwork we verify and what you get on "
        "delivery.",
        "How We Certify", "How we certify a car",
        "“Certified” is a word used loosely. Here is exactly what it means here.",
        page_tv_cert, "True Value", banner_image="tv-cert", banner_alt='A technician inspecting the engine bay of a used car',
        channel="truevalue", banner_eyebrow="True Value",
        breadcrumb=[("Home", "index.html"), ("True Value", "true-value/index.html"),
                    ("How We Certify", None)])

    # ---- service ----------------------------------------------------------
    add("service", "service/index.html",
        "Maruti Suzuki Service Centre in Thanjavur" + T,
        "Authorised Maruti Suzuki workshop in Thanjavur. Periodic maintenance, body and "
        "paint, genuine parts and extended warranty. Free pick-up and drop in the city.",
        "Service Overview", "Maruti Suzuki Service",
        "An authorised workshop: Maruti-trained technicians, genuine parts, and an "
        "estimate you approve before anything is touched.",
        page_service_index, "Service", banner_image="service", banner_alt='A Maruti-trained technician working under the bonnet',
        channel="service", banner_eyebrow="Workshop",
        breadcrumb=[("Home", "index.html"), ("Service", None)])

    add("book-service", "service/book-service.html",
        "Book a Car Service in Thanjavur" + T,
        "Book a Maruti Suzuki service slot at Pillai & Sons, Thanjavur. Free pick-up and "
        "drop within the city, estimate before work starts, same-day delivery on "
        "standard services.",
        "Book a Service", "Book a service",
        "Tell us the car and the date. We confirm the slot the same working day.",
        page_book_service, "Service", banner_image="book-service", banner_alt='The customer lounge at a Maruti Suzuki service centre',
        channel="service", banner_eyebrow="Workshop",
        breadcrumb=[("Home", "index.html"), ("Service", "service/index.html"),
                    ("Book a Service", None)])

    for s in C.SERVICES:
        add("service-" + s["key"], "service/%s.html" % s["key"],
            "%s — Maruti Suzuki Workshop, Thanjavur%s" % (s["name"], T),
            s["blurb"],
            s["name"], s["name"], s["blurb"], page_service_detail, "Service",
            service=s, channel="service", banner_eyebrow="Workshop",
            banner_image=s["key"],
            banner_alt="%s at an authorised Maruti Suzuki workshop" % s["name"],
            faq_ld=s["faqs"],
            breadcrumb=[("Home", "index.html"), ("Service", "service/index.html"),
                        (s["name"], None)])

    # ---- driving school ---------------------------------------------------
    add("driving-school", "driving-school.html",
        "Maruti Driving School in Thanjavur — Courses and Fees" + T,
        "Learn to drive at the Maruti Driving School, Thanjavur. Dual-control cars, "
        "certified instructors, simulator sessions and licence assistance. Three courses "
        "from Rs 6,500.",
        "Driving School", "Maruti Driving School",
        "Dual-control cars, certified instructors and a syllabus that covers more than "
        "passing the test.",
        page_driving_school, "Driving School", banner_image="driving-school", banner_alt='A Maruti Driving School branch with a dual-control training car',
        channel="school", banner_eyebrow="Learn to drive",
        breadcrumb=[("Home", "index.html"), ("Driving School", None)])

    # ---- about ------------------------------------------------------------
    add("about", "about.html", "About Pillai & Sons Motor Company, Thanjavur" + T,
        "Thirty years selling and servicing Maruti Suzuki cars in Thanjavur. A family "
        "business running ARENA, NEXA, True Value, a workshop and the driving school.",
        "About Us", "About Pillai &amp; Sons",
        "Thirty years, one address, and the family whose name is on the board still "
        "running it.",
        page_about, "About", banner_image="about", banner_alt='Colleagues putting their hands together',
        banner_eyebrow="About us",
        breadcrumb=[("Home", "index.html"), ("About", None)])

    add("why-us", "why-us.html", "Why Buy From Pillai & Sons, Thanjavur" + T,
        "Written on-road quotations that do not change, free valuations, finance compared "
        "across nine lenders and an authorised workshop two minutes away.",
        "Why Choose Us", "Why choose us",
        "Four reasons people drive past two other dealers to get here.",
        page_why_us, "About", banner_image="why-us", banner_alt='A customer being handed the keys to a new Maruti Suzuki',
        banner_eyebrow="About us",
        breadcrumb=[("Home", "index.html"), ("About", "about.html"), ("Why Choose Us", None)])

    add("team", "team.html", "Our Team" + T,
        "The people you will actually deal with at Pillai & Sons Motor Company, "
        "Thanjavur — sales, workshop, True Value and the driving school.",
        "Our Team", "Our team",
        "Small floor, long service. Most of these names have been here more than a decade.",
        page_team, "About", banner_image="team", banner_alt='A sales advisor going through paperwork with two customers',
        banner_eyebrow="About us",
        breadcrumb=[("Home", "index.html"), ("About", "about.html"), ("Our Team", None)])

    add("testimonials", "testimonials.html", "Customer Stories and Reviews" + T,
        "What customers say about buying and servicing with Pillai & Sons Motor Company "
        "in Thanjavur, published as written.",
        "Customer Stories", "Customer stories",
        "The test of a dealership is not the day you buy. It is the third service, two "
        "years later.",
        page_testimonials, "About", banner_image="testimonials", banner_alt='Three cars outside a Maruti Suzuki True Value outlet',
        banner_eyebrow="Reviews",
        breadcrumb=[("Home", "index.html"), ("About", "about.html"),
                    ("Customer Stories", None)])

    add("careers", "careers.html", "Careers — Jobs at Pillai & Sons, Thanjavur" + T,
        "Six open positions across the showroom, the workshop and the driving school at "
        "Pillai & Sons Motor Company, Thanjavur. Training provided, PF and ESI from day one.",
        "Careers", "Careers",
        "Six open positions across the showroom, the workshop and the driving school.",
        page_careers, "Careers", banner_image="careers", banner_alt='An open road at sunrise',
        banner_eyebrow="Join us",
        breadcrumb=[("Home", "index.html"), ("About", "about.html"), ("Careers", None)])

    # ---- offers / finance / faq / blog ------------------------------------
    add("offers", "offers.html", "Current Offers on Maruti Suzuki Cars, Thanjavur" + T,
        "Exchange bonus, corporate and fleet benefit, rural offer and finance schemes at "
        "Pillai & Sons, Thanjavur. Ask what is live on your model this month.",
        "Offers", "Offers and benefits",
        "Most buyers qualify for more than one. Here is what exists and what the "
        "conditions actually are.",
        page_offers, "Offers",
        banner_eyebrow="This month",
        breadcrumb=[("Home", "index.html"), ("Offers", None)])

    add("finance", "finance.html", "Car Finance and Insurance in Thanjavur" + T,
        "Car loans compared across nine lenders, and insurance quoted from several "
        "insurers, at Pillai & Sons Motor Company, Thanjavur. No fee for arranging finance.",
        "Finance and Insurance", "Finance and insurance",
        "Nine lenders, compared on one sheet. We are not paid more to push one of them.",
        page_finance, "Finance", banner_image="finance", banner_alt='A car insurance document and a calculator',
        banner_eyebrow="Paying for it",
        breadcrumb=[("Home", "index.html"), ("Finance", None)])

    add("faqs", "faqs.html", "Frequently Asked Questions" + T,
        "Buying, finance, servicing and pre-owned questions answered plainly by Pillai "
        "& Sons Motor Company, the authorised Maruti Suzuki dealer in Thanjavur.",
        "FAQs", "Frequently asked questions",
        "Grouped by what you are actually trying to do.",
        page_faqs, "FAQs",
        banner_eyebrow="Answers",
        faq_ld=[qa for _, items in C.FAQ_GROUPS for qa in items],
        breadcrumb=[("Home", "index.html"), ("FAQs", None)])

    add("blog", "blog.html", "News and Advice" + T,
        "Straight advice on on-road prices, CNG running costs and choosing between "
        "variants, from Pillai & Sons Motor Company, Thanjavur.",
        "News and Advice", "News and advice",
        "Written by the people who deal with these questions every day.",
        page_blog, "Blog", banner_image="blog", banner_alt='Traffic on an Indian road beneath speed cameras',
        banner_eyebrow="Reading",
        breadcrumb=[("Home", "index.html"), ("News and Advice", None)])

    for post in C.POSTS:
        add("post-" + post["key"], "blog/" + post["slug"],
            post["title"] + T, post["excerpt"],
            post["title"], e(post["title"]), post["excerpt"], page_post, "Blog",
            post=post, banner_eyebrow=post["tag"], og_type="article",
            article_ld={"headline": post["title"], "date": post["date"]},
            breadcrumb=[("Home", "index.html"), ("News and Advice", "blog.html"),
                        (post["title"], None)])

    # ---- contact ----------------------------------------------------------
    add("contact", "contact.html", "Contact Pillai & Sons Motor Company, Thanjavur" + T,
        "Call, WhatsApp, email or visit Pillai & Sons Motor Company at 31-A, Medical "
        "College Road, Thanjavur. Separate numbers for sales and for the workshop.",
        "Contact Us", "Contact us",
        "Two numbers, because there are two kinds of call. Both answered by a person.",
        page_contact, "Contact", banner_image="contact", banner_alt='New Maruti Suzuki cars on a showroom floor',
        banner_eyebrow="Get in touch",
        breadcrumb=[("Home", "index.html"), ("Contact", None)])

    add("test-drive", "test-drive.html", "Book a Test Drive in Thanjavur" + T,
        "Book a Maruti Suzuki test drive at the showroom or at your home anywhere in "
        "Thanjavur. Free, and with no obligation.",
        "Book a Test Drive", "Book a test drive",
        "At the showroom, or at your door. No charge, and no obligation at the end of it.",
        page_test_drive, "Contact",
        banner_eyebrow="Try before you buy",
        breadcrumb=[("Home", "index.html"), ("Contact", "contact.html"),
                    ("Book a Test Drive", None)])

    add("locations", "locations.html", "Find Us — Medical College Road, Thanjavur" + T,
        "Directions, opening hours and the areas we cover from 31-A, Medical College "
        "Road, Rajjappa Nagar, Thanjavur 613007.",
        "Find Us", "Find us",
        "One address on Medical College Road carries all five businesses.",
        page_locations, "Contact",
        banner_eyebrow="Visit",
        breadcrumb=[("Home", "index.html"), ("Contact", "contact.html"), ("Find Us", None)])

    # ---- legal ------------------------------------------------------------
    add("privacy", "privacy-policy.html",
        "Privacy Policy, Disclaimer and Terms of Usage" + T,
        "How Pillai & Sons Motor Company collects and uses information from visitors to "
        "this website, together with the copyright, trademark and liability terms that "
        "apply to it.",
        "Privacy Policy", "Privacy Policy, Disclaimer &amp; Terms of Usage",
        "How we handle information collected during your visits to this website, and the "
        "legal terms that go with it.",
        page_legal, "Legal", blocks=L.PRIVACY, banner_eyebrow="Legal",
        breadcrumb=[("Home", "index.html"), ("Privacy Policy", None)])

    add("terms", "terms-conditions.html", "Terms and Conditions" + T,
        "The terms and conditions governing use of the Pillai & Sons Motor Company "
        "website: definitions, acknowledgment, liability, governing law and how these "
        "terms may change.",
        "Terms and Conditions", "Terms and Conditions",
        "Please read these terms and conditions carefully before using our service.",
        page_legal, "Legal", blocks=L.TERMS, banner_eyebrow="Legal",
        breadcrumb=[("Home", "index.html"), ("Terms and Conditions", None)])

    # ---- 404 --------------------------------------------------------------
    add("notfound", "404.html", "Page not found" + T,
        "That page does not exist on the Pillai & Sons Motor Company website. Here are "
        "the links back to new cars, True Value, the workshop and the driving school.",
        "Page not found", "Page not found", "That link has moved on.",
        page_404, "General", robots="noindex, follow", no_banner=True, no_sitemap=True)


# ===========================================================================
#  WRITE
# ===========================================================================
def depth_of(href):
    return href.count("/")


def build():
    check_required()
    build_page_table()

    base = P.site_base_path()

    # Bake the <base> into the markup only once site_url has actually been set.
    # A baked-in base that is wrong is worse than none at all: the preload
    # scanner follows it, every asset 404s, and only then does the script fix it.
    # While site_url is still the placeholder we cannot know the answer, so the
    # script works it out at runtime instead. tools/deploy.sh writes the real
    # URL and regenerates, so a deployed site always gets the fast path.
    configured = "example.github.io" not in P.SITE_URL and P.SITE_URL.startswith("http")
    static_base = ('<base href=%s data-auto>\n' % json.dumps(base)) if configured else ""
    shim = BASE_SHIM % (static_base, json.dumps(base))

    written = []
    for pg in PAGES:
        depth = depth_of(pg["href"])
        pg["head_first"] = shim if pg["key"] == "notfound" else ""

        parts = [P.build_head(pg, depth), P.build_topbar(),
                 P.build_header(depth, pg["href"])]

        # Everything from the banner down lives inside <main>, and <main> carries
        # the skip-link target. Page bodies are written with id="main" on their
        # first section (it reads naturally when you are writing them); it is
        # stripped here so there is exactly one #main, and so the page banner is
        # not stranded outside a landmark.
        inner = []
        if not pg.get("no_banner"):
            inner.append(P.build_banner(pg, depth, pg["group"]))
        inner.append(pg["render"](pg).replace(' id="main"', "", 1))
        parts.append('<main id="main">' + "".join(inner) + "</main>")
        parts.append(P.build_footer(depth))

        out = "\n".join(parts)
        path = os.path.join(ROOT, pg["href"])
        os.makedirs(os.path.dirname(path) or ROOT, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(out)
        written.append((pg["href"], len(out)))

    write_content_js()
    write_sitemap()
    write_robots()
    open(os.path.join(ROOT, ".nojekyll"), "w").close()

    total = sum(n for _, n in written)
    print("%d pages, %.1f KB of HTML" % (len(written), total / 1024.0))
    print("%d editable content entries" % len(P.REGISTRY))
    return written


def write_content_js():
    """Emit the editable-content manifest the admin panel reads.

    Shape is {groups: [{name, fields: [{k, t, l, v}]}]} — grouped, because the
    editor renders one collapsible section per group and a flat list of 289
    fields would be unusable.
    """
    path = os.path.join(ROOT, "assets", "js", "content.js")

    order, by_group = [], {}
    for item in P.REGISTRY:
        g = item["g"]
        if g not in by_group:
            by_group[g] = []
            order.append(g)
        by_group[g].append({"k": item["k"], "t": item["t"],
                            "l": item["l"], "v": item["v"]})

    payload = {"groups": [{"name": g, "fields": by_group[g]} for g in order]}
    body = json.dumps(payload, ensure_ascii=False, indent=1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("/* content.js  —  V1\n"
                 " * GENERATED FILE — do not edit by hand.\n"
                 " * Source: tools/gen_content.py + tools/generate_site.py\n"
                 " * Rebuild: python3 tools/generate_site.py\n"
                 " *\n"
                 " * The catalogue of every editable string and image on the site.\n"
                 " * admin/index.html reads it to build the editing forms; main.js\n"
                 " * reads the saved overrides rather than this file.\n"
                 " */\n")
        fh.write("window.SITE_CONTENT = %s;\n" % body)
        fh.write("window.SITE_CONTENT_OVERRIDES = window.SITE_CONTENT_OVERRIDES || {};\n")


def write_sitemap():
    site = P.SITE_URL
    urls = []
    for pg in PAGES:
        if pg.get("no_sitemap"):
            continue
        loc = site + "/" + pg["href"]
        pr = "1.0" if pg["key"] == "home" else ("0.8" if pg["href"].count("/") == 0 else "0.7")
        freq = "weekly" if pg["key"] in ("home", "offers", "cars") else "monthly"
        urls.append("  <url>\n    <loc>%s</loc>\n    <changefreq>%s</changefreq>\n"
                    "    <priority>%s</priority>\n  </url>" % (esc(loc), freq, pr))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(urls) + "\n</urlset>\n")
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(xml)


def write_robots():
    txt = ("User-agent: *\n"
           "Allow: /\n"
           "Disallow: /admin/\n"
           "\n"
           "Sitemap: %s/sitemap.xml\n" % P.SITE_URL)
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt)


if __name__ == "__main__":
    build()
