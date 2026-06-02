#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase: 445
Date:  2026-06-02
Scope: Hauptstädte-Vergleiche — 7 neue Modi + capitals_extended.json (80 Hauptstädte)

Modi: hl_capital_einwohner, hl_capital_hoehe, capital_match_kontinent,
      capital_match_grossstadt, capital_pin_lage, hl_capital_dist_aequator,
      ws_capital_reykjavik

i18n: FESTE Strings (kein dynamisches replace — vermeidet "" Bug).
Zero-Bug Policy: assert count==1.
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

VC_OLD = 'def check_nparks_extended(filename, data):'
VC_NEW = '''\
def check_capitals_extended(filename, data):
    """Validiert data/capitals_extended.json."""
    REQUIRED = ['land','kontinent','einwohner_mio','hoehe_m','lat','lng']
    KONT = {'Europa','Asien','Afrika','Nordamerika','Südamerika','Ozeanien'}
    if not isinstance(data, dict):
        warn(filename,'struktur','root','muss ein Dict sein'); return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename,'eintrag',name,'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename,'pflichtfeld',name,f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT:
            warn(filename,'enum:kontinent',name,f"'{k}' ungültig")


def check_nparks_extended(filename, data):'''

VC_DISP_OLD = (
    '    elif name == "nparks_extended.json":\n'
    '        check_nparks_extended(filename, data)\n'
)
VC_DISP_NEW = (
    '    elif name == "capitals_extended.json":\n'
    '        check_capitals_extended(filename, data)\n'
    '    elif name == "nparks_extended.json":\n'
    '        check_nparks_extended(filename, data)\n'
)

patch(VC, [
    (VC_OLD,      VC_NEW,      'VC: check_capitals_extended'),
    (VC_DISP_OLD, VC_DISP_NEW, 'VC: dispatch capitals'),
])


print('\n-- 2. gen.py --')

