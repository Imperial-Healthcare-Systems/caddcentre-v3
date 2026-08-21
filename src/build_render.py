# -*- coding: utf-8 -*-
import re
"""Generic renderers driven by build_data. One template, many pages."""

from build_parts import figure, photo, photo_card
from build_pages import _faq
from build_shell import L, PHONE, PHONE_D, EMAIL, ADDRESS, DEPT_OF_COURSE
from build_data import PATHS, PROGRAMS, MASTERS, CERT_LEVELS, IDEAL_FOR

PATH_BY_KEY = {p[0]: p for p in PATHS}
PROG_BY_SLUG = {p[0]: p for p in PROGRAMS}

FIG_FOR_PATH = {"bim": "bim", "civil": "civil", "arch": "arch", "mech": "mech",
                "struct": "struct", "mep": "mep", "pm": "pm", "ai": "ai"}

# Discipline -> real image slot. Paths without a matching asset keep the
# generated CAD drawing rather than borrowing an unrelated photo.
PHOTO_FOR_PATH = {"bim": "bim", "civil": "civil", "arch": "arch", "mech": "mech",
                  "struct": "proj-rcc-structure", "pm": "proj-construction-programme",
                  "mep": None, "ai": "printing"}

# Programme slug -> its own image slot. A programme listed here shows its own
# artwork instead of the shared department drawing. Anything not listed keeps
# the drawing, so this grows one course at a time.
PHOTO_FOR_PROGRAM = {"revit-architecture": "prog-revit-architecture",
                     "revit-structure":   "prog-revit-structure",
                     "revit-mep":         "prog-revit-mep",
                     "civil-3d":          "prog-civil-3d",
                     "autocad-civil":     "prog-autocad-civil",
                     "staad-pro":         "prog-staad-pro",
                     "etabs":             "prog-etabs",
                     "5d-bim":            "prog-5d-bim",
                     "5d-bim-navisworks": "prog-5d-bim-navisworks",
                     "sketchup":          "prog-sketchup",
                     "v-ray":             "prog-v-ray",
                     "lumion":            "prog-lumion",
                     "3ds-max":           "prog-3ds-max",
                     "solidworks":        "prog-solidworks",
                     "catia":             "prog-catia",
                     "nx-cad":            "prog-nx-cad",
                     "creo":              "prog-creo",
                     "ansys":             "prog-ansys",
                     "ansys-workbench":   "prog-ansys-workbench",
                     "ansys-fluent":      "prog-ansys-fluent",
                     "nx-nastran":        "prog-nx-nastran",
                     "autodesk-inventor": "prog-autodesk-inventor",
                     "gdt":               "prog-gdt",
                     "autocad-mechanical": "prog-autocad-mechanical",
                     "autocad-3d":        "prog-autocad-3d",
                     "3d-printing":       "prog-3d-printing",
                     "primavera-ppm":     "prog-primavera-ppm",
                     "ms-project-ppm":    "prog-ms-project-ppm",
                     "autocad-electrical": "prog-autocad-electrical",
                     "pc-schematic":      "prog-pc-schematic",
                     "automation-cad":    "prog-automation-cad"}


def program_media(slug, pkey, depth=0, sizes="(max-width: 767px) 100vw, 33vw"):
    """Media block for a programme card, wherever one is listed. Uses the
    course's own image if it has one, otherwise the department drawing. Shared
    so the programmes index and the career paths can never disagree."""
    slot = PHOTO_FOR_PROGRAM.get(slug)
    if slot:
        return photo_card(slot, depth, "Representative project output", sizes)
    return figure(FIG_FOR_PATH[pkey])


def crumbs(mode, depth, trail):
    out = f'<a {L("home", mode, depth)} style="text-decoration:none">Home</a>'
    for label, route in trail:
        out += " / " + (f'<a {L(route, mode, depth)} style="text-decoration:none">{label}</a>' if route else label)
    return f'<p class="label mb-3">{out}</p>'


