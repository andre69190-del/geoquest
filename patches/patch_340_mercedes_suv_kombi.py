#!/usr/bin/env python3
"""
Phase: 340
Date:  2026-06-01
Author: Claude / Andre
Scope: Mercedes-Benz Kategorie-Ergänzung — SUV & T-Modell

Description:
  Nach Sprint 339 fehlten zwei Fahrzeugkategorien im Mercedes-Segment:

  SUV & Geländewagen:
    Mercedes-Benz G 63 AMG  (2012) — 544 PS / 5461 ccm / 230 km/h / 5.4s
      Ikone des Geländewagen-Segments, AMG-Topmodell der G-Klasse.

  T-Modelle / Kombis:
    Mercedes-Benz E 63 AMG T-Modell (2009) — 525 PS / 6208 ccm / 250 km/h / 4.5s
      Schnellster Kombi seiner Zeit, M156-Motor.

  Damit sind alle 6 Mercedes-Benz Baukategorien repräsentiert:
    Limousinen / SUV / T-Modell / Kompakt / Coupé / Roadster

Dependencies: Phase 339 (Mercedes-Sprint)
Zero-Bug Policy: Kein gen.py-Patch nötig — alle Arrays bereits registriert
"""
import json, os, subprocess, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")

CARS = [
    # Mercedes-Benz G 63 AMG (2012) — M157, 5461 ccm, 544 PS, 230 km/h (el.), 5.4s
    {"key": "Mercedes-Benz G 63 AMG (Deutschland, 2012)",
     "ps": 544, "ccm": 5461, "vmax": 230, "accel": 5.4, "bj": 2012, "ev": False},
    # Mercedes-Benz E 63 AMG T-Modell (2009) — M156, 6208 ccm, 525 PS, 250 km/h (el.), 4.5s
    {"key": "Mercedes-Benz E 63 AMG T-Modell (Deutschland, 2009)",
     "ps": 525, "ccm": 6208, "vmax": 250, "accel": 4.5, "bj": 2009, "ev": False},
]


def dedup(items, name, val):
    if any(e["name"].lower() == name.lower() for e in items):
        return 0
    items.append({"name": name, "val": val})
    return 1


def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-400:])
    if r.stderr: print(r.stderr[-200:], file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    print("=" * 55)
    print("PATCH 340 — Mercedes SUV & T-Modell (2 Modelle)")
    print("=" * 55)

    with open(AUTOS, encoding="utf-8") as f:
        d = json.load(f)

    totals = {k: 0 for k in ("auto_ps", "auto_vmax", "auto_accel", "auto_ccm", "auto_bj")}

    for car in CARS:
        n = car["key"]
        totals["auto_ps"]    += dedup(d["auto_ps"]["items"],    n, car["ps"])
        totals["auto_vmax"]  += dedup(d["auto_vmax"]["items"],  n, car["vmax"])
        totals["auto_accel"] += dedup(d["auto_accel"]["items"], n, car["accel"])
        totals["auto_bj"]    += dedup(d["auto_bj"]["items"],    n, car["bj"])
        if not car["ev"]:
            totals["auto_ccm"] += dedup(d["auto_ccm"]["items"], n, car["ccm"])
        print(f"  {'EV ' if car['ev'] else '   '}+ {n}")

    with open(AUTOS, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)

    print()
    for k, n in totals.items():
        print(f"  {k}: +{n} (gesamt: {len(d[k]['items'])})")

    print("\n  Build …")
    if run([sys.executable, "gen.py"]) != 0:
        sys.exit(1)
    print("  Verify …")
    if run([sys.executable, "verify.py"]) != 0:
        sys.exit(1)
    run([sys.executable, "validate_content.py"])
    run([sys.executable, "post_phase.py",
         "--phase", "340",
         "--patch", "patches/patch_340_mercedes_suv_kombi.py",
         "--summary",
         "Mercedes-Kategorie-Ergänzung: G 63 AMG (SUV) + E 63 AMG T-Modell (Kombi) "
         "— alle 6 MB-Kategorien jetzt repräsentiert (gesamt 11 Mercedes)"])
