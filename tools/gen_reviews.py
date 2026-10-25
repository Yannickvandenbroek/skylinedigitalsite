"""Bouwt de Google-reviewsectie op de homepage en de portfoliopagina uit content/reviews.json.
Nieuwe review? Voeg hem toe in content/reviews.json (en pas rating/count aan), draai dit script en daarna tools/i18n_build.py."""
import json, html, os, re
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
D = json.load(open("content/reviews.json"))
START, END = "<!-- REVIEWS (Google) -->", "<!-- /REVIEWS (Google) -->"
G_LOGO = ('<svg class="g-logo" viewBox="0 0 48 48" aria-hidden="true">'
          '<path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>'
          '<path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>'
          '<path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>'
          '<path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>')
COLORS = ["#1a73e8", "#34a853", "#ea4335", "#f9ab00", "#a142f4", "#12b5cb"]
def esc(s): return html.escape(s, quote=True)
def stars(n): return "★" * int(round(n)) + "☆" * (5 - int(round(n)))
def card(r, i, hidden=False):
    hid = ' aria-hidden="true"' if hidden else ""
    return (f'<article class="g-card"{hid}>'
            f'<div class="g-head"><span class="g-avatar" style="background:{COLORS[i % len(COLORS)]}">{esc(r["author"][0])}</span>'
            f'<div class="g-who"><p class="g-name notranslate">{esc(r["author"])}</p><p class="g-stars" aria-label="{r["rating"]} van 5 sterren">{stars(r["rating"])}</p></div>{G_LOGO}</div>'
            f'<p class="g-text notranslate">{esc(r["text"])}</p></article>')
revs = D["reviews"]
# genoeg kaarten per rij voor een naadloze lus; alleen de eerste set is voor schermlezers zichtbaar
reps = max(2, -(-8 // len(revs)))
def track(order):
    first = "".join(card(r, revs.index(r)) for r in order)
    rest = "".join(card(r, revs.index(r), hidden=True) for _ in range(reps * 2 - 1) for r in order)
    return first + rest
score = f'{D["rating"]:.1f}'.replace(".", ",")
SECTION = f'''{START}
  <section class="bg-white full g-section" id="reviews">
    <div class="wrap">
      <div class="g-top">
        <div class="section-head reveal">
          <div class="gold-rule"></div>
          <p class="eyebrow">Reviews</p>
          <h2>Wat klanten <span class="gold-text">zeggen</span></h2>
        </div>
        <div class="g-summary reveal">
          <div class="g-brand">{G_LOGO}<span>Google Reviews</span></div>
          <div class="g-scoreline"><span class="g-score">{score}</span><span class="g-stars g-stars-lg" aria-label="{D["rating"]} van 5 sterren">{stars(D["rating"])}</span></div>
          <p class="g-count">op basis van <span data-g-count>{D["count"]}</span> reviews</p>
          <div class="g-actions">
            <a class="g-btn g-btn-primary" href="{esc(D["writeUrl"])}" target="_blank" rel="noopener">Schrijf een review</a>
            <a class="g-btn" href="{esc(D["mapsUrl"])}" target="_blank" rel="noopener">Bekijk op Google</a>
          </div>
        </div>
      </div>
    </div>
    <div class="g-marquee" data-google-reviews>
      <div class="g-row"><div class="g-track">{track(revs)}</div></div>
      <div class="g-row g-row-rev"><div class="g-track">{track(list(reversed(revs)))}</div></div>
    </div>
    <div class="wrap g-foot"><p class="g-attr">Reviews van Google Maps</p></div>
  </section>
  {END}'''
for p in ("index.html", "portfolio.html"):
    s = open(p).read()
    if START in s and END in s:
        s = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda m: SECTION, s, count=1, flags=re.S)
    elif START in s:  # eerste keer: oude sectie (zonder eindmarkering) vervangen
        s = re.sub(re.escape(START) + r"\n  <section.*?</section>\n", lambda m: SECTION + "\n", s, count=1, flags=re.S)
    else:
        raise SystemExit(f"{p}: reviewsectie niet gevonden")
    open(p, "w").write(s)
print(f"Reviewsectie gebouwd: {len(revs)} reviews, score {score}")
