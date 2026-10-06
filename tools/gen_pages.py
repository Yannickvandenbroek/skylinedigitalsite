import re, json, html, os, glob
os.chdir("/Users/yannickvandenbroek/Documents/Skylinedigital/own site/skyline-digital")
BASE = "https://skylinedigital.nl"
TODAY = "2026-10-06"
src = open("website-seo.html").read()
HEADER = re.search(r'  <header class="nav".*?</header>\n', src, re.S).group(0)
HEADER = re.sub(r' aria-current="page"', '', HEADER)
FOOTER = re.search(r'    <footer class="footer">.*?</footer>\n', src, re.S).group(0)
ARROW = '<span class="row-arrow" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg></span>'

CITIES = [
 dict(slug="den-bosch", name="Den Bosch", full="'s-Hertogenbosch", in_="in Den Bosch", region="Noord-Brabant",
      intro="Skyline Digital zit zelf aan de Bruistensingel in 's-Hertogenbosch. Een website laten maken in Den Bosch betekent bij ons: een bureau om de hoek, een kop koffie in het Paleiskwartier of de binnenstad, en een site die precies past bij hoe Bossche klanten zoeken en kopen.",
      intro2="Van ondernemers op bedrijventerrein De Herven en De Brand tot winkels in de Vughterstraat en praktijken in Maaspoort en Rosmalen: we kennen de stad, de concurrentie en de zoekwoorden waar jouw klanten op zoeken.",
      sectors=["bouw, installatie en afbouw", "horeca en retail in de binnenstad", "zakelijke dienstverlening in het Paleiskwartier", "zorg- en wellnesspraktijken"],
      places="de Binnenstad, het Paleiskwartier, Maaspoort, De Groote Wielen, Engelen en Empel", near=["rosmalen","vught","oss"], travel="Wij zitten zelf in Den Bosch — een afspraak op jouw locatie is zo gemaakt."),
 dict(slug="rosmalen", name="Rosmalen", full="Rosmalen", in_="in Rosmalen", region="Noord-Brabant",
      intro="Rosmalen groeit hard: De Groote Wielen, bedrijventerrein Kruisstraat en een levendig centrum rond de Molenhoekpassage. Wie hier een website laat maken, wil een site die net zo professioneel oogt als de bedrijven die er zitten — en die gevonden wordt door inwoners van Rosmalen én de rest van de gemeente 's-Hertogenbosch.",
      intro2="Vanaf ons kantoor aan de Bruistensingel zijn we in tien minuten in Rosmalen. We bouwen websites voor aannemers, autobedrijven, kappers, fysiotherapeuten en andere lokale ondernemers die meer uit hun online vindbaarheid willen halen.",
      sectors=["bouw- en klusbedrijven", "autobedrijven en garages", "praktijken voor fysio, tandarts en huid", "sport, fitness en personal training"],
      places="het centrum, De Groote Wielen, Kruisstraat, Hintham en Maliskamp", near=["den-bosch","oss","vught"], travel="Rosmalen ligt op tien minuten van ons kantoor — we komen graag langs."),
 dict(slug="vught", name="Vught", full="Vught", in_="in Vught", region="Noord-Brabant",
      intro="Vught staat bekend om zijn groene villawijken, de IJzeren Man en een ondernemend centrum. Klanten in Vught verwachten kwaliteit — ook online. Een website laten maken in Vught vraagt dus om een ontwerp met rust, klasse en een uitstraling die bij het dorp past.",
      intro2="We werken voor Vughtse interieurzaken, makelaars, adviesbureaus, zorgverleners en horeca. Omdat we vanuit Den Bosch op een kwartier afstand zitten, combineren we een persoonlijk gesprek op locatie met de snelheid van een klein, gespecialiseerd team.",
      sectors=["makelaars en vastgoed", "interieur, tuin en woninginrichting", "advies- en coachingpraktijken", "restaurants en lunchrooms"],
      places="het centrum, Vught-Noord, de Loonse en Drunense Duinen-zijde en Cromvoirt", near=["den-bosch","rosmalen","tilburg"], travel="Vught ligt op een kwartier van ons kantoor in Den Bosch."),
 dict(slug="oss", name="Oss", full="Oss", in_="in Oss", region="Noord-Brabant",
      intro="Oss is een echte maak- en handelsstad: van farma en food tot logistiek en metaal. Juist in een stad met zoveel bedrijvigheid maakt een sterke website het verschil tussen gevonden worden en overgeslagen worden. Een website laten maken in Oss doe je daarom met een bureau dat snelheid, vindbaarheid en een professionele uitstraling combineert.",
      intro2="Vanuit Den Bosch zijn we in twintig minuten in Oss. We bouwen voor productiebedrijven en toeleveranciers op Elzenburg en Vorstengrafdonk, maar net zo goed voor winkels in het centrum en praktijken in Ruwaard en Ussen.",
      sectors=["maakindustrie en toeleveranciers", "logistiek en transport", "installatie- en technische bedrijven", "winkels en horeca in het centrum"],
      places="het centrum, Ruwaard, Ussen, Schadewijk en de bedrijventerreinen Elzenburg, Moleneind en Vorstengrafdonk", near=["den-bosch","uden","nijmegen"], travel="Oss ligt op twintig minuten van ons kantoor via de A59."),
 dict(slug="eindhoven", name="Eindhoven", full="Eindhoven", in_="in Eindhoven", region="Noord-Brabant",
      intro="Eindhoven is de technologie- en designstad van Nederland: Brainport, de High Tech Campus, Strijp-S en de Dutch Design Week. Bedrijven die hier een website laten maken, meten zich met een hoog niveau. Wij bouwen sites die dat niveau halen — strak ontworpen, technisch scherp en gebouwd om te converteren.",
      intro2="Of je nu een startup bent op Strijp-S, een installatiebedrijf in Woensel of een restaurant in het centrum: we vertalen jouw verhaal naar een website die bij de Eindhovense standaard past en die in Google boven de concurrentie uitkomt.",
      sectors=["tech, software en startups", "design- en creatieve bureaus", "installatie- en bouwbedrijven", "horeca, retail en leisure"],
      places="het centrum, Strijp-S, Woensel, Stratum, Gestel, Tongelre en de High Tech Campus", near=["den-bosch","tilburg","oss"], travel="Eindhoven ligt op een half uur van Den Bosch via de A2 — we komen graag langs."),
 dict(slug="tilburg", name="Tilburg", full="Tilburg", in_="in Tilburg", region="Noord-Brabant",
      intro="Tilburg combineert een rijk textielverleden met een jonge, creatieve energie: de Spoorzone, Tilburg University, Piushaven en een enorme studentenpopulatie. Een website laten maken in Tilburg vraagt om een frisse uitstraling die opvalt bij een jong, kritisch publiek — en om vindbaarheid in een stad met veel concurrentie.",
      intro2="We werken voor Tilburgse horeca, logistieke bedrijven, creatieve ondernemers en praktijken. Vanuit Den Bosch zitten we op een halfuur afstand, dus een kennismaking op locatie in de Spoorzone of in jouw eigen zaak is zo geregeld.",
      sectors=["logistiek en distributie", "creatieve sector en events", "horeca en nachtleven", "onderwijs- en zorgpartijen"],
      places="het centrum, de Spoorzone, Piushaven, Reeshof, Berkel-Enschot en Udenhout", near=["den-bosch","vught","breda"], travel="Tilburg ligt op een half uur van ons kantoor via de N65."),
 dict(slug="breda", name="Breda", full="Breda", in_="in Breda", region="Noord-Brabant",
      intro="Breda is een stad met allure: de Grote Markt, het Ginneken, de haven en een sterke mix van zakelijke dienstverlening, food en toerisme. Een website laten maken in Breda betekent voor ons een ontwerp dat die Bourgondische kwaliteit uitstraalt en tegelijk keihard werkt voor je omzet.",
      intro2="We bouwen voor Bredase adviesbureaus, bouwbedrijven, hospitality en winkels in de binnenstad. Door onze focus op snelheid en SEO zie je de resultaten terug in Google — ook in een stad waar veel bureaus actief zijn.",
      sectors=["zakelijke dienstverlening en advies", "food, horeca en hospitality", "bouw, installatie en vastgoed", "retail in de binnenstad en het Ginneken"],
      places="het centrum, het Ginneken, Princenhage, Haagse Beemden, Teteringen en Prinsenbeek", near=["tilburg","den-bosch","eindhoven"], travel="Breda ligt op drie kwartier van Den Bosch; de kennismaking doen we op locatie of via video."),
 dict(slug="nijmegen", name="Nijmegen", full="Nijmegen", in_="in Nijmegen", region="Gelderland",
      intro="Nijmegen is de oudste stad van Nederland en tegelijk een van de jongste door de Radboud Universiteit en het Radboudumc. Zorg, onderwijs, horeca en een actief MKB zorgen voor een drukke online markt. Wie in Nijmegen een website laat maken, wil opvallen tussen die concurrentie — met een site die snel is, mooi oogt en vindbaar is.",
      intro2="Vanuit Den Bosch zijn we in veertig minuten in Nijmegen. We werken voor praktijken en zorgondernemers rond het Radboud, voor horeca aan de Waalkade en voor bedrijven op Bijsterhuizen en de Winkelsteeg.",
      sectors=["zorg, therapie en paramedische praktijken", "horeca aan de Waalkade en in de binnenstad", "onderwijs en trainingsbureaus", "bedrijven op Bijsterhuizen en Winkelsteeg"],
      places="het centrum, de Waalkade, Dukenburg, Lindenholt, Nijmegen-Noord en de Winkelsteeg", near=["oss","den-bosch","uden"], travel="Nijmegen ligt op veertig minuten van ons kantoor via de A50 en A73."),
 dict(slug="waalwijk", name="Waalwijk", full="Waalwijk", in_="in Waalwijk", region="Noord-Brabant",
      intro="Waalwijk is van oudsher de schoen- en lederstad en vandaag een logistieke hotspot aan de A59, met Haven Zeven en Haven Acht als snelgroeiende bedrijventerreinen. Een website laten maken in Waalwijk doen we voor transporteurs, groothandels en productiebedrijven, maar net zo goed voor winkels en horeca aan de Grotestraat.",
      intro2="We zitten op twintig minuten rijden in Den Bosch. Dat betekent korte lijnen, een persoonlijk gesprek op jouw locatie en een website die gebouwd is om in Waalwijk, Kaatsheuvel, Sprang-Capelle en de rest van De Langstraat gevonden te worden.",
      sectors=["logistiek, transport en groothandel", "productie en maakindustrie", "winkels en horeca in het centrum", "bouw- en installatiebedrijven"],
      places="het centrum, Haven Zeven en Haven Acht, Sprang-Capelle, Waspik en Kaatsheuvel", near=["den-bosch","tilburg","vught"], travel="Waalwijk ligt op twintig minuten van Den Bosch via de A59."),
 dict(slug="uden", name="Uden", full="Uden", in_="in Uden", region="Noord-Brabant",
      intro="Uden is het winkel- en zorghart van de gemeente Maashorst, met een gezellig centrum, ziekenhuis Bernhoven en een sterk MKB op Loopkant-Liessent en Goorkens. Een website laten maken in Uden betekent voor ons een site die lokaal vindbaar is — niet alleen in Uden, maar in de hele regio tot aan Veghel, Boekel en Oss.",
      intro2="Vanuit Den Bosch zijn we in een half uur in Uden. We bouwen voor winkeliers, zorgverleners, bouwbedrijven en agrarische ondernemers die hun online uitstraling willen laten aansluiten bij de kwaliteit die ze in de praktijk leveren.",
      sectors=["retail en horeca in het centrum", "zorg- en gezondheidspraktijken", "bouw, installatie en techniek", "agrarische en groene bedrijven"],
      places="het centrum, Uden-Zuid, Volkel, Odiliapeel en de bedrijventerreinen Loopkant-Liessent en Goorkens", near=["oss","den-bosch","nijmegen"], travel="Uden ligt op een half uur van ons kantoor via de A50."),
]
CITY_BY = {c["slug"]: c for c in CITIES}

