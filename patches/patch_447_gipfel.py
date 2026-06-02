#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase: 447
Date:  2026-06-02
Scope: Gipfel & Berge — 7 neue Modi + gipfel_extended.json (80 Einträge)

Modi: hl_gipfel_hoehe, gipfel_match_gebirge, gipfel_match_kontinent,
      gipfel_pin_lage, hl_gipfel_erstbesteigung, timeline_gipfel_besteigung,
      ws_gipfel_himalaya
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
assert 'check_gipfel_extended' in c_vc, 'check_gipfel_extended missing from VC'
print('  OK  VC: check_gipfel_extended already present')


print('\n-- 2. gen.py --')

LOAD_OLD = (
    "        INSELN_WS_J = __import__('json').dumps(__import__('json').load(_inswf),"
    " ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/gipfel_extended.json'), 'r', encoding='utf-8') as _gipf:\n"
    "        GIPFEL_J = __import__('json').dumps(__import__('json').load(_gipf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/gipfel_ws.json'), 'r', encoding='utf-8') as _gipwf:\n"
    "        GIPFEL_WS_J = __import__('json').dumps(__import__('json').load(_gipwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

JS_CONST_OLD = "const INSELN_DATA=PLACEHOLDER_INSELN;"
JS_CONST_NEW = (
    "const INSELN_DATA=PLACEHOLDER_INSELN;\n"
    "const GIPFEL_WS_DATA=PLACEHOLDER_GIPFEL_WS;\n"
    "const GIPFEL_DATA=PLACEHOLDER_GIPFEL;"
)

MKWS_OLD = 'var initInselnWS=_mkWS(INSELN_WS_DATA,"Inseln");'
MKWS_NEW = (
    'var initInselnWS=_mkWS(INSELN_WS_DATA,"Inseln");\n'
    'var initGipfelWS=_mkWS(GIPFEL_WS_DATA,"Gipfel");'
)

GEN_FUNCS_OLD = "window.genInselnPinQ=genInselnPinQ;"
GEN_FUNCS_NEW = r"""window.genInselnPinQ=genInselnPinQ;
function genGipfelHLExt(field,opts){var o=opts||{};var items=[];var _GD=GIPFEL_DATA;for(var k in _GD){var e=_GD[k];var v=e[field];if(v!=null){items.push({name:k,val:v,land:e.land||"",kontinent:e.kontinent||"",gebirge:e.gebirge||"",_raw:v});}}if(items.length<4)return null;items.sort(function(a,b){return b.val-a.val;});var pool=items.slice(0,40);var idx=Math.floor(Math.random()*pool.length);var chosen=pool[idx];var distractors=pool.filter(function(x){return x.name!==chosen.name;}).sort(function(){return Math.random()-0.5;}).slice(0,3);var choices=[chosen].concat(distractors).sort(function(){return Math.random()-0.5;});var prompt=o.prompt||_tc("Welcher Gipfel ist höher?");return _mkHLQ(chosen,distractors,choices,prompt,o);}
function genGipfelMatchExt(field,prompt){var _GD=GIPFEL_DATA;var pool=Object.keys(_GD).map(function(k){return{name:k,val:_GD[k][field]};}).filter(function(x){return x.val!=null;});if(pool.length<4)return null;var shuffled=pool.sort(function(){return Math.random()-0.5;}).slice(0,4);var correct=shuffled[0];var choices=shuffled.map(function(x){return x.name;}).sort(function(){return Math.random()-0.5;});return {type:"match",prompt:prompt||_tc("Zu welchem Gebirge gehört dieser Gipfel?"),subject:correct.val,choices:choices,answer:correct.name,explanation:correct.name+" → "+correct.val};}
function genGipfelPinQ(){var _GD=GIPFEL_DATA;var keys=Object.keys(_GD).filter(function(k){return _GD[k].lat!=null&&_GD[k].lng!=null;});if(keys.length<1)return null;var k=keys[Math.floor(Math.random()*keys.length)];var e=_GD[k];return {type:"pin",prompt:_tc("Wo liegt dieser Gipfel?"),subject:k,lat:e.lat,lng:e.lng,explanation:k+" ("+e.gebirge+", "+e.hoehe_m+"m)",radius:300};}
function genGipfelTimelineQ(){var _GD=GIPFEL_DATA;var keys=Object.keys(_GD).filter(function(k){return _GD[k].erstbesteigung_jahr!=null;});if(keys.length<4)return null;var pool=keys.sort(function(){return Math.random()-0.5;}).slice(0,4);return {type:"timeline",prompt:_tc("Sortiere diese Gipfel nach Erstbesteigung (älteste zuerst)!"),items:pool.map(function(k){return{label:k,year:_GD[k].erstbesteigung_jahr};})};}
window.genGipfelHLExt=genGipfelHLExt;
window.genGipfelMatchExt=genGipfelMatchExt;
window.genGipfelPinQ=genGipfelPinQ;
window.genGipfelTimelineQ=genGipfelTimelineQ;"""

I18N_PL_OLD = '"Welche Insel liegt weiter vom Äquator entfernt?":"Która wyspa jest dalej od równika?"},"en":{"Welche Serie startete f'
I18N_PL_NEW = '"Welche Insel liegt weiter vom Äquator entfernt?":"Która wyspa jest dalej od równika?","Welcher Gipfel ist höher?":"Który szczyt jest wyższy?","Zu welchem Gebirge gehört dieser Gipfel?":"Do jakiego pasma górskiego należy ten szczyt?","Auf welchem Kontinent liegt dieser Gipfel?":"Na jakim kontynencie leży ten szczyt?","Wo liegt dieser Gipfel?":"Gdzie leży ten szczyt?","Welcher Gipfel wurde zuerst bestiegen?":"Który szczyt został zdobyty jako pierwszy?","Sortiere diese Gipfel nach Erstbesteigung (älteste zuerst)!":"Posortuj te szczyty według pierwszego wejścia (od najstarszego)!"},"en":{"Welche Serie startete f'

I18N_EN_OLD = '"Which island is farther from the equator?"}};\nfuncti'
I18N_EN_NEW = '"Which island is farther from the equator?","Welcher Gipfel ist höher?":"Which peak is higher?","Zu welchem Gebirge gehört dieser Gipfel?":"Which mountain range does this peak belong to?","Auf welchem Kontinent liegt dieser Gipfel?":"On which continent is this peak?","Wo liegt dieser Gipfel?":"Where is this peak located?","Welcher Gipfel wurde zuerst bestiegen?":"Which peak was first climbed?","Sortiere diese Gipfel nach Erstbesteigung (älteste zuerst)!":"Sort these peaks by first ascent (oldest first)!"}};\nfuncti'

MODES_OLD = '{id:"ws_insel_groenland",icon:"\\u{1F3DD}\\uFE0F",title:"WS: Gr\\u00f6nland",group:"inseln",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GROENLAND!",desc:"Anagramm-R\\u00e4tsel \\u2014 9 Buchstaben",prompt_en:"Form words from GROENLAND!"},'
MODES_NEW = (
    '{id:"ws_insel_groenland",icon:"\\u{1F3DD}\\uFE0F",title:"WS: Gr\\u00f6nland",group:"inseln",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GROENLAND!",desc:"Anagramm-R\\u00e4tsel \\u2014 9 Buchstaben",prompt_en:"Form words from GROENLAND!"},\n'
    '    {id:"hl_gipfel_hoehe",icon:"\\u26F0\\uFE0F",title:"Gipfel: H\\u00f6he",group:"gipfel",prompt:"Welcher Gipfel ist h\\u00f6her?",desc:"H\\u00f6he in Meter",prompt_en:"Which peak is higher?"},\n'
    '    {id:"gipfel_match_gebirge",icon:"\\u26F0\\uFE0F",title:"Gipfel: Gebirge",group:"gipfel",prompt:"Zu welchem Gebirge geh\\u00f6rt dieser Gipfel?",desc:"Gipfel \\u2192 Gebirge",prompt_en:"Which mountain range does this peak belong to?"},\n'
    '    {id:"gipfel_match_kontinent",icon:"\\u26F0\\uFE0F",title:"Gipfel: Kontinent",group:"gipfel",prompt:"Auf welchem Kontinent liegt dieser Gipfel?",desc:"Gipfel \\u2192 Kontinent",prompt_en:"On which continent is this peak?"},\n'
    '    {id:"gipfel_pin_lage",icon:"\\u26F0\\uFE0F",title:"Gipfel: Lage auf der Karte",group:"gipfel",prompt:"Wo liegt dieser Gipfel?",desc:"Pin auf der Weltkarte",prompt_en:"Where is this peak located?"},\n'
    '    {id:"hl_gipfel_erstbesteigung",icon:"\\u26F0\\uFE0F",title:"Gipfel: Erstbesteigung",group:"gipfel",prompt:"Welcher Gipfel wurde zuerst bestiegen?",desc:"Erstbesteigungsjahr vergleichen",prompt_en:"Which peak was first climbed?"},\n'
    '    {id:"timeline_gipfel_besteigung",icon:"\\u26F0\\uFE0F",title:"Gipfel: Zeitleiste",group:"gipfel",prompt:"Sortiere diese Gipfel nach Erstbesteigung (\\u00e4lteste zuerst)!",desc:"Zeitleiste der Erstbesteigungen",prompt_en:"Sort these peaks by first ascent (oldest first)!"},\n'
    '    {id:"ws_gipfel_himalaya",icon:"\\u26F0\\uFE0F",title:"WS: Himalaya",group:"gipfel",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus HIMALAYA!",desc:"Anagramm-R\\u00e4tsel \\u2014 8 Buchstaben",prompt_en:"Form words from HIMALAYA!"},'
)

CATS_OLD = 'inseln:{label:"Inseln weltweit",icon:"\\u{1F3DD}\\uFE0F",modes:["hl_insel_flaeche","hl_insel_einwohner","insel_match_ozean","insel_match_kontinent","insel_pin_lage","hl_insel_aequator","ws_insel_groenland"],cost:0},'
CATS_NEW = (
    'inseln:{label:"Inseln weltweit",icon:"\\u{1F3DD}\\uFE0F",modes:["hl_insel_flaeche","hl_insel_einwohner","insel_match_ozean","insel_match_kontinent","insel_pin_lage","hl_insel_aequator","ws_insel_groenland"],cost:0},\n'
    '  gipfel:{label:"Gipfel & Berge",icon:"\\u26F0\\uFE0F",modes:["hl_gipfel_hoehe","gipfel_match_gebirge","gipfel_match_kontinent","gipfel_pin_lage","hl_gipfel_erstbesteigung","timeline_gipfel_besteigung","ws_gipfel_himalaya"],cost:0},'
)

GEN_DISP_OLD = 'ws_insel_groenland:()=>{initInselnWS("groenland");return null;},'
GEN_DISP_NEW = (
    'ws_insel_groenland:()=>{initInselnWS("groenland");return null;},\n'
    '  hl_gipfel_hoehe:()=>genGipfelHLExt("hoehe_m",{unit:"m",prompt:_tc("Welcher Gipfel ist höher?")}),\n'
    '  gipfel_match_gebirge:()=>genGipfelMatchExt("gebirge",_tc("Zu welchem Gebirge gehört dieser Gipfel?")),\n'
    '  gipfel_match_kontinent:()=>genGipfelMatchExt("kontinent",_tc("Auf welchem Kontinent liegt dieser Gipfel?")),\n'
    '  gipfel_pin_lage:()=>genGipfelPinQ(),\n'
    '  hl_gipfel_erstbesteigung:()=>genGipfelHLExt("erstbesteigung_jahr",{unit:"",lowerWins:true,prompt:_tc("Welcher Gipfel wurde zuerst bestiegen?")}),\n'
    '  timeline_gipfel_besteigung:()=>genGipfelTimelineQ(),\n'
    '  ws_gipfel_himalaya:()=>{initGipfelWS("himalaya");return null;},'
)

REP_OLD = ".replace('PLACEHOLDER_INSELN',         INSELN_J)"
REP_NEW = (
    ".replace('PLACEHOLDER_INSELN',         INSELN_J)\n"
    "  .replace('PLACEHOLDER_GIPFEL_WS',      GIPFEL_WS_J)\n"
    "  .replace('PLACEHOLDER_GIPFEL',         GIPFEL_J)"
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

print('\nPatch 447 fertig.')
