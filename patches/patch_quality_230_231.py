#!/usr/bin/env python3
"""
patch_quality_230_231.py
========================
Qualitaets-Patch fuer Phasen 230 + 231:

  Fix 1: [BETA] prefix auf alle Modes in groups technologie, emobilitaet, archaeologie
  Fix 2: pflanzen-Modes: group:"tiere" -> group:"pflanzen"
  Fix 3: archaeologie_pin.json, archaeologie_hl.json, archaeologie_match.json
         von 12 auf 20 Items pro Kategorie erweitern
  Fix 4: verify.py um Checks fuer alle neuen JSON-Dateien erweitern

Sicherheit: assert + c.count() checks vor jedem re.sub
"""

import re
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN_PY = os.path.join(BASE, 'gen.py')
VERIFY_PY = os.path.join(BASE, 'verify.py')
DATA_DIR = os.path.join(BASE, 'data')

print("=" * 60)
print("patch_quality_230_231.py  -- Quality patch for Phase 230/231")
print("=" * 60)

# ============================================================
# Load gen.py
# ============================================================
with open(GEN_PY, 'r', encoding='utf-8') as f:
    c = f.read()

original_len = len(c)
print(f"\n[INFO] gen.py loaded: {len(c)} chars")

# ============================================================
# FIX 1: Add [BETA] prefix to technologie, emobilitaet,
#         archaeologie mode titles
# ============================================================
print("\n--- Fix 1: [BETA] prefix for new mode groups ---")

def add_beta_to_title(line):
    """For a single line containing group:'X', fix title if missing [BETA]."""
    m = re.search(r'title:"([^"]*)"', line)
    if not m:
        return line
    title = m.group(1)
    if title.startswith('[BETA]'):
        return line  # already has it
    new_title = '[BETA] ' + title
    return line.replace('title:"' + title + '"', 'title:"' + new_title + '"', 1)

target_groups = ['technologie', 'emobilitaet', 'archaeologie']
beta_added = 0
lines = c.split('\n')
new_lines = []

for line in lines:
    original_line = line
    for grp in target_groups:
        if 'group:"' + grp + '"' in line:
            line = add_beta_to_title(line)
            if line != original_line:
                beta_added += 1
            break  # only one group per line
    new_lines.append(line)

c = '\n'.join(new_lines)

# Safety check: verify all target-group lines now have [BETA]
missing_beta = []
for line in c.split('\n'):
    for grp in target_groups:
        if 'group:"' + grp + '"' in line:
            m = re.search(r'title:"([^"]*)"', line)
            if m and not m.group(1).startswith('[BETA]'):
                missing_beta.append(line.strip()[:100])
assert len(missing_beta) == 0, f"Still missing [BETA] on {len(missing_beta)} lines:\n" + "\n".join(missing_beta)
print(f"  [OK] {beta_added} [BETA] tags added, 0 remaining without tag")

# ============================================================
# FIX 2: pflanzen modes: group:"tiere" -> group:"pflanzen"
# ============================================================
print("\n--- Fix 2: pflanzen modes group: tiere -> pflanzen ---")

pflanzen_tiere_count_before = sum(
    1 for line in c.split('\n')
    if re.search(r'id:"(uk|hl|ws)_pflanzen_', line) and 'group:"tiere"' in line
)
print(f"  [INFO] Lines matching id:*_pflanzen_* with group:tiere before: {pflanzen_tiere_count_before}")
assert pflanzen_tiere_count_before > 0, "Expected to find pflanzen lines with group:tiere -- check gen.py"

pflanzen_changed = 0
new_lines = []
for line in c.split('\n'):
    if re.search(r'id:"(uk|hl|ws)_pflanzen_', line) and 'group:"tiere"' in line:
        line = line.replace('group:"tiere"', 'group:"pflanzen"', 1)
        pflanzen_changed += 1
    new_lines.append(line)

c = '\n'.join(new_lines)

remaining = sum(
    1 for line in c.split('\n')
    if re.search(r'id:"(uk|hl|ws)_pflanzen_', line) and 'group:"tiere"' in line
)
assert remaining == 0, f"{remaining} pflanzen lines still have group:tiere"
assert pflanzen_changed == pflanzen_tiere_count_before, \
    f"Changed {pflanzen_changed} but expected {pflanzen_tiere_count_before}"
print(f"  [OK] {pflanzen_changed} pflanzen mode lines updated: group:tiere -> group:pflanzen")

# ============================================================
# Write updated gen.py
# ============================================================
with open(GEN_PY, 'w', encoding='utf-8') as f:
    f.write(c)
print(f"\n[OK] gen.py written ({len(c)} chars, delta: {len(c)-original_len:+d})")


# ============================================================
# FIX 3: Expand archaeologie JSON files from 12 to 20 items
# ============================================================
print("\n--- Fix 3: Expand archaeologie JSON data to 20 items/category ---")

# ---- archaeologie_pin.json ----
pin_path = os.path.join(DATA_DIR, 'archaeologie_pin.json')
with open(pin_path, 'r', encoding='utf-8') as f:
    pin_data = json.load(f)

