#!/usr/bin/env python3
# patch_tiere_routing.py — Phase 227 Step 1
# Adds "tiere" category to MODE_CATS + 21 MODES entries (10 Pin + 11 H/L)
# All titles prefixed with [BETA]

import re

SRC = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"

with open(SRC, "r", encoding="utf-8") as f:
    content = f.read()

# ──────────────────────────────────────────────────────────────────────────────
# PATCH 1: Add tiere category to MODE_CATS (after sport entry)
# ──────────────────────────────────────────────────────────────────────────────
OLD_SPORT_LINE = '  sport:{label:"Sport",icon:"\\u{1F3C6}",modes:["stadium","jersey","crest","comp_olympics","comp_flight","hl_b_wm","b1","b2","b4","b6","b7","b9","b11","b17","b19","b20","derby_hotspots","eishockey_nationen","f1_historisch","tdf_paesse","olympia_winter_historie","wm_gastgeber","wm_finalstadien","weltmeister_nationen","fussball_legenden","road_to_2026","frauen_wm_meilensteine","sommerspiele_metropolen","winter_exoten_klassiker","olympische_rekorde","olympia_hoehe","boykott_spiele","em_gastgeber_historie","em_finalstadien","f1_map","stadium_map","uk_nationalsport_off","uk_hohe_stadien","uk_leichtathletik_wm"],cost:0},'

NEW_SPORT_PLUS_TIERE = OLD_SPORT_LINE + """
  tiere:{label:"Tiere & Natur",icon:"\\u{1F98B}",modes:[
    "uk_tiere_endemisch","uk_tiere_bigfive","uk_tiere_grosskatzen",
    "uk_tiere_invasiv","uk_tiere_vogelzug","uk_tiere_haustiere",
    "uk_tiere_nationaltier_pin","uk_tiere_primaten",
    "uk_tiere_hai","uk_tiere_baeren",
    "hl_tiere_gewicht_land","hl_tiere_gewicht_meer",
    "hl_tiere_speed_land","hl_tiere_speed_luft","hl_tiere_speed_wasser",
    "hl_tiere_lebenserwartung","hl_tiere_traechtigkeit",
    "hl_tiere_wurf","hl_tiere_gift",
    "hl_tiere_population","hl_tiere_schlaf"
  ],cost:0},"""

if OLD_SPORT_LINE not in content:
    print("ERROR: sport MODE_CATS line not found – check gen.py")
    exit(1)

content = content.replace(OLD_SPORT_LINE, NEW_SPORT_PLUS_TIERE, 1)
print("✓ PATCH 1: tiere category added to MODE_CATS")

# ──────────────────────────────────────────────────────────────────────────────
# PATCH 2: Add MODES entries for all 21 tiere modes
# Insert before the closing ]; of the MODES array (after b60 entry)
# ──────────────────────────────────────────────────────────────────────────────
MODES_ANCHOR = '    {id:"b60",icon:"\\u{1F303}",title:"\\u{1F9EA} Nacht-Satellit",         group:"map_mode",prompt:"Welche Region leuchtet nachts am hellsten?",             desc:"Lichtintensitaet auf Satellitenkarten"}\n];'

