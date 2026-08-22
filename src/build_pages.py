# -*- coding: utf-8 -*-
"""Page bodies. Copy is taken from Document 2 — Website Content & Copy Master."""

from build_parts import figure, hero_bg, wire, solid, photo, photo_card, icon, hero_picture, card_art, path_media
from build_shell import L, PHONE, PHONE_D, EMAIL, ADDRESS, DEPARTMENTS
from build_data import PROGRAMS as ALL_PROGRAMS
from build_reviews import reviews_section

PATH_CARDS = [
    ("bim", "path-bim", "BIM &amp; Digital Construction",
     "The way modern buildings are actually designed, coordinated and delivered.",
     "BIM Modeller &middot; BIM Engineer &middot; BIM Coordinator"),
    ("civil", "career-paths", "Civil &amp; Infrastructure Design",
     "Roads, corridors, terrain and quantities &mdash; designed digitally.",
     "Design Engineer &middot; Highway Designer &middot; Quantity Engineer"),
    ("arch", "career-paths", "Architecture &amp; Visualisation",
     "From concept model to a render a client will believe.",
     "Architectural Designer &middot; 3D Visualiser"),
    ("mech", "career-paths", "Mechanical &amp; Product Design",
     "Take a product from sketch to a manufacturable assembly.",
     "Design Engineer &middot; Product Designer &middot; CAD Engineer"),
    ("struct", "career-paths", "Structural Engineering &amp; Analysis",
     "Model it, analyse it, and prove it stands up.",
     "Structural Designer &middot; Analysis Engineer"),
    ("mep", "career-paths", "Electrical &amp; MEP Design",
     "The systems that make a building work.",
     "MEP Designer &middot; Electrical Design Engineer"),
    ("pm", "career-paths", "Project Planning &amp; Management",
     "Plan the schedule, hold the cost, deliver the project.",
     "Planning Engineer &middot; Cost Engineer"),
    ("ai", "career-paths", "AI &amp; Emerging Engineering Tech",
     "Automation, generative design and AI-assisted workflows.",
     "Design Automation Specialist &middot; BIM Technologist"),
]


def _path_grid(mode, depth, limit=8):
    out = ""
    for i, (kind, route, name, line, roles) in enumerate(PATH_CARDS[:limit]):
        out += f"""<a class="card rv" data-delay="{(i%4)*60}" {L(route, mode, depth)}>
  {path_media(kind, depth)}
  <div class="card__body">
    <h3 class="t-h3">{name}</h3>
    <p class="t-small t-muted">{line}</p>
    <p class="label card__roles">{roles}</p>
  </div>
</a>"""
    return out


# ============================================================================
# HOME
# ============================================================================
def testimonial_band(mode, depth=0):
    """Learner video testimonials, high on the home page.

    Sits directly under the accreditation strip, before the visitor has been
    asked to choose anything: proof works hardest before a decision, not after
    it. Shows the first four and sends the rest to the full page.

    Renders nothing until real footage is supplied, so a build on a machine
    without the video files cannot publish an empty section.
    """
    from build_parts import published_testimonials, testimonial_tiles
    items = published_testimonials()
    if not items:
        return ""
    more = ""
    if len(items) > 3:
        more = (f'<a class="btn btn--secondary mt-6" {L("testimonials", mode, depth)}>'
                f'See all {len(items)} learner stories</a>')
    return f"""
<section class="section testi" aria-labelledby="testi-h">
  <div class="wrap">
    <p class="label label--accent">What learners say</p>
    <h2 class="t-display mt-1 mb-2" id="testi-h">Hear it from them.</h2>
    <p class="t-lead measure mb-6">Not a marketing line and not a written quote we could have made up
      &mdash; the learners themselves, on camera, saying what the course did for them.</p>
    <div class="testi__grid">{testimonial_tiles(items[:3], depth)}</div>
    {more}
  </div>
</section>
"""


