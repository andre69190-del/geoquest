# -*- coding: utf-8 -*-
"""
Phase: 288
Date:  2026-05-29
Author: Claude / Andre
Scope: Polnische Inhalte fuer 5 Rubriken (E-Mobilitaet, Archaeologie, Astronomie, Geologie, Sport)

Description:
  Ziel: Diese 5 Rubriken sollen gut auf Polnisch spielbar sein.
  Uebersetzt werden (Auswahl des Nutzers): Frage-Prompts (196), Einheiten (54)
  und die Match-Antwort-Buttons / fixedOpts (deutsche Begriffe + Laendernamen).
  Eigennamen/Modell-/Ortsnamen bleiben unveraendert (korrekt).

  Mechanismus (ERWEITERBAR fuer weitere Sprachen):
    const _CONTENT_I18N = { pl: { "<de>":"<pl>", ... } };   // spaeter: en:{...}, fr:{...}
    function _tc(s){ ...nimmt Uebersetzung fuer aktuelle Sprache, sonst Original... }

  Verdrahtung in den 3 Universal-Engines (_mkPinQ/_mkHL/_mkMatchQ), die alle
  5 Rubriken bedienen:
    - prompt:  _tc(prompt)
    - unit:    _tc(unit)   (im HL-meta)
    - match:   opts + ans  werden konsistent durch _tc gemappt
  Eigennamen/Codes (CCS, Tesla, NMC, ISO 15118, % ...) sind NICHT im Map ->
  _tc gibt sie unveraendert zurueck. Andere Rubriken (tech/gastro/tiere)
  nutzen dieselben Engines, ihre Strings sind aber nicht im Map -> unveraendert.

  Antwort-Logik bleibt korrekt: opts UND ans werden gleich gemappt, der Vergleich
  a===S.q.ans erfolgt damit konsistent in der Anzeigesprache.

Dependencies: patch_287_i18n_de_en_pl.py
"""

import os, json

GEN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'gen.py')
with open(GEN, encoding='utf-8') as f:
    content = f.read()

