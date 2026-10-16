# Schrijfgids kennisbank Skyline Digital

Doel: artikelen die Nederlandse ondernemers echt helpen. Dan scoren ze in Google en worden ze geciteerd door AI-zoekmachines (Google AI Overviews/AI Mode, ChatGPT-search, Copilot, Perplexity).
De regels hieronder volgen uit Google's eigen richtlijnen (helpful content, E-E-A-T, AI-features, spambeleid) en uit onderzoek naar generative engine optimization (GEO).

## Wat Google en AI belonen, en wat we dus doen
- **Mensen eerst.** Schrijf voor een ondernemer die deze vraag echt heeft, niet voor een zoekwoord. Google noemt "content vooral maken om zoekverkeer te trekken" en "veel automatisering zonder toegevoegde waarde" expliciet als waarschuwingssignalen. Massaal AI-pagina's maken zonder eigen waarde valt onder *scaled content abuse*.
- **Eigen ervaring (E-E-A-T).** Elk artikel bevat minstens één stuk dat alleen Skyline Digital kan schrijven: hoe wij het aanpakken, onze echte prijzen, een concreet project uit het portfolio (met link naar `/werk-…`), of wat we zagen bij het bouwen. Gebruik **alleen feiten die op de site staan**. Verzin niets.
- **Direct antwoord.** AI-zoekmachines citeren passages die een vraag meteen beantwoorden. Daarom:
  - bovenaan een `Kort antwoord` van 40–70 woorden;
  - tussenkoppen (`<h2>`) formuleren als de vraag die mensen stellen;
  - direct onder elke tussenkop 1–2 zinnen met het antwoord, daarna pas de uitleg;
  - één punt per alinea, korte alinea's, lijsten en tabellen waar dat helpt.
- **Cijfers en bronnen.** Onderzoek (GEO, Princeton/KDD 2024) liet zien dat statistieken, citaten en bronvermeldingen de zichtbaarheid in AI-antwoorden het meest verhogen. Keyword stuffing deed het juist slechter. Daarom:
  - gebruik concrete cijfers, maar **alleen met een bron die je in deze sessie zelf hebt geopend en gecontroleerd** (officieel heeft voorkeur: Google Search Central, Rijksoverheid, KVK, ILT, Autoriteit Persoonsgegevens, CBS, EU);
  - link de bron in de tekst en zet hem in `Bronnen`;
  - geen bron? Dan geen cijfer.
- **Eerlijk en actueel.** Zet nooit een datum of "in 2026" als dat niet klopt. Pas geen datums aan om "vers" te lijken (Google noemt dat expliciet). Geen beloftes over rankings of resultaten.
- **Geen streeflengte.** Google heeft geen voorkeurslengte. Een artikel is zo lang als nodig om de vraag volledig te beantwoorden, meestal 800–1400 woorden.
- **Zoekwoord natuurlijk.** Het hoofdzoekwoord staat in de titel (liefst vooraan), in de eerste alinea en in één tussenkop. Verder schrijf je gewoon natuurlijke zinnen met synoniemen, zonder herhaling om de herhaling.

## Vaste feiten (exact zo gebruiken)
- Multipage website **€499** eenmalig · 3D Cinematic website **€749** eenmalig · SEO **€39 per maand**
- Video-/fotoshoot op locatie **€250**, met drone **€300** · Social media beheer **vanaf €79 per maand**
- AI-content: **€50 per video**, **€5 per foto** (vanaf €100 10% korting, vanaf €200 20%, minimum €20)
- Gratis testwebsite: wij bouwen eerst een voorbeeld, de klant beslist daarna (`/aanvraag`)
- Bureau in 's-Hertogenbosch (Bruistensingel 500), werkt in heel Nederland; villa-films in Spanje (Moraira, Jávea)
- Oprichter: Yannick van den Broek
- Niet gebruiken tenzij het op de site staat: klantaantallen, conversiecijfers, "x% meer aanvragen", citaten van klanten, reviews.