# ===========================================================================
# PROGRAMME PAGE — one template, ~33 pages
# ===========================================================================
def render_program(slug, mode, depth=0):
    p = PROG_BY_SLUG[slug]
    (s, name, cat, pkey, tier, dur, sw, headline, deliverable,
     modules, roles, careers, legacy) = p
    path = PATH_BY_KEY[pkey]
    fig = FIG_FOR_PATH[pkey]

    acc = ""
    for i, (title, bullets) in enumerate(modules):
        op = "true" if i == 0 else "false"
        acc += (f'<button class="acc2__t" id="module-{i+1}" data-acc-trigger '
                f'aria-expanded="{op}" aria-controls="{s}-m{i}">'
                f'<span>{title}</span>'
                f'<span class="plus" aria-hidden="true"></span></button>'
                f'<div class="acc2__p" id="{s}-m{i}" data-open="{op}"><ul>'
                + "".join(f"<li>{b}</li>" for b in bullets) + "</ul></div>")

    rolecards = "".join(
        f'<div class="dim"><strong>{r}</strong></div>' for r in roles)

    dept = DEPT_OF_COURSE.get(s)
    crumb_trail = [("Programmes", "programs")]
    if dept:
        crumb_trail.append((dept["name"], "path:" + dept["key"]))
    crumb_trail.append((name, None))
    crumb_html = crumbs(mode, depth, crumb_trail)
    dept_line = (f'Department &middot; <a {L("path:" + dept["key"], mode, depth)}>{dept["name"]}</a>'
                 f' &nbsp;/&nbsp; {len(modules)} modules') if dept else f'{len(modules)} modules' 

    # BreadcrumbList so the hierarchy is machine-readable too
    _items = [("Home", "https://caddcentregurugram.com/"),
              ("Programmes", "https://caddcentregurugram.com/programs/")]
    if dept:
        _items.append((re.sub(r"&[a-z]+;", "and", dept["name"]),
                       f'https://caddcentregurugram.com/career-paths/{dept["slug"]}/'))
    _items.append((re.sub(r"&[a-z]+;", "and", name),
                   f"https://caddcentregurugram.com/programs/{s}/"))
    crumb_schema = ('<script type="application/ld+json">{"@context":"https://schema.org",'
                    '"@type":"BreadcrumbList","itemListElement":[' +
                    ",".join(f'{{"@type":"ListItem","position":{i+1},"name":"{n}","item":"{u}"}}'
                             for i, (n, u) in enumerate(_items)) + ']}</script>')

    _ps = PHOTO_FOR_PATH.get(pkey)
    photo_hero = (f'<figure class="figure">{photo(_ps, depth)}<figcaption>Representative project output</figcaption></figure>'
                  if _ps else f'<div class="card" style="pointer-events:none">{figure(fig)}</div>')

    cert_cards = "".join(
        f'<div class="pillar rv" data-delay="{i*60}">'
                f'<h3 class="t-h3 mb-2 mt-1">{lvl}</h3>'
        f'<p class="t-small t-muted">{desc}</p></div>'
        for i, (lvl, desc) in enumerate(CERT_LEVELS))

    ideal_items = "".join(f"<li>{x}</li>" for x in IDEAL_FOR.get(pkey, []))

    related = [q for q in PROGRAMS if q[3] == pkey and q[0] != s][:3]
    rel = "".join(
        f'<a class="card rv" {L("program:" + q[0], mode, depth)}>{program_media(q[0], q[3], depth)}'
        f'<div class="card__body"><p class="label label--accent">{q[4]}</p>'
        f'<h3 class="t-h3">{q[1]}</h3><p class="t-small t-muted">{q[6]}</p></div></a>'
        for q in related)

    return f"""
<main id="main">
{crumb_schema}
<section class="section section--tight">
  <div class="wrap">
    {crumb_html}
    <div class="grid g-2" style="align-items:end">
      <div>
        <h1 class="t-h1 mb-2">{name} course in Gurgaon</h1>
        <p class="t-display" style="font-size:var(--t-h2);margin-bottom:var(--s-3)">Don't just learn {name}.<br>{headline}.</p>
        <p class="label"><span class="stars" style="letter-spacing:2px">&#9733;&#9733;&#9733;&#9733;&#9733;</span> &nbsp;4.9 on Google &middot; 207 reviews</p>
        <div class="flex wrapf gap-2 mt-3">
          <a class="btn btn--primary" href="/api/syllabus?slug={s}" data-syllabus="{s}">Download syllabus</a>
          <button class="btn btn--secondary" data-enquire type="button">Book a free demo class</button>
        </div>
      </div>
      {photo_hero}
    </div>
    <p class="label mt-4">{('Department: <a href="#" style="color:var(--c-accent)">' if False else '')}{dept_line}</p>
    <div class="factbar mt-6" data-cta-sentinel>
      <div><p class="label">Duration</p><p class="t-h3 mt-1">{dur}</p></div>
      <div><p class="label">Format</p><p class="t-h3 mt-1">Classroom + online</p></div>
      <div><p class="label">Projects</p><p class="t-h3 mt-1">Live project</p></div>
      <div><p class="label">Certification</p><p class="t-h3 mt-1">CADD Centre</p></div>
    </div>
  </div>
</section>

<nav class="subnav" data-subnav aria-label="On this page">
  <div class="wrap subnav__inner">
    <a href="#s-outcome">Outcome</a>
    <a href="#s-curriculum">Curriculum</a>
    <a href="#s-certification">Certification</a>
    <a href="#s-eligibility">Eligibility</a>
    <a href="#s-careers">Careers</a>
    <a href="#s-batches">Batches</a>
    <a href="#s-faq">FAQs</a>
  </div>
</nav>

<section class="section section--warm section--rule" id="s-outcome">
  <div class="wrap grid g-2">
    <div>
      <div class="marker"><span class="label label--accent">Outcome</span></div>
      <h2 class="t-h2 mb-3">What this qualifies you to do</h2>
      <div class="grid" style="gap:10px">{rolecards}</div>
      <p class="mt-3 t-small t-muted">Part of the <a {L("path:" + pkey, mode, depth)}>{path[2]}</a> career path.</p>
    </div>
    <div>
      <div class="marker"><span class="label label--accent">Deliverable</span></div>
      <h2 class="t-h2 mb-3">What you will have built</h2>
      <p>{deliverable}</p>
      <p class="t-small t-muted">This becomes a substantial piece in your portfolio, and it is what you will be asked about in an interview.</p>
    </div>
  </div>
</section>

<section class="section" id="s-curriculum">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Curriculum</span></div>
    <h2 class="t-h2 mb-2">What you will learn</h2>
    <p class="t-lead measure mb-4">The sequence follows how the work is actually done, not how the software's menus are organised.</p>
    <div class="acc2__tools"><button type="button" data-acc-all="acc-{s}" data-state="closed">Expand all</button></div>
    <div class="acc2" id="acc-{s}">{acc}</div>
    <div class="tags mt-4"><span class="tag">{sw}</span><span class="tag">{cat}</span><span class="tag">{tier}</span></div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap grid g-2">
    <div>
      <span id="s-careers"></span>
      <div class="marker"><span class="label label--accent">Careers</span></div>
      <h2 class="t-h2 mb-3">Where this leads</h2>
      <p>{careers}</p>
    </div>
    <div>
      <div class="marker"><span class="label label--accent">After the certificate</span></div>
      <h2 class="t-h2 mb-3">Placement support, honestly</h2>
      <p class="t-small">Portfolio development and review. CV and LinkedIn work against the roles you are targeting. Mock interviews with real technical questioning. Introductions through our Industry Recruitment Panel.</p>
      <p class="t-small"><strong>We cannot guarantee you a job.</strong> Hiring depends on your background, your portfolio, how you interview and the market that quarter. What we can guarantee is that you will not walk into an interview unprepared.</p>
      <a class="alink mt-2" {L("careers", mode, depth)}>See placement support
        <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
<span id="s-certification"></span>
    <div class="marker"><span class="label label--accent">Certification</span></div>
    <h2 class="t-h2 mb-2">Three levels. Pick the one that matches your goal.</h2>
    <p class="t-lead measure mb-6">{name} is certified at three levels. Most people start at Proficient; which level actually suits you depends on your background and how far you want to go — we will tell you straight at counselling.</p>
    <div class="grid g-3">
      {cert_cards}
    </div>
    <p class="note mt-4">Hours and fees vary by level. Book a counselling session and we will confirm exactly which level suits your background.</p>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap grid g-2">
    <div>
      <span id="s-eligibility"></span>
      <div class="marker"><span class="label label--accent">Eligibility</span></div>
      <h2 class="t-h2 mb-3">Who this is for</h2>
      <ul class="stack t-small" style="padding-left:1.1rem;color:var(--c-ink-2)">
        {ideal_items}
      </ul>
      <p class="t-small t-muted mt-3">No prior software experience is assumed at Proficient level.</p>
    </div>
    <div>
      <div class="marker"><span class="label label--accent">Scope</span></div>
      <h2 class="t-h2 mb-3">What the course covers</h2>
      <p>{deliverable}</p>
      <div class="tags mt-3"><span class="tag">{sw}</span><span class="tag">{cat}</span><span class="tag">{dur}</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
<span id="s-batches"></span>
    <div class="marker"><span class="label label--accent">Batches</span></div>
    <h2 class="t-h2 mb-4">Upcoming batches</h2>
    <table class="tbl">
      <thead><tr><th>Starts</th><th>Days</th><th>Timing</th><th>Mode</th><th>Availability</th></tr></thead>
      <tbody>
        <tr><td data-l="Starts">Next weekday batch</td><td data-l="Days">Mon&ndash;Fri</td><td data-l="Timing">11:00 am &ndash; 1:00 pm</td><td data-l="Mode">Classroom</td><td data-l="Availability">Confirm at counselling</td></tr>
        <tr><td data-l="Starts">Next evening batch</td><td data-l="Days">Mon, Wed, Fri</td><td data-l="Timing">6:30 pm &ndash; 8:30 pm</td><td data-l="Mode">Classroom</td><td data-l="Availability">Confirm at counselling</td></tr>
        <tr><td data-l="Starts">Next weekend batch</td><td data-l="Days">Sat &amp; Sun</td><td data-l="Timing">10:00 am &ndash; 1:00 pm</td><td data-l="Mode">Hybrid</td><td data-l="Availability">Confirm at counselling</td></tr>
      </tbody>
    </table>
    <p class="note mt-3">Batch start dates are confirmed at the centre. Call <a href="tel:+919990707382">+91 99907 07382</a> or book a visit for current availability.</p>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
<span id="s-faq"></span>
    <h2 class="t-h2 mb-4">Frequently asked</h2>
    <div class="acc2">
      {_faq([
        ("Who can join this programme?", "Students, graduates, diploma and ITI holders, and working professionals. We will tell you honestly at counselling whether this is the right starting point for your background."),
        ("Do I need prior experience?", "No. The foundation modules start from the basics. Existing CAD experience helps you move faster but is not required."),
        ("Are there weekend or evening batches?", "Yes. Weekday, evening and weekend batches all run. Confirm current availability at counselling."),
        ("What certification do I receive?", "A CADD Centre certification on completion. The exact additional certifications this centre is authorised to award are being confirmed and will be stated precisely rather than implied."),
        ("What are the fees?", "Fees depend on level, format and whether certification is included. Book a counselling session for an exact figure, along with an honest view of whether a shorter or longer programme would serve you better."),
        ("Can I visit before enrolling?", "Yes. Centre visits are free and carry no obligation. You can meet the trainer and sit in on a live class before paying anything."),
      ], s)}
    </div>
  </div>
</section>

{f'''<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Related</span></div>
    <h2 class="t-h2 mb-4">Others on this path</h2>
    <div class="grid g-3">{rel}</div>
  </div>
</section>''' if rel else ''}

<section class="section section--inverse">
  <div class="wrap tc">
    <h2 class="t-display mb-3">Still not sure {name}<br>is the right choice?</h2>
    <p class="t-lead" style="color:#C4C4C4;margin-inline:auto;max-width:52ch">Speak to an engineer, not a salesperson. We will tell you honestly if a different programme suits you better &mdash; or if you do not need us at all.</p>
    <a class="btn btn--primary mt-4" {L("contact", mode, depth)}>Book career counselling</a>
  </div>
</section>
</main>

<div class="stickycta" data-stickycta data-show="false">
  <div class="wrap stickycta__inner">
    <div class="stickycta__meta">
      <p class="stickycta__t">{name}</p>
      <p class="stickycta__s">{dur} &middot; Proficient / Masters / Expert</p>
    </div>
    <div class="flex gap-2">
      <a class="btn btn--primary" href="/api/syllabus?slug={s}" data-syllabus="{s}">Download syllabus</a>
    </div>
  </div>
</div>
"""


