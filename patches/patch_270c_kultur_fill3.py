"""
patch_270c_kultur_fill3.py — Dritter & letzter Pass
Alle verbleibenden ⚠️ kultur.json-Keys auf 40+ Items bringen.
"""
import json, os

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

# ── BAHNSTRECKEN  (38 → 43) ───────────────────────────────────────────────
report['bahnstrecken'] = kext(data['bahnstrecken'], [
    {"n": "Gotthard-Basistunnel",          "c": "Schweiz"},
    {"n": "Kanada-Pazifikbahn (CPR)",       "c": "Kanada"},
    {"n": "Highveld-Linie",                "c": "Südafrika"},
    {"n": "Lhasa-Eisenbahn",               "c": "China"},
    {"n": "Flam-Bahn",                     "c": "Norwegen"},
])

# ── BRÜCKEN pin  (37 → 43) ────────────────────────────────────────────────
report['bruecken'] = kext_pin(data['bruecken'], [
    {"n": "Millau-Viadukt",        "lat": 44.099, "lng": 3.026,   "c": "Frankreich"},
    {"n": "Øresund-Brücke",        "lat": 55.583, "lng": 12.917,  "c": "Dänemark"},
    {"n": "Tower Bridge",          "lat": 51.506, "lng": -0.076,  "c": "Vereinigtes Königreich"},
    {"n": "Sydney Harbour Bridge", "lat": -33.852,"lng": 151.211, "c": "Australien"},
    {"n": "Danyang-Kunshan-Viadukt","lat": 31.9,  "lng": 121.2,   "c": "China"},
    {"n": "Akashi-Kaikyō-Brücke",  "lat": 34.616, "lng": 135.017,"c": "Japan"},
])

# ── GOTTESHÄUSER pin  (33 → 43) ───────────────────────────────────────────
report['gotteshaeuser'] = kext_pin(data['gotteshaeuser'], [
    {"n": "Notre-Dame de Paris",       "lat": 48.853,  "lng": 2.350,   "c": "Frankreich"},
    {"n": "Sagrada Família",           "lat": 41.404,  "lng": 2.174,   "c": "Spanien"},
    {"n": "Kölner Dom",                "lat": 50.941,  "lng": 6.958,   "c": "Deutschland"},
    {"n": "Pantheon (Rom)",            "lat": 41.899,  "lng": 12.477,  "c": "Italien"},
    {"n": "Shwedagon-Pagode",          "lat": 16.798,  "lng": 96.150,  "c": "Myanmar"},
    {"n": "Temple of Heaven",          "lat": 39.882,  "lng": 116.406, "c": "China"},
    {"n": "Angkor Wat",                "lat": 13.412,  "lng": 103.867, "c": "Kambodscha"},
    {"n": "Borobudur",                 "lat": -7.608,  "lng": 110.204, "c": "Indonesien"},
    {"n": "Meenakshi-Amman-Tempel",    "lat": 9.920,   "lng": 78.119,  "c": "Indien"},
    {"n": "Rock-Hewn-Churches Lalibela","lat": 12.031,  "lng": 39.047, "c": "Äthiopien"},
])

# ── GRENZFLÜSSE  (35 → 42) ────────────────────────────────────────────────
report['grenzfluesse'] = kext(data['grenzfluesse'], [
    {"n": "Jordan (Grenze zu)",        "c": "Jordanien"},
    {"n": "Amu Darya (Grenze zu)",     "c": "Afghanistan"},
    {"n": "Sambesi (Grenze zu)",       "c": "Sambia"},
    {"n": "Limpopo (Grenze zu)",       "c": "Simbabwe"},
    {"n": "Mekong (Grenze zu)",        "c": "Laos"},
    {"n": "Tumen (Grenze zu)",         "c": "Nordkorea"},
    {"n": "Oder (Grenze zu)",          "c": "Polen"},
])

