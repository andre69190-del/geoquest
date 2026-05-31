#!/usr/bin/env python3
"""
Phase: 328
Date:  2026-05-31
Author: Claude / Andre
Scope: Heimvorteil-Algorithmus 70/30 in _mkMatchQ() einbauen

Description:
  Erweitert die universelle Match-Generator-Funktion _mkMatchQ() in gen.py
  um eine 70/30-Präferenz für das Heimatland des Nutzers.

  Analyse-Ergebnisse:
  - Richtige Funktion: _mkMatchQ(DATA), NICHT genUniversalMatchQ (existiert nicht)
  - S.language (nicht S.lang) ist die Sprachvariable
  - Das Muster (langLandMap + rng()<0.7) ist bereits in genZugReisezeitMC()
    (Phase 321b) etabliert — wird hier konsistent übernommen
  - Distraktoren bleiben unverändert (kommen aus items.map(x=>x.c) = globaler Pool)
  - Non-country c-Felder (Gesteinsklasse, Epochen usw.) → localPool leer → 100% Fallback
  - Pin-Modus (keine c-Feld) wird bewusst NICHT angefasst

  Patch-Logik: Exakt eine Zeile wird ersetzt:
    OLD: var idx=~~(rng()*items.length);
    NEW: Heimvorteil-Block (lang→Ländername-Mapping + localPool + 70/30-Wahl)

Dependencies: patch_321_zug_routen.py (etabliert das 70/30-Muster in genZugReisezeitMC)
Zero-Bug Policy: assert c.count(old) == 1 vor jedem replace()
"""

import sys
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, "gen.py")

# ---------------------------------------------------------------------------
# Patch-Hilfsfunktion (Zero-Bug Policy)
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Neuer Heimvorteil-Block für _mkMatchQ
#
# Ersetzt: var idx=~~(rng()*items.length);
# Durch:   70/30-Selektion basierend auf S.language → deutschem Ländernamen
#
# Mapping-Design:
#   - Lang-Code → deutscher Ländername (wie er im c-Feld der JSONs steht)
#   - Mehrsprachige Gebiete (de, at, ch) → alle auf "Deutschland"-Pool ODER
#     dedizierter Eintrag: "at"→"Österreich", "ch"→"Schweiz" (genauer)
#   - Fallback: leerer localPool → 100% global (perfekt für nicht-geogr. Arrays)
# ---------------------------------------------------------------------------

OLD = 'var idx=~~(rng()*items.length);\n    var correct=items[idx];'

NEW = '''\
/* Phase 328: Heimvorteil 70/30 — bevorzuge Einträge aus Nutzer-Land */
    var _hv_lang=(S&&S.language)||"de";
    var _hv_cmap={
      "de":"Deutschland","at":"Österreich","ch":"Schweiz",
      "fr":"Frankreich","it":"Italien","es":"Spanien",
      "pt":"Portugal","nl":"Niederlande","be":"Belgien",
      "pl":"Polen","cs":"Tschechien","sk":"Slowakei",
      "hu":"Ungarn","ro":"Rumänien","bg":"Bulgarien",
      "el":"Griechenland","hr":"Kroatien","tr":"Türkei",
      "sv":"Schweden","no":"Norwegen","da":"Dänemark","fi":"Finnland",
      "en":"Großbritannien","ru":"Russland","uk":"Ukraine",
      "ja":"Japan","zh":"China","ko":"Südkorea",
      "ar":"Ägypten","hi":"Indien","id":"Indonesien"
    };
    var _hv_cn=_hv_cmap[_hv_lang];
    var _hv_lp=_hv_cn?items.filter(function(x){return x.c===_hv_cn;}):[];
    var idx=(_hv_lp.length>0&&rng()<0.7)
      ?items.indexOf(_hv_lp[~~(rng()*_hv_lp.length)])
      :~~(rng()*items.length);
    var correct=items[idx];'''

# ---------------------------------------------------------------------------
# Patch ausführen
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("PATCH 328 – Heimvorteil-Algorithmus 70/30 in _mkMatchQ()")
    print("=" * 60)

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    size_before = len(c)
    c = patch(c, OLD, NEW, "_mkMatchQ(): Heimvorteil 70/30 eingebaut")
    size_after = len(c)
    print(f"  gen.py: {size_before} → {size_after} Bytes (+{size_after - size_before})")

    with open(GEN, "w", encoding="utf-8") as f:
        f.write(c)
    print("  ✓ gen.py gespeichert")

    print("\n" + "=" * 60)
    print("Build …")
    print("=" * 60)
    rb = run([sys.executable, "gen.py"])
    if rb != 0:
        print("✗ gen.py Build fehlgeschlagen")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("Verifizierung …")
    print("=" * 60)
    rv = run([sys.executable, "verify.py"])
    if rv != 0:
        print("✗ verify.py fehlgeschlagen")
        sys.exit(1)

    rc = run([sys.executable, "validate_content.py"])

    print("\n" + "=" * 60)
    print("Post-Phase …")
    print("=" * 60)
    run([sys.executable, "post_phase.py",
         "--phase", "328",
         "--patch", "patches/patch_328_heimvorteil_engine.py",
         "--summary",
         "ENGINE: Heimvorteil 70/30 in _mkMatchQ() — alle Match-Modi "
         "bevorzugen jetzt Einträge aus dem Heimatland des Nutzers (S.language → "
         "Ländername-Mapping, localPool, rng()<0.7). Fallback 100% global für "
         "nicht-geographische c-Felder."])
