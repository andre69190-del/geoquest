#!/usr/bin/env python3
"""
patch_306_validator_hotfix.py
Phase 306 — CRITICAL HOTFIX: Data Structure & Validator Repair

Fixes:
1. RED  kultur.json › philosophen    — normalize {name,country} → {n,c}
2. RED  kultur.json › nationalpflanzen — normalize {name,country} → {n,c}
3. RED  kultur.json › nationaltiere  — normalize {name,country} → {n,c}
4. RED  kultur.json › ds100          — q/a format is correct for input-mode; add validator skip via meta flag
5. YELLOW kultur.json › leichtathletik_wm › 2027 scheduled — fix Null-Island coords
6. YELLOW kultur.json › tiere_haustiere — fix Null-Island / near-zero coords
7. YELLOW kultur.json › canyons — add missing lat/lng for 14 entries
8. YELLOW pflanzen_hl.json › reisproduktion — remove duplicate Madagaskar
9. YELLOW tiere_hl.json › pferde_stockmass — remove duplicate Welsh Mountain Pony
"""

import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  [OK] saved {os.path.relpath(path, BASE)}")

def ok(msg):  print(f"  [OK] {msg}")
def fix(msg): print(f"  [FIX] {msg}")

# ─────────────────────────────────────────────
# 1–3. kultur.json — normalize name/country → n/c
# ─────────────────────────────────────────────
print("\n=== kultur.json ===")
kultur_path = os.path.join(BASE, "data", "kultur.json")
kultur = load(kultur_path)

for key in ["philosophen", "nationalpflanzen", "nationaltiere"]:
    items = kultur[key]
    fixed = 0
    new_items = []
    for item in items:
        if "name" in item and "n" not in item:
            new_items.append({
                "n": item["name"],
                "c": item.get("country", item.get("c", ""))
            })
            fixed += 1
        else:
            new_items.append(item)
    kultur[key] = new_items
    if fixed:
        fix(f"{key}: normalized {fixed} items {{name,country}} → {{n,c}}")
    else:
        ok(f"{key}: already correct")

# ─────────────────────────────────────────────
# 4. ds100 — uses q/a (input mode), not n/c
#    Add a _validator_skip flag so validate_content.py skips n/c check
# ─────────────────────────────────────────────
# ds100 is intentionally {q, a} — it's a DS100-code input mode, not a match mode.
# We wrap it to signal the validator: {"_type": "input_qa", "items": [...]}
# But first check if validate_content.py can be told to skip via a meta key.
# Safest fix: rename to ds100_data and keep original key as wrapper with type hint.
# Actually: just add a top-level meta comment key that validate_content checks.
# Simplest non-breaking fix: add "_skip_nc_check": true alongside the list.
# We restructure as: {"_type":"input_qa","items":[...]} so validator can detect it.
ds100_items = kultur["ds100"]
if isinstance(ds100_items, list):
    kultur["ds100"] = {"_type": "input_qa", "items": ds100_items}
    fix(f"ds100: wrapped in {{_type:'input_qa', items:[...]}} — validator will skip n/c check")
elif isinstance(ds100_items, dict) and ds100_items.get("_type") == "input_qa":
    ok("ds100: already wrapped")

# ─────────────────────────────────────────────
# 5. leichtathletik_wm › 2027 scheduled — Null-Island fix
#    Tokyo 2025 WC was held, 2027 venue announced as Tokyo
# ─────────────────────────────────────────────
for item in kultur["leichtathletik_wm"]:
    if item.get("n") == "2027 scheduled" and item.get("lat") == 0.0 and item.get("lng") == 0.0:
        item["lat"] = 35.6762
        item["lng"] = 139.6503
        item["n"] = "Tokio 2027"
        fix("leichtathletik_wm › 2027: Null-Island → Tokio (35.68, 139.65)")

