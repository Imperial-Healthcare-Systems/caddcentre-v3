# -*- coding: utf-8 -*-
"""Remaining page bodies."""

from build_parts import figure, photo, photo_card, icon
from build_pages import _faq
from build_shell import L, PHONE, PHONE_D, WHATSAPP, WHATSAPP_LINK, EMAIL, ADDRESS

from build_data import PROGRAMS as ALL_PROGRAMS, MASTERS, TRAINERS, STORIES

TIER_TAG = {"Master": "master", "Professional": "cert", "Short-term": "short"}


# Department identity for the programmes overview: an accent colour and a
# small line icon each, so a card is recognisable before it is read.
DEPT_STYLE = {
    "bim":    ("#E8455A", "#FDE8EB", '<path d="M4 21V7l7-4 7 4v14"/><path d="M9 21v-5h4v5"/><path d="M8 11h2M14 11h2"/>'),
    "civil":  ("#F0863A", "#FDEEE4", '<path d="M2 16h20"/><path d="M5 16V9M19 16V9"/><path d="M2 11c5-4 15-4 20 0"/><path d="M9 16v-3M15 16v-3"/>'),
    "arch":   ("#4A7DF0", "#E8EFFD", '<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
    "mech":   ("#9B5CF0", "#F0E9FD", '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/>'),
    "struct": ("#3FAE73", "#E6F5ED", '<path d="M4 21V4h16v17"/><path d="M4 9h16M4 15h16M12 4v17"/>'),
    "mep":    ("#F0B93A", "#FDF4E1", '<path d="M13 2L4 14h6l-1 8 9-12h-6z"/>'),
    "pm":     ("#3FB6C4", "#E4F4F6", '<path d="M8 4h8v3H8z"/><path d="M6 6H5v15h14V6h-1"/><path d="M9 12h6M9 16h4"/>'),
    "ai":     ("#7C8794", "#EEF1F4", '<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>'),
}


def _dept_icon(key, colour="#fff"):
    """The glyph itself. Drawn in white because it sits on a solid colour disc."""
    body = DEPT_STYLE.get(key, DEPT_STYLE["ai"])[2]
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{colour}" stroke-width="1.7" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>')


def page_programs(mode, depth=0):
    """Programmes index.

    Opens as a department overview — one card per department, colour-coded,
    with a few of its courses and a way in — then carries the complete course
    list underneath, still grouped by department and still filterable. The
    overview answers "what do you teach?" and the list answers "show me
    everything", which were previously fighting for the same screen.
    """
    from build_render import program_media
    from build_shell import DEPARTMENTS

    depts = [d for d in DEPARTMENTS if d["courses"]]
    by_slug = {x[0]: x for x in ALL_PROGRAMS}
    tier_order = {"Master": 0, "Professional": 1, "Short-term": 2}
    n_courses = len(ALL_PROGRAMS)
    up = "../" * depth
    n_masters = len(MASTERS)

    # ---- overview cards -------------------------------------------------
    cards = ""
    for d in depts:
        colour, tint, _ = DEPT_STYLE.get(d["key"], DEPT_STYLE["ai"])
        n = len(d["courses"])
        bullets = "".join(f'<li>{cn}</li>' for _cs, cn in d["courses"][:5])
        more = f'<li class="deptc__more">and {n - 5} more</li>' if n > 5 else ""
        cards += f"""<a class="deptc" {L("path:" + d['key'], mode, depth)}>
  <div class="deptc__top">
    <span class="deptc__ico" style="background:{colour}">{_dept_icon(d['key'])}</span>
    <span class="deptc__n">{n}</span>
  </div>
  <h3 class="deptc__name">{d['name']}</h3>
  <ul class="deptc__list">{bullets}{more}</ul>
  <span class="deptc__go" style="color:{colour}">All {n} courses
    <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></span>
</a>"""

    cards += f"""<a class="deptc deptc--all" href="#all-courses">
  <div class="deptc__top">
    <span class="deptc__ico" style="background:#FDE8EB">
      <svg viewBox="0 0 24 24" fill="none" stroke="#E8455A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h7v7H4zM13 4h7v7h-7zM4 13h7v7H4zM13 13h7v7h-7z"/></svg>
    </span>
  </div>
  <h3 class="deptc__name">All courses</h3>
  <p class="deptc__blurb">{n_courses} courses and {n_masters} Master Certificates across {len(depts)} departments. Each one opens into its module-by-module curriculum.</p>
  <span class="btn btn--primary mt-3">Browse all
    <svg viewBox="0 0 14 14" fill="none" aria-hidden="true" style="width:13px;height:13px"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></span>
</a>"""

    # ---- full grouped list ----------------------------------------------
    groups = ""
    master_cards = ""
    for mp in MASTERS:
        mslug, mname, mcat, mpkey, mtier, mdur, msw, mheadline = mp[0], mp[1], mp[2], mp[3], mp[4], mp[5], mp[6], mp[7]
        mdeliverable, mmodules, mroles = mp[8], mp[9], mp[10]
        covers = "".join(f'<li>{x}</li>' for x in mmodules)
        roles = "".join(f'<span class="tag">{r}</span>' for r in mroles)
        master_cards += f"""<article class="card mastercard" data-tags="{mpkey} master">
  <div class="card__body">
    <p class="label label--accent">{mtier} certificate &middot; {mcat}</p>
    <h3 class="t-h3">{mname}</h3>
    <p class="t-small t-muted">{mheadline}.</p>
    <div class="tags card__roles"><span class="tag">{mdur}</span><span class="tag">{msw}</span></div>
    <p class="mastercard__lbl label">What you build</p>
    <p class="t-small t-muted">{mdeliverable}</p>
    <p class="mastercard__lbl label">What it covers</p>
    <ul class="mastercard__list t-small">{covers}</ul>
    <p class="mastercard__lbl label">Roles it leads to</p>
    <div class="tags">{roles}</div>
    <a class="btn btn--secondary btn--wide mt-3" {L("contact", mode, depth)}>Talk to an advisor about this</a>
  </div>
</article>"""

    groups = f"""
<section class="progroup" id="dept-master" data-group="master" aria-labelledby="dept-master-h">
  <div class="progroup__head">
    <div class="progroup__title">
      <h2 class="t-h2" id="dept-master-h">Master Certificates</h2>
      <p class="progroup__count label">{n_masters} programmes</p>
    </div>
    <p class="progroup__outcome t-small t-muted">Long-format programmes that run six to eight months and take you from no experience to a portfolio you can be hired on. Each one combines several software courses with a single continuous project.</p>
  </div>
  <div class="grid g-3 progroup__grid">{master_cards}</div>
</section>"""

    for d in depts:
        progs = sorted((by_slug[cs] for cs, _cn in d["courses"]),
                       key=lambda x: (tier_order.get(x[4], 9), x[1]))
        cs_html = ""
        for i, pr in enumerate(progs):
            slug, name, cat, pkey, tier, dur, sw, headline = pr[0], pr[1], pr[2], pr[3], pr[4], pr[5], pr[6], pr[7]
            tags = f"{pkey} {TIER_TAG.get(tier, 'short')}"
            cs_html += f"""<a class="card rv" data-tags="{tags}" data-delay="{(i%3)*50}" {L("program:" + slug, mode, depth)}>
  {program_media(slug, pkey, depth)}
  <div class="card__body">
    <p class="label label--accent">{tier} &middot; {cat}</p>
    <h3 class="t-h3">{name}</h3>
    <p class="t-small t-muted">{headline}.</p>
    <div class="tags card__roles"><span class="tag">{dur}</span><span class="tag">{sw}</span></div>
  </div>
</a>"""
        n = len(progs)
        colour = DEPT_STYLE.get(d["key"], DEPT_STYLE["ai"])[0]
        groups += f"""
<section class="progroup" id="dept-{d['key']}" data-group="{d['key']}" aria-labelledby="dept-{d['key']}-h">
  <div class="progroup__head" style="border-bottom-color:{colour}">
    <div class="progroup__title">
      <h2 class="t-h2" id="dept-{d['key']}-h">{d['name']}</h2>
      <p class="progroup__count label" style="color:{colour}">{n} course{'' if n == 1 else 's'}</p>
    </div>
    <p class="progroup__outcome t-small t-muted">{d['outcome']}</p>
    <a class="alink progroup__path" {L("path:" + d['key'], mode, depth)}>Where this department leads
      <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></a>
  </div>
  <div class="grid g-3 progroup__grid">{cs_html}</div>
</section>"""

    return f"""
<main id="main">
<section class="section proghero">
  <div class="wrap proghero__inner">
    <div class="proghero__copy">
      <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / Programmes</p>
      <p class="label label--accent proghero__kicker">Programmes</p>
      <h1 class="t-display mt-2 mb-3">{n_courses} courses.<br><em>{len(depts)} departments.</em></h1>
      <p class="t-lead measure">Every course sits inside a department and opens into a module-by-module
        curriculum. Jump straight to a department below, or filter by level if you already know what you need.</p>
    </div>
    <div class="proghero__art" aria-hidden="true">
      <svg viewBox="0 0 460 360" fill="none" xmlns="http://www.w3.org/2000/svg" role="img" aria-hidden="true">
        <defs>
          <linearGradient id="pgRed" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#F2536A"/><stop offset="1" stop-color="#D01F35"/>
          </linearGradient>
          <linearGradient id="pgRedT" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0" stop-color="#FF7285"/><stop offset="1" stop-color="#EE3D55"/>
          </linearGradient>
          <linearGradient id="pgGrey" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0" stop-color="#F7F8FA"/><stop offset="1" stop-color="#E7EAEF"/>
          </linearGradient>
          <pattern id="pgDots" width="11" height="11" patternUnits="userSpaceOnUse">
            <circle cx="1.6" cy="1.6" r="1.6" fill="#F0919E" opacity="0.55"/>
          </pattern>
        </defs>

        <g opacity="0.5" stroke="#F3B8C1" stroke-width="1">
          <path d="M30 250l150-86M110 296l150-86M190 342l150-86M120 118l150 86M200 72l150 86M280 26l150 86"/>
        </g>
        <rect x="330" y="16" width="112" height="72" fill="url(#pgDots)"/>
        <rect x="24" y="268" width="92" height="60" fill="url(#pgDots)" opacity="0.7"/>

        <path d="M96 236l74-43 74 43-74 43z" fill="#EDEFF3"/>
        <path d="M96 236v14l74 43 74-43v-14l-74 43z" fill="#DFE3EA"/>
        <path d="M232 190l86-50 86 50-86 50z" fill="#EDEFF3"/>
        <path d="M232 190v14l86 50 86-50v-14l-86 50z" fill="#DFE3EA"/>

        <g>
          <path d="M108 186l52-30 52 30-52 30z" fill="url(#pgGrey)"/>
          <path d="M108 186v34l52 30v-34z" fill="#E3E7ED"/>
          <path d="M212 186v34l-52 30v-34z" fill="#D6DBE3"/>
          <g stroke="#B9C0CB" stroke-width="1.4" opacity="0.9">
            <path d="M146 208h28v18h-28z"/><path d="M160 208v18"/>
          </g>
        </g>

        <g>
          <path d="M262 300l44-25 44 25-44 25z" fill="url(#pgGrey)"/>
          <path d="M262 300v26l44 25v-26z" fill="#E3E7ED"/>
          <path d="M350 300v26l-44 25v-26z" fill="#D6DBE3"/>
          <g stroke="#B9C0CB" stroke-width="1.3" opacity="0.9">
            <circle cx="292" cy="322" r="7"/><path d="M292 315v14M285 322h14"/>
          </g>
        </g>

        <g>
          <path d="M240 92l78-45 78 45-78 45z" fill="url(#pgRedT)"/>
          <path d="M240 92v58l78 45v-58z" fill="url(#pgRed)"/>
          <path d="M396 92v58l-78 45v-58z" fill="#B81A2E"/>
          <g stroke="#fff" stroke-width="1.7" opacity="0.95" stroke-linecap="round" stroke-linejoin="round">
            <path d="M300 84h36v22h-36z"/><path d="M318 84v22M300 95h36"/>
          </g>
          <g stroke="#fff" stroke-width="1.6" opacity="0.75" stroke-linecap="round">
            <path d="M266 122v26M278 129v26M290 136v26"/>
          </g>
          <g stroke="#fff" stroke-width="1.6" opacity="0.55" stroke-linecap="round">
            <circle cx="356" cy="134" r="11"/><path d="M356 123v22M345 134h22"/>
          </g>
        </g>
      </svg>
    </div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap proglayout">
    <div class="deptgrid">{cards}</div>

    <aside class="progside">
      <div class="progside__card">
        <span class="progside__ico">
          <svg viewBox="0 0 24 24" fill="none" stroke="#E8455A" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M7 12h10M10 18h4"/></svg>
        </span>
        <p class="label label--accent mt-2">All courses</p>
        <h2 class="t-h3 mt-1 mb-2">Filter by department, level and format.</h2>
        <p class="t-small t-muted">Each one opens into its module-by-module curriculum.</p>
        <div class="progside__facts">
          <div class="progfact"><span class="progfact__ico" style="background:#FDE8EB">{icon("layers")}</span>
            <div><strong>{len(depts)} departments</strong></div></div>
          <div class="progfact"><span class="progfact__ico" style="background:#FDF4E1">{icon("book")}</span>
            <div><strong>{n_courses} courses</strong></div></div>
          <div class="progfact"><span class="progfact__ico" style="background:#E6F5ED">{icon("badge")}</span>
            <div><strong>{n_masters} Master Certificates</strong></div></div>
        </div>
        <a class="btn btn--accentline btn--wide mt-3" href="#all-courses">Browse all</a>
        <a class="progside__pdf" href="{up}assets/docs/cadd-centre-prospectus.pdf" download>{icon("book")}<span><strong>Download the prospectus</strong><em>PDF &middot; 8 pages &middot; 7 MB</em></span></a>
      </div>
    </aside>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="progcta">
      <span class="progcta__ico">{icon("target")}</span>
      <div class="progcta__copy">
        <strong>Not sure which programme is right for you?</strong>
        <span>Four questions. No sign-up, and you see the result before we ask for anything.</span>
      </div>
      <a class="btn btn--primary" {L("finder", mode, depth)}>Find My Career Path</a>
    </div>
  </div>
</section>

<section class="section section--warm section--rule" id="all-courses">
  <div class="wrap">
    <div class="flex jcb aic wrapf gap-3 mb-4">
      <div class="filters" data-filter-group data-filter-target="#prog-list" data-filter-empty="#prog-empty" data-filter-count="#prog-count">
        <span class="label" style="margin-right:8px">Department</span>
        <button class="chip" data-filter="all" aria-pressed="true">All</button>
        <button class="chip" data-filter="bim" aria-pressed="false">BIM &amp; Digital Construction</button>
        <button class="chip" data-filter="civil" aria-pressed="false">Civil &amp; Infrastructure</button>
        <button class="chip" data-filter="arch" aria-pressed="false">Architecture &amp; Visualisation</button>
        <button class="chip" data-filter="mech" aria-pressed="false">Mechanical &amp; Product Design</button>
        <button class="chip" data-filter="struct" aria-pressed="false">Structural &amp; Analysis</button>
        <button class="chip" data-filter="mep" aria-pressed="false">Electrical &amp; MEP</button>
        <button class="chip" data-filter="pm" aria-pressed="false">Project Planning</button>
        <span class="label" style="margin:0 8px 0 16px">Level</span>
        <button class="chip" data-filter="master" aria-pressed="false">Master</button>
        <button class="chip" data-filter="cert" aria-pressed="false">Certificate</button>
        <button class="chip" data-filter="short" aria-pressed="false">Short-term</button>
      </div>
      <p class="label"><span id="prog-count">{n_courses + n_masters}</span> programmes</p>
    </div>

    <div id="prog-list">{groups}</div>

    <div id="prog-empty" class="note is-hidden mt-4">No programmes match that combination yet. Try widening your filters, or talk to an advisor &mdash; we will point you to the right starting place.</div>

    <p class="note mt-6">Durations shown are indicative and depend on the certification level you choose. Fees are confirmed at counselling, along with EMI options and an honest view of whether a shorter or longer programme suits you better.</p>
  </div>
</section>
</main>
"""


def page_program_revit(mode, depth=0):
    modules = [
        ("Project setup", ["Templates, levels and grids", "The BIM way of thinking about a building", "Project browser and view organisation"]),
        ("Building the envelope", ["Walls, compound structures and layers", "Floors and floor systems", "Roofs, ceilings and voids"]),
        ("Openings and components", ["Doors and windows", "Joinery and fixed furniture", "Component placement and constraints"]),
        ("Complex geometry", ["Curtain walls, grids and mullions", "Stairs and ramps", "Railings and balustrades"]),
        ("Site and context", ["Topography and toposurfaces", "Site components and grading", "Building pads"]),
        ("Families", ["Family editor fundamentals", "Parametric family creation", "Nested and shared families"]),
        ("Documentation", ["Schedules and quantities", "Sheets, titleblocks and revisions", "Annotation and dimensioning"]),
        ("Presentation", ["View templates and graphic overrides", "Visualisation and camera views", "Presentation output"]),
        ("Collaboration", ["Worksharing and worksets", "Central and local models", "Coordination and linked models"]),
        ("Applied", ["Introduction to energy analysis", "BIM coordination basics", "Interoperability and IFC"]),
        ("Live project", ["A full building from setup to issued drawing set", "Portfolio-ready deliverable", "Review and critique"]),
    ]
    acc = ""
    for i, (title, bullets) in enumerate(modules):
        acc += f"""<button class="acc2__t" data-acc-trigger aria-expanded="{'true' if i==0 else 'false'}" aria-controls="mod-{i}">
<span>{title}</span><span class="plus" aria-hidden="true"></span></button>
<div class="acc2__p" id="mod-{i}" data-open="{'true' if i==0 else 'false'}">
<ul>{''.join(f'<li>{b}</li>' for b in bullets)}</ul></div>"""

    return f"""
<main id="main">
<section class="section section--tight">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / <a {L("programs", mode, depth)} style="text-decoration:none">Programmes</a> / Revit Architecture</p>
    <div class="grid g-2" style="align-items:end">
      <div>
        <h1 class="t-h1 mb-2">Revit Architecture course in Gurgaon</h1>
        <p class="t-display" style="font-size:var(--t-h2);margin-bottom:var(--s-3)">Don't just learn Revit.<br>Learn how buildings are designed in BIM.</p>
        <p class="label"><span class="stars" style="letter-spacing:2px">&#9733;&#9733;&#9733;&#9733;&#9733;</span> &nbsp;4.9 on Google &middot; 207 reviews</p>
        <div class="flex wrapf gap-2 mt-3">
          <a class="btn btn--primary" {L("contact", mode, depth)}>Download syllabus</a>
          <a class="btn btn--secondary" {L("contact", mode, depth)}>Book a free demo class</a>
        </div>
      </div>
      <div class="card" style="pointer-events:none">{figure("bim")}</div>
    </div>
    <div class="factbar mt-6">
      <div><p class="label">Duration</p><p class="t-h3 mt-1">~60 hours</p></div>
      <div><p class="label">Format</p><p class="t-h3 mt-1">Classroom + online</p></div>
      <div><p class="label">Projects</p><p class="t-h3 mt-1">Live project</p></div>
      <div><p class="label">Certification</p><p class="t-h3 mt-1">CADD Centre</p></div>
    </div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap grid g-2">
    <div>
      <div class="marker"><span class="label label--accent">Outcome</span></div>
      <h2 class="t-h2 mb-3">What this qualifies you to do</h2>
      <div class="grid" style="gap:10px">
        {''.join(f'<div class="dim"><strong>{r}</strong><br><span class="t-small t-muted">{d}</span></div>' for r, d in [("BIM Modeller","Build and maintain discipline models to project standards"),("Revit Technician","Produce construction documentation from the model"),("Architectural Designer","Take a design from concept model to coordinated output"),("Documentation Assistant","Support drawing production and issue control")])}
      </div>
    </div>
    <div>
      <div class="marker"><span class="label label--accent">Deliverable</span></div>
      <h2 class="t-h2 mb-3">What you will have built</h2>
      <p>A complete multi-storey building model &mdash; levels, grids, walls, floors, roofs, curtain systems, stairs and custom families &mdash; taken through to a coordinated drawing set with schedules and quantities extracted from the model itself.</p>
      <p class="t-small t-muted">This becomes the first substantial piece in your portfolio, and it is what you will be asked about in an interview.</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Curriculum</span></div>
    <h2 class="t-h2 mb-2">What you will learn</h2>
    <p class="t-lead measure mb-4">The sequence follows how a building is actually put together, not how the software's menus are organised.</p>
    <div class="acc2">{acc}</div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">After the certificate</span></div>
    <h2 class="t-h2 mb-3">Placement support, described honestly</h2>
    <div class="grid g-2">
      <div>
        <p><strong>What we do.</strong> Portfolio development and review. CV and LinkedIn profile work against the roles you are targeting. Mock interviews with real technical questioning and honest feedback. Introductions through our Industry Recruitment Panel. Guidance on internships and project-based openings.</p>
      </div>
      <div>
        <p><strong>What we cannot do.</strong> We cannot guarantee you a job. Hiring depends on your background, how much effort you put into your portfolio, how you interview, and the state of the market that quarter. What we can guarantee is that you will not walk into an interview unprepared.</p>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
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
    <p class="note mt-3">Batch data is driven by the CMS <code>batch</code> content type (Document&nbsp;1, Section&nbsp;9.2) so dates never go stale. Live dates pending client feed.</p>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <h2 class="t-h2 mb-4">Frequently asked</h2>
    <div class="acc2">
      {_faq([
        ("Who can join this programme?", "Architecture and civil engineering students and graduates, diploma and ITI holders, interior designers, working professionals moving into BIM, and beginners entering the construction industry."),
        ("Do I need prior experience?", "No. The foundation modules start from the basics. Existing AutoCAD experience will help you move faster but is not required."),
        ("Are there weekend or evening batches?", "Yes. Weekday, evening and weekend batches all run. Confirm current availability at counselling."),
        ("What certification do I receive?", "A CADD Centre certification on completion. The exact additional certifications this centre is authorised to award are being confirmed and will be stated precisely rather than implied."),
        ("What are the fees?", "Fees depend on level, format and whether certification is included. Book a counselling session for an exact figure, along with an honest view of whether a shorter or longer programme would serve you better."),
        ("Can I visit before enrolling?", "Yes. Centre visits are free and carry no obligation. You can meet the trainer and sit in on a live class before paying anything."),
      ], "rev")}
    </div>
  </div>
</section>

<section class="section section--inverse">
  <div class="wrap tc">
    <h2 class="t-display mb-3">Still not sure Revit<br>is the right choice?</h2>
    <p class="t-lead" style="color:#C4C4C4;margin-inline:auto;max-width:52ch">Speak to an engineer, not a salesperson. We will tell you honestly if a different programme suits you better &mdash; or if you do not need us at all.</p>
    <a class="btn btn--primary mt-4" {L("contact", mode, depth)}>Book career counselling</a>
  </div>
</section>
</main>
"""


# Student work, grouped by discipline. Each entry:
#   (image slug, title, software, what the project involved)
# Images live in assets/img as {slug}-{480,960,1600}.{webp,avif}; which widths
# exist depends on the resolution of the source the learner supplied, so
# _sw_media() offers only the ones on disk rather than pointing at a 404.
STUDENT_WORK = [
    ("Architecture &amp; Interior Design", "arch", [
        ("sw-tower", "Multi-storey residential tower", "Revit &middot; Rendering",
         "A full residential block modelled floor by floor, with balcony detailing, jaali screens and a dusk exterior render."),
        ("sw-villa-night", "Villa &mdash; night lighting study", "Revit &middot; Rendering",
         "Classical villa elevation taken through to an evening render, with external lighting placed and balanced."),
        ("sw-brick-house", "Three-bedroom house &mdash; exterior", "Revit &middot; Rendering",
         "Brick-clad residence with cantilevered slabs and an external stair, rendered at sunset."),
        ("sw-residence", "Contemporary residence", "Revit &middot; Rendering",
         "Two-storey house with car port, terrace and landscaped frontage, modelled and rendered in context."),
        ("sw-house-front", "Two-storey residence &mdash; front elevation", "Revit &middot; Rendering",
         "Front elevation study with balcony, boundary treatment and planting."),
        ("sw-house-timber", "Residence with timber cladding", "Revit &middot; Rendering",
         "Massing and material study &mdash; timber banding against render, shown from the approach."),
        ("sw-house-elev", "Residence &mdash; elevation study", "Revit &middot; Rendering",
         "Elevation worked up with glazing, railings and porch detail."),
        ("sw-revit-first", "Working drawing set &mdash; first floor", "Revit",
         "Dimensioned first-floor plan with room names and a 3D view, issued on a titled sheet."),
        ("sw-revit-ground", "Working drawing set &mdash; ground and first", "Revit",
         "Ground and first floor plans with door and window marks, set out on a single sheet alongside the model."),
    ]),
    ("Mechanical &amp; Product Design", "mech", [
        ("sw-engine-dwg", "Four-cylinder engine &mdash; assembly drawing", "SolidWorks",
         "Piston, connecting rod and crankshaft modelled as parts, assembled, and documented as a drawing with a bill of materials."),
        ("sw-crankshaft", "Crankshaft and piston assembly", "SolidWorks",
         "The same engine shown as a built assembly, with mates checked through the full rotation."),
        ("sw-steam-dwg", "Muncaster steam engine &mdash; drawing sheet", "SolidWorks",
         "A complete A2 sheet: detail views, an exploded sub-assembly, a bill of materials and manufacturing notes."),
        ("sw-steam-3d", "Muncaster steam engine &mdash; assembly", "SolidWorks",
         "The finished engine assembled from its own machined parts, flywheel to cylinder."),
        ("sw-tractor", "Agricultural tractor", "Siemens NX",
         "Full vehicle assembly &mdash; bonnet surfacing, wheels, canopy and decals, built as constrained components."),
        ("sw-cultivator", "Cultivator implement", "Siemens NX",
         "Frame, tines and three-point linkage modelled as a working assembly."),
        ("sw-chair", "Office chair", "Siemens NX",
         "Product model with upholstered surfaces, gas lift and castor base, presented in a rendered scene."),
        ("sw-fan", "Wall-mounted fan", "Siemens NX",
         "Blade, guard and motor housing modelled and assembled concentrically."),
        ("sw-hook", "Hook and screw assembly", "Siemens NX",
         "Lifting hook with threaded shaft, assembled with constraints and checked for interference."),
        ("sw-wheel", "Alloy wheel and tyre", "SolidWorks",
         "Spoke geometry and tread pattern modelled, then rendered as a presentation image."),
        ("sw-cannon", "Model cannon assembly", "SolidWorks",
         "Turned barrel, carriage and wheels built as parts and mated into a working assembly."),
        ("sw-truck", "Military cargo truck", "SolidWorks",
         "Six-wheel vehicle body, cab and load bed modelled and rendered."),
    ]),
]


def _sw_media(slug, depth):
    """Responsive picture for a student work card, offering only the widths
    that were actually generated for that image."""
    import os as _os
    here = _os.path.dirname(_os.path.abspath(__file__))
    up = "../" * depth
    have = [w for w in (480, 960, 1600)
            if _os.path.exists(_os.path.join(here, "assets/img", f"{slug}-{w}.webp"))]
    if not have:
        return ""
    sizes = "(max-width: 767px) 100vw, 33vw"

    def srcset(ext):
        return ", ".join(f"{up}assets/img/{slug}-{w}.{ext} {w}w" for w in have)

    biggest = have[-1]
    return (f'<div class="card__media card__media--photo"><picture>'
            f'<source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img src="{up}assets/img/{slug}-{biggest}.webp" alt="" '
            f'width="1600" height="1200" loading="lazy" decoding="async">'
            f'</picture></div>')


def page_student_work(mode, depth=0):
    """Student work, grouped by discipline.

    These are real learner projects rather than illustrative stand-ins. Names
    are not published yet — the centre is confirming permission with each maker
    — so a card credits the software and describes the work instead.
    """
    groups = ""
    total = 0
    for title, key, items in STUDENT_WORK:
        cards = ""
        for i, (slug, name, sw, blurb) in enumerate(items):
            media = _sw_media(slug, depth)
            if not media:
                continue
            cards += f'''<article class="card rv" data-tags="{key}" data-delay="{(i % 3) * 50}">
  {media}
  <div class="card__body">
    <h3 class="t-h3">{name}</h3>
    <p class="t-small t-muted">{blurb}</p>
    <div class="tags card__roles"><span class="tag">{sw}</span></div>
  </div>
</article>'''
        n = cards.count("<article")
        total += n
        plural = "" if n == 1 else "s"
        groups += f'''
<section class="progroup" id="sw-{key}" data-group="{key}" aria-labelledby="sw-{key}-h">
  <div class="progroup__head">
    <div class="progroup__title">
      <h2 class="t-h2" id="sw-{key}-h">{title}</h2>
      <p class="progroup__count label">{n} project{plural}</p>
    </div>
  </div>
  <div class="grid g-3 progroup__grid">{cards}</div>
</section>'''

    return f'''
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / Student work</p>
    <h1 class="t-display mb-3">The work you will be able to do.</h1>
    <p class="t-lead measure">Every project on this page was built by a learner at the Sector 14 centre
      &mdash; modelled, detailed and rendered in the same software the industry runs on.</p>
    <p class="note mt-4" style="max-width:66ch">Projects are credited by software and discipline. We are
      confirming permission with each maker before publishing names alongside their work.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="flex jcb aic wrapf gap-3 mb-4">
      <div class="filters" data-filter-group data-filter-target="#sw-list" data-filter-empty="#sw-empty" data-filter-count="#sw-count">
        <span class="label" style="margin-right:8px">Discipline</span>
        <button class="chip" data-filter="all" aria-pressed="true">All</button>
        <button class="chip" data-filter="arch" aria-pressed="false">Architecture &amp; Interior</button>
        <button class="chip" data-filter="mech" aria-pressed="false">Mechanical &amp; Product</button>
      </div>
      <p class="label"><span id="sw-count">{total}</span> projects</p>
    </div>
    <div id="sw-list">{groups}</div>
    <div id="sw-empty" class="note is-hidden mt-4">Nothing here yet for that combination. Try a wider filter, or see everything.</div>
  </div>
</section>
</main>
'''


def page_finder(mode, depth=0):
    def choices(name, opts, nxt="auto"):
        out = '<div class="choices">'
        for val, label in opts:
            out += f'<label class="choice"><input type="radio" name="{name}" value="{val}"><span>{label}</span></label>'
        return out + "</div>"

    base = "" if mode == "spa" else "../"
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / Career path finder</p>
    <h1 class="t-display mb-3">Find your career path<br>in 60 seconds.</h1>
    <p class="t-lead measure">Four questions. No sign-up, no phone number, and you see the result before we ask for anything.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="formcard" data-finder data-base="{base}">
      <div class="steps">
        <span class="label" data-step-label>Step 1 of 4</span>
        <span class="steps__bar"><span class="steps__fill" data-steps-fill style="width:0%"></span></span>
      </div>

      <div class="panel" data-active="true">
        <h2 class="t-h2 mb-3">What did you study?</h2>
        {choices("background", [("civil","Civil engineering"),("mech","Mechanical engineering"),("arch","Architecture"),("elec","Electrical engineering"),("other","Something else")])}
      </div>

      <div class="panel" data-active="false">
        <h2 class="t-h2 mb-3">Where are you right now?</h2>
        {choices("stage", [("studying","Still studying"),("fresher","Graduated, looking for my first role"),("upskill","Working, want to upskill"),("switch","Working, want to change direction")])}
        <button class="btn btn--ghost mt-3" data-finder-back type="button">&larr; Back</button>
      </div>

      <div class="panel" data-active="false">
        <h2 class="t-h2 mb-3">What kind of work interests you most?</h2>
        {choices("interest", [("buildings","Buildings and how they are designed"),("infra","Roads, infrastructure and terrain"),("products","Products and how they are made"),("analysis","Analysis, simulation and whether it holds up"),("planning","Planning, cost and delivery"),("unsure","Honestly, not sure yet")])}
        <button class="btn btn--ghost mt-3" data-finder-back type="button">&larr; Back</button>
      </div>

      <div class="panel" data-active="false" data-next="result">
        <h2 class="t-h2 mb-3">What are you trying to achieve?</h2>
        {choices("goal", [("job","Get my first job"),("better","Get better at what I already do"),("change","Change what I do"),("abroad","Work internationally")])}
        <button class="btn btn--ghost mt-3" data-finder-back type="button">&larr; Back</button>
      </div>

      <div class="panel" data-active="false">
        <div class="result">
          <div class="result__head">
            <p class="label" style="color:#C4C4C4">Your recommended path</p>
            <h2 class="t-h2 mt-1" style="color:#fff" data-r-name>&nbsp;</h2>
          </div>
          <div class="result__body">
            <p class="label label--accent">Why this fits</p>
            <p class="mb-4" data-r-why>&nbsp;</p>

            <p class="label label--accent">Skills roadmap</p>
            <div class="roadmap mb-4" data-r-roadmap></div>

            <div class="grid g-2 mb-4">
              <div>
                <p class="label label--accent">Roles this leads to</p>
                <ul class="t-small mt-1" style="padding-left:1.1rem;color:var(--c-ink-2)" data-r-roles></ul>
              </div>
              <div>
                <p class="label label--accent">Recommended starting point</p>
                <p class="t-h3 mt-1" data-r-tier>&nbsp;</p>
                <p class="t-small t-muted" data-r-tiernote>&nbsp;</p>
              </div>
            </div>

            <div class="note is-hidden mb-4" data-r-intl>Because you are aiming at international roles, ask about certification and international standards for this path in your counselling session &mdash; requirements differ by market.</div>

            <div class="flex wrapf gap-2">
              <a class="btn btn--primary" {L("contact", mode, depth)}>Book a counselling slot</a>
              <a class="btn btn--secondary" href="{WHATSAPP_LINK}">WhatsApp an advisor</a>
              <a class="btn btn--ghost" data-r-link href="#">See the full path</a>
            </div>

            <div class="dim mt-4">
              <p class="t-small t-muted">Want this sent to you? Enter your number and we will WhatsApp the full path guide and syllabus. Optional &mdash; the result stays visible either way.</p>
              <button class="btn btn--ghost mt-2" data-finder-restart type="button">Start again</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <p class="note mt-4" style="max-width:min(680px,100%)">This is a starting point, not a verdict. If the result does not feel right, tell a career advisor why &mdash; that conversation is usually more useful than the quiz.</p>
  </div>
</section>
</main>
"""


def page_corporate(mode, depth=0):
    return f"""
<main id="main">
<section class="section section--inverse">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / Industry / Corporate training</p>
    <h1 class="t-display mb-3">Corporate training for engineering<br>and design teams.</h1>
    <p class="t-lead" style="color:#C4C4C4;max-width:64ch">Software licences do not create capability. Teams do. We deliver structured, assessed training for engineering, design and project teams &mdash; on your site or at our Sector 14 centre &mdash; built around the workflows your people actually run rather than a generic syllabus.</p>
    <a class="btn btn--primary mt-4" href="#corp-form">Request a proposal</a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <figure class="figure mb-6">{photo("corporate", depth, "100vw")}<figcaption>Illustrative image</figcaption></figure>
    <div class="marker"><span class="label label--accent">Engagement models</span></div>
    <h2 class="t-h2 mb-4">Four ways we deliver</h2>
    <div class="grid g-4">
      <div class="pillar"><h3 class="t-h3 mb-2">On-site delivery</h3><p class="t-small t-muted">Our trainer at your premises, scheduled around operational commitments.</p></div>
      <div class="pillar"><h3 class="t-h3 mb-2">At our centre</h3><p class="t-small t-muted">Your team in our lab, with equipment and licences provided.</p></div>
      <div class="pillar"><h3 class="t-h3 mb-2">Blended</h3><p class="t-small t-muted">Instructor-led core with structured self-paced practice.</p></div>
      <div class="pillar"><h3 class="t-h3 mb-2">Assessment</h3><p class="t-small t-muted">Skills benchmarking across a team to identify gaps before training design.</p></div>
    </div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap grid g-2">
    <div>
      <h2 class="t-h2 mb-3">What an engagement includes</h2>
      <ul class="stack t-small" style="padding-left:1.1rem;color:var(--c-ink-2)">
        <li>Pre-training capability assessment</li>
        <li>A syllabus built against your workflows and standards</li>
        <li>Delivery by a practising trainer</li>
        <li>Assessed outcomes rather than attendance certificates</li>
        <li>A post-training capability report for your L&amp;D records</li>
      </ul>
    </div>
    <div>
      <h2 class="t-h2 mb-3">Common briefs we handle</h2>
      <ul class="stack t-small" style="padding-left:1.1rem;color:var(--c-ink-2)">
        <li>Migrating a drafting team from 2D CAD to BIM</li>
        <li>Standardising modelling practice across offices</li>
        <li>Bringing a mechanical design team onto a new CAD platform</li>
        <li>Building planning capability in a project controls team</li>
        <li>GD&amp;T standardisation between design and quality functions</li>
      </ul>
    </div>
  </div>
</section>

<section class="section" id="corp-form">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Enquiry</span></div>
    <h2 class="t-h2 mb-2">Request a proposal</h2>
    <p class="t-lead measure mb-4">Tell us the capability gap and we will come back with a scoped approach, not a brochure.</p>
    <form class="formcard" onsubmit="return false">
      <div class="grid g-2">
        <div class="field"><label for="c1">Name</label><input id="c1" type="text" required></div>
        <div class="field"><label for="c2">Designation</label><input id="c2" type="text"></div>
      </div>
      <div class="grid g-2">
        <div class="field"><label for="c3">Company</label><input id="c3" type="text" required></div>
        <div class="field"><label for="c4">Work email</label><input id="c4" type="email" required></div>
      </div>
      <div class="grid g-2">
        <div class="field"><label for="c5">Phone</label><input id="c5" type="tel" inputmode="numeric"></div>
        <div class="field"><label for="c6">Team size</label>
          <select id="c6"><option>1&ndash;5</option><option>6&ndash;15</option><option>16&ndash;40</option><option>40+</option></select></div>
      </div>
      <div class="field"><label for="c7">What is the requirement?</label><textarea id="c7" rows="4"></textarea></div>
      <button class="btn btn--primary btn--wide" type="submit">Request a proposal</button>
      <p class="t-small t-muted mt-2">Corporate enquiries are handled by a dedicated team, not the admissions desk.</p>
    </form>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <p class="note">Corporate engagements are contracted through Vara Global Tech, which owns and operates CADD Centre Gurugram, Sector 14 &mdash; an Authorised Training Centre of CADD Centre Training Services.</p>
  </div>
</section>
</main>
"""


def _centre_tile(slug, title, caption, depth=0, wide=False):
    """One photo of the centre. Only the widths actually generated are offered,
    because the source photographs vary in resolution."""
    import os as _os
    here = _os.path.dirname(_os.path.abspath(__file__))
    up = "../" * depth
    have = [w for w in (480, 960, 1600)
            if _os.path.exists(_os.path.join(here, "assets/img", f"{slug}-{w}.webp"))]
    if not have:
        return ""
    sizes = "(max-width: 767px) 100vw, (max-width: 1100px) 50vw, 33vw"

    def srcset(ext):
        return ", ".join(f"{up}assets/img/{slug}-{w}.{ext} {w}w" for w in have)

    cls = "centretile centretile--wide" if wide else "centretile"
    return (f'<figure class="{cls}">'
            f'<picture>'
            f'<source type="image/avif" srcset="{srcset("avif")}" sizes="{sizes}">'
            f'<source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img src="{up}assets/img/{slug}-{have[-1]}.webp" alt="{title} at CADD Centre Gurugram, Sector 14" '
            f'width="1600" height="1200" loading="lazy" decoding="async">'
            f'</picture>'
            f'<figcaption><strong>{title}</strong><span>{caption}</span></figcaption>'
            f'</figure>')


def page_about(mode, depth=0):
    # Trainer cards render only from verified records. With none on file the
    # section invites a visit rather than printing an empty placeholder.
    if TRAINERS:
        trainer_block = '<div class="grid g-4">' + "".join(
            f'<div class="trainer rv"><div class="trainer__img"></div><div class="trainer__body">'
            f'<p class="label label--accent">{t["specialisms"]}</p>'
            f'<h3 class="t-h3 mt-1">{t["name"]}</h3>'
            f'<p class="t-small t-muted mt-1">{t["experience"]} &middot; {t["background"]}</p>'
            f'</div></div>' for t in TRAINERS) + '</div>'
    else:
        trainer_block = (
            '<div class="note" style="max-width:66ch">'
            '<strong>Meet them before you enrol.</strong> We would rather you met your trainer in '
            'person than read a paragraph about them. Book a free demo class and sit in on the '
            'session you would actually be joining.</div>')
    up = "../" * depth

    # What we do differently — the same four points, as cards.
    DIFF = [
        ("target", "We organise around careers, not software.",
         "You should not need to know whether you want Revit Structure or Civil 3D before you can talk to us."),
        ("layers", "We publish real work.",
         "Everything in Student Work was made here, by learners."),
        ("mentor", "We name our trainers.",
         "You know who will teach you, and you can meet them before you pay."),
        ("shield", "We are honest about placement.",
         "We do not advertise guarantees we cannot keep."),
    ]
    diff_cards = "".join(
        f'<article class="abcard rv" data-delay="{i*60}">'
        f'<span class="abcard__ico">{icon(ic)}</span>'
        f'<h3 class="abcard__t">{title}</h3>'
        f'<p class="abcard__d">{body}</p></article>'
        for i, (ic, title, body) in enumerate(DIFF))

    # Milestones, drawn from the network paragraph already on this page.
    MILES = [("1988", "CADD Centre Training Services founded"),
             ("Today", "One of Asia&rsquo;s largest CAD training networks"),
             ("Sector 14", "This centre, operated by Vara Global Tech"),
             ("NSDC", "Collaboration to strengthen employability")]
    miles = "".join(
        f'<li class="mile"><span class="mile__dot" aria-hidden="true"></span>'
        f'<strong>{k}</strong><span>{v}</span></li>' for k, v in MILES)

    return f"""
<main id="main">

<section class="section abhero">
  <div class="wrap abhero__inner">
    <div class="abhero__copy">
      <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / About</p>
      <p class="label label--accent proghero__kicker">About CADD Centre Gurugram</p>
      <h1 class="t-display mt-2 mb-3">CADD Centre Gurugram,<br><em>Sector 14.</em></h1>
      <p class="t-lead measure">We run industry-focused programmes in CAD, BIM, product design, structural engineering, project management and AI-assisted engineering workflows. We are an Authorised Training Centre of CADD Centre Training Services, and we are operated by Vara Global Tech.</p>
      <div class="flex wrapf gap-2 mt-4">
        <a class="btn btn--primary" {L("finder", mode, depth)}>Find My Career Path</a>
        <a class="btn btn--secondary" {L("contact", mode, depth)}>Book a Centre Visit</a>
      </div>
    </div>
    <div class="abhero__art">{photo("facilities", depth, "(max-width:900px) 100vw, 46vw")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">The centre</span></div>
    <h2 class="t-h2 mb-2">Inside Sector 14</h2>
    <p class="t-lead measure mb-6">Not a stock photograph of somewhere else &mdash; this is the building you would walk into, the labs you would work in and the room the 3D printer sits in.</p>
    <div class="centrelead">
      <figure class="tcard">
        <button class="tcard__media" type="button" data-testi
          data-src="{up}assets/video/centre-intro-preview.mp4"
          data-full="{up}assets/video/centre-intro.mp4"
          data-name="a walk through the Sector 14 centre"
          aria-label="Play a short introduction to the Sector 14 centre">
          <img class="tcard__poster" src="{up}assets/img/testimonials/centre-intro.webp" alt="" loading="lazy" decoding="async">
          <video class="tcard__vid" muted loop playsinline preload="none" width="1080" height="1920" aria-hidden="true"></video>
          <span class="tcard__play" aria-hidden="true"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></span>
          <span class="tcard__sound" aria-hidden="true">Click for sound</span>
        </button>
      </figure>
      <div class="centrelead__copy">
        <p class="label label--accent">A minute inside</p>
        <h3 class="t-h3 mt-1 mb-2">Come and see the place.</h3>
        <p class="t-small t-muted">The fastest way to decide whether we are right for you is to walk in.
          We are open seven days a week, 9:30 am to 7:00 pm.</p>
        <a class="btn btn--secondary mt-3" {L("contact", mode, depth)}>Book a centre visit</a>
      </div>
    </div>
  </div>
</section>

<section class="section abstats-wrap" style="padding-block:0">
  <div class="wrap">
    <div class="abstats">
      <div class="abstat"><span class="abstat__ico">{icon("calendar")}</span>
        <strong>1988</strong><span>CADD Centre founded</span></div>
      <div class="abstat"><span class="abstat__ico">{icon("star")}</span>
        <strong>4.9</strong><span>Google rating, 207 reviews</span></div>
      <div class="abstat"><span class="abstat__ico">{icon("pin")}</span>
        <strong>Sector 14</strong><span>Authorised training centre</span></div>
      <div class="abstat"><span class="abstat__ico">{icon("clock")}</span>
        <strong>7 days</strong><span>Open 9:30 am &ndash; 7:00 pm</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap abstory">
    <div>
      <div class="marker"><span class="label label--accent">Who we are</span></div>
      <h2 class="t-h2 mb-3">The local part matters more than the national part</h2>
      <p>What the franchise means in practice is that we carry the curriculum, certification and standards of a national training network, and we run them locally &mdash; with our own trainers, our own labs, our own equipment, and our own relationships with employers in the NCR.</p>
      <p>A curriculum is a document. What actually determines whether you come out employable is who teaches you, how much you build, and who is willing to introduce you to a hiring manager. Those things happen in a room in Sector 14, not on a network map.</p>
    </div>
    <div class="abstory__art">{_centre_tile("centre-reception", "Reception", "Walk in here. Certifications on the wall behind the desk.", depth)}</div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">What we do differently</span></div>
    <h2 class="t-h2 mb-6">Four things we hold to</h2>
    <div class="abgrid">{diff_cards}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Who teaches you</span></div>
    <h2 class="t-h2 mb-2">Practitioners, not presenters.</h2>
    <p class="t-lead measure mb-6">Every trainer here worked in the field before they taught it. You will know your trainer's name, their background and their experience before you enrol &mdash; and you can meet them in a free demo class before you pay anything.</p>
    {trainer_block}
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Facilities</span></div>
    <h2 class="t-h2 mb-2">Where you will actually work</h2>
    <p class="t-lead measure mb-6">Come and see it. That invitation is not a formality &mdash; the equipment is the argument.</p>
    <div class="centregrid">
      {_centre_tile("centre-lab", "Workstations &amp; labs", "Licensed software on machines specified for the work &mdash; modelling, rendering and analysis have very different demands.", depth)}
      {_centre_tile("centre-printlab", "The 3D printing lab", "Where a CAD model becomes a physical part you can hold. Open to learners across the mechanical and product design paths.", depth)}
      {_centre_tile("centre-classroom", "Classrooms &amp; review space", "Small batches, so a trainer can look over your shoulder while you are still making the mistake.", depth)}
      {_centre_tile("centre-teaching", "Teaching room", "Domain expertise and the tools that go with it.", depth)}
      {_centre_tile("centre-corridor", "The corridor", "Glass classrooms, one per discipline.", depth)}
    </div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap abnet">
    <div>
      <div class="marker"><span class="label label--accent">The network</span></div>
      <h2 class="t-h2 mb-3">The network behind this centre</h2>
      <p class="measure">CADD Centre Training Services was founded in 1988 and has grown into one of Asia's largest CAD training networks.</p>
      <p class="measure">CADD Centre has long been at the forefront of design engineering, transforming lives through future-ready learning. From being a trusted technical training institute to becoming a hub for next-generation skill development, CADD Centre has continuously evolved to meet the demands of a dynamic world.</p>
      <p class="measure">CADD Centre Gurugram also works in collaboration with the <strong>National Skill Development Corporation (NSDC)</strong> to strengthen learner employability.</p>
    </div>
    <ul class="miles">{miles}</ul>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="progcta">
      <span class="progcta__ico">{icon("target")}</span>
      <div class="progcta__copy">
        <strong>Not sure which programme is right for you?</strong>
        <span>Four questions. No sign-up, and you see the result before we ask for anything.</span>
      </div>
      <a class="btn btn--primary" {L("finder", mode, depth)}>Find My Career Path</a>
    </div>
  </div>
</section>
</main>
"""


def page_contact(mode, depth=0):
    def ch(name, opts):
        out = '<div class="choices">'
        for v, l in opts:
            out += f'<label class="choice"><input type="radio" name="{name}" value="{v}"><span>{l}</span></label>'
        return out + "</div>"

    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / Contact</p>
    <h1 class="t-display mb-3">Come and see the place.</h1>
    <p class="t-lead measure">The fastest way to decide whether we are right for you is to walk in. We are open seven days a week, 9:30 am to 7:00 pm.</p>
  </div>
</section>

<section class="section">
  <div class="wrap grid g-2">
    <div>
      <div class="marker"><span class="label label--accent">Start here</span></div>
      <h2 class="t-h2 mb-4">Let's find the right programme for you.</h2>

      <div class="formcard" data-leadform>
        <div class="steps">
          <span class="label" data-step-label>Step 1 of 4</span>
          <span class="steps__bar"><span class="steps__fill" data-steps-fill style="width:0%"></span></span>
        </div>

        <div class="panel" data-active="true">
          <h3 class="t-h3 mb-3">What best describes you?</h3>
          {ch("lead_stage", [("studying","Student"),("fresher","Fresher"),("upskill","Working professional"),("switch","Changing career")])}
        </div>

        <div class="panel" data-active="false">
          <h3 class="t-h3 mb-3">What is your background?</h3>
          {ch("lead_background", [("civil","Civil"),("mech","Mechanical"),("arch","Architecture"),("elec","Electrical"),("other","Other")])}
          <button class="btn btn--ghost mt-3" data-lead-back type="button">&larr; Back</button>
        </div>

        <div class="panel" data-active="false">
          <h3 class="t-h3 mb-3">What do you want to achieve?</h3>
          {ch("lead_goal", [("job","Get a job"),("better","Upskill in my current role"),("change","Switch career"),("abroad","Work abroad")])}
          <button class="btn btn--ghost mt-3" data-lead-back type="button">&larr; Back</button>
        </div>

        <div class="panel" data-active="false" data-next="manual">
          <h3 class="t-h3 mb-3">Where should we send your recommendation?</h3>
          <div class="field">
            <label for="ln">Your name</label>
            <input id="ln" name="lead_name" type="text" required autocomplete="name">
            <span class="field__err">Please enter your name</span>
          </div>
          <div class="field">
            <label for="lp">Mobile number</label>
            <input id="lp" name="lead_phone" type="tel" inputmode="numeric" required autocomplete="tel">
            <span class="field__help">We will send your recommendation here on WhatsApp</span>
            <span class="field__err">Enter a 10-digit mobile number</span>
          </div>
          <div class="field">
            <label for="le">Email address (optional)</label>
            <input id="le" name="lead_email" type="email" autocomplete="email">
            <span class="field__err">Enter a valid email address, or leave this blank</span>
          </div>
          <p class="t-small t-muted mb-3">By continuing you agree to be contacted by CADD Centre Gurugram about programmes and admissions.</p>
          <button class="btn btn--primary btn--wide" data-lead-submit type="button">Show my recommendation</button>
          <button class="btn btn--ghost mt-2" data-lead-back type="button">&larr; Back</button>
        </div>

        <div class="panel" data-active="false">
          <h3 class="t-h2 mb-2">Here is your recommendation, <span data-reward-name>there</span>.</h3>
          <p class="t-small t-muted mb-3">Based on what you told us, this is the path that makes the most sense from where you are.</p>
          <p class="label label--accent">Recommended path</p>
          <p class="t-h3 mb-3" data-reward-path>&nbsp;</p>
          <p class="label label--accent">Skills roadmap</p>
          <div class="roadmap mb-3" data-reward-roadmap></div>
          <p class="label label--accent">Starting point</p>
          <p class="mb-4" data-reward-tier>&nbsp;</p>

          <div class="dim">
            <h4 class="t-h3 mb-1">When would you like us to call?</h4>
            <p class="t-small t-muted mb-2">Pick a slot that actually works for you. We would rather call you when you can talk than catch you in a lecture.</p>
            <div data-sched-group>
              <p class="label mb-1">Day</p>
              <div class="slots mb-3">
                <button class="chip" data-sched="day" aria-pressed="false" type="button">Today</button>
                <button class="chip" data-sched="day" aria-pressed="false" type="button">Tomorrow</button>
                <button class="chip" data-sched="day" aria-pressed="false" type="button">This weekend</button>
              </div>
            </div>
            <div data-sched-group>
              <p class="label mb-1">Time</p>
              <div class="slots mb-3">
                <button class="chip" data-sched="time" aria-pressed="false" type="button">10 am &ndash; 12 pm</button>
                <button class="chip" data-sched="time" aria-pressed="false" type="button">12 pm &ndash; 2 pm</button>
                <button class="chip" data-sched="time" aria-pressed="false" type="button">2 pm &ndash; 4 pm</button>
                <button class="chip" data-sched="time" aria-pressed="false" type="button">4 pm &ndash; 6 pm</button>
                <button class="chip" data-sched="time" aria-pressed="false" type="button">6 pm &ndash; 7 pm</button>
              </div>
            </div>
            <div data-sched-group>
              <p class="label mb-1">How would you prefer to connect?</p>
              <div class="slots mb-3">
                <button class="chip" data-sched="channel" aria-pressed="false" type="button">WhatsApp</button>
                <button class="chip" data-sched="channel" aria-pressed="false" type="button">Phone call</button>
                <button class="chip" data-sched="channel" aria-pressed="false" type="button">Video</button>
                <button class="chip" data-sched="channel" aria-pressed="false" type="button">Visit the centre</button>
              </div>
            </div>
            <button class="btn btn--primary btn--wide" data-sched-confirm type="button" disabled>Confirm my slot</button>
          </div>
        </div>

        <div class="panel" data-active="false">
          <p class="label label--accent">Booked</p>
          <h3 class="t-h2 mb-2" data-sched-summary>&nbsp;</h3>
          <p class="t-small t-muted mb-3">An advisor will contact you then. If something changes, message us on WhatsApp and we will move it &mdash; no need to explain.</p>
          <div class="flex wrapf gap-2">
            <a class="btn btn--primary" href="{WHATSAPP_LINK}">Message us on WhatsApp</a>
            <a class="btn btn--ghost" href="tel:{PHONE}">Call {PHONE_D}</a>
          </div>
        </div>
      </div>
    </div>

    <div>
      <div class="marker"><span class="label label--accent">Or just turn up</span></div>
      <h2 class="t-h2 mb-3">Experience CADD before you decide.</h2>
      <p class="t-lead mb-3">Come in for an hour. There is no charge, no obligation, and no sales pitch you cannot walk out of.</p>
      <ul class="stack" style="list-style:none;padding:0;margin:0 0 var(--s-4)">
        {''.join(f'<li class="dim t-small">{t}</li>' for t in ["Meet the trainer who would actually teach you","See the labs and the equipment","Sit in on a live class","Look at real student projects","Try the software yourself","Get honest career guidance"])}
      </ul>

      <div class="story">
        <p class="label label--accent mb-2">Visit us</p>
        <p class="mb-2">{ADDRESS}</p>
        <p class="t-small t-muted mb-3">Landmark: near Haldiram, Sector 14</p>
        <dl>
          <div class="story__row"><dt>Phone</dt><dd><a href="tel:{PHONE}" style="text-decoration:none">{PHONE_D}</a></dd></div>
          <div class="story__row"><dt>Email</dt><dd><a href="mailto:{EMAIL}" style="text-decoration:none">{EMAIL}</a></dd></div>
          <div class="story__row"><dt>Open</dt><dd>7 days &middot; 9:30 am &ndash; 7:00 pm</dd></div>
        </dl>
      </div>

    </div>
  </div>
</section>
</main>
"""