# =====================================================================
# Polnische Uebersetzungen  (de -> pl)
# =====================================================================
PROMPTS = {
"Auf welchem Kontinent wurde diese Sportart erfunden / ist am populaersten?": "Na którym kontynencie wynaleziono ten sport / jest najpopularniejszy?",
"Auf welcher Fahrzeugplattform basiert dieses EV-Modell?": "Na jakiej platformie pojazdu bazuje ten model EV?",
"Auf welcher Technologie basiert dieser Elektromotortyp?": "Na jakiej technologii opiera się ten typ silnika elektrycznego?",
"Auf welcher tektonischen Hauptplatte liegt dieser Kontinent / diese Region?": "Na której głównej płycie tektonicznej leży ten kontynent / region?",
"Auf welcher tektonischen Platte liegt dieses Land hauptsaechlich?": "Na której płycie tektonicznej leży głównie ten kraj?",
"Aus welchem Land kommt diese Sportlegende?": "Z jakiego kraju pochodzi ta legenda sportu?",
"Aus welchem Land stammt dieses EV-Startup?": "Z jakiego kraju pochodzi ten startup EV?",
"Aus welcher Zeit stammt dieses Werkzeug?": "Z jakiego okresu pochodzi to narzędzie?",
"Bei welchem Fahrzeug dauert das Laden von 10% auf 80% kürzer?": "W którym pojeździe ładowanie z 10% do 80% trwa krócej?",
"Diese Stadt hat eine der höchsten EV-Dichten weltweit — wo liegt sie?": "To miasto ma jedną z najwyższych gęstości EV na świecie — gdzie leży?",
"Durch welchen Prozess entstand dieses Naturwunder hauptsächlich?": "W wyniku jakiego procesu powstał głównie ten cud natury?",
"Durch welchen tektonischen Prozess entstand dieses Gebirge?": "W wyniku jakiego procesu tektonicznego powstało to pasmo górskie?",
"Für welche Anwendung ist diese 3D-Methode am besten?": "Do jakiego zastosowania ta metoda 3D nadaje się najlepiej?",
"Für welche Entdeckung oder welches Gesetz ist dieser Astronom bekannt?": "Z jakiego odkrycia lub prawa znany jest ten astronom?",
"In welche Kategorie fällt der Anteil erneuerbarer Energien in diesem Land?": "Do jakiej kategorii należy udział energii odnawialnej w tym kraju?",
"In welchem Erdzeitalter lebte dieses Wesen?": "W której erze geologicznej żyła ta istota?",
"In welchem Grab wurden mehr Beigaben gefunden?": "W którym grobie znaleziono więcej darów grobowych?",
"In welchem Jahr ereignete sich dieses historische Erdbeben?": "W którym roku doszło do tego historycznego trzęsienia ziemi?",
"In welchem Land fand diese Fussball-WM statt?": "W jakim kraju odbyły się te mistrzostwa świata w piłce nożnej?",
"In welchem Land gilt diese EV-Fördermaßnahme?": "W jakim kraju obowiązuje ten program dopłat do EV?",
"In welchem Land gilt dieses EV-Privileg?": "W jakim kraju obowiązuje ten przywilej dla EV?",
"In welchem Land liegt dieser Vulkan?": "W jakim kraju leży ten wulkan?",
"In welchem Land liegt dieses Höhlensystem?": "W jakim kraju leży ten system jaskiń?",
"In welchem Land oder Region wurde diese Sportart entwickelt?": "W jakim kraju lub regionie rozwinął się ten sport?",
"In welchem modernen Land liegt diese Indus-Tal-Stätte?": "W jakim współczesnym kraju leży to stanowisko cywilizacji doliny Indusu?",
"In welcher Stadt fanden diese Olympischen Sommerspiele statt?": "W jakim mieście odbyły się te letnie igrzyska olimpijskie?",
"In welcher Stadt findet dieser Formel-E-ePrix statt?": "W jakim mieście odbywa się ten ePrix Formuły E?",
"In welcher Stadt wird diese berühmte Sammlung aufbewahrt?": "W jakim mieście przechowywana jest ta słynna kolekcja?",
"Ist diese Sportart bei den Olympischen Spielen vertreten?": "Czy ten sport jest reprezentowany na igrzyskach olimpijskich?",
"Mit welchem Partner/Protokoll kann dieses Ladenetzwerk Roaming?": "Z jakim partnerem/protokołem ta sieć ładowania umożliwia roaming?",
"Von welchem Hersteller stammt dieses EV-Konzeptfahrzeug?": "Od jakiego producenta pochodzi ten koncepcyjny pojazd EV?",
"Was bedeutet diese EV-Warnanzeige im Armaturenbrett?": "Co oznacza ten wskaźnik ostrzegawczy EV na desce rozdzielczej?",
"Was behauptete diese berühmte Fälschung zu sein?": "Za co podawało się to słynne fałszerstwo?",
"Was erkennt diese archäologische Surveymethode?": "Co wykrywa ta archeologiczna metoda badawcza?",
"Was schreibt die AVAS-Vorschrift für dieses Szenario vor?": "Co nakazuje przepis AVAS w tym scenariuszu?",
"Was verrät diese Isotopenanalyse?": "Co zdradza ta analiza izotopowa?",
"Welche Antriebsart nutzt diese Rakete oder Raumsonde?": "Jakiego rodzaju napęd wykorzystuje ta rakieta lub sonda kosmiczna?",
"Welche Bedrohung gefährdet diese UNESCO-Welterbestätte?": "Jakie zagrożenie dotyka to miejsce światowego dziedzictwa UNESCO?",
"Welche Beschreibung passt zu diesem astronomischen Objekt?": "Który opis pasuje do tego obiektu astronomicznego?",
"Welche Bohrung / Mine reicht tiefer?": "Który odwiert / kopalnia sięga głębiej?",
"Welche Datierungsmethode ist hier am besten geeignet?": "Która metoda datowania jest tu najlepsza?",
"Welche Eigenschaft beschreibt diesen Planeten am besten?": "Która cecha najlepiej opisuje tę planetę?",
"Welche Entdeckung ist jünger?": "Które odkrycie jest młodsze?",
"Welche Epoche deckt dieses Digitalprojekt ab?": "Jaką epokę obejmuje ten projekt cyfrowy?",
"Welche Funktion übernimmt diese TMS-Komponente?": "Jaką funkcję pełni ten komponent TMS?",
"Welche Information liefert dieser Pflanzenfund in der Archäologie?": "Jakiej informacji dostarcza to znalezisko roślinne w archeologii?",
"Welche Platte driftet schneller?": "Która płyta przesuwa się szybciej?",
"Welche Rakete transportiert mehr Nutzlast in die Erdumlaufbahn (LEO)?": "Która rakieta wynosi większy ładunek na orbitę okołoziemską (LEO)?",
"Welche Raumsonde / welches Teleskop war länger im Betrieb?": "Która sonda / który teleskop działał dłużej?",
"Welche Ruinenanlage ist größer?": "Który kompleks ruin jest większy?",
"Welche Schlucht ist tiefer?": "Który wąwóz jest głębszy?",
"Welche V2X-Technologie beschreibt diese Netzinteraktion?": "Która technologia V2X opisuje tę interakcję z siecią?",
"Welche Verhaltensregel beschreibt diese Ladesituation?": "Którą zasadę zachowania opisuje ta sytuacja ładowania?",
"Welche charakteristische Farbe hat dieses Mineral?": "Jaki charakterystyczny kolor ma ten minerał?",
"Welchem Galaxientyp gehört diese Galaxie an?": "Do jakiego typu należy ta galaktyka?",
"Welchem Kristallsystem gehört dieses Mineral an?": "Do jakiego układu krystalograficznego należy ten minerał?",
"Welchem Ladestandard entspricht dieser Steckertyp?": "Jakiemu standardowi ładowania odpowiada ten typ wtyczki?",
"Welchem SAE-Autonomiegrad entspricht diese Funktion?": "Jakiemu poziomowi autonomii SAE odpowiada ta funkcja?",
"Welchem Weltverband gehoert diese Sportart an?": "Do jakiej światowej federacji należy ten sport?",
"Welchen Vorteil bietet dieses EV-spezifische Reifenmerkmal?": "Jaką korzyść daje ta cecha opony przeznaczonej dla EV?",
"Welcher Berg ist hoeher?": "Która góra jest wyższa?",
"Welcher Epoche gehört dieses Artefakt an?": "Do jakiej epoki należy ten artefakt?",
"Welcher Exoplanet ist weiter von der Erde entfernt?": "Która egzoplaneta jest dalej od Ziemi?",
"Welcher Faktor reduziert die EV-Reichweite auf diese Weise?": "Który czynnik zmniejsza zasięg EV w ten sposób?",
"Welcher Fund liegt tiefer?": "Które znalezisko leży głębiej?",
"Welcher Himmelskörper hat die stärkere Oberflächengravitation?": "Które ciało niebieskie ma silniejszą grawitację powierzchniową?",
"Welcher Kultur entstammt diese Schrift?": "Z jakiej kultury pochodzi to pismo?",
"Welcher Kultur gehört diese astronomische Stätte oder Beobachtung?": "Do jakiej kultury należy to stanowisko lub obserwacja astronomiczna?",
"Welcher Kultur gehört dieser Bestattungsritus an?": "Do jakiej kultury należy ten obrzęd pogrzebowy?",
"Welcher Kultur gehört dieser Keramikstil an?": "Do jakiej kultury należy ten styl ceramiki?",
"Welcher Ladekorridore / EV-Roadtrip-Route führt durch diesen Ort?": "Który korytarz ładowania / trasa road tripu EV prowadzi przez to miejsce?",
"Welcher Marathon hat eine laengere Geschichte?": "Który maraton ma dłuższą historię?",
"Welcher Megalith ist schwerer?": "Który megalit jest cięższy?",
"Welcher Planet hat den groesseren Durchmesser?": "Która planeta ma większą średnicę?",
"Welcher Planet hat mehr bekannte Monde?": "Która planeta ma więcej znanych księżyców?",
"Welcher Planet ist durchschnittlich heißer (Oberflächentemperatur)?": "Która planeta jest średnio cieplejsza (temperatura powierzchni)?",
"Welcher Prozess hat diese Landschaftsform erschaffen?": "Jaki proces stworzył tę formę krajobrazu?",
"Welcher Transfer war teurer?": "Który transfer był droższy?",
"Welcher Tsunami war höher?": "Które tsunami było wyższe?",
"Welcher Vorteil ist typisch für diese Batteriezellchemie?": "Jaka zaleta jest typowa dla tej chemii ogniw akumulatora?",
"Welcher Vulkan hat den hoeheren Gipfel?": "Który wulkan ma wyższy szczyt?",
"Welcher Vulkanausbruch war explosiver (VEI)?": "Która erupcja wulkanu była bardziej eksplozywna (VEI)?",
"Welcher Zivilisation gehört diese Münze?": "Do jakiej cywilizacji należy ta moneta?",
"Welcher Zivilisation gehörte diese Währung?": "Do jakiej cywilizacji należała ta waluta?",
"Welcher antiken Kultur entstammt diese medizinische Praxis?": "Z jakiej starożytnej kultury pochodzi ta praktyka medyczna?",
"Welcher griechischen Ordnung gehört dieser Tempel an?": "Do jakiego porządku greckiego należy ta świątynia?",
"Welches 3D-Scan-Projekt hat mehr Datenmenge?": "Który projekt skanowania 3D ma więcej danych?",
"Welches Artefakt hat einen höheren Schätzwert?": "Który artefakt ma wyższą szacowaną wartość?",
"Welches Artefakt ist älter?": "Który artefakt jest starszy?",
"Welches Eisvorkommen hat größeres Volumen?": "Które złoże lodu ma większą objętość?",
"Welches Elektroauto beschleunigt schneller von 0 auf 100 km/h?": "Który samochód elektryczny przyspiesza szybciej od 0 do 100 km/h?",
"Welches Elektroauto hat eine größere Batteriekapazität?": "Który samochód elektryczny ma większą pojemność akumulatora?",
"Welches Elektroauto hat eine größere WLTP-Reichweite?": "Który samochód elektryczny ma większy zasięg WLTP?",
"Welches Elektroauto hat mehr Systemdrehmoment?": "Który samochód elektryczny ma większy moment obrotowy układu?",
"Welches Elektroauto ist schwerer?": "Który samochód elektryczny jest cięższy?",
"Welches Elektroauto ist teurer (Basispreis)?": "Który samochód elektryczny jest droższy (cena podstawowa)?",
"Welches Elektroauto lädt mit höherer Maximalleistung?": "Który samochód elektryczny ładuje się z wyższą mocą maksymalną?",
"Welches Erdbeben hatte die groessere Magnitude?": "Które trzęsienie ziemi miało większą magnitudę?",
"Welches Fahrzeug arbeitet mit einer höheren Systemspannung?": "Który pojazd pracuje przy wyższym napięciu układu?",
"Welches Fahrzeug hat einen niedrigeren Luftwiderstandsbeiwert (cw)?": "Który pojazd ma niższy współczynnik oporu powietrza (cx)?",
"Welches Fahrzeug hat mehr Batteriezellen?": "Który pojazd ma więcej ogniw akumulatora?",
"Welches Fahrzeug hat mehr Ladeanschlüsse (AC + DC kombiniert)?": "Który pojazd ma więcej złączy ładowania (AC + DC łącznie)?",
"Welches Fahrzeug zeigt dieses typische Ladeverhalten?": "Który pojazd wykazuje to typowe zachowanie podczas ładowania?",
"Welches Gestein / welche Gesteinsformation ist älter?": "Która skała / formacja skalna jest starsza?",
"Welches Höhlensystem ist länger?": "Który system jaskiń jest dłuższy?",
"Welches Land fordert dieses Artefakt zurück?": "Który kraj domaga się zwrotu tego artefaktu?",
"Welches Land hat diesen Sport als inoffiziellen Nationalsport?": "Który kraj ma ten sport jako nieoficjalny sport narodowy?",
"Welches Material hat einen höheren Schmelzpunkt?": "Który materiał ma wyższą temperaturę topnienia?",
"Welches Mineral ist härter (Mohs-Skala)?": "Który minerał jest twardszy (skala Mohsa)?",
"Welches Objekt ist laut C14-Datierung älter?": "Który obiekt jest starszy według datowania C14?",
"Welches Objekt ist weiter von der Sonne entfernt?": "Który obiekt jest dalej od Słońca?",
"Welches Objekt wurde früher entdeckt?": "Który obiekt odkryto wcześniej?",
"Welches Protokoll/welcher Standard ermöglicht diese EV-Smart-Home-Funktion?": "Który protokół/standard umożliwia tę funkcję EV smart home?",
"Welches Stadion fasst mehr Zuschauer?": "Który stadion mieści więcej widzów?",
"Welches Stadion wurde frueher erbaut?": "Który stadion zbudowano wcześniej?",
"Welches Ziel hat diese Raumsonde angesteuert?": "Do jakiego celu zmierzała ta sonda kosmiczna?",
"Welches antike Bauwerk ist höher?": "Która starożytna budowla jest wyższa?",
"Welches antike Straßennetz ist länger?": "Która starożytna sieć dróg jest dłuższa?",
"Welches stratigraphische Grundprinzip wird hier beschrieben?": "Która podstawowa zasada stratygrafii jest tu opisana?",
"Wer entdeckte oder ergrub diese Fundstätte?": "Kto odkrył lub przebadał to stanowisko?",
"Wer erzielte mehr Tore in einer Saison?": "Kto strzelił więcej goli w jednym sezonie?",
"Wer gewann mehr Olympia-Goldmedaillen?": "Kto zdobył więcej złotych medali olimpijskich?",
"Wer haelt diesen Weltrekord?": "Kto jest posiadaczem tego rekordu świata?",
"Wer hat einen hoeheren Marktwert?": "Kto ma wyższą wartość rynkową?",
"Wer hob mehr? (Reissen + Stossen zusammen)": "Kto podniósł więcej? (rwanie + podrzut łącznie)",
"Wer sprang hoeher?": "Kto skoczył wyżej?",
"Wer verdient mehr pro Jahr?": "Kto zarabia więcej rocznie?",
"Wessen Bau hat länger gedauert?": "Czyja budowa trwała dłużej?",
"Wie historisch korrekt ist diese Darstellung?": "Na ile historycznie poprawne jest to przedstawienie?",
"Wie viele Spieler umfasst eine Mannschaft bei diesem Feldsport?": "Ilu zawodników liczy drużyna w tym sporcie zespołowym?",
"Wie wurde diese archäologische Entdeckung gemacht?": "W jaki sposób dokonano tego odkrycia archeologicznego?",
"Wo befinden sich diese Steilküsten / Klippen?": "Gdzie znajdują się te klify / strome wybrzeża?",
"Wo befinden sich diese prähistorischen Höhlenmalereien?": "Gdzie znajdują się te prehistoryczne malowidła jaskiniowe?",
"Wo befinden sich diese prähistorischen Pfahlbauten?": "Gdzie znajdują się te prehistoryczne budowle palowe?",
"Wo befindet sich diese EV-Batterie-Gigafactory?": "Gdzie znajduje się ta gigafabryka akumulatorów EV?",
"Wo befindet sich diese EV-Batterie-Recyclinganlage?": "Gdzie znajduje się ten zakład recyklingu akumulatorów EV?",
"Wo befindet sich dieser bedeutende Ladepark?": "Gdzie znajduje się ten ważny park ładowania?",
"Wo befindet sich dieser bedeutende Solarpark?": "Gdzie znajduje się ta ważna farma słoneczna?",
"Wo befindet sich dieses Batterie-Forschungsinstitut?": "Gdzie znajduje się ten instytut badań nad akumulatorami?",
"Wo befindet sich dieses Teleskop oder Observatorium?": "Gdzie znajduje się ten teleskop lub obserwatorium?",
"Wo befindet sich dieses bedeutende Lithiumvorkommen oder -bergwerk?": "Gdzie znajduje się to ważne złoże lub kopalnia litu?",
"Wo fand dieser Meilenstein der frühen Elektromobilität statt?": "Gdzie miał miejsce ten kamień milowy wczesnej elektromobilności?",
"Wo fand dieser historische Meilenstein der Elektromobilität statt?": "Gdzie miał miejsce ten historyczny kamień milowy elektromobilności?",
"Wo hat diese digitale Archäologie-Institution ihren Sitz?": "Gdzie ma siedzibę ta instytucja archeologii cyfrowej?",
"Wo hat dieses E-Fahrzeug-Startup seinen Hauptsitz?": "Gdzie ma siedzibę główną ten startup pojazdów elektrycznych?",
"Wo liegt diese Geothermalquelle?": "Gdzie leży to źródło geotermalne?",
"Wo liegt diese Grand-Slam-Tennis-Arena?": "Gdzie leży ta arena tenisowa Wielkiego Szlema?",
"Wo liegt diese Maya- oder Inka-Ruine?": "Gdzie leży ta ruina Majów lub Inków?",
"Wo liegt diese Megalithanlage?": "Gdzie leży ten kompleks megalityczny?",
"Wo liegt diese Mine oder dieses Bohrprojekt?": "Gdzie leży ta kopalnia lub ten projekt wiertniczy?",
"Wo liegt diese Motorsport-Rennstrecke?": "Gdzie leży ten tor wyścigowy?",
"Wo liegt diese Schlucht / dieser Canyon?": "Gdzie leży ten wąwóz / kanion?",
"Wo liegt diese Wikinger-Siedlung heute?": "Gdzie leży dziś ta osada wikingów?",
"Wo liegt diese Wüste oder Wüstenlandschaft?": "Gdzie leży ta pustynia lub krajobraz pustynny?",
"Wo liegt diese bedeutende Fossilien-Fundstätte?": "Gdzie leży to ważne stanowisko skamieniałości?",
"Wo liegt diese berühmte Felsformation?": "Gdzie leży ta słynna formacja skalna?",
"Wo liegt diese berühmte Nekropole?": "Gdzie leży ta słynna nekropolia?",
"Wo liegt diese verlassene Wüstenstadt?": "Gdzie leży to opuszczone miasto na pustyni?",
"Wo liegt diese versunkene Stadt?": "Gdzie leży to zatopione miasto?",
"Wo liegt dieser Geysir?": "Gdzie leży ten gejzer?",
"Wo liegt dieser Gletscher?": "Gdzie leży ten lodowiec?",
"Wo liegt dieser Marathon-Start/-Ziel?": "Gdzie jest start/meta tego maratonu?",
"Wo liegt dieser Meteoritenkrater?": "Gdzie leży ten krater meteorytowy?",
"Wo liegt dieser Nationalpark mit besonderer Geologie?": "Gdzie leży ten park narodowy o szczególnej geologii?",
"Wo liegt dieser Ozeangraben / tiefste Punkt?": "Gdzie leży ten rów oceaniczny / najgłębszy punkt?",
"Wo liegt dieser Vulkan?": "Gdzie leży ten wulkan?",
"Wo liegt dieser Wintersport-Ort?": "Gdzie leży ta miejscowość sportów zimowych?",
"Wo liegt dieser beruehmt Golfplatz?": "Gdzie leży to słynne pole golfowe?",
"Wo liegt dieser tektonische Graben / diese Spalte?": "Gdzie leży ten rów tektoniczny / ta szczelina?",
"Wo liegt dieser weltberuehmt Surfspot?": "Gdzie leży to słynne na świecie miejsce do surfingu?",
"Wo liegt dieses Dark-Sky-Reservat?": "Gdzie leży ten rezerwat ciemnego nieba?",
"Wo liegt dieses Fussballstadion?": "Gdzie leży ten stadion piłkarski?",
"Wo liegt dieses Höhlensystem?": "Gdzie leży ten system jaskiń?",
"Wo liegt dieses Observatorium?": "Gdzie leży to obserwatorium?",
"Wo liegt dieses Olympiastadion?": "Gdzie leży ten stadion olimpijski?",
"Wo liegt dieses Raumfahrtkontrollzentrum?": "Gdzie leży to centrum kontroli lotów kosmicznych?",
"Wo liegt dieses Raumfahrtzentrum / diese Startrampe?": "Gdzie leży to centrum kosmiczne / ta wyrzutnia?",
"Wo liegt dieses beruehmt Klettergebiet?": "Gdzie leży ten słynny region wspinaczkowy?",
"Wo liegt dieses beruehmt Skigebiet?": "Gdzie leży ten słynny ośrodek narciarski?",
"Wo liegt dieses berühmte Schiffswrack?": "Gdzie leży ten słynny wrak statku?",
"Wo liegt dieses römische Grenzkastell oder dieser Limesabschnitt?": "Gdzie leży ten rzymski fort graniczny lub odcinek limesu?",
"Wo sitzt der Ladeanschluss bei diesem Fahrzeug?": "Gdzie znajduje się gniazdo ładowania w tym pojeździe?",
"Wo werden autonome Fahrzeuge getestet?": "Gdzie testowane są pojazdy autonomiczne?",
"Wo wird dieses Artefakt aufbewahrt?": "Gdzie przechowywany jest ten artefakt?",
"Wo wurde dieser Sensationsfund gemacht?": "Gdzie dokonano tego sensacyjnego znaleziska?",
"Wofür steht dieses E-Mobilitäts-Akronym?": "Co oznacza ten akronim z dziedziny elektromobilności?",
"Wofür wird dieses Gestein / Mineral hauptsächlich genutzt?": "Do czego głównie używa się tej skały / tego minerału?",
"Wozu wird dieses Mineral oder Gestein hauptsaechlich verwendet?": "Do czego głównie wykorzystuje się ten minerał lub skałę?",
"Zu welchem Gebirge gehört dieser Berg?": "Do jakiego pasma górskiego należy ta góra?",
"Zu welchem Sternenhimmel gehört dieses Sternbild hauptsächlich?": "Do jakiego nieba należy głównie ten gwiazdozbiór?",
"Zu welchem Typ gehört dieser Himmelskörper?": "Do jakiego typu należy to ciało niebieskie?",
"Zu welcher Gesteinsklasse gehoert dieses Gestein?": "Do jakiej klasy skał należy ta skała?",
"Zu welcher Kultur gehört diese Gottheit?": "Do jakiej kultury należy to bóstwo?",
"Zu welcher Raumfahrtagentur gehoert diese Mission?": "Do jakiej agencji kosmicznej należy ta misja?",
"Zu welcher Sportdisziplin gehoert diese Uebung?": "Do jakiej dyscypliny sportu należy to ćwiczenie?",
"Über welche Handelsroute kam dieses Gut?": "Którym szlakiem handlowym przybył ten towar?",
}

