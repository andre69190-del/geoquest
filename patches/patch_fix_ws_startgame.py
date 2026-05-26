"""
patch_fix_ws_startgame.py
==========================
Bug: startGame() only had a special early-return for ws_tiere_* modes.
     All other WS prefixes (ws_arch_*, ws_tech_*, ws_emob_*, ws_gastro_*,
     ws_pflanzen_*, ws_pferde_*) fell through to lq() which returns null
     for WS generators → S.ph="menu" → home screen shown instead of game.

Fix: Add a generic ws_* early-return AFTER the ws_tiere_ check.
     All WS GEN entries already call the right initXxxWS function and
     return null — we just call GEN[_m]() directly then render().
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

OLD = (
    '  if(_m&&_m.startsWith("ws_tiere_")){var _twk=_m.replace("ws_tiere_","");initTierWortSchmiede(_twk);render();return;}\n'
    '  lq();'
)
NEW = (
    '  if(_m&&_m.startsWith("ws_tiere_")){var _twk=_m.replace("ws_tiere_","");initTierWortSchmiede(_twk);render();return;}\n'
    '  /* Phase 234: generic WS early-return — ws_arch_* / ws_tech_* / ws_emob_* / ws_gastro_* / ws_pflanzen_* / ws_pferde_* */\n'
    '  if(_m&&_m.startsWith("ws_")&&GEN[_m]){GEN[_m]();render();return;}\n'
    '  lq();'
)

assert c.count(OLD) == 1, f"Anchor not unique: startGame WS check (found {c.count(OLD)})"
c = c.replace(OLD, NEW)
print("  [OK] startGame: generic ws_* early-return added — all WS modes now route correctly")

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("  [OK] gen.py updated")
