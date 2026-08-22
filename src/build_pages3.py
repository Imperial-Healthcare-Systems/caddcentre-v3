# -*- coding: utf-8 -*-
"""Pages that were missing from the first build. Every one traces to an
inventory row flagged NO."""

from build_parts import figure, photo, photo_card, icon
from build_pages import _faq
from build_render import crumbs
from build_shell import L, PHONE, PHONE_D, EMAIL, ADDRESS
from build_data import STORIES


# ===========================================================================
# FIRST JOB PAKKA — was missed entirely. Promoted into Careers.
# ===========================================================================
def page_first_job_pakka(mode, depth=0):
    return f"""
<main id="main">
<section class="section section--inverse">
  <div class="wrap">
    {crumbs(mode, depth, [("Careers", "careers"), ("First Job Pakka", None)])}
    <p class="label label--accent mb-3">A CADD Centre national initiative</p>
    <h1 class="t-display mb-3">First Job Pakka.<br>In 80 hours.</h1>
    <p class="t-lead" style="color:#C4C4C4;max-width:64ch">The first job is the hardest one to get. First Job Pakka is CADD Centre's training-and-placement initiative, built around a simple idea: eighty focused hours on the right skills, aimed squarely at making you employable rather than merely certified.</p>
    <div class="flex wrapf gap-2 mt-4">
      <button class="btn btn--primary" data-enquire type="button">Talk to us about First Job Pakka</button>
      <a class="btn btn--secondary" {L("finder", mode, depth)}>Find my career path</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">What makes it different</span></div>
    <h2 class="t-display mb-2">Three things, done deliberately.</h2>
    <p class="t-lead measure mb-6">This is not a repackaged software course. The structure is built backwards from what employers actually screen for.</p>
    <div class="grid g-3">
      <div class="pillar rv">
        <h3 class="t-h3 mb-2 mt-1">Core competence</h3>
        <p class="t-small t-muted">A holistic approach covering engineering design and development alongside project management. Expert training on the CAD and CAE tools employers use, taught with the engineering concepts behind them &mdash; so you learn how the tools are used in real engineering work, not just which buttons produce which result.</p>
      </div>
      <div class="pillar rv" data-delay="60">
        <h3 class="t-h3 mb-2 mt-1">Hands-on</h3>
        <p class="t-small t-muted">Practical application in the lab, with the theory taught alongside rather than in front. You get time and space to think through each action, and a trainer who can give real-time feedback while you are still making the mistake &mdash; which is when feedback is worth something.</p>
      </div>
      <div class="pillar rv" data-delay="120">
        <h3 class="t-h3 mb-2 mt-1">Programming skills for engineers</h3>
        <p class="t-small t-muted">Whatever branch of engineering you are in, computational skill is now a baseline expectation. AI, IoT and robotics are creating engineering jobs that assume some knowledge of programming and algorithms. This is the part most CAD training leaves out entirely.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap grid g-2" style="align-items:center">
    <div>
      <div class="marker"><span class="label label--accent">Why this matters here</span></div>
      <h2 class="t-h2 mb-3">The programming component is the differentiator</h2>
      <p>Every CAD institute in Gurugram teaches the same software. Very few of them teach engineers to think computationally alongside it.</p>
      <p>That combination &mdash; a design tool plus the ability to automate and reason about it &mdash; is what separates an engineer who can operate software from one who can improve how their team works. It is also the capability that ages best as tooling changes.</p>
      <p class="t-small t-muted">First Job Pakka also includes exposure to job fairs and pre-placement assessment as part of the national programme.</p>
    </div>
    <div class="card" style="pointer-events:none">{figure("ai")}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="note mb-6">
      <strong>Being precise about what this is.</strong> First Job Pakka is a training-and-placement initiative, not a job guarantee &mdash; and we will not describe it as one. Ask an advisor which programmes qualify, what the eligibility is, and exactly what placement support is included. You will get a straight answer.
    </div>
    <div class="tc">
      <h2 class="t-display mb-3">Ask us what it means for you.</h2>
      <p class="t-lead measure" style="margin-inline:auto">Bring your background and your timeline. We will tell you honestly whether this route fits.</p>
      <div class="flex wrapf gap-2 mt-4" style="justify-content:center">
        <button class="btn btn--primary" data-enquire type="button">Enquire about First Job Pakka</button>
        <a class="btn btn--secondary" href="tel:{PHONE}">Call {PHONE_D}</a>
      </div>
    </div>
  </div>
</section>
</main>
"""


