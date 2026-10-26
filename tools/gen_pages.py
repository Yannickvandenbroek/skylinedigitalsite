import re, json, html, os, glob
os.chdir("/Users/yannickvandenbroek/Documents/Skylinedigital/own site/skyline-digital")
BASE = "https://www.skylinedigital.nl"
TODAY = "2026-10-06"
src = open("website-seo.html").read()
HEADER = re.search(r'  <header class="nav".*?</header>\n', src, re.S).group(0)
HEADER = re.sub(r' aria-current="page"', '', HEADER)
FOOTER = re.search(r'    <footer class="footer">.*?</footer>\n', src, re.S).group(0)
ARROW = '<span class="row-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>'

CITIES = [
 dict(slug="den-bosch", name="Den Bosch", full="'s-Hertogenbosch", in_="in Den Bosch", region="Noord-Brabant",
      intro="Skyline Digital zit zelf aan de Bruistensingel in 's-Hertogenbosch. Een website laten maken in Den Bosch betekent bij ons: een bureau om de hoek, een kop koffie in het Paleiskwartier of de binnenstad, en een site die precies past bij hoe Bossche klanten zoeken en kopen.",
      intro2="Van ondernemers op bedrijventerrein De Herven en De Brand tot winkels in de Vughterstraat en praktijken in Maaspoort en Rosmalen: we kennen de stad, de concurrentie en de zoekwoorden waar jouw klanten op zoeken.",
      sectors=["bouw, installatie en afbouw", "horeca en retail in de binnenstad", "zakelijke dienstverlening in het Paleiskwartier", "zorg- en wellnesspraktijken"],
      places="de Binnenstad, het Paleiskwartier, Maaspoort, De Groote Wielen, Engelen en Empel", near=["rosmalen","vught","oss"], travel="Wij zitten zelf in Den Bosch — een afspraak op jouw locatie is zo gemaakt."),
 dict(slug="rosmalen", name="Rosmalen", full="Rosmalen", in_="in Rosmalen", region="Noord-Brabant",
      intro="Rosmalen groeit hard: De Groote Wielen, bedrijventerrein Kruisstraat en een levendig centrum rond de Molenhoekpassage. Wie hier een website laat maken, wil een site die net zo professioneel oogt als de bedrijven die er zitten — en die gevonden wordt door inwoners van Rosmalen én de rest van de gemeente 's-Hertogenbosch.",
      intro2="Vanaf ons kantoor aan de Bruistensingel zijn we in tien minuten in Rosmalen. We bouwen websites voor aannemers, autobedrijven, kappers, fysiotherapeuten en andere lokale ondernemers die meer uit hun online vindbaarheid willen halen.",
      sectors=["bouw- en klusbedrijven", "autobedrijven en garages", "praktijken voor fysio, tandarts en huid", "sport, fitness en personal training"],
      places="het centrum, De Groote Wielen, Kruisstraat, Hintham en Maliskamp", near=["den-bosch","oss","vught"], travel="Rosmalen ligt op tien minuten van ons kantoor — we komen graag langs."),
 dict(slug="vught", name="Vught", full="Vught", in_="in Vught", region="Noord-Brabant",
      intro="Vught staat bekend om zijn groene villawijken, de IJzeren Man en een ondernemend centrum. Klanten in Vught verwachten kwaliteit — ook online. Een website laten maken in Vught vraagt dus om een ontwerp met rust, klasse en een uitstraling die bij het dorp past.",
      intro2="We werken voor Vughtse interieurzaken, makelaars, adviesbureaus, zorgverleners en horeca. Omdat we vanuit Den Bosch op een kwartier afstand zitten, combineren we een persoonlijk gesprek op locatie met de snelheid van een klein, gespecialiseerd team.",
      sectors=["makelaars en vastgoed", "interieur, tuin en woninginrichting", "advies- en coachingpraktijken", "restaurants en lunchrooms"],
      places="het centrum, Vught-Noord, de Loonse en Drunense Duinen-zijde en Cromvoirt", near=["den-bosch","rosmalen","tilburg"], travel="Vught ligt op een kwartier van ons kantoor in Den Bosch."),
 dict(slug="oss", name="Oss", full="Oss", in_="in Oss", region="Noord-Brabant",
      intro="Oss is een echte maak- en handelsstad: van farma en food tot logistiek en metaal. Juist in een stad met zoveel bedrijvigheid maakt een sterke website het verschil tussen gevonden worden en overgeslagen worden. Een website laten maken in Oss doe je daarom met een bureau dat snelheid, vindbaarheid en een professionele uitstraling combineert.",
      intro2="Vanuit Den Bosch zijn we in twintig minuten in Oss. We bouwen voor productiebedrijven en toeleveranciers op Elzenburg en Vorstengrafdonk, maar net zo goed voor winkels in het centrum en praktijken in Ruwaard en Ussen.",
      sectors=["maakindustrie en toeleveranciers", "logistiek en transport", "installatie- en technische bedrijven", "winkels en horeca in het centrum"],
      places="het centrum, Ruwaard, Ussen, Schadewijk en de bedrijventerreinen Elzenburg, Moleneind en Vorstengrafdonk", near=["den-bosch","uden","nijmegen"], travel="Oss ligt op twintig minuten van ons kantoor via de A59."),
 dict(slug="eindhoven", name="Eindhoven", full="Eindhoven", in_="in Eindhoven", region="Noord-Brabant",
      intro="Eindhoven is de technologie- en designstad van Nederland: Brainport, de High Tech Campus, Strijp-S en de Dutch Design Week. Bedrijven die hier een website laten maken, meten zich met een hoog niveau. Wij bouwen sites die dat niveau halen — strak ontworpen, technisch scherp en gebouwd om te converteren.",
      intro2="Of je nu een startup bent op Strijp-S, een installatiebedrijf in Woensel of een restaurant in het centrum: we vertalen jouw verhaal naar een website die bij de Eindhovense standaard past en die in Google boven de concurrentie uitkomt.",
      sectors=["tech, software en startups", "design- en creatieve bureaus", "installatie- en bouwbedrijven", "horeca, retail en leisure"],
      places="het centrum, Strijp-S, Woensel, Stratum, Gestel, Tongelre en de High Tech Campus", near=["den-bosch","tilburg","oss"], travel="Eindhoven ligt op een half uur van Den Bosch via de A2 — we komen graag langs."),
 dict(slug="tilburg", name="Tilburg", full="Tilburg", in_="in Tilburg", region="Noord-Brabant",
      intro="Tilburg combineert een rijk textielverleden met een jonge, creatieve energie: de Spoorzone, Tilburg University, Piushaven en een enorme studentenpopulatie. Een website laten maken in Tilburg vraagt om een frisse uitstraling die opvalt bij een jong, kritisch publiek — en om vindbaarheid in een stad met veel concurrentie.",
      intro2="We werken voor Tilburgse horeca, logistieke bedrijven, creatieve ondernemers en praktijken. Vanuit Den Bosch zitten we op een halfuur afstand, dus een kennismaking op locatie in de Spoorzone of in jouw eigen zaak is zo geregeld.",
      sectors=["logistiek en distributie", "creatieve sector en events", "horeca en nachtleven", "onderwijs- en zorgpartijen"],
      places="het centrum, de Spoorzone, Piushaven, Reeshof, Berkel-Enschot en Udenhout", near=["den-bosch","vught","breda"], travel="Tilburg ligt op een half uur van ons kantoor via de N65."),
 dict(slug="breda", name="Breda", full="Breda", in_="in Breda", region="Noord-Brabant",
      intro="Breda is een stad met allure: de Grote Markt, het Ginneken, de haven en een sterke mix van zakelijke dienstverlening, food en toerisme. Een website laten maken in Breda betekent voor ons een ontwerp dat die Bourgondische kwaliteit uitstraalt en tegelijk keihard werkt voor je omzet.",
      intro2="We bouwen voor Bredase adviesbureaus, bouwbedrijven, hospitality en winkels in de binnenstad. Door onze focus op snelheid en SEO zie je de resultaten terug in Google — ook in een stad waar veel bureaus actief zijn.",
      sectors=["zakelijke dienstverlening en advies", "food, horeca en hospitality", "bouw, installatie en vastgoed", "retail in de binnenstad en het Ginneken"],
      places="het centrum, het Ginneken, Princenhage, Haagse Beemden, Teteringen en Prinsenbeek", near=["tilburg","den-bosch","eindhoven"], travel="Breda ligt op drie kwartier van Den Bosch; de kennismaking doen we op locatie of via video."),
 dict(slug="nijmegen", name="Nijmegen", full="Nijmegen", in_="in Nijmegen", region="Gelderland",
      intro="Nijmegen is de oudste stad van Nederland en tegelijk een van de jongste door de Radboud Universiteit en het Radboudumc. Zorg, onderwijs, horeca en een actief MKB zorgen voor een drukke online markt. Wie in Nijmegen een website laat maken, wil opvallen tussen die concurrentie — met een site die snel is, mooi oogt en vindbaar is.",
      intro2="Vanuit Den Bosch zijn we in veertig minuten in Nijmegen. We werken voor praktijken en zorgondernemers rond het Radboud, voor horeca aan de Waalkade en voor bedrijven op Bijsterhuizen en de Winkelsteeg.",
      sectors=["zorg, therapie en paramedische praktijken", "horeca aan de Waalkade en in de binnenstad", "onderwijs en trainingsbureaus", "bedrijven op Bijsterhuizen en Winkelsteeg"],
      places="het centrum, de Waalkade, Dukenburg, Lindenholt, Nijmegen-Noord en de Winkelsteeg", near=["oss","den-bosch","uden"], travel="Nijmegen ligt op veertig minuten van ons kantoor via de A50 en A73."),
 dict(slug="waalwijk", name="Waalwijk", full="Waalwijk", in_="in Waalwijk", region="Noord-Brabant",
      intro="Waalwijk is van oudsher de schoen- en lederstad en vandaag een logistieke hotspot aan de A59, met Haven Zeven en Haven Acht als snelgroeiende bedrijventerreinen. Een website laten maken in Waalwijk doen we voor transporteurs, groothandels en productiebedrijven, maar net zo goed voor winkels en horeca aan de Grotestraat.",
      intro2="We zitten op twintig minuten rijden in Den Bosch. Dat betekent korte lijnen, een persoonlijk gesprek op jouw locatie en een website die gebouwd is om in Waalwijk, Kaatsheuvel, Sprang-Capelle en de rest van De Langstraat gevonden te worden.",
      sectors=["logistiek, transport en groothandel", "productie en maakindustrie", "winkels en horeca in het centrum", "bouw- en installatiebedrijven"],
      places="het centrum, Haven Zeven en Haven Acht, Sprang-Capelle, Waspik en Kaatsheuvel", near=["den-bosch","tilburg","vught"], travel="Waalwijk ligt op twintig minuten van Den Bosch via de A59."),
 dict(slug="uden", name="Uden", full="Uden", in_="in Uden", region="Noord-Brabant",
      intro="Uden is het winkel- en zorghart van de gemeente Maashorst, met een gezellig centrum, ziekenhuis Bernhoven en een sterk MKB op Loopkant-Liessent en Goorkens. Een website laten maken in Uden betekent voor ons een site die lokaal vindbaar is — niet alleen in Uden, maar in de hele regio tot aan Veghel, Boekel en Oss.",
      intro2="Vanuit Den Bosch zijn we in een half uur in Uden. We bouwen voor winkeliers, zorgverleners, bouwbedrijven en agrarische ondernemers die hun online uitstraling willen laten aansluiten bij de kwaliteit die ze in de praktijk leveren.",
      sectors=["retail en horeca in het centrum", "zorg- en gezondheidspraktijken", "bouw, installatie en techniek", "agrarische en groene bedrijven"],
      places="het centrum, Uden-Zuid, Volkel, Odiliapeel en de bedrijventerreinen Loopkant-Liessent en Goorkens", near=["oss","den-bosch","nijmegen"], travel="Uden ligt op een half uur van ons kantoor via de A50."),
]
CITY_BY = {c["slug"]: c for c in CITIES}

