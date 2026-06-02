#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase: 446
Date:  2026-06-02
Scope: Inseln weltweit — 7 neue Modi + inseln_extended.json (80 Einträge)

Modi: hl_insel_flaeche, hl_insel_einwohner, insel_match_ozean,
      insel_match_kontinent, insel_pin_lage, hl_insel_aequator,
      ws_insel_groenland
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
assert 'check_inseln_extended' in c_vc, 'check_inseln_extended missing from VC'
print('  OK  VC: check_inseln_extended already present')


print('\n-- 2. gen.py --')

LOAD_OLD = (
    "        CAPITALS_WS_J = __import__('json').dumps(__import__('json').load(_capwf),"
    " ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/inseln_extended.json'), 'r', encoding='utf-8') as _iself:\n"
    "        INSELN_J = __import__('json').dumps(__import__('json').load(_iself),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/inseln_ws.json'), 'r', encoding='utf-8') as _inswf:\n"
    "        INSELN_WS_J = __import__('json').dumps(__import__('json').load(_inswf),"
    " ensure_ascii=False, separators=(',',':'))"
)

JS_CONST_OLD = "const CAPITALS_DATA=PLACEHOLDER_CAPITALS;"
JS_CONST_NEW = (
    "const CAPITALS_DATA=PLACEHOLDER_CAPITALS;\n"
    "const INSELN_WS_DATA=PLACEHOLDER_INSELN_WS;\n"
    "const INSELN_DATA=PLACEHOLDER_INSELN;"
)

MKWS_OLD = 'var initCapitalsWS=_mkWS(CAPITALS_WS_DATA,"Capitals");'
MKWS_NEW = (
    'var initCapitalsWS=_mkWS(CAPITALS_WS_DATA,"Capitals");\n'
    'var initInselnWS=_mkWS(INSELN_WS_DATA,"Inseln");'
)

GEN_FUNCS_OLD = "window.genCapitalsPinQ=genCapitalsPinQ;"
GEN_FUNCS_NEW = r"""window.genCapitalsPinQ=genCapitalsPinQ;
function genInselnHLExt(field,opts){var o=opts||{};var items=[];var _ID=INSELN_DATA;for(var k in _ID){var e=_ID[k];var v=e[field];if(v!=null){if(o.absVal)v=Math.abs(v);items.push({name:k,val:v,land:e.land||"",kontinent:e.kontinent||"",_raw:e[field]});}}if(items.length<4)return null;items.sort(function(a,b){return b.val-a.val;});var pool=items.slice(0,40);var idx=Math.floor(Math.random()*pool.length);var chosen=pool[idx];var distractors=pool.filter(function(x){return x.name!==chosen.name;}).sort(function(){return Math.random()-0.5;}).slice(0,3);var choices=[chosen].concat(distractors).sort(function(){return Math.random()-0.5;});var prompt=o.prompt||_tc("Welche Insel ist größer?");return _mkHLQ(chosen,distractors,choices,prompt,o);}
function genInselnMatchExt(field,prompt){var _ID=INSELN_DATA;var pool=Object.keys(_ID).map(function(k){return{name:k,val:_ID[k][field]};}).filter(function(x){return x.val!=null;});if(pool.length<4)return null;var shuffled=pool.sort(function(){return Math.random()-0.5;}).slice(0,4);var correct=shuffled[0];var choices=shuffled.map(function(x){return x.name;}).sort(function(){return Math.random()-0.5;});return {type:"match",prompt:prompt||_tc("Zu welchem Ozean gehört diese Insel?"),subject:correct.val,choices:choices,answer:correct.name,explanation:correct.name+" → "+correct.val};}
function genInselnPinQ(){var _ID=INSELN_DATA;var keys=Object.keys(_ID).filter(function(k){return _ID[k].lat!=null&&_ID[k].lng!=null;});if(keys.length<1)return null;var k=keys[Math.floor(Math.random()*keys.length)];var e=_ID[k];return {type:"pin",prompt:_tc("Wo liegt diese Insel?"),subject:k,lat:e.lat,lng:e.lng,explanation:k+" ("+e.kontinent+")",radius:500};}
window.genInselnHLExt=genInselnHLExt;
window.genInselnMatchExt=genInselnMatchExt;
window.genInselnPinQ=genInselnPinQ;"""

