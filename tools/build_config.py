#!/usr/bin/env python3
"""
build_config.py  —  V2
Reads  config/site-config.xlsx  and writes  assets/js/site-config.js

Run this after every edit to the workbook, then commit the generated JS:

    python3 tools/build_config.py

Requires:  pip install openpyxl

If you would rather not install Python, open admin/index.html, drop the
.xlsx onto the "Excel Config" tab and press "Download site-config.js" —
it produces a byte-for-byte equivalent file.
"""
import json
import os
import sys

from openpyxl import load_workbook

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, "config", "site-config.xlsx")
OUT = os.path.join(ROOT, "assets", "js", "site-config.js")

SOCIAL_ORDER = ["facebook", "instagram", "linkedin", "twitter", "pinterest",
                "youtube", "indiamart", "justdial", "whatsapp"]


def as_text(value):
    if value is None:
        return ""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def read_kv(wb, sheet_name, meta=None):
    """Two-column Setting/Value sheet -> dict. Stops at the NOTE row."""
    if sheet_name not in wb.sheetnames:
        raise SystemExit("Missing sheet: %s" % sheet_name)
    ws = wb[sheet_name]
    out = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row:
            continue
        key = as_text(row[0])
        if not key or key.upper() == "NOTE" or key.lower() == "setting":
            continue
        out[key] = as_text(row[1] if len(row) > 1 else "")
        if meta is not None:
            meta[key] = as_text(row[2] if len(row) > 2 else "")
    return out


# Keys whose auto-generated label would read badly. "Ch arena" is technically a
# humanised key; it is not a label anyone can act on.
LABELS = {
    "ch_arena": "ARENA channel colour",
    "ch_nexa": "NEXA channel colour",
    "ch_truevalue": "True Value channel colour",
    "ch_service": "Service channel colour",
    "ch_school": "Driving School channel colour",
    "phone_service": "Service phone",
    "phone_service_display": "Service phone (as displayed)",
    "phone_display": "Phone (as displayed)",
    "email_service": "Service email",
    "whatsapp_number": "WhatsApp number",
    "whatsapp_greeting": "WhatsApp greeting",
    "map_embed_url": "Google Map embed URL",
    "map_link": "Google Map link",
    "site_url": "Site URL",
    "google_fonts_url": "Google Fonts URL",
    "business_hours_sun": "Sunday hours",
    "dealer_disclaimer": "Dealer disclaimer",
    "pincode": "PIN code",
}


def humanise(key):
    if key in LABELS:
        return LABELS[key]
    return key.replace("_", " ").strip().capitalize()


def field_kind(section, key, value):
    if section == "colors":
        return "color"
    if key.endswith("_family"):
        return "font"
    if key in ("map_embed_url", "map_link", "site_url", "google_fonts_url"):
        return "url"
    if key in ("short_description", "whatsapp_greeting", "copyright_line",
               "dealer_disclaimer"):
        return "textarea"
    if section == "fonts":
        if key.endswith(("_size", "_weight", "_radius", "_spacing", "_width",
                         "_size_tablet", "_size_mobile", "_line_height")):
            return "number"
    return "text"


def read_social(wb):
    ws = wb["Social"]
    found = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row:
            continue
        platform = as_text(row[0]).lower()
        if not platform or platform.upper() == "NOTE" or platform == "platform":
            continue
        enabled = as_text(row[2] if len(row) > 2 else "yes").lower()
        found[platform] = {
            "platform": platform,
            "url": as_text(row[1] if len(row) > 1 else ""),
            "enabled": enabled not in ("no", "false", "0", "off"),
            "label": as_text(row[3] if len(row) > 3 else "") or platform.title(),
        }
    return [found[p] for p in SOCIAL_ORDER if p in found] + \
           [v for k, v in found.items() if k not in SOCIAL_ORDER]


def read_themes(wb):
    ws = wb["Themes"]
    themes = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if not row:
            continue
        name = as_text(row[0])
        if not name or name.upper() == "NOTE" or name.lower() == "theme name":
            continue
        cols = [as_text(c) for c in row[1:9]]
        cols += [""] * (8 - len(cols))
        if not cols[0]:
            continue
        themes.append({
            "name": name,
            "primary": cols[0],
            "primary_ink": cols[1] or cols[0],
            "secondary": cols[2],
            "tertiary": cols[3],
            "tertiary_ink": cols[4] or cols[3],
            "accent_cream": cols[5],
            "footer_bg": cols[6] or cols[1] or cols[0],
            "topbar_bg": cols[7] or cols[1] or cols[0],
        })
    return themes


def main():
    if not os.path.exists(XLSX):
        raise SystemExit("Cannot find %s" % XLSX)
    wb = load_workbook(XLSX, data_only=True)

    help_business, help_colors, help_fonts = {}, {}, {}
    config = {
        "business": read_kv(wb, "Business", help_business),
        "colors": read_kv(wb, "Colors", help_colors),
        "fonts": read_kv(wb, "Fonts", help_fonts),
        "social": read_social(wb),
        "themes": read_themes(wb),
    }

    meta = {}
    for section, helps in (("business", help_business), ("colors", help_colors),
                           ("fonts", help_fonts)):
        meta[section] = [
            {"k": key, "l": humanise(key), "h": helps.get(key, ""),
             "t": field_kind(section, key, config[section][key])}
            for key in config[section]
        ]

    problems = []
    for key, value in config["colors"].items():
        if value and not (value.startswith("#") and len(value) in (4, 7, 9)):
            problems.append("Colors!%s = %r is not a hex colour" % (key, value))
    wa = config["business"].get("whatsapp_number", "")
    if wa and not wa.isdigit():
        problems.append("Business!whatsapp_number = %r must be digits only "
                        "(country code + number)" % wa)
    for p in problems:
        print("  warning: %s" % p, file=sys.stderr)

    body = json.dumps(config, indent=2, ensure_ascii=False)
    js = (
        "/* site-config.js  —  V1\n"
        " * GENERATED FILE — do not edit by hand.\n"
        " * Source: config/site-config.xlsx\n"
        " * Rebuild: python3 tools/build_config.py\n"
        " *   (or use the Excel Config tab in admin/index.html)\n"
        " */\n"
        "window.SITE_CONFIG = " + body + ";\n"
        "window.SITE_CONFIG_META = " + json.dumps(meta, ensure_ascii=False) + ";\n"
    )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(js)
    print("wrote %s  (%d business, %d colors, %d fonts, %d social, %d themes)" % (
        os.path.relpath(OUT, ROOT), len(config["business"]), len(config["colors"]),
        len(config["fonts"]), len(config["social"]), len(config["themes"])))


if __name__ == "__main__":
    main()
