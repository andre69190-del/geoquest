#!/usr/bin/env python3
"""
Phase: 333  Scope: BMW-Sprint — 6 weitere Modelle (BMW M3 E30 bereits vorhanden)

  BMW 2002 Turbo       (1973) — 170 PS / 1990 ccm / 211 km/h / 6.9s
  BMW M1               (1978) — 277 PS / 3453 ccm / 262 km/h / 5.6s
  BMW M5 E34           (1988) — 315 PS / 3535 ccm / 250 km/h / 5.9s
  BMW Z8               (2000) — 400 PS / 4941 ccm / 250 km/h / 4.7s
  BMW M3 E92           (2008) — 420 PS / 3999 ccm / 250 km/h / 4.8s
  BMW M4 Competition   (2021) — 510 PS / 2993 ccm / 290 km/h / 3.9s
"""
import json, os, subprocess, sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")

CARS = [
    {"key": "BMW 2002 Turbo (Deutschland, 1973)",
     "ps": 170, "ccm": 1990, "vmax": 211, "accel": 6.9, "bj": 1973},
    {"key": "BMW M1 (Deutschland, 1978)",
     "ps": 277, "ccm": 3453, "vmax": 262, "accel": 5.6, "bj": 1978},
    {"key": "BMW M5 E34 (Deutschland, 1988)",
     "ps": 315, "ccm": 3535, "vmax": 250, "accel": 5.9, "bj": 1988},
    {"key": "BMW Z8 (Deutschland, 2000)",
     "ps": 400, "ccm": 4941, "vmax": 250, "accel": 4.7, "bj": 2000},
    {"key": "BMW M3 E92 (Deutschland, 2008)",
     "ps": 420, "ccm": 3999, "vmax": 250, "accel": 4.8, "bj": 2008},
    {"key": "BMW M4 Competition (Deutschland, 2021)",
     "ps": 510, "ccm": 2993, "vmax": 290, "accel": 3.9, "bj": 2021},
]

def dedup(items, name, val):
    if any(e["name"].lower() == name.lower() for e in items):
        return 0
    items.append({"name": name, "val": val}); return 1

def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    print(r.stdout[-300:] if r.stdout else "")
    return r.returncode

if __name__ == "__main__":
    print("PATCH 333 — BMW-Sprint")
    with open(AUTOS, encoding="utf-8") as f: d = json.load(f)
    for car in CARS:
        n = car["key"]
        dedup(d["auto_ps"]["items"],    n, car["ps"])
        dedup(d["auto_vmax"]["items"],  n, car["vmax"])
        dedup(d["auto_accel"]["items"], n, car["accel"])
        dedup(d["auto_ccm"]["items"],   n, car["ccm"])
        dedup(d["auto_bj"]["items"],    n, car["bj"])
        print(f"  + {n}")
    with open(AUTOS, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  auto_ps gesamt: {len(d['auto_ps']['items'])}")
    if run([sys.executable, "gen.py"]) != 0: sys.exit(1)
    if run([sys.executable, "verify.py"]) != 0: sys.exit(1)
    run([sys.executable, "post_phase.py", "--phase", "333",
         "--patch", "patches/patch_333_bmw.py",
         "--summary", "BMW-Sprint: 2002 Turbo, M1, M5 E34, Z8, M3 E92, M4 Competition (6 Modelle)"])
