# -*- coding: utf-8 -*-
"""Shared assets: SVG illustration system + page shell partials."""

import os as _os

# ============================================================================
# SVG ILLUSTRATION SYSTEM
# ----------------------------------------------------------------------------
# No photography exists yet (Doc 1, 6.6 / Doc 2, Section 16 items 7-8).
# Rather than stock imagery — which would collapse the premium proposition —
# every image slot is filled with a generated CAD-style technical drawing.
# Each has a WIREFRAME layer and a RENDERED layer; the card hover crossfades
# between them. This is the signature interaction from Doc 1, 6.7.
# These are drop-in replacements: swap the <svg> for an <img> when photography
# lands, and the .wf__line / .wf__solid classes keep working.
# ============================================================================

_UID = [0]


def _nid(prefix):
    _UID[0] += 1
    return f"{prefix}{_UID[0]}"


GRID_DEFS = """<defs>
<pattern id="g{u}" width="16" height="16" patternUnits="userSpaceOnUse">
<path d="M16 0H0V16" fill="none" stroke="#E5E5E3" stroke-width="0.5"/></pattern>
<linearGradient id="sky{u}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#2A2A2A"/><stop offset="1" stop-color="#454545"/></linearGradient>
</defs>"""


def _shell(u, body, bg="#FAFAF9"):
    return (f'<svg viewBox="0 0 400 300" xmlns="http://www.w3.org/2000/svg" '
            f'role="img" aria-hidden="true" preserveAspectRatio="xMidYMid slice">'
            f'{GRID_DEFS.replace("{u}", u)}'
            f'<rect width="400" height="300" fill="{bg}"/>'
            f'<rect width="400" height="300" fill="url(#g{u})"/>{body}</svg>')


def _dims(u):
    """Drafting dimension marks — the recurring annotation motif."""
    return ('<g stroke="#8A8A8A" stroke-width="0.75" opacity="0.75">'
            '<path d="M24 274h352M24 270v8M376 270v8"/>'
            '<path d="M14 34v212M10 34h8M10 246h8"/></g>'
            '<g fill="#8A8A8A" font-family="monospace" font-size="7" opacity="0.85">'
            '<text x="188" y="286">SCALE 1:100</text></g>')