I18N_PL_OLD = '"Welche Hauptstadt ist weiter vom Äquator entfernt?":"Która stolica jest dalej od równika?"},"en":{"Welche Serie startete fr'
I18N_PL_NEW = '"Welche Hauptstadt ist weiter vom Äquator entfernt?":"Która stolica jest dalej od równika?","Welche Insel ist größer?":"Która wyspa jest większa?","Welche Insel hat mehr Einwohner?":"Która wyspa ma więcej mieszkańców?","Zu welchem Ozean gehört diese Insel?":"Do jakiego oceanu należy ta wyspa?","Auf welchem Kontinent liegt diese Insel?":"Na jakim kontynencie leży ta wyspa?","Wo liegt diese Insel?":"Gdzie leży ta wyspa?","Welche Insel liegt weiter vom Äquator entfernt?":"Która wyspa jest dalej od równika?"},"en":{"Welche Serie startete fr'

I18N_EN_OLD = '"Which capital is farther from the equator?"}};\nfuncti'
I18N_EN_NEW = '"Which capital is farther from the equator?","Welche Insel ist größer?":"Which island is larger?","Welche Insel hat mehr Einwohner?":"Which island has more inhabitants?","Zu welchem Ozean gehört diese Insel?":"Which ocean does this island belong to?","Auf welchem Kontinent liegt diese Insel?":"On which continent is this island?","Wo liegt diese Insel?":"Where is this island located?","Welche Insel liegt weiter vom Äquator entfernt?":"Which island is farther from the equator?"}};\nfuncti'

MODES_OLD = '{id:"ws_capital_reykjavik",icon:"\\u{1F3D9}\\uFE0F",title:"WS: Reykjavik",group:"capitals",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus REYKJAVIK!",desc:"Anagramm-R\\u00e4tsel \\u2014 9 Buchstaben",prompt_en:"Form words from REYKJAVIK!"},'
MODES_NEW = (
    '{id:"ws_capital_reykjavik",icon:"\\u{1F3D9}\\uFE0F",title:"WS: Reykjavik",group:"capitals",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus REYKJAVIK!",desc:"Anagramm-R\\u00e4tsel \\u2014 9 Buchstaben",prompt_en:"Form words from REYKJAVIK!"},\n'
    '    {id:"hl_insel_flaeche",icon:"\\u{1F3DD}\\uFE0F",title:"Inseln: Fl\\u00e4che",group:"inseln",prompt:"Welche Insel ist gr\\u00f6\\u00dfer?",desc:"Fl\\u00e4che in km\\u00b2",prompt_en:"Which island is larger?"},\n'
    '    {id:"hl_insel_einwohner",icon:"\\u{1F3DD}\\uFE0F",title:"Inseln: Einwohner",group:"inseln",prompt:"Welche Insel hat mehr Einwohner?",desc:"Bev\\u00f6lkerung in Tsd.",prompt_en:"Which island has more inhabitants?"},\n'
    '    {id:"insel_match_ozean",icon:"\\u{1F3DD}\\uFE0F",title:"Inseln: Ozean-Zuordnung",group:"inseln",prompt:"Zu welchem Ozean geh\\u00f6rt diese Insel?",desc:"Insel \\u2192 Ozean",prompt_en:"Which ocean does this island belong to?"},\n'
    '    {id:"insel_match_kontinent",icon:"\\u{1F3DD}\\uFE0F",title:"Inseln: Kontinent",group:"inseln",prompt:"Auf welchem Kontinent liegt diese Insel?",desc:"Insel \\u2192 Kontinent",prompt_en:"On which continent is this island?"},\n'
    '    {id:"insel_pin_lage",icon:"\\u{1F3DD}\\uFE0F",title:"Inseln: Lage auf der Karte",group:"inseln",prompt:"Wo liegt diese Insel?",desc:"Pin auf der Weltkarte",prompt_en:"Where is this island located?"},\n'
    '    {id:"hl_insel_aequator",icon:"\\u{1F3DD}\\uFE0F",title:"Inseln: \\u00c4quatordistanz",group:"inseln",prompt:"Welche Insel liegt weiter vom \\u00c4quator entfernt?",desc:"\\u00c4quatordistanz vergleichen",prompt_en:"Which island is farther from the equator?"},\n'
    '    {id:"ws_insel_groenland",icon:"\\u{1F3DD}\\uFE0F",title:"WS: Gr\\u00f6nland",group:"inseln",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GROENLAND!",desc:"Anagramm-R\\u00e4tsel \\u2014 9 Buchstaben",prompt_en:"Form words from GROENLAND!"},'
)

