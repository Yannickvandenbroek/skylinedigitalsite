import re, json, os, hashlib, sys
from bs4 import BeautifulSoup, NavigableString, Comment
os.chdir("/Users/yannickvandenbroek/Documents/Skylinedigital/own site/skyline-digital")
BASE = "https://www.skylinedigital.nl"
PAGES = ["index","over-ons","website-seo","drone-video","social-media","ai-content","portfolio","pricing","contact","aanvraag","video","werk-dekgro","werk-lillis","werk-bodyscan","werk-echtgrieks","werk-carslease","werk-lassie","werk-dejonge","werk-elektropost","werk-palmyra"]
LANGS = [l for l in sys.argv[1:]] or ["en","it","es"]
LOCALE = {"en":"en-GB","it":"it-IT","es":"es-ES","nl":"nl-NL","xx":"xx-XX"}
INLINE = {"span","a","strong","em","b","i","br","small","svg","img","sup","sub","code","u","mark","abbr","time"}
SKIP = {"script","style","noscript","svg","head","title"}
ATTRS = ["alt","placeholder","aria-label","title","data-label"]
JS_STRINGS = {"pricing": ['Korting (', "Kies je aantal video's en foto's.", 'Minimumbesteding €20 — voeg meer toe.', 'Klaar om aan te vragen.']}
src = json.load(open("i18n/source.json"))["segments"]
JS_TR = json.load(open("i18n/js.json")) if os.path.exists("i18n/js.json") else {}
def sid(s): return hashlib.md5(s.encode()).hexdigest()[:10]
def path_of(lang, slug):
    p = "/" if slug == "index" else f"/{slug}"
    return p if lang == "nl" else (f"/{lang}" if slug == "index" else f"/{lang}/{slug}")
def alt_script(slug):
    alts = {l: path_of(l, slug) for l in ["nl"] + ["en","it","es"]}
    return '<script>window.SKY_ALT=' + json.dumps(alts) + '</script>'
def hreflangs(slug):
    out = ""
    for l in ["nl","en","it","es"]:
        out += f'\n  <link rel="alternate" hreflang="{l}" href="{BASE}{path_of(l, slug)}" />'
    out += f'\n  <link rel="alternate" hreflang="x-default" href="{BASE}{path_of("nl", slug)}" />'
    return out

def translate_soup(soup, tr):
    t = soup.find("title")
    if t:
        k = sid(t.get_text().strip())
        if k in tr: t.string = BeautifulSoup(tr[k], "html.parser").get_text()
    for m in soup.find_all("meta"):
        c = m.get("content", "")
        if c and sid(c.strip()) in tr: m["content"] = BeautifulSoup(tr[sid(c.strip())], "html.parser").get_text()
    for el in list(soup.body.descendants):
        if not hasattr(el, "name") or el.name is None: continue
        if el.name in SKIP or el.find_parent(list(SKIP - {"head","title"})): continue
        for a in ATTRS:
            if el.get(a) and sid(el[a].strip()) in tr: el[a] = BeautifulSoup(tr[sid(el[a].strip())], "html.parser").get_text()
        if el.get("class") and "notranslate" in el.get("class"): continue
        kids = list(el.children)
        has_text = any(isinstance(k, NavigableString) and not isinstance(k, Comment) and k.strip() for k in kids)
        only_inline = all((isinstance(k, NavigableString)) or (k.name in INLINE) for k in kids)
        if has_text and only_inline:
            inner = re.sub(r'\s+', ' ', el.decode_contents()).strip()
            k = sid(inner)
            if k in tr:
                el.clear(); el.append(BeautifulSoup(tr[k], "html.parser"))

def localize_links(soup, lang):
    for a in soup.find_all("a", href=True):
        h = a["href"]
        if not h.startswith("/") or h.startswith("//"): continue
        m = re.match(r'^/([a-z0-9-]*)(\?[^#]*)?(#.*)?$', h)
        if not m: continue
        slug = m.group(1) or "index"
        if slug in PAGES:
            a["href"] = path_of(lang, slug) + (m.group(2) or "") + (m.group(3) or "")