# Kennisbankartikelen staan als losse bestanden in content/kennisbank/<datum>-<slug>.html:
# een commentaarblok met velden (title, slug, date, eyebrow, read, img, desc) en daaronder de HTML van het artikel.
# Nieuw artikel = nieuw bestand; zie content/kennisbank/SCHRIJFGIDS.md.
STRICT_FROM = "2026-10-17"  # artikelen vanaf deze datum volgen de volledige SCHRIJFGIDS
def load_articles():
    arts, errors = [], []
    for path in sorted(glob.glob("content/kennisbank/*.html")):
        raw = open(path).read()
        m = re.match(r"\s*<!--(.*?)-->\s*(.*)", raw, re.S)
        if not m: errors.append(f"{path}: geen <!-- ... --> blok met velden bovenaan"); continue
        meta = {}
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip()
        meta["body"] = m.group(2).strip()
        missing = [k for k in ("title", "slug", "date", "eyebrow", "read", "img", "desc") if not meta.get(k)]
        if missing: errors.append(f"{path}: veld(en) ontbreken: {', '.join(missing)}"); continue
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", meta["slug"]): errors.append(f"{path}: slug '{meta['slug']}' mag alleen kleine letters, cijfers en streepjes bevatten")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["date"]): errors.append(f"{path}: date moet JJJJ-MM-DD zijn")
        if len(meta["title"]) > 70: errors.append(f"{path}: title is {len(meta['title'])} tekens (max 70)")
        if not 70 <= len(meta["desc"]) <= 160: errors.append(f"{path}: desc is {len(meta['desc'])} tekens (70–160)")
        if not os.path.exists("assets/" + meta["img"]): errors.append(f"{path}: afbeelding assets/{meta['img']} bestaat niet")
        body = meta["body"]
        if body.count("<h2>") < 3: errors.append(f"{path}: minimaal 3 <h2>-tussenkoppen nodig")
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        if words < 350: errors.append(f"{path}: artikel is {words} woorden (minimaal 350)")
        if meta["date"] >= STRICT_FROM:
            if 'class="tldr"' not in body: errors.append(f"{path}: blok <div class=\"tldr\"> (Kort antwoord) ontbreekt")
            if body.count("<details>") < 3: errors.append(f"{path}: minimaal 3 FAQ-vragen (<details>) nodig")
            if not re.search(r'href="https?://(?!www\.skylinedigital\.nl)', body): errors.append(f"{path}: minimaal 1 externe bron (link) nodig")
            if len(meta["title"]) > 60: errors.append(f"{path}: title is {len(meta['title'])} tekens (max 60 voor nieuwe artikelen)")
        links = re.findall(r'href="(/[^"#?]*)', body)
        if len(links) < 3: errors.append(f"{path}: minimaal 3 interne links nodig")
        for l in links:
            target = "index.html" if l == "/" else l.strip("/") + ".html"
            if not os.path.exists(target) and not os.path.exists(l.strip("/") + "/index.html") and not any(l == "/kennisbank/" + a2 for a2 in [os.path.basename(x)[11:-5] for x in glob.glob("content/kennisbank/*.html")]):
                errors.append(f"{path}: interne link {l} bestaat niet")
        arts.append(meta)
    slugs = [a["slug"] for a in arts]
    for s_ in set(slugs):
        if slugs.count(s_) > 1: errors.append(f"slug '{s_}' komt dubbel voor")
    if errors:
        raise SystemExit("Kennisbank-controle mislukt:\n  - " + "\n  - ".join(errors))
    return sorted(arts, key=lambda a: (a["date"], a["slug"]), reverse=True)

