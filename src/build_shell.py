# -*- coding: utf-8 -*-
"""Shared page shell: head, header, mega menus, drawer, footer, advisor."""

PHONE = "+919990707382"
PHONE_D = "+91 99907 07382"
PHONE2_D = "+91 84483 12600"
WHATSAPP = "+918448312600"      # live site: WhatsApp is the SECOND number
WHATSAPP_LINK = "https://wa.link/6u8w51"  # official short link on /contact/
EMAIL = "hr.gurugramsec14@caddcentre.com"
ADDRESS = "2nd Floor, SCO-26 area, HUDA Market, Old Delhi Road, Sector 14, Gurugram, Haryana 122001"

# Nav model — single source of truth for header, drawer and footer.
PATHS_NAV = [
    ("bim", "BIM &amp; Digital Construction", "The way modern buildings are designed and coordinated."),
    ("civil", "Civil &amp; Infrastructure Design", "Roads, corridors, terrain and quantities."),
    ("arch", "Architecture &amp; Visualisation", "Concept model to a render a client believes."),
    ("mech", "Mechanical &amp; Product Design", "Sketch to manufacturable assembly."),
    ("struct", "Structural Engineering &amp; Analysis", "Model it, analyse it, prove it stands up."),
    ("mep", "Electrical &amp; MEP Design", "The systems that make a building work."),
    ("pm", "Project Planning &amp; Management", "Plan the schedule, hold the cost, deliver."),
    ("ai", "AI &amp; Emerging Engineering Tech", "Automation, generative and AI-assisted workflows."),
]

PROGRAMS_NAV = [
    ("All programmes", "Filter by path, level and format", "programs"),
    ("Revit Architecture", "BIM for buildings", "program:revit-architecture"),
    ("Civil 3D", "Corridors and quantities", "program:civil-3d"),
    ("SolidWorks", "Parts, assemblies, drawings", "program:solidworks"),
    ("STAAD.Pro", "Structural analysis", "program:staad-pro"),
    ("Primavera P6", "Planning and project control", "program:primavera-ppm"),
    ("AutoCAD Electrical", "Schematics and panels", "program:autocad-electrical"),
    ("3D Printing", "CAD to physical part", "program:3d-printing"),
]

# Routing helper: in the single-file preview links are hash routes; in the
# deployable build they are real URLs. `L()` resolves both from one source.
from build_data import PATHS as _PATHS, PROGRAMS as _PROGS

# Department -> its courses, derived from each programme's declared path key.
DEPARTMENTS = []
for _k, _slug, _name, _outcome, *_rest in _PATHS:
    _courses = [(p[0], p[1]) for p in _PROGS if p[3] == _k]
    DEPARTMENTS.append({"key": _k, "slug": _slug, "name": _name,
                        "outcome": _outcome, "courses": _courses})

DEPT_OF_COURSE = {}
for _d in DEPARTMENTS:
    for _cs, _cn in _d["courses"]:
        DEPT_OF_COURSE[_cs] = _d

ROUTES = {
    "home": "index.html",
    "career-paths": "career-paths/index.html",
    "programs": "programs/index.html",
    "student-work": "student-work/index.html",
    "finder": "career-path-finder/index.html",
    "corporate": "industry/corporate-training/index.html",
    "about": "about/index.html",
    "contact": "contact/index.html",
    "careers": "careers/index.html",
    "first-job-pakka": "careers/first-job-pakka/index.html",
    "life": "life-at-cadd/index.html",
    "mentor": "apply-as-mentor/index.html",
    "news": "news/index.html",
    "testimonials": "testimonials/index.html",
    "privacy-policy": "privacy-policy/index.html",
    "terms-conditions": "terms-conditions/index.html",
    "disclaimer": "disclaimer/index.html",
}
# Dynamic routes
for _k, _slug, *_ in _PATHS:
    ROUTES["path:" + _k] = f"career-paths/{_slug}/index.html"
for _p in _PROGS:
    ROUTES["program:" + _p[0]] = f"programs/{_p[0]}/index.html"
