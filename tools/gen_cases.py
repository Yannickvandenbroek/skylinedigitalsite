"""Genereert de projectpagina's (werk-<slug>.html) voor alle projecten in de carrousel.
Teksten staan in CASES; header/footer komen uit website-seo.html zodat ze gelijk blijven aan de rest van de site.
Daarna: tools/i18n_extract.py + vertalen + tools/i18n_build.py voor /en, /it, /es."""
import re, json, html, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
BASE = "https://www.skylinedigital.nl"

CASES = [
 dict(slug="dekgro", name="Tegeltechniek Dekgro", h1=("Tegeltechniek", "Dekgro"), domain="dekgro.nl", url="https://dekgro.nl",
      chips=["Website", "SEO"],
      lead="Van lokaal vakbedrijf naar professionele online aanwezigheid — een complete website voor een specialist in tegelwerk van 400 m² tot 5.000 m².",
      results=["Maatwerk website met uitgebreide projectgalerij", "Professionele uitstraling passend bij het vakmanschap", "Optimalisatie voor lokale vindbaarheid in de regio"]),
 dict(slug="lillis", name="Lilli's Schilderwerken", h1=("Lilli's", "Schilderwerken"), domain="lillischilderwerken.nl", url="https://lillischilderwerken.indedemo.nl",
      chips=["Website"],
      lead="Persoonlijk en vakkundig schilderwerk voor jouw huis — een stijlvolle website die het vakmanschap en de betrouwbaarheid van het bedrijf uitstraalt.",
      results=["Sfeervolle uitstraling die vertrouwen wekt", "Helder dienstenoverzicht met binnenwerk, buitenwerk en behang", "Contactformulier en directe call-to-actions"]),
 dict(slug="bodyscan", name="BodyScan Waalre", h1=("BodyScan", "Waalre"), domain="bodyscanwaalre.nl", url="https://bodyscanwaalre.nl",
      chips=["Website", "Wellness"],
      lead="Luister naar wat jouw lichaam je vertelt — een rustige, vertrouwenwekkende website voor een specialist in Vitalfeld Technologie en gezondheidsscans.",
      results=["Kalm kleurgebruik dat vertrouwen en rust uitstraalt", "Duidelijke uitleg van de Vitalfeld Technologie", "Directe call-to-action voor het maken van een afspraak"]),
 dict(slug="echtgrieks", name="Echt Grieks", h1=("Echt Grieks —", "House Marika"), domain="echtgrieks.nl", url="https://echtgrieks.nl",
      chips=["Website", "Vakantie"],
      lead="Ervaar de unieke schoonheid van Sykia in een authentiek Grieks vakantiehuis — een sfeervolle website die vakantiegangers direct verliefd maakt op de locatie.",
      results=["Sfeervolle fotografie centraal in het design", "Duidelijke weergave van faciliteiten en locatie", "Directe boekingsflow voor meer reserveringen"]),
 dict(slug="carslease", name="CarsLease", h1=("Leaseplatform", "CarsLease"), domain="carslease.nl", url="https://carslease.nl",
      chips=["Website", "Calculator"],
      lead="De lease van je voertuig binnen 15 minuten geregeld — een snel leaseplatform voor ondernemers uit Eindhoven, met een doorzoekbare collectie en een calculator die direct je maandbedrag laat zien.",
      results=["Doorzoekbare collectie met filters op merk, model en budget", "Interactieve leasecalculator voor financial en operational lease", "Conversiegerichte opbouw met reviews en directe contactopties"]),
 dict(slug="lassie", name="Keukenmontage Lassie", h1=("Keukenmontage", "Lassie"), domain="keukenmontage-lassie.vercel.app", url="https://keukenmontage-lassie.vercel.app",
      chips=["Website", "Scroll-animatie"],
      lead="Van oud naar droomkeuken — een cinematische website voor een keukenmontage- en klussenbedrijf uit Veendam, waarin bezoekers het hele montageproces zien terwijl ze scrollen.",
      results=["Scroll-animatie die het montageproces van A tot Z laat zien", "Heldere pagina's voor keukenmontage, leidingwerk en maatwerk", "Offerteformulier en contactgegevens altijd binnen handbereik"]),
 dict(slug="dejonge", name="De Jonge Elektrotechniek", h1=("De Jonge", "Elektrotechniek"), domain="dejonge-elektrotechniek.nl", url="https://dejonge-elektrotechniek.nl",
      chips=["Website", "SEO"],
      lead="Stroom dat klopt, tot in het detail — een krachtige website voor een elektrotechnisch installatiebedrijf uit Nijkerk, gebouwd om gevonden te worden in Nijkerk, Amersfoort, Barneveld en de hele regio.",
      results=["Duidelijke pagina's per specialisme: elektra, data en beveiliging", "Lokale SEO voor Nijkerk en de omliggende plaatsen", "Werkproces, referentieprojecten en FAQ die vertrouwen wekken"]),
 dict(slug="elektropost", name="Elektropost", h1=("Installatiebedrijf", "Elektropost"), domain="elektropost.nl", url="https://elektropost.dedemoversie.nl",
      chips=["Website", "Design"],
      lead="Van laadpaal tot lichtplan — een frisse, persoonlijke website voor een elektrotechnisch installatiebedrijf uit Woudenberg dat werkt in een straal van zo'n 40 kilometer.",
      results=["Zeven specialismen overzichtelijk in beeld, van laadpalen tot zonnepanelen", "Warme, toegankelijke uitstraling die past bij een persoonlijk vakbedrijf", "Telefoonnummer en contactroutes altijd zichtbaar"]),
 dict(slug="palmyra", name="Palmyra Coaching", h1=("Palmyra", "Coaching"), domain="palmyra-coaching.dedemoversie.nl", url="https://palmyra-coaching.dedemoversie.nl",
      chips=["Website", "Coaching"],
      lead="Persoonlijke begeleiding in beweging, voeding en balans vanuit Oss — een rustige, warme website met een stapelende 'In balans'-sectie die de aanpak in drie stappen vertelt.",
      results=["Sfeervolle beeldtaal die rust en vertrouwen uitstraalt", "Alle specialisaties overzichtelijk gebundeld", "Klantverhalen, FAQ en directe contactopties via telefoon en WhatsApp"]),
]

