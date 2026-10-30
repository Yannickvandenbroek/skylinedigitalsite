"""Zet de Google-tag (GA4) met toestemmingsmodus v2 in de <head> van elke pagina en geeft gedeelde css/js een versie (?v=hash) tegen verouderde browsercache.
Idempotent: een bestaand blok wordt vervangen. Wordt ook gebruikt door gen_pages.py en gen_cases.py,
en de vertaalde pagina's erven het blok via i18n_build.py.
Gebruik: python3 tools/add_ga.py"""
import re, glob, os, hashlib

GA_ID = "G-39LM88JLSL"
START, END = "<!-- Google tag (gtag.js) -->", "<!-- /Google tag -->"
SNIPPET = f'''{START}
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    var skyConsentChoice = null; try {{ skyConsentChoice = localStorage.getItem('sky_consent'); }} catch (e) {{}}
    gtag('consent', 'default', {{ ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', analytics_storage: skyConsentChoice === 'granted' ? 'granted' : 'denied' }});
    gtag('js', new Date());
    gtag('config', '{GA_ID}', {{ cookie_expires: 34128000 }});
  </script>
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script src="/consent.js" defer></script>
  <script src="/lead.js" defer></script>
  {END}'''

# lead.js zit in hetzelfde blok (stuurt elk Formspree-formulier ook naar het CRM); los toevoegen
# verdween bij het opnieuw zetten van dit blok, zo blijft hij staan.
ASSETS = ["styles.css", "pages.css", "awards.css", "scroll-cinematic.js", "consent.js", "lead.js", "films.js", "instagram.js"]
def bust(html):
    # Zet ?v=<hash van de inhoud> achter gedeelde css/js, zodat browsers na een wijziging direct de nieuwe versie laden.
    for a in ASSETS:
        if not os.path.exists(a): continue
        v = hashlib.md5(open(a, "rb").read()).hexdigest()[:8]
        html = re.sub(r'((?:src|href)="(?:https://www\.skylinedigital\.nl)?/?)' + re.escape(a) + r'(?:\?v=[0-9a-f]+)?"', lambda m: f'{m.group(1)}{a}?v={v}"', html)
    return html

def inject(html, external=False):
    html = re.sub(r"\s*" + re.escape(START) + r".*?" + re.escape(END), "", html, flags=re.S)
    snip = SNIPPET.replace('src="/consent.js"', 'src="https://www.skylinedigital.nl/consent.js"').replace('src="/lead.js"', 'src="https://www.skylinedigital.nl/lead.js"') if external else SNIPPET
    return re.sub(r'(<meta charset="utf-8"\s*/?>)', lambda m: m.group(1) + "\n  " + snip, html, count=1, flags=re.I)

if __name__ == "__main__":
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    files = [f for f in glob.glob("*.html") + glob.glob("blog/*.html") + glob.glob("en/*.html") + glob.glob("it/*.html") + glob.glob("es-site/*.html")
             if not os.path.basename(f).startswith("google")]
    n = 0
    for f in files:
        s = open(f).read(); t = bust(inject(s, external=f.startswith("es-site/")))
        if GA_ID not in t: print("GEEN charset-meta in", f); continue
        if t != s: open(f, "w").write(t); n += 1
    print(f"Google-tag in {n} van {len(files)} pagina's gezet")
