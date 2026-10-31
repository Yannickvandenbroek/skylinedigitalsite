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
 # --- buiten Brabant, waar al klanten zitten (CRM, 2026-10-27) ---
 dict(slug="barneveld", name="Barneveld", full="Barneveld", in_="in Barneveld", region="Gelderland",
      intro="Barneveld ligt midden in de Gelderse Vallei, aan de A1 en de A30, en is een groeiende gemeente met veel familiebedrijven in bouw, installatie en de agrarische sector. Op bedrijventerrein Harselaar groeit het MKB door. Een website laten maken in Barneveld betekent voor ons: een nuchtere, duidelijke site die laat zien wat je doet en waar je werkt.",
      intro2="In Barneveld bouwden we al websites voor drie installatiebedrijven: GK Vloerverwarming, MSB Vloerverwarming en Installatiebedrijf H. Ploeg. We werken voor ondernemers in Barneveld, Voorthuizen, Kootwijkerbroek, Garderen en de rest van de gemeente.",
      sectors=["installatie, vloerverwarming en loodgieters", "bouw en afbouw", "agrarische en pluimveebedrijven", "winkels en dienstverlening in het centrum"],
      places="Barneveld, Voorthuizen, Kootwijkerbroek, Garderen, Stroe en Zwartebroek", near=["amersfoort","apeldoorn","nijmegen"], travel="Met ondernemers in de Gelderse Vallei werken we vooral op afstand: kennismaking via telefoon of video."),
 dict(slug="amersfoort", name="Amersfoort", full="Amersfoort", in_="in Amersfoort", region="Utrecht",
      intro="Amersfoort ligt bij knooppunt Hoevelaken, waar de A1 en de A28 samenkomen, en heeft een van de drukste stations van het land. Dat maakt de stad aantrekkelijk voor kantoren, ICT-bedrijven en zakelijke dienstverleners, op bedrijventerreinen als De Hoef en Calveen. Een website laten maken in Amersfoort betekent: opvallen in een stad met veel concurrentie en tegelijk de dorpen eromheen bereiken.",
      intro2="Rond Amersfoort bouwden we websites voor installateurs in Nijkerk, Woudenberg, Scherpenzeel en Barneveld. We werken voor ondernemers in Amersfoort, Hoogland, Leusden, Soest en de rest van Eemland.",
      sectors=["zakelijke dienstverlening en ICT", "bouw, installatie en techniek", "winkels en horeca in de binnenstad", "zorg- en coachingpraktijken"],
      places="de binnenstad, Vathorst, Nieuwland, Kattenbroek, Schothorst, Hoogland en de bedrijventerreinen De Hoef en Calveen", near=["barneveld","apeldoorn","den-bosch"], travel="Met ondernemers in en rond Amersfoort werken we vooral op afstand: kennismaking via telefoon of video."),
 dict(slug="apeldoorn", name="Apeldoorn", full="Apeldoorn", in_="in Apeldoorn", region="Gelderland",
      intro="Apeldoorn is de grootste stad van de Veluwe. Naast grote werkgevers als de Belastingdienst en het Kadaster heeft de stad een breed MKB, met bedrijventerreinen als de Ecofactorij en Apeldoorn-Noord. Een website laten maken in Apeldoorn betekent voor ons een site die gevonden wordt in de stad én in de dorpen eromheen.",
      intro2="Op de Veluwe bouwden we al websites voor G.J. Elektro en JM Installatie Service in Vaassen en voor Vlaskamp Installatietechniek in Heerde. We werken voor ondernemers in Apeldoorn, Ugchelen, Beekbergen, Loenen, Vaassen en Epe.",
      sectors=["installatie- en elektrotechnische bedrijven", "zakelijke dienstverlening", "recreatie en horeca op de Veluwe", "zorg en praktijken"],
      places="het centrum, Zevenhuizen, De Maten, Ugchelen, Beekbergen, Vaassen en Epe", near=["zwolle","barneveld","amersfoort"], travel="Met ondernemers op de Veluwe werken we vooral op afstand: kennismaking via telefoon of video."),
 dict(slug="zwolle", name="Zwolle", full="Zwolle", in_="in Zwolle", region="Overijssel",
      intro="Zwolle is de hoofdstad van Overijssel en het centrum van een grote regio, met ziekenhuis Isala, hogeschool Windesheim en een Hanzebinnenstad vol winkels. Op bedrijventerreinen als Hessenpoort en de Marslanden zitten logistiek, groothandel en techniek. Een website laten maken in Zwolle betekent: lokaal gevonden worden in een stad waar klanten uit de hele regio naartoe komen.",
      intro2="In de regio bouwden we websites voor Woninginrichting van Breukelen in Zwolle, RSTK Rioolservice in Kampen en Vlaskamp Installatietechniek in Heerde. We werken voor ondernemers in Zwolle, Kampen, Hattem, Heerde en Dalfsen.",
      sectors=["winkels en woninginrichting", "installatie, loodgieters en rioolservice", "logistiek en groothandel", "zorg en dienstverlening"],
      places="de binnenstad, Stadshagen, Assendorp, Berkum, Kampen, Hattem en Heerde", near=["apeldoorn","barneveld","amersfoort"], travel="Met ondernemers in de regio Zwolle werken we vooral op afstand: kennismaking via telefoon of video."),
]
CITY_BY = {c["slug"]: c for c in CITIES}

