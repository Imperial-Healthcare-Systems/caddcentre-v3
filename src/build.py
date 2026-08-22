# -*- coding: utf-8 -*-
"""
Build script.

Targets:
  1. dist/        — deployable multi-page static site
  2. preview.html — single self-contained file, hash-routed

Also runs verify_coverage(): asserts every live URL recorded in
content-inventory.csv is either produced as a page or has an explicit
redirect. The build FAILS if anything is unaccounted for.

Run:  python3 build.py
"""

import os, re, shutil, csv, sys

import build_shell as S
from build_pages import page_home, page_career_paths
from build_pages2 import (page_programs, page_student_work, page_finder,
                          page_corporate, page_about, page_contact)
from build_pages3 import (page_first_job_pakka, page_careers, page_life,
                          page_news, page_mentor, page_testimonials,
                          render_article, render_legal, ARTICLES)
from build_render import render_program, render_path
from build_admin_demo import page_admin_demo
from build_data import PATHS, PROGRAMS, EXTRA_REDIRECTS

# Articles can come from the admin API, so their routes are registered here —
# after ARTICLES is resolved — rather than at module import time.
S.register_articles([a[0] for a in ARTICLES])

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")


def _mk(fn, *a):
    return lambda mode, depth=0: fn(*a, mode, depth)


PAGES = [
    ("home", "index.html", 0,
     "CADD Centre Gurugram — CAD, BIM & Engineering Careers",
     "Career-focused CAD, BIM, mechanical design and project management training in Sector 14, Gurugram. Real labs, real projects, placement support.",
     "home", page_home),
    ("career-paths", "career-paths/index.html", 1,
     "Career Paths — Engineering Training in Gurgaon | CADD Centre",
     "Eight engineering career paths — BIM, civil, architecture, mechanical, structural, MEP, planning and AI. Choose the career; we handle the software.",
     "career-paths", page_career_paths),
    ("programs", "programs/index.html", 1,
     "All Programmes — CAD, BIM & Design Courses in Gurgaon | CADD Centre",
     "Filter every programme by career path, level and format. Master programmes, professional certificates and short-term software courses in Gurugram.",
     "programs", page_programs),
    ("student-work", "student-work/index.html", 1,
     "Student Work — Built at CADD Centre Gurugram",
     "Real projects built by learners at CADD Centre Gurugram. BIM coordination, corridor design, mechanical assemblies and 3D printed prototypes.",
     "student-work", page_student_work),
    ("finder", "career-path-finder/index.html", 1,
     "Career Path Finder — Find Your Engineering Path | CADD Centre",
     "Four questions, sixty seconds. Get a recommended engineering career path, a skills roadmap and a starting programme. No sign-up required.",
     "", page_finder),
    ("careers", "careers/index.html", 1,
     "Careers & Placement Support | CADD Centre Gurugram",
     "Portfolio development, CV and profile work, mock interviews and employer introductions. Placement support described honestly.",
     "careers", page_careers),
    ("first-job-pakka", "careers/first-job-pakka/index.html", 2,
     "First Job Pakka — Training & Placement in 80 Hours | CADD Centre Gurugram",
     "CADD Centre's First Job Pakka initiative: core competence, hands-on learning and programming skills for engineers. Built to make you employable, not just certified.",
     "careers", page_first_job_pakka),
    ("life", "life-at-cadd/index.html", 1,
     "Life @ CADD Gurugram — Events, CADD Quest & the 3D Printing Lab",
     "Industry visits, technical competitions including CADD Quest 2026, workshops, mock interviews and the 3D printing lab at CADD Centre Gurugram, Sector 14.",
     "life", page_life),
    ("mentor", "apply-as-mentor/index.html", 1,
     "Apply as a Mentor — Teach at CADD Centre Gurugram",
     "Teach CAD, BIM, structural, mechanical, MEP or project management at CADD Centre Gurugram, Sector 14. For practitioners who still work in the field.",
     "mentor", page_mentor),
    ("news", "news/index.html", 1,
     "News & Updates | CADD Centre Gurugram",
     "Latest news from CADD Centre Gurugram, Sector 14 — new batches, events, competitions, placement updates and guides to the software the industry uses.",
     "news", page_news),
    ("corporate", "industry/corporate-training/index.html", 2,
     "Corporate Training for Engineering Teams | CADD Centre Gurugram",
     "Structured, assessed CAD and BIM training for engineering and design teams, on your site or at our Sector 14 centre in Gurugram.",
     "corporate", page_corporate),
    ("about", "about/index.html", 1,
     "About CADD Centre Gurugram, Sector 14",
     "An authorised CADD Centre training centre in Sector 14, Gurugram, operated by Vara Global Tech. Our trainers, our labs and how we work.",
     "about", page_about),
    ("contact", "contact/index.html", 1,
     "Contact & Book a Centre Visit | CADD Centre Gurugram",
     "Book a free centre visit or career counselling in Sector 14, Gurugram. Open 7 days, 9:30 am to 7:00 pm. Call, WhatsApp or walk in.",
     "contact", page_contact),
]