def wire(kind, u):
    """Wireframe (line-drawing) layer."""
    s = 'fill="none" stroke="#141414" stroke-width="1.1" stroke-linejoin="round"'
    t = 'fill="none" stroke="#D42027" stroke-width="1.1"'
    if kind == "bim":
        b = (f'<g {s}><path d="M96 232V108l104-52 104 52v124"/>'
             f'<path d="M96 108h208M96 150h208M96 192h208"/>'
             f'<path d="M148 232v-42h44v42M226 232v-42h44v42"/>'
             f'<path d="M130 122h40v18h-40zM230 122h40v18h-40zM130 164h40v18h-40zM230 164h40v18h-40z"/>'
             f'<path d="M200 56v176"/></g>'
             f'<g {t}><circle cx="200" cy="150" r="7"/><path d="M200 138v24M188 150h24"/></g>')
    elif kind == "civil":
        b = (f'<g {s}><path d="M20 208c60-46 120 24 190-16s110-38 170-6"/>'
             f'<path d="M20 240c60-46 120 24 190-16s110-38 170-6"/>'
             f'<path d="M20 176c60-46 120 24 190-16s110-38 170-6" stroke-dasharray="5 5"/></g>'
             f'<g {s} opacity="0.5"><path d="M60 120v104M140 96v128M220 128v96M300 100v124"/></g>'
             f'<g {t}><path d="M20 192c60-46 120 24 190-16s110-38 170-6" stroke-dasharray="9 5"/></g>')
    elif kind == "mech":
        b = (f'<g {s}><circle cx="200" cy="150" r="66"/><circle cx="200" cy="150" r="30"/>'
             f'<circle cx="200" cy="150" r="14"/>'
             f'<path d="M200 84v-18M200 234v18M134 150h-18M284 150h18"/>'
             f'<circle cx="200" cy="98" r="7"/><circle cx="200" cy="202" r="7"/>'
             f'<circle cx="148" cy="150" r="7"/><circle cx="252" cy="150" r="7"/>'
             f'<path d="M158 108l84 84M242 108l-84 84" stroke-dasharray="4 4" opacity="0.55"/></g>'
             f'<g {t}><path d="M200 60v180M110 150h180" stroke-dasharray="9 5" opacity="0.85"/></g>')
    elif kind == "struct":
        b = (f'<g {s}><path d="M70 240V80h260v160"/>'
             f'<path d="M70 133h260M70 186h260M135 80v160M200 80v160M265 80v160"/>'
             f'<path d="M70 80l65 53M135 133l65-53M200 80l65 53M265 133l65-53" opacity="0.55"/>'
             f'<path d="M60 240h280"/></g>'
             f'<g {t}><path d="M100 62v14M180 62v14M260 62v14M320 62v14"/>'
             f'<path d="M96 76l4 6 4-6M176 76l4 6 4-6M256 76l4 6 4-6M316 76l4 6 4-6" fill="#D42027"/></g>')
    elif kind == "mep":
        b = (f'<g {s}><path d="M40 96h150v54h130v96"/>'
             f'<path d="M40 132h114v118M226 96h134"/>'
             f'<circle cx="190" cy="96" r="6"/><circle cx="154" cy="132" r="6"/>'
             f'<circle cx="320" cy="150" r="6"/><circle cx="226" cy="96" r="6"/></g>'
             f'<g {t}><path d="M40 210h110M40 240h110" stroke-dasharray="7 4"/>'
             f'<rect x="150" y="196" width="46" height="58" rx="1"/></g>')
    elif kind == "arch":
        b = (f'<g {s}><path d="M60 240V128l140-72 140 72v112"/>'
             f'<path d="M60 128h280"/>'
             f'<path d="M120 240v-68h48v68M232 240v-68h48v68"/>'
             f'<path d="M176 150h48v34h-48z"/>'
             f'<path d="M60 240h280"/></g>'
             f'<g {t}><path d="M200 40v28M186 54l14-14 14 14"/></g>')
    elif kind == "pm":
        rows = ""
        bars = [(60, 150), (90, 200), (120, 120), (150, 240), (180, 90)]
        for i, (y, w) in enumerate(bars):
            rows += f'<rect x="{60 + i*14}" y="{y}" width="{w}" height="16" fill="none" stroke="#141414" stroke-width="1.1"/>'
        b = (f'<g>{rows}</g><g {s} opacity="0.4"><path d="M60 44v212M130 44v212M200 44v212M270 44v212M340 44v212"/></g>'
             f'<g {t}><path d="M245 40v220" stroke-dasharray="6 4"/></g>')
    else:  # ai / default
        b = (f'<g {s}><circle cx="130" cy="150" r="10"/><circle cx="200" cy="96" r="10"/>'
             f'<circle cx="200" cy="204" r="10"/><circle cx="272" cy="150" r="10"/>'
             f'<path d="M138 143l54-40M138 157l54 40M210 100l54 42M210 200l54-42"/>'
             f'<rect x="60" y="120" width="42" height="60"/><rect x="300" y="120" width="42" height="60"/></g>'
             f'<g {t}><circle cx="200" cy="150" r="26"/><path d="M186 150h28M200 136v28"/></g>')
    return _shell(u, b + _dims(u))