# ===========================================================================
# CAREERS HUB
# ===========================================================================
def page_careers(mode, depth=0):
    if STORIES:
        story_block = '<div class="grid g-3">' + "".join(
            f'<div class="story rv"><h3 class="t-h3 mb-2">{s["name"]}</h3><dl>'
            f'<div class="story__row"><dt>Before</dt><dd>{s["before"]}</dd></div>'
            f'<div class="story__row"><dt>Track</dt><dd>{s["track"]}</dd></div>'
            f'<div class="story__row"><dt>Skills</dt><dd>{s["skills"]}</dd></div>'
            f'<div class="story__row"><dt>Now</dt><dd>{s["role"]}</dd></div>'
            f'</dl></div>' for s in STORIES) + '</div>'
    else:
        story_block = (
            '<div class="note" style="max-width:66ch"><strong>Ask us for references.</strong> '
            'We publish outcomes only with the person\'s written permission, so this page stays '
            'thin by choice. In a counselling session we will talk you through where recent '
            'learners from your background actually went, and put you in touch where they agree '
            'to it.</div>')
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    {crumbs(mode, depth, [("Careers", None)])}
    <h1 class="t-display mb-3">What happens after<br>the certificate.</h1>
    <p class="t-lead measure">A certificate on its own does not get anybody hired. A portfolio, a straight answer in a technical interview, and somebody willing to make an introduction &mdash; that is what moves people from trained to employed. This is what we do about it.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Placement support</span></div>
    <h2 class="t-display mb-2">Described honestly.</h2>
    <p class="t-lead measure mb-6">A lot of training providers advertise 100% placement. We do not, because it is not a claim anyone can honestly stand behind.</p>
    <div class="grid g-2">
      <div>
        <h3 class="t-h3 mb-3">What we do</h3>
        <div class="grid" style="gap:var(--s-2)">
          <div class="dim"><strong>Portfolio development.</strong><br><span class="t-small t-muted">You finish with real project work, presented properly. For technical roles, the portfolio does more work than the CV.</span></div>
          <div class="dim"><strong>CV and profile.</strong><br><span class="t-small t-muted">We rewrite your CV against the roles you are targeting and get your LinkedIn profile into a state where recruiters find it.</span></div>
          <div class="dim"><strong>Mock interviews.</strong><br><span class="t-small t-muted">Technical questioning by a trainer who has worked in the field, followed by honest feedback about what you got wrong.</span></div>
          <div class="dim"><strong>Industry Recruitment Panel.</strong><br><span class="t-small t-muted">Introductions to employers in our network who are actively hiring.</span></div>
          <div class="dim"><strong>Internship guidance.</strong><br><span class="t-small t-muted">Where a full role is not immediately available, we help you find project-based work that builds experience.</span></div>
        </div>
      </div>
      <div>
        <h3 class="t-h3 mb-3">What we cannot do</h3>
        <p>We cannot guarantee you a job. Hiring depends on your background, how much effort you put into your portfolio, how you interview, and the state of the market that quarter.</p>
        <p>What we can guarantee is that you will not walk into an interview unprepared.</p>
        <div class="note mt-4">
          <strong>First Job Pakka.</strong> CADD Centre runs a national training-and-placement initiative built around eighty focused hours, including a programming component most CAD training leaves out.
          <a class="alink mt-2" {L("first-job-pakka", mode, depth)}>Read about First Job Pakka
            <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M1 7h12M8 2l5 5-5 5" stroke="currentColor" stroke-width="1.6"/></svg></a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Outcomes</span></div>
    <h2 class="t-display mb-2">From classroom to career.</h2>
    <p class="t-lead measure mb-6">Real names, real programmes, real roles. Every person here has given us permission to tell their story.</p>
    {story_block}
    <p class="note mt-4">Individual outcomes. Results vary by background, effort and market conditions.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Employers</span></div>
    <h2 class="t-h2 mb-3">Industry Recruitment Panel</h2>
    <p class="measure">Our Industry Recruitment Panel connects firms that need trained engineering and design talent with people who have just finished building a portfolio. For employers, it is a shortlist of candidates who have been technically assessed. For learners, it is a route to an interview that does not start with a job portal.</p>

    <a class="btn btn--secondary mt-4" {L("corporate", mode, depth)}>Hire from us</a>
  </div>