# The learner stories page is only produced once there is footage to put on
# it — an empty page would be worse than no page.
from build_data import TESTIMONIALS as _TESTI
if any(t.get("video") for t in _TESTI):
    PAGES.append(("testimonials", "testimonials/index.html", 1,
                  "Learner Stories — Video Testimonials | CADD Centre Gurugram",
                  "Hear from learners who trained at CADD Centre Gurugram, Sector 14 — in their own words, on camera.",
                  "", page_testimonials))

for k, slug, name, outcome, *_ in PATHS:
    plain = re.sub(r"&[a-z]+;", "and", name)
    PAGES.append((f"path:{k}", f"career-paths/{slug}/index.html", 2,
                  f"{plain} Career Path — Training in Gurgaon | CADD Centre",
                  f"Build a career in {plain.lower()}. Skills roadmap, programmes, roles and placement support at CADD Centre Gurugram, Sector 14.",
                  "career-paths", _mk(render_path, k)))

for p in PROGRAMS:
    slug, name = p[0], p[1]
    plain = re.sub(r"&[a-z]+;", "and", name)
    PAGES.append((f"program:{slug}", f"programs/{slug}/index.html", 2,
                  f"{plain} Course in Gurgaon | CADD Centre",
                  f"{p[5]} {plain} training in Gurgaon with live projects, certification and placement support. Weekday, evening and weekend batches.",
                  "programs", _mk(render_program, slug)))

for a in ARTICLES:
    PAGES.append((f"article:{a[0]}", f"news/{a[0]}/index.html", 2,
                  f"{a[1]} | CADD Centre Gurugram", a[2], "news", _mk(render_article, a[0])))

for key, title in [("privacy-policy", "Privacy Policy"),
                   ("terms-conditions", "Terms & Conditions"),
                   ("disclaimer", "Disclaimer")]:
    PAGES.append((key, f"{key}/index.html", 1,
                  f"{title} | CADD Centre Gurugram",
                  f"{title} for CADD Centre Gurugram, Sector 14, operated by Vara Global Tech.",
                  "", _mk(render_legal, key)))


def all_redirects():
    r = []
    for p in PROGRAMS:
        for old in p[12]:
            r.append((old, f"/programs/{p[0]}/", f"Course page rewritten — {p[1]}"))
    # Every article moved with the section rename, so each old /insights/ URL
    # needs its own 301. Generated from ARTICLES rather than hand-listed, so an
    # article added later cannot be forgotten here.
    for a in ARTICLES:
        r.append((f"/insights/{a[0]}/", f"/news/{a[0]}/",
                  "Article moved with the Insights to News rename"))
    r.extend(EXTRA_REDIRECTS)
    return r


