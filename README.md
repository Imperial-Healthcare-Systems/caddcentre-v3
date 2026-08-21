# CADD Centre Gurugram — Website

Phase 1 reference implementation, built to **Document 1 — Website Strategy & Execution Blueprint** and **Document 2 — Website Content & Copy Master**.

Zero dependencies. No build tooling required to deploy. No npm install, no framework, no bundler.

---

## What is in this package

```
preview.html          Single self-contained file — ALL 56 pages, CSS, JS and artwork
                      inlined. Double-click to open. No server, no internet needed.

dist/                 Deployable static site — 57 pages. Upload as-is to any host.
  index.html
  career-paths/            hub + 8 full career path pages
  programs/                index + 32 programme pages
  student-work/
  career-path-finder/
  careers/                 hub + first-job-pakka/
  life-at-cadd/            events, CADD Quest, testimonial video, 3D lab
  insights/                index + 2 migrated articles
  industry/corporate-training/
  about/
  contact/
  privacy-policy/  terms-conditions/  disclaimer/
  404.html
  content-inventory.csv    51-row live-site inventory (build gate)
  assets/css/main.css
  assets/js/main.js
  robots.txt
  sitemap.xml
  _headers              Security headers (Netlify format)
  netlify.toml          Netlify config + starter redirects
  vercel.json           Vercel config + starter redirects
  redirect-map.csv      Starter migration map — SEE WARNING BELOW

Source (only needed if you want to regenerate):
  build.py              Emits both targets from one source of truth
  build_shell.py        Head, header, mega menus, drawer, footer, advisor
  build_pages.py        Home, career paths hub, BIM path
  build_pages2.py       Programmes, finder, corporate, about, contact
  build_parts.py        SVG illustration system
  assets/               Canonical CSS and JS
```

Rebuild after any edit to the source files:

```bash
python3 build.py
#   dist/ built — 57 pages, 71 redirects
#   preview.html built — 56 routes
#   coverage OK — 74 redirects, 56 pages, 0 unresolved
```

**The build is gated.** `verify_coverage()` reads `content-inventory.csv` and exits
non-zero if any live URL is neither produced as a page nor covered by a redirect.
Content coverage is enforced by machinery, not by memory.

---

## Deploying

**Any static host works.** The site is plain HTML, CSS and JS.

```bash
# Netlify
netlify deploy --prod --dir=dist

# Vercel
vercel --prod dist

# Cloudflare Pages
wrangler pages deploy dist

# Traditional hosting / cPanel
# Upload the contents of dist/ to public_html/

# Local check before deploying
cd dist && python3 -m http.server 8080
```

`preview.html` is for review and sign-off. It is **not** the deployable artefact — it has no per-page URLs, so it cannot rank in search. Deploy `dist/`.

---

## Before this goes live

### 1. The redirect map — now generated, still needs live data

`dist/redirect-map.csv` is now **generated from the data model with 71 redirects**, covering every URL recorded in `content-inventory.csv`. The build fails if any inventoried URL is unaccounted for.

What it still needs from you: a live crawl to populate the `sessions_12mo` and `ranking_keywords` columns, and to catch any URL the inventory missed.

The existing site serves the same course content at **multiple URL patterns** — a `/courses/` prefix, a root-level slug, and a category-prefixed path such as `/autocad/`. That splits ranking signals today and it complicates the migration. You must:

1. Crawl `caddcentregurugram.com` (Screaming Frog or equivalent) and diff against `content-inventory.csv`
2. Add any new rows to the inventory — the build will fail until each is covered
3. Export 16 months of Search Console data as the pre-launch baseline
4. Populate sessions and ranking keywords so priority is evidence-based
5. Test on staging, deploy, then verify in production within the hour

Document 1, Section 12.2 has the full procedure and the success criterion.

### 2. Wire the lead form to a real backend

`assets/js/main.js` → `initLeadForm()` contains a `setTimeout` standing in for the CRM POST. Replace it:

```js
// Find this in initLeadForm():
setTimeout(function () { ... }, 700);

// Replace with:
fetch('/api/leads', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: data.name,
    phone: data.phone,
    stage: data.lead_stage,
    background: data.lead_background,
    goal: data.lead_goal,
    utm: Object.fromEntries(new URLSearchParams(location.search))
  })
})
.then(function (r) { if (!r.ok) throw new Error('bad response'); return r.json(); })
.then(function () { /* render reward screen — existing code */ })
.catch(function () { /* show the recoverable error copy from Document 2, 2.4 */ });
```

**The CRM decision is still open** (Document 1, Section 18, item 6). Until it is made, leads have nowhere to go and the flows below deliver limited value.

### 3. Replace the placeholder artwork

