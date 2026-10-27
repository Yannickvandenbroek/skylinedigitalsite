import re, json, html, os, glob
os.chdir("/Users/yannickvandenbroek/Documents/Skylinedigital/own site/skyline-digital")
BASE = "https://www.skylinedigital.nl"
TODAY = "2026-10-06"
src = open("website-seo.html").read()
HEADER = re.search(r'  <header class="nav".*?</header>\n', src, re.S).group(0)
HEADER = re.sub(r' aria-current="page"', '', HEADER)
BLOG_HEADER = HEADER.replace('<a href="/blog">Blog</a>', '<a href="/blog" aria-current="page">Blog</a>', 1)
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
 # --- nieuw sinds 2026-10-27 ---
 dict(slug="veghel", name="Veghel", full="Veghel", in_="in Veghel", region="Noord-Brabant",
      intro="Veghel is het economische hart van de gemeente Meierijstad. Grote namen als Vanderlande, Mars en het hoofdkantoor van Jumbo zitten hier, en langs de Zuid-Willemsvaart groeit een sterk MKB van toeleveranciers, installateurs en dienstverleners. Een website laten maken in Veghel betekent voor ons: een site die professioneel genoeg is voor die zakelijke omgeving en die lokaal goed gevonden wordt.",
      intro2="Vanuit Den Bosch zijn we in twintig minuten in Veghel. We bouwen voor bedrijven op Doornhoek en De Dubbelen, voor winkels en horeca in het centrum en voor ondernemers in Erp, Eerde en Zijtaart.",
      sectors=["toeleveranciers en maakindustrie", "logistiek en techniek", "bouw- en installatiebedrijven", "winkels en horeca in het centrum"],
      places="het centrum, Doornhoek, De Dubbelen, Erp, Eerde, Mariaheide en Zijtaart", near=["uden","schijndel","den-bosch"], travel="Veghel ligt op twintig minuten van ons kantoor via de A50."),
 dict(slug="schijndel", name="Schijndel", full="Schijndel", in_="in Schijndel", region="Noord-Brabant",
      intro="Schijndel is een van de grotere kernen van Meierijstad, met een levendig centrum, veel familiebedrijven en een sterk verenigingsleven. Hier kennen klanten elkaar en is mond-tot-mondreclame belangrijk. Een goede website zorgt dat die aanbeveling ook online klopt: wie je naam googelt, ziet direct wat je doet en hoe hij je bereikt.",
      intro2="We bouwen voor ondernemers in Schijndel, Wijbosch en het buitengebied, van bouw- en klusbedrijven tot winkels, kappers en zorgpraktijken. Vanuit Den Bosch zijn we er in twintig minuten.",
      sectors=["familiebedrijven in bouw en techniek", "winkels, kappers en horeca", "zorg- en beautypraktijken", "agrarische en groene bedrijven"],
      places="het centrum, Wijbosch en het buitengebied richting Sint-Oedenrode en Boxtel", near=["veghel","boxtel","den-bosch"], travel="Schijndel ligt op twintig minuten van ons kantoor."),
 dict(slug="boxtel", name="Boxtel", full="Boxtel", in_="in Boxtel", region="Noord-Brabant",
      intro="Boxtel ligt op een knooppunt: aan de A2, met een intercitystation en de Dommel en natuurgebied Kampina om de hoek. Dat trekt zowel bedrijven als bezoekers. Een website laten maken in Boxtel betekent voor ons een site die past bij de lokale ondernemer en die ook bezoekers uit de regio weet te bereiken.",
      intro2="Vanuit Den Bosch zijn we in een kwartier in Boxtel. We bouwen voor ondernemers in het centrum, in Lennisheuvel, Liempde en Esch, van horeca en recreatie tot bouw, techniek en zakelijke dienstverlening.",
      sectors=["horeca, recreatie en toerisme", "bouw, techniek en installatie", "zakelijke dienstverlening", "winkels in het centrum"],
      places="het centrum, Lennisheuvel, Liempde, Esch en het buitengebied rond Kampina", near=["den-bosch","schijndel","vught"], travel="Boxtel ligt op een kwartier van ons kantoor via de A2."),
 dict(slug="sint-michielsgestel", name="Sint-Michielsgestel", full="Sint-Michielsgestel", in_="in Sint-Michielsgestel", region="Noord-Brabant",
      intro="Sint-Michielsgestel is een groene gemeente vlak naast Den Bosch, met Berlicum, Den Dungen, Gemonde en Middelrode als eigen kernen. Er zitten veel zelfstandigen, familiebedrijven en ondernemers met een vaste klantenkring. Een website laten maken in Sint-Michielsgestel betekent voor ons: een verzorgde site die vertrouwen geeft en lokaal goed te vinden is.",
      intro2="We zitten op tien minuten rijden. Een kennismaking aan de keukentafel of in je bedrijf is dus zo geregeld, net als een foto- of videoshoot op locatie.",
      sectors=["zzp'ers en familiebedrijven", "bouw, tuin en installatie", "zorg, coaching en beauty", "horeca en recreatie"],
      places="Sint-Michielsgestel, Berlicum, Den Dungen, Gemonde en Middelrode", near=["den-bosch","vught","boxtel"], travel="Sint-Michielsgestel ligt op tien minuten van ons kantoor."),
 dict(slug="zaltbommel", name="Zaltbommel", full="Zaltbommel", in_="in Zaltbommel", region="Gelderland",
      intro="Zaltbommel is een historische vestingstad aan de Waal, met de Martinus Nijhoffbrug en de A2 als snelle verbinding naar Den Bosch en Utrecht. In de Bommelerwaard zitten veel bedrijven in transport, bouw, tuinbouw en recreatie. Een website laten maken in Zaltbommel betekent voor ons een site die zowel lokale klanten als zakelijke relaties langs de A2 aanspreekt.",
      intro2="Vanuit Den Bosch zijn we in twintig minuten in Zaltbommel. We bouwen voor ondernemers in de binnenstad, op de bedrijventerreinen en in de dorpen van de Bommelerwaard.",
      sectors=["transport en logistiek langs de A2", "bouw, installatie en techniek", "tuinbouw en agrarische bedrijven", "horeca, winkels en recreatie in de vestingstad"],
      places="de historische binnenstad, Brakel, Nederhemert, Zuilichem en de rest van de Bommelerwaard", near=["den-bosch","drunen","vught"], travel="Zaltbommel ligt op twintig minuten van ons kantoor via de A2."),
 dict(slug="drunen", name="Drunen", full="Drunen", in_="in Drunen", region="Noord-Brabant",
      intro="Drunen is de grootste kern van de gemeente Heusden, aan de rand van de Loonse en Drunense Duinen. Samen met Vlijmen, Nieuwkuijk en vestingstadje Heusden vormt het een gemeente met veel MKB, bouw- en installatiebedrijven en recreatie. Een website laten maken in Drunen betekent voor ons een site die in de hele gemeente Heusden gevonden wordt.",
      intro2="Vanuit Den Bosch zijn we in een kwartier in Drunen. We bouwen voor ondernemers in Drunen, Vlijmen, Nieuwkuijk, Elshout en Heusden, van aannemers en installateurs tot horeca rond de Duinen.",
      sectors=["bouw-, klus- en installatiebedrijven", "horeca en recreatie rond de Duinen", "winkels en dienstverlening", "transport en groothandel"],
      places="Drunen, Vlijmen, Nieuwkuijk, Elshout, Haarsteeg en Heusden", near=["den-bosch","waalwijk","vught"], travel="Drunen ligt op een kwartier van ons kantoor."),
 dict(slug="helmond", name="Helmond", full="Helmond", in_="in Helmond", region="Noord-Brabant",
      intro="Helmond is een industriestad in beweging: van textiel en metaal naar automotive en slimme maakindustrie, met de Automotive Campus als zichtbaar middelpunt. Daarnaast groeit de stad met wijken als Brandevoort en Dierdonk. Een website laten maken in Helmond betekent voor ons een site die past bij die technische, ondernemende stad.",
      intro2="We komen vanuit Den Bosch naar Helmond voor een kennismaking op locatie, of spreken af via video. We bouwen voor technische bedrijven, installateurs, winkels en horeca in het centrum en voor ondernemers in Brandevoort, Stiphout en Mierlo-Hout.",
      sectors=["automotive, techniek en maakindustrie", "installatie- en bouwbedrijven", "winkels en horeca in het centrum", "zorg en dienstverlening in de wijken"],
      places="het centrum, Brandevoort, Dierdonk, Stiphout, Mierlo-Hout en de Automotive Campus", near=["eindhoven","veldhoven","uden"], travel="Helmond ligt op ongeveer drie kwartier van Den Bosch; de kennismaking doen we op locatie of via video."),
 dict(slug="veldhoven", name="Veldhoven", full="Veldhoven", in_="in Veldhoven", region="Noord-Brabant",
      intro="Veldhoven is wereldwijd bekend door ASML, maar er zit veel meer: Máxima MC, bedrijvenpark De Run, congrescentrum NH Koningshof en een groot aantal toeleveranciers en dienstverleners in de high-tech keten. Een website laten maken in Veldhoven betekent voor ons een site die past bij dat hoge niveau, maar die net zo goed werkt voor de lokale ondernemer in Zeelst of Meerveldhoven.",
      intro2="Vanuit Den Bosch zijn we in ruim een half uur in Veldhoven. We bouwen voor high-tech toeleveranciers, zakelijke dienstverleners, zorgpraktijken en winkels en horeca in het centrum.",
      sectors=["high-tech toeleveranciers", "zakelijke en technische dienstverlening", "zorg- en gezondheidspraktijken", "winkels en horeca in het centrum"],
      places="het centrum, Zeelst, Meerveldhoven, Oerle, Veldhoven-Dorp en bedrijvenpark De Run", near=["eindhoven","helmond","tilburg"], travel="Veldhoven ligt op ruim een half uur van ons kantoor via de A2."),
]
CITY_BY = {c["slug"]: c for c in CITIES}

