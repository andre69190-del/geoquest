# -*- coding: utf-8 -*-
"""
Phase: 403
Date:  2026-06-01
Author: Claude / Andre
Scope: Audit-Polish: JSON-Parser try/except + Prototype-Pollution hasOwnProperty-Guard

Description:
  Schließt die letzten beiden offenen Findings aus dem Phase-400-Audit:
  1. JSON-Parser Robustheit (Python Build-Time):
     - autos_extended.json und games_extended.json Ladeprozesse werden in
       try/except json.JSONDecodeError gewickelt.
     - Bei Fehler: sauberes SystemExit mit Dateiname und Fehlermeldung.
  2. Prototype-Pollution-Schutz (JavaScript Run-Time):
     - Object.keys(_GE) und Object.keys(_AE) in allen Extended-Generatoren
       werden um hasOwnProperty-Filter ergaenzt.
     - Schuetzt gegen manipulierte Keys wie __proto__, constructor etc.
  WontFix: Lazy-Init fuer Extended-Daten (Lead Architect abgelehnt).

Dependencies: patch_402 (games_extended.json vorhanden)
Zero-Bug Policy: assert c.count(old)==1 vor jedem c.replace()
"""

import os
import re

HERE   = os.path.dirname(os.path.abspath(__file__))
GEN_PY = os.path.join(HERE, '..', 'gen.py')

with open(GEN_PY, 'r', encoding='utf-8') as f:
    c = f.read()

changes = []

# ─────────────────────────────────────────────────────────────────────────────
# FIX 1: JSON-Parser Robustheit — autos_extended.json
# ─────────────────────────────────────────────────────────────────────────────
old_autos = (
    "with open(os.path.join(os.path.dirname(__file__), 'data/autos_extended.json'), "
    "'r', encoding='utf-8') as _f:\n"
    "    import json as _ejson\n"
    "    AUTOS_EXT_J  = _ejson.dumps(_ejson.load(_f), ensure_ascii=False, separators=(',',':'))"
)
new_autos = (
    "try:\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/autos_extended.json'), "
    "'r', encoding='utf-8') as _f:\n"
    "        import json as _ejson\n"
    "        AUTOS_EXT_J = _ejson.dumps(_ejson.load(_f), ensure_ascii=False, separators=(',',':'))\n"
    "except json.JSONDecodeError as _e:\n"
    "    raise SystemExit(f'[FATAL] JSON Decode Error in autos_extended.json: {_e}')\n"
    "except FileNotFoundError:\n"
    "    raise SystemExit('[FATAL] data/autos_extended.json nicht gefunden')"
)
assert c.count(old_autos) == 1, f"Anker autos_extended nicht eindeutig: {c.count(old_autos)}x"
c = c.replace(old_autos, new_autos, 1)
changes.append("JSON try/except: autos_extended.json")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 2: JSON-Parser Robustheit — games_extended.json
# ─────────────────────────────────────────────────────────────────────────────
old_games = (
    "with open(os.path.join(os.path.dirname(__file__), 'data/games_extended.json'), "
    "'r', encoding='utf-8') as _gf:\n"
    "    GAMES_EXT_J  = __import__('json').dumps(__import__('json').load(_gf), "
    "ensure_ascii=False, separators=(',',':'))"
)
new_games = (
    "try:\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/games_extended.json'), "
    "'r', encoding='utf-8') as _gf:\n"
    "        GAMES_EXT_J = __import__('json').dumps(__import__('json').load(_gf), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "except __import__('json').JSONDecodeError as _ge:\n"
    "    raise SystemExit(f'[FATAL] JSON Decode Error in games_extended.json: {_ge}')\n"
    "except FileNotFoundError:\n"
    "    raise SystemExit('[FATAL] data/games_extended.json nicht gefunden')"
)
assert c.count(old_games) == 1, f"Anker games_extended nicht eindeutig: {c.count(old_games)}x"
c = c.replace(old_games, new_games, 1)
changes.append("JSON try/except: games_extended.json")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 3: Prototype-Pollution-Guard — Object.keys(_GE) in genGamesHLExt
# ─────────────────────────────────────────────────────────────────────────────
# genGamesHLExt: var _ks=Object.keys(_GE);
old_gkeys = "  var _ks=Object.keys(_GE);"
new_gkeys = "  var _ks=Object.keys(_GE).filter(function(k){return Object.prototype.hasOwnProperty.call(_GE,k)});"
assert c.count(old_gkeys) == 1, f"Anker Object.keys(_GE) HL nicht eindeutig: {c.count(old_gkeys)}x"
c = c.replace(old_gkeys, new_gkeys, 1)
changes.append("Prototype-Guard: Object.keys(_GE) in genGamesHLExt")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 4: Prototype-Pollution-Guard — Object.keys(_GE) in genGamesMatchExt
# ─────────────────────────────────────────────────────────────────────────────
# genGamesMatchExt: var valid=Object.keys(_GE).filter(...)  [first occurrence]
old_gmatch = "  var valid=Object.keys(_GE).filter(function(n){\n    var v=_GE[n][field];\n    return v!==null&&v!==undefined&&v!==\"\";"
new_gmatch = "  var valid=Object.keys(_GE).filter(function(k){return Object.prototype.hasOwnProperty.call(_GE,k)}).filter(function(n){\n    var v=_GE[n][field];\n    return v!==null&&v!==undefined&&v!==\"\";"
assert c.count(old_gmatch) == 1, f"Anker Object.keys(_GE) Match nicht eindeutig: {c.count(old_gmatch)}x"
c = c.replace(old_gmatch, new_gmatch, 1)
changes.append("Prototype-Guard: Object.keys(_GE) in genGamesMatchExt")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 5: Prototype-Pollution-Guard — Object.keys(_GE) in genGamesPinQ + genGamesBaujahrMC
# ─────────────────────────────────────────────────────────────────────────────
# genGamesPinQ: var valid=Object.keys(_GE).filter(...)
old_gpin = "  var valid=Object.keys(_GE).filter(function(n){\n    var d=_GE[n];"
new_gpin = "  var valid=Object.keys(_GE).filter(function(k){return Object.prototype.hasOwnProperty.call(_GE,k)}).filter(function(n){\n    var d=_GE[n];"
assert c.count(old_gpin) == 1, f"Anker Object.keys(_GE) Pin nicht eindeutig: {c.count(old_gpin)}x"
c = c.replace(old_gpin, new_gpin, 1)
changes.append("Prototype-Guard: Object.keys(_GE) in genGamesPinQ")

