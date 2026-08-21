# -*- coding: utf-8 -*-
"""Remaining page bodies."""

from build_parts import figure, photo, photo_card
from build_pages import _faq
from build_shell import L, PHONE, PHONE_D, WHATSAPP, WHATSAPP_LINK, EMAIL, ADDRESS

from build_data import PROGRAMS as ALL_PROGRAMS, MASTERS, TRAINERS, STORIES

TIER_TAG = {"Master": "master", "Professional": "cert", "Short-term": "short"}


def page_programs(mode, depth=0):
    """Programmes index, grouped by department.

    Every course belongs to a department, so the page is built that way rather
    than as one undifferentiated grid: a department is a titled section with
    its own heading, outcome line and course count, and the courses inside it
    are ordered by level so the progression reads the same way in every
    department. The filter chips still work across the whole page — a
    department whose courses are all filtered out hides itself.
    """
    from build_render import program_media
    from build_shell import DEPARTMENTS

    depts = [d for d in DEPARTMENTS if d["courses"]]
    by_slug = {x[0]: x for x in ALL_PROGRAMS}
    # Master first, then Professional, then Short-term — the same progression
    # in every department, so the reading order is predictable.
    tier_order = {"Master": 0, "Professional": 1, "Short-term": 2}

    jump = f'<a class="deptjump__i" href="#dept-master">Master Certificates<span class="deptjump__n">{len(MASTERS)}</span></a>'
    jump += "".join(
        f'<a class="deptjump__i" href="#dept-{d["key"]}">{d["name"]}'
        f'<span class="deptjump__n">{len(d["courses"])}</span></a>'
        for d in depts)

    # Master Certificates are the long-format flagship programmes. They are not
    # tied to a single department the way a software course is, so they get
    # their own section at the top rather than being filed under one of them.
    # They have no individual pages yet, so each card carries its own detail
    # and sends the reader to an advisor rather than to a link that is not
    # there.
    master_cards = ""
    for m in MASTERS:
        mslug, mname, mcat, mpkey, mtier, mdur, msw, mheadline = m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7]
        mdeliverable, mmodules, mroles = m[8], m[9], m[10]
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
      <p class="progroup__count label">{len(MASTERS)} programmes</p>
    </div>
    <p class="progroup__outcome t-small t-muted">Long-format programmes that run six to eight months and take you from no experience to a portfolio you can be hired on. Each one combines several software courses with a single continuous project.</p>
  </div>
  <div class="grid g-3 progroup__grid">{master_cards}</div>
</section>"""

    for d in depts:
        progs = sorted((by_slug[cs] for cs, _cn in d["courses"]),
                       key=lambda x: (tier_order.get(x[4], 9), x[1]))
        cards = ""
        for i, pr in enumerate(progs):
            slug, name, cat, pkey, tier, dur, sw, headline = pr[0], pr[1], pr[2], pr[3], pr[4], pr[5], pr[6], pr[7]
            tags = f"{pkey} {TIER_TAG.get(tier, 'short')}"
            cards += f"""<a class="card rv" data-tags="{tags}" data-delay="{(i%3)*50}" {L("program:" + slug, mode, depth)}>
  {program_media(slug, pkey, depth)}
  <div class="card__body">
    <p class="label label--accent">{tier} &middot; {cat}</p>
    <h3 class="t-h3">{name}</h3>
    <p class="t-small t-muted">{headline}.</p>
    <div class="tags card__roles"><span class="tag">{dur}</span><span class="tag">{sw}</span></div>
  </div>
</a>"""
        n = len(progs)
        groups += f"""
<section class="progroup" id="dept-{d['key']}" data-group="{d['key']}" aria-labelledby="dept-{d['key']}-h">
  <div class="progroup__head">
    <div class="progroup__title">
      <h2 class="t-h2" id="dept-{d['key']}-h">{d['name']}</h2>
      <p class="progroup__count label">{n} course{'' if n == 1 else 's'}</p>
    </div>
    <p class="progroup__outcome t-small t-muted">{d['outcome']}</p>
    <a class="alink progroup__path" {L("path:" + d['key'], mode, depth)}>Where this department leads
      <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></a>
  </div>
  <div class="grid g-3 progroup__grid">{cards}</div>