# Per plaats eigen inhoud, zodat de plaatspagina's geen bijna-kopieën van elkaar zijn (Google ziet dat als doorway pages):
# tag = titeltoevoeging met het synoniem dat daar gezocht wordt (Search Console / Keyword Planner), syn = eigen tussenkop + alinea,
# focus = drie lokale aandachtspunten, case = passend project, faq = twee eigen vragen, img = eigen kopfoto.
LOCAL = {
 "den-bosch": dict(tag="webdesign vanaf €499", img="blog-wat-kost-een-website.jpg", who="ondernemers in 's-Hertogenbosch, van de binnenstad tot De Herven",
   syn=("Webdesigner of websitebouwer in Den Bosch?", "Of je nu zoekt op webdesign, een websitebouwer of een internetbureau in Den Bosch: je wilt iemand die ontwerp, techniek en vindbaarheid in één keer goed doet. Bij ons krijg je één vast aanspreekpunt in je eigen stad, en de lokale SEO zetten we meteen bij de bouw goed."),
   focus=[("Bossche zoekwoorden", "Klanten zoeken op 'Den Bosch', ''s-Hertogenbosch' én op wijknamen. We verwerken die varianten natuurlijk in je pagina's, zonder ze erin te proppen."),
          ("Binnenstad of bedrijventerrein", "Een winkel in de binnenstad heeft andere wensen dan een installateur op De Herven: route en openingstijden tegenover werkgebied en offerte-aanvragen. Je site wordt daarop ingericht."),
          ("Even langskomen", "We zitten aan de Bruistensingel. Samen naar het ontwerp kijken kan gewoon bij ons of bij jou op locatie.")],
   case=("Bekijk ons werk", "/portfolio", "In ons portfolio staan websites voor installateurs, schilders, coaches en vakantieverhuur, plus onze films van Brabant tot de Costa Blanca."),
   faq=[("Hebben jullie een kantoor in Den Bosch?", "Ja, we zitten aan de Bruistensingel 500 in 's-Hertogenbosch. Afspreken kan daar, bij jou op locatie of via video."),
        ("Maken jullie ook websites voor Empel, Engelen en De Groote Wielen?", "Zeker. Voor Rosmalen en Vught hebben we eigen pagina's, en ook voor ondernemers in Empel, Engelen en De Groote Wielen bouwen we websites vanuit Den Bosch.")]),
 "rosmalen": dict(tag="webdesigner om de hoek", img="blog-drone-video-vastgoed.jpg", who="ondernemers in Rosmalen, De Groote Wielen en Maliskamp",
   syn=("Webdesign in Rosmalen: dichtbij en snel geschakeld", "Wie in Rosmalen zoekt op webdesign of een webdesigner, wil vaak iemand die snel kan schakelen en de buurt kent. We zitten op tien minuten rijden en bouwen sites die gevonden worden op 'Rosmalen' én in de rest van de gemeente 's-Hertogenbosch."),
   focus=[("Groeiende wijken", "In De Groote Wielen en Maliskamp wonen veel nieuwe gezinnen die online naar lokale diensten zoeken. Een goed Google Bedrijfsprofiel en een snelle site vangen die vraag op."),
          ("Werkgebied duidelijk", "Voor aannemers en installateurs zetten we het werkgebied helder op de site: Rosmalen, Den Bosch, Nuland en omgeving."),
          ("Eigen beeld", "Foto's en video van je eigen projecten werken beter dan stockbeelden. Een shoot op locatie kost €250, met drone €300.")],
   case=("Woningfilm in Rosmalen", "/video?v=woning-rosmalen", "Voor een woning in Rosmalen maakten we een film met binnen- en drone-opnames. Zo laat je in één video zien wat foto's missen."),
   faq=[("Werken jullie ook voor bedrijven in De Groote Wielen?", "Ja. De Groote Wielen hoort bij Rosmalen en de gemeente 's-Hertogenbosch; we zitten er op tien minuten van."),
        ("Kunnen jullie ook foto's en video maken in Rosmalen?", "Ja, we filmen op locatie. Een shoot kost €250, met drone-opnames €300, inclusief montage en kleurcorrectie.")]),
 "vught": dict(tag="webdesign met klasse", img="photo-prints-desk.jpg", who="interieurzaken, makelaars en praktijken in Vught, Cromvoirt en Helvoirt",
   syn=("Webdesign en webshops in Vught", "Vughtse ondernemers zoeken naast een website ook vaak een webshop. Beide bouwen we met dezelfde rust en kwaliteit: een strak ontwerp, snelle pagina's en een bestelproces dat klopt."),
   focus=[("Rust en uitstraling", "Interieurzaken, makelaars en praktijken in Vught verkopen kwaliteit. Veel witruimte, mooie beelden en rustige typografie passen daarbij."),
          ("Vught, Cromvoirt en Helvoirt", "We nemen de plaatsnamen mee waarop je klanten zoeken, zodat je ook in de omliggende kernen gevonden wordt."),
          ("Beeld dat verkoopt", "Voor makelaars en interieurzaken maken we ook foto's, video en dronebeelden.")],
   case=("Schildersbedrijf Lilli's", "/werk-lillis", "Voor schildersbedrijf Lilli's bouwden we een verzorgde site met het vakmanschap centraal: de uitstraling die past bij wonen en interieur in Vught."),
   faq=[("Bouwen jullie ook webshops in Vught?", "Ja, we bouwen ook webshops en koppelingen met bijvoorbeeld je CRM of agenda. De prijs hangt af van het aantal producten en koppelingen; je krijgt vooraf een offerte op maat."),
        ("Valt Helvoirt ook onder jullie werkgebied?", "Ja. Helvoirt hoort sinds 2021 bij de gemeente Vught en ligt, net als Vught zelf, dicht bij ons kantoor.")]),
 "oss": dict(tag="website bouwer vanaf €499", img="blog-cinematic-scroll-website.jpg", who="productiebedrijven, winkels en praktijken in Oss, Berghem en Lith",
   syn=("Website bouwer in Oss, met SEO erbij", "Zoek je een website bouwer in Oss, dan wil je meestal meer dan een mooie site: je wilt dat hij aanvragen oplevert. Daarom zetten we de SEO bij de bouw meteen goed op, en kun je daarna kiezen voor SEO-onderhoud voor €39 per maand."),
   focus=[("Specialismen per pagina", "Productiebedrijven en toeleveranciers willen precies uitleggen wat ze maken. Elke dienst krijgt een eigen pagina, zodat inkopers je vinden op wat je echt doet."),
          ("Werken bij", "Veel Osse bedrijven zoeken personeel. Een goede vacaturepagina met beeld van de werkvloer helpt je opvallen."),
          ("Oss en omgeving", "We richten je vindbaarheid op Oss, Berghem, Lith en de rest van de regio.")],
   case=("Palmyra Coaching in Oss", "/werk-palmyra", "Voor Palmyra Coaching in Oss bouwden we een rustige website die vertrouwen uitstraalt en bezoekers naar een afspraak leidt."),
   faq=[("Hebben jullie al klanten in Oss?", "Ja, onder andere Palmyra Coaching in Oss. Het project staat in ons portfolio."),
        ("Doen jullie ook SEO voor bedrijven in Oss?", "Ja. Bij elke website zetten we de basis-SEO goed. Daarna kun je SEO afnemen voor €39 per maand, met een maandelijkse rapportage.")]),
 "eindhoven": dict(tag="internetbureau vanaf €499", img="photo-studio-monitor.jpg", who="tech, design en MKB in Eindhoven en Brainport",
   syn=("Internetbureau voor Eindhovense ondernemers", "In Eindhoven zoeken veel bedrijven een internetbureau dat design en techniek allebei serieus neemt. Wij combineren maatwerk design met snelle, schone code en, als je wilt, een cinematische scroll-website die opvalt in de designstad."),
   focus=[("Hoog designniveau", "In de stad van de Dutch Design Week valt een standaardtemplate op, en niet positief. Daarom ontwerpen we elke site op maat, met een 3D Cinematic-variant vanaf €749."),
          ("Internationaal publiek", "Werk je met internationale klanten of collega's? We bouwen meertalige websites, zoals onze eigen site in vier talen."),
          ("Techniek en koppelingen", "Calculators, configurators en koppelingen met je systemen, zoals de leasecalculator die we voor CarsLease bouwden.")],
   case=("CarsLease in Eindhoven", "/werk-carslease", "Voor CarsLease in Eindhoven bouwden we een leaseplatform met calculator, zodat bezoekers direct hun maandbedrag zien."),
   faq=[("Werken jullie ook voor bedrijven op Strijp-S of de High Tech Campus?", "Ja. We komen langs in heel Eindhoven; Strijp-S en de High Tech Campus zijn vanuit Den Bosch goed bereikbaar via de A2."),
        ("Kunnen jullie een meertalige website maken?", "Ja. Onze eigen site staat in het Nederlands, Engels, Italiaans en Spaans, met echte vertalingen en de juiste taalkoppelingen voor Google.")]),
 "tilburg": dict(tag="website bouwen vanaf €499", img="photo-studio-loft.jpg", who="logistiek, horeca en creatieve ondernemers in Tilburg",
   syn=("Website bouwen in Tilburg: zo pakken we het aan", "Een website bouwen in Tilburg begint bij ons met een gratis testwebsite. Je ziet eerst hoe je nieuwe site eruitziet; bevalt het, dan bouwen we hem af, met snelle laadtijden en een goede basis voor Google."),
   focus=[("Jong publiek", "Met zoveel studenten en jonge gezinnen moet je site op de telefoon perfect werken. We bouwen mobiel-first."),
          ("Logistiek en B2B", "Voor logistieke bedrijven rond Tilburg draait het om vertrouwen, duidelijke diensten en een goede vacaturepagina."),
          ("Horeca en events", "Agenda, reserveren en sfeerbeelden: voor horeca en evenementen maken we de site én de video.")],
   case=("Bekijk ons portfolio", "/portfolio", "Van installateurs tot vakantieverhuur: in ons portfolio zie je hoe we per branche een andere uitstraling kiezen."),
   faq=[("Werken jullie ook in Berkel-Enschot en Udenhout?", "Ja. Die horen bij de gemeente Tilburg en liggen voor ons op een half uur rijden."),
        ("Maken jullie ook video voor Tilburgse bedrijven?", "Ja. We filmen op locatie voor €250 per shoot, met drone €300, inclusief montage en kleurcorrectie.")]),
 "breda": dict(tag="website bouwen en SEO", img="photo-handshake.jpg", who="horeca, retail en dienstverleners in Breda en omgeving",
   syn=("Website maken in Breda die ook gevonden wordt", "In Breda zijn veel bureaus actief. Het verschil zit in snelheid en vindbaarheid: we bouwen sites die op de telefoon direct laden en die vanaf de eerste dag goed in elkaar zitten voor Google."),
   focus=[("Bourgondisch en verzorgd", "Horeca, food en retail in Breda verkopen beleving. Grote beelden, korte teksten en een duidelijke knop naar reserveren of bestellen."),
          ("Zakelijke dienstverlening", "Adviesbureaus willen vertrouwen wekken: duidelijke diensten, cases en een persoonlijk 'over ons'."),
          ("Prinsenbeek en Teteringen", "We richten je vindbaarheid ook op de kernen rondom Breda, waar veel van je klanten vandaan komen.")],
   case=("Keukenmontage Lassie", "/werk-lassie", "Voor Keukenmontage Lassie bouwden we een cinematische website met scroll-animatie: een voorbeeld van opvallen in een drukke markt."),
   faq=[("Is Breda niet te ver weg voor jullie?", "Nee. Breda ligt op drie kwartier van Den Bosch. De kennismaking doen we op locatie of via video, en de rest gaat net zo snel als bij een bureau om de hoek."),
        ("Kunnen jullie ook drone-opnames maken in Breda?", "Ja, een shoot met drone kost €300. We checken vooraf altijd of er gevlogen mag worden, bijvoorbeeld in verband met vliegbasis Gilze-Rijen.")]),
 "nijmegen": dict(tag="website maken vanaf €499", img="blog-lokale-seo.jpg", who="praktijken, horeca en MKB in Nijmegen en Lent",
   syn=("Webdesign in Nijmegen voor zorg, horeca en MKB", "Wie in Nijmegen een website laat maken, wil opvallen in een drukke online markt. We combineren een helder ontwerp met snelle techniek en lokale vindbaarheid, zodat je gevonden wordt door patiënten, studenten en bedrijven."),
   focus=[("Zorg en praktijken", "Cliënten willen snel weten wat je doet, hoe ze een afspraak maken en of je vergoed wordt. Dat zetten we bovenaan."),
          ("Studentenstad", "Veel bezoekers komen via de telefoon en Instagram. Daarom koppelen we je site aan je social media."),
          ("Beide kanten van de Waal", "We richten je vindbaarheid op Nijmegen én op Lent en Nijmegen-Noord.")],
   case=("BodyScan", "/werk-bodyscan", "Voor BodyScan bouwden we een website die rust uitstraalt en uitlegt hoe een behandeling werkt: het soort site dat ook bij Nijmeegse praktijken past."),
   faq=[("Werken jullie ook voor zorgpraktijken in Nijmegen?", "Ja. We bouwen websites voor praktijken en zorgondernemers, met duidelijke uitleg, afspraakknoppen en een rustige uitstraling."),
        ("Kan mijn website gekoppeld worden aan Instagram?", "Ja. We kunnen je laatste Instagram-posts automatisch op je site tonen, zoals we op onze eigen site doen.")]),
 "waalwijk": dict(tag="webdesigner vanaf €499", img="photo-wall-screen.jpg", who="logistiek, productie en winkels in Waalwijk en De Langstraat",
   syn=("Webdesigner of internetbureau in Waalwijk?", "In Waalwijk wordt veel gezocht op webdesign, een webdesigner of een internetbureau. Bij ons krijg je het beste van beide: één vast aanspreekpunt zoals bij een zelfstandige webdesigner, en ontwerp, techniek, SEO en video onder één dak zoals bij een bureau."),
   focus=[("Logistiek en groothandel", "Bedrijven op Haven Zeven en Haven Acht verkopen vooral aan andere bedrijven. Heldere diensten, certificeringen en een snelle offerte-aanvraag maken het verschil."),
          ("Personeel werven", "In een logistieke regio is een goede vacaturepagina bijna net zo belangrijk als je dienstenpagina."),
          ("De Langstraat", "We richten je site ook op Kaatsheuvel, Sprang-Capelle en Waspik, waar veel van je klanten vandaan komen.")],
   case=("Elektropost", "/werk-elektropost", "Voor installateur Elektropost bouwden we een frisse, persoonlijke site met de diensten duidelijk op een rij: een opzet die ook voor technische bedrijven in Waalwijk werkt."),
   faq=[("Bouwen jullie ook webshops in Waalwijk?", "Ja, ook webshops en koppelingen. De prijs hangt af van het aantal producten en koppelingen; je krijgt vooraf een offerte op maat."),
        ("Werken jullie ook in Kaatsheuvel en Sprang-Capelle?", "Ja. We bouwen voor ondernemers in heel De Langstraat; Kaatsheuvel en Sprang-Capelle liggen vlak bij Waalwijk.")]),
 "uden": dict(tag="webdesign vanaf €499", img="photo-cafe-shoot.jpg", who="winkels, zorgverleners en bouwbedrijven in Uden en Maashorst",
   syn=("Webdesign en websitebouw in Uden", "Of je nu zoekt op webdesign, een websitebouwer of een internetbureau in Uden: je wilt een site die lokaal gevonden wordt en die past bij de kwaliteit die je levert. Daar bouwen we op, met een vaste prijs vanaf €499."),
   focus=[("Winkelstad", "Voor winkels en horeca in het centrum van Uden draait het om openingstijden, route en een Google Bedrijfsprofiel dat klopt."),
          ("Zorg rond Bernhoven", "Praktijken en zorgverleners willen rust en duidelijkheid: wat je doet, voor wie, en hoe iemand een afspraak maakt."),
          ("Maashorst en omgeving", "We richten je site op Uden, Volkel en Odiliapeel, en op Veghel en Oss in de buurt.")],
   case=("De Jonge Elektrotechniek", "/werk-dejonge", "Voor De Jonge Elektrotechniek bouwden we een krachtige site die gevonden wordt op de diensten die ze echt leveren: dezelfde aanpak gebruiken we voor bouw- en technische bedrijven in Uden."),
   faq=[("Werken jullie in de hele gemeente Maashorst?", "Ja. Uden en Landerd zijn in 2022 samengegaan tot Maashorst; we bouwen voor ondernemers in de hele gemeente."),
        ("Kunnen jullie een bestaande website verbeteren?", "Ja. We kijken eerst in een gratis adviesgesprek naar je huidige site en adviseren of verbeteren of opnieuw bouwen slimmer is.")]),
 "veghel": dict(tag="webdesign vanaf €499", img="blog-bedrijfsvideo-kosten.jpg", who="toeleveranciers, installateurs en winkels in Veghel en Meierijstad",
   syn=("Webdesign in Veghel: zakelijk en lokaal", "Zoek je webdesign in Veghel, dan zit je in een regio met grote, professionele werkgevers. Je website moet daar zakelijk tegenop kunnen, en tegelijk lokaal goed gevonden worden. Dat combineren we in elke site die we bouwen."),
   focus=[("Toeleveranciers zichtbaar", "Bedrijven die leveren aan grote spelers in de regio willen hun kwaliteit en certificeringen laten zien. Een overzichtelijke dienstenpagina en echte projectfoto's helpen daarbij."),
          ("Werken bij in Meierijstad", "In een regio met grote werkgevers is goed personeel schaars. Een vacaturepagina met video van de werkvloer valt op."),
          ("Heel Meierijstad", "We richten je vindbaarheid op Veghel, Schijndel, Sint-Oedenrode en de kerkdorpen.")],
   case=("Elektropost", "/werk-elektropost", "Voor installateur Elektropost bouwden we een frisse site met de diensten duidelijk op een rij: een opzet die goed werkt voor technische bedrijven in Veghel."),
   faq=[("Werken jullie ook voor bedrijven op Doornhoek en De Dubbelen?", "Ja. We komen langs op jouw locatie; vanuit Den Bosch zijn we in twintig minuten in Veghel."),
        ("Kunnen jullie ook een vacaturevideo maken?", "Ja. We filmen op locatie voor €250 per shoot, met drone €300, inclusief montage. Die video gebruik je op je site en op social media.")]),
 "schijndel": dict(tag="website maken vanaf €499", img="blog-website-zzp.jpg", who="familiebedrijven, winkels en zzp'ers in Schijndel en Wijbosch",
   syn=("Website maken in Schijndel: persoonlijk en dichtbij", "In Schijndel draait veel om vertrouwen en aanbevelingen. Een website maken we daarom persoonlijk: we leren je bedrijf kennen, laten je eerst gratis een testwebsite zien en bouwen pas verder als het klopt."),
   focus=[("Mond-tot-mond online", "Wie je via via aangeraden krijgt, zoekt je daarna op. Reviews, foto's van je werk en een duidelijke contactknop maken die aanbeveling af."),
          ("Familiebedrijf in beeld", "Laat zien wie er achter het bedrijf zit. Een korte bedrijfsvideo of eigen foto's doen meer dan stockbeelden."),
          ("Meierijstad als werkgebied", "We maken je vindbaar in Schijndel, Wijbosch, Sint-Oedenrode en Veghel.")],
   case=("Keukenmontage Lassie", "/werk-lassie", "Voor Keukenmontage Lassie bouwden we een website die het vakmanschap laat zien: een aanpak die past bij veel familiebedrijven in Schijndel."),
   faq=[("Kunnen jullie mijn Google-reviews op mijn website zetten?", "Ja. We tonen je Google-reviews op je site, zoals we ook op onze eigen homepage doen."),
        ("Werken jullie ook voor zzp'ers in Schijndel?", "Ja. Voor zzp'ers is een compacte website vaak genoeg; maatwerk begint bij €499. Lees ook ons artikel over <a href=\"/blog/website-laten-maken-zzp\" style=\"color:var(--gold-deep)\">een website laten maken als zzp'er</a>.")]),
 "boxtel": dict(tag="webdesign vanaf €499", img="blog-website-laten-maken-checklist.jpg", who="horeca, recreatie en MKB in Boxtel, Liempde en Esch",
   syn=("Webdesign in Boxtel voor ondernemers en recreatie", "Zoek je webdesign in Boxtel, dan heb je vaak twee doelgroepen: inwoners en bezoekers uit de regio. We bouwen een site die beide aanspreekt, met duidelijke informatie en sfeervolle beelden."),
   focus=[("Bezoekers uit de regio", "Voor horeca en recreatie rond de Dommel en Kampina komen klanten vaak van buiten Boxtel. Sfeerbeelden, openingstijden en reserveren staan dan bovenaan."),
          ("Bereikbaarheid als troef", "Zit je dicht bij het station of de A2? Zet het op je site: voor zakelijke klanten is dat een reden om voor je te kiezen."),
          ("Beelden vanuit de lucht", "Een terrein, terras of locatie in het groen laat zich het best zien vanuit de lucht. Een shoot met drone kost €300.")],
   case=("Echt Grieks", "/werk-echtgrieks", "Voor vakantiehuis Echt Grieks bouwden we een site die sfeer en boekingen combineert: een aanpak die ook voor recreatie en horeca in Boxtel werkt."),
   faq=[("Werken jullie ook in Liempde en Esch?", "Ja. Liempde en Esch horen bij de gemeente Boxtel; we bouwen voor ondernemers in de hele gemeente."),
        ("Mag je met een drone filmen in Boxtel?", "Vaak wel, maar het hangt af van de exacte locatie en het luchtruim. Dat checken we vooraf op de officiële kaarten. Lees meer in ons artikel over <a href=\"/blog/drone-video-laten-maken-kosten-en-regels\" style=\"color:var(--gold-deep)\">drone video laten maken</a>.")]),
 "sint-michielsgestel": dict(tag="webdesign om de hoek", img="photo-cafe-desk.jpg", who="zelfstandigen en familiebedrijven in Gestel, Berlicum en Den Dungen",
   syn=("Website voor ondernemers in Gestel, Berlicum en Den Dungen", "Sint-Michielsgestel bestaat uit meerdere kernen, en klanten zoeken op hun eigen dorp. We bouwen een site die in alle kernen gevonden wordt en die past bij een ondernemer met een vaste, trouwe klantenkring."),
   focus=[("Alle kernen vindbaar", "We nemen Sint-Michielsgestel, Berlicum, Den Dungen, Gemonde en Middelrode mee in je teksten."),
          ("Vertrouwen voor vaste klanten", "Een persoonlijk 'over ons', echte foto's en reviews maken het verschil voor ondernemers die het van hun reputatie moeten hebben."),
          ("Klein beginnen", "Een compacte site van een paar pagina's is vaak genoeg, en die bouw je later rustig uit.")],
   case=("Palmyra Coaching", "/werk-palmyra", "Voor Palmyra Coaching bouwden we een rustige, persoonlijke website: precies wat veel zelfstandigen en praktijken in Sint-Michielsgestel nodig hebben."),
   faq=[("Werken jullie ook in Berlicum en Den Dungen?", "Ja. Berlicum, Den Dungen, Gemonde en Middelrode horen bij de gemeente Sint-Michielsgestel en liggen vlak bij ons kantoor."),
        ("Kan ik eerst een voorbeeld zien?", "Ja. We bouwen eerst gratis een testwebsite; pas als die bevalt, maken we hem af.")]),
 "zaltbommel": dict(tag="webdesign Bommelerwaard", img="photo-sketch.jpg", who="transport, bouw en horeca in Zaltbommel en de Bommelerwaard",
   syn=("Webdesign voor de Bommelerwaard", "Een website laten maken in Zaltbommel betekent vaak twee publieken bedienen: klanten uit de eigen regio en zakelijke relaties langs de A2. We bouwen een site die voor beide duidelijk en betrouwbaar is."),
   focus=[("Historie als decor", "Horeca en winkels in de vestingstad hebben een prachtig decor. Goede foto's en een korte film van je zaak vertellen dat verhaal."),
          ("Zakelijk langs de A2", "Transport- en bouwbedrijven willen betrouwbaar overkomen: duidelijke diensten, certificeringen, werkgebied en een snelle offerte-aanvraag."),
          ("Hele Bommelerwaard", "We richten je site op Zaltbommel én de dorpen eromheen, zodat ook klanten uit Brakel en Zuilichem je vinden.")],
   case=("De Jonge Elektrotechniek", "/werk-dejonge", "Voor De Jonge Elektrotechniek bouwden we een krachtige site, gebouwd om gevonden te worden: een opzet die ook voor technische bedrijven in de Bommelerwaard werkt."),
   faq=[("Werken jullie ook voor bedrijven in Brakel en Zuilichem?", "Ja. We bouwen voor ondernemers in de hele gemeente Zaltbommel en de rest van de Bommelerwaard."),
        ("Kunnen jullie ook dronebeelden maken in Zaltbommel?", "Ja, met drone kost een shoot €300. We checken vooraf altijd of en waar er gevlogen mag worden.")]),
 "drunen": dict(tag="webdesign gemeente Heusden", img="photo-wireframes.jpg", who="bouw, horeca en MKB in Drunen, Vlijmen en Nieuwkuijk",
   syn=("Webdesign in Drunen, Vlijmen en Nieuwkuijk", "Klanten in de gemeente Heusden zoeken op hun eigen kern. Daarom bouwen we een site die gevonden wordt in Drunen, Vlijmen, Nieuwkuijk en de rest van de gemeente, met het werk van je bedrijf centraal."),
   focus=[("Hele gemeente Heusden", "We maken je site vindbaar in Drunen, Vlijmen, Nieuwkuijk, Elshout en Heusden."),
          ("Vakmanschap laten zien", "Voor aannemers en installateurs werken projectfoto's, voor-en-na-beelden en een duidelijk werkgebied het best."),
          ("Recreatie en horeca", "Rond de Loonse en Drunense Duinen draait het om sfeer, route en reserveren. Dronebeelden laten je locatie in het groen zien.")],
   case=("Dekgro", "/werk-dekgro", "Voor tegelzetbedrijf Dekgro bouwden we een site met het werk centraal: een opzet die goed werkt voor bouw- en klusbedrijven in Drunen."),
   faq=[("Werken jullie ook in Vlijmen en Nieuwkuijk?", "Ja. We bouwen voor ondernemers in de hele gemeente Heusden, dus ook in Vlijmen, Nieuwkuijk, Elshout, Haarsteeg en Heusden zelf."),
        ("Kunnen jullie een website maken met voor-en-na-foto's?", "Ja. Voor bouw- en klusbedrijven maken we projectpagina's met voor-en-na-foto's, zodat klanten direct zien wat je kunt.")]),
 "helmond": dict(tag="webdesign vanaf €499", img="photo-filming-workshop.jpg", who="techniek, automotive en MKB in Helmond",
   syn=("Webdesign in Helmond: techniek helder uitgelegd", "Zoek je webdesign in Helmond, dan heb je vaak een technisch verhaal te vertellen. Wij vertalen dat naar heldere pagina's, sterke beelden en een site die zowel inkopers als particulieren begrijpen."),
   focus=[("Techniek begrijpelijk", "Technische bedrijven doen vaak complexe dingen. Wij vertalen dat naar duidelijke pagina's per dienst, zodat bezoekers snappen wat je doet."),
          ("Werken bij", "In een technische regio is goed personeel schaars. Een vacaturepagina met beelden van de werkvloer helpt je opvallen."),
          ("Nieuwe wijken", "In Brandevoort en Dierdonk wonen veel gezinnen die lokaal zoeken. Een goed Google Bedrijfsprofiel en een snelle site vangen die vraag op.")],
   case=("CarsLease", "/werk-carslease", "Voor CarsLease bouwden we een leaseplatform met calculator: een voorbeeld van techniek en gebruiksgemak in één."),
   faq=[("Werken jullie ook voor bedrijven op de Automotive Campus?", "Ja. We bouwen voor technische en automotive bedrijven, ook met calculators of configurators zoals bij CarsLease."),
        ("Is Helmond niet te ver weg voor jullie?", "Nee. We komen graag langs voor de kennismaking; de rest gaat net zo snel als bij een bureau in de buurt.")]),
 "veldhoven": dict(tag="meertalig webdesign", img="blog-website-kosten-per-maand.jpg", who="high-tech, zakelijke dienstverlening en praktijken in Veldhoven",
   syn=("Webdesign voor de high-tech regio", "In Veldhoven werken veel bedrijven voor internationale klanten. Je website moet dan in meerdere talen goed zijn, technisch scherp en snel. Tegelijk wil de lokale praktijk of winkel juist in Veldhoven zelf gevonden worden. Beide bouwen we."),
   focus=[("Internationale klanten", "Veel bedrijven in Veldhoven werken voor klanten en met collega's uit het buitenland. Een Engelse versie van je site is dan geen luxe."),
          ("Specialistisch en helder", "Toeleveranciers willen hun specialisme precies uitleggen. Een eigen pagina per dienst of technologie maakt je vindbaar op wat je echt doet."),
          ("Lokaal voor praktijken", "Voor zorgpraktijken en winkels draait het juist om lokaal gevonden worden in Veldhoven en omgeving.")],
   case=("Onze eigen meertalige site", "/en", "Onze eigen website staat in vier talen met echte vertalingen. Zo'n opzet bouwen we ook voor internationale bedrijven in Veldhoven."),
   faq=[("Kunnen jullie een Engelse versie van mijn website maken?", "Ja. We bouwen meertalige websites met echte vertalingen en de juiste taalkoppelingen voor Google, zoals onze eigen site in vier talen."),
        ("Werken jullie ook voor bedrijven op De Run?", "Ja. We komen langs op De Run en in de rest van Veldhoven; vanuit Den Bosch is het ruim een half uur via de A2.")]),
}
for c in CITIES: c.update(LOCAL[c["slug"]])

