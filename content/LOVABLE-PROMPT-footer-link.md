# Lovable-prompt: link naar Skyline Digital in de footer van klantsites

Op 28 okt 2026 gecontroleerd: 23 van de 29 klantsites hebben al "Website gerealiseerd door Skyline Digital" in de footer. Deze zes nog niet:

| Klant | Site | Lovable-project |
|---|---|---|
| Bato Ontstoppingen | bato-ontstoppingen.nl | plak de prompt |
| De Jonge Elektrotechniek | dejonge-elektrotechniek.nl | plak de prompt |
| De Jongh Projects | dejonghprojects.nl | plak de prompt |
| RSTK Rioolservice | rioolontstopperkampen.nl | plak de prompt |
| Van Loosbroek Installatietechniek | vanloosbroekinstallatietechniek.nl | plak de prompt |
| Regio Autorijschool Peter Barten | peterbartenrijschool.lovable.app | plak de prompt |

Airco Nick (airconick.nl) heeft de link ook niet; alleen doen als die site van jou is.

De klantsites staan in Lovable zonder GitHub-koppeling, dus dit gaat per project: open het project in Lovable, plak de prompt hieronder, controleer de preview, publiceer. Zo'n twee minuten per site.

## Prompt (plak in elk van de zes projecten)

```
Voeg onderaan in de footer, onder of naast de copyrightregel, één kleine regel toe:

Website gerealiseerd door Skyline Digital

waarbij "Skyline Digital" een link is naar https://www.skylinedigital.nl met target="_blank" en rel="noopener" (géén rel="nofollow"). Gebruik dezelfde kleine, gedempte tekststijl als de copyrightregel en dezelfde uitlijning; bij hover mag de link onderstrepen of de accentkleur krijgen. Verander verder niets aan de site.
```

## Opvallende variant (zoals award-sites het doen)

Award-sites zetten de credit niet weg als kleine grijze tekst, maar als een klein ontworpen element: een label in hoofdletters, de naam in een sterker gewicht, en een kleine hover-animatie. Deze prompt bouwt dat, in de huisstijl van de klantsite.

```
Bouw onderaan de footer, helemaal rechts op desktop en gecentreerd op mobiel, een opvallende maar verfijnde "credit" voor de maker van de site. Het is één link naar https://www.skylinedigital.nl (target="_blank", rel="noopener", géén nofollow) met aria-label "Website gerealiseerd door Skyline Digital".

Opbouw van de link:
1. Een klein label in hoofdletters met letterafstand 0.12em, lettergrootte 11px, gedempte kleur: "SITE BY"
2. Daarnaast de naam "Skyline Digital" in de koptekst-font van deze site, 14–15px, medium/semi-bold, in de normale tekstkleur van de footer.
3. Daarachter een klein pijltje naar rechtsboven (↗, als inline SVG, 12px).

Hover-animatie (alleen CSS, respecteer prefers-reduced-motion):
- De naam schuift in 300ms omhoog uit beeld en eronder schuift dezelfde tekst in de accentkleur van de site in (text-swap effect: wrapper met overflow hidden, twee gestapelde spans die 100% verschuiven op hover).
- Het pijltje beweegt 2px naar rechtsboven en krijgt de accentkleur.
- Onder de naam tekent zich van links naar rechts een lijn van 1px in de accentkleur (scaleX van 0 naar 1, transform-origin left).

Scheid de credit van de copyrightregel met een dunne verticale lijn (1px, 30% dekking) op desktop, of zet hem op een eigen regel op mobiel. Zorg dat het goed werkt op een donkere én lichte footer: gebruik de bestaande kleurvariabelen van de site, geen hardgecodeerde kleuren behalve de dekking. Verander verder niets aan de site.
```

Wil je dat het nóg meer opvalt: vervang stap 2 door het Skyline-logo (`https://www.skylinedigital.nl/assets/logo.png`, hoogte 18px, bij hover licht vergroten naar 1.05). Doe dat alleen bij klanten met een donkere footer; het logo is licht.

## Voor nieuwe sites

Zet dit standaard in elke nieuwe Lovable-site. In het CRM (module SEO-content, zie `LOVABLE-PROMPT-seo-content.md`) kan dit later automatisch als de site via GitHub of WordPress gekoppeld is; bij losse Lovable-projecten blijft het plakken.

## Waarom de bedrijfsnaam als linktekst

Google vindt veel links met dezelfde zoekwoordtekst ("website laten maken Den Bosch") verdacht. Links met je bedrijfsnaam vanaf echte klantsites zijn precies wat Google wil zien.