# ── HAFEN_WORLD  (34 → 42) ────────────────────────────────────────────────
report['hafen_world'] = kext(data['hafen_world'], [
    {"n": "Hafen Singapur",            "c": "Singapur"},
    {"n": "Hafen Ningbo-Zhoushan",     "c": "China"},
    {"n": "Hafen Guangzhou",           "c": "China"},
    {"n": "Hafen Busan",               "c": "Südkorea"},
    {"n": "Hafen Jebel Ali",           "c": "VAE"},
    {"n": "Hafen Los Angeles",         "c": "USA"},
    {"n": "Hafen Colombo",             "c": "Sri Lanka"},
    {"n": "Hafen Piraeus",             "c": "Griechenland"},
])

# ── INSELGRUPPEN  (39 → 44) ───────────────────────────────────────────────
report['inselgruppen'] = kext(data['inselgruppen'], [
    {"n": "Seychellen",                "c": "Seychellen"},
    {"n": "Komoren",                   "c": "Komoren"},
    {"n": "São Tomé und Príncipe",     "c": "São Tomé und Príncipe"},
    {"n": "Salomonen",                 "c": "Salomonen"},
    {"n": "Turks- und Caicosinseln",   "c": "Vereinigtes Königreich"},
])

# ── KUNSTWERKE pin  (34 → 42) ─────────────────────────────────────────────
report['kunstwerke'] = kext_pin(data['kunstwerke'], [
    {"n": "Sixtinische Kapelle (Vatikan)",    "lat": 41.903,  "lng": 12.454, "c": "Vatikan"},
    {"n": "Guernica (Museo Reina Sofía)",     "lat": 40.408,  "lng": -3.694, "c": "Spanien"},
    {"n": "Der Schrei (Nationalmuseum Oslo)", "lat": 59.916,  "lng": 10.727, "c": "Norwegen"},
    {"n": "Nachtwache (Rijksmuseum)",         "lat": 52.360,  "lng": 4.885,  "c": "Niederlande"},
    {"n": "Starry Night (MoMA New York)",     "lat": 40.761,  "lng": -73.978,"c": "USA"},
    {"n": "Terrakotta-Armee (Xi'an)",         "lat": 34.384,  "lng": 109.274,"c": "China"},
    {"n": "Venus de Milo (Louvre)",           "lat": 48.861,  "lng": 2.336,  "c": "Frankreich"},
    {"n": "Pietà (Petersdom, Vatikan)",       "lat": 41.902,  "lng": 12.457, "c": "Vatikan"},
])

# ── METROSTÄDTE  (39 → 44) ────────────────────────────────────────────────
report['metrostaedte'] = kext(data['metrostaedte'], [
    {"n": "Mexico City Metro",         "c": "Mexiko"},
    {"n": "Kairo Metro",               "c": "Ägypten"},
    {"n": "Teheran Metro",             "c": "Iran"},
    {"n": "Washington Metro",          "c": "USA"},
    {"n": "Santiago Metro",            "c": "Chile"},
])

# ── NATIONALSPORT_OFF  (33 → 42) ──────────────────────────────────────────
report['nationalsport_off'] = kext(data['nationalsport_off'], [
    {"n": "Cricket (offiziell)",       "c": "England"},
    {"n": "Sumo (inoffiziell)",        "c": "Japan"},
    {"n": "Baseball (offiziell)",      "c": "Kuba"},
    {"n": "Volleyball (offiziell)",    "c": "Sri Lanka"},
    {"n": "Taekwondo (offiziell)",     "c": "Südkorea"},
    {"n": "Jiujutsu (offiziell)",      "c": "Brasilien"},
    {"n": "Muay Thai (offiziell)",     "c": "Thailand"},
    {"n": "Polo (inoffiziell)",        "c": "Argentinien"},
    {"n": "Shinty (offiziell)",        "c": "Schottland"},
])

# ── REEDEREIEN  (35 → 42) ─────────────────────────────────────────────────
report['reedereien'] = kext(data['reedereien'], [
    {"n": "CMA CGM",                   "c": "Frankreich"},
    {"n": "Evergreen Marine",          "c": "Taiwan"},
    {"n": "Yang Ming",                 "c": "Taiwan"},
    {"n": "ONE (Ocean Network Express)","c": "Japan"},
    {"n": "Hapag-Lloyd",               "c": "Deutschland"},
    {"n": "Wan Hai Lines",             "c": "Taiwan"},
    {"n": "ZIM Integrated Shipping",   "c": "Israel"},
])