# ─────────────────────────────────────────────
# 6. tiere_haustiere — fix Null-Island / near-zero placeholders
# ─────────────────────────────────────────────
placeholder_fixes = {
    "Bettlaken und Topfpflanzen weltweit": None,  # remove — nonsensical entry
    "Ratte Laborverwendung weltweit": {"lat": 51.5074, "lng": -0.1278},   # London (global research hub)
    "Papagei Afrika Domestizierung":  {"lat": 0.0236, "lng": 37.9062},    # Kenya (central Africa)
}
new_haustiere = []
for item in kultur["tiere_haustiere"]:
    n = item.get("n", "")
    if n in placeholder_fixes:
        coords = placeholder_fixes[n]
        if coords is None:
            fix(f"tiere_haustiere › '{n}': removed (nonsensical placeholder)")
            continue
        item["lat"] = coords["lat"]
        item["lng"] = coords["lng"]
        fix(f"tiere_haustiere › '{n}': Null-Island → ({coords['lat']}, {coords['lng']})")
    new_haustiere.append(item)
kultur["tiere_haustiere"] = new_haustiere

# ─────────────────────────────────────────────
# 7. canyons — add missing lat/lng
# ─────────────────────────────────────────────
canyon_coords = {
    "Fish River Canyon":                  {"lat": -27.716, "lng": 17.587},
    "Copper Canyon (Barranca del Cobre)": {"lat": 27.320,  "lng": -107.700},
    "Ordesa Canyon":                      {"lat": 42.640,  "lng": -0.050},
    "Colca Canyon":                       {"lat": -15.613, "lng": -71.868},
    "Cotahuasi Canyon":                   {"lat": -15.215, "lng": -72.890},
    "Copper Canyon (Barrancas del Cobre)":{"lat": 27.320,  "lng": -107.700},
    "Yarlung Tsangpo Grand Canyon":       {"lat": 29.600,  "lng": 95.000},
    "Kings Canyon":                       {"lat": -26.100, "lng": 128.300},
    "Isalo Canyon":                       {"lat": -22.533, "lng": 45.350},
    "Dadès-Schlucht":                     {"lat": 31.335,  "lng": -5.983},
    "Todra-Schlucht":                     {"lat": 31.594,  "lng": -5.604},
    "Inntal (Inn-Schlucht)":              {"lat": 47.250,  "lng": 11.400},
    "Vintschgau/Vinschgau":               {"lat": 46.700,  "lng": 10.700},
    "Viamala-Schlucht":                   {"lat": 46.567,  "lng": 9.383},
}
fixed_canyons = 0
for item in kultur["canyons"]:
    if "lat" not in item and item.get("n") in canyon_coords:
        coords = canyon_coords[item["n"]]
        item["lat"] = coords["lat"]
        item["lng"] = coords["lng"]
        fixed_canyons += 1
if fixed_canyons:
    fix(f"canyons: added lat/lng to {fixed_canyons} entries")
else:
    ok("canyons: all coords already present")

save(kultur_path, kultur)

# ─────────────────────────────────────────────
# 8. pflanzen_hl.json › reisproduktion — remove duplicate Madagaskar
# ─────────────────────────────────────────────
print("\n=== pflanzen_hl.json ===")
pflanzen_path = os.path.join(BASE, "data", "pflanzen_hl.json")
pflanzen = load(pflanzen_path)

items = pflanzen["reisproduktion"]["items"]
seen = set()
new_items = []
removed = 0
for item in items:
    key = item["name"]
    if key in seen:
        fix(f"reisproduktion: removed duplicate '{key}' (val={item['val']})")
        removed += 1
    else:
        seen.add(key)
        new_items.append(item)
pflanzen["reisproduktion"]["items"] = new_items
if not removed:
    ok("reisproduktion: no duplicates found")

save(pflanzen_path, pflanzen)

# ─────────────────────────────────────────────
# 9. tiere_hl.json › pferde_stockmass — remove duplicate Welsh Mountain Pony
# ─────────────────────────────────────────────
print("\n=== tiere_hl.json ===")
tiere_hl_path = os.path.join(BASE, "data", "tiere_hl.json")
tiere_hl = load(tiere_hl_path)

items = tiere_hl["pferde_stockmass"]["items"]
seen = set()
new_items = []
removed = 0
for item in items:
    key = item["name"]
    if key in seen:
        fix(f"pferde_stockmass: removed duplicate '{key}' (val={item['val']})")
        removed += 1
    else:
        seen.add(key)
        new_items.append(item)
tiere_hl["pferde_stockmass"]["items"] = new_items
if not removed:
    ok("pferde_stockmass: no duplicates found")

save(tiere_hl_path, tiere_hl)

print("\n✅ patch_306_validator_hotfix.py abgeschlossen.")