def verify_coverage():
    inv_path = os.path.join(ROOT, "content-inventory.csv")
    if not os.path.exists(inv_path):
        print("  ! content-inventory.csv missing — cannot verify")
        return True
    produced = {"/" + p.replace("index.html", "") for _, p, *_ in PAGES}
    redirected = {old for old, _n, _x in all_redirects()}
    unresolved = []
    with open(inv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            url = row["url"].strip()
            if url in ("N/A", ""):
                continue
            if url in redirected or url in produced:
                continue
            unresolved.append((url, row["page_title"]))
    if unresolved:
        print("\n  BUILD FAILED — live URLs with no page and no redirect:")
        for u, t in unresolved:
            print(f"    {u}  ({t})")
        return False
    print(f"  coverage OK — {len(redirected)} redirects, {len(produced)} pages, 0 unresolved")
    return True


def build_mpa():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(DIST, "assets"))

    for pid, path, depth, title, desc, active, fn in PAGES:
        html = (S.head(title, desc, "mpa", depth) + S.header("mpa", depth, active, pid)
                + fn("mpa", depth) + S.footer("mpa", depth) + S.tail(depth))
        out = os.path.join(DIST, path)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "w", encoding="utf-8").write(html)

    html404 = (S.head("Page not found | CADD Centre Gurugram", "This page has moved.", "mpa", 0)
               + S.header("mpa", 0)
               + """<main id="main"><section class="section"><div class="wrap">
<p class="label label--accent mb-3">404</p>
<h1 class="t-display mb-3">This page has moved</h1>
<p class="t-lead measure mb-4">The page you were looking for is not here any more. Try the career paths, browse all programmes, or call us on +91 99907 07382 and we will point you in the right direction.</p>
<div class="flex wrapf gap-2">
<a class="btn btn--primary" href="/career-paths/">Career paths</a>
<a class="btn btn--secondary" href="/programs/">All programmes</a>
<a class="btn btn--ghost" href="/">Home</a></div>
</div></section></main>"""
               + S.footer("mpa", 0) + S.tail(0))
    open(os.path.join(DIST, "404.html"), "w", encoding="utf-8").write(html404)

    open(os.path.join(DIST, "robots.txt"), "w").write(
        "User-agent: *\nAllow: /\nDisallow: /lp/\nDisallow: /admin\nDisallow: /api/\n\n"
        "Sitemap: https://caddcentregurugram.com/sitemap.xml\n")

    # News is the one section the centre updates itself, so it and its posts
    # are advertised as changing weekly rather than monthly.
    def _freq(pid):
        return "weekly" if pid == "news" or pid.startswith("article:") else "monthly"

    urls = "".join(
        f"  <url><loc>https://caddcentregurugram.com/{p.replace('index.html','')}</loc>"
        f"<changefreq>{_freq(pid)}</changefreq>"
        f"<priority>{'1.0' if pid=='home' else '0.8'}</priority></url>\n"
        for pid, p, *_ in PAGES)
    open(os.path.join(DIST, "sitemap.xml"), "w").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}</urlset>\n')

    open(os.path.join(DIST, "_headers"), "w").write("""/*
  Strict-Transport-Security: max-age=15768000; includeSubDomains
  X-Content-Type-Options: nosniff
  X-Frame-Options: SAMEORIGIN
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; script-src 'self'; frame-src https://www.youtube-nocookie.com; frame-ancestors 'self'; base-uri 'self'; form-action 'self'

/assets/*
  Cache-Control: public, max-age=31536000, immutable
""")

    with open(os.path.join(DIST, "redirect-map.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["old_url", "new_url", "redirect_type", "sessions_12mo",
                    "ranking_keywords", "tested", "verified_prod", "notes"])
        for old, new, note in all_redirects():
            w.writerow([old, new, "301" if old != new else "n/a (retained)", "", "", "N", "N", note])

    rules = "\n".join(
        f'[[redirects]]\n  from = "{o}"\n  to = "{n}"\n  status = 301\n  force = true\n'
        for o, n, _ in all_redirects() if o != n)
    open(os.path.join(DIST, "netlify.toml"), "w").write(
        f'[build]\n  publish = "."\n\n{rules}\n'
        '# Generated from build_data.py. Complete the sessions/keywords columns in\n'
        '# redirect-map.csv from a live crawl before launch.\n')

    vre = ",\n".join(
        f'    {{ "source": "{o.rstrip("/")}", "destination": "{n}", "permanent": true }}'
        for o, n, _ in all_redirects() if o != n)
    open(os.path.join(DIST, "vercel.json"), "w").write(
        '{\n  "cleanUrls": true,\n  "trailingSlash": true,\n'
        '  "headers": [{ "source": "/(.*)", "headers": ['
        '{ "key": "X-Content-Type-Options", "value": "nosniff" },'
        '{ "key": "X-Frame-Options", "value": "SAMEORIGIN" },'
        '{ "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }] }],\n'
        f'  "redirects": [\n{vre}\n  ]\n}}\n')

    # backend: admin UI, serverless functions, schema
    for d in ("admin", "api", "db"):
        src = os.path.join(ROOT, d)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(DIST, d))

    for extra in ("content-inventory.csv", "README.md", "ADMIN-SETUP.md", "LAUNCH-BLOCKERS.md", "RUN-LOCALLY.md", "serve.js"):
        src = os.path.join(ROOT, extra)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(DIST, extra))

    print(f"  dist/ built — {len(PAGES) + 1} pages, "
          f"{len([1 for o,n,_ in all_redirects() if o!=n])} redirects")


