"""
patch_301_housekeeping.py
Phase 301 — Final Housekeeping:
1. JSON-Duplikate entfernen (geo_pin, tiere_pin, archaeologie_pin, astro_match, tech_match)
2. MODE_CATS zuege Cleanup (hl_b_rail/uk_bahnstrecken falls doppelt)
3. Data-Upscale: zug_taktfrequenz, zug_panorama, zug_vkm, zug_bahnhof_bau auf 80+
"""
import os, json, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def dedupe_safe(items):
    """Duplikate sicher entfernen — erkennt automatisch den richtigen Name-Key."""
    seen = set()
    result = []
    for item in items:
        # Versuche alle moeglichen Name-Keys
        key_val = item.get("n") or item.get("name") or item.get("subject") or str(item)
        if key_val not in seen:
            seen.add(key_val)
            result.append(item)
    return result

def extend_safe(arr, new_items, key_field="n"):
    """Nur Items hinzufuegen die noch nicht vorhanden sind."""
    existing = {i.get(key_field,"") for i in arr}
    added = 0
    for item in new_items:
        if item.get(key_field,"") not in existing:
            arr.append(item)
            existing.add(item[key_field])
            added += 1
    return added

print("=" * 58)
print(" Patch 301 — Final Housekeeping")
print("=" * 58)

# =============================================================
# TEIL 1: JSON-Duplikate entfernen
# =============================================================
print("\n[1] Duplikate entfernen")

for fname in ["geo_pin.json", "tiere_pin.json", "archaeologie_pin.json"]:
    path = os.path.join(BASE, "data", fname)
    with open(path, "r", encoding="utf-8") as f: d = json.load(f)
    total_removed = 0
    for key in d:
        val = d[key]
        if isinstance(val, dict) and "items" in val:
            before = len(val["items"])
            val["items"] = dedupe_safe(val["items"])
            removed = before - len(val["items"])
            if removed:
                print(f"  {fname}/{key}: -{removed} ({before}→{len(val['items'])})")
                total_removed += removed
        elif isinstance(val, list) and val and isinstance(val[0], dict):
            before = len(val)
            d[key] = dedupe_safe(val)
            removed = before - len(d[key])
            if removed:
                print(f"  {fname}/{key}: -{removed} ({before}→{len(d[key])})")
                total_removed += removed
    if total_removed:
        with open(path, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"  [OK] {fname}: {total_removed} Duplikate gesamt entfernt")
    else:
        print(f"  [--] {fname}: keine Duplikate")

for fname in ["astro_match.json", "tech_match.json"]:
    path = os.path.join(BASE, "data", fname)
    with open(path, "r", encoding="utf-8") as f: d = json.load(f)
    total_removed = 0
    for key in d:
        val = d[key]
        if isinstance(val, dict) and "items" in val:
            before = len(val["items"])
            val["items"] = dedupe_safe(val["items"])
            removed = before - len(val["items"])
            if removed:
                print(f"  {fname}/{key}: -{removed}")
                total_removed += removed
    if total_removed:
        with open(path, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)
        print(f"  [OK] {fname}: {total_removed} Duplikate entfernt")
    else:
        print(f"  [--] {fname}: keine Duplikate")

# =============================================================
# TEIL 2: MODE_CATS zuege cleanup
# =============================================================
print("\n[2] MODE_CATS zuege — Doppeleintraege pruefen")
gen_path = os.path.join(BASE, "gen.py")
with open(gen_path, "r", encoding="utf-8") as f: g = f.read()

idx = g.find('zuege:{label:')
end = g.find('},', idx)
zuege_block = g[idx:end+2]

changed = False
for mode in ["hl_b_rail", "uk_bahnstrecken", "zug_ds100", "zug_metro_logos"]:
    count = zuege_block.count(f'"{mode}"')
    if count > 1:
        # Remove the second occurrence
        first = zuege_block.find(f'"{mode}"')
        second = zuege_block.find(f'"{mode}"', first + 1)
        # Remove with surrounding comma
        for pattern in [f'"{mode}",', f',"{mode}"']:
            if zuege_block.count(pattern) > 1:
                zuege_block = zuege_block.replace(pattern, pattern[:-1] if pattern.endswith(',') else pattern[1:], 1)
                changed = True
                print(f"  [OK] Duplikat '{mode}' entfernt")
                break
    elif count == 0:
        print(f"  [--] '{mode}' nicht in zuege (OK wenn woanders)")
    else:
        print(f"  [OK] '{mode}' genau 1x vorhanden")

