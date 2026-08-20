"""
gen_cars.py  —  V3
Side-profile car silhouettes, drawn by hand as SVG.

Why illustrations and not photographs: we are not Maruti Suzuki and cannot ship
their official product photography, and a generic stock photo of some other
manufacturer's car sitting under the word "Swift" would mislead a buyer. A clean
body-type silhouette is honest, stays sharp at any size, weighs nothing, and is
how most car configurators present a line-up anyway.

Every drawing uses the same 200x84 viewBox, the same wheel positions and the
same sill height, so the whole range reads as one family when the cards sit side
by side. Swap any of them for official Maruti media-kit photography from the
admin panel — the markup already supports it.

V2: closed body outlines with real wheel-arch cutouts, replacing V1's open
strokes which left hooks at the bumpers and ran straight through the wheels.
V3: car_art() takes an optional label. Unlabelled, the drawing is marked
aria-hidden, because it duplicates the model name sitting next to it. Labelled,
it carries role="img" and a <title> that says plainly that this is an
illustration of a body type — a screen-reader user should not be told there is
a photograph of a car here when there is not.
"""

# Shared geometry — change here and the whole range stays consistent.
REAR_X, FRONT_X, AXLE_Y, TYRE_R = 52, 150, 64, 13

_WHEELS = (
    '<g fill="none" stroke="currentColor" stroke-width="4.5">'
    '<circle cx="%d" cy="%d" r="%d"/><circle cx="%d" cy="%d" r="%d"/></g>'
    '<g fill="currentColor" opacity=".25">'
    '<circle cx="%d" cy="%d" r="4.6"/><circle cx="%d" cy="%d" r="4.6"/></g>'
) % (REAR_X, AXLE_Y, TYRE_R, FRONT_X, AXLE_Y, TYRE_R,
     REAR_X, AXLE_Y, FRONT_X, AXLE_Y)

# Lower edge: sill, up and over the rear wheel, sill, up and over the front
# wheel, sill. Arch radius is bigger than the tyre so the rubber clears it.
_SILLS = ("L 36 70 A 16 16 0 0 1 68 70 "
          "L 134 70 A 16 16 0 0 1 166 70 ")

_BODY = ('fill="none" stroke="currentColor" stroke-width="4.5" '
         'stroke-linejoin="round"')
_GLASS = 'fill="currentColor" opacity=".15" stroke="none"'
_PILLAR = ('fill="none" stroke="currentColor" stroke-width="2.4" '
           'stroke-linecap="round" opacity=".45"')
_CLAD = ('fill="none" stroke="currentColor" stroke-width="6" '
         'stroke-linecap="round" opacity=".22"')


_RAIL = ('fill="none" stroke="currentColor" stroke-width="4" '
         'stroke-linecap="round" opacity=".7"')


def _car(outline, glass, pillars="", cladding="", roofrail=""):
    """Returns the drawing with a %s placeholder for the accessibility
    attributes, filled in by car_art()."""
    return ('<svg class="car-art" viewBox="0 0 200 84" %s'
            'preserveAspectRatio="xMidYMid meet">%s'
            '<path d="M 14 70 ' + _SILLS + ' L 184 70 ' + outline + ' Z" ' + _BODY + '/>'
            '<path d="' + glass + '" ' + _GLASS + '/>'
            + (('<path d="%s" %s/>' % (pillars, _PILLAR)) if pillars else "")
            + (('<path d="%s" %s/>' % (cladding, _CLAD)) if cladding else "")
            + (('<path d="%s" %s/>' % (roofrail, _RAIL)) if roofrail else "")
            + _WHEELS + '</svg>')


# --------------------------------------------------------------- HATCHBACK --
# Swift, Baleno, Celerio, Alto K10. Low roof, short tail, steep tailgate.
HATCHBACK = _car(
    outline=("C 190 70 193 67 193 61 L 192 52 C 191 46 187 43 181 42 "
             "L 152 38 L 130 21 C 126 18 121 17 115 17 L 82 17 "
             "C 74 17 68 19 63 24 L 48 41 L 22 45 C 16 46 13 50 13 56 L 14 70"),
    glass="M 70 39 L 82 22 C 86 20 90 20 96 20 L 113 20 C 118 20 122 21 125 24 L 143 39 Z",
    pillars="M 100 20 L 100 39")

# ---------------------------------------------------------------- TALL HATCH --
# WagonR, S-Presso. Upright screen, flat roof, near-vertical tailgate.
TALL_HATCH = _car(
    outline=("C 190 70 193 67 193 61 L 192 52 C 191 46 187 43 181 42 "
             "L 156 38 L 143 18 C 140 14 135 12 128 12 L 76 12 "
             "C 68 12 63 15 60 21 L 50 40 L 20 44 C 15 45 13 49 13 55 L 14 70"),
    glass="M 66 38 L 74 20 C 76 16 80 15 85 15 L 126 15 C 131 15 134 16 136 20 L 148 38 Z",
    pillars="M 104 15 L 104 38")

# ------------------------------------------------------------------- SEDAN --
# Dzire. Three-box: bonnet, cabin, then a separate boot with a deck line.
SEDAN = _car(
    outline=("C 190 70 193 67 193 61 L 192 52 C 191 46 187 43 181 42 "
             "L 152 38 L 132 21 C 128 18 123 17 117 17 L 90 17 "
             "C 83 17 78 19 74 24 L 62 37 "      # rear screen
             "L 24 39 "                          # flat boot deck
             "C 16 39 12 43 12 51 L 14 70"),     # upright tail
    glass="M 78 37 L 88 22 C 91 20 95 20 100 20 L 115 20 C 120 20 124 21 127 24 L 145 37 Z",
    pillars="M 104 20 L 104 37")