# ── RUINEN pin  (34 → 43) ─────────────────────────────────────────────────
report['ruinen'] = kext_pin(data['ruinen'], [
    {"n": "Machu Picchu",         "lat": -13.163, "lng": -72.545, "c": "Peru"},
    {"n": "Chichén Itzá",         "lat": 20.683,  "lng": -88.569, "c": "Mexiko"},
    {"n": "Pompeji",              "lat": 40.748,  "lng": 14.489,  "c": "Italien"},
    {"n": "Ephesus",              "lat": 37.939,  "lng": 27.341,  "c": "Türkei"},
    {"n": "Knossos",              "lat": 35.297,  "lng": 25.163,  "c": "Griechenland"},
    {"n": "Palenque",             "lat": 17.483,  "lng": -92.046, "c": "Mexiko"},
    {"n": "Tikal",                "lat": 17.222,  "lng": -89.624, "c": "Guatemala"},
    {"n": "Skara Brae",           "lat": 59.049,  "lng": -3.342,  "c": "Vereinigtes Königreich"},
    {"n": "Great Zimbabwe",       "lat": -20.267, "lng": 30.933,  "c": "Simbabwe"},
])

# ── SURF_SPOTS pin  (35 → 43) ─────────────────────────────────────────────
report['surf_spots'] = kext_pin(data['surf_spots'], [
    {"n": "Nazaré",               "lat": 39.601,  "lng": -9.070},
    {"n": "Supertubes (Jeffreys Bay)","lat": -34.054,"lng": 24.924},
    {"n": "Hossegor",             "lat": 43.671,  "lng": -1.415},
    {"n": "Skeleton Bay (Namibia)","lat": -22.901, "lng": 14.509},
    {"n": "Chicama",              "lat": -7.849,  "lng": -79.444},
    {"n": "Nias Island",          "lat": 0.720,   "lng": 97.557},
    {"n": "Desert Point (Lombok)","lat": -8.788,  "lng": 115.965},
    {"n": "Cloudbreak (Fiji)",    "lat": -17.947, "lng": 177.127},
])

# ── WEINREGIONEN pin  (31 → 42) ───────────────────────────────────────────
report['wein_regionen'] = kext_pin(data['wein_regionen'], [
    {"n": "Mosel",                "lat": 50.000,  "lng": 7.100,   "c": "Deutschland"},
    {"n": "Rheingau",             "lat": 50.020,  "lng": 8.050,   "c": "Deutschland"},
    {"n": "Rioja",                "lat": 42.466,  "lng": -2.441,  "c": "Spanien"},
    {"n": "Ribera del Duero",     "lat": 41.626,  "lng": -3.689,  "c": "Spanien"},
    {"n": "Douro-Tal",            "lat": 41.150,  "lng": -7.510,  "c": "Portugal"},
    {"n": "Champagne",            "lat": 49.100,  "lng": 4.030,   "c": "Frankreich"},
    {"n": "Burgundy (Bourgogne)", "lat": 47.052,  "lng": 4.840,   "c": "Frankreich"},
    {"n": "Barossa Valley",       "lat": -34.530, "lng": 138.950, "c": "Australien"},
    {"n": "Marlborough",          "lat": -41.512, "lng": 173.961, "c": "Neuseeland"},
    {"n": "Stellenbosch",         "lat": -33.936, "lng": 18.861,  "c": "Südafrika"},
    {"n": "Mendoza",              "lat": -33.000, "lng": -68.820, "c": "Argentinien"},
])

# ── Save ──────────────────────────────────────────────────────────────────
with open(DATA, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("patch_270c — Ergebnis:")
for key, added in sorted(report.items()):
    total = len(data[key]) if isinstance(data[key], list) else len(data[key].get('items',[]))
    status = "✅" if total >= 40 else "⚠️ NOCH UNTER 40"
    print(f"  {key:30s}: +{added:2d} → {total:3d}  {status}")