ARTICLES = load_articles()
AUTHOR = {"@type":"Person","@id":BASE+"/over-ons#yannick","name":"Yannick van den Broek","jobTitle":"Oprichter Skyline Digital",
          "worksFor":{"@id":BASE+"/#organization"},"url":BASE+"/over-ons"}
MONTHS = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]
def nl_date(d): y, m, dd = d.split("-"); return f"{int(dd)} {MONTHS[int(m)-1]} {y}"

def head(title, desc, url, og, ld, extra=""):
    t = html.escape(title, quote=True); d = html.escape(desc, quote=True)
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t}</title>
  <meta name="description" content="{d}" />
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="{'article' if '/kennisbank/' in url else 'website'}" />
  <meta property="og:locale" content="nl_NL" />
  <meta property="og:site_name" content="Skyline Digital" />
  <meta property="og:title" content="{t}" />
  <meta property="og:description" content="{d}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{BASE}{og}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{t}" />
  <meta name="twitter:description" content="{d}" />
  <meta name="twitter:image" content="{BASE}{og}" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",",":"))}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400..900&family=Inter:wght@400..700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <link rel="stylesheet" href="/pages.css" />
  <link rel="stylesheet" href="/awards.css" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/assets/favicon.svg" />
  <meta name="theme-color" content="#07080b" />{extra}