# Blogartikelen staan als losse bestanden in content/blog/<datum>-<slug>.html:
# een commentaarblok met velden (title, slug, date, eyebrow, read, img, desc) en daaronder de HTML van het artikel.
# Nieuw artikel = nieuw bestand; zie content/blog/SCHRIJFGIDS.md.
STRICT_FROM = "2026-10-17"  # artikelen vanaf deze datum volgen de volledige SCHRIJFGIDS
def load_articles():
    arts, errors = [], []
    for path in sorted(glob.glob("content/blog/*.html")):
        raw = open(path).read()
        m = re.match(r"\s*<!--(.*?)-->\s*(.*)", raw, re.S)
        if not m: errors.append(f"{path}: geen <!-- ... --> blok met velden bovenaan"); continue
        meta = {}
        for line in m.group(1).strip().splitlines():
            if ":" in line:
                k, v = line.split(":", 1); meta[k.strip()] = v.strip()
        meta["body"] = m.group(2).strip()
        missing = [k for k in ("title", "slug", "date", "eyebrow", "read", "img", "desc") if not meta.get(k)]
        if missing: errors.append(f"{path}: veld(en) ontbreken: {', '.join(missing)}"); continue
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", meta["slug"]): errors.append(f"{path}: slug '{meta['slug']}' mag alleen kleine letters, cijfers en streepjes bevatten")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", meta["date"]): errors.append(f"{path}: date moet JJJJ-MM-DD zijn")
        if len(meta["title"]) > 70: errors.append(f"{path}: title is {len(meta['title'])} tekens (max 70)")
        if not 70 <= len(meta["desc"]) <= 160: errors.append(f"{path}: desc is {len(meta['desc'])} tekens (70–160)")
        if not os.path.exists("assets/" + meta["img"]): errors.append(f"{path}: afbeelding assets/{meta['img']} bestaat niet")
        body = meta["body"]
        if body.count("<h2>") < 3: errors.append(f"{path}: minimaal 3 <h2>-tussenkoppen nodig")
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        if words < 350: errors.append(f"{path}: artikel is {words} woorden (minimaal 350)")
        if meta["date"] >= STRICT_FROM:
            if 'class="tldr"' not in body: errors.append(f"{path}: blok <div class=\"tldr\"> (Kort antwoord) ontbreekt")
            if body.count("<details>") < 3: errors.append(f"{path}: minimaal 3 FAQ-vragen (<details>) nodig")
            if not re.search(r'href="https?://(?!www\.skylinedigital\.nl)', body): errors.append(f"{path}: minimaal 1 externe bron (link) nodig")
            if len(meta["title"]) > 60: errors.append(f"{path}: title is {len(meta['title'])} tekens (max 60 voor nieuwe artikelen)")
        links = re.findall(r'href="(/[^"#?]*)', body)
        if len(links) < 3: errors.append(f"{path}: minimaal 3 interne links nodig")
        for l in links:
            target = "index.html" if l == "/" else l.strip("/") + ".html"
            if not os.path.exists(target) and not os.path.exists(l.strip("/") + "/index.html") and not any(l == "/blog/" + a2 for a2 in [os.path.basename(x)[11:-5] for x in glob.glob("content/blog/*.html")]):
                errors.append(f"{path}: interne link {l} bestaat niet")
        arts.append(meta)
    slugs = [a["slug"] for a in arts]
    for s_ in set(slugs):
        if slugs.count(s_) > 1: errors.append(f"slug '{s_}' komt dubbel voor")
    if errors:
        raise SystemExit("Blog-controle mislukt:\n  - " + "\n  - ".join(errors))
    return sorted(arts, key=lambda a: (a["date"], a["slug"]), reverse=True)

