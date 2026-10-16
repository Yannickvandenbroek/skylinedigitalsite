"""Meldt URL's direct aan bij Bing (en daarmee Copilot) en de andere IndexNow-zoekmachines.
Gebruik:  python3 tools/indexnow.py https://www.skylinedigital.nl/kennisbank/<slug> [meer URL's]
          python3 tools/indexnow.py --all     (alle URL's uit sitemap.xml)
De sleutel staat in /c2f7663f6653db1a6ea0e5012eaa9095.txt in de root van de site."""
import json, re, sys, os, urllib.request
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
KEY = "c2f7663f6653db1a6ea0e5012eaa9095"
HOST = "www.skylinedigital.nl"
urls = re.findall(r"<loc>([^<]+)</loc>", open("sitemap.xml").read()) if "--all" in sys.argv else [u for u in sys.argv[1:] if u.startswith("https://")]
if not urls: raise SystemExit("Geen URL's opgegeven")
body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=20) as r: print(f"IndexNow: {r.status} voor {len(urls)} URL('s)")
except urllib.error.HTTPError as e:
    print(f"IndexNow: HTTP {e.code} — {e.read()[:200]!r}"); sys.exit(1)