</head>
<body>
'''
ORG_REF = {"@id": BASE + "/#organization"}
def crumbs_ld(url, items):
    lst = [{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"}]
    for i,(n,u) in enumerate(items, 2): lst.append({"@type":"ListItem","position":i,"name":n,"item":u})
    return {"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":lst}
def faq_ld(url, faqs):
    return {"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r'<[^>]+>','',a)}} for q,a in faqs]}
def faq_html(faqs):
    return '<div class="faq reveal">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs) + '</div>'
def tail():
    return FOOTER + '\n  <script src="/scroll-cinematic.js"></script>\n</body>\n</html>\n'
def rows(items):
    out = '<div class="rows">'
    for i,(h,p) in enumerate(items,1):
        out += f'<div class="row reveal"><span class="row-num">{i:02d}</span><div class="row-body"><h3>{h}</h3><p>{p}</p></div>{ARROW}</div>'
    return out + '</div>'

# ---------- Locatiepagina's ----------
for c in CITIES:
    slug = f"website-laten-maken-{c['slug']}"; url = f"{BASE}/{slug}"
    title = f"Website laten maken {c['name']} — vanaf €499 | Skyline Digital"
    desc = f"Website laten maken {c['in_']}? Skyline Digital bouwt snelle maatwerk websites vanaf €499 voor ondernemers in {c['full']} en omgeving. SEO inbegrepen. Vraag gratis een testwebsite aan."
    near = [CITY_BY[n] for n in c["near"]]
    faqs = [
      (f"Wat kost een website laten maken {c['in_']}?", f"Een maatwerk multipage website kost bij ons €499 eenmalig, een 3D cinematic website €749. SEO is optioneel voor €39 per maand. Die prijzen gelden voor ondernemers {c['in_']} net zo goed als in de rest van Nederland — bekijk de <a href=\"/pricing\" style=\"color:var(--gold-deep)\">prijzen</a>."),
      (f"Komen jullie langs {c['in_']}?", f"Ja. {c['travel']} De kennismaking doen we op jouw locatie, bij ons in Den Bosch of via een videogesprek — wat jij prettig vindt."),
      (f"Hoe word ik beter gevonden in Google {c['in_']}?", f"Door een snelle site met goede teksten, een volledig Google Bedrijfsprofiel, reviews en een pagina die specifiek over {c['full']} gaat. Dat zetten we bij de bouw meteen goed; met het SEO-abonnement houden we het daarna bij."),
      ("Hoe lang duurt het?", "Een multipage website staat meestal binnen twee tot vier weken online, afhankelijk van hoe snel we teksten en beeld ontvangen. Een gratis testwebsite laten we je vaak al binnen een paar dagen zien."),
    ]
    ld = {"@context":"https://schema.org","@graph":[
        crumbs_ld(url, [("Regio's", BASE+"/regio"), (f"Website laten maken {c['name']}", url)]),
        {"@type":"Service","@id":url+"#service","name":f"Website laten maken {c['in_']}","serviceType":"Webdesign en websiteontwikkeling","provider":ORG_REF,
         "areaServed":{"@type":"City","name":c["full"],"containedInPlace":{"@type":"AdministrativeArea","name":c["region"]}},"url":url,
         "offers":[{"@type":"Offer","name":"Multipage website","price":"499","priceCurrency":"EUR"},{"@type":"Offer","name":"3D Cinematic website","price":"749","priceCurrency":"EUR"}]},
        faq_ld(url, faqs),
        {"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"about":ORG_REF,"breadcrumb":{"@id":url+"#breadcrumb"}}]}
    sectors = "".join(f"<li>{s[0].upper()+s[1:]}</li>" for s in c["sectors"])
    nearlinks = ", ".join(f'<a href="/website-laten-maken-{n["slug"]}">{n["name"]}</a>' for n in near)
    body = HEADER + f'''
  <section class="page-hero has-image">
    <div class="page-hero-bg"><img src="/assets/photo-laptop-desk.jpg" alt="Website laten maken {c['in_']} — Skyline Digital" /></div>
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · <a href="/regio">Regio's</a> · {c['name']}</p>
      <h1>Website laten maken <span class="gold-text">{c['in_']}.</span></h1>
      <p class="lead">Maatwerk websites vanaf €499 voor ondernemers in {c['full']} en omgeving. Snel, vindbaar in Google en gebouwd om klanten op te leveren — door een bureau uit Den Bosch.</p>
      <div class="hero-actions"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite</a><a href="/portfolio" class="btn btn-ghost-light">Bekijk ons werk</a></div>
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="frow">
        <div class="frow-media reveal reveal--left"><div class="media-frame"><img src="/assets/photo-sketch.jpg" alt="Ontwerpschets van een website voor een ondernemer {c['in_']}" loading="lazy" /></div></div>
        <div class="frow-copy reveal reveal--right">
          <div class="gold-rule"></div>
          <p class="eyebrow">Webdesign {c['name']}</p>
          <h2>Een website die past bij <span class="gold-text">{c['full']}.</span></h2>
          <p class="lead">{c['intro']}</p>
          <p>{c['intro2']}</p>
          <a href="/aanvraag" class="btn btn-dark">Start je project</a>
        </div>
      </div>
    </div>
  </section>

  <section class="bg-dark full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Voor wie</p>
        <h2>Websites voor ondernemers <span class="gold-text">{c['in_']}</span></h2>
        <p class="lead">We bouwen voor allerlei sectoren in {c['full']}, onder andere voor:</p>
      </div>
      <ul class="checks" style="max-width:720px">{sectors}</ul>
      <p style="margin-top:28px;max-width:720px;color:var(--on-dark-dim)">Klanten uit {c['places']} vinden je via Google — en via een site die op elke telefoon snel laadt.</p>
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Wat je krijgt</p>
        <h2>Alles wat een website <span class="gold-text">moet kunnen.</span></h2>
      </div>
      {rows([
        ("Maatwerk ontwerp", f"Geen template: een ontwerp rond jouw merk en jouw klanten {c['in_']}."),
        ("Razendsnel en mobiel-first", "Groene PageSpeed-scores op mobiel — goed voor bezoekers én voor Google."),
        ("Lokale SEO ingebouwd", f"Titels, teksten, structured data en een Google Bedrijfsprofiel-koppeling gericht op {c['full']}."),
        ("Zelf te beheren", "Een eenvoudig CMS plus uitleg, zodat je teksten en foto's zelf aanpast."),
        ("Beeld en video", "Optioneel eigen foto-, video- en drone-opnames op jouw locatie, of AI-content in jouw stijl."),
        ("Eén aanspreekpunt", "Van ontwerp tot oplevering één contactpersoon, korte lijnen en heldere prijzen."),
      ])}
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Veelgestelde vragen</p>
        <h2>Website laten maken {c['in_']}: <span class="gold-text">goed om te weten</span></h2>
      </div>
      {faq_html(faqs)}
      <p style="margin-top:40px;text-align:center;color:var(--ink-dim)">Ook actief in {nearlinks} · <a href="/regio">alle regio's</a></p>
    </div>
  </section>

  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Eerst zien, dan beslissen.</h2>
      <p class="lead">We bouwen gratis een testwebsite voor jouw bedrijf {c['in_']}. Bevalt het? Dan gaan we door. Zo niet, dan kost het je niets.</p>
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite aanvragen</a><a href="/contact" class="btn btn-ghost-light">Plan een gesprek</a></div>
    </div>
  </section>