</section>
</main>
"""


# ===========================================================================
# LIFE @ CADD — includes CADD Quest 2026 and the testimonial video
# ===========================================================================
def _embed(url):
    """Turn a pasted URL into a playable embed. Supports YouTube (watch, short
    and shorts forms), Vimeo, and any direct video file on a CDN."""
    import re as _re
    u = (url or "").strip()
    m = _re.search(r'(?:youtube\.com/(?:watch\?v=|embed/|shorts/)|youtu\.be/)([\w-]{6,})', u)
    if m:
        return ('<iframe src="https://www.youtube-nocookie.com/embed/' + m.group(1) + '" '
                'title="" loading="lazy" allowfullscreen '
                'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe>')
    m = _re.search(r'vimeo\.com/(?:video/)?(\d+)', u)
    if m:
        return ('<iframe src="https://player.vimeo.com/video/' + m.group(1) + '" '
                'title="" loading="lazy" allowfullscreen></iframe>')
    if _re.search(r'\.(mp4|webm|mov|m3u8)(\?|$)', u, _re.I):
        return ('<video controls preload="none" playsinline '
                'style="position:absolute;inset:0;width:100%;height:100%">'
                '<source src="' + u + '"></video>')
    return ""


def _fetch_videos():
    """Videos managed in /admin. Empty on any failure — a build never breaks
    because the backend is unreachable."""
    import os, json, urllib.request
    api = os.environ.get("VIDEOS_API")
    if not api:
        return []
    try:
        with urllib.request.urlopen(api, timeout=8) as r:
            rows = json.loads(r.read().decode())["rows"]
        print(f"  + {len(rows)} video(s) fetched from the admin")
        return rows
    except Exception as e:
        print(f"  ! videos API unreachable ({e}) — using the built-in video only")
        return []


def page_life(mode, depth=0):
    vids = _fetch_videos()
    if vids:
        blocks = ""
        for v in vids:
            emb = _embed(v.get("url", ""))
            if not emb:
                continue
            cap = v.get("caption") or ""
            blocks += (f'<figure class="vidbox"><div class="vidbox__frame">{emb}</div>'
                       f'<figcaption><strong>{v.get("title","")}</strong>'
                       + (f' &mdash; {cap}' if cap else '') + '</figcaption></figure>')
        video_section = blocks or ""
    else:
        video_section = (
            '<figure class="vidbox"><div class="vidbox__frame">'
            '<iframe src="https://www.youtube-nocookie.com/embed/NQdqWVcbkMg" '
            'title="CADD Centre Gurugram, Sector 14 — Autodesk Authorised Training Centre" loading="lazy" allowfullscreen '
            'allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture">'
            '</iframe></div><figcaption><strong>Inside CADD Centre Gurugram, Sector 14</strong></figcaption></figure>')
    # (image slot, title, icon, what actually happens)
    tiles = [
        ("sitevisit", "Site visit", "building",
         "See a live project and how the drawing becomes the building."),
        ("presentation", "Project presentation", "mic",
         "Stand up, present your work, and defend the decisions in it."),
        ("printing", "3D printing lab", "layers",
         "Take a model off the screen and hold the printed part."),
        ("classroom", "Live class", "cap",
         "Taught in the room, with a trainer who answers as you go."),
        ("trainer-context", "Guest session", "mentor",
         "A practitioner from the field, talking about the work as it is."),
        ("corporate", "Industry session", "briefcase",
         "What employers are hiring for, from the people doing the hiring."),
        ("facilities", "The lab", "target",
         "Licensed software on machines specified for the work."),
        ("bim", "BIM review", "check",
         "Models opened, clashes found, and the fixes agreed."),
        ("competition", "Technical competition", "star",
         "Timed technical challenges, judged on the work you produce."),
        ("career-workshop", "Career workshop", "rocket",
         "CV, portfolio and the questions you will actually be asked."),
        ("mock-interview", "Mock interview", "users",
         "Real technical questioning, and honest feedback afterwards."),
        ("job-fair", "Job fair", "hands",
         "Employers in the room, with your portfolio in your hand."),
    ]
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    {crumbs(mode, depth, [("Life @ CADD", None)])}
    <h1 class="t-display mb-3">More than a classroom.</h1>
    <p class="t-lead measure">This is the part that an online course cannot give you &mdash; and the reason people who could have learned this from a video still come here. A room full of people solving the same problem. A trainer who can look over your shoulder. Competitions, site visits, guest sessions, and a lab you can stay late in.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Events &amp; contests</span></div>
    <div class="grid g-2" style="align-items:center">
      <div>
        <p class="label label--accent mb-2">Now open</p>
        <h2 class="t-display mb-3">CADD Quest 2026</h2>
        <p class="t-lead">CADD Centre's national design competition, now in its 2026 edition. Learners across the network compete on real design challenges &mdash; one of the few chances to benchmark your work against people outside your own centre.</p>
        <p class="t-small t-muted">Registration details, categories and deadlines confirmed at the centre.</p>
        <div class="flex wrapf gap-2 mt-4">
          <button class="btn btn--primary" data-enquire type="button">Register interest</button>
          <a class="btn btn--secondary" {L("contact", mode, depth)}>Ask at the centre</a>
        </div>
      </div>
      <figure class="figure">{photo("presentation", depth)}<figcaption>Illustrative image</figcaption></figure>
    </div>
  </div>
</section>

<section class="section section--inverse">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">In their words</span></div>
    <h2 class="t-display mb-4">Hear from our learners.</h2>
    <div class="vidgrid">{video_section}</div>

  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">The calendar</span></div>
    <h2 class="t-h2 mb-2">Events we run and take part in</h2>
    <p class="t-lead measure mb-4">These are real fixtures, not a generic activities list.</p>
    <div class="grid g-3 mb-8">
      <div class="pillar"><p class="label label--accent">Competition</p><h3 class="t-h3 mb-2 mt-1">CADD Quest</h3><p class="t-small t-muted">The national design competition. 2025 and 2026 editions both ran.</p></div>
      <div class="pillar"><p class="label label--accent">Festival</p><h3 class="t-h3 mb-2 mt-1">BIM Festival</h3><p class="t-small t-muted">A network-wide BIM event &mdash; sessions, challenges and industry exposure.</p></div>
      <div class="pillar"><p class="label label--accent">Emerging tech</p><h3 class="t-h3 mb-2 mt-1">AI in Engineering sessions</h3><p class="t-small t-muted">Where AI-assisted design workflows are demonstrated and discussed.</p></div>
    </div>
    <p class="note mb-8">Dates, categories and entry terms are announced at the centre. Ask an advisor or follow us on social for the current calendar.</p>

    <div class="gallhead">
      <p class="label label--accent">The gallery</p>
      <h2 class="t-h2 mt-1">What happens here</h2>
      <span class="gallhead__rule" aria-hidden="true"></span>
      <p class="t-lead mt-3">Explore, learn, build and get in front of employers &mdash; all in one place.</p>
    </div>
    <div class="gallgrid">
      {''.join(
        f'<article class="gcard rv" data-delay="{(i%6)*40}">'
        f'<div class="gcard__img">{photo(sl, depth, "(max-width: 600px) 50vw, 17vw") if sl else ""}</div>'
        f'<span class="gcard__ico">{icon(ic)}</span>'
        f'<h3 class="gcard__t">{c}</h3>'
        f'<p class="gcard__d">{d}</p>'
        f'</article>' for i, (sl, c, ic, d) in enumerate(tiles))}
    </div>
  </div>
</section>

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

    </div>
    <figure class="figure">{photo("printing", depth)}<figcaption>Representative of the CAD-to-prototype workflow</figcaption></figure>
  </div>
</section>

<section class="section section--inverse">
  <div class="wrap tc">
    <h2 class="t-display mb-3">Come and see it.</h2>
    <p class="t-lead" style="color:#C4C4C4;margin-inline:auto;max-width:52ch">An hour, no charge, no obligation.</p>
    <a class="btn btn--primary mt-4" {L("contact", mode, depth)}>Book my centre visit</a>
  </div>
</section>
</main>
"""


