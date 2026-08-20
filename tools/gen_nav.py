"""
gen_nav.py  —  V1
Single source of truth for the navigation tree and the footer columns.

Hrefs are site-root-relative (no leading slash). generate_site.py rewrites them
per page depth so every internal link stays relative — required for GitHub Pages
project sites served from /reponame/.

Edit this file, re-run  python3 tools/generate_site.py,  and the menu updates on
every page at once.
"""
import gen_content as C

_ARENA = [{"label": m["name"], "href": "cars/%s.html" % m["key"]}
          for m in C.ARENA_MODELS]
_NEXA = [{"label": m["name"], "href": "cars/%s.html" % m["key"]}
         for m in C.NEXA_MODELS]

NAV = [
    {"label": "Home", "href": "index.html"},

    {"label": "About", "href": "about.html", "children": [
        {"label": "About Us",         "href": "about.html"},
        {"label": "Why Choose Us",    "href": "why-us.html"},
        {"label": "Our Team",         "href": "team.html"},
        {"label": "Customer Stories", "href": "testimonials.html"},
        {"label": "Careers",          "href": "careers.html"},
    ]},

    {"label": "Cars", "href": "cars/index.html", "children": [
        {"label": "All Models", "href": "cars/index.html"},
        {"label": "ARENA", "href": "cars/arena.html", "children": _ARENA},
        {"label": "NEXA",  "href": "cars/nexa.html",  "children": _NEXA},
    ]},

    {"label": "True Value", "href": "true-value/index.html", "children": [
        {"label": "Buy Pre-Owned",  "href": "true-value/index.html"},
        {"label": "Sell Your Car",  "href": "true-value/sell-your-car.html"},
        {"label": "How We Certify", "href": "true-value/certification.html"},
    ]},

    {"label": "Service", "href": "service/index.html", "children": [
        {"label": "Service Overview",      "href": "service/index.html"},
        {"label": "Book a Service",        "href": "service/book-service.html"},
        {"label": "Periodic Maintenance",  "href": "service/periodic-maintenance.html"},
        {"label": "Body Shop",             "href": "service/body-shop.html"},
        {"label": "Parts and Accessories", "href": "service/parts-accessories.html"},
        {"label": "Extended Warranty",     "href": "service/extended-warranty.html"},
    ]},

    {"label": "Driving School", "href": "driving-school.html"},

    {"label": "More", "href": "offers.html", "children": [
        {"label": "Offers",                "href": "offers.html"},
        {"label": "Finance and Insurance", "href": "finance.html"},
        {"label": "FAQs",                  "href": "faqs.html"},
        {"label": "News and Advice",       "href": "blog.html"},
        {"label": "Privacy Policy",        "href": "privacy-policy.html"},
        {"label": "Terms and Conditions",  "href": "terms-conditions.html"},
    ]},

    {"label": "Contact", "href": "contact.html", "children": [
        {"label": "Contact Us",        "href": "contact.html"},
        {"label": "Book a Test Drive", "href": "test-drive.html"},
        {"label": "Find Us",           "href": "locations.html"},
    ]},
]

FOOTER_COLUMNS = [
    ("New Cars", [
        ("All Models",            "cars/index.html"),
        ("ARENA Range",           "cars/arena.html"),
        ("NEXA Range",            "cars/nexa.html"),
        ("Book a Test Drive",     "test-drive.html"),
        ("Current Offers",        "offers.html"),
        ("Finance and Insurance", "finance.html"),
    ]),
    ("Owning a Maruti", [
        ("Book a Service",        "service/book-service.html"),
        ("Periodic Maintenance",  "service/periodic-maintenance.html"),
        ("Body Shop",             "service/body-shop.html"),
        ("Parts and Accessories", "service/parts-accessories.html"),
        ("Extended Warranty",     "service/extended-warranty.html"),
        ("Sell Your Car",         "true-value/sell-your-car.html"),
    ]),
]