'''
    open(slug + ".html", "w").write(head(title, desc, url, "/assets/photo-laptop-desk.jpg", ld) + body + tail())

# ---------- Regio-hub ----------
url = BASE + "/regio"; title = "Website laten maken in Brabant en omgeving — regio's | Skyline Digital"
desc = "Skyline Digital bouwt websites, video en content voor ondernemers in Den Bosch, Rosmalen, Vught, Oss, Eindhoven, Tilburg, Breda, Nijmegen, Waalwijk en Uden. Bekijk je regio."
ld = {"@context":"https://schema.org","@graph":[crumbs_ld(url,[("Regio's",url)]),
      {"@type":"ItemList","@id":url+"#list","itemListElement":[{"@type":"ListItem","position":i+1,"name":f"Website laten maken {c['name']}","url":f"{BASE}/website-laten-maken-{c['slug']}"} for i,c in enumerate(CITIES)]},
      {"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"breadcrumb":{"@id":url+"#breadcrumb"}}]}
body = HEADER + f'''
  <section class="page-hero center" style="background:radial-gradient(90% 100% at 50% 0%, #16171f, #07080c)">
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · Regio's</p>
      <h1>Actief in Den Bosch <span class="gold-text">en ver daarbuiten.</span></h1>
      <p class="lead">Ons kantoor staat in 's-Hertogenbosch. Van daaruit bouwen we websites, films en content voor ondernemers in heel Brabant, Gelderland en de rest van Nederland.</p>
    </div>
  </section>
  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Kies je plaats</p>
        <h2>Website laten maken <span class="gold-text">in jouw regio</span></h2>
      </div>
      {rows([(f'<a href="/website-laten-maken-{c["slug"]}" style="color:inherit;text-decoration:none">Website laten maken {c["name"]}</a>', c["intro"].split(". ")[0] + ".") for c in CITIES])}
      <p style="margin-top:40px;color:var(--ink-dim)">Staat jouw plaats er niet bij? We werken door heel Nederland en op afstand — <a href="/contact">neem contact op</a>.</p>
    </div>
  </section>
  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Zien hoe jouw bedrijf eruit kan zien?</h2>
      <p class="lead">Vraag een gratis testwebsite aan — je ziet eerst het resultaat, dan beslis je.</p>
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite</a><a href="/pricing" class="btn btn-ghost-light">Bekijk prijzen</a></div>
    </div>
  </section>