if changed:
    g = g[:idx] + zuege_block + g[end+2:]
    with open(gen_path, "w", encoding="utf-8") as f: f.write(g)
else:
    print("  [--] Keine Duplikate gefunden")

# =============================================================
# TEIL 3: Data-Upscale — alle 4 Arrays auf 80+
# =============================================================
print("\n[3] Data-Upscale auf 80+ Items")

# --- 3a: zug_taktfrequenz (sport_hl.json, {name, val}) ---
with open(os.path.join(BASE, "data", "sport_hl.json"), "r", encoding="utf-8") as f: s = json.load(f)

NEW_TAKT = [
    {"name": "Paris Metro Linie 13 (HVZ)", "val": 20},
    {"name": "London Elizabeth Line (HVZ)", "val": 24},
    {"name": "London Northern Line (HVZ)", "val": 24},
    {"name": "London Victoria Line (HVZ)", "val": 36},
    {"name": "Berlin U6 Stosszeit", "val": 12},
    {"name": "Berlin S1 (HVZ)", "val": 10},
    {"name": "Muenchen S8 Stosszeit", "val": 10},
    {"name": "Hamburg U1 (HVZ)", "val": 10},
    {"name": "Hamburg S3 Stosszeit", "val": 10},
    {"name": "Wien S45 Stadtbahn (HVZ)", "val": 10},
    {"name": "Zuerich S2 S-Bahn (HVZ)", "val": 6},
    {"name": "Basel S-Bahn (HVZ)", "val": 6},
    {"name": "Kopenhagen Metro M2 (24h)", "val": 20},
    {"name": "Stockholm T-bana T14 (HVZ)", "val": 15},
    {"name": "Oslo Metro Linie 4 (HVZ)", "val": 10},
    {"name": "Madrid Cercanias C1 (HVZ)", "val": 12},
    {"name": "Barcelona Metro L5 (HVZ)", "val": 15},
    {"name": "Mailand Metro M1 (HVZ)", "val": 12},
    {"name": "Tokio Chuo Rapid Line (Stosszeit)", "val": 22},
    {"name": "Tokio Keio Linie (Stosszeit)", "val": 24},
    {"name": "Osaka Keihan Main Line (Stosszeit)", "val": 20},
    {"name": "Delhi Metro Yellow Line (HVZ)", "val": 20},
    {"name": "Mumbai Suburban Western (Stosszeit)", "val": 30},
    {"name": "RER D Paris (HVZ)", "val": 12},
    {"name": "Thalys Paris–Bruessel (HVZ)", "val": 2},
    {"name": "ICE Berlin–Hamburg (HVZ)", "val": 2},
    {"name": "DB RE1 Koeln–Aachen (HVZ)", "val": 4},
    {"name": "S-Bahn Stuttgart S1 (HVZ)", "val": 10},
]

existing_takt = {i["name"] for i in s["zug_taktfrequenz"]["items"]}
added_t = 0
for item in NEW_TAKT:
    if item["name"] not in existing_takt:
        s["zug_taktfrequenz"]["items"].append(item)
        existing_takt.add(item["name"])
        added_t += 1

with open(os.path.join(BASE, "data", "sport_hl.json"), "w", encoding="utf-8") as f: json.dump(s, f, ensure_ascii=False, indent=2)
print(f"  [OK] zug_taktfrequenz: +{added_t} → {len(s['zug_taktfrequenz']['items'])} Items")

# --- 3b: zug_panorama + zug_vkm (kultur.json) ---
with open(os.path.join(BASE, "data", "kultur.json"), "r", encoding="utf-8") as f: k = json.load(f)

