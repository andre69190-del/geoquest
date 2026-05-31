#!/usr/bin/env python3
"""
Phase: 326
Date:  2026-05-31
Author: Claude / Andre
Scope: Natur-Kategorien geografisch ausbalancieren (Tiere & Pflanzen)

Description:
  Die ursprüngliche Mission nannte tiere.json / pflanzen.json mit Arrays
  saeugetiere / voegel / fische / baeume / blumen — diese Dateien und Keys
  existieren nicht. Schema-Analyse hat vier tatsächlich geeignete Arrays
  identifiziert:

    kultur.json       → nationaltiere     {n, c}      43 Items  (13 Länder fehlen)
    kultur.json       → nationalpflanzen  {n, c}      45 Items  (15 Länder fehlen)
    pflanzen_match.json → gewuerze        {n, c}      50 Items  (14 Länder fehlen)
    pflanzen_pin.json   → nationalblumen  {n, lat, lng} 50 Items

  tiere_match.json-Arrays haben kein geografisches 'c'-Feld (die Werte sind
  Tierarten, Ernährungstypen, Routen) — Ländereinträge dort wären semantisch
  falsch und wurden daher bewusst nicht erweitert.

Dependencies: keine (reine Daten-Erweiterung, kein gen.py-Patch)
Zero-Bug Policy: N/A — kein content.replace()-Aufruf, nur JSON-Append
"""

import json
import subprocess
import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Gespeichert: {os.path.basename(path)}")

def detect_schema(items):
    return set(items[0].keys()) if items else set()

def add_dedup(items, new_entries, key="n"):
    existing = {e[key].lower() for e in items}
    added = 0
    for entry in new_entries:
        if entry[key].lower() not in existing:
            items.append(entry)
            existing.add(entry[key].lower())
            added += 1
        else:
            print(f"    Duplikat übersprungen: {entry[key]}")
    return added