def fix_ld(s, lang, slug, soup):
    def repl(m):
        try: d = json.loads(m.group(1))
        except Exception: return m.group(0)
        url_nl = BASE + path_of("nl", slug); url = BASE + path_of(lang, slug)
        txt = json.dumps(d, ensure_ascii=False)
        txt = txt.replace(url_nl + "#", url + "#").replace('"url": "' + url_nl + '"', '"url": "' + url + '"').replace('"item": "' + url_nl + '"', '"item": "' + url + '"')
        d = json.loads(txt)
        title = soup.find("title").get_text() if soup.find("title") else ""
        desc = (soup.find("meta", attrs={"name":"description"}) or {}).get("content", "")
        faqs = []
        for det in soup.select("details"):
            q = det.find("summary"); p = det.find("p")
            if q and p: faqs.append({"@type":"Question","name":q.get_text(" ", strip=True),"acceptedAnswer":{"@type":"Answer","text":p.get_text(" ", strip=True)}})
        for g in d.get("@graph", []):
            t = g.get("@type")
            if t in ("WebPage", ["WebPage","ItemPage"]) or (isinstance(t, list) and "WebPage" in t):
                g["inLanguage"] = LOCALE[lang]; g["name"] = title; g["description"] = desc; g["url"] = url
                g["@id"] = url + "#webpage"
            if t == "FAQPage" and faqs: g["mainEntity"] = faqs
            if t == "CreativeWork":
                lead = soup.select_one(".case-info .lead")
                if lead: g["about"] = lead.get_text(" ", strip=True)
            if t == "BreadcrumbList":
                for it in g.get("itemListElement", []):
                    if it.get("position") == 1: it["item"] = BASE + path_of(lang, "index"); it["name"] = {"en":"Home","it":"Home","es":"Inicio"}.get(lang,"Home")
        return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, separators=(",",":")) + '</script>'
    return re.sub(r'<script type="application/ld\+json">(.*?)</script>', repl, s, count=1, flags=re.S)

def absolutize(s):
    s = re.sub(r'(src|href)="(assets/|frames/|styles\.css|pages\.css|awards\.css|scroll-cinematic\.js|films\.js)', r'\1="/\2', s)
    s = s.replace("'assets/", "'/assets/").replace('"assets/', '"/assets/').replace("`frames/", "`/frames/").replace("'frames/", "'/frames/")
    return s

# --- NL-pagina's: hreflang + SKY_ALT toevoegen ---
for slug in PAGES:
    p = slug + ".html"; s = open(p).read()
    s = re.sub(r'\n  <link rel="alternate" hreflang="[^"]*" href="[^"]*" />', '', s)
    s = re.sub(r'<script>window\.SKY_ALT=.*?</script>\n?', '', s)
    s = s.replace('<link rel="canonical" href="' + BASE + path_of("nl", slug) + '" />', '<link rel="canonical" href="' + BASE + path_of("nl", slug) + '" />' + hreflangs(slug), 1)
    s = s.replace('</head>', '  ' + alt_script(slug) + '\n</head>', 1)
    open(p, "w").write(s)

for lang in LANGS:
    tr = json.load(open(f"i18n/{lang}.json"))
    os.makedirs(lang, exist_ok=True)
    for slug in PAGES:
        raw = open(slug + ".html").read()
        soup = BeautifulSoup(raw, "html.parser")
        translate_soup(soup, tr)
        localize_links(soup, lang)
        soup.html["lang"] = lang
        can = soup.find("link", rel="canonical")
        if can: can["href"] = BASE + path_of(lang, slug)
        for m in soup.find_all("meta", property="og:url"): m["content"] = BASE + path_of(lang, slug)
        for m in soup.find_all("meta", property="og:locale"): m["content"] = LOCALE[lang].replace("-", "_")
        for l in soup.find_all("link", rel="alternate"): l.decompose()
        sc = soup.find("script", string=re.compile(r"window\.SKY_ALT"))
        if sc: sc.decompose()
        out = str(soup)
        out = re.sub(r'(<link[^>]*rel="canonical"[^>]*/>)', lambda m: m.group(1) + hreflangs(slug), out, count=1)
        out = out.replace('</head>', '  ' + alt_script(slug) + '\n</head>', 1)
        out = fix_ld(out, lang, slug, soup)
        out = absolutize(out)
        for js in JS_STRINGS.get(slug, []):
            if sid(js) in tr: out = out.replace(js, BeautifulSoup(tr[sid(js)], "html.parser").get_text())
        for nl_js, tr_js in JS_TR.get(lang, {}).items(): out = out.replace(nl_js, tr_js)
        # projectlinks in de carrousel-scripts naar de vertaalde projectpagina's
        out = re.sub(r"href: '/(werk-[a-z]+)'", lambda m: f"href: '/{lang}/{m.group(1)}'", out)
        open(f"{lang}/{slug}.html", "w").write(out)
    print(lang, "ok")