pin_additions = {
    "artefakte": [
        {"n": "Benin-Bronzen (British Museum)", "lat": 51.5194, "lng": -0.1270},
        {"n": "Nefertari-Papyrus (Turin)", "lat": 45.0703, "lng": 7.6869},
        {"n": "Lewis-Schachfiguren (Edinburgh)", "lat": 55.9468, "lng": -3.1883},
        {"n": "Goldmaske von Mykene (Athen)", "lat": 37.9714, "lng": 23.7258},
        {"n": "Voynich-Manuskript (Yale)", "lat": 41.3163, "lng": -72.9223},
        {"n": "Ludovisi-Thron (Rom)", "lat": 41.9022, "lng": 12.4539},
        {"n": "Jade-Totenmaske (Mexiko City)", "lat": 19.4326, "lng": -99.1332},
        {"n": "Sutton-Hoo-Helm (British Museum)", "lat": 51.5194, "lng": -0.1270},
    ],
    "megalithanlagen": [
        {"n": "Skara Brae (Orkney)", "lat": 59.0486, "lng": -3.3416},
        {"n": "Bru na Boinne (Knowth)", "lat": 53.7011, "lng": -6.4867},
        {"n": "Men-an-Tol (Cornwall)", "lat": 50.1614, "lng": -5.6072},
        {"n": "Nabta Playa (Aegypten)", "lat": 22.5267, "lng": 30.7244},
        {"n": "Lough Gur (Irland)", "lat": 52.5150, "lng": -8.5350},
        {"n": "Recumbent Stone Circle (Aberdeenshire)", "lat": 57.1500, "lng": -2.6833},
        {"n": "Dolmen von Bagneux (Frankreich)", "lat": 47.4667, "lng": -0.0667},
        {"n": "Monte d'Accoddi (Sardinien)", "lat": 40.7667, "lng": 8.5000},
    ],
    "versunkene_staedte": [
        {"n": "Dunwich (Suffolk, UK)", "lat": 52.2764, "lng": 1.6283},
        {"n": "Vineta (Ostsee, Deutschland)", "lat": 53.9667, "lng": 14.2500},
        {"n": "Epidaurus Limera (Griechenland)", "lat": 36.7667, "lng": 23.0833},
        {"n": "Canopus (Abuqir-Bucht, Aegypten)", "lat": 31.3333, "lng": 30.0833},
        {"n": "Olbia (Ukraine, Schwarzes Meer)", "lat": 46.6333, "lng": 31.9000},
        {"n": "Phanagoria (Schwarzes Meer)", "lat": 45.2167, "lng": 36.9333},
        {"n": "Kaupang (Norwegen, versunkener Hafen)", "lat": 59.0000, "lng": 10.2000},
        {"n": "Shi Cheng (Qiandao-See, China)", "lat": 29.6050, "lng": 119.0072},
    ],
    "hoehlenmalerien": [
        {"n": "El Castillo (Kantabrien, Spanien)", "lat": 43.3833, "lng": -4.0000},
        {"n": "Pettakere (Sulawesi, Indonesien)", "lat": -4.9322, "lng": 119.7117},
        {"n": "Cueva de El Pindal (Asturien)", "lat": 43.3833, "lng": -4.5167},
        {"n": "Pech Merle (Lot, Frankreich)", "lat": 44.4917, "lng": 1.6833},
        {"n": "Rouffignac (Dordogne)", "lat": 45.0500, "lng": 0.9833},
        {"n": "Gabarnmung (Arnhem Land, Australien)", "lat": -12.3333, "lng": 134.2167},
        {"n": "Wadi Sura II (Libysches Massiv)", "lat": 23.0000, "lng": 25.1667},
        {"n": "Cueva de la Pileta (Malaga)", "lat": 36.7000, "lng": -5.1000},
    ],
    "digitalprojekte": [
        {"n": "Europeana (Den Haag)", "lat": 52.0800, "lng": 4.3100},
        {"n": "Google Arts & Culture (Mountain View)", "lat": 37.4192, "lng": -122.0574},
        {"n": "3D-Museo Nazionale Romano (Rom)", "lat": 41.9022, "lng": 12.4539},
        {"n": "Virtual Museum of Iraq (Bagdad)", "lat": 33.3406, "lng": 44.4009},
        {"n": "Institut national du patrimoine (Paris)", "lat": 48.8566, "lng": 2.3522},
        {"n": "Heritage Foundation of Pakistan (Lahore)", "lat": 31.5546, "lng": 74.3572},
        {"n": "Egyptian Heritage Archive (Kairo)", "lat": 30.0444, "lng": 31.2357},
        {"n": "ARIADNE Research Infrastructure (Florenz)", "lat": 43.7696, "lng": 11.2558},
    ],
    "graberfelder": [
        {"n": "Pompeji (Nekropole vor den Toren)", "lat": 40.7508, "lng": 14.4897},
        {"n": "Kerameikos (Athen)", "lat": 37.9773, "lng": 23.7184},
        {"n": "Tenochtitlan Templo Mayor Opferplatz", "lat": 19.4352, "lng": -99.1316},
        {"n": "Huaca Pucllana (Lima)", "lat": -12.1117, "lng": -77.0333},
        {"n": "Banditaccia-Nekropole (Cerveteri)", "lat": 42.0000, "lng": 12.1000},
        {"n": "Mound of the Hostages (Tara, Irland)", "lat": 53.5833, "lng": -6.6167},
        {"n": "Vetulonia (Etruskische Graeber)", "lat": 42.7833, "lng": 11.1333},
        {"n": "Pazyryk-Kurgane (Sibirien)", "lat": 50.2000, "lng": 87.9000},
    ],
    "schiffswracks": [
        {"n": "Helike (Korinthischer Golf)", "lat": 38.2333, "lng": 22.1333},
        {"n": "San Jose-Wrack (Kolumbien)", "lat": 9.7000, "lng": -75.8000},
        {"n": "Nanhai Nr. 1 (China, Guangdong)", "lat": 21.4667, "lng": 111.7167},
        {"n": "Bronze-Age Dover-Boat (Aermelkanal)", "lat": 51.1279, "lng": 1.3134},
        {"n": "Kinneret Fischerboot (Genezareth)", "lat": 32.8342, "lng": 35.5347},
        {"n": "Bodrum-Wrack Kos-Kanal (Tuerkei)", "lat": 36.9000, "lng": 27.3000},
        {"n": "Herculaneum Boote (unterirdisch)", "lat": 40.8058, "lng": 14.3483},
        {"n": "Cabrera-Archipel Wrack (Mallorca)", "lat": 39.1500, "lng": 2.9333},
    ],
    "maya_inka": [
        {"n": "Caral (Peru, aelteste Stadt Amerikas)", "lat": -10.8908, "lng": -77.5206},
        {"n": "Tiwanaku (Bolivien)", "lat": -16.5544, "lng": -68.6731},
        {"n": "Xochicalco (Mexiko)", "lat": 18.8000, "lng": -99.2833},
        {"n": "Monte Alban (Oaxaca)", "lat": 17.0437, "lng": -96.7675},
        {"n": "Chavín de Huantar (Peru)", "lat": -9.5939, "lng": -77.1769},
        {"n": "Ek Balam (Yucatan)", "lat": 20.8792, "lng": -88.2481},
        {"n": "Ollantaytambo (Peru)", "lat": -13.2589, "lng": -72.2639},
        {"n": "Comalcalco (Tabasco -- Backstein-Maya)", "lat": 18.2764, "lng": -93.2047},
    ],
    "roemische_limes": [
        {"n": "Vindolanda (Hadrianswall)", "lat": 54.9942, "lng": -2.3608},
        {"n": "Masada (Israel -- roem. Belagerungsring)", "lat": 31.3156, "lng": 35.3534},
        {"n": "Dura-Europos (Syrien)", "lat": 34.7500, "lng": 40.7333},
        {"n": "Aquincum (Budapest)", "lat": 47.5556, "lng": 19.0417},
        {"n": "Carnuntum (Niederoesterreich)", "lat": 48.1167, "lng": 16.8667},
        {"n": "Xanten (Colonia Ulpia Traiana)", "lat": 51.6578, "lng": 6.4533},
        {"n": "Gerasa (Jerash, Jordanien)", "lat": 32.2817, "lng": 35.8917},
        {"n": "Timgad Limes-Naehe (Algerien)", "lat": 35.4833, "lng": 6.4667},
    ],
    "pfahlbauten": [
        {"n": "La Motte aux Magnins (Chalain-See)", "lat": 46.6667, "lng": 5.7500},
        {"n": "Zug-Sumpf (Zuerich)", "lat": 47.1667, "lng": 8.5167},
        {"n": "Luokesas (Litauen)", "lat": 54.1167, "lng": 25.6333},
        {"n": "Molino San Vincenzo (Varese-See)", "lat": 45.8000, "lng": 8.7167},
        {"n": "Sutz-Lattrigen (Bielersee)", "lat": 47.1167, "lng": 7.1833},
        {"n": "Pestenacker (Bayern)", "lat": 48.1833, "lng": 10.9500},
        {"n": "Burgaschisee-Sued (Schweiz)", "lat": 47.1167, "lng": 7.6500},
        {"n": "Dispilio Erweiterung (Kastoria)", "lat": 40.5000, "lng": 21.2667},
    ],
    "wuestenstaedte": [
        {"n": "Jiaohe (Xinjiang, China)", "lat": 42.8667, "lng": 89.0167},
        {"n": "Ctesiphon (Irak)", "lat": 33.0944, "lng": 44.5806},
        {"n": "Nisa (Turkmenistan -- Parther)", "lat": 37.9167, "lng": 58.3333},
        {"n": "Hegra (Al-Ula, Saudi-Arabien)", "lat": 26.7833, "lng": 37.9500},
        {"n": "Shahr-e Sokhteh (Iran)", "lat": 30.5833, "lng": 61.3333},
        {"n": "Karakorum (Mongolei)", "lat": 47.1844, "lng": 102.8381},
        {"n": "Timbuktu (Mali) -- historische Kernstadt", "lat": 16.7667, "lng": -3.0000},
        {"n": "Gebel Barkal (Sudan)", "lat": 18.5333, "lng": 31.8167},
    ],
    "fossilien": [
        {"n": "Miguasha (Kanada -- Devonische Fische)", "lat": 48.1000, "lng": -66.3500},
        {"n": "Joggins Fossil Cliffs (Nova Scotia)", "lat": 45.6944, "lng": -64.4428},
        {"n": "Ischigualasto (Argentinien -- Trias)", "lat": -29.9333, "lng": -67.8833},
        {"n": "Sichuan Zigong Dinosauriermuseum", "lat": 29.3500, "lng": 104.7667},
        {"n": "Florissant (Colorado -- Eozaen)", "lat": 38.9133, "lng": -105.2836},
        {"n": "Riversleigh (Queensland -- Saeugetiere)", "lat": -19.0833, "lng": 138.7167},
        {"n": "Tsagaan Khushuu (Mongolei -- Protoceratops)", "lat": 43.8000, "lng": 100.4000},
        {"n": "Joggins Fossil Cliffs (Canada)", "lat": 45.6944, "lng": -64.4428},
    ],
    "sensationsfunde": [
        {"n": "Goldschatz von Varna (Baggerfuehrer)", "lat": 43.2042, "lng": 27.9106},
        {"n": "Hoxne-Schatz (Bauer sucht Hammer)", "lat": 52.3489, "lng": 1.1756},
        {"n": "Willendorf-Venus (Eisenbahnarbeiter)", "lat": 48.3578, "lng": 15.3944},
        {"n": "Staffordshire Hoard (Metalldetektor)", "lat": 52.7333, "lng": -2.0167},
        {"n": "Nag-Hammadi-Kodizes (Bauer beim Graeben)", "lat": 26.0333, "lng": 32.2333},
        {"n": "Vogelherd-Figurinen (Hoehlengrabung 1931)", "lat": 48.5167, "lng": 10.1667},
        {"n": "Sipan-Grab (Archaeologe Alva 1987)", "lat": -6.6919, "lng": -79.9261},
        {"n": "Lydischer Schatz -- Karun Hoard (Bauer)", "lat": 38.6000, "lng": 27.8333},
    ],
}