NEW_PANORAMA = [
    {"n": "TranzAlpine (Christchurch–Greymouth, Neuseeland)", "c": "Neuseeland"},
    {"n": "Coastal Pacific (Picton–Christchurch)", "c": "Neuseeland"},
    {"n": "Northern Explorer (Auckland–Wellington)", "c": "Neuseeland"},
    {"n": "Inlandsbahn (Inlandsbanan, Gaelvare–Kristinehamn)", "c": "Schweden"},
    {"n": "Nariz del Diablo (Teufelsnase, Ecuador)", "c": "Ecuador"},
    {"n": "Serra Verde Express (Curitiba–Morretes)", "c": "Brasilien"},
    {"n": "White Pass & Yukon Route (Skagway–Whitehorse)", "c": "USA"},
    {"n": "Harz-Schmalspurbahn (Wernigerode–Brocken)", "c": "Deutschland"},
    {"n": "Chepe Express (Chihuahua–Los Mochis)", "c": "Mexiko"},
    {"n": "Shunka Shuutou (Herbst-Express Tohoku, Japan)", "c": "Japan"},
    {"n": "Puffing Billy Railway (Melbourne, Dampfzug)", "c": "Australien"},
    {"n": "Kuranda Scenic Railway (Cairns, Queensland)", "c": "Australien"},
    {"n": "Reunionbahn (seilgesteuerter Bergzug)", "c": "Frankreich"},
    {"n": "Maeklong Railway (Bangkok Markt-Bahn)", "c": "Thailand"},
    {"n": "Konkan Railway (Mumbai–Goa, Viadukte)", "c": "Indien"},
    {"n": "Kalka-Shimla Railway (UNESCO)", "c": "Indien"},
    {"n": "Qinghai-Tibet Railway (Lhasa, hoechste Bahn)", "c": "China"},
    {"n": "Yunnan–Vietnam Bahn (Meter-Spur Yunnan)", "c": "China"},
    {"n": "Llanberis Lake Railway (Nordwales)", "c": "Grossbritannien"},
    {"n": "Talyllyn Railway (erste erhaltene Schmalspurbahn)", "c": "Grossbritannien"},
    {"n": "Cog Railway Mount Washington (steilste USA)", "c": "USA"},
    {"n": "Durango & Silverton Narrow Gauge", "c": "USA"},
    {"n": "Cumbres & Toltec Scenic Railroad", "c": "USA"},
    {"n": "Verde Canyon Railroad (Arizona)", "c": "USA"},
    {"n": "Inca Rail Aguas Calientes–Machu Picchu", "c": "Peru"},
    {"n": "Tren a las Nubes (Zug zu den Wolken, Argentinien)", "c": "Argentinien"},
    {"n": "Patagonia Express (El Maiten–Esquel)", "c": "Argentinien"},
    {"n": "Rovos Rail Kapstadt–Daressalam", "c": "Suedafrika"},
    {"n": "Namibia Desert Express (Windhoek–Swakopmund)", "c": "Namibia"},
    {"n": "Uganda Railway (Mombasa–Kampala, historisch)", "c": "Kenia"},
    {"n": "Ethiopian Railways (Addis Abeba–Dschibuti)", "c": "Aethiopien"},
    {"n": "Hedjaz Railway (historisch, Damaskus–Medina)", "c": "Saudi-Arabien"},
]

added_p = extend_safe(k["zug_panorama"], NEW_PANORAMA)
print(f"  [OK] zug_panorama: +{added_p} → {len(k['zug_panorama'])} Items")

NEW_VKM = [
    {"n": "CH-SBB", "c": "Schweiz"},
    {"n": "CH-BLS", "c": "Schweiz"},
    {"n": "CH-RhB", "c": "Schweiz"},
    {"n": "F-SNCF", "c": "Frankreich"},
    {"n": "F-OUIGO", "c": "Frankreich"},
    {"n": "F-TGVLYRIA", "c": "Frankreich"},
    {"n": "I-TI", "c": "Italien"},
    {"n": "I-NTV", "c": "Italien"},
    {"n": "I-TRENITALIA", "c": "Italien"},
    {"n": "E-RENFE", "c": "Spanien"},
    {"n": "E-OUIGO", "c": "Spanien"},
    {"n": "E-IRYO", "c": "Spanien"},
    {"n": "NL-NS", "c": "Niederlande"},
    {"n": "NL-ABELLIO", "c": "Niederlande"},
    {"n": "B-SNCB", "c": "Belgien"},
    {"n": "B-NMBS", "c": "Belgien"},
    {"n": "GB-GWR", "c": "Grossbritannien"},
    {"n": "GB-LNER", "c": "Grossbritannien"},
    {"n": "GB-TPE", "c": "Grossbritannien"},
    {"n": "GB-AVANTI", "c": "Grossbritannien"},
    {"n": "PL-PKP", "c": "Polen"},
    {"n": "PL-REGIO", "c": "Polen"},
    {"n": "CZ-CD", "c": "Tschechien"},
    {"n": "CZ-REGIOJET", "c": "Tschechien"},
    {"n": "CZ-LEO", "c": "Tschechien"},
    {"n": "SK-ZSSK", "c": "Slowakei"},
    {"n": "H-MAV", "c": "Ungarn"},
    {"n": "RO-CFR", "c": "Rumaenien"},
    {"n": "BG-BDZ", "c": "Bulgarien"},
    {"n": "GR-OSE", "c": "Griechenland"},
    {"n": "TR-TCDD", "c": "Tuerkei"},
    {"n": "S-SJ", "c": "Schweden"},
    {"n": "N-NSB", "c": "Norwegen"},
    {"n": "FIN-VR", "c": "Finnland"},
    {"n": "DK-DSB", "c": "Daenemark"},
    {"n": "IRL-IE", "c": "Irland"},
    {"n": "P-CP", "c": "Portugal"},
]