ARTICLES = load_articles()
AUTHOR = {"@type":"Person","@id":BASE+"/over-ons#yannick","name":"Yannick van den Broek","jobTitle":"Oprichter Skyline Digital",
          "worksFor":{"@id":BASE+"/#organization"},"url":BASE+"/over-ons"}
MONTHS = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]
def nl_date(d): y, m, dd = d.split("-"); return f"{int(dd)} {MONTHS[int(m)-1]} {y}"

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
  <meta property="og:type" content="{'article' if '/blog/' in url else 'website'}" />
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
    title = f"Website laten maken {c['name']}: {c['tag']} | Skyline Digital"
    desc = f"Website laten maken {c['in_']}? Maatwerk websites vanaf €499 voor {c['who']}. Snel, vindbaar en eerst gratis een testwebsite."
    near = [CITY_BY[n] for n in c["near"]]
    faqs = [
      (f"Wat kost een website laten maken {c['in_']}?", f"Een maatwerk multipage website kost bij ons €499 eenmalig, een 3D cinematic website €749. SEO is optioneel voor €39 per maand. Die prijzen gelden voor ondernemers {c['in_']} net zo goed als in de rest van Nederland — bekijk de <a href=\"/pricing\" style=\"color:var(--gold-deep)\">prijzen</a>."),
      ("Hoe lang duurt het?", "Een multipage website staat meestal binnen twee tot vier weken online, afhankelijk van hoe snel we teksten en beeld ontvangen. Een gratis testwebsite laten we je vaak al binnen een paar dagen zien."),
    ] + c["faq"]
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
    <div class="page-hero-bg"><img src="/assets/{c['img']}" alt="Website laten maken {c['in_']} — Skyline Digital" /></div>
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · <a href="/regio">Regio's</a> · {c['name']}</p>
      <h1>Website laten maken <span class="gold-text">{c['in_']}.</span></h1>
      <p class="lead">Maatwerk websites vanaf €499 voor {c['who']}. {c['travel']}</p>
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

  <section class="bg-cream full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Waar we {c['in_']} op letten</p>
        <h2>{c['syn'][0]}</h2>
        <p class="lead">{c['syn'][1]}</p>
      </div>
      {rows(c['focus'])}
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
      <p style="margin-top:18px;max-width:720px;color:var(--on-dark-dim)"><strong style="color:var(--on-dark)">{c['case'][0]}.</strong> {c['case'][2]} <a href="{c['case'][1]}" style="color:var(--gold)">Bekijk het project →</a></p>
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Wat je krijgt</p>
        <h2>Maatwerk, snel en <span class="gold-text">vindbaar.</span></h2>
        <p class="lead">Elke site die we {c['in_']} bouwen is maatwerk, mobiel-first en met de SEO-basis meteen goed gezet: een multipage website voor €499 of een 3D Cinematic website voor €749. Wat er precies in zit, lees je op <a href="/website-seo" style="color:var(--gold-deep)">website &amp; SEO</a> en bij de <a href="/pricing" style="color:var(--gold-deep)">prijzen</a>.</p>
      </div>
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
desc = f"Skyline Digital bouwt websites, video en content voor ondernemers in Den Bosch, Eindhoven, Tilburg en nog {len(CITIES) - 3} plaatsen in Brabant en Gelderland. Bekijk je regio."
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
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite</a><a href="/pricing" class="btn btn-ghost-light">Bekijk prijzen</a></div>
    </div>
  </section>