# Per plaats eigen inhoud, zodat de plaatspagina's geen bijna-kopieën van elkaar zijn (Google ziet dat als doorway pages):
# tag = titeltoevoeging met het synoniem dat daar gezocht wordt (Search Console / Keyword Planner), syn = eigen tussenkop + alinea,
# focus = drie lokale aandachtspunten, case = passend project, faq = twee eigen vragen, img = eigen kopfoto.
LOCAL = {
 "den-bosch": dict(tag="webdesign vanaf €375", img="blog-wat-kost-een-website.jpg", who="ondernemers in 's-Hertogenbosch, van de binnenstad tot De Herven",
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
 "oss": dict(tag="website bouwer vanaf €375", img="blog-cinematic-scroll-website.jpg", who="productiebedrijven, winkels en praktijken in Oss, Berghem en Lith",
   syn=("Website bouwer in Oss, met SEO erbij", "Zoek je een website bouwer in Oss, dan wil je meestal meer dan een mooie site: je wilt dat hij aanvragen oplevert. Daarom zetten we de SEO bij de bouw meteen goed op, en kun je daarna kiezen voor SEO-onderhoud voor €79 per maand."),
   focus=[("Specialismen per pagina", "Productiebedrijven en toeleveranciers willen precies uitleggen wat ze maken. Elke dienst krijgt een eigen pagina, zodat inkopers je vinden op wat je echt doet."),
          ("Werken bij", "Veel Osse bedrijven zoeken personeel. Een goede vacaturepagina met beeld van de werkvloer helpt je opvallen."),
          ("Oss en omgeving", "We richten je vindbaarheid op Oss, Berghem, Lith en de rest van de regio.")],
   case=("Palmyra Coaching in Oss", "/werk-palmyra", "Voor Palmyra Coaching in Oss bouwden we een rustige website die vertrouwen uitstraalt en bezoekers naar een afspraak leidt."),
   faq=[("Hebben jullie al klanten in Oss?", "Ja, onder andere Van Loosbroek Installatietechniek, De Jongh Projects en Palmyra Coaching. Hun sites staan hieronder en in ons portfolio."),
        ("Doen jullie ook SEO voor bedrijven in Oss?", "Ja. Bij elke website zetten we de basis-SEO goed. Daarna kun je SEO afnemen voor €79 per maand, met een maandelijkse rapportage.")]),
 "eindhoven": dict(tag="internetbureau vanaf €375", img="photo-studio-monitor.jpg", who="tech, design en MKB in Eindhoven en Brainport",
   syn=("Internetbureau voor Eindhovense ondernemers", "In Eindhoven zoeken veel bedrijven een internetbureau dat design en techniek allebei serieus neemt. Wij combineren maatwerk design met snelle, schone code en, als je wilt, een cinematische scroll-website die opvalt in de designstad."),
   focus=[("Hoog designniveau", "In de stad van de Dutch Design Week valt een standaardtemplate op, en niet positief. Daarom ontwerpen we elke site op maat, met een 3D Cinematic-variant vanaf €749."),
          ("Internationaal publiek", "Werk je met internationale klanten of collega's? We bouwen meertalige websites, zoals onze eigen site in vier talen."),
          ("Techniek en koppelingen", "Calculators, configurators en koppelingen met je systemen, zoals de leasecalculator die we voor CarsLease bouwden.")],
   case=("CarsLease in Eindhoven", "/werk-carslease", "Voor CarsLease in Eindhoven bouwden we een leaseplatform met calculator, zodat bezoekers direct hun maandbedrag zien."),
   faq=[("Werken jullie ook voor bedrijven op Strijp-S of de High Tech Campus?", "Ja. We komen langs in heel Eindhoven; Strijp-S en de High Tech Campus zijn vanuit Den Bosch goed bereikbaar via de A2."),
        ("Kunnen jullie een meertalige website maken?", "Ja. Onze eigen site staat in het Nederlands, Engels, Italiaans en Spaans, met echte vertalingen en de juiste taalkoppelingen voor Google.")]),
 "tilburg": dict(tag="website bouwen vanaf €375", img="photo-studio-loft.jpg", who="logistiek, horeca en creatieve ondernemers in Tilburg",
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
 "nijmegen": dict(tag="website maken vanaf €375", img="blog-lokale-seo.jpg", who="praktijken, horeca en MKB in Nijmegen en Lent",
   syn=("Webdesign in Nijmegen voor zorg, horeca en MKB", "Wie in Nijmegen een website laat maken, wil opvallen in een drukke online markt. We combineren een helder ontwerp met snelle techniek en lokale vindbaarheid, zodat je gevonden wordt door patiënten, studenten en bedrijven."),
   focus=[("Zorg en praktijken", "Cliënten willen snel weten wat je doet, hoe ze een afspraak maken en of je vergoed wordt. Dat zetten we bovenaan."),
          ("Studentenstad", "Veel bezoekers komen via de telefoon en Instagram. Daarom koppelen we je site aan je social media."),
          ("Beide kanten van de Waal", "We richten je vindbaarheid op Nijmegen én op Lent en Nijmegen-Noord.")],
   case=("BodyScan", "/werk-bodyscan", "Voor BodyScan bouwden we een website die rust uitstraalt en uitlegt hoe een behandeling werkt: het soort site dat ook bij Nijmeegse praktijken past."),
   faq=[("Werken jullie ook voor zorgpraktijken in Nijmegen?", "Ja. We bouwen websites voor praktijken en zorgondernemers, met duidelijke uitleg, afspraakknoppen en een rustige uitstraling."),
        ("Kan mijn website gekoppeld worden aan Instagram?", "Ja. We kunnen je laatste Instagram-posts automatisch op je site tonen, zoals we op onze eigen site doen.")]),
 "waalwijk": dict(tag="webdesigner vanaf €375", img="photo-wall-screen.jpg", who="logistiek, productie en winkels in Waalwijk en De Langstraat",
   syn=("Webdesigner of internetbureau in Waalwijk?", "In Waalwijk wordt veel gezocht op webdesign, een webdesigner of een internetbureau. Bij ons krijg je het beste van beide: één vast aanspreekpunt zoals bij een zelfstandige webdesigner, en ontwerp, techniek, SEO en video onder één dak zoals bij een bureau."),
   focus=[("Logistiek en groothandel", "Bedrijven op Haven Zeven en Haven Acht verkopen vooral aan andere bedrijven. Heldere diensten, certificeringen en een snelle offerte-aanvraag maken het verschil."),
          ("Personeel werven", "In een logistieke regio is een goede vacaturepagina bijna net zo belangrijk als je dienstenpagina."),
          ("De Langstraat", "We richten je site ook op Kaatsheuvel, Sprang-Capelle en Waspik, waar veel van je klanten vandaan komen.")],
   case=("Elektropost", "/werk-elektropost", "Voor installateur Elektropost bouwden we een frisse, persoonlijke site met de diensten duidelijk op een rij: een opzet die ook voor technische bedrijven in Waalwijk werkt."),
   faq=[("Bouwen jullie ook webshops in Waalwijk?", "Ja, ook webshops en koppelingen. De prijs hangt af van het aantal producten en koppelingen; je krijgt vooraf een offerte op maat."),
        ("Werken jullie ook in Kaatsheuvel en Sprang-Capelle?", "Ja. We bouwen voor ondernemers in heel De Langstraat; Kaatsheuvel en Sprang-Capelle liggen vlak bij Waalwijk.")]),
 "uden": dict(tag="webdesign vanaf €375", img="photo-cafe-shoot.jpg", who="winkels, zorgverleners en bouwbedrijven in Uden en Maashorst",
   syn=("Webdesign en websitebouw in Uden", "Of je nu zoekt op webdesign, een websitebouwer of een internetbureau in Uden: je wilt een site die lokaal gevonden wordt en die past bij de kwaliteit die je levert. Daar bouwen we op, met een vaste prijs vanaf €375."),
   focus=[("Winkelstad", "Voor winkels en horeca in het centrum van Uden draait het om openingstijden, route en een Google Bedrijfsprofiel dat klopt."),
          ("Zorg rond Bernhoven", "Praktijken en zorgverleners willen rust en duidelijkheid: wat je doet, voor wie, en hoe iemand een afspraak maakt."),
          ("Maashorst en omgeving", "We richten je site op Uden, Volkel en Odiliapeel, en op Veghel en Oss in de buurt.")],
   case=("De Jonge Elektrotechniek", "/werk-dejonge", "Voor De Jonge Elektrotechniek bouwden we een krachtige site die gevonden wordt op de diensten die ze echt leveren: dezelfde aanpak gebruiken we voor bouw- en technische bedrijven in Uden."),
   faq=[("Werken jullie in de hele gemeente Maashorst?", "Ja. Uden en Landerd zijn in 2022 samengegaan tot Maashorst; we bouwen voor ondernemers in de hele gemeente."),
        ("Kunnen jullie een bestaande website verbeteren?", "Ja. We kijken eerst in een gratis adviesgesprek naar je huidige site en adviseren of verbeteren of opnieuw bouwen slimmer is.")]),
 "veghel": dict(tag="webdesign vanaf €375", img="blog-bedrijfsvideo-kosten.jpg", who="toeleveranciers, installateurs en winkels in Veghel en Meierijstad",
   syn=("Webdesign in Veghel: zakelijk en lokaal", "Zoek je webdesign in Veghel, dan zit je in een regio met grote, professionele werkgevers. Je website moet daar zakelijk tegenop kunnen, en tegelijk lokaal goed gevonden worden. Dat combineren we in elke site die we bouwen."),
   focus=[("Toeleveranciers zichtbaar", "Bedrijven die leveren aan grote spelers in de regio willen hun kwaliteit en certificeringen laten zien. Een overzichtelijke dienstenpagina en echte projectfoto's helpen daarbij."),
          ("Werken bij in Meierijstad", "In een regio met grote werkgevers is goed personeel schaars. Een vacaturepagina met video van de werkvloer valt op."),
          ("Heel Meierijstad", "We richten je vindbaarheid op Veghel, Schijndel, Sint-Oedenrode en de kerkdorpen.")],
   case=("Elektropost", "/werk-elektropost", "Voor installateur Elektropost bouwden we een frisse site met de diensten duidelijk op een rij: een opzet die goed werkt voor technische bedrijven in Veghel."),
   faq=[("Werken jullie ook voor bedrijven op Doornhoek en De Dubbelen?", "Ja. We komen langs op jouw locatie; vanuit Den Bosch zijn we in twintig minuten in Veghel."),
        ("Kunnen jullie ook een vacaturevideo maken?", "Ja. We filmen op locatie voor €250 per shoot, met drone €300, inclusief montage. Die video gebruik je op je site en op social media.")]),
 "schijndel": dict(tag="website maken vanaf €375", img="blog-website-zzp.jpg", who="familiebedrijven, winkels en zzp'ers in Schijndel en Wijbosch",
   syn=("Website maken in Schijndel: persoonlijk en dichtbij", "In Schijndel draait veel om vertrouwen en aanbevelingen. Een website maken we daarom persoonlijk: we leren je bedrijf kennen, laten je eerst gratis een testwebsite zien en bouwen pas verder als het klopt."),
   focus=[("Mond-tot-mond online", "Wie je via via aangeraden krijgt, zoekt je daarna op. Reviews, foto's van je werk en een duidelijke contactknop maken die aanbeveling af."),
          ("Familiebedrijf in beeld", "Laat zien wie er achter het bedrijf zit. Een korte bedrijfsvideo of eigen foto's doen meer dan stockbeelden."),
          ("Meierijstad als werkgebied", "We maken je vindbaar in Schijndel, Wijbosch, Sint-Oedenrode en Veghel.")],
   case=("Keukenmontage Lassie", "/werk-lassie", "Voor Keukenmontage Lassie bouwden we een website die het vakmanschap laat zien: een aanpak die past bij veel familiebedrijven in Schijndel."),
   faq=[("Kunnen jullie mijn Google-reviews op mijn website zetten?", "Ja. We tonen je Google-reviews op je site, zoals we ook op onze eigen homepage doen."),
        ("Werken jullie ook voor zzp'ers in Schijndel?", "Ja. Voor zzp'ers is een compacte website vaak genoeg; maatwerk begint bij €375. Lees ook ons artikel over <a href=\"/blog/website-laten-maken-zzp\" style=\"color:var(--gold-deep)\">een website laten maken als zzp'er</a>.")]),
 "boxtel": dict(tag="webdesign vanaf €375", img="blog-website-laten-maken-checklist.jpg", who="horeca, recreatie en MKB in Boxtel, Liempde en Esch",
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
 "helmond": dict(tag="webdesign vanaf €375", img="photo-filming-workshop.jpg", who="techniek, automotive en MKB in Helmond",
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
 "barneveld": dict(tag="websites voor vakbedrijven", img="photo-laptop-desk.jpg", who="installateurs, bouwers en familiebedrijven in Barneveld en de Gelderse Vallei",
   syn=("Een website voor vakbedrijven in de Gelderse Vallei", "In Barneveld werken we vooral voor vakmensen: installateurs, vloerverwarmingsspecialisten en loodgieters. Zij willen een site die laat zien wat ze doen, waar ze werken en hoe je ze snel belt. Geen poespas, wel gevonden worden."),
   focus=[("Werkgebied op de kaart", "Veel vakbedrijven uit Barneveld werken ver buiten de gemeente. We zetten je werkgebied duidelijk op de site en richten de vindbaarheid op de plaatsen waar je het meeste werk wilt."),
          ("Bellen of offerte in één tik", "Op de telefoon staan je nummer en een offerteknop altijd binnen bereik. Zo wordt een bezoeker sneller een klant."),
          ("Eigen projectfoto's", "Foto's van je eigen werk zeggen meer dan stockbeelden. We helpen je kiezen welke foto's het best werken.")],
   case=("GK Vloerverwarming", "https://gkvloerverwarming.nl", "Voor GK Vloerverwarming uit Barneveld bouwden we een site over watergedragen en elektrische vloerverwarming, die meteen duidelijk maakt dat ze in heel Nederland werken."),
   faq=[("Werken jullie voor bedrijven in Barneveld, terwijl jullie in Den Bosch zitten?", "Ja. We bouwden al websites voor drie installatiebedrijven in Barneveld. De kennismaking doen we via telefoon of video, en je ziet eerst gratis een testwebsite."),
        ("Kan mijn website laten zien dat ik in heel Nederland werk?", "Ja. We zetten je werkgebied duidelijk op de site en kunnen extra pagina's maken voor de regio's waar je het meeste werk wilt.")]),
 "amersfoort": dict(tag="webdesign vanaf €375", img="photo-phone-city.jpg", who="MKB, installateurs en dienstverleners in Amersfoort en Eemland",
   syn=("Webdesign in Amersfoort en omgeving", "Wie in Amersfoort zoekt op webdesign of een websitebouwer, vindt veel bureaus. Wij onderscheiden ons met vaste prijzen vanaf €375, een gratis testwebsite vooraf en echte klanten in de regio, van Nijkerk tot Scherpenzeel."),
   focus=[("Stad en dorpen", "Klanten zoeken op Amersfoort, maar ook op Hoogland, Leusden of Nijkerk. We nemen de plaatsen mee waar jouw klanten wonen."),
          ("Zakelijk publiek", "Voor dienstverleners en ICT-bedrijven telt vertrouwen: duidelijke diensten, cases en een persoonlijk 'over ons'."),
          ("Vakbedrijven", "Voor installateurs en bouwers werken projectfoto's, een duidelijk werkgebied en een snelle offerteknop het best.")],
   case=("Elektropost in Woudenberg", "/werk-elektropost", "Voor installateur Elektropost uit Woudenberg bouwden we een frisse, persoonlijke site met zeven specialismen overzichtelijk op een rij."),
   faq=[("Hebben jullie klanten in de regio Amersfoort?", "Ja. We bouwden websites voor onder andere De Jonge Elektrotechniek in Nijkerk, Elektropost in Woudenberg en Klok en van Ginkel Elektrotechniek in Scherpenzeel."),
        ("Hoe gaat de samenwerking als jullie niet om de hoek zitten?", "We beginnen met een kennismaking via telefoon of video en laten je eerst gratis een testwebsite zien. Daarna gaat alles online, net zo snel als bij een bureau in de buurt.")]),
 "apeldoorn": dict(tag="website bouwen vanaf €375", img="photo-flatlay-phone.jpg", who="installateurs, MKB en recreatiebedrijven in Apeldoorn en op de Veluwe",
   syn=("Website bouwen in Apeldoorn en op de Veluwe", "Een website bouwen in Apeldoorn begint bij ons met een gratis testwebsite. Je ziet eerst hoe je site eruitziet; bevalt het, dan maken we hem af met snelle laadtijden en een goede basis voor Google."),
   focus=[("Stad en dorpen", "We maken je vindbaar in Apeldoorn én in Ugchelen, Beekbergen, Loenen en de dorpen in de buurt."),
          ("Vakmanschap tonen", "Voor installateurs en bouwers werken projectfoto's, certificeringen en een duidelijk werkgebied het best."),
          ("Recreatie op de Veluwe", "Campings, B&B's en horeca verkopen sfeer: grote beelden, eventueel vanuit de lucht, en een duidelijke knop om te boeken.")],
   case=("G.J. Elektro in Vaassen", "https://gjelektrotechniek.nl", "Voor G.J. Elektro uit Vaassen bouwden we een site voor huis- en bedrijfsinstallaties, zonnepanelen en domotica, met alle diensten overzichtelijk op een rij."),
   faq=[("Hebben jullie klanten in de buurt van Apeldoorn?", "Ja. In Vaassen bouwden we websites voor G.J. Elektro en JM Installatie Service, en in Heerde voor Vlaskamp Installatietechniek."),
        ("Kunnen jullie een website maken voor een camping of B&B op de Veluwe?", "Ja. Voor recreatie maken we sites met sfeerbeelden en een duidelijke knop om te reserveren. Een foto- of videoshoot op locatie kost €250, met drone €300.")]),
 "zwolle": dict(tag="webdesigner vanaf €375", img="photo-edit-suite.jpg", who="winkels, installateurs en MKB in Zwolle, Kampen en omgeving",
   syn=("Webdesigner voor Zwolle en de regio", "Zoek je een webdesigner in Zwolle, dan wil je iemand die je bedrijf snapt en snel schakelt. Bij ons krijg je één vast aanspreekpunt, vaste prijzen en eerst een gratis testwebsite, net als onze klanten in Zwolle, Kampen en Heerde."),
   focus=[("Winkels met een verhaal", "Een zaak met een lange geschiedenis verdient een site die dat laat zien: wie je bent, wat je verkoopt en waarom klanten al jaren terugkomen."),
          ("Dag en nacht bereikbaar", "Voor loodgieters en rioolservice draait alles om snel bellen. Je nummer staat altijd in beeld, ook op de telefoon."),
          ("Regio Zwolle", "We maken je vindbaar in Zwolle én in Kampen, Hattem, Heerde en Dalfsen.")],
   case=("Woninginrichting van Breukelen", "https://woninginrichtingvanbreukelen.nl", "Voor Woninginrichting van Breukelen in Zwolle, al ruim negentig jaar specialist in raambekleding, vloeren en slaapkamers, bouwden we een site die het assortiment overzichtelijk laat zien."),
   faq=[("Hebben jullie klanten in de regio Zwolle?", "Ja, onder andere Woninginrichting van Breukelen in Zwolle, RSTK Rioolservice in Kampen en Vlaskamp Installatietechniek in Heerde."),
        ("Hoe werken jullie met klanten buiten Brabant?", "Grotendeels online: kennismaking via telefoon of video, daarna een gratis testwebsite en de afronding op afstand.")]),
}
# "Ondernemen in <plaats>": lokale economie en wat dat betekent voor je website (twee alinea's), plus twee extra eigen vragen.
BIZ = {
 "den-bosch": ("'s-Hertogenbosch is de provinciehoofdstad van Noord-Brabant en heeft een opvallend gemengde economie: overheid en zakelijke dienstverlening in het Paleiskwartier, winkels en horeca in de historische binnenstad rond de Sint-Jan, en bouw, logistiek en techniek op De Rietvelden, De Herven en De Brand. Daarnaast trekt de stad veel bezoekers, wat horeca en retail een groot publiek van buiten geeft.",
               "Voor je website betekent dat: wie in de binnenstad zit, concurreert om bezoekers die vooraf online zoeken waar ze gaan eten of winkelen. Wie op een bedrijventerrein zit, wordt vooral gevonden door andere bedrijven die zoeken op een specialisme. We stemmen je pagina's af op het publiek dat voor jou telt."),
 "rosmalen": ("Rosmalen hoort bij de gemeente 's-Hertogenbosch, maar voelt voor veel inwoners als een eigen dorp met een eigen centrum. Met de groei van De Groote Wielen zijn er veel jonge gezinnen bijgekomen, en op bedrijventerrein Kruisstraat en rond Hintham zitten bouw-, auto- en installatiebedrijven. Rond de Molenhoekpassage zitten winkels, praktijken en dienstverleners die vooral voor inwoners werken.",
              "Een website in Rosmalen bedient daarom vaak twee soorten klanten: inwoners die lokaal een vakman, praktijk of kapper zoeken, en bedrijven uit de hele regio. We maken duidelijk voor wie je er bent en zorgen dat je zowel op 'Rosmalen' als op 'Den Bosch' gevonden wordt."),
 "vught": ("Vught is een groene gemeente met villawijken, landgoederen en een centrum rond de Taalstraat met veel zelfstandige winkels, interieurzaken en horeca. Sinds 2021 hoort ook Helvoirt bij de gemeente. Daarnaast werken er veel zelfstandige adviseurs, coaches en zorgverleners vanuit huis of een kleine praktijk.",
           "In Vught telt de eerste indruk zwaar: klanten zijn kritisch en vergelijken. Rustige vormgeving, goede foto's en duidelijke informatie over je aanbod werken hier beter dan opvallende kleuren of acties."),
 "oss": ("Oss heeft een lange geschiedenis als industriestad, van vleeswaren en margarine tot farmacie. Die traditie zie je nog op bedrijventerreinen als Elzenburg, Moleneind en Vorstengrafdonk, waar productiebedrijven, toeleveranciers en logistieke bedrijven zitten. Tegelijk is Oss het centrum voor dorpen als Berghem, Lith en Ravenstein.",
         "Voor B2B-bedrijven in Oss is de website vaak het eerste wat een inkoper of nieuwe medewerker ziet. Dat vraagt om duidelijke specialismen, echte foto's van de productie en een makkelijke manier om contact op te nemen. Voor winkels en praktijken in het centrum draait het juist om lokale vindbaarheid en actuele openingstijden."),
 "eindhoven": ("Eindhoven is de vijfde stad van Nederland en het centrum van de Brainport-regio, met de TU/e, de High Tech Campus en een sterk netwerk van technologiebedrijven en toeleveranciers. Daarnaast kent de stad een grote creatieve sector rond Strijp-S en de Dutch Design Week, en een levendige binnenstad met horeca en retail.",
               "Bezoekers in Eindhoven zijn gewend aan goed ontworpen, snelle websites; een trage of verouderde site valt hier eerder op dan elders. Voor tech- en B2B-bedrijven komt daar vaak een internationaal publiek bij, waardoor een Engelse versie al snel nodig is."),
 "tilburg": ("Tilburg is de tweede stad van Brabant, met een sterke mix van onderwijs (Tilburg University en Fontys), logistiek langs de A58 en een groeiende creatieve sector in de Spoorzone en rond de Piushaven. In wijken als de Reeshof en in Berkel-Enschot werken veel lokale vakmensen, praktijken en winkels vooral voor hun eigen buurt.",
             "Dat geeft ondernemers in Tilburg een gevarieerd publiek: studenten en jonge gezinnen die vooral mobiel zoeken, en bedrijven in logistiek en dienstverlening die zakelijk inkopen. We kiezen per site welk publiek voorop staat en richten tekst, vormgeving en vindbaarheid daarop in."),
 "breda": ("Breda heeft een sterke binnenstad rond de Grote Markt met veel horeca, retail en evenementen. Daarnaast zitten er veel zakelijke dienstverleners, bouwbedrijven en logistieke bedrijven aan de A16 richting België. Rond de stad liggen kernen als Prinsenbeek, Teteringen, Bavel en Ulvenhout, elk met hun eigen ondernemers.",
           "Omdat Breda veel bezoekers trekt, zoeken mensen hier vaak vooraf online naar een restaurant, winkel of dienst. Je website moet dan in één oogopslag laten zien wat je biedt en hoe ze je bereiken. Voor zakelijke klanten telt juist betrouwbaarheid: duidelijke diensten, referenties en een snelle offerte-aanvraag."),
 "nijmegen": ("Nijmegen is een studenten- en zorgstad: de Radboud Universiteit, de HAN en het Radboudumc trekken veel jonge mensen en zorgprofessionals. Daarnaast heeft de stad een sterke horeca- en evenementencultuur, met de Waalkade en de binnenstad als middelpunt. Aan de noordkant van de Waal groeit Nijmegen-Noord met Lent.",
              "Veel Nijmegenaren zoeken diensten via hun telefoon en social media. Een website die snel laadt, goed werkt op mobiel en gekoppeld is aan Instagram of een afsprakensysteem past daar het best bij. Voor zorgpraktijken hoort er heldere informatie bij over wat je doet en hoe iemand bij je terechtkan."),
 "waalwijk": ("Waalwijk was lange tijd het centrum van de Nederlandse schoen- en lederindustrie. Tegenwoordig is het vooral een logistieke regio, met grote distributiecentra en transportbedrijven langs de A59. In het centrum en in Sprang-Capelle en Waspik zitten winkels, horeca en dienstverleners.",
              "Voor logistieke bedrijven is de website het visitekaartje richting opdrachtgevers én sollicitanten. Voor winkels en horeca draait het om lokale vindbaarheid in De Langstraat. Wie in Waalwijk zoekt, gebruikt net zo vaak 'webdesign' of 'internetbureau' als 'website laten maken'; we zorgen dat je site op al die vragen een duidelijk antwoord geeft."),
 "uden": ("Uden is het grootste winkelcentrum van de gemeente Maashorst en heeft met ziekenhuis Bernhoven een belangrijke zorgfunctie. Op de bedrijventerreinen zitten bouw-, installatie- en productiebedrijven, en het buitengebied kent veel agrarische ondernemers. In de dorpen eromheen, zoals Nistelrode en Heesch, zitten veel bouw- en klusbedrijven die in de hele regio werken.",
          "Voor winkels en horeca in Uden draait het om lokale vindbaarheid en een goed bijgehouden Google Bedrijfsprofiel. Bouw- en technische bedrijven willen vooral hun werkgebied en vakmanschap laten zien. Omdat klanten ook uit Veghel, Oss en Boekel komen, richten we je site op de hele regio en niet alleen op Uden."),
 "veghel": ("Veghel ligt aan de Zuid-Willemsvaart en de A50 en is uitgegroeid tot een van de belangrijkste werkgeverscentra van Noordoost-Brabant. Naast grote bedrijven zit er een dicht netwerk van toeleveranciers, transporteurs en technische dienstverleners. Sinds 2017 hoort Veghel bij de gemeente Meierijstad, samen met Schijndel en Sint-Oedenrode.",
            "Voor het MKB in Veghel is de concurrentie om personeel groot. Een website die laat zien hoe het is om bij jou te werken, met echte foto's of een korte video, helpt daarbij net zo veel als je dienstenpagina. Zakelijke klanten letten vooral op heldere specialismen en een snelle manier om contact op te nemen."),
 "schijndel": ("Schijndel is na Veghel de grootste kern van Meierijstad, met een compact centrum en veel lokale winkels. Het dorp heeft een sterk verenigingsleven en veel familiebedrijven in bouw, techniek en de agrarische sector. Wijbosch ligt er direct tegenaan, en in het buitengebied richting Sint-Oedenrode en Boxtel zitten veel kleinere ondernemers.",
               "Klanten in Schijndel kiezen vaak voor een bedrijf dat ze kennen of dat iemand aanraadt. Je website moet dat vertrouwen bevestigen: wie je bent, wat je hebt gemaakt en wat klanten zeggen. Grote beloftes werken hier minder goed dan echte foto's, reviews en een persoonlijke toon."),
 "boxtel": ("Boxtel is een knooppunt midden in Brabant: het station ligt op de lijnen richting Eindhoven, Tilburg en Den Bosch, en de A2 loopt vlak langs de gemeente. Rond de Dommel en natuurgebied Kampina zitten horeca- en recreatiebedrijven die veel bezoekers van buiten trekken. Bedrijven vind je zowel in het centrum als op de bedrijventerreinen langs de A2.",
            "Voor horeca, recreatie en winkels in Boxtel is een groot deel van de klanten bezoeker. Die zoeken op hun telefoon naar openingstijden, route en sfeer, vaak vlak voordat ze komen. Voor zakelijke dienstverleners is de centrale ligging juist een argument: vanuit Boxtel ben je snel in Den Bosch, Eindhoven en Tilburg."),
 "sint-michielsgestel": ("De gemeente Sint-Michielsgestel bestaat uit kernen met elk een eigen karakter: Sint-Michielsgestel aan de Dommel, Berlicum, Den Dungen, Gemonde en Middelrode. Er wonen veel gezinnen en werken veel zelfstandigen, en de nabijheid van Den Bosch maakt het een fijne plek voor dienstverleners die rustiger willen zitten. In het buitengebied liggen landgoederen en agrarische bedrijven.",
                         "Omdat de kernen klein zijn, is een goede reputatie hier alles. Een verzorgde website die duidelijk laat zien wie je bent, helpt om die reputatie online vast te houden. We zorgen dat je in alle kernen gevonden wordt, en niet alleen op de naam van de gemeente."),
 "zaltbommel": ("Zaltbommel is de hoofdplaats van de Bommelerwaard, het gebied tussen Maas en Waal. De historische binnenstad binnen de vestingwallen trekt bezoekers, terwijl de ligging aan de A2 en het spoor de stad aantrekkelijk maakt voor transport, groothandel en bouw. In de dorpen eromheen zitten veel tuinders, agrarische bedrijven en vakmensen.",
                "Voor ondernemers in de Bommelerwaard is de regio het werkgebied, niet alleen de eigen plaats. We noemen daarom de dorpen waar je klanten vandaan komen, en zorgen dat je ook gevonden wordt door klanten aan de Brabantse kant van de Waal."),
 "drunen": ("Drunen is de grootste kern van de gemeente Heusden, waartoe ook Vlijmen, Nieuwkuijk, Elshout, Haarsteeg, Oudheusden en de vestingstad Heusden horen. Aan de zuidkant ligt Nationaal Park De Loonse en Drunense Duinen, en Drunen heeft een sterk MKB in bouw, techniek en dienstverlening.",
            "Omdat de gemeente uit veel kernen bestaat, zoeken klanten vaak op de naam van hun eigen dorp of op 'Heusden'. Een website die die namen natuurlijk noemt, wordt vaker gevonden. Voor recreatie en horeca rond de Duinen komen er bezoekers uit de hele regio bij, die vooral letten op sfeer en bereikbaarheid."),
 "helmond": ("Helmond heeft een rijke industriële geschiedenis in textiel en metaal en is nu een van de centra van de Nederlandse automotive-sector, met de Automotive Campus en veel technische toeleveranciers. De stad groeit met wijken als Brandevoort en Dierdonk, waar installateurs, bouwers en praktijken veel werk hebben.",
             "Voor technische bedrijven in Helmond is de website vaak de plek waar opdrachtgevers en monteurs je als eerste tegenkomen. Duidelijke specialismen, certificeringen en echte projectfoto's maken het verschil. Voor winkels, horeca en zorg in de wijken telt vooral lokale vindbaarheid: wie in Brandevoort of Mierlo-Hout zoekt, wil een bedrijf in de buurt."),
 "veldhoven": ("Veldhoven ontstond uit een aantal dorpen en is uitgegroeid tot een belangrijke technologiegemeente. ASML heeft hier zijn hoofdkantoor, Máxima MC is een van de grote ziekenhuizen in de regio, en op De Run zitten veel high-tech toeleveranciers. De oude kernen Zeelst, Meerveldhoven, Oerle en Veldhoven-Dorp hebben nog steeds hun eigen karakter.",
               "Voor bedrijven in de high-tech keten is de website vooral een visitekaartje voor internationale opdrachtgevers en specialisten die een baan zoeken: Engels, duidelijke technische informatie en een professionele uitstraling zijn dan belangrijk. Voor zorgpraktijken, winkels en horeca telt juist lokale vindbaarheid in Veldhoven en de buurgemeenten."),
# --- buiten Brabant ---
 "barneveld": ("Barneveld hoort bij Regio Foodvalley en heeft van oudsher een sterke agrarische en pluimveesector. Daaromheen is een breed netwerk van vakbedrijven ontstaan: bouwers, installateurs, loodgieters en toeleveranciers, vaak familiebedrijven. Veel van die bedrijven werken ver buiten de gemeente.",
               "Dat zie je terug bij onze klanten hier: GK Vloerverwarming werkt door heel Nederland, MSB Vloerverwarming in de regio van Barneveld tot Apeldoorn, en Installatiebedrijf H. Ploeg vooral voor woningen en bedrijven in en rond Barneveld. Voor je website betekent dat: kies bewust of je lokaal of landelijk gevonden wilt worden, en richt je pagina's daarop in."),
 "amersfoort": ("Amersfoort is een forensen- en dienstenstad: door de ligging bij knooppunt Hoevelaken en het grote station zitten er veel kantoren, ICT-bedrijven en zakelijke dienstverleners. In de nieuwere wijken als Vathorst en Nieuwland wonen veel gezinnen, en in de dorpen rondom, van Nijkerk tot Woudenberg, zit een sterk MKB in bouw en installatie.",
                "Voor je website betekent dat twee dingen. Zakelijke klanten vergelijken grondig, dus je site moet vertrouwen wekken. Particulieren in de nieuwbouwwijken zoeken juist snel een vakman in de buurt. Bij onze installateurs rond Amersfoort richten we de site daarom op de dorpen en wijken waar het werk vandaan komt."),
 "apeldoorn": ("Naast grote werkgevers als de Belastingdienst en het Kadaster heeft Apeldoorn een breed MKB in bouw, installatie, zakelijke dienstverlening en zorg. Ten noorden van de stad, in Vaassen, Epe en Heerde, zitten veel vakbedrijven die in de hele regio werken. Op de Veluwe zelf draait veel om recreatie: campings, B&B's en horeca.",
               "Voor installateurs en bouwers is de regio het werkgebied, niet alleen de eigen plaats; we noemen daarom de dorpen waar je klanten zitten. Voor recreatiebedrijven telt vooral de beleving: sfeerbeelden, informatie over de omgeving en een makkelijke manier om te boeken."),
 "zwolle": ("Zwolle is het centrum van een regio van Kampen tot Dalfsen. Met Isala en Windesheim zijn zorg en onderwijs grote werkgevers, en de binnenstad trekt winkelend publiek uit de hele omgeving. Op Hessenpoort en de Marslanden zitten logistiek, groothandel en techniek.",
            "Voor winkels in de binnenstad telt dat klanten vooraf online kijken wat je verkoopt. Voor loodgieters en installateurs telt vooral snelheid: bij een lekkage of verstopping bellen mensen het eerste bedrijf dat ze vinden. Daarom staat bij RSTK Rioolservice in Kampen '24/7' al in de paginatitel."),
}
L = 'style="color:var(--gold-deep)"'
FAQ2 = {
 "den-bosch": [("Kunnen jullie ook een webshop bouwen voor mijn winkel in de binnenstad?", "Ja. We bouwen ook webshops en koppelen die waar nodig aan je betaalsysteem. Je krijgt vooraf een offerte op maat."),
               ("Doen jullie ook SEO voor bedrijven in Den Bosch?", f"Ja. Bij elke site zetten we de basis-SEO goed; daarna kan SEO voor €79 per maand, met maandelijkse rapportage. Lees ook onze <a href=\"/blog/lokale-seo-tips\" {L}>tips voor lokale SEO</a>.")],
 "rosmalen": [("Moet ik op 'Rosmalen' of op 'Den Bosch' gevonden worden?", "Allebei. Klanten zoeken op beide namen; we nemen ze natuurlijk mee in je teksten en in je Google Bedrijfsprofiel."),
              ("Kunnen jullie mijn bestaande website verbeteren?", "Ja. In een gratis adviesgesprek kijken we naar je huidige site en adviseren we of verbeteren of opnieuw bouwen slimmer is.")],
 "vught": [("Kunnen jullie ook professionele foto's maken voor mijn winkel in Vught?", "Ja. Een foto- of videoshoot op locatie kost €250, met dronebeelden €300, inclusief montage en kleurcorrectie."),
           ("Is een webshop voor een kleine winkel de moeite waard?", "Dat hangt af van je producten en klanten. In een gratis gesprek kijken we of een webshop loont, of dat een site met je assortiment en een duidelijke contactknop genoeg is.")],
 "oss": [("Werken jullie ook in Ravenstein en Lith?", "Ja. We bouwen voor ondernemers in de hele gemeente Oss, inclusief Berghem, Lith en Ravenstein."),
         ("Kunnen jullie dronebeelden maken van ons bedrijfspand in Oss?", "Ja. Een shoot met drone kost €300. We checken vooraf of er op die plek gevlogen mag worden.")],
 "eindhoven": [("Bouwen jullie ook websites voor startups in Eindhoven?", "Ja. Een startup heeft vaak genoeg aan een compacte, snelle site die later meegroeit; maatwerk begint bij €375."),
               ("Kunnen jullie een cinematische scroll-website maken?", f"Ja. Een 3D Cinematic website kost €749 eenmalig. Lees meer in ons artikel over <a href=\"/blog/wat-is-een-cinematic-scroll-website\" {L}>cinematic scroll-websites</a>.")],
 "tilburg": [("Bouwen jullie ook webshops in Tilburg?", "Ja. De prijs hangt af van het aantal producten en koppelingen; je krijgt vooraf een offerte op maat."),
             ("Werken jullie ook voor startende ondernemers in Tilburg?", "Ja. Voor een startende onderneming is een compacte site vaak genoeg; maatwerk begint bij €375 en is later uit te breiden.")],
 "breda": [("Werken jullie ook in Prinsenbeek en Teteringen?", "Ja. We bouwen voor ondernemers in de hele gemeente Breda, ook in Prinsenbeek, Teteringen, Bavel en Ulvenhout."),
           ("Kunnen jullie mijn restaurant of winkel in Breda filmen?", "Ja. Een video- of fotoshoot op locatie kost €250, met drone €300, inclusief montage.")],
 "nijmegen": [("Kunnen jullie een online agenda of afsprakensysteem koppelen?", "Ja. We koppelen je website aan je agenda- of afsprakensysteem, zodat klanten direct een afspraak kunnen maken."),
              ("Werken jullie ook in Lent en Nijmegen-Noord?", "Ja. We bouwen voor ondernemers aan beide kanten van de Waal.")],
 "waalwijk": [("Kunnen jullie een vacaturepagina maken voor ons logistieke bedrijf?", "Ja. We maken vacaturepagina's met beelden van de werkvloer en een eenvoudig sollicitatieformulier; een video-opname op locatie kost €250."),
              ("Doen jullie ook online marketing in Waalwijk?", "We doen SEO (€79 per maand) en social media beheer (vanaf €79 per maand). Daarmee werk je naast je website aan vindbaarheid en zichtbaarheid.")],
 "uden": [("Bouwen jullie ook webshops in Uden?", "Ja. Je krijgt vooraf een offerte op maat, afhankelijk van het aantal producten en koppelingen."),
          ("Kunnen jullie ook social media voor mijn bedrijf in Uden beheren?", "Ja. Social media beheer kost vanaf €79 per maand, met content in jouw huisstijl en een maandelijkse rapportage.")],
 "veghel": [("Werken jullie in heel Meierijstad?", "Ja. We bouwen voor ondernemers in Veghel, Schijndel, Sint-Oedenrode en de kerkdorpen; voor Schijndel hebben we ook een eigen pagina."),
            ("Kunnen jullie onze website ook in het Engels maken?", "Ja. Voor bedrijven met internationale klanten of medewerkers bouwen we meertalige websites met echte vertalingen.")],
 "schijndel": [("Kunnen jullie een korte bedrijfsvideo maken voor ons familiebedrijf?", "Ja. Een video-opname op locatie kost €250, inclusief montage en kleurcorrectie; met drone €300."),
               ("Heeft een kleine ondernemer echt een website nodig?", "Verplicht is het niet, maar wie je via via aangeraden krijgt, zoekt je bijna altijd even op. Een compacte site met je werk, reviews en contactgegevens is dan genoeg om vertrouwen te geven.")],
 "boxtel": [("Kunnen jullie een website maken voor een B&B of recreatiebedrijf in Boxtel?", "Ja. Voor recreatie maken we sites met sfeerbeelden, informatie over de omgeving en een duidelijke knop om te reserveren of contact op te nemen."),
            ("Hebben jullie ervaring met vakantieverhuur?", "Ja. Voor vakantiehuis Echt Grieks bouwden we een site die sfeer en boekingen combineert, en we maken villa-films in Spanje.")],
 "sint-michielsgestel": [("Kunnen jullie een website maken voor mijn praktijk aan huis?", "Ja. Voor praktijken aan huis bouwen we rustige, persoonlijke sites met uitleg over je werkwijze en een duidelijke manier om een afspraak te maken."),
                         ("Hoe word ik in mijn eigen dorp gevonden?", f"Door de naam van je kern op je site te noemen, een volledig Google Bedrijfsprofiel en reviews van klanten. Lees ook onze <a href=\"/blog/lokale-seo-tips\" {L}>tips voor lokale SEO</a>.")],
 "zaltbommel": [("Werken jullie ook voor tuinbouwbedrijven in de Bommelerwaard?", "Ja. We bouwen ook voor agrarische en tuinbouwbedrijven, met duidelijke informatie over je producten en eventueel dronebeelden van je bedrijf."),
                ("Ligt Zaltbommel niet al in Gelderland?", "Klopt, Zaltbommel ligt in Gelderland, net over de Waal vanaf Den Bosch. Voor ons maakt dat niets uit: we zijn er in twintig minuten.")],
 "drunen": [("Werken jullie ook in vestingstad Heusden?", "Ja. Heusden hoort bij dezelfde gemeente als Drunen, en voor horeca en winkels in de vestingstad maken we ook graag foto's en video."),
            ("Hoe laat ik mijn projecten goed zien op mijn website?", "Met een projectpagina per klus: een paar sterke foto's, een korte omschrijving en de plaats. Dat werkt voor klanten én voor Google.")],
 "helmond": [("Kunnen jullie een configurator of calculator bouwen?", "Ja. Net als de leasecalculator voor CarsLease bouwen we rekenhulpen en configurators; je krijgt vooraf een offerte op maat."),
             ("Werken jullie ook in de rest van de regio Eindhoven?", "Ja. Voor Eindhoven en Veldhoven hebben we eigen pagina's, en we bouwen voor ondernemers in de hele regio.")],
 "barneveld": [("Werken jullie ook in Voorthuizen en Kootwijkerbroek?", "Ja. We bouwen voor ondernemers in de hele gemeente Barneveld, dus ook in Voorthuizen, Kootwijkerbroek, Garderen en Stroe."),
               ("Wat kost een website voor een installatiebedrijf?", f"Een Horizon website kost €375 eenmalig; SEO kan erbij voor €79 per maand. Lees meer op onze pagina <a href=\"/website-voor-installateurs\" {L}>website voor installateurs</a>.")],
 "amersfoort": [("Werken jullie ook in Hoogland en Vathorst?", "Ja. We bouwen voor ondernemers in heel Amersfoort, ook in Hoogland en Vathorst, en in Leusden en Soest."),
                ("Doen jullie ook SEO voor bedrijven in Amersfoort?", "Ja. Bij elke site zetten we de basis-SEO goed; daarna kan SEO voor €79 per maand, met maandelijkse rapportage.")],
 "apeldoorn": [("Werken jullie ook in Epe en Vaassen?", "Ja. In Vaassen zitten al twee van onze klanten, en we werken in de hele regio Apeldoorn."),
               ("Is Apeldoorn niet te ver weg voor jullie?", "Nee. De kennismaking doen we via telefoon of video en je ziet eerst gratis een testwebsite. Daarna gaat alles online.")],
 "zwolle": [("Werken jullie ook in Kampen en Hattem?", "Ja. In Kampen zit al een van onze klanten, en we bouwen voor ondernemers in de hele regio Zwolle."),
            ("Kan ik mijn website zelf bijhouden?", "Ja. We bouwen in een gebruiksvriendelijk CMS en leggen uit hoe je teksten en beelden zelf aanpast.")],
 "veldhoven": [("Kunnen jullie een werken-bij-pagina maken?", "Ja. We maken werken-bij-pagina's met beelden van je team en werkplek; een video-opname op locatie kost €250."),
               ("Werken jullie ook voor zorgpraktijken in Veldhoven?", "Ja. Voor praktijken bouwen we rustige, duidelijke sites met uitleg over behandelingen en een eenvoudige manier om een afspraak te maken.")],
}
for c in CITIES:
    c.update(LOCAL[c["slug"]]); c["biz"] = BIZ[c["slug"]]; c["faq"] = c["faq"] + FAQ2[c["slug"]]

# Echte klanten (CRM, fase 'afgerond'); naam en plaats zoals op hun eigen site. Yannick gaf akkoord voor naam + link,
# behalve Claassen Elektro: die nooit noemen. Velden: naam, link (eigen site of ons projectverhaal), plaats, wat ze doen, installateur?
CLIENTS = {
 "vlaspoel": ("Verkeersschool Vlaspoel", "https://verkeersschoolvlaspoel.nl", "Rosmalen", "rijlessen voor auto en motor", False),
 "barten": ("Regio Autorijschool Peter Barten", "https://peterbartenrijschool.lovable.app", "Heesch", "rijlessen", False),
 "gremmen": ("Gremmen Bouw & Timmerwerken", "https://gremmenbouw.nl", "Nistelrode", "verbouwingen en maatwerk timmerwerk", False),
 "dejongh": ("De Jongh Projects", "https://dejonghprojects.nl", "Oss", "houtrotherstel en kozijnreparatie", False),
 "vanloosbroek": ("Van Loosbroek Installatietechniek", "https://vanloosbroekinstallatietechniek.nl", "Oss", "airco, warmtepompen en cv-ketels", True),
 "bato": ("Bato Ontstoppingen", "https://www.bato-ontstoppingen.nl", "Valkenswaard", "rioolontstopping en camera-inspectie", True),
 "bodyscan": ("BodyScan Waalre", "/werk-bodyscan", "Waalre", "gezondheidsscans", False),
 "vanbeveren": ("Van Beveren Dienstverlening", "https://vanbevereninstallaties.nl", "Breda", "klussen en installaties", True),
 "bevmontage": ("Beveiligings-Montage", "https://beveiligings-montage.nl", "Sprundel", "inbraaksignalering en camerasystemen", True),
 "ahrens": ("Ahrens Elektro", "https://ahrens-elektro.nl", "Druten", "elektra, zonnepanelen en laadpalen", True),
 "gennissen": ("Gennissen Beveiliging", "https://gennissenbeveiliging.nl", "Alphen", "alarmsystemen en camerabewaking", True),
 "gk": ("GK Vloerverwarming", "https://gkvloerverwarming.nl", "Barneveld", "vloerverwarming", True),
 "msb": ("MSB Vloerverwarming", "https://msbvloerverwarming.nl", "Barneveld", "vloerverwarming", True),
 "ploeg": ("Installatiebedrijf H. Ploeg", "https://installatiebedrijfploeg.nl", "Barneveld", "verwarming, sanitair en loodgieterswerk", True),
 "klok": ("Klok en van Ginkel Elektrotechniek", "https://klokenvanginkel.nl", "Scherpenzeel", "elektrotechniek", True),
 "michel": ("Michel Installatie", "https://loodgietermichel.nl", "Scherpenzeel", "loodgieterswerk en badkamers", True),
 "dejonge": ("De Jonge Elektrotechniek", "/werk-dejonge", "Nijkerk", "elektra, data en beveiliging", True),
 "elektropost": ("Elektropost", "/werk-elektropost", "Woudenberg", "elektrotechniek", True),
 "laseur": ("Laseur Elektrotechniek", "https://www.laseur-elektrotechniek.nl", "Bunnik", "elektrotechniek en verduurzaming", True),
 "gj": ("G.J. Elektro", "https://gjelektrotechniek.nl", "Vaassen", "elektrotechnische installaties", True),
 "jm": ("JM Installatie Service", "https://jm-installatieservice.nl", "Vaassen", "sanitair, cv en ventilatie", True),
 "vlaskamp": ("Vlaskamp Installatietechniek", "https://www.vlaskampinstallatietechniek.nl", "Heerde", "elektrotechniek", True),
 "vanbreukelen": ("Woninginrichting van Breukelen", "https://woninginrichtingvanbreukelen.nl", "Zwolle", "raambekleding, vloeren en slaapkamers", False),
 "rstk": ("RSTK Rioolservice", "https://rioolontstopperkampen.nl", "Kampen", "loodgieter en rioolservice", True),
 "driehuizen": ("Loodgietersbedrijf D. Driehuizen", "https://loodgieterdriehuizen.nl", "Heemstede", "loodgieterswerk, cv en badkamers", True),
}
CITY_CLIENTS = {
 "den-bosch": ["vlaspoel", "barten", "vanloosbroek", "gremmen", "dejongh"], "rosmalen": ["vlaspoel", "barten", "gremmen"],
 "oss": ["vanloosbroek", "dejongh", "barten", "gremmen"], "uden": ["gremmen", "vanloosbroek", "barten", "dejongh"], "veghel": ["vanloosbroek", "gremmen"],
 "eindhoven": ["bato", "bodyscan"], "veldhoven": ["bodyscan", "bato"], "helmond": ["bato", "bodyscan"],
 "breda": ["vanbeveren", "bevmontage"], "nijmegen": ["ahrens", "gennissen"],
 "barneveld": ["gk", "msb", "ploeg", "klok", "michel", "dejonge"], "amersfoort": ["dejonge", "elektropost", "klok", "michel", "laseur", "ploeg"],
 "apeldoorn": ["gj", "jm", "vlaskamp"], "zwolle": ["vanbreukelen", "rstk", "vlaskamp"],
}
def client_link(k):
    n, u = CLIENTS[k][:2]
    ext = ' target="_blank" rel="noopener"' if u.startswith("http") else ""
    return f'<a href="{u}"{ext} style="color:inherit;text-decoration:none">{n}</a>'
def client_rows(keys):
    return rows([(client_link(k), f"{CLIENTS[k][2]} · {CLIENTS[k][3]}") for k in keys])

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
V_INTRO = [lambda c: f"Een website die past bij <span class=\"gold-text\">{c['full']}.</span>",
           lambda c: f"Gebouwd voor ondernemers <span class=\"gold-text\">{c['in_']}.</span>",
           lambda c: f"Jouw bedrijf, <span class=\"gold-text\">goed online.</span>",
           lambda c: f"Van eerste schets <span class=\"gold-text\">tot livegang.</span>"]
V_PRICE = ["Vaste prijzen: Horizon website €375, 3D Cinematic website €749, SEO €79 per maand",
           "Een Horizon website kost €375, een 3D Cinematic website €749",
           "Websites vanaf €375; SEO kan erbij voor €79 per maand",
           "Geen uurtje-factuurtje: je weet vooraf wat je betaalt, vanaf €375",
           "Maatwerk vanaf €375, cinematic vanaf €749, zonder verborgen kosten"]
V_SECT = ["Voor wie we hier vooral bouwen:", "Sectoren waar we hier vaak voor werken:", "Typische opdrachtgevers in deze omgeving:"]
V_PLACES = [lambda c: f"We werken ook voor klanten in {c['places']}.",
            lambda c: f"Ook vanuit {c['places']} komen aanvragen binnen.",
            lambda c: f"Ons werkgebied rond {c['name']}: {c['places']}.",
            lambda c: f"Klanten uit {c['places']} vinden je via Google, op een site die op elke telefoon snel laadt."]
V_FAQH = [lambda c: f"Website laten maken {c['in_']}: <span class=\"gold-text\">goed om te weten</span>",
          lambda c: f"Vragen uit <span class=\"gold-text\">{c['name']}</span>",
          lambda c: f"Wat ondernemers {c['in_']} <span class=\"gold-text\">ons vragen</span>"]
V_CLH = [lambda c: "Klanten <span class=\"gold-text\">in de buurt</span>",
         lambda c: "Zij gingen je <span class=\"gold-text\">voor</span>",
         lambda c: f"Ons werk rond <span class=\"gold-text\">{c['name']}</span>"]
def client_section(c, h):
    keys = CITY_CLIENTS.get(c["slug"])
    if not keys: return ""
    inst = ('<p style="margin-top:32px;color:var(--ink-dim)">Ben je zelf installateur? Bekijk <a href="/website-voor-installateurs" style="color:var(--gold-deep)">wat we voor installatiebedrijven maken</a>.</p>'
            if any(CLIENTS[k][4] for k in keys) else "")
    return f'''
  <section class="bg-cream full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Klanten uit de regio</p>
        <h2>{h(c)}</h2>
        <p class="lead">Websites die we bouwden voor ondernemers in en rond {c['name']}. Klik op een naam om de site of het project te bekijken.</p>
      </div>
      {client_rows(keys)}
      {inst}
    </div>
  </section>
'''
V_CTA = [lambda c: ("Eerst zien, dan beslissen.", f"We bouwen gratis een testwebsite voor jouw bedrijf {c['in_']}. Bevalt het? Dan gaan we door. Zo niet, dan kost het je niets."),
         lambda c: ("Benieuwd hoe jouw site eruit kan zien?", "Vraag een gratis testwebsite aan. Je ziet het ontwerp voordat je iets betaalt."),
         lambda c: (f"Klaar voor een nieuwe website {c['in_']}?", "Vertel kort over je bedrijf; je hoort binnen één werkdag van ons en krijgt eerst een gratis testversie."),
         lambda c: ("Zonder risico beginnen.", "Je krijgt eerst een gratis testwebsite. Pas als je tevreden bent, gaan we verder.")]
for ci, c in enumerate(CITIES):
    vi = lambda arr: arr[ci % len(arr)]
    slug = f"website-laten-maken-{c['slug']}"; url = f"{BASE}/{slug}"
    title = f"Website laten maken {c['name']}: {c['tag']} | Skyline Digital"
    desc = f"Website laten maken {c['in_']}? Maatwerk websites vanaf €375 voor {c['who']}. Snel, vindbaar en eerst gratis een testwebsite."
    near = [CITY_BY[n] for n in c["near"]]
    faqs = c["faq"]
    ld = {"@context":"https://schema.org","@graph":[
        crumbs_ld(url, [("Regio's", BASE+"/regio"), (f"Website laten maken {c['name']}", url)]),
        {"@type":"Service","@id":url+"#service","name":f"Website laten maken {c['in_']}","serviceType":"Webdesign en websiteontwikkeling","provider":ORG_REF,
         "areaServed":{"@type":"City","name":c["full"],"containedInPlace":{"@type":"AdministrativeArea","name":c["region"]}},"url":url,
         "offers":[{"@type":"Offer","name":"Horizon website","price":"375","priceCurrency":"EUR"},{"@type":"Offer","name":"3D Cinematic website","price":"749","priceCurrency":"EUR"}]},
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
      <p class="lead">Maatwerk websites vanaf €375 voor {c['who']}. {c['travel']}</p>
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
          <h2>{vi(V_INTRO)(c)}</h2>
          <p class="lead">{c['intro']}</p>
          <p>{c['intro2']}</p>
          <p style="font-size:.95rem;color:var(--ink-dim)">{vi(V_PRICE)} · <a href="/pricing" style="color:var(--gold-deep)">alle prijzen</a></p>
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
        <p class="eyebrow">Lokale markt</p>
        <h2>Ondernemen <span class="gold-text">{c['in_']}</span></h2>
        <p class="lead">{c['biz'][0]}</p>
      </div>
      <p class="reveal" style="max-width:720px;color:var(--on-dark-dim)">{c['biz'][1]}</p>
      <p style="margin:36px 0 18px;max-width:720px;color:var(--on-dark)">{vi(V_SECT)}</p>
      <ul class="checks" style="max-width:720px">{sectors}</ul>
      <p style="margin-top:28px;max-width:720px;color:var(--on-dark-dim)">{vi(V_PLACES)(c)}</p>
      <p style="margin-top:18px;max-width:720px;color:var(--on-dark-dim)"><strong style="color:var(--on-dark)">{c['case'][0]}.</strong> {c['case'][2]} <a href="{c['case'][1]}" style="color:var(--gold)">Bekijk het project →</a></p>
    </div>
  </section>
{client_section(c, vi(V_CLH))}
  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Veelgestelde vragen</p>
        <h2>{vi(V_FAQH)(c)}</h2>
      </div>
      {faq_html(faqs)}
      <p style="margin-top:40px;text-align:center;color:var(--ink-dim)">Ook actief in {nearlinks} · <a href="/regio">alle regio's</a></p>
    </div>
  </section>

  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>{vi(V_CTA)(c)[0]}</h2>
      <p class="lead">{vi(V_CTA)(c)[1]}</p>
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite aanvragen</a><a href="/contact" class="btn btn-ghost-light">Plan een gesprek</a></div>
    </div>
  </section>

'''
    open(slug + ".html", "w").write(head(title, desc, url, "/assets/photo-laptop-desk.jpg", ld) + body + tail())

# ---------- Branchepagina: website voor installateurs ----------
# Opbouw volgens content/PAGINAPLAN.md (type 1); hoofdzoekwoord "website laten maken installatiebedrijf".
INSTALLERS = ["dejonge", "elektropost", "vanloosbroek", "gk", "msb", "ploeg", "klok", "michel", "laseur", "gj", "jm", "vlaskamp",
              "rstk", "driehuizen", "ahrens", "gennissen", "bato", "bevmontage", "vanbeveren"]
url = BASE + "/website-voor-installateurs"
title = "Website laten maken installatiebedrijf: vanaf €375 | Skyline Digital"
desc = "Website laten maken voor je installatiebedrijf? Ruim 20 installateurs, elektriciens en loodgieters gingen je voor. Vanaf €375, eerst gratis een testwebsite."
faqs = [
 ("Wat kost een website voor een installatiebedrijf?", f"Een Horizon website kost €375 eenmalig, een 3D Cinematic website €749. SEO kan erbij voor €79 per maand. Lees ook <a href=\"/blog/wat-kost-een-website-laten-maken\" {L}>wat een website laten maken kost</a>."),
 ("Hoe lang duurt het voordat mijn website online staat?", "Gemiddeld 4 tot 8 weken, afhankelijk van de omvang en hoe snel we foto's en feedback ontvangen. Je ziet eerst gratis een testwebsite."),
 ("Ik heb geen tijd om teksten te schrijven. Is dat een probleem?", "Nee. Met een paar gegevens over je diensten en werkgebied maken wij de teksten voor je testwebsite; jij past aan wat niet klopt."),
 ("Word ik gevonden op 'elektricien' of 'loodgieter' plus mijn plaats?", f"Daar richten we de site op: je belangrijkste diensten en je werkgebied krijgen een eigen plek, en de technische basis-SEO staat goed. Een vaste positie in Google kan niemand beloven; met SEO voor €79 per maand werken we daar elke maand aan. Lees ook onze <a href=\"/blog/lokale-seo-tips\" {L}>tips voor lokale SEO</a>."),
 ("Werken jullie ook voor installateurs buiten Brabant?", "Ja. Onze klanten zitten van Heemstede en Bunnik tot Kampen, Heerde en Sprundel. De kennismaking doen we via telefoon of video."),
 ("Kunnen jullie ook foto's of video van mijn projecten maken?", "Ja. Een foto- of videoshoot op locatie kost €250, met dronebeelden €300, inclusief montage en kleurcorrectie."),
]
ld = {"@context":"https://schema.org","@graph":[
    crumbs_ld(url, [("Website & SEO", BASE+"/website-seo"), ("Website voor installateurs", url)]),
    {"@type":"Service","@id":url+"#service","name":"Website laten maken voor installatiebedrijven","serviceType":"Webdesign voor installatiebedrijven","provider":ORG_REF,
     "audience":{"@type":"BusinessAudience","audienceType":"Installatiebedrijven, elektriciens en loodgieters"},"areaServed":{"@type":"Country","name":"Nederland"},"url":url,
     "offers":[{"@type":"Offer","name":"Horizon website","price":"375","priceCurrency":"EUR"},{"@type":"Offer","name":"3D Cinematic website","price":"749","priceCurrency":"EUR"},
               {"@type":"Offer","name":"SEO","price":"39","priceCurrency":"EUR","priceSpecification":{"@type":"UnitPriceSpecification","price":"39","priceCurrency":"EUR","unitText":"maand"}}]},
    faq_ld(url, faqs),
    {"@type":"WebPage","@id":url+"#webpage","url":url,"name":title,"description":desc,"inLanguage":"nl-NL","isPartOf":{"@id":BASE+"/#website"},"about":ORG_REF,"breadcrumb":{"@id":url+"#breadcrumb"}}]}
needs = [
 ("Gevonden worden op dienst en plaats", "Klanten zoeken op 'elektricien Nijkerk' of 'loodgieter Heemstede', niet op je bedrijfsnaam. Je belangrijkste diensten en de plaatsen waar je werkt krijgen daarom een vaste plek op de site. De site van De Jonge Elektrotechniek heet niet voor niets 'Elektricien Nijkerk'."),
 ("Direct kunnen bellen", "Bij een storing of lekkage bellen mensen het eerste bedrijf dat ze vinden. Je telefoonnummer staat daarom altijd in beeld, ook op de telefoon. RSTK Rioolservice in Kampen zet '24/7' zelfs in de paginatitel."),
 ("Vertrouwen in één oogopslag", "Certificeringen, jaren ervaring en reviews maken het verschil. Beveiligings-Montage laat zien dat ze VCA-gecertificeerd zijn, Bato Ontstoppingen dat ze er al sinds 1996 zijn."),
 ("Een duidelijk werkgebied", "Werk je in de regio of door heel Nederland? GK Vloerverwarming uit Barneveld installeert door het hele land, Van Loosbroek Installatietechniek werkt in heel Noord-Brabant. Dat staat op hun site meteen duidelijk."),
 ("Een offerte zonder gedoe", "Een kort formulier of een directe knop naar WhatsApp maakt de drempel laag. Bezoekers hoeven niet eerst een lange vragenlijst in te vullen."),
 ("Vakmensen werven", "Veel installatiebedrijven zoeken personeel. Een werken-bij-pagina met echte foto's of een korte video van de werkvloer helpt je opvallen."),
]
steps = [
 ("Kennismaking", "Een kort gesprek via telefoon, video of op locatie: welke diensten je levert, waar je werkt en welke uitstraling bij je past."),
 ("Gratis testwebsite", "We bouwen eerst een testversie met je logo, kleuren en diensten. Gratis en vrijblijvend."),
 ("Aanpassen tot het klopt", "Je geeft feedback en wij passen aan, tot je er trots op bent."),
 ("Live", "We regelen het domein en zetten de site live. Daarna kun je SEO of onderhoud erbij nemen."),
]
city_links = " · ".join(f'<a href="/website-laten-maken-{c["slug"]}" style="color:var(--gold-deep)">{c["name"]}</a>' for c in CITIES)
body = HEADER + f'''
  <section class="page-hero has-image">
    <div class="page-hero-bg"><img src="/assets/photo-installateur.jpg" alt="Installateur aan het werk bij een meterkast" /></div>
    <div class="page-hero-inner">
      <p class="crumbs"><a href="/">Home</a> · <a href="/website-seo">Website &amp; SEO</a> · Installateurs</p>
      <h1>Website laten maken voor je <span class="gold-text">installatiebedrijf.</span></h1>
      <p class="lead">Voor elektriciens, loodgieters, cv- en airco-installateurs en vloerverwarmingsspecialisten. Ruim 20 installatiebedrijven gingen je voor, van Heemstede tot Kampen.</p>
      <div class="hero-actions"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite</a><a href="#klanten" class="btn btn-ghost-light">Bekijk onze klanten</a></div>
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Kort antwoord</p>
        <h2>Wat kost een website voor een <span class="gold-text">installatiebedrijf?</span></h2>
        <p class="lead">Een complete website met meerdere pagina's kost bij ons €375 eenmalig: op maat, met je diensten, werkgebied en projecten, een duidelijke bel- en offerteknop en een SEO-vriendelijke opbouw. Wil je daarna hoger in Google komen, dan kan SEO erbij voor €79 per maand. Je ziet eerst gratis een testwebsite; pas als die bevalt, gaan we verder.</p>
      </div>
    </div>
  </section>

  <section class="bg-cream full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Wat de site moet doen</p>
        <h2>Zes dingen die een installateurswebsite <span class="gold-text">goed moet doen</span></h2>
        <p class="lead">Dit zien we bij elke installateur terugkomen, of je nu elektricien bent in Nijkerk of loodgieter in Heemstede.</p>
      </div>
      {rows(needs)}
    </div>
  </section>

  <section class="bg-dark full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Wat we maken</p>
        <h2>Alles voor je online zichtbaarheid, <span class="gold-text">vaste prijzen</span></h2>
        <p class="lead">Je kiest wat je nodig hebt. De meeste installateurs beginnen met een website en nemen later SEO of beeld erbij.</p>
      </div>
      <ul class="checks" style="max-width:760px">
        <li>Horizon website op maat: €375 eenmalig, of een 3D Cinematic website voor €749</li>
        <li>SEO voor €79 per maand, met maandelijkse rapportage</li>
        <li>Foto- en videoshoot van je projecten: €250, met dronebeelden €300</li>
        <li>Social media beheer vanaf €79 per maand</li>
        <li>Onderhoudsabonnement: je site veilig, snel en up-to-date</li>
      </ul>
      <p style="margin-top:28px;color:var(--on-dark-dim)">Alle prijzen en pakketten staan op onze <a href="/pricing" style="color:var(--gold)">prijzenpagina</a>.</p>
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Werkwijze</p>
        <h2>Zo werkt het, <span class="gold-text">in vier stappen</span></h2>
      </div>
      {rows(steps)}
    </div>
  </section>

  <section class="bg-cream full" id="klanten">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Klanten</p>
        <h2>Installateurs die <span class="gold-text">je voorgingen</span></h2>
        <p class="lead">Een greep uit de installatiebedrijven waarvoor we een website bouwden. Klik op een naam om de site live te bekijken. Bij De Jonge Elektrotechniek en Elektropost lees je hoe we het aanpakten.</p>
      </div>
      {client_rows(INSTALLERS)}
    </div>
  </section>

  <section class="bg-white full">
    <div class="wrap">
      <div class="section-head reveal">
        <div class="gold-rule"></div>
        <p class="eyebrow">Veelgestelde vragen</p>
        <h2>Website voor installateurs: <span class="gold-text">goed om te weten</span></h2>
      </div>
      {faq_html(faqs)}
      <p style="margin-top:40px;text-align:center;color:var(--ink-dim)">Ook per plaats: {city_links}</p>
    </div>
  </section>

  <section class="cta-band">
    <div class="inner reveal">
      <div class="gold-rule" style="margin-inline:auto"></div>
      <h2>Eerst zien hoe jouw site eruitziet?</h2>
      <p class="lead">We bouwen gratis een testwebsite voor je installatiebedrijf. Bevalt hij, dan gaan we verder. Zo niet, dan kost het je niets.</p>
      <div class="hero-actions hero-actions-center"><a href="/aanvraag" class="btn btn-gold">Gratis testwebsite aanvragen</a><a href="/contact" class="btn btn-ghost-light">Plan een gesprek</a></div>
    </div>
  </section>

'''
open("website-voor-installateurs.html", "w").write(head(title, desc, url, "/assets/photo-installateur.jpg", ld) + body + tail())

# ---------- Regio-hub ----------
url = BASE + "/regio"; title = "Website laten maken in Brabant, Gelderland en verder | Skyline Digital"
desc = f"Skyline Digital bouwt websites, video en content voor ondernemers in Den Bosch, Eindhoven, Tilburg en nog {len(CITIES) - 3} plaatsen in Brabant, Gelderland, Utrecht en Overijssel. Bekijk je regio."
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
      <p style="margin-top:40px;color:var(--ink-dim)">Installateur? Bekijk ook onze pagina <a href="/website-voor-installateurs">website voor installateurs</a>.</p>
      <p style="margin-top:12px;color:var(--ink-dim)">Staat jouw plaats er niet bij? We werken door heel Nederland en op afstand — <a href="/contact">neem contact op</a>.</p>
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
# Volgorde = plaatsen met de meeste vertoningen in Search Console (okt 2026), plus de installateurspagina.
FOOTER_CITIES = ["den-bosch", "waalwijk", "oss", "uden", "nijmegen", "breda", "eindhoven", "tilburg"]
NEW_COL = ('        <div class="footer-col"><h4>Regio\'s</h4>'
           + "".join(f'<a href="/website-laten-maken-{k}">Website laten maken {CITY_BY[k]["name"]}</a>' for k in FOOTER_CITIES)
           + '<a href="/website-voor-installateurs">Website voor installateurs</a><a href="/regio">Alle regio\'s</a></div>\n')
for path in glob.glob("*.html") + glob.glob("blog/*.html"):
    if path.startswith("google"): continue
    s = open(path).read()
    if "<h4>Regio's</h4>" in s:
        s = re.sub(r"        <div class=\"footer-col\">\s*<h4>Regio's</h4>.*?</div>\n", NEW_COL, s, count=1, flags=re.S)
    else:
        s = re.sub(r'        <div class="footer-col">\n          <h4>Over ons</h4>.*?</div>\n', NEW_COL, s, count=1, flags=re.S)
    if '<a href="/blog">Blog</a>' not in s.split('<footer', 1)[-1]:
        s = s.replace('          <a href="/aanvraag" class="footer-gratis">★ Gratis testwebsite</a>', '          <a href="/blog">Blog</a>\n          <a href="/aanvraag" class="footer-gratis">★ Gratis testwebsite</a>', 1)
    # relatieve assets in footer/nav werken niet vanuit /blog/ — maak ze absoluut
    if path.startswith("blog/"):
        s = s.replace('src="assets/', 'src="/assets/')
    open(path, "w").write(s)

# ---------- Sitemap ----------
urls = [("/",1.0,"weekly"),("/website-seo",0.9,"monthly"),("/drone-video",0.9,"monthly"),("/social-media",0.9,"monthly"),("/ai-content",0.9,"monthly"),
        ("/pricing",0.8,"monthly"),("/portfolio",0.8,"monthly"),("/over-ons",0.7,"monthly"),("/contact",0.7,"yearly"),("/aanvraag",0.8,"yearly"),
        ("/regio",0.7,"monthly"),("/blog",0.7,"weekly"),("/website-voor-installateurs",0.8,"monthly"),("/seo-den-bosch",0.8,"monthly","2026-10-31")]
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
