#!/usr/bin/env python3
"""
Phase: 350
Date:  2026-06-01
Author: Claude / Andre
Scope: autos_extended.json erstellen — 431 Fahrzeuge mit Zusatzdaten

Description:
  Liest die 8 Rohdaten-Dateien (enrich_A bis enrich_H, je 53-55 Fahrzeuge),
  validiert alle Einträge gegen das Schema, und schreibt
  data/autos_extended.json als Lookup-Dictionary.

  Merge-Regel: Vorhandene Keys werden NICHT überschrieben (Idempotenz).

  Schema (22 Felder pro Fahrzeug):
    gewicht, drehmoment, cw, kofferraum, laenge, tank, akku, reichweite_km,
    verbrauch_l, verbrauch_kwh, antrieb, karosserie, antriebsart, motorbauart,
    zylinder, turbo, getriebe, sitze, neupreis_eur, baujahr_ende,
    nordschleife, konzern

Dependencies: enrich_A.py … enrich_H.py, Phase 343
Zero-Bug Policy: Kein gen.py-Patch nötig (autos_extended.json wird via
  Service Worker gecacht, nicht in GeoQuest.html eingebettet)
"""

import json
import os
import subprocess
import sys

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATCHES = os.path.join(ROOT, "patches")
OUTFILE = os.path.join(ROOT, "data", "autos_extended.json")

# ─── Enum-Wertmengen ────────────────────────────────────────────────────────
ANTRIEB     = {"Front", "Heck", "Allrad"}
GETRIEBE    = {"Handschalter", "Automatik", "E-Getriebe"}
MOTORBAUART = {"Reihe", "V", "W", "Boxer", "Wankel", "E-Motor"}
ANTRIEBSART = {"Benzin", "Diesel", "EV", "Hybrid", "PHEV", "MHEV"}
KAROSSERIE  = {"Hatchback", "Limousine", "Kombi", "SUV", "Coupé",
               "Cabrio", "Roadster", "Sportwagen", "Van", "Pickup"}
KONZERN     = {"VW", "BMW", "Mercedes", "Stellantis", "Ford",
               "Renault-Nissan", "Toyota", "Hyundai-Kia", "Tata",
               "Geely", "Honda", "Mazda", "Subaru", "unabhängig"}

REQUIRED = [
    "gewicht", "drehmoment", "cw", "kofferraum", "laenge",
    "tank", "akku", "reichweite_km", "verbrauch_l", "verbrauch_kwh",
    "antrieb", "karosserie", "antriebsart", "motorbauart", "zylinder",
    "turbo", "getriebe", "sitze", "neupreis_eur", "baujahr_ende",
    "nordschleife", "konzern",
]

# ─── Validation ─────────────────────────────────────────────────────────────

def validate(name, entry):
    errors = []

    # Pflichtfelder
    for f in REQUIRED:
        if f not in entry:
            errors.append(f"Feld '{f}' fehlt")

    if errors:
        return errors   # Weitere Checks sinnlos

    # Enum-Checks (lenient: unbekannte Werte → Warnung, kein Abbruch)
    for field, allowed in [
        ("antrieb",     ANTRIEB),
        ("getriebe",    GETRIEBE),
        ("motorbauart", MOTORBAUART),
        ("antriebsart", ANTRIEBSART),
        ("karosserie",  KAROSSERIE),
        ("konzern",     KONZERN),
    ]:
        val = entry.get(field, "")
        if val not in allowed:
            errors.append(f"{field}={val!r} nicht im Enum {sorted(allowed)}")

    # Logik-Checks
    art = entry.get("antriebsart", "")
    if art == "EV":
        if entry.get("tank", -1) != 0:
            errors.append("EV: tank muss 0 sein")
        if entry.get("verbrauch_l", -1) != 0.0:
            errors.append("EV: verbrauch_l muss 0.0 sein")
        if entry.get("zylinder", -1) != 0:
            errors.append("EV: zylinder muss 0 sein")
    if art not in ("EV", "Hybrid", "PHEV", "MHEV"):
        if entry.get("akku", -1) != 0.0:
            errors.append(f"{art}: akku muss 0.0 sein (ist {entry.get('akku')})")

    return errors

# ─── Laden aller Roh-Daten ───────────────────────────────────────────────────

def load_raw():
    sys.path.insert(0, PATCHES)
    merged = {}
    for suffix in "ABCDEFGH":
        mod_name = f"enrich_{suffix}"
        mod = __import__(mod_name)
        for k, v in mod.DATA.items():
            if k not in merged:
                merged[k] = v
            else:
                print(f"  [SKIP-DUP] {k}")
    return merged

# ─── Hauptprogramm ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 62)
    print("PATCH 350 — autos_extended.json Merge & Validate")
    print("=" * 62)

    # 1. Rohdaten laden
    raw = load_raw()
    print(f"\n  Rohdaten geladen: {len(raw)} Einträge aus 8 Batches")

    # 2. Vorhandene Datei laden (Merge-Regel: kein Überschreiben)
    existing = {}
    if os.path.exists(OUTFILE):
        with open(OUTFILE, encoding="utf-8") as f:
            existing = json.load(f)
        print(f"  Bereits vorhanden: {len(existing)} Einträge (werden nicht überschrieben)")

    # 3. Validierung + Merge
    total_new   = 0
    total_skip  = 0
    total_warn  = 0
    warn_list   = []

    merged = dict(existing)   # Kopie

    for name, entry in raw.items():
        errs = validate(name, entry)
        if errs:
            total_warn += 1
            for e in errs:
                warn_list.append(f"  ⚠  {name}: {e}")
        if name in existing:
            total_skip += 1
        else:
            merged[name] = entry
            total_new += 1

    # 4. Schreiben
    with open(OUTFILE, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"\n  Neu hinzugefügt: {total_new}")
    print(f"  Übersprungen   : {total_skip}  (bereits vorhanden)")
    print(f"  Validierungswarnungen: {total_warn}")
    if warn_list:
        for w in warn_list[:30]:
            print(w)
        if len(warn_list) > 30:
            print(f"  ... (+{len(warn_list)-30} weitere)")
    print(f"\n  → {OUTFILE}")
    print(f"     Gesamt: {len(merged)} Einträge")

    # 5. Build (sw.js muss autos_extended.json cachen)
    print("\n" + "=" * 62)
    print("Build …")
    print("=" * 62)
    r = subprocess.run([sys.executable, "gen.py"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.stdout: print(r.stdout[-400:])
    if r.returncode != 0:
        print("✗ Build fehlgeschlagen"); sys.exit(1)

    # 6. Verify
    print("Verify …")
    r = subprocess.run([sys.executable, "verify.py"], cwd=ROOT,
                       capture_output=True, text=True)
    print(r.stdout[-500:] if r.stdout else "")
    if r.returncode != 0:
        print("✗ verify.py fehlgeschlagen"); sys.exit(1)

    # 7. validate_content.py
    subprocess.run([sys.executable, "validate_content.py"], cwd=ROOT,
                   capture_output=True, text=True)

    # 8. Post-Phase
    subprocess.run([
        sys.executable, "post_phase.py",
        "--phase", "350",
        "--patch", "patches/patch_350_enrich_merge.py",
        "--summary",
        f"autos_extended.json: {len(merged)} Fahrzeuge mit 22 technischen Zusatzfeldern "
        f"(gewicht, drehmoment, cw, karosserie, antriebsart, konzern, …)"
    ], cwd=ROOT, capture_output=True, text=True)
    print("\n✅ Phase 350 — autos_extended.json bereit")
    print("💡 Nächster Schritt: unlock_and_push.bat")