UNITS = {
"Anschlüsse gesamt": "złącza łącznie",
"Anzahl Objekte (ca.)": "liczba obiektów (ok.)",
"Baujahr": "rok budowy",
"GB Scandaten": "GB danych skanu",
"Goldmedaillen": "złote medale",
"Gruendungsjahr": "rok założenia",
"Hektar": "hektary",
"Jahr": "rok",
"Jahr der Entdeckung": "rok odkrycia",
"Jahre BP (vor heute)": "lat BP (przed teraźniejszością)",
"Jahre Bauzeit (geschätzt)": "lata budowy (szacowane)",
"Jahre v. Chr.": "lat p.n.e.",
"Lichtjahre": "lata świetlne",
"Meter Höhe": "metry wysokości",
"Meter Tiefe": "metry głębokości",
"Millionen Jahre": "miliony lat",
"Minuten (10–80%)": "minuty (10–80%)",
"Mio Euro": "mln euro",
"Mio Euro/Jahr": "mln euro/rok",
"Mio. EUR Schätzwert": "mln EUR wartości szacunkowej",
"Mio. km": "mln km",
"Mohs-Härtegrad": "twardość w skali Mohsa",
"Monde": "księżyce",
"Nm": "Nm",
"Richter-Skala": "skala Richtera",
"Sekunden (0-100 km/h)": "sekundy (0-100 km/h)",
"Tage (Betrieb bis 2026)": "dni (eksploatacja do 2026)",
"Tonnen": "tony",
"Tore": "gole",
"Tsd. EUR": "tys. EUR",
"Tsd. Plaetze": "tys. miejsc",
"Volt": "wolty",
"Vulkanexplosivitätsindex (VEI)": "indeks eksplozywności wulkanu (VEI)",
"Zellen (gesamt)": "ogniwa (łącznie)",
"cm": "cm",
"cw × 1000": "cx × 1000",
"kW (DC max.)": "kW (DC maks.)",
"kWh (nutzbar)": "kWh (użyteczne)",
"kg": "kg",
"kg (Leergewicht)": "kg (masa własna)",
"km": "km",
"km (WLTP)": "km (WLTP)",
"km (kartierte Länge)": "km (zmierzona długość)",
"km Gesamtlänge": "km długości całkowitej",
"km³ (Eisvolumen)": "km³ (objętość lodu)",
"m": "m",
"m (Tiefe unter Erdoberfläche)": "m (głębokość pod powierzchnią)",
"m (Tiefe)": "m (głębokość)",
"m (maximale Wellenhöhe)": "m (maksymalna wysokość fali)",
"m/s²": "m/s²",
"mm/Jahr (Driftgeschwindigkeit)": "mm/rok (prędkość dryfu)",
"t (Nutzlast LEO)": "t (ładunek LEO)",
"°C (Durchschnitt)": "°C (średnia)",
"°C (Schmelzpunkt)": "°C (temp. topnienia)",
}

