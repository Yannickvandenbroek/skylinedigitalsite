# Lovable-prompt: module "SEO-content" voor skylinedigitalcrm

Plak alles onder de streep in Lovable (project skylinedigitalcrm). Bouw het eventueel in twee rondes: eerst deel 1–4 (data, scherm, genereren), daarna deel 5–6 (planning en publiceren).

---

Bouw een nieuwe module **"SEO-content"** in mijn CRM. Hiermee maak ik automatisch SEO- en GEO-geoptimaliseerde blogs en pagina's voor mijn SEO-klanten, en zie ik alles per klant en in één overzicht op mijn dashboard. Gebruik de bestaande stijl, de bestaande tabel `customers` en de bestaande Supabase-secret `ANTHROPIC_API_KEY`. Alle teksten in de app in het Nederlands.

## 1. Database (Supabase-migratie, met RLS zoals de andere tabellen)

**`seo_profielen`**: één per klant met SEO-abonnement
- `customer_id` (fk naar customers), `actief` (bool), `website_url`, `taal` (nl/en/es, standaard nl)
- `bedrijfsomschrijving` (tekst), `diensten` (tekst: dienst + prijs per regel), `werkgebied` (plaatsen/regio's), `doelgroep`
- `bewijs` (tekst: projecten, cases, ervaring die in teksten mag; alleen echte feiten)
- `tone_of_voice` (tekst, standaard: "je-vorm, helder, nuchter, deskundig, geen verkooppraat")
- `verboden` (tekst: dingen die nooit genoemd mogen worden)
- `ritme` (enum: wekelijks, tweewekelijks, maandelijks), `publicatiedag` (0–6), `goedkeuring_nodig` (bool, standaard true)
- `publicatiemethode` (enum: handmatig, github, wordpress) + bijbehorende instellingen (zie deel 6)

**`seo_onderwerpen`**: de onderwerpenlijst per klant
- `customer_id`, `type` (blog | pagina | plaatspagina | branchepagina), `titel`, `hoofdzoekwoord`, `extra_zoekwoorden` (text[]), `invalshoek`, `interne_links` (text[]), `prioriteit` (int), `status` (open | ingepland | gebruikt), `gepland_op` (date)

**`seo_content`**: de gemaakte stukken
- `customer_id`, `onderwerp_id`, `type`, `titel` (max 60 tekens), `slug`, `meta_omschrijving` (120–155 tekens), `hoofdzoekwoord`
- `kort_antwoord`, `html` (de volledige inhoud), `faq` (jsonb: vraag/antwoord), `bronnen` (jsonb: naam/url), `woorden` (int)
- `status` (concept | ter_goedkeuring | goedgekeurd | gepubliceerd | afgekeurd), `opmerkingen`, `gepubliceerd_op`, `live_url`
- `kosten_tokens` (int), `model` (tekst), `created_at`

## 2. Schermen

**Menu-item "SEO-content"** met drie tabbladen:
1. **Overzicht**: alle klanten met een actief SEO-profiel als kaarten: aantal gepubliceerd deze maand, volgende geplande datum, aantal concepten dat op mijn goedkeuring wacht (rode badge), laatste live-link.
2. **Te keuren**: lijst van alle stukken met status `ter_goedkeuring`, met een voorbeeldweergave (gerenderde HTML), en knoppen **Goedkeuren & publiceren**, **Aanpassen** (bewerkbare velden + editor) en **Afkeuren** (met reden; de reden wordt bij de volgende generatie meegegeven).
3. **Agenda**: kalender met geplande en gepubliceerde stukken per klant.

**Op de klantpagina (`KlantDetail`)** een tab "SEO-content":
- formulier voor het SEO-profiel (deel 1);
- de onderwerpenlijst met slepen om de volgorde te bepalen, en een knop **"Onderwerpen voorstellen"** (deel 3);
- de lijst van gemaakte stukken met status en live-link;
- knop **"Nu een stuk maken"** voor het bovenste open onderwerp.

**Op het hoofddashboard** een kaart "SEO-content": deze maand gepubliceerd (totaal), wachtend op goedkeuring, en de eerstvolgende drie geplande stukken.

## 3. Edge function `seo-onderwerpen` (onderwerpen voorstellen)

Input: `customer_id`. Doet:
1. Haalt Google-zoeksuggesties op voor de diensten × plaatsen uit het profiel via `https://suggestqueries.google.com/complete/search?client=firefox&hl=<taal>&gl=<land>&q=<zoekterm>` (ook met "wat kost", "hoe", "beste", "voor", "in" ervoor of erachter).
2. Houdt alleen **long-tail zoekopdrachten van 4 of meer woorden** over.
3. Laat Claude daar 12 onderwerpen van maken (mix van blogs en pagina's), zonder overlap met bestaande onderwerpen en content van deze klant, elk met hoofdzoekwoord (4+ woorden), extra zoekwoorden, invalshoek en 2–4 interne links naar bestaande pagina's van de klant.
4. Slaat ze op als `open` in `seo_onderwerpen`.

## 4. Edge function `seo-schrijf` (een stuk maken)

Input: `customer_id` (pakt het bovenste open onderwerp) of `onderwerp_id`.

Roep de Anthropic Messages API aan met model **`claude-sonnet-5-5`** en schakel de **web search-tool** van de API in (zie de Anthropic-docs voor de actuele tool-naam), zodat Claude bronnen zelf kan openen en controleren. Gebruik deze systeeminstructie (vul de profielvelden in):

> Je schrijft SEO- en GEO-geoptimaliseerde content voor {bedrijfsnaam}, {bedrijfsomschrijving}. Taal: {taal}. Doelgroep: {doelgroep}. Toon: {tone_of_voice}.
> Regels (volgen Google's helpful-content-richtlijnen en onderzoek naar generative engine optimization):
> 1. Schrijf voor een mens met deze vraag, niet voor een zoekwoord. Het hoofdzoekwoord ({hoofdzoekwoord}) staat in de titel (liefst vooraan), in de eerste alinea en in één tussenkop; verder natuurlijke taal, geen herhaling om de herhaling.
> 2. Begin met een korte inleiding en een blok "Kort antwoord" van 40–70 woorden dat de hoofdvraag volledig beantwoordt.
> 3. Tussenkoppen (h2) zijn de vragen die mensen echt stellen; direct onder elke kop 1–2 zinnen met het antwoord, daarna pas uitleg. Korte alinea's, lijsten en tabellen waar dat helpt.
> 4. Gebruik alleen feiten over het bedrijf die hieronder staan: diensten en prijzen {diensten}, werkgebied {werkgebied}, bewijs {bewijs}. Verzin nooit klanten, citaten, reviews, resultaten of cijfers. Nooit noemen: {verboden}.
> 5. Cijfers en regels alleen met een bron die je met de web search-tool zelf hebt geopend; officiële bronnen hebben voorkeur. Zet de bron als link in de tekst en in een lijst "Bronnen". Geen bron = geen cijfer. Geen juridisch, fiscaal of medisch advies; verwijs naar de officiële bron.
> 6. Eén sectie met eigen ervaring van het bedrijf (uit {bewijs}), met een link naar de relevante pagina.
> 7. 3–5 veelgestelde vragen met korte antwoorden.
> 8. 2–6 interne links naar: {interne_links}. Eén duidelijke uitnodiging aan het eind.
> 9. Geen clichés ("in de digitale wereld van vandaag", "kortom"), geen superlatieven, geen beloftes over rankings.
> 10. Lengte: zo lang als nodig, meestal 800–1400 woorden. Een pagina (dienst/plaats/branche) krijgt echte, eigen inhoud; geen bijna-kopie van andere pagina's (geen doorway pages).
> Geef het resultaat als JSON: { titel (max 60 tekens), slug, meta_omschrijving (120–155 tekens), kort_antwoord, html (alleen de inhoud vanaf de inleiding, met h2/h3/p/ul/ol/table/details), faq: [{vraag, antwoord}], bronnen: [{naam, url}] }.

Daarna controleert de function het resultaat en weigert het (status `afgekeurd` + reden in `opmerkingen`) als: titel > 60 tekens, meta niet 120–155 tekens, minder dan 3 h2's, minder dan 3 FAQ's, geen externe bron, of minder dan 3 interne links. Bij afkeuring één nieuwe poging met de foutmelding erbij.

Opslaan in `seo_content` met status `ter_goedkeuring` (of `goedgekeurd` als `goedkeuring_nodig` uit staat), woordtelling, model en tokens. Log het verbruik ook in de bestaande tabel `api_verbruik`. Stuur mij een melding via de bestaande meldingen (push/Telegram): "📝 Nieuw concept voor {klant}: {titel}".

## 5. Planning (pg_cron)

Een dagelijkse cron-job om 08:00 (Europe/Amsterdam) die voor elk actief profiel controleert of er volgens `ritme` en `publicatiedag` vandaag een stuk gemaakt moet worden, en dan `seo-schrijf` aanroept. Als er minder dan 3 open onderwerpen zijn, eerst `seo-onderwerpen` aanroepen.

## 6. Publiceren (bij "Goedkeuren & publiceren", of automatisch als goedkeuring uit staat)

Per klant volgens `publicatiemethode`:
- **handmatig**: status wordt `goedgekeurd`; knoppen "Kopieer HTML" en "Download .md". Ik zet het zelf live en vul daarna de live-URL in.
- **github**: instellingen `repo` (eigenaar/naam), `branch`, `pad` (bijv. `content/blog/{datum}-{slug}.md`). Commit het stuk als Markdown met frontmatter (titel, slug, datum, meta, hoofdzoekwoord) via de GitHub-API met een secret `GITHUB_TOKEN`. De site van de klant bouwt daar zelf de pagina van.
- **wordpress**: instellingen `wp_url`, `wp_gebruiker`, en een applicatiewachtwoord als secret per klant. Maak een bericht via de WordPress REST API (`/wp-json/wp/v2/posts` voor blogs, `/pages` voor pagina's), status "publish", met de meta-omschrijving in het excerpt.

Na publiceren: status `gepubliceerd`, `gepubliceerd_op` en `live_url` invullen, en een melding "✅ Live voor {klant}: {live_url}".

## 7. Veiligheid en kwaliteit
- Standaard staat **goedkeuring aan**: niets gaat live zonder dat ik op "Goedkeuren" heb gedrukt, tenzij ik het per klant uitzet.
- Geheimen (GitHub-token, WordPress-wachtwoorden) alleen als Supabase-secrets, nooit in de database of de frontend.
- Toon in elk concept duidelijk de bronnen, zodat ik ze kan controleren voordat ik goedkeur.
