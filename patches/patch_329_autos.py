#!/usr/bin/env python3
"""
Phase: 329
Date:  2026-05-31
Author: Claude / Andre
Scope: Auto-Quartett (4 HL-Modi) in gen.py registrieren

Description:
  Integriert data/autos.json in die GeoQuest-Engine als 4 Higher/Lower-Modi:
    hl_auto_ps    — Welches Fahrzeug hat mehr PS?
    hl_auto_vmax  — Welches Fahrzeug ist schneller?
    hl_auto_accel — Welches Fahrzeug braucht LÄNGER für 0-100 km/h?
    hl_auto_ccm   — Welches Fahrzeug hat mehr Hubraum?

  Accel-Hinweis: Da _mkHL() den höheren Zahlenwert als "richtiger" bewertet,
  ist der accel-Prompt bewusst auf "braucht LÄNGER" formuliert — höhere Sekunden
  = richtige Antwort. Der Prompt in autos.json ist entsprechend gesetzt.

  Patchpunkte (je exakt 1× im Quelltext):
    1. Python-Dateiladeblock  — nach TIMELINE_J load
    2. JS-const-Deklaration   — nach SPORT_HL_DATA=PLACEHOLDER_SPORT_HL
    3. Python .replace()-Kette — nach PLACEHOLDER_TIMELINE replace
    4. Generator-Variable      — nach initSportWissenWS
    5. MODES-Array             — neue Gruppe "autos" nach letztem zuege-Eintrag
    6. MODE_CATS               — neuer Eintrag "autos" vor abschließendem };
    7. GEN-Dispatch            — 4 neue IDs nach zug_reisezeit_hl

Dependencies: Phase 329a (autos.json angelegt)
Zero-Bug Policy: assert c.count(old) == 1 vor jedem replace()
"""

import sys
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, "gen.py")

def patch(c, old, new, label):
    count = c.count(old)
    assert count == 1, f"[FAIL] Anker nicht eindeutig ({count}×): {old!r}"
    c = c.replace(old, new, 1)
    print(f"  [OK] {label}")
    return c

