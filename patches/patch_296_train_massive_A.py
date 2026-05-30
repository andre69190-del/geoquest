#!/usr/bin/env python3
"""
patch_296_train_massive_A.py — Phase 296.2 Trainspotter Mega Sprint
Fügt hinzu:
  sport_hl.json:   zug_speed (80 Items), zug_jahr (80 Items), zug_km (80 Items)
  timeline.json:   zug_hsb (80 Items — HSR + Metro-Meilensteine)
  tiere_ws.json:   15 Zug-Namen Wort-Schmiede-Einträge
  gen.py:          5 neue MODES + GEN dispatch + zuege MODE_CATS erweitert
"""
import json, sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─────────────────────────────────────────────────────────────────────────────
# 1. HL_ZUG_SPEED — Betriebsgeschwindigkeit in km/h (80 Items)
# ─────────────────────────────────────────────────────────────────────────────
HL_ZUG_SPEED = {
    "prompt": "Höhere Betriebsgeschwindigkeit?",
    "unit": "km/h",
    "items": [
        # Maglev / Experimentell
        {"name": "Shanghai Maglev (China)", "val": 430},
        {"name": "JR L0 Maglev (Japan, Testrekord)", "val": 603},
        {"name": "Transrapid TR09 (Deutschland, Test)", "val": 550},
        # China CR-Serie (HSR)
        {"name": "Fuxing CR400BF (China)", "val": 350},
        {"name": "Fuxing CR400AF (China)", "val": 350},
        {"name": "CRH380A (China)", "val": 380},
        {"name": "CRH380B (China)", "val": 380},
        {"name": "CRH3C (China, Velaro CN)", "val": 350},
        {"name": "CRH2C (China)", "val": 350},
        {"name": "CRH5A (China)", "val": 250},
        # Japan Shinkansen
        {"name": "Shinkansen N700S (Japan)", "val": 320},
        {"name": "Shinkansen N700 (Japan)", "val": 300},
        {"name": "Shinkansen E5/H5 (Japan)", "val": 320},
        {"name": "Shinkansen E7/W7 (Japan)", "val": 260},
        {"name": "Shinkansen E2 Series (Japan)", "val": 275},
        {"name": "Shinkansen 700 Series (Japan)", "val": 285},
        {"name": "Shinkansen 500 Series (Japan)", "val": 300},
        {"name": "Shinkansen 200 Series (Japan)", "val": 240},
        {"name": "Shinkansen 0 Series (Japan, 1964)", "val": 210},
        {"name": "Shinkansen E6 Komachi (Japan)", "val": 320},
        # Frankreich TGV
        {"name": "TGV Euroduplex (Frankreich)", "val": 320},
        {"name": "TGV Duplex (Frankreich)", "val": 320},
        {"name": "TGV PSE (Frankreich, original 1981)", "val": 270},
        {"name": "TGV INOUI (Frankreich)", "val": 320},
        {"name": "AGV Italo (Italien)", "val": 300},
        # Spanien AVE
        {"name": "AVE S-103 Velaro E (Spanien)", "val": 310},
        {"name": "AVE S-100 Talgo 350 (Spanien)", "val": 330},
        {"name": "AVE S-102 Talgo 350 (Spanien)", "val": 330},
        {"name": "OUIGO Spanien", "val": 300},
        # Deutschland ICE
        {"name": "ICE 3 (Deutschland)", "val": 300},
        {"name": "ICE 4 (Deutschland)", "val": 250},
        {"name": "ICE 1 (Deutschland)", "val": 280},
        {"name": "ICE 2 (Deutschland)", "val": 280},
        {"name": "ICE T (Deutschland, Neigetechnik)", "val": 230},
        # Südkorea KTX
        {"name": "KTX-II / KTX-Sancheon (Südkorea)", "val": 300},
        {"name": "KTX-I (Südkorea)", "val": 305},
        {"name": "KTX-Eum (Südkorea)", "val": 260},
        {"name": "SRT (Südkorea SR)", "val": 305},
        # Italien Frecciarossa
        {"name": "Frecciarossa 1000 (Italien)", "val": 300},
        {"name": "Frecciarossa ETR 500 (Italien)", "val": 300},
        {"name": "Frecciargento ETR 610 (Italien)", "val": 250},
        {"name": "Frecciabianca (Italien)", "val": 200},
        # International / Europakorridore
        {"name": "Eurostar e320 (UK–Frankreich–Belgien)", "val": 300},
        {"name": "Eurostar e300 (UK–Frankreich)", "val": 300},
        {"name": "Thalys PBKA (Belgien–Frankreich)", "val": 300},
        {"name": "Thalys PBA (Belgien)", "val": 300},
        {"name": "ICE 3M (International, Deutschland)", "val": 300},
        # Österreich / Schweiz
        {"name": "Railjet (Österreich, Velaro A)", "val": 230},
        {"name": "Nightjet (Österreich, Schlafzug)", "val": 160},
        {"name": "IC2000 (Schweiz)", "val": 200},
        {"name": "Giruno RABe 501 (Schweiz)", "val": 250},
        {"name": "Pendolino ETR 470 (Schweiz–Italien)", "val": 200},
        # Skandinavien
        {"name": "X 2000 (Schweden)", "val": 210},
        {"name": "FLIRT (Norwegen, Regio)", "val": 160},
        {"name": "IC3 (Dänemark)", "val": 180},
        {"name": "Caledonian Sleeper (Schottland)", "val": 160},
        # Russland / Osteuropa
        {"name": "Sapsan (Russland, Velaro RUS)", "val": 250},
        {"name": "Lastochka (Russland, Desiro)", "val": 160},
        {"name": "Allegro (Finnland–Russland)", "val": 220},
        {"name": "Pendolino SM3 (Finnland)", "val": 220},
        {"name": "Leo Express (Tschechien–Polen)", "val": 200},
        {"name": "RegioJet (Tschechien–Slovakei)", "val": 160},
        # USA / Nordamerika
        {"name": "Acela (USA, Amtrak)", "val": 240},
        {"name": "Amtrak Cascades Talgo (USA)", "val": 200},
        {"name": "VIA Rail Renaissance (Kanada)", "val": 145},
        # Türkei / Naher Osten
        {"name": "TCDD YHT (Türkei HSR)", "val": 250},
        {"name": "Saudi Arabia Haramain HSR", "val": 300},
        # Taiwan / Südostasien
        {"name": "THSR 700T (Taiwan)", "val": 300},
        {"name": "EMU700 Taiwan Tze-Chiang", "val": 130},
        {"name": "MRT Bangkok (Thailand)", "val": 80},
        # Indien
        {"name": "Vande Bharat Express (Indien)", "val": 180},
        {"name": "Rajdhani Express (Indien)", "val": 130},
        # Marokko
        {"name": "Al Boraq ONCF (Marokko)", "val": 320},
        # UK HS2 / HS1
        {"name": "Eurostar (HS1-Abschnitt, UK)", "val": 300},
        {"name": "LNER Azuma (UK)", "val": 200},
        {"name": "Pendolino Avanti (UK)", "val": 200},
        {"name": "Elizabeth Line (London, Metro)", "val": 100},
        # Weitere
        {"name": "Talgo 350 (Spanien, Renfe)", "val": 330},
        {"name": "Bernina Express (Schweiz, Panorama)", "val": 70},
        {"name": "Trans-Sibirian Express (Russland)", "val": 80},
    ]
}
assert len(HL_ZUG_SPEED["items"]) >= 80, f"zug_speed: only {len(HL_ZUG_SPEED['items'])} items"