added_v = extend_safe(k["zug_vkm"], NEW_VKM)
print(f"  [OK] zug_vkm: +{added_v} → {len(k['zug_vkm'])} Items")

with open(os.path.join(BASE, "data", "kultur.json"), "w", encoding="utf-8") as f: json.dump(k, f, ensure_ascii=False, indent=2)

# --- 3c: zug_bahnhof_bau (timeline.json) ---
with open(os.path.join(BASE, "data", "timeline.json"), "r", encoding="utf-8") as f: t = json.load(f)

existing_bau = {i["n"] for i in t["zug_bahnhof_bau"]["items"]}
NEW_BAHNHOF_BAU = [
    {"n": "Baltimore & Ohio Station (erste US-Eisenbahn)", "year": 1830, "hint": "Baltimore, USA — Beginn des amerikanischen Schienenzeitalters"},
    {"n": "Koeln Hauptbahnhof (erster Neubau)", "year": 1859, "hint": "Koeln — nahe dem Dom, zweiter Neubau 1894"},
    {"n": "Dresden Hauptbahnhof", "year": 1898, "hint": "Dresden — Jugendstil, Glasdach"},
    {"n": "Muenchen Hauptbahnhof (erster Bau)", "year": 1839, "hint": "Muenchen — erster Terminus Bayerns"},
    {"n": "Berlin Lehrter Stadtbahnhof (historisch)", "year": 1871, "hint": "Berlin — Vorlaefer des heutigen Hauptbahnhofs"},
    {"n": "Zurich Hauptbahnhof (historischer Bau)", "year": 1871, "hint": "Zuerich — seither mehrfach erweitert"},
    {"n": "Gare d'Orsay Paris (heute Musee d'Orsay)", "year": 1900, "hint": "Paris — zur Weltausstellung gebaut, heute Museum"},
    {"n": "Budapest Nyugati (Westbahnhof, Eiffel)", "year": 1877, "hint": "Budapest — von Gustave Eiffel erbaut"},
    {"n": "Wroclaw Hauptbahnhof (historisch)", "year": 1857, "hint": "Breslau/Wroclaw — Neugotik, Niederschlesien"},
    {"n": "Amsterdam Centraal", "year": 1889, "hint": "Amsterdam — P.J.H. Cuypers, hollaendischer Neorenaissance"},
    {"n": "Gare Centrale Bruessel", "year": 1952, "hint": "Bruessel — Victor Horta, Art Deco"},
    {"n": "Gdansk Hauptbahnhof", "year": 1900, "hint": "Danzig/Gdansk — Backstein-Gotik"},
    {"n": "Warszawa Wileńska (erster Warschauer Bf)", "year": 1862, "hint": "Warschau — Verbindung zum zaristischen Russland"},
    {"n": "Lviv Hauptbahnhof", "year": 1904, "hint": "Lwiw/Lemberg — Secessionsstil, k.u.k. Erbe"},
    {"n": "Kyiw Hauptbahnhof (sowjet. Umbau)", "year": 1932, "hint": "Kiew — Stalinist. Architektur"},
    {"n": "Moskau Komsomolskaya (drei Bahnhöfe)", "year": 1849, "hint": "Moskau — drei Fernbahnhöfe auf einem Platz"},
    {"n": "Helsinki Zentralbahnhof (neues Gebaeude)", "year": 1919, "hint": "Helsinki — Eliel Saarinen, Jugendstilikone"},
    {"n": "Oslo Ostbahnhof (Histor. Gebaeude)", "year": 1854, "hint": "Oslo — erster Bahnhof Norwegens"},
    {"n": "Kopenhagen Hauptbahnhof", "year": 1911, "hint": "Kopenhagen — Heinrich Wenck, Nationalromantik"},
    {"n": "Stockholms Centralstation", "year": 1871, "hint": "Stockholm — Adolf Wilhelm Edelsvaerd, Nordisch-Romanisch"},
    {"n": "Lissabon Rossio Bahnhof", "year": 1890, "hint": "Lissabon — neo-manuelinischer Stil"},
    {"n": "Barcelona Passeig de Gracia (unterirdisch)", "year": 1863, "hint": "Barcelona — oberster Knoten des Cercanias-Netzes"},
    {"n": "Florenz Santa Maria Novella", "year": 1935, "hint": "Florenz — Modernistisches Manifest, Gruppo Toscano"},
    {"n": "Athen Larissa Bahnhof", "year": 1902, "hint": "Athen — griechischer Normalspurnetz-Kopfbahnhof"},
    {"n": "Istanbul Pendik (neuer Hauptbahnhof)", "year": 2023, "hint": "Istanbul — ersetzt Haydarpasha nach Jahrzehnten"},
    {"n": "Union Station Los Angeles", "year": 1939, "hint": "Los Angeles — Spanish Colonial Revival, letzter grosser US-Bahnhof"},
    {"n": "Union Station Toronto", "year": 1927, "hint": "Toronto — Beaux Arts, Canadian Pacific/National"},
    {"n": "Gare du Palais Quebec City", "year": 1915, "hint": "Quebec — Chateaustil, Wahrzeichen"},
    {"n": "Estacion de Francia Barcelona", "year": 1929, "hint": "Barcelona — Glasdach, Art Deco"},
    {"n": "Termini Roma (neues Gebaeude)", "year": 1950, "hint": "Rom — Nachkriegsmodernismus, laengste Fassade"},
    {"n": "Shin-Osaka (erster Shinkansen-Halt ausserh. Tokio)", "year": 1964, "hint": "Osaka — zur Olympiade 1964 eroeffnet"},
    {"n": "Kyoto Station (moderner Neubau)", "year": 1997, "hint": "Kyoto — Hiroshi Hara, futuristisch, 70m hoch"},
    {"n": "Narita International Terminal (JR-Haltestelle)", "year": 1991, "hint": "Tokio — Verbindung Innenstadt–Flughafen"},
    {"n": "Shanghai Hongqiao Station (groesste Bahnhof Welt)", "year": 2010, "hint": "Shanghai — 1300m lang, 30 Gleise"},
    {"n": "Haramain West Station Mekka", "year": 2018, "hint": "Mekka — Saudi-Arabiens HSR, 50 Mio. Pilger/Jahr"},
    {"n": "Riyadh King Abdullah Financial District Station", "year": 2021, "hint": "Riad — Zaha Hadid Architects"},
    {"n": "Expo 2020 Dubai Metro Station", "year": 2020, "hint": "Dubai — Architekturreferenz fuer Wuestenbahnhof"},
    {"n": "Kairo Ramses Bahnhof (historisch)", "year": 1892, "hint": "Kairo — erster Bahnhof Afrikas und des Nahen Ostens"},
    {"n": "Dakar Hauptbahnhof (historisch)", "year": 1914, "hint": "Dakar — Westafrika, ehemals laengste Strecke Afrikas"},
    {"n": "Buenos Aires Retiro Station", "year": 1915, "hint": "Buenos Aires — britische Eisenbahninfrastruktur"},
]

