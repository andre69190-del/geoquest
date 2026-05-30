#!/usr/bin/env python3
"""
patch_296_train_data.py
Phase 296.1 — Trainspotter-Paket Teil 1
Fügt hinzu:
  - kultur.json: 'zug_panorama' (50 Items), 'zug_vkm' (52 Items), 'ds100' (50 Items)
  - gen.py: 2 neue MODES (zug_panorama, zug_vkm) + GEN dispatch + airports MODE_CATS
"""
import json, sys, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KULTUR = os.path.join(BASE, 'data', 'kultur.json')
GEN    = os.path.join(BASE, 'gen.py')

# ─── 1. DATEN ────────────────────────────────────────────────────────────────

ZUG_PANORAMA = [
    # Schweiz (8)
    {"n": "Glacier Express (Zermatt–St. Moritz)", "c": "Schweiz"},
    {"n": "Bernina Express (Chur–Tirano)", "c": "Schweiz"},
    {"n": "GoldenPass Express (Montreux–Interlaken)", "c": "Schweiz"},
    {"n": "Gotthard Panorama Express", "c": "Schweiz"},
    {"n": "Voralpen-Express (St. Gallen–Luzern)", "c": "Schweiz"},
    {"n": "Lötschberger (Bern–Brig)", "c": "Schweiz"},
    {"n": "Rigi-Bahn (älteste Bergbahn Europas, 1871)", "c": "Schweiz"},
    {"n": "Furka-Dampfbahn (Dampfzug Alpen)", "c": "Schweiz"},
    # Norwegen (5)
    {"n": "Flåmbahn (Myrdal–Flåm)", "c": "Norwegen"},
    {"n": "Bergenbahn (Bergen–Oslo)", "c": "Norwegen"},
    {"n": "Rauma-Bahn (Dombås–Åndalsnes)", "c": "Norwegen"},
    {"n": "Ofotbahn (Narvik–Riksgränsen)", "c": "Norwegen"},
    {"n": "Nordlandsbahn (Oslo–Bodø)", "c": "Norwegen"},
    # Schottland (3)
    {"n": "Jacobite Steam Train (Hogwarts-Express-Strecke)", "c": "Vereinigtes Königreich"},
    {"n": "West Highland Line (Glasgow–Mallaig)", "c": "Vereinigtes Königreich"},
    {"n": "Caledonian Sleeper (London–Inverness)", "c": "Vereinigtes Königreich"},
    # Österreich (3)
    {"n": "Semmeringbahn (älteste Gebirgsbahn, UNESCO)", "c": "Österreich"},
    {"n": "Mariazellerbahn (St. Pölten–Mariazell)", "c": "Österreich"},
    {"n": "Arlberg Express (Wien–Bregenz)", "c": "Österreich"},
    # Indien (4)
    {"n": "Darjeeling Himalayan Railway (Toy Train, UNESCO)", "c": "Indien"},
    {"n": "Palace on Wheels (Rajasthan-Luxuszug)", "c": "Indien"},
    {"n": "Deccan Odyssey (Mumbai–Goa–Maharashtra)", "c": "Indien"},
    {"n": "Nilgiri Mountain Railway (UNESCO)", "c": "Indien"},
    # Australien (3)
    {"n": "The Ghan (Adelaide–Darwin, 2979 km)", "c": "Australien"},
    {"n": "Indian Pacific (Sydney–Perth, 4352 km)", "c": "Australien"},
    {"n": "The Overland (Melbourne–Adelaide)", "c": "Australien"},
    # Kanada (3)
    {"n": "Rocky Mountaineer (Vancouver–Banff)", "c": "Kanada"},
    {"n": "The Canadian (Toronto–Vancouver, 4466 km)", "c": "Kanada"},
    {"n": "VIA Rail Ocean (Montréal–Halifax)", "c": "Kanada"},
    # USA (4)
    {"n": "California Zephyr (Chicago–San Francisco)", "c": "USA"},
    {"n": "Coast Starlight (Los Angeles–Seattle)", "c": "USA"},
    {"n": "Empire Builder (Chicago–Seattle)", "c": "USA"},
    {"n": "Auto Train (Washington D.C.–Orlando)", "c": "USA"},
    # Peru (2)
    {"n": "Andean Explorer (Cusco–Puno–Arequipa)", "c": "Peru"},
    {"n": "Machu Picchu Train (Cusco–Aguas Calientes)", "c": "Peru"},
    # Südafrika (2)
    {"n": "Blue Train (Kapstadt–Pretoria)", "c": "Südafrika"},
    {"n": "Rovos Rail (Pride of Africa, Kapstadt–Daressalam)", "c": "Südafrika"},
    # Japan (3)
    {"n": "Shinkansen Nozomi (Tokio–Osaka, 270 km/h)", "c": "Japan"},
    {"n": "Twilight Express Mizukaze (Osaka–Sapporo)", "c": "Japan"},
    {"n": "Seven Stars in Kyushu (Luxus-Rundreisezug)", "c": "Japan"},
    # Myanmar (1)
    {"n": "Gokteik-Viadukt-Bahn (höchste Brücke Myanmars)", "c": "Myanmar"},
    # Kolumbien (1)
    {"n": "Tren Turístico de la Sabana (Bogotá–Zipaquirá)", "c": "Kolumbien"},
    # Ecuador (1)
    {"n": "Tren Crucero (Quito–Guayaquil, Andenmassiv)", "c": "Ecuador"},
    # Russland (2)
    {"n": "Transsibirische Eisenbahn (Moskau–Wladiwostok)", "c": "Russland"},
    {"n": "Zarengold (Berlin–Moskau–Ulan-Ude, Nostalgiezug)", "c": "Russland"},
    # Sri Lanka (1)
    {"n": "Kandy–Ella Bergzug (berühmteste Bahnstrecke Asiens)", "c": "Sri Lanka"},
    # Dänemark (1)
    {"n": "DSB IC3 (Kopenhagen–Aarhus, Dieseltriebwagen)", "c": "Dänemark"},
    # Marokko (1)
    {"n": "Casablanca–Tanger (Al Boraq, schnellster Zug Afrikas)", "c": "Marokko"},
]

