"""
patch_270_kultur_fill.py
Phase 270 — Datendichte-Fix: alle unter 40 Items liegenden kultur.json-Schlüssel
auf 40-50 Items bringen. Duplikat-Guard aktiv.
"""
import json, os, sys

DATA = os.path.join(os.path.dirname(__file__), '..', 'data', 'kultur.json')

def kext(lst, new_items, key='n'):
    seen = {it[key] for it in lst}
    added = 0
    for it in new_items:
        if it.get(key) not in seen:
            lst.append(it); seen.add(it[key]); added += 1
    return added

def kext_pin(lst, new_items):
    seen_n = {it['n'] for it in lst}
    seen_c = {(round(it['lat'],3), round(it['lng'],3)) for it in lst}
    added = 0
    for it in new_items:
        coord = (round(it['lat'],3), round(it['lng'],3))
        if it['n'] not in seen_n and coord not in seen_c:
            lst.append(it); seen_n.add(it['n']); seen_c.add(coord); added += 1
    return added

with open(DATA, encoding='utf-8') as f:
    data = json.load(f)

report = {}

# ── 1. ENKLAVE  (10 → 40) ──────────────────────────────────────────────────
new_enklave = [
    {"n": "Llívia",                  "c": "Spanien"},
    {"n": "Jungholz",                "c": "Österreich"},
    {"n": "Kleinwalsertal",          "c": "Österreich"},
    {"n": "Oecusse",                 "c": "Osttimor"},
    {"n": "Point Roberts",           "c": "USA"},
    {"n": "Northwest Angle",         "c": "USA"},
    {"n": "Madha",                   "c": "Oman"},
    {"n": "Nahwa",                   "c": "VAE"},
    {"n": "Sokh",                    "c": "Usbekistan"},
    {"n": "Vorukh",                  "c": "Tadschikistan"},
    {"n": "Shakhimardan",            "c": "Usbekistan"},
    {"n": "Barak",                   "c": "Kirgisistan"},
    {"n": "Gibraltar",               "c": "Vereinigtes Königreich"},
    {"n": "Peñón de Vélez de la Gomera", "c": "Spanien"},
    {"n": "Musandam",                "c": "Oman"},
    {"n": "Temburong",               "c": "Brunei"},
    {"n": "Dahagram-Angarpota",      "c": "Bangladesch"},
    {"n": "Baarle-Nassau",           "c": "Niederlande"},
    {"n": "Cooch Behar (Tin Bigha)", "c": "Indien"},
    {"n": "Dubrovnik-Halbinsel",     "c": "Kroatien"},
    {"n": "Uvira-Korridor",          "c": "Demokratische Republik Kongo"},
    {"n": "Peñones de Alhucemas",    "c": "Spanien"},
    {"n": "Islas Chafarinas",        "c": "Spanien"},
    {"n": "Oman-Enklave Wakan",      "c": "Oman"},
    {"n": "Courchevel (Vauclair)",   "c": "Frankreich"},
    {"n": "Llivia",                  "c": "Spanien"},
    {"n": "Kyaukpyu",                "c": "Myanmar"},
    {"n": "Siliguri-Korridor (Hühnerhalskorridor)", "c": "Indien"},
    {"n": "Wakhan-Korridor",         "c": "Afghanistan"},
    {"n": "Aktobe-Oblast-Zipfel",    "c": "Kasachstan"},
]
report['enklave'] = kext(data['enklave'], new_enklave)

# ── 2. DELTAMUENDUNGEN  (26 → 42) ─────────────────────────────────────────
new_delta = [
    {"n": "Amazonas-Delta",          "c": "Brasilien"},
    {"n": "Mississippi-Delta",       "c": "USA"},
    {"n": "Donau-Delta",             "c": "Rumänien"},
    {"n": "Irrawaddy-Delta",         "c": "Myanmar"},
    {"n": "Indus-Delta",             "c": "Pakistan"},
    {"n": "Ganges-Brahmaputra-Delta","c": "Bangladesch"},
    {"n": "Niger-Delta",             "c": "Nigeria"},
    {"n": "Orinoco-Delta",           "c": "Venezuela"},
    {"n": "Lena-Delta",              "c": "Russland"},
    {"n": "Okavango-Delta",          "c": "Botswana"},
    {"n": "Huang-He-Delta",          "c": "China"},
    {"n": "Yukon-Delta",             "c": "USA"},
    {"n": "Ebro-Delta",              "c": "Spanien"},
    {"n": "Po-Delta",                "c": "Italien"},
    {"n": "Rhein-Delta",             "c": "Niederlande"},
    {"n": "Mackenzie-Delta",         "c": "Kanada"},
]
report['deltamuendungen'] = kext(data['deltamuendungen'], new_delta)

