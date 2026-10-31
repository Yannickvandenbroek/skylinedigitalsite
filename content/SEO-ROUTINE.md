# SEO-routine skylinedigital.nl (automatisch, cloud)

Gestart 31 oktober 2026 op verzoek van Yannick: driemaal het tempo van een SEO-klant, dus **12 blogs en 6 pagina's per maand** (3 blogs per week, 1 à 2 pagina's per week). Een routine op claude.ai draait elke werkdag om 06:00 en doet hoogstens één stuk per ronde.

## Wat de ronde doet (in deze volgorde)
1. `git pull`. Installeer zo nodig `pip install beautifulsoup4`.
2. **Tel** wat er al is: blogs = bestanden `content/blog/<datum>-*.html` met een datum in de huidige ISO-week; pagina's = regels met `✅ live <datum>` in `content/PAGINAPLAN.md` in de huidige kalendermaand.
3. **Kies één klus**:
   - minder dan 3 blogs deze week → **blog** (stap 4);
   - anders minder dan 6 pagina's deze maand → **pagina** (stap 5);
   - anders: stop met "niets te doen".
4. **Blog.** Neem het bovenste open onderwerp (`- [ ]`) uit `content/blog/ONDERWERPEN.md` en schrijf het volledig volgens `content/blog/SCHRIJFGIDS.md` (kort antwoord, vraag-koppen, eigen ervaring met een link naar een `/werk-…`-project, alleen bronnen die je zelf hebt geopend, vaste prijzen exact uit de gids, je-vorm). Bestand `content/blog/<vandaag>-<slug>.html`. Vink het onderwerp af met datum en URL. Staan er daarna minder dan 5 open onderwerpen, voeg er dan 5 toe: long-tail (4+ woorden) uit Google-zoeksuggesties (`https://suggestqueries.google.com/complete/search?client=firefox&hl=nl&q=<begin>`), over websites, SEO, video, drone of lokale vindbaarheid voor ondernemers, nooit een hoofdzoekwoord dat al een blog, dienst-, branche- of plaatspagina heeft.
5. **Pagina.** Neem de eerstvolgende nog niet gebouwde pagina uit de tabel "Planning" in `content/PAGINAPLAN.md`. Sla pagina's over die op een antwoord van Yannick wachten ("Wat ik van Yannick nodig heb": onderhoudsabonnement, webshops, website-check-tool, goede doelen, landingspagina's/webapplicaties). Bouw hem met de vaste opbouw van dat paginatype uit het plan en in exact de stijl van een bestaande pagina van hetzelfde type (branchepagina's: kopieer de opbouw van `website-voor-installateurs.html`; dienstpagina's: die van `website-seo.html`; plaatspagina's lopen via `tools/gen_pages.py`). Alleen echte feiten en prijzen uit de schrijfgids; cases alleen uit het portfolio. Voeg de pagina toe aan `META` in `tools/seo_pass.py` en draai dat script. Zet in `content/PAGINAPLAN.md` achter de pagina `✅ live <datum>`. Alleen Nederlands; vertalen gebeurt later apart.
6. **Bouwen**, altijd in deze volgorde: `python3 tools/gen_pages.py` → `python3 tools/seo_pass.py` → `python3 tools/i18n_build.py` → `python3 tools/add_ga.py`. Kijk daarna naar `git diff --stat`: er mogen alleen jouw nieuwe stuk, `blog.html`, `sitemap.xml`, `content/…`, `tools/seo_pass.py` (je META-regel) en de vertaalde versies van exact die pagina's veranderen. Veranderen er andere pagina's (oude prijzen, andere teksten), commit die dan **niet** (`git checkout -- <bestand>`), en meld het in je slotbericht: dan loopt een bronbestand achter op de live site. Verander nooit andere pagina's met de hand.
7. **Controleren**: open de nieuwe pagina lokaal (`python3 -m http.server`) en controleer: één h1, titel en omschrijving, geen kapotte interne links, afbeeldingen met alt, geen "u" in de lopende tekst.
8. **Live zetten**: commit alleen de nieuwe en gegenereerde bestanden met een duidelijke boodschap, push naar `main` (Vercel zet hem live), en meld de nieuwe URL's bij IndexNow: `python3 tools/indexnow.py https://www.skylinedigital.nl/<pad>`.
9. **Afsluiten** met een paar regels: wat er live ging (URL), of iets is overgeslagen en waarom.

## Harde regels
- Kwaliteit boven tempo. Google straft "scaled content abuse": veel pagina's zonder eigen waarde. Elk stuk heeft een eigen zoekwoord, eigen ervaring van Skyline en echte bronnen. Twijfel je of iets waardevol is, schrijf dan het volgende onderwerp.
- Nooit twee stukken op hetzelfde hoofdzoekwoord (kannibalisatie): zoek eerst in `content/blog/`, de plaatspagina's en de branchepagina's.
- Geen geld uitgeven: geen betaalde API's, geen beeldgeneratie. Beeld: bestaande foto's uit `assets/`.
- Geen klantnamen, cijfers of reviews die niet op de site staan.