def solid(kind, u):
    """Rendered layer — the same object, materialised."""
    ink, acc, mid, lite = "#141414", "#D42027", "#5A5A5A", "#D8D8D6"
    if kind == "bim":
        b = (f'<rect x="96" y="108" width="208" height="124" fill="{ink}"/>'
             f'<path d="M96 108l104-52 104 52z" fill="{mid}"/>'
             f'<g fill="#FFF" opacity="0.9"><rect x="130" y="122" width="40" height="18"/>'
             f'<rect x="230" y="122" width="40" height="18"/><rect x="130" y="164" width="40" height="18"/>'
             f'<rect x="230" y="164" width="40" height="18"/></g>'
             f'<rect x="148" y="190" width="44" height="42" fill="{acc}"/>'
             f'<rect x="226" y="190" width="44" height="42" fill="#FFF" opacity="0.85"/>')
    elif kind == "civil":
        b = (f'<path d="M20 208c60-46 120 24 190-16s110-38 170-6v58H20z" fill="{ink}"/>'
             f'<path d="M20 192c60-46 120 24 190-16s110-38 170-6" stroke="{acc}" stroke-width="3" fill="none"/>'
             f'<path d="M20 176c60-46 120 24 190-16s110-38 170-6v22c-60-32-100-34-170 6s-130-30-190 16z" fill="{mid}"/>')
    elif kind == "mech":
        b = (f'<circle cx="200" cy="150" r="66" fill="{ink}"/>'
             f'<circle cx="200" cy="150" r="30" fill="{lite}"/><circle cx="200" cy="150" r="14" fill="{acc}"/>'
             f'<g fill="{lite}"><circle cx="200" cy="98" r="7"/><circle cx="200" cy="202" r="7"/>'
             f'<circle cx="148" cy="150" r="7"/><circle cx="252" cy="150" r="7"/></g>')
    elif kind == "struct":
        b = (f'<g fill="{ink}"><rect x="70" y="80" width="12" height="160"/><rect x="129" y="80" width="12" height="160"/>'
             f'<rect x="194" y="80" width="12" height="160"/><rect x="259" y="80" width="12" height="160"/>'
             f'<rect x="318" y="80" width="12" height="160"/></g>'
             f'<g fill="{mid}"><rect x="70" y="80" width="260" height="11"/>'
             f'<rect x="70" y="128" width="260" height="11"/><rect x="70" y="181" width="260" height="11"/></g>'
             f'<rect x="60" y="240" width="280" height="9" fill="{acc}"/>')
    elif kind == "mep":
        b = (f'<g stroke="{ink}" stroke-width="7" fill="none" stroke-linecap="round">'
             f'<path d="M40 96h150v54h130v96"/><path d="M40 132h114v118"/></g>'
             f'<g stroke="{acc}" stroke-width="7" fill="none" stroke-linecap="round">'
             f'<path d="M40 210h110M40 240h110"/></g>'
             f'<rect x="150" y="196" width="46" height="58" fill="{mid}"/>')
    elif kind == "arch":
        b = (f'<path d="M60 128l140-72 140 72z" fill="{acc}"/>'
             f'<rect x="60" y="128" width="280" height="112" fill="{ink}"/>'
             f'<g fill="#FFF" opacity="0.88"><rect x="120" y="172" width="48" height="68"/>'
             f'<rect x="232" y="172" width="48" height="68"/><rect x="176" y="150" width="48" height="34"/></g>')
    elif kind == "pm":
        cols = [acc, ink, mid, ink, lite]
        b = "".join(f'<rect x="{60 + i*14}" y="{y}" width="{w}" height="16" fill="{cols[i]}"/>'
                    for i, (y, w) in enumerate([(60, 150), (90, 200), (120, 120), (150, 240), (180, 90)]))
        b += f'<path d="M245 40v220" stroke="{acc}" stroke-width="2" stroke-dasharray="6 4"/>'
    else:
        b = (f'<g fill="{ink}"><circle cx="130" cy="150" r="10"/><circle cx="200" cy="96" r="10"/>'
             f'<circle cx="200" cy="204" r="10"/><circle cx="272" cy="150" r="10"/></g>'
             f'<g stroke="{mid}" stroke-width="2"><path d="M138 143l54-40M138 157l54 40M210 100l54 42M210 200l54-42"/></g>'
             f'<circle cx="200" cy="150" r="26" fill="{acc}"/>')
    return _shell(u, b + _dims(u), bg="#F2F2F0")


def figure(kind, badge="wireframe"):
    """A card media block with both layers + the state badge."""
    return (f'<div class="card__media"><div class="wf">'
            f'<div class="wf__line">{wire(kind, _nid("w"))}</div>'
            f'<div class="wf__solid">{solid(kind, _nid("s"))}</div>'
            f'<span class="wf__badge">{badge}</span></div></div>')


