# -*- coding: utf-8 -*-
"""
Google Business Profile reviews for the homepage review section.

The site is static, so reviews are fetched at build time and written into the
HTML. No API key ever reaches the browser and pages stay request-free.

    # refresh from Google, then write the section into the pages
    GOOGLE_MAPS_API_KEY=AIza... python3 src/build_reviews.py --fetch --render

    # re-render from the cached JSON (no network, no key needed)
    python3 src/build_reviews.py --render

Data lives in src/data/reviews.json. Until the first --fetch runs, that file
holds the figures and quotes taken from the Google listing by hand, so the
section is real content either way.

The Places API returns the five most recent reviews for a place, not the whole
history — "Read all N reviews on Google" links out for the rest. Google's terms
require the rating, the author and a link back to Google to be shown together,
and reviews not to be cached indefinitely: re-run --fetch on a schedule (a
weekly cron or CI job is enough). See src/REVIEWS-SETUP.md.
"""

import argparse, html, io, json, os, re, sys, urllib.error, urllib.parse, urllib.request
from datetime import date, datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(HERE, "data", "reviews.json")

# Pages carrying the review section: the built homepage and the SPA preview.
TARGETS = [os.path.join(ROOT, "index.html"), os.path.join(HERE, "preview.html")]

PLACE_QUERY = "CADD Centre Gurugram Sector 14"
API = "https://places.googleapis.com/v1"
DETAIL_FIELDS = "id,rating,userRatingCount,googleMapsUri,reviews"

START, END = "<!-- reviews:start -->", "<!-- reviews:end -->"

# The Google mark, shown on each avatar so a review reads as Google's own.
GOOGLE_G = (
    '<svg viewBox="0 0 48 48" aria-hidden="true">'
    '<path fill="#4285F4" d="M45.1 24.5c0-1.6-.1-3.1-.4-4.5H24v8.5h11.8c-.5 2.8-2 5.1-4.4 6.7v5.5h7.1c4.2-3.8 6.6-9.5 6.6-16.2z"/>'
    '<path fill="#34A853" d="M24 46c5.9 0 10.9-2 14.6-5.3l-7.1-5.5c-2 1.3-4.5 2.1-7.5 2.1-5.7 0-10.6-3.9-12.3-9.1H4.3v5.7C8 41.1 15.4 46 24 46z"/>'
    '<path fill="#FBBC05" d="M11.7 28.2c-.4-1.3-.7-2.7-.7-4.2s.3-2.9.7-4.2v-5.7H4.3C2.9 17.1 2 20.5 2 24s.9 6.9 2.3 9.9l7.4-5.7z"/>'
    '<path fill="#EA4335" d="M24 10.8c3.2 0 6.1 1.1 8.4 3.3l6.3-6.3C34.9 4.2 29.9 2 24 2 15.4 2 8 6.9 4.3 14.1l7.4 5.7c1.7-5.2 6.6-9 12.3-9z"/>'
    '</svg>'
)

# The "verified" tick shown beside a rating.
VERIFIED = (
    '<svg viewBox="0 0 24 24" aria-hidden="true">'
    '<circle cx="12" cy="12" r="11" fill="currentColor"/>'
    '<path fill="#fff" d="M10.4 16.6 6.2 12.4l1.6-1.6 2.6 2.6 5.8-5.8 1.6 1.6z"/>'
    '</svg>'
)


# --------------------------------------------------------------------------- #
# Fetch
# --------------------------------------------------------------------------- #

def _call(url, key, field_mask, payload=None):
    req = urllib.request.Request(url, data=None if payload is None else json.dumps(payload).encode())
    req.add_header("X-Goog-Api-Key", key)
    req.add_header("X-Goog-FieldMask", field_mask)
    if payload is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"Places API {e.code}: {e.read().decode('utf-8', 'replace')[:600]}")


