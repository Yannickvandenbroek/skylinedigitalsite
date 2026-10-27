"""Bouwt de Spaanse site op www.skylinedigital.es (map es-site/, eigen Vercel-project met die map als root).
De vertaalde hoofdpagina's komen uit tools/i18n_build.py; dit script maakt de rest: Vercel-instellingen,
robots.txt, IndexNow-sleutel en sitemap. Afbeeldingen, css en js staan op de .nl en worden daar volledig naar gelinkt.
Gebruik: python3 tools/i18n_build.py && python3 tools/gen_es.py"""
import os, glob, json, shutil, datetime

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
ES_BASE = "https://www.skylinedigital.es"
DIR = "es-site"
os.makedirs(DIR, exist_ok=True)

# ---------- Vercel: schone adressen, kaal domein naar www, dezelfde headers als de .nl ----------
vercel = {
    "cleanUrls": True,
    "trailingSlash": False,
    "redirects": [
        {"source": "/:path*", "has": [{"type": "host", "value": "skylinedigital.es"}], "destination": ES_BASE + "/:path*", "permanent": True},
    ],
    "headers": [
        {"source": "/(.*)", "headers": [
            {"key": "X-Content-Type-Options", "value": "nosniff"},
            {"key": "X-Frame-Options", "value": "SAMEORIGIN"},
            {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
            {"key": "Permissions-Policy", "value": "camera=(), microphone=(), geolocation=()"},
        ]},
    ],
}
open(f"{DIR}/vercel.json", "w").write(json.dumps(vercel, indent=2, ensure_ascii=False) + "\n")
open(f"{DIR}/robots.txt", "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {ES_BASE}/sitemap.xml\n")
for key in glob.glob("[0-9a-f]" * 32 + ".txt"):  # IndexNow-sleutel moet ook op dit domein staan
    shutil.copy(key, f"{DIR}/{key}")

# ---------- Sitemap ----------
today = datetime.date.today().isoformat()
pages = sorted(os.path.basename(p)[:-5] for p in glob.glob(f"{DIR}/*.html") if not p.endswith("404.html"))
def prio(slug):
    if slug == "index": return "1.0"
    if slug.startswith("proyecto-"): return "0.5"
    return "0.8"
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for slug in pages:
    loc = ES_BASE + ("/" if slug == "index" else f"/{slug}")
    sm += f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod><priority>{prio(slug)}</priority></url>\n"
open(f"{DIR}/sitemap.xml", "w").write(sm + "</urlset>\n")
print("es-site:", len(pages), "pagina's in sitemap")
