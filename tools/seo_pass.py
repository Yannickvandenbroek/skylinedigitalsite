import re, glob, html, json, os
os.chdir("/Users/yannickvandenbroek/Documents/Skylinedigital/own site/skyline-digital")
BASE = "https://skylinedigital.nl"

META = {
 "index": ("Website laten maken in Den Bosch | Skyline Digital",
           "Website laten maken? Skyline Digital in 's-Hertogenbosch bouwt snelle maatwerk websites vanaf €499, cinematische video's en drone-opnames. Vraag gratis een testwebsite aan.",
           "/assets/og-home.jpg"),
 "over-ons": ("Over Skyline Digital — creatief bureau in 's-Hertogenbosch",
           "Skyline Digital is een creatief digitaal bureau uit 's-Hertogenbosch voor websites, SEO, video, drone en AI-content. Eén team, één aanspreekpunt. Leer ons kennen.",
           "/assets/photo-studio-loft.jpg"),
 "website-seo": ("Website laten maken & SEO — vanaf €499 | Skyline Digital",
           "Maatwerk website laten maken vanaf €499, razendsnel en SEO-vriendelijk gebouwd. SEO-abonnement vanaf €39 per maand. Bureau in Den Bosch, actief in heel Nederland.",
           "/assets/photo-laptop-desk.jpg"),
 "drone-video": ("Drone & bedrijfsvideo laten maken in Den Bosch | Skyline Digital",
           "Cinematische bedrijfsfilms, villa-films en drone-opnames vanaf €250 per shoot. Gecertificeerde dronepiloot, professionele montage. Skyline Digital, 's-Hertogenbosch.",
           "/assets/photo-drone-villa.jpg"),
 "social-media": ("Social media beheer & content vanaf €79 p/m | Skyline Digital",
           "Social media beheer, contentcreatie en reels vanaf €79 per maand. Strategie, productie en publicatie in jouw huisstijl. Skyline Digital, Den Bosch.",
           "/assets/photo-flatlay-phone.jpg"),
 "ai-content": ("AI content laten maken: video's & foto's | Skyline Digital",
           "AI-video's vanaf €15 en AI-foto's vanaf €3 per stuk, altijd met menselijke eindcontrole. Meer content in minder tijd, in jouw stijl. Skyline Digital, Den Bosch.",
           "/assets/photo-edit-suite.jpg"),
 "pricing": ("Prijzen: website vanaf €499, video, social & AI | Skyline Digital",
           "Transparante prijzen: multipage website €499, 3D cinematic website €749, SEO €39 p/m, video-shoot €250, social media vanaf €79 p/m. Geen verborgen kosten.",
           "/assets/photo-handshake.jpg"),
 "portfolio": ("Portfolio — websites & cinematische villa-films | Skyline Digital",
           "Bekijk ons werk: maatwerk websites voor o.a. Dekgro, CarsLease en Lassie, en cinematische villa-films in Moraira en Jávea. Skyline Digital, Den Bosch.",
           "/assets/work-dekgro.jpg"),
 "contact": ("Contact — gratis adviesgesprek | Skyline Digital Den Bosch",
           "Neem contact op met Skyline Digital in 's-Hertogenbosch voor een gratis adviesgesprek over je website, video of content. Bel 06 86 85 02 89 of mail ons.",
           "/assets/photo-handshake.jpg"),
 "aanvraag": ("Gratis testwebsite aanvragen | Skyline Digital",
           "Vraag gratis een testwebsite aan: je ziet eerst het resultaat, dan beslis je. Of start direct je project voor website, video, social media of AI-content.",
           "/assets/photo-laptop-desk.jpg"),
 "privacybeleid": ("Privacybeleid | Skyline Digital", "Lees hoe Skyline Digital omgaat met je persoonsgegevens, cookies en je rechten volgens de AVG.", "/assets/og-home.jpg"),
 "algemene-voorwaarden": ("Algemene voorwaarden | Skyline Digital", "De algemene voorwaarden van Skyline Digital voor websites, video, social media en AI-content.", "/assets/og-home.jpg"),
 "cookiebeleid": ("Cookiebeleid | Skyline Digital", "Welke cookies Skyline Digital gebruikt, waarvoor en hoe je ze beheert.", "/assets/og-home.jpg"),
 "werk-dekgro": ("Website voor Tegeltechniek Dekgro — case | Skyline Digital", None, "/assets/work-dekgro.jpg"),
 "werk-lillis": ("Website voor Lilli's Schilderwerken — case | Skyline Digital", None, "/assets/work-lillis.jpg"),
 "werk-bodyscan": ("Website voor BodyScan Waalre — case | Skyline Digital", None, "/assets/work-bodyscan.jpg"),
 "werk-echtgrieks": ("Website voor Echt Grieks — case | Skyline Digital", None, "/assets/work-echtgrieks.jpg"),
 "video": ("Cinematische villa-film — gratis voorbeeld | Skyline Digital", None, "/assets/og-home.jpg"),
}
SERVICE = {
 "website-seo": ("Website laten maken & SEO", "Maatwerk websites en zoekmachineoptimalisatie"),
 "drone-video": ("Drone & bedrijfsvideo", "Cinematische bedrijfsfilms, villa-films en drone-opnames"),
 "social-media": ("Social media beheer & content", "Strategie, contentcreatie en beheer van social media"),
 "ai-content": ("AI content", "AI-gegenereerde video's en foto's met menselijke eindcontrole"),
}
BREAD = {
 "over-ons": "Over ons", "website-seo": "Website & SEO", "drone-video": "Drone & Video", "social-media": "Social Media",
 "ai-content": "AI Content", "pricing": "Pricing", "portfolio": "Portfolio", "contact": "Contact", "aanvraag": "Aanvraag",
 "privacybeleid": "Privacybeleid", "algemene-voorwaarden": "Algemene voorwaarden", "cookiebeleid": "Cookiebeleid",
}
ORG = {
 "@type": ["ProfessionalService","LocalBusiness"], "@id": BASE + "/#organization", "name": "Skyline Digital",
 "alternateName": "Skyline Digital Den Bosch", "url": BASE + "/", "logo": BASE + "/assets/logo.png", "image": BASE + "/assets/og-home.jpg",
 "description": "Creatief digitaal bureau in 's-Hertogenbosch voor maatwerk websites, SEO, cinematische video, drone-opnames, social media en AI-content.",
 "telephone": "+31686850289", "email": "yannick@skylinedigital.nl", "priceRange": "€€",
 "address": {"@type": "PostalAddress", "streetAddress": "Bruistensingel 500", "postalCode": "5232 AH", "addressLocality": "'s-Hertogenbosch", "addressRegion": "Noord-Brabant", "addressCountry": "NL"},
 "geo": {"@type": "GeoCoordinates", "latitude": 51.7044, "longitude": 5.3324},
 "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "09:00", "closes": "18:00"}],
 "areaServed": [{"@type": "Country", "name": "Nederland"}, {"@type": "City", "name": "'s-Hertogenbosch"}, {"@type": "City", "name": "Eindhoven"}, {"@type": "City", "name": "Tilburg"}, {"@type": "City", "name": "Breda"}, {"@type": "City", "name": "Oss"}, {"@type": "City", "name": "Nijmegen"}],
 "founder": {"@type": "Person", "name": "Yannick van den Broek"},
 "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Diensten", "itemListElement": [
   {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Multipage website", "url": BASE + "/website-seo"}, "price": "499", "priceCurrency": "EUR"},
   {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "3D Cinematic website", "url": BASE + "/website-seo"}, "price": "749", "priceCurrency": "EUR"},
   {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "SEO-abonnement", "url": BASE + "/website-seo"}, "price": "39", "priceCurrency": "EUR"},
   {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Video- en droneshoot", "url": BASE + "/drone-video"}, "price": "250", "priceCurrency": "EUR"},
   {"@type": "Offer", "itemOffered": {"@type": "Service", "name": "Social media beheer", "url": BASE + "/social-media"}, "price": "79", "priceCurrency": "EUR"},
 ]},
}
WEBSITE = {"@type": "WebSite", "@id": BASE + "/#website", "url": BASE + "/", "name": "Skyline Digital", "inLanguage": "nl-NL", "publisher": {"@id": BASE + "/#organization"}}