</section>"""

    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / Programmes</p>
    <h1 class="t-display mb-3">{len(ALL_PROGRAMS) + len(MASTERS)} programmes.<br>{len(depts)} departments.</h1>
    <p class="t-lead measure">Every course sits inside a department and opens into a module-by-module curriculum. Jump straight to a department below, or filter by level if you already know what you need.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <nav class="deptjump" aria-label="Jump to department">{jump}</nav>

    <div class="flex jcb aic wrapf gap-3 mb-4 progfilter">
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
      <p class="label"><span id="prog-count">{len(ALL_PROGRAMS) + len(MASTERS)}</span> programmes</p>
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


def page_student_work(mode, depth=0):
    items = [
        ("Commercial building BIM coordination", "proj-bim-coordination", "bim", "Revit &middot; Navisworks", "Federated architectural, structural and MEP model, clash-checked and issued as a drawing set."),
        ("Highway corridor design", "proj-highway-corridor", "civil", "Civil 3D", "Alignment, profile, corridor model and extracted earthwork quantities."),
        ("RCC structural analysis", "proj-rcc-structure", "struct", "STAAD.Pro &middot; ETABS", "Analysis model, load cases, code checks and structural detailing for an RCC frame."),
        ("Mechanical assembly", "proj-mechanical-assembly", "mech", "SolidWorks &middot; GD&amp;T", "Parts, mates, interference checks and a fully toleranced drawing set."),
        ("Architectural visualisation", "proj-architectural-viz", "arch", "Revit &middot; V-Ray", "Concept model taken through materials, lighting and final render."),
        ("Construction programme", "proj-construction-programme", "pm", "Primavera P6", "WBS, critical path, resource loading and earned-value reporting."),
        ("Product prototype", "printing", "mech", "CAD &middot; 3D printing", "A designed part taken from model to printed physical component."),
        ("MEP services coordination", "proj-mep-coordination", "mep", "Revit MEP &middot; Navisworks", "HVAC, plumbing and electrical routed and coordinated against the architectural model."),
    ]
    cards = ""
    for i, (title, slot, tag, sw, blurb) in enumerate(items):
        media = photo_card(slot, depth, "Representative") if slot else figure(tag if tag in ("bim","civil","arch","mech","struct","mep","pm") else "bim")
        cards += f"""<article class="card rv" data-tags="{tag}" data-delay="{(i%3)*50}">
  {media}
  <div class="card__body">
    <h3 class="t-h3">{title}</h3>
    <p class="t-small t-muted">{blurb}</p>
    <div class="tags card__roles"><span class="tag">{sw}</span></div>
  </div>
</article>"""
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / Student work</p>
    <h1 class="t-display mb-3">The work you will be able to do.</h1>
    <p class="t-lead measure">These are representative projects &mdash; illustrative examples of the deliverables and industry workflows our programmes cover. Filter by discipline to see what each career path actually produces.</p>
    <p class="note mt-4" style="max-width:66ch">Every project we publish carries the maker's name and their written permission. A portfolio you can verify is worth more than one you cannot.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="flex jcb aic wrapf gap-3 mb-4">
      <div class="filters" data-filter-group data-filter-target="#sw-list" data-filter-empty="#sw-empty" data-filter-count="#sw-count">
        <span class="label" style="margin-right:8px">Discipline</span>
        <button class="chip" data-filter="all" aria-pressed="true">All</button>
        <button class="chip" data-filter="bim" aria-pressed="false">BIM</button>
        <button class="chip" data-filter="civil" aria-pressed="false">Civil</button>
        <button class="chip" data-filter="struct" aria-pressed="false">Structural</button>
        <button class="chip" data-filter="mech" aria-pressed="false">Mechanical</button>
        <button class="chip" data-filter="mep" aria-pressed="false">MEP</button>
        <button class="chip" data-filter="arch" aria-pressed="false">Architecture</button>
        <button class="chip" data-filter="pm" aria-pressed="false">Planning</button>
      </div>
      <p class="label"><span id="sw-count">{len(items)}</span> projects</p>
    </div>
    <div class="grid g-3" id="sw-list">{cards}</div>
    <div id="sw-empty" class="note is-hidden mt-4">Nothing here yet for that combination. Try a wider filter, or see everything.</div>

  </div>
</section>
</main>
"""


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
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / About</p>
    <h1 class="t-display mb-3">CADD Centre Gurugram,<br>Sector 14.</h1>
    <p class="t-lead measure">We run industry-focused programmes in CAD, BIM, product design, structural engineering, project management and AI-assisted engineering workflows. We are an Authorised Training Centre of CADD Centre Training Services, and we are operated by Vara Global Tech.</p>
  </div>