pin_items_added = 0
for key, new_items in pin_additions.items():
    assert key in pin_data, f"Key '{key}' not found in archaeologie_pin.json"
    before = len(pin_data[key]['items'])
    pin_data[key]['items'].extend(new_items)
    after = len(pin_data[key]['items'])
    pin_items_added += (after - before)
    assert after == 20, f"Category '{key}' has {after} items, expected 20"

with open(pin_path, 'w', encoding='utf-8') as f:
    json.dump(pin_data, f, ensure_ascii=False, indent=2)

with open(pin_path, 'r', encoding='utf-8') as f:
    verify_pin = json.load(f)
for key in pin_data:
    assert len(verify_pin[key]['items']) == 20, f"Verify failed: {key} has {len(verify_pin[key]['items'])} items"
print(f"  [OK] archaeologie_pin.json: {pin_items_added} items added, all categories now have 20 items")


# ---- archaeologie_hl.json ----
hl_path = os.path.join(DATA_DIR, 'archaeologie_hl.json')
with open(hl_path, 'r', encoding='utf-8') as f:
    hl_data = json.load(f)

hl_additions = {
    "alter_artefakte": [
        {"name": "Oetzi der Eismann", "val": 5300},
        {"name": "Newgrange-Anlage (Bau)", "val": 5200},
        {"name": "Gobekli Tepe (Erbauung)", "val": 11500},
        {"name": "Catalhoyuk (erste Besiedlung)", "val": 9400},
        {"name": "Vogelherd-Pferd (Elfenbein)", "val": 40000},
        {"name": "Chauvet-Malereien", "val": 36000},
        {"name": "Tabun-Hoehle Homo sapiens-Schaedel", "val": 120000},
        {"name": "Dolni Vestonice Venus", "val": 29000},
    ],
    "gewicht_megalithen": [
        {"name": "Dolmen de Bagneux Deckstein", "val": 90},
        {"name": "Callanish Hauptstein", "val": 5},
        {"name": "Ring of Brodgar Steine (je)", "val": 10},
        {"name": "Maeshowe Deckstein", "val": 30},
        {"name": "Rujm el-Hiri Megalith (gesamt)", "val": 37000},
        {"name": "Gobekli Tepe T-Pfeiler Zentrum", "val": 20},
        {"name": "Ahu Tongariki Moai (groesster)", "val": 86},
        {"name": "Menhir de Champ-Dolent (Bretagne)", "val": 150},
    ],
    "entdeckungsjahr": [
        {"name": "Pompeji (erste Ausgrabungen)", "val": 1748},
        {"name": "Parthenon-Skulpturen (Elgin)", "val": 1801},
        {"name": "Rosetta-Stein", "val": 1799},
        {"name": "Venus von Willendorf", "val": 1908},
        {"name": "Machu Picchu", "val": 1911},
        {"name": "Laetoli-Fussspuren", "val": 1976},
        {"name": "Altamira (offizielle Anerkennung)", "val": 1902},
        {"name": "Gunung Padang (erste Beschreibung)", "val": 1914},
    ],
    "fundtiefe": [
        {"name": "Pompeji Ascheschicht", "val": 6},
        {"name": "Herculaneum (Pyroklastit)", "val": 20},
        {"name": "Ur Koenigsgraeber", "val": 12},
        {"name": "Qin-Palastkomplex (unausgegraben)", "val": 35},
        {"name": "Maya-Cenoten-Funde (Mittelwert)", "val": 15},
        {"name": "Dolni Vestonice (Loesslehm)", "val": 5},
        {"name": "Clovis-Fund (New Mexico)", "val": 2},
        {"name": "Antikythera-Mechanismus-Wrack", "val": 45},
    ],
    "groesse_ruinen": [
        {"name": "Borobudur (Java)", "val": 2},
        {"name": "Angkor Thom", "val": 900},
        {"name": "Great Zimbabwe", "val": 722},
        {"name": "Karnak-Tempelkomplex", "val": 100},
        {"name": "Palenque Gesamtflaeche", "val": 1780},
        {"name": "Caral (Peru)", "val": 626},
        {"name": "Tula (Tolteken)", "val": 1400},
        {"name": "Bogazkoy (Hethiter)", "val": 180},
    ],
    "grabbeigaben": [
        {"name": "Qin Shi Huang (Gesamtanlage)", "val": 40000},
        {"name": "Vix-Grabhugel (Frankreich)", "val": 600},
        {"name": "Hochdorf-Fuerst (Sueddeutschland)", "val": 450},
        {"name": "Vergina-Grab (Philipp II.)", "val": 300},
        {"name": "Pazyryk-Kurgan (Sibirien)", "val": 200},
        {"name": "Tollund-Mann (nur Koerper)", "val": 1},
        {"name": "Tutankhamun Sarg Massivgold (einzeln)", "val": 110},
        {"name": "Mawangdui Grab Nr.1 (Han-Fuerstin)", "val": 3000},
    ],
    "strassenlaenge": [
        {"name": "Seidenstrasse (Gesamtroute)", "val": 10000},
        {"name": "Via Domitia (Suedfrankreich)", "val": 160},
        {"name": "Bernstein-Route (Mitteleuropa)", "val": 1200},
        {"name": "Grosser Inka-Weg (Qhapaq Nan)", "val": 30000},
        {"name": "Koenigsweg (Persien, Susa-Sardis)", "val": 2699},
        {"name": "Via Egnatia (Griechenland-Konstantinopel)", "val": 1120},
        {"name": "Via Aurelia (Rom-Arles)", "val": 1060},
        {"name": "Nabataische Weihrauchroute", "val": 2400},
    ],
    "c14_alter": [
        {"name": "Gobekli Tepe erste Schicht", "val": 11500},
        {"name": "Altamira Malereien", "val": 22000},
        {"name": "Kennewick Man (USA)", "val": 9000},
        {"name": "Spirit Cave Mumie (Nevada)", "val": 10600},
        {"name": "Guitarrero-Hoehle (Peru, Textilien)", "val": 12000},
        {"name": "Pesse-Kanu (Niederlande)", "val": 10000},
        {"name": "Dolni Vestonice Venus", "val": 29000},
        {"name": "Ain Ghazal-Statuen (Jordanien)", "val": 9200},
    ],
    "scandatenvolumen": [
        {"name": "Colosseum Gesamtscan", "val": 5000},
        {"name": "Notre-Dame-de-Paris Scan (vor Brand)", "val": 2000},
        {"name": "Bamiyan-Buddhas Rekonstruktion", "val": 800},
        {"name": "Palmyra (nach ISIS) CyArk", "val": 1500},
        {"name": "Taj Mahal Laserscan", "val": 1200},
        {"name": "Gobekli Tepe 3D Survey", "val": 600},
        {"name": "Altamira Hoehlen-Scan", "val": 400},
        {"name": "Machu Picchu Drohnenkartierung", "val": 4500},
    ],
    "bauzeit": [
        {"name": "Forum Romanum (Gesamtentwicklung)", "val": 900},
        {"name": "Hagia Sophia (erste Fassung)", "val": 5},
        {"name": "Grosse Mauer Chinas (gesamt)", "val": 1800},
        {"name": "Koelner Dom (historisch)", "val": 632},
        {"name": "Newgrange-Anlage", "val": 20},
        {"name": "Tempel von Karnak (gesamt)", "val": 2000},
        {"name": "Acropolis von Athen (Perikles)", "val": 15},
        {"name": "Alhambra (Granada)", "val": 200},
    ],
    "hoehe_bauwerke": [
        {"name": "Stufenpyramide des Djoser", "val": 62},
        {"name": "Tempel I Tikal", "val": 47},
        {"name": "Mausoleum von Halikarnassos (Schaetzung)", "val": 45},
        {"name": "Pyramide von Cestius (Rom)", "val": 36},
        {"name": "Borobudur Hauptturm", "val": 34},
        {"name": "Teotihuacan Mondpyramide", "val": 43},
        {"name": "Chephren-Pyramide (original)", "val": 143},
        {"name": "El Castillo Chichen Itza", "val": 30},
    ],
    "versicherungswert": [
        {"name": "Benin-Bronzen (Gesamtkollektion)", "val": 5000},
        {"name": "Moai-Statue Ahu Tongariki (symbolisch)", "val": 50},
        {"name": "Goldmaske von Mykene", "val": 2000},
        {"name": "Lewis-Schachfiguren (Auktionswert)", "val": 3},
        {"name": "Jade-Totenmaske Pakal (Mexiko)", "val": 200},
        {"name": "Sutton-Hoo-Helm (Schaetzung)", "val": 1500},
        {"name": "Vix-Krater (Bronzegefaess)", "val": 150},
        {"name": "Hochdorf-Goldfunde", "val": 100},
    ],
}