src = open("website-seo.html").read()
HEADER = re.search(r'  <header class="nav".*?</header>\n', src, re.S).group(0)
HEADER = HEADER.replace(' aria-current="page"', '').replace('<a href="/portfolio">Portfolio</a>', '<a href="/portfolio" aria-current="page">Portfolio</a>', 1)
FOOTER = re.search(r'    <footer class="footer">.*?</footer>\n', src, re.S).group(0)
ld_index = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', open("index.html").read(), re.S).group(1))
ORG, WEBSITE = ld_index["@graph"][0], ld_index["@graph"][1]
EXT_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><line x1="7" y1="17" x2="17" y2="7"/><polyline points="7 7 17 7 17 17"/></svg>'

def esc(s): return html.escape(s, quote=True)

for i, c in enumerate(CASES):
    slug = f"werk-{c['slug']}"; url = f"{BASE}/{slug}"; img = f"/assets/work-{c['slug']}.jpg"
    title = f"Website voor {c['name']} — case | Skyline Digital"
    desc = c["lead"].split(" — ")[-1].rstrip(".")
    desc = (desc[0].upper() + desc[1:] + ". Bekijk hoe Skyline Digital deze website maakte.")
    if len(desc) > 160: desc = desc[:desc.rfind(" ", 0, 157)] + "…"
    others = [CASES[(i + k) % len(CASES)] for k in (1, 2, 3)]
    ld = {"@context": "https://schema.org", "@graph": [ORG, WEBSITE,
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Portfolio", "item": BASE + "/portfolio"},
            {"@type": "ListItem", "position": 3, "name": c["name"], "item": url}]},
        {"@type": "CreativeWork", "@id": url + "#work", "name": f"Website {c['name']}", "url": c["url"], "image": BASE + img,
         "creator": {"@id": BASE + "/#organization"}, "about": c["lead"]},
        {"@type": ["WebPage", "ItemPage"], "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "nl-NL",
         "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#organization"}, "primaryImageOfPage": BASE + img,
         "breadcrumb": {"@id": url + "#breadcrumb"}, "mainEntity": {"@id": url + "#work"}}]}
    chips = "".join(f'\n            <span class="case-chip">{esc(ch)}</span>' for ch in c["chips"])
    results = "".join(f"\n            <li>{esc(r)}</li>" for r in c["results"])
    gallery = "".join(f'\n        <a href="/werk-{o["slug"]}" class="gitem reveal"><img src="assets/work-{o["slug"]}-m.jpg" alt="{esc(o["name"])}" loading="lazy" /><div class="gcap"><span>Website</span>{esc(o["name"])}</div></a>' for o in others)
    page = f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="nl_NL" />
  <meta property="og:site_name" content="Skyline Digital" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{BASE}{img}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{BASE}{img}" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",", ":"))}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400..900&family=Inter:wght@400..700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css" />
  <link rel="stylesheet" href="pages.css" />
  <link rel="stylesheet" href="awards.css" />
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <meta name="theme-color" content="#07080b" />
</head>
<body>

