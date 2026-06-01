#!/usr/bin/env python3
"""
Phase: 341
Date:  2026-06-01
Author: Claude / Andre
Scope: Mercedes-Benz Vollständigkeit — alle fehlenden Hauptbaureihen

Description:
  Ergänzt die noch fehlenden Mercedes-Benz Baureihen, jeweils sportlichste Variante:

  B-Klasse:
    Mercedes-Benz B 250 Sport (2012) — 211 PS / 1991 ccm / 240 km/h / 6.8s

  CLA:
    Mercedes-Benz CLA 45 AMG (2013) — 381 PS / 1991 ccm / 270 km/h / 4.6s

  CLS:
    Mercedes-Benz CLS 63 AMG (2012) — 557 PS / 5461 ccm / 300 km/h / 4.4s

  GLC (kompakter SUV):
    Mercedes-Benz GLC 63 S AMG (2017) — 510 PS / 3982 ccm / 270 km/h / 3.8s

  GLE (mittelgroßer SUV):
    Mercedes-Benz GLE 63 S AMG (2015) — 585 PS / 5461 ccm / 280 km/h / 4.2s

  GLS (großer SUV):
    Mercedes-Benz GLS 63 AMG (2020) — 630 PS / 3982 ccm / 280 km/h / 4.2s

  Danach sind alle aktuellen Mercedes-Benz Hauptbaureihen vertreten:
    A / B / C / CLA / CLS / E / G / GLC / GLE / GLS / S / SL / AMG GT + Hypercar

Dependencies: Phase 340 (Mercedes Kategorie-Ergänzung)
Zero-Bug Policy: Kein gen.py-Patch nötig
"""
import json, os, subprocess, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")

CARS = [
    # B-Klasse — B 250 Sport (2012), M270, 1991 ccm, 211 PS, 240 km/h, 6.8s
    {"key": "Mercedes-Benz B 250 Sport (Deutschland, 2012)",
     "ps": 211, "ccm": 1991, "vmax": 240, "accel": 6.8, "bj": 2012, "ev": False},
    # CLA — CLA 45 AMG (2013), M133, 1991 ccm, 381 PS, 270 km/h, 4.6s
    {"key": "Mercedes-Benz CLA 45 AMG (Deutschland, 2013)",
     "ps": 381, "ccm": 1991, "vmax": 270, "accel": 4.6, "bj": 2013, "ev": False},
    # CLS — CLS 63 AMG (2012), M157, 5461 ccm, 557 PS, 300 km/h, 4.4s
    {"key": "Mercedes-Benz CLS 63 AMG (Deutschland, 2012)",
     "ps": 557, "ccm": 5461, "vmax": 300, "accel": 4.4, "bj": 2012, "ev": False},
    # GLC — GLC 63 S AMG (2017), M177, 3982 ccm, 510 PS, 270 km/h (el.), 3.8s
    {"key": "Mercedes-Benz GLC 63 S AMG (Deutschland, 2017)",
     "ps": 510, "ccm": 3982, "vmax": 270, "accel": 3.8, "bj": 2017, "ev": False},
    # GLE — GLE 63 S AMG (2015), M157, 5461 ccm, 585 PS, 280 km/h (el.), 4.2s
    {"key": "Mercedes-Benz GLE 63 S AMG (Deutschland, 2015)",
     "ps": 585, "ccm": 5461, "vmax": 280, "accel": 4.2, "bj": 2015, "ev": False},
    # GLS — GLS 63 AMG (2020), M177, 3982 ccm, 630 PS, 280 km/h (el.), 4.2s
    {"key": "Mercedes-Benz GLS 63 AMG (Deutschland, 2020)",
     "ps": 630, "ccm": 3982, "vmax": 280, "accel": 4.2, "bj": 2020, "ev": False},
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
    print("=" * 58)
    print("PATCH 341 — Mercedes-Benz Vollständigkeit (6 Modelle)")
    print("=" * 58)

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
        print(f"  + {n}")

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
         "--phase", "341",
         "--patch", "patches/patch_341_mercedes_complete.py",
         "--summary",
         "Mercedes-Vollständigkeit: B 250 Sport, CLA 45 AMG, CLS 63 AMG, "
         "GLC 63 S, GLE 63 S, GLS 63 AMG (6 Modelle) — alle Hauptbaureihen komplett"])