added_b = 0
for item in NEW_BAHNHOF_BAU:
    if item["n"] not in existing_bau:
        t["zug_bahnhof_bau"]["items"].append(item)
        existing_bau.add(item["n"])
        added_b += 1

with open(os.path.join(BASE, "data", "timeline.json"), "w", encoding="utf-8") as f: json.dump(t, f, ensure_ascii=False, indent=2)
print(f"  [OK] zug_bahnhof_bau: +{added_b} → {len(t['zug_bahnhof_bau']['items'])} Items")

# =============================================================
# ABSCHLUSS
# =============================================================
print("\n" + "=" * 58)
with open(os.path.join(BASE,"data","sport_hl.json"),"r",encoding="utf-8") as f: s2=json.load(f)
with open(os.path.join(BASE,"data","kultur.json"),"r",encoding="utf-8") as f: k2=json.load(f)
with open(os.path.join(BASE,"data","timeline.json"),"r",encoding="utf-8") as f: t2=json.load(f)
print(f" zug_taktfrequenz:  {len(s2['zug_taktfrequenz']['items']):3d} Items {'✅' if len(s2['zug_taktfrequenz']['items'])>=80 else '❌'}")
print(f" zug_panorama:      {len(k2['zug_panorama']):3d} Items {'✅' if len(k2['zug_panorama'])>=80 else '❌'}")
print(f" zug_vkm:           {len(k2['zug_vkm']):3d} Items {'✅' if len(k2['zug_vkm'])>=80 else '❌'}")
print(f" zug_bahnhof_bau:   {len(t2['zug_bahnhof_bau']['items']):3d} Items {'✅' if len(t2['zug_bahnhof_bau']['items'])>=80 else '❌'}")
print("=" * 58)
print("[DONE] Jetzt: python gen.py && python verify.py")
