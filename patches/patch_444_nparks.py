#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase: 444
Date:  2026-06-02
Scope: Nationalparks weltweit — 7 neue Modi + nparks_extended.json (80 Parks)

Modi: hl_npark_flaeche, hl_npark_gruendung, npark_match_land,
      npark_match_kontinent, npark_match_oekosystem,
      npark_pin_lage, ws_npark_yellowstone

Zero-Bug Policy: assert count==1 vor jedem replace.
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


# ── 1. validate_content.py ────────────────────────────────────────────────
print('\n-- 1. validate_content.py --')

VC_CHECK_OLD = 'def check_fluesse_extended(filename, data):'
VC_CHECK_NEW = '''\
def check_nparks_extended(filename, data):
    """Validiert data/nparks_extended.json."""
    REQUIRED = ['flaeche_km2','gruendung','land','kontinent','oekosystem','lat','lng']
    KONT_ENUM = {'Nordamerika','Südamerika','Europa','Afrika','Asien','Ozeanien','Arktis'}
    if not isinstance(data, dict):
        warn(filename,'struktur','root','muss ein Dict sein'); return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename,'eintrag',name,'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename,'pflichtfeld',name,f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT_ENUM:
            warn(filename,'enum:kontinent',name,f"'{k}' ungültig")
        for num_f in ('flaeche_km2','gruendung'):
            v = e.get(num_f)
            if v is not None and not isinstance(v,(int,float)):
                warn(filename,'typ:'+num_f,name,'Muss Zahl sein')


def check_fluesse_extended(filename, data):'''

VC_DISP_OLD = (
    '    elif name == "fluesse_extended.json":\n'
    '        check_fluesse_extended(filename, data)\n'
)
VC_DISP_NEW = (
    '    elif name == "nparks_extended.json":\n'
    '        check_nparks_extended(filename, data)\n'
    '    elif name == "fluesse_extended.json":\n'
    '        check_fluesse_extended(filename, data)\n'
)

patch(VC, [
    (VC_CHECK_OLD, VC_CHECK_NEW, 'VC: check_nparks_extended'),
    (VC_DISP_OLD,  VC_DISP_NEW,  'VC: dispatch nparks'),
])


# ── 2. gen.py ─────────────────────────────────────────────────────────────
print('\n-- 2. gen.py --')

