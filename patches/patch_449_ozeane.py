#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase: 449
Date:  2026-06-02
Scope: Ozeane & Meere — 7 neue Modi + ozeane_extended.json (80 Einträge)

Modi: hl_ozean_flaeche, hl_ozean_tiefe, ozean_match_typ,
      ozean_match_kontinent, hl_ozean_flaeche_klein,
      ozean_match_name, ws_ozean_atlantik
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, 'gen.py')
VC   = os.path.join(ROOT, 'validate_content.py')


def patch(path, edits):
    c = open(path, 'r', encoding='utf-8').read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, f'Anker "{tag}" count={n} (erwartet 1)'
        c = c.replace(old, new)
        print('  OK  ' + tag)
    open(path, 'w', encoding='utf-8').write(c)


print('\n-- 1. validate_content.py --')
c_vc = open(VC, 'r', encoding='utf-8').read()
assert 'check_ozeane_extended' in c_vc, 'check_ozeane_extended missing from VC'
print('  OK  VC: check_ozeane_extended already present')


print('\n-- 2. gen.py --')

LOAD_OLD = (
    "        KLIMA_WS_J = __import__('json').dumps(__import__('json').load(_klimwf),"
    " ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/ozeane_extended.json'), 'r', encoding='utf-8') as _ozf:\n"
    "        OZEANE_J = __import__('json').dumps(__import__('json').load(_ozf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/ozeane_ws.json'), 'r', encoding='utf-8') as _ozwf:\n"
    "        OZEANE_WS_J = __import__('json').dumps(__import__('json').load(_ozwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

JS_CONST_OLD = "const KLIMA_DATA=PLACEHOLDER_KLIMA;"
JS_CONST_NEW = (
    "const KLIMA_DATA=PLACEHOLDER_KLIMA;\n"
    "const OZEANE_WS_DATA=PLACEHOLDER_OZEANE_WS;\n"
    "const OZEANE_DATA=PLACEHOLDER_OZEANE;"
)

MKWS_OLD = 'var initKlimaWS=_mkWS(KLIMA_WS_DATA,"Klima");'
MKWS_NEW = (
    'var initKlimaWS=_mkWS(KLIMA_WS_DATA,"Klima");\n'
    'var initOzeaneWS=_mkWS(OZEANE_WS_DATA,"Ozeane");'
)

GEN_FUNCS_OLD = "window.genKlimaPinQ=genKlimaPinQ;"
GEN_FUNCS_NEW = r"""window.genKlimaPinQ=genKlimaPinQ;
function genOzeaneHLExt(field,opts){var o=opts||{};var items=[];var _OD=OZEANE_DATA;for(var k in _OD){var e=_OD[k];var v=e[field];if(v!=null){items.push({name:k,val:v,typ:e.typ||"",kontinent:e.kontinent_grenze||"",_raw:v});}}if(items.length<4)return null;items.sort(function(a,b){return b.val-a.val;});var pool=items.slice(0,40);var idx=Math.floor(Math.random()*pool.length);var chosen=pool[idx];var distractors=pool.filter(function(x){return x.name!==chosen.name;}).sort(function(){return Math.random()-0.5;}).slice(0,3);var choices=[chosen].concat(distractors).sort(function(){return Math.random()-0.5;});var prompt=o.prompt||_tc("Welches Gewässer ist größer?");return _mkHLQ(chosen,distractors,choices,prompt,o);}
function genOzeaneMatchExt(field,prompt){var _OD=OZEANE_DATA;var pool=Object.keys(_OD).map(function(k){return{name:k,val:_OD[k][field]};}).filter(function(x){return x.val!=null;});if(pool.length<4)return null;var shuffled=pool.sort(function(){return Math.random()-0.5;}).slice(0,4);var correct=shuffled[0];var choices=shuffled.map(function(x){return x.name;}).sort(function(){return Math.random()-0.5;});return {type:"match",prompt:prompt||_tc("Welcher Typ ist dieses Gewässer?"),subject:correct.val,choices:choices,answer:correct.name,explanation:correct.name+" → "+correct.val};}
window.genOzeaneHLExt=genOzeaneHLExt;
window.genOzeaneMatchExt=genOzeaneMatchExt;"""

I18N_PL_OLD = '"Welches Land ist kälter?":"Który kraj jest zimniejszy?"},"en":{"Welche Serie startete f'
I18N_PL_NEW = '"Welches Land ist kälter?":"Który kraj jest zimniejszy?","Welches Gewässer ist größer?":"Które akwen jest większy?","Welches Gewässer ist tiefer?":"Które akwen jest głębsze?","Welcher Typ ist dieses Gewässer?":"Jaki typ to akwen?","An welchem Kontinent liegt dieses Gewässer?":"Przy jakim kontynencie leży ten akwen?","Welches Gewässer ist kleiner?":"Które akwen jest mniejsze?","Wie heißt dieses Gewässer?":"Jak nazywa się ten akwen?"},"en":{"Welche Serie startete f'

I18N_EN_OLD = '"Which country is colder?"}};\nfuncti'
I18N_EN_NEW = '"Which country is colder?","Welches Gewässer ist größer?":"Which body of water is larger?","Welches Gewässer ist tiefer?":"Which body of water is deeper?","Welcher Typ ist dieses Gewässer?":"What type of water body is this?","An welchem Kontinent liegt dieses Gewässer?":"Which continent does this body of water border?","Welches Gewässer ist kleiner?":"Which body of water is smaller?","Wie heißt dieses Gewässer?":"What is this body of water called?"}};\nfuncti'

MODES_OLD = '{id:"ws_klima_monsun",icon:"\\u{1F321}\\uFE0F",title:"WS: Monsun",group:"klima",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus MONSUN!",desc:"Anagramm-R\\u00e4tsel \\u2014 6 Buchstaben",prompt_en:"Form words from MONSUN!"},'
MODES_NEW = (
    '{id:"ws_klima_monsun",icon:"\\u{1F321}\\uFE0F",title:"WS: Monsun",group:"klima",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus MONSUN!",desc:"Anagramm-R\\u00e4tsel \\u2014 6 Buchstaben",prompt_en:"Form words from MONSUN!"},\n'
    '    {id:"hl_ozean_flaeche",icon:"\\u{1F30A}",title:"Ozeane: Fl\\u00e4che",group:"ozeane",prompt:"Welches Gew\\u00e4sser ist gr\\u00f6\\u00dfer?",desc:"Fl\\u00e4che in km\\u00b2",prompt_en:"Which body of water is larger?"},\n'
    '    {id:"hl_ozean_tiefe",icon:"\\u{1F30A}",title:"Ozeane: Tiefe",group:"ozeane",prompt:"Welches Gew\\u00e4sser ist tiefer?",desc:"Maximale Tiefe vergleichen",prompt_en:"Which body of water is deeper?"},\n'
    '    {id:"ozean_match_typ",icon:"\\u{1F30A}",title:"Ozeane: Typ-Zuordnung",group:"ozeane",prompt:"Welcher Typ ist dieses Gew\\u00e4sser?",desc:"Gew\\u00e4sser \\u2192 Typ",prompt_en:"What type of water body is this?"},\n'
    '    {id:"ozean_match_kontinent",icon:"\\u{1F30A}",title:"Ozeane: Kontinent",group:"ozeane",prompt:"An welchem Kontinent liegt dieses Gew\\u00e4sser?",desc:"Gew\\u00e4sser \\u2192 Kontinent",prompt_en:"Which continent does this body of water border?"},\n'
    '    {id:"hl_ozean_flaeche_klein",icon:"\\u{1F30A}",title:"Ozeane: Kleiner?",group:"ozeane",prompt:"Welches Gew\\u00e4sser ist kleiner?",desc:"Kleinstes Gew\\u00e4sser finden",prompt_en:"Which body of water is smaller?"},\n'
    '    {id:"ozean_match_name",icon:"\\u{1F30A}",title:"Ozeane: Name-Zuordnung",group:"ozeane",prompt:"Wie hei\\u00dft dieses Gew\\u00e4sser?",desc:"Typ \\u2192 richtigen Namen finden",prompt_en:"What is this body of water called?"},\n'
    '    {id:"ws_ozean_atlantik",icon:"\\u{1F30A}",title:"WS: Atlantik",group:"ozeane",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus ATLANTIK!",desc:"Anagramm-R\\u00e4tsel \\u2014 8 Buchstaben",prompt_en:"Form words from ATLANTIK!"},'
)

CATS_OLD = 'klima:{label:"Klimazonen weltweit",icon:"\\u{1F321}\\uFE0F",modes:["klima_match_zone","klima_match_kontinent","hl_klima_temp","hl_klima_niederschlag","klima_pin_land","hl_klima_temp_diff","ws_klima_monsun"],cost:0},'
CATS_NEW = (
    'klima:{label:"Klimazonen weltweit",icon:"\\u{1F321}\\uFE0F",modes:["klima_match_zone","klima_match_kontinent","hl_klima_temp","hl_klima_niederschlag","klima_pin_land","hl_klima_temp_diff","ws_klima_monsun"],cost:0},\n'
    '  ozeane:{label:"Ozeane & Meere",icon:"\\u{1F30A}",modes:["hl_ozean_flaeche","hl_ozean_tiefe","ozean_match_typ","ozean_match_kontinent","hl_ozean_flaeche_klein","ozean_match_name","ws_ozean_atlantik"],cost:0},'
)

GEN_DISP_OLD = 'ws_klima_monsun:()=>{initKlimaWS("monsun");return null;},'
GEN_DISP_NEW = (
    'ws_klima_monsun:()=>{initKlimaWS("monsun");return null;},\n'
    '  hl_ozean_flaeche:()=>genOzeaneHLExt("flaeche_km2",{unit:"km²",prompt:_tc("Welches Gewässer ist größer?")}),\n'
    '  hl_ozean_tiefe:()=>genOzeaneHLExt("max_tiefe_m",{unit:"m",prompt:_tc("Welches Gewässer ist tiefer?")}),\n'
    '  ozean_match_typ:()=>genOzeaneMatchExt("typ",_tc("Welcher Typ ist dieses Gewässer?")),\n'
    '  ozean_match_kontinent:()=>genOzeaneMatchExt("kontinent_grenze",_tc("An welchem Kontinent liegt dieses Gewässer?")),\n'
    '  hl_ozean_flaeche_klein:()=>genOzeaneHLExt("flaeche_km2",{unit:"km²",lowerWins:true,prompt:_tc("Welches Gewässer ist kleiner?")}),\n'
    '  ozean_match_name:()=>genOzeaneMatchExt("typ",_tc("Wie heißt dieses Gewässer?")),\n'
    '  ws_ozean_atlantik:()=>{initOzeaneWS("atlantik");return null;},'
)

REP_OLD = ".replace('PLACEHOLDER_KLIMA',          KLIMA_J)"
REP_NEW = (
    ".replace('PLACEHOLDER_KLIMA',          KLIMA_J)\n"
    "  .replace('PLACEHOLDER_OZEANE_WS',      OZEANE_WS_J)\n"
    "  .replace('PLACEHOLDER_OZEANE',         OZEANE_J)"
)

patch(GEN, [
    (LOAD_OLD,       LOAD_NEW,       'GEN: Python Loader'),
    (JS_CONST_OLD,   JS_CONST_NEW,   'GEN: JS Constants'),
    (MKWS_OLD,       MKWS_NEW,       'GEN: _mkWS init'),
    (GEN_FUNCS_OLD,  GEN_FUNCS_NEW,  'GEN: Generator functions'),
    (I18N_PL_OLD,    I18N_PL_NEW,    'GEN: i18n PL'),
    (I18N_EN_OLD,    I18N_EN_NEW,    'GEN: i18n EN'),
    (MODES_OLD,      MODES_NEW,      'GEN: MODES array'),
    (CATS_OLD,       CATS_NEW,       'GEN: MODE_CATS'),
    (GEN_DISP_OLD,   GEN_DISP_NEW,   'GEN: GEN dispatch'),
    (REP_OLD,        REP_NEW,        'GEN: Replace chain'),
])

print('\nPatch 449 fertig.')