Every image slot currently holds a **generated CAD-style technical drawing** rather than a photograph. This was deliberate: stock imagery would collapse the premium positioning, and the drawings look intentional while the real shoot is pending.

Each slot has two layers — a wireframe and a rendered version — which is what drives the hover transition. To swap in photography:

```html
<!-- Replace the SVG inside these wrappers, keeping the class names -->
<div class="wf">
  <div class="wf__line"><img src="/assets/img/project-wireframe.avif" alt="..."></div>
  <div class="wf__solid"><img src="/assets/img/project-final.avif" alt="..."></div>
</div>
```

The shot list is in Document 1, Section 6.6.

### 4. Analytics

No tracking is installed. Deliberate — the current site loads **two GTM containers**, which almost certainly double-counts conversions. Resolve that before establishing any baseline, then add a single container. Event names are specified in Document 1, Section 13.2.

### 5. Content gaps

Eighteen `[TO CONFIRM]` items are listed in Document 2, Section 16. The most consequential:

- Verified CADD Centre network figures — the homepage currently withholds them rather than repeating unverified numbers
- Trainer names, credentials and photograph consent
- Consented student projects and success stories
- Authorised certification list per programme
- Fee policy — bands or counselling-only
- **"First Job Pakka"** — formal terms, or remove it

---

## Design system

Implements Document 1, Section 6. Tokens live in `:root` in `main.css`; nothing below that block uses a raw hex value or a raw pixel spacing.

| | |
|---|---|
| Style | Swiss Modernism 2.0 — strict grid, mathematical spacing, single accent |
| Colour | 70% white / 20% charcoal / 10% CADD red (`#D42027` — confirm against franchise guidelines) |
| Type | Inter (display + body), JetBrains Mono (technical labels, statistics, captions) |
| Grid | 12 / 8 / 4 columns, 8px base unit |
| Motion | 150–400ms, `transform` and `opacity` only, `prefers-reduced-motion` respected throughout |

**Signature interaction:** career-path and project cards crossfade from a wireframe line drawing to a rendered image on hover — the site demonstrates the discipline it teaches. It degrades to the rendered state under reduced-motion.

---

## Verified at build time

| Check | Result |
|---|---|
| HTML tag balance, all pages | 57/57 clean |
| Broken internal links | 0 |
| Orphan pages (<2 inbound links) | 0 |
| One `h1` per page | 57/57 |
| Title + meta description | 57/57 |
| Skip link, `lang="en-IN"`, schema.org | 57/57 |
| All form inputs labelled | 57/57 |
| Career Path Finder combinations | 480 tested, 0 empty results |
| Live URLs unaccounted for | 0 |

## What actually works in this build

- Click-activated mega menus, fully keyboard operable, Escape closes and returns focus
- Mobile drawer with a focus trap; closed drawer is not tabbable
- **Career Path Finder** — 4 questions, real recommendation logic implementing the mapping table in Document 2, Section 12.4. All **480** answer combinations tested; none return an empty result (Document 1, Section 14.3 QA gate)
- **Conversational lead form** — 4 steps, validation on blur, errors adjacent to fields, loading and error states, back navigation preserving answers
- **Self-scheduled counselling** — day, time window and channel; confirm stays disabled until all three are chosen
- Filterable programmes index and student work gallery, with honest empty states
- Curriculum and FAQ accordions
- Scroll reveal and statistic count-up, both suppressed under reduced-motion
- Floating advisor pill (desktop) and fixed call/WhatsApp bar (mobile)
- `LocalBusiness` / `EducationalOrganization` structured data

## Accessibility

Built to WCAG 2.2 AA (Document 1, Section 5.5). Skip link, sequential headings, one `h1` per page, visible focus never removed, 44×44px touch targets, labels on every input, `aria-live` error announcement, `lang="en-IN"`, contrast verified on every token pair.

**Still to do before sign-off:** screen reader pass (NVDA/VoiceOver), 200% zoom check, real-device testing. Automated tooling catches roughly a third of accessibility defects — the rest need a person.

## Performance

No framework, no bundler, no runtime dependencies. Artwork is inline SVG, so there are no image requests on first paint. The only external request is the Google Fonts stylesheet.

**For production**, self-host the two font families as WOFF2 subsets (Document 1, Section 11.2) — that removes the third-party request, improves LCP, and satisfies the `font-src` CSP directive without allowing `fonts.gstatic.com`.

## Browser support

Modern evergreen browsers. Uses CSS Grid, `clamp()`, `aspect-ratio` and `:focus-visible`, with a `padding-bottom` fallback for `aspect-ratio` on older engines. JavaScript is ES5-syntax and dependency-free; if it fails to load, navigation still works as plain links and the site remains readable.

---

*Built to Document 1 and Document 2. Where the two documents and this code disagree, the documents win — raise it as a defect.*
