"""
config_schema.py  —  V2
Single source of truth for what lives in config/site-config.xlsx.

Used by:
  * make_config_xlsx.py  (writes a fresh workbook from these defaults)
  * build_config.py      (reads the workbook back and emits assets/js/site-config.js)

Every row is (key, default_value, help_text).
"""

BUSINESS = [
    ("business_name",      "Pillai & Sons Motor Company",     "Shown in the logo, page titles and footer."),
    ("legal_name",         "Pillai & Sons Motor Company",     "Full registered name, used in the legal pages."),
    ("tagline",            "Authorised Maruti Suzuki Dealer", "Small line under the logo and in the footer."),
    ("short_description",  "Authorised Maruti Suzuki dealer in Thanjavur — ARENA and NEXA new cars, True Value pre-owned, service, genuine parts and the Maruti Driving School, all under one roof.",
                                                              "Used in the footer and as the fallback meta description."),
    ("phone",              "8939752872",                      "Digits only, no spaces. Used to build tel: links."),
    ("phone_display",      "+91 89397 52872",                 "How the phone number is printed on screen."),
    ("phone_country_code", "91",                              "Country code without '+'. India = 91."),
    ("phone_service",      "8939752872",                      "Workshop / service booking number. Digits only."),
    ("phone_service_display", "+91 89397 52872",              "How the service number is printed on screen."),
    ("whatsapp_number",    "918939752872",                    "Country code + number, digits only. Every form opens wa.me/<this>."),
    ("email",              "sales@pillaiandsons.in",          "The address printed on the contact page, in the footer and in the "
                                                              "search-engine listing."),
    ("email_service",      "sales@pillaiandsons.in",           "Optional separate workshop address. Nothing on the site shows this "
                                                              "yet; set it and it is ready for a service-enquiry link."),
    ("address_line1",      "31-A, Medical College Road",      "Street address line 1."),
    ("address_line2",      "Rajjappa Nagar, Jayalakshmi Nagar", "Street address line 2 / locality."),
    ("city",               "Thanjavur",                       "City."),
    ("state",              "Tamil Nadu",                      "State."),
    ("pincode",            "613007",                          "PIN code."),
    ("country",            "India",                           "Country."),
    ("business_hours",     "Mon - Sat  09:00 AM - 07:30 PM",  "Showroom hours, printed in the top bar and footer."),
    ("business_hours_sun", "Sunday  10:00 AM - 05:00 PM",     "Sunday hours."),
    ("service_hours",      "Mon - Sat  08:30 AM - 06:30 PM",  "Workshop hours."),
    ("map_embed_url",      "https://www.google.com/maps?q=31-A,+Medical+College+Road,+Rajjappa+Nagar,+Thanjavur,+Tamil+Nadu+613007&output=embed",
                                                              "Google Maps EMBED url (must end with &output=embed or be a /maps/embed link)."),
    ("map_link",           "https://www.google.com/maps/search/?api=1&query=31-A+Medical+College+Road+Thanjavur+613007",
                                                              "Google Maps link opened by the 'Get Directions' button."),
    ("years_experience",   "30",                              "Number shown in the 'Years' counter."),
    ("cars_delivered",     "18000",                           "Counter: cars delivered."),
    ("happy_customers",    "16500",                           "Counter: customers served."),
    ("site_url",           "https://example.github.io/pillai-and-sons",
                                                              "Live URL. Drives canonical tags, sitemap.xml and the 404 base path."),
    ("copyright_line",     "Pillai & Sons Motor Company. All rights reserved.",
                                                              "Footer copyright text (the year is added automatically)."),
    ("whatsapp_greeting",  "Hello Pillai & Sons, I would like to enquire about a Maruti Suzuki car.",
                                                              "Text pre-filled when someone taps the floating WhatsApp button."),
    ("dealer_disclaimer",  "Pillai & Sons Motor Company is an authorised dealer of Maruti Suzuki India Limited. Maruti Suzuki, ARENA, NEXA and True Value are trademarks of Maruti Suzuki India Limited.",
                                                              "Shown in the footer. Keep this accurate."),
]