# ── 3. LUFT_REKORDE  (25 → 42) ────────────────────────────────────────────
new_luft = [
    {"n": "Höchster Passagierflughafen (Daocheng Yading)",       "c": "China"},
    {"n": "Tiefstgelegener Flughafen (Quseir, Ägypten)",         "c": "Ägypten"},
    {"n": "Erster Überschallpassagierflug (Concorde)",           "c": "Frankreich"},
    {"n": "Erster Nonstop-Transatlantikflug (Alcock & Brown)",   "c": "Vereinigtes Königreich"},
    {"n": "Erster Solarflug um die Erde (Solar Impulse 2)",      "c": "Schweiz"},
    {"n": "Höchster Passagierjet (Concorde Mach 2, 18 km)",      "c": "Frankreich"},
    {"n": "Größtes Passagierflugzeug (Airbus A380)",             "c": "Frankreich"},
    {"n": "Erster Frachtflug über den Atlantik",                 "c": "USA"},
    {"n": "Kürzeste Linienflugstrecke (Westray–Papa Westray, 2 min)", "c": "Vereinigtes Königreich"},
    {"n": "Schnellstes Passagierflugzeug (Concorde, 2179 km/h)", "c": "Frankreich"},
    {"n": "Erster Heißluftballon (Montgolfier)",                 "c": "Frankreich"},
    {"n": "Längste Nonstop-Propellerflugstrecke (Lucky Lady II)","c": "USA"},
    {"n": "Erster Rundflug der Welt (Douglas World Cruiser)",    "c": "USA"},
    {"n": "Meistgeflogene Route der Welt (Jeju–Seoul)",          "c": "Südkorea"},
    {"n": "Meiste Passagiere pro Jahr – Flughafen (Atlanta Hartsfield)", "c": "USA"},
    {"n": "Erster Flug über den Südpol (Byrd Expedition)",       "c": "USA"},
    {"n": "Größter Frachtflughafen der Welt (Memphis International)", "c": "USA"},
]
report['luft_rekorde'] = kext(data['luft_rekorde'], new_luft)

# ── 4. MEERBUSEN  (33 → 43) ───────────────────────────────────────────────
new_meerbusen = [
    {"n": "Golf von Bengalen",       "c": "Bangladesch"},
    {"n": "Persischer Golf",         "c": "Iran"},
    {"n": "Golf von Oman",           "c": "Oman"},
    {"n": "Golf von Aden",           "c": "Jemen"},
    {"n": "Golf von Tonkin",         "c": "Vietnam"},
    {"n": "Golf von Thailand",       "c": "Thailand"},
    {"n": "Golf von Carpentaria",    "c": "Australien"},
    {"n": "Korinthischer Golf",      "c": "Griechenland"},
    {"n": "Golf von Triest",         "c": "Italien"},
    {"n": "Golf von Valencia",       "c": "Spanien"},
]
report['meerbusen'] = kext(data['meerbusen'], new_meerbusen)

# ── 5. HALBINSELN  (34 → 44) ──────────────────────────────────────────────
new_halbinseln = [
    {"n": "Malaiische Halbinsel",    "c": "Malaysia"},
    {"n": "Kamtschatka",             "c": "Russland"},
    {"n": "Kola-Halbinsel",          "c": "Russland"},
    {"n": "Taimyr-Halbinsel",        "c": "Russland"},
    {"n": "Yamal-Halbinsel",         "c": "Russland"},
    {"n": "Gaspésie",                "c": "Kanada"},
    {"n": "Labrador-Halbinsel",      "c": "Kanada"},
    {"n": "Baja California",         "c": "Mexiko"},
    {"n": "Yucatán",                 "c": "Mexiko"},
    {"n": "Sinai-Halbinsel",         "c": "Ägypten"},
]
report['halbinseln'] = kext(data['halbinseln'], new_halbinseln)