ZUG_VKM = [
    # Deutschland (14)
    {"n": "D-DB",      "c": "Deutschland"},
    {"n": "D-FLX",     "c": "Deutschland"},
    {"n": "D-ODEG",    "c": "Deutschland"},
    {"n": "D-HLB",     "c": "Deutschland"},
    {"n": "D-VIAS",    "c": "Deutschland"},
    {"n": "D-NEB",     "c": "Deutschland"},
    {"n": "D-BEG",     "c": "Deutschland"},
    {"n": "D-MRB",     "c": "Deutschland"},
    {"n": "D-ALEX",    "c": "Deutschland"},
    {"n": "D-NOBIL",   "c": "Deutschland"},
    {"n": "D-ERX",     "c": "Deutschland"},
    {"n": "D-ENNO",    "c": "Deutschland"},
    {"n": "D-TLX",     "c": "Deutschland"},
    {"n": "D-RRX",     "c": "Deutschland"},
    # Österreich (6)
    {"n": "A-OBB",     "c": "Österreich"},
    {"n": "A-WB",      "c": "Österreich"},
    {"n": "A-GYSEV",   "c": "Österreich"},
    {"n": "A-STB",     "c": "Österreich"},
    {"n": "A-WLB",     "c": "Österreich"},
    {"n": "A-VBG",     "c": "Österreich"},
    # Schweiz (5)
    {"n": "CH-SBB",    "c": "Schweiz"},
    {"n": "CH-BLS",    "c": "Schweiz"},
    {"n": "CH-AB",     "c": "Schweiz"},
    {"n": "CH-MGB",    "c": "Schweiz"},
    {"n": "CH-SOB",    "c": "Schweiz"},
    # Frankreich (4)
    {"n": "F-SNCF",    "c": "Frankreich"},
    {"n": "F-OUI",     "c": "Frankreich"},
    {"n": "F-TRENITALIA","c": "Frankreich"},
    {"n": "F-THELLO",  "c": "Frankreich"},
    # Italien (4)
    {"n": "I-FS",      "c": "Italien"},
    {"n": "I-NTV",     "c": "Italien"},
    {"n": "I-TPER",    "c": "Italien"},
    {"n": "I-TRENORD", "c": "Italien"},
    # Niederlande (3)
    {"n": "NL-NS",     "c": "Niederlande"},
    {"n": "NL-ARRIVA", "c": "Niederlande"},
    {"n": "NL-CONNEXXION","c": "Niederlande"},
    # Belgien (3)
    {"n": "B-SNCB",    "c": "Belgien"},
    {"n": "B-THALYS",  "c": "Belgien"},
    {"n": "B-EUROSTAR","c": "Belgien"},
    # Spanien (3)
    {"n": "E-RENFE",   "c": "Spanien"},
    {"n": "E-OUIGO",   "c": "Spanien"},
    {"n": "E-FGC",     "c": "Spanien"},
    # Polen (3)
    {"n": "PL-PKP",    "c": "Polen"},
    {"n": "PL-POLREGIO","c": "Polen"},
    {"n": "PL-KD",     "c": "Polen"},
    # Schweden (3)
    {"n": "S-SJ",      "c": "Schweden"},
    {"n": "S-MTR",     "c": "Schweden"},
    {"n": "S-SNALLTAGET","c": "Schweden"},
    # Tschechien (2)
    {"n": "CZ-CD",     "c": "Tschechien"},
    {"n": "CZ-REGIOJET","c": "Tschechien"},
    # Ungarn (2)
    {"n": "H-MAV",     "c": "Ungarn"},
    {"n": "H-MAVSTART","c": "Ungarn"},
]