def accreditation_band(mode, depth=0):
    """Autodesk / PMI authorisation band for the home page.

    Only credentials we can actually evidence are published: an entry with
    neither logo nor certificate is skipped entirely rather than shown as an
    unsupported claim, which is the same rule the partner logo band follows.
    Supply the artwork in ACCREDITATIONS and the credential appears on the next
    build; supply none and the whole band disappears.
    """
    try:
        from build_data import PROGRAMS as ALL_PROGRAMS, ACCREDITATIONS
    except ImportError:
        return ""
    shown = [a for a in ACCREDITATIONS if a.get("logo") or a.get("cert")]
    if not shown:
        return ""

    up = "../" * depth
    cards = ""
    for a in shown:
        if a.get("logo"):
            mark = (f'<img class="cred__logoimg" src="{up}assets/img/logos/{a["logo"]}" '
                    f'alt="{a["awarding"]} {a["title"]}" '
                    f'width="{a["logo_w"]}" height="{a["logo_h"]}" decoding="async">')
        else:
            # Never invent a lockup for someone else's mark — set the name in
            # our own type instead until the official artwork arrives.
            mark = f'<span class="cred__wordmark">{a["awarding"]}</span>'

        if a.get("cert"):
            view = (f'<button class="cred__view" type="button" '
                    f'data-cert="{up}assets/img/certs/{a["cert"]}" '
                    f'data-cert-w="{a["cert_w"]}" data-cert-h="{a["cert_h"]}" '
                    f'data-cert-alt="{a["awarding"]} {a["title"]} certificate issued to '
                    f'CADD Centre Gurugram, Sector 14">View the certificate</button>')
        else:
            view = ""

        detail = f'<p class="cred__detail">{a["detail"]}</p>' if a.get("detail") else ""
        valid = f'<p class="cred__valid">{a["valid"]}</p>' if a.get("valid") else ""

        cards += (f'<article class="cred">'
                  f'<div class="cred__mark">{mark}</div>'
                  f'<div class="cred__body">'
                  f'<h3 class="cred__name">{a["awarding"]}</h3>'
                  f'<p class="cred__title">{a["title"]}</p>'
                  f'<p class="cred__note">{a["note"]}</p>'
                  f'{detail}{valid}{view}</div></article>')

    # One credential should not be stretched across the full width; two sit
    # side by side.
    wide = " creds__grid--single" if len(shown) == 1 else ""
    names = " and ".join(a["awarding"] for a in shown)

    return f"""
<section class="section creds" aria-labelledby="creds-h">
  <div class="wrap">
    <p class="label label--accent">Accreditation</p>
    <h2 class="t-h2 mt-1 mb-2" id="creds-h">Authorised by {names}.</h2>
    <p class="t-lead measure mb-6">A body that actually sets the standards in this industry has
      authorised this centre to train against them. The certificate is here &mdash; read it, and
      check the numbers on it.</p>
    <div class="creds__grid{wide}">{cards}</div>
  </div>
</section>
"""