COLORS = [
    ("primary",         "#D5232B", "House accent — the Maruti red used on buttons and highlights."),
    ("primary_ink",     "#B01D24", "Deeper red for anything carrying white text, so contrast passes WCAG AA. "
                                   "Set it equal to primary for a flatter look and the audit will start failing."),
    ("secondary",       "#1B1D21", "Graphite. Dark panels, headings on light, hover states."),
    ("tertiary",        "#1D6FA3", "Steel blue. Informational accents and links inside body copy."),
    ("tertiary_ink",    "#175B87", "Deeper steel blue for white text on blue."),
    ("heading",         "#14161A", "All headings h1-h6."),
    ("text",            "#565D66", "Body copy."),
    ("accent_cream",    "#F1F4F7", "Cool tinted panels and highlight boxes."),
    ("white_smoke",     "#F7F9FA", "Light section backgrounds."),
    ("border",          "#DDE2E7", "Hairline borders and dividers."),
    ("body_bg",         "#FFFFFF", "Page background."),
    ("topbar_bg",       "#14161A", "Thin bar above the header."),
    ("topbar_text",     "#FFFFFF", "Text colour in the top bar."),
    ("header_bg",       "#FFFFFF", "Main navigation bar background."),
    ("nav_link",        "#1B1D21", "Navigation link colour."),
    ("nav_link_active", "#FFFFFF", "Navigation link colour when the item is active or open."),
    ("footer_bg",       "#14161A", "Footer background."),
    ("footer_text",     "#FFFFFF", "Footer text and links."),
    ("button_text",     "#FFFFFF", "Text inside primary buttons."),
    ("star",            "#F5A623", "Rating stars."),
    # --- the five business channels -------------------------------------
    ("ch_arena",        "#D5232B", "ARENA channel colour — Maruti red."),
    ("ch_nexa",         "#1C1F26", "NEXA channel colour — near-black premium."),
    ("ch_truevalue",    "#17548C", "True Value channel colour — deep blue."),
    ("ch_service",      "#B4591A", "Service channel colour — workshop amber."),
    ("ch_school",       "#2E7D5B", "Driving School channel colour — green."),
]

FONTS = [
    ("heading_family",       "Poppins",    "Font for headings. Bundled offline: Poppins, Montserrat."),
    ("body_family",          "Montserrat", "Font for body copy."),
    ("google_fonts_url",     "",           "Optional. Paste a Google Fonts stylesheet URL to use a font that is not bundled."),
    ("base_size",            "16.5",       "Body font size in px (desktop)."),
    ("base_size_mobile",     "16",         "Body font size in px (mobile)."),
    ("base_line_height",     "1.7",        "Body line height (unitless)."),
    ("base_weight",          "400",        "Body font weight."),
    ("h1_size",              "58",         "H1 size px, desktop."),
    ("h1_size_tablet",       "44",         "H1 size px, tablet."),
    ("h1_size_mobile",       "34",         "H1 size px, mobile."),
    ("h1_weight",            "700",        "H1 weight."),
    ("h2_size",              "42",         "H2 size px, desktop."),
    ("h2_size_tablet",       "34",         "H2 size px, tablet."),
    ("h2_size_mobile",       "28",         "H2 size px, mobile."),
    ("h2_weight",            "700",        "H2 weight."),
    ("h3_size",              "30",         "H3 size px, desktop."),
    ("h3_size_tablet",       "26",         "H3 size px, tablet."),
    ("h3_size_mobile",       "23",         "H3 size px, mobile."),
    ("h3_weight",            "700",        "H3 weight."),
    ("h4_size",              "22",         "H4 size px, desktop."),
    ("h4_size_mobile",       "19",         "H4 size px, mobile."),
    ("h4_weight",            "600",        "H4 weight."),
    ("h5_size",              "18",         "H5 size px, desktop."),
    ("h5_size_mobile",       "17",         "H5 size px, mobile."),
    ("h5_weight",            "600",        "H5 weight."),
    ("h6_size",              "16",         "H6 size px."),
    ("h6_weight",            "600",        "H6 weight."),
    ("heading_line_height",  "1.22",       "Line height for all headings."),
    ("subheading_size",      "12",         "The small uppercase eyebrow label above section titles."),
    ("subheading_weight",    "700",        "Eyebrow weight."),
    ("subheading_spacing",   "2.2",        "Eyebrow letter-spacing in px."),
    ("nav_size",             "14.5",       "Navigation link size px."),
    ("nav_weight",           "600",        "Navigation link weight."),
    ("button_size",          "14.5",       "Button label size px."),
    ("button_weight",        "600",        "Button label weight."),
    ("button_radius",        "6",          "Button corner radius px. 6 reads technical; 30 reads friendly."),
    ("card_radius",          "12",         "Card and image corner radius px."),
    ("container_width",      "1280",       "Max content width in px."),
]