'''
open("regio.html","w").write(head(title, desc, url, "/assets/og-home.jpg", ld) + body + tail())

# ---------- Kennisbank ----------
os.makedirs("blog", exist_ok=True)
for a in ARTICLES:
    url = f"{BASE}/blog/{a['slug']}"; og = f"/assets/{a['img']}"
    ld = {"@context":"https://schema.org","@graph":[
        crumbs_ld(url, [("Blog", BASE+"/blog"), (a["title"], url)]),
        {"@type":"Article","@id":url+"#article","headline":a["title"],"description":a["desc"],"image":BASE+og,"datePublished":a["date"],"dateModified":a.get("updated") or a["date"],
         "author":AUTHOR,"publisher":ORG_REF,"mainEntityOfPage":url,"inLanguage":"nl-NL"},
        {"@type":"WebPage","@id":url+"#webpage","url":url,"name":a["title"],"description":a["desc"],"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"breadcrumb":{"@id":url+"#breadcrumb"}}]}
    faqs = [(html.unescape(re.sub(r"<[^>]+>", "", q)).strip(), html.unescape(re.sub(r"<[^>]+>", "", an)).strip())
            for q, an in re.findall(r"<details>\s*<summary>(.*?)</summary>(.*?)</details>", a["body"], re.S)]
    if faqs: ld["@graph"].insert(-1, {"@type":"FAQPage","@id":url+"#faq","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":an}} for q, an in faqs]})
    others = [o for o in ARTICLES if o is not a][:3]
    body = BLOG_HEADER + f'''
  <section class="page-hero has-image">
    <div class="page-hero-bg"><img src="{og}" alt="{html.escape(a['title'])}" /></div>
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · <a href="/blog">Blog</a> · {a['eyebrow']}</p>
      <h1>{a['title']}</h1>
      <p class="lead">{a['eyebrow']} · {nl_date(a['date'])} · {a['read']} leestijd · door Yannick van den Broek</p>
    </div>
  </section>
  <section class="bg-white full">
    <div class="wrap-sm">
      <article class="article">
{a['body']}
      </article>
      <aside class="author-box">
        <img src="/assets/logo.png" alt="Skyline Digital" />
        <div>
          <p class="author-name">Yannick van den Broek <span>· oprichter Skyline Digital</span></p>
          <p>Bouwt maatwerk websites en maakt bedrijfs-, villa- en dronefilms vanuit 's-Hertogenbosch. Gepubliceerd {nl_date(a['date'])}{(' · bijgewerkt ' + nl_date(a['updated'])) if a.get('updated') else ''}.</p>
          <p class="author-note">Dit artikel is geschreven met hulp van AI, op basis van onze eigen werkwijze, prijzen en projecten. Cijfers en regels zijn gecontroleerd aan de hand van de genoemde bronnen.</p>
        </div>
      </aside>
      <div class="article-more">
        <h2>Verder lezen</h2>
        {rows([(f'<a href="/blog/{o["slug"]}" style="color:inherit;text-decoration:none">{o["title"]}</a>', o["desc"]) for o in others])}
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
    page = head(a["title"] + " | Skyline Digital", a["desc"], url, og, ld) + body + tail()
    page = page.replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    open(f"blog/{a['slug']}.html","w").write(page)

