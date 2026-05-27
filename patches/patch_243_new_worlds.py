"""
Phase: 243
Date:  2026-05-27
Author: Claude / Andre
Scope: Die 3 Neuen Welten — Astronomie, Geologie, Sport-Wissen

Description:
  Erstellt 12 neue JSON-Datendateien und integriert sie in gen.py:

  Astronomie (4 Dateien, ~25 Modi):
    astro_pin.json    — Observatorien + Startrampen (2 Pin-Kategorien)
    astro_hl.json     — Planeten-Groesse, Monde-Anzahl, Sonnen-Entfernung
    astro_match.json  — Weltraummissionen, Planeten-Eigenschaften, Kosmologie
    astro_ws.json     — Sternwarte, Raumstation, Astronaut

  Geologie (4 Dateien, ~23 Modi):
    geo_pin.json      — Vulkane + Geothermal-Wunder (2 Pin-Kategorien)
    geo_hl.json       — Berghoehen, Vulkan-Hoehen, Erdbeben-Magnituden
    geo_match.json    — Gesteinsarten, Tektonische Platten, Mineralien
    geo_ws.json       — STALAKTITEN, VULKANISMUS, ERDBEBEN

  Sport-Wissen (4 Dateien, ~22 Modi):
    sport_pin.json    — Olympiastadien + Marathon-Strecken (2 Pin-Kategorien)
    sport_hl.json     — Marathon-Alter, Stadien-Kapazitaet
    sport_match.json  — Sportarten-Herkunft, Spieleranzahl, Olympia-Erstausgabe
    sport_ws.json     — MARATHON, TRIATHLON, STAFFELLAUF

  Verbesserungen gegenueber Spec:
  - Kein Migrieren aus kultur.json (wuerde existierende Modi brechen)
  - String-IDs statt numerischer ID-Bloecke (passt zur GeoQuest-Architektur)
  - sport_wissen als eigene Kategorie (getrennt vom geo-fokussierten 'sport' cat)
  - Alle 3 Kategorien nutzen _mkPinQ/_mkHL/_mkMatchQ/_mkWS Factories

Dependencies: patch_242_engine_animals.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import os, json

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.dirname(HERE)
DATA   = os.path.join(ROOT, 'data')
GEN    = os.path.join(ROOT, 'gen.py')

# ==============================================================================
# STEP 1 — Create all 12 JSON data files
# ==============================================================================

# ── ASTRONOMIE PIN ─────────────────────────────────────────────────────────────
astro_pin = {
  "astro_observatorien": [
    {"n": "Mauna Kea Observatory (Hawaii)", "lat": 19.82, "lng": -155.47},
    {"n": "ALMA (Atacama, Chile)", "lat": -23.02, "lng": -67.75},
    {"n": "La Palma Roque de los Muchachos", "lat": 28.76, "lng": -17.89},
    {"n": "Cerro Paranal ESO (Chile)", "lat": -24.63, "lng": -70.40},
    {"n": "Effelsberg Radioteleskop (Deutschland)", "lat": 50.52, "lng": 6.88},
    {"n": "Jodrell Bank Observatory (England)", "lat": 53.24, "lng": -2.31},
    {"n": "Kitt Peak Observatory (Arizona, USA)", "lat": 31.96, "lng": -111.60},
    {"n": "Parkes Radio Telescope (Australien)", "lat": -32.99, "lng": 148.26}
  ],
  "astro_startrampen": [
    {"n": "Kennedy Space Center (Florida, USA)", "lat": 28.52, "lng": -80.65},
    {"n": "Baikonur Kosmodrom (Kasachstan)", "lat": 45.97, "lng": 63.31},
    {"n": "Guiana Space Centre (Kourou, Frz.-Guyana)", "lat": 5.24, "lng": -52.77},
    {"n": "Tanegashima Space Center (Japan)", "lat": 30.40, "lng": 130.97},
    {"n": "Wenchang Launch Site (China)", "lat": 19.61, "lng": 110.96},
    {"n": "Satish Dhawan Space Centre (Indien)", "lat": 13.73, "lng": 80.23},
    {"n": "Plesetsk Kosmodrom (Russland)", "lat": 62.93, "lng": 40.58},
    {"n": "Vandenberg SFB (Kalifornien, USA)", "lat": 34.74, "lng": -120.57}
  ]
}

# ── ASTRONOMIE HL ──────────────────────────────────────────────────────────────
astro_hl = {
  "astro_planet_groesse": {
    "prompt": "Welcher Planet hat den groesseren Durchmesser?",
    "unit": "km",
    "items": [
      {"name": "Jupiter", "val": 139820},
      {"name": "Saturn", "val": 116460},
      {"name": "Uranus", "val": 50724},
      {"name": "Neptun", "val": 49244},
      {"name": "Erde", "val": 12742},
      {"name": "Venus", "val": 12104},
      {"name": "Mars", "val": 6779},
      {"name": "Merkur", "val": 4879}
    ]
  },
  "astro_monde_anzahl": {
    "prompt": "Welcher Planet hat mehr bekannte Monde?",
    "unit": "Monde",
    "items": [
      {"name": "Saturn", "val": 146},
      {"name": "Jupiter", "val": 95},
      {"name": "Uranus", "val": 28},
      {"name": "Neptun", "val": 16},
      {"name": "Mars", "val": 2},
      {"name": "Erde", "val": 1},
      {"name": "Merkur", "val": 0},
      {"name": "Venus", "val": 0}
    ]
  },
  "astro_sonnenentfernung": {
    "prompt": "Welches Objekt ist weiter von der Sonne entfernt?",
    "unit": "Mio. km",
    "items": [
      {"name": "Neptun", "val": 4495},
      {"name": "Uranus", "val": 2872},
      {"name": "Saturn", "val": 1432},
      {"name": "Jupiter", "val": 778},
      {"name": "Mars", "val": 228},
      {"name": "Erde", "val": 150},
      {"name": "Venus", "val": 108},
      {"name": "Merkur", "val": 58}
    ]
  }
}

# ── ASTRONOMIE MATCH ───────────────────────────────────────────────────────────
astro_match = {
  "astro_missionen": {
    "prompt": "Zu welcher Raumfahrtagentur gehoert diese Mission?",
    "items": [
      {"n": "Apollo 11 (Mondlandung 1969)", "c": "NASA"},
      {"n": "Sputnik 1 (Erster Satellit 1957)", "c": "Sowjetunion/Roskosmos"},
      {"n": "Rosetta/Philae (Komet 67P)", "c": "ESA"},
      {"n": "Chang'e 5 (Mondproben 2020)", "c": "CNSA"},
      {"n": "Mangalyaan (Mars Orbiter 2013)", "c": "ISRO"},
      {"n": "Curiosity Rover (Mars 2012)", "c": "NASA"},
      {"n": "BepiColombo (Merkur-Mission)", "c": "ESA"},
      {"n": "Tianwen-1 (Mars-Rover 2021)", "c": "CNSA"},
      {"n": "Artemis I (Mondprogramm 2022)", "c": "NASA"},
      {"n": "Hayabusa2 (Asteroid 2014)", "c": "JAXA"}
    ]
  },
  "astro_planeten": {
    "prompt": "Welche Eigenschaft beschreibt diesen Planeten am besten?",
    "items": [
      {"n": "Jupiter", "c": "Groesster Planet des Sonnensystems"},
      {"n": "Merkur", "c": "Naechster Planet zur Sonne"},
      {"n": "Venus", "c": "Heissester Planet (Treibhauseffekt)"},
      {"n": "Mars", "c": "Roter Planet mit Phobos und Deimos"},
      {"n": "Saturn", "c": "Planet mit markanten Ringen"},
      {"n": "Uranus", "c": "Rotiert auf der Seite (97 Grad Achsenneigung)"},
      {"n": "Neptun", "c": "Windigster Planet (600 m/s Windgeschwindigkeit)"},
      {"n": "Erde", "c": "Einziger bekannter bewohnter Planet"}
    ]
  },
  "astro_kosmologie": {
    "prompt": "Welche Beschreibung passt zu diesem astronomischen Objekt?",
    "items": [
      {"n": "Schwarzes Loch", "c": "Gravitation so stark, kein Licht entkommt"},
      {"n": "Neutronenstern", "c": "Supernova-Ueberrest, ultra-dichte Materie"},
      {"n": "Pulsar", "c": "Rotierender Neutronenstern sendet Radiopulse"},
      {"n": "Quasar", "c": "Extrem leuchtender aktiver Galaxienkern"},
      {"n": "Supernova", "c": "Explosion eines massereichen Sterns"},
      {"n": "Weisser Zwerg", "c": "Gluehender Kern eines ausgebrannten Sterns"},
      {"n": "Riesenstern (Red Giant)", "c": "Aufgeblasener Stern am Ende seines Lebens"},
      {"n": "Planetarischer Nebel", "c": "Leuchtende Gashuelle um sterbenden Stern"}
    ]
  }
}

# ── ASTRONOMIE WS ──────────────────────────────────────────────────────────────
astro_ws = {
  "sternwarte": {
    "word": "STERNWARTE",
    "validWords": {"de": ["STERN","WARTE","WARTEN","ARTEN","RATEN","ERNST","RENTE","ERNTE","WERT","WARE","WESTEN","ERST","NETTER","RENTE","ANTWERT","RATEN","WATERS"]}
  },
  "raumstation": {
    "word": "RAUMSTATION",
    "validWords": {"de": ["RAUM","RATION","MONAT","TURM","SATURN","TAURIN","STATION","NAOMI","ROMAN"]}
  },
  "astronaut": {
    "word": "ASTRONAUT",
    "validWords": {"de": ["AUTOR","NATUR","SATURN","TARTAN","TRAUT","TURNA","RANT","TAU","ROTAUS"]}
  }
}

# ── GEOLOGIE PIN ───────────────────────────────────────────────────────────────
geo_pin = {
  "geo_vulkane": [
    {"n": "Mauna Loa (Hawaii, USA)", "lat": 19.48, "lng": -155.59},
    {"n": "Etna (Sizilien, Italien)", "lat": 37.75, "lng": 14.99},
    {"n": "Vesuv (Neapel, Italien)", "lat": 40.82, "lng": 14.43},
    {"n": "Krakatau (Indonesien)", "lat": -6.10, "lng": 105.42},
    {"n": "Eyjafjallajokull (Island)", "lat": 63.63, "lng": -19.62},
    {"n": "Popocatepetl (Mexiko)", "lat": 19.02, "lng": -98.63},
    {"n": "Pinatubo (Philippinen)", "lat": 15.14, "lng": 120.35},
    {"n": "Santorini-Caldera (Griechenland)", "lat": 36.40, "lng": 25.40}
  ],
  "geo_geothermal": [
    {"n": "Geysir Strokkur (Island)", "lat": 64.31, "lng": -20.30},
    {"n": "Old Faithful Geysir (Yellowstone, USA)", "lat": 44.46, "lng": -110.83},
    {"n": "Rotorua Geothermalgebiet (Neuseeland)", "lat": -38.14, "lng": 176.25},
    {"n": "Dallol Vulkankrater (Aethiopien)", "lat": 14.24, "lng": 40.30},
    {"n": "Mutnovsky Vulkan (Kamtschatka)", "lat": 52.45, "lng": 158.20},
    {"n": "Taal Vulkansee (Philippinen)", "lat": 14.00, "lng": 120.99},
    {"n": "Myvatn-Gebiet (Island)", "lat": 65.59, "lng": -17.00},
    {"n": "Wai-O-Tapu Thermalwunder (Neuseeland)", "lat": -38.36, "lng": 176.37}
  ]
}

# ── GEOLOGIE HL ────────────────────────────────────────────────────────────────
geo_hl = {
  "geo_berghoehen": {
    "prompt": "Welcher Berg ist hoeher?",
    "unit": "m",
    "items": [
      {"name": "Mount Everest (Nepal/China)", "val": 8849},
      {"name": "K2 (Pakistan/China)", "val": 8611},
      {"name": "Kangchenjunga (Nepal/Indien)", "val": 8586},
      {"name": "Lhotse (Nepal)", "val": 8516},
      {"name": "Aconcagua (Argentinien)", "val": 6961},
      {"name": "Denali / McKinley (USA)", "val": 6190},
      {"name": "Kilimandscharo (Tansania)", "val": 5895},
      {"name": "Mont Blanc (Frankreich/Italien)", "val": 4808}
    ]
  },
  "geo_vulkan_hoehen": {
    "prompt": "Welcher Vulkan hat den hoeheren Gipfel?",
    "unit": "m",
    "items": [
      {"name": "Ojos del Salado (Chile/Argentinien)", "val": 6893},
      {"name": "Llullaillaco (Argentinien)", "val": 6739},
      {"name": "Cotopaxi (Ecuador)", "val": 5897},
      {"name": "Kilimandscharo (Tansania)", "val": 5895},
      {"name": "Popocatepetl (Mexiko)", "val": 5426},
      {"name": "Mount Erebus (Antarktis)", "val": 3794},
      {"name": "Etna (Sizilien, Italien)", "val": 3357},
      {"name": "Vesuv (Italien)", "val": 1281}
    ]
  },
  "geo_erdbeben_magnitude": {
    "prompt": "Welches Erdbeben hatte die groessere Magnitude?",
    "unit": "Richter-Skala",
    "items": [
      {"name": "Valdivia 1960 (Chile)", "val": 95},
      {"name": "Alaska 1964 (USA)", "val": 92},
      {"name": "Tohoku 2011 (Japan)", "val": 91},
      {"name": "Sumatra 2004 (Indonesien)", "val": 91},
      {"name": "Kamtschatka 1952 (Russland)", "val": 90},
      {"name": "Chile 2010", "val": 88},
      {"name": "Haiti 2010", "val": 70},
      {"name": "Kobe 1995 (Japan)", "val": 69}
    ]
  }
}

# ── GEOLOGIE MATCH ─────────────────────────────────────────────────────────────
geo_match = {
  "geo_gesteinsarten": {
    "prompt": "Zu welcher Gesteinsklasse gehoert dieses Gestein?",
    "items": [
      {"n": "Granit", "c": "Magmatisch"},
      {"n": "Marmor", "c": "Metamorph"},
      {"n": "Sandstein", "c": "Sedimentaer"},
      {"n": "Basalt", "c": "Magmatisch"},
      {"n": "Schiefer", "c": "Metamorph"},
      {"n": "Kalkstein", "c": "Sedimentaer"},
      {"n": "Obsidian", "c": "Magmatisch"},
      {"n": "Quarzit", "c": "Metamorph"},
      {"n": "Konglomerat", "c": "Sedimentaer"},
      {"n": "Gneis", "c": "Metamorph"}
    ]
  },
  "geo_tektonik": {
    "prompt": "Auf welcher tektonischen Platte liegt dieses Land hauptsaechlich?",
    "items": [
      {"n": "Deutschland", "c": "Eurasische Platte"},
      {"n": "Australien", "c": "Australische Platte"},
      {"n": "Suedafrika", "c": "Afrikanische Platte"},
      {"n": "Brasilien", "c": "Suedamerikanische Platte"},
      {"n": "Kanada", "c": "Nordamerikanische Platte"},
      {"n": "Indien", "c": "Indische Platte"},
      {"n": "Japan", "c": "Eurasische Platte"},
      {"n": "Neuseeland", "c": "Pazifische Platte"}
    ]
  },
  "geo_mineralien": {
    "prompt": "Wozu wird dieses Mineral oder Gestein hauptsaechlich verwendet?",
    "items": [
      {"n": "Diamant", "c": "Schmuck und Industriewerkzeuge"},
      {"n": "Graphit", "c": "Bleistifte und Batterien"},
      {"n": "Kalzit", "c": "Zement und Kalk"},
      {"n": "Halit (Steinsalz)", "c": "Lebensmittel und Chemie"},
      {"n": "Quarz", "c": "Elektronik und Glas"},
      {"n": "Gips", "c": "Bauwesen und Medizin"},
      {"n": "Magnetit (Eisenerz)", "c": "Stahlproduktion"},
      {"n": "Feldspat", "c": "Keramik und Glasherstellung"}
    ]
  }
}

# ── GEOLOGIE WS ────────────────────────────────────────────────────────────────
geo_ws = {
  "stalaktiten": {
    "word": "STALAKTITEN",
    "validWords": {"de": ["KALT","LATTE","LATTEN","ALTEN","STIEL","ATLAS","TALENT","TINTE","ATTEST","STATT","STIL","ANSTALT","TITLE","ITALIA","TALENT","LATEIN","TAKT","TILTS"]}
  },
  "vulkanismus": {
    "word": "VULKANISMUS",
    "validWords": {"de": ["MUSIK","KLIMA","MAIS","KAUM","MINUS","MAUL","VAKUUM","LAUS","SKLAVIN","KULM","MANIS","KLAUN"]}
  },
  "erdbeben": {
    "word": "ERDBEBEN",
    "validWords": {"de": ["ERDE","BEBEN","REBE","ERBE","EBER","NERD","REDEN","BEENDEN","BENDER"]}
  }
}

# ── SPORT PIN ──────────────────────────────────────────────────────────────────
sport_pin = {
  "sport_olympiastadien": [
    {"n": "Olympiastadion Berlin (1936/2006)", "lat": 52.51, "lng": 13.24},
    {"n": "Stade de France Paris (1998)", "lat": 48.92, "lng": 2.36},
    {"n": "Olympic Stadium Barcelona (1992)", "lat": 41.36, "lng": 2.12},
    {"n": "Athens Olympic Stadium (2004)", "lat": 38.04, "lng": 23.78},
    {"n": "Beijing National Stadium Nest (2008)", "lat": 40.00, "lng": 116.40},
    {"n": "London Olympic Stadium (2012)", "lat": 51.54, "lng": -0.02},
    {"n": "Estadio Maracana Rio (2016)", "lat": -22.91, "lng": -43.23},
    {"n": "Japan National Stadium Tokyo (2021)", "lat": 35.68, "lng": 139.72}
  ],
  "sport_marathonstrecken": [
    {"n": "Boston Marathon Start (Hopkinton, USA)", "lat": 42.23, "lng": -71.52},
    {"n": "NYC Marathon Start (Staten Island, USA)", "lat": 40.60, "lng": -74.07},
    {"n": "Berlin Marathon Start (Charlottenburg)", "lat": 52.52, "lng": 13.29},
    {"n": "London Marathon Start (Greenwich)", "lat": 51.48, "lng": 0.00},
    {"n": "Tokyo Marathon Start (Shinjuku)", "lat": 35.69, "lng": 139.69},
    {"n": "Chicago Marathon Start (Grant Park)", "lat": 41.87, "lng": -87.62},
    {"n": "Wien Marathon Start (Reichsbruecke)", "lat": 48.24, "lng": 16.41},
    {"n": "Sydney Marathon Ziel (Opera House)", "lat": -33.86, "lng": 151.21}
  ]
}

# ── SPORT HL ───────────────────────────────────────────────────────────────────
sport_hl = {
  "sport_marathon_alter": {
    "prompt": "Welcher Marathon hat eine laengere Geschichte?",
    "unit": "Gruendungsjahr",
    "items": [
      {"name": "Boston Marathon (USA)", "val": 1897},
      {"name": "Yonkers Marathon (USA)", "val": 1907},
      {"name": "Kosice Peace Marathon (Slowakei)", "val": 1924},
      {"name": "Fukuoka Marathon (Japan)", "val": 1947},
      {"name": "Berlin Marathon", "val": 1974},
      {"name": "Chicago Marathon", "val": 1977},
      {"name": "New York City Marathon", "val": 1970},
      {"name": "London Marathon", "val": 1981}
    ]
  },
  "sport_stadien_kapazitaet": {
    "prompt": "Welches Stadion fasst mehr Zuschauer?",
    "unit": "Tsd. Plaetze",
    "items": [
      {"name": "Rungrado May Day (Nordkorea)", "val": 114},
      {"name": "Michigan Stadium (USA)", "val": 107},
      {"name": "Beaver Stadium (Penn State, USA)", "val": 107},
      {"name": "Ohio Stadium (USA)", "val": 102},
      {"name": "Melbourne Cricket Ground (Australien)", "val": 100},
      {"name": "Camp Nou (Barcelona, Spanien)", "val": 99},
      {"name": "Wembley Stadium (London)", "val": 90},
      {"name": "Estadio Azteca (Mexiko)", "val": 87}
    ]
  }
}

# ── SPORT MATCH ────────────────────────────────────────────────────────────────
sport_match = {
  "sport_herkunft": {
    "prompt": "In welchem Land oder Region wurde diese Sportart entwickelt?",
    "items": [
      {"n": "Sumo", "c": "Japan"},
      {"n": "Taekwondo", "c": "Korea"},
      {"n": "Cricket", "c": "England"},
      {"n": "Kabaddi", "c": "Indien"},
      {"n": "Sepak Takraw", "c": "Suedostasien"},
      {"n": "Lacrosse", "c": "Nordamerika"},
      {"n": "Polo", "c": "Persien / Zentralasien"},
      {"n": "Capoeira", "c": "Brasilien"},
      {"n": "Pelota Vasca", "c": "Spanien"},
      {"n": "Judo", "c": "Japan"}
    ]
  },
  "sport_teamgroesse": {
    "prompt": "Wie viele Spieler umfasst eine Mannschaft bei diesem Feldsport?",
    "items": [
      {"n": "Fussball", "c": "11 Spieler"},
      {"n": "American Football", "c": "11 Spieler"},
      {"n": "Basketball", "c": "5 Spieler"},
      {"n": "Volleyball", "c": "6 Spieler"},
      {"n": "Rugby Union", "c": "15 Spieler"},
      {"n": "Baseball", "c": "9 Spieler"},
      {"n": "Handball", "c": "7 Spieler"},
      {"n": "Eishockey", "c": "6 Spieler"}
    ]
  },
  "sport_olympia_standort": {
    "prompt": "In welcher Stadt fanden diese Olympischen Sommerspiele statt?",
    "items": [
      {"n": "Erste Neuzeit-Olympiade 1896", "c": "Athen"},
      {"n": "Olympiade 1900", "c": "Paris"},
      {"n": "Olympiade 1936", "c": "Berlin"},
      {"n": "Olympiade 1964", "c": "Tokio"},
      {"n": "Olympiade 1980", "c": "Moskau"},
      {"n": "Olympiade 1992", "c": "Barcelona"},
      {"n": "Olympiade 2008", "c": "Peking"},
      {"n": "Olympiade 2016", "c": "Rio de Janeiro"}
    ]
  }
}

# ── SPORT WS ───────────────────────────────────────────────────────────────────
sport_ws = {
  "marathon": {
    "word": "MARATHON",
    "validWords": {"de": ["MONAT","ROMAN","AHORN","THRON","HORN","RANT","MARAT","MANOR"]}
  },
  "triathlon": {
    "word": "TRIATHLON",
    "validWords": {"de": ["THRON","TRAIL","TRIAL","HALT","HORN","ORAL","TORION","ATHLON"]}
  },
  "staffellauf": {
    "word": "STAFFELLAUF",
    "validWords": {"de": ["STAFF","LAUTE","FLAU","LAUF","FATAL","FALLE","FLAUTE","SAAL","STALL","FALLS","FLUSS","ATLAS","TAFEL"]}
  }
}

# Write all 12 JSON files
files = [
    ("astro_pin.json",   astro_pin),
    ("astro_hl.json",    astro_hl),
    ("astro_match.json", astro_match),
    ("astro_ws.json",    astro_ws),
    ("geo_pin.json",     geo_pin),
    ("geo_hl.json",      geo_hl),
    ("geo_match.json",   geo_match),
    ("geo_ws.json",      geo_ws),
    ("sport_pin.json",   sport_pin),
    ("sport_hl.json",    sport_hl),
    ("sport_match.json", sport_match),
    ("sport_ws.json",    sport_ws),
]
for fname, data in files:
    path = os.path.join(DATA, fname)
    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print(f'  [OK] Created {fname}')

# ==============================================================================
# STEP 2 — Patch gen.py
# ==============================================================================
with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ── 2a: Python load section ────────────────────────────────────────────────────
OLD_LOAD = "with open(os.path.join(os.path.dirname(__file__), 'data/tiere_pin.json'), 'r', encoding='utf-8') as _f: TIER_PIN_J = _f.read()"
NEW_LOAD = OLD_LOAD + """
with open(os.path.join(os.path.dirname(__file__), 'data/astro_pin.json'),   'r', encoding='utf-8') as _f: ASTRO_PIN_J   = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/astro_hl.json'),    'r', encoding='utf-8') as _f: ASTRO_HL_J    = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/astro_match.json'), 'r', encoding='utf-8') as _f: ASTRO_MATCH_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/astro_ws.json'),    'r', encoding='utf-8') as _f: ASTRO_WS_J    = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/geo_pin.json'),     'r', encoding='utf-8') as _f: GEO_PIN_J     = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/geo_hl.json'),      'r', encoding='utf-8') as _f: GEO_HL_J      = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/geo_match.json'),   'r', encoding='utf-8') as _f: GEO_MATCH_J   = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/geo_ws.json'),      'r', encoding='utf-8') as _f: GEO_WS_J      = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/sport_pin.json'),   'r', encoding='utf-8') as _f: SPORT_PIN_J   = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/sport_hl.json'),    'r', encoding='utf-8') as _f: SPORT_HL_J    = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/sport_match.json'), 'r', encoding='utf-8') as _f: SPORT_MATCH_J = _f.read()
with open(os.path.join(os.path.dirname(__file__), 'data/sport_ws.json'),    'r', encoding='utf-8') as _f: SPORT_WS_J    = _f.read()"""
assert c.count(OLD_LOAD) == 1, f'2a anchor not unique ({c.count(OLD_LOAD)})'
c = c.replace(OLD_LOAD, NEW_LOAD, 1)
print('  [OK] 2a: Python load section (12 new files)')

# ── 2b: JS const declarations ─────────────────────────────────────────────────
OLD_CONST = 'const ARCH_WS_DATA=PLACEHOLDER_ARCH_WS;'
NEW_CONST = OLD_CONST + """
const ASTRO_PIN_DATA=PLACEHOLDER_ASTRO_PIN;
const ASTRO_HL_DATA=PLACEHOLDER_ASTRO_HL;
const ASTRO_MATCH_DATA=PLACEHOLDER_ASTRO_MATCH;
const ASTRO_WS_DATA=PLACEHOLDER_ASTRO_WS;
const GEO_PIN_DATA=PLACEHOLDER_GEO_PIN;
const GEO_HL_DATA=PLACEHOLDER_GEO_HL;
const GEO_MATCH_DATA=PLACEHOLDER_GEO_MATCH;
const GEO_WS_DATA=PLACEHOLDER_GEO_WS;
const SPORT_PIN_DATA=PLACEHOLDER_SPORT_PIN;
const SPORT_HL_DATA=PLACEHOLDER_SPORT_HL;
const SPORT_MATCH_DATA=PLACEHOLDER_SPORT_MATCH;
const SPORT_WS_DATA=PLACEHOLDER_SPORT_WS;"""
assert c.count(OLD_CONST) == 1, f'2b anchor not unique ({c.count(OLD_CONST)})'
c = c.replace(OLD_CONST, NEW_CONST, 1)
print('  [OK] 2b: JS const declarations (12 new PLACEHOLDERs)')

# ── 2c: JS factory generator instantiation ────────────────────────────────────
OLD_FACTORY = 'var initArchWS=_mkWS(ARCH_WS_DATA,"Arch");'
NEW_FACTORY = OLD_FACTORY + """
var genAstroPinQ=_mkPinQ(ASTRO_PIN_DATA);
var genAstroHL=_mkHL(ASTRO_HL_DATA);
var genAstroMatchQ=_mkMatchQ(ASTRO_MATCH_DATA);
var initAstroWS=_mkWS(ASTRO_WS_DATA,"Astro");
var genGeoPinQ=_mkPinQ(GEO_PIN_DATA);
var genGeoHL=_mkHL(GEO_HL_DATA);
var genGeoMatchQ=_mkMatchQ(GEO_MATCH_DATA);
var initGeoWS=_mkWS(GEO_WS_DATA,"Geo");
var genSportWissenPinQ=_mkPinQ(SPORT_PIN_DATA);
var genSportWissenHL=_mkHL(SPORT_HL_DATA);
var genSportWissenMatchQ=_mkMatchQ(SPORT_MATCH_DATA);
var initSportWissenWS=_mkWS(SPORT_WS_DATA,"SportW");"""
assert c.count(OLD_FACTORY) == 1, f'2c anchor not unique ({c.count(OLD_FACTORY)})'
c = c.replace(OLD_FACTORY, NEW_FACTORY, 1)
print('  [OK] 2c: JS factory generators (12 new instances)')

# ── 2d: GEN entries ───────────────────────────────────────────────────────────
OLD_GEN = '  ws_arch_radiocarbondatierung:()=>{initArchWS("radiocarbondatierung");return null;},'
NEW_GEN = OLD_GEN + """
  /* Phase 243: Astronomie */
  uk_astro_observatorien:()=>genAstroPinQ("astro_observatorien"),
  uk_astro_startrampen:()=>genAstroPinQ("astro_startrampen"),
  hl_astro_planet_groesse:()=>genAstroHL("astro_planet_groesse"),
  hl_astro_monde_anzahl:()=>genAstroHL("astro_monde_anzahl"),
  hl_astro_sonnenentfernung:()=>genAstroHL("astro_sonnenentfernung"),
  uk_astro_missionen:()=>genAstroMatchQ("astro_missionen"),
  uk_astro_planeten:()=>genAstroMatchQ("astro_planeten"),
  uk_astro_kosmologie:()=>genAstroMatchQ("astro_kosmologie"),
  ws_astro_sternwarte:()=>{initAstroWS("sternwarte");return null;},
  ws_astro_raumstation:()=>{initAstroWS("raumstation");return null;},
  ws_astro_astronaut:()=>{initAstroWS("astronaut");return null;},
  /* Phase 243: Geologie */
  uk_geo_vulkane:()=>genGeoPinQ("geo_vulkane"),
  uk_geo_geothermal:()=>genGeoPinQ("geo_geothermal"),
  hl_geo_berghoehen:()=>genGeoHL("geo_berghoehen"),
  hl_geo_vulkan_hoehen:()=>genGeoHL("geo_vulkan_hoehen"),
  hl_geo_erdbeben:()=>genGeoHL("geo_erdbeben_magnitude"),
  uk_geo_gesteinsarten:()=>genGeoMatchQ("geo_gesteinsarten"),
  uk_geo_tektonik:()=>genGeoMatchQ("geo_tektonik"),
  uk_geo_mineralien:()=>genGeoMatchQ("geo_mineralien"),
  ws_geo_stalaktiten:()=>{initGeoWS("stalaktiten");return null;},
  ws_geo_vulkanismus:()=>{initGeoWS("vulkanismus");return null;},
  ws_geo_erdbeben:()=>{initGeoWS("erdbeben");return null;},
  /* Phase 243: Sport-Wissen */
  uk_sportwissen_olympiastadien:()=>genSportWissenPinQ("sport_olympiastadien"),
  uk_sportwissen_marathonstrecken:()=>genSportWissenPinQ("sport_marathonstrecken"),
  hl_sportwissen_marathon_alter:()=>genSportWissenHL("sport_marathon_alter"),
  hl_sportwissen_stadien_kapazitaet:()=>genSportWissenHL("sport_stadien_kapazitaet"),
  uk_sportwissen_herkunft:()=>genSportWissenMatchQ("sport_herkunft"),
  uk_sportwissen_teamgroesse:()=>genSportWissenMatchQ("sport_teamgroesse"),
  uk_sportwissen_olympia_standort:()=>genSportWissenMatchQ("sport_olympia_standort"),
  ws_sportwissen_marathon:()=>{initSportWissenWS("marathon");return null;},
  ws_sportwissen_triathlon:()=>{initSportWissenWS("triathlon");return null;},
  ws_sportwissen_staffellauf:()=>{initSportWissenWS("staffellauf");return null;},"""
assert c.count(OLD_GEN) == 1, f'2d anchor not unique ({c.count(OLD_GEN)})'
c = c.replace(OLD_GEN, NEW_GEN, 1)
print('  [OK] 2d: GEN entries (30 new modes registered)')

# ── 2e: MODE_CATS new categories ──────────────────────────────────────────────
OLD_CATS = '"ws_arch_radiocarbondatierung"\n  ],cost:0},\n};'
NEW_CATS = ('"ws_arch_radiocarbondatierung"\n  ],cost:0},\n'
'  astronomie:{label:"Astronomie & Raumfahrt",icon:"\\u{1F52D}",modes:[\n'
'    "uk_astro_observatorien","uk_astro_startrampen",\n'
'    "hl_astro_planet_groesse","hl_astro_monde_anzahl","hl_astro_sonnenentfernung",\n'
'    "uk_astro_missionen","uk_astro_planeten","uk_astro_kosmologie",\n'
'    "ws_astro_sternwarte","ws_astro_raumstation","ws_astro_astronaut"\n'
'  ],cost:0},\n'
'  geologie:{label:"Geologie & Vulkane",icon:"\\u{1F30B}",modes:[\n'
'    "uk_geo_vulkane","uk_geo_geothermal",\n'
'    "hl_geo_berghoehen","hl_geo_vulkan_hoehen","hl_geo_erdbeben",\n'
'    "uk_geo_gesteinsarten","uk_geo_tektonik","uk_geo_mineralien",\n'
'    "ws_geo_stalaktiten","ws_geo_vulkanismus","ws_geo_erdbeben"\n'
'  ],cost:0},\n'
'  sport_wissen:{label:"Sport-Wissen",icon:"\\u{1F3C5}",modes:[\n'
'    "uk_sportwissen_olympiastadien","uk_sportwissen_marathonstrecken",\n'
'    "hl_sportwissen_marathon_alter","hl_sportwissen_stadien_kapazitaet",\n'
'    "uk_sportwissen_herkunft","uk_sportwissen_teamgroesse","uk_sportwissen_olympia_standort",\n'
'    "ws_sportwissen_marathon","ws_sportwissen_triathlon","ws_sportwissen_staffellauf"\n'
'  ],cost:0},\n'
'};')
assert c.count(OLD_CATS) == 1, f'2e anchor not unique ({c.count(OLD_CATS)})'
c = c.replace(OLD_CATS, NEW_CATS, 1)
print('  [OK] 2e: MODE_CATS — 3 new categories added (astronomie, geologie, sport_wissen)')

# ── 2f: Python substitution block ─────────────────────────────────────────────
OLD_SUBST = "  .replace('PLACEHOLDER_ARCH_WS', ARCH_WS_J)"
NEW_SUBST = (OLD_SUBST
  + "\n  .replace('PLACEHOLDER_ASTRO_PIN',   ASTRO_PIN_J)"
  + "\n  .replace('PLACEHOLDER_ASTRO_HL',    ASTRO_HL_J)"
  + "\n  .replace('PLACEHOLDER_ASTRO_MATCH', ASTRO_MATCH_J)"
  + "\n  .replace('PLACEHOLDER_ASTRO_WS',    ASTRO_WS_J)"
  + "\n  .replace('PLACEHOLDER_GEO_PIN',     GEO_PIN_J)"
  + "\n  .replace('PLACEHOLDER_GEO_HL',      GEO_HL_J)"
  + "\n  .replace('PLACEHOLDER_GEO_MATCH',   GEO_MATCH_J)"
  + "\n  .replace('PLACEHOLDER_GEO_WS',      GEO_WS_J)"
  + "\n  .replace('PLACEHOLDER_SPORT_PIN',   SPORT_PIN_J)"
  + "\n  .replace('PLACEHOLDER_SPORT_HL',    SPORT_HL_J)"
  + "\n  .replace('PLACEHOLDER_SPORT_MATCH', SPORT_MATCH_J)"
  + "\n  .replace('PLACEHOLDER_SPORT_WS',    SPORT_WS_J)")
assert c.count(OLD_SUBST) == 1, f'2f anchor not unique ({c.count(OLD_SUBST)})'
c = c.replace(OLD_SUBST, NEW_SUBST, 1)
print('  [OK] 2f: Python substitution block (12 new PLACEHOLDERs)')

# ── 2g: _CAT_ORDER update ─────────────────────────────────────────────────────
OLD_ORDER = '"emobilitaet","archaeologie"]'
NEW_ORDER = '"emobilitaet","archaeologie","astronomie","geologie","sport_wissen"]'
assert c.count(OLD_ORDER) == 1, f'2g anchor not unique ({c.count(OLD_ORDER)})'
c = c.replace(OLD_ORDER, NEW_ORDER, 1)
print('  [OK] 2g: _CAT_ORDER updated (3 new categories in nav order)')

# ── Write gen.py ───────────────────────────────────────────────────────────────
with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print()
print('  All Phase 243 fixes applied (12 JSON files + 7 gen.py anchors, ~30 new modes).')
print('  Run: python3 gen.py && python3 verify.py')