# ===========================================================================
# INSIGHTS index + the two migrated articles
# ===========================================================================
_FALLBACK_ARTICLES = [
    ("autocad-basic-drawing-guide",
     "AutoCAD Basic Drawing: A Complete Beginner's Guide",
     "A practical starting guide to AutoCAD drafting — setup, the commands that matter, and the habits that make later work easier.",
     "AutoCAD", "autocad",
     [("Start with the setup, not the commands",
       "Most beginners open AutoCAD and start drawing lines. That works for about twenty minutes, and then the drawing becomes unmanageable. Units, limits, layers and a template are boring for ten minutes and save hours afterwards."),
      ("The commands that carry most of the work",
       "A small set of commands does most real drafting: LINE, CIRCLE, ARC, OFFSET, TRIM, EXTEND, FILLET, COPY, MOVE, MIRROR and ARRAY. Learn these to the point of not thinking about them before adding anything else."),
      ("Precision is not optional",
       "Drawing by eye is the single most common beginner habit and the hardest to unlearn. Object snaps, polar tracking and typed coordinates exist so that geometry is exact. A drawing that looks right and measures wrong is worse than no drawing."),
      ("Layers are how drawings stay readable",
       "Layers separate what a drawing is made of. Set them up early with sensible names, colours and linetypes. When somebody else opens your file — and they will — layers are what makes it navigable."),
      ("Annotation and output",
       "A drawing communicates or it fails. Dimension styles, text styles, layouts, viewports and plot scales are the part that turns geometry into something a workshop or a site can use.")],
     "If you are learning AutoCAD to get work rather than as a hobby, the drafting standard matters more than the software speed. Employers look at whether your drawing is readable, correctly layered and correctly annotated."),

    ("autocad-2d-mechanical-drawing",
     "Master AutoCAD 2D Mechanical Drawing",
     "How mechanical parts are actually drafted in 2D — projection, sections, tolerancing and the drawing conventions a shop floor expects.",
     "AutoCAD", "mechanical",
     [("Orthographic projection is the foundation",
       "Mechanical drawing is a language, and projection is its grammar. First-angle and third-angle projection describe the same part differently, and getting the convention wrong makes a drawing actively dangerous rather than merely unclear."),
      ("Sections and auxiliary views",
       "Internal features cannot be described with hidden lines alone once a part gets complex. Full sections, half sections, offset and revolved sections each exist for a reason, and picking the right one is a design decision."),
      ("Dimensioning with intent",
       "Every dimension on a drawing is an instruction to somebody making the part. Dimension from datums that reflect how the part functions and how it will be held during machining, not from whichever edge is convenient."),
      ("Tolerances and fits",
       "A dimension without a tolerance is an unanswered question. Understanding clearance, transition and interference fits — and where each is appropriate — is what makes a drawing manufacturable rather than aspirational."),
      ("Title blocks, BOM and standards",
       "Revision control, part numbers, material specification and surface finish are not administrative overhead. They are how a drawing survives contact with a real supply chain.")],
     "2D mechanical drafting is often described as obsolete. It is not — in most Indian manufacturing and fabrication firms, the issued drawing is still 2D, even when the design was modelled in 3D. It remains directly employable."),
]