# fixedOpts: nur uebersetzbare deutsche Begriffe + Laendernamen.
# Eigennamen/Codes (CCS, CHAdeMO, Tesla, NMC, NCA, LFP, V2G/H/L/V, OCPP,
# ISO 15118, EEBus, RTI, C14, LiDAR, %, Maya ...) NICHT enthalten -> _tc gibt
# sie unveraendert zurueck.
FIXEDOPTS = {
"Alter": "Wiek",
"Antike": "Starożytność",
"Atlantikhandel": "Handel atlantycki",
"Autobahn": "Autostrada",
"Bauarbeiten": "Prace budowlane",
"Bernsteinstraße": "Szlak bursztynowy",
"Bodenradar": "Georadar",
"Bronzezeit": "Epoka brązu",
"Cross-Cutting": "Relacje przecięcia",
"Dendrochronologie": "Dendrochronologia",
"Dorisch": "Dorycki",
"Eisenzeit": "Epoka żelaza",
"Ernährung": "Odżywianie",
"Geräusch": "Hałas",
"Gewicht": "Masa",
"Gleichstrom": "Prąd stały",
"Griechenland": "Grecja",
"Grip": "Przyczepność",
"Handel": "Handel",
"Heizen": "Ogrzewanie",
"Herkunft": "Pochodzenie",
"Historisch falsch": "Historycznie błędne",
"Horizontalität": "Pierwotna poziomość",
"Indien": "Indie",
"Induktion": "Indukcja",
"Ionisch": "Joński",
"Isolieren": "Izolowanie",
"Kabel wegräumen": "Schować kabel",
"Klima": "Klimat",
"Klimawandel": "Zmiana klimatu",
"Komplett erfunden": "Całkowicie zmyślone",
"Korinthisch": "Koryncki",
"Krieg": "Wojna",
"Kälte": "Zimno",
"Kühlen": "Chłodzenie",
"Laden abbrechen": "Przerwać ładowanie",
"Landwirt": "Rolnik",
"Landwirtschaft": "Rolnictwo",
"Laserscanning": "Skanowanie laserowe",
"Level 1": "Poziom 1",
"Level 2": "Poziom 2",
"Level 3": "Poziom 3",
"Level 4/5": "Poziom 4/5",
"Magnetometrie": "Magnetometria",
"Mesopotamien": "Mezopotamia",
"Metalldetektoren": "Wykrywacze metali",
"Mittelalter": "Średniowiecze",
"Neolithikum": "Neolit",
"Neuzeit": "Czasy nowożytne",
"Nicht blockieren": "Nie blokować",
"Original Continuity": "Pierwotna ciągłość",
"Paläolithikum": "Paleolit",
"Permanentmagnet": "Magnes trwały",
"Photogrammetrie": "Fotogrametria",
"Priorität": "Priorytet",
"Regeln": "Zasady",
"Reichweite": "Zasięg",
"Religion": "Religia",
"Reluktanz": "Reluktancja",
"Seidenstraße": "Jedwabny szlak",
"Stark vereinfacht": "Mocno uproszczone",
"Steinzeit": "Epoka kamienia",
"Stonehenge-Kultur": "Kultura Stonehenge",
"Stratigraphie": "Stratygrafia",
"Superposition": "Superpozycja",
"Taucher": "Nurek",
"Thermolumineszenz": "Termoluminescencja",
"Toskanisch": "Toskański",
"Tourismus": "Turystyka",
"Urbanisierung": "Urbanizacja",
"Urgeschichte": "Prehistoria",
"Wanderer": "Wędrowiec",
"Weihrauchstraße": "Szlak kadzidlany",
"Weitgehend korrekt": "W dużej mierze poprawne",
"Ägypten": "Egipt",
"Afghanistan": "Afganistan",
"China": "Chiny",
"Iran": "Iran",
"Pakistan": "Pakistan",
}