def register_articles(slugs):
    """Article routes are registered by build.py once ARTICLES is known.
    Doing it at import time would be circular: build_pages3 imports L() from
    here, so this module cannot import build_pages3."""
    for _s in slugs:
        ROUTES["article:" + _s] = f"news/{_s}/index.html"

# Back-compat aliases used by earlier page modules
ROUTES["path-bim"] = ROUTES["path:bim"]
ROUTES["program-revit"] = ROUTES["program:revit-architecture"]


def L(route, mode, depth=0):
    """Link resolver. mode='spa' -> hash route; mode='mpa' -> relative URL."""
    key = route.replace(":", "--") if mode == "spa" else route
    if mode == "spa":
        return f'href="#{key}" data-route="{key}"'
    up = "../" * depth
    return f'href="{up}{ROUTES[route]}"'


def head(title, desc, mode, depth=0):
    up = "../" * depth
    css = f"{up}assets/css/main.css"
    return f"""<!DOCTYPE html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#141414">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_IN">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,300;0,400;0,700;0,900;1,400;1,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"EducationalOrganization","name":"CADD Centre Gurugram",
"description":"Career-focused CAD, BIM, mechanical design and project management training in Sector 14, Gurugram.",
"telephone":"{PHONE_D}","email":"{EMAIL}",
"address":{{"@type":"PostalAddress","streetAddress":"2nd Floor, SCO-26 area, HUDA Market, Old Delhi Road","addressLocality":"Gurugram","addressRegion":"Haryana","postalCode":"122001","addressCountry":"IN"}},
"geo":{{"@type":"GeoCoordinates","latitude":28.4756556,"longitude":77.0443789}},
"openingHours":"Mo-Su 09:00-19:00","parentOrganization":{{"@type":"Organization","name":"CADD Centre Training Services"}}}}
</script>
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<div class="progress" aria-hidden="true"><div class="progress__bar" data-progress></div></div>
"""


# Where "Back" lands when there is no in-site history to return to — someone
# arriving from search or a shared link. The parent section beats home: on a
# deep page it is the more useful destination, and it is what the breadcrumb
# would have offered.
BACK_FALLBACK = [
    ("program:", "programs"),
    ("path:", "career-paths"),
    ("article:", "news"),
]


def back_fallback(pid):
    for prefix, route in BACK_FALLBACK:
        if pid.startswith(prefix):
            return route
    if pid == "first-job-pakka":
        return "careers"
    if pid == "corporate":
        return "home"
    return "home"