# ─────────────────────────────────────────────────────────────────────────────
# 2. HL_ZUG_JAHR — Erstinbetriebnahme / Einführungsjahr (80 Items)
# ─────────────────────────────────────────────────────────────────────────────
HL_ZUG_JAHR = {
    "prompt": "Früher in Betrieb genommen?",
    "unit": "Jahr der Ersöffnung",
    "items": [
        # Pioniere des Eisenbahnzeitalters
        {"name": "Stockton & Darlington Railway (England)", "val": 1825},
        {"name": "Liverpool & Manchester Railway (England)", "val": 1830},
        {"name": "Baltimore & Ohio Railroad (USA)", "val": 1830},
        {"name": "Paris–Saint-Germain (Frankreich)", "val": 1837},
        {"name": "Nürnberg–Fürth (Deutschland)", "val": 1835},
        {"name": "Semmeringbahn (Österreich)", "val": 1854},
        {"name": "Transsibirische Eisenbahn (Russland)", "val": 1905},
        {"name": "Darjeeling Himalayan Railway (Indien)", "val": 1881},
        {"name": "Bergenbahn (Norwegen)", "val": 1909},
        {"name": "Orient Express (Europa)", "val": 1883},
        # Erste Metros weltweit
        {"name": "London Underground (erste U-Bahn der Welt)", "val": 1863},
        {"name": "Chicago L (USA)", "val": 1892},
        {"name": "Glasgow Subway (UK)", "val": 1896},
        {"name": "Budapest Metro (erste kontinentale U-Bahn)", "val": 1896},
        {"name": "Paris Métro (Frankreich)", "val": 1900},
        {"name": "Berlin U-Bahn (Deutschland)", "val": 1902},
        {"name": "New York City Subway (USA)", "val": 1904},
        {"name": "Buenos Aires Metro (erstes Lateinamerika)", "val": 1913},
        {"name": "Madrid Metro (Spanien)", "val": 1919},
        {"name": "Tokio Metro Ginza Line (Japan, erste Asien)", "val": 1927},
        {"name": "Moskauer Metro (UdSSR)", "val": 1935},
        {"name": "Stockholm Tunnelbana (Schweden)", "val": 1950},
        {"name": "Toronto Subway (Kanada)", "val": 1954},
        # Hochgeschwindigkeitsbahn-Geschichte
        {"name": "Shinkansen Tokaido (Japan, erste HSR weltweit)", "val": 1964},
        {"name": "Shinkansen San'yo (Japan)", "val": 1972},
        {"name": "Shinkansen Tohoku (Japan)", "val": 1982},
        {"name": "TGV Paris–Lyon (Frankreich)", "val": 1981},
        {"name": "TGV Atlantique (Frankreich)", "val": 1990},
        {"name": "ICE 1 (Deutschland)", "val": 1991},
        {"name": "AVE Madrid–Sevilla (Spanien)", "val": 1992},
        {"name": "Eurostar (UK–Frankreich)", "val": 1994},
        {"name": "Thalys (Belgien–Frankreich)", "val": 1996},
        {"name": "ICE 3 (Deutschland–Niederlande)", "val": 2000},
        {"name": "KTX-I (Südkorea)", "val": 2004},
        {"name": "TGV Est (Paris–Straßburg)", "val": 2007},
        {"name": "Beijing–Tianjin Intercity (China, erste HSR China)", "val": 2008},
        {"name": "Velaro RUS Sapsan (Russland)", "val": 2009},
        {"name": "AVE Madrid–Barcelona (Spanien)", "val": 2008},
        {"name": "Shinkansen Kyushu (Japan)", "val": 2011},
        {"name": "Frecciarossa 1000 (Italien)", "val": 2015},
        {"name": "Al Boraq (Marokko, erste HSR Afrika)", "val": 2018},
        {"name": "Haramain HSR (Saudi-Arabien)", "val": 2018},
        {"name": "THSR (Taiwan)", "val": 2007},
        # Moderne Metros
        {"name": "Montréal Metro (Kanada)", "val": 1966},
        {"name": "BART San Francisco (USA)", "val": 1972},
        {"name": "Washington Metro (USA)", "val": 1976},
        {"name": "Mexico City Metro (Mexiko)", "val": 1969},
        {"name": "São Paulo Metro (Brasilien)", "val": 1974},
        {"name": "Cairo Metro (Ägypten, erste Afrika)", "val": 1987},
        {"name": "Bangkok BTS Skytrain (Thailand)", "val": 1999},
        {"name": "Delhi Metro (Indien)", "val": 2002},
        {"name": "Dubai Metro (VAE)", "val": 2009},
        {"name": "Shanghai Metro (China)", "val": 1993},
        {"name": "Beijing Subway (China)", "val": 1969},
        {"name": "Hong Kong MTR (China)", "val": 1979},
        {"name": "Singapore MRT", "val": 1987},
        {"name": "Taipei MRT (Taiwan)", "val": 1996},
        {"name": "Kuala Lumpur LRT (Malaysia)", "val": 1996},
        # Fernstrecken modern
        {"name": "Eurostar (HS1-Vollbetrieb, London)", "val": 2007},
        {"name": "ICE 4 (Deutschland)", "val": 2017},
        {"name": "Fuxing CR400 (China)", "val": 2017},
        {"name": "AGV Italo (Italien)", "val": 2012},
        {"name": "Ouigo (Frankreich, Billigzug)", "val": 2013},
        {"name": "Flixbus Train (Deutschland)", "val": 2018},
        {"name": "Acela (USA, erste Generation)", "val": 2000},
        {"name": "Rocky Mountaineer (Kanada)", "val": 1990},
        {"name": "Glacier Express (Schweiz)", "val": 1930},
        {"name": "Bernina Express (Schweiz)", "val": 1910},
        {"name": "Flåmbahn (Norwegen)", "val": 1940},
        {"name": "The Ghan (Australien, neu)", "val": 2004},
        {"name": "Indian Pacific (Australien)", "val": 1970},
        {"name": "California Zephyr (USA, neu)", "val": 1983},
        {"name": "Pendolino SM3 (Finnland)", "val": 1997},
        {"name": "X 2000 (Schweden)", "val": 1990},
        {"name": "TCDD YHT (Türkei)", "val": 2009},
        {"name": "Vande Bharat Express (Indien)", "val": 2019},
        {"name": "Shinkansen E5/H5 (Japan)", "val": 2011},
        {"name": "TGV Euroduplex (Frankreich)", "val": 2012},
        {"name": "KTX-Eum (Südkorea)", "val": 2021},
        {"name": "Nightjet Wien–Amsterdam (neue Generation)", "val": 2020},
    ]
}
assert len(HL_ZUG_JAHR["items"]) >= 80, f"zug_jahr: only {len(HL_ZUG_JAHR['items'])} items"