# platform, url, enabled, label
SOCIAL = [
    ("facebook",  "https://www.facebook.com/",  "yes", "Facebook"),
    ("instagram", "https://www.instagram.com/", "yes", "Instagram"),
    ("youtube",   "https://www.youtube.com/",   "yes", "YouTube"),
    ("linkedin",  "https://www.linkedin.com/",  "yes", "LinkedIn"),
    ("twitter",   "https://twitter.com/",       "yes", "X / Twitter"),
    ("pinterest", "https://www.pinterest.com/", "no",  "Pinterest"),
    ("indiamart", "https://www.indiamart.com/", "no",  "IndiaMART"),
    ("justdial",  "https://www.justdial.com/",  "yes", "JustDial"),
    ("whatsapp",  "",                           "yes", "WhatsApp"),
]


# --- contrast helpers -------------------------------------------------------
def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def luminance(hex_colour):
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contrast_on_white(hex_colour):
    return 1.05 / (luminance(hex_colour) + 0.05)


# The brand colour is used two ways: as a background carrying white text, and as
# text on the pale tinted panels. The panel case is the stricter of the two, so
# INK_TEXT is the target for anything that might become text, INK_FILL for
# backgrounds only.
INK_TEXT = 5.15
INK_FILL = 4.6


def ink(hex_colour, target=INK_TEXT):
    """Darken a brand colour just far enough to carry white text at WCAG AA.

    Returns the colour unchanged when it already passes, so a palette designed
    with contrast in mind is left alone.
    """
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    for step in range(0, 101):
        f = 1 - step / 100.0
        cand = "#%02X%02X%02X" % (int(r * f), int(g * f), int(b * f))
        if contrast_on_white(cand) >= target:
            return cand
    return "#000000"


# name, primary, secondary, tertiary, accent
_THEME_BASE = [
    ("Maruti Red (default)", "#D5232B", "#1B1D21", "#1D6FA3", "#F1F4F7"),
    ("Graphite",             "#3E4854", "#15181C", "#2E7D8F", "#F2F4F6"),
    ("Deep Blue",            "#17548C", "#111A24", "#C1611A", "#EEF2F7"),
    ("Forest",               "#2E7D5B", "#14201A", "#B4591A", "#EFF4F1"),
    ("Midnight Amber",       "#B4591A", "#16181D", "#1D6FA3", "#F6F2ED"),
]

# name, primary, primary_ink, secondary, tertiary, tertiary_ink,
# accent_cream, footer_bg, topbar_bg
THEMES = [
    (name, primary, ink(primary, INK_TEXT), secondary,
     tertiary, ink(tertiary, INK_FILL), accent, secondary, secondary)
    for name, primary, secondary, tertiary, accent in _THEME_BASE
]