PL = {}
PL.update(PROMPTS); PL.update(UNITS); PL.update(FIXEDOPTS)
print(f'Polnische Eintraege: {len(PROMPTS)} Prompts + {len(UNITS)} Einheiten + {len(FIXEDOPTS)} Buttons = {len(PL)}')

# =====================================================================
# 1) _CONTENT_I18N + _tc()  einfuegen (nach dem T()-Alias)
# =====================================================================
i18n_js = '{pl:' + json.dumps(PL, ensure_ascii=False) + '}'
helper = (
'\n/* P288: erweiterbare Inhalts-Uebersetzung (Prompts/Einheiten/Match-Buttons).\n'
'   Weitere Sprachen: einfach _CONTENT_I18N um en:{...}, fr:{...} erweitern. */\n'
'const _CONTENT_I18N=' + i18n_js + ';\n'
'function _tc(s){if(!s)return s;var _l=(typeof S!=="undefined"&&S.language)||localStorage.getItem("gq_lang")||"de";if(_l==="de")return s;var _m=_CONTENT_I18N[_l];return(_m&&_m[s])||s;}\n'
)

anchor = '/* Backwards-compat alias */\nfunction T(k){return t(k);}'
assert content.count(anchor) == 1, ('T-alias anchor', content.count(anchor))
content = content.replace(anchor, anchor + helper, 1)
print('[OK]   _CONTENT_I18N + _tc() eingefuegt')

