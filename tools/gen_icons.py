"""
gen_icons.py  —  V1
Inline SVG icon set for the dealership site.

Icons are inlined into every page rather than loaded from a sprite file, so they
render correctly when the site is opened straight off disk (file://) as well as
over HTTP, and so one CSS colour change repaints them all.

All paths sit on a 24x24 grid, are stroke-based unless noted, and inherit
currentColor. Three groups: interface, contact/social, and the automotive set
that carries the five business channels (ARENA, NEXA, True Value, Service,
Driving School).
"""

_S = 'stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" fill="none"'
_T = 'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none"'
_F = 'fill="currentColor"'

ICONS = {
    # --- interface --------------------------------------------------------
    "arrow-right":   '<path d="M4 12h15M13 6l6 6-6 6" %s/>' % _S,
    "arrow-left":    '<path d="M20 12H5M11 6l-6 6 6 6" %s/>' % _S,
    "arrow-up":      '<path d="M12 19V5M6 11l6-6 6 6" %s/>' % _S,
    "chevron-down":  '<path d="M5 9l7 7 7-7" %s/>' % _S,
    "chevron-right": '<path d="M9 5l7 7-7 7" %s/>' % _S,
    "chevron-left":  '<path d="M15 5l-7 7 7 7" %s/>' % _S,
    "check": '<path d="M4 12.5 9 17.5 20 6.5" %s/>' % _S,
    "check-square": '<rect x="3" y="3" width="18" height="18" rx="4" %s/>'
                    '<path d="M7.5 12.2 10.6 15.3 16.5 9" %s/>' % (_S, _S),
    "close": '<path d="M6 6l12 12M18 6L6 18" %s/>' % _S,
    "plus":  '<path d="M12 5v14M5 12h14" %s/>' % _S,
    "minus": '<path d="M5 12h14" %s/>' % _S,
    "play":  '<path d="M8 5.5v13l11-6.5-11-6.5Z" %s/>' % _F,
    "quote": '<path d="M9.6 6C6.5 7.5 4.8 10.2 4.8 13.6V18h6.1v-6H8.1c0-2 .7-3.4 2.4-4.3L9.6 6Zm9.3 0c-3.1 1.5-4.8 4.2-4.8 7.6V18h6.1v-6h-2.8c0-2 .7-3.4 2.4-4.3L18.9 6Z" %s/>' % _F,
    "star":  '<path d="m12 3.6 2.6 5.4 5.9.8-4.3 4.2 1 5.9-5.2-2.8-5.2 2.8 1-5.9L3.5 9.8l5.9-.8L12 3.6Z" %s/>' % _F,
    "search": '<circle cx="10.8" cy="10.8" r="7.2" %s/><path d="m16.1 16.1 4.5 4.5" %s/>' % (_S, _S),
    "filter": '<path d="M3.4 5.4h17.2l-6.8 8.2v6.2l-3.6-2.2v-4.2L3.4 5.4Z" %s/>' % _S,
    "info":   '<circle cx="12" cy="12" r="9" %s/><path d="M12 11.2v5M12 7.4v.4" %s/>' % (_S, _S),
    "grid":   '<rect x="3.4" y="3.4" width="7" height="7" rx="1.6" %s/>'
              '<rect x="13.6" y="3.4" width="7" height="7" rx="1.6" %s/>'
              '<rect x="3.4" y="13.6" width="7" height="7" rx="1.6" %s/>'
              '<rect x="13.6" y="13.6" width="7" height="7" rx="1.6" %s/>' % (_S, _S, _S, _S),
    "layers": '<path d="m12 3.4 8.6 4.4L12 12.2 3.4 7.8 12 3.4Z" %s/>'
              '<path d="m3.4 12 8.6 4.4L20.6 12M3.4 16.2 12 20.6l8.6-4.4" %s/>' % (_S, _S),
    "download": '<path d="M21 15.4v3.4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-3.4" %s/>'
                '<path d="m7.6 10.6 4.4 4.4 4.4-4.4M12 15V3.4" %s/>' % (_S, _S),
    "palette": '<path d="M12 3.4a8.6 8.6 0 0 0 0 17.2 1.7 1.7 0 0 0 1.7-1.7c0-.5-.2-.9-.5-1.2a1.7 1.7 0 0 1 1.2-2.9h2a3.8 3.8 0 0 0 3.8-3.8c0-4.2-3.8-7.6-8.2-7.6Z" %s/>'
               '<circle cx="7.8" cy="11.4" r="1.1" %s/><circle cx="11.2" cy="8" r="1.1" %s/>'
               '<circle cx="15.6" cy="8.8" r="1.1" %s/>' % (_S, _F, _F, _F),
    "sparkle": '<path d="m12 3.4 2 5.4 5.4 2-5.4 2-2 5.4-2-5.4-5.4-2 5.4-2 2-5.4ZM18.6 15.6l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8.8-2Z" %s/>' % _S,
    "target": '<circle cx="12" cy="12" r="8.6" %s/><circle cx="12" cy="12" r="4.8" %s/>'
              '<circle cx="12" cy="12" r="1.3" %s/>' % (_S, _S, _F),

    # --- contact ----------------------------------------------------------
    "phone": '<path d="M21 16.9v2.6a1.8 1.8 0 0 1-2 1.8 17.6 17.6 0 0 1-7.7-2.7 17.3 17.3 0 0 1-5.3-5.3A17.6 17.6 0 0 1 3.3 5.5a1.8 1.8 0 0 1 1.8-2h2.6a1.8 1.8 0 0 1 1.8 1.6c.1.9.3 1.7.6 2.5a1.8 1.8 0 0 1-.4 1.9l-1.1 1.1a14 14 0 0 0 5.3 5.3l1.1-1.1a1.8 1.8 0 0 1 1.9-.4c.8.3 1.6.5 2.5.6a1.8 1.8 0 0 1 1.6 1.9Z" %s/>' % _S,
    "mail": '<rect x="2.6" y="4.6" width="18.8" height="14.8" rx="2.4" %s/>'
            '<path d="m3.4 6.4 8.6 6 8.6-6" %s/>' % (_S, _S),
    "map-pin": '<path d="M20 10.5c0 5.4-8 12-8 12s-8-6.6-8-12a8 8 0 0 1 16 0Z" %s/>'
               '<circle cx="12" cy="10.3" r="2.9" %s/>' % (_S, _S),
    "clock": '<circle cx="12" cy="12" r="9" %s/><path d="M12 7v5.3l3.4 2" %s/>' % (_S, _S),
    "send": '<path d="M21.5 2.5 10.8 13.2M21.5 2.5l-6.8 19-3.9-8.3-8.3-3.9 19-6.8Z" %s/>' % _S,
    "calendar": '<rect x="3.2" y="5" width="17.6" height="16" rx="2.6" %s/>'
                '<path d="M3.2 10h17.6M8 3v4M16 3v4" %s/>' % (_S, _S),
    "headset": '<path d="M4.4 14.6v-2.4a7.6 7.6 0 0 1 15.2 0v2.4" %s/>'
               '<path d="M4.4 14a2.2 2.2 0 0 1 2.2 2.2v1.6a2.2 2.2 0 0 1-4.4 0v-1.6A2.2 2.2 0 0 1 4.4 14ZM19.6 14a2.2 2.2 0 0 1 2.2 2.2v1.6a2.2 2.2 0 0 1-4.4 0v-1.6A2.2 2.2 0 0 1 19.6 14Z" %s/>' % (_S, _S),
    "store": '<path d="M4 9.5V20h16V9.5" %s/>'
             '<path d="M3 4h18l1 5.5a3 3 0 0 1-5.5 1.6 3 3 0 0 1-5 0 3 3 0 0 1-5 0A3 3 0 0 1 2 9.5L3 4Z" %s/>'
             '<path d="M9.5 20v-5.5h5V20" %s/>' % (_S, _S, _S),
    "building": '<path d="M4.4 21V4.4a1 1 0 0 1 1-1h8.2a1 1 0 0 1 1 1V21M14.6 21V10h4a1 1 0 0 1 1 1v10" %s/>'
                '<path d="M7.6 7.6h3.4M7.6 11.6h3.4M7.6 15.6h3.4M2.6 21h18.8" %s/>' % (_S, _S),
    "home": '<path d="M3.5 10.4 12 3.6l8.5 6.8V20a1.4 1.4 0 0 1-1.4 1.4H4.9A1.4 1.4 0 0 1 3.5 20v-9.6Z" %s/>'
            '<path d="M9.4 21.4v-7.2h5.2v7.2" %s/>' % (_S, _S),

    # --- social (filled brand glyphs) -------------------------------------
    "facebook": '<path d="M13.5 21v-8h2.7l.4-3.1h-3.1V7.9c0-.9.25-1.5 1.55-1.5H16.7V3.6a22 22 0 0 0-2.4-.12c-2.4 0-4 1.45-4 4.12v2.3H7.6V13h2.7v8h3.2Z" %s/>' % _F,
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5.2" %s/><circle cx="12" cy="12" r="4" %s/>'
                 '<circle cx="17.2" cy="6.8" r="1.2" %s/>' % (_S, _S, _F),
    "linkedin": '<path d="M6.9 8.6H4V21h2.9V8.6ZM5.45 3.4a1.7 1.7 0 1 0 0 3.4 1.7 1.7 0 0 0 0-3.4ZM20 13.9c0-3.2-1.7-4.7-4-4.7a3.5 3.5 0 0 0-3.1 1.7h-.1V8.6H10V21h2.9v-6.1c0-1.6.3-3.2 2.3-3.2s2 1.8 2 3.3V21H20v-7.1Z" %s/>' % _F,
    "twitter": '<path d="M17.6 3h3.3l-7.2 8.2L22 21h-6.6l-5.2-6.8L4.3 21H1l7.7-8.8L1.3 3H8l4.7 6.2L17.6 3Zm-1.2 16h1.8L7.7 4.9H5.8L16.4 19Z" %s/>' % _F,
    "pinterest": '<path d="M12 3a9 9 0 0 0-3.3 17.4c-.08-.7-.15-1.9.03-2.7l1.1-4.6s-.28-.56-.28-1.4c0-1.3.76-2.3 1.7-2.3.8 0 1.2.6 1.2 1.3 0 .8-.5 2-.78 3.2-.22 1 .5 1.8 1.5 1.8 1.8 0 3.1-1.9 3.1-4.6 0-2.4-1.7-4.1-4.2-4.1a4.4 4.4 0 0 0-4.5 4.4c0 .9.33 1.8.75 2.3.08.1.09.2.07.3l-.28 1.1c-.04.2-.15.2-.34.1-1.3-.6-2.1-2.5-2.1-4 0-3.2 2.4-6.2 6.8-6.2 3.6 0 6.4 2.5 6.4 5.9 0 3.5-2.2 6.4-5.3 6.4-1 0-2-.5-2.3-1.2l-.6 2.4c-.2.9-.8 2-1.2 2.6A9 9 0 1 0 12 3Z" %s/>' % _F,
    "youtube": '<path d="M21.6 7.9a2.6 2.6 0 0 0-1.8-1.8C18.2 5.6 12 5.6 12 5.6s-6.2 0-7.8.5A2.6 2.6 0 0 0 2.4 7.9 27 27 0 0 0 2 12a27 27 0 0 0 .4 4.1 2.6 2.6 0 0 0 1.8 1.8c1.6.5 7.8.5 7.8.5s6.2 0 7.8-.5a2.6 2.6 0 0 0 1.8-1.8A27 27 0 0 0 22 12a27 27 0 0 0-.4-4.1ZM10 15V9l5.2 3L10 15Z" %s/>' % _F,
    "whatsapp": '<path d="M17.5 14.4c-.3-.15-1.75-.86-2-.96-.28-.1-.48-.15-.68.15s-.78.96-.95 1.16c-.18.2-.35.22-.65.07a8.2 8.2 0 0 1-2.4-1.48 9 9 0 0 1-1.66-2.07c-.18-.3 0-.46.13-.6.13-.14.3-.35.45-.53.15-.18.2-.3.3-.5.1-.2.05-.38-.02-.53-.08-.15-.68-1.62-.93-2.22-.24-.58-.5-.5-.68-.51h-.58c-.2 0-.53.07-.8.37-.28.3-1.05 1.02-1.05 2.5s1.08 2.9 1.23 3.1c.15.2 2.12 3.24 5.14 4.54.72.31 1.28.5 1.71.63.72.23 1.38.2 1.9.12.58-.09 1.75-.72 2-1.4.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35ZM12 2.2A9.7 9.7 0 0 0 3.72 17L2.4 21.9l5-1.3A9.7 9.7 0 1 0 12 2.2Zm0 17.7a8 8 0 0 1-4.1-1.12l-.3-.18-3 .78.8-2.92-.2-.3A8 8 0 1 1 12 19.9Z" %s/>' % _F,
    "google": '<path d="M21.6 12.2c0-.7-.06-1.4-.18-2.05H12v3.9h5.4a4.6 4.6 0 0 1-2 3v2.5h3.2c1.9-1.75 3-4.3 3-7.35Z" fill="#4285F4"/>'
              '<path d="M12 22c2.7 0 5-.9 6.6-2.45l-3.2-2.5c-.9.6-2.05.95-3.4.95-2.6 0-4.8-1.75-5.6-4.1H3.1v2.6A10 10 0 0 0 12 22Z" fill="#34A853"/>'
              '<path d="M6.4 13.9a6 6 0 0 1 0-3.8V7.5H3.1a10 10 0 0 0 0 9l3.3-2.6Z" fill="#FBBC05"/>'
              '<path d="M12 5.95c1.47 0 2.79.5 3.83 1.5l2.85-2.85C16.97 2.98 14.7 2 12 2A10 10 0 0 0 3.1 7.5l3.3 2.6C7.2 7.7 9.4 5.95 12 5.95Z" fill="#EA4335"/>',
    "book-open": '<path d="M2.6 5.2h6a3.4 3.4 0 0 1 3.4 3.4V20a2.6 2.6 0 0 0-2.6-2.6h-6.8V5.2ZM21.4 5.2h-6A3.4 3.4 0 0 0 12 8.6V20a2.6 2.6 0 0 1 2.6-2.6h6.8V5.2Z" %s/>' % _S,

    # --- automotive -------------------------------------------------------
    # The workhorses. Every channel section, spec chip and service card pulls
    # from this group, so they share one stroke weight and one optical size.
    "car": '<path d="M4.4 16.4v-3.6l2-4.6a2.2 2.2 0 0 1 2-1.4h7.2a2.2 2.2 0 0 1 2 1.4l2 4.6v3.6" %s/>'
           '<path d="M2.6 12.8h18.8" %s/>'
           '<circle cx="7.6" cy="16.6" r="2" %s/><circle cx="16.4" cy="16.6" r="2" %s/>'
           '<path d="M9.8 16.6h4.4" %s/>' % (_S, _S, _S, _S, _S),
    "car-front": '<path d="M4 17.6v1.8a1 1 0 0 1-1 1H2.4M20 17.6v1.8a1 1 0 0 0 1 1h.6" %s/>'
                 '<path d="M3.4 17.6v-4.4l2-5.2a2.2 2.2 0 0 1 2-1.4h9.2a2.2 2.2 0 0 1 2 1.4l2 5.2v4.4Z" %s/>'
                 '<path d="M3.4 13.2h17.2M6.8 15.4h1.6M15.6 15.4h1.6" %s/>' % (_S, _S, _S),
    "exchange": '<path d="M3.4 8.6h14.2M14.4 5.4l3.2 3.2-3.2 3.2" %s/>'
                '<path d="M20.6 15.4H6.4M9.6 12.2l-3.2 3.2 3.2 3.2" %s/>' % (_S, _S),
    "steering": '<circle cx="12" cy="12" r="9" %s/><circle cx="12" cy="12" r="2.8" %s/>'
                '<path d="M3.2 11.4h6M14.8 11.4h6M12 14.8V21" %s/>' % (_S, _S, _S),
    "wrench": '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.8-3.8a6 6 0 0 1-7.9 7.9l-6.9 6.9a2.1 2.1 0 0 1-3-3l6.9-6.9a6 6 0 0 1 7.9-7.9l-3.8 3.8Z" %s/>' % _S,
    "tools": '<path d="M14.2 6.6a4 4 0 0 1 5.4 5.2l-8.4 8.4a2.3 2.3 0 0 1-3.2-3.2l8.4-8.4" %s/>'
             '<path d="M9.4 4.4 5.6 8.2 3.4 6 7.2 2.2M3.4 6l2.2 2.2" %s/>' % (_S, _S),
    "cog": '<circle cx="12" cy="12" r="3.2" %s/>'
           '<path d="M19.5 15a1.7 1.7 0 0 0 .34 1.87l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.7 1.7 0 0 0-1.87-.34 1.7 1.7 0 0 0-1 1.55V21a2 2 0 1 1-4 0v-.09A1.7 1.7 0 0 0 9 19.4a1.7 1.7 0 0 0-1.87.34l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.7 1.7 0 0 0 4.6 15a1.7 1.7 0 0 0-1.55-1H3a2 2 0 1 1 0-4h.09A1.7 1.7 0 0 0 4.6 9a1.7 1.7 0 0 0-.34-1.87l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.7 1.7 0 0 0 9 4.6h.08A1.7 1.7 0 0 0 10 3.05V3a2 2 0 1 1 4 0v.09a1.7 1.7 0 0 0 1 1.55 1.7 1.7 0 0 0 1.87-.34l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.7 1.7 0 0 0 19.4 9v.08a1.7 1.7 0 0 0 1.55 1H21a2 2 0 1 1 0 4h-.09a1.7 1.7 0 0 0-1.55 1Z" %s/>' % (_S, _T),
    "certificate": '<path d="M14.6 3.4H6.6a2 2 0 0 0-2 2v13.2a2 2 0 0 0 2 2h4.2" %s/>'
                   '<path d="M8 7.8h6.4M8 11.4h4.2" %s/>'
                   '<circle cx="16.8" cy="14.6" r="3.4" %s/>'
                   '<path d="m14.4 17.2-.8 4 3.2-1.7 3.2 1.7-.8-4" %s/>' % (_S, _S, _S, _S),
    "shield": '<path d="M12 3.2 20 6v5.5c0 4.6-3.2 8.2-8 9.4-4.8-1.2-8-4.8-8-9.4V6l8-2.8Z" %s/>'
              '<path d="m8.8 12.2 2.2 2.2 4.2-4.4" %s/>' % (_S, _S),
    "award": '<circle cx="12" cy="9.4" r="5.6" %s/>'
             '<path d="m8.6 14.2-1.4 6.4 4.8-2.6 4.8 2.6-1.4-6.4" %s/>' % (_S, _S),
    "fuel": '<path d="M4.6 20.6V5.4a2 2 0 0 1 2-2h5.6a2 2 0 0 1 2 2v15.2M3.2 20.6h13" %s/>'
            '<path d="M14.2 9.6h2.4a1.8 1.8 0 0 1 1.8 1.8v5a1.8 1.8 0 0 0 3.6 0V9.8l-2.8-2.8" %s/>'
            '<path d="M7.2 7.6h4.8v3.2H7.2z" %s/>' % (_S, _S, _S),
    # A dial, not an arc floating in space: the flat base closes the shape so it
    # still reads as a speedometer at 18px in a spec chip.
    "gauge": '<path d="M3.4 17.2a8.6 8.6 0 1 1 17.2 0Z" %s/>'
             '<path d="m12 17.2 4.6-6" %s/><circle cx="12" cy="17.2" r="1.6" %s/>' % (_S, _S, _S),
    "gearbox": '<path d="M5.6 6.4v12.2M12 6.4v12.2M18.4 6.4v12.2M5.6 12h12.8" %s/>'
               '<circle cx="5.6" cy="4.6" r="1.8" %s/><circle cx="12" cy="4.6" r="1.8" %s/>'
               '<circle cx="18.4" cy="4.6" r="1.8" %s/><circle cx="18.4" cy="20.4" r="1.8" %s/>'
               % (_S, _S, _S, _S, _S),
    # The bolt is filled, not stroked — a stroked bolt at 18px collapses into a
    # zigzag scribble inside the cell.
    "battery": '<rect x="2.6" y="6.8" width="16" height="10.4" rx="2.4" %s/>'
               '<path d="M21.4 10.2v3.6" %s/>'
               '<path d="M12.4 8.6 8.8 13.4h2.2l-.8 3.4 3.6-4.8h-2.2l.8-3.4Z" %s/>' % (_S, _S, _F),
    "key": '<circle cx="7.6" cy="16.4" r="3.6" %s/>'
           '<path d="m10.2 13.8 9.6-9.6M16.4 7.6l2.4 2.4M13.8 10.2l2.4 2.4" %s/>' % (_S, _S),
    "road": '<path d="M7.6 3.4 4.6 20.6M16.4 3.4l3 17.2" %s/>'
            '<path d="M12 4v2.8M12 10.6v2.8M12 17.4v3.2" %s/>' % (_S, _S),
    "tag": '<path d="M20.2 12.6 12.6 20.2a2 2 0 0 1-2.8 0l-6.6-6.6a2 2 0 0 1-.6-1.4V4.6a2 2 0 0 1 2-2h7.6a2 2 0 0 1 1.4.6l6.6 6.6a2 2 0 0 1 0 2.8Z" %s/>'
           '<circle cx="7.8" cy="7.8" r="1.5" %s/>' % (_S, _S),
    "rupee": '<path d="M7 4.6h10M7 8.6h10" %s/>'
             '<path d="M7 4.6h3.6a4 4 0 0 1 0 8H7l8.6 7.4" %s/>' % (_S, _S),
    "percent": '<path d="M19.4 4.6 4.6 19.4" %s/><circle cx="7.6" cy="7.6" r="3" %s/>'
               '<circle cx="16.4" cy="16.4" r="3" %s/>' % (_S, _S, _S),
    "wallet": '<rect x="2.6" y="5.6" width="18.8" height="14" rx="2.6" %s/>'
              '<path d="M2.6 10.4h18.8M16.6 15.2h2" %s/>' % (_S, _S),
    "chart": '<path d="M3.4 20.6h17.2" %s/>'
             '<path d="M6.8 20.6v-5.4M11.4 20.6V9.4M16 20.6v-8M20.6 20.6V4.8" %s/>' % (_S, _S),
    "clipboard": '<path d="M9 4.4H7a2 2 0 0 0-2 2v12.2a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V6.4a2 2 0 0 0-2-2h-2" %s/>'
                 '<rect x="9" y="2.6" width="6" height="3.6" rx="1.2" %s/>'
                 '<path d="m9.2 13 2.2 2.2 4-4.4" %s/>' % (_S, _S, _S),
    "truck": '<path d="M2.6 6.6h11v10.2h-11z" %s/>'
             '<path d="M13.6 10.4h3.8l3 3.2v3.2h-6.8" %s/>'
             '<circle cx="7" cy="18.4" r="1.9" %s/><circle cx="17" cy="18.4" r="1.9" %s/>' % (_S, _S, _S, _S),
    "snow": '<path d="M12 2.6v18.8M3.9 7.3l16.2 9.4M20.1 7.3 3.9 16.7" %s/>'
            '<path d="M9.4 4.6 12 7.2l2.6-2.6M9.4 19.4 12 16.8l2.6 2.6" %s/>' % (_S, _T),
    "screen": '<rect x="2.6" y="4.4" width="18.8" height="12.4" rx="2.2" %s/>'
              '<path d="M8.4 20.6h7.2M12 16.8v3.8" %s/>' % (_S, _S),
    "users": '<circle cx="9.2" cy="8.2" r="3.6" %s/><path d="M2.8 20.6a6.4 6.4 0 0 1 12.8 0" %s/>'
             '<path d="M16.4 4.9a3.6 3.6 0 0 1 0 6.9M17.6 14.6a6.4 6.4 0 0 1 3.6 5.8" %s/>' % (_S, _S, _S),
    "briefcase": '<rect x="2.6" y="7.4" width="18.8" height="13.2" rx="2.2" %s/>'
                 '<path d="M8.6 7.4V5.6a2 2 0 0 1 2-2h2.8a2 2 0 0 1 2 2v1.8M2.6 13h18.8" %s/>' % (_S, _S),
}

# Names generate_site.py hard-codes. icon() raises on a miss rather than
# rendering nothing, so a rename here fails the build loudly instead of
# quietly leaving holes in the pages.
REQUIRED = ("arrow-right", "chevron-down", "chevron-right", "check", "close",
            "plus", "minus", "star", "quote", "play", "palette",
            "phone", "mail", "map-pin", "clock", "send", "calendar",
            "whatsapp", "car", "steering", "wrench", "certificate")


def icon(name, cls="", extra=""):
    """Return a complete inline <svg> for the named icon."""
    body = ICONS.get(name)
    if body is None:
        raise KeyError("Unknown icon: %s (known: %s)"
                       % (name, ", ".join(sorted(ICONS))))
    cls_attr = ' class="%s"' % cls if cls else ""
    return ('<svg viewBox="0 0 24 24"%s aria-hidden="true" focusable="false"%s>%s</svg>'
            % (cls_attr, (" " + extra) if extra else "", body))


def check_required():
    missing = [n for n in REQUIRED if n not in ICONS]
    if missing:
        raise KeyError("gen_icons.py is missing required icons: %s"
                       % ", ".join(missing))
    return True