def resolve_place_id(key, query=PLACE_QUERY):
    """Text Search, so the Place ID does not have to be found by hand."""
    res = _call(f"{API}/places:searchText", key,
                "places.id,places.displayName,places.formattedAddress",
                {"textQuery": query, "languageCode": "en", "maxResultCount": 1})
    places = res.get("places") or []
    if not places:
        sys.exit(f"No place matched {query!r}. Pass GOOGLE_PLACE_ID explicitly.")
    p = places[0]
    print(f"resolved place: {p.get('displayName', {}).get('text')} — {p.get('formattedAddress')}")
    return p["id"]


def fetch(key, place_id=None):
    place_id = place_id or resolve_place_id(key)
    res = _call(f"{API}/places/{place_id}?languageCode=en", key, DETAIL_FIELDS)

    reviews = []
    for r in res.get("reviews", []):
        text = (r.get("text") or r.get("originalText") or {}).get("text", "").strip()
        author = (r.get("authorAttribution") or {}).get("displayName", "").strip()
        if not text:
            continue
        reviews.append({
            "author": author or "Google reviewer",
            "rating": r.get("rating", 5),
            "when": r.get("relativePublishTimeDescription", ""),
            "publishTime": r.get("publishTime", ""),
            "text": text,
            # Google-hosted avatar. Rendered when present, initial letter when not.
            "photo": (r.get("authorAttribution") or {}).get("photoUri", ""),
        })

    data = {
        "source": "places-api",
        "placeId": res.get("id", place_id),
        "rating": res.get("rating"),
        "ratingCount": res.get("userRatingCount"),
        "reviewsUrl": res.get("googleMapsUri", ""),
        "fetchedAt": datetime.now(timezone.utc).date().isoformat(),
        "reviews": reviews,
    }
    os.makedirs(os.path.dirname(DATA), exist_ok=True)
    with io.open(DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"wrote {os.path.relpath(DATA, ROOT)}: {data['rating']} from "
          f"{data['ratingCount']} reviews, {len(reviews)} quotes")
    return data


# --------------------------------------------------------------------------- #
# Render
# --------------------------------------------------------------------------- #

def load():
    with io.open(DATA, encoding="utf-8") as f:
        return json.load(f)


def _stars(rating):
    full = int(round(rating or 5))
    full = max(1, min(5, full))
    return ("&#9733;" * full) + ("&#9734;" * (5 - full))


def _avatar_hue(name):
    """Stable colour per reviewer, the way Google tints a letter avatar."""
    return sum(ord(c) * (i + 7) for i, c in enumerate(name)) % 360


def _initial(name):
    for ch in name:
        if ch.isalnum():
            return ch.upper()
    return "G"


def _when(review):
    """Prefer Google's own phrasing, else a month from the publish date."""
    if review.get("when"):
        return html.escape(review["when"])
    stamp = review.get("publishTime", "")
    try:
        return datetime.fromisoformat(stamp.replace("Z", "+00:00")).strftime("%b %Y")
    except ValueError:
        return ""