# genGamesBaujahrMC + genGamesF2PQ: beide nutzen var keys=Object.keys(_GE);
# Spezifische Anker mit Kontext-Zeile davor
old_gbj = "function genGamesBaujahrMC(){\n  var _GE=GAMES_EXT_DATA;\n  var keys=Object.keys(_GE);"
new_gbj = "function genGamesBaujahrMC(){\n  var _GE=GAMES_EXT_DATA;\n  var keys=Object.keys(_GE).filter(function(k){return Object.prototype.hasOwnProperty.call(_GE,k)});"
assert c.count(old_gbj) == 1, f"Anker genGamesBaujahrMC nicht eindeutig: {c.count(old_gbj)}x"
c = c.replace(old_gbj, new_gbj, 1)
changes.append("Prototype-Guard: Object.keys(_GE) in genGamesBaujahrMC")

old_gf2p = "function genGamesF2PQ(){\n  var _GE=GAMES_EXT_DATA;\n  var keys=Object.keys(_GE);"
new_gf2p = "function genGamesF2PQ(){\n  var _GE=GAMES_EXT_DATA;\n  var keys=Object.keys(_GE).filter(function(k){return Object.prototype.hasOwnProperty.call(_GE,k)});"
assert c.count(old_gf2p) == 1, f"Anker genGamesF2PQ nicht eindeutig: {c.count(old_gf2p)}x"
c = c.replace(old_gf2p, new_gf2p, 1)
changes.append("Prototype-Guard: Object.keys(_GE) in genGamesF2PQ")

# ─────────────────────────────────────────────────────────────────────────────
# FIX 6: Prototype-Pollution-Guard — Object.keys(_AE) in genAutosHLExt + variants
# ─────────────────────────────────────────────────────────────────────────────
# genAutosHLExt: var _ks=Object.keys(_AE);
old_akeys = "  var _ks=Object.keys(_AE);"
new_akeys = "  var _ks=Object.keys(_AE).filter(function(k){return Object.prototype.hasOwnProperty.call(_AE,k)});"
assert c.count(old_akeys) == 1, f"Anker Object.keys(_AE) HL nicht eindeutig: {c.count(old_akeys)}x"
c = c.replace(old_akeys, new_akeys, 1)
changes.append("Prototype-Guard: Object.keys(_AE) in genAutosHLExt")

# Object.keys(_AE).forEach — genAutoPsKg + genAutoCO2
old_foreach = "  Object.keys(_AE).forEach(function(n){"
new_foreach = "  Object.keys(_AE).filter(function(k){return Object.prototype.hasOwnProperty.call(_AE,k)}).forEach(function(n){"
cnt = c.count(old_foreach)
assert cnt == 2, f"Anker Object.keys(_AE).forEach nicht 2x: {cnt}x"
c = c.replace(old_foreach, new_foreach)  # beide ersetzen
changes.append(f"Prototype-Guard: Object.keys(_AE).forEach (2x: genAutoPsKg + genAutoCO2)")

# genAutosMatchExt: var valid=Object.keys(_AE).filter
old_amatch = "  var valid=Object.keys(_AE).filter(function(n){"
new_amatch = "  var valid=Object.keys(_AE).filter(function(k){return Object.prototype.hasOwnProperty.call(_AE,k)}).filter(function(n){"
assert c.count(old_amatch) == 1, f"Anker Object.keys(_AE) Match nicht eindeutig: {c.count(old_amatch)}x"
c = c.replace(old_amatch, new_amatch, 1)
changes.append("Prototype-Guard: Object.keys(_AE) in genAutosMatchExt")

# ──────────────────────────────────────────────────────────────────────────