# 2.1 Python Loader
LOAD_OLD = (
    "        NPARKS_WS_J = __import__('json').dumps(__import__('json').load(_npwf),"
    " ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/capitals_extended.json'), 'r', encoding='utf-8') as _capf:\n"
    "        CAPITALS_J = __import__('json').dumps(__import__('json').load(_capf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/capitals_ws.json'), 'r', encoding='utf-8') as _capwf:\n"
    "        CAPITALS_WS_J = __import__('json').dumps(__import__('json').load(_capwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

# 2.2 LAND_LATLON: fehlende Länder
LL_OLD = '"Ghana":[7.946,-1.023]\n};'
LL_NEW = (
    '"Ghana":[7.946,-1.023],\n'
    '  "Bolivien":[-16.5,-68.1],"Guatemala":[15.8,-90.2],"Panama":[9.0,-79.5],\n'
    '  "Nicaragua":[12.9,-85.2],"Jamaika":[18.1,-77.3],"Bahamas":[25.0,-77.4],\n'
    '  "Fidschi":[-17.7,178.1],"Mongolei":[46.9,103.8],'
    '"Saudi-Arabien":[23.9,45.1],\n'
    '  "Philippinen":[12.9,121.8],"Singapur":[1.4,103.8],'
    '"Angola":[-11.2,17.9],\n'
    '  "Marokko":[31.8,-7.1],"Sudan":[12.9,30.2]\n'
    '};'
)

# 2.3 JS Konstanten
CONST_OLD = 'const NPARKS_WS_DATA=PLACEHOLDER_NPARKS_WS;\nconst NPARKS_DATA=PLACEHOLDER_NPARKS;'
CONST_NEW = (
    'const NPARKS_WS_DATA=PLACEHOLDER_NPARKS_WS;\n'
    'const NPARKS_DATA=PLACEHOLDER_NPARKS;\n'
    'const CAPITALS_WS_DATA=PLACEHOLDER_CAPITALS_WS;\n'
    'const CAPITALS_DATA=PLACEHOLDER_CAPITALS;'
)

# 2.4 _mkWS Init
MKWS_OLD = 'var initNparksWS=_mkWS(NPARKS_WS_DATA,"Nparks");'
MKWS_NEW = (
    'var initNparksWS=_mkWS(NPARKS_WS_DATA,"Nparks");\n'
    'var initCapitalsWS=_mkWS(CAPITALS_WS_DATA,"Capitals");'
)

# 2.5 Generator-Funktionen
GEN_FN_OLD = 'window.genNparksPinQ=genNparksPinQ;'
GEN_FN_NEW = (
    'window.genNparksPinQ=genNparksPinQ;\n'
    '\n'
    '/* Phase 445: Hauptstädte */\n'
    'function genCapitalsHLExt(field,opts){var o=opts||{};var items=[];var _CD=CAPITALS_DATA;\n'
    '  var _ks=Object.keys(_CD).filter(function(k){return Object.prototype.hasOwnProperty.call(_CD,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_CD[_n][field]);if(!isNaN(_v)&&_v>=0)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" \\u00b7 "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welche Hauptstadt hat mehr Einwohner?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"cap_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genCapitalsHLExt=genCapitalsHLExt;\n'
    '\n'
    'function genCapitalsMatchExt(field,prompt,fixedPool){var _CD=CAPITALS_DATA;\n'
    '  var valid=Object.keys(_CD).filter(function(k){return Object.prototype.hasOwnProperty.call(_CD,k)&&_CD[k][field]!=null&&_CD[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_CD[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_CD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"cap_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genCapitalsMatchExt=genCapitalsMatchExt;\n'
    '\n'
    'function genCapitalsPinQ(){var _CD=CAPITALS_DATA;\n'
    '  var keys=Object.keys(_CD).filter(function(k){return Object.prototype.hasOwnProperty.call(_CD,k)&&_CD[k].lat&&_CD[k].lng;});\n'
    '  if(keys.length<4)return null;\n'
    '  var idx=~~(rng()*keys.length),name=keys[idx],e=_CD[name];\n'
    '  return{type:"uk_pin",cat:"capitals",prompt:_tc("Wo auf der Welt liegt diese Hauptstadt?"),\n'
    '    subj:name,lat:e.lat,lng:e.lng,lid:"cappin_"+idx,cc:"de"};\n'
    '}\n'
    'window.genCapitalsPinQ=genCapitalsPinQ;'
)

# 2.6 i18n PL — FESTE Strings (kein dynamisches replace!)
I18N_PL_OLD = (
    '"Wo auf der Welt liegt dieser Nationalpark?":"Gdzie na świecie leży ten park narodowy?"'
    '},"en":{"Welche Seri'
)
I18N_PL_NEW = (
    '"Wo auf der Welt liegt dieser Nationalpark?":"Gdzie na świecie leży ten park narodowy?",'
    '"Welche Hauptstadt hat mehr Einwohner?":"Które miasto stołeczne ma więcej mieszkańców?",'
    '"Welche Hauptstadt liegt höher?":"Które miasto stołeczne leży wyżej?",'
    '"Auf welchem Kontinent liegt diese Hauptstadt?":"Na jakim kontynencie leży ta stolica?",'
    '"Wie groß ist diese Hauptstadt?":"Jak duża jest ta stolica?",'
    '"Wo auf der Welt liegt diese Hauptstadt?":"Gdzie na świecie leży ta stolica?",'
    '"Welche Hauptstadt ist weiter vom Äquator entfernt?":"Która stolica jest dalej od równika?"'
    '},"en":{"Welche Seri'
)

# 2.7 i18n EN — FESTE Strings
I18N_EN_OLD = (
    '"Wo auf der Welt liegt dieser Nationalpark?":"Where in the world is this national park?"'
    '}};'
)
I18N_EN_NEW = (
    '"Wo auf der Welt liegt dieser Nationalpark?":"Where in the world is this national park?",'
    '"Welche Hauptstadt hat mehr Einwohner?":"Which capital city has more inhabitants?",'
    '"Welche Hauptstadt liegt höher?":"Which capital city is situated higher?",'
    '"Auf welchem Kontinent liegt diese Hauptstadt?":"On which continent is this capital?",'
    '"Wie groß ist diese Hauptstadt?":"How large is this capital city?",'
    '"Wo auf der Welt liegt diese Hauptstadt?":"Where in the world is this capital city?",'
    '"Welche Hauptstadt ist weiter vom Äquator entfernt?":"Which capital is farther from the equator?"'
    '}};'
)

# 2.8 MODES
MODES_OLD = (
    '{id:"ws_npark_yellowstone",icon:"\\u{1F332}",title:"WS: Yellowstone",'
    'group:"nparks",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus YELLOWSTONE!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben",'
    'prompt_en:"Form words from YELLOWSTONE!"},'
)
MODES_NEW = (
    MODES_OLD +
    '\n    /* Phase 445: Hauptstädte */\n'
    '    {id:"hl_capital_einwohner",icon:"\\u{1F3D9}\\uFE0F",title:"Hauptst\\u00e4dte: Einwohner",'
    'group:"capitals",prompt:"Welche Hauptstadt hat mehr Einwohner?",'
    'desc:"Tokio vs. Paris \\u2014 welche Hauptstadt ist gr\\u00f6\\u00dfer?",'
    'prompt_en:"Which capital city has more inhabitants?"},\n'
    '    {id:"hl_capital_hoehe",icon:"\\u26F0\\uFE0F",title:"Hauptst\\u00e4dte: H\\u00f6he",'
    'group:"capitals",prompt:"Welche Hauptstadt liegt h\\u00f6her?",'
    'desc:"La Paz, Quito, Addis Abeba \\u2014 H\\u00f6he \\u00fcber dem Meeresspiegel.",'
    'prompt_en:"Which capital city is situated higher?"},\n'
    '    {id:"capital_match_kontinent",icon:"\\u{1F30D}",title:"Hauptst\\u00e4dte: Kontinent",'
    'group:"capitals",prompt:"Auf welchem Kontinent liegt diese Hauptstadt?",'
    'desc:"Europa, Asien, Afrika \\u2014 erkenne den Kontinent.",'
    'prompt_en:"On which continent is this capital?"},\n'
    '    {id:"capital_match_grossstadt",icon:"\\u{1F3D9}\\uFE0F",title:"Hauptst\\u00e4dte: Gr\\u00f6\\u00dfe",'
    'group:"capitals",prompt:"Wie gro\\u00df ist diese Hauptstadt?",'
    'desc:"Millionenstadt, Gro\\u00dfstadt oder Kleinstadt?",'
    'prompt_en:"How large is this capital city?"},\n'
    '    {id:"capital_pin_lage",icon:"\\u{1F4CD}",title:"Hauptst\\u00e4dte: Lage pinnen",'
    'group:"capitals",prompt:"Wo auf der Welt liegt diese Hauptstadt?",'
    'desc:"Pinne die Hauptstadt auf der Weltkarte.",'
    'prompt_en:"Where in the world is this capital city?"},\n'
    '    {id:"hl_capital_aequator",icon:"\\u{1F30D}",title:"Hauptst\\u00e4dte: \\u00c4quator-Distanz",'
    'group:"capitals",prompt:"Welche Hauptstadt ist weiter vom \\u00c4quator entfernt?",'
    'desc:"Absoluter Breitengrad \\u2014 Reykjavik vs. Singapore.",'
    'prompt_en:"Which capital is farther from the equator?"},\n'
    '    {id:"ws_capital_reykjavik",icon:"\\u{1F3D9}\\uFE0F",title:"WS: Reykjavik",'
    'group:"capitals",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus REYKJAVIK!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 9 Buchstaben",'
    'prompt_en:"Form words from REYKJAVIK!"},'
)

# 2.9 MODE_CATS
CATS_OLD = (
    'nparks:{label:"Nationalparks weltweit",icon:"\\u{1F332}",'
    'modes:["hl_npark_flaeche","hl_npark_gruendung","npark_match_land","npark_match_kontinent",'
    '"npark_match_oekosystem","npark_pin_lage","ws_npark_yellowstone"],cost:0},'
)
CATS_NEW = (
    CATS_OLD +
    '\n  capitals:{label:"Hauptst\\u00e4dte weltweit",icon:"\\u{1F3D9}\\uFE0F",'
    'modes:["hl_capital_einwohner","hl_capital_hoehe","capital_match_kontinent",'
    '"capital_match_grossstadt","capital_pin_lage","hl_capital_aequator","ws_capital_reykjavik"],cost:0},'
)

# 2.10 GEN Dispatcher
DISP_OLD = 'ws_npark_yellowstone:()=>{initNparksWS("yellowstone");return null;},'
DISP_NEW = (
    DISP_OLD +
    '\n  /* Phase 445: Hauptstädte */\n'
    '  hl_capital_einwohner:()=>genCapitalsHLExt("einwohner_mio",{unit:"Mio.",prompt:_tc("Welche Hauptstadt hat mehr Einwohner?")}),\n'
    '  hl_capital_hoehe:()=>genCapitalsHLExt("hoehe_m",{unit:"m",prompt:_tc("Welche Hauptstadt liegt h\\u00f6her?")}),\n'
    '  capital_match_kontinent:()=>genCapitalsMatchExt("kontinent",_tc("Auf welchem Kontinent liegt diese Hauptstadt?"),["Europa","Asien","Afrika","Nordamerika","S\\u00fcdamerika","Ozeanien"]),\n'
    '  capital_match_grossstadt:()=>genCapitalsMatchExt("grossstadt",_tc("Wie gro\\u00df ist diese Hauptstadt?")),\n'
    '  capital_pin_lage:()=>genCapitalsPinQ(),\n'
        '  hl_capital_aequator:()=>genCapitalsHLExt("dist_aequator",{unit:"\\u00b0",prompt:_tc("Welche Hauptstadt ist weiter vom \\u00c4quator entfernt?")}),\n'
'  ws_capital_reykjavik:()=>{initCapitalsWS("reykjavik");return null;},'
)

# 2.11 Replace-Kette
REPL_OLD = "  .replace('PLACEHOLDER_NPARKS',         NPARKS_J)"
REPL_NEW = (
    "  .replace('PLACEHOLDER_NPARKS',         NPARKS_J)\n"
    "  .replace('PLACEHOLDER_CAPITALS_WS',    CAPITALS_WS_J)\n"
    "  .replace('PLACEHOLDER_CAPITALS',       CAPITALS_J)"
)

patch(GEN, [
    (LOAD_OLD,       LOAD_NEW,        'Py: capitals + capitals_ws laden'),
    (LL_OLD,         LL_NEW,          'JS: LAND_LATLON neue Länder'),
    (CONST_OLD,      CONST_NEW,       'JS: CAPITALS Konstanten'),
    (MKWS_OLD,       MKWS_NEW,        'JS: initCapitalsWS'),
    (GEN_FN_OLD,     GEN_FN_NEW,      'JS: genCapitalsHLExt + Match + Pin'),
    (I18N_PL_OLD,    I18N_PL_NEW,     'i18n PL: 7 Capitals-Strings'),
    (I18N_EN_OLD,    I18N_EN_NEW,     'i18n EN: 7 Capitals-Strings'),
    (MODES_OLD,      MODES_NEW,       'MODES: 7 Capitals-Modi'),
    (CATS_OLD,       CATS_NEW,        'MODE_CATS: capitals'),
    (DISP_OLD,       DISP_NEW,        'GEN dispatch: 7 Capitals-Modi'),
    (REPL_OLD,       REPL_NEW,        'Replace-Kette: CAPITALS_WS + CAPITALS'),
])

print('\nPatch 445 fertig!')