hl_items_added = 0
for key, new_items in hl_additions.items():
    assert key in hl_data, f"Key '{key}' not found in archaeologie_hl.json"
    before = len(hl_data[key]['items'])
    hl_data[key]['items'].extend(new_items)
    after = len(hl_data[key]['items'])
    hl_items_added += (after - before)
    assert after == 20, f"Category '{key}' has {after} items, expected 20"

with open(hl_path, 'w', encoding='utf-8') as f:
    json.dump(hl_data, f, ensure_ascii=False, indent=2)

with open(hl_path, 'r', encoding='utf-8') as f:
    verify_hl = json.load(f)
for key in hl_data:
    assert len(verify_hl[key]['items']) == 20
print(f"  [OK] archaeologie_hl.json: {hl_items_added} items added, all categories now have 20 items")


# ---- archaeologie_match.json ----
match_path = os.path.join(DATA_DIR, 'archaeologie_match.json')
with open(match_path, 'r', encoding='utf-8') as f:
    match_data = json.load(f)

match_additions = {
    "epochen": [
        {"n": "Tutanchamun-Maske", "c": "Bronzezeit"},
        {"n": "Antikythera-Mechanismus", "c": "Antike"},
        {"n": "Vasa-Wrack", "c": "Fruehe Neuzeit"},
        {"n": "Sutton-Hoo-Helm", "c": "Voelkerwanderungszeit"},
        {"n": "Oetzi der Eismann", "c": "Neolithikum"},
        {"n": "Himmelsscheibe von Nebra", "c": "Bronzezeit"},
        {"n": "Tollund-Mann", "c": "Eisenzeit"},
        {"n": "Stein von Rosette", "c": "Antike"},
    ],
    "werkzeuge": [
        {"n": "Drehherd-Toepferscheibe", "c": "Chalkolithikum"},
        {"n": "Bronzesichel", "c": "Bronzezeit"},
        {"n": "Eisenpflug", "c": "Eisenzeit"},
        {"n": "Obsidian-Skalpell", "c": "Neolithikum"},
        {"n": "Kupferbeil (Oetzi-Typ)", "c": "Neolithikum"},
        {"n": "Schilfstift (Calamus) fuer Keilschrift", "c": "Bronzezeit"},
        {"n": "Schmiedezange (Eisenzeit-Typ)", "c": "Eisenzeit"},
        {"n": "Steinmetzwerkzeug Dolerit-Pounder", "c": "Neolithikum"},
    ],
    "archaeologen": [
        {"n": "Pompeji (erste Ausgrabungen)", "c": "Karl Weber"},
        {"n": "Knossos", "c": "Arthur Evans"},
        {"n": "Ur (Koenigsgraeber)", "c": "Leonard Woolley"},
        {"n": "Olduvai Gorge", "c": "Louis Leakey"},
        {"n": "Machu Picchu", "c": "Hiram Bingham"},
        {"n": "Sipan-Grab", "c": "Walter Alva"},
        {"n": "Sutton Hoo", "c": "Basil Brown"},
        {"n": "Sanxingdui", "c": "Guanghan-Museum-Team"},
    ],
    "datierungsmethoden": [
        {"n": "Jahresringe einer Eiche im Schiff", "c": "Dendrochronologie"},
        {"n": "Pollenspektrum in Moorschicht", "c": "Palynologie"},
        {"n": "Thermo-Lumineszenz von gebranntem Ton", "c": "TL-Datierung"},
        {"n": "Stratigraphische Position der Scherbe", "c": "Stratigraphie"},
        {"n": "Uran-Thorium in Korallenriff", "c": "U/Th-Datierung"},
        {"n": "Magnetisierung von Lehmziegeln", "c": "Archaeomagnetismus"},
        {"n": "Optisch stimulierte Lumineszenz im Quarz", "c": "OSL-Datierung"},
        {"n": "Aminosaeure-Racemisierung in Muscheln", "c": "AAR-Datierung"},
    ],
    "3d_methoden": [
        {"n": "Unterirdische Mauern unter Acker", "c": "Bodenradar (GPR)"},
        {"n": "Farbabweichungen in Ernte", "c": "Luftfotografie"},
        {"n": "Reliefkarte unter Baumkronen", "c": "LiDAR"},
        {"n": "Detailmodell einer Steininschrift", "c": "Photogrammetrie"},
        {"n": "Magnetische Anomalie einer Grube", "c": "Magnetometrie"},
        {"n": "Leitfaehigkeitsmessung Pfostenreihe", "c": "EM-Survey"},
        {"n": "3D-Farbdruck eines Gefaessfragments", "c": "3D-Druck"},
        {"n": "Multispektralfoto verblasster Inschrift", "c": "RTI / DStretch"},
    ],
    "schriften": [
        {"n": "Rongorongo", "c": "Osterinsel"},
        {"n": "Lineares A", "c": "Minoisch (undechiffriert)"},
        {"n": "Indus-Schrift", "c": "Indus-Tal-Zivilisation"},
        {"n": "Nahuatl-Piktogramme", "c": "Azteken"},
        {"n": "Ogham-Schrift", "c": "Keltisch / Irland"},
        {"n": "Nabataeische Schrift", "c": "Nabataeer"},
        {"n": "Phoenizisches Alphabet", "c": "Phoenizier"},
        {"n": "Meroitische Schrift", "c": "Meroe / Kush"},
    ],
    "goetter": [
        {"n": "Quetzalcoatl", "c": "Azteken"},
        {"n": "Inanna", "c": "Sumer"},
        {"n": "Thor", "c": "Wikinger"},
        {"n": "Amaterasu", "c": "Japan"},
        {"n": "Pachamama", "c": "Inka"},
        {"n": "Huitzilopochtli", "c": "Azteken"},
        {"n": "Enlil", "c": "Mesopotamien"},
        {"n": "Lugh", "c": "Keltisch"},
    ],
    "bestattungsriten": [
        {"n": "Hockerbestattung mit Ocker", "c": "Jungsteinzeit"},
        {"n": "Brandbestattung auf Scheiterhaufen", "c": "Wikinger / Hindu"},
        {"n": "Baumbestattung (Luftbestattung)", "c": "Nordamerikanische Staemme"},
        {"n": "Exkarnation (Sky Burial)", "c": "Tibet"},
        {"n": "Mumifizierung mit Natron", "c": "Aegypten"},
        {"n": "Bootsgrab mit Waffen und Schmuck", "c": "Wikinger"},
        {"n": "Urnenfeldgrab", "c": "Urnenfelderkultur"},
        {"n": "Kammergrab mit Dromos", "c": "Mykene / Griechenland"},
    ],
    "stratigraphie": [
        {"n": "Eine Muenze datiert die Schicht, in der sie liegt", "c": "Terminus post quem"},
        {"n": "Spaetere Grube schneidet aeltere Schicht", "c": "Stratigraphischer Kontakt"},
        {"n": "Alle Schichten in Sequenz folgen aufeinander", "c": "Superposition"},
        {"n": "Gleicher Fundtyp in zwei raeumlich getrennten Schichten", "c": "Korrelation"},
        {"n": "Schicht wird durch Baumwurzel gestoert", "c": "Postdepositionaler Prozess"},
        {"n": "Scherbe aus tieferer Schicht in juengerer Position", "c": "Intrusion"},
        {"n": "Abfolge von Ascheschichten nach Vulkanausbruch", "c": "Tephra-Chronologie"},
        {"n": "Schnittstelle zwischen Baugrube und Planum", "c": "Befundgrenze"},
    ],
    "keramikstile": [
        {"n": "Schnurkeramik (Corded Ware)", "c": "Mitteleuropa Spaetneolithikum"},
        {"n": "Bandkeramik (LBK)", "c": "Fruehneolithikum Europa"},
        {"n": "Beaker-Kultur-Becher", "c": "Westeuropa Bronzezeit"},
        {"n": "Majolika-Fayence", "c": "Islamisch / Renaissance"},
        {"n": "Nazca-Polychromkeramik", "c": "Peru (Nazca-Kultur)"},
        {"n": "Joemon-Keramik", "c": "Japan"},
        {"n": "Yangshao-Spiraldekor", "c": "China (Neolithikum)"},
        {"n": "Raku-Glasur (Teeschale)", "c": "Japan"},
    ],
    "numismatik": [
        {"n": "Obol des Charon (Bestattungsmuenze)", "c": "Griechenland"},
        {"n": "Aureus (Goldmuenze)", "c": "Roemer"},
        {"n": "Dirham (Silber)", "c": "Islamisch"},
        {"n": "Stater (Elektrum)", "c": "Lydien"},
        {"n": "Daric (Goldmuenze)", "c": "Persien"},
        {"n": "Solidus (Byzanz)", "c": "Byzanz"},
        {"n": "Cash (quadratisches Loch)", "c": "China"},
        {"n": "Schekel (Silber-Gewichtseinheit)", "c": "Phoenizien / Israel"},
    ],
    "isotopenanalyse": [
        {"n": "Blei-206/204-Verhaeltnis in Bronze", "c": "Rohstoffherkunft"},
        {"n": "Stickstoff-15-Anreicherung im Knochen", "c": "Proteinanteil Ernaehrung"},
        {"n": "Sauerstoff-18-Verhaeltnis in Zahnschmelz", "c": "Klimarekonstruktion"},
        {"n": "Kupfer-Isotope in Bronzewaffe", "c": "Bergbauregion"},
        {"n": "Kohlenstoff-13 in Mais", "c": "C4-Pflanzen Ernaehrung"},
        {"n": "Schwefel-34 in Meeresknochen", "c": "Kuestennahe Ernaehrung"},
        {"n": "Uran-Thorium in Kalzit-Schicht", "c": "Altersdatierung"},
        {"n": "Argon-40-Verhaeltnis in Vulkangestein", "c": "K-Ar Datierung"},
    ],
    "museen": [
        {"n": "Antikythera-Mechanismus", "c": "Athen"},
        {"n": "Himmelsscheibe von Nebra", "c": "Halle (Saale)"},
        {"n": "Goldmaske von Mykene", "c": "Athen"},
        {"n": "Jade-Maske Pakal", "c": "Mexiko City"},
        {"n": "Tollund-Mann", "c": "Silkeborg"},
        {"n": "Benin-Bronzen (Hauptbestand)", "c": "London"},
        {"n": "Lewis-Schachfiguren", "c": "London / Edinburgh"},
        {"n": "Terrakotta-Armee", "c": "Xi'an"},
    ],
    "archaeobotanik": [
        {"n": "Weintraubenkerne in Amphore", "c": "Handel"},
        {"n": "Opium-Mohnrueckstaende in Gefaess", "c": "Medizin / Ritual"},
        {"n": "Feigenreste an Strandmarkt-Funde", "c": "Nahrungsmittel"},
        {"n": "Palmenbluetenstaub in aegyptischer Grabkammer", "c": "Ritual / Religion"},
        {"n": "Korianderreste in Pompeji-Speicher", "c": "Gewuerze / Kueche"},
        {"n": "Birkenpech als Klebstoff (Neandertaler)", "c": "Werkzeugherstellung"},
        {"n": "Leinensamen in jungsteinzeitlicher Grube", "c": "Textilproduktion"},
        {"n": "Kaffeepollen in osmanischer Schicht", "c": "Handels- / Kulturkontakt"},
    ],
    "handelsrouten": [
        {"n": "Pfefferkoerner aus Indien in Rom", "c": "Gewuerzroute"},
        {"n": "Lapislazuli aus Afghanistan in Aegypten", "c": "Lapislazuli-Route"},
        {"n": "Zinn aus Cornwall in Bronzezeit-Europa", "c": "Zinnhandelsroute"},
        {"n": "Obsidian aus Anatolien auf Zypern", "c": "Aegaeischer Seehandel"},
        {"n": "Elfenbein aus Afrika in phoenizischen Staedten", "c": "Transsahararoute"},
        {"n": "Rohseide in Palmyra", "c": "Seidenstrasse"},
        {"n": "Kupfer von Zypern in der Aegaeis", "c": "Ostmediterraner Seehandel"},
        {"n": "Bernstein aus Ostsee in Mykene", "c": "Bernsteinstrasse"},
    ],
    "waehrungen": [
        {"n": "Wampum-Perlen", "c": "Nordamerika (Irokesen)"},
        {"n": "Kauri-Muscheln", "c": "Suedostasien / Afrika"},
        {"n": "Sesterz (Bronzemuenze)", "c": "Roemer"},
        {"n": "Maravedi", "c": "Spanien (Mittelalter)"},
        {"n": "Golddinar", "c": "Islamisch"},
        {"n": "Hacksilber (Gewichtsgeld)", "c": "Wikinger"},
        {"n": "Kakaobaum-Samen als Waehrung", "c": "Azteken / Maya"},
        {"n": "Kaurischnecken als Standardgeld", "c": "China (Shang-Dynastie)"},
    ],
    "faelschungen": [
        {"n": "Protokoll der Weisen von Zion", "c": "Antisemitisches Pamphlet"},
        {"n": "Karte von Vinland", "c": "Mittelalterliche Karte"},
        {"n": "Glozel-Funde (Frankreich)", "c": "Neolithische Tafeln"},
        {"n": "Tasaday (Philippinen)", "c": "Steinzeitvolk"},
        {"n": "James Ossuary Inschrift", "c": "Knochenkiste"},
        {"n": "Archaeoraptor (National Geographic)", "c": "Dinosaurier-Vogel-Hybrid"},
        {"n": "Crystal Skull Smithsonian", "c": "Maya-Artefakt"},
        {"n": "Acambaro-Figuren (Mexiko)", "c": "Dinosaurier-Terrakotten"},
    ],
    "tempel_ordnungen": [
        {"n": "Tempel von Segesta", "c": "Dorisch"},
        {"n": "Tempel der Artemis Ephesos", "c": "Ionisch"},
        {"n": "Erechtheion Nordportikus", "c": "Ionisch"},
        {"n": "Tempel des Zeus Olympia", "c": "Dorisch"},
        {"n": "Lysikrates-Monument (Athen)", "c": "Korinthisch"},
        {"n": "Pantheon (Rom) -- Frontsaeulen", "c": "Korinthisch"},
        {"n": "Stoa von Attalos", "c": "Ionisch / Dorisch"},
        {"n": "Olympieion (Athen)", "c": "Korinthisch"},
    ],
    "indus_tal": [
        {"n": "Lothal", "c": "Indien (Gujarat)"},
        {"n": "Dholavira", "c": "Indien (Gujarat)"},
        {"n": "Rakhigarhi", "c": "Indien (Haryana)"},
        {"n": "Kalibangan", "c": "Indien (Rajasthan)"},
        {"n": "Chanhu-daro", "c": "Pakistan"},
        {"n": "Sutkagen Dor", "c": "Pakistan (Baluchistan)"},
        {"n": "Alamgirpur", "c": "Indien (Uttar Pradesh)"},
        {"n": "Banawali", "c": "Indien (Haryana)"},
    ],
    "wikinger": [
        {"n": "Jorvik (York)", "c": "Grossbritannien"},
        {"n": "Birka", "c": "Schweden"},
        {"n": "Kaupang", "c": "Norwegen"},
        {"n": "Trelleborg (Ringburg)", "c": "Daenemark"},
        {"n": "Hedeby (Haithabu)", "c": "Deutschland"},
        {"n": "Ribe", "c": "Daenemark"},
        {"n": "Dublin (Dyflin)", "c": "Irland"},
        {"n": "Novgorod (Wikinger-Schicht)", "c": "Russland"},
    ],
    "repatriierung": [
        {"n": "Obelisk von Axum (war in Rom)", "c": "Aethiopien"},
        {"n": "Moai aus Chile (im Britischen Museum)", "c": "Chile / Osterinsel"},
        {"n": "Skull of Hoa Hakananai'a", "c": "Osterinsel"},
        {"n": "Lusatian Treasures (in Berlin)", "c": "Polen"},
        {"n": "Lydian Hoard (in NY Metropolitan)", "c": "Tuerkei"},
        {"n": "Priams Treasure (in Moskau)", "c": "Tuerkei / Deutschland"},
        {"n": "Kennewick Man (USA -- Repatriierung 2017)", "c": "Colville-Stamm"},
        {"n": "Benin-Bronzen (Einigung 2022)", "c": "Nigeria"},
    ],
    "popkultur_vs_realitaet": [
        {"n": "Mumienfluche (Tutanchamun)", "c": "Legende"},
        {"n": "Atlantis (Platon)", "c": "Literarische Allegorie"},
        {"n": "Pyramiden als Getreidespeicher", "c": "Historisch falsch"},
        {"n": "Roemer trugen Sandalen im Schnee", "c": "Vereinfacht"},
        {"n": "Wikinger hatten Hoernerhelme", "c": "Historisch falsch"},
        {"n": "Cleopatra war ptolemaeisch, nicht aegyptisch", "c": "Historisch korrekt"},
        {"n": "Gladiatoren kaempften selten bis zum Tod", "c": "Historisch korrekt"},
        {"n": "Stonehenge wurde von Druiden gebaut", "c": "Historisch falsch"},
    ],
    "welterbe_gefahr": [
        {"n": "Nimrud (Irak)", "c": "Terrorismus / Krieg"},
        {"n": "Timbuktu (Mali)", "c": "Islamistischer Extremismus"},
        {"n": "Machu Picchu", "c": "Massentourismus"},
        {"n": "Lascaux (Original)", "c": "Schimmel durch Tourismus"},
        {"n": "Sanaa (Jemen)", "c": "Krieg"},
        {"n": "Everglades (Florida)", "c": "Entwaesserung / Klima"},
        {"n": "Rapa Nui / Osterinsel", "c": "Klimawandel / Erosion"},
        {"n": "Palmyra (Syrien)", "c": "Krieg / ISIS"},
    ],
    "zufallsfunde": [
        {"n": "Goldschatz von Varna", "c": "Baggerfuehrer"},
        {"n": "Hoxne-Schatz", "c": "Metalldetektorist"},
        {"n": "Staffordshire Hoard", "c": "Metalldetektorist"},
        {"n": "Willendorf-Venus", "c": "Eisenbahnarbeiter"},
        {"n": "Nag-Hammadi-Kodizes", "c": "Bauer"},
        {"n": "Oetzi der Eismann", "c": "Wanderer"},
        {"n": "Schriftrollen vom Toten Meer", "c": "Beduinen-Hirte"},
        {"n": "Lascaux-Hoehle", "c": "Kinder beim Spielen"},
    ],
    "digifund_epochen": [
        {"n": "Virtual Stonehenge (360 Grad)", "c": "Jungsteinzeit"},
        {"n": "Pompeji 3D-Rekonstruktion", "c": "Roemerzeit"},
        {"n": "Angkor Wat LiDAR-Survey", "c": "Mittelalter"},
        {"n": "Gobekli Tepe VR-Tour", "c": "Praeneolithikum"},
        {"n": "Notre-Dame-de-Paris Scan (2019)", "c": "Mittelalter"},
        {"n": "Herculaneum Scroll Entzifferung (AI)", "c": "Antike"},
        {"n": "Teotihuacan Tunnelscan", "c": "Praeklassik"},
        {"n": "Versailles 3D (Barock)", "c": "Fruehe Neuzeit"},
    ],
    "antike_medizin": [
        {"n": "Edwin Smith Papyrus (chirurgische Anweisungen)", "c": "Aegypten"},
        {"n": "Galenus' Vier-Saefte-Lehre", "c": "Roemer / Griechenland"},
        {"n": "Ayurveda (Charaka Samhita)", "c": "Indien"},
        {"n": "Imhotep als Arzt-Gottheit", "c": "Aegypten"},
        {"n": "Akupunktur (Bian Que Tradition)", "c": "China"},
        {"n": "Hammurabi-Kodex Arzt-Paragraphen", "c": "Babylonien"},
        {"n": "Inka-Trepanation (Schaedeloperation)", "c": "Peru"},
        {"n": "Epidauros-Asklepion (Tempel-Heilung)", "c": "Griechenland"},
    ],
    "schatzsuche_methoden": [
        {"n": "Waermeanomalie ueber Hohlraum im Fels", "c": "Thermografie"},
        {"n": "Seismische Reflexion fuer tiefe Strukturen", "c": "Seismik"},
        {"n": "Anomalie durch Metallgehalt im Boden", "c": "Metalldetektoren"},
        {"n": "Farbkontrast Reifespuren im Luftbild", "c": "Luftfotografie"},
        {"n": "Leitfaehigkeitsmessung von Steinmauern", "c": "EM-Survey"},
        {"n": "Magnetische Abweichung durch Eisenerzfunde", "c": "Magnetometrie"},
        {"n": "Unterwasserstruktur im Sonar-Echolot", "c": "Side-Scan-Sonar"},
        {"n": "Mikrovibration im Boden durch Hohlraum", "c": "Mikrogravimetrie"},
    ],
    "antike_astronomie": [
        {"n": "Sonnenwende-Ausrichtung bei Newgrange", "c": "Keltisch / Neolithisch"},
        {"n": "Plejaden-Zaehlung auf Himmelsscheibe Nebra", "c": "Bronzezeit"},
        {"n": "Heliacal Rising des Sirius -- Nilflut", "c": "Aegypten"},
        {"n": "Venustafeln des Ammi-saduqa", "c": "Babylonien"},
        {"n": "Dresden Codex -- Maya Astronomie", "c": "Maya"},
        {"n": "Antikythera-Mechanismus Mondphase", "c": "Griechenland"},
        {"n": "Bighorn Medicine Wheel -- Sonnenwende", "c": "Nordamerika"},
        {"n": "Abu Simbel Tempel -- Aequinoktium-Licht", "c": "Aegypten"},
    ],
}