def _md_to_sections(md):
    """Split Markdown into the (heading, paragraph) pairs the article template
    expects. Deliberately minimal: ## headings and the prose beneath them."""
    import re as _re
    sections, head, buf = [], None, []
    for line in (md or "").splitlines():
        m = _re.match(r'^#{2,3}\s+(.*)', line.strip())
        if m:
            if head:
                sections.append((head, " ".join(buf).strip()))
            head, buf = m.group(1).strip(), []
        elif line.strip():
            buf.append(line.strip())
    if head:
        sections.append((head, " ".join(buf).strip()))
    if not sections and md:
        sections = [("Overview", " ".join(md.split())[:1200])]
    return sections


def _fetch_published():
    """Pull published posts from the admin API. Returns [] on any failure, so
    a build never breaks because the backend is unreachable."""
    import os, json, urllib.request
    api = os.environ.get("POSTS_API")
    if not api:
        return []
    try:
        with urllib.request.urlopen(api, timeout=8) as r:
            rows = json.loads(r.read().decode())["rows"]
    except Exception as e:
        print(f"  ! posts API unreachable ({e}) — using built-in articles only")
        return []
    out = []
    for p in rows:
        secs = _md_to_sections(p.get("body_md", ""))
        closing = secs.pop()[1] if len(secs) > 1 else ""
        out.append((p["slug"], p["title"], p.get("excerpt") or "",
                    p.get("tag") or "News", (p.get("tag") or "").lower(),
                    secs, closing))
    print(f"  + {len(out)} published article(s) fetched from the admin")
    return out