ARTICLES = [
 dict(slug="wat-kost-een-website-laten-maken", title="Wat kost een website laten maken in 2026?", eyebrow="Prijzen", read="6 min", img="photo-laptop-desk.jpg",
      desc="Wat kost een website laten maken in 2026? Een eerlijk overzicht van prijzen: van €499 voor een maatwerk multipage website tot de kosten van hosting, SEO en onderhoud.",
      body="""
<p class="lead">De vraag die elke ondernemer stelt vóór het eerste gesprek: wat kost een website laten maken? Het eerlijke antwoord is "dat hangt ervan af" — maar daar heb je niets aan. Daarom hieronder concrete bedragen, wat je ervoor krijgt en waar de verschillen vandaan komen.</p>
<h2>De korte versie</h2>
<ul>
<li><strong>Doe-het-zelf (Wix, Squarespace, WordPress-template):</strong> €10 tot €40 per maand, plus heel veel eigen uren.</li>
<li><strong>Freelancer of klein bureau, maatwerk:</strong> €500 tot €3.000 eenmalig.</li>
<li><strong>Groot bureau, uitgebreid maatwerk of webshop:</strong> €5.000 tot €25.000+.</li>
</ul>
<p>Bij Skyline Digital bouwen we een <a href="/website-seo">maatwerk multipage website voor €499</a> en een <a href="/pricing">3D cinematic website voor €749</a>. Dat kan omdat we met een klein team, een vaste werkwijze en eigen tooling werken — niet omdat we templates van de plank halen.</p>
<h2>Waar betaal je eigenlijk voor?</h2>
<p>Een websiteprijs bestaat uit vier blokken. Als je die uit elkaar trekt, begrijp je meteen waarom de ene offerte €600 is en de andere €6.000.</p>
<h3>1. Ontwerp</h3>
<p>Een template kost nul ontwerpuren. Maatwerk kost er tien tot veertig. Het verschil zie je direct terug in herkenbaarheid: een maatwerkontwerp past bij jouw merk, een template lijkt op duizend andere sites.</p>
<h3>2. Bouw en techniek</h3>
<p>Hoe de site gebouwd is, bepaalt de laadsnelheid, de veiligheid en hoe goed Google de site kan lezen. Een snelle, schone bouw zonder overbodige plug-ins is goedkoper in onderhoud én scoort beter in de zoekresultaten.</p>
<h3>3. Content</h3>
<p>Teksten, foto's en video. Dit wordt vaak vergeten in de offerte, terwijl het de grootste invloed heeft op of een bezoeker klant wordt. Wij combineren websites daarom met <a href="/drone-video">eigen foto- en videoproductie</a> en <a href="/ai-content">AI-content</a>, zodat je niet met lege pagina's blijft zitten.</p>
<h3>4. Doorlopende kosten</h3>
<p>Reken op €5 tot €25 per maand voor hosting en domein. SEO is optioneel: bij ons <a href="/pricing">€39 per maand</a>, inclusief technische optimalisatie, zoekwoorden en een maandelijkse rapportage.</p>
<h2>Wat kost een website laten maken in Den Bosch of omgeving?</h2>
<p>Regionaal verschillen de prijzen weinig; de bureaukeuze maakt het verschil. In Noord-Brabant zie je voor maatwerk websites meestal €1.000 tot €4.000. Omdat wij in <a href="/website-laten-maken-den-bosch">Den Bosch</a> zitten en vanuit daar werken voor <a href="/website-laten-maken-eindhoven">Eindhoven</a>, <a href="/website-laten-maken-tilburg">Tilburg</a>, <a href="/website-laten-maken-oss">Oss</a> en de rest van Nederland, kunnen we een vaste, lage instapprijs hanteren.</p>
<h2>Vijf vragen die je moet stellen voordat je tekent</h2>
<ol>
<li>Is het ontwerp maatwerk of een aangepaste template?</li>
<li>Wie is eigenaar van de site en het domein — jij of het bureau?</li>
<li>Wat is de verwachte laadtijd en PageSpeed-score bij oplevering?</li>
<li>Zit SEO-basis (titels, meta-omschrijvingen, sitemap, structured data) in de prijs?</li>
<li>Wat kost een extra pagina of aanpassing na oplevering?</li>
</ol>
<h2>Eerst zien, dan beslissen</h2>
<p>Twijfel je of een maatwerk website het waard is? Wij bouwen eerst een <a href="/aanvraag">gratis testwebsite</a>. Je ziet het ontwerp en de snelheid voordat je iets betaalt — dat is de eerlijkste manier om de prijs te beoordelen.</p>
"""),
 dict(slug="website-laten-maken-waar-op-letten", title="Website laten maken: 10 dingen waar je op moet letten", eyebrow="Checklist", read="7 min", img="photo-wireframes.jpg",
      desc="Een website laten maken? Deze checklist van 10 punten voorkomt dure fouten: eigendom, snelheid, SEO, mobiel, content, onderhoud en de vragen die je het bureau moet stellen.",
      body="""
<p class="lead">Een website laat je niet elk jaar maken. Daarom loont het om de keuze één keer goed te doen. Deze checklist komt uit de praktijk van tientallen projecten — inclusief de fouten die we ondernemers zagen maken bij hun vorige bureau.</p>
<h2>1. Jij bent eigenaar — van alles</h2>
<p>Domeinnaam, hosting, broncode en content moeten op jouw naam staan. Een bureau dat de site "in beheer houdt" en je bij vertrek laat betalen voor je eigen website, is een rode vlag.</p>
<h2>2. Snelheid is geen luxe</h2>
<p>Elke seconde laadtijd kost bezoekers, en Google gebruikt snelheid als rankingfactor. Vraag om een PageSpeed-score bij oplevering en laat die vastleggen. Onze sites halen op mobiel standaard groene scores.</p>
<h2>3. Mobiel is het uitgangspunt, niet een afterthought</h2>
<p>Meer dan 70% van het lokale zoekverkeer komt van een telefoon. Beoordeel het ontwerp dus eerst op mobiel: knoppen groot genoeg, telefoonnummer klikbaar, formulieren kort.</p>
<h2>4. SEO-basis hoort erbij</h2>
<p>Unieke paginatitels, meta-omschrijvingen, een sitemap, schone URL's, structured data en snelle afbeeldingen: dat is geen "SEO-pakket", dat is gewoon een goed gebouwde website. Lees ook onze <a href="/kennisbank/lokale-seo-tips">tips voor lokale SEO</a>.</p>
<h2>5. Content op tijd regelen</h2>
<p>De meeste vertraging in websiteprojecten komt door ontbrekende teksten en foto's. Spreek af wie wat levert en wanneer — of laat het bureau de <a href="/drone-video">foto's en video</a> en de teksten verzorgen.</p>
<h2>6. Eén duidelijke actie per pagina</h2>
<p>Bellen, offerte aanvragen, afspraak maken: kies per pagina één doel en maak dat overal zichtbaar. Een site met tien knoppen die allemaal iets anders willen, converteert slechter dan een site met één duidelijke vraag.</p>
<h2>7. Zelf kunnen aanpassen</h2>
<p>Je moet een tekst of foto zelf kunnen wijzigen zonder factuur. Vraag of er een CMS in zit en of je uitleg krijgt.</p>
<h2>8. Beveiliging en back-ups</h2>
<p>SSL (het slotje) is vanzelfsprekend. Vraag ook naar updates, back-ups en wat er gebeurt als de site gehackt wordt. Een <a href="/pricing">onderhoudsabonnement</a> is vaak goedkoper dan één keer herstel.</p>
<h2>9. Bekijk echt werk, geen mockups</h2>
<p>Klik door het <a href="/portfolio">portfolio</a> op je telefoon. Laden de sites snel? Werken de formulieren? Staan de klanten nog online met die site?</p>
<h2>10. Weet wat het daarna kost</h2>
<p>Hosting, domein, onderhoud, extra pagina's: laat het op papier zetten. Bij ons staan de bedragen gewoon op de <a href="/pricing">pricingpagina</a>.</p>
<h2>Bonus: vraag een gratis testwebsite</h2>
<p>De beste check is het resultaat zelf zien. Daarom bouwen we eerst een <a href="/aanvraag">gratis testwebsite</a>, en beslis je daarna.</p>
"""),
 dict(slug="drone-video-laten-maken-kosten-en-regels", title="Drone video laten maken: kosten, regels en wat je mag verwachten", eyebrow="Drone & video", read="6 min", img="photo-drone-villa.jpg",
      desc="Een drone video laten maken? Lees wat het kost (vanaf €250 per shoot), welke regels gelden in Nederland, waar je wel en niet mag vliegen en hoe een shoot verloopt.",
      body="""
<p class="lead">Dronebeelden geven een bedrijf, villa of evenement in een paar seconden grootsheid. Maar wat kost een drone video laten maken, wat mag wel en niet, en wat krijg je uiteindelijk geleverd? Hieronder het complete overzicht.</p>
<h2>Wat kost een drone video?</h2>
<p>Bij Skyline Digital kost een <a href="/drone-video">video-shoot op locatie €250</a>; met drone-opnames erbij €300. Daar zit de opname met professionele apparatuur, de montage en de kleurcorrectie in. Een complete cinematische bedrijfsfilm of villa-film offreren we op maat, afhankelijk van de lengte, het aantal locaties en of er voice-over of muziek met licentie bij moet.</p>
<p>Ter vergelijking: in de markt zie je voor losse drone-opnames €150 tot €500 per dagdeel, en voor volledige bedrijfsfilms €1.500 tot €10.000. De grote verschillen zitten in montage, aantal draaidagen en of er een crew meekomt.</p>
<h2>Welke regels gelden in Nederland?</h2>
<p>Sinds 2021 gelden de Europese droneregels. Voor commerciële opnames met een drone onder de 25 kg vlieg je meestal in de "open categorie" (A1, A2 of A3). De piloot heeft een registratie en een vliegbewijs, en de drone is voorzien van een operatornummer.</p>
<ul>
<li><strong>No-fly zones:</strong> rond vliegvelden en militaire terreinen mag je niet vliegen. In Brabant geldt dat bijvoorbeeld rond Eindhoven Airport, Volkel en Gilze-Rijen. We checken vooraf altijd de officiële kaart.</li>
<li><strong>Maximale hoogte:</strong> 120 meter boven de grond.</li>
<li><strong>Mensen:</strong> niet boven mensenmassa's en afhankelijk van de drone op afstand van omstanders.</li>
<li><strong>Privacy:</strong> buren en voorbijgangers niet herkenbaar in beeld zonder toestemming — belangrijk bij villa-films in woonwijken.</li>
</ul>
<p>Het belangrijkste voor jou als opdrachtgever: werk met een piloot die deze regels kent en vooraf de locatie beoordeelt. Dan weet je zeker dat de beelden ook gebruikt mogen worden.</p>
<h2>Hoe verloopt een shoot?</h2>
<ol>
<li><strong>Intake:</strong> doel van de film, locatie, wensen en voorbeelden. We adviseren over het beste tijdstip (vaak het "gouden uur" vlak na zonsopgang of voor zonsondergang).</li>
<li><strong>Locatiecheck:</strong> luchtruim, vergunningen, weersverwachting.</li>
<li><strong>Opnamedag:</strong> drone- en grondopnames in één dagdeel. Voor villa's filmen we ook de binnenruimtes met gestabiliseerde camera.</li>
<li><strong>Montage:</strong> selectie, kleurcorrectie, muziek, eventueel logo en tekst. Binnen één tot twee weken klaar.</li>
<li><strong>Levering:</strong> horizontale versie voor website en YouTube, verticale versie voor Instagram en TikTok.</li>
</ol>
<h2>Waarvoor gebruik je dronebeelden?</h2>
<p>Vastgoed en villa's (bekijk onze <a href="/portfolio#videos">villa-films in Moraira en Jávea</a>), bedrijfspanden en terreinen, bouwvoortgang, evenementen, horeca met buitenlocatie en recreatie. Combineer de drone-opnames met een <a href="/website-seo">snelle website</a> en je hebt een homepage die bezoekers direct vasthoudt.</p>
<h2>Eerst een voorbeeld zien?</h2>
<p>Voor villa-eigenaren en makelaars maken we eerst een <a href="/video?v=modern-villa-moraira">gratis voorbeeld gericht op jouw woning</a>. Zo zie je de stijl voordat je beslist.</p>
"""),
 dict(slug="lokale-seo-tips", title="Lokale SEO: zo word je gevonden in Den Bosch en omgeving", eyebrow="SEO", read="8 min", img="photo-phone-city.jpg",
      desc="Lokale SEO voor ondernemers in Den Bosch en Brabant: Google Bedrijfsprofiel, reviews, locatiepagina's, NAP-gegevens, structured data en snelheid. Praktische tips die direct werken.",
      body="""
<p class="lead">De meeste klanten van een lokaal bedrijf zoeken op "dienst + plaats": <em>fysiotherapeut Rosmalen</em>, <em>schilder Den Bosch</em>, <em>restaurant Vught</em>. Lokale SEO is alles wat je doet om bij die zoekopdrachten bovenaan te staan — in de kaartresultaten én in de normale resultaten. Dit zijn de stappen die het meeste opleveren.</p>
<h2>1. Claim en vul je Google Bedrijfsprofiel volledig in</h2>
<p>Het gratis Google Bedrijfsprofiel (voorheen Google Mijn Bedrijf) bepaalt of je in de kaart met drie resultaten verschijnt. Vul álles in: categorie, openingstijden, diensten, foto's, een beschrijving met je belangrijkste zoekwoorden en een link naar je website. Plaats regelmatig updates en beantwoord vragen.</p>
<h2>2. Verzamel reviews — en reageer erop</h2>
<p>Aantal, gemiddelde en recentheid van reviews wegen zwaar mee. Vraag elke tevreden klant actief om een review (stuur een directe link), en reageer op elke review, ook de kritische. Dat laat Google én nieuwe klanten zien dat je actief bent.</p>
<h2>3. Zorg voor consistente NAP-gegevens</h2>
<p>NAP staat voor Name, Address, Phone. Zorg dat je bedrijfsnaam, adres en telefoonnummer overal exact hetzelfde zijn: website, Google, Facebook, KVK-vermeldingen, branchegidsen. Kleine verschillen ("straat" versus "str.") verwarren zoekmachines.</p>
<h2>4. Maak locatiepagina's met echte inhoud</h2>
<p>Werk je in meerdere plaatsen? Maak per plaats een pagina met unieke tekst: welke wijken, welke klanten, hoe je bereikbaar bent, lokale voorbeelden. Kopieer niet dezelfde tekst met alleen de plaatsnaam vervangen — dat herkent Google en het levert niets op. Bekijk ter voorbeeld onze pagina's voor <a href="/website-laten-maken-den-bosch">Den Bosch</a>, <a href="/website-laten-maken-rosmalen">Rosmalen</a> en <a href="/website-laten-maken-oss">Oss</a>.</p>
<h2>5. Gebruik structured data (schema.org)</h2>
<p>Met LocalBusiness-structured data vertel je Google in code wie je bent, waar je zit, wanneer je open bent en welke diensten je levert. Het kost niets en maakt je zichtbaar voor uitgebreide zoekresultaten. Ook FAQ-structured data op pagina's met veelgestelde vragen werkt goed.</p>
<h2>6. Maak je website snel en mobiel</h2>
<p>Lokale zoekers zitten bijna altijd op een telefoon. Een trage site verliest ze vóór ze je telefoonnummer zien. Comprimeer afbeeldingen, beperk scripts en zorg dat de belangrijkste informatie bovenaan staat. Onze <a href="/website-seo">websites worden gebouwd op snelheid</a>, precies hierom.</p>
<h2>7. Lokale links en vermeldingen</h2>
<p>Vermeldingen op de site van de ondernemersvereniging, de gemeente, lokale media, leveranciers en sponsoren tellen mee. Ze bevestigen dat je echt in die plaats actief bent.</p>
<h2>8. Content over je regio</h2>
<p>Schrijf over projecten in de buurt, lokale evenementen waar je bij was, of veelgestelde vragen van klanten uit jouw stad. Het is de meest natuurlijke manier om plaatsnamen en diensten te combineren.</p>
<h2>9. Meet wat werkt</h2>
<p>Google Search Console laat gratis zien op welke zoekwoorden je gevonden wordt en op welke positie. Het Bedrijfsprofiel toont hoeveel mensen bellen of de route opvragen. Kijk er maandelijks naar en stuur bij.</p>
<h2>Hulp nodig?</h2>
<p>Met ons <a href="/pricing">SEO-abonnement van €39 per maand</a> nemen we dit uit handen: technische optimalisatie, zoekwoorden, content en maandelijks een rapportage. Of begin met een <a href="/contact">gratis adviesgesprek</a>.</p>
"""),
 dict(slug="wat-is-een-cinematic-scroll-website", title="Wat is een cinematic scroll website — en wanneer is het slim?", eyebrow="Webdesign", read="5 min", img="photo-studio-monitor.jpg",
      desc="Een cinematic scroll website speelt een film af terwijl de bezoeker scrolt. Lees hoe het werkt, wat het kost (vanaf €749), wat het doet voor je merk en wanneer je er beter niet voor kiest.",
      body="""
<p class="lead">Je hebt ze vast gezien bij Apple of bij premium automerken: je scrolt, en een product draait, opent of vliegt door beeld alsof je een film bestuurt. Dat heet een cinematic scroll website (ook wel scroll-driven video of scrollytelling). Onze eigen <a href="/">homepage</a> werkt zo. Hieronder leggen we uit hoe het werkt en voor wie het de investering waard is.</p>
<h2>Hoe werkt het technisch?</h2>
<p>Een korte film wordt opgeknipt in losse beelden (frames). Terwijl je scrolt, bepaalt je scrollpositie welk frame er getoond wordt. Scrol je terug, dan speelt de film achteruit. Omdat het geen video-element is maar losse beelden op een canvas, voelt het direct en soepel — ook op mobiel, mits het goed gebouwd is.</p>
<p>Tekst en knoppen worden op vaste momenten in de film getoond. Daar vertragen we het scrollen iets, zodat je de boodschap rustig leest voordat de film verder gaat.</p>
<h2>Wat doet het voor je merk?</h2>
<ul>
<li><strong>Aandacht:</strong> bezoekers blijven langer en scrollen verder, omdat ze willen zien wat er gebeurt.</li>
<li><strong>Positionering:</strong> het straalt premium uit. Voor villa's, exclusieve producten, architectuur, auto's en bureaus die kwaliteit verkopen, is dat precies het punt.</li>
<li><strong>Verhaal:</strong> je leidt de bezoeker in een vaste volgorde door je boodschap, in plaats van dat hij willekeurig klikt.</li>
</ul>
<h2>Wanneer kies je er beter niet voor?</h2>
<p>Als bezoekers vooral snel iets moeten regelen — een afspraak boeken, een prijs vinden, bellen — zet je het effect alleen op de homepage of helemaal niet. Een huisartsenpraktijk heeft er weinig aan; een villa-makelaar of designstudio juist veel. Ook bij een heel beperkt budget voor beeld is een strakke <a href="/website-seo">multipage website</a> de betere keuze.</p>
<h2>Wat kost een cinematic scroll website?</h2>
<p>Bij ons kost een <a href="/pricing">3D cinematic website €749</a>, inclusief beeldmateriaal: we genereren of filmen de film, bouwen het scroll-effect en zetten de rest van de site erachter. Elders zie je voor dit soort sites vaak bedragen van €5.000 of meer, omdat het handmatig animatiewerk is. Wij hebben er een vaste werkwijze voor ontwikkeld.</p>
<h2>Heeft het invloed op SEO en snelheid?</h2>
<p>Alleen als het slecht gebouwd is. Wij laden de beelden slim (eerst de frames die je direct ziet, daarna de rest), houden de bestandsgrootte laag en zorgen dat alle tekst gewoon in de HTML staat. Daardoor kan Google de pagina normaal lezen en blijft de site snel.</p>
<h2>Zelf ervaren?</h2>
<p>Scrol door onze <a href="/">homepage</a> of bekijk de <a href="/portfolio">voorbeelden in het portfolio</a>. En wil je weten hoe het er voor jouw bedrijf uitziet: vraag een <a href="/aanvraag">gratis testwebsite</a> aan.</p>
"""),
]

