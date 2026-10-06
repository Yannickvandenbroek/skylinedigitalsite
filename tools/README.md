# Tools (Python 3 + beautifulsoup4)

Alle scripts draaien vanuit de projectmap (ze doen zelf `os.chdir`).

- `seo_pass.py` — zet op elke NL-pagina een consistente SEO-head (title/description/canonical/og/robots) en JSON-LD `@graph` (LocalBusiness, WebSite, WebPage, Breadcrumb, Service, FAQ). Titels/omschrijvingen staan in `META` bovenin.
- `gen_pages.py` — genereert de locatiepagina's (`website-laten-maken-<plaats>.html`, `regio.html`), de kennisbank (`kennisbank.html`, `kennisbank/*.html`), de footerkolom Regio's en `sitemap.xml`. Teksten staan in `CITIES` en `ARTICLES`.
- `i18n_extract.py` — haalt alle vertaalbare segmenten uit de NL-hoofdpagina's naar `i18n/source.json`.
- `i18n_build.py` — bouwt `/en`, `/it`, `/es` uit `i18n/<taal>.json` (zelfde keys als source.json) met hreflang, gelocaliseerde links en structured data, en zet `SKY_ALT` + hreflang op de NL-pagina's.

Workflow bij tekstwijzigingen op een hoofdpagina: NL-pagina aanpassen → `i18n_extract.py` → nieuwe keys in `i18n/en.json`, `it.json`, `es.json` vertalen → `i18n_build.py`.
