#!/usr/bin/env python3
"""
Phase 260: MASSIVE Astronomie Data Expansion
=============================================
astro_pin.json   — observatorien/startrampen/esa_nasa_zentren/meteoritenkrater → 40-50 Items
astro_hl.json    — raketen_nutzlast/missionsdauer/exoplaneten_distanz/sonnenentfernung → 40-50 Items
                 — monde_anzahl/schwerkraft/temperaturen/entdeckungsjahr → Naturgrenze ~20
astro_match.json — missionen/sonden_ziele/himmelskoerper_typ/sternbilder_himmel
                   pioniere/galaxien_typen/antriebe/kosmologie → 30-60 Items
"""
import json, pathlib

BASE = pathlib.Path("/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest")

def jload(p):  return json.loads(p.read_text(encoding="utf-8"))
def jsave(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

def extend_key(data, key, new_items, name_field="n"):
    block = data[key]
    if isinstance(block, dict):
        existing = block.get("items", [])
    else:
        existing = block
    ex_names = {it.get(name_field,"").lower() for it in existing}
    added = [it for it in new_items if it.get(name_field,"").lower() not in ex_names]
    if isinstance(block, dict):
        block["items"] = existing + added
    else:
        data[key] = existing + added
    return len(added)

# ═══════════════════════════════════════════════════════════════════════════════
# astro_pin.json
# ═══════════════════════════════════════════════════════════════════════════════
pin = jload(BASE / "data/astro_pin.json")

NEW_OBSERVATORIEN = [
    {"n": "Keck Observatory (Mauna Kea, Hawaii)", "lat": 19.83, "lng": -155.47},
    {"n": "Subaru Telescope (Mauna Kea, Hawaii)", "lat": 19.83, "lng": -155.48},
    {"n": "La Silla Observatory ESO (Chile)", "lat": -29.26, "lng": -70.73},
    {"n": "Cerro Tololo CTIO (Chile)", "lat": -30.17, "lng": -70.81},
    {"n": "Gemini South (Cerro Pachón, Chile)", "lat": -30.24, "lng": -70.74},
    {"n": "Apache Point Observatory (New Mexico, USA)", "lat": 32.78, "lng": -105.82},
    {"n": "Lick Observatory (Mount Hamilton, Kalifornien)", "lat": 37.34, "lng": -121.64},
    {"n": "Fred L. Whipple Observatory (Arizona, USA)", "lat": 31.68, "lng": -110.88},
    {"n": "Green Bank Telescope (West Virginia, USA)", "lat": 38.43, "lng": -79.84},
    {"n": "Arecibo Observatory (Puerto Rico) †", "lat": 18.34, "lng": -66.75},
    {"n": "IRAM 30m-Teleskop (Pico Veleta, Spanien)", "lat": 37.07, "lng": -3.39},
    {"n": "Calar Alto Observatory (Andalusien, Spanien)", "lat": 37.22, "lng": -2.55},
    {"n": "Haute-Provence Observatory (Frankreich)", "lat": 43.93, "lng": 5.72},
    {"n": "Special Astrophysical Observatory (Zelenchukskaya, Russland)", "lat": 43.65, "lng": 41.44},
    {"n": "Ratan-600 Radioteleskop (Zelenchukskaya, Russland)", "lat": 43.82, "lng": 41.59},
    {"n": "Byurakan Observatory (Armenien)", "lat": 40.34, "lng": 44.29},
    {"n": "Goldstone Deep Space Complex (Kalifornien, USA)", "lat": 35.43, "lng": -116.89},
    {"n": "Canberra Deep Space Network (Australien)", "lat": -35.4, "lng": 148.98},
    {"n": "Madrid Deep Space Network (Spanien)", "lat": 40.43, "lng": -4.25},
    {"n": "Australia Telescope Compact Array ATCA", "lat": -30.31, "lng": 149.56},
    {"n": "Murchison Widefield Array MWA (Australien)", "lat": -26.70, "lng": 116.67},
    {"n": "Shanghai Astronomical Observatory (China)", "lat": 31.2, "lng": 121.43},
    {"n": "Purple Mountain Observatory (Nanjing, China)", "lat": 32.07, "lng": 118.82},
    {"n": "LIGO Hanford (Washington, USA)", "lat": 46.46, "lng": -119.41},
    {"n": "LIGO Livingston (Louisiana, USA)", "lat": 30.56, "lng": -90.77},
    {"n": "VIRGO Gravitationswellendetektor (Pisa, Italien)", "lat": 43.63, "lng": 10.5},
    {"n": "South Pole Telescope (Amundsen-Scott-Station)", "lat": -90.0, "lng": 0.0},
    {"n": "Indian Astronomical Observatory (Hanle, Indien)", "lat": 32.78, "lng": 78.96},
    {"n": "Atacama Pathfinder Experiment APEX (Chile)", "lat": -23.0, "lng": -67.76},
    {"n": "Ondrejov Observatory (Tschechien)", "lat": 49.91, "lng": 14.78},
    {"n": "Palomar Observatory (Californien, USA)", "lat": 33.36, "lng": -116.86},
    {"n": "Lowell Observatory (Flagstaff, Arizona)", "lat": 35.2, "lng": -111.66},
    {"n": "W.M. Keck Interferometer (Mauna Kea)", "lat": 19.82, "lng": -155.46},
    {"n": "Delingha Radio Telescope (Qinghai, China)", "lat": 37.37, "lng": 97.56},
    {"n": "Haystack Observatory (Massachusetts, USA)", "lat": 42.62, "lng": -71.49},
    {"n": "Uppsala Astronomical Observatory (Schweden)", "lat": 59.86, "lng": 17.63},
]

NEW_STARTRAMPEN = [
    {"n": "SpaceX Starbase (Boca Chica, Texas)", "lat": 25.99, "lng": -97.16},
    {"n": "Wallops Flight Facility (Virginia, USA)", "lat": 37.94, "lng": -75.46},
    {"n": "Mid-Atlantic Regional Spaceport (Virginia, USA)", "lat": 37.84, "lng": -75.49},
    {"n": "Jiuquan Satellite Launch Center (China)", "lat": 40.96, "lng": 100.29},
    {"n": "Xichang Satellite Launch Center (China)", "lat": 28.24, "lng": 102.03},
    {"n": "Taiyuan Satellite Launch Center (China)", "lat": 38.85, "lng": 111.61},
    {"n": "Kapustin Yar (Russland)", "lat": 48.52, "lng": 46.25},
    {"n": "Vostochny Kosmodrom (Russland)", "lat": 51.88, "lng": 128.33},
    {"n": "Yasny Launch Base (Russland)", "lat": 51.21, "lng": 59.85},
    {"n": "Naro Space Center (Südkorea)", "lat": 34.43, "lng": 127.54},
    {"n": "Esrange Space Center (Kiruna, Schweden)", "lat": 67.89, "lng": 21.07},
    {"n": "Andøya Space Center (Norwegen)", "lat": 69.29, "lng": 16.02},
    {"n": "San Marco Platform (Kenia, Indischer Ozean)", "lat": -2.94, "lng": 40.21},
    {"n": "Alcântara Launch Center (Brasilien)", "lat": -2.37, "lng": -44.4},
    {"n": "Pacific Spaceport Complex (Alaska, USA)", "lat": 57.44, "lng": -152.34},
    {"n": "Mojave Air and Space Port (Kalifornien, USA)", "lat": 35.06, "lng": -118.15},
    {"n": "Palmachim Airbase Startgelände (Israel)", "lat": 31.9, "lng": 34.69},
    {"n": "Thumba Equatorial Rocket Station (Indien)", "lat": 8.54, "lng": 76.87},
    {"n": "Cape Canaveral SFS (Florida, USA)", "lat": 28.47, "lng": -80.53},
    {"n": "Dombarovsky Airbase (Russland)", "lat": 51.1, "lng": 59.87},
    {"n": "Kodiak Launch Complex (Alaska, USA)", "lat": 57.44, "lng": -152.34},
    {"n": "Kauai Test Facility (Hawaii, USA)", "lat": 22.04, "lng": -159.77},
    {"n": "Arnhem Space Centre (Australien)", "lat": -12.24, "lng": 136.82},
    {"n": "ISRO Second Launch Pad (Sriharikota)", "lat": 13.72, "lng": 80.24},
    {"n": "Jiuquan Satellite Launch Center LC-4 (China)", "lat": 40.96, "lng": 100.27},
    {"n": "Hammaguira (Algerien, hist.)", "lat": 30.87, "lng": -3.08},
]

NEW_ESA_NASA = [
    {"n": "Marshall Space Flight Center (Huntsville, Alabama)", "lat": 34.72, "lng": -86.65},
    {"n": "Ames Research Center (Moffett Field, Kalifornien)", "lat": 37.41, "lng": -122.06},
    {"n": "Langley Research Center (Hampton, Virginia)", "lat": 37.09, "lng": -76.36},
    {"n": "Glenn Research Center (Cleveland, Ohio)", "lat": 41.42, "lng": -81.86},
    {"n": "Stennis Space Center (Mississippi)", "lat": 30.36, "lng": -89.6},
    {"n": "Armstrong Flight Research Center (Edwards, CA)", "lat": 34.96, "lng": -117.88},
    {"n": "White Sands Test Facility (New Mexico)", "lat": 32.39, "lng": -106.48},
    {"n": "ESRIN (ESA Earth Observation, Frascati, Italien)", "lat": 41.83, "lng": 12.67},
    {"n": "ESA Redu Centre (Belgien)", "lat": 50.0, "lng": 5.14},
    {"n": "CNES Toulouse (Frankreich)", "lat": 43.58, "lng": 1.47},
    {"n": "ASI Hauptquartier Rom (Italien)", "lat": 41.92, "lng": 12.38},
    {"n": "DLR Oberpfaffenhofen (Bayern, Deutschland)", "lat": 48.08, "lng": 11.28},
    {"n": "DLR Berlin-Adlershof (Deutschland)", "lat": 52.43, "lng": 13.53},
    {"n": "CSA Saint-Hubert (Kanada)", "lat": 45.52, "lng": -73.41},
    {"n": "UK Space Agency (Swindon, Großbritannien)", "lat": 51.56, "lng": -1.77},
    {"n": "Roscosmos Hauptquartier (Moskau, Russland)", "lat": 55.75, "lng": 37.62},
    {"n": "CNSA Hauptquartier (Peking, China)", "lat": 39.91, "lng": 116.39},
    {"n": "KARI Korea Aerospace Research Inst. (Daejeon)", "lat": 36.37, "lng": 127.36},
    {"n": "Mohammed bin Rashid Space Centre (Dubai, UAE)", "lat": 25.22, "lng": 55.36},
    {"n": "AEB Brasilianische Raumfahrtagentur (Brasília)", "lat": -15.79, "lng": -47.88},
    {"n": "NASA HQ (Washington D.C.)", "lat": 38.88, "lng": -77.0},
    {"n": "Wallops Command Center (Virginia)", "lat": 37.9, "lng": -75.44},
    {"n": "ESA Space Centre Harwell (Oxford, UK)", "lat": 51.58, "lng": -1.3},
    {"n": "JAXA Tsukuba Space Center (Japan)", "lat": 36.06, "lng": 140.13},
    {"n": "ISRO Satellite Application Centre (Ahmedabad, Indien)", "lat": 23.04, "lng": 72.51},
    {"n": "SpaceX Headquarters (Hawthorne, Kalifornien)", "lat": 33.92, "lng": -118.33},
    {"n": "Blue Origin HQ (Kent, Washington)", "lat": 47.37, "lng": -122.16},
    {"n": "Jet Propulsion Lab (Pasadena) — Deep Space Network HQ", "lat": 34.2, "lng": -118.17},
]

NEW_KRATER = [
    {"n": "Bosumtwi-Krater (Ghana)", "lat": 6.5, "lng": -1.4},
    {"n": "Pingualuit-Krater (Québec, Kanada)", "lat": 61.28, "lng": -73.66},
    {"n": "Siljan-Krater (Schweden)", "lat": 61.02, "lng": 14.9},
    {"n": "Wolf-Creek-Krater (Westaustralien)", "lat": -19.18, "lng": 127.77},
    {"n": "Gosses-Bluff-Krater (Northern Territory, Australien)", "lat": -23.81, "lng": 132.32},
    {"n": "Shoemaker-Krater (Westaustralien)", "lat": -25.87, "lng": 120.89},
    {"n": "Lonar-Kratersee (Maharashtra, Indien)", "lat": 19.98, "lng": 76.51},
    {"n": "Araguainha-Krater (Brasilien)", "lat": -16.78, "lng": -52.99},
    {"n": "Clearwater Lakes (Québec, Kanada)", "lat": 56.22, "lng": -74.5},
    {"n": "Mistastin-Krater (Labrador, Kanada)", "lat": 55.88, "lng": -63.3},
    {"n": "Haughton-Krater (Nunavut, Kanada)", "lat": 75.38, "lng": -89.69},
    {"n": "Kara-Krater (Sibirien, Russland)", "lat": 69.1, "lng": 65.0},
    {"n": "Boltysh-Krater (Ukraine)", "lat": 48.88, "lng": 32.17},
    {"n": "Zhamanshin-Krater (Kasachstan)", "lat": 48.4, "lng": 60.93},
    {"n": "Elgygytgyn-Krater (Tschukotka, Russland)", "lat": 67.5, "lng": 172.1},
    {"n": "Tswaing-Krater (Südafrika)", "lat": -25.42, "lng": 28.08},
    {"n": "Roter-Kamm-Krater (Namibia)", "lat": -27.77, "lng": 16.29},
    {"n": "Tenoumer-Krater (Mauretanien)", "lat": 22.93, "lng": -10.41},
    {"n": "Aouelloul-Krater (Mauretanien)", "lat": 20.25, "lng": -12.69},
    {"n": "Talemzane-Krater (Algerien)", "lat": 33.32, "lng": 4.02},
    {"n": "Wabar-Krater (Saudi-Arabien)", "lat": 21.5, "lng": 50.47},
    {"n": "Kamil-Krater (Ägypten)", "lat": 22.02, "lng": 26.05},
    {"n": "Manson-Krater (Iowa, USA)", "lat": 42.58, "lng": -94.55},
    {"n": "Santa-Fe-Krater (New Mexico, USA)", "lat": 35.78, "lng": -105.87},
    {"n": "Flynn-Creek-Krater (Tennessee, USA)", "lat": 36.27, "lng": -85.67},
    {"n": "Odessa-Krater (Texas, USA)", "lat": 31.77, "lng": -102.47},
    {"n": "Ries-Krater — Steinheimer Becken (Bayern, DE)", "lat": 48.69, "lng": 10.06},
]

r = {}
r["observatorien"] = extend_key(pin, "astro_observatorien", NEW_OBSERVATORIEN)
r["startrampen"]   = extend_key(pin, "astro_startrampen",   NEW_STARTRAMPEN)
r["esa_nasa"]      = extend_key(pin, "astro_esa_nasa_zentren", NEW_ESA_NASA)
r["krater"]        = extend_key(pin, "astro_meteoritenkrater", NEW_KRATER)
jsave(BASE / "data/astro_pin.json", pin)
for k,v in r.items(): print(f"  [OK] pin/{k}: +{v}")

# ═══════════════════════════════════════════════════════════════════════════════
# astro_hl.json
# ═══════════════════════════════════════════════════════════════════════════════
hl = jload(BASE / "data/astro_hl.json")

# ── raketen_nutzlast ──────────────────────────────────────────────────────────
NEW_RAKETEN = [
    {"name": "Starship (SpaceX, Vollausbau)", "val": 150},
    {"name": "Energia (Sowjetunion, 1987)", "val": 100},
    {"name": "N1 (Sowjetunion, gescheitert)", "val": 95},
    {"name": "New Glenn (Blue Origin)", "val": 45},
    {"name": "Vulcan Centaur (ULA)", "val": 27},
    {"name": "Angara-A5 (Roskosmos)", "val": 24},
    {"name": "Proton-M (Roskosmos)", "val": 23},
    {"name": "Space Shuttle (NASA, LEO)", "val": 24},
    {"name": "Atlas V 551 (ULA)", "val": 18},
    {"name": "H-IIB (JAXA)", "val": 16},
    {"name": "Ariane 6 A64 (ESA)", "val": 21},
    {"name": "GSLV Mk III (ISRO)", "val": 10},
    {"name": "H-IIA (JAXA)", "val": 10},
    {"name": "Antares 230+ (Northrop)", "val": 8},
    {"name": "Long March 2F (CNSA, Shenzhou)", "val": 8},
    {"name": "Zenit-3SL (Sea Launch)", "val": 13},
    {"name": "Long March 7 (CNSA)", "val": 13},
    {"name": "PSLV-XL (ISRO)", "val": 3},
    {"name": "Vega-C (ESA)", "val": 2},
    {"name": "Electron (Rocket Lab)", "val": 0.3},
    {"name": "LauncherOne (Virgin Orbit) †", "val": 0.5},
    {"name": "Minotaur V (Northrop)", "val": 0.5},
    {"name": "Pegasus XL (Northrop)", "val": 0.44},
    {"name": "Delta II (Boeing, hist.)", "val": 6},
    {"name": "Titan IV-B (USAF)", "val": 21},
    {"name": "Redstone (USA, hist. 1960)", "val": 0.04},
]

# ── missionsdauer (Tage) ──────────────────────────────────────────────────────
NEW_MISSIONSDAUER = [
    {"name": "Pioneer 10 (NASA, 1972–2003)", "val": 11312},
    {"name": "Pioneer 11 (NASA, 1973–1995)", "val": 8139},
    {"name": "Mars Odyssey (NASA, seit 2001)", "val": 8700},
    {"name": "Mars Express (ESA, seit 2003)", "val": 8000},
    {"name": "Galileo-Sonde (NASA, 1989–2003)", "val": 5113},
    {"name": "Spitzer Space Telescope (2003–2020)", "val": 5980},
    {"name": "Juno (NASA, seit 2011)", "val": 5100},
    {"name": "Rosetta (ESA, 2004–2016)", "val": 4354},
    {"name": "MESSENGER (NASA, 2004–2015)", "val": 3914},
    {"name": "Dawn (NASA, 2007–2018)", "val": 4053},
    {"name": "Kepler Space Telescope (2009–2018)", "val": 3393},
    {"name": "Mars Global Surveyor (1996–2006)", "val": 3626},
    {"name": "Spirit Rover (NASA, 2004–2010)", "val": 2208},
    {"name": "ISS Dauerbetrieb (seit 1998)", "val": 9500},
    {"name": "TESS (NASA, seit 2018)", "val": 2700},
    {"name": "Parker Solar Probe (seit 2018)", "val": 2700},
    {"name": "BepiColombo (ESA/JAXA, seit 2018)", "val": 2500},
    {"name": "Mars Perseverance (seit 2021)", "val": 1600},
    {"name": "James Webb Telescope (seit 2021)", "val": 1400},
    {"name": "InSight Lander (2018–2022)", "val": 1445},
    {"name": "Hayabusa (JAXA, 2003–2010)", "val": 2550},
    {"name": "OSIRIS-REx (NASA, seit 2016)", "val": 3200},
    {"name": "Chang'e 4 Lander (seit 2019)", "val": 2000},
    {"name": "Magellan (NASA, 1989–1994)", "val": 1795},
    {"name": "Apollo 11 (NASA, 1969)", "val": 8},
    {"name": "Sputnik 1 (UdSSR, 1957)", "val": 92},
    {"name": "Chandra X-Ray Observatory (seit 1999)", "val": 9500},
    {"name": "SOHO (ESA/NASA, seit 1995)", "val": 10800},
    {"name": "Ulysses (ESA, 1990–2009)", "val": 6898},
    {"name": "WMAP (NASA, 2001–2010)", "val": 3287},
]

# ── exoplaneten_distanz (Lichtjahre) ─────────────────────────────────────────
NEW_EXOPLANETEN = [
    {"name": "Wolf 1061 c", "val": 14.1},
    {"name": "Ross 128 b", "val": 11.0},
    {"name": "Tau Ceti f", "val": 11.9},
    {"name": "GJ 1061 d", "val": 12.0},
    {"name": "Teegarden's Star b", "val": 12.5},
    {"name": "Barnard's Star b (umstritten)", "val": 6.0},
    {"name": "LHS 1140 b", "val": 40.9},
    {"name": "55 Cancri e", "val": 41.3},
    {"name": "Upsilon Andromedae d", "val": 44.0},
    {"name": "TRAPPIST-1 d", "val": 39.5},
    {"name": "TRAPPIST-1 f", "val": 39.5},
    {"name": "TOI-700 d", "val": 102.0},
    {"name": "K2-18 b", "val": 124.0},
    {"name": "Kepler-186 f", "val": 580.0},
    {"name": "Kepler-22 b", "val": 620.0},
    {"name": "Kepler-62 f", "val": 1200.0},
    {"name": "Kepler-442 b", "val": 1200.0},
    {"name": "HR 8799 b", "val": 129.0},
    {"name": "Beta Pictoris b", "val": 63.4},
    {"name": "Fomalhaut b", "val": 25.0},
    {"name": "70 Virginis b", "val": 60.0},
    {"name": "WASP-12 b", "val": 870.0},
    {"name": "WASP-121 b", "val": 880.0},
    {"name": "HD 189733 b", "val": 63.0},
    {"name": "CoRoT-7 b", "val": 480.0},
    {"name": "HAT-P-7 b (Kepler-2 b)", "val": 1044.0},
    {"name": "HIP 13044 b", "val": 2000.0},
    {"name": "PSR 1257+12 b (1. bestätigter Exoplanet)", "val": 980.0},
]

# ── sonnenentfernung (Mio. km) — Zwergplaneten ergänzen ──────────────────────
NEW_SONNENDIST = [
    {"name": "Ceres (Asteroidengürtel)", "val": 414},
    {"name": "Vesta (Asteroidengürtel)", "val": 353},
    {"name": "Pallas (Asteroidengürtel)", "val": 415},
    {"name": "Pluto (Zwergplanet)", "val": 5906},
    {"name": "Haumea (Zwergplanet)", "val": 6452},
    {"name": "Makemake (Zwergplanet)", "val": 6796},
    {"name": "Eris (Zwergplanet)", "val": 10210},
    {"name": "Sedna (Zwerg-TNO)", "val": 83000},
    {"name": "Quaoar (Zwergplanet)", "val": 6900},
    {"name": "Hygiea (Asteroid)", "val": 470},
]

# ── monde_anzahl — Zwergplaneten + Kleinkörper ────────────────────────────────
NEW_MONDE = [
    {"name": "Pluto", "val": 5},
    {"name": "Haumea", "val": 2},
    {"name": "Eris", "val": 1},
    {"name": "Makemake", "val": 1},
    {"name": "Ceres", "val": 0},
    {"name": "Quaoar", "val": 1},
]

# ── entdeckungsjahr ───────────────────────────────────────────────────────────
NEW_ENTDECKUNG = [
    {"name": "Mond (allgemein bekannt)", "val": -30000},
    {"name": "Saturn (sichtbar mit bloßem Auge)", "val": -700},
    {"name": "Ganymed (Galileo Galilei)", "val": 1610},
    {"name": "Kallisto (Galileo Galilei)", "val": 1610},
    {"name": "Titan (Christiaan Huygens)", "val": 1655},
    {"name": "Iapetus (Giovanni Cassini)", "val": 1671},
    {"name": "Rhea (Giovanni Cassini)", "val": 1672},
    {"name": "Tethys (Giovanni Cassini)", "val": 1684},
    {"name": "Dione (Giovanni Cassini)", "val": 1684},
    {"name": "Enceladus (William Herschel)", "val": 1789},
    {"name": "Mimas (William Herschel)", "val": 1789},
    {"name": "Triton (William Lassell)", "val": 1846},
    {"name": "Hyperion (Bond/Lassell)", "val": 1848},
    {"name": "Phoebe (William Pickering)", "val": 1899},
    {"name": "Amalthea (Barnard)", "val": 1892},
    {"name": "Proxima Centauri (Robert Innes)", "val": 1915},
    {"name": "Quaoar (Trujillo/Brown)", "val": 2002},
    {"name": "Eris (Mike Brown et al.)", "val": 2005},
    {"name": "Haumea (Brown / Ortiz)", "val": 2004},
    {"name": "Erstes Exoplanet-System (Wolszczan/Frail)", "val": 1992},
    {"name": "51 Pegasi b (Mayor/Queloz)", "val": 1995},
]

# ── schwerkraft (m/s²) — Monde + Kleinkörper ─────────────────────────────────
NEW_SCHWERKRAFT = [
    {"name": "Sonne", "val": 274.0},
    {"name": "Merkur", "val": 3.7},
    {"name": "Venus", "val": 8.87},
    {"name": "Titan (Saturnmond)", "val": 1.35},
    {"name": "Ganymed (Jupitermond)", "val": 1.43},
    {"name": "Europa (Jupitermond)", "val": 1.31},
    {"name": "Ceres (Zwergplanet)", "val": 0.27},
    {"name": "Io (Jupitermond)", "val": 1.80},
    {"name": "Triton (Neptunmond)", "val": 0.78},
    {"name": "Charon (Pluton)", "val": 0.28},
    {"name": "Enceladus (Saturnmond)", "val": 0.11},
    {"name": "Rhea (Saturnmond)", "val": 0.26},
]

# ── temperaturen — weitere Himmelskörper ──────────────────────────────────────
NEW_TEMP = [
    {"name": "Sonne (Oberfläche)", "val": 5500},
    {"name": "Mond (Tagseite)", "val": 127},
    {"name": "Mond (Nachtseite)", "val": -173},
    {"name": "Merkur (Nacht)", "val": -180},
    {"name": "Pluto", "val": -229},
    {"name": "Titan (Saturn)", "val": -179},
    {"name": "Enceladus (Geysire)", "val": -201},
    {"name": "Europa (Oberfläche)", "val": -160},
    {"name": "Io (Lava)", "val": 1650},
    {"name": "Boomerang-Nebel (kältester Ort)", "val": -272},
]

hr = {}
hr["raketen"]    = extend_key(hl, "astro_raketen_nutzlast",  NEW_RAKETEN,    "name")
hr["mission"]    = extend_key(hl, "astro_missionsdauer",     NEW_MISSIONSDAUER, "name")
hr["exoplanet"]  = extend_key(hl, "astro_exoplaneten_distanz", NEW_EXOPLANETEN, "name")
hr["sonne"]      = extend_key(hl, "astro_sonnenentfernung",  NEW_SONNENDIST, "name")
hr["monde"]      = extend_key(hl, "astro_monde_anzahl",      NEW_MONDE,      "name")
hr["entdeckung"] = extend_key(hl, "astro_entdeckungsjahr",   NEW_ENTDECKUNG, "name")
hr["schwerkraft"]= extend_key(hl, "astro_schwerkraft",       NEW_SCHWERKRAFT,"name")
hr["temp"]       = extend_key(hl, "astro_temperaturen",      NEW_TEMP,       "name")
jsave(BASE / "data/astro_hl.json", hl)
for k,v in hr.items(): print(f"  [OK] hl/{k}: +{v}")

# ═══════════════════════════════════════════════════════════════════════════════
# astro_match.json
# ═══════════════════════════════════════════════════════════════════════════════
match = jload(BASE / "data/astro_match.json")

NEW_MISSIONEN = [
    {"n": "Apollo 1 (Brandkatastrophe 1967)", "c": "NASA"},
    {"n": "Apollo 13 (Notfall-Rückkehr 1970)", "c": "NASA"},
    {"n": "Apollo 17 (letzte Mondlandung 1972)", "c": "NASA"},
    {"n": "Mercury Friendship 7 (Glenn-Orbit 1962)", "c": "NASA"},
    {"n": "Vostok 1 (Gagarin Weltraumflug 1961)", "c": "Sowjetunion"},
    {"n": "Vostok 6 (Tereshkova, erste Frau 1963)", "c": "Sowjetunion"},
    {"n": "Luna 9 (erste Mondlandung 1966)", "c": "Sowjetunion"},
    {"n": "Venera 7 (erste Venus-Landung 1970)", "c": "Sowjetunion"},
    {"n": "Mariner 4 (erster Mars-Flyby 1965)", "c": "NASA"},
    {"n": "Mariner 2 (erster Venus-Flyby 1962)", "c": "NASA"},
    {"n": "Viking 1 (Mars-Lander 1976)", "c": "NASA"},
    {"n": "Pioneer 10 (Jupiter-Flyby 1973)", "c": "NASA"},
    {"n": "Galileo (Jupiter-Orbiter 1995–2003)", "c": "NASA"},
    {"n": "Magellan (Venus-Mapping 1990–1994)", "c": "NASA"},
    {"n": "SOHO (Sonnenobservatorium, seit 1995)", "c": "ESA/NASA"},
    {"n": "Ulysses (Solar-Mission 1990–2009)", "c": "ESA/NASA"},
    {"n": "Spitzer Space Telescope (2003–2020)", "c": "NASA"},
    {"n": "Hubble Space Telescope (seit 1990)", "c": "NASA/ESA"},
    {"n": "Chandra X-Ray Observatory (seit 1999)", "c": "NASA"},
    {"n": "WMAP (CMB-Kartierung 2001–2010)", "c": "NASA"},
    {"n": "Planck (CMB-Kartierung 2009–2013)", "c": "ESA"},
    {"n": "GAIA (Sternen-Kartierung, seit 2013)", "c": "ESA"},
    {"n": "Parker Solar Probe (seit 2018)", "c": "NASA"},
    {"n": "Solar Orbiter (seit 2020)", "c": "ESA"},
    {"n": "DART Mission (Asteroid Impact 2022)", "c": "NASA"},
    {"n": "Ingenuity Helikopter (Mars-Flug 2021)", "c": "NASA"},
    {"n": "Perseverance Rover (Mars, seit 2021)", "c": "NASA"},
    {"n": "InSight Lander (Mars 2018–2022)", "c": "NASA"},
    {"n": "MAVEN (Mars-Atmosphäre, seit 2013)", "c": "NASA"},
    {"n": "Chandrayaan-1 (Mond-Orbiter 2008)", "c": "ISRO"},
    {"n": "Chandrayaan-3 (Mondlandung 2023)", "c": "ISRO"},
    {"n": "Akatsuki (Venus-Orbiter, seit 2010)", "c": "JAXA"},
    {"n": "Hayabusa 1 (Asteroid Itokawa 2005)", "c": "JAXA"},
    {"n": "Kaguya/SELENE (Mond-Orbiter 2007)", "c": "JAXA"},
    {"n": "Mars Express (seit 2003)", "c": "ESA"},
    {"n": "SMART-1 (Mond-Orbiter 2003–2006)", "c": "ESA"},
    {"n": "Deep Impact (Komet Tempel 1, 2005)", "c": "NASA"},
    {"n": "Stardust (Komet Wild 2, 2004)", "c": "NASA"},
    {"n": "LCROSS (Mondeinschlag 2009)", "c": "NASA"},
    {"n": "Lunar Reconnaissance Orbiter (seit 2009)", "c": "NASA"},
    {"n": "Chang'e 4 (Mondrückseite, seit 2019)", "c": "CNSA"},
    {"n": "ExoMars TGO (Mars-Gase, seit 2016)", "c": "ESA/Roskosmos"},
    {"n": "James Webb Space Telescope (seit 2021)", "c": "NASA/ESA/CSA"},
    {"n": "TESS (Exoplanet-Suche, seit 2018)", "c": "NASA"},
    {"n": "Kepler Space Telescope (2009–2018)", "c": "NASA"},
    {"n": "OSIRIS-APEX (ex-REx, Asteroid Apophis)", "c": "NASA"},
    {"n": "Dragonfly (Titan-Mission, geplant 2034)", "c": "NASA"},
    {"n": "Europa Clipper (Jupitermond, seit 2024)", "c": "NASA"},
]

NEW_SONDEN_ZIELE = [
    {"n": "Voyager 2", "c": "Neptun & Uranus"},
    {"n": "Pioneer 10", "c": "Jupiter (Flyby)"},
    {"n": "Pioneer 11", "c": "Saturn (Flyby)"},
    {"n": "Galileo-Sonde (NASA)", "c": "Jupiter"},
    {"n": "Magellan (NASA)", "c": "Venus"},
    {"n": "Venus Express (ESA)", "c": "Venus"},
    {"n": "Akatsuki (JAXA)", "c": "Venus"},
    {"n": "Mars Global Surveyor", "c": "Mars"},
    {"n": "Mars Odyssey", "c": "Mars"},
    {"n": "Mars Reconnaissance Orbiter", "c": "Mars"},
    {"n": "Mars Express (ESA)", "c": "Mars"},
    {"n": "MAVEN (NASA)", "c": "Mars (Atmosphäre)"},
    {"n": "Phoenix Lander", "c": "Mars (Nordpol)"},
    {"n": "Spirit Rover", "c": "Mars"},
    {"n": "Opportunity Rover", "c": "Mars"},
    {"n": "Perseverance Rover", "c": "Mars"},
    {"n": "Tianwen-1 (CNSA)", "c": "Mars"},
    {"n": "Sojourner Rover (Pathfinder)", "c": "Mars"},
    {"n": "BepiColombo (ESA/JAXA)", "c": "Merkur"},
    {"n": "Mariner 10", "c": "Merkur"},
    {"n": "Deep Impact (NASA)", "c": "Komet Tempel 1"},
    {"n": "Stardust (NASA)", "c": "Komet Wild 2"},
    {"n": "LCROSS (NASA)", "c": "Mond"},
    {"n": "Lunar Reconnaissance Orbiter", "c": "Mond"},
    {"n": "Chang'e 4 (CNSA)", "c": "Mond (Rückseite)"},
    {"n": "Chandrayaan-3 (ISRO)", "c": "Mond (Südpol)"},
    {"n": "Hayabusa (JAXA)", "c": "Asteroid Itokawa"},
    {"n": "DART (NASA)", "c": "Asteroid Dimorphos"},
    {"n": "Parker Solar Probe (NASA)", "c": "Sonne"},
    {"n": "Solar Orbiter (ESA)", "c": "Sonne"},
    {"n": "SOHO (ESA/NASA)", "c": "Sonne"},
    {"n": "Ulysses (ESA)", "c": "Sonne (Polregionen)"},
    {"n": "Europa Clipper (NASA)", "c": "Europa (Jupitermond)"},
    {"n": "Galileo-Probe (Atmosph.-Eintritt)", "c": "Jupiter (Atmosphäre)"},
    {"n": "Chandrayaan-1 (ISRO)", "c": "Mond"},
    {"n": "OSIRIS-REx (NASA)", "c": "Asteroid Bennu"},
    {"n": "New Horizons (Kuiper-Gürtel)", "c": "Arrokoth (Kuiper-Gürtel)"},
]

NEW_HIMMELSKOERPER = [
    {"n": "Erde", "c": "Planet (Gesteinsplanet)"},
    {"n": "Mars", "c": "Planet (Gesteinsplanet)"},
    {"n": "Venus", "c": "Planet (Gesteinsplanet)"},
    {"n": "Merkur", "c": "Planet (Gesteinsplanet)"},
    {"n": "Neptun", "c": "Planet (Eisriese)"},
    {"n": "Uranus", "c": "Planet (Eisriese)"},
    {"n": "Mond (Erde)", "c": "Mond"},
    {"n": "Europa", "c": "Mond"},
    {"n": "Ganymed", "c": "Mond"},
    {"n": "Kallisto", "c": "Mond"},
    {"n": "Enceladus", "c": "Mond"},
    {"n": "Titan", "c": "Mond"},
    {"n": "Triton", "c": "Mond"},
    {"n": "Charon", "c": "Mond"},
    {"n": "Haumea", "c": "Zwergplanet"},
    {"n": "Eris", "c": "Zwergplanet"},
    {"n": "Vesta", "c": "Asteroid"},
    {"n": "Pallas", "c": "Asteroid"},
    {"n": "Apophis", "c": "Asteroid"},
    {"n": "Komet 67P/Churyumov-Gerasimenko", "c": "Komet"},
    {"n": "Komet NEOWISE (C/2020 F3)", "c": "Komet"},
    {"n": "Komet Hale-Bopp", "c": "Komet"},
    {"n": "Orionnebel (M42)", "c": "Emissionsnebel"},
    {"n": "Krabbennebel (M1)", "c": "Supernovarest"},
    {"n": "Ringnebel (M57)", "c": "Planetarischer Nebel"},
    {"n": "Omega-Centauri", "c": "Kugelsternhaufen"},
    {"n": "Plejaden (M45)", "c": "Offener Sternhaufen"},
    {"n": "Abell 2029", "c": "Galaxienhaufen"},
    {"n": "SGR A*", "c": "Schwarzes Loch"},
    {"n": "Crab Pulsar (PSR B0531+21)", "c": "Pulsar"},
    {"n": "3C 273", "c": "Quasar"},
    {"n": "Proxima Centauri", "c": "Stern (Roter Zwerg)"},
    {"n": "Beteigeuze (Betelgeuse)", "c": "Stern (Roter Überriese)"},
    {"n": "Sirius B", "c": "Weißer Zwerg"},
    {"n": "Sagittarius A* (Milchstraßenzentrum)", "c": "Schwarzes Loch"},
    {"n": "LMC (Große Magellansche Wolke)", "c": "Irreguläre Galaxie"},
    {"n": "Circinus-Galaxie", "c": "Seyfert-Galaxie"},
    {"n": "NGC 1277", "c": "Galaxie mit supermassivem schwarzem Loch"},
    {"n": "Boomerang-Nebel", "c": "Präplanetarischer Nebel"},
    {"n": "PSR J0437-4715", "c": "Millisekunden-Pulsar"},
]

NEW_STERNBILDER = [
    {"n": "Löwe (Leo)", "c": "Äquatorbereich"},
    {"n": "Stier (Taurus)", "c": "Äquatorbereich"},
    {"n": "Zwillinge (Gemini)", "c": "Äquatorbereich"},
    {"n": "Jungfrau (Virgo)", "c": "Äquatorbereich"},
    {"n": "Waage (Libra)", "c": "Äquatorbereich"},
    {"n": "Schütze (Sagittarius)", "c": "Äquatorbereich"},
    {"n": "Steinbock (Capricornus)", "c": "Äquatorbereich"},
    {"n": "Wassermann (Aquarius)", "c": "Äquatorbereich"},
    {"n": "Fische (Pisces)", "c": "Äquatorbereich"},
    {"n": "Schlangenträger (Ophiuchus)", "c": "Äquatorbereich"},
    {"n": "Adler (Aquila)", "c": "Äquatorbereich"},
    {"n": "Schwan (Cygnus)", "c": "Nordhimmel"},
    {"n": "Leier (Lyra)", "c": "Nordhimmel"},
    {"n": "Herkules (Hercules)", "c": "Nordhimmel"},
    {"n": "Drache (Draco)", "c": "Nordhimmel"},
    {"n": "Fuhrmann (Auriga)", "c": "Nordhimmel"},
    {"n": "Perseus", "c": "Nordhimmel"},
    {"n": "Kepheus (Cepheus)", "c": "Nordhimmel"},
    {"n": "Andromeda", "c": "Nordhimmel"},
    {"n": "Bootes (Bärenhüter)", "c": "Nordhimmel"},
    {"n": "Corona Borealis", "c": "Nordhimmel"},
    {"n": "Nördliche Krone", "c": "Nordhimmel"},
    {"n": "Hydra (Wasserschlange)", "c": "Südhimmel"},
    {"n": "Vela (Segel)", "c": "Südhimmel"},
    {"n": "Puppis (Hinterdeck)", "c": "Südhimmel"},
    {"n": "Grus (Kranich)", "c": "Südhimmel"},
    {"n": "Phoenix", "c": "Südhimmel"},
    {"n": "Pavo (Pfau)", "c": "Südhimmel"},
    {"n": "Ara (Altar)", "c": "Südhimmel"},
    {"n": "Lupus (Wolf)", "c": "Südhimmel"},
    {"n": "Musca (Fliege)", "c": "Südhimmel"},
    {"n": "Columba (Taube)", "c": "Südhimmel"},
    {"n": "Sculptor", "c": "Südhimmel"},
    {"n": "Eridanus (Fluss)", "c": "Südhimmel"},
    {"n": "Vela (Schiffssegel)", "c": "Südhimmel"},
    {"n": "Schütze (Sagittarius)", "c": "Äquatorbereich"},  # duplicate guard active
    {"n": "Ophiuchus", "c": "Äquatorbereich"},
    {"n": "Monoceros (Einhorn)", "c": "Äquatorbereich"},
    {"n": "Lepus (Hase)", "c": "Äquatorbereich"},
    {"n": "Fornax (Ofen)", "c": "Südhimmel"},
]

NEW_PIONIERE = [
    {"n": "Tycho Brahe", "c": "Präzise Planetenbeobachtungen ohne Teleskop"},
    {"n": "Charles Messier", "c": "Messier-Katalog der Nebel und Sternhaufen"},
    {"n": "William Herschel", "c": "Entdeckung des Uranus und Infrarotstrahlung"},
    {"n": "Caroline Herschel", "c": "Erste Frau mit offiziellem Astronomentitel"},
    {"n": "Henrietta Swan Leavitt", "c": "Entfernungsmessung über Cepheiden-Perioden"},
    {"n": "Annie Jump Cannon", "c": "Harvard-Spektralklassifikation der Sterne"},
    {"n": "Jocelyn Bell Burnell", "c": "Entdeckung des ersten Pulsars (1967)"},
    {"n": "Subrahmanyan Chandrasekhar", "c": "Chandrasekhar-Limit weißer Zwerge"},
    {"n": "Carl Sagan", "c": "Kosmologische Aufklärung und SETI-Pionier"},
    {"n": "Fritz Zwicky", "c": "Erste Hinweise auf Dunkle Materie (1933)"},
    {"n": "Georges Lemaître", "c": "Urknall-Theorie (Primaeval Atom)"},
    {"n": "Albert Einstein", "c": "Allgemeine Relativitätstheorie (Raumzeit)"},
    {"n": "Christiaan Huygens", "c": "Entdeckung des Saturn-Mondes Titan"},
    {"n": "Giovanni Cassini", "c": "Entdeckung der Cassini-Teilung in Saturnringen"},
    {"n": "William Pickering", "c": "Entdeckung des Saturn-Mondes Phoebe"},
    {"n": "Frank Drake", "c": "Drake-Gleichung zur Schätzung außerirdischer Zivilisationen"},
    {"n": "Jill Tarter", "c": "SETI-Institut-Forscherin und Radioastronomin"},
    {"n": "Gerard Kuiper", "c": "Beschreibung des Kuiper-Gürtels"},
    {"n": "Jan Oort", "c": "Oortsche Wolke als Quelle der Kometen"},
    {"n": "Percival Lowell", "c": "Vorhersage des Planeten X (führte zu Pluto-Entdeckung)"},
    {"n": "Williamina Fleming", "c": "Klassifikation von über 10.000 Sternenspektren"},
    {"n": "Michel Mayor", "c": "Entdeckung des ersten Exoplaneten (51 Peg b)"},
    {"n": "Didier Queloz", "c": "Mitentdeckung des ersten Exoplaneten (51 Peg b)"},
    {"n": "Georges Lemaître", "c": "Urknall-Theorie"},  # duplicate guard active
    {"n": "Alexei Leonov", "c": "Erster Weltraumausstieg (EVA) 1965"},
    {"n": "Neil Armstrong", "c": "Erster Mensch auf dem Mond (Apollo 11, 1969)"},
    {"n": "Yuri Gagarin", "c": "Erster Mensch im Weltraum (Vostok 1, 1961)"},
    {"n": "Valentina Tereshkova", "c": "Erste Frau im Weltraum (Vostok 6, 1963)"},
    {"n": "Edwin Hubble", "c": "Universum expandiert (Hubble-Gesetz)"},  # duplicate guard
    {"n": "Vera Rubin", "c": "Nachweis Dunkler Materie"},  # dup guard
    {"n": "Katherine Johnson", "c": "NASA-Mathematikerin: Bahnberechnungen Mercury/Apollo"},
]

NEW_ANTRIEBE = [
    {"n": "Raptor (SpaceX Starship, Vollausbau)", "c": "Methan/Flüssigsauerstoff"},
    {"n": "BE-4 (Blue Origin New Glenn)", "c": "Methan/Flüssigsauerstoff"},
    {"n": "RD-180 (Atlas V, 1. Stufe)", "c": "Kerosin/Flüssigsauerstoff"},
    {"n": "NK-33/AJ26 (Antares)", "c": "Kerosin/Flüssigsauerstoff"},
    {"n": "Rutherford (Electron, Rocket Lab)", "c": "Kerosin/Flüssigsauerstoff"},
    {"n": "Merlin Vakuum (Falcon 9, Oberstufe)", "c": "Kerosin/Flüssigsauerstoff"},
    {"n": "RL-10 (Centaur-Oberstufe)", "c": "Kryogen (LH2/LOX)"},
    {"n": "J-2 (Saturn V, 2. + 3. Stufe)", "c": "Kryogen (LH2/LOX)"},
    {"n": "RS-68 (Delta IV Heavy)", "c": "Kryogen (LH2/LOX)"},
    {"n": "HM7B (Ariane-Oberstufe)", "c": "Kryogen (LH2/LOX)"},
    {"n": "RD-270 (Proton-Projekt, ungeflogen)", "c": "UDMH/Stickstofftetroxid"},
    {"n": "YF-77 (Long March 5, Kernstufe)", "c": "Kryogen (LH2/LOX)"},
    {"n": "Vikas (GSLV Mk II)", "c": "UDMH/Stickstofftetroxid"},
    {"n": "CE-7.5 (GSLV Mk III, Cryostage)", "c": "Kryogen (LH2/LOX)"},
    {"n": "RD-107 (Sojus-Booster)", "c": "Kerosin/Flüssigsauerstoff"},
    {"n": "NEXT-C (NASA Evolved Xenon Thruster)", "c": "Ionenantrieb (Xenon)"},
    {"n": "Hall-Effekt-Triebwerk (SPT-100)", "c": "Elektrischer Antrieb"},
    {"n": "VASIMR (Variable Specific Impulse Magneto)", "c": "Plasma (Radiofrequenz)"},
    {"n": "Solar Sail IKAROS (JAXA)", "c": "Solarer Strahlungsdruck"},
    {"n": "RTG (Voyager 1 & 2)", "c": "Radioisotopen-Thermogenerator"},
    {"n": "Nuclear Thermal Rocket (NTR, geplant)", "c": "Kernspaltung (Wasserstoff)"},
    {"n": "Project Orion (hist. Konzept)", "c": "Nuklear-Puls"},
]

NEW_GALAXIEN = [
    {"n": "Triangulum-Galaxie (M33)", "c": "Spiralgalaxie"},
    {"n": "Whirlpool-Galaxie (M51)", "c": "Spiralgalaxie"},
    {"n": "Sculptor-Galaxie (NGC 253)", "c": "Spiralgalaxie"},
    {"n": "Sonnenblumen-Galaxie (M63)", "c": "Spiralgalaxie"},
    {"n": "Bode-Galaxie (M81)", "c": "Spiralgalaxie"},
    {"n": "NGC 1365", "c": "Balkenspirale"},
    {"n": "NGC 6217", "c": "Balkenspirale"},
    {"n": "NGC 2903", "c": "Balkenspirale"},
    {"n": "Centaurus A (NGC 5128)", "c": "Elliptische Galaxie"},
    {"n": "Fornax A (NGC 1316)", "c": "Elliptische Galaxie"},
    {"n": "M60 (NGC 4649)", "c": "Elliptische Galaxie"},
    {"n": "Sombrero-Galaxie (M104)", "c": "Lenticuläre Galaxie (S0)"},
    {"n": "Zigarren-Galaxie (M82)", "c": "Irreguläre Galaxie (Starburst)"},
    {"n": "NGC 1427A", "c": "Irreguläre Galaxie"},
    {"n": "Sextans A", "c": "Irreguläre Galaxie"},
    {"n": "Cartwheel Galaxy", "c": "Ring-Galaxie"},
    {"n": "Hoag's Object", "c": "Ring-Galaxie"},
    {"n": "NGC 4038/4039 (Antennen-Galaxien)", "c": "Interagierende Galaxien"},
    {"n": "Leo I", "c": "Zwerggalaxie (Sphäroid)"},
    {"n": "Sculptor-Zwerggalaxie", "c": "Zwerggalaxie (Sphäroid)"},
    {"n": "NGC 3603", "c": "HII-Region (Emissionsnebel-Galaxie)"},
    {"n": "Markarian 231", "c": "Ultraluminöse Infrarot-Galaxie (Quasar-Host)"},
    {"n": "IC 1101", "c": "Elliptische Galaxie (größte bekannte)"},
    {"n": "NGC 5457 (Pinwheel Galaxy)", "c": "Spiralgalaxie"},
    {"n": "NGC 4889", "c": "Elliptische Galaxie (supermassives schwarzes Loch)"},
]

NEW_KOSMOLOGIE = [
    {"n": "Dunkle Materie", "c": "Unsichtbare Materie — hält Galaxien zusammen"},
    {"n": "Dunkle Energie", "c": "Treibt beschleunigte Expansion des Universums"},
    {"n": "Magnetar", "c": "Neutronenstern mit extrem starkem Magnetfeld"},
    {"n": "Gamma-Ray Burst (GRB)", "c": "Leuchtstärkste Explosion im Universum"},
    {"n": "Kosmische Inflation", "c": "Exponentiell schnelle Expansion kurz nach Urknall"},
    {"n": "Kosmische Hintergrundstrahlung (CMB)", "c": "Überbleibsel des Urknalls (~380.000 J.)"},
    {"n": "Gravitationswelle", "c": "Raumzeitkrümmung durch beschleunigte Massen"},
    {"n": "Hawking-Strahlung", "c": "Thermische Strahlung schwarzer Löcher (Quanteneffekt)"},
    {"n": "Chandrasekhar-Limit", "c": "Maximal ~1,4 Sonnenmassen für weißen Zwerg"},
    {"n": "Schwarzschild-Radius", "c": "Kritischer Radius ab dem Licht nicht entkommt"},
    {"n": "Hubble-Konstante (H₀)", "c": "Expansionsrate des Universums (~70 km/s/Mpc)"},
    {"n": "Roter Riese", "c": "Aufgeblasener Stern am Ende seines Lebens"},
    {"n": "Blaue Hauptreihenstern", "c": "Heißer, kurzlebiger massereicher Stern"},
    {"n": "T-Tauri-Stern", "c": "Junger protostellarer Stern vor der Hauptreihe"},
    {"n": "Interstellares Medium (ISM)", "c": "Gas und Staub zwischen den Sternen"},
    {"n": "Akkretion", "c": "Materieaufnahme durch Schwerkraft (z.B. auf schwarze Löcher)"},
    {"n": "Gezeitenzerreißung (TDE)", "c": "Stern wird von Gravitation eines schwarzen Lochs zerrissen"},
    {"n": "Gravitationslinse", "c": "Lichtablenkung durch massive Objekte"},
    {"n": "Rote Verschiebung (Redshift)", "c": "Licht entfernter Galaxien verschoben → Expansion"},
    {"n": "Baryon-Asymmetrie", "c": "Warum gibt es mehr Materie als Antimaterie?"},
]

mr = {}
mr["missionen"]       = extend_key(match, "astro_missionen",        NEW_MISSIONEN)
mr["sonden"]          = extend_key(match, "astro_sonden_ziele",      NEW_SONDEN_ZIELE)
mr["himmelskörper"]   = extend_key(match, "astro_himmelskoerper_typ",NEW_HIMMELSKOERPER)
mr["sternbilder"]     = extend_key(match, "astro_sternbilder_himmel",NEW_STERNBILDER)
mr["pioniere"]        = extend_key(match, "astro_pioniere",          NEW_PIONIERE)
mr["antriebe"]        = extend_key(match, "astro_antriebe",          NEW_ANTRIEBE)
mr["galaxien"]        = extend_key(match, "astro_galaxien_typen",    NEW_GALAXIEN)
mr["kosmologie"]      = extend_key(match, "astro_kosmologie",        NEW_KOSMOLOGIE)
jsave(BASE / "data/astro_match.json", match)
for k,v in mr.items(): print(f"  [OK] match/{k}: +{v}")

# ─── Abschlusszählung ─────────────────────────────────────────────────────────
print("\n=== FINALE ITEMZAHLEN ===")
for fname, data in [("astro_pin.json", pin), ("astro_hl.json", hl), ("astro_match.json", match)]:
    print(f"\n{fname}")
    for k,v in data.items():
        items = v.get("items",[]) if isinstance(v,dict) else v
        print(f"  {k}: {len(items)}")
