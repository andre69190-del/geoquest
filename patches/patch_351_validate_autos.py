#!/usr/bin/env python3
"""
Phase: 351
Date:  2026-06-01
Author: Claude / Andre
Scope: validate_content.py — 3 neue Checks für Mobilitäts-Daten

Description:
  Lücke 1: detect_and_check() erkennt jetzt autos.json
    → check_hl() für alle 5 HL-Arrays (auto_ps, auto_vmax, auto_accel, auto_ccm, auto_bj)
    → Extra-Check: auto_ccm darf keine ccm=0 enthalten (EVs müssen ausgeschlossen sein)

  Lücke 2: Neue Funktion check_autos_extended()
    → Pflichtfelder-Check (22 Felder)
    → Enum-Validierung (antrieb, karosserie, antriebsart, motorbauart, getriebe, konzern)
    → Logik-Checks (EV: tank=0, verbrauch_l=0.0, zylinder=0; Verbrenner: akku=0.0)

  Lücke 3: Cross-Validation am Ende von main()
    → Prüft ob jeder Name aus autos.json[auto_bj] in autos_extended.json vorhanden ist
    → Fehlende Keys → warn() (Lookup würde zur Laufzeit crashen)

Dependencies: Phase 350 (autos_extended.json)
Zero-Bug Policy: assert c.count(old) == 1 vor jedem replace()
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VC   = os.path.join(ROOT, "validate_content.py")


def patch(c, old, new, label):
    count = c.count(old)
    assert count == 1, f"[FAIL] Anker {count}x gefunden: {old[:60]!r}"
    print(f"  [OK] {label}")
    return c.replace(old, new, 1)


if __name__ == "__main__":
    print("=" * 62)
    print("PATCH 351 — validate_content.py: 3 neue Auto-Checks")
    print("=" * 62)

    with open(VC, encoding="utf-8") as f:
        c = f.read()

    # ── Lücke 2: check_autos_extended() vor detect_and_check() einfügen ─────
    FUNC_ANCHOR = "def detect_and_check(filename):"
    CHECK_EXT = '''\
def check_autos_extended(filename, data):
    """Validiert data/autos_extended.json (flaches Dict, 22 Pflichtfelder)."""
    REQUIRED_FIELDS = [
        "gewicht", "drehmoment", "cw", "kofferraum", "laenge",
        "tank", "akku", "reichweite_km", "verbrauch_l", "verbrauch_kwh",
        "antrieb", "karosserie", "antriebsart", "motorbauart", "zylinder",
        "turbo", "getriebe", "sitze", "neupreis_eur", "baujahr_ende",
        "nordschleife", "konzern",
    ]
    ENUMS = {
        "antrieb":     {"Front", "Heck", "Allrad"},
        "getriebe":    {"Handschalter", "Automatik", "E-Getriebe"},
        "motorbauart": {"Reihe", "V", "W", "Boxer", "Wankel", "E-Motor"},
        "antriebsart": {"Benzin", "Diesel", "EV", "Hybrid", "PHEV", "MHEV"},
        "karosserie":  {"Hatchback", "Limousine", "Kombi", "SUV",
                        "Coupé", "Cabrio", "Roadster", "Sportwagen", "Van", "Pickup"},
        "konzern":     {"VW", "BMW", "Mercedes", "Stellantis", "Ford",
                        "Renault-Nissan", "Toyota", "Hyundai-Kia", "Tata",
                        "Geely", "Honda", "Mazda", "Subaru", "unabhaengig", "unabhängig"},
    }
    if not isinstance(data, dict):
        warn(filename, "struktur", "root", "autos_extended.json muss ein Dict sein")
        return
    for car_name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, "eintrag", car_name, "Wert ist kein Dict")
            continue
        # Pflichtfelder
        for f in REQUIRED_FIELDS:
            if f not in entry:
                warn(filename, "pflichtfeld", car_name, f"Feld '{f}' fehlt")
        # Enum-Checks
        for field, allowed in ENUMS.items():
            val = entry.get(field)
            if val is not None and val not in allowed:
                warn(filename, f"enum:{field}", car_name,
                     f"Wert {val!r} nicht erlaubt")
        # Logik-Checks
        art = entry.get("antriebsart", "")
        if art == "EV":
            if entry.get("tank", -1) != 0:
                warn(filename, "logik:EV-tank", car_name,
                     f"EV muss tank=0 haben (ist {entry.get('tank')})")
            if entry.get("verbrauch_l", -1) != 0.0:
                warn(filename, "logik:EV-verbrauch_l", car_name,
                     f"EV muss verbrauch_l=0.0 haben (ist {entry.get('verbrauch_l')})")
            if entry.get("zylinder", -1) != 0:
                warn(filename, "logik:EV-zylinder", car_name,
                     f"EV muss zylinder=0 haben (ist {entry.get('zylinder')})")
        if art not in ("EV", "Hybrid", "PHEV", "MHEV"):
            akku = entry.get("akku", None)
            if akku is not None and float(akku) != 0.0:
                warn(filename, "logik:akku", car_name,
                     f"{art}: akku muss 0.0 sein (ist {akku})")


''' + FUNC_ANCHOR

    c = patch(c, FUNC_ANCHOR, CHECK_EXT, "check_autos_extended() eingefügt")

    # ── Lücke 1: detect_and_check() — Routing für autos.json + autos_extended.json
    OLD_TL = '    elif name == "timeline.json":'
    NEW_TL = '''\
    elif name == "autos.json":
        # Lücke 1: 5 HL-Arrays per check_hl validieren
        if isinstance(data, dict):
            for arr_key, block in data.items():
                if isinstance(block, dict) and "items" in block:
                    check_hl(filename, {arr_key: block})
                    if arr_key == "auto_ccm":
                        bad = [i.get("name", "?") for i in block.get("items", [])
                               if i.get("val", 1) == 0]
                        if bad:
                            warn(filename, "auto_ccm", bad[0],
                                 f"{len(bad)} Eintraege mit ccm=0 (EVs muessen ausgeschlossen sein)")
    elif name == "autos_extended.json":
        check_autos_extended(filename, data)
    elif name == "timeline.json":'''

    c = patch(c, OLD_TL, NEW_TL, "detect_and_check: autos.json + autos_extended.json Routing")

    # ── Lücke 3: Cross-Validation am Ende der main()-Schleife ────────────────
    OLD_RESULTS = (
        '    print("\\n" + BOLD + "=" * 62)\n'
        '    print(" Results: " + str(checked) + "/" + str(len(json_files)) + '
        '" files scanned  |  " + str(len(warnings)) + " warning(s)")\n'
        '    print("=" * 62 + RESET + "\\n")'
    )
    NEW_RESULTS = (
        '    # Lücke 3: Cross-Validation autos.json <-> autos_extended.json\n'
        '    import json as _json\n'
        '    _autos_p    = os.path.join(DATA, "autos.json")\n'
        '    _extended_p = os.path.join(DATA, "autos_extended.json")\n'
        '    if os.path.exists(_autos_p) and os.path.exists(_extended_p):\n'
        '        print("  [Cross-Val autos <-> extended]", end=" ")\n'
        '        try:\n'
        '            with open(_autos_p,    encoding="utf-8") as _fh: _a = _json.load(_fh)\n'
        '            with open(_extended_p, encoding="utf-8") as _fh: _e = _json.load(_fh)\n'
        '            _all  = {i["name"] for i in _a.get("auto_bj", {}).get("items", [])}\n'
        '            _miss = sorted(n for n in _all if n not in _e)\n'
        '            if _miss:\n'
        '                for _n in _miss:\n'
        '                    warn("cross_validation", "autos_extended", _n,\n'
        '                         "Auto in autos.json aber NICHT in autos_extended.json")\n'
        '                print(WARN + f"{len(_miss)} fehlend" + RESET)\n'
        '            else:\n'
        '                print(OK + f"OK -- alle {len(_all)} Autos im Extended-Dict" + RESET)\n'
        '        except Exception as _exc:\n'
        '            warn("cross_validation", "load", "", f"Fehler: {_exc}")\n'
        '            print(WARN + "Fehler" + RESET)\n'
        '\n'
        '    print("\\n" + BOLD + "=" * 62)\n'
        '    print(" Results: " + str(checked) + "/" + str(len(json_files)) + '
        '" files scanned  |  " + str(len(warnings)) + " warning(s)")\n'
        '    print("=" * 62 + RESET + "\\n")'
    )

    c = patch(c, OLD_RESULTS, NEW_RESULTS, "main(): Cross-Validation eingefügt")

    with open(VC, "w", encoding="utf-8") as f:
        f.write(c)
    print("  validate_content.py gespeichert")

    # Syntax-Check
    r = subprocess.run([sys.executable, "-m", "py_compile", VC],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  SYNTAX-FEHLER: {r.stderr}")
        sys.exit(1)
    print("  Syntax OK")

    # Smoke-Test
    print("\n  Smoke-Test (validate_content.py):")
    r = subprocess.run([sys.executable, "validate_content.py"],
                       cwd=ROOT, capture_output=True, text=True)
    print(r.stdout[-600:] if r.stdout else "")
    if r.stderr: print(r.stderr[-200:])

    # Post-Phase
    subprocess.run([
        sys.executable, "post_phase.py",
        "--phase", "351",
        "--patch", "patches/patch_351_validate_autos.py",
        "--summary",
        "validate_content.py: check_autos_extended() + autos.json HL-Routing + "
        "auto_ccm EV-Check + Cross-Validation autos <-> autos_extended"
    ], cwd=ROOT, capture_output=True, text=True)
    print("\n  Ergebnis:")
    if r.returncode == 0:
        print("  OK — keine neuen Warnings erwartet")
    else:
        print(f"  {r.returncode} Return-Code")