# ===========================================================================
# CAREER PATH PAGE — one template, 8 pages
# ===========================================================================
def render_path(key, mode, depth=0):
    (k, slug, name, outcome, intro, roadmap, roles, suits, notfor, progs) = PATH_BY_KEY[key]
    fig = FIG_FOR_PATH[k]

    rm = ""
    for i, step in enumerate(roadmap):
        if i:
            rm += '<span class="roadmap__arrow">&rarr;</span>'
        rm += f'<span class="roadmap__step">{step}</span>'

    rows = "".join(f'<tr><td data-l="Role"><strong>{r}</strong></td><td data-l="Work">{d}</td></tr>' for r, d in roles)

    progcards = ""
    for ps in progs:
        if ps not in PROG_BY_SLUG:
            continue
        q = PROG_BY_SLUG[ps]
        progcards += (f'<a class="card rv" {L("program:" + q[0], mode, depth)}>'
                      f'{program_media(q[0], q[3], depth)}'
                      f'<div class="card__body"><p class="label label--accent">{q[4]} &middot; {q[5]}</p>'
                      f'<h3 class="t-h3">{q[1]}</h3><p class="t-small t-muted">{q[6]}</p></div></a>')

    intro_html = "".join(f"<p>{para}</p>" for para in intro[1:])
    _ps = PHOTO_FOR_PATH.get(k)
    path_media = (f'<figure class="figure">{photo(_ps, depth)}<figcaption>Representative project output</figcaption></figure>'
                  if _ps else f'<div class="card" style="pointer-events:none">{figure(fig)}</div>')

    return f"""
<main id="main">
<section class="section section--inverse">
  <div class="wrap">
    {crumbs(mode, depth, [("Career paths", "career-paths"), (name, None)])}
    <h1 class="t-display mb-3">Build a career in<br>{name}.</h1>
    <p class="t-lead" style="color:#C4C4C4;max-width:64ch">{intro[0]}</p>
    <p class="label mt-4">{' &middot; '.join(r for r, d in roles)}</p>
    <div class="flex wrapf gap-2 mt-4">
      <a class="btn btn--primary" {L("contact", mode, depth)}>Talk to a career advisor</a>
      <a class="btn btn--secondary" {L("finder", mode, depth)}>Not sure? Try the finder</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid g-2">
    <div>
      <div class="marker"><span class="label label--accent">The work</span></div>
      <h2 class="t-h2 mb-3">What this work actually involves</h2>
      {intro_html}
    </div>
    {path_media}
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Skills roadmap</span></div>
    <h2 class="t-h2 mb-4">The sequence that gets you there</h2>
    <div class="roadmap">{rm}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Roles</span></div>
    <h2 class="t-h2 mb-4">Roles this leads to</h2>
    <table class="tbl"><thead><tr><th>Role</th><th>What you would do</th></tr></thead><tbody>{rows}</tbody></table>
  </div>
</section>

{f'''<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Programmes</span></div>
    <h2 class="t-h2 mb-4">Programmes on this path</h2>
    <div class="grid g-3">{progcards}</div>
  </div>
</section>''' if progcards else ''}

<section class="section">
  <div class="wrap grid g-2">
    <div>
      <h2 class="t-h2 mb-3">A good fit if you are</h2>
      <ul class="stack t-small" style="padding-left:1.1rem;color:var(--c-ink-2)">
        {''.join(f'<li>{x}</li>' for x in suits)}
      </ul>
    </div>
    <div>
      <h2 class="t-h2 mb-3">Probably not the right start if</h2>
      <ul class="stack t-small" style="padding-left:1.1rem;color:var(--c-ink-2)">
        {''.join(f'<li>{x}</li>' for x in notfor)}
      </ul>
    </div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
<span id="s-faq"></span>
    <h2 class="t-h2 mb-4">Frequently asked</h2>
    <div class="acc2">
      {_faq([
        ("Do I need prior software experience?", "Not for the foundation programmes on this path. If you already have some, you will move faster and we may recommend starting further along."),
        ("Can I do this alongside a job?", "Yes. Weekend and evening batches run for every programme on this path."),
        ("How long before I am employable?", "It depends on your starting point and how much you build. People who finish a full portfolio project are ready to interview. We will give you a straight answer about your own situation at counselling."),
        ("What certification will I receive?", "A CADD Centre certification. The exact additional certifications this centre is authorised to award are being confirmed and will be stated precisely rather than implied."),
        ("Is there placement support?", "Yes — portfolio review, CV and profile work, mock interviews and introductions through our Industry Recruitment Panel. We do not guarantee jobs and we do not claim to."),
      ], "p-" + k)}
    </div>
  </div>
</section>

<section class="section section--inverse">
  <div class="wrap tc">
    <h2 class="t-display mb-3">Still deciding?</h2>
    <p class="t-lead" style="color:#C4C4C4;margin-inline:auto;max-width:52ch">Speak to an engineer, not a salesperson. We will tell you honestly if a different path suits you better.</p>
    <div class="flex wrapf gap-2 mt-4" style="justify-content:center">
      <a class="btn btn--primary" {L("contact", mode, depth)}>Book career counselling</a>
      <a class="btn btn--secondary" {L("finder", mode, depth)}>Try the career path finder</a>
    </div>
  </div>
</section>
</main>
"""
