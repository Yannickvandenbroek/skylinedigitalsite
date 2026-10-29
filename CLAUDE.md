# Skyline Digital website (skylinedigital.nl) — werkafspraken voor Claude

Statische site (HTML/CSS/JS, geen framework). Repo skylinedigitalsite; elke push naar `main` gaat via Vercel live op www.skylinedigital.nl. Nederlands, kort en concreet. Eigenaar: Yannick van den Broek (Den Bosch).

## Werkwijze
- Na een afgeronde en gecontroleerde wijziging direct committen en pushen, zonder te vragen (Yannicks afspraak). Zegt hij "niet pushen", dan stoppen.
- Tools in `tools/` (Python 3 + beautifulsoup4; zie `tools/README.md`): `gen_pages.py` (locatiepagina's, blog, sitemap), `gen_cases.py` (projectpagina's), `gen_reviews.py`, `seo_pass.py`, `indexnow.py`, `i18n_extract.py` + `i18n_build.py` (EN/IT/ES). Tekstwijziging op een hoofdpagina: NL aanpassen → `i18n_extract.py` → vertalen in `i18n/*.json` → `i18n_build.py`.
- Blogs: `content/blog/` volgens `SCHRIJFGIDS.md`; onderwerpvolgorde in `ONDERWERPEN.md`; planning in `content/CONTENTPLAN.md` (long-tail = 4+ woorden; geen doorway pages; alleen feiten van de site of van Yannick).
- Instagram-posts: generator in `social/tools/make-<datum>.py` (Pillow, fonts Inter/Inter Tight in dezelfde map), uitvoer in `social/<datum>/`; stijl: donker (#07080b), goud (#d9b25a), Inter Tight 800/900, 1080×1350. Beelden worden publiek via de site (`https://www.skylinedigital.nl/social/<datum>/<bestand>`). Inplannen via Metricool (brand 7654924, tijdzone Europe/Madrid) **alleen na expliciet akkoord per post**. Higgsfield-beelden kosten credits: alleen na akkoord.
- Geen foto's van Yannick op blogposts; mensen op zijn privéfoto's nooit gebruiken.
- Prijzen zoals op `/pricing`: website vanaf €499, 3D cinematic €749, SEO €39 p/m, social vanaf €79 p/m, AI-video €50, shoot €250 (+€300 drone). Niets anders beloven.

## Verwant
Het CRM (repo skylinedigitalcrm) beheert klanten, SEO-content voor klanten en WhatsApp; zie de CLAUDE.md daar.