def _inline_images(html):
    """The preview is a single double-clickable file, so every image has to be
    embedded. We drop the <source> variants and inline one WebP per slot as a
    data URI — srcset is meaningless without a filesystem anyway."""
    import base64, glob
    imgdir = os.path.join(ROOT, "assets/img")
    cache = {}

    # Pick a width per slot from what actually exists on disk. Hardcoding a
    # width list meant a new crop (hero-wide only has 768/1280/1920) matched
    # nothing and produced an empty src.
    import glob as _glob, re as _re
    WIDE = {"hero", "hero-wide", "hero-mid", "hero-tall", "heroexterior", "facilities"}
    MID = {"printing", "mech", "arch", "bim", "civil", "classroom",
           "sitevisit", "presentation", "corporate", "trainer-context"}

    def _widths(stem, ext):
        out = []
        for p in _glob.glob(os.path.join(imgdir, f"{stem}-*.{ext}")):
            m = _re.match(rf"{_re.escape(stem)}-(\d+)\.{ext}$", os.path.basename(p))
            if m:
                out.append(int(m.group(1)))
        return sorted(out)

    def data_uri(stem):
        if stem in cache:
            return cache[stem]
        # target width by role, then snap to the nearest available
        target = 1280 if stem in WIDE else (960 if stem in MID else 700)
        for ext, mime in (("avif", "image/avif"), ("webp", "image/webp")):
            ws = _widths(stem, ext)
            if not ws:
                continue
            pick = min(ws, key=lambda w: (abs(w - target), w))
            p = os.path.join(imgdir, f"{stem}-{pick}.{ext}")
            b = base64.b64encode(open(p, "rb").read()).decode()
            cache[stem] = f"data:{mime};base64,{b}"
            return cache[stem]
        print(f"  ! preview: no asset found for slot '{stem}'")
        cache[stem] = ""
        return ""

    # remove the <source> elements — they point at files that will not exist
    html = re.sub(r'<source\b[^>]*>', '', html)

    # 18 unique images are used 66 times. Embedding the blob at each use point
    # tripled the file, so each image is emitted ONCE into a stylesheet and the
    # <img> elements carry a transparent pixel plus a class. Alt text, sizing
    # and object-fit behaviour are unchanged.
    PIXEL = ("data:image/gif;base64,"
             "R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7")
    used = []

    def repl(m):
        stem = m.group(1)
        uri = data_uri(stem)
        if not uri:
            return 'src=""'
        if stem not in used:
            used.append(stem)
        return f'src="{PIXEL}" class="ph ph-{stem}"'

    html = re.sub(r'src="(?:\.\./)*assets/img/([a-z0-9-]+)-\d+\.(?:webp|avif)"', repl, html)

    rules = "".join(
        f".ph-{stem}{{background-image:url({cache[stem]})}}" for stem in used if cache.get(stem))
    style = ("<style>.ph{background-size:cover;background-position:center;"
             "background-repeat:no-repeat}" + rules + "</style>")
    return html.replace("</head>", style + "</head>", 1)


def build_preview():
    css = open(os.path.join(ROOT, "assets/css/main.css"), encoding="utf-8").read()
    js = open(os.path.join(ROOT, "assets/js/main.js"), encoding="utf-8").read()
    sections = ""
    for pid, path, depth, title, desc, active, fn in PAGES:
        rid = pid.replace(":", "--")
        sections += (f'<div data-page="{rid}" data-title="{title}"'
                     f'{" hidden" if pid != "home" else ""}>\n{fn("spa", 0)}\n</div>\n')

    # Preview-only demo of the admin, so the interface can be shown without a
    # server. Reachable at #admin. Not present in dist/.
    sections += ('<div data-page="admin" data-title="Admin (demo) — CADD Centre Gurugram" hidden>\n'
                 + page_admin_demo("spa", 0) + '\n</div>\n')
    head = S.head("CADD Centre Gurugram — CAD, BIM & Engineering Careers", PAGES[0][4], "spa", 0)
    head = re.sub(r'<link rel="stylesheet" href="[^"]*">', f"<style>\n{css}\n</style>", head)
    html = (head + S.header("spa", 0) + sections + S.footer("spa", 0)
            + f"<script>\n{js}\n</script>\n</body>\n</html>\n")
    html = _inline_images(html)
    open(os.path.join(ROOT, "preview.html"), "w", encoding="utf-8").write(html)
    print(f"  preview.html built — "
          f"{os.path.getsize(os.path.join(ROOT,'preview.html'))/1024:.0f} KB, {len(PAGES)} routes")


if __name__ == "__main__":
    print("Building…")
    build_mpa()
    build_preview()
    if not verify_coverage():
        sys.exit(1)
    print("Done.")
