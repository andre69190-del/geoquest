#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase: 448
Date:  2026-06-02
Scope: Klimazonen & Länder — 7 neue Modi + klima_extended.json (80 Einträge)

Modi: klima_match_zone, klima_match_kontinent, hl_klima_temp,
      hl_klima_niederschlag, klima_pin_land, hl_klima_temp_diff,
      ws_klima_monsun
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
assert 'check_klima_extended' in c_vc, 'check_klima_extended missing from VC'
print('  OK  VC: check_klima_extended already present')


print('\n-- 2. gen.py --')

LOAD_OLD = (
    "        GIPFEL_WS_J = __import__('json').dumps(__import__('json').load(_gipwf),"
    " ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/klima_extended.json'), 'r', encoding='utf-8') as _klimf:\n"
    "        KLIMA_J = __import__('json').dumps(__import__('json').load(_klimf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/klima_ws.json'), 'r', encoding='utf-8') as _klimwf:\n"
    "        KLIMA_WS_J = __import__('json').dumps(__import__('json').load(_klimwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

JS_CONST_OLD = "const GIPFEL_DATA=PLACEHOLDER_GIPFEL;"
JS_CONST_NEW = (
    "const GIPFEL_DATA=PLACEHOLDER_GIPFEL;\n"
    "const KLIMA_WS_DATA=PLACEHOLDER_KLIMA_WS;\n"
    "const KLIMA_DATA=PLACEHOLDER_KLIMA;"
)

MKWS_OLD = 'var initGipfelWS=_mkWS(GIPFEL_WS_DATA,"Gipfel");'
MKWS_NEW = (
    'var initGipfelWS=_mkWS(GIPFEL_WS_DATA,"Gipfel");\n'
    'var initKlimaWS=_mkWS(KLIMA_WS_DATA,"Klima");'
)

GEN_FUNCS_OLD = "window.genGipfelTimelineQ=genGipfelTimelineQ;"
GEN_FUNCS_NEW = r"""window.genGipfelTimelineQ=genGipfelTimelineQ;
function genKlimaHLExt(field,opts){var o=opts||{};var items=[];var _KD=KLIMA_DATA;for(var k in _KD){var e=_KD[k];var v=e[field];if(v!=null){items.push({name:k,val:v,klimazone:e.klimazone||"",kontinent:e.kontinent||"",_raw:v});}}if(items.length<4)return null;items.sort(function(a,b){return b.val-a.val;});var pool=items.slice(0,40);var idx=Math.floor(Math.random()*pool.length);var chosen=pool[idx];var distractors=pool.filter(function(x){return x.name!==chosen.name;}).sort(function(){return Math.random()-0.5;}).slice(0,3);var choices=[chosen].concat(distractors).sort(function(){return Math.random()-0.5;});var prompt=o.prompt||_tc("Welches Land ist wärmer?");return _mkHLQ(chosen,distractors,choices,prompt,o);}
function genKlimaMatchExt(field,prompt){var _KD=KLIMA_DATA;var pool=Object.keys(_KD).map(function(k){return{name:k,val:_KD[k][field]};}).filter(function(x){return x.val!=null;});if(pool.length<4)return null;var shuffled=pool.sort(function(){return Math.random()-0.5;}).slice(0,4);var correct=shuffled[0];var choices=shuffled.map(function(x){return x.name;}).sort(function(){return Math.random()-0.5;});return {type:"match",prompt:prompt||_tc("Welche Klimazone hat dieses Land?"),subject:correct.val,choices:choices,answer:correct.name,explanation:correct.name+" → "+correct.val};}
function genKlimaPinQ(){var _KD=KLIMA_DATA;var keys=Object.keys(_KD);if(keys.length<1)return null;var k=keys[Math.floor(Math.random()*keys.length)];var e=_KD[k];var LL=window.LAND_LATLON||{};var coords=LL[k];if(!coords)return null;return {type:"pin",prompt:_tc("Wo liegt dieses Land (Klimazone: "+e.klimazone+")?"),subject:k,lat:coords[0],lng:coords[1],explanation:k+" ("+e.klimazone+")",radius:600};}
window.genKlimaHLExt=genKlimaHLExt;
window.genKlimaMatchExt=genKlimaMatchExt;
window.genKlimaPinQ=genKlimaPinQ;"""

I18N_PL_OLD = '"Sortiere diese Gipfel nach Erstbesteigung (älteste zuerst)!":"Posortuj te szczyty według pierwszego wejścia (od najstarszego)!"},"en":{"Welche Serie startete f'
I18N_PL_NEW = '"Sortiere diese Gipfel nach Erstbesteigung (älteste zuerst)!":"Posortuj te szczyty według pierwszego wejścia (od najstarszego)!","Welches Land ist wärmer?":"Który kraj jest cieplejszy?","Welches Land hat mehr Niederschlag?":"Który kraj ma więcej opadów?","Welche Klimazone hat dieses Land?":"Jaką strefę klimatyczną ma ten kraj?","Auf welchem Kontinent liegt dieses Land?":"Na jakim kontynencie leży ten kraj?","Wo liegt dieses Land (Klimazone: ":"Gdzie leży ten kraj (strefa klimatyczna: ","Welches Land ist kälter?":"Który kraj jest zimniejszy?"},"en":{"Welche Serie startete f'

I18N_EN_OLD = '"Sort these peaks by first ascent (oldest first)!"}};\nfuncti'
I18N_EN_NEW = '"Sort these peaks by first ascent (oldest first)!","Welches Land ist wärmer?":"Which country is warmer?","Welches Land hat mehr Niederschlag?":"Which country has more rainfall?","Welche Klimazone hat dieses Land?":"Which climate zone does this country have?","Auf welchem Kontinent liegt dieses Land?":"On which continent is this country?","Wo liegt dieses Land (Klimazone: ":"Where is this country (climate zone: ","Welches Land ist kälter?":"Which country is colder?"}};\nfuncti'

MODES_OLD = '{id:"ws_gipfel_himalaya",icon:"\\u26F0\\uFE0F",title:"WS: Himalaya",group:"gipfel",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus HIMALAYA!",desc:"Anagramm-R\\u00e4tsel \\u2014 8 Buchstaben",prompt_en:"Form words from HIMALAYA!"},'
MODES_NEW = (
    '{id:"ws_gipfel_himalaya",icon:"\\u26F0\\uFE0F",title:"WS: Himalaya",group:"gipfel",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus HIMALAYA!",desc:"Anagramm-R\\u00e4tsel \\u2014 8 Buchstaben",prompt_en:"Form words from HIMALAYA!"},\n'
    '    {id:"klima_match_zone",icon:"\\u{1F321}\\uFE0F",title:"Klima: Zone zuordnen",group:"klima",prompt:"Welche Klimazone hat dieses Land?",desc:"Land \\u2192 Klimazone",prompt_en:"Which climate zone does this country have?"},\n'
    '    {id:"klima_match_kontinent",icon:"\\u{1F321}\\uFE0F",title:"Klima: Kontinent",group:"klima",prompt:"Auf welchem Kontinent liegt dieses Land?",desc:"Land \\u2192 Kontinent",prompt_en:"On which continent is this country?"},\n'
    '    {id:"hl_klima_temp",icon:"\\u{1F321}\\uFE0F",title:"Klima: W\\u00e4rmer?",group:"klima",prompt:"Welches Land ist w\\u00e4rmer?",desc:"Durchschnittstemperatur vergleichen",prompt_en:"Which country is warmer?"},\n'
    '    {id:"hl_klima_niederschlag",icon:"\\u{1F321}\\uFE0F",title:"Klima: Mehr Niederschlag?",group:"klima",prompt:"Welches Land hat mehr Niederschlag?",desc:"Jahresniederschlag vergleichen",prompt_en:"Which country has more rainfall?"},\n'
    '    {id:"klima_pin_land",icon:"\\u{1F321}\\uFE0F",title:"Klima: Land auf der Karte",group:"klima",prompt:"Wo liegt dieses Land?",desc:"Pin auf der Weltkarte",prompt_en:"Where is this country located?"},\n'
    '    {id:"hl_klima_temp_diff",icon:"\\u{1F321}\\uFE0F",title:"Klima: K\\u00e4lter?",group:"klima",prompt:"Welches Land ist k\\u00e4lter?",desc:"K\\u00e4ltestes Land finden",prompt_en:"Which country is colder?"},\n'
    '    {id:"ws_klima_monsun",icon:"\\u{1F321}\\uFE0F",title:"WS: Monsun",group:"klima",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus MONSUN!",desc:"Anagramm-R\\u00e4tsel \\u2014 6 Buchstaben",prompt_en:"Form words from MONSUN!"},'
)

CATS_OLD = 'gipfel:{label:"Gipfel & Berge",icon:"\\u26F0\\uFE0F",modes:["hl_gipfel_hoehe","gipfel_match_gebirge","gipfel_match_kontinent","gipfel_pin_lage","hl_gipfel_erstbesteigung","timeline_gipfel_besteigung","ws_gipfel_himalaya"],cost:0},'
CATS_NEW = (
    'gipfel:{label:"Gipfel & Berge",icon:"\\u26F0\\uFE0F",modes:["hl_gipfel_hoehe","gipfel_match_gebirge","gipfel_match_kontinent","gipfel_pin_lage","hl_gipfel_erstbesteigung","timeline_gipfel_besteigung","ws_gipfel_himalaya"],cost:0},\n'
    '  klima:{label:"Klimazonen weltweit",icon:"\\u{1F321}\\uFE0F",modes:["klima_match_zone","klima_match_kontinent","hl_klima_temp","hl_klima_niederschlag","klima_pin_land","hl_klima_temp_diff","ws_klima_monsun"],cost:0},'
)

GEN_DISP_OLD = 'ws_gipfel_himalaya:()=>{initGipfelWS("himalaya");return null;},'
GEN_DISP_NEW = (
    'ws_gipfel_himalaya:()=>{initGipfelWS("himalaya");return null;},\n'
    '  klima_match_zone:()=>genKlimaMatchExt("klimazone",_tc("Welche Klimazone hat dieses Land?")),\n'
    '  klima_match_kontinent:()=>genKlimaMatchExt("kontinent",_tc("Auf welchem Kontinent liegt dieses Land?")),\n'
    '  hl_klima_temp:()=>genKlimaHLExt("durchschnitt_temp_c",{unit:"°C",prompt:_tc("Welches Land ist wärmer?")}),\n'
    '  hl_klima_niederschlag:()=>genKlimaHLExt("jahresniederschlag_mm",{unit:"mm",prompt:_tc("Welches Land hat mehr Niederschlag?")}),\n'
    '  klima_pin_land:()=>genKlimaPinQ(),\n'
    '  hl_klima_temp_diff:()=>genKlimaHLExt("durchschnitt_temp_c",{unit:"°C",lowerWins:true,prompt:_tc("Welches Land ist kälter?")}),\n'
    '  ws_klima_monsun:()=>{initKlimaWS("monsun");return null;},'
)

REP_OLD = ".replace('PLACEHOLDER_GIPFEL',         GIPFEL_J)"
REP_NEW = (
    ".replace('PLACEHOLDER_GIPFEL',         GIPFEL_J)\n"
    "  .replace('PLACEHOLDER_KLIMA_WS',       KLIMA_WS_J)\n"
    "  .replace('PLACEHOLDER_KLIMA',          KLIMA_J)"
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

print('\nPatch 448 fertig.')