def page_home(mode, depth=0):
    from build_data import STORIES
    from build_render import PHOTO_FOR_PATH, FIG_FOR_PATH

    _depts = [
        ("bim",    "BIM &amp; Digital Construction", "Building information modelling for architecture, structure and MEP."),
        ("mech",   "Mechanical &amp; Product Design", "CAD, 3D modelling, product design and manufacturing drawings."),
        ("struct", "Structural Engineering",          "STAAD.Pro, ETABS and RCC steel structure design and analysis."),
        ("pm",     "Project Planning &amp; Management","Primavera P6, MS Project and industry-standard PM practice."),
        ("ai",     "AI &amp; Emerging Tech",           "Automation, generative design and AI-assisted engineering workflows."),
    ]
    _work = [("proj-bim-coordination","BIM coordination"),
             ("proj-highway-corridor","Highway corridor"),
             ("proj-mechanical-assembly","Mechanical assembly"),
             ("proj-architectural-viz","Architectural visualisation"),
             ("proj-rcc-structure","RCC structure"),
             ("proj-construction-programme","Construction programme")]
    work_items = "".join(
        f'<a class="workitem" {L("student-work", mode, depth)}>{photo(sl, depth, "260px")}'
        f'<figcaption>{cap}</figcaption></a>' for sl, cap in _work)

    try:
        from build_data import PARTNERS
    except ImportError:
        PARTNERS = []
    if PARTNERS:
        _up = "../" * depth

        def _logomark(pn, pf, pw, ph, dup=False):
            # The track is duplicated so the scroll can loop seamlessly; the
            # second copy is decorative and hidden from assistive tech.
            _ah = ' aria-hidden="true"' if dup else ''
            return (f'<div class="logomark"{_ah}>'
                    f'<img src="{_up}assets/img/logos/{pf}" '
                    f'alt="{"" if dup else pn.replace("&", "&amp;")}" '
                    f'width="{pw}" height="{ph}" loading="lazy" decoding="async"></div>')

        _run = "".join(_logomark(*p) for p in PARTNERS)
        _run += "".join(_logomark(*p, dup=True) for p in PARTNERS)
        partner_band = ('<div class="logoband__marquee">'
                        f'<div class="logoband__track">{_run}</div></div>')
    else:
        partner_band = (
            '<div class="note tc" style="max-width:min(70ch,100%);margin-inline:auto">'
            'We name employers only where we have their written permission to do so. '
            'Ask a career advisor which firms have hired from this centre recently &mdash; '
            'we will tell you, and we will not decorate the answer with logos we have no right to use.'
            '</div>')

    _aud = [
        ("student",      "cap",       "College student",       "I want skills that go beyond my degree.",       "See student paths",  "career-paths"),
        ("fresher",      "rocket",    "Fresher",               "I have the degree. I need to become employable.", "Find my path",      "finder"),
        ("professional", "briefcase", "Working professional",  "I want to upskill, or move into a better role.", "Weekend options",   "programs"),
        ("corporate",    "building",  "Employer or corporate", "I need to train my team, or hire trained people.", "Corporate training","corporate"),
    ]
    aud_cards = ""
    for i, (art, ic, title, desc, cta, route) in enumerate(_aud):
        # A card uses a photograph where one has been supplied for it, and falls
        # back to the line drawing otherwise. Both fill the same 260:150 box.
        art_html = (photo(f"aud-{art}", depth, "(max-width: 1100px) 45vw, 240px",
                          cls="cardart cardart--photo")
                    or card_art(art))
        aud_cards += (
            f'<a class="audcard rv" data-delay="{i*40}" {L(route, mode, depth)}>'
            f'<div class="audcard__top">{icon(ic)}</div>'
            f'<div class="audcard__art">{art_html}</div>'
            f'<h3 class="audcard__t">{title}</h3>'
            f'<p class="audcard__d">{desc}</p>'
            f'<span class="audcard__cta">{cta}'
            f'<svg viewBox="0 0 20 12" fill="none" aria-hidden="true">'
            f'<path d="M1 6h17M13 1l5 5-5 5" stroke="currentColor" stroke-width="1.4" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg></span>'
            f'</a>')

    dept_cards = ""
    for i, (k, nm, blurb) in enumerate(_depts):
        slot = PHOTO_FOR_PATH.get(k)
        media = photo_card(slot, depth, "") if slot else figure(FIG_FOR_PATH[k])
        dept_cards += (
            f'<a class="card deptcard rv" data-delay="{i*40}" {L("path:" + k, mode, depth)}>'
            f'{media}<div class="card__body"><h3 class="t-h3">{nm}</h3>'
            f'<p class="t-small t-muted">{blurb}</p></div></a>')
    if STORIES:
        home_story_block = '<div class="grid g-3">' + "".join(
            f'<div class="story rv"><h3 class="t-h3 mb-2">{s["name"]}</h3><dl>'
            f'<div class="story__row"><dt>Before</dt><dd>{s["before"]}</dd></div>'
            f'<div class="story__row"><dt>Track</dt><dd>{s["track"]}</dd></div>'
            f'<div class="story__row"><dt>Now</dt><dd>{s["role"]}</dd></div>'
            f'</dl></div>' for s in STORIES[:3]) + '</div>'
    else:
        home_story_block = (
            '<div class="grid g-3">'
            '<div class="pillar">'
            '<h3 class="t-h3 mb-2 mt-1">Build a portfolio</h3>'
            '<p class="t-small t-muted">You finish with real project work, presented properly. '
            'For technical roles the portfolio does more work than the CV.</p></div>'
            '<div class="pillar">'
            '<h3 class="t-h3 mb-2 mt-1">Prepare for the room</h3>'
            '<p class="t-small t-muted">CV and profile work, then mock interviews with real '
            'technical questioning and honest feedback.</p></div>'
            '<div class="pillar">'
            '<h3 class="t-h3 mb-2 mt-1">Get introduced</h3>'
            '<p class="t-small t-muted">Introductions through our Industry Recruitment Panel to '
            'employers who are actively hiring.</p></div>'
            '</div>')
    return f"""
<main id="main">

<section class="hero">
  <div class="hero__photo" data-hero-slides>{hero_picture(depth)}</div>
  <div class="hero__scrim"></div>
  <div class="wrap hero__inner">
    <span class="crosshair" style="top:24px;right:40px"></span>
    <div class="hero__body">
      <p class="label hero__kicker" style="--d:80ms">CADD Centre Gurugram &middot; Sector 14</p>
      <h1 class="t-hero">
        <span class="hero__mask"><span style="--d:180ms">Don't just learn</span></span>
        <span class="hero__mask"><span style="--d:300ms">the software.</span></span>
        <span class="hero__mask"><span style="--d:420ms"><em>Build the career.</em></span></span>
      </h1>
      <p class="hero__sub" style="--d:620ms">CAD &middot; BIM &middot; PRODUCT DESIGN &middot; STRUCTURAL &middot; PROJECT MANAGEMENT &middot; AI</p>
      <p class="hero__lead" style="--d:740ms">Industry-focused engineering training in Sector 14, Gurugram. Real labs. Real projects. Real placement support.</p>
      <div class="hero__actions" style="--d:860ms">
        <a class="btn btn--primary" {L("career-paths", mode, depth)}>Explore career paths</a>
        <a class="btn btn--secondary" {L("contact", mode, depth)}>Book career counselling</a>
      </div>
      <div class="trustpts">
        <div class="trustpt">{icon("badge")}<span>Placement<br>support</span></div>
        <div class="trustpt">{icon("hands")}<span>Hands-on<br>projects</span></div>
        <div class="trustpt">{icon("mentor")}<span>Practitioner<br>trainers</span></div>
        <div class="trustpt">{icon("shield")}<span>Certified<br>programmes</span></div>
      </div>
    </div>
  </div>
</section>

<!-- Trust strip: elevated dark card overlapping the hero -->
<div class="statbar-wrap">
  <div class="wrap">
    <div class="statbar rv">
      <div class="statbar__cell">
        <div class="statbar__top">{icon("star")}<span class="statbar__n"><span data-count="4.9">4.9</span></span></div>
        <p class="statbar__l">Google rating<br><span data-count="207">207</span> reviews</p>
      </div>
      <div class="statbar__cell">
        <div class="statbar__top">{icon("calendar")}<span class="statbar__n"><span data-count="1988">1988</span></span></div>
        <p class="statbar__l">CADD Centre<br>founded</p>
      </div>
      <div class="statbar__cell">
        <div class="statbar__top">{icon("pin")}<span class="statbar__n">Sector 14</span></div>
        <p class="statbar__l">Authorised<br>training centre</p>
      </div>
      <div class="statbar__cell">
        <div class="statbar__top">{icon("clock")}<span class="statbar__n">7 days</span></div>
        <p class="statbar__l">Open 9:30 am &ndash; 7:00 pm</p>
      </div>
    </div>
  </div>
</div>

{accreditation_band(mode, depth)}

{testimonial_band(mode, depth)}

<!-- Audience selector -->
<section class="section audience">
  <div class="audience__bg" aria-hidden="true">{photo("audience-bg", depth, "100vw")}</div>
  <div class="audience__veil" aria-hidden="true"></div>
  <div class="wrap audience__inner">
    <p class="label label--accent audience__eyebrow">Start here</p>
    <h2 class="t-display audience__h">Where are you<br>right now<em>?</em></h2>
    <span class="audience__rule" aria-hidden="true"></span>
    <p class="t-lead audience__sub">Pick the one that fits. We will show you the<br class="dtop">path that makes sense from there.</p>

    <div class="audgrid">
      {aud_cards}
    </div>
  </div>
</section>

<!-- Finder promo -->
<section class="section section--inverse">
  <div class="wrap grid g-2" style="align-items:center">
    <div>
      <p class="label label--accent mb-3">60 seconds &middot; no sign-up</p>
      <h2 class="t-display mb-3">Not sure which programme is right for you?</h2>
      <p>Most people arrive knowing the job they want, not the software they need. Answer four questions and we will map a career path, the skills sequence to get there, and the programme that starts you off.</p>
      <p><strong style="color:#fff">You see the result before we ask for your number.</strong></p>
      <a class="btn btn--primary mt-3" {L("finder", mode, depth)}>Find my career path</a>
    </div>
    <div>
      <div class="roadmap">
        <span class="roadmap__step" style="background:#1F1F1F;border-color:#333;color:#fff">AutoCAD</span>
        <span class="roadmap__arrow">&rarr;</span>
        <span class="roadmap__step" style="background:#1F1F1F;border-color:#333;color:#fff">Revit</span>
        <span class="roadmap__arrow">&rarr;</span>
        <span class="roadmap__step" style="background:#1F1F1F;border-color:#333;color:#fff">Navisworks</span>
        <span class="roadmap__arrow">&rarr;</span>
        <span class="roadmap__step" style="background:#D42027;border-color:#D42027;color:#fff">BIM Coordinator</span>
      </div>
      <p class="label mt-3">Example output &mdash; civil background, first job</p>
    </div>
  </div>
</section>

<!-- Departments -->
<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Programmes</span></div>
    <div class="flex jcb aic wrapf gap-3 mb-2">
      <h2 class="t-display">Industry-ready programmes.</h2>
      <a class="alink" {L("programs", mode, depth)}>View all {len(ALL_PROGRAMS)} courses
        <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></a>
    </div>
    <p class="t-lead measure mb-6">{len([d for d in DEPARTMENTS if d["courses"]])} departments, each opening into a module-by-module curriculum. Start from where you want to end up.</p>
    <div class="deptrow">
      {dept_cards}
    </div>
  </div>
</section>

<!-- Student work: dark strip -->
<section class="section">
  <div class="wrap">
    <div class="workstrip rv">
      <div class="workstrip__head">
        <div>
          <div class="marker"><span class="label label--accent">The output</span></div>
          <h2 class="t-display" style="color:#fff">Real projects. Real skills.</h2>
        </div>
        <a class="alink" {L("student-work", mode, depth)} style="color:#fff">View student work
          <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></a>
      </div>
      <div class="workscroll">
        {work_items}
      </div>
      <p class="t-small mt-3" style="color:#9A9A9A">Representative projects &mdash; illustrative of the deliverables our programmes cover.</p>
    </div>
  </div>
</section>

<!-- The narrative spine — genuinely a sequence, so numbering carries meaning -->
<section class="section section--inverse">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">The method</span></div>
    <h2 class="t-display mb-6">Four stages. One outcome.</h2>
    <div class="spine">
      <div class="spine__item rv"><span class="spine__n">01 / LEARN</span>
        <div><h3 class="t-h3 mb-2" style="color:#fff">Structured, not scattered</h3>
        <p>Small batches, certified trainers, and a curriculum sequenced the way the work is actually done &mdash; not the way a menu is organised.</p></div></div>
      <div class="spine__item rv" data-delay="60"><span class="spine__n">02 / BUILD</span>
        <div><h3 class="t-h3 mb-2" style="color:#fff">Projects, not exercises</h3>
        <p>You build real deliverables: a coordinated model, a corridor design, a manufacturable assembly, a printed prototype. They become your portfolio.</p></div></div>
      <div class="spine__item rv" data-delay="120"><span class="spine__n">03 / EXPERIENCE</span>
        <div><h3 class="t-h3 mb-2" style="color:#fff">Beyond the classroom</h3>
        <p>Industry visits, technical competitions, workshops, guest sessions from practising engineers, and a lab you can use.</p></div></div>
      <div class="spine__item rv" data-delay="180"><span class="spine__n">04 / CAREER READY</span>
        <div><h3 class="t-h3 mb-2" style="color:#fff">Prepared, not just certified</h3>
        <p>Portfolio review, CV and profile work, mock interviews, certification preparation, and introductions through our Industry Recruitment Panel.</p></div></div>
    </div>
  </div>
</section>

<!-- Outcomes -->
<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Outcomes</span></div>
    <h2 class="t-display mb-2">From classroom to career.</h2>
    <p class="t-lead measure mb-6">What we actually do to move you from trained to employed.</p>
    {home_story_block}
    <p class="note mt-4">Individual outcomes. Results vary by background, effort and market conditions. We publish learner outcomes only with written permission.</p>
  </div>
</section>

<!-- 3D printing -->
<section class="section section--warm section--rule">
  <div class="wrap grid g-2" style="align-items:center">
    <div>
      <div class="marker"><span class="label label--accent">Make it real</span></div>
      <h2 class="t-display mb-3">Design it. Model it.<br>Make it real.</h2>
      <p class="t-lead">There is a specific moment in a designer's education when something changes &mdash; the first time a part they drew on a screen comes off a printer and they can hold it. Suddenly wall thickness is not a parameter, it is a thing that snaps.</p>
      <div class="roadmap mt-4">
        <span class="roadmap__step">CAD model</span><span class="roadmap__arrow">&rarr;</span>
        <span class="roadmap__step">Design review</span><span class="roadmap__arrow">&rarr;</span>
        <span class="roadmap__step">3D print</span><span class="roadmap__arrow">&rarr;</span>
        <span class="roadmap__step">Physical part</span>
      </div>
      <a class="btn btn--secondary mt-4" {L("life", mode, depth)}>See the lab</a>
    </div>
    <figure class="figure">{photo("printing", depth, "(max-width: 767px) 100vw, 50vw")}<figcaption>Representative of the CAD-to-prototype workflow</figcaption></figure>
  </div>
</section>

<!-- Why CADD -->
<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Why CADD</span></div>
    <div class="whygrid">
      <div>
        <h2 class="t-display mb-2">More than a classroom.</h2>
        <p class="t-lead measure mb-6">This is the part an online course cannot give you &mdash; and the reason people who could have learned this from a video still come here.</p>
        <div class="featgrid">
          <div class="feat rv">{icon("book","ico--lg")}<strong>Industry-relevant curriculum</strong><span class="t-small t-muted">Sequenced the way the work is done, not the way a menu is organised.</span></div>
          <div class="feat rv" data-delay="30">{icon("layers","ico--lg")}<strong>Live projects &amp; hands-on labs</strong><span class="t-small t-muted">You build real deliverables, not exercises.</span></div>
          <div class="feat rv" data-delay="60">{icon("mentor","ico--lg")}<strong>Mentorship from practitioners</strong><span class="t-small t-muted">Every trainer worked in the field before they taught it.</span></div>
          <div class="feat rv" data-delay="90">{icon("target","ico--lg")}<strong>Placement support</strong><span class="t-small t-muted">Portfolio, CV, mock interviews and employer introductions.</span></div>
          <div class="feat rv" data-delay="120">{icon("mic","ico--lg")}<strong>Soft skills &amp; interview prep</strong><span class="t-small t-muted">Technical questioning with honest feedback.</span></div>
          <div class="feat rv" data-delay="150">{icon("infinity","ico--lg")}<strong>A community you keep</strong><span class="t-small t-muted">Events, competitions and alumni who stay in touch.</span></div>
        </div>
        <a class="btn btn--secondary mt-6" {L("life", mode, depth)}>See what happens here</a>
      </div>

      <aside class="expbox rv">
        <div class="marker"><span class="label label--accent">Experience CADD</span></div>
        <h3 class="t-h2 mb-3">Experience CADD before you decide.</h3>
        <ul>
          <li>{icon("check")}<span>Meet the trainers</span></li>
          <li>{icon("check")}<span>See the labs and tools</span></li>
          <li>{icon("check")}<span>Sit in on a live class</span></li>
          <li>{icon("check")}<span>Look at real student projects</span></li>
          <li>{icon("check")}<span>Get honest career guidance</span></li>
        </ul>
        <a class="btn btn--primary btn--wide" {L("contact", mode, depth)}>Book a centre visit</a>
        <p class="t-small t-muted mt-2">An hour, no charge, no obligation.</p>
      </aside>
    </div>
  </div>
</section>

<!-- Industry -->
<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Industry</span></div>
    <h2 class="t-display mb-6">Built with industry. For industry.</h2>
    <div class="grid g-4">
      <div class="pillar rv"><h3 class="t-h3 mb-2">Corporate training</h3><p class="t-small t-muted">Upskilling engineering and design teams, on your site or ours.</p></div>
      <div class="pillar rv" data-delay="60"><h3 class="t-h3 mb-2">Recruitment panel</h3><p class="t-small t-muted">Connecting employers with trained, portfolio-ready talent.</p></div>
      <div class="pillar rv" data-delay="120"><h3 class="t-h3 mb-2">Collaborations</h3><p class="t-small t-muted">Curriculum input, workshops and technical exposure from practising firms.</p></div>
      <div class="pillar rv" data-delay="180"><h3 class="t-h3 mb-2">Industrial visits</h3><p class="t-small t-muted">Learning where the work actually happens.</p></div>
    </div>
    <a class="btn btn--secondary mt-6" {L("corporate", mode, depth)}>Explore Industry Connect</a>
  </div>
</section>

<!-- Reviews -->
<section class="section">
  <div class="wrap">
    {reviews_section()}
  </div>
</section>

<!-- News -->
<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">News</span></div>
    <div class="flex jcb aic wrapf gap-3 mb-6">
      <h2 class="t-display">Latest from the centre.</h2>
      <a class="alink" {L("news", mode, depth)}>All news
        <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></a>
    </div>
    <div class="grid g-3">
      <a class="card rv" {L("article:autocad-basic-drawing-guide", mode, depth)}>{path_media("autocad-basics", depth, "news")}
        <div class="card__body"><p class="label label--accent">AutoCAD</p>
        <h3 class="t-h3">AutoCAD Basic Drawing: A Complete Beginner's Guide</h3>
        <p class="t-small t-muted">Setup, the commands that matter, and the habits that make later work easier.</p></div></a>
      <a class="card rv" data-delay="60" {L("article:autocad-2d-mechanical-drawing", mode, depth)}>{path_media("autocad-2d", depth, "news")}
        <div class="card__body"><p class="label label--accent">AutoCAD</p>
        <h3 class="t-h3">Master AutoCAD 2D Mechanical Drawing</h3>
        <p class="t-small t-muted">Projection, sections, tolerancing and the conventions a shop floor expects.</p></div></a>
      <a class="card rv" data-delay="120" {L("first-job-pakka", mode, depth)}>{path_media("struct", depth, "path")}
        <div class="card__body"><p class="label label--accent">Placement</p>
        <h3 class="t-h3">First Job Pakka, in 80 hours</h3>
        <p class="t-small t-muted">Core competence, hands-on practice, and the programming component most CAD training leaves out.</p></div></a>
    </div>
  </div>
</section>

<!-- Employer band -->
<section class="section section--tight logoband">
  <div class="wrap">
    <p class="label tc mb-4">Trusted by industry &middot; Chosen by learners</p>
    {partner_band}
  </div>
</section>

<!-- Final CTA -->
<section class="section section--inverse">
  <div class="wrap">
    <span class="crosshair" style="top:0;left:var(--margin)"></span>
    <div class="grid g-2" style="align-items:center">
      <div>
        <h2 class="t-display mb-3">Experience CADD<br>before you decide.</h2>
        <p class="t-lead" style="color:#C4C4C4">Come in for an hour. There is no charge, no obligation, and no sales pitch you cannot walk out of.</p>
        <div class="flex wrapf gap-2 mt-4">
          <a class="btn btn--primary" {L("contact", mode, depth)}>Book my centre visit</a>
          <a class="btn btn--secondary" href="tel:{PHONE}">Call {PHONE_D}</a>
        </div>
      </div>
      <ul class="stack" style="list-style:none;padding:0;margin:0">
        {''.join(f'<li class="dim" style="color:#C4C4C4">{t}</li>' for t in ["Meet the trainer who would actually teach you","See the labs and the equipment","Sit in on a live class","Look at real student projects","Try the software yourself","Get honest career guidance &mdash; including whether we are the right fit"])}
      </ul>
    </div>
  </div>
</section>

</main>
"""