# DS100 Rohdaten (für späteren Input-Modus, noch nicht aktiv)
DS100 = [
    {"q": "Frankfurt (Main) Hbf", "a": "FF"},
    {"q": "München Hbf", "a": "MH"},
    {"q": "Hamburg Hbf", "a": "AH"},
    {"q": "Berlin Hbf", "a": "BLB"},
    {"q": "Köln Hbf", "a": "KK"},
    {"q": "Stuttgart Hbf", "a": "TS"},
    {"q": "Düsseldorf Hbf", "a": "KD"},
    {"q": "Hannover Hbf", "a": "HH"},
    {"q": "Leipzig Hbf", "a": "LE"},
    {"q": "Nürnberg Hbf", "a": "NN"},
    {"q": "Dortmund Hbf", "a": "EDO"},
    {"q": "Dresden Hbf", "a": "DD"},
    {"q": "Mannheim Hbf", "a": "RM"},
    {"q": "Karlsruhe Hbf", "a": "RK"},
    {"q": "Bremen Hbf", "a": "HB"},
    {"q": "Augsburg Hbf", "a": "MA"},
    {"q": "Essen Hbf", "a": "EE"},
    {"q": "Freiburg (Breisgau) Hbf", "a": "RFB"},
    {"q": "Erfurt Hbf", "a": "EF"},
    {"q": "Mainz Hbf", "a": "RMZ"},
    {"q": "Rostock Hbf", "a": "NRS"},
    {"q": "Kiel Hbf", "a": "AKI"},
    {"q": "Saarbrücken Hbf", "a": "RSB"},
    {"q": "Wiesbaden Hbf", "a": "RWI"},
    {"q": "Kassel Hbf", "a": "KS"},
    {"q": "Bielefeld Hbf", "a": "EBD"},
    {"q": "Magdeburg Hbf", "a": "MD"},
    {"q": "Bochum Hbf", "a": "EBO"},
    {"q": "Halle (Saale) Hbf", "a": "MLH"},
    {"q": "Lübeck Hbf", "a": "AL"},
    # Österreich
    {"q": "Wien Hbf", "a": "WHF"},
    {"q": "Wien Westbahnhof", "a": "WW"},
    {"q": "Salzburg Hbf", "a": "SZ"},
    {"q": "Graz Hbf", "a": "GZ"},
    {"q": "Innsbruck Hbf", "a": "INN"},
    # Schweiz (SBB Abkürzungen)
    {"q": "Zürich HB", "a": "ZUE"},
    {"q": "Bern", "a": "BN"},
    {"q": "Basel SBB", "a": "BAS"},
    {"q": "Genf", "a": "GE"},
    {"q": "Lausanne", "a": "LS"},
    # Sonstige Europa
    {"q": "Paris Gare de Lyon", "a": "PFGL"},
    {"q": "Amsterdam Centraal", "a": "NASC"},
    {"q": "Brüssel Midi/Zuid", "a": "BBMU"},
    {"q": "Wien Meidling", "a": "WMEID"},
    {"q": "Dortmund Signal Iduna Park", "a": "EDSI"},
    {"q": "Hannover Messe/Laatzen", "a": "HHLM"},
    {"q": "München Ost", "a": "MHO"},
    {"q": "Berlin Ostbahnhof", "a": "BLO"},
    {"q": "Köln Messe/Deutz", "a": "KKMD"},
    {"q": "Hamburg-Altona", "a": "AHAT"},
]