# ------------------------------------------------------------- COMPACT SUV --
# Brezza, Fronx. Raised stance, black cladding, short overhangs.
COMPACT_SUV = _car(
    outline=("C 187 70 190 66 190 60 L 189 49 C 188 43 184 40 178 39 "
             "L 152 35 L 131 18 C 127 15 122 14 116 14 L 82 14 "
             "C 74 14 68 16 63 22 L 49 38 L 24 42 C 18 43 15 47 15 53 L 14 70"),
    glass="M 70 36 L 81 19 C 85 17 89 17 94 17 L 114 17 C 119 17 123 18 126 21 L 143 36 Z",
    pillars="M 102 17 L 102 36",
    cladding="M 22 57 L 36 57 M 164 57 L 180 57")

# ----------------------------------------------------------------- MID SUV --
# Grand Vitara, Victoris, e Vitara. Longer, squarer shoulder, roof rails.
MID_SUV = _car(
    outline=("C 191 70 194 66 194 60 L 193 46 C 192 40 188 37 182 36 "
             "L 158 32 L 138 15 C 134 12 129 11 123 11 L 76 11 "
             "C 68 11 62 13 57 19 L 44 35 L 18 39 C 12 40 9 44 9 50 L 14 70"),
    glass="M 66 33 L 78 16 C 82 14 86 14 91 14 L 121 14 C 126 14 130 15 133 18 L 149 33 Z",
    pillars="M 100 14 L 100 33",
    cladding="M 18 55 L 34 55 M 168 55 L 186 55",
    roofrail="M 66 9 L 132 9")

# --------------------------------------------------------------- OFFROADER --
# Jimny. Flat roof, vertical screen, square arches, upright everything.
OFFROADER = _car(
    outline=("C 190 70 193 66 193 60 L 193 40 C 193 34 189 31 183 31 "
             "L 158 30 L 152 15 C 150 12 146 11 141 11 L 63 11 "
             "C 56 11 52 13 50 18 L 44 30 L 20 31 C 14 31 11 35 11 41 L 14 70"),
    glass="M 56 30 L 62 17 C 64 15 66 14 70 14 L 139 14 C 143 14 145 15 146 18 L 151 30 Z",
    pillars="M 92 14 L 92 30 M 120 14 L 120 30",
    cladding="M 18 54 L 36 54 M 166 54 L 186 54")

# --------------------------------------------------------------------- MPV --
# Ertiga, XL6, Invicto. One-and-a-half box, long glasshouse, three rows.
MPV = _car(
    outline=("C 191 70 194 66 194 60 L 193 48 C 192 42 188 39 182 38 "
             "L 162 34 L 142 15 C 138 12 133 11 126 11 L 72 11 "
             "C 64 11 58 14 54 20 L 42 37 L 18 41 C 12 42 9 46 9 52 L 14 70"),
    glass="M 64 35 L 76 17 C 79 15 83 14 88 14 L 124 14 C 129 14 133 15 136 18 L 152 35 Z",
    pillars="M 92 14 L 92 35 M 120 14 L 120 35")

# --------------------------------------------------------------------- VAN --
# Eeco. Cab-forward, near-vertical nose, tall slab side, huge glass area.
VAN = _car(
    outline=("C 191 70 194 66 194 58 L 192 38 C 191 28 185 22 174 21 "
             "L 44 18 C 30 18 22 24 21 35 L 19 44 C 13 45 10 49 10 55 L 14 70"),
    glass="M 30 36 C 31 27 35 24 43 24 L 88 25 L 88 36 Z "
          "M 96 25 L 168 27 C 176 27 180 30 181 37 L 96 36 Z",
    pillars="M 92 25 L 92 36",
    cladding="M 26 56 L 44 56")

BODY_ART = {
    "hatchback": HATCHBACK,
    "tall-hatch": TALL_HATCH,
    "sedan": SEDAN,
    "compact-suv": COMPACT_SUV,
    "mid-suv": MID_SUV,
    "offroader": OFFROADER,
    "mpv": MPV,
    "van": VAN,
}

BODY_LABEL = {
    "hatchback": "Hatchback",
    "tall-hatch": "Tall-boy hatchback",
    "sedan": "Sedan",
    "compact-suv": "Compact SUV",
    "mid-suv": "SUV",
    "offroader": "Off-roader",
    "mpv": "MPV",
    "van": "Van",
}


def car_art(body, label=None):
    """Return the silhouette SVG for a body type.

    label=None  -> aria-hidden, for the common case where the model name is
                   already sitting next to the drawing.
    label="…"   -> role="img" plus a <title>. Pass the model name; the words
                   "body profile illustration" are appended so nobody is told
                   there is a photograph here.
    """
    try:
        art = BODY_ART[body]
    except KeyError:
        raise KeyError("Unknown body type %r. Known: %s"
                       % (body, ", ".join(sorted(BODY_ART))))
    if label:
        title = "%s — %s body profile illustration" % (label, body_label(body).lower())
        return art % ('role="img" ',
                      "<title>%s</title>" % _escape(title))
    return art % ('aria-hidden="true" focusable="false" ', "")


def _escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def body_label(body):
    return BODY_LABEL.get(body, body.replace("-", " ").title())