url = BASE + "/blog"; title = "Blog: websites, SEO, video & content | Skyline Digital"
desc = "Blog van Skyline Digital: eerlijke artikelen over website laten maken, kosten, SEO, bedrijfsvideo en drone video, met echte prijzen en bronnen."
ld = {"@context":"https://schema.org","@graph":[crumbs_ld(url,[("Blog",url)]),
      {"@type":"Blog","@id":url+"#blog","url":url,"name":"Blog Skyline Digital","description":desc,"inLanguage":"nl-NL","publisher":ORG_REF,
       "blogPost":[{"@type":"BlogPosting","headline":a["title"],"url":f"{BASE}/blog/{a['slug']}","datePublished":a["date"],"image":f"{BASE}/assets/{a['img']}"} for a in ARTICLES]},
      {"@type":"CollectionPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"breadcrumb":{"@id":url+"#breadcrumb"},"mainEntity":{"@id":url+"#blog"}}]}
def blog_card(a, big=False):
    # kaarten gebruiken de kleine variant (<naam>-m.jpg) als die bestaat; de grote bovenste kaart de volledige foto
    small = a["img"].replace(".jpg", "-m.jpg")
    img = a["img"] if big or not os.path.exists("assets/" + small) else small
    return (f'<a class="blog-card{" blog-card-big" if big else ""} reveal" href="/blog/{a["slug"]}">'
            f'<span class="blog-card-img"><img src="/assets/{img}" alt="{html.escape(a["title"])}" loading="{"eager" if big else "lazy"}" /></span>'
            f'<span class="blog-card-body"><span class="blog-meta">{a["eyebrow"]} · {nl_date(a["date"])} · {a["read"]}</span>'
            f'<span class="blog-card-title">{a["title"]}</span><span class="blog-card-desc">{a["desc"]}</span>'
            f'<span class="blog-more">Lees artikel {ARROW}</span></span></a>')
body = BLOG_HEADER + f'''
  <section class="page-hero center" style="background:radial-gradient(90% 100% at 50% 0%, #16171f, #07080c)">
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · Blog</p>
      <h1>Blog over websites, SEO <span class="gold-text">&amp; video.</span></h1>
      <p class="lead">Eerlijke artikelen over websites, prijzen, vindbaarheid en video. Zonder verkooppraat, met echte cijfers en bronnen.</p>
    </div>
  </section>
  <section class="bg-white full">
    <div class="wrap">
      {blog_card(ARTICLES[0], big=True)}
      <div class="blog-grid">{"".join(blog_card(a) for a in ARTICLES[1:])}</div>
    </div>
  </section>
  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Vragen over jouw situatie?</h2>
      <p class="lead">Plan een gratis adviesgesprek, we denken graag mee.</p>
      <div class="hero-actions hero-actions-center"><a href="/contact" class="btn btn-gold">Plan een gesprek</a><a href="/pricing" class="btn btn-ghost-light">Bekijk prijzen</a></div>
    </div>
  </section>

'''
open("blog.html","w").write(head(title, desc, url, "/assets/og-home.jpg", ld) + body + tail())

# ---------- Footer op alle pagina's: Regio's + Blog ----------
NEW_COL = '''        <div class="footer-col">
          <h4>Regio's</h4>
''' + "".join(f'          <a href="/website-laten-maken-{c["slug"]}">Website laten maken {c["name"]}</a>\n' for c in CITIES[:8]) + '''          <a href="/regio">Alle regio's</a>
        </div>
'''
for path in glob.glob("*.html") + glob.glob("blog/*.html"):
    if path.startswith("google"): continue
    s = open(path).read()
    if "Website laten maken Den Bosch</a>" in s: continue
    s = re.sub(r'        <div class="footer-col">\n          <h4>Over ons</h4>.*?</div>\n', NEW_COL, s, count=1, flags=re.S)
    s = s.replace('          <a href="/aanvraag" class="footer-gratis">★ Gratis testwebsite</a>', '          <a href="/blog">Blog</a>\n          <a href="/aanvraag" class="footer-gratis">★ Gratis testwebsite</a>', 1)
    # relatieve assets in footer/nav werken niet vanuit /blog/ — maak ze absoluut
    if path.startswith("blog/"):
        s = s.replace('src="assets/', 'src="/assets/')
    open(path, "w").write(s)

# ---------- Sitemap ----------
urls = [("/",1.0,"weekly"),("/website-seo",0.9,"monthly"),("/drone-video",0.9,"monthly"),("/social-media",0.9,"monthly"),("/ai-content",0.9,"monthly"),
        ("/pricing",0.8,"monthly"),("/portfolio",0.8,"monthly"),("/over-ons",0.7,"monthly"),("/contact",0.7,"yearly"),("/aanvraag",0.8,"yearly"),
        ("/regio",0.7,"monthly"),("/blog",0.7,"weekly")]
urls += [(f"/website-laten-maken-{c['slug']}",0.8,"monthly") for c in CITIES]
urls += [(f"/blog/{a['slug']}",0.7,"monthly",a["date"]) for a in ARTICLES]
W = ["dekgro","lillis","bodyscan","echtgrieks","carslease","lassie","dejonge","elektropost","palmyra"]
urls += [(f"/werk-{w}",0.5,"yearly") for w in W]
MAIN = ["","/over-ons","/website-seo","/drone-video","/social-media","/ai-content","/portfolio","/pricing","/contact","/aanvraag"]
# het Spaans staat op www.skylinedigital.es met een eigen sitemap (tools/gen_es.py)
for l in ["en","it"]:
    urls += [(f"/{l}{m}", 0.8 if m == "" else 0.6, "monthly") for m in MAIN]
    urls += [(f"/{l}/werk-{w}", 0.4, "yearly") for w in W]
urls += [("/privacybeleid",0.2,"yearly"),("/algemene-voorwaarden",0.2,"yearly"),("/cookiebeleid",0.2,"yearly")]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for entry in urls:
    u, p, f = entry[:3]; lm = entry[3] if len(entry) > 3 else (max(a["date"] for a in ARTICLES) if u == "/blog" else TODAY)
    sm += f'  <url><loc>{BASE}{u}</loc><lastmod>{lm}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority></url>\n'
open("sitemap.xml","w").write(sm + "</urlset>\n")
print("pages:", len(CITIES)+len(ARTICLES)+2, "sitemap urls:", len(urls))

# Google-tag (GA4 + toestemmingsmodus) op alle pagina's, ook de zojuist gegenereerde
import subprocess, sys
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "add_ga.py")], check=True)