def head(title, desc, url, og, ld, extra=""):
    t = html.escape(title, quote=True); d = html.escape(desc, quote=True)
    return f'''<!DOCTYPE html>
<html lang="nl">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{t}</title>
  <meta name="description" content="{d}" />
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="{'article' if '/kennisbank/' in url else 'website'}" />
  <meta property="og:locale" content="nl_NL" />
  <meta property="og:site_name" content="Skyline Digital" />
  <meta property="og:title" content="{t}" />
  <meta property="og:description" content="{d}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{BASE}{og}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{t}" />
  <meta name="twitter:description" content="{d}" />
  <meta name="twitter:image" content="{BASE}{og}" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False, separators=(",",":"))}</script>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400..900&family=Inter:wght@400..700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/styles.css" />
  <link rel="stylesheet" href="/pages.css" />
  <link rel="stylesheet" href="/awards.css" />
  <link rel="icon" href="/assets/favicon.svg" type="image/svg+xml" />
  <link rel="apple-touch-icon" href="/assets/favicon.svg" />
  <meta name="theme-color" content="#07080b" />{extra}
</head>
<body>
'''
ORG_REF = {"@id": BASE + "/#organization"}
def crumbs_ld(url, items):
    lst = [{"@type":"ListItem","position":1,"name":"Home","item":BASE+"/"}]
    for i,(n,u) in enumerate(items, 2): lst.append({"@type":"ListItem","position":i,"name":n,"item":u})
    return {"@type":"BreadcrumbList","@id":url+"#breadcrumb","itemListElement":lst}