_remote = _fetch_published()
_seen = {a[0] for a in _remote}
ARTICLES = _remote + [a for a in _FALLBACK_ARTICLES if a[0] not in _seen]

ART_BY_SLUG = {a[0]: a for a in ARTICLES}


def page_news(mode, depth=0):
    """News index — centre updates, announcements and guides.

    Posts come from the admin portal, so this page is the one part of the site
    the centre updates itself: publish from /admin/ and the item appears here
    on the next build. The built-in articles below are the starting content.
    """
    cards = ""
    for slug, title, blurb, tag, cat, _s, _c in ARTICLES:
        cards += (f'<a class="card rv" {L("article:" + slug, mode, depth)}>{figure("mech" if cat=="mechanical" else "civil")}'
                  f'<div class="card__body"><p class="label label--accent">{tag}</p>'
                  f'<h3 class="t-h3">{title}</h3><p class="t-small t-muted">{blurb}</p></div></a>')
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    {crumbs(mode, depth, [("News", None)])}
    <h1 class="t-display mb-3">News.</h1>
    <p class="t-lead measure">What is happening at the Sector 14 centre &mdash; new batches, events and competitions, placement news, and straight guides to the software the industry actually uses.</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid g-3">{cards}</div>
    <div class="note mt-6">
      This page is updated as things happen. Ask a career advisor about anything you see here,
      or tell us what you want explained &mdash; the questions we get asked most are the ones we write about next.
    </div>
  </div>
</section>
</main>
"""


def render_article(slug, mode, depth=0):
    a = ART_BY_SLUG[slug]
    _s, title, blurb, tag, cat, sections, closing = a
    body = "".join(f'<h2 class="t-h2 mt-6 mb-2">{h}</h2><p>{p}</p>' for h, p in sections)
    return f"""
<main id="main">
<article class="section">
  <div class="wrap" style="max-width:min(760px,100%)">
    {crumbs(mode, depth, [("News", "news"), (tag, None)])}
    <h1 class="t-h1 mb-3">{title}</h1>
    <p class="t-lead mb-6">{blurb}</p>
    <div class="card mb-6" style="pointer-events:none">{figure("mech" if cat=="mechanical" else "civil")}</div>
    {body}
    <h2 class="t-h2 mt-6 mb-2">Where this leaves you</h2>
    <p>{closing}</p>

    <div class="note mt-6">
      <strong>Learning this properly?</strong> Our AutoCAD programmes cover this material with live projects and a portfolio deliverable at the end.
      <div class="flex wrapf gap-2 mt-3">
        <a class="btn btn--primary" {L("programs", mode, depth)}>See AutoCAD programmes</a>
        <a class="btn btn--ghost" {L("finder", mode, depth)}>Find my career path</a>
      </div>
    </div>
  </div>