# ─────────────────────────────────────────────────────────────────────────────
# 3. HL_ZUG_KM — Streckenlänge in km (80 Items)
# ─────────────────────────────────────────────────────────────────────────────
HL_ZUG_KM = {
    "prompt": "Längere Strecke?",
    "unit": "km",
    "items": [
        # Weltrekorde Fernstrecken
        {"name": "Transsibirische Eisenbahn Moskau–Wladiwostok", "val": 9289},
        {"name": "Kanada-Pazifikbahn Montréal–Vancouver", "val": 4654},
        {"name": "The Canadian Toronto–Vancouver", "val": 4466},
        {"name": "Indian Pacific Sydney–Perth", "val": 4352},
        {"name": "California Zephyr Chicago–San Francisco", "val": 3924},
        {"name": "Coast Starlight Los Angeles–Seattle", "val": 3496},
        {"name": "Empire Builder Chicago–Seattle", "val": 3549},
        {"name": "The Ghan Adelaide–Darwin", "val": 2979},
        {"name": "Blue Train Kapstadt–Pretoria", "val": 1600},
        {"name": "Trans-Mongolian Moskau–Peking (via Mongolei)", "val": 7865},
        {"name": "Beijing–Lhasa Qinghai–Tibet Railway", "val": 1956},
        {"name": "Andean Explorer Cusco–Arequipa", "val": 389},
        {"name": "Rovos Rail Kapstadt–Daressalam", "val": 4800},
        # Europa Fernstrecken (HSR)
        {"name": "Madrid–Barcelona AVE", "val": 621},
        {"name": "Paris–Lyon TGV", "val": 427},
        {"name": "Paris–Marseille TGV", "val": 777},
        {"name": "London–Edinburgh East Coast Main Line", "val": 632},
        {"name": "Hamburg–München ICE", "val": 775},
        {"name": "Amsterdam–Wien Nightjet", "val": 1245},
        {"name": "Paris–Berlin (via Brüssel)", "val": 1050},
        {"name": "Zürich–Roma Pendolino", "val": 839},
        {"name": "Wien–Salzburg Railjet", "val": 295},
        {"name": "Stockholm–Göteborg SJ", "val": 455},
        {"name": "Helsinki–Tampere Pendolino", "val": 187},
        {"name": "Oslo–Bergen Bergenbahn", "val": 371},
        {"name": "Kopenhagen–Aarhus IC3", "val": 315},
        {"name": "Lisboa–Porto Alfa Pendular", "val": 336},
        {"name": "Brüssel–Amsterdam Thalys", "val": 212},
        {"name": "London–Paris Eurostar", "val": 494},
        {"name": "Frankfurt–Paris ICE/TGV", "val": 563},
        # Japan Shinkansen Strecken
        {"name": "Shinkansen Tokio–Shin-Osaka (Tokaido)", "val": 515},
        {"name": "Shinkansen Tokio–Hakata (Tokio–Kyushu)", "val": 1174},
        {"name": "Shinkansen Tokio–Sapporo (Hokkaido)", "val": 860},
        {"name": "Shinkansen Tokio–Shin-Aomori", "val": 675},
        # China HSR
        {"name": "Beijing–Shanghai HSR", "val": 1318},
        {"name": "Beijing–Guangzhou HSR", "val": 2298},
        {"name": "Shanghai–Kunming HSR", "val": 2252},
        {"name": "Beijing–Harbin HSR", "val": 1388},
        # Skandinavien
        {"name": "Flåmbahn Myrdal–Flåm (Norwegen)", "val": 20},
        {"name": "Rauma-Bahn (Norwegen, Dombås–Åndalsnes)", "val": 114},
        {"name": "Nordlandsbahn Oslo–Bodø", "val": 729},
        {"name": "Ofotbahn Narvik–Riksgränsen", "val": 42},
        # Schweiz
        {"name": "Glacier Express Zermatt–St. Moritz", "val": 291},
        {"name": "Bernina Express Chur–Tirano", "val": 144},
        {"name": "GoldenPass Montreux–Interlaken", "val": 100},
        {"name": "Gotthard Basistunnel (längster Tunnel)", "val": 57},
        # Nahverkehr / S-Bahnen
        {"name": "London Underground (gesamtes Netz)", "val": 402},
        {"name": "Shanghai Metro (gesamtes Netz)", "val": 802},
        {"name": "Peking Metro (gesamtes Netz)", "val": 783},
        {"name": "New York City Subway (gesamtes Netz)", "val": 394},
        {"name": "Moskauer Metro (gesamtes Netz)", "val": 440},
        {"name": "Tokio Metro + Toei (gesamtes Netz)", "val": 313},
        {"name": "Paris Métro (gesamtes Netz)", "val": 225},
        {"name": "Berlin BVG S+U (gesamtes Netz)", "val": 473},
        # Weitere Fernstrecken
        {"name": "Cairo–Luxor–Aswan (Ägypten)", "val": 900},
        {"name": "Zarengold Berlin–Ulan-Ude", "val": 7100},
        {"name": "Machu Picchu Train Cusco–Aguas Calientes", "val": 112},
        {"name": "Darjeeling Himalayan Railway", "val": 88},
        {"name": "Palace on Wheels (Rundkurs Rajasthan)", "val": 1800},
        {"name": "Deccan Odyssey (Rundkurs Maharashtra)", "val": 2400},
        {"name": "Seven Stars Kyushu (Rundkurs)", "val": 1400},
        {"name": "Al Boraq Casablanca–Tanger", "val": 350},
        {"name": "Haramain HSR Medina–Mekka", "val": 453},
        {"name": "THSR Taipei–Kaohsiung", "val": 345},
        {"name": "KTX Seoul–Busan", "val": 423},
        {"name": "AVE Madrid–Valencia", "val": 391},
        {"name": "Madrid–Sevilla AVE (erste HSR Spanien)", "val": 471},
        {"name": "Kandy–Ella Scenic Rail (Sri Lanka)", "val": 174},
        {"name": "West Highland Line Glasgow–Mallaig", "val": 264},
        {"name": "Jacobite Steam Train (Schottland)", "val": 135},
        {"name": "Tren Crucero Quito–Guayaquil", "val": 456},
        {"name": "Gokteik-Viadukt-Bahn (Myanmar)", "val": 260},
        {"name": "Overland Melbourne–Adelaide", "val": 828},
        {"name": "VIA Rail Ocean Montréal–Halifax", "val": 1346},
        {"name": "Caledonian Sleeper London–Inverness", "val": 918},
        {"name": "Nightjet Wien–Amsterdam", "val": 1245},
        {"name": "Lötschbergbahn Bern–Brig (Schweiz)", "val": 74},
        {"name": "Arlberg Express Wien–Bregenz", "val": 629},
        {"name": "EuroCity Praha–Brüssel", "val": 1050},
        {"name": "EuroCity Kraków–Zürich", "val": 1200},
    ]
}
assert len(HL_ZUG_KM["items"]) >= 80, f"zug_km: only {len(HL_ZUG_KM['items'])} items"

