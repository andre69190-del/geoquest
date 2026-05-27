"""
Phase: 252
Date:  2026-05-27
Author: Claude / Andre
Scope: Astronomie & Raumfahrt — Massiver Content-Ausbau: 17 neue Modi.

Description:
  Erweitert die vier data/astro_*.json Dateien um hochqualitative Inhalte
  und registriert 17 neue Spielmodi in gen.py (MODES + MODE_CATS + GEN).

  astro_pin.json  (+4 Kategorien):
    astro_esa_nasa_zentren, astro_weltraumteleskope,
    astro_meteoritenkrater, astro_dark_sky

  astro_hl.json   (+6 Kategorien):
    astro_raketen_nutzlast, astro_missionsdauer, astro_schwerkraft,
    astro_temperaturen, astro_entdeckungsjahr, astro_exoplaneten_distanz

  astro_match.json (+6 Kategorien):
    astro_sonden_ziele, astro_himmelskoerper_typ, astro_sternbilder_himmel,
    astro_pioniere, astro_antriebe, astro_galaxien_typen

  astro_ws.json   (+1 Eintrag):
    schwarzesloch

Dependencies: patch_243_new_worlds.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import json, pathlib, sys

ROOT = pathlib.Path(__file__).parent.parent
DATA = ROOT / "data"
GEN  = ROOT / "gen.py"

# ══════════════════════════════════════════════════════════════════════════════
# 1. JSON DATA
# ══════════════════════════════════════════════════════════════════════════════

# ── astro_pin.json ────────────────────────────────────────────────────────────
NEW_PIN = {
  "astro_esa_nasa_zentren": {
    "prompt": "Wo liegt dieses Raumfahrtkontrollzentrum?",
    "items": [
      {"n": "Johnson Space Center (Houston, Texas)", "lat": 29.56, "lng": -95.09},
      {"n": "ESOC Darmstadt (ESA Missionskontrolle)", "lat": 49.87, "lng": 8.62},
      {"n": "JPL Pasadena (NASA Jet Propulsion Lab)", "lat": 34.20, "lng": -118.18},
      {"n": "ESTEC Noordwijk (ESA Technikzentrum)", "lat": 52.22, "lng": 4.43},
      {"n": "JAXA Sagamihara Space Operations Center", "lat": 35.55, "lng": 139.49},
      {"n": "Goddard Space Flight Center (Maryland)", "lat": 39.00, "lng": -76.87},
      {"n": "ISRO Headquarters (Bangalore, Indien)", "lat": 12.96, "lng": 77.57},
      {"n": "European Space Astronomy Centre (Madrid)", "lat": 40.44, "lng": -3.95}
    ]
  },
  "astro_weltraumteleskope": {
    "prompt": "Wo befindet sich dieses Teleskop oder Observatorium?",
    "items": [
      {"n": "FAST Radioteleskop (Guizhou, China)", "lat": 25.65, "lng": 106.86},
      {"n": "VLA Very Large Array (New Mexico, USA)", "lat": 34.08, "lng": -107.62},
      {"n": "ELT Extremely Large Telescope (Cerro Armazones, Chile)", "lat": -24.59, "lng": -70.19},
      {"n": "Square Kilometre Array SKA (Karoo, Südafrika)", "lat": -30.71, "lng": 21.44},
      {"n": "South African Large Telescope SALT", "lat": -32.38, "lng": 20.81},
      {"n": "McDonald Observatory (Texas, USA)", "lat": 30.68, "lng": -104.02},
      {"n": "Palomar Observatory (Kalifornien, USA)", "lat": 33.36, "lng": -116.86},
      {"n": "Lowell Observatory (Flagstaff, Arizona)", "lat": 35.20, "lng": -111.66}
    ]
  },
  "astro_meteoritenkrater": {
    "prompt": "Wo liegt dieser Meteoritenkrater?",
    "items": [
      {"n": "Chicxulub-Krater (Yucatán, Mexiko)", "lat": 21.40, "lng": -89.50},
      {"n": "Vredefort-Krater (Südafrika)", "lat": -27.00, "lng": 27.50},
      {"n": "Nördlinger Ries (Bayern, Deutschland)", "lat": 48.88, "lng": 10.59},
      {"n": "Barringer Meteor Crater (Arizona, USA)", "lat": 35.03, "lng": -111.02},
      {"n": "Manicouagan-Krater (Québec, Kanada)", "lat": 51.38, "lng": -68.70},
      {"n": "Popigai-Krater (Sibirien, Russland)", "lat": 71.64, "lng": 111.40},
      {"n": "Acraman-Krater (Südaustralien)", "lat": -32.02, "lng": 135.45},
      {"n": "Sudbury Basin (Ontario, Kanada)", "lat": 46.60, "lng": -81.18}
    ]
  },
  "astro_dark_sky": {
    "prompt": "Wo liegt dieses Dark-Sky-Reservat?",
    "items": [
      {"n": "NamibRand Nature Reserve (Namibia)", "lat": -25.18, "lng": 16.05},
      {"n": "Aoraki Mackenzie Dark Sky Reserve (Neuseeland)", "lat": -43.90, "lng": 170.70},
      {"n": "Kerry Dark Sky Reserve (Irland)", "lat": 52.00, "lng": -9.75},
      {"n": "Galloway Forest Park Dark Sky Park (Schottland)", "lat": 55.14, "lng": -4.36},
      {"n": "Mont-Mégantic Observatory (Québec, Kanada)", "lat": 45.45, "lng": -71.15},
      {"n": "Westhavelland Sternenpark (Brandenburg, DE)", "lat": 52.70, "lng": 12.15},
      {"n": "Big Bend Dark Sky Reserve (Texas, USA)", "lat": 29.25, "lng": -103.25},
      {"n": "Zselic Starry Sky Park (Ungarn)", "lat": 46.18, "lng": 17.85}
    ]
  }
}

# ── astro_hl.json ─────────────────────────────────────────────────────────────
NEW_HL = {
  "astro_raketen_nutzlast": {
    "prompt": "Welche Rakete transportiert mehr Nutzlast in die Erdumlaufbahn (LEO)?",
    "unit": "t (Nutzlast LEO)",
    "items": [
      {"name": "Saturn V (NASA, 1967)", "val": 140},
      {"name": "SLS Block 1 (NASA, 2022)", "val": 95},
      {"name": "Falcon Heavy (SpaceX)", "val": 64},
      {"name": "Long March 5 (CNSA)", "val": 25},
      {"name": "Falcon 9 Block 5 (SpaceX)", "val": 23},
      {"name": "Delta IV Heavy (ULA)", "val": 29},
      {"name": "Ariane 5 ECA (ESA)", "val": 21},
      {"name": "Soyuz-2.1b (Roskosmos)", "val": 9}
    ]
  },
  "astro_missionsdauer": {
    "prompt": "Welche Raumsonde / welches Teleskop war länger im Betrieb?",
    "unit": "Tage (Betrieb bis 2026)",
    "items": [
      {"name": "Voyager 1 (NASA, seit 1977)", "val": 17785},
      {"name": "Voyager 2 (NASA, seit 1977)", "val": 17728},
      {"name": "Hubble-Weltraumteleskop (seit 1990)", "val": 13150},
      {"name": "Mars Reconnaissance Orbiter (seit 2006)", "val": 7300},
      {"name": "Cassini (1997–2017)", "val": 7285},
      {"name": "New Horizons (seit 2006)", "val": 7350},
      {"name": "Opportunity Rover (2004–2018)", "val": 5352},
      {"name": "Curiosity Rover (seit 2012)", "val": 5000}
    ]
  },
  "astro_schwerkraft": {
    "prompt": "Welcher Himmelskörper hat die stärkere Oberflächengravitation?",
    "unit": "m/s²",
    "items": [
      {"name": "Jupiter", "val": 24.79},
      {"name": "Neptun", "val": 11.15},
      {"name": "Saturn", "val": 10.44},
      {"name": "Erde", "val": 9.81},
      {"name": "Uranus", "val": 8.87},
      {"name": "Venus", "val": 8.87},
      {"name": "Mars", "val": 3.72},
      {"name": "Mond", "val": 1.62},
      {"name": "Pluto", "val": 0.62}
    ]
  },
  "astro_temperaturen": {
    "prompt": "Welcher Planet ist durchschnittlich heißer (Oberflächentemperatur)?",
    "unit": "°C (Durchschnitt)",
    "items": [
      {"name": "Venus", "val": 465},
      {"name": "Merkur (Durchschnitt)", "val": 167},
      {"name": "Erde", "val": 15},
      {"name": "Mars", "val": -63},
      {"name": "Jupiter (Wolkenoberseite)", "val": -108},
      {"name": "Saturn (Wolkenoberseite)", "val": -138},
      {"name": "Uranus", "val": -195},
      {"name": "Neptun", "val": -200}
    ]
  },
  "astro_entdeckungsjahr": {
    "prompt": "Welches Objekt wurde früher entdeckt?",
    "unit": "Jahr der Entdeckung",
    "items": [
      {"name": "Io (Galileo Galilei)", "val": 1610},
      {"name": "Europa (Galileo Galilei)", "val": 1610},
      {"name": "Titan (Christiaan Huygens)", "val": 1655},
      {"name": "Uranus (William Herschel)", "val": 1781},
      {"name": "Ceres (Giuseppe Piazzi)", "val": 1801},
      {"name": "Neptun (Le Verrier / Adams)", "val": 1846},
      {"name": "Pluto (Clyde Tombaugh)", "val": 1930},
      {"name": "Charon (James Christy)", "val": 1978}
    ]
  },
  "astro_exoplaneten_distanz": {
    "prompt": "Welcher Exoplanet ist weiter von der Erde entfernt?",
    "unit": "Lichtjahre",
    "items": [
      {"name": "Proxima Centauri b", "val": 4.24},
      {"name": "Alpha Centauri Bb", "val": 4.37},
      {"name": "Gliese 667C c", "val": 23.6},
      {"name": "TRAPPIST-1e", "val": 39.5},
      {"name": "GJ 1214 b", "val": 42.0},
      {"name": "51 Pegasi b (Helvetios)", "val": 50.9},
      {"name": "HD 209458 b (Osiris)", "val": 154.0},
      {"name": "Kepler-452b", "val": 1400.0}
    ]
  }
}

# ── astro_match.json ──────────────────────────────────────────────────────────
NEW_MATCH = {
  "astro_sonden_ziele": {
    "prompt": "Welches Ziel hat diese Raumsonde angesteuert?",
    "items": [
      {"n": "Curiosity Rover", "c": "Mars"},
      {"n": "InSight Lander", "c": "Mars"},
      {"n": "Cassini-Huygens", "c": "Saturn"},
      {"n": "Juno", "c": "Jupiter"},
      {"n": "New Horizons", "c": "Pluto / Kuiper-Gürtel"},
      {"n": "MESSENGER", "c": "Merkur"},
      {"n": "Dawn", "c": "Asteroiden (Ceres/Vesta)"},
      {"n": "Hayabusa2 (JAXA)", "c": "Asteroid Ryugu"},
      {"n": "OSIRIS-REx (NASA)", "c": "Asteroid Bennu"},
      {"n": "Voyager 1", "c": "Interstellarer Raum"}
    ]
  },
  "astro_himmelskoerper_typ": {
    "prompt": "Zu welchem Typ gehört dieser Himmelskörper?",
    "items": [
      {"n": "Jupiter", "c": "Planet (Gasriese)"},
      {"n": "Sonne", "c": "Stern"},
      {"n": "Andromeda-Galaxie (M31)", "c": "Galaxie"},
      {"n": "Titan", "c": "Mond"},
      {"n": "Pluto", "c": "Zwergplanet"},
      {"n": "Io", "c": "Mond"},
      {"n": "Sirius", "c": "Stern"},
      {"n": "Ceres", "c": "Zwergplanet"},
      {"n": "Halleyscher Komet", "c": "Komet"},
      {"n": "Makemake", "c": "Zwergplanet"}
    ]
  },
  "astro_sternbilder_himmel": {
    "prompt": "Zu welchem Sternenhimmel gehört dieses Sternbild hauptsächlich?",
    "items": [
      {"n": "Kassiopeia", "c": "Nordhimmel"},
      {"n": "Großer Bär (Ursa Major)", "c": "Nordhimmel"},
      {"n": "Kleiner Bär (Polarstern)", "c": "Nordhimmel"},
      {"n": "Kreuz des Südens (Crux)", "c": "Südhimmel"},
      {"n": "Zentaur (Centaurus)", "c": "Südhimmel"},
      {"n": "Toucan (Tucana)", "c": "Südhimmel"},
      {"n": "Orion", "c": "Äquatorbereich"},
      {"n": "Widder (Aries)", "c": "Äquatorbereich"},
      {"n": "Pegasus", "c": "Nordhimmel"},
      {"n": "Skorpion (Scorpius)", "c": "Südhimmel"}
    ]
  },
  "astro_pioniere": {
    "prompt": "Für welche Entdeckung oder welches Gesetz ist dieser Astronom bekannt?",
    "items": [
      {"n": "Galileo Galilei", "c": "Entdeckung der Jupiter-Monde"},
      {"n": "Johannes Kepler", "c": "Keplersche Planetengesetze"},
      {"n": "Isaac Newton", "c": "Universelles Gravitationsgesetz"},
      {"n": "Nikolaus Kopernikus", "c": "Heliozentrisches Weltbild"},
      {"n": "Edwin Hubble", "c": "Universum expandiert (Hubble-Gesetz)"},
      {"n": "Vera Rubin", "c": "Nachweis Dunkler Materie"},
      {"n": "Stephen Hawking", "c": "Hawking-Strahlung schwarzer Löcher"},
      {"n": "Cecilia Payne-Gaposchkin", "c": "Sterne bestehen hauptsächlich aus Wasserstoff"}
    ]
  },
  "astro_antriebe": {
    "prompt": "Welche Antriebsart nutzt diese Rakete oder Raumsonde?",
    "items": [
      {"n": "Saturn V (1. Stufe — F-1-Triebwerk)", "c": "Kerosin/Flüssigsauerstoff"},
      {"n": "Falcon 9 (Merlin-Triebwerk)", "c": "Kerosin/Flüssigsauerstoff"},
      {"n": "SLS (Kernstufe — RS-25)", "c": "Kryogen (LH2/LOX)"},
      {"n": "Ariane 5 (Vulcain-Hauptstufe)", "c": "Kryogen (LH2/LOX)"},
      {"n": "Space Shuttle SRB", "c": "Feststofftreibstoff"},
      {"n": "Titan IV B (Booster)", "c": "Feststofftreibstoff"},
      {"n": "Dawn (NASA-Sonde)", "c": "Ionenantrieb"},
      {"n": "Deep Space 1 (NASA-Sonde)", "c": "Ionenantrieb"}
    ]
  },
  "astro_galaxien_typen": {
    "prompt": "Welchem Galaxientyp gehört diese Galaxie an?",
    "items": [
      {"n": "Andromeda-Galaxie (M31)", "c": "Spiralgalaxie"},
      {"n": "Feuerwerksgalaxie (NGC 6946)", "c": "Spiralgalaxie"},
      {"n": "Milchstraße", "c": "Balkenspirale"},
      {"n": "NGC 1300", "c": "Balkenspirale"},
      {"n": "Messier 87 (M87)", "c": "Elliptische Galaxie"},
      {"n": "NGC 1052", "c": "Elliptische Galaxie"},
      {"n": "Große Magellansche Wolke", "c": "Irreguläre Galaxie"},
      {"n": "Kleine Magellansche Wolke", "c": "Irreguläre Galaxie"}
    ]
  }
}

# ── astro_ws.json ─────────────────────────────────────────────────────────────
NEW_WS = {
  "schwarzesloch": {
    "word": "SCHWARZESLOCH",
    "validWords": {
      "de": [
        "SCHWARZ",
        "SCHACH",
        "SCHAL",
        "SCHALE",
        "LASCHE",
        "ARCHE",
        "LACHS",
        "WACHE",
        "CHAOS",
        "WALZE",
        "HARSCH",
        "LOCH"
      ],
      "en": [
        "SCHOLAR",
        "CRASH",
        "CLASH",
        "CRAWLS",
        "CHORAL",
        "HARSH",
        "SHOAL",
        "LARCH",
        "CHARS",
        "CAROL",
        "CLAW",
        "HAZE"
      ]
    }
  }
}

# ══════════════════════════════════════════════════════════════════════════════
# 2. WRITE JSON FILES
# ══════════════════════════════════════════════════════════════════════════════
def merge_and_write(path: pathlib.Path, new_data: dict):
    existing = json.loads(path.read_text(encoding="utf-8"))
    for k, v in new_data.items():
        assert k not in existing, f"Key collision — '{k}' already exists in {path.name}!"
    existing.update(new_data)
    path.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  ✓ {path.name}: +{len(new_data)} Kategorien ({len(existing)} total)")

print("── Schreibe JSON-Daten ──────────────────────────────────────────────────")
merge_and_write(DATA / "astro_pin.json",   NEW_PIN)
merge_and_write(DATA / "astro_hl.json",    NEW_HL)
merge_and_write(DATA / "astro_match.json", NEW_MATCH)
merge_and_write(DATA / "astro_ws.json",    NEW_WS)

# ══════════════════════════════════════════════════════════════════════════════
# 3. PATCH gen.py
# ══════════════════════════════════════════════════════════════════════════════
print("── Patch gen.py ─────────────────────────────────────────────────────────")
c = GEN.read_text(encoding="utf-8")
original_len = len(c)

# ── Step A: Insert 17 new MODES entries before the Geologie comment ──────────
OLD_MODES = '  /* === Phase 243b: Geologie === */'
NEW_MODES_BLOCK = (
    '  /* === Phase 252: Astronomie Expansion — 17 neue Modi === */\n'
    # ── Pin ──
    '  {id:"uk_astro_esa_nasa_zentren",icon:"\\u{1F6F0}\\uFE0F",title:"Kontrollzentren & Raumfahrtbehörden",group:"astronomie",prompt:"Wo liegt dieses Raumfahrtkontrollzentrum?",desc:"JSC, ESOC, JPL, Goddard und mehr"},\n'
    '  {id:"uk_astro_weltraumteleskope",icon:"\\u{1F52D}",title:"Teleskop-Standorte weltweit",group:"astronomie",prompt:"Wo befindet sich dieses Teleskop?",desc:"FAST, VLA, ELT, SALT und weitere Riesen"},\n'
    '  {id:"uk_astro_meteoritenkrater",icon:"\\u2604\\uFE0F",title:"Meteoritenkrater orten",group:"astronomie",prompt:"Wo liegt dieser Meteoritenkrater?",desc:"Chicxulub, Nördlinger Ries, Vredefort"},\n'
    '  {id:"uk_astro_dark_sky",icon:"\\u2728",title:"Dark-Sky-Reservate",group:"astronomie",prompt:"Wo liegt dieses Dark-Sky-Reservat?",desc:"Die dunkelsten Nächte unserer Erde"},\n'
    # ── HL ──
    '  {id:"hl_astro_raketen_nutzlast",icon:"\\u{1F680}",title:"H/L: Raketen-Nutzlast",group:"astronomie",prompt:"Welche Rakete trägt mehr Nutzlast in den LEO?",desc:"Höher/Niedriger: Nutzlast in Tonnen"},\n'
    '  {id:"hl_astro_missionsdauer",icon:"\\u23F3",title:"H/L: Missionsdauer",group:"astronomie",prompt:"Welche Mission/Sonde war länger aktiv?",desc:"Höher/Niedriger: Betriebstage"},\n'
    '  {id:"hl_astro_schwerkraft",icon:"\\u{1FA90}",title:"H/L: Oberflächengravitation",group:"astronomie",prompt:"Welcher Himmelskörper hat stärkere Gravitation?",desc:"Höher/Niedriger: m/s²"},\n'
    '  {id:"hl_astro_temperaturen",icon:"\\u{1F321}\\uFE0F",title:"H/L: Oberflächentemperatur",group:"astronomie",prompt:"Welcher Planet ist durchschnittlich wärmer?",desc:"Höher/Niedriger: Celsius"},\n'
    '  {id:"hl_astro_entdeckungsjahr",icon:"\\u{1F52D}",title:"H/L: Entdeckungsjahr",group:"astronomie",prompt:"Welches Objekt wurde früher entdeckt?",desc:"Höher/Niedriger: Jahr der Erstentdeckung"},\n'
    '  {id:"hl_astro_exoplaneten_distanz",icon:"\\u{1F30C}",title:"H/L: Exoplaneten-Distanz",group:"astronomie",prompt:"Welcher Exoplanet ist weiter entfernt?",desc:"Höher/Niedriger: Entfernung in Lichtjahren"},\n'
    # ── Match ──
    '  {id:"uk_astro_sonden_ziele",icon:"\\u{1F6F8}",title:"Raumsonden & Ziele",group:"astronomie",prompt:"Welches Ziel hat diese Raumsonde angesteuert?",desc:"Curiosity, Cassini, Juno & Co."},\n'
    '  {id:"uk_astro_himmelskoerper_typ",icon:"\\u{1FA90}",title:"Himmelskörper-Typen",group:"astronomie",prompt:"Zu welchem Typ gehört dieser Himmelskörper?",desc:"Planet, Mond, Stern, Galaxie oder Zwergplanet?"},\n'
    '  {id:"uk_astro_sternbilder_himmel",icon:"\\u2B50",title:"Sternbilder zuordnen",group:"astronomie",prompt:"Zu welchem Sternenhimmel gehört dieses Sternbild?",desc:"Nord- oder Südhimmel oder Äquatorbereich?"},\n'
    '  {id:"uk_astro_pioniere",icon:"\\u{1F9D1}\\u200D\\u{1F52C}",title:"Astronomie-Pioniere",group:"astronomie",prompt:"Für welche Entdeckung ist dieser Wissenschaftler bekannt?",desc:"Kopernikus, Hubble, Vera Rubin & mehr"},\n'
    '  {id:"uk_astro_antriebe",icon:"\\u{1F525}",title:"Raketenantriebe",group:"astronomie",prompt:"Welche Antriebsart nutzt diese Rakete?",desc:"Kerosin, Kryogen, Feststoff oder Ionenantrieb"},\n'
    '  {id:"uk_astro_galaxien_typen",icon:"\\u{1F30C}",title:"Galaxien-Typen",group:"astronomie",prompt:"Welchem Galaxientyp gehört diese Galaxie an?",desc:"Spiral, Elliptisch, Balken oder Irregulär"},\n'
    # ── WS ──
    '  {id:"ws_astro_schwarzesloch",icon:"\\u26AB",title:"WS: Schwarzes Loch",group:"astronomie",noMultiplayer:true,prompt:"Bilde Wörter aus SCHWARZESLOCH!",desc:"Anagramm-Rätsel — 13 Buchstaben"},\n'
    '  /* === Phase 243b: Geologie === */'
)
assert c.count(OLD_MODES) == 1, f"Anchor nicht eindeutig: {OLD_MODES!r}"
c = c.replace(OLD_MODES, NEW_MODES_BLOCK, 1)
print("  ✓ Step A: 17 MODES-Einträge eingefügt")

# ── Step B: MODE_CATS — astronomie.modes erweitern ───────────────────────────
OLD_CATS = (
    '"ws_astro_sternwarte","ws_astro_raumstation","ws_astro_astronaut"\n'
    '  ],cost:0},\n'
    '  geologie:'
)
NEW_CATS = (
    '"ws_astro_sternwarte","ws_astro_raumstation","ws_astro_astronaut",\n'
    '    "uk_astro_esa_nasa_zentren","uk_astro_weltraumteleskope","uk_astro_meteoritenkrater","uk_astro_dark_sky",\n'
    '    "hl_astro_raketen_nutzlast","hl_astro_missionsdauer","hl_astro_schwerkraft","hl_astro_temperaturen","hl_astro_entdeckungsjahr","hl_astro_exoplaneten_distanz",\n'
    '    "uk_astro_sonden_ziele","uk_astro_himmelskoerper_typ","uk_astro_sternbilder_himmel","uk_astro_pioniere","uk_astro_antriebe","uk_astro_galaxien_typen",\n'
    '    "ws_astro_schwarzesloch"\n'
    '  ],cost:0},\n'
    '  geologie:'
)
assert c.count(OLD_CATS) == 1, f"Anchor nicht eindeutig (MODE_CATS): {OLD_CATS!r}"
c = c.replace(OLD_CATS, NEW_CATS, 1)
print("  ✓ Step B: MODE_CATS astronomie.modes erweitert (+17 IDs)")

# ── Step C: GEN dispatch-table — 17 neue Einträge ────────────────────────────
OLD_GEN = (
    '  ws_astro_astronaut:()=>{initAstroWS("astronaut");return null;},\n'
    '  /* Phase 243: Geologie */'
)
NEW_GEN = (
    '  ws_astro_astronaut:()=>{initAstroWS("astronaut");return null;},\n'
    '  /* Phase 252: Astronomie Expansion */\n'
    '  uk_astro_esa_nasa_zentren:()=>genAstroPinQ("astro_esa_nasa_zentren"),\n'
    '  uk_astro_weltraumteleskope:()=>genAstroPinQ("astro_weltraumteleskope"),\n'
    '  uk_astro_meteoritenkrater:()=>genAstroPinQ("astro_meteoritenkrater"),\n'
    '  uk_astro_dark_sky:()=>genAstroPinQ("astro_dark_sky"),\n'
    '  hl_astro_raketen_nutzlast:()=>genAstroHL("astro_raketen_nutzlast"),\n'
    '  hl_astro_missionsdauer:()=>genAstroHL("astro_missionsdauer"),\n'
    '  hl_astro_schwerkraft:()=>genAstroHL("astro_schwerkraft"),\n'
    '  hl_astro_temperaturen:()=>genAstroHL("astro_temperaturen"),\n'
    '  hl_astro_entdeckungsjahr:()=>genAstroHL("astro_entdeckungsjahr"),\n'
    '  hl_astro_exoplaneten_distanz:()=>genAstroHL("astro_exoplaneten_distanz"),\n'
    '  uk_astro_sonden_ziele:()=>genAstroMatchQ("astro_sonden_ziele"),\n'
    '  uk_astro_himmelskoerper_typ:()=>genAstroMatchQ("astro_himmelskoerper_typ"),\n'
    '  uk_astro_sternbilder_himmel:()=>genAstroMatchQ("astro_sternbilder_himmel"),\n'
    '  uk_astro_pioniere:()=>genAstroMatchQ("astro_pioniere"),\n'
    '  uk_astro_antriebe:()=>genAstroMatchQ("astro_antriebe"),\n'
    '  uk_astro_galaxien_typen:()=>genAstroMatchQ("astro_galaxien_typen"),\n'
    '  ws_astro_schwarzesloch:()=>{initAstroWS("schwarzesloch");return null;},\n'
    '  /* Phase 243: Geologie */'
)
assert c.count(OLD_GEN) == 1, f"Anchor nicht eindeutig (GEN): {OLD_GEN!r}"
c = c.replace(OLD_GEN, NEW_GEN, 1)
print("  ✓ Step C: GEN dispatch-table um 17 Einträge erweitert")

# ── Write back ────────────────────────────────────────────────────────────────
GEN.write_text(c, encoding="utf-8")
print(f"  ✓ gen.py geschrieben ({original_len} → {len(c)} bytes, Δ={len(c)-original_len:+d})")

# ══════════════════════════════════════════════════════════════════════════════
# 4. VERIFY WS WORD LETTERS (SCHWARZESLOCH)
# ══════════════════════════════════════════════════════════════════════════════
print("── WS-Validierung SCHWARZESLOCH ─────────────────────────────────────────")
from collections import Counter

base = Counter("SCHWARZESLOCH")
errors = []
for lang, words in [("de", NEW_WS["schwarzesloch"]["validWords"]["de"]),
                    ("en", NEW_WS["schwarzesloch"]["validWords"]["en"])]:
    for w in words:
        needed = Counter(w)
        for ch, cnt in needed.items():
            if base[ch] < cnt:
                errors.append(f"  [{lang}] '{w}' braucht {cnt}x'{ch}', Basis hat nur {base[ch]}x")
if errors:
    print("  FEHLER IN WÖRTERN:")
    for e in errors: print(e)
    sys.exit(1)
else:
    print(f"  ✓ Alle {len(NEW_WS['schwarzesloch']['validWords']['de'])} DE + {len(NEW_WS['schwarzesloch']['validWords']['en'])} EN Wörter buchstabenvalid")

print("\n✓ patch_252_astro_expansion.py FERTIG — run_patch.py als nächstes")