</article>
</main>
"""


def page_mentor(mode, depth=0):
    """Apply as Mentor — trainer recruitment.

    The form posts through the same lead pipeline as every other form on the
    site, tagged source="mentor_application", so applications land in the
    existing admin dashboard and can be filtered and exported there. No new
    backend, no second inbox to watch.

    The copy here is a first draft written to match the rest of the site's
    register: specific, and careful not to promise terms the centre has not
    agreed. The centre should correct the specifics — disciplines, time
    commitment and how applications are answered — before this goes live.
    """
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    {crumbs(mode, depth, [("Apply as Mentor", None)])}
    <h1 class="t-display mb-3">Teach what you<br>actually practise.</h1>
    <p class="t-lead measure">Every trainer here worked in the field before they taught it, and most
      still do. If you have built the thing you would be teaching &mdash; coordinated a model, run a
      corridor design, taken a part to manufacture, held a programme to schedule &mdash; we would like
      to hear from you.</p>
    <a class="btn btn--primary mt-4" href="#mentor-form">Apply now</a>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Who we look for</span></div>
    <h2 class="t-h2 mb-4">Practitioners, not presenters</h2>
    <div class="grid g-3">
      <div class="pillar"><h3 class="t-h3 mb-2">Industry experience first</h3>
        <p class="t-small t-muted">Time spent doing the work on real projects, not only time spent
          teaching it. That is what learners can tell the difference between.</p></div>
      <div class="pillar"><h3 class="t-h3 mb-2">Depth in one discipline</h3>
        <p class="t-small t-muted">Strong in one area &mdash; BIM, civil, structural, mechanical, MEP,
          visualisation or project planning &mdash; beats a shallow pass across all of them.</p></div>
      <div class="pillar"><h3 class="t-h3 mb-2">Willing to be questioned</h3>
        <p class="t-small t-muted">Our sessions are hands-on and learners interrupt. The trainers who
          do well here enjoy that rather than tolerate it.</p></div>
    </div>
  </div>
</section>

<section class="section section--warm section--rule">
  <div class="wrap grid g-2">
    <div>
      <h2 class="t-h2 mb-3">What it involves</h2>
      <ul class="stack t-small" style="padding-left:1.1rem;color:var(--c-ink-2)">
        <li>Teaching to a set curriculum, with room to bring your own project examples</li>
        <li>Reviewing learner work and giving usable feedback, not just marks</li>
        <li>Mock interviews and portfolio reviews as learners approach placement</li>
        <li>Keeping your own material current as the software moves</li>
      </ul>
    </div>
    <div>
      <h2 class="t-h2 mb-3">How it fits around a job</h2>
      <p class="t-small t-muted mb-3">Most of our trainers teach alongside practice. Batches run on
        weekday evenings and at weekends as well as in the day, so tell us honestly what you can
        commit to &mdash; we would rather build a schedule around you than have you drop a batch
        halfway through.</p>
      <p class="t-small t-muted">Terms are discussed individually and depend on discipline,
        experience and how much you want to take on.</p>
    </div>
  </div>
</section>

<section class="section" id="mentor-form">
  <div class="wrap">
    <div class="marker"><span class="label label--accent">Application</span></div>
    <h2 class="t-h2 mb-2">Apply as a mentor</h2>
    <p class="t-lead measure mb-4">Tell us what you have built and what you could teach. If there is
      a fit, someone from the centre will call you.</p>
    <form class="formcard" onsubmit="return false">
      <div class="grid g-2">
        <div class="field"><label for="m1">Your name</label><input id="m1" type="text" required></div>
        <div class="field"><label for="m2">Mobile number</label><input id="m2" type="tel" inputmode="numeric" required>
          <span class="field__help">We will call or message on WhatsApp</span></div>
      </div>
      <div class="grid g-2">
        <div class="field"><label for="m3">Email</label><input id="m3" type="email"></div>
        <div class="field"><label for="m4">Discipline you would teach</label>
          <select id="m4">
            <option>BIM &amp; Digital Construction</option>
            <option>Civil &amp; Infrastructure Design</option>
            <option>Architecture &amp; Visualisation</option>
            <option>Mechanical &amp; Product Design</option>
            <option>Structural Engineering &amp; Analysis</option>
            <option>Electrical &amp; MEP Design</option>
            <option>Project Planning &amp; Management</option>
            <option>AI &amp; Emerging Engineering Tech</option>
          </select></div>
      </div>
      <div class="grid g-2">
        <div class="field"><label for="m5">Years in industry</label>
          <select id="m5">
            <option>1&ndash;3</option><option>4&ndash;7</option>
            <option>8&ndash;12</option><option>12+</option>
          </select></div>
        <div class="field"><label for="m6">Current role and employer</label><input id="m6" type="text"></div>
      </div>
      <div class="field"><label for="m7">When could you teach?</label>
        <select id="m7">
          <option>Weekday evenings</option><option>Weekends</option>
          <option>Weekdays, daytime</option><option>Flexible</option>
        </select></div>
      <div class="field"><label for="m8">Software you would teach, and one project you have delivered</label>
        <textarea id="m8" rows="4"></textarea></div>
      <button class="btn btn--primary btn--wide" type="submit">Send application</button>
      <p class="t-small t-muted mt-2">We read every application. If your discipline is not one we are
        running right now we will say so rather than leave you waiting.</p>
    </form>
  </div>
</section>
</main>
"""


def page_testimonials(mode, depth=0):
    """Every learner testimonial, with the person named and credited."""
    from build_parts import published_testimonials, testimonial_tiles
    items = published_testimonials()
    return f"""
<main id="main">
<section class="section section--warm">
  <div class="wrap">
    {crumbs(mode, depth, [("Learner stories", None)])}
    <h1 class="t-display mb-3">Hear it from them.</h1>
    <p class="t-lead measure">Every one of these is a learner who sat in a classroom in Sector 14.
      No scripts, no actors &mdash; and every name here is published with that person's permission.</p>
  </div>
</section>

<section class="section testi">
  <div class="wrap">
    <div class="testi__grid testi__grid--page">{testimonial_tiles(items, depth)}</div>
    <p class="note mt-6">Thinking about the same move? Book a free counselling session and we will tell you
      honestly whether one of these paths fits your background.</p>
    <div class="flex wrapf gap-2 mt-3">
      <a class="btn btn--primary" {L("contact", mode, depth)}>Book career counselling</a>
      <a class="btn btn--ghost" {L("finder", mode, depth)}>Find my career path</a>
    </div>
  </div>
</section>
</main>
"""