match_items_added = 0
for key, new_items in match_additions.items():
    assert key in match_data, f"Key '{key}' not found in archaeologie_match.json"
    before = len(match_data[key]['items'])
    match_data[key]['items'].extend(new_items)
    after = len(match_data[key]['items'])
    match_items_added += (after - before)
    assert after == 20, f"Category '{key}' has {after} items, expected 20"

with open(match_path, 'w', encoding='utf-8') as f:
    json.dump(match_data, f, ensure_ascii=False, indent=2)

with open(match_path, 'r', encoding='utf-8') as f:
    verify_match = json.load(f)
for key in match_data:
    assert len(verify_match[key]['items']) == 20
print(f"  [OK] archaeologie_match.json: {match_items_added} items added, all {len(match_data)} categories now have 20 items")

total_json_items_added = pin_items_added + hl_items_added + match_items_added
print(f"\n  [SUMMARY] Total JSON items added: {total_json_items_added}")

# ============================================================
# FIX 4: Extend verify.py JSON checks
# ============================================================
print("\n--- Fix 4: Extend verify.py JSON file checks ---")

with open(VERIFY_PY, 'r', encoding='utf-8') as f:
    vc = f.read()

old_check = "for fname in ['kultur.json', 'tiere_hl.json', 'tiere_match.json', 'tiere_ws.json']:"

