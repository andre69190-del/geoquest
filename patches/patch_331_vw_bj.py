#!/usr/bin/env python3
"""
Phase: 331
Date:  2026-06-01
Author: Claude / Andre
Scope: VW-Modelle (alle Golf-Generationen + Corrado/Phaeton) + neues auto_bj-Array

Description:
  Zwei Dinge in einem Sprint:

  A) Neues Array auto_bj (Baujahr-Vergleich):
     "Welches Fahrzeug wurde SPÄTER gebaut?" — höheres Jahr = gewinnt.
     Befüllt mit Baujahr-Werten ALLER bereits vorhandenen 55 Fahrzeuge.
     Neuer Modus hl_auto_bj in gen.py registriert.

  B) VW-Marken-Sprint (erste Marke des Serien-Aufbaus):
     Golf 1 GTI      (1976) — 110 PS  / 1588 ccm / 182 km/h / 9.0s
     Golf 2 GTI 16V  (1987) — 139 PS  / 1781 ccm / 205 km/h / 8.3s
     Golf 3 GTI 2.0  (1992) — 115 PS  / 1984 ccm / 200 km/h / 9.2s
     Golf 4 R32      (2002) — 241 PS  / 3189 ccm / 250 km/h / 6.6s
     Golf 5 GTI      (2004) — 200 PS  / 1984 ccm / 236 km/h / 7.2s
     Golf 6 GTI      (2009) — 210 PS  / 1984 ccm / 244 km/h / 6.9s
     Golf 7 R        (2013) — 300 PS  / 1984 ccm / 250 km/h / 4.9s
     Golf 8 GTI CS   (2021) — 300 PS  / 1984 ccm / 250 km/h / 5.6s
     VW Corrado VR6  (1992) — 190 PS  / 2861 ccm / 231 km/h / 7.3s
     VW Phaeton W12  (2002) — 420 PS  / 5998 ccm / 300 km/h / 5.7s
     Alle VW-Werte aus offiziellen Werksdaten / EG-Typgenehmigungen.

Dependencies: Phase 330 (autos.json mit 55 Fahrzeugen, genAutosHL registriert)
Zero-Bug Policy: assert c.count(old) == 1 vor jedem replace()
"""

import json
import os
import subprocess
import sys

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTOS = os.path.join(ROOT, "data", "autos.json")
GEN   = os.path.join(ROOT, "gen.py")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ {os.path.basename(path)} gespeichert")

def add_dedup(items, new_entries, key="name"):
    existing = {e[key].lower() for e in items}
    added = 0
    for entry in new_entries:
        if entry[key].lower() not in existing:
            items.append(entry)
            existing.add(entry[key].lower())
            added += 1
        else:
            print(f"    Duplikat: {entry[key]}")
    return added

def patch(c, old, new, label):
    count = c.count(old)
    assert count == 1, f"[FAIL] Anker {count}×: {old!r}"
    print(f"  [OK] {label}")
    return c.replace(old, new, 1)