def header(mode, depth=0, active="", pid=""):
    def link(route, label, extra=""):
        cur = ' aria-current="page"' if route == active else ""
        return f'<a class="nav__link" {L(route, mode, depth)}{cur}{extra}>{label}</a>'

    mega_paths = "".join(
        f'<a class="mega__link" {L("path:" + k, mode, depth)}>'
        f'<strong>{n}</strong><span>{d}</span></a>' for k, n, d in PATHS_NAV)

    def _dept_block(d):
        courses = "".join(
            f'<a class="mega__course" {L("program:" + cs, mode, depth)}>{cn}</a>'
            for cs, cn in d["courses"][:7])
        more = (f'<a class="mega__course" style="color:var(--c-accent)" '
                f'{L("path:" + d["key"], mode, depth)}>All {len(d["courses"])} courses &rarr;</a>'
                if len(d["courses"]) > 7 else "")
        return (f'<div class="mega__dept"><span class="label label--accent">'
                f'<a {L("path:" + d["key"], mode, depth)} style="text-decoration:none;color:inherit">{d["name"]}</a>'
                f'</span>{courses}{more}</div>')

    mega_programs = "".join(_dept_block(d) for d in DEPARTMENTS if d["courses"])
    n_progs = len(_PROGS)
    n_depts = len([d for d in DEPARTMENTS if d["courses"]])

    drawer_paths = "".join(
        f'<a {L("path:" + k, mode, depth)}>{n}</a>' for k, n, d in PATHS_NAV)
    drawer_programs = "".join(
        '<div class="drawer__dept"><span>' + d["name"] + '</span>' +
        "".join(f'<a {L("program:" + cs, mode, depth)}>{cn}</a>' for cs, cn in d["courses"]) +
        '</div>'
        for d in DEPARTMENTS if d["courses"])

    # Persistent Home / Back strip. It sits inside the sticky header so both
    # controls stay reachable after scrolling, and it is suppressed on the home
    # page itself, where neither has anywhere to go. Back is a real link to the
    # parent section, upgraded by JS into history.back() when there is history
    # to go back to — so it still works with JavaScript off.
    back_ico = ('<svg class="pagebar__ico" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
                '<path d="M10 3L5 8l5 5" stroke="currentColor" stroke-width="1.6" '
                'stroke-linecap="round" stroke-linejoin="round"/></svg>')
    home_ico = ('<svg class="pagebar__ico" viewBox="0 0 16 16" fill="none" aria-hidden="true">'
                '<path d="M2.5 6.9L8 2.5l5.5 4.4V13a.9.9 0 0 1-.9.9H3.4a.9.9 0 0 1-.9-.9V6.9z" '
                'stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/></svg>')
    pagebar = (
        f'<div class="pagebar" data-pagebar{" hidden" if (mode == "mpa" and pid == "home") else ""}>'
        f'<div class="wrap pagebar__inner">'
        f'<a class="pagebar__btn" data-back {L(back_fallback(pid), mode, depth)}>'
        f'{back_ico}<span>Back</span></a>'
        f'<a class="pagebar__btn pagebar__btn--home" {L("home", mode, depth)}>'
        f'{home_ico}<span>Home</span></a>'
        f'</div></div>')

    return f"""
<div class="ribbon" data-ribbon hidden>
  <div class="wrap ribbon__inner">
    <span class="ribbon__tag">New</span>
    <a class="ribbon__badgelink" {L("first-job-pakka", mode, depth)} aria-label="First Job Pakka &mdash; training and placement in 80 hours"><img class="ribbon__badge" src="{'../' * depth}assets/img/logos/first-job-pakka-badge.webp" alt="First Job Pakka" width="640" height="117" decoding="async"></a>
    <span>&mdash; training and placement, built around 80 focused hours.
      <a {L("first-job-pakka", mode, depth)}>See what is included</a></span>
    <button class="ribbon__x" data-ribbon-close type="button" aria-label="Dismiss announcement">&times;</button>
  </div>
</div>

<div class="utility">
  <div class="wrap utility__inner">
    <div class="utility__group">
      <a href="tel:{PHONE}">{PHONE_D}</a>
      <a class="utility__hide" href="{WHATSAPP_LINK}">WhatsApp</a>
      <a class="utility__hide" href="mailto:{EMAIL}">{EMAIL}</a>
    </div>
    <div class="utility__group"><span class="utility__hide">Open 7 days &middot; 9:30 am &ndash; 7:00 pm</span></div>
  </div>
</div>

<header class="header">
  <div class="wrap header__inner">
    <a class="logo" {L("home", mode, depth)}><img class="logo__img" src="{'../' * depth}assets/img/logos/cadd-centre-logo.webp" alt="CADD Centre Gurugram, Sector 14 &mdash; Design India, Innovate India" width="480" height="80" decoding="async"></a>

    <nav class="nav" aria-label="Primary">
      {link("home", "Home")}
      {link("about", "About")}
      {link("career-paths", "Career Paths")}
      {link("programs", "Programs")}
      {link("corporate", "Corporate Training")}
      {link("careers", "Careers")}
      {link("life", "Life @ CADD")}
      {link("mentor", "Apply as Mentor")}
      {link("news", "News")}
    </nav>

    <div class="header__cta">
      <a class="btn btn--primary" {L("finder", mode, depth)}>Find My Career Path</a>
      <button class="burger" data-burger aria-expanded="false" aria-controls="drawer" aria-label="Open menu"><span></span></button>
    </div>
  </div>

  {pagebar}

</header>

<div class="drawer" id="drawer" data-drawer data-open="false" aria-hidden="true">
  <div class="drawer__head">
    <a class="logo" {L("home", mode, depth)}><span class="logo__mark">CADD<span>.</span></span></a>
    <button class="burger" data-drawer-close aria-label="Close menu" aria-expanded="true"><span></span></button>
  </div>
  <div class="drawer__body">
    <a class="acc__trigger" {L("home", mode, depth)}>Home</a>
    <a class="acc__trigger" {L("about", mode, depth)}>About</a>
    <button class="acc__trigger" data-acc-trigger aria-expanded="false" aria-controls="d1">Career Paths <span class="plus"></span></button>
    <div class="acc__panel" id="d1" data-open="false">{drawer_paths}</div>
    <button class="acc__trigger" data-acc-trigger aria-expanded="false" aria-controls="d2">Programs <span class="plus"></span></button>
    <div class="acc__panel" id="d2" data-open="false">{drawer_programs}</div>
    <a class="acc__trigger" {L("corporate", mode, depth)}>Corporate Training</a>
    <a class="acc__trigger" {L("careers", mode, depth)}>Careers</a>
    <a class="acc__trigger" {L("life", mode, depth)}>Life @ CADD</a>
    <a class="acc__trigger" {L("mentor", mode, depth)}>Apply as Mentor</a>
    <a class="acc__trigger" {L("news", mode, depth)}>News</a>
    <a class="acc__trigger" {L("contact", mode, depth)}>Contact</a>
    <a class="btn btn--primary btn--wide mt-4" {L("finder", mode, depth)}>Find My Career Path</a>
    <a class="btn btn--secondary btn--wide mt-2" href="tel:{PHONE}">Call {PHONE_D}</a>
  </div>
</div>
"""


