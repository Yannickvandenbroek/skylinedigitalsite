import re, json, os, hashlib
from bs4 import BeautifulSoup, NavigableString, Comment
os.chdir("/Users/yannickvandenbroek/Documents/Skylinedigital/own site/skyline-digital")
PAGES = ["index","over-ons","website-seo","drone-video","social-media","ai-content","portfolio","pricing","contact","aanvraag","video","404"]
INLINE = {"span","a","strong","em","b","i","br","small","svg","img","sup","sub","code","u","mark","abbr","time"}
SKIP = {"script","style","noscript","svg","head","title"}
ATTRS = ["alt","placeholder","aria-label","title","data-label"]
JS_STRINGS = {
 "pricing": ['Korting (', 'Kies je aantal video\'s en foto\'s.', 'Minimumbesteding €20 — voeg meer toe.', 'Klaar om aan te vragen.'],
}
segs = {}      # id -> source html
pages = {}     # page -> [ids]
def sid(s): return hashlib.md5(s.encode()).hexdigest()[:10]
def add(page, s):
    s = s.strip()
    if not s or not re.search(r'[A-Za-zÀ-ÿ]', s): return
    if re.fullmatch(r'[\d\s€%+.,:/–—·|()x-]+', s): return
    k = sid(s); segs[k] = s; pages[page].append(k)
for p in PAGES:
    pages[p] = []
    soup = BeautifulSoup(open(p + ".html").read(), "html.parser")
    t = soup.find("title")
    if t: add(p, t.get_text())
    for m in soup.find_all("meta"):
        if m.get("name") in ("description","twitter:title","twitter:description") or (m.get("property") or "").startswith("og:") and m.get("property") in ("og:title","og:description"):
            add(p, m.get("content",""))
    for el in soup.body.descendants if soup.body else []:
        if not hasattr(el, "name") or el.name is None: continue
        if el.name in SKIP or el.find_parent(list(SKIP - {"head","title"})): continue
        for a in ATTRS:
            if el.get(a): add(p, el[a])
        if el.get("class") and "notranslate" in el.get("class"): continue
        kids = list(el.children)
        has_text = any(isinstance(k, NavigableString) and not isinstance(k, Comment) and k.strip() for k in kids)
        only_inline = all((isinstance(k, NavigableString)) or (k.name in INLINE) for k in kids)
        if has_text and only_inline:
            inner = el.decode_contents()
            inner = re.sub(r'\s+', ' ', inner).strip()
            # sla over als een voorouder al als segment is meegenomen (gebeurt niet bij inline-only check, maar voor de zekerheid)
            add(p, inner)
    for s in JS_STRINGS.get(p, []): add(p, s)
os.makedirs("i18n", exist_ok=True)
json.dump({"segments": segs, "pages": pages}, open("i18n/source.json","w"), ensure_ascii=False, indent=1)
words = sum(len(re.sub(r'<[^>]+>',' ',v).split()) for v in segs.values())
print("segments:", len(segs), "words:", words)
for p in PAGES: print(p, len(pages[p]))
