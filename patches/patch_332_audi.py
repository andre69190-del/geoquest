#!/usr/bin/env python3
"""
Phase: 332
Date:  2026-06-01
Author: Claude / Andre
Scope: Audi-Sprint — 7 Modelle in autos.json (kein gen.py-Patch nötig)

Modelle (EG-Typgenehmigung / offizielle Werksdaten):
  Audi Quattro Urquattro (1980)  — 200 PS / 2144 ccm / 220 km/h / 7.1s
  Audi Sport Quattro     (1984)  — 306 PS / 2133 ccm / 250 km/h / 5.0s
  Audi RS2 Avant         (1994)  — 315 PS / 2226 ccm / 262 km/h / 5.4s
  Audi TT 8N             (1998)  — 180 PS / 1781 ccm / 235 km/h / 7.4s
  Audi R8 V10            (2009)  — 525 PS / 5204 ccm / 316 km/h / 3.9s
  Audi RS6 C8 Avant      (2019)  — 600 PS / 3996 ccm / 305 km/h / 3.6s
  Audi e-tron GT         (2021)  — 476 PS / EV       / 245 km/h / 4.1s
"""
import json, os, subprocess, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")

AUDI = [
    {"key": "Audi Quattro Urquattro (Deutschland, 1980)",
     "ps": 200, "ccm": 2144, "vmax": 220, "accel": 7.1, "bj": 1980, "ev": False},
    {"key": "Audi Sport Quattro (Deutschland, 1984)",
     "ps": 306, "ccm": 2133, "vmax": 250, "accel": 5.0, "bj": 1984, "ev": False},
    {"key": "Audi RS2 Avant (Deutschland, 1994)",
     "ps": 315, "ccm": 2226, "vmax": 262, "accel": 5.4, "bj": 1994, "ev": False},
    {"key": "Audi TT 8N (Deutschland, 1998)",
     "ps": 180, "ccm": 1781, "vmax": 235, "accel": 7.4, "bj": 1998, "ev": False},
    {"key": "Audi R8 V10 (Deutschland, 2009)",
     "ps": 525, "ccm": 5204, "vmax": 316, "accel": 3.9, "bj": 2009, "ev": False},
    {"key": "Audi RS6 C8 Avant (Deutschland, 2019)",
     "ps": 600, "ccm": 3996, "vmax": 305, "accel": 3.6, "bj": 2019, "ev": False},
    {"key": "Audi e-tron GT (Deutschland, 2021)",
     "ps": 476, "ccm":    0, "vmax": 245, "accel": 4.1, "bj": 2021, "ev": True},
]

def dedup(items, name, val, key="name"):
    if any(e[key].lower() == name.lower() for e in items):
        return 0
    items.append({key: name, "val": val})
    return 1

def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-400:])
    if r.stderr: print(r.stderr[-200:], file=sys.stderr)
    return r.returncode

if __name__ == "__main__":
    print("=" * 55)
    print("PATCH 332 — Audi-Sprint (7 Modelle)")
    print("=" * 55)

    with open(AUTOS, encoding="utf-8") as f:
        d = json.load(f)

    totals = {k: 0 for k in ("auto_ps","auto_vmax","auto_accel","auto_ccm","auto_bj")}

    for car in AUDI:
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

    print("\n Build …")
    if run([sys.executable, "gen.py"]) != 0: sys.exit(1)
    print(" Verify …")
    if run([sys.executable, "verify.py"]) != 0: sys.exit(1)
    run([sys.executable, "validate_content.py"])
    run([sys.executable, "post_phase.py",
         "--phase", "332", "--patch", "patches/patch_332_audi.py",
         "--summary", "Audi-Sprint: Quattro, Sport Quattro, RS2, TT, R8 V10, RS6 C8, e-tron GT (7 Modelle)"])