def _has_testimonials():
    """The Learner stories page exists only once real footage is supplied, so
    the footer must not link to a page the build did not produce."""
    try:
        from build_data import TESTIMONIALS
        return any(t.get("video") for t in TESTIMONIALS)
    except ImportError:
        return False


def footer(mode, depth=0):
    up = "../" * depth
    paths = "".join(f'<li><a {L("path:" + k, mode, depth)}>{n}</a></li>' for k, n, d in PATHS_NAV)
    progs = "".join(f'<li><a {L(r, mode, depth)}>{n}</a></li>' for n, d, r in PROGRAMS_NAV)
    company = "".join(f'<li><a {L(r, mode, depth)}>{n}</a></li>' for n, r in [
        ("About the centre", "about"), ("Corporate training", "corporate"),
        ("Careers &amp; placement", "careers"), ("First Job Pakka", "first-job-pakka"),
        ("Life @ CADD", "life"), ("Student work", "student-work"),
        ("Apply as Mentor", "mentor"), ("News", "news"), ("Contact", "contact")]
        + ([("Learner stories", "testimonials")] if _has_testimonials() else []))
    return f"""
<button class="totop" data-totop data-show="false" aria-label="Back to top" type="button">
  <svg viewBox="0 0 14 14" width="14" height="14" fill="none" aria-hidden="true"><path d="M7 13V1M2 6l5-5 5 5" stroke="currentColor" stroke-width="1.6"/></svg>
</button>

<div class="advisor">
  <div class="advisor__panel" data-advisor-panel data-open="false">
    <p class="label label--accent">Need help choosing?</p>
    <p class="t-h3 mt-2">Talk to a career advisor</p>
    <p class="t-small t-muted">Tell us your background and we will point you to the right starting place. No pressure.</p>
    <div class="flex fcol gap-1 mt-3">
      <a class="btn btn--primary btn--wide" href="{WHATSAPP_LINK}">WhatsApp us</a>
      <a class="btn btn--ghost btn--wide" href="tel:{PHONE}">Call {PHONE_D}</a>
      <a class="btn btn--ghost btn--wide" {L("contact", mode, depth)}>Schedule a call</a>
    </div>
  </div>
  <button class="advisor__btn" data-advisor aria-expanded="false" aria-label="Talk to a career advisor">
    <span class="advisor__dot" aria-hidden="true"></span> Talk to a career advisor
  </button>
</div>

<div class="modal" data-modal hidden>
  <div class="modal__scrim" data-modal-close></div>
  <div class="modal__box" role="dialog" aria-modal="true" aria-labelledby="enq-t">
    <button class="modal__x" data-modal-close aria-label="Close">&times;</button>
    <p class="label label--accent">Enquire now</p>
    <h2 class="t-h2 mt-1 mb-3" id="enq-t">Tell us what you need</h2>
    <form onsubmit="return false">
      <div class="field"><label for="eq-n">Your name</label><input id="eq-n" type="text" required></div>
      <div class="field"><label for="eq-p">Mobile number</label><input id="eq-p" type="tel" inputmode="numeric" required>
        <span class="field__help">We will reply on WhatsApp</span></div>
      <div class="field"><label for="eq-c">Course category</label>
        <select id="eq-c">
          <option>Architecture, Engineering &amp; Construction</option>
          <option>Mechanical</option>
          <option>Project Management</option>
          <option>Hybrid</option>
          <option>Electrical CAD</option>
          <option>Not sure yet</option>
        </select></div>
      <button class="btn btn--primary btn--wide" type="submit">Send enquiry</button>
    </form>
    <p class="t-small t-muted mt-2">Migrated from the existing site's enquiry popup, including the course-category selector.</p>
  </div>
</div>

<nav class="bottombar" aria-label="Quick actions">
  <a href="tel:{PHONE}">Call</a>
  <a class="is-accent" href="{WHATSAPP_LINK}">WhatsApp</a>
</nav>

<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <a class="logo" {L("home", mode, depth)}><img class="logo__img" src="{'../' * depth}assets/img/logos/cadd-centre-logo-white.webp" alt="CADD Centre Gurugram, Sector 14 &mdash; Design India, Innovate India" width="480" height="76" loading="lazy" decoding="async"></a>
        <p class="t-small mt-3" style="max-width:38ch">Engineering careers, built in Gurugram. Industry-focused training in CAD, BIM, product design, structural engineering, project management and AI-assisted workflows.</p>
        <p class="label mt-3" style="color:#fff">An Authorised Training Centre of CADD Centre Training Services</p>
        <div class="flex gap-2 mt-3">
          <a href="https://www.facebook.com/caddcentregurugram/" rel="noopener">Facebook</a>
          <a href="https://www.instagram.com/caddcentregurugram/" rel="noopener">Instagram</a>
          <a href="http://linkedin.com/company/cadd-centre-gurugram/" rel="noopener">LinkedIn</a>
        </div>
      </div>
      <div><h4>Career paths</h4><ul>{paths}</ul></div>
      <div><h4>Programmes</h4><ul>{progs}</ul></div>
      <div><h4>Company</h4><ul>{company}
        <li><a href="{up}assets/docs/cadd-centre-prospectus.pdf" download>Course prospectus (PDF)</a></li>
      </ul></div>
      <div>
        <h4>Visit the centre</h4>
        <ul>
          <li>{ADDRESS}</li>
          <li>Open 7 days, 9:30 am &ndash; 7:00 pm</li>
        </ul>
        <a class="btn btn--primary mt-2" {L("contact", mode, depth)}>Book a centre visit</a>
      </div>
      <div>
        <h4>Contact</h4>
        <ul>
          <li><a href="tel:{PHONE}">{PHONE_D}</a></li>
          <li><a href="tel:+918448312600">{PHONE2_D}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="footer__base">
      <span>&copy; 2026 CADD Centre Gurugram, Sector 14. Operated by Vara Global Tech.</span>
      <span class="flex wrapf gap-2">
        {'<a href="#admin" data-route="admin" style="color:#fff;border-bottom:1px solid var(--c-accent);padding-bottom:1px">Admin portal (demo)</a>' if mode == "spa" else ''}
        <a {L("privacy-policy", mode, depth)}>Privacy</a>
        <a {L("terms-conditions", mode, depth)}>Terms</a>
        <a {L("disclaimer", mode, depth)}>Disclaimer</a>
        <a class="footer__by" href="https://www.imperialtechinnovations.com/" rel="noopener">Built by <span>Imperial</span></a>
      </span>
    </div>
  </div>
</footer>
"""


def tail(depth=0):
    up = "../" * depth
    return f'<script src="{up}assets/js/main.js"></script>\n</body>\n</html>\n'