## Toon
- Je-vorm, helder, nuchter, deskundig. Uitleggen zoals je het aan een ondernemer aan tafel zou doen.
- Geen clichés ("in de digitale wereld van vandaag", "in dit artikel gaan we…", "kortom"), geen overdreven superlatieven, geen verkooppraat. Eén duidelijke uitnodiging aan het eind is genoeg.
- Juridische of fiscale onderwerpen: alleen uitleg met bron, geen advies; verwijs naar de officiële bron.

## Bestand en opbouw
Bestand: `content/kennisbank/<JJJJ-MM-DD>-<slug>.html` (datum = publicatiedag, slug = kleine letters met streepjes, zoekwoord erin).

```html
<!--
title: <max 60 tekens, zoekwoord vooraan, geen "| Skyline Digital">
slug: <slug-zonder-datum>
date: <JJJJ-MM-DD>
eyebrow: <categorie: Prijzen | Webdesign | SEO | Drone & video | Social media | AI | Branche>
read: <x min>
img: <bestand uit assets/, bijv. photo-laptop-desk.jpg>
desc: <120–155 tekens: belofte + zoekwoord, eindigt met punt>
-->
<p class="lead">2–3 zinnen: voor wie dit is en wat je na het lezen weet.</p>
<div class="tldr"><strong>Kort antwoord</strong> 40–70 woorden die de hoofdvraag volledig beantwoorden.</div>

<h2>Vraag zoals mensen hem stellen?</h2>
<p>Direct antwoord in 1–2 zinnen.</p>
<p>Uitleg…</p>
… (meerdere <h2>, eventueel <h3>, <ul>/<ol>, <table>)

<h2>Hoe wij dit aanpakken</h2>   ← eigen ervaring, met link naar een /werk-… pagina of dienstpagina

<h2>Veelgestelde vragen</h2>
<details><summary>Vraag?</summary><p>Antwoord in 1–3 zinnen.</p></details>   ← 3 tot 5 vragen, uit de zoeksuggesties
<p>Afsluitende zin met één uitnodiging (gratis testwebsite /aanvraag of gesprek /contact).</p>

<h2>Bronnen</h2>
<ul><li><a href="https://…" rel="noopener">Naam bron — titel pagina</a></li></ul>
```
- Afbeeldingen: kies een passende `assets/photo-*.jpg`. Varieer: niet dezelfde als de twee vorige artikelen.
- Interne links: 3–6 stuks naar dienstpagina's, `/pricing`, relevante `/werk-…`, een locatiepagina of een ander kennisbankartikel. Gebruik alleen paden die bestaan, zonder `.html`.
- Externe links: `rel="noopener"`, alleen naar betrouwbare bronnen.

## Werkwijze per week
1. `git pull`. Pak in `content/kennisbank/ONDERWERPEN.md` het bovenste open onderwerp.
2. Haal de echte vragen op voor tussenkoppen en FAQ:
   `curl -s "https://suggestqueries.google.com/complete/search?client=firefox&hl=nl&gl=nl&q=<zoekwoord>"` (ook met "wat", "hoe", "kosten", "waarom" ervoor of erachter).
3. Controleer dat geen bestaand artikel, geen dienstpagina en geen locatiepagina dezelfde vraag al beantwoordt. Zo ja: kies een andere invalshoek of het volgende onderwerp.
4. Zoek en open 1–3 betrouwbare bronnen voor cijfers en regels.
5. Schrijf het bestand volgens de opbouw hierboven.
6. `python3 tools/gen_pages.py`. Die controleert het artikel en stopt met een duidelijke melding als er iets mist. Los de melding op en draai opnieuw.
7. Lees het resultaat in `kennisbank/<slug>.html` nog één keer na op feiten, prijzen en links.
8. Vink het onderwerp af in ONDERWERPEN.md: `- [x] <datum> → /kennisbank/<slug> — <titel>`. Verplaats de regel naar `## Gedaan`.
9. Commit (`Kennisbank: <titel>`) en push naar `main`; Vercel zet het live.
10. Na ±2 minuten: `python3 tools/indexnow.py https://www.skylinedigital.nl/kennisbank/<slug> https://www.skylinedigital.nl/kennisbank https://www.skylinedigital.nl/sitemap.xml`.
11. Is de lijst bijna leeg (minder dan 5 open)? Voeg dan nieuwe onderwerpen toe op basis van zoeksuggesties rond de diensten, zonder overlap met wat er al is.
