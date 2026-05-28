#!/usr/bin/env python3
"""
patch_265_geo_sport_astro_sweep.py — Phase 265
Erweitert alle 8-20-Item-Modi in geo_hl, geo_match, sport_hl, sport_match,
astro_hl, astro_match und archaeologie_match auf 30-40+ Items.

Ziel-Modi (40 Modi gesamt):
  geo_hl      : geo_berghoehen, geo_vulkan_hoehen, geo_erdbeben_magnitude,
                geo_vei_ausbruch, geo_kontinentaldrift, geo_schmelztemperatur,
                geo_tsunami_hoehe
  geo_match   : geo_gesteinsarten, geo_tektonik, geo_mineralien,
                geo_fossil_zeitalter, geo_landschaft_ursprung,
                geo_kontinent_platte, geo_hoehlen_land,
                geo_mineral_kristall, geo_gebirge_entstehung
  sport_hl    : sport_hochsprung_rekorde, sport_olympia_goldmedaillen,
                sport_fussball_marktwert, sport_gewichtheben_rekorde,
                sport_tore_saison
  sport_match : sport_teamgroesse, sport_olympia_standort, sport_olympisch,
                sport_nationalsport_match, sport_rekordhalter,
                sport_disziplin_kategorie, sport_sportart_kontinent
  astro_hl    : astro_planet_groesse, astro_monde_anzahl,
                astro_sonnenentfernung, astro_temperaturen
  astro_match : astro_planeten
  arch_match  : werkzeuge, schriften, bestattungsriten, waehrungen,
                tempel_ordnungen, zufallsfunde, welterbe_gefahr
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(os.path.dirname(BASE), "data")


def load(fn):
    with open(os.path.join(DATA, fn), encoding="utf-8") as f:
        return json.load(f)


def save(fn, data):
    with open(os.path.join(DATA, fn), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extend_hl(data, key, new_items):
    """Dedup by name (case-insensitive)."""
    block = data[key]
    existing = block.get("items", [])
    ex_names = {it["name"].lower() for it in existing}
    added = []
    for it in new_items:
        if it["name"].lower() not in ex_names:
            ex_names.add(it["name"].lower())
            added.append(it)
    block["items"] = existing + added
    return len(added)


def extend_match(data, key, new_items):
    """Dedup by n (case-insensitive)."""
    block = data[key]
    existing = block.get("items", [])
    ex_names = {it["n"].lower() for it in existing}
    added = []
    for it in new_items:
        if it["n"].lower() not in ex_names:
            ex_names.add(it["n"].lower())
            added.append(it)
    block["items"] = existing + added
    return len(added)


total_added = 0


def report(fn, key, n, final):
    global total_added
    total_added += n
    print(f"  {fn}:{key}  +{n} → {final} Items")


# ═══════════════════════════════════════════════════════════════════
# 1) GEO HL
# ═══════════════════════════════════════════════════════════════════
print("\n📐 geo_hl.json")
geo_hl = load("geo_hl.json")

n = extend_hl(geo_hl, "geo_berghoehen", [
    {"name": "Makalu (Nepal/China)",            "val": 8485},
    {"name": "Cho Oyu (Nepal/China)",           "val": 8188},
    {"name": "Dhaulagiri I (Nepal)",            "val": 8167},
    {"name": "Manaslu (Nepal)",                 "val": 8163},
    {"name": "Nanga Parbat (Pakistan)",         "val": 8126},
    {"name": "Annapurna I (Nepal)",             "val": 8091},
    {"name": "Gasherbrum I (Pakistan/China)",   "val": 8080},
    {"name": "Broad Peak (Pakistan/China)",     "val": 8051},
    {"name": "Gasherbrum II (Pakistan/China)",  "val": 8035},
    {"name": "Shishapangma (China)",            "val": 8027},
    {"name": "Elbrus (Russland)",               "val": 5642},
    {"name": "Vinson-Massiv (Antarktis)",       "val": 4892},
    {"name": "Puncak Jaya (Indonesien)",        "val": 4884},
    {"name": "Matterhorn (Schweiz/Italien)",    "val": 4478},
    {"name": "Mount Whitney (USA)",             "val": 4421},
    {"name": "Großglockner (Österreich)",       "val": 3798},
    {"name": "Fujisan (Japan)",                 "val": 3776},
    {"name": "Monte Olympus (Griechenland)",    "val": 2918},
    {"name": "Ben Nevis (Vereinigtes Königreich)", "val": 1345},
    {"name": "Zugspitze (Deutschland)",         "val": 2962},
    {"name": "Kebnekaise (Schweden)",           "val": 2099},
    {"name": "Monte Rosa (Schweiz/Italien)",    "val": 4634},
    {"name": "Dom (Schweiz)",                   "val": 4545},
    {"name": "Pikes Peak (USA, Colorado)",      "val": 4302},
    {"name": "Tafelberg (Südafrika)",           "val": 1086},
    {"name": "Snæfellsjökull (Island)",         "val": 1446},
])
report("geo_hl", "geo_berghoehen", n, len(geo_hl["geo_berghoehen"]["items"]))

n = extend_hl(geo_hl, "geo_vulkan_hoehen", [
    {"name": "Sajama (Bolivien)",               "val": 6542},
    {"name": "Chimborazo (Ecuador)",            "val": 6268},
    {"name": "Sangay (Ecuador)",                "val": 5230},
    {"name": "Tungurahua (Ecuador)",            "val": 5023},
    {"name": "Wrangell (Alaska, USA)",          "val": 4317},
    {"name": "Colima (Mexiko)",                 "val": 3860},
    {"name": "Mauna Loa (Hawaii, USA)",         "val": 4169},
    {"name": "Mauna Kea (Hawaii, USA)",         "val": 4207},
    {"name": "Rainier (Washington, USA)",       "val": 4392},
    {"name": "Pico de Teide (Spanien)",         "val": 3715},
    {"name": "Nyiragongo (Kongo/DRC)",          "val": 3470},
    {"name": "Merapi (Indonesien)",             "val": 2930},
    {"name": "Ol Doinyo Lengai (Tansania)",     "val": 2960},
    {"name": "Shishaldin (Alaska, USA)",        "val": 2857},
    {"name": "Ruapehu (Neuseeland)",            "val": 2797},
    {"name": "Mt. St. Helens (USA)",            "val": 2549},
    {"name": "Galeras (Kolumbien)",             "val": 4276},
    {"name": "Piton de la Fournaise (Réunion)", "val": 2632},
    {"name": "Mayon (Philippinen)",             "val": 2462},
    {"name": "Katmai (Alaska, USA)",            "val": 2047},
    {"name": "Stromboli (Italien)",             "val": 924},
    {"name": "Santorini / Thera (Griechenland)","val": 584},
    {"name": "Krakatau (Indonesien)",           "val": 813},
])
report("geo_hl", "geo_vulkan_hoehen", n, len(geo_hl["geo_vulkan_hoehen"]["items"]))

n = extend_hl(geo_hl, "geo_erdbeben_magnitude", [
    {"name": "Ecuador/Kolumbien 1906",          "val": 87},
    {"name": "Rat Islands 1965 (Alaska)",       "val": 87},
    {"name": "Lissabon 1755 (Portugal)",        "val": 87},
    {"name": "Alaska 1957 (Aleutinen)",         "val": 86},
    {"name": "Nias 2005 (Indonesien)",          "val": 86},
    {"name": "Assam/Tibet 1950",                "val": 86},
    {"name": "Sumatra 2012",                    "val": 86},
    {"name": "Chile 1922",                      "val": 85},
    {"name": "Kamtschatka 1923 (Russland)",     "val": 84},
    {"name": "Mexico City 1985",                "val": 81},
    {"name": "San Francisco 1906 (USA)",        "val": 79},
    {"name": "Sichuan 2008 (China)",            "val": 79},
    {"name": "Nepal 2015",                      "val": 78},
    {"name": "Türkei 2023 (Kahramanmaraş)",     "val": 78},
    {"name": "Tangshan 1976 (China)",           "val": 76},
    {"name": "Kuril-Inseln 2006 (Russland)",    "val": 80},
    {"name": "Athen 1999 (Griechenland)",       "val": 59},
    {"name": "Christchurch 2011 (Neuseeland)",  "val": 63},
    {"name": "L'Aquila 2009 (Italien)",         "val": 63},
    {"name": "Armenia 1988",                    "val": 69},
])
report("geo_hl", "geo_erdbeben_magnitude", n, len(geo_hl["geo_erdbeben_magnitude"]["items"]))

n = extend_hl(geo_hl, "geo_vei_ausbruch", [
    {"name": "Toba (~74.000 v. Chr., Indonesien)",          "val": 8},
    {"name": "Yellowstone (~640.000 v. Chr., USA)",         "val": 8},
    {"name": "Samalas / Rinjani 1257 (Indonesien)",         "val": 7},
    {"name": "Huaynaputina 1600 (Peru)",                    "val": 6},
    {"name": "Laki 1783 (Island)",                          "val": 6},
    {"name": "Santa María 1902 (Guatemala)",                "val": 6},
    {"name": "Novarupta 1912 (Alaska, USA)",                "val": 6},
    {"name": "Hunga Tonga 2022 (Tonga)",                    "val": 5},
    {"name": "Merapi 2010 (Indonesien)",                    "val": 4},
    {"name": "Ruapehu 1996 (Neuseeland)",                   "val": 3},
    {"name": "Pelée 1902 (Martinique)",                     "val": 4},
    {"name": "Sarychev 2009 (Russland)",                    "val": 4},
    {"name": "Raikoke 2019 (Russland)",                     "val": 4},
    {"name": "Sinabung 2014 (Indonesien)",                  "val": 4},
    {"name": "Galeras 1993 (Kolumbien)",                    "val": 3},
    {"name": "Llaima 2008 (Chile)",                         "val": 3},
    {"name": "Ontake 2014 (Japan)",                         "val": 3},
    {"name": "Eldgjá 934 (Island)",                         "val": 6},
    {"name": "Unzen 1792 (Japan)",                          "val": 3},
    {"name": "Stromboli (anhaltend, Italien)",              "val": 1},
])
report("geo_hl", "geo_vei_ausbruch", n, len(geo_hl["geo_vei_ausbruch"]["items"]))

n = extend_hl(geo_hl, "geo_kontinentaldrift", [
    {"name": "Tonga-Platte",                    "val": 240},
    {"name": "Cocos-Platte",                    "val": 90},
    {"name": "Philippinische Platte",           "val": 52},
    {"name": "Karibische Platte",               "val": 20},
    {"name": "Südamerikanische Platte",         "val": 19},
    {"name": "Afrikanische Platte",             "val": 21},
    {"name": "Scotia-Platte",                   "val": 22},
    {"name": "Amur-Platte",                     "val": 26},
    {"name": "Somalische Platte",               "val": 18},
    {"name": "Anatolische Platte",              "val": 24},
    {"name": "Karolinische Platte",             "val": 25},
    {"name": "Rivera-Platte",                   "val": 40},
    {"name": "Sunda-Platte",                    "val": 12},
    {"name": "Mariana-Platte",                  "val": 35},
    {"name": "Easter-Platte",                   "val": 67},
    {"name": "Birmanische Platte",              "val": 10},
    {"name": "Indische Platte",                 "val": 55},
    {"name": "Adriatische Platte",              "val": 5},
])
report("geo_hl", "geo_kontinentaldrift", n, len(geo_hl["geo_kontinentaldrift"]["items"]))

n = extend_hl(geo_hl, "geo_schmelztemperatur", [
    {"name": "Wolfram (W)",                     "val": 3422},
    {"name": "Rhenium (Re)",                    "val": 3186},
    {"name": "Osmium (Os)",                     "val": 3033},
    {"name": "Tantal (Ta)",                     "val": 2996},
    {"name": "Molybdän (Mo)",                   "val": 2623},
    {"name": "Platin (Pt)",                     "val": 1768},
    {"name": "Titan (Ti)",                      "val": 1668},
    {"name": "Nickeleisen (Meteorit)",          "val": 1600},
    {"name": "Nikkel (Ni)",                     "val": 1455},
    {"name": "Kobalt (Co)",                     "val": 1495},
    {"name": "Magnetit (Fe₃O₄)",               "val": 1590},
    {"name": "Pyroxen (Mineral)",               "val": 1100},
    {"name": "Halit / Steinsalz (NaCl)",        "val": 801},
    {"name": "Kupfer (Cu)",                     "val": 1085},
    {"name": "Gold (Au)",                       "val": 1064},
    {"name": "Silber (Ag)",                     "val": 962},
    {"name": "Aluminium (Al)",                  "val": 660},
    {"name": "Obsidian (vulkanisches Glas)",    "val": 850},
    {"name": "Blei (Pb)",                       "val": 327},
    {"name": "Zinn (Sn)",                       "val": 232},
    {"name": "Bismut (Bi)",                     "val": 271},
    {"name": "Zink (Zn)",                       "val": 420},
    {"name": "Gallium (Ga)",                    "val": 30},
])
report("geo_hl", "geo_schmelztemperatur", n, len(geo_hl["geo_schmelztemperatur"]["items"]))

n = extend_hl(geo_hl, "geo_tsunami_hoehe", [
    {"name": "Sanriku 1896 (Japan)",            "val": 38},
    {"name": "Sanriku 1933 (Japan)",            "val": 28},
    {"name": "Hokkaido 1993 (Japan)",           "val": 31},
    {"name": "Alaska 1946 (Aleutinen)",         "val": 35},
    {"name": "Alaska 1957 (Aleutinen)",         "val": 23},
    {"name": "Lissabon 1755 (Portugal/Marokko)","val": 30},
    {"name": "Messina 1908 (Italien)",          "val": 12},
    {"name": "Peru 1868",                       "val": 21},
    {"name": "Nicaragua 1992",                  "val": 10},
    {"name": "Flores 1992 (Indonesien)",        "val": 26},
    {"name": "Java 2006 (Indonesien)",          "val": 21},
    {"name": "Krakatau 1883 (Indonesien)",      "val": 37},
    {"name": "Solomon Islands 2007",            "val": 12},
    {"name": "Samoa 2009",                      "val": 14},
    {"name": "Chile 2010 (Maule)",              "val": 29},
    {"name": "Tōhoku 2011, Miyako (Japan)",     "val": 40},
    {"name": "Neuseeland 2016 (Kaikōura)",      "val": 7},
    {"name": "Türkei 2020 (Izmir/Samos)",       "val": 4},
    {"name": "Banda Aceh 2004 (Indonesien)",    "val": 30},
    {"name": "Haiti 2010 (Karibik)",            "val": 3},
    {"name": "Aleutinen 1965 (Alaska)",         "val": 10},
    {"name": "Nankaidō 1707 Hōei (Japan)",      "val": 25},
])
report("geo_hl", "geo_tsunami_hoehe", n, len(geo_hl["geo_tsunami_hoehe"]["items"]))

save("geo_hl.json", geo_hl)
print("  ✓ geo_hl.json gespeichert")

# ═══════════════════════════════════════════════════════════════════
# 2) GEO MATCH
# ═══════════════════════════════════════════════════════════════════
print("\n🗺️  geo_match.json")
geo_match = load("geo_match.json")

n = extend_match(geo_match, "geo_gesteinsarten", [
    {"n": "Basalt",             "c": "Magmatisch"},
    {"n": "Rhyolith",           "c": "Magmatisch"},
    {"n": "Obsidian",           "c": "Magmatisch"},
    {"n": "Gabbro",             "c": "Magmatisch"},
    {"n": "Andesit",            "c": "Magmatisch"},
    {"n": "Diorit",             "c": "Magmatisch"},
    {"n": "Peridotit",          "c": "Magmatisch"},
    {"n": "Vulkanischer Tuff",  "c": "Magmatisch"},
    {"n": "Gneis",              "c": "Metamorph"},
    {"n": "Schiefer",           "c": "Metamorph"},
    {"n": "Quarzit",            "c": "Metamorph"},
    {"n": "Phyllit",            "c": "Metamorph"},
    {"n": "Eklogit",            "c": "Metamorph"},
    {"n": "Serpentinit",        "c": "Metamorph"},
    {"n": "Hornfels",           "c": "Metamorph"},
    {"n": "Amphibolit",         "c": "Metamorph"},
    {"n": "Kalkstein",          "c": "Sedimentaer"},
    {"n": "Tonstein",           "c": "Sedimentaer"},
    {"n": "Konglomerat",        "c": "Sedimentaer"},
    {"n": "Breccie",            "c": "Sedimentaer"},
    {"n": "Kreide",             "c": "Sedimentaer"},
    {"n": "Steinkohle",         "c": "Sedimentaer"},
    {"n": "Evaporit (Gips)",    "c": "Sedimentaer"},
    {"n": "Travertin",          "c": "Sedimentaer"},
    {"n": "Ölschiefer",         "c": "Sedimentaer"},
    {"n": "Dolomit",            "c": "Sedimentaer"},
])
report("geo_match", "geo_gesteinsarten", n, len(geo_match["geo_gesteinsarten"]["items"]))

n = extend_match(geo_match, "geo_tektonik", [
    {"n": "Japan",              "c": "Eurasische Platte"},
    {"n": "Indien",             "c": "Indische Platte"},
    {"n": "Saudi-Arabien",      "c": "Arabische Platte"},
    {"n": "Philippinen",        "c": "Philippinische Platte"},
    {"n": "Mexiko",             "c": "Nordamerikanische Platte"},
    {"n": "Peru",               "c": "Südamerikanische Platte"},
    {"n": "Argentinien",        "c": "Südamerikanische Platte"},
    {"n": "Kenia",              "c": "Afrikanische Platte"},
    {"n": "Ägypten",            "c": "Afrikanische Platte"},
    {"n": "Nigeria",            "c": "Afrikanische Platte"},
    {"n": "USA (Atlantikküste)","c": "Nordamerikanische Platte"},
    {"n": "Kanada",             "c": "Nordamerikanische Platte"},
    {"n": "Frankreich",         "c": "Eurasische Platte"},
    {"n": "China (Ostküste)",   "c": "Eurasische Platte"},
    {"n": "Hawaii",             "c": "Pazifische Platte"},
    {"n": "Jamaika",            "c": "Karibische Platte"},
    {"n": "Neuseeland",         "c": "Australische Platte"},
    {"n": "Türkei",             "c": "Anatolische Platte"},
    {"n": "Kasachstan",         "c": "Eurasische Platte"},
    {"n": "Indonesien (Java)",  "c": "Sunda-Platte"},
    {"n": "Grönland",           "c": "Nordamerikanische Platte"},
    {"n": "Tonga",              "c": "Australische Platte"},
])
report("geo_match", "geo_tektonik", n, len(geo_match["geo_tektonik"]["items"]))

n = extend_match(geo_match, "geo_mineralien", [
    {"n": "Halit (Steinsalz)",              "c": "Nahrungsmittel und Chemie"},
    {"n": "Magnetit",                       "c": "Eisenerz und Magnete"},
    {"n": "Quarz (Siliziumdioxid)",         "c": "Elektronik und Glasherstellung"},
    {"n": "Feldspat (Orthoklas)",           "c": "Keramik und Glasindustrie"},
    {"n": "Glimmer (Muskovit)",             "c": "Elektroisolierung und Kosmetik"},
    {"n": "Fluorit",                        "c": "Optik und Flusssäureproduktion"},
    {"n": "Baryt",                          "c": "Bohrspülung und Farben"},
    {"n": "Gips",                           "c": "Baumaterial und Medizin"},
    {"n": "Apatit",                         "c": "Düngemittel (Phosphorquelle)"},
    {"n": "Pyrit (Katzengold)",             "c": "Schwefelsäure-Herstellung"},
    {"n": "Talkum",                         "c": "Kosmetik und Papierbeschichtung"},
    {"n": "Kaolin",                         "c": "Porzellan und Papierherstellung"},
    {"n": "Beryll (Smaragd/Aquamarin)",     "c": "Schmuck und Industrie"},
    {"n": "Turmalin",                       "c": "Schmuck und Piezoelektrizität"},
    {"n": "Malachit",                       "c": "Schmuck und historische Pigmente"},
    {"n": "Olivin",                         "c": "Stahlproduktion und Schmuck"},
    {"n": "Zirkon",                         "c": "Keramik und radiometrische Datierung"},
    {"n": "Serpentin",                      "c": "Bausteine und Dekorationsmaterial"},
    {"n": "Hämatit",                        "c": "Eisenerz und Pigmente (Rötelstift)"},
    {"n": "Chalcopyrit (Kupferkies)",       "c": "Kupfergewinnung"},
    {"n": "Galenit (Bleiglanz)",            "c": "Bleigewinnung"},
    {"n": "Sphalerit",                      "c": "Zinkgewinnung"},
])
report("geo_match", "geo_mineralien", n, len(geo_match["geo_mineralien"]["items"]))

n = extend_match(geo_match, "geo_fossil_zeitalter", [
    {"n": "Ammonit",                "c": "Mesozoikum"},
    {"n": "Belemnit",               "c": "Mesozoikum"},
    {"n": "Tyrannosaurus rex",      "c": "Mesozoikum"},
    {"n": "Stegosaurus",            "c": "Mesozoikum"},
    {"n": "Brachiosaurus",          "c": "Mesozoikum"},
    {"n": "Triceratops",            "c": "Mesozoikum"},
    {"n": "Iguanodon",              "c": "Mesozoikum"},
    {"n": "Pterosaurier",           "c": "Mesozoikum"},
    {"n": "Ichthyosaurier",         "c": "Mesozoikum"},
    {"n": "Plesiosaur",             "c": "Mesozoikum"},
    {"n": "Smilodon (Säbelzahntiger)", "c": "Känozoikum"},
    {"n": "Megaloceros (Riesenhirsch)", "c": "Känozoikum"},
    {"n": "Wollnashorn",            "c": "Känozoikum"},
    {"n": "Dodo",                   "c": "Känozoikum"},
    {"n": "Australopithecus",       "c": "Känozoikum"},
    {"n": "Homo erectus",           "c": "Känozoikum"},
    {"n": "Graptolith",             "c": "Paläozoikum"},
    {"n": "Seelilie (Crinoide)",    "c": "Paläozoikum"},
    {"n": "Dunkleosteus (Panzerfisch)", "c": "Paläozoikum"},
    {"n": "Ichthyostega",           "c": "Paläozoikum"},
    {"n": "Diplocaulus",            "c": "Paläozoikum"},
    {"n": "Baumfarn (Karbon)",      "c": "Paläozoikum"},
    {"n": "Eurypterus (Seeskorpion)","c": "Paläozoikum"},
    {"n": "Orthoceras (Nautiloid)", "c": "Paläozoikum"},
])
report("geo_match", "geo_fossil_zeitalter", n, len(geo_match["geo_fossil_zeitalter"]["items"]))

n = extend_match(geo_match, "geo_landschaft_ursprung", [
    {"n": "Grand Canyon (USA)",         "c": "Fluviale Erosion"},
    {"n": "Sanddüne (Sahara)",          "c": "Äolische Sedimentation"},
    {"n": "Lössebene (China)",          "c": "Äolische Sedimentation"},
    {"n": "Atoll (Malediven)",          "c": "Korallenriff-Wachstum"},
    {"n": "Karstlandschaft (Karst)",    "c": "Chemische Verwitterung"},
    {"n": "Sinkhole (Zentralamerika)",  "c": "Karst-Auflösung"},
    {"n": "Caldera (Kratersee)",        "c": "Vulkanischer Kollaps"},
    {"n": "Vulkankegel (Stratovolcan)", "c": "Magmatismus"},
    {"n": "Tafelberg / Mesa (USA)",     "c": "Differenzielle Erosion"},
    {"n": "Playa / Salzfläche",         "c": "Trockenheit und Verdunstung"},
    {"n": "Drumlin",                    "c": "Glaziale Sedimentation"},
    {"n": "Esker",                      "c": "Subglazialer Schmelzwasserfluss"},
    {"n": "Schwemmfächer",              "c": "Flusssedimentation"},
    {"n": "Terrassenlandschaft",        "c": "Fluviale Erosion und Hebung"},
    {"n": "Watt (Nordsee)",             "c": "Gezeitenprozesse"},
    {"n": "Stranddüne",                 "c": "Küstenprozesse und Wind"},
    {"n": "Stalaktiten-Höhle",          "c": "Chemische Verwitterung"},
    {"n": "Ringstruktur (Nördlinger Ries)", "c": "Meteoriteneinschlag"},
    {"n": "Riff (Great Barrier Reef)",  "c": "Korallenriff-Wachstum"},
    {"n": "Schwemmebene / Alluvialebene", "c": "Flusssedimentation"},
    {"n": "Horst und Graben (Rift Valley)", "c": "Tektonisches Rifting"},
    {"n": "Talus / Schuttkegel",        "c": "Schwerkraft-Massenbewegung"},
])
report("geo_match", "geo_landschaft_ursprung", n, len(geo_match["geo_landschaft_ursprung"]["items"]))

n = extend_match(geo_match, "geo_kontinent_platte", [
    {"n": "Arabische Halbinsel",        "c": "Arabische Platte"},
    {"n": "Indischer Subkontinent",     "c": "Indische Platte"},
    {"n": "Ostanatolien (Türkei)",      "c": "Anatolische Platte"},
    {"n": "Russland / Sibirien",        "c": "Eurasische Platte"},
    {"n": "Skandinavien",               "c": "Eurasische Platte"},
    {"n": "Iberische Halbinsel",        "c": "Eurasische Platte"},
    {"n": "Zentralafrika",              "c": "Afrikanische Platte"},
    {"n": "Ostafrika (Rift Valley)",    "c": "Somalische Platte"},
    {"n": "Neuseeland",                 "c": "Australische Platte"},
    {"n": "Great Barrier Reef",         "c": "Australische Platte"},
    {"n": "Grönland",                   "c": "Nordamerikanische Platte"},
    {"n": "Karibische Inseln",          "c": "Karibische Platte"},
    {"n": "Philippinen",                "c": "Philippinische Platte"},
    {"n": "Hawaii (Inseln)",            "c": "Pazifische Platte"},
    {"n": "Galapagos-Inseln",           "c": "Nazca-Platte"},
    {"n": "Antarktis gesamt",           "c": "Antarktische Platte"},
    {"n": "Westantarktis (Halbinsel)",  "c": "Antarktische Platte"},
    {"n": "Mittelatlantischer Rücken (West)", "c": "Nordamerikanische Platte"},
    {"n": "Mittelatlantischer Rücken (Ost)",  "c": "Eurasische Platte"},
    {"n": "Island",                     "c": "Nordamerikanische Platte"},
    {"n": "Japan (Hauptinseln)",        "c": "Amur-Platte"},
    {"n": "Tonga-Inseln",               "c": "Australische Platte"},
])
report("geo_match", "geo_kontinent_platte", n, len(geo_match["geo_kontinent_platte"]["items"]))

n = extend_match(geo_match, "geo_hoehlen_land", [
    {"n": "Jewel Cave",                     "c": "USA"},
    {"n": "Wind Cave",                      "c": "USA"},
    {"n": "Lechuguilla Cave",               "c": "USA"},
    {"n": "Sistema Sac Actun",              "c": "Mexiko"},
    {"n": "Höhle von Altamira (Felsmalerei)", "c": "Spanien"},
    {"n": "Lascaux (Felsmalerei)",          "c": "Frankreich"},
    {"n": "Gouffre Berger",                 "c": "Frankreich"},
    {"n": "Réseau Jean Bernard",            "c": "Frankreich"},
    {"n": "Eisriesenwelt",                  "c": "Österreich"},
    {"n": "Dachstein Rieseneishöhle",       "c": "Österreich"},
    {"n": "Škocjanske Jame",                "c": "Slowenien"},
    {"n": "Postojna",                       "c": "Slowenien"},
    {"n": "Aggtelek-Karst (Baradla)",       "c": "Ungarn"},
    {"n": "Reed Flute Cave (Ludigyan)",     "c": "China"},
    {"n": "Zhijin Cave",                    "c": "China"},
    {"n": "Clearwater Cave",                "c": "Malaysia"},
    {"n": "Sarawak Chamber (Deer Cave)",    "c": "Malaysia"},
    {"n": "Tham Luang",                     "c": "Thailand"},
    {"n": "Waitomo Glühwürmchen-Höhle",     "c": "Neuseeland"},
    {"n": "Shakta Veryovkina",              "c": "Georgien"},
    {"n": "Krubera-Voronya",                "c": "Georgien"},
    {"n": "Cueva del Milodón",              "c": "Chile"},
    {"n": "Optimisticheskaya Cave",         "c": "Ukraine"},
])
report("geo_match", "geo_hoehlen_land", n, len(geo_match["geo_hoehlen_land"]["items"]))

n = extend_match(geo_match, "geo_mineral_kristall", [
    {"n": "Pyrit",              "c": "Kubisch"},
    {"n": "Fluorit",            "c": "Kubisch"},
    {"n": "Gold",               "c": "Kubisch"},
    {"n": "Magnetit",           "c": "Kubisch"},
    {"n": "Granat",             "c": "Kubisch"},
    {"n": "Galenit (Bleiglanz)","c": "Kubisch"},
    {"n": "Spinell",            "c": "Kubisch"},
    {"n": "Turmalin",           "c": "Trigonal / Hexagonal"},
    {"n": "Calcit",             "c": "Trigonal / Hexagonal"},
    {"n": "Korund (Rubin/Saphir)", "c": "Trigonal / Hexagonal"},
    {"n": "Hämatit",            "c": "Trigonal / Hexagonal"},
    {"n": "Dolomit",            "c": "Trigonal / Hexagonal"},
    {"n": "Rutil",              "c": "Tetragonal"},
    {"n": "Zirkon",             "c": "Tetragonal"},
    {"n": "Kassiterit (Zinnstein)", "c": "Tetragonal"},
    {"n": "Schwefel",           "c": "Orthorhombisch"},
    {"n": "Baryt",              "c": "Orthorhombisch"},
    {"n": "Aragonit",           "c": "Orthorhombisch"},
    {"n": "Olivin",             "c": "Orthorhombisch"},
    {"n": "Topas",              "c": "Orthorhombisch"},
    {"n": "Gips",               "c": "Monoklin"},
    {"n": "Orthoklas (Feldspat)","c": "Monoklin"},
    {"n": "Glimmer (Muskovit)", "c": "Monoklin"},
    {"n": "Jadeit (Jadeit-Jade)","c": "Monoklin"},
    {"n": "Azurit",             "c": "Monoklin"},
    {"n": "Albit",              "c": "Triklin"},
    {"n": "Labradorit",         "c": "Triklin"},
    {"n": "Rhodonit",           "c": "Triklin"},
    {"n": "Kyanit",             "c": "Triklin"},
])
report("geo_match", "geo_mineral_kristall", n, len(geo_match["geo_mineral_kristall"]["items"]))

n = extend_match(geo_match, "geo_gebirge_entstehung", [
    {"n": "Rocky Mountains (USA/Kanada)",    "c": "Ozean-Kontinent-Subduktion"},
    {"n": "Kaskaden (USA)",                  "c": "Ozean-Kontinent-Subduktion"},
    {"n": "Japanische Inseln",               "c": "Ozean-Ozean-Subduktion"},
    {"n": "Aleuten (Alaska)",                "c": "Ozean-Ozean-Subduktion"},
    {"n": "Kuril-Inseln (Russland)",         "c": "Ozean-Ozean-Subduktion"},
    {"n": "Ural (Russland)",                 "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Appalachen (USA)",                "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Atlas (Nordafrika)",              "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Pyrenäen (Spanien/Frankreich)",   "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Karpaten (Osteuropa)",            "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Kaukasus",                        "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Karakorum (Pakistan/China)",      "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Hindukusch (Afghanistan)",        "c": "Kontinent-Kontinent-Kollision"},
    {"n": "Hawaii (Inselkette)",             "c": "Hotspot-Vulkanismus"},
    {"n": "Kanarische Inseln (Spanien)",     "c": "Hotspot-Vulkanismus"},
    {"n": "Kapverdische Inseln",             "c": "Hotspot-Vulkanismus"},
    {"n": "Island",                          "c": "Rift-Zone (Divergenz)"},
    {"n": "Ostafrikanischer Grabenbruch",    "c": "Rift-Zone (Divergenz)"},
    {"n": "Mittelatlantischer Rücken",       "c": "Rift-Zone (Divergenz)"},
    {"n": "Skandinavisches Gebirge",         "c": "Alter Kaledonischer Faltengürtel"},
    {"n": "Sibirische Tiefebene (Schild)",   "c": "Tektonischer Schild (stabil)"},
])
report("geo_match", "geo_gebirge_entstehung", n, len(geo_match["geo_gebirge_entstehung"]["items"]))

save("geo_match.json", geo_match)
print("  ✓ geo_match.json gespeichert")

# ═══════════════════════════════════════════════════════════════════
# 3) SPORT HL
# ═══════════════════════════════════════════════════════════════════
print("\n🏅 sport_hl.json")
sport_hl = load("sport_hl.json")

n = extend_hl(sport_hl, "sport_hochsprung_rekorde", [
    {"name": "Mutaz Essa Barshim (Katar, 2014)",    "val": 241},
    {"name": "Ivan Ukhov (Russland, 2014)",          "val": 241},
    {"name": "Patrik Sjöberg (Schweden, 1987)",      "val": 242},
    {"name": "Charles Austin (USA, Atlanta 1996)",   "val": 239},
    {"name": "Yaroslav Rybakov (Russland, 2005)",    "val": 240},
    {"name": "Stefan Holm (Schweden, 2005)",         "val": 240},
    {"name": "Rudolf Povarnitsyn (UdSSR, 1985)",     "val": 240},
    {"name": "Vyacheslav Voronin (Russland, 2000)",  "val": 239},
    {"name": "Hollis Conway (USA, 1989)",             "val": 238},
    {"name": "Derek Drouin (Kanada, London 2012)",   "val": 238},
    {"name": "Erik Kynard (USA, London 2012)",       "val": 238},
    {"name": "Andriy Protsenko (Ukraine, 2014)",     "val": 237},
    {"name": "Kyriakos Ioannou (Zypern, 2007)",      "val": 235},
    {"name": "Jesse Williams (USA, 2012 WM)",        "val": 236},
    {"name": "Majd Eddin Ghazal (Syrien, 2017)",     "val": 238},
    {"name": "Hamish Kerr (Neuseeland, Paris 2024)", "val": 236},
    {"name": "Blanka Vlasic (Kroatien, 2009 WR Frau)", "val": 208},
    {"name": "Anna Chicherova (Russland, 2011)",     "val": 206},
    {"name": "Hestrie Cloete (Südafrika, 2003)",     "val": 206},
    {"name": "Yelena Slesarenko (Russland, Athen 04)", "val": 206},
    {"name": "Ruth Beitia (Spanien, 2016)",          "val": 197},
    {"name": "Antonietta Di Martino (Italien, 2007)", "val": 201},
])
report("sport_hl", "sport_hochsprung_rekorde", n, len(sport_hl["sport_hochsprung_rekorde"]["items"]))

n = extend_hl(sport_hl, "sport_olympia_goldmedaillen", [
    {"name": "Mark Spitz (Schwimmen, USA, 1972)",       "val": 9},
    {"name": "Carl Lewis (Leichtathletik, USA)",        "val": 9},
    {"name": "Nikolai Andrianov (Turnen, UdSSR)",       "val": 7},
    {"name": "Boris Shakhlin (Turnen, UdSSR)",          "val": 7},
    {"name": "Vitali Scherbo (Turnen, Belarus)",        "val": 6},
    {"name": "Marit Bjørgen (Skilanglauf, Norwegen)",   "val": 8},
    {"name": "Ole Einar Bjørndalen (Biathlon, Norwegen)","val": 8},
    {"name": "Bjørn Dæhlie (Skilanglauf, Norwegen)",    "val": 8},
    {"name": "Birgit Fischer (Kanu, Deutschland)",      "val": 8},
    {"name": "Usain Bolt (Leichtathletik, Jamaika)",    "val": 8},
    {"name": "Matt Biondi (Schwimmen, USA)",            "val": 8},
    {"name": "Jenny Thompson (Schwimmen, USA)",         "val": 8},
    {"name": "Aladár Gerevich (Fechten, Ungarn)",       "val": 7},
    {"name": "Edoardo Mangiarotti (Fechten, Italien)",  "val": 6},
    {"name": "Ian Thorpe (Schwimmen, Australien)",      "val": 5},
    {"name": "Nadia Comăneci (Turnen, Rumänien)",       "val": 5},
    {"name": "Agnes Keleti (Turnen, Ungarn)",           "val": 5},
    {"name": "Takashi Ono (Turnen, Japan)",             "val": 5},
    {"name": "Lasse Virén (Leichtathletik, Finnland)",  "val": 4},
    {"name": "Emil Zátopek (Leichtathletik, Tschechien)", "val": 4},
    {"name": "Michael Johnson (Leichtathletik, USA)",   "val": 4},
    {"name": "Amy Van Dyken (Schwimmen, USA)",          "val": 4},
])
report("sport_hl", "sport_olympia_goldmedaillen", n, len(sport_hl["sport_olympia_goldmedaillen"]["items"]))

n = extend_hl(sport_hl, "sport_fussball_marktwert", [
    {"name": "Vinicius Jr. (Real Madrid, 2024)",        "val": 180},
    {"name": "Lamine Yamal (FC Barcelona, 2024)",       "val": 180},
    {"name": "Bukayo Saka (Arsenal, 2024)",             "val": 140},
    {"name": "Jamal Musiala (Bayern München, 2024)",    "val": 150},
    {"name": "Phil Foden (Manchester City, 2024)",      "val": 150},
    {"name": "Florian Wirtz (Bayer Leverkusen, 2024)",  "val": 130},
    {"name": "Pedri (FC Barcelona, 2024)",              "val": 100},
    {"name": "Rodri (Manchester City, 2024)",           "val": 130},
    {"name": "Harry Kane (Bayern München, 2024)",       "val": 100},
    {"name": "Federico Valverde (Real Madrid, 2024)",   "val": 100},
    {"name": "Trent Alexander-Arnold (2024)",           "val": 80},
    {"name": "Rúben Dias (Manchester City, 2024)",      "val": 80},
    {"name": "Virgil van Dijk (Liverpool, 2024)",       "val": 50},
    {"name": "Neymar Jr. (Al-Hilal, 2024)",             "val": 45},
    {"name": "Lionel Messi (Inter Miami, 2024)",        "val": 35},
    {"name": "Cristiano Ronaldo (Al-Nassr, 2024)",      "val": 15},
    {"name": "Aitana Bonmatí (FC Barcelona, Frauen 24)", "val": 30},
    {"name": "Alexia Putellas (FC Barcelona, Frauen)",  "val": 20},
    {"name": "Robert Lewandowski (FC Barcelona, 2024)", "val": 20},
    {"name": "Antoine Griezmann (Atlético, 2024)",      "val": 30},
    {"name": "Alisson Becker (Liverpool, 2024)",        "val": 50},
])
report("sport_hl", "sport_fussball_marktwert", n, len(sport_hl["sport_fussball_marktwert"]["items"]))

n = extend_hl(sport_hl, "sport_gewichtheben_rekorde", [
    {"name": "Ilya Ilyin (Kasachstan, 94 kg, 2012)",    "val": 418},
    {"name": "Pyrros Dimas (Griechenland, 85 kg)",      "val": 360},
    {"name": "Kakhi Kakhiashvili (GRE, 99 kg, 1996)",   "val": 412},
    {"name": "Naim Süleymanoğlu (Türkei, 60 kg, 1988)", "val": 342},
    {"name": "Halil Mutlu (Türkei, 56 kg, 2000)",       "val": 305},
    {"name": "Hossein Rezazadeh (Iran, +105 kg, 2004)", "val": 472},
    {"name": "Shi Zhiyong (China, 73 kg, 2021)",        "val": 364},
    {"name": "Lyu Xiaojun (China, 81 kg, 2021)",        "val": 374},
    {"name": "Chen Lijun (China, 67 kg, 2019)",         "val": 352},
    {"name": "Meredith Alford (USA, Frau 87 kg)",       "val": 249},
    {"name": "Liu Chunhong (China, Frau 69 kg, 2008)",  "val": 286},
    {"name": "Chen Yanqing (China, Frau 58 kg, 2006)",  "val": 261},
    {"name": "Li Ping (China, Frau 49 kg, 2019)",       "val": 218},
    {"name": "Rahimov Nijat (Aserbaidschan, 77 kg)",    "val": 379},
    {"name": "Apti Auhadov (Deutschland, 85 kg)",       "val": 370},
    {"name": "Andrei Aramnau (Belarus, 105 kg, 2008)",  "val": 436},
])
report("sport_hl", "sport_gewichtheben_rekorde", n, len(sport_hl["sport_gewichtheben_rekorde"]["items"]))

n = extend_hl(sport_hl, "sport_tore_saison", [
    {"name": "Gerd Müller (Bayern, Bundesliga 1971/72)", "val": 40},
    {"name": "Robert Lewandowski (Bayern, BL 2020/21)", "val": 41},
    {"name": "Dixie Dean (Everton, Division 1 1927/28)", "val": 60},
    {"name": "Jimmy McGrory (Celtic, 1931/32)",          "val": 52},
    {"name": "Alan Shearer (Blackburn, PL 1994/95)",     "val": 34},
    {"name": "Andrew Cole (Newcastle, PL 1993/94)",      "val": 34},
    {"name": "Mohamed Salah (Liverpool, PL 2017/18)",    "val": 32},
    {"name": "Cristiano Ronaldo (PL 2022/23)",           "val": 12},
    {"name": "Eusébio (Benfica, Liga NOS 1967/68)",      "val": 42},
    {"name": "Neymar Jr. (PSG, Ligue 1 2017/18)",        "val": 19},
    {"name": "Kylian Mbappé (PSG, Ligue 1 2018/19)",     "val": 33},
    {"name": "Ronaldo Lima (Barcellona, La Liga 1996/97)","val": 34},
    {"name": "Thierry Henry (Arsenal, PL 2004/05)",      "val": 25},
    {"name": "Ruud van Nistelrooy (ManUtd, PL 2002/03)", "val": 25},
    {"name": "Cristiano Ronaldo (CL Rekord, 2013/14)",   "val": 17},
    {"name": "Messi (CL Rekord je Saison, 2011/12)",     "val": 14},
    {"name": "Filippo Inzaghi (Serie A, 2000/01)",       "val": 24},
])
report("sport_hl", "sport_tore_saison", n, len(sport_hl["sport_tore_saison"]["items"]))

save("sport_hl.json", sport_hl)
print("  ✓ sport_hl.json gespeichert")

# ═══════════════════════════════════════════════════════════════════
# 4) SPORT MATCH
# ═══════════════════════════════════════════════════════════════════
print("\n⚽ sport_match.json")
sport_match = load("sport_match.json")

n = extend_match(sport_match, "sport_teamgroesse", [
    {"n": "Volleyball",             "c": "6 Spieler"},
    {"n": "Rugby Union",            "c": "15 Spieler"},
    {"n": "Rugby League",           "c": "13 Spieler"},
    {"n": "Handball",               "c": "7 Spieler"},
    {"n": "Eishockey",              "c": "6 Spieler"},
    {"n": "Baseball",               "c": "9 Spieler"},
    {"n": "Softbal",                "c": "9 Spieler"},
    {"n": "Cricket",                "c": "11 Spieler"},
    {"n": "Feldhockey",             "c": "11 Spieler"},
    {"n": "Wasserball",             "c": "7 Spieler"},
    {"n": "Tennis (Einzel)",        "c": "1 Spieler"},
    {"n": "Golf",                   "c": "1 Spieler"},
    {"n": "Polo",                   "c": "4 Spieler"},
    {"n": "Curling",                "c": "4 Spieler"},
    {"n": "Bobsleigh (Vierer)",     "c": "4 Spieler"},
    {"n": "Rudern (Achter)",        "c": "9 Spieler"},
    {"n": "Badminton (Einzel)",     "c": "1 Spieler"},
    {"n": "Kanu (Einer)",           "c": "1 Spieler"},
    {"n": "Boxen",                  "c": "1 Spieler"},
    {"n": "Lacrosse (Feld)",        "c": "10 Spieler"},
    {"n": "Netball",                "c": "7 Spieler"},
    {"n": "Gaelic Football",        "c": "15 Spieler"},
])
report("sport_match", "sport_teamgroesse", n, len(sport_match["sport_teamgroesse"]["items"]))

n = extend_match(sport_match, "sport_olympia_standort", [
    {"n": "Olympiade 1904",     "c": "St. Louis"},
    {"n": "Olympiade 1908",     "c": "London"},
    {"n": "Olympiade 1912",     "c": "Stockholm"},
    {"n": "Olympiade 1920",     "c": "Antwerpen"},
    {"n": "Olympiade 1924",     "c": "Paris"},
    {"n": "Olympiade 1928",     "c": "Amsterdam"},
    {"n": "Olympiade 1932",     "c": "Los Angeles"},
    {"n": "Olympiade 1948",     "c": "London"},
    {"n": "Olympiade 1952",     "c": "Helsinki"},
    {"n": "Olympiade 1956",     "c": "Melbourne"},
    {"n": "Olympiade 1960",     "c": "Rom"},
    {"n": "Olympiade 1964",     "c": "Tokio"},
    {"n": "Olympiade 1968",     "c": "Mexiko-Stadt"},
    {"n": "Olympiade 1972",     "c": "München"},
    {"n": "Olympiade 1976",     "c": "Montréal"},
    {"n": "Olympiade 1980",     "c": "Moskau"},
    {"n": "Olympiade 1984",     "c": "Los Angeles"},
    {"n": "Olympiade 1988",     "c": "Seoul"},
    {"n": "Olympiade 1992",     "c": "Barcelona"},
    {"n": "Olympiade 1996",     "c": "Atlanta"},
    {"n": "Olympiade 2000",     "c": "Sydney"},
    {"n": "Olympiade 2004",     "c": "Athen"},
    {"n": "Olympiade 2008",     "c": "Peking"},
    {"n": "Olympiade 2012",     "c": "London"},
    {"n": "Olympiade 2016",     "c": "Rio de Janeiro"},
    {"n": "Olympiade 2020/21",  "c": "Tokio"},
    {"n": "Olympiade 2024",     "c": "Paris"},
    {"n": "Olympiade 2028",     "c": "Los Angeles"},
])
report("sport_match", "sport_olympia_standort", n, len(sport_match["sport_olympia_standort"]["items"]))

n = extend_match(sport_match, "sport_olympisch", [
    {"n": "Badminton",          "c": "Ja"},
    {"n": "Bogenschießen",      "c": "Ja"},
    {"n": "Boxen",              "c": "Ja"},
    {"n": "Gewichtheben",       "c": "Ja"},
    {"n": "Judo",               "c": "Ja"},
    {"n": "Klettern (Sport)",   "c": "Ja"},
    {"n": "Rudern",             "c": "Ja"},
    {"n": "Taekwondo",          "c": "Ja"},
    {"n": "Tischtennis",        "c": "Ja"},
    {"n": "Triathlon",          "c": "Ja"},
    {"n": "Rugby Sevens",       "c": "Ja"},
    {"n": "Baseball/Softball",  "c": "Ja"},
    {"n": "Breakdance",         "c": "Ja"},
    {"n": "Karate",             "c": "Nein"},
    {"n": "Cricket",            "c": "Nein"},
    {"n": "American Football",  "c": "Nein"},
    {"n": "Netball",            "c": "Nein"},
    {"n": "Squash",             "c": "Nein"},
    {"n": "Bowling",            "c": "Nein"},
    {"n": "Motorsport (F1)",    "c": "Nein"},
    {"n": "Schach",             "c": "Nein"},
    {"n": "Muay Thai",          "c": "Nein"},
    {"n": "Pool-Billard",       "c": "Nein"},
    {"n": "Darts",              "c": "Nein"},
])
report("sport_match", "sport_olympisch", n, len(sport_match["sport_olympisch"]["items"]))

n = extend_match(sport_match, "sport_nationalsport_match", [
    {"n": "Eishockey",                  "c": "Kanada"},
    {"n": "Aussie Rules Football",      "c": "Australien"},
    {"n": "Muay Thai",                  "c": "Thailand"},
    {"n": "Sepak Takraw",               "c": "Malaysia"},
    {"n": "Hurling",                    "c": "Irland"},
    {"n": "Pesäpallo (Finnball)",       "c": "Finnland"},
    {"n": "Bandy",                      "c": "Russland"},
    {"n": "Buzkashi (Reitsport)",       "c": "Afghanistan"},
    {"n": "Lacrosse",                   "c": "Kanada (indigene Tradition)"},
    {"n": "Polo",                       "c": "Argentinien"},
    {"n": "Capoeira",                   "c": "Brasilien"},
    {"n": "Taekwondo",                  "c": "Südkorea"},
    {"n": "Pelota Vasca",               "c": "Spanien (Baskenland)"},
    {"n": "Baseball",                   "c": "USA"},
    {"n": "Basketball",                 "c": "USA"},
    {"n": "Kendo",                      "c": "Japan"},
    {"n": "Floorball",                  "c": "Schweden"},
    {"n": "Korfball",                   "c": "Niederlande"},
    {"n": "Wushu (Kung Fu)",            "c": "China"},
])
report("sport_match", "sport_nationalsport_match", n, len(sport_match["sport_nationalsport_match"]["items"]))

n = extend_match(sport_match, "sport_rekordhalter", [
    {"n": "200m Männer (19,19 s, Berlin 2009)",     "c": "Usain Bolt"},
    {"n": "400m Männer (43,03 s, Rio 2016)",        "c": "Wayde van Niekerk"},
    {"n": "800m Männer (1:40,91, London 2012)",     "c": "David Rudisha"},
    {"n": "1500m Männer (3:26,00, 1998)",           "c": "Hicham El Guerrouj"},
    {"n": "5000m Männer (12:35,36, 2020)",          "c": "Joshua Cheptegei"},
    {"n": "Marathon Männer (2:00:35, 2023)",        "c": "Kelvin Kiptum"},
    {"n": "110m Hürden (12,80 s, 2012)",            "c": "Aries Merritt"},
    {"n": "400m Hürden Männer (45,94 s, Tokio)",   "c": "Karsten Warholm"},
    {"n": "Stabhochsprung (6,24 m, 2024)",         "c": "Mondo Duplantis"},
    {"n": "Dreisprung Männer (18,29 m, 1995)",     "c": "Jonathan Edwards"},
    {"n": "Kugelstoßen Männer (23,56 m, 2021)",    "c": "Ryan Crouser"},
    {"n": "Diskuswurf Männer (74,08 m, 1986)",     "c": "Jürgen Schult"},
    {"n": "Hammerwurf Männer (86,74 m, 1986)",     "c": "Yuriy Sedykh"},
    {"n": "Speerwurf Männer (98,48 m, 1996)",      "c": "Jan Železný"},
    {"n": "100m Frauen (10,49 s, Seoul 1988)",     "c": "Florence Griffith-Joyner"},
    {"n": "400m Hürden Frauen (50,68 s, 2022)",    "c": "Sydney McLaughlin-Levrone"},
    {"n": "Stabhochsprung Frauen (5,06 m, 2024)",  "c": "Katie Moon / Mondo"},
    {"n": "Marathon Frauen (2:09:56, 2024)",       "c": "Ruth Chepngetich"},
])
report("sport_match", "sport_rekordhalter", n, len(sport_match["sport_rekordhalter"]["items"]))

n = extend_match(sport_match, "sport_disziplin_kategorie", [
    {"n": "Salto rückwärts",        "c": "Turnen"},
    {"n": "Pirouette",              "c": "Eiskunstlauf"},
    {"n": "Axel-Sprung",            "c": "Eiskunstlauf"},
    {"n": "Slalom-Kurve",           "c": "Skifahren"},
    {"n": "Telemark-Landung",       "c": "Skispringen"},
    {"n": "Kraulen",                "c": "Schwimmen"},
    {"n": "Delphin-Stoß",           "c": "Schwimmen"},
    {"n": "Pferdchen / Brustschwimmen", "c": "Schwimmen"},
    {"n": "Kranzbackhand",          "c": "Tennis"},
    {"n": "Serve & Volley",         "c": "Tennis"},
    {"n": "Plyometrisches Training", "c": "Leichtathletik"},
    {"n": "Fosbury-Flop",           "c": "Hochsprung"},
    {"n": "O'Brien-Technik",        "c": "Kugelstoßen"},
    {"n": "Crouch Start (Blocks)",  "c": "Sprint"},
    {"n": "Kufen-Schritt",          "c": "Eisschnelllauf"},
    {"n": "Jab-Cross-Kombination",  "c": "Boxen"},
    {"n": "Ippon (Ganzkörperwurf)", "c": "Judo"},
    {"n": "Randori",                "c": "Judo"},
    {"n": "Kata-Ausführung",        "c": "Karate"},
    {"n": "Hakama tragen",          "c": "Kendo"},
    {"n": "Seitenwindschiessen",    "c": "Bogenschießen"},
    {"n": "Laufschritt (Kadenz)",   "c": "Leichtathletik"},
])
report("sport_match", "sport_disziplin_kategorie", n, len(sport_match["sport_disziplin_kategorie"]["items"]))

n = extend_match(sport_match, "sport_sportart_kontinent", [
    {"n": "Kabaddi",                    "c": "Asien"},
    {"n": "Sepak Takraw",               "c": "Asien"},
    {"n": "Kendo",                      "c": "Asien"},
    {"n": "Polo (Ursprung Persien)",    "c": "Asien"},
    {"n": "Capoeira",                   "c": "Südamerika"},
    {"n": "Cachibol",                   "c": "Südamerika"},
    {"n": "Pelota",                     "c": "Europa"},
    {"n": "Curling",                    "c": "Europa"},
    {"n": "Schwingen (Ringen)",         "c": "Europa"},
    {"n": "Cricket",                    "c": "Europa"},
    {"n": "Hurling",                    "c": "Europa"},
    {"n": "Gaelic Football",            "c": "Europa"},
    {"n": "Baseball",                   "c": "Nordamerika"},
    {"n": "Lacrosse",                   "c": "Nordamerika"},
    {"n": "Basketball",                 "c": "Nordamerika"},
    {"n": "Volleyball",                 "c": "Nordamerika"},
    {"n": "Aussie Rules Football",      "c": "Australien/Ozeanien"},
    {"n": "Oztag",                      "c": "Australien/Ozeanien"},
    {"n": "Dambe (Boxen)",              "c": "Afrika"},
    {"n": "Nguni-Stockkampf",           "c": "Afrika"},
    {"n": "Savate",                     "c": "Europa"},
])
report("sport_match", "sport_sportart_kontinent", n, len(sport_match["sport_sportart_kontinent"]["items"]))

save("sport_match.json", sport_match)
print("  ✓ sport_match.json gespeichert")

# ═══════════════════════════════════════════════════════════════════
# 5) ASTRO HL
# ═══════════════════════════════════════════════════════════════════
print("\n🔭 astro_hl.json")
astro_hl = load("astro_hl.json")

n = extend_hl(astro_hl, "astro_planet_groesse", [
    {"name": "Sonne",                           "val": 1391000},
    {"name": "Ganymed (Jupitermond)",           "val": 5268},
    {"name": "Titan (Saturnmond)",              "val": 5150},
    {"name": "Callisto (Jupitermond)",          "val": 4820},
    {"name": "Io (Jupitermond)",                "val": 3642},
    {"name": "Mond (Erdmond)",                  "val": 3474},
    {"name": "Europa (Jupitermond)",            "val": 3122},
    {"name": "Triton (Neptunmond)",             "val": 2706},
    {"name": "Pluto (Zwergplanet)",             "val": 2376},
    {"name": "Eris (Zwergplanet)",              "val": 2326},
    {"name": "Titania (Uranusmond)",            "val": 1578},
    {"name": "Oberon (Uranusmond)",             "val": 1523},
    {"name": "Rhea (Saturnmond)",               "val": 1527},
    {"name": "Iapetus (Saturnmond)",            "val": 1469},
    {"name": "Makemake (Zwergplanet)",          "val": 1434},
    {"name": "Charon (Plutomon)",               "val": 1212},
    {"name": "Umbriel (Uranusmond)",            "val": 1169},
    {"name": "Ariel (Uranusmond)",              "val": 1158},
    {"name": "Dione (Saturnmond)",              "val": 1123},
    {"name": "Ceres (Zwergplanet)",             "val": 945},
    {"name": "Vesta (Asteroid)",                "val": 525},
    {"name": "Pallas (Asteroid)",               "val": 512},
    {"name": "Hygiea (Asteroid)",               "val": 430},
])
report("astro_hl", "astro_planet_groesse", n, len(astro_hl["astro_planet_groesse"]["items"]))

n = extend_hl(astro_hl, "astro_monde_anzahl", [
    {"name": "Orcus (Zwergplanet)",     "val": 1},
    {"name": "Gonggong (Zwergplanet)",  "val": 1},
    {"name": "Salacia (Zwergplanet)",   "val": 1},
    {"name": "Varda (Zwergplanet)",     "val": 1},
    {"name": "Sedna (TNO)",             "val": 0},
    {"name": "Varuna (TNO)",            "val": 0},
    {"name": "Asteroid Ida",            "val": 1},
    {"name": "Asteroid Eugenia",        "val": 2},
    {"name": "Asteroid Sylvia",         "val": 2},
    {"name": "Asteroid Elektra",        "val": 3},
    {"name": "Asteroid Camilla",        "val": 2},
    {"name": "Ixion (Zwergplanet)",     "val": 0},
    {"name": "Chaos (TNO)",             "val": 0},
])
report("astro_hl", "astro_monde_anzahl", n, len(astro_hl["astro_monde_anzahl"]["items"]))

n = extend_hl(astro_hl, "astro_sonnenentfernung", [
    {"name": "Chiron (Zentaur)",        "val": 2631},
    {"name": "Pholus (Zentaur)",        "val": 3051},
    {"name": "Chariklo (Zentaur)",      "val": 2363},
    {"name": "Nessus (Zentaur)",        "val": 3679},
    {"name": "Orcus (Zwergplanet)",     "val": 5835},
    {"name": "2002 MS4 (Zwergplanet)", "val": 6137},
    {"name": "Altjira (TNO)",           "val": 6582},
    {"name": "2004 GV9 (TNO)",         "val": 6284},
    {"name": "Gonggong (Zwergplanet)", "val": 10022},
    {"name": "2002 TX300 (TNO)",       "val": 6434},
])
report("astro_hl", "astro_sonnenentfernung", n, len(astro_hl["astro_sonnenentfernung"]["items"]))

n = extend_hl(astro_hl, "astro_temperaturen", [
    {"name": "Sonnenkorona",                            "val": 1000000},
    {"name": "Sonnenkern",                              "val": 15000000},
    {"name": "Proxima Centauri (Oberfläche)",           "val": 3042},
    {"name": "Beteigeuze (Oberfläche)",                 "val": 3500},
    {"name": "Rigel (Oberfläche)",                      "val": 12130},
    {"name": "Sirius A (Oberfläche)",                   "val": 9940},
    {"name": "Alpha Centauri A (Oberfläche)",           "val": 5790},
    {"name": "Ganymede (Oberfläche)",                   "val": -163},
    {"name": "Callisto (Oberfläche)",                   "val": -139},
    {"name": "Rhea (Saturnmond)",                       "val": -174},
    {"name": "Triton (Neptunmond)",                     "val": -235},
    {"name": "Merkur (Tagseite Maximum)",               "val": 430},
])
report("astro_hl", "astro_temperaturen", n, len(astro_hl["astro_temperaturen"]["items"]))

save("astro_hl.json", astro_hl)
print("  ✓ astro_hl.json gespeichert")

# ═══════════════════════════════════════════════════════════════════
# 6) ASTRO MATCH
# ═══════════════════════════════════════════════════════════════════
print("\n🌌 astro_match.json")
astro_match = load("astro_match.json")

n = extend_match(astro_match, "astro_planeten", [
    {"n": "Pluto",      "c": "Erster bekannter Zwergplanet — 5 Monde (inkl. Charon)"},
    {"n": "Ceres",      "c": "Einziger Zwergplanet im Asteroidengürtel"},
    {"n": "Eris",       "c": "Massereicher als Pluto — löste Pluto-Debatte aus"},
    {"n": "Titan",      "c": "Einziger Mond mit dichter Atmosphäre (Saturn)"},
    {"n": "Europa",     "c": "Flüssiger Ozean unter Eisschicht (Jupiter)"},
    {"n": "Io",         "c": "Vulkanischster Körper im Sonnensystem (Jupiter)"},
    {"n": "Ganymed",    "c": "Größter Mond im Sonnensystem (Jupiter)"},
    {"n": "Triton",     "c": "Einziger großer Mond mit rückläufiger Umlaufbahn (Neptun)"},
    {"n": "Enceladus",  "c": "Wassergeysire — Kandidat für außerirdisches Leben (Saturn)"},
    {"n": "Phobos",     "c": "Wird in ~50 Mio. Jahren auf den Mars stürzen"},
    {"n": "Charon",     "c": "Fast so groß wie Pluto — bilden Doppelsystem"},
    {"n": "Makemake",   "c": "Zwergplanet ohne nachgewiesene Atmosphäre"},
    {"n": "Haumea",     "c": "Schnellst rotierender Zwergplanet (3,9h Rotation)"},
    {"n": "Vesta",      "c": "Hellster Asteroid — mit bloßem Auge sichtbar"},
    {"n": "Pallas",     "c": "Zweitgrößter Asteroid im Hauptgürtel"},
    {"n": "Hygiea",     "c": "Viertgrößter Asteroid — kugelförmig"},
    {"n": "Sedna",      "c": "Extremer Orbit — möglicherweise aus Oortscher Wolke"},
    {"n": "Gonggong",   "c": "Roter Transneptunischer Körper mit einem Mond"},
    {"n": "Quaoar",     "c": "Hat einen Ring — außergewöhnlich weit vom Körper entfernt"},
    {"n": "Proxima Centauri b", "c": "Nächster bekannter Exoplanet (4,2 Lichtjahre)"},
    {"n": "TRAPPIST-1e","c": "Potenziell bewohnbarer Exoplanet in der habitablen Zone"},
    {"n": "Kepler-452b","c": "\"Erd-Cousin\" — ähnliche Größe wie Erde, G-Typ-Stern"},
    {"n": "Hot Jupiter",    "c": "Klasse Gasriesen in extrem engen Sternenorbits"},
    {"n": "Ultima Thule / Arrokoth", "c": "Kontaktzwilling — von New Horizons fotografiert"},
    {"n": "Asteroid Ida",   "c": "Erster Asteroid mit bestätigtem eigenem Mond (Dactyl)"},
])
report("astro_match", "astro_planeten", n, len(astro_match["astro_planeten"]["items"]))

save("astro_match.json", astro_match)
print("  ✓ astro_match.json gespeichert")

# ═══════════════════════════════════════════════════════════════════
# 7) ARCHAEOLOGIE MATCH (verbleibende 18-19-Item-Modi)
# ═══════════════════════════════════════════════════════════════════
print("\n🏛️  archaeologie_match.json")
arch_match = load("archaeologie_match.json")

n = extend_match(arch_match, "werkzeuge", [
    {"n": "Knochennadel",                   "c": "Paläolithikum"},
    {"n": "Muschelspitze (Burin)",          "c": "Paläolithikum"},
    {"n": "Klingenkern",                    "c": "Mesolithikum"},
    {"n": "Mikrolith",                      "c": "Mesolithikum"},
    {"n": "Knochenangel",                   "c": "Mesolithikum"},
    {"n": "Flachhacke aus Geweih",          "c": "Neolithikum"},
    {"n": "Sichelstein (Obsidian-Einlagen)", "c": "Neolithikum"},
    {"n": "Kupfermeißel",                   "c": "Kupferzeit (Chalkolithikum)"},
    {"n": "Arsenikbronze-Schwert",          "c": "Frühe Bronzezeit"},
    {"n": "Zinnbronze-Speer",               "c": "Bronzezeit"},
    {"n": "Gussform für Bronzeäxte",        "c": "Bronzezeit"},
    {"n": "Eisenpflug",                     "c": "Eisenzeit"},
    {"n": "Keltisches Latène-Schwert",      "c": "Eisenzeit"},
    {"n": "Gladius (römisches Kurzschwert)","c": "Römerzeit"},
    {"n": "Wasserrad (röm. Typ)",           "c": "Römerzeit"},
    {"n": "Hypokaustenziegel",              "c": "Römerzeit"},
    {"n": "Arabische Astrolabe",            "c": "Mittelalter"},
    {"n": "Armbrust",                       "c": "Mittelalter"},
    {"n": "Schiesspulver-Kanone",           "c": "Mittelalter"},
    {"n": "Buchdruckmechanismus (Gutenberg)", "c": "Frühe Neuzeit"},
    {"n": "Dampfmaschinen-Kolben (Watt)",   "c": "Industriezeitalter"},
])
report("arch_match", "werkzeuge", n, len(arch_match["werkzeuge"]["items"]))

n = extend_match(arch_match, "schriften", [
    {"n": "Phönizisches Alphabet",      "c": "Phönizien"},
    {"n": "Demotische Schrift",         "c": "Ägypten"},
    {"n": "Koptische Schrift",          "c": "Ägypten"},
    {"n": "Aramäische Schrift",         "c": "Mesopotamien / Levante"},
    {"n": "Sanskrit / Brahmi-Schrift",  "c": "Indien"},
    {"n": "Chinesische Orakelknochenschrift", "c": "China"},
    {"n": "Chinesische Siegelschrift",  "c": "China"},
    {"n": "Japanische Kanji",           "c": "Japan"},
    {"n": "Koreanisches Hangul",        "c": "Korea"},
    {"n": "Runen (Futhark)",            "c": "Germanen / Wikinger"},
    {"n": "Ogham-Schrift",              "c": "Kelten (Irland)"},
    {"n": "Aztekische Bilderschrift",   "c": "Azteken"},
    {"n": "Maya-Glyphen",               "c": "Maya"},
    {"n": "Inka-Quipu (Knotenschrift)", "c": "Inka"},
    {"n": "Protosinaïtische Schrift",   "c": "Levante / Sinai"},
    {"n": "Elamische Linearschrift",    "c": "Iran / Elam"},
    {"n": "Luwische Hieroglyphen",      "c": "Hethiter / Anatolien"},
    {"n": "Meroitische Schrift",        "c": "Nubien / Meroe"},
    {"n": "Äthiopisches Ge'ez (Fidäl)", "c": "Äthiopien"},
    {"n": "Rongorongo",                 "c": "Osterinsel"},
    {"n": "Indus-Schrift",              "c": "Indus-Zivilisation"},
])
report("arch_match", "schriften", n, len(arch_match["schriften"]["items"]))

n = extend_match(arch_match, "bestattungsriten", [
    {"n": "Sati (Witwenverbrennung)",       "c": "Hindus"},
    {"n": "Terrakotta-Grabbeigaben",        "c": "China (Han)"},
    {"n": "Steinkreis-Hügelgrab",           "c": "Kelten"},
    {"n": "Pyramidengrab für Pharao",       "c": "Ägypten"},
    {"n": "Megalith-Ganggrab",              "c": "Neolithikum Europa"},
    {"n": "Sky Burial (Luftbestattung)",    "c": "Tibet / Buddhisten"},
    {"n": "Kartonnage mit Amuletten",       "c": "Ägypten"},
    {"n": "Brandbestattung mit Urne",       "c": "Römer"},
    {"n": "Katakomben-Bestattung",          "c": "Römer / Urkirche"},
    {"n": "Türme des Schweigens",           "c": "Zoroastrismus (Persien)"},
    {"n": "Schamanengrab mit Trommel",      "c": "Sibirische Kulturen"},
    {"n": "Schiffsbestattung in Hügeln",    "c": "Wikinger"},
    {"n": "Gräber mit Fußgolf (Azteken)",   "c": "Azteken"},
    {"n": "Gefäßbestattung (Hockergrab)",   "c": "Jungsteinzeit Europa"},
    {"n": "Beinhäuser / Ossuar",            "c": "Christentum / Europa"},
    {"n": "Natürliche Höhlengräber",        "c": "Paläolithikum"},
    {"n": "Mastaba-Grab",                   "c": "Ägypten"},
    {"n": "Dolmen-Grab",                    "c": "Megalithkulturen"},
    {"n": "Tumulus (Grabhügel)",            "c": "Thraker / Skythen"},
    {"n": "Schachtgräber mit Gold",         "c": "Mykene"},
    {"n": "Sarkophag aus Marmor",           "c": "Römer / Griechenland"},
])
report("arch_match", "bestattungsriten", n, len(arch_match["bestattungsriten"]["items"]))

n = extend_match(arch_match, "waehrungen", [
    {"n": "Shekel",                         "c": "Mesopotamien / Israel"},
    {"n": "Stater",                         "c": "Griechenland"},
    {"n": "Drachme",                        "c": "Griechenland"},
    {"n": "Solidus",                        "c": "Byzanz"},
    {"n": "Antoninian",                     "c": "Römer (3. Jh.)"},
    {"n": "Sesterz",                        "c": "Römer"},
    {"n": "Aureus",                         "c": "Römer"},
    {"n": "Dirham",                         "c": "Islamisches Kalifat"},
    {"n": "Dinar",                          "c": "Islamisches Kalifat"},
    {"n": "Kaurimuscheln (großer Handel)",  "c": "Westafrika / Ozeanien"},
    {"n": "Wampum-Perlenstickerei",         "c": "Nordamerika (Irokesen)"},
    {"n": "Jade-Beil als Zahlungsmittel",   "c": "Mesoamerika (Maya)"},
    {"n": "Kakaobohnen",                    "c": "Azteken"},
    {"n": "Gewürznelken als Tauschmittel",  "c": "Gewürzinseln (Indienhandel)"},
    {"n": "Hacksilber",                     "c": "Wikinger"},
    {"n": "Seidenstoffe als Währung",       "c": "China (Seidenstraße)"},
    {"n": "Feathered Quill (Pelzhandel)",   "c": "Kanada (Kolonialzeit)"},
    {"n": "Kupferbarren (Manilla)",         "c": "Westafrika"},
    {"n": "Glasperlen (europäischer Handel)", "c": "Subsahara-Afrika"},
    {"n": "Salz (Salzstraßen)",             "c": "Äthiopien / Antike"},
    {"n": "Florin",                         "c": "Florenz (Mittelalter)"},
])
report("arch_match", "waehrungen", n, len(arch_match["waehrungen"]["items"]))

n = extend_match(arch_match, "tempel_ordnungen", [
    {"n": "Theseustempel (Athen)",          "c": "Dorisch"},
    {"n": "Hephaisteion (Athen)",           "c": "Dorisch"},
    {"n": "Tempel von Paestum (S-Italien)", "c": "Dorisch"},
    {"n": "Tempel von Aphaia (Ägina)",      "c": "Dorisch"},
    {"n": "Artemistempel Ephesos",          "c": "Ionisch"},
    {"n": "Nike-Tempel Akropolis",          "c": "Ionisch"},
    {"n": "Tempel des Apollo (Didyma)",     "c": "Ionisch"},
    {"n": "Tempel des Zeus (Olympia)",      "c": "Dorisch"},
    {"n": "Lysikrates-Monument (Athen)",    "c": "Korinthisch"},
    {"n": "Tempel der Vesta (Rom)",         "c": "Korinthisch"},
    {"n": "Pantheon (Rom) — Vorhalle",      "c": "Korinthisch"},
    {"n": "Tempel des Castor (Forum Rom.)", "c": "Korinthisch"},
    {"n": "Maison Carrée (Nîmes)",          "c": "Korinthisch"},
    {"n": "Trajanssäule (Basis)",           "c": "Toskanisch"},
    {"n": "Pont du Gard (Bögen)",           "c": "Toskanisch"},
    {"n": "Titusbogen (Rom)",               "c": "Toskanisch"},
    {"n": "Konstantinsbogen (Rom)",         "c": "Komposit"},
    {"n": "Septimius-Severus-Bogen",        "c": "Komposit"},
    {"n": "Tempel des Bacchus (Baalbek)",   "c": "Korinthisch"},
    {"n": "Tempel von Baalbek (Jupiter)",   "c": "Korinthisch"},
    {"n": "Hadrianstor (Athen)",            "c": "Korinthisch"},
])
report("arch_match", "tempel_ordnungen", n, len(arch_match["tempel_ordnungen"]["items"]))

n = extend_match(arch_match, "zufallsfunde", [
    {"n": "Lascaux-Höhle (1940)",               "c": "Kinder (beim Spielen)"},
    {"n": "Höhle von Altamira (1868)",           "c": "Wanderer / Jäger"},
    {"n": "Laetoli-Fußabdrücke (1976)",         "c": "Wissenschaftliche Expedition"},
    {"n": "Sutton Hoo (1938)",                   "c": "Grundstückeigentümer"},
    {"n": "Dōngbāo (Elefant-Elfenbein-Lager)",  "c": "Bauarbeiter"},
    {"n": "Ötzi (1991)",                         "c": "Wanderer"},
    {"n": "Ägyptische Mumien in Tanis",          "c": "Archäologen-Expedition"},
    {"n": "Tollund-Mann (1950)",                 "c": "Torfstecher"},
    {"n": "Grauballe-Mann (1952)",               "c": "Torfstecher"},
    {"n": "Windeby-Mädchen (1952)",              "c": "Torfstecher"},
    {"n": "Babenberger-Gruft (Wien)",            "c": "Bauarbeiter"},
    {"n": "Pompeji (Ausgrabungen ab 1748)",      "c": "Bauarbeiter"},
    {"n": "Sixtinische Kapellen-Inschriften",    "c": "Restauratoren"},
    {"n": "Rosetta-Stein (1799)",                "c": "Napoleons Soldaten"},
    {"n": "Qumran-Schriftrollen (1947)",         "c": "Hirtenknabe"},
    {"n": "Nag-Hammadi-Texte (1945)",            "c": "Bauer"},
    {"n": "Vinland-Karte (gefunden 1957)",       "c": "Buchhändler"},
    {"n": "Sipán-Königsgräber (1987, Peru)",     "c": "Polizei verfolgte Grabräuber"},
    {"n": "Antikythera-Mechanismus (1900/01)",   "c": "Schwammtaucher"},
    {"n": "Thera-Bronzefiguren (Ägäis)",        "c": "Taucher"},
    {"n": "Lanzarote-Höhlenmalereien",           "c": "Speleologen"},
])
report("arch_match", "zufallsfunde", n, len(arch_match["zufallsfunde"]["items"]))

n = extend_match(arch_match, "welterbe_gefahr", [
    {"n": "Ruinen von Aleppo (Syrien)",         "c": "Krieg"},
    {"n": "Altstadtmauern von Hebron",          "c": "Politischer Konflikt"},
    {"n": "Machu Picchu (Peru)",                "c": "Overtourismus"},
    {"n": "Venedig (Italien)",                  "c": "Klimawandel / Tourismus"},
    {"n": "Everest-Gebiet (Nepal)",             "c": "Tourismus / Müllverschmutzung"},
    {"n": "Great Barrier Reef (Australien)",    "c": "Klimawandel (Korallenbleiche)"},
    {"n": "Donautal (Deutschland/Österreich)", "c": "Infrastrukturprojekte"},
    {"n": "Kolosseum (Rom)",                    "c": "Erschütterungen / Tourismus"},
    {"n": "Santorin-Caldera",                   "c": "Overtourismus"},
    {"n": "Okavangodelta (Botswana)",           "c": "Klimawandel / Wasserentnahme"},
    {"n": "Sundarbans (Bangladesch/Indien)",    "c": "Klimawandel (Meeresspiegel)"},
    {"n": "Chan Chan (Peru)",                   "c": "Klimawandel (El Niño-Regen)"},
    {"n": "Prambanan-Tempel (Indonesien)",      "c": "Erdbeben"},
    {"n": "Borobudur (Indonesien)",             "c": "Vulkanismus / Tourismus"},
    {"n": "Cholula-Pyramide (Mexiko)",          "c": "Urbanisierung"},
    {"n": "Kakadu (Australien)",                "c": "Invasive Tierarten"},
    {"n": "Lascaux II — Replikation nötig",     "c": "Schimmelbefall durch Tourismus"},
    {"n": "Timbuktu (Mali)",                    "c": "Islamistischer Terror"},
    {"n": "Bamiyan-Buddhas (Afghanistan)",      "c": "Zerstört durch Taliban 2001"},
    {"n": "Altstadt von Mosul (Irak)",          "c": "Krieg (IS-Zerstörung 2015)"},
    {"n": "Bam-Zitadelle (Iran)",               "c": "Erdbeben (2003)"},
    {"n": "Ephesus (Türkei)",                   "c": "Tourismus / Erosion"},
])
report("arch_match", "welterbe_gefahr", n, len(arch_match["welterbe_gefahr"]["items"]))

save("archaeologie_match.json", arch_match)
print("  ✓ archaeologie_match.json gespeichert")

# ═══════════════════════════════════════════════════════════════════
# ABSCHLUSS
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'='*55}")
print(f"✅ patch_265 abgeschlossen — {total_added} Items hinzugefügt")
print(f"{'='*55}\n")
