#!/usr/bin/env python3
"""
Phase: 339
Date:  2026-06-01
Author: Claude / Andre
Scope: Mercedes-Benz-Sprint — 5 neue Modelle in autos.json

Description:
  Bereits vorhanden (werden per Dedup übersprungen):
    Mercedes-Benz 300 SL (1954), 190E 2.3-16 Cosworth (1984),
    C63 AMG (2006), Mercedes-AMG ONE (2023)

  Neu hinzugefügt (offizielle Werksdaten / EG-Typgenehmigungen):
    Mercedes-Benz 450 SEL 6.9 (1975) — 286 PS / 6834 ccm / 225 km/h / 7.4s
    Mercedes-Benz 500E W124  (1992) — 326 PS / 4973 ccm / 250 km/h / 6.1s
    Mercedes-Benz SLS AMG    (2010) — 571 PS / 6208 ccm / 317 km/h / 3.8s
    Mercedes-Benz A45 AMG    (2013) — 381 PS / 1991 ccm / 270 km/h / 4.6s
    Mercedes-AMG GT Black Series (2020) — 730 PS / 3982 ccm / 325 km/h / 3.2s

Dependencies: Phase 338 (autos.json mit auto_bj Array vorhanden)
Zero-Bug Policy: Kein gen.py-Patch nötig — alle Arrays bereits registriert
"""
import json, os, subprocess, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")

CARS = [
    # Mercedes-Benz 450 SEL 6.9 (1975) — M100, 6834 ccm, 286 PS, 225 km/h, 7.4s
    {"key": "Mercedes-Benz 450 SEL 6.9 (Deutschland, 1975)",
     "ps": 286, "ccm": 6834, "vmax": 225, "accel": 7.4, "bj": 1975, "ev": False},
    # Mercedes-Benz 500E W124 (1992) — M119, 4973 ccm, 326 PS, 250 km/h, 6.1s
    {"key": "Mercedes-Benz 500E W124 (Deutschland, 1992)",
     "ps": 326, "ccm": 4973, "vmax": 250, "accel": 6.1, "bj": 1992, "ev": False},
    # Mercedes-Benz SLS AMG (2010) — M159, 6208 ccm, 571 PS, 317 km/h, 3.8s
    {"key": "Mercedes-Benz SLS AMG (Deutschland, 2010)",
     "ps": 571, "ccm": 6208, "vmax": 317, "accel": 3.8, "bj": 2010, "ev": False},
    # Mercedes-Benz A45 AMG (2013) — M133, 1991 ccm, 381 PS, 270 km/h, 4.6s
    {"key": "Mercedes-Benz A45 AMG (Deutschland, 2013)",
     "ps": 381, "ccm": 1991, "vmax": 270, "accel": 4.6, "bj": 2013, "ev": False},
    # Mercedes-AMG GT Black Series (2020) — M178 LS2, 3982 ccm, 730 PS, 325 km/h, 3.2s
    {"key": "Mercedes-AMG GT Black Series (Deutschland, 2020)",
     "ps": 730, "ccm": 3982, "vmax": 325, "accel": 3.2, "bj": 2020, "ev": False},
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
    print("PATCH 339 — Mercedes-Benz-Sprint (5 neue Modelle)")
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
         "--phase", "339",
         "--patch", "patches/patch_339_mercedes.py",
         "--summary",
         "Mercedes-Benz-Sprint: 450 SEL 6.9, 500E W124, SLS AMG, A45 AMG, "
         "AMG GT Black Series (5 neue Modelle — gesamt 9 Mercedes)"])