# ─────────────────────────────────────────────────────────────────────────────
# 4. TIMELINE ZUG_HSB — Meilensteine der Hochgeschwindigkeit & Metro (80 Items)
# ─────────────────────────────────────────────────────────────────────────────
TIMELINE_ZUG_HSB = {
    "prompt": "Sortiere diese Bahn-Meilensteine chronologisch!",
    "unit": "Jahr",
    "items": [
        {"n": "Stockton–Darlington (erste dampfbetriebene Eisenbahn)", "year": 1825, "hint": "England — George Stephenson"},
        {"n": "Baltimore & Ohio Railroad (erste USA)", "year": 1830, "hint": "USA — erste Personenbeförderung"},
        {"n": "Nürnberg–Fürth (erste Deutschland)", "year": 1835, "hint": "Bayern — Adler-Lokomotive"},
        {"n": "London Underground (erste U-Bahn der Welt)", "year": 1863, "hint": "Metropolitan Railway, Dampfbetrieb"},
        {"n": "Orient Express erste Fahrt Paris–Istanbul", "year": 1883, "hint": "Compagnie Internationale des Wagons-Lits"},
        {"n": "Transsibirische Eisenbahn (Baubeginn)", "year": 1891, "hint": "9.289 km, fertig 1916"},
        {"n": "Budapest Metro (erste Kontinentaleuropa)", "year": 1896, "hint": "Millennium Underground — 3,7 km"},
        {"n": "Paris Métro Eröffnung", "year": 1900, "hint": "Linie 1 — Exposition Universelle"},
        {"n": "Berlin U-Bahn Eröffnung", "year": 1902, "hint": "Siemens & Halske — Stralauer Tor"},
        {"n": "New York City Subway Eröffnung", "year": 1904, "hint": "IRT — erste 28 km"},
        {"n": "Bernina Express erste Fahrt (Schweiz)", "year": 1910, "hint": "2253m Höhe — heute UNESCO"},
        {"n": "Buenos Aires Metro (erste Latinamerika)", "year": 1913, "hint": "Subte Linie A — älteste Latam"},
        {"n": "Glacier Express erste Durchfahrt", "year": 1930, "hint": "Zermatt–St. Moritz — 291 km"},
        {"n": "Moskauer Metro Eröffnung", "year": 1935, "hint": "12 Stationen — Palast-Stationen"},
        {"n": "Shinkansen Tokaido (erste HSR weltweit)", "year": 1964, "hint": "Tokio–Osaka — 210 km/h"},
        {"n": "Mexico City Metro (erste Mexiko)", "year": 1969, "hint": "Linie 1 — 12 km"},
        {"n": "Shinkansen San'yo (Osaka–Okayama)", "year": 1972, "hint": "250 km/h Betrieb"},
        {"n": "BART San Francisco Eröffnung", "year": 1972, "hint": "Bay Area Rapid Transit — 43 km"},
        {"n": "São Paulo Metro (erste Brasilien)", "year": 1974, "hint": "Linie 1 — 7 Stationen"},
        {"n": "Washington Metro (USA)", "year": 1976, "hint": "District of Columbia — 178 km"},
        {"n": "Hong Kong MTR Eröffnung", "year": 1979, "hint": "erste Hochgeschwindigkeits-Metro Asiens"},
        {"n": "TGV Paris–Lyon (erste HSR Europa)", "year": 1981, "hint": "260 km/h → später 300"},
        {"n": "Shinkansen Tohoku (Tokio–Morioka)", "year": 1982, "hint": "240 km/h"},
        {"n": "California Zephyr (Amtrak neu)", "year": 1983, "hint": "Chicago–San Francisco — 3.924 km"},
        {"n": "Cairo Metro (erste Afrika)", "year": 1987, "hint": "Linie 1 — erste U-Bahn Afrikas"},
        {"n": "Singapore MRT Eröffnung", "year": 1987, "hint": "Mass Rapid Transit — 67 km initial"},
        {"n": "ICE 1 erste Fahrt (Deutschland)", "year": 1991, "hint": "Hamburg–München — 280 km/h"},
        {"n": "AVE Madrid–Sevilla (erste HSR Spanien)", "year": 1992, "hint": "270 km/h — Expo 1992"},
        {"n": "Shanghai Metro (erste China Großstadt)", "year": 1993, "hint": "Linie 1 — heute 802 km"},
        {"n": "Eurostar London–Paris Eröffnung", "year": 1994, "hint": "Ärmelkanaltunnel — 494 km"},
        {"n": "Thalys Paris–Brüssel–Amsterdam", "year": 1996, "hint": "300 km/h — PBKA"},
        {"n": "Taipei MRT Eröffnung", "year": 1996, "hint": "erste vollautomatische Metro Asiens"},
        {"n": "Delhi Metro Eröffnung", "year": 2002, "hint": "erste Phase Delhi — 8,4 km"},
        {"n": "KTX-I erste Fahrt (Südkorea)", "year": 2004, "hint": "Seoul–Busan — 300 km/h"},
        {"n": "The Ghan Adelaide–Darwin (neue Strecke)", "year": 2004, "hint": "2.979 km — Vollendung"},
        {"n": "TGV Est Paris–Straßburg", "year": 2007, "hint": "320 km/h Betriebsgeschwindigkeit"},
        {"n": "THSR Taipei–Kaohsiung (Taiwan HSR)", "year": 2007, "hint": "300 km/h — Shinkansen-Technologie"},
        {"n": "Beijing–Shanghai HSR Eröffnung (erster China-HSR-Zug)", "year": 2008, "hint": "350 km/h — 1.318 km"},
        {"n": "AVE Madrid–Barcelona", "year": 2008, "hint": "Spanien — 600 km in 2:30h"},
        {"n": "Velaro RUS Sapsan (Russland)", "year": 2009, "hint": "Moskau–St. Petersburg — 250 km/h"},
        {"n": "Dubai Metro Eröffnung", "year": 2009, "hint": "erste führerlose Metro Naher Osten"},
        {"n": "TCDD YHT (Türkei HSR Ankara–Eskişehir)", "year": 2009, "hint": "250 km/h"},
        {"n": "Shinkansen Kyushu Hakata–Kagoshima", "year": 2011, "hint": "260 km/h"},
        {"n": "Shinkansen E5/H5 Debüt (Hayabusa)", "year": 2011, "hint": "320 km/h — Tokio–Shin-Aomori"},
        {"n": "AGV Italo erste Fahrt (Italien)", "year": 2012, "hint": "NTV — 300 km/h, Privatbahn"},
        {"n": "TGV Euroduplex Einführung", "year": 2012, "hint": "320 km/h — 2-stöckig"},
        {"n": "Ouigo Frankreich (Low-Cost TGV)", "year": 2013, "hint": "SNCF Tochter — 300 km/h"},
        {"n": "Frecciarossa 1000 (schnellster Zug Europas)", "year": 2015, "hint": "400 km/h Rekord — 300 km/h Betrieb"},
        {"n": "Haramain HSR Medina–Mekka", "year": 2018, "hint": "Saudi-Arabien — 300 km/h"},
        {"n": "Al Boraq Casablanca–Tanger (erste HSR Afrika)", "year": 2018, "hint": "Marokko ONCF — 320 km/h"},
        {"n": "FlixTrain Deutschlandstart", "year": 2018, "hint": "erstes privates Fernzugnetz Deutschland"},
        {"n": "Vande Bharat Express (Indien)", "year": 2019, "hint": "Make in India — 180 km/h"},
        {"n": "Shinkansen Hokkaido (Sapporo)", "year": 2030, "hint": "geplant — Tokio–Sapporo 4:30h"},
        {"n": "Elizabeth Line London (Crossrail)", "year": 2022, "hint": "118 km — 24 Stationen"},
        {"n": "KTX-Eum (Südkorea, eigene Technologie)", "year": 2021, "hint": "260 km/h — heimische Entwicklung"},
        {"n": "CR450 Fuxing (China, geplant)", "year": 2025, "hint": "400 km/h Betrieb — in Entwicklung"},
        # Metro-Erweiterungen Global
        {"n": "Stockholm Tunnelbana Eröffnung", "year": 1950, "hint": "Schweden — Umwandlung der Ringbahn"},
        {"n": "Toronto Subway Line 1", "year": 1954, "hint": "Kanada — erste U-Bahn Kanadas"},
        {"n": "Montréal Metro (Gummireifen)", "year": 1966, "hint": "Kanada — Expo 67 Erweiterung"},
        {"n": "München U-Bahn (vor Olympia)", "year": 1971, "hint": "Deutschland — Olympische Spiele 1972"},
        {"n": "Peking Metro erste Linie", "year": 1969, "hint": "China — heute 783 km Netz"},
        {"n": "Tokio Metro Ginza Line (erste Asien)", "year": 1927, "hint": "Japan — Asakusa–Ueno"},
        {"n": "Madrid Metro Eröffnung", "year": 1919, "hint": "Spanien — Sol–Cuatro Caminos"},
        {"n": "Glasgow Subway Eröffnung", "year": 1896, "hint": "UK — Seilbahn, dann Strom"},
        {"n": "Budapest Millennium Underground", "year": 1896, "hint": "erste kontinental-europ. Metro"},
        {"n": "Bangkok BTS Skytrain", "year": 1999, "hint": "Thailand — erste vollklimatisierte Sky-Rail"},
        {"n": "Copenhagen Metro (driverless)", "year": 2002, "hint": "Dänemark — führerlos"},
        {"n": "Riyadh Metro Eröffnung", "year": 2021, "hint": "Saudi-Arabien — größte neue Metro"},
        {"n": "Athens Metro (Modernisierung)", "year": 2000, "hint": "Griechenland — Olympia-Vorbereitung"},
        {"n": "Mailand Metro Linie 1", "year": 1964, "hint": "Italien — Zara–Sesto Marelli"},
        {"n": "Barcelona Metro Eröffnung", "year": 1924, "hint": "Spanien — Gran Vía"},
        {"n": "Wien U-Bahn Linie U1 Eröffnung", "year": 1978, "hint": "Österreich — Reumannplatz–Karlsplatz"},
        {"n": "Chicago 'L' Hochbahn Eröffnung", "year": 1892, "hint": "USA — erstes Hochbahnsystem"},
        {"n": "Oslo T-bane Eröffnung", "year": 1966, "hint": "Norwegen — Untergrundnetz"},
        {"n": "Warschau Metro Linie 1", "year": 1995, "hint": "Polen — 22 Stationen"},
        {"n": "Prag Metro Eröffnung", "year": 1974, "hint": "Tschechien — sowjetische Bauweise"},
        {"n": "Brüssel Metro (erste Linie)", "year": 1976, "hint": "Belgien — Linie 1A/1B"},
        {"n": "Amsterdam Metro Linie 50", "year": 1977, "hint": "Niederlande — Bijlmermeer"},
        {"n": "Krakau Straßenbahn-Tunnellinie", "year": 1997, "hint": "Polen — unterirdische Tram"},
        {"n": "EuroCity Praha–Zürich erste planmäßige Fahrt", "year": 1993, "hint": "Tschechien–Schweiz via Deutschland"},
    ]
}
assert len(TIMELINE_ZUG_HSB["items"]) >= 80, f"timeline: only {len(TIMELINE_ZUG_HSB['items'])} items"