def clean_links(s):
    # interne links naar clean URLs (Vercel cleanUrls) — voorkomt een redirect per klik
    s = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1) or ""}"', s)
    s = re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"', lambda m: f'href="/{m.group(1)}{m.group(2) or ""}"', s)
    s = re.sub(r'href="(video)\?', r'href="/\1?', s)
    return s

def faq_items(s):
    out = []
    for m in re.finditer(r'<details>\s*<summary>(.*?)</summary>\s*<p>(.*?)</p>\s*</details>', s, re.S):
        q = html.unescape(re.sub(r'<[^>]+>', '', m.group(1))).strip()
        a = html.unescape(re.sub(r'<[^>]+>', '', m.group(2))).strip()
        out.append({"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}})
    return out

def h1_text(s):
    m = re.search(r'<h1[^>]*>(.*?)</h1>', s, re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', m.group(1))).replace("  ", " ").strip() if m else ""

for path in sorted(glob.glob("*.html")):
    slug = path[:-5]
    if slug.startswith("google"): continue
    s = open(path).read()
    orig = s
    s = clean_links(s)
    url = BASE + "/" if slug == "index" else f"{BASE}/{slug}"
    title, desc, og = META.get(slug, (None, None, "/assets/og-home.jpg"))
    if desc is None:
        m = re.search(r'<meta name="description" content="([^"]*)"', s); desc = m.group(1) if m else ""
    if title is None:
        m = re.search(r'<title>(.*?)</title>', s); title = m.group(1)
    t_esc = html.escape(title, quote=True); d_esc = html.escape(html.unescape(desc), quote=True)
    # strip bestaande head-SEO en zet een consistente blok terug
    s = re.sub(r'\s*<title>.*?</title>', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<meta name="description"[^>]*>', '', s)
    s = re.sub(r'\s*<link rel="canonical"[^>]*>', '', s)
    s = re.sub(r'\s*<meta (?:property|name)="(?:og:|twitter:)[^"]*"[^>]*>', '', s)
    s = re.sub(r'\s*<meta name="robots"[^>]*>', '', s)
    s = re.sub(r'\s*<script type="application/ld\+json">.*?</script>', '', s, flags=re.S)
    robots = "noindex,follow" if slug == "video" else "index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1"
    head = f'''
  <title>{t_esc}</title>
  <meta name="description" content="{d_esc}" />
  <meta name="robots" content="{robots}" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="website" />
  <meta property="og:locale" content="nl_NL" />
  <meta property="og:site_name" content="Skyline Digital" />
  <meta property="og:title" content="{t_esc}" />
  <meta property="og:description" content="{d_esc}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{BASE}{og}" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{t_esc}" />
  <meta name="twitter:description" content="{d_esc}" />
  <meta name="twitter:image" content="{BASE}{og}" />'''
    # JSON-LD graph
    graph = [ORG, WEBSITE]
    page = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": html.unescape(desc), "inLanguage": "nl-NL", "isPartOf": {"@id": BASE + "/#website"}, "about": {"@id": BASE + "/#organization"}, "primaryImageOfPage": BASE + og}
    if slug in BREAD or slug.startswith("werk-"):
        crumbs = [{"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"}]
        if slug.startswith("werk-"):
            crumbs.append({"@type": "ListItem", "position": 2, "name": "Portfolio", "item": BASE + "/portfolio"})
            crumbs.append({"@type": "ListItem", "position": 3, "name": h1_text(s) or title, "item": url})
        elif slug in SERVICE:
            crumbs.append({"@type": "ListItem", "position": 2, "name": "Diensten", "item": BASE + "/#diensten"})
            crumbs.append({"@type": "ListItem", "position": 3, "name": BREAD[slug], "item": url})
        else:
            crumbs.append({"@type": "ListItem", "position": 2, "name": BREAD[slug], "item": url})
        graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": crumbs})
        page["breadcrumb"] = {"@id": url + "#breadcrumb"}
    if slug in SERVICE:
        name, sd = SERVICE[slug]
        graph.append({"@type": "Service", "@id": url + "#service", "name": name, "description": sd, "url": url, "serviceType": name,
                      "provider": {"@id": BASE + "/#organization"}, "areaServed": {"@type": "Country", "name": "Nederland"}})
    if slug.startswith("werk-"):
        page["@type"] = ["WebPage", "ItemPage"]
    faqs = faq_items(s)
    if faqs:
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": faqs})
    graph.append(page)
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    head += f'\n  <script type="application/ld+json">{ld}</script>'
    # invoegen direct na viewport
    s = re.sub(r'(<meta name="viewport"[^>]*>)', lambda m: m.group(1) + head, s, count=1)
    open(path, "w").write(s)
    print(f"{path}: title={len(title)} desc={len(html.unescape(desc))} faq={len(faqs)} {'(links changed)' if clean_links(orig)!=orig else ''}")