# ─── 2. KULTUR.JSON PATCHEN ──────────────────────────────────────────────────

print("[1/3] Patche data/kultur.json ...")
with open(KULTUR, 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'zug_panorama' in data:
    print("  [SKIP] zug_panorama already exists")
else:
    data['zug_panorama'] = ZUG_PANORAMA
    print(f"  [OK] zug_panorama: {len(ZUG_PANORAMA)} Items")

if 'zug_vkm' in data:
    print("  [SKIP] zug_vkm already exists")
else:
    data['zug_vkm'] = ZUG_VKM
    print(f"  [OK] zug_vkm: {len(ZUG_VKM)} Items")

if 'ds100' in data:
    print("  [SKIP] ds100 already exists")
else:
    data['ds100'] = DS100
    print(f"  [OK] ds100: {len(DS100)} Items (Rohdaten, noch kein aktiver Modus)")

with open(KULTUR, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("  [OK] kultur.json gespeichert")

# Validierung: Match-Engine braucht >= 4 unique c-Werte
for key, items in [('zug_panorama', ZUG_PANORAMA), ('zug_vkm', ZUG_VKM)]:
    cats = list(set(x['c'] for x in items))
    min_per_cat = min(sum(1 for x in items if x['c']==c) for c in cats)
    print(f"  [CHECK] {key}: {len(cats)} Kategorien, min {min_per_cat} Item/Kat")
    if len(cats) < 4:
        print(f"  [WARN] Zu wenige Kategorien für Match-Engine!")

# ─── 3. GEN.PY PATCHEN ───────────────────────────────────────────────────────

print("\n[2/3] Patche gen.py ...")
with open(GEN, 'r', encoding='utf-8') as f:
    content = f.read()

# A: MODES-Einträge nach uk_bahnstrecken einfügen
ANCHOR = '{id:"uk_bahnstrecken",    icon:"\\u{1F686}",title:"Ber\\u00fchmte Bahnstrecken"'
if 'zug_panorama' in content:
    print("  [SKIP] MODES-Einträge bereits vorhanden")
else:
    NEW_MODES = (
        '\n    {id:"zug_panorama",       icon:"\\u{1F6A2}",title:"Panorama-Z\\u00fcge",           '
        'group:"airports",prompt:"In welchem Land f\\u00e4hrt dieser Panorama- oder Luxuszug?",    '
        'desc:"Glacier Express, The Ghan, Rocky Mountaineer & Co."},\n'
        '    {id:"zug_vkm",            icon:"\\u{1F3F7}\\uFE0F",title:"Halterk\\u00fcrzel (VKM)",   '
        'group:"airports",prompt:"Aus welchem Land kommt dieses Fahrzeughalter-K\\u00fcrzel?",     '
        'desc:"D-DB, A-OBB, CH-SBB — europ\\u00e4ische VKM-Codes"},'
    )
    if ANCHOR in content:
        idx = content.find(ANCHOR)
        # Füge NACH dem Zeilenende des Anchors ein
        line_end = content.find('\n', idx)
        content = content[:line_end] + NEW_MODES + content[line_end:]
        print("  [OK] MODES-Einträge eingefügt")
    else:
        print("  [WARN] Anchor für MODES nicht gefunden — manuell prüfen")

# B: GEN dispatch Einträge
DISPATCH_ANCHOR = 'uk_bahnstrecken:()=>genUniversalMatchQ("bahnstrecken")'
if 'zug_panorama:()=>' in content:
    print("  [SKIP] GEN dispatch bereits vorhanden")
elif DISPATCH_ANCHOR in content:
    idx = content.find(DISPATCH_ANCHOR)
    line_end = content.find('\n', idx)
    NEW_DISPATCH = (
        '\n  zug_panorama:()=>genUniversalMatchQ("zug_panorama"),'
        '\n  zug_vkm:()=>genUniversalMatchQ("zug_vkm"),'
    )
    content = content[:line_end] + NEW_DISPATCH + content[line_end:]
    print("  [OK] GEN dispatch eingefügt")
else:
    print("  [WARN] GEN dispatch Anchor nicht gefunden")

# C: MODE_CATS airports — neue IDs eintragen
CATS_ANCHOR = '"uk_bahnstrecken"'
if '"zug_panorama"' in content:
    print("  [SKIP] MODE_CATS bereits aktualisiert")
else:
    # Finde ersten Treffer in MODE_CATS (nicht in MODES)
    cats_idx = content.find('"airports":{label:')
    if cats_idx > 0:
        anchor_in_cats = content.find('"uk_bahnstrecken"', cats_idx)
        if anchor_in_cats > 0:
            content = content[:anchor_in_cats+len('"uk_bahnstrecken"')] + \
                      ',"zug_panorama","zug_vkm"' + \
                      content[anchor_in_cats+len('"uk_bahnstrecken"'):]
            print("  [OK] MODE_CATS airports erweitert")
        else:
            print("  [WARN] airports cats anchor nicht gefunden")
    else:
        print("  [WARN] airports category nicht gefunden")

with open(GEN, 'w', encoding='utf-8') as f:
    f.write(content)
print("  [OK] gen.py gespeichert")

print("\n[3/3] Validation ...")
# Nochmal lesen und prüfen
with open(GEN, 'r', encoding='utf-8') as f:
    c2 = f.read()
checks = {
    'zug_panorama MODES': 'id:"zug_panorama"' in c2,
    'zug_vkm MODES':      'id:"zug_vkm"' in c2,
    'zug_panorama GEN':   'zug_panorama:()=>genUniversalMatchQ' in c2,
    'zug_vkm GEN':        'zug_vkm:()=>genUniversalMatchQ' in c2,
    'MODE_CATS updated':  '"zug_panorama"' in c2,
}
all_ok = True
for k,v in checks.items():
    sym = '[OK]' if v else '[!!]'
    print(f"  {sym} {k}")
    if not v: all_ok = False

if all_ok:
    print("\n✓ Patch erfolgreich abgeschlossen!")
else:
    print("\n⚠ Einige Checks fehlgeschlagen — gen.py manuell prüfen")
    sys.exit(1)