</section>

<section class="section">
  <div class="wrap grid g-2">
    <div>
      <h2 class="t-h2 mb-3">The local part matters more than the national part</h2>
      <p>What the franchise means in practice is that we carry the curriculum, certification and standards of a national training network, and we run them locally &mdash; with our own trainers, our own labs, our own equipment, and our own relationships with employers in the NCR.</p>
      <p>A curriculum is a document. What actually determines whether you come out employable is who teaches you, how much you build, and who is willing to introduce you to a hiring manager. Those things happen in a room in Sector 14, not on a network map.</p>
    </div>
    <div>
      <h2 class="t-h2 mb-3">What we do differently</h2>
      <div class="grid" style="gap:var(--s-2)">
        <div class="dim"><strong>We organise around careers, not software.</strong><br><span class="t-small t-muted">You should not need to know whether you want Revit Structure or Civil 3D before you can talk to us.</span></div>
        <div class="dim"><strong>We publish real work.</strong><br><span class="t-small t-muted">Everything in Student Work was made here, by learners.</span></div>
        <div class="dim"><strong>We name our trainers.</strong><br><span class="t-small t-muted">You know who will teach you, and you can meet them before you pay.</span></div>
        <div class="dim"><strong>We are honest about placement.</strong><br><span class="t-small t-muted">We do not advertise guarantees we cannot keep.</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Who teaches you</span></div>
    <h2 class="t-h2 mb-2">Practitioners, not presenters.</h2>
    <p class="t-lead measure mb-6">Every trainer here worked in the field before they taught it. You will know your trainer's name, their background and their experience before you enrol &mdash; and you can meet them in a free demo class before you pay anything.</p>
    {trainer_block}

  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Facilities</span></div>
    <h2 class="t-h2 mb-2">Where you will actually work</h2>
    <p class="t-lead measure mb-6">Come and see it. That invitation is not a formality &mdash; the equipment is the argument.</p>
    <figure class="figure mb-6">{photo("facilities", depth, "100vw")}<figcaption>Illustrative image &mdash; photography of the Sector 14 centre pending</figcaption></figure>
    <div class="grid g-3">
      <div class="pillar"><h3 class="t-h3 mb-2 mt-1">Workstations &amp; labs</h3><p class="t-small t-muted">Licensed software on machines specified for the work &mdash; modelling, rendering and analysis have very different demands.</p></div>
      <div class="pillar"><h3 class="t-h3 mb-2 mt-1">The 3D printing lab</h3><p class="t-small t-muted">Where a CAD model becomes a physical part you can hold. Open to learners across the mechanical and product design paths.</p></div>
      <div class="pillar"><h3 class="t-h3 mb-2 mt-1">Classrooms &amp; review space</h3><p class="t-small t-muted">Small batches, so a trainer can look over your shoulder while you are still making the mistake.</p></div>
    </div>
    <a class="btn btn--secondary mt-6" {L("contact", mode, depth)}>Book a centre visit</a>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">The network</span></div>
    <h2 class="t-h2 mb-3">The network behind this centre</h2>
    <p class="measure">CADD Centre Training Services was founded in 1988 and has grown into one of Asia's largest CAD training networks.</p>
    <p class="measure">CADD Centre has long been at the forefront of design engineering, transforming lives through future-ready learning. From being a trusted technical training institute to becoming a hub for next-generation skill development, CADD Centre has continuously evolved to meet the demands of a dynamic world.</p>
    <p class="measure">CADD Centre Gurugram also works in collaboration with the <strong>National Skill Development Corporation (NSDC)</strong> to strengthen learner employability.</p>


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