'''
open("regio.html","w").write(head(title, desc, url, "/assets/og-home.jpg", ld) + body + tail())

# ---------- Kennisbank ----------
os.makedirs("kennisbank", exist_ok=True)
for a in ARTICLES:
    url = f"{BASE}/kennisbank/{a['slug']}"; og = f"/assets/{a['img']}"
    ld = {"@context":"https://schema.org","@graph":[
        crumbs_ld(url, [("Kennisbank", BASE+"/kennisbank"), (a["title"], url)]),
        {"@type":"Article","@id":url+"#article","headline":a["title"],"description":a["desc"],"image":BASE+og,"datePublished":a["date"],"dateModified":a.get("updated") or a["date"],
         "author":AUTHOR,"publisher":ORG_REF,"mainEntityOfPage":url,"inLanguage":"nl-NL"},
        {"@type":"WebPage","@id":url+"#webpage","url":url,"name":a["title"],"description":a["desc"],"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"breadcrumb":{"@id":url+"#breadcrumb"}}]}
    faqs = [(html.unescape(re.sub(r"<[^>]+>", "", q)).strip(), html.unescape(re.sub(r"<[^>]+>", "", an)).strip())
            for q, an in re.findall(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", a["body"], re.S)]
    if faqs: ld["@graph"].insert(-1, {"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":an}} for q, an in faqs]})
    others = [o for o in ARTICLES if o is not a][:3]
    body = HEADER + f'''
  <section class="page-hero has-image">
    <div class="page-hero-bg"><img src="{og}" alt="{html.escape(a['title'])}" /></div>
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · <a href="/kennisbank">Kennisbank</a> · {a['eyebrow']}</p>
      <h1>{a['title']}</h1>
      <p class="lead">{a['eyebrow']} · {nl_date(a['date'])} · {a['read']} leestijd · door Yannick van den Broek</p>
    </div>
  </section>
  <section class="bg-white full">
    <div class="wrap-sm">
      <article class="article">
{a['body']}
      </article>
      <aside class="author-box">
        <img src="/assets/logo.png" alt="Skyline Digital" />
        <div>
          <p class="author-name">Yannick van den Broek <span>· oprichter Skyline Digital</span></p>
          <p>Bouwt maatwerk websites en maakt bedrijfs-, villa- en dronefilms vanuit 's-Hertogenbosch. Gepubliceerd {nl_date(a['date'])}{(' · bijgewerkt ' + nl_date(a['updated'])) if a.get('updated') else ''}.</p>
          <p class="author-note">Dit artikel is geschreven met hulp van AI, op basis van onze eigen werkwijze, prijzen en projecten. Cijfers en regels zijn gecontroleerd aan de hand van de genoemde bronnen.</p>
        </div>
      </aside>
      <div class="article-more">
        <h2>Verder lezen</h2>
        {rows([(f'<a href="/kennisbank/{o["slug"]}" style="color:inherit;text-decoration:none">{o["title"]}</a>', o["desc"]) for o in others])}
      </div>
    </div>
  </section>
  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Liever gewoon zien wat het oplevert?</h2>
      <p class="lead">Vraag een gratis testwebsite aan of plan een vrijblijvend gesprek.</p>
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite</a><a href="/contact" class="btn btn-ghost-light">Plan een gesprek</a></div>
    </div>
  </section>