# 2.1 Python Loader (nach fluesse_ws)
LOAD_OLD = (
    "        FLUESSE_WS_J = __import__('json').dumps(__import__('json').load(_flwf),"
    " ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/nparks_extended.json'), 'r', encoding='utf-8') as _npf:\n"
    "        NPARKS_J = __import__('json').dumps(__import__('json').load(_npf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/nparks_ws.json'), 'r', encoding='utf-8') as _npwf:\n"
    "        NPARKS_WS_J = __import__('json').dumps(__import__('json').load(_npwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

# 2.2 LAND_LATLON — 14 fehlende Länder ergänzen
LL_OLD = '"Venezuela":[6.424,-66.589]\n};'
LL_NEW = (
    '"Venezuela":[6.424,-66.589],\n'
    '  "Kenia":[-0.023,37.906],"Tansania":[-6.369,34.889],"Uganda":[1.373,32.290],\n'
    '  "Namibia":[-22.956,18.490],"Botswana":[-22.328,24.685],"Äthiopien":[9.145,40.490],\n'
    '  "Ecuador":[-1.831,-78.183],"Nepal":[28.394,84.124],"Malaysia":[4.211,101.976],\n'
    '  "Jordanien":[30.585,36.238],"Costa Rica":[9.748,-83.754],\n'
    '  "Kirgisistan":[41.204,74.766],"Sri Lanka":[7.873,80.772],"Ghana":[7.946,-1.023]\n'
    '};'
)

# 2.3 JS Konstanten
CONST_OLD = 'const FLUESSE_WS_DATA=PLACEHOLDER_FLUESSE_WS;\nconst FLUESSE_DATA=PLACEHOLDER_FLUESSE;'
CONST_NEW = (
    'const FLUESSE_WS_DATA=PLACEHOLDER_FLUESSE_WS;\n'
    'const FLUESSE_DATA=PLACEHOLDER_FLUESSE;\n'
    'const NPARKS_WS_DATA=PLACEHOLDER_NPARKS_WS;\n'
    'const NPARKS_DATA=PLACEHOLDER_NPARKS;'
)

# 2.4 _mkWS Init
MKWS_OLD = 'var initFluessWS=_mkWS(FLUESSE_WS_DATA,"Fluesse");'
MKWS_NEW = (
    'var initFluessWS=_mkWS(FLUESSE_WS_DATA,"Fluesse");\n'
    'var initNparksWS=_mkWS(NPARKS_WS_DATA,"Nparks");'
)

# 2.5 Generator-Funktionen (nach genFlussPinQ)
GEN_FN_OLD = 'window.genFlussPinQ=genFlussPinQ;'
GEN_FN_NEW = (
    'window.genFlussPinQ=genFlussPinQ;\n'
    '\n'
    '/* Phase 444: Nationalparks */\n'
    'function genNparksHLExt(field,opts){var o=opts||{};var items=[];var _ND=NPARKS_DATA;\n'
    '  var _ks=Object.keys(_ND).filter(function(k){return Object.prototype.hasOwnProperty.call(_ND,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_ND[_n][field]);if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" \\u00b7 "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welcher Nationalpark ist gr\\u00f6\\u00dfer?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"npark_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genNparksHLExt=genNparksHLExt;\n'
    '\n'
    'function genNparksMatchExt(field,prompt,fixedPool){var _ND=NPARKS_DATA;\n'
    '  var valid=Object.keys(_ND).filter(function(k){return Object.prototype.hasOwnProperty.call(_ND,k)&&_ND[k][field]!=null&&_ND[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_ND[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_ND[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"npark_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genNparksMatchExt=genNparksMatchExt;\n'
    '\n'
    'function genNparksPinQ(){var _ND=NPARKS_DATA;\n'
    '  var keys=Object.keys(_ND).filter(function(k){return Object.prototype.hasOwnProperty.call(_ND,k)&&_ND[k].lat&&_ND[k].lng;});\n'
    '  if(keys.length<4)return null;\n'
    '  var idx=~~(rng()*keys.length),name=keys[idx],e=_ND[name];\n'
    '  return{type:"uk_pin",cat:"nparks",prompt:_tc("Wo auf der Welt liegt dieser Nationalpark?"),\n'
    '    subj:name,lat:e.lat,lng:e.lng,lid:"nparkpin_"+idx,cc:"de"};\n'
    '}\n'
    'window.genNparksPinQ=genNparksPinQ;'
)

# 2.6 i18n PL
I18N_PL_OLD = (
    '"Wo liegt die Mündung dieses Flusses?":"Gdzie leży ujście tej rzeki?"'
    '},"en":{"Welche Serie'
)
raw = open(GEN, encoding='utf-8').read()
# Suche den echten String im File
import re as _re
m = _re.search(r'"Wo liegt die M.ndung dieses Flusses\?":"[^"]+"},"en":\{"Welche Serie', raw)
if m:
    I18N_PL_OLD = raw[m.start():m.end()]
    I18N_PL_NEW = I18N_PL_OLD.replace(
        '},"en":{"Welche Serie',
        ',"Welcher Nationalpark ist größer?":"Który park narodowy jest większy?",'
        '"Welcher Nationalpark wurde früher gegründet?":"Który park narodowy założono wcześniej?",'
        '"In welchem Land liegt dieser Nationalpark?":"W jakim kraju leży ten park narodowy?",'
        '"Auf welchem Kontinent liegt dieser Nationalpark?":"Na jakim kontynencie leży ten park?",'
        '"Welches Ökosystem hat dieser Nationalpark?":"Jaki ekosystem ma ten park narodowy?",'
        '"Wo auf der Welt liegt dieser Nationalpark?":"Gdzie na świecie leży ten park narodowy?"'
        '},"en":{"Welche Serie'
    )
else:
    raise AssertionError("PL-Anker nicht gefunden")

# 2.7 i18n EN
I18N_EN_OLD_STR = '"Wo liegt die Mündung dieses Flusses?":"Where is the mouth of this river?"'
m2 = _re.search(_re.escape(I18N_EN_OLD_STR) + r'\}\};', raw)
if m2:
    I18N_EN_OLD = raw[m2.start():m2.end()]
    I18N_EN_NEW = I18N_EN_OLD.replace(
        '}};',
        ',"Welcher Nationalpark ist größer?":"Which national park is larger?",'
        '"Welcher Nationalpark wurde früher gegründet?":"Which national park was founded earlier?",'
        '"In welchem Land liegt dieser Nationalpark?":"In which country is this national park?",'
        '"Auf welchem Kontinent liegt dieser Nationalpark?":"On which continent is this national park?",'
        '"Welches Ökosystem hat dieser Nationalpark?":"What ecosystem does this national park have?",'
        '"Wo auf der Welt liegt dieser Nationalpark?":"Where in the world is this national park?"'
        '}};'
    )
else:
    raise AssertionError("EN-Anker nicht gefunden")

# 2.8 MODES
MODES_OLD = (
    '{id:"ws_fluss_amazonas",icon:"\\u{1F30A}",title:"WS: Amazonas",'
    'group:"fluesse",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus AMAZONAS!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 8 Buchstaben",'
    'prompt_en:"Form words from AMAZONAS!"},'
)
MODES_NEW = (
    MODES_OLD +
    '\n    /* Phase 444: Nationalparks */\n'
    '    {id:"hl_npark_flaeche",icon:"\\u{1F332}",title:"Nationalparks: Fl\\u00e4che",'
    'group:"nparks",prompt:"Welcher Nationalpark ist gr\\u00f6\\u00dfer?",'
    'desc:"Fl\\u00e4che in km\\u00b2 \\u2014 von winzig bis riesig.",'
    'prompt_en:"Which national park is larger?"},\n'
    '    {id:"hl_npark_gruendung",icon:"\\u{1F332}",title:"Nationalparks: Gr\\u00fcndung",'
    'group:"nparks",prompt:"Welcher Nationalpark wurde fr\\u00fcher gegr\\u00fcndet?",'
    'desc:"Gr\\u00fcndungsjahr \\u2014 \\u00e4lter gewinnt.",prompt_en:"Which national park was founded earlier?"},\n'
    '    {id:"npark_match_land",icon:"\\u{1F30D}",title:"Nationalparks: Land",'
    'group:"nparks",prompt:"In welchem Land liegt dieser Nationalpark?",'
    'desc:"Serengeti, Yellowstone, Kruger \\u2014 richtig zuordnen.",'
    'prompt_en:"In which country is this national park?"},\n'
    '    {id:"npark_match_kontinent",icon:"\\u{1F30D}",title:"Nationalparks: Kontinent",'
    'group:"nparks",prompt:"Auf welchem Kontinent liegt dieser Nationalpark?",'
    'desc:"Afrika, Asien, Amerika \\u2014 erkenne den Kontinent.",'
    'prompt_en:"On which continent is this national park?"},\n'
    '    {id:"npark_match_oekosystem",icon:"\\u{1F333}",title:"Nationalparks: \\u00d6kosystem",'
    'group:"nparks",prompt:"Welches \\u00d6kosystem hat dieser Nationalpark?",'
    'desc:"Regenwald, Steppe, Gebirge \\u2014 erkenne das \\u00d6kosystem.",'
    'prompt_en:"What ecosystem does this national park have?"},\n'
    '    {id:"npark_pin_lage",icon:"\\u{1F4CD}",title:"Nationalparks: Lage pinnen",'
    'group:"nparks",prompt:"Wo auf der Welt liegt dieser Nationalpark?",'
    'desc:"Pinne den Nationalpark auf der Weltkarte.",'
    'prompt_en:"Where in the world is this national park?"},\n'
    '    {id:"ws_npark_yellowstone",icon:"\\u{1F332}",title:"WS: Yellowstone",'
    'group:"nparks",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus YELLOWSTONE!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben",'
    'prompt_en:"Form words from YELLOWSTONE!"},'
)

# 2.9 MODE_CATS
CATS_OLD = (
    'fluesse:{label:"Fl\\u00fcsse & Gew\\u00e4sser",icon:"\\u{1F30A}",'
    'modes:["hl_fluss_laenge","hl_fluss_einzug","fluss_match_kontinent","fluss_match_land",'
    '"fluss_match_muendung","fluss_pin_muendung","ws_fluss_amazonas"],cost:0},'
)
CATS_NEW = (
    CATS_OLD +
    '\n  nparks:{label:"Nationalparks weltweit",icon:"\\u{1F332}",'
    'modes:["hl_npark_flaeche","hl_npark_gruendung","npark_match_land","npark_match_kontinent",'
    '"npark_match_oekosystem","npark_pin_lage","ws_npark_yellowstone"],cost:0},'
)

# 2.10 GEN Dispatcher
DISP_OLD = (
    'ws_fluss_amazonas:()=>{initFluessWS("amazonas");return null;},'
)
DISP_NEW = (
    DISP_OLD +
    '\n  /* Phase 444: Nationalparks */\n'
    '  hl_npark_flaeche:()=>genNparksHLExt("flaeche_km2",{unit:"km\\u00b2",prompt:_tc("Welcher Nationalpark ist gr\\u00f6\\u00dfer?")}),\n'
    '  hl_npark_gruendung:()=>genNparksHLExt("gruendung",{lowerWins:true,unit:"",prompt:_tc("Welcher Nationalpark wurde fr\\u00fcher gegr\\u00fcndet?")}),\n'
    '  npark_match_land:()=>genNparksMatchExt("land",_tc("In welchem Land liegt dieser Nationalpark?")),\n'
    '  npark_match_kontinent:()=>genNparksMatchExt("kontinent",_tc("Auf welchem Kontinent liegt dieser Nationalpark?"),["Nordamerika","S\\u00fcdamerika","Europa","Afrika","Asien","Ozeanien","Arktis"]),\n'
    '  npark_match_oekosystem:()=>genNparksMatchExt("oekosystem",_tc("Welches \\u00d6kosystem hat dieser Nationalpark?")),\n'
    '  npark_pin_lage:()=>genNparksPinQ(),\n'
    '  ws_npark_yellowstone:()=>{initNparksWS("yellowstone");return null;},'
)

# 2.11 Replace-Kette
REPL_OLD = "  .replace('PLACEHOLDER_FLUESSE',        FLUESSE_J)"
REPL_NEW = (
    "  .replace('PLACEHOLDER_FLUESSE',        FLUESSE_J)\n"
    "  .replace('PLACEHOLDER_NPARKS_WS',      NPARKS_WS_J)\n"
    "  .replace('PLACEHOLDER_NPARKS',         NPARKS_J)"
)

patch(GEN, [
    (LOAD_OLD,       LOAD_NEW,        'Py: nparks + nparks_ws laden'),
    (LL_OLD,         LL_NEW,          'JS: LAND_LATLON + 14 Länder'),
    (CONST_OLD,      CONST_NEW,       'JS: NPARKS Konstanten'),
    (MKWS_OLD,       MKWS_NEW,        'JS: initNparksWS'),
    (GEN_FN_OLD,     GEN_FN_NEW,      'JS: genNparksHLExt + Match + Pin'),
    (I18N_PL_OLD,    I18N_PL_NEW,     'i18n PL: 6 Nparks-Strings'),
    (I18N_EN_OLD,    I18N_EN_NEW,     'i18n EN: 6 Nparks-Strings'),
    (MODES_OLD,      MODES_NEW,       'MODES: 7 Nparks-Modi'),
    (CATS_OLD,       CATS_NEW,        'MODE_CATS: nparks'),
    (DISP_OLD,       DISP_NEW,        'GEN dispatch: 7 Nparks-Modi'),
    (REPL_OLD,       REPL_NEW,        'Replace-Kette: NPARKS_WS + NPARKS'),
])

print('\nPatch 444 fertig!')