def reviews_section(data=None):
    """Inner HTML of the review section, between the start/end markers."""
    d = data or load()
    rating = d.get("rating") or 0
    count = d.get("ratingCount") or 0
    url = d.get("reviewsUrl") or (
        "https://www.google.com/maps/search/?api=1&query="
        + urllib.parse.quote(PLACE_QUERY))

    cards = ""
    for i, r in enumerate(d.get("reviews", [])):
        name = r.get("author") or "Google reviewer"
        stars = int(round(r.get("rating") or 5))
        delay = f' data-delay="{i * 60}"' if i else ""
        when = _when(r)
        if r.get("photo"):
            face = (f'<img src="{html.escape(r["photo"])}" alt="" width="64" height="64" '
                    f'loading="lazy" decoding="async" referrerpolicy="no-referrer">')
        else:
            face = _initial(name)
        cards += f"""      <article class="grr__card rv"{delay}>
        <div class="grr__avatar" style="--grr-av:hsl({_avatar_hue(name)} 45% 70%)" aria-hidden="true">{face}
          <span class="grr__g">{GOOGLE_G}</span>
        </div>
        <p class="grr__name">{html.escape(name)}</p>
        <p class="grr__when">{when or "on Google"}</p>
        <p class="grr__rating"><span class="grr__stars" role="img" aria-label="{stars} out of 5">{_stars(stars)}</span><span class="grr__check" title="Verified Google review">{VERIFIED}</span></p>
        <p class="grr__text" data-grr-text>{html.escape(" ".join(r["text"].split()))}</p>
      </article>
"""

    rating_txt = f"{rating:.1f}".rstrip("0").rstrip(".") if rating else "&mdash;"
    updated = d.get("fetchedAt") or ""
    try:
        updated = date.fromisoformat(updated).strftime("%d %b %Y")
    except ValueError:
        pass

    return f"""{START}
    <div class="marker"><span class="label label--accent">Reviews</span></div>
    <h2 class="t-display mb-2">What learners say.</h2>
    <div class="grsum">
      <span class="grsum__g">{GOOGLE_G}</span>
      <span class="grsum__score" data-grr-rating>{rating_txt}</span>
      <span class="grsum__meta">
        <span class="grr__stars" role="img" aria-label="{rating_txt} out of 5">{_stars(rating)}</span>
        <span class="grsum__count"><span data-grr-count>{count}</span> Google reviews</span>
      </span>
      <a class="btn btn--google" href="{html.escape(url)}" target="_blank" rel="noopener" data-grr-link>
        <span class="btn__gicon">{GOOGLE_G}</span>All reviews
      </a>
    </div>
    <div class="grr" data-grr>
      <button class="grr__nav grr__nav--prev" type="button" data-grr-prev aria-label="Previous reviews" hidden>
        <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M9 1L3 7l6 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
      <div class="grr__track" data-grr-track tabindex="0" role="group" aria-label="Google reviews">
{cards}      </div>
      <button class="grr__nav grr__nav--next" type="button" data-grr-next aria-label="More reviews" hidden>
        <svg viewBox="0 0 14 14" fill="none" aria-hidden="true"><path d="M5 1l6 6-6 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
    </div>
    <p class="label mt-4 t-muted" data-grr-stamp>Reviews and rating from Google &middot; last updated {updated}</p>
    {END}"""


def patch(path, block, data):
    with io.open(path, encoding="utf-8") as f:
        src = f.read()

    if START not in src or END not in src:
        print(f"SKIP {os.path.relpath(path, ROOT)}: no reviews markers")
        return False

    out = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, src, flags=re.S)

    # Keep the hero trust strip on the same numbers as the section below it.
    rating = data.get("rating")
    count = data.get("ratingCount")
    if rating:
        txt = f"{rating:.1f}".rstrip("0").rstrip(".")
        out = re.sub(r'(<span data-count=")[\d.]+(">)[\d.]+(</span></span>\s*</div>\s*'
                     r'<p class="statbar__l">Google rating)',
                     lambda m: f"{m.group(1)}{txt}{m.group(2)}{txt}{m.group(3)}", out)
    if count:
        out = re.sub(r'(Google rating<br><span data-count=")\d+(">)\d+(</span> reviews)',
                     lambda m: f"{m.group(1)}{count}{m.group(2)}{count}{m.group(3)}", out)

    if out == src:
        print(f"unchanged {os.path.relpath(path, ROOT)}")
        return False
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"updated {os.path.relpath(path, ROOT)}")
    return True


def render():
    data = load()
    block = reviews_section(data)
    for path in TARGETS:
        if os.path.exists(path):
            patch(path, block, data)


# --------------------------------------------------------------------------- #

def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--fetch", action="store_true", help="refresh src/data/reviews.json from Google")
    ap.add_argument("--render", action="store_true", help="write the section into the pages")
    args = ap.parse_args()
    if not (args.fetch or args.render):
        args.render = True

    if args.fetch:
        key = os.environ.get("GOOGLE_MAPS_API_KEY")
        if not key:
            sys.exit("GOOGLE_MAPS_API_KEY is not set — see src/REVIEWS-SETUP.md")
        fetch(key, os.environ.get("GOOGLE_PLACE_ID"))
    if args.render:
        render()


if __name__ == "__main__":
    main()