new_check = """for fname in [
        'kultur.json', 'tiere_hl.json', 'tiere_match.json', 'tiere_ws.json',
        'pflanzen_pin.json', 'pflanzen_hl.json', 'pflanzen_match.json', 'pflanzen_ws.json',
        'gastro_pin.json', 'gastro_hl.json', 'gastro_match.json', 'gastro_ws.json',
        'tech_pin.json', 'tech_hl.json', 'tech_match.json', 'tech_ws.json',
        'emob_pin.json', 'emob_hl.json', 'emob_match.json', 'emob_ws.json',
        'archaeologie_pin.json', 'archaeologie_hl.json', 'archaeologie_match.json', 'archaeologie_ws.json',
    ]:"""

assert vc.count(old_check) == 1, f"Expected exactly 1 occurrence of old check, got {vc.count(old_check)}"
vc = vc.replace(old_check, new_check, 1)
assert new_check in vc, "Replacement not found after replace()"

with open(VERIFY_PY, 'w', encoding='utf-8') as f:
    f.write(vc)
print("  [OK] verify.py updated: JSON file list expanded from 4 to 24 files")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("PATCH COMPLETE")
print(f"  Fix 1: {beta_added} [BETA] tags added to technologie/emobilitaet/archaeologie modes")
print(f"  Fix 2: {pflanzen_changed} pflanzen mode lines: group:tiere -> group:pflanzen")
print(f"  Fix 3: {total_json_items_added} items added to archaeologie JSON files")
print(f"         - archaeologie_pin.json:   {pin_items_added} items (13 categories x 8)")
print(f"         - archaeologie_hl.json:    {hl_items_added} items (12 categories x 8)")
print(f"         - archaeologie_match.json: {match_items_added} items (28 categories x 8)")
print(f"  Fix 4: verify.py JSON checks expanded from 4 to 24 files")
print("=" * 60)