def hero_bg():
    """Ambient technical drawing behind the hero."""
    return ('<svg viewBox="0 0 1440 700" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" '
            'preserveAspectRatio="xMidYMid slice">'
            '<defs><pattern id="hg" width="40" height="40" patternUnits="userSpaceOnUse">'
            '<path d="M40 0H0V40" fill="none" stroke="#6E6E6E" stroke-width="0.5"/></pattern></defs>'
            '<rect width="1440" height="700" fill="#141414"/>'
            '<rect width="1440" height="700" fill="url(#hg)"/>'
            '<g fill="none" stroke="#C9C9C9" stroke-width="1.2" opacity="0.55">'
            '<path d="M840 620V300l220-120 220 120v320"/>'
            '<path d="M840 300h440M840 380h440M840 460h440M840 540h440"/>'
            '<path d="M1060 180v440"/>'
            '<path d="M900 322h80v42h-80zM1140 322h80v42h-80zM900 402h80v42h-80zM1140 402h80v42h-80z"/>'
            '<path d="M900 482h80v42h-80zM1140 482h80v42h-80z"/></g>'
            '<g fill="none" stroke="#D42027" stroke-width="1.4" opacity="0.9">'
            '<circle cx="1060" cy="380" r="14"/><path d="M1060 356v48M1036 380h48"/></g>'
            '<g fill="none" stroke="#8A8A8A" stroke-width="0.8" opacity="0.6">'
            '<path d="M840 660h440M840 652v16M1280 652v16"/></g>'
            '<g fill="#8A8A8A" font-family="monospace" font-size="13" opacity="0.75">'
            '<text x="1020" y="682">44.0 M</text></g>'
            '<g fill="none" stroke="#4A4A4A" stroke-width="1" opacity="0.5">'
            '<path d="M120 560c120-90 240 40 360-30s220-70 340-12"/>'
            '<path d="M120 610c120-90 240 40 360-30s220-70 340-12"/></g>'
            '</svg>')



# ============================================================================
# PHOTOGRAPHY
# ----------------------------------------------------------------------------
# Real image slots, emitted by build_images.py as responsive AVIF + WebP.
# Every slot carries a tier:
#   A = work/objects only, no identifiable people   -> no caption required
#   B = labelled illustrative project output        -> caption required
#   C = depicts people                              -> caption required
# Captions are visible, not hidden in alt text, because the whole positioning
# rests on proof over claim. An unlabelled synthetic photo would undercut it.
# ============================================================================

from image_manifest import IMAGES

WIDTHS = [480, 960, 1600]


def _widths_on_disk(stem, ext):
    """Widths actually emitted for this slot, read from the filenames rather
    than assumed. A small source gets a native-width rung that is not on the
    standard ladder, and the srcset has to advertise it or it goes unused."""
    import os, re, glob
    here = os.path.dirname(os.path.abspath(__file__))
    pat = os.path.join(here, "assets/img", f"{stem}-*.{ext}")
    out = []
    for p in glob.glob(pat):
        m = re.fullmatch(re.escape(stem) + r"-(\d+)\." + re.escape(ext),
                         os.path.basename(p))
        if m:
            out.append(int(m.group(1)))
    return sorted(out)


def _srcset(stem, ext):
    return ", ".join(f"{{up}}assets/img/{stem}-{w}.{ext} {w}w"
                     for w in _widths_on_disk(stem, ext))


def _largest(stem, ext="webp"):
    have = _widths_on_disk(stem, ext)
    return max(have) if have else None


def photo(slot, depth=0, sizes="(max-width: 767px) 100vw, 50vw", cls="", eager=False):
    """A responsive picture element. Returns '' if the slot has no asset."""
    if slot not in IMAGES:
        return ""
    m = IMAGES[slot]
    up = "../" * depth
    fallback = _largest(slot)
    if fallback is None:
        return ""
    avif = _srcset(slot, "avif").replace("{up}", up)
    webp = _srcset(slot, "webp").replace("{up}", up)
    loading = 'loading="eager" fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<picture class="{cls}">'
            f'<source type="image/avif" srcset="{avif}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{webp}" sizes="{sizes}">'
            f'<img src="{up}assets/img/{slot}-{fallback}.webp" alt="{m["alt"]}" '
            f'width="{m["w"]}" height="{m["h"]}" {loading}>'
            f'</picture>')


def photo_card(slot, depth=0, badge=None, sizes="(max-width: 767px) 100vw, 33vw"):
    """Card media block backed by a real image, with its provenance label."""
    if slot not in IMAGES:
        return ""
    m = IMAGES[slot]
    label = badge if badge is not None else m.get("caption", "")
    tag = f'<span class="wf__badge">{label}</span>' if label else ""
    return (f'<div class="card__media card__media--photo">'
            f'{photo(slot, depth, sizes)}{tag}</div>')


# ============================================================================
# ICON SET — Lucide-style line icons, inline SVG.
# Stroke-based so they inherit currentColor and stay crisp at any size.
# ============================================================================
_I = ('<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
      'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">')