def run(cmd, cwd=ROOT):
    print(f"\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.stdout: print(r.stdout)
    if r.stderr: print(r.stderr, file=sys.stderr)
    return r.returncode


# ---------------------------------------------------------------------------
# A) auto_bj — Baujahr aller 55 bestehenden Fahrzeuge
#    (Jahr direkt aus den Klammern im Name extrahiert)
# ---------------------------------------------------------------------------

# Mapping: name (exakt wie in autos.json) → Baujahr
BAUJAHR_MAP = {
    "VW Käfer 1200 (Deutschland, 1965)":        1965,
    "Citroën 2CV (Frankreich, 1949)":           1949,
    "Fiat 500 (Italien, 1957)":                 1957,
    "Mini Cooper S (UK, 1964)":                 1964,
    "Ford Mustang GT (USA, 1964)":              1964,
    "Porsche 911 Carrera (Deutschland, 1963)":  1963,
    "Ferrari 250 GTO (Italien, 1962)":          1962,
    "Jaguar E-Type (UK, 1961)":                 1961,
    "Chevrolet Corvette C1 (USA, 1953)":        1953,
    "Toyota Supra MK4 (Japan, 1993)":           1993,
    "Lamborghini Miura (Italien, 1966)":        1966,
    "Aston Martin DB5 (UK, 1963)":              1963,
    "Peugeot 205 GTI (Frankreich, 1984)":       1984,
    "BMW M3 E30 (Deutschland, 1986)":           1986,
    "Honda NSX (Japan, 1990)":                  1990,
    "Škoda 130 RS (Tschechien, 1975)":          1975,
    "Tatra 603 (Tschechien, 1956)":             1956,
    "Dacia 1300 (Rumänien, 1969)":              1969,
    "Dacia Sandero RS (Rumänien, 2015)":        2015,
    "FSO Polonez (Polen, 1978)":                1978,
    "Arrinera Hussarya GT (Polen, 2014)":       2014,
    "Volvo P1800 (Schweden, 1961)":             1961,
    "Koenigsegg Agera RS (Schweden, 2015)":     2015,
    "SEAT Ibiza Cupra (Spanien, 2000)":         2000,
    "Cupra Formentor VZ5 (Spanien, 2021)":      2021,
    "Donkervoort D8 GTO (Niederlande, 2013)":   2013,
    "Spyker C8 (Niederlande, 2000)":            2000,
    "Rimac Nevera (Kroatien, 2021)":            2021,
    "Zenvo TSR-S (Dänemark, 2018)":             2018,
    "KTM X-Bow R (Österreich, 2012)":           2012,
    "Togg T10X (Türkei, 2023)":                 2023,
    "Anadol A1 (Türkei, 1966)":                 1966,
    "Hyundai i30 N (Südkorea, 2017)":           2017,
    "Kia Stinger GT (Südkorea, 2017)":          2017,
    "Renault 5 Turbo (Frankreich, 1980)":       1980,
    "Alfa Romeo Giulia GTA (Italien, 1965)":    1965,
    "Bugatti Veyron 16.4 (Frankreich, 2005)":   2005,
    "Bugatti Chiron (Frankreich, 2016)":        2016,
    "Bentley Continental GT (UK, 2003)":        2003,
    "Rolls-Royce Silver Shadow (UK, 1965)":     1965,
    "Dodge Viper GTS (USA, 1996)":              1996,
    "Ford GT40 (USA/UK, 1964)":                 1964,
    "Nissan GT-R R35 (Japan, 2007)":            2007,
    "Mazda RX-7 FD (Japan, 1992)":              1992,
    "Mercedes-Benz 300 SL (Deutschland, 1954)": 1954,
    "Porsche 918 Spyder (Deutschland, 2013)":   2013,
    "Ferrari LaFerrari (Italien, 2013)":        2013,
    "McLaren F1 (UK, 1992)":                    1992,
    "Tesla Model S Plaid (USA, 2021)":          2021,
    "Rimac C_Two (Kroatien, 2018)":             2018,
    "Gillet Vertigo (Belgien, 2003)":           2003,
    "Think City (Norwegen, 2008, EV)":          2008,
    "Sin Cars R1 (Bulgarien, 2014)":            2014,
    "UMM Alter II (Portugal, 1985)":            1985,
    "NAMCO Pony (Griechenland, 1972)":          1972,
}

# ---------------------------------------------------------------------------
# B) Neue VW-Einträge — 10 Fahrzeuge
# ---------------------------------------------------------------------------

NEW_VW = [
    # Golf 1 GTI (1976) — 1588 ccm, 110 PS, 182 km/h, 9.0s
    {"key": "Golf 1 GTI (VW, Deutschland, 1976)",
     "ps": 110, "ccm": 1588, "vmax": 182, "accel": 9.0, "bj": 1976},
    # Golf 2 GTI 16V (1987) — 1781 ccm, 139 PS, 205 km/h, 8.3s
    {"key": "Golf 2 GTI 16V (VW, Deutschland, 1987)",
     "ps": 139, "ccm": 1781, "vmax": 205, "accel": 8.3, "bj": 1987},
    # Golf 3 GTI 2.0 (1992) — 1984 ccm, 115 PS, 200 km/h, 9.2s
    {"key": "Golf 3 GTI 2.0 (VW, Deutschland, 1992)",
     "ps": 115, "ccm": 1984, "vmax": 200, "accel": 9.2, "bj": 1992},
    # Golf 4 R32 (2002) — 3189 ccm, 241 PS, 250 km/h, 6.6s
    {"key": "Golf 4 R32 (VW, Deutschland, 2002)",
     "ps": 241, "ccm": 3189, "vmax": 250, "accel": 6.6, "bj": 2002},
    # Golf 5 GTI (2004) — 1984 ccm, 200 PS, 236 km/h, 7.2s
    {"key": "Golf 5 GTI (VW, Deutschland, 2004)",
     "ps": 200, "ccm": 1984, "vmax": 236, "accel": 7.2, "bj": 2004},
    # Golf 6 GTI (2009) — 1984 ccm, 210 PS, 244 km/h, 6.9s
    {"key": "Golf 6 GTI (VW, Deutschland, 2009)",
     "ps": 210, "ccm": 1984, "vmax": 244, "accel": 6.9, "bj": 2009},
    # Golf 7 R (2013) — 1984 ccm, 300 PS, 250 km/h (el. begrenzt), 4.9s
    {"key": "Golf 7 R (VW, Deutschland, 2013)",
     "ps": 300, "ccm": 1984, "vmax": 250, "accel": 4.9, "bj": 2013},
    # Golf 8 GTI Clubsport (2021) — 1984 ccm, 300 PS, 250 km/h, 5.6s
    {"key": "Golf 8 GTI Clubsport (VW, Deutschland, 2021)",
     "ps": 300, "ccm": 1984, "vmax": 250, "accel": 5.6, "bj": 2021},
    # VW Corrado VR6 (1992) — 2861 ccm, 190 PS, 231 km/h, 7.3s
    {"key": "VW Corrado VR6 (Deutschland, 1992)",
     "ps": 190, "ccm": 2861, "vmax": 231, "accel": 7.3, "bj": 1992},
    # VW Phaeton W12 (2002) — 5998 ccm, 420 PS, 300 km/h, 5.7s
    {"key": "VW Phaeton W12 (Deutschland, 2002)",
     "ps": 420, "ccm": 5998, "vmax": 300, "accel": 5.7, "bj": 2002},
]

# ---------------------------------------------------------------------------
# Patch ausführen
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("PATCH 331 — VW-Sprint + auto_bj (Baujahr-Modus)")
    print("=" * 60)

    autos = load_json(AUTOS)

    # ── A1: auto_bj Array anlegen (aus bestehenden + neuen VW) ────────────
    if "auto_bj" not in autos:
        autos["auto_bj"] = {
            "prompt": "Welches Fahrzeug wurde SPÄTER gebaut?",
            "unit": "Jahr",
            "items": []
        }
        print("\n  [NEU] auto_bj Array angelegt")

    bj_items = autos["auto_bj"]["items"]

    # Baujahr für alle bereits vorhandenen Fahrzeuge eintragen
    bj_existing = {e["name"].lower() for e in bj_items}
    for name, year in BAUJAHR_MAP.items():
        if name.lower() not in bj_existing:
            bj_items.append({"name": name, "val": year})
            bj_existing.add(name.lower())
    print(f"  auto_bj: {len(bj_items)} Baujahr-Einträge (bestehende Fahrzeuge)")

    # ── B: VW-Fahrzeuge in alle 5 Arrays eintragen ────────────────────────
    print("\n  VW-Modelle:")
    totals = {"auto_ps": 0, "auto_vmax": 0, "auto_accel": 0,
              "auto_ccm": 0, "auto_bj": 0}

    for car in NEW_VW:
        name = car["key"]

        # PS
        n = add_dedup(autos["auto_ps"]["items"],
                      [{"name": name, "val": car["ps"]}])
        totals["auto_ps"] += n

        # vmax
        n = add_dedup(autos["auto_vmax"]["items"],
                      [{"name": name, "val": car["vmax"]}])
        totals["auto_vmax"] += n

        # accel
        n = add_dedup(autos["auto_accel"]["items"],
                      [{"name": name, "val": car["accel"]}])
        totals["auto_accel"] += n

        # ccm (alle VW hier sind Verbrenner)
        n = add_dedup(autos["auto_ccm"]["items"],
                      [{"name": name, "val": car["ccm"]}])
        totals["auto_ccm"] += n

        # bj
        n = add_dedup(autos["auto_bj"]["items"],
                      [{"name": name, "val": car["bj"]}])
        totals["auto_bj"] += n

        print(f"    + {name}")

    print()
    for arr, n in totals.items():
        total = len(autos[arr]["items"])
        print(f"  {arr}: +{n} neu (gesamt: {total})")

    save_json(AUTOS, autos)

    # ── C: gen.py patchen — hl_auto_bj registrieren ───────────────────────
    print("\n" + "=" * 60)
    print("gen.py — hl_auto_bj registrieren")
    print("=" * 60)

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    # C1: MODES — neuer Eintrag nach hl_auto_ccm
    OLD_M = ('id:"hl_auto_ccm",   icon:"\\u2699\\uFE0F",'
             'title:"Auto-Quartett: Hubraum",      '
             'group:"autos",prompt:"Welcher Verbrenner hat mehr Hubraum?",'
             'desc:"Nur Verbrenner \\u2014 375 ccm bis 7993 ccm",'
             'prompt_en:"Which combustion car has the larger engine displacement?"}')
    NEW_M = (OLD_M + ',\n'
             '    {id:"hl_auto_bj",    icon:"\\u{1F4C5}",'
             'title:"Auto-Quartett: Baujahr",       '
             'group:"autos",prompt:"Welches Fahrzeug wurde SP\\u00c4TER gebaut?",'
             'desc:"Neueres Modell gewinnt \\u2014 1949 bis heute",'
             'prompt_en:"Which car was built LATER?"}')
    c = patch(c, OLD_M, NEW_M, "MODES: hl_auto_bj")

    # C2: MODE_CATS — autos-Gruppe erweitern
    OLD_C = ('"hl_auto_ps","hl_auto_vmax","hl_auto_accel","hl_auto_ccm"],'
             'cost:0},')
    NEW_C = ('"hl_auto_ps","hl_auto_vmax","hl_auto_accel","hl_auto_ccm",'
             '"hl_auto_bj"],cost:0},')
    c = patch(c, OLD_C, NEW_C, "MODE_CATS: hl_auto_bj")

    # C3: GEN dispatch — nach hl_auto_ccm
    OLD_G = 'hl_auto_ccm:()=>genAutosHL("auto_ccm"),'
    NEW_G = (OLD_G + '\n'
             '  hl_auto_bj:()=>genAutosHL("auto_bj"),')
    c = patch(c, OLD_G, NEW_G, "GEN dispatch: hl_auto_bj")

    with open(GEN, "w", encoding="utf-8") as f:
        f.write(c)
    print("  ✓ gen.py gespeichert")

    # ── Build + Verify + Post ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Build …")
    print("=" * 60)
    if run([sys.executable, "gen.py"]) != 0:
        print("✗ Build fehlgeschlagen"); sys.exit(1)

    print("\n" + "=" * 60)
    print("Verifizierung …")
    print("=" * 60)
    if run([sys.executable, "verify.py"]) != 0:
        print("✗ verify.py fehlgeschlagen"); sys.exit(1)

    run([sys.executable, "validate_content.py"])

    print("\n" + "=" * 60)
    print("Post-Phase …")
    print("=" * 60)
    run([sys.executable, "post_phase.py",
         "--phase", "331",
         "--patch", "patches/patch_331_vw_bj.py",
         "--summary",
         "VW-Sprint: Golf 1-8 GTI/R + Corrado VR6 + Phaeton W12 (10 Modelle) — "
         "NEU: auto_bj Baujahr-Array + hl_auto_bj Modus (726 Modi)"])