# ============================================================================
# CAREER PATHS HUB
# ============================================================================
def page_career_paths(mode, depth=0):
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / Career paths</p>
    <h1 class="t-display mb-3">Choose the career.<br>We will handle the software.</h1>
    <p class="t-lead measure">Nobody sets out wanting to learn Navisworks. They want to coordinate buildings without clashes. Nobody wants CATIA for its own sake &mdash; they want to design parts that get manufactured. So we have organised everything around where you want to end up, not around a software menu.</p>
    <a class="btn btn--primary mt-4" {L("finder", mode, depth)}>Not sure yet? Find my career path</a>
  </div>
</section>

<section class="section">
  <div class="wrap"><div class="grid g-3">{_path_grid(mode, depth)}</div></div>
</section>
</main>
"""


# ============================================================================
# BIM CAREER PATH (full detail)
# ============================================================================
def page_path_bim(mode, depth=0):
    return f"""
<main id="main">
<section class="section section--inverse">
  <div class="wrap">
    <p class="label mb-3"><a {L("home", mode, depth)} style="text-decoration:none">Home</a> / <a {L("career-paths", mode, depth)} style="text-decoration:none">Career paths</a> / BIM</p>
    <h1 class="t-display mb-3">Build a career in BIM.</h1>
    <p class="t-lead" style="color:#C4C4C4;max-width:62ch">BIM is not a piece of software. It is how large projects are now run &mdash; a single coordinated model that architects, structural engineers and MEP teams all work against, so clashes are found on a screen rather than on site.</p>
    <p class="label mt-4">BIM Modeller &middot; Revit Technician &middot; BIM Engineer &middot; BIM Coordinator &middot; Documentation Lead</p>
    <div class="flex wrapf gap-2 mt-4">
      <a class="btn btn--primary" {L("contact", mode, depth)}>Talk to a career advisor</a>
      <a class="btn btn--secondary" {L("program-revit", mode, depth)}>See the starting programme</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap grid g-2">
    <div>
      <div class="marker"><span class="label label--accent">The work</span></div>
      <h2 class="t-h2 mb-3">What this work actually involves</h2>
      <p>A BIM modeller builds and maintains the model &mdash; walls, structure, systems, families, levels and grids &mdash; to a standard the whole project team can rely on. A coordinator sits a level above: running clash detection between disciplines, chairing coordination reviews, managing model federation, and keeping the information structure consistent as the project changes.</p>
      <p>It is precise, collaborative work. You will spend as much time on naming conventions, worksets and information standards as on geometry, because the value of BIM is the data, not the picture. If you like resolving problems before they become expensive, and you are comfortable being the person who spots the conflict everyone else missed, this suits you.</p>
    </div>
    <div class="card" style="pointer-events:none">{figure("bim")}</div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Skills roadmap</span></div>
    <h2 class="t-h2 mb-4">The sequence that gets you there</h2>
    <div class="roadmap">
      <span class="roadmap__step">AutoCAD fundamentals</span><span class="roadmap__arrow">&rarr;</span>
      <span class="roadmap__step">Revit Architecture</span><span class="roadmap__arrow">&rarr;</span>
      <span class="roadmap__step">Revit Structure / MEP</span><span class="roadmap__arrow">&rarr;</span>
      <span class="roadmap__step">Navisworks clash detection</span><span class="roadmap__arrow">&rarr;</span>
      <span class="roadmap__step">Model federation</span><span class="roadmap__arrow">&rarr;</span>
      <span class="roadmap__step">ISO 19650 concepts</span><span class="roadmap__arrow">&rarr;</span>
      <span class="roadmap__step">Live coordination project</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Roles</span></div>
    <h2 class="t-h2 mb-4">Roles this leads to</h2>
    <table class="tbl">
      <thead><tr><th>Role</th><th>What you would do</th></tr></thead>
      <tbody>
        <tr><td data-l="Role"><strong>BIM Modeller</strong></td><td data-l="Work">Build and maintain discipline models to project standards</td></tr>
        <tr><td data-l="Role"><strong>Revit Technician</strong></td><td data-l="Work">Produce construction documentation from the model</td></tr>
        <tr><td data-l="Role"><strong>BIM Engineer</strong></td><td data-l="Work">Own a discipline model and its data integrity</td></tr>
        <tr><td data-l="Role"><strong>BIM Coordinator</strong></td><td data-l="Work">Run clash detection and cross-discipline coordination</td></tr>
        <tr><td data-l="Role"><strong>Documentation Lead</strong></td><td data-l="Work">Manage drawing production and issue control</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap grid g-2">
    <div>
      <h2 class="t-h2 mb-3">A good fit if you are</h2>
      <ul class="stack t-small" style="padding-left:1.1rem;color:var(--c-ink-2)">
        <li>A civil engineering or architecture graduate</li>
        <li>A working draughtsperson wanting to move up</li>
        <li>An interior or site professional aiming at larger projects</li>
        <li>Targeting Gulf or European roles where BIM is mandated</li>
      </ul>
    </div>
    <div>
      <h2 class="t-h2 mb-3">Probably not the right start if</h2>
      <ul class="stack t-small" style="padding-left:1.1rem;color:var(--c-ink-2)">
        <li>You want purely creative visualisation work &mdash; look at Architecture &amp; Visualisation instead</li>
        <li>You want to stay entirely in analysis and calculation &mdash; Structural Engineering is the better path</li>
      </ul>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Questions</span></div>
    <h2 class="t-h2 mb-4">Frequently asked</h2>
    <div class="acc2">
      {_faq([
        ("Do I need to know AutoCAD before starting BIM?", "It helps, but it is not required. Our foundation programmes start from the basics. If you already draft in AutoCAD, you will move faster."),
        ("Is BIM only for architects?", "No. Civil, structural and MEP engineers all work in BIM, and coordination roles specifically need people who understand more than one discipline."),
        ("Can I do this alongside a job?", "Yes. We run weekend and evening batches. Current schedule confirmed at counselling."),
        ("Will I get a certificate employers recognise?", "You receive a CADD Centre certification. The exact additional certifications this centre is authorised to issue are being confirmed and will be stated precisely rather than implied."),
        ("How long before I am employable?", "That depends on your starting point and how much you build. People who complete the programme and finish a full portfolio project are ready to interview for modeller roles. We will give you a straight answer about your own situation in a counselling session."),
      ], "bim")}
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


def _faq(items, prefix):
    out = ""
    for i, (q, a) in enumerate(items):
        out += f"""<button class="acc2__t" data-acc-trigger aria-expanded="false" aria-controls="{prefix}-faq-{i}">
<span>{q}</span><span class="plus" aria-hidden="true"></span></button>
<div class="acc2__p" id="{prefix}-faq-{i}" data-open="false"><p class="t-small" style="color:var(--c-ink-2);margin:0">{a}</p></div>"""
    return out