ICONS = {
 "badge":     _I + '<path d="M12 2l2.6 1.9 3.2-.1.9 3.1 2.6 1.9-1.2 3 1.2 3-2.6 1.9-.9 3.1-3.2-.1L12 22l-2.6-1.9-3.2.1-.9-3.1L2.7 15l1.2-3-1.2-3 2.6-1.9.9-3.1 3.2.1z"/><path d="M9 12l2 2 4-4"/></svg>',
 "hands":     _I + '<path d="M3 12h4l2-7 4 14 2-7h6"/></svg>',
 "mentor":    _I + '<circle cx="12" cy="8" r="3.2"/><path d="M5 21a7 7 0 0114 0"/></svg>',
 "shield":    _I + '<path d="M12 3l7 3v5c0 4.4-3 8.3-7 10-4-1.7-7-5.6-7-10V6z"/><path d="M9 12l2 2 4-4"/></svg>',
 "star":      _I + '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg>',
 "calendar":  _I + '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
 "pin":       _I + '<path d="M12 21s7-5.6 7-11a7 7 0 10-14 0c0 5.4 7 11 7 11z"/><circle cx="12" cy="10" r="2.6"/></svg>',
 "clock":     _I + '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/></svg>',
 "cap":       _I + '<path d="M2 9l10-4 10 4-10 4z"/><path d="M6 11.5V17c0 1.7 2.7 3 6 3s6-1.3 6-3v-5.5"/></svg>',
 "rocket":    _I + '<path d="M5 15c-1.5 1.5-2 6-2 6s4.5-.5 6-2a3 3 0 10-4-4z"/><path d="M9 12l3-5a9 9 0 017-4 9 9 0 01-4 7l-5 3z"/><path d="M12 12l3 3"/></svg>',
 "briefcase": _I + '<rect x="2.5" y="7" width="19" height="13" rx="2"/><path d="M9 7V5a2 2 0 012-2h2a2 2 0 012 2v2M2.5 12h19"/></svg>',
 "building":  _I + '<rect x="4" y="3" width="16" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2"/></svg>',
 "book":      _I + '<path d="M4 5a2 2 0 012-2h13v18H6a2 2 0 01-2-2z"/><path d="M8 7h7M8 11h7"/></svg>',
 "layers":    _I + '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5M3 17l9 5 9-5"/></svg>',
 "users":     _I + '<circle cx="9" cy="8" r="3"/><path d="M2.5 20a6.5 6.5 0 0113 0"/><path d="M16 5.2a3 3 0 010 5.6M17 14.4a6.5 6.5 0 014.5 5.6"/></svg>',
 "target":    _I + '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/></svg>',
 "mic":       _I + '<rect x="9" y="3" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0014 0M12 18v3"/></svg>',
 "infinity":  _I + '<path d="M7 12a3 3 0 100-.1M17 12a3 3 0 100-.1"/><path d="M9.9 12c1 1.7 1.9 3.5 4.1 3.5a3.5 3.5 0 000-7c-2.2 0-3.1 1.8-4.1 3.5-1 1.7-1.9 3.5-4.1 3.5a3.5 3.5 0 010-7c2.2 0 3.1 1.8 4.1 3.5z"/></svg>',
 "check":     _I + '<circle cx="12" cy="12" r="9"/><path d="M8.5 12.2l2.4 2.4 4.6-4.8"/></svg>',
 "arrow":     _I + '<path d="M4 12h15M13 6l6 6-6 6"/></svg>',
}


def icon(name, cls=""):
    svg = ICONS.get(name, ICONS["check"])
    return svg.replace('class="ico"', f'class="ico {cls}"') if cls else svg



# Home-page hero slideshow.
#   stem   filename prefix; crops are {stem}-{wide|mid|tall}-{width}.{ext}
#   alt    only the first slide carries alt text — the rest repeat the same
#          idea, so describing each one again would just be noise in a screen
#          reader. They are marked decorative instead.
HERO_SLIDES = [
    ("hero",
     "Design studio overlooking a city skyline, with drawings, a scale model "
     "and building models on screen"),
    # Supplied by the centre. Ordered so the disciplines alternate rather than
    # showing two building shots or two mechanical shots back to back.
    ("hero-arch", ""),     # BIM workstation, building model on screen
    ("hero-mech", ""),     # mechanical assembly on screen, machined parts on the desk
    ("hero-tower", ""),    # construction model reviewed against a real skyline
    ("hero-sim", ""),      # exploded assembly and analysis
    ("hero-infra", ""),    # infrastructure plan over a real corridor
    ("hero-studio", ""),
    ("hero-floor", ""),
]

