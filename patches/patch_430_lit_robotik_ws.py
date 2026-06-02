#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 430: Wort-Schmiede-Modi für Literatur & Robotik/KI.

Ergänzt die bereits in gen.py integrierten Kategorien `literatur` und `robotik`
um je einen Wort-Schmiede-Modus:
  - ws_lit_protagonist  → Wort: TINTENHERZ  (Cornelia Funke)
  - ws_robot_name       → Wort: MASCHINENLERNEN (Machine Learning)

Neue Dateien: data/literatur_ws.json, data/robotik_ws.json
Zero-Bug-Policy: assert count==1 vor jedem replace.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, 'gen.py')


def patch_file(path, edits, label):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, f'[{label}] Anker "{tag}" count={n} (erwartet 1)'
        c = c.replace(old, new)
        print(f'  OK  {label}: {tag}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)


# ─────────────────────────────────────────────────────────────────────────────
# 1) Python-Daten laden (nach robotik_extended)
# ─────────────────────────────────────────────────────────────────────────────
LOAD_OLD = (
    "    with open(os.path.join(os.path.dirname(__file__), 'data/robotik_extended.json'), 'r', encoding='utf-8') as _rf:\n"
    "        ROBOT_J = __import__('json').dumps(__import__('json').load(_rf), ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = LOAD_OLD + """
    with open(os.path.join(os.path.dirname(__file__), 'data/literatur_ws.json'), 'r', encoding='utf-8') as _lwf:
        LIT_WS_J = __import__('json').dumps(__import__('json').load(_lwf), ensure_ascii=False, separators=(',',':'))
    with open(os.path.join(os.path.dirname(__file__), 'data/robotik_ws.json'), 'r', encoding='utf-8') as _rwf:
        ROBOT_WS_J = __import__('json').dumps(__import__('json').load(_rwf), ensure_ascii=False, separators=(',',':'))"""

# ─────────────────────────────────────────────────────────────────────────────
# 2) JS-Konstanten (nach ROBOT_DATA)
# ─────────────────────────────────────────────────────────────────────────────
CONST_OLD = "const LIT_DATA=PLACEHOLDER_LIT;\nconst ROBOT_DATA=PLACEHOLDER_ROBOT;"
CONST_NEW = (
    "const LIT_DATA=PLACEHOLDER_LIT;\n"
    "const ROBOT_DATA=PLACEHOLDER_ROBOT;\n"
    "const LIT_WS_DATA=PLACEHOLDER_LIT_WS;\n"
    "const ROBOT_WS_DATA=PLACEHOLDER_ROBOT_WS;"
)

# ─────────────────────────────────────────────────────────────────────────────
# 3) _mkWS Initialisierung (nach initGastroWS)
# ─────────────────────────────────────────────────────────────────────────────
MKWS_OLD = "var initGastroWS=_mkWS(GASTRO_WS_DATA,\"Gastro\");"
MKWS_NEW = (
    "var initGastroWS=_mkWS(GASTRO_WS_DATA,\"Gastro\");\n"
    "var initLitWS=_mkWS(LIT_WS_DATA,\"Lit\");\n"
    "var initRobotWS=_mkWS(ROBOT_WS_DATA,\"Robot\");"
)

# ─────────────────────────────────────────────────────────────────────────────
# 4) MODES-Einträge (nach timeline_lit_release und nach timeline_robot_jahr)
# ─────────────────────────────────────────────────────────────────────────────
LIT_MODES_OLD = (
    '    {id:"timeline_lit_release",icon:"\\u{1F4DA}",title:"Literatur-Timeline",'
    'group:"literatur",prompt:"Welches Werk erschien zuerst?",desc:"Von Hamlet bis Demon Slayer \\u2014 Literaturgeschichte sortieren."'
    ',prompt_en:"Which work came first?"},'
)
LIT_MODES_NEW = LIT_MODES_OLD + """
    {id:"ws_lit_protagonist",icon:"\\u270F\\uFE0F",title:"WS: Tintenherz",group:"literatur",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus TINTENHERZ!",desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben",prompt_en:"Form words from TINTENHERZ!"},"""

ROBOT_MODES_OLD = (
    '    {id:"timeline_robot_jahr",icon:"\\u{1F916}",title:"KI/Robotik-Timeline",'
    'group:"robotik",prompt:"Welcher Meilenstein kam zuerst?",desc:"ENIAC bis ChatGPT \\u2014 die Geschichte der KI."'
    ',prompt_en:"Which milestone came first?"},'
)
ROBOT_MODES_NEW = ROBOT_MODES_OLD + """
    {id:"ws_robot_name",icon:"\\u{1F9E0}",title:"WS: Maschinenlernen",group:"robotik",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus MASCHINENLERNEN!",desc:"Anagramm-R\\u00e4tsel \\u2014 15 Buchstaben",prompt_en:"Form words from MASCHINENLERNEN!"},"""

# ─────────────────────────────────────────────────────────────────────────────
# 5) MODE_CATS — literatur + robotik modes-Listen erweitern
# ─────────────────────────────────────────────────────────────────────────────
CATS_LIT_OLD = (
    'literatur:{label:"Literatur \\u0026 Comics",icon:"\\u{1F4DA}",'
    'modes:["hl_lit_sales","hl_lit_release","lit_match_autor","lit_match_land","lit_match_protagonist","timeline_lit_release"],cost:0},'
)
CATS_LIT_NEW = (
    'literatur:{label:"Literatur \\u0026 Comics",icon:"\\u{1F4DA}",'
    'modes:["hl_lit_sales","hl_lit_release","lit_match_autor","lit_match_land","lit_match_protagonist","timeline_lit_release","ws_lit_protagonist"],cost:0},'
)

CATS_ROBOT_OLD = (
    'robotik:{label:"KI, Robotik \\u0026 Hardware",icon:"\\u{1F916}",'
    'modes:["hl_robot_jahr","robot_match_kategorie","robot_match_land","robot_match_entwickler","robot_match_fakt","timeline_robot_jahr"],cost:0},'
)
CATS_ROBOT_NEW = (
    'robotik:{label:"KI, Robotik \\u0026 Hardware",icon:"\\u{1F916}",'
    'modes:["hl_robot_jahr","robot_match_kategorie","robot_match_land","robot_match_entwickler","robot_match_fakt","timeline_robot_jahr","ws_robot_name"],cost:0},'
)

# ─────────────────────────────────────────────────────────────────────────────
# 6) GEN-Dispatch (nach timeline_lit_release und timeline_robot_jahr)
# ─────────────────────────────────────────────────────────────────────────────
DISPATCH_LIT_OLD = "  timeline_lit_release:()=>genTimelineQ(\"lit_release\"),"
DISPATCH_LIT_NEW = (
    "  timeline_lit_release:()=>genTimelineQ(\"lit_release\"),\n"
    "  ws_lit_protagonist:()=>{initLitWS(\"tintenherz\");return null;},"
)

DISPATCH_ROBOT_OLD = "  timeline_robot_jahr:()=>genTimelineQ(\"robot_jahr\"),"
DISPATCH_ROBOT_NEW = (
    "  timeline_robot_jahr:()=>genTimelineQ(\"robot_jahr\"),\n"
    "  ws_robot_name:()=>{initRobotWS(\"maschinenlernen\");return null;},"
)

# ─────────────────────────────────────────────────────────────────────────────
# 7) Placeholder-Replace-Kette (spezifischste zuerst! _WS vor Basis)
# ─────────────────────────────────────────────────────────────────────────────
REPL_OLD = (
    "  .replace('PLACEHOLDER_LIT',            LIT_J)\n"
    "  .replace('PLACEHOLDER_ROBOT',          ROBOT_J)"
)
REPL_NEW = (
    "  .replace('PLACEHOLDER_LIT_WS',         LIT_WS_J)\n"
    "  .replace('PLACEHOLDER_LIT',            LIT_J)\n"
    "  .replace('PLACEHOLDER_ROBOT_WS',       ROBOT_WS_J)\n"
    "  .replace('PLACEHOLDER_ROBOT',          ROBOT_J)"
)


edits_gen = [
    (LOAD_OLD,         LOAD_NEW,         "Python: LIT_WS_J + ROBOT_WS_J laden"),
    (CONST_OLD,        CONST_NEW,        "JS: LIT_WS_DATA + ROBOT_WS_DATA Konstanten"),
    (MKWS_OLD,         MKWS_NEW,         "JS: initLitWS + initRobotWS via _mkWS"),
    (LIT_MODES_OLD,    LIT_MODES_NEW,    "MODES: ws_lit_protagonist"),
    (ROBOT_MODES_OLD,  ROBOT_MODES_NEW,  "MODES: ws_robot_name"),
    (CATS_LIT_OLD,     CATS_LIT_NEW,     "MODE_CATS: literatur +ws_lit_protagonist"),
    (CATS_ROBOT_OLD,   CATS_ROBOT_NEW,   "MODE_CATS: robotik +ws_robot_name"),
    (DISPATCH_LIT_OLD, DISPATCH_LIT_NEW, "Dispatch: ws_lit_protagonist"),
    (DISPATCH_ROBOT_OLD, DISPATCH_ROBOT_NEW, "Dispatch: ws_robot_name"),
    (REPL_OLD,         REPL_NEW,         "Replace-Kette: LIT_WS + ROBOT_WS"),
]

print("=== patch_430_lit_robotik_ws.py ===")
patch_file(GEN, edits_gen, "gen.py")
print("\nPatch abgeschlossen. Jetzt: python3 gen.py && python3 verify.py && python3 validate_content.py")