# ─────────────────────────────────────────────────────────────────────────────
# 5. WORT-SCHMIEDE — Zug-Namen (15 hochwertige Einträge, 7+ Buchstaben)
# ─────────────────────────────────────────────────────────────────────────────
WS_ZUG = {
    "zug_intercity": {
        "word": "INTERCITY",
        "validWords": {
            "de": ["INTER", "CITY", "RICE", "CITE", "TIRE", "NICE", "RITE", "REIN", "TIER", "NEIN", "CENT", "RICY"],
            "en": ["INTER", "CITY", "RICE", "CITE", "TIRE", "NICE", "RITE", "REIN", "CENT", "TERN", "TINY", "INCI"]
        }
    },
    "zug_shinkansen": {
        "word": "SHINKANSEN",
        "validWords": {
            "de": ["SINN", "KAHN", "NASE", "HANS", "SHIN", "HASEN", "INNEN", "SENK", "KANIS"],
            "en": ["SHIN", "SKIN", "SINK", "KHAN", "SHAKE", "SNAKE", "INANE", "ANNEX", "SENK"]
        }
    },
    "zug_frecciarossa": {
        "word": "FRECCIAROSSA",
        "validWords": {
            "de": ["ROSS", "ROSE", "CERO", "RASSE", "SARC", "CARE", "RACE", "ARCO", "ORCA", "OSCAR"],
            "en": ["FORCE", "RACE", "ROSE", "CARE", "CROSS", "SCORE", "FARCE", "ARCO", "SCAR", "ROOF"]
        }
    },
    "zug_pendolino": {
        "word": "PENDOLINO",
        "validWords": {
            "de": ["DINO", "LINO", "PEIN", "NOEL", "LIED", "OPEN", "PEON", "ODIN", "LINDEN", "ONDE"],
            "en": ["DINO", "PILED", "NODE", "ONLINE", "LINED", "OPINE", "ELOPED", "DONE", "PEON", "LOIN"]
        }
    },
    "zug_railjet": {
        "word": "RAILJET",
        "validWords": {
            "de": ["RAIL", "LITER", "REIT", "JATI", "TIER", "EILE", "REIL"],
            "en": ["RAIL", "TRAIL", "JAIL", "JILT", "LITE", "LITER", "TILE", "LAIR", "TAIL", "RATE"]
        }
    },
    "zug_eurostar": {
        "word": "EUROSTAR",
        "validWords": {
            "de": ["EURO", "STAR", "TOUR", "RAUS", "ROTE", "OSTE", "RAST"],
            "en": ["EURO", "STAR", "TOUR", "ROAST", "STORE", "ROUSE", "OATER", "OUTER", "ROUTE", "UREA"]
        }
    },
    "zug_thalys": {
        "word": "THALYS",
        "validWords": {
            "de": ["HALT", "SLAY", "LAST", "SALT", "LATH"],
            "en": ["HALT", "LASH", "SLAY", "LAST", "SALT", "STAY", "LATH", "HATS", "HYLAS", "YALT"]
        }
    },
    "zug_velaro": {
        "word": "VELARO",
        "validWords": {
            "de": ["AVEL", "LORE", "ORAL", "VALE", "ALER", "ROVE"],
            "en": ["VALE", "ORAL", "LOVE", "ROVE", "OVER", "VEAL", "LAVE", "LORE", "VALOR", "AVORE"]
        }
    },
    "zug_bernina": {
        "word": "BERNINA",
        "validWords": {
            "de": ["BEIN", "REIN", "NAIB", "RANI", "BEER", "BIER", "IRAN"],
            "en": ["BRINE", "BRAIN", "REIN", "BEAR", "RAIN", "RANI", "INNER", "BRAN", "BARE", "BEAN"]
        }
    },
    "zug_trenitalia": {
        "word": "TRENITALIA",
        "validWords": {
            "de": ["TRAIL", "TRAIN", "LITER", "REIN", "TIER", "LITE", "NITER", "REITAL", "TRIAL", "NARITA"],
            "en": ["TRAIL", "TRAIN", "TRIAL", "LITER", "LINER", "ALIEN", "INERT", "RENAL", "TITER", "LITRE"]
        }
    },
    "zug_itineraire": {
        "word": "ITINERAIRE",
        "validWords": {
            "de": ["REIN", "TIER", "IRAN", "ITER", "NEIN", "IRENE"],
            "en": ["TRAIN", "REIN", "REIN", "RAIN", "INTER", "INERT", "AIRLINE", "ENTIRE", "RETINA", "IRENE"]
        }
    },
    "zug_talgo": {
        "word": "TALGO",
        "validWords": {
            "de": ["GALT", "TALO", "LOTA"],
            "en": ["GLOAT", "ALTO", "GOAL", "TALO", "LOGO", "GALE", "OGLE", "TOTAL", "GALT"]
        }
    },
    "zug_maglev": {
        "word": "MAGLEV",
        "validWords": {
            "de": ["GALE", "MALE", "LAME", "MEGA"],
            "en": ["GAVEL", "VALE", "MALE", "LAME", "MEGA", "LAVE", "VEAL", "GAME", "GAVE", "GLAM"]
        }
    },
    "zug_flixzug": {
        "word": "FLIXZUG",
        "validWords": {
            "de": ["LUGE", "GLUF", "FLIP", "GILF"],
            "en": ["GLUG", "FLUX", "GILF", "GLIB"]
        }
    },
    "zug_acela": {
        "word": "ACELA",
        "validWords": {
            "de": ["CALE", "LACE", "KALE"],
            "en": ["LACE", "CALE", "ALCE", "ACNE", "ALEC", "CELA", "LACE", "ACEA"]
        }
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# PATCH AUSFÜHREN
# ─────────────────────────────────────────────────────────────────────────────
print("=" * 58)
print(" Phase 296.2 — Trainspotter Mega Sprint")
print("=" * 58)

# 1. sport_hl.json patchen
print("\n[1/4] sport_hl.json — 3 neue HL-Sets ...")
spath = os.path.join(BASE, 'data', 'sport_hl.json')
with open(spath, 'r', encoding='utf-8') as f: sport_hl = json.load(f)

for key, data in [('zug_speed', HL_ZUG_SPEED), ('zug_jahr', HL_ZUG_JAHR), ('zug_km', HL_ZUG_KM)]:
    if key in sport_hl:
        print(f"  [SKIP] {key} already exists")
    else:
        sport_hl[key] = data
        print(f"  [OK] {key}: {len(data['items'])} Items, prompt={repr(data['prompt'])[:40]}")

with open(spath, 'w', encoding='utf-8') as f: json.dump(sport_hl, f, ensure_ascii=False, indent=2)
print("  [OK] sport_hl.json gespeichert")

# 2. timeline.json patchen
print("\n[2/4] timeline.json — zug_hsb ...")
tpath = os.path.join(BASE, 'data', 'timeline.json')
with open(tpath, 'r', encoding='utf-8') as f: timeline = json.load(f)

if 'zug_hsb' in timeline:
    print("  [SKIP] zug_hsb already exists")
else:
    timeline['zug_hsb'] = TIMELINE_ZUG_HSB
    print(f"  [OK] zug_hsb: {len(TIMELINE_ZUG_HSB['items'])} Items")

with open(tpath, 'w', encoding='utf-8') as f: json.dump(timeline, f, ensure_ascii=False, indent=2)
print("  [OK] timeline.json gespeichert")

# 3. tiere_ws.json patchen
print("\n[3/4] tiere_ws.json — 15 Zug-Namen WS ...")
wpath = os.path.join(BASE, 'data', 'tiere_ws.json')
with open(wpath, 'r', encoding='utf-8') as f: ws_data = json.load(f)

added_ws = 0
for key, entry in WS_ZUG.items():
    if key in ws_data:
        print(f"  [SKIP] {key}")
    else:
        ws_data[key] = entry
        added_ws += 1

with open(wpath, 'w', encoding='utf-8') as f: json.dump(ws_data, f, ensure_ascii=False, indent=2)
print(f"  [OK] {added_ws} WS-Einträge hinzugefügt → tiere_ws.json")

# 4. gen.py patchen
print("\n[4/4] gen.py — MODES + GEN dispatch + MODE_CATS ...")
gpath = os.path.join(BASE, 'gen.py')
with open(gpath, 'r', encoding='utf-8') as f: content = f.read()

already_done = 'hl_zug_speed' in content

if already_done:
    print("  [SKIP] Modi bereits vorhanden")
else:
    # A: MODES Einträge nach zug_vkm einfügen
    ANCHOR_MODES = '{id:"zug_vkm"'
    if ANCHOR_MODES in content:
        idx = content.find(ANCHOR_MODES)
        line_end = content.find('\n', idx)
        NEW_MODES = (
            '\n    {id:"hl_zug_speed",      icon:"\\u26A1",title:"H/L: Zuggeschwindigkeit",        '
            'group:"zuege",prompt:"Höhere Betriebsgeschwindigkeit?",                         '
            'desc:"ICE vs. Shinkansen vs. TGV vs. Maglev"},\n'
            '    {id:"hl_zug_jahr",       icon:"\\u{1F4C5}",title:"H/L: Bahn-Geschichte",          '
            'group:"zuege",prompt:"Früher in Betrieb genommen?",                              '
            'desc:"Wann eröffnete dieses Netz oder dieser Zug?"},\n'
            '    {id:"hl_zug_km",         icon:"\\u{1F4CF}",title:"H/L: Streckenkil. Fernzug",     '
            'group:"zuege",prompt:"Längere Strecke?",                                        '
            'desc:"Trans-Sibirisch vs. Glacier Express — Streckenlängen"},\n'
            '    {id:"timeline_zug_hsb",  icon:"\\u{1F686}",title:"Bahn-Timeline",                 '
            'group:"zuege",prompt:"Chronologisch sortieren — Bahn-Meilensteine!",                 '
            'desc:"Erste HSR, Metro-Eröffnungen & Zuggeschichte"},\n'
        )
        # WS Modi
        for ws_key in WS_ZUG.keys():
            short = ws_key.replace('zug_', '')
            word  = WS_ZUG[ws_key]['word']
            NEW_MODES += (
                f'    {{id:"ws_{ws_key}",        icon:"\\u{{1F524}}",title:"WS: {word.title()}",              '
                f'group:"zuege",prompt:"Bilde Wörter aus dem Zugnamen!",                     '
                f'desc:"Anagramm-Rätsel: {word} — {len(word)} Buchstaben"}},\n'
            )
        content = content[:line_end] + NEW_MODES + content[line_end:]
        print("  [OK] MODES Einträge eingefügt")
    else:
        print("  [WARN] zug_vkm anchor nicht gefunden")

    # B: GEN dispatch nach zug_vkm
    ANCHOR_GEN = 'zug_vkm:()=>genUniversalMatchQ("zug_vkm")'
    if ANCHOR_GEN in content:
        idx = content.find(ANCHOR_GEN)
        line_end = content.find('\n', idx)
        NEW_GEN = (
            '\n  hl_zug_speed:()=>genSportWissenHL("zug_speed"),'
            '\n  hl_zug_jahr:()=>genSportWissenHL("zug_jahr"),'
            '\n  hl_zug_km:()=>genSportWissenHL("zug_km"),'
            '\n  timeline_zug_hsb:()=>genTimelineQ("zug_hsb"),'
        )
        for ws_key in WS_ZUG.keys():
            NEW_GEN += f'\n  ws_{ws_key}:()=>initTierWortSchmiede("{ws_key}"),'
        content = content[:line_end] + NEW_GEN + content[line_end:]
        print("  [OK] GEN dispatch eingefügt")
    else:
        print("  [WARN] GEN anchor nicht gefunden")

    # C: MODE_CATS zuege erweitern
    CATS_ANCHOR = '"zug_panorama","zug_vkm","uk_bahnstrecken","hl_b_rail"'
    NEW_CATS = ('"zug_panorama","zug_vkm","uk_bahnstrecken","hl_b_rail",'
                '"hl_zug_speed","hl_zug_jahr","hl_zug_km","timeline_zug_hsb",'
                + ','.join(f'"ws_{k}"' for k in WS_ZUG.keys()))
    if CATS_ANCHOR in content:
        content = content.replace(CATS_ANCHOR, NEW_CATS, 1)
        print("  [OK] MODE_CATS zuege erweitert")
    else:
        print("  [WARN] zuege cats anchor nicht gefunden")

with open(gpath, 'w', encoding='utf-8') as f: f.write(content)

# Finale Validierung
print("\n[CHECK] Validierung ...")
with open(gpath) as f: c2 = f.read()
checks = {
    'hl_zug_speed MODES':    'id:"hl_zug_speed"' in c2,
    'hl_zug_jahr MODES':     'id:"hl_zug_jahr"' in c2,
    'hl_zug_km MODES':       'id:"hl_zug_km"' in c2,
    'timeline_zug_hsb MODES':'id:"timeline_zug_hsb"' in c2,
    'ws_zug_intercity MODES':'id:"ws_zug_intercity"' in c2,
    'HL GEN dispatch':       'hl_zug_speed:()=>genSportWissenHL' in c2,
    'Timeline GEN':          'timeline_zug_hsb:()=>genTimelineQ' in c2,
    'WS GEN':                'ws_zug_intercity:()=>initTierWortSchmiede' in c2,
}
all_ok = True
for k, v in checks.items():
    print(f"  {'[OK]' if v else '[!!]'} {k}")
    if not v: all_ok = False

print()
if all_ok:
    print("PATCH ABGESCHLOSSEN — jetzt gen.py rebuilden!")
else:
    print("FEHLER — manuelle Prüfung nötig")
    sys.exit(1)
