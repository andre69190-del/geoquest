"""
Phase: 253
Date:  2026-05-27
Author: Claude / Andre
Scope: Geologie & Vulkane — Massiver Content-Ausbau: 40 neue Modi.

Description:
  Erweitert die vier data/geo_*.json Dateien und registriert 40 neue Modi:

  geo_pin.json  (+12): felsformationen, hoehlensysteme, canyons, geysire,
    fossilien_fundstaetten, ozeangraeben, gletscher, wuesten,
    minen_bohrungen, rifts, nationalparks_geologie, steilkuesten

  geo_hl.json   (+10): mohshaerte, vei_ausbruch, hoehlen_laenge,
    gesteins_alter, schluchten_tiefe, kontinentaldrift, schmelztemperatur,
    gletscher_volumen, tsunami_hoehe, bohrtiefe

  geo_match.json (+12): vulkan_land, berg_gebirge, wunder_entstehung,
    fossil_zeitalter, erdbeben_jahr, gestein_nutzung, landschaft_ursprung,
    mineral_farbe, kontinent_platte, hoehlen_land, mineral_kristall,
    gebirge_entstehung

  geo_ws.json   (+6): tropfstein, magmakammer, kontinent, fossilien,
    erdkruste, mineralien

Dependencies: patch_243_new_worlds.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import json, pathlib, sys
from collections import Counter

ROOT = pathlib.Path(__file__).parent.parent
DATA = ROOT / "data"
GEN  = ROOT / "gen.py"

# ══════════════════════════════════════════════════════════════════════════════
# 1. JSON DATA
# ══════════════════════════════════════════════════════════════════════════════

NEW_PIN = {
  "geo_felsformationen": {
    "prompt": "Wo liegt diese berühmte Felsformation?",
    "items": [
      {"n": "Uluru / Ayers Rock (Australien)", "lat": -25.34, "lng": 131.04},
      {"n": "Giant's Causeway (Nordirland, UK)", "lat": 55.24, "lng": -6.51},
      {"n": "Preikestolen (Norwegen)", "lat": 58.99, "lng": 6.19},
      {"n": "Wave Rock (Westaustralien)", "lat": -32.44, "lng": 118.90},
      {"n": "Zhangjiajie Sandsteinsäulen (China)", "lat": 29.33, "lng": 110.44},
      {"n": "Moeraki Boulders (Neuseeland)", "lat": -45.35, "lng": 170.84},
      {"n": "Bungle Bungle Range (Australien)", "lat": -17.51, "lng": 128.44},
      {"n": "Kappadokien Feenkamine (Türkei)", "lat": 38.63, "lng": 34.83}
    ]
  },
  "geo_hoehlensysteme": {
    "prompt": "Wo liegt dieses Höhlensystem?",
    "items": [
      {"n": "Mammoth Cave System (Kentucky, USA)", "lat": 37.19, "lng": -86.10},
      {"n": "Son Doong (Phong Nha, Vietnam)", "lat": 17.55, "lng": 106.29},
      {"n": "Eisriesenwelt (Werfen, Österreich)", "lat": 47.50, "lng": 13.19},
      {"n": "Sistema Ox Bel Ha (Yucatán, Mexiko)", "lat": 20.02, "lng": -87.63},
      {"n": "Reed Flute Cave (Guilin, China)", "lat": 25.28, "lng": 110.28},
      {"n": "Jenolan Caves (Neusüdwales, Australien)", "lat": -33.82, "lng": 150.02},
      {"n": "Škocjan-Höhlen (Slowenien)", "lat": 45.66, "lng": 13.99},
      {"n": "Carlsbad Caverns (New Mexico, USA)", "lat": 32.18, "lng": -104.44}
    ]
  },
  "geo_canyons": {
    "prompt": "Wo liegt diese Schlucht / dieser Canyon?",
    "items": [
      {"n": "Grand Canyon (Arizona, USA)", "lat": 36.05, "lng": -112.14},
      {"n": "Colca Canyon (Peru)", "lat": -15.53, "lng": -71.98},
      {"n": "Tara Canyon (Montenegro)", "lat": 43.15, "lng": 19.25},
      {"n": "Cotahuasi Canyon (Peru)", "lat": -15.22, "lng": -72.88},
      {"n": "Verdon-Schlucht (Frankreich)", "lat": 43.72, "lng": 6.32},
      {"n": "Fish River Canyon (Namibia)", "lat": -27.72, "lng": 17.58},
      {"n": "Antelope Canyon (Arizona, USA)", "lat": 36.86, "lng": -111.37},
      {"n": "Bryce Canyon (Utah, USA)", "lat": 37.57, "lng": -112.18}
    ]
  },
  "geo_geysire": {
    "prompt": "Wo liegt dieser Geysir?",
    "items": [
      {"n": "El Tatio (Atacama, Chile)", "lat": -22.33, "lng": -68.02},
      {"n": "Fly Geyser (Black Rock Desert, Nevada, USA)", "lat": 40.86, "lng": -119.33},
      {"n": "Steamboat Geyser (Yellowstone, USA)", "lat": 44.66, "lng": -110.87},
      {"n": "Pohutu Geyser (Whakarewarewa, Neuseeland)", "lat": -38.12, "lng": 176.27},
      {"n": "Geysir (Haukadalur, Island)", "lat": 64.31, "lng": -20.29},
      {"n": "Castle Geyser (Yellowstone, USA)", "lat": 44.46, "lng": -110.84},
      {"n": "Nagqu Geothermie-Geysire (Tibet, China)", "lat": 31.48, "lng": 92.06},
      {"n": "Beowawe Geysers (Nevada, USA)", "lat": 40.58, "lng": -116.57}
    ]
  },
  "geo_fossilien_fundstaetten": {
    "prompt": "Wo liegt diese bedeutende Fossilien-Fundstätte?",
    "items": [
      {"n": "Jurassic Coast (Dorset, England)", "lat": 50.73, "lng": -2.73},
      {"n": "Grube Messel (Hessen, Deutschland)", "lat": 49.92, "lng": 8.74},
      {"n": "Burgess Shale (British Columbia, Kanada)", "lat": 51.44, "lng": -116.49},
      {"n": "Solnhofener Plattenkalk (Bayern, Deutschland)", "lat": 48.90, "lng": 11.05},
      {"n": "Hell Creek Formation (Montana, USA)", "lat": 47.50, "lng": -104.10},
      {"n": "Ediacara Hills (Südaustralien)", "lat": -31.06, "lng": 138.41},
      {"n": "Bernissart (Iguanodon-Fundort, Belgien)", "lat": 50.47, "lng": 3.66},
      {"n": "Liang Bua (Homo floresiensis, Indonesien)", "lat": -8.53, "lng": 120.45}
    ]
  },
  "geo_ozeangraeben": {
    "prompt": "Wo liegt dieser Ozeangraben / tiefste Punkt?",
    "items": [
      {"n": "Marianengraben (Pazifik)", "lat": 11.37, "lng": 142.60},
      {"n": "Tongagraben (Pazifik)", "lat": -23.23, "lng": -175.38},
      {"n": "Philippinengraben (Pazifik)", "lat": 10.00, "lng": 126.60},
      {"n": "Puerto-Rico-Graben (Atlantik)", "lat": 19.72, "lng": -66.25},
      {"n": "Kurilen-Kamtschatka-Graben (Pazifik)", "lat": 44.50, "lng": 150.00},
      {"n": "Java-Graben / Sundagraben (Ind. Ozean)", "lat": -10.00, "lng": 108.00},
      {"n": "Izu-Bonin-Graben (Pazifik)", "lat": 30.00, "lng": 143.00},
      {"n": "Südandinen Graben (Pazifik)", "lat": -43.00, "lng": -72.00}
    ]
  },
  "geo_gletscher": {
    "prompt": "Wo liegt dieser Gletscher?",
    "items": [
      {"n": "Aletschgletscher (Schweiz)", "lat": 46.47, "lng": 8.05},
      {"n": "Perito Moreno (Patagonien, Argentinien)", "lat": -50.50, "lng": -73.03},
      {"n": "Franz-Josef-Gletscher (Neuseeland)", "lat": -43.48, "lng": 170.18},
      {"n": "Athabasca-Gletscher (Kanada)", "lat": 52.23, "lng": -117.25},
      {"n": "Jostedalsbreen (Norwegen)", "lat": 61.66, "lng": 6.95},
      {"n": "Svalbard Kongsvegen-Gletscher (Norwegen)", "lat": 78.80, "lng": 12.98},
      {"n": "Gornergletscher (Schweiz)", "lat": 45.97, "lng": 7.79},
      {"n": "Biafo-Gletscher (Pakistan)", "lat": 35.80, "lng": 75.75}
    ]
  },
  "geo_wuesten": {
    "prompt": "Wo liegt diese Wüste oder Wüstenlandschaft?",
    "items": [
      {"n": "Namib-Wüste (Namibia)", "lat": -22.00, "lng": 15.00},
      {"n": "Atacama-Wüste (Chile)", "lat": -24.50, "lng": -69.25},
      {"n": "Sossusvlei Dünen (Namibia)", "lat": -24.73, "lng": 15.35},
      {"n": "Wadi Rum (Jordanien)", "lat": 29.59, "lng": 35.42},
      {"n": "Weiße Wüste (Sahara, Ägypten)", "lat": 28.30, "lng": 27.24},
      {"n": "Rub' al Khali (Saudi-Arabien)", "lat": 20.00, "lng": 51.00},
      {"n": "Taklamakan-Wüste (Xinjiang, China)", "lat": 38.90, "lng": 83.65},
      {"n": "Karakum-Wüste (Turkmenistan)", "lat": 38.74, "lng": 60.00}
    ]
  },
  "geo_minen_bohrungen": {
    "prompt": "Wo liegt diese Mine oder dieses Bohrprojekt?",
    "items": [
      {"n": "Kola Superdeep Borehole (Russland)", "lat": 69.40, "lng": 30.61},
      {"n": "Bingham Canyon Mine (Utah, USA)", "lat": 40.52, "lng": -112.14},
      {"n": "Chuquicamata Kupfermine (Chile)", "lat": -22.31, "lng": -68.92},
      {"n": "Mir-Diamantmine (Jakutien, Russland)", "lat": 62.53, "lng": 113.99},
      {"n": "South Deep Gold Mine (Südafrika)", "lat": -26.71, "lng": 27.61},
      {"n": "Diavik Diamantmine (Northwest Territories, Kanada)", "lat": 64.52, "lng": -110.25},
      {"n": "Escondida Kupfermine (Chile)", "lat": -24.27, "lng": -69.07},
      {"n": "Bayan Obo (Seltene Erden, China)", "lat": 41.77, "lng": 109.95}
    ]
  },
  "geo_rifts": {
    "prompt": "Wo liegt dieser tektonische Graben / diese Spalte?",
    "items": [
      {"n": "Ostafrikanischer Grabenbruch (Kenia)", "lat": 1.00, "lng": 37.00},
      {"n": "Silfra-Spalte (Island)", "lat": 64.26, "lng": -21.12},
      {"n": "Rotes-Meer-Rift (Eritrea/Jemen)", "lat": 15.00, "lng": 43.00},
      {"n": "Totes-Meer-Transform (Jordanien)", "lat": 31.60, "lng": 35.50},
      {"n": "Baikal-Rift (Sibirien, Russland)", "lat": 53.50, "lng": 108.00},
      {"n": "Rio Grande Rift (New Mexico, USA)", "lat": 36.00, "lng": -106.50},
      {"n": "Limagne-Graben (Auvergne, Frankreich)", "lat": 45.75, "lng": 3.13},
      {"n": "Basin-and-Range Province (Nevada, USA)", "lat": 39.00, "lng": -117.00}
    ]
  },
  "geo_nationalparks_geologie": {
    "prompt": "Wo liegt dieser Nationalpark mit besonderer Geologie?",
    "items": [
      {"n": "Yellowstone National Park (USA)", "lat": 44.43, "lng": -110.59},
      {"n": "Pamukkale Travertine (Türkei)", "lat": 37.92, "lng": 29.12},
      {"n": "Tsingy de Bemaraha (Madagaskar)", "lat": -18.94, "lng": 44.83},
      {"n": "Chocolate Hills (Bohol, Philippinen)", "lat": 9.80, "lng": 124.15},
      {"n": "Waitomo Caves (Neuseeland)", "lat": -38.26, "lng": 175.10},
      {"n": "Plitvice Seen (Kroatien)", "lat": 44.88, "lng": 15.62},
      {"n": "White Sands National Monument (USA)", "lat": 32.78, "lng": -106.17},
      {"n": "Danakil-Senke (Äthiopien)", "lat": 14.23, "lng": 40.29}
    ]
  },
  "geo_steilkuesten": {
    "prompt": "Wo befinden sich diese Steilküsten / Klippen?",
    "items": [
      {"n": "Cliffs of Moher (Irland)", "lat": 52.97, "lng": -9.43},
      {"n": "White Cliffs of Dover (England)", "lat": 51.13, "lng": 1.38},
      {"n": "Bunda Cliffs (Nullarbor, Australien)", "lat": -31.67, "lng": 129.58},
      {"n": "Étretat Kreidefelsen (Normandie, Frankreich)", "lat": 49.71, "lng": 0.20},
      {"n": "Cape Hauy (Tasmanien, Australien)", "lat": -43.03, "lng": 147.91},
      {"n": "Rubjerg Knude (Nordjütland, Dänemark)", "lat": 57.43, "lng": 9.78},
      {"n": "Hornelen Klippe (Norwegen)", "lat": 61.67, "lng": 5.17},
      {"n": "Ponta de São Lourenço (Madeira)", "lat": 32.74, "lng": -16.72}
    ]
  }
}

NEW_HL = {
  "geo_mohshaerte": {
    "prompt": "Welches Mineral ist härter (Mohs-Skala)?",
    "unit": "Mohs-Härtegrad",
    "items": [
      {"name": "Diamant", "val": 10},
      {"name": "Korund (Rubin/Saphir)", "val": 9},
      {"name": "Topas", "val": 8},
      {"name": "Quarz", "val": 7},
      {"name": "Feldspat (Orthoklas)", "val": 6},
      {"name": "Apatit", "val": 5},
      {"name": "Fluorit", "val": 4},
      {"name": "Kalzit", "val": 3},
      {"name": "Gips", "val": 2},
      {"name": "Talk", "val": 1}
    ]
  },
  "geo_vei_ausbruch": {
    "prompt": "Welcher Vulkanausbruch war explosiver (VEI)?",
    "unit": "Vulkanexplosivitätsindex (VEI)",
    "items": [
      {"name": "Tambora 1815 (Indonesien)", "val": 7},
      {"name": "Krakatau 1883 (Indonesien)", "val": 6},
      {"name": "Pinatubo 1991 (Philippinen)", "val": 6},
      {"name": "Katmai 1912 (Alaska, USA)", "val": 6},
      {"name": "Mt. St. Helens 1980 (USA)", "val": 5},
      {"name": "Vesuv 79 n. Chr. (Italien)", "val": 5},
      {"name": "Eyjafjallajökull 2010 (Island)", "val": 4},
      {"name": "Kilauea 2018 (Hawaii, USA)", "val": 1}
    ]
  },
  "geo_hoehlen_laenge": {
    "prompt": "Welches Höhlensystem ist länger?",
    "unit": "km (kartierte Länge)",
    "items": [
      {"name": "Mammoth Cave System (USA)", "val": 685},
      {"name": "Sistema Ox Bel Ha (Mexiko)", "val": 368},
      {"name": "Jewel Cave (South Dakota, USA)", "val": 338},
      {"name": "Wind Cave (South Dakota, USA)", "val": 222},
      {"name": "Hölloch (Schweiz)", "val": 215},
      {"name": "Lechuguilla Cave (USA)", "val": 240},
      {"name": "Hirlatzhöhle (Österreich)", "val": 100},
      {"name": "Eisriesenwelt (Österreich)", "val": 42}
    ]
  },
  "geo_gesteins_alter": {
    "prompt": "Welches Gestein / welche Gesteinsformation ist älter?",
    "unit": "Millionen Jahre",
    "items": [
      {"name": "Jack Hills Zirkon (Australien)", "val": 4400},
      {"name": "Acasta Gneiss (Kanada)", "val": 4030},
      {"name": "Isua-Grünsteingürtel (Grönland)", "val": 3700},
      {"name": "Pilbara-Kraton (Australien)", "val": 3500},
      {"name": "Barberton Greenstone Belt (Südafrika)", "val": 3400},
      {"name": "Fennoskandischer Schild (Finnland)", "val": 3100},
      {"name": "Schwarzwald-Gneis (Deutschland)", "val": 380},
      {"name": "Jurakalk (Süddeutschland)", "val": 150}
    ]
  },
  "geo_schluchten_tiefe": {
    "prompt": "Welche Schlucht ist tiefer?",
    "unit": "m (Tiefe)",
    "items": [
      {"name": "Kali Gandaki Gorge (Nepal)", "val": 5571},
      {"name": "Cotahuasi Canyon (Peru)", "val": 3535},
      {"name": "Colca Canyon (Peru)", "val": 3270},
      {"name": "Grand Canyon (USA)", "val": 1857},
      {"name": "Blyde River Canyon (Südafrika)", "val": 800},
      {"name": "Verdon-Schlucht (Frankreich)", "val": 700},
      {"name": "Fish River Canyon (Namibia)", "val": 550},
      {"name": "Rheindurchbruch (Deutschland)", "val": 130}
    ]
  },
  "geo_kontinentaldrift": {
    "prompt": "Welche Platte driftet schneller?",
    "unit": "mm/Jahr (Driftgeschwindigkeit)",
    "items": [
      {"name": "Pazifische Platte", "val": 75},
      {"name": "Australisch-Indische Platte", "val": 70},
      {"name": "Nazca-Platte", "val": 70},
      {"name": "Juan-de-Fuca-Platte", "val": 40},
      {"name": "Arabische Platte", "val": 25},
      {"name": "Nordamerikanische Platte", "val": 23},
      {"name": "Eurasische Platte", "val": 21},
      {"name": "Antarktische Platte", "val": 15}
    ]
  },
  "geo_schmelztemperatur": {
    "prompt": "Welches Material hat einen höheren Schmelzpunkt?",
    "unit": "°C (Schmelzpunkt)",
    "items": [
      {"name": "Olivin (Mineral)", "val": 1890},
      {"name": "Reines SiO₂ (Quarz)", "val": 1650},
      {"name": "Eisen (Fe)", "val": 1538},
      {"name": "Basalt (Gestein)", "val": 1150},
      {"name": "Kalkstein (CaCO₃, Zersetzung)", "val": 840},
      {"name": "Granit (beginnt zu schmelzen)", "val": 700},
      {"name": "Schwefel", "val": 119},
      {"name": "Eis", "val": 0}
    ]
  },
  "geo_gletscher_volumen": {
    "prompt": "Welches Eisvorkommen hat größeres Volumen?",
    "unit": "km³ (Eisvolumen)",
    "items": [
      {"name": "Antarktisches Eisschild", "val": 26500000},
      {"name": "Grönländisches Eisschild", "val": 2850000},
      {"name": "Kanadische Arktis (gesamt)", "val": 150000},
      {"name": "Alaska-Gletscher (gesamt)", "val": 75000},
      {"name": "Patagonische Eisfelder", "val": 13000},
      {"name": "Svalbard (gesamt)", "val": 6700},
      {"name": "Alpengletscher (gesamt)", "val": 100},
      {"name": "Aletschgletscher", "val": 15}
    ]
  },
  "geo_tsunami_hoehe": {
    "prompt": "Welcher Tsunami war höher?",
    "unit": "m (maximale Wellenhöhe)",
    "items": [
      {"name": "Lituya Bay 1958 (Alaska, Mega-Tsunami)", "val": 524},
      {"name": "Alaska 1964 (Good Friday)", "val": 67},
      {"name": "Tohoku 2011 (Japan)", "val": 40},
      {"name": "Chile 1960 (Valdivia)", "val": 25},
      {"name": "Indischer Ozean 2004", "val": 30},
      {"name": "Papua-Neuguinea 1998", "val": 15},
      {"name": "Anak Krakatau 2018", "val": 13},
      {"name": "Sulawesi 2018 (Palu)", "val": 10}
    ]
  },
  "geo_bohrtiefe": {
    "prompt": "Welche Bohrung / Mine reicht tiefer?",
    "unit": "m (Tiefe unter Erdoberfläche)",
    "items": [
      {"name": "Kola Superdeep Borehole (Russland)", "val": 12262},
      {"name": "KTB Kontinentale Tiefbohrung (Deutschland)", "val": 9101},
      {"name": "Bertha-Rogers-Gasbohrung (Oklahoma, USA)", "val": 9583},
      {"name": "Mponeng Gold Mine (Südafrika)", "val": 4000},
      {"name": "TauTona Mine (Südafrika)", "val": 3900},
      {"name": "Gotthard-Basistunnel (tiefster Punkt)", "val": 2300},
      {"name": "Wieliczka Salzmine (Polen)", "val": 327},
      {"name": "Bergwerk Prosper-Haniel (Ruhrgebiet, DE)", "val": 1250}
    ]
  }
}

NEW_MATCH = {
  "geo_vulkan_land": {
    "prompt": "In welchem Land liegt dieser Vulkan?",
    "items": [
      {"n": "Ätna", "c": "Italien"},
      {"n": "Kilauea", "c": "USA (Hawaii)"},
      {"n": "Fuji", "c": "Japan"},
      {"n": "Cotopaxi", "c": "Ecuador"},
      {"n": "Popocatépetl", "c": "Mexiko"},
      {"n": "Nyiragongo", "c": "DR Kongo"},
      {"n": "Erebus", "c": "Antarktis"},
      {"n": "Merapi", "c": "Indonesien"}
    ]
  },
  "geo_berg_gebirge": {
    "prompt": "Zu welchem Gebirge gehört dieser Berg?",
    "items": [
      {"n": "Matterhorn", "c": "Alpen"},
      {"n": "Mount Everest", "c": "Himalaya"},
      {"n": "Aconcagua", "c": "Anden"},
      {"n": "Denali", "c": "Alaska Range"},
      {"n": "Elbrus", "c": "Kaukasus"},
      {"n": "Kilimandscharo", "c": "Ostafrikanisches Massiv"},
      {"n": "Puncak Jaya", "c": "Maoke-Gebirge (Neuguinea)"},
      {"n": "Vinson Massif", "c": "Ellsworth Mountains (Antarktis)"}
    ]
  },
  "geo_wunder_entstehung": {
    "prompt": "Durch welchen Prozess entstand dieses Naturwunder hauptsächlich?",
    "items": [
      {"n": "Grand Canyon", "c": "Flusserosion"},
      {"n": "Giant's Causeway (Nordirland)", "c": "Vulkanismus (Basaltlava)"},
      {"n": "Marianengraben", "c": "Plattentektonik (Subduktion)"},
      {"n": "Moränenlandschaft (z.B. Norddeutsche Tiefebene)", "c": "Glaziale Erosion"},
      {"n": "Saharadünen", "c": "Äolische Sedimentation (Wind)"},
      {"n": "Tropfsteinhöhle (z.B. Eisriesenwelt)", "c": "Karst (chemische Auflösung)"},
      {"n": "Fjord (z.B. Geirangerfjord)", "c": "Glaziale Erosion"},
      {"n": "Atoll (z.B. Bikini-Atoll)", "c": "Korallenriff auf sinkender Vulkaninsel"}
    ]
  },
  "geo_fossil_zeitalter": {
    "prompt": "In welchem Erdzeitalter lebte dieses Wesen?",
    "items": [
      {"n": "Trilobit", "c": "Paläozoikum"},
      {"n": "Archaeopteryx", "c": "Mesozoikum"},
      {"n": "Mammut", "c": "Känozoikum"},
      {"n": "Stromatolithen (Cyanobakterien)", "c": "Präkambrium"},
      {"n": "Tyrannosaurus rex", "c": "Mesozoikum"},
      {"n": "Ammonit", "c": "Mesozoikum"},
      {"n": "Säbelzahntiger (Smilodon)", "c": "Känozoikum"},
      {"n": "Seelilienfossil (Kambrium)", "c": "Paläozoikum"}
    ]
  },
  "geo_erdbeben_jahr": {
    "prompt": "In welchem Jahr ereignete sich dieses historische Erdbeben?",
    "items": [
      {"n": "Lissabon-Erdbeben (Portugal)", "c": "1755"},
      {"n": "San-Francisco-Erdbeben (USA)", "c": "1906"},
      {"n": "Messina-Erdbeben (Sizilien)", "c": "1908"},
      {"n": "Valdivia-Erdbeben (Chile)", "c": "1960"},
      {"n": "Kobe-Erdbeben (Japan)", "c": "1995"},
      {"n": "Haiti-Erdbeben", "c": "2010"},
      {"n": "Tohoku-Erdbeben (Japan)", "c": "2011"},
      {"n": "Türkei-Syrien-Erdbeben", "c": "2023"}
    ]
  },
  "geo_gestein_nutzung": {
    "prompt": "Wofür wird dieses Gestein / Mineral hauptsächlich genutzt?",
    "items": [
      {"n": "Marmor", "c": "Bildhauerei & Architektur"},
      {"n": "Granit", "c": "Bauplatten & Küchen"},
      {"n": "Schiefer", "c": "Dachbedeckung"},
      {"n": "Kalkstein", "c": "Zementherstellung"},
      {"n": "Basalt", "c": "Straßenbau & Gleisbett"},
      {"n": "Kohle", "c": "Energiegewinnung"},
      {"n": "Obsidian", "c": "Historische Werkzeuge (Messer/Spitzen)"},
      {"n": "Kreide", "c": "Tafelkreide & Malerfarben"}
    ]
  },
  "geo_landschaft_ursprung": {
    "prompt": "Welcher Prozess hat diese Landschaftsform erschaffen?",
    "items": [
      {"n": "Moräne", "c": "Gletscher-Transport"},
      {"n": "Delta", "c": "Flusssedimentation"},
      {"n": "Fjord", "c": "Glaziale Erosion"},
      {"n": "Mäander", "c": "Flusserosion"},
      {"n": "Doline", "c": "Karstauflösung"},
      {"n": "Barchan-Düne", "c": "Windablagerung (Äolisch)"},
      {"n": "Heiße Quelle / Fumarole", "c": "Geothermalaufstieg"},
      {"n": "Atollring", "c": "Korallenriff & Vulkansenkung"}
    ]
  },
  "geo_mineral_farbe": {
    "prompt": "Welche charakteristische Farbe hat dieses Mineral?",
    "items": [
      {"n": "Malachit", "c": "Grün"},
      {"n": "Lapislazuli", "c": "Blau"},
      {"n": "Hämatit", "c": "Rot / Rotbraun"},
      {"n": "Schwefel", "c": "Gelb"},
      {"n": "Magnetit", "c": "Schwarz"},
      {"n": "Rhodonit", "c": "Rosa"},
      {"n": "Amethyst", "c": "Violett"},
      {"n": "Türkis", "c": "Türkis / Blaugrün"}
    ]
  },
  "geo_kontinent_platte": {
    "prompt": "Auf welcher tektonischen Hauptplatte liegt dieser Kontinent / diese Region?",
    "items": [
      {"n": "Westeuropa", "c": "Eurasische Platte"},
      {"n": "Nordamerika", "c": "Nordamerikanische Platte"},
      {"n": "Südamerika", "c": "Südamerikanische Platte"},
      {"n": "Afrika", "c": "Afrikanische Platte"},
      {"n": "Australien", "c": "Australische Platte"},
      {"n": "Antarktis", "c": "Antarktische Platte"},
      {"n": "Indien (Subkontinent)", "c": "Indisch-Australische Platte"},
      {"n": "Arabische Halbinsel", "c": "Arabische Platte"}
    ]
  },
  "geo_hoehlen_land": {
    "prompt": "In welchem Land liegt dieses Höhlensystem?",
    "items": [
      {"n": "Mammoth Cave System", "c": "USA"},
      {"n": "Son Doong", "c": "Vietnam"},
      {"n": "Sistema Ox Bel Ha", "c": "Mexiko"},
      {"n": "Eisriesenwelt", "c": "Österreich"},
      {"n": "Carlsbad Caverns", "c": "USA"},
      {"n": "Jenolan Caves", "c": "Australien"},
      {"n": "Škocjan-Höhlen", "c": "Slowenien"},
      {"n": "Reed Flute Cave", "c": "China"}
    ]
  },
  "geo_mineral_kristall": {
    "prompt": "Welchem Kristallsystem gehört dieses Mineral an?",
    "items": [
      {"n": "Halit (Steinsalz)", "c": "Kubisch"},
      {"n": "Diamant", "c": "Kubisch"},
      {"n": "Quarz", "c": "Trigonal / Hexagonal"},
      {"n": "Turmalin", "c": "Trigonal / Hexagonal"},
      {"n": "Topas", "c": "Orthorhombisch"},
      {"n": "Glimmer (Muskovit)", "c": "Monoklin"},
      {"n": "Gips", "c": "Monoklin"},
      {"n": "Feldspat (Albit)", "c": "Triklin"}
    ]
  },
  "geo_gebirge_entstehung": {
    "prompt": "Durch welchen tektonischen Prozess entstand dieses Gebirge?",
    "items": [
      {"n": "Alpen", "c": "Kontinent-Kontinent-Kollision"},
      {"n": "Himalaya", "c": "Kontinent-Kontinent-Kollision"},
      {"n": "Anden", "c": "Ozean-Kontinent-Subduktion"},
      {"n": "Mittelatlantischer Rücken / Island", "c": "Mittelozeanischer Rücken (Rifting)"},
      {"n": "Appalachen (USA)", "c": "Alt-Kollision (Variszisch)"},
      {"n": "Ural (Russland)", "c": "Alt-Kollision (Variszisch)"},
      {"n": "Ostafrikanischer Graben", "c": "Rift-Tektonik (Dehnung)"},
      {"n": "Hawaiianische Inseln", "c": "Hotspot-Vulkanismus"}
    ]
  }
}

NEW_WS = {
  "tropfstein": {
    "word": "TROPFSTEIN",
    "validWords": {
      "de": ["STEIN", "FROST", "TROST", "SPORT", "STERN", "TROPEN", "PROST", "PROFIS"],
      "en": ["STONE", "FRONT", "FROST", "NOTES", "SPORT", "PRINT", "STRIP", "SPINE", "SNIPE"]
    }
  },
  "magmakammer": {
    "word": "MAGMAKAMMER",
    "validWords": {
      "de": ["MAGMA", "KAMMER", "KAMERA", "KARMA", "GRAM", "MARKE", "KARGE", "KRAM", "ARME"],
      "en": ["MAKER", "KARMA", "GAME", "MARK", "MARE", "MAKE", "GRAM", "MAGE", "RAKE"]
    }
  },
  "kontinent": {
    "word": "KONTINENT",
    "validWords": {
      "de": ["TONNE", "TONNEN", "NOTEN", "KNOTEN", "NOTE", "INTENT", "TOKEN"],
      "en": ["TOKEN", "KNOT", "NOTE", "TONE", "NEON", "TENT", "INTENT", "TONIC"]
    }
  },
  "fossilien": {
    "word": "FOSSILIEN",
    "validWords": {
      "de": ["FOSSIL", "INSEL", "SILO", "LINSE", "FOLIE", "FIEL"],
      "en": ["FOSSIL", "LION", "SOIL", "ISLE", "NOISE", "LINES", "FELONS", "LOIN"]
    }
  },
  "erdkruste": {
    "word": "ERDKRUSTE",
    "validWords": {
      "de": ["DURST", "TREU", "KURS", "RUDE", "DUSTER"],
      "en": ["DUSK", "DESK", "RUDE", "DUSTER", "STUD", "TREK", "RUDEST", "DRUSE"]
    }
  },
  "mineralien": {
    "word": "MINERALIEN",
    "validWords": {
      "de": ["MINERAL", "LINEAR", "MARINE", "LINIE", "MANIE", "EINER", "ALIEN"],
      "en": ["MINERAL", "LINEAR", "MARINE", "ALIEN", "LINER", "RAIN", "LANE", "MENIAL", "REALM"]
    }
  }
}

# ══════════════════════════════════════════════════════════════════════════════
# 2. WRITE JSON FILES
# ══════════════════════════════════════════════════════════════════════════════
def merge_and_write(path, new_data):
    existing = json.loads(path.read_text(encoding="utf-8"))
    overwrites = [k for k in new_data if k in existing]
    if overwrites:
        print(f"  [idempotent] {path.name}: ueberschreibe {len(overwrites)} bestehende Keys (Re-Run)")
    existing.update(new_data)
    path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    added = len([k for k in new_data if k not in overwrites])
    print(f"  OK {path.name}: +{added} neu, {len(overwrites)} aktualisiert ({len(existing)} total)")

print("── Schreibe JSON-Daten ──────────────────────────────────────────────────")
merge_and_write(DATA / "geo_pin.json",   NEW_PIN)
merge_and_write(DATA / "geo_hl.json",    NEW_HL)
merge_and_write(DATA / "geo_match.json", NEW_MATCH)
merge_and_write(DATA / "geo_ws.json",    NEW_WS)

# ══════════════════════════════════════════════════════════════════════════════
# 3. WS LETTER VALIDATION
# ══════════════════════════════════════════════════════════════════════════════
print("── WS-Buchstabenvalidierung ─────────────────────────────────────────────")
# Step 1: Filter out any words that don't fit the letter pool (auto-fix)
for key, entry in NEW_WS.items():
    base = Counter(entry["word"])
    for lang in list(entry["validWords"]):
        before = entry["validWords"][lang]
        filtered = [w for w in before
                    if all(Counter(w)[ch] <= base[ch] for ch in Counter(w))]
        removed = set(before) - set(filtered)
        if removed:
            print(f"  [auto-filter] {key}/{lang}: entfernt {sorted(removed)}")
        entry["validWords"][lang] = filtered

# Step 2: Validate — after filtering, nothing invalid should remain
errors = []
for key, entry in NEW_WS.items():
    base = Counter(entry["word"])
    for lang, words in entry["validWords"].items():
        for w in words:
            needed = Counter(w)
            for ch, cnt in needed.items():
                if base[ch] < cnt:
                    errors.append(f"  [{key}/{lang}] '{w}' braucht {cnt}x'{ch}', Basis '{entry['word']}' hat nur {base[ch]}x")

if errors:
    print("  FEHLER:")
    for e in errors:
        print(e)
    import sys; sys.exit(1)
else:
    print("  ✓ Alle WS-Wörter buchstabenvalid")

# Re-write geo_ws.json with filtered validWords
existing_ws = json.loads((DATA / "geo_ws.json").read_text(encoding="utf-8"))
for key, entry in NEW_WS.items():
    existing_ws[key] = entry
(DATA / "geo_ws.json").write_text(json.dumps(existing_ws, ensure_ascii=False, indent=2), encoding="utf-8")
print("  ✓ geo_ws.json nach Filter neu geschrieben")

# ══════════════════════════════════════════════════════════════════════════════
# 4. PATCH gen.py
# ══════════════════════════════════════════════════════════════════════════════
print("── Patch gen.py ─────────────────────────────────────────────────────────")
c = GEN.read_text(encoding="utf-8")
orig_len = len(c)

# ── Step A: MODES ─────────────────────────────────────────────────────────────
OLD_MODES = '  /* === Phase 243b: Sport-Wissen === */'
NEW_MODES_BLOCK = (
    '  /* === Phase 253: Geologie Expansion — 40 neue Modi === */\n'
    # ── Pin ──
    '  {id:"uk_geo_felsformationen",icon:"\\u{1FAA8}",title:"Felsformationen weltweit",group:"geologie",prompt:"Wo liegt diese berühmte Felsformation?",desc:"Uluru, Giant\'s Causeway, Kappadokien & mehr"},\n'
    '  {id:"uk_geo_hoehlensysteme",icon:"\\u{1F30C}",title:"Höhlensysteme orten",group:"geologie",prompt:"Wo liegt dieses Höhlensystem?",desc:"Mammoth Cave, Son Doong, Eisriesenwelt"},\n'
    '  {id:"uk_geo_canyons",icon:"\\u26F0\\uFE0F",title:"Canyons & Schluchten",group:"geologie",prompt:"Wo liegt diese Schlucht / dieser Canyon?",desc:"Grand Canyon, Colca Canyon, Antelope Canyon"},\n'
    '  {id:"uk_geo_geysire",icon:"\\u{1F4A7}",title:"Geysire orten",group:"geologie",prompt:"Wo liegt dieser Geysir?",desc:"El Tatio, Fly Geyser, Steamboat, Pohutu"},\n'
    '  {id:"uk_geo_fossilien_fundstaetten",icon:"\\u{1F9B4}",title:"Fossilien-Fundstätten",group:"geologie",prompt:"Wo liegt diese Fossilien-Fundstätte?",desc:"Jurassic Coast, Grube Messel, Burgess Shale"},\n'
    '  {id:"uk_geo_ozeangraeben",icon:"\\u{1F30A}",title:"Ozeangraben-Standorte",group:"geologie",prompt:"Wo liegt dieser Ozeangraben?",desc:"Marianengraben, Tongagraben, Puerto-Rico-Graben"},\n'
    '  {id:"uk_geo_gletscher",icon:"\\u2744\\uFE0F",title:"Gletscher orten",group:"geologie",prompt:"Wo liegt dieser Gletscher?",desc:"Aletsch, Perito Moreno, Athabasca & mehr"},\n'
    '  {id:"uk_geo_wuesten",icon:"\\u{1F3DC}\\uFE0F",title:"Wüsten & Dünenlandschaften",group:"geologie",prompt:"Wo liegt diese Wüste?",desc:"Namib, Atacama, Rub\' al Khali, Taklamakan"},\n'
    '  {id:"uk_geo_minen_bohrungen",icon:"\\u26CF\\uFE0F",title:"Minen & Tiefbohrungen",group:"geologie",prompt:"Wo liegt diese Mine oder dieses Bohrprojekt?",desc:"Kola Borehole, Bingham Canyon, Mir-Diamantmine"},\n'
    '  {id:"uk_geo_rifts",icon:"\\u{1F30D}",title:"Tektonische Gräben & Rifts",group:"geologie",prompt:"Wo liegt dieser tektonische Graben?",desc:"Ostafrikanischer Graben, Silfra, Baikal-Rift"},\n'
    '  {id:"uk_geo_nationalparks_geologie",icon:"\\u{1F333}",title:"Geologische Nationalparks",group:"geologie",prompt:"Wo liegt dieser geologisch bedeutsame Park?",desc:"Yellowstone, Pamukkale, Tsingy, Plitvice"},\n'
    '  {id:"uk_geo_steilkuesten",icon:"\\u{1F30A}",title:"Steilküsten & Klippen",group:"geologie",prompt:"Wo befinden sich diese Steilküsten?",desc:"Cliffs of Moher, White Cliffs, Bunda Cliffs"},\n'
    # ── HL ──
    '  {id:"hl_geo_mohshaerte",icon:"\\u{1F48E}",title:"H/L: Mohs-Härte",group:"geologie",prompt:"Welches Mineral ist härter?",desc:"Höher/Niedriger: Mohs-Härteskala 1–10"},\n'
    '  {id:"hl_geo_vei_ausbruch",icon:"\\u{1F30B}",title:"H/L: Vulkan-Explosivität",group:"geologie",prompt:"Welcher Ausbruch war explosiver (VEI)?",desc:"Höher/Niedriger: Volcanic Explosivity Index"},\n'
    '  {id:"hl_geo_hoehlen_laenge",icon:"\\u{1F30C}",title:"H/L: Höhlenlänge",group:"geologie",prompt:"Welches Höhlensystem ist länger?",desc:"Höher/Niedriger: kartierte Länge in km"},\n'
    '  {id:"hl_geo_gesteins_alter",icon:"\\u{1FAA8}",title:"H/L: Gesteinsalter",group:"geologie",prompt:"Welches Gestein ist älter?",desc:"Höher/Niedriger: Alter in Millionen Jahren"},\n'
    '  {id:"hl_geo_schluchten_tiefe",icon:"\\u26F0\\uFE0F",title:"H/L: Schluchten-Tiefe",group:"geologie",prompt:"Welche Schlucht ist tiefer?",desc:"Höher/Niedriger: Tiefe in Metern"},\n'
    '  {id:"hl_geo_kontinentaldrift",icon:"\\u{1F30D}",title:"H/L: Kontinentaldrift",group:"geologie",prompt:"Welche Platte driftet schneller?",desc:"Höher/Niedriger: Driftgeschwindigkeit mm/Jahr"},\n'
    '  {id:"hl_geo_schmelztemperatur",icon:"\\u{1F525}",title:"H/L: Schmelztemperatur",group:"geologie",prompt:"Welches Material hat höheren Schmelzpunkt?",desc:"Höher/Niedriger: Temperatur in °C"},\n'
    '  {id:"hl_geo_gletscher_volumen",icon:"\\u2744\\uFE0F",title:"H/L: Gletschervolumen",group:"geologie",prompt:"Welches Eisvorkommen hat mehr Volumen?",desc:"Höher/Niedriger: km³ Eis"},\n'
    '  {id:"hl_geo_tsunami_hoehe",icon:"\\u{1F30A}",title:"H/L: Tsunami-Höhe",group:"geologie",prompt:"Welcher Tsunami war höher?",desc:"Höher/Niedriger: maximale Wellenhöhe in Metern"},\n'
    '  {id:"hl_geo_bohrtiefe",icon:"\\u26CF\\uFE0F",title:"H/L: Bohrtiefe",group:"geologie",prompt:"Welche Bohrung / Mine reicht tiefer?",desc:"Höher/Niedriger: Tiefe in Metern"},\n'
    # ── Match ──
    '  {id:"uk_geo_vulkan_land",icon:"\\u{1F30B}",title:"Vulkan-Länder zuordnen",group:"geologie",prompt:"In welchem Land liegt dieser Vulkan?",desc:"Ätna, Kilauea, Fuji & mehr"},\n'
    '  {id:"uk_geo_berg_gebirge",icon:"\\u26F0\\uFE0F",title:"Berg zum Gebirge",group:"geologie",prompt:"Zu welchem Gebirge gehört dieser Berg?",desc:"Matterhorn→Alpen, Everest→Himalaya"},\n'
    '  {id:"uk_geo_wunder_entstehung",icon:"\\u{1F30D}",title:"Naturwunder & Entstehung",group:"geologie",prompt:"Durch welchen Prozess entstand dieses Naturwunder?",desc:"Erosion, Vulkanismus, Gletscher oder Tektonik"},\n'
    '  {id:"uk_geo_fossil_zeitalter",icon:"\\u{1F9B4}",title:"Fossilien & Erdzeitalter",group:"geologie",prompt:"In welchem Erdzeitalter lebte dieses Wesen?",desc:"Präkambrium, Paläozoikum, Mesozoikum, Känozoikum"},\n'
    '  {id:"uk_geo_erdbeben_jahr",icon:"\\u{1F30D}",title:"Historische Erdbeben",group:"geologie",prompt:"In welchem Jahr ereignete sich dieses Erdbeben?",desc:"Lissabon 1755 bis Türkei-Syrien 2023"},\n'
    '  {id:"uk_geo_gestein_nutzung",icon:"\\u{1FAA8}",title:"Gestein & Nutzung",group:"geologie",prompt:"Wofür wird dieses Gestein hauptsächlich genutzt?",desc:"Marmor, Schiefer, Basalt & ihre Anwendungen"},\n'
    '  {id:"uk_geo_landschaft_ursprung",icon:"\\u{1F3DD}\\uFE0F",title:"Landschaftsformen & Ursprung",group:"geologie",prompt:"Durch welchen Prozess entstand diese Landschaftsform?",desc:"Gletscher, Fluss, Wind, Karst oder Geothermal"},\n'
    '  {id:"uk_geo_mineral_farbe",icon:"\\u{1F48E}",title:"Mineral-Farben",group:"geologie",prompt:"Welche charakteristische Farbe hat dieses Mineral?",desc:"Malachit, Lapislazuli, Amethyst & Co."},\n'
    '  {id:"uk_geo_kontinent_platte",icon:"\\u{1F30D}",title:"Kontinente & Platten",group:"geologie",prompt:"Auf welcher tektonischen Platte liegt diese Region?",desc:"Eurasisch, Pazifisch, Afrikanisch & mehr"},\n'
    '  {id:"uk_geo_hoehlen_land",icon:"\\u{1F30C}",title:"Höhlensystem → Land",group:"geologie",prompt:"In welchem Land liegt dieses Höhlensystem?",desc:"Von Mammoth Cave bis Son Doong"},\n'
    '  {id:"uk_geo_mineral_kristall",icon:"\\u{1F52C}",title:"Mineral-Kristallsysteme",group:"geologie",prompt:"Welchem Kristallsystem gehört dieses Mineral an?",desc:"Kubisch, Hexagonal, Monoklin, Triklin"},\n'
    '  {id:"uk_geo_gebirge_entstehung",icon:"\\u26F0\\uFE0F",title:"Gebirge & Entstehung",group:"geologie",prompt:"Durch welchen Prozess entstand dieses Gebirge?",desc:"Kollision, Subduktion, Rift oder Hotspot"},\n'
    # ── WS ──
    '  {id:"ws_geo_tropfstein",icon:"\\u{1FAA8}",title:"WS: Tropfstein",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus TROPFSTEIN!",desc:"Anagramm-Rätsel — 10 Buchstaben"},\n'
    '  {id:"ws_geo_magmakammer",icon:"\\u{1F30B}",title:"WS: Magmakammer",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus MAGMAKAMMER!",desc:"Anagramm-Rätsel — 11 Buchstaben"},\n'
    '  {id:"ws_geo_kontinent",icon:"\\u{1F30D}",title:"WS: Kontinent",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus KONTINENT!",desc:"Anagramm-Rätsel — 9 Buchstaben"},\n'
    '  {id:"ws_geo_fossilien",icon:"\\u{1F9B4}",title:"WS: Fossilien",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus FOSSILIEN!",desc:"Anagramm-Rätsel — 9 Buchstaben"},\n'
    '  {id:"ws_geo_erdkruste",icon:"\\u{1FAA8}",title:"WS: Erdkruste",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus ERDKRUSTE!",desc:"Anagramm-Rätsel — 9 Buchstaben"},\n'
    '  {id:"ws_geo_mineralien",icon:"\\u{1F48E}",title:"WS: Mineralien",group:"geologie",noMultiplayer:true,prompt:"Bilde Wörter aus MINERALIEN!",desc:"Anagramm-Rätsel — 10 Buchstaben"},\n'
    '  /* === Phase 243b: Sport-Wissen === */'
)
assert c.count(OLD_MODES) == 1, f"Anchor nicht eindeutig: {OLD_MODES!r}"
c = c.replace(OLD_MODES, NEW_MODES_BLOCK, 1)
print("  ✓ Step A: 40 MODES-Einträge eingefügt")

# ── Step B: MODE_CATS geo.modes erweitern ─────────────────────────────────────
OLD_CATS = (
    '"ws_geo_stalaktiten","ws_geo_vulkanismus","ws_geo_erdbeben"\n'
    '  ],cost:0},\n'
    '  sport_wissen:'
)
NEW_CATS = (
    '"ws_geo_stalaktiten","ws_geo_vulkanismus","ws_geo_erdbeben",\n'
    '    "uk_geo_felsformationen","uk_geo_hoehlensysteme","uk_geo_canyons","uk_geo_geysire",\n'
    '    "uk_geo_fossilien_fundstaetten","uk_geo_ozeangraeben","uk_geo_gletscher","uk_geo_wuesten",\n'
    '    "uk_geo_minen_bohrungen","uk_geo_rifts","uk_geo_nationalparks_geologie","uk_geo_steilkuesten",\n'
    '    "hl_geo_mohshaerte","hl_geo_vei_ausbruch","hl_geo_hoehlen_laenge","hl_geo_gesteins_alter",\n'
    '    "hl_geo_schluchten_tiefe","hl_geo_kontinentaldrift","hl_geo_schmelztemperatur","hl_geo_gletscher_volumen",\n'
    '    "hl_geo_tsunami_hoehe","hl_geo_bohrtiefe",\n'
    '    "uk_geo_vulkan_land","uk_geo_berg_gebirge","uk_geo_wunder_entstehung","uk_geo_fossil_zeitalter",\n'
    '    "uk_geo_erdbeben_jahr","uk_geo_gestein_nutzung","uk_geo_landschaft_ursprung","uk_geo_mineral_farbe",\n'
    '    "uk_geo_kontinent_platte","uk_geo_hoehlen_land","uk_geo_mineral_kristall","uk_geo_gebirge_entstehung",\n'
    '    "ws_geo_tropfstein","ws_geo_magmakammer","ws_geo_kontinent","ws_geo_fossilien",\n'
    '    "ws_geo_erdkruste","ws_geo_mineralien"\n'
    '  ],cost:0},\n'
    '  sport_wissen:'
)
assert c.count(OLD_CATS) == 1, f"Anchor nicht eindeutig (MODE_CATS): {OLD_CATS!r}"
c = c.replace(OLD_CATS, NEW_CATS, 1)
print("  ✓ Step B: MODE_CATS geologie.modes erweitert (+40 IDs)")

# ── Step C: GEN dispatch ──────────────────────────────────────────────────────
OLD_GEN = (
    '  ws_geo_erdbeben:()=>{initGeoWS("erdbeben");return null;},\n'
    '  /* Phase 243: Sport-Wissen */'
)
NEW_GEN = (
    '  ws_geo_erdbeben:()=>{initGeoWS("erdbeben");return null;},\n'
    '  /* Phase 253: Geologie Expansion */\n'
    '  uk_geo_felsformationen:()=>genGeoPinQ("geo_felsformationen"),\n'
    '  uk_geo_hoehlensysteme:()=>genGeoPinQ("geo_hoehlensysteme"),\n'
    '  uk_geo_canyons:()=>genGeoPinQ("geo_canyons"),\n'
    '  uk_geo_geysire:()=>genGeoPinQ("geo_geysire"),\n'
    '  uk_geo_fossilien_fundstaetten:()=>genGeoPinQ("geo_fossilien_fundstaetten"),\n'
    '  uk_geo_ozeangraeben:()=>genGeoPinQ("geo_ozeangraeben"),\n'
    '  uk_geo_gletscher:()=>genGeoPinQ("geo_gletscher"),\n'
    '  uk_geo_wuesten:()=>genGeoPinQ("geo_wuesten"),\n'
    '  uk_geo_minen_bohrungen:()=>genGeoPinQ("geo_minen_bohrungen"),\n'
    '  uk_geo_rifts:()=>genGeoPinQ("geo_rifts"),\n'
    '  uk_geo_nationalparks_geologie:()=>genGeoPinQ("geo_nationalparks_geologie"),\n'
    '  uk_geo_steilkuesten:()=>genGeoPinQ("geo_steilkuesten"),\n'
    '  hl_geo_mohshaerte:()=>genGeoHL("geo_mohshaerte"),\n'
    '  hl_geo_vei_ausbruch:()=>genGeoHL("geo_vei_ausbruch"),\n'
    '  hl_geo_hoehlen_laenge:()=>genGeoHL("geo_hoehlen_laenge"),\n'
    '  hl_geo_gesteins_alter:()=>genGeoHL("geo_gesteins_alter"),\n'
    '  hl_geo_schluchten_tiefe:()=>genGeoHL("geo_schluchten_tiefe"),\n'
    '  hl_geo_kontinentaldrift:()=>genGeoHL("geo_kontinentaldrift"),\n'
    '  hl_geo_schmelztemperatur:()=>genGeoHL("geo_schmelztemperatur"),\n'
    '  hl_geo_gletscher_volumen:()=>genGeoHL("geo_gletscher_volumen"),\n'
    '  hl_geo_tsunami_hoehe:()=>genGeoHL("geo_tsunami_hoehe"),\n'
    '  hl_geo_bohrtiefe:()=>genGeoHL("geo_bohrtiefe"),\n'
    '  uk_geo_vulkan_land:()=>genGeoMatchQ("geo_vulkan_land"),\n'
    '  uk_geo_berg_gebirge:()=>genGeoMatchQ("geo_berg_gebirge"),\n'
    '  uk_geo_wunder_entstehung:()=>genGeoMatchQ("geo_wunder_entstehung"),\n'
    '  uk_geo_fossil_zeitalter:()=>genGeoMatchQ("geo_fossil_zeitalter"),\n'
    '  uk_geo_erdbeben_jahr:()=>genGeoMatchQ("geo_erdbeben_jahr"),\n'
    '  uk_geo_gestein_nutzung:()=>genGeoMatchQ("geo_gestein_nutzung"),\n'
    '  uk_geo_landschaft_ursprung:()=>genGeoMatchQ("geo_landschaft_ursprung"),\n'
    '  uk_geo_mineral_farbe:()=>genGeoMatchQ("geo_mineral_farbe"),\n'
    '  uk_geo_kontinent_platte:()=>genGeoMatchQ("geo_kontinent_platte"),\n'
    '  uk_geo_hoehlen_land:()=>genGeoMatchQ("geo_hoehlen_land"),\n'
    '  uk_geo_mineral_kristall:()=>genGeoMatchQ("geo_mineral_kristall"),\n'
    '  uk_geo_gebirge_entstehung:()=>genGeoMatchQ("geo_gebirge_entstehung"),\n'
    '  ws_geo_tropfstein:()=>{initGeoWS("tropfstein");return null;},\n'
    '  ws_geo_magmakammer:()=>{initGeoWS("magmakammer");return null;},\n'
    '  ws_geo_kontinent:()=>{initGeoWS("kontinent");return null;},\n'
    '  ws_geo_fossilien:()=>{initGeoWS("fossilien");return null;},\n'
    '  ws_geo_erdkruste:()=>{initGeoWS("erdkruste");return null;},\n'
    '  ws_geo_mineralien:()=>{initGeoWS("mineralien");return null;},\n'
    '  /* Phase 243: Sport-Wissen */'
)
assert c.count(OLD_GEN) == 1, f"Anchor nicht eindeutig (GEN): {OLD_GEN!r}"
c = c.replace(OLD_GEN, NEW_GEN, 1)
print("  OK Step C: GEN dispatch um 40 Eintraege erweitert")

GEN.write_text(c, encoding="utf-8")
print(f"  OK gen.py geschrieben ({orig_len} -> {len(c)} bytes, Delta={len(c)-orig_len:+d})")
print("\nOK patch_253_geo_expansion.py FERTIG")
 encoding="utf-8")
print(f"  OK gen.py geschrieben ({orig_len} -> {len(c)} bytes, Delta={len(c)-orig_len:+d})")
print("\nOK patch_253_geo_expansion.py FERTIG")