# Candidate widths per crop. Anything without a file on disk is dropped, so a
# slide built from a smaller source simply offers fewer sizes rather than
# pointing at a 404.
_HERO_WIDTHS = {
    "wide": (768, 1280, 1600, 1920, 2560),
    "mid":  (600, 1024, 1200, 1536),
    "tall": (390, 675, 700, 780, 1170),
}
_HERO_RATIO = {"wide": (1920, 1080), "mid": (1536, 1152), "tall": (1170, 1560)}
_PIXEL = ("data:image/gif;base64,"
          "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")


def hero_picture(depth=0):
    """Art-directed, cross-fading hero.

    Three separate crops per slide rather than one image squeezed by
    object-fit:
      >=1024px  16:9  full scene
      600-1023  4:3   tighter
      <600px    3:4   portrait, so a phone shows the subject and not a sliver

    Every source declares its own intrinsic ratio, so the browser reserves the
    right box before the bytes arrive — no layout shift at any width.

    Only the first slide is fetched by the browser. The rest carry their URLs
    in data- attributes and are promoted by initHeroSlides() once the page has
    loaded, so the hero image stays the uncontested LCP candidate and a visitor
    on mobile data never pays for slides they may not sit still long enough to
    see. With JavaScript off, the first slide is simply a static hero.
    """
    up = "../" * depth
    here = _os.path.dirname(_os.path.abspath(__file__))

    def have(stem, variant):
        return tuple(w for w in _HERO_WIDTHS[variant]
                     if _os.path.exists(_os.path.join(
                         here, "assets/img", f"{stem}-{variant}-{w}.avif")))

    def srcset(stem, variant, widths, ext):
        return ", ".join(
            f"{up}assets/img/{stem}-{variant}-{w}.{ext} {w}w" for w in widths)

    slides = ""
    for i, (stem, alt) in enumerate(HERO_SLIDES):
        wide, mid, tall = (have(stem, v) for v in ("wide", "mid", "tall"))
        if not wide:
            continue
        first = i == 0
        # Deferred slides keep their URLs out of src/srcset so the preload
        # scanner never queues them; the attribute name is the only difference.
        a = "srcset" if first else "data-srcset"
        sources = ""
        for variant, media, widths in (("wide", '(min-width:1024px)', wide),
                                       ("mid",  '(min-width:600px)', mid),
                                       ("tall", "", tall)):
            if not widths:
                continue
            m = f'media="{media}" ' if media else ""
            w, h = _HERO_RATIO[variant]
            for ext, mime in (("avif", "image/avif"), ("webp", "image/webp")):
                sources += (f'<source {m}type="{mime}" '
                            f'{a}="{srcset(stem, variant, widths, ext)}" '
                            f'sizes="100vw" width="{w}" height="{h}">')

        fallback = f'{up}assets/img/{stem}-wide-{wide[min(1, len(wide) - 1)]}.webp'
        if first:
            img = (f'<img src="{fallback}" alt="{alt}" width="1920" height="1080" '
                   f'loading="eager" fetchpriority="high" decoding="async">')
        else:
            # A transparent pixel keeps the element valid while its real URL
            # waits in data-src. Same pixel the preview build uses.
            img = (f'<img src="{_PIXEL}" data-src="{fallback}" alt="" '
                   f'aria-hidden="true" width="1920" height="1080" decoding="async">')

        active = ' data-active="true"' if first else ''
        slides += (f'<div class="hero__slide" data-hero-slide{active}>'
                   f'<picture>{sources}{img}</picture></div>')

    return slides


# ============================================================================
# AUDIENCE CARD ILLUSTRATIONS
# Line-art drawings in the technical-sketch register of the reference: thin
# graphite strokes, one red accent each, generous white space.
# ============================================================================

_L = ('<svg class="cardart" viewBox="0 0 260 150" fill="none" '
      'xmlns="http://www.w3.org/2000/svg" aria-hidden="true">')
_S = 'stroke="#2A2A2A" stroke-width="1" stroke-linejoin="round" stroke-linecap="round"'
_F = 'stroke="#9A9A9A" stroke-width="0.6" stroke-dasharray="3 3"'
_R = 'stroke="#D42027" stroke-width="1.2"'