CATS_OLD = 'capitals:{label:"Hauptst\\u00e4dte weltweit",icon:"\\u{1F3D9}\\uFE0F",modes:["hl_capital_einwohner","hl_capital_hoehe","capital_match_kontinent","capital_match_grossstadt","capital_pin_lage","hl_capital_aequator","ws_capital_reykjavik"],cost:0},'
CATS_NEW = (
    'capitals:{label:"Hauptst\\u00e4dte weltweit",icon:"\\u{1F3D9}\\uFE0F",modes:["hl_capital_einwohner","hl_capital_hoehe","capital_match_kontinent","capital_match_grossstadt","capital_pin_lage","hl_capital_aequator","ws_capital_reykjavik"],cost:0},\n'
    '  inseln:{label:"Inseln weltweit",icon:"\\u{1F3DD}\\uFE0F",modes:["hl_insel_flaeche","hl_insel_einwohner","insel_match_ozean","insel_match_kontinent","insel_pin_lage","hl_insel_aequator","ws_insel_groenland"],cost:0},'
)

GEN_DISP_OLD = 'ws_capital_reykjavik:()=>{initCapitalsWS("reykjavik");return null;},'
GEN_DISP_NEW = (
    'ws_capital_reykjavik:()=>{initCapitalsWS("reykjavik");return null;},\n'
    '  hl_insel_flaeche:()=>genInselnHLExt("flaeche_km2",{unit:"km²",prompt:_tc("Welche Insel ist größer?")}),\n'
    '  hl_insel_einwohner:()=>genInselnHLExt("einwohner_tsd",{unit:"Tsd.",prompt:_tc("Welche Insel hat mehr Einwohner?")}),\n'
    '  insel_match_ozean:()=>genInselnMatchExt("ozean",_tc("Zu welchem Ozean gehört diese Insel?")),\n'
    '  insel_match_kontinent:()=>genInselnMatchExt("kontinent",_tc("Auf welchem Kontinent liegt diese Insel?")),\n'
    '  insel_pin_lage:()=>genInselnPinQ(),\n'
    '  hl_insel_aequator:()=>genInselnHLExt("lat",{unit:"°",absVal:true,prompt:_tc("Welche Insel liegt weiter vom Äquator entfernt?")}),\n'
    '  ws_insel_groenland:()=>{initInselnWS("groenland");return null;},'
)

REP_OLD = ".replace('PLACEHOLDER_CAPITALS',       CAPITALS_J)"
REP_NEW = (
    ".replace('PLACEHOLDER_CAPITALS',       CAPITALS_J)\n"
    "  .replace('PLACEHOLDER_INSELN_WS',      INSELN_WS_J)\n"
    "  .replace('PLACEHOLDER_INSELN',         INSELN_J)"
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

print('\nPatch 446 fertig.')