'''
    page = head(a["title"] + " | Skyline Digital", a["desc"], url, og, ld) + body + tail()
    page = page.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    open(f"kennisbank/{a['slug']}.html","w").write(page)

url = BASE + "/kennisbank"; title = "Kennisbank: websites, SEO, video & content | Skyline Digital"
desc = "Praktische artikelen over website laten maken, kosten, lokale SEO, drone video en cinematic webdesign — geschreven door Skyline Digital uit Den Bosch."
ld = {"@context":"https://schema.org","@graph":[crumbs_ld(url,[("Kennisbank",url)]),
      {"@type":"CollectionPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"breadcrumb":{"@id":url+"#breadcrumb"},
       "hasPart":[{"@type":"Article","headline":a["title"],"url":f"{BASE}/kennisbank/{a['slug']}"} for a in ARTICLES]}]}
body = HEADER + f'''
  <section class="page-hero center" style="background:radial-gradient(90% 100% at 50% 0%, #16171f, #07080c)">
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · Kennisbank</p>
      <h1>Kennis die je <span class="gold-text">verder helpt.</span></h1>
      <p class="lead">Eerlijke artikelen over websites, prijzen, SEO en video — zonder verkooppraat, met de cijfers erbij.</p>
    </div>
  </section>
  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Artikelen</p>
        <h2>Lees <span class="gold-text">verder</span></h2>
      </div>
      {rows([(f'<a href="/kennisbank/{a["slug"]}" style="color:inherit;text-decoration:none">{a["title"]}</a>', nl_date(a["date"]) + " · " + a["desc"]) for a in ARTICLES])}
    </div>
  </section>
  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Vragen over jouw situatie?</h2>
      <p class="lead">Plan een gratis adviesgesprek — we denken graag mee.</p>
      <div class="hero-actions hero-actions-center"><a href="/contact" class="btn btn-gold">Plan een gesprek</a><a href="/pricing" class="btn btn-ghost-light">Bekijk prijzen</a></div>
    </div>
  </section>