def card_art(kind):
    if kind == "student":
        # Axonometric block with one red curtain-wall panel
        b = (f'<g {_F}><path d="M16 122h228"/><path d="M74 26v96M186 26v96"/></g>'
             f'<g {_S}>'
             # front face
             f'<path d="M74 122V54h74v68z"/>'
             # side face
             f'<path d="M148 122V54l38-20v68z"/>'
             # roof
             f'<path d="M74 54l38-20h74l-38 20z"/>'
             # front glazing grid
             f'<path d="M74 76h74M74 98h74M99 54v68M124 54v68"/>'
             # side glazing
             f'<path d="M148 76l38-20M148 98l38-20M167 44v68"/>'
             # entrance
             f'<path d="M100 122v-18h22v18"/>'
             f'<path d="M56 122h150"/>'
             f'</g>'
             f'<g {_R}><path d="M99 76h25v22H99z" fill="#D42027" fill-opacity="0.14"/>'
             f'<path d="M99 76h25v22H99z"/></g>'
             f'<g {_F}><path d="M74 134h112M74 130v8M186 130v8"/></g>')
    elif kind == "fresher":
        # Technical dial being set — the "find the right path" idea
        b = (f'<g {_F}><path d="M130 22v106M77 75h106"/>'
             f'<path d="M92 37l76 76M168 37l-76 76"/></g>'
             f'<g {_S}><circle cx="130" cy="75" r="48"/><circle cx="130" cy="75" r="30"/>'
             f'<circle cx="130" cy="75" r="4"/></g>'
             f'<g {_R}><path d="M98 106a46 46 0 0 1-14-40" stroke-linecap="round"/>'
             f'<path d="M162 44a46 46 0 0 1 12 26" stroke-linecap="round"/></g>'
             f'<g {_S}><path d="M170 96l24 26-9 2-4 9z" fill="#fff"/></g>'
             f'<g {_F}><path d="M82 132h96M82 128v8M178 128v8"/></g>')
    elif kind == "professional":
        # Desk: task lamp, monitor showing a model, small plant
        b = (f'<g {_S}>'
             # monitor
             f'<rect x="88" y="32" width="98" height="66" rx="3"/>'
             f'<path d="M126 98v10h22v-10M114 116h46"/>'
             # desk
             f'<path d="M34 116h198"/>'
             # task lamp: base, arm, shade
             f'<path d="M40 116h26M53 116V96"/>'
             f'<path d="M53 96l6-30"/>'
             f'<path d="M52 66l16-6 8 18-16 6z"/>'
             # plant
             f'<path d="M198 116l3-20h20l3 20z"/>'
             f'<path d="M211 96V78"/>'
             f'<path d="M211 84c-8-2-11-8-11-14 6 0 11 4 11 10"/>'
             f'<path d="M211 88c8-3 11-9 11-15-6 0-11 4-11 11"/>'
             f'</g>'
             # model on screen
             f'<g {_S} stroke-width="0.85">'
             f'<path d="M108 84V56h34v28z"/><path d="M108 56l16-9h34l-16 9M142 84l16-9V47"/>'
             f'<path d="M108 68h34M119 56v28"/>'
             f'</g>'
             f'<g {_R}><path d="M142 75l16-9v18l-16 9z" fill="#D42027" fill-opacity="0.12"/>'
             f'<path d="M142 75l16-9v18l-16 9z"/></g>'
             f'<g {_F}><path d="M88 130h98M88 126v8M186 126v8"/></g>')
    else:  # corporate — city elevation
        b = (f'<g {_F}><path d="M14 120h232"/></g>'
             f'<g {_S}>'
             f'<path d="M34 120V78h26v42M60 120V56h24v64M112 120V38h30v82"/>'
             f'<path d="M170 120V62h26v58M196 120V84h22v36"/>'
             f'<path d="M84 120V70h28v50"/>'
             f'<path d="M38 86h18M38 96h18M38 106h18M64 64h16M64 76h16M64 88h16M64 100h16"/>'
             f'<path d="M88 78h20M88 90h20M88 102h20M174 70h18M174 82h18M174 94h18M174 106h18"/>'
             f'<path d="M20 120h220"/>'
             f'</g>'
             f'<g {_R}><path d="M116 120V42h22v78"/><path d="M120 54h14M120 68h14M120 82h14M120 96h14"/></g>'
             f'<g {_F}><path d="M34 132h184M34 128v8M218 128v8"/></g>')
    return _L + b + "</svg>"