def faq_ld(url, faqs):
    return {"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":re.sub(r'<[^>]+>','',a)}} for q,a in faqs]}
def faq_html(faqs):
    return '<div class="faq reveal">' + "".join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in faqs) + '</div>'
def tail():
    return FOOTER + '\n  <script src="/scroll-cinematic.js"></script>\n</body>\n</html>\n'
def rows(items):
    out = '<div class="rows">'
    for i,(h,p) in enumerate(items,1):
        out += f'<div class="row reveal"><span class="row-num">{i:02d}</span><div class="row-body"><h3>{h}</h3><p>{p}</p></div>{ARROW}</div>'
    return out + '</div>'

# ---------- Locatiepagina's ----------
for c in CITIES:
    slug = f"website-laten-maken-{c['slug']}"; url = f"{BASE}/{slug}"
    title = f"Website laten maken {c['name']} — vanaf €499 | Skyline Digital"
    desc = f"Website laten maken {c['in_']}? Skyline Digital bouwt snelle maatwerk websites vanaf €499 voor ondernemers in {c['full']} en omgeving. SEO inbegrepen. Vraag gratis een testwebsite aan."
    near = [CITY_BY[n] for n in c["near"]]
    faqs = [
      (f"Wat kost een website laten maken {c['in_']}?", f"Een maatwerk multipage website kost bij ons €499 eenmalig, een 3D cinematic website €749. SEO is optioneel voor €39 per maand. Die prijzen gelden voor ondernemers {c['in_']} net zo goed als in de rest van Nederland — bekijk de <a href=\"/pricing\" style=\"color:var(--gold-deep)\">pricing</a>."),
      (f"Komen jullie langs {c['in_']}?", f"Ja. {c['travel']} De kennismaking doen we op jouw locatie, bij ons in Den Bosch of via een videogesprek — wat jij prettig vindt."),
      (f"Hoe word ik beter gevonden in Google {c['in_']}?", f"Door een snelle site met goede teksten, een volledig Google Bedrijfsprofiel, reviews en een pagina die specifiek over {c['full']} gaat. Dat zetten we bij de bouw meteen goed; met het SEO-abonnement houden we het daarna bij."),
      ("Hoe lang duurt het?", "Een multipage website staat meestal binnen twee tot vier weken online, afhankelijk van hoe snel we teksten en beeld ontvangen. Een gratis testwebsite laten we je vaak al binnen een paar dagen zien."),
    ]
    ld = {"@context":"https://schema.org","@graph":[
        crumbs_ld(url, [("Regio's", BASE+"/regio"), (f"Website laten maken {c['name']}", url)]),
        {"@type":"Service","@id":url+"#service","name":f"Website laten maken {c['in_']}","serviceType":"Webdesign en websiteontwikkeling","provider":ORG_REF,
         "areaServed":{"@type":"City","name":c["full"],"containedInPlace":{"@type":"AdministrativeArea","name":c["region"]}},"url":url,
         "offers":[{"@type":"Offer","name":"Multipage website","price":"499","priceCurrency":"EUR"},{"@type":"Offer","name":"3D Cinematic website","price":"749","priceCurrency":"EUR"}]},
        faq_ld(url, faqs),
        {"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"about":ORG_REF,"breadcrumb":{"@id":url+"#breadcrumb"}}]}
    sectors = "".join(f"<li>{s[0].upper()+s[1:]}</li>" for s in c["sectors"])
    nearlinks = ", ".join(f'<a href="/website-laten-maken-{n["slug"]}">{n["name"]}</a>' for n in near)
    body = HEADER + f'''
  <section class="page-hero has-image">
    <div class="page-hero-bg"><img src="/assets/photo-laptop-desk.jpg" alt="Website laten maken {c['in_']} — Skyline Digital" /></div>
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · <a href="/regio">Regio's</a> · {c['name']}</p>
      <h1>Website laten maken <span class="gold-text">{c['in_']}.</span></h1>
      <p class="lead">Maatwerk websites vanaf €499 voor ondernemers in {c['full']} en omgeving. Snel, vindbaar in Google en gebouwd om klanten op te leveren — door een bureau uit Den Bosch.</p>
      <div class="hero-actions"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite</a><a href="/portfolio" class="btn btn-ghost-light">Bekijk ons werk</a></div>
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="frow">
        <div class="frow-media reveal reveal--left"><div class="media-frame"><img src="/assets/photo-sketch.jpg" alt="Ontwerpschets van een website voor een ondernemer {c['in_']}" loading="lazy" /></div></div>
        <div class="frow-copy reveal reveal--right">
          <div class="gold-rule"></div>
          <p class="eyebrow">Webdesign {c['name']}</p>
          <h2>Een website die past bij <span class="gold-text">{c['full']}.</span></h2>
          <p class="lead">{c['intro']}</p>
          <p>{c['intro2']}</p>
          <a href="/aanvraag" class="btn btn-dark">Start je project</a>
        </div>
      </div>
    </div>
  </section>

  <section class="bg-dark full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Voor wie</p>
        <h2>Websites voor ondernemers <span class="gold-text">{c['in_']}</span></h2>
        <p class="lead">We bouwen voor allerlei sectoren in {c['full']}, onder andere voor:</p>
      </div>
      <ul class="checks" style="max-width:720px">{sectors}</ul>
      <p style="margin-top:28px;max-width:720px;color:var(--on-dark-dim)">Klanten uit {c['places']} vinden je via Google — en via een site die op elke telefoon snel laadt.</p>
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Wat je krijgt</p>
        <h2>Alles wat een website <span class="gold-text">moet kunnen.</span></h2>
      </div>
      {rows([
        ("Maatwerk ontwerp", f"Geen template: een ontwerp rond jouw merk en jouw klanten {c['in_']}."),
        ("Razendsnel en mobiel-first", "Groene PageSpeed-scores op mobiel — goed voor bezoekers én voor Google."),
        ("Lokale SEO ingebouwd", f"Titels, teksten, structured data en een Google Bedrijfsprofiel-koppeling gericht op {c['full']}."),
        ("Zelf te beheren", "Een eenvoudig CMS plus uitleg, zodat je teksten en foto's zelf aanpast."),
        ("Beeld en video", "Optioneel eigen foto-, video- en drone-opnames op jouw locatie, of AI-content in jouw stijl."),
        ("Eén aanspreekpunt", "Van ontwerp tot oplevering één contactpersoon, korte lijnen en heldere prijzen."),
      ])}
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Veelgestelde vragen</p>
        <h2>Website laten maken {c['in_']}: <span class="gold-text">goed om te weten</span></h2>
      </div>
      {faq_html(faqs)}
      <p style="margin-top:40px;text-align:center;color:var(--ink-dim)">Ook actief in {nearlinks} · <a href="/regio">alle regio's</a></p>
    </div>
  </section>

  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Eerst zien, dan beslissen.</h2>
      <p class="lead">We bouwen gratis een testwebsite voor jouw bedrijf {c['in_']}. Bevalt het? Dan gaan we door. Zo niet, dan kost het je niets.</p>
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite aanvragen</a><a href="/contact" class="btn btn-ghost-light">Plan een gesprek</a></div>
    </div>
  </section>

'''
    open(slug + ".html", "w").write(head(title, desc, url, "/assets/photo-laptop-desk.jpg", ld) + body + tail())

# ---------- Regio-hub ----------
url = BASE + "/regio"; title = "Website laten maken in Brabant en omgeving — regio's | Skyline Digital"
desc = "Skyline Digital bouwt websites, video en content voor ondernemers in Den Bosch, Rosmalen, Vught, Oss, Eindhoven, Tilburg, Breda, Nijmegen, Waalwijk en Uden. Bekijk je regio."
ld = {"@context":"https://schema.org","@graph":[crumbs_ld(url,[("Regio's",url)]),
      {"@type":"ItemList","@id":url+"#list","itemListElement":[{"@type":"ListItem","position":i+1,"name":f"Website laten maken {c['name']}","url":f"{BASE}/website-laten-maken-{c['slug']}"} for i,c in enumerate(CITIES)]},
      {"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"breadcrumb":{"@id":url+"#breadcrumb"}}]}
body = HEADER + f'''
  <section class="page-hero center" style="background:radial-gradient(90% 100% at 50% 0%, #16171f, #07080c)">
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · Regio's</p>
      <h1>Actief in Den Bosch <span class="gold-text">en ver daarbuiten.</span></h1>
      <p class="lead">Ons kantoor staat in 's-Hertogenbosch. Van daaruit bouwen we websites, films en content voor ondernemers in heel Brabant, Gelderland en de rest van Nederland.</p>
    </div>
  </section>
  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Kies je plaats</p>
        <h2>Website laten maken <span class="gold-text">in jouw regio</span></h2>
      </div>
      {rows([(f'<a href="/website-laten-maken-{c["slug"]}" style="color:inherit;text-decoration:none">Website laten maken {c["name"]}</a>', c["intro"].split(". ")[0] + ".") for c in CITIES])}
      <p style="margin-top:40px;color:var(--ink-dim)">Staat jouw plaats er niet bij? We werken door heel Nederland en op afstand — <a href="/contact">neem contact op</a>.</p>
    </div>
  </section>
  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Zien hoe jouw bedrijf eruit kan zien?</h2>
      <p class="lead">Vraag een gratis testwebsite aan — je ziet eerst het resultaat, dan beslis je.</p>
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite</a><a href="/pricing" class="btn btn-ghost-light">Bekijk pricing</a></div>
    </div>
  </section>

'''
open("regio.html","w").write(head(title, desc, url, "/assets/og-home.jpg", ld) + body + tail())

# ---------- Kennisbank ----------
os.makedirs("kennisbank", exist_ok=True)
for a in ARTICLES:
    url = f"{BASE}/kennisbank/{a['slug']}"; og = f"/assets/{a['img']}"
    ld = {"@context":"https://schema.org","@graph":[
        crumbs_ld(url, [("Kennisbank", BASE+"/kennisbank"), (a["title"], url)]),
        {"@type":"Article","@id":url+"#article","headline":a["title"],"description":a["desc"],"image":BASE+og,"datePublished":TODAY,"dateModified":TODAY,
         "author":{"@type":"Person","name":"Yannick van den Broek","url":BASE+"/over-ons"},"publisher":ORG_REF,"mainEntityOfPage":url,"inLanguage":"nl-NL"},
        {"@type":"WebPage","@id":url+"#webpage","url":url,"name":a["title"],"description":a["desc"],"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"breadcrumb":{"@id":url+"#breadcrumb"}}]}
    others = [o for o in ARTICLES if o is not a][:3]
    body = HEADER + f'''
  <section class="page-hero has-image">
    <div class="page-hero-bg"><img src="{og}" alt="{html.escape(a['title'])}" /></div>
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · <a href="/kennisbank">Kennisbank</a> · {a['eyebrow']}</p>
      <h1>{a['title']}</h1>
      <p class="lead">{a['eyebrow']} · {a['read']} leestijd · door Yannick van den Broek</p>
    </div>
  </section>
  <section class="bg-white full">
    <div class="wrap-sm">
      <article class="article">
{a['body']}
      </article>
      <div class="article-more">
        <h2>Verder lezen</h2>
        {rows([(f'<a href="/kennisbank/{o["slug"]}" style="color:inherit;text-decoration:none">{o["title"]}</a>', o["desc"]) for o in others])}
      </div>
    </div>
  </section>
  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Liever gewoon zien wat het oplevert?</h2>
      <p class="lead">Vraag een gratis testwebsite aan of plan een vrijblijvend gesprek.</p>
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite</a><a href="/contact" class="btn btn-ghost-light">Plan een gesprek</a></div>
    </div>
  </section>

'''
    open(f"kennisbank/{a['slug']}.html","w").write(head(a["title"] + " | Skyline Digital", a["desc"], url, og, ld) + body + tail())

url = BASE + "/kennisbank"; title = "Kennisbank: websites, SEO, video & content | Skyline Digital"
desc = "Praktische artikelen over website laten maken, kosten, lokale SEO, drone video en cinematic webdesign — geschreven door Skyline Digital uit Den Bosch."
ld = {"@context":"https://schema.org","@graph":[crumbs_ld(url,[("Kennisbank",url)]),
      {"@type":"CollectionPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"breadcrumb":{"@id":url+"#breadcrumb"},
       "hasPart":[{"@type":"Article","headline":a["title"],"url":f"{BASE}/kennisbank/{a['slug']}"} for a in ARTICLES]}]}
body = HEADER + f'''
  <section class="page-hero center" style="background:radial-gradient(90% 100% at 50% 0%, #16171f, #07080c)">
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · Kennisbank</p>
      <h1>Kennis die je <span class="gold-text">verder helpt.</span></h1>
      <p class="lead">Eerlijke artikelen over websites, prijzen, SEO en video — zonder verkooppraat, met de cijfers erbij.</p>
    </div>
  </section>
  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Artikelen</p>
        <h2>Lees <span class="gold-text">verder</span></h2>
      </div>
      {rows([(f'<a href="/kennisbank/{a["slug"]}" style="color:inherit;text-decoration:none">{a["title"]}</a>', a["desc"]) for a in ARTICLES])}
    </div>
  </section>
  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Vragen over jouw situatie?</h2>
      <p class="lead">Plan een gratis adviesgesprek — we denken graag mee.</p>
      <div class="hero-actions hero-actions-center"><a href="/contact" class="btn btn-gold">Plan een gesprek</a><a href="/pricing" class="btn btn-ghost-light">Bekijk pricing</a></div>
    </div>
  </section>

'''
open("kennisbank.html","w").write(head(title, desc, url, "/assets/og-home.jpg", ld) + body + tail())

# ---------- Footer op alle pagina's: Regio's + Kennisbank ----------
NEW_COL = '''        <div class="footer-col">
          <h4>Regio's</h4>
''' + "".join(f'          <a href="/website-laten-maken-{c["slug"]}">Website laten maken {c["name"]}</a>\n' for c in CITIES[:8]) + '''          <a href="/regio">Alle regio's</a>
        </div>
'''
for path in glob.glob("*.html") + glob.glob("kennisbank/*.html"):
    if path.startswith("google"): continue
    s = open(path).read()
    if "Website laten maken Den Bosch</a>" in s: continue
    s = re.sub(r'        <div class="footer-col">\n          <h4>Over ons</h4>.*?</div>\n', NEW_COL, s, count=1, flags=re.S)
    s = s.replace('          <a href="/aanvraag" class="footer-gratis">★ Gratis testwebsite</a>', '          <a href="/kennisbank">Kennisbank</a>\n          <a href="/aanvraag" class="footer-gratis">★ Gratis testwebsite</a>', 1)
    # relatieve assets in footer/nav werken niet vanuit /kennisbank/ — maak ze absoluut
    if path.startswith("kennisbank/"):
        s = s.replace('src="assets/', 'src="/assets/')
    open(path, "w").write(s)

# ---------- Sitemap ----------
urls = [("/",1.0,"weekly"),("/website-seo",0.9,"monthly"),("/drone-video",0.9,"monthly"),("/social-media",0.9,"monthly"),("/ai-content",0.9,"monthly"),
        ("/pricing",0.8,"monthly"),("/portfolio",0.8,"monthly"),("/over-ons",0.7,"monthly"),("/contact",0.7,"yearly"),("/aanvraag",0.8,"yearly"),
        ("/regio",0.7,"monthly"),("/kennisbank",0.7,"weekly")]
urls += [(f"/website-laten-maken-{c['slug']}",0.8,"monthly") for c in CITIES]
urls += [(f"/kennisbank/{a['slug']}",0.7,"monthly") for a in ARTICLES]
urls += [(f"/werk-{w}",0.5,"yearly") for w in ["dekgro","lillis","bodyscan","echtgrieks"]]
urls += [("/privacybeleid",0.2,"yearly"),("/algemene-voorwaarden",0.2,"yearly"),("/cookiebeleid",0.2,"yearly")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u,p,f in urls:
    sm += f'  <url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority></url>\n'
open("sitemap.xml","w").write(sm + "</urlset>\n")
print("pages:", len(CITIES)+len(ARTICLES)+2, "sitemap urls:", len(urls))