'''
open("kennisbank.html","w").write(head(title, desc, url, "/assets/og-home.jpg", ld) + body + tail())

# ---------- Footer op alle pagina's: Regio's + Kennisbank ----------
NEW_COL = '''        <div class="footer-col">
          <h4>Regio's</h4>
''' + "".join(f'          <a href="/website-laten-maken-{c["slug"]}">Website laten maken {c["name"]}</a>\n' for c in CITIES[:8]) + '''          <a href="/regio">Alle regio's</a>
        </div>
'''
for path in glob.glob("*.html") + glob.glob("kennisbank/*.html"):
    if path.startswith("google"): continue
    s = open(path).read()
    if "Website laten maken Den Bosch</a>" in s: continue
    s = re.sub(r'        <div class="footer-col">\n          <h4>Over ons</h4>.*?</div>\n', NEW_COL, s, count=1, flags=re.S)
    s = s.replace('          <a href="/aanvraag" class="footer-gratis">★ Gratis testwebsite</a>', '          <a href="/kennisbank">Kennisbank</a>\n          <a href="/aanvraag" class="footer-gratis">★ Gratis testwebsite</a>', 1)
    # relatieve assets in footer/nav werken niet vanuit /kennisbank/ — maak ze absoluut
    if path.startswith("kennisbank/"):
        s = s.replace('src="assets/', 'src="/assets/')
    open(path, "w").write(s)

# ---------- Sitemap ----------
urls = [("/",1.0,"weekly"),("/website-seo",0.9,"monthly"),("/drone-video",0.9,"monthly"),("/social-media",0.9,"monthly"),("/ai-content",0.9,"monthly"),
        ("/pricing",0.8,"monthly"),("/portfolio",0.8,"monthly"),("/over-ons",0.7,"monthly"),("/contact",0.7,"yearly"),("/aanvraag",0.8,"yearly"),
        ("/regio",0.7,"monthly"),("/kennisbank",0.7,"weekly")]
urls += [(f"/website-laten-maken-{c['slug']}",0.8,"monthly") for c in CITIES]
urls += [(f"/kennisbank/{a['slug']}",0.7,"monthly",a["date"]) for a in ARTICLES]
W = ["dekgro","lillis","bodyscan","echtgrieks","carslease","lassie","dejonge","elektropost","palmyra"]
urls += [(f"/werk-{w}",0.5,"yearly") for w in W]
MAIN = ["","/over-ons","/website-seo","/drone-video","/social-media","/ai-content","/portfolio","/pricing","/contact","/aanvraag"]
for l in ["en","it","es"]:
    urls += [(f"/{l}{m}", 0.8 if m == "" else 0.6, "monthly") for m in MAIN]
    urls += [(f"/{l}/werk-{w}", 0.4, "yearly") for w in W]
urls += [("/privacybeleid",0.2,"yearly"),("/algemene-voorwaarden",0.2,"yearly"),("/cookiebeleid",0.2,"yearly")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for entry in urls:
    u, p, f = entry[:3]; lm = entry[3] if len(entry) > 3 else (max(a["date"] for a in ARTICLES) if u == "/kennisbank" else TODAY)
    sm += f'  <url><loc>{BASE}{u}</loc><lastmod>{lm}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority></url>\n'
open("sitemap.xml","w").write(sm + "</urlset>\n")
print("pages:", len(CITIES)+len(ARTICLES)+2, "sitemap urls:", len(urls))

# Google-tag (GA4 + toestemmingsmodus) op alle pagina's, ook de zojuist gegenereerde
import subprocess, sys
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_ga.py")], check=True)