def run(cmd, cwd=ROOT):
    print(f"\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if r.stdout: print(r.stdout)
    if r.stderr: print(r.stderr, file=sys.stderr)
    return r.returncode


if __name__ == "__main__":
    print("=" * 60)
    print("PATCH 329 — Auto-Quartett Engine-Integration")
    print("=" * 60)

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    # ── 1. Python: Datei laden ────────────────────────────────────────────────
    OLD1 = ("'data/timeline.json'),   'r', encoding='utf-8') as _f: "
            "TIMELINE_J    = _f.read()")
    NEW1 = (OLD1 + "\n"
            "with open(os.path.join(os.path.dirname(__file__), "
            "'data/autos.json'),       'r', encoding='utf-8') as _f: "
            "AUTOS_J       = _f.read()")
    c = patch(c, OLD1, NEW1, "Python: autos.json laden")

    # ── 2. JS: const-Deklaration ─────────────────────────────────────────────
    OLD2 = "const SPORT_HL_DATA=PLACEHOLDER_SPORT_HL;"
    NEW2 = OLD2 + "\nconst AUTOS_DATA=PLACEHOLDER_AUTOS;"
    c = patch(c, OLD2, NEW2, "JS const: AUTOS_DATA=PLACEHOLDER_AUTOS")

    # ── 3. Python: .replace()-Kette ──────────────────────────────────────────
    OLD3 = ".replace('PLACEHOLDER_TIMELINE',     TIMELINE_J)"
    NEW3 = OLD3 + "\n  .replace('PLACEHOLDER_AUTOS',          AUTOS_J)"
    c = patch(c, OLD3, NEW3, "Python replace: PLACEHOLDER_AUTOS → AUTOS_J")

    # ── 4. JS: Generator-Variable ────────────────────────────────────────────
    OLD4 = 'var initSportWissenWS=_mkWS(SPORT_WS_DATA,"SportW");'
    NEW4 = (OLD4 + "\n"
            "/* === Phase 329: Auto-Quartett-Generator === */\n"
            "var genAutosHL=_mkHL(AUTOS_DATA);")
    c = patch(c, OLD4, NEW4, "JS var: genAutosHL=_mkHL(AUTOS_DATA)")

    # ── 5. MODES: 4 neue Einträge (Gruppe autos) ─────────────────────────────
    # Anchor: unique closing of the last zug_ds100_input block into uk_hafen_world
    OLD5 = ('},\n\n    {id:"uk_hafen_world",     icon:"\\u{1F6A2}",'
            'title:"Welthafen zuordnen",  ')
    NEW5 = ('},\n\n'
            '    /* === Phase 329: Auto-Quartett === */\n'
            '    {id:"hl_auto_ps",    icon:"\\u{1F3CE}\\uFE0F",'
            'title:"Auto-Quartett: Leistung",  '
            'group:"autos",prompt:"Welches Fahrzeug hat mehr PS?",'
            'desc:"Von 9 PS (2CV) bis 1914 PS (Rimac Nevera) — ",'
            'prompt_en:"Which car has more horsepower?"},\n'
            '    {id:"hl_auto_vmax",  icon:"\\u{1F3C1}",'
            'title:"Auto-Quartett: Top-Speed",   '
            'group:"autos",prompt:"Welches Fahrzeug ist schneller?",'
            'desc:"Höchstgeschwindigkeit — 85 bis 447 km/h",'
            'prompt_en:"Which car has a higher top speed?"},\n'
            '    {id:"hl_auto_accel", icon:"\\u23F1\\uFE0F",'
            'title:"Auto-Quartett: 0-100 km/h",  '
            'group:"autos",prompt:"Welches Fahrzeug braucht L\\u00e4nger auf 100?",'
            'desc:"H\\u00f6herer Wert = langsamer = h\\u00f6her in diesem Modus",'
            'prompt_en:"Which car takes LONGER to reach 100 km/h?"},\n'
            '    {id:"hl_auto_ccm",   icon:"\\u2699\\uFE0F",'
            'title:"Auto-Quartett: Hubraum",      '
            'group:"autos",prompt:"Welcher Verbrenner hat mehr Hubraum?",'
            'desc:"Nur Verbrenner — 375 ccm bis 7993 ccm",'
            'prompt_en:"Which combustion car has the larger engine displacement?"},\n'
            '\n    {id:"uk_hafen_world",     icon:"\\u{1F6A2}",'
            'title:"Welthafen zuordnen",  ')
    c = patch(c, OLD5, NEW5, "MODES: 4 Auto-Quartett-Einträge")

    # ── 6. MODE_CATS: neue Gruppe autos ──────────────────────────────────────
    OLD6 = ('timeline_sport_stadien"\n  ],cost:0},\n};')
    NEW6 = ('timeline_sport_stadien"\n  ],cost:0},\n'
            '  autos:{label:"Auto-Quartett",icon:"\\u{1F3CE}\\uFE0F",'
            'modes:["hl_auto_ps","hl_auto_vmax","hl_auto_accel","hl_auto_ccm"],'
            'cost:0},\n};')
    c = patch(c, OLD6, NEW6, "MODE_CATS: autos-Gruppe")

    # ── 7. GEN: Dispatch-Einträge ─────────────────────────────────────────────
    OLD7 = "zug_reisezeit_hl:()=>genZugReisezeitHL(),"
    NEW7 = (OLD7 + "\n"
            "  /* === Phase 329: Auto-Quartett === */\n"
            "  hl_auto_ps:()=>genAutosHL(\"auto_ps\"),\n"
            "  hl_auto_vmax:()=>genAutosHL(\"auto_vmax\"),\n"
            "  hl_auto_accel:()=>genAutosHL(\"auto_accel\"),\n"
            "  hl_auto_ccm:()=>genAutosHL(\"auto_ccm\"),")
    c = patch(c, OLD7, NEW7, "GEN dispatch: 4 Auto-HL-IDs")

    with open(GEN, "w", encoding="utf-8") as f:
        f.write(c)
    print("  ✓ gen.py gespeichert")

    print("\n" + "=" * 60)
    print("Build …")
    print("=" * 60)
    rb = run([sys.executable, "gen.py"])
    if rb != 0:
        print("✗ gen.py Build fehlgeschlagen"); sys.exit(1)

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
         "--phase", "329",
         "--patch", "patches/patch_329_autos.py",
         "--summary",
         "Auto-Quartett: 4 HL-Modi (PS, vmax, accel, ccm) aus data/autos.json — "
         "50 Fahrzeuge von VW Käfer bis Rimac Nevera, 17 Länder, EVs im ccm-Array ausgeschlossen"])