TIERE_MODES = """    {id:"b60",icon:"\\u{1F303}",title:"\\u{1F9EA} Nacht-Satellit",         group:"map_mode",prompt:"Welche Region leuchtet nachts am hellsten?",             desc:"Lichtintensitaet auf Satellitenkarten"},
    /* === Phase 227: Tiere & Natur — Pin Modi (10) === */
    {id:"uk_tiere_endemisch",      icon:"\\u{1F98E}",title:"[BETA] Endemische Arten",       group:"tiere",prompt:"\\u{1F4CD} Wo lebt dieses Tier exklusiv?",           desc:"Lemur, Kiwi, Komodo-Waran — nur an einem Ort"},
    {id:"uk_tiere_bigfive",        icon:"\\u{1F418}",title:"[BETA] Big Five Afrikas",        group:"tiere",prompt:"\\u{1F4CD} In welchem Nationalpark lebt die Big Five?",desc:"Serengeti, Kruger, Masai Mara und mehr"},
    {id:"uk_tiere_grosskatzen",    icon:"\\u{1F42F}",title:"[BETA] Großkatzen-Habitate",     group:"tiere",prompt:"\\u{1F4CD} Wo ist das letzte Refugium dieser Großkatze?",desc:"Tiger, Jaguar, Schneeleopard — letzte Wildnis"},
    {id:"uk_tiere_invasiv",        icon:"\\u{1F40D}",title:"[BETA] Invasive Arten",          group:"tiere",prompt:"\\u{1F4CD} Aus welchem Land stammt diese invasive Art?", desc:"Ursprungsland invasiver Tiere weltweit"},
    {id:"uk_tiere_vogelzug",       icon:"\\u{1F426}",title:"[BETA] Vogelzug-Knotenpunkte",  group:"tiere",prompt:"\\u{1F4CD} Wo liegt dieser wichtige Vogelzug-Rastplatz?",desc:"Wichtige Rastpl\\u00e4tze auf globalen Zugrouten"},
    {id:"uk_tiere_haustiere",      icon:"\\u{1F436}",title:"[BETA] Ursprung der Haustiere",  group:"tiere",prompt:"\\u{1F4CD} Wo wurde dieses Tier zuerst domestiziert?",  desc:"Hund, Katze, Pferd — Wiege der Domestizierung"},
    {id:"uk_tiere_nationaltier_pin",icon:"\\u{1F98A}",title:"[BETA] Nationaltiere Pin",      group:"tiere",prompt:"\\u{1F4CD} In welchem Land ist dieses Tier ein Nationalsymbol?",desc:"Nationaltiere auf der Weltkarte pinnen"},
    {id:"uk_tiere_primaten",       icon:"\\u{1F412}",title:"[BETA] Primaten-Zentren",        group:"tiere",prompt:"\\u{1F4CD} Wo liegt dieser Regenwald der Menschenaffen?",desc:"Letzte Refugien von Schimpanse, Gorilla, Orang-Utan"},
    {id:"uk_tiere_hai",            icon:"\\u{1F988}",title:"[BETA] Hai-Hotspots",             group:"tiere",prompt:"\\u{1F4CD} Wo liegt dieser bekannte Hai-Hotspot?",      desc:"Statistisch bedeutsame Küstenabschnitte weltweit"},
    {id:"uk_tiere_baeren",         icon:"\\u{1F43B}",title:"[BETA] Bären-Verbreitung",       group:"tiere",prompt:"\\u{1F4CD} Wo lebt diese Bärenart?",                   desc:"Eisbär, Braunbär, Panda — Reviere der Welt"},
    /* === Phase 227: Tiere & Natur — Higher/Lower Modi (11) === */
    {id:"hl_tiere_gewicht_land",   icon:"\\u2696\\uFE0F",title:"[BETA] H/L Gewicht Landtiere",   group:"tiere",prompt:"Welches Landtier ist schwerer?",    desc:"K\\u00f6rpergewicht in kg — von Maus bis Elefant"},
    {id:"hl_tiere_gewicht_meer",   icon:"\\u{1F40B}",title:"[BETA] H/L Gewicht Meerestiere",  group:"tiere",prompt:"Welches Meerestier ist schwerer?",   desc:"K\\u00f6rpergewicht in kg — Seepferdchen bis Blauwal"},
    {id:"hl_tiere_speed_land",     icon:"\\u{1F406}",title:"[BETA] H/L Speed: Land",          group:"tiere",prompt:"Welches Tier l\\u00e4uft schneller?",  desc:"H\\u00f6chstgeschwindigkeit in km/h auf dem Land"},
    {id:"hl_tiere_speed_luft",     icon:"\\u{1F985}",title:"[BETA] H/L Speed: Luft",          group:"tiere",prompt:"Welches Tier fliegt schneller?",       desc:"H\\u00f6chstgeschwindigkeit in km/h in der Luft"},
    {id:"hl_tiere_speed_wasser",   icon:"\\u{1F41F}",title:"[BETA] H/L Speed: Wasser",        group:"tiere",prompt:"Welches Tier schwimmt schneller?",     desc:"H\\u00f6chstgeschwindigkeit in km/h im Wasser"},
    {id:"hl_tiere_lebenserwartung",icon:"\\u23F3",title:"[BETA] H/L Lebenserwartung",         group:"tiere",prompt:"Welches Tier wird \\u00e4lter?",        desc:"Maximales Alter in Jahren — Eintagsfliege bis Grönlandhai"},
    {id:"hl_tiere_traechtigkeit",  icon:"\\u{1F930}",title:"[BETA] H/L Tr\\u00e4chtigkeit",    group:"tiere",prompt:"Welches Tier tr\\u00e4gt l\\u00e4nger?",desc:"Tr\\u00e4chtigkeitsdauer in Tagen"},
    {id:"hl_tiere_wurf",           icon:"\\u{1F423}",title:"[BETA] H/L Wurfgr\\u00f6\\u00dfe", group:"tiere",prompt:"Welches Tier hat mehr Nachkommen?",   desc:"Max. Nachkommen pro Zyklus"},
    {id:"hl_tiere_gift",           icon:"\\u2620\\uFE0F",title:"[BETA] H/L Giftigkeit",        group:"tiere",prompt:"Welches Tier ist giftiger?",           desc:"Toxizit\\u00e4tsindex — h\\u00f6her = gef\\u00e4hrlicher"},
    {id:"hl_tiere_population",     icon:"\\u{1F4CA}",title:"[BETA] H/L Wildpopulation",       group:"tiere",prompt:"Von welchem Tier gibt es mehr Individuen?",desc:"Verbliebene Wildtiere laut IUCN"},
    {id:"hl_tiere_schlaf",         icon:"\\u{1F634}",title:"[BETA] H/L Schlafbedarf",         group:"tiere",prompt:"Welches Tier schl\\u00e4ft l\\u00e4nger?",desc:"Schlafstunden pro Tag"}
];"""

if MODES_ANCHOR not in content:
    print("ERROR: MODES closing anchor not found – check gen.py")
    exit(1)

content = content.replace(MODES_ANCHOR, TIERE_MODES, 1)
print("✓ PATCH 2: 21 MODES entries added for tiere category")

# ──────────────────────────────────────────────────────────────────────────────
# Write result
# ──────────────────────────────────────────────────────────────────────────────
with open(SRC, "w", encoding="utf-8") as f:
    f.write(content)

print("✓ gen.py written successfully — routing patch complete")
print("  Next: run enrich_tiere_part1.py to add data + generators")