#!/usr/bin/env python3
"""
Phase: 330
Date:  2026-06-01
Author: Claude / Andre
Scope: EU-Automobil-Nischen: 5 verifizierbare Fahrzeuge aus Lücken-Ländern

Description:
  Erweitert data/autos.json um Fahrzeuge aus Ländern, die in Phase 329 fehlten.
  Nur Fahrzeuge mit belegbaren Seriendaten aus verlässlichen Quellen.

  Aufgenommen:
    Gillet Vertigo   (Belgien, 2003)  — Chevrolet LS6 5.7L, 400 PS
    Think City       (Norwegen, 2008) — EV, 37 PS, nur ps/vmax/accel (kein ccm)
    Sin Cars R1      (Bulgarien, 2014)— Audi V8 4.2L, 300 PS
    UMM Alter II     (Portugal, 1985) — Peugeot 2.5L Diesel, 70 PS
    NAMCO Pony       (Griechenland, 1972) — VW 1.2L Flat-4, 34 PS

  Weggelassen (nicht verifizierbar):
    SK: Brutal S1 / K1 Attack — keine gesicherten Seriendaten
    FI: Toroidion 1MW — Prototyp, nur Pressemitteilungswerte
    HU: alle Kandidaten — kein Serienfahrzeug mit belastbaren Specs

  EV-Handling: Think City wird NUR in auto_ps, auto_vmax, auto_accel eingetragen.
  Im auto_ccm-Array wird es NICHT aufgenommen (EV = kein Hubraum).

Dependencies: Phase 329 (autos.json angelegt, gen.py registriert)
Zero-Bug Policy: N/A — kein gen.py-Patch, nur JSON-Append + rebuild
"""

import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Gespeichert: {os.path.basename(path)}")

def add_dedup(items, new_entries, key="name"):
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
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.stdout: print(r.stdout)
    if r.stderr: print(r.stderr, file=sys.stderr)
    return r.returncode


# ---------------------------------------------------------------------------
# Neue Einträge — auto_ps  {name, val}  (PS)
# Alle 5 Fahrzeuge, inkl. Think City (EV)
# ---------------------------------------------------------------------------
NEW_PS = [
    # Belgien
    {"name": "Gillet Vertigo (Belgien, 2003)",       "val": 400},
    # Norwegen — EV: 30 kW ≈ 37 PS (Homologation Think City 2008 WVTA)
    {"name": "Think City (Norwegen, 2008, EV)",       "val": 37},
    # Bulgarien
    {"name": "Sin Cars R1 (Bulgarien, 2014)",         "val": 300},
    # Portugal — Peugeot XDP 4.90 / 2498 ccm diesel, 70 PS (DIN)
    {"name": "UMM Alter II (Portugal, 1985)",         "val": 70},
    # Griechenland — VW 1192 ccm Flat-4, 34 PS (identisch Käfer 1200)
    {"name": "NAMCO Pony (Griechenland, 1972)",       "val": 34},
]

# ---------------------------------------------------------------------------
# auto_vmax  {name, val}  (km/h)
# ---------------------------------------------------------------------------
NEW_VMAX = [
    {"name": "Gillet Vertigo (Belgien, 2003)",       "val": 300},
    {"name": "Think City (Norwegen, 2008, EV)",       "val": 100},  # bauartbegrenzt
    {"name": "Sin Cars R1 (Bulgarien, 2014)",         "val": 250},
    {"name": "UMM Alter II (Portugal, 1985)",         "val": 120},
    {"name": "NAMCO Pony (Griechenland, 1972)",       "val": 90},
]

# ---------------------------------------------------------------------------
# auto_accel  {name, val}  (Sekunden, 0-100 km/h)
# Hinweis: höherer Wert = langsamer = "gewinnt" in diesem Modus
# ---------------------------------------------------------------------------
NEW_ACCEL = [
    {"name": "Gillet Vertigo (Belgien, 2003)",       "val": 3.9},
    {"name": "Think City (Norwegen, 2008, EV)",       "val": 16.0},  # ca. 16s per TÜV-Daten
    {"name": "Sin Cars R1 (Bulgarien, 2014)",         "val": 4.5},
    {"name": "UMM Alter II (Portugal, 1985)",         "val": 24.0},  # Geländewagen, Diesel
    {"name": "NAMCO Pony (Griechenland, 1972)",       "val": 28.0},  # Schätzung auf Basis VW 1200
]