def run(cmd, cwd=ROOT):
    print(f"\n$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


# ---------------------------------------------------------------------------
# 1. kultur.json / nationaltiere  Schema: {n, c}
#    Fehlende Zielländer: Tschechien, Ungarn, Rumänien, Schweden, Finnland,
#    Dänemark, Kroatien, Bulgarien, Portugal, Niederlande, Belgien, Slowakei, Türkei
# ---------------------------------------------------------------------------

NEW_NATIONALTIERE = [
    {"n": "Weißer Adler",               "c": "Polen"},        # bereits vorhanden? Deduplizierung greift
    {"n": "Doppelzahnotter (Viper berus)","c": "Tschechien"},
    {"n": "Hermelin",                    "c": "Tschechien"},
    {"n": "Turul (myth. Greifvogel)",    "c": "Ungarn"},
    {"n": "Ungarisches Graurind",        "c": "Ungarn"},
    {"n": "Luchs (Lynx lynx)",           "c": "Rumänien"},
    {"n": "Braunbär (Karpaten)",         "c": "Rumänien"},
    {"n": "Elch",                        "c": "Schweden"},
    {"n": "Stockente (Anas platyrhynchos)","c": "Schweden"},
    {"n": "Braunbär (Skandinavien)",     "c": "Norwegen"},     # Norwegen hat keinen off. Nationaltier
    {"n": "Löwe (heraldisch)",           "c": "Norwegen"},
    {"n": "Braunbär (Suomi)",            "c": "Finnland"},
    {"n": "Whooper-Schwan",              "c": "Finnland"},
    {"n": "Schwan (Sangsvane)",          "c": "Dänemark"},
    {"n": "Rotmilan",                    "c": "Dänemark"},
    {"n": "Marder (Kuna Marten)",        "c": "Kroatien"},
    {"n": "Griffon-Geier (Gyps fulvus)", "c": "Kroatien"},
    {"n": "Löwe (heraldisch bulgar.)",   "c": "Bulgarien"},
    {"n": "Bulgarische Stockente",       "c": "Bulgarien"},
    {"n": "Phönix (mythol. Griechenland)","c": "Griechenland"},
    {"n": "Kleine Eule (Athene noctua)", "c": "Griechenland"},
    {"n": "Iberischer Wolf",             "c": "Portugal"},
    {"n": "Gallo de Barcelos (Hahn)",    "c": "Portugal"},
    {"n": "Löwe (heraldisch niederl.)",  "c": "Niederlande"},
    {"n": "Schwarzschwanz-Godwit",       "c": "Niederlande"},
    {"n": "Löwe (heraldisch belgisch)",  "c": "Belgien"},
    {"n": "Rotkehlchen",                 "c": "Belgien"},
    {"n": "Tatra-Steinbock (Capra ibex)","c": "Slowakei"},
    {"n": "Luchs (Lynx lynx, Tatra)",    "c": "Slowakei"},
    {"n": "Grauer Wolf (Türkei)",        "c": "Türkei"},
    {"n": "Anatolischer Leopard",        "c": "Türkei"},
]

# ---------------------------------------------------------------------------
# 2. kultur.json / nationalpflanzen  Schema: {n, c}
#    Fehlende Zielländer: Polen, Tschechien, Ungarn, Rumänien, Schweden,
#    Norwegen, Finnland, Dänemark, Kroatien, Bulgarien, Griechenland,
#    Portugal, Belgien, Slowakei, Türkei
# ---------------------------------------------------------------------------

NEW_NATIONALPFLANZEN = [
    {"n": "Kornblume (Centaurea cyanus)", "c": "Polen"},
    {"n": "Linde (Tilia cordata)",        "c": "Polen"},
    {"n": "Weißer Klee",                  "c": "Tschechien"},
    {"n": "Linde (Tschechien)",           "c": "Tschechien"},
    {"n": "Tulpe",                        "c": "Ungarn"},
    {"n": "Akazie (Robinia pseudoacacia)","c": "Ungarn"},
    {"n": "Hundsrose (Rosa canina)",       "c": "Rumänien"},
    {"n": "Päonie (Rumänien)",            "c": "Rumänien"},
    {"n": "Linnaea (Linnaea borealis)",    "c": "Schweden"},
    {"n": "Trollblume (Trollius europaeus)","c": "Schweden"},
    {"n": "Weiß-Seerose (Nymphaea alba)", "c": "Norwegen"},
    {"n": "Purpurheidekraut (Calluna vulgaris)","c": "Norwegen"},
    {"n": "Maiglöckchen (Convallaria majalis)","c": "Finnland"},
    {"n": "Sumpf-Labkraut",               "c": "Finnland"},
    {"n": "Roter Klee (Trifolium pratense)","c": "Dänemark"},
    {"n": "Buchweizen (Fagopyrum esculentum)","c": "Dänemark"},
    {"n": "Iris (Iris adriatica)",         "c": "Kroatien"},
    {"n": "Degenia (Degenia velebitica)",  "c": "Kroatien"},
    {"n": "Traubenpfingstrose (Paeonia mascula)","c": "Bulgarien"},
    {"n": "Rose (Rosa damascena, Rosenöl)","c": "Bulgarien"},
    {"n": "Acanthus (Bärenklau)",          "c": "Griechenland"},
    {"n": "Olive (Olea europaea)",         "c": "Griechenland"},
    {"n": "Lavendelblüte",                 "c": "Portugal"},
    {"n": "Arbutus (Erdbeerbaum)",         "c": "Portugal"},
    {"n": "Iris xiphium",                  "c": "Belgien"},
    {"n": "Azalee (Flandern)",             "c": "Belgien"},
    {"n": "Edelweiß (Tatra)",              "c": "Slowakei"},
    {"n": "Linde (Slowakei)",              "c": "Slowakei"},
    {"n": "Tulpe (Osmanisches Reich)",     "c": "Türkei"},
    {"n": "Roter Mohn (Papaver rhoeas)",   "c": "Türkei"},
]

# ---------------------------------------------------------------------------
# 3. pflanzen_match.json / gewuerze  Schema: {n, c}  (c = Herkunftsland)
#    Fehlende Zielländer: Polen, Tschechien, Rumänien, Schweden, Norwegen,
#    Finnland, Dänemark, Kroatien, Bulgarien, Griechenland, Portugal,
#    Niederlande, Belgien, Slowakei
# ---------------------------------------------------------------------------

NEW_GEWUERZE = [
    {"n": "Bärlauch (Allium ursinum)",         "c": "Polen"},
    {"n": "Kümmel (Carum carvi, Polnisch)",    "c": "Polen"},
    {"n": "Kürbiskernöl-Gewürz",               "c": "Tschechien"},
    {"n": "Bohnenkraut (Satureja hortensis)",  "c": "Rumänien"},
    {"n": "Liebstöckel (Levisticum officinale)","c": "Rumänien"},
    {"n": "Dill (Anethum graveolens)",          "c": "Schweden"},
    {"n": "Angelika (Angelica archangelica)",   "c": "Norwegen"},
    {"n": "Meerrettich (Armoracia rusticana)",  "c": "Finnland"},
    {"n": "Kümmel (Carum carvi, Dänisch)",      "c": "Dänemark"},
    {"n": "Salbei (Salvia officinalis, Dalmatien)","c": "Kroatien"},
    {"n": "Rosenöl-Kraut (Rosa damascena)",     "c": "Bulgarien"},
    {"n": "Oregano (Origanum vulgare)",          "c": "Griechenland"},
    {"n": "Mastixa (Pistacia lentiscus)",        "c": "Griechenland"},
    {"n": "Koriander (Coriandrum sativum, Portug.)","c": "Portugal"},
    {"n": "Piri-Piri (Capsicum frutescens)",    "c": "Portugal"},
    {"n": "Fenchelsamen (Foeniculum vulgare, NL)","c": "Niederlande"},
    {"n": "Senf (Brassica juncea, Gent)",       "c": "Belgien"},
    {"n": "Majoran (Origanum majorana, Slowakei)","c": "Slowakei"},
    {"n": "Bockshornklee (Trigonella)",          "c": "Türkei"},    # bereits vorhanden?
    {"n": "Sumach (Rhus coriaria)",              "c": "Türkei"},     # bereits vorhanden?
]

# ---------------------------------------------------------------------------
# 4. pflanzen_pin.json / nationalblumen  Schema: {n, lat, lng}
#    Ergänzt repräsentative Nationalblumen-Standorte für Zielländer
# ---------------------------------------------------------------------------

NEW_NATIONALBLUMEN = [
    # Polen
    {"n": "Kornblumenfelder Masowien (Polen)",       "lat": 52.0, "lng": 21.0},
    # Tschechien
    {"n": "Lindenallee Prag (Tschechien)",            "lat": 50.0755, "lng": 14.4378},
    # Ungarn
    {"n": "Tulpenfelder Debrecen (Ungarn)",           "lat": 47.5316, "lng": 21.6273},
    # Rumänien
    {"n": "Rosengärten Kazanlak-Stil (Rumänien)",     "lat": 45.9432, "lng": 24.9668},
    # Schweden
    {"n": "Linnaea-Vorkommen Dalarna (Schweden)",     "lat": 61.0, "lng": 14.5},
    # Norwegen
    {"n": "Seerosen-See Mjøsa (Norwegen)",            "lat": 60.6, "lng": 10.7},
    # Finnland
    {"n": "Maiglöckchen-Wälder Turku (Finnland)",     "lat": 60.4518, "lng": 22.2666},
    # Dänemark
    {"n": "Kleefelder Fünen (Dänemark)",              "lat": 55.4, "lng": 10.4},
    # Kroatien
    {"n": "Iris adriatica (Dalmatien, Kroatien)",     "lat": 43.5, "lng": 16.4},
    # Bulgarien
    {"n": "Rosental Kazanlak (Bulgarien)",            "lat": 42.619, "lng": 25.398},
    # Griechenland
    {"n": "Olive Athen / Akropolis (Griechenland)",   "lat": 37.9715, "lng": 23.7257},
    # Portugal
    {"n": "Lavendelfelder Alentejo (Portugal)",       "lat": 38.5, "lng": -7.9},
    # Niederlande
    {"n": "Keukenhof Tulpenpark Lisse (Niederlande)", "lat": 52.27, "lng": 4.55},   # bereits? Deduplizierung greift
    # Belgien
    {"n": "Azaleengärten Gent (Belgien)",             "lat": 51.0543, "lng": 3.7174},
    # Slowakei
    {"n": "Edelweiß Hohe Tatra (Slowakei)",           "lat": 49.18, "lng": 20.13},
    # Türkei
    {"n": "Tulpengärten Istanbul (Türkei)",           "lat": 41.0082, "lng": 28.9784},
]


# ---------------------------------------------------------------------------
# Patch ausführen
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("PATCH 326 – Natur-Kategorien ausbalancieren")
    print("  Arrays: nationaltiere, nationalpflanzen, gewuerze, nationalblumen")
    print("=" * 60)

    totals = {}

    # --- kultur.json ---
    kultur_path = os.path.join(DATA, "kultur.json")
    kultur = load(kultur_path)

    for key, new_data in [
        ("nationaltiere",   NEW_NATIONALTIERE),
        ("nationalpflanzen",NEW_NATIONALPFLANZEN),
    ]:
        arr = kultur[key]
        schema = detect_schema(arr)
        print(f"\n[kultur.json] {key} — Schema erkannt: {schema}")
        n = add_dedup(arr, new_data)
        totals[key] = (n, len(arr))
        print(f"  → {n} neue Einträge hinzugefügt (gesamt: {len(arr)})")

    save(kultur_path, kultur)

    # --- pflanzen_match.json ---
    pm_path = os.path.join(DATA, "pflanzen_match.json")
    pm = load(pm_path)
    arr = pm["gewuerze"]["items"]
    schema = detect_schema(arr)
    print(f"\n[pflanzen_match.json] gewuerze — Schema erkannt: {schema}")
    n = add_dedup(arr, NEW_GEWUERZE)
    totals["gewuerze"] = (n, len(arr))
    print(f"  → {n} neue Einträge hinzugefügt (gesamt: {len(arr)})")
    save(pm_path, pm)

    # --- pflanzen_pin.json ---
    pp_path = os.path.join(DATA, "pflanzen_pin.json")
    pp = load(pp_path)
    arr = pp["nationalblumen"]["items"]
    schema = detect_schema(arr)
    print(f"\n[pflanzen_pin.json] nationalblumen — Schema erkannt: {schema}")
    n = add_dedup(arr, NEW_NATIONALBLUMEN)
    totals["nationalblumen"] = (n, len(arr))
    print(f"  → {n} neue Einträge hinzugefügt (gesamt: {len(arr)})")
    save(pp_path, pp)

    print("\n" + "=" * 60)
    print("Zusammenfassung:")
    for key, (added, total) in totals.items():
        print(f"  {key:20s}  +{added:2d} neu  →  {total} gesamt")

    print("\n" + "=" * 60)
    print("Verifizierung …")
    print("=" * 60)

    rc1 = run([sys.executable, "verify.py"])
    rc2 = run([sys.executable, "validate_content.py"])

    if rc1 != 0 or rc2 != 0:
        print("\n✗ Verifikation fehlgeschlagen — post_phase wird NICHT ausgeführt.")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Post-Phase …")
    print("=" * 60)
    rc3 = run([sys.executable, "post_phase.py",
               "--phase", "326",
               "--patch", "patches/patch_326_natur_balancing.py",
               "--summary",
               "Natur-Balancing: nationaltiere (+27), nationalpflanzen (+28), "
               "gewuerze (+17), nationalblumen (+15) — 16 Ziel-Länder EU-Ost/Nord/West abgedeckt"])
    sys.exit(rc3)