{HEADER}
  <section class="case-hero bg-cream">
    <div class="orb orb-gold" style="right:-200px;top:-100px;width:500px;height:500px;opacity:.35"></div>
    <div class="wrap">
      <p class="crumbs" style="margin-bottom:36px"><a href="/">Home</a> · <a href="/portfolio">Portfolio</a> · {esc(c['name'])}</p>
      <div class="case-grid">

        <div class="case-mockup reveal reveal--left">
          <div class="browser-mockup">
            <div class="browser-bar">
              <span class="browser-dot"></span>
              <span class="browser-dot"></span>
              <span class="browser-dot"></span>
              <div class="browser-url-bar notranslate">{c['domain']}</div>
            </div>
            <img src="assets/work-{c['slug']}.jpg" alt="Website {esc(c['name'])}" />
          </div>
          <a href="{c['url']}" target="_blank" rel="noopener" class="case-visit-link">
            Ga naar de website
            {EXT_ICON}
          </a>
        </div>

        <div class="case-info reveal reveal--right">
          <div class="case-chips">{chips}
          </div>
          <h1>{esc(c['h1'][0])}<br /><span class="gold-text">{esc(c['h1'][1])}</span></h1>
          <p class="lead">{esc(c['lead'])}</p>
          <ul class="case-results">{results}
          </ul>

          <hr class="case-divider" />
          <p class="case-cta-label">Vergelijkbare website laten maken?</p>
          <p class="case-cta-sub">Binnen één dag nemen we contact met je op.</p>

          <form class="case-form" id="case-form" action="https://formspree.io/f/mdavvjrr" method="POST">
            <input type="hidden" name="_subject" value="Aanvraag via portfolio — {esc(c['name'])} pagina" />
            <div class="case-form-row">
              <input type="text" name="Naam" placeholder="Naam" required />
              <input type="tel" name="Telefoon" placeholder="Telefoon" />
            </div>
            <input type="email" name="Email" placeholder="E-mailadres" required />
            <button type="submit" class="case-form-submit">
              Neem contact met me op
              {ARROW}
            </button>
            <p class="case-form-sent" id="case-sent">Bedankt! We nemen snel contact op.</p>
          </form>
        </div>

      </div>
    </div>
  </section>

  <section class="bg-dark full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule" style="margin-inline:auto"></div>
        <p class="eyebrow">Meer werk</p>
        <h2>Recente <span class="gold-text">projecten</span></h2>
      </div>
      <div class="gallery gallery-shots">{gallery}
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Jouw bedrijf als volgende?</h2>
      <p class="lead">Laten we samen iets bouwen waar jij trots op bent.</p>
      <div class="hero-actions hero-actions-center">
        <a href="/aanvraag" class="btn btn-gold">Start je project</a>
        <a href="/portfolio" class="btn btn-ghost-light">Meer werk bekijken</a>
      </div>
    </div>
  </section>

{FOOTER}
  <script src="scroll-cinematic.js"></script>
  <script>
    document.getElementById('case-form').addEventListener('submit', async function (e) {{
      e.preventDefault();
      await fetch(this.action, {{ method: 'POST', body: new FormData(this), headers: {{ 'Accept': 'application/json' }} }});
      this.reset();
      document.getElementById('case-sent').style.display = 'block';
    }});
  </script>
</body>
</html>
'''
    open(slug + ".html", "w").write(page)
    print(slug, "desc", len(desc))

# Carrousels (home + portfolio): elk project naar zijn eigen projectpagina
for p in ("index.html", "portfolio.html"):
    s = open(p).read()
    for c in CASES:
        s = re.sub(r"(t: '" + re.escape(c["name"]).replace("'", "\\\\'") + r"',\s*href: )'[^']*'(, ext: true)?", lambda m: m.group(1) + f"'/werk-{c['slug']}'", s)
    open(p, "w").write(s)