# ===========================================================================
# LEGAL — these were broken links in the previous build
# ===========================================================================
LEGAL = {
    "privacy-policy": ("Privacy Policy", [
        ("What we collect", "When you enquire, book a counselling call or request a syllabus, we collect your name, mobile number and, if you choose to give it, your email address. We also record the answers you give in our career path questions so that a counsellor can have a useful conversation with you rather than starting from nothing."),
        ("Why we collect it", "To respond to your enquiry, to send you the programme information you asked for, and to arrange counselling or a centre visit. We do not sell your data."),
        ("How long we keep it", "Enquiry records are retained for as long as is necessary to respond and to maintain admission records, and are then deleted."),
        ("Analytics and advertising", "We use analytics to understand how the website is used. Non-essential tracking, including advertising pixels, runs only after you consent through the cookie banner."),
        ("Your rights", "You can ask us what we hold about you, ask us to correct it, or ask us to delete it. Contact us using the details below."),
        ("Contact", f"CADD Centre Gurugram, Sector 14. Email {EMAIL}. Phone {PHONE_D}."),
    ], None),  # LAUNCH BLOCKER: legal review against the DPDP Act required before go-live

    "terms-conditions": ("Terms &amp; Conditions", [
        ("Using this website", "This website provides information about training programmes delivered at CADD Centre Gurugram, Sector 14. Programme content, duration, schedules and fees are indicative and are confirmed at the point of enrolment."),
        ("Enrolment", "Enrolment is subject to batch availability and to the admission terms provided at the centre. Nothing on this website constitutes an offer of admission."),
        ("Placement support", "We provide placement support as described on the Careers page. We do not guarantee employment, and no statement on this website should be read as such a guarantee."),
        ("Certification", "Certification issued is as stated at enrolment. Any third-party certification is subject to that body's own terms and assessment."),
        ("Intellectual property", "Content on this website is the property of CADD Centre Gurugram and its licensors. CADD Centre and related marks belong to CADD Centre Training Services."),
        ("Governing law", "These terms are governed by the laws of India, with jurisdiction in Gurugram, Haryana."),
    ], None),  # LAUNCH BLOCKER: legal review + confirm registered entity before go-live

    "disclaimer": ("Disclaimer", [
        ("Information accuracy", "We take care to keep programme information accurate, but curriculum, duration, batch timings and fees are subject to change. Confirm current details with the centre before enrolling."),
        ("Outcome statements", "Where individual learner outcomes are shown, they are individual results published with that person's consent. Results vary by background, effort and market conditions. They are not a prediction of your result."),
        ("Third-party trademarks", "Autodesk, Bentley, Dassault Systèmes, Siemens, PTC, Ansys, Oracle and other software names and marks referenced on this website are the property of their respective owners. Their use here is descriptive and does not imply endorsement."),
        ("External links", "This website may link to third-party websites. We are not responsible for their content or their privacy practices."),
        ("Franchise relationship", "CADD Centre Gurugram, Sector 14 is an Authorised Training Centre of CADD Centre Training Services and is owned and operated by Vara Global Tech."),
    ], None),  # LAUNCH BLOCKER: legal review + confirm registered entity before go-live
}


def render_legal(key, mode, depth=0):
    title, sections, note = LEGAL[key]
    body = "".join(f'<h2 class="t-h2 mt-6 mb-2">{h}</h2><p>{p}</p>' for h, p in sections)
    return f"""
<main id="main">
<section class="section">
  <div class="wrap" style="max-width:min(760px,100%)">
    {crumbs(mode, depth, [(title, None)])}
    <h1 class="t-h1 mb-3">{title}</h1>
    <p class="label">Last updated: August 2026</p>
    {body}
    {f'<div class="note mt-6">{note}</div>' if note else ''}
  </div>
</section>
</main>
"""