# ── 6. SEEN_MATCH  (34 → 44) ──────────────────────────────────────────────
new_seen = [
    {"n": "Kaspisches Meer",         "c": "Kasachstan"},
    {"n": "Aralsee",                 "c": "Usbekistan"},
    {"n": "Huronsee",                "c": "Kanada"},
    {"n": "Michigansee",             "c": "USA"},
    {"n": "Eriesee",                 "c": "USA"},
    {"n": "Ontariosee",              "c": "Kanada"},
    {"n": "Ladogasee",               "c": "Russland"},
    {"n": "Onega-See",               "c": "Russland"},
    {"n": "Balaton",                 "c": "Ungarn"},
    {"n": "Genfer See",              "c": "Schweiz"},
]
report['seen_match'] = kext(data['seen_match'], new_seen)

# ── 7. KAPS  (36 → 46) ────────────────────────────────────────────────────
new_kaps = [
    {"n": "Kap Farvel",              "c": "Grönland"},
    {"n": "Kap Chelyuskin",          "c": "Russland"},
    {"n": "Kap Agulhas",             "c": "Südafrika"},
    {"n": "Ras Hafun",               "c": "Somalia"},
    {"n": "Kap Bojador",             "c": "Marokko"},
    {"n": "Kap Verde (Kap Blanc)",   "c": "Senegal"},
    {"n": "Kap Finisterre",          "c": "Spanien"},
    {"n": "Kap Skagen",              "c": "Dänemark"},
    {"n": "Kap Dezhnev",             "c": "Russland"},
    {"n": "Kap York",                "c": "Australien"},
]
report['kaps'] = kext(data['kaps'], new_kaps)

# ── 8. BERGGIPFEL pin  (42 → 52) ──────────────────────────────────────────
new_berge = [
    {"n": "Kazbek",          "lat": 42.699,  "lng": 44.518},
    {"n": "Belukha",         "lat": 49.807,  "lng": 86.593},
    {"n": "Pico de Orizaba", "lat": 19.030,  "lng": -97.270},
    {"n": "Mount Logan",     "lat": 60.567,  "lng": -140.405},
    {"n": "Puncak Jaya",     "lat": -4.079,  "lng": 137.158},
    {"n": "Mount Wilhelm",   "lat": -5.779,  "lng": 145.028},
    {"n": "Vinson Massif",   "lat": -78.526, "lng": -85.617},
    {"n": "Nevado Sajama",   "lat": -18.106, "lng": -68.885},
    {"n": "Cotopaxi",        "lat": -0.684,  "lng": -78.436},
    {"n": "Popocatépetl",    "lat": 19.023,  "lng": -98.622},
]
report['berggipfel'] = kext_pin(data['berggipfel'], new_berge)

# ── 9. WASSERFAELLE pin  (45 → 52) ────────────────────────────────────────
new_falls = [
    {"n": "Sutherland-Fälle",       "lat": -44.816, "lng": 167.993},
    {"n": "Yosemite-Fälle",         "lat": 37.756,  "lng": -119.596},
    {"n": "Kaieteur-Fälle",         "lat": 5.174,   "lng": -59.484},
    {"n": "Jim-Jim-Fälle",          "lat": -13.274, "lng": 132.846},
    {"n": "Gavarnie-Wasserfall",    "lat": 42.728,  "lng": -0.006},
    {"n": "Gullfoss",               "lat": 64.327,  "lng": -20.121},
    {"n": "Hraunfossar",            "lat": 64.727,  "lng": -21.517},
    {"n": "Marmore-Wasserfälle",    "lat": 42.577,  "lng": 12.709},
]
report['wasserfaelle'] = kext_pin(data['wasserfaelle'], new_falls)

# ── Save ───────────────────────────────────────────────────────────────────
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("patch_270_kultur_fill.py — Ergebnis:")
for key, added in sorted(report.items()):
    entry = data[key]
    total = len(entry) if isinstance(entry, list) else len(entry.get('items',[]))
    print(f"  {key:30s}: +{added} neue → {total} Items gesamt")