# =====================================================================
# 2) Engines verdrahten
# =====================================================================
def patch(old, new, label):
    global content
    c = content.count(old)
    if c != 1:
        print(f'[FAIL] {label}: count={c}')
        raise SystemExit(1)
    content = content.replace(old, new, 1)
    print(f'[OK]   {label}')

# --- _mkPinQ: prompt ---
patch('ans:item.n,prompt:d.prompt,cat:cat,',
      'ans:item.n,prompt:_tc(d.prompt),cat:cat,',
      '_mkPinQ: prompt -> _tc')

# --- _mkHL: unit (meta) + prompt ---
patch('var unit=d.unit||"";\n      var meta=a.name+": "+a.val+(unit?" "+unit:"")+" \\u00b7 "+b.name+": "+b.val+(unit?" "+unit:"");',
      'var unit=_tc(d.unit||"");\n      var meta=a.name+": "+a.val+(unit?" "+unit:"")+" \\u00b7 "+b.name+": "+b.val+(unit?" "+unit:"");',
      '_mkHL: unit -> _tc')
patch('return{type:"beta_hl",prompt:d.prompt||"Welches ist mehr?",subj:"",\n        opts:[a.name,b.name],ans:higher.name,meta:meta,lid:_lid,cc:"de"};',
      'return{type:"beta_hl",prompt:_tc(d.prompt||"Welches ist mehr?"),subj:"",\n        opts:[a.name,b.name],ans:higher.name,meta:meta,lid:_lid,cc:"de"};',
      '_mkHL: prompt -> _tc')

# --- _mkMatchQ: prompt + opts/ans konsistent uebersetzen ---
patch('return{type:"uk_match",subj:correct.n,ans:correct.c,opts:opts,\n      prompt:d.prompt||"Ordne richtig zu:",lid:"mkm_"+cat+"_"+idx};',
      'return{type:"uk_match",subj:correct.n,ans:_tc(correct.c),opts:opts.map(_tc),\n      prompt:_tc(d.prompt||"Ordne richtig zu:"),lid:"mkm_"+cat+"_"+idx};',
      '_mkMatchQ: prompt + opts/ans -> _tc')

# =====================================================================
_tmp = GEN + '.tmp'
with open(_tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(_tmp, GEN)
print('\nPatch complete.')