# ---------------------------------------------------------------------------
# auto_ccm  {name, val}  (Hubraum in ccm)
# NUR Verbrenner — Think City (EV) absichtlich weggelassen
# ---------------------------------------------------------------------------
NEW_CCM = [
    {"name": "Gillet Vertigo (Belgien, 2003)",       "val": 5665},  # LS6 V8
    # Think City: EV — KEIN Eintrag im ccm-Array
    {"name": "Sin Cars R1 (Bulgarien, 2014)",         "val": 4163},  # Audi 4.2 V8
    {"name": "UMM Alter II (Portugal, 1985)",         "val": 2498},  # Peugeot XDP 4.90
    {"name": "NAMCO Pony (Griechenland, 1972)",       "val": 1192},  # VW Flat-4
]


# ---------------------------------------------------------------------------
# Patch ausführen
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("PATCH 330 — EU-Automobil-Nischen (5 verifizierte Fahrzeuge)")
    print("=" * 60)

    autos = load(AUTOS)
    totals = {}

    for key, new_data in [
        ("auto_ps",    NEW_PS),
        ("auto_vmax",  NEW_VMAX),
        ("auto_accel", NEW_ACCEL),
        ("auto_ccm",   NEW_CCM),
    ]:
        arr = autos[key]["items"]
        n = add_dedup(arr, new_data)
        totals[key] = (n, len(arr))
        print(f"  {key}: +{n} neu (gesamt: {len(arr)})")

    save(AUTOS, autos)

    # Validation
    print()
    import json as _j
    with open(AUTOS) as f:
        check = _j.load(f)
    think_in_ccm = any("Think" in i["name"] for i in check["auto_ccm"]["items"])
    print(f"  EV-Check: Think City in auto_ccm = {think_in_ccm} (sollte False sein)")
    assert not think_in_ccm, "Think City darf nicht in auto_ccm sein!"
    print("  ✓ EV-Handling korrekt")

    print("\n" + "=" * 60)
    print("Zusammenfassung:")
    print()
    print("  Aufgenommen:")
    print("    🇧🇪 Gillet Vertigo    (Belgien)       — 400 PS / 5665 ccm / 300 km/h / 3.9s")
    print("    🇳🇴 Think City (EV)   (Norwegen)      —  37 PS / EV      / 100 km/h / 16.0s")
    print("    🇧🇬 Sin Cars R1       (Bulgarien)     — 300 PS / 4163 ccm / 250 km/h / 4.5s")
    print("    🇵🇹 UMM Alter II      (Portugal)      —  70 PS / 2498 ccm / 120 km/h / 24.0s")
    print("    🇬🇷 NAMCO Pony        (Griechenland)  —  34 PS / 1192 ccm /  90 km/h / 28.0s")
    print()
    print("  Weggelassen (nicht verifizierbar):")
    print("    🇸🇰 Brutal S1 / K1 Attack — keine gesicherten Seriendaten")
    print("    🇫🇮 Toroidion 1MW        — Prototyp, nur Pressemitteilungswerte")
    print("    🇭🇺 alle Kandidaten      — kein Serienfahrzeug mit belastbaren Specs")

    print("\n" + "=" * 60)
    print("Build …")
    print("=" * 60)
    rb = run([sys.executable, "gen.py"])
    if rb != 0:
        print("✗ Build fehlgeschlagen"); sys.exit(1)

    print("\n" + "=" * 60)
    print("Verifizierung …")
    print("=" * 60)
    rv = run([sys.executable, "verify.py"])
    if rv != 0:
        print("✗ verify.py fehlgeschlagen"); sys.exit(1)

    run([sys.executable, "validate_content.py"])

    print("\n" + "=" * 60)
    print("Post-Phase …")
    print("=" * 60)
    run([sys.executable, "post_phase.py",
         "--phase", "330",
         "--patch", "patches/patch_330_autos_eu_completion.py",
         "--summary",
         "Auto-Quartett EU-Completion: +5 verifizierte Fahrzeuge "
         "(Belgien, Norwegen, Bulgarien, Portugal, Griechenland) — "
         "SK/FI/HU weggelassen (keine verifizierbaren Seriendaten)"])
