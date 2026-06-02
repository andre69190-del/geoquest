#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase: 443
Date:  2026-06-02
Scope: Flüsse & Gewässer — 7 neue Modi + fluesse_extended.json (80 Weltflüsse)

Modi: hl_fluss_laenge, hl_fluss_einzug, fluss_match_kontinent,
      fluss_match_land, fluss_match_muendung, fluss_pin_mündung, ws_fluss_amazonas

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

VC_CHECK_OLD = 'def check_hunde_extended(filename, data):'
VC_CHECK_NEW = '''\
def check_fluesse_extended(filename, data):
    """Validiert data/fluesse_extended.json."""
    REQUIRED = ['laenge_km', 'einzugsgebiet_km2', 'kontinent',
                'hauptland', 'muendung', 'lat', 'lng']
    KONT_ENUM = {'Afrika','Asien','Europa','Nordamerika','Südamerika','Australien'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'muss ein Dict sein')
        return
    for name, e in data.items():
        if not isinstance(e, dict):
            warn(filename, 'eintrag', name, 'kein Dict'); continue
        for f in REQUIRED:
            if f not in e:
                warn(filename, 'pflichtfeld', name, f"Feld '{f}' fehlt")
        k = e.get('kontinent')
        if k and k not in KONT_ENUM:
            warn(filename, 'enum:kontinent', name, f"'{k}' ungültig")
        for num_f in ('laenge_km', 'einzugsgebiet_km2'):
            v = e.get(num_f)
            if v is not None and not isinstance(v, (int, float)):
                warn(filename, 'typ:'+num_f, name, f'Muss Zahl sein')
        for coord_f in ('lat', 'lng'):
            v = e.get(coord_f)
            if v is not None and not isinstance(v, (int, float)):
                warn(filename, 'typ:'+coord_f, name, f'Muss Float sein')


def check_hunde_extended(filename, data):'''

VC_DISP_OLD = (
    '    elif name == "hunde_extended.json":\n'
    '        check_hunde_extended(filename, data)\n'
)
VC_DISP_NEW = (
    '    elif name == "fluesse_extended.json":\n'
    '        check_fluesse_extended(filename, data)\n'
    '    elif name == "hunde_extended.json":\n'
    '        check_hunde_extended(filename, data)\n'
)

patch(VC, [
    (VC_CHECK_OLD, VC_CHECK_NEW, 'VC: check_fluesse_extended'),
    (VC_DISP_OLD,  VC_DISP_NEW,  'VC: dispatch fluesse'),
])


# ── 2. gen.py ─────────────────────────────────────────────────────────────
print('\n-- 2. gen.py --')

# 2.1 Python Loader
LOAD_OLD = (
    "        GARTEN_WS_J = __import__('json').dumps(__import__('json').load(_gwf),"
    " ensure_ascii=False, separators=(',','::'))"
)
raw = open(GEN, encoding='utf-8').read()
if LOAD_OLD not in raw:
    LOAD_OLD = (
        "        GARTEN_WS_J = __import__('json').dumps(__import__('json').load(_gwf),"
        " ensure_ascii=False, separators=(',',':'))"
    )

LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/fluesse_extended.json'), 'r', encoding='utf-8') as _flf:\n"
    "        FLUESSE_J = __import__('json').dumps(__import__('json').load(_flf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/fluesse_ws.json'), 'r', encoding='utf-8') as _flwf:\n"
    "        FLUESSE_WS_J = __import__('json').dumps(__import__('json').load(_flwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

# 2.2 LAND_LATLON erweitern (9 fehlende Länder)
LL_OLD = '"Pazifik":[-15.0,-170.0]\n};'
LL_NEW = (
    '"Pazifik":[-15.0,-170.0],\n'
    '  "Demokratische Republik Kongo":[-4.038,21.758],'
    '"Papua-Neuguinea":[-6.315,143.956],\n'
    '  "Moldau":[47.411,28.369],"Mosambik":[-18.665,35.530],'
    '"Bangladesch":[23.685,90.356],\n'
    '  "Myanmar":[21.914,95.956],"Pakistan":[30.375,69.345],'
    '"Irak":[33.223,43.679],"Venezuela":[6.424,-66.589]\n'
    '};'
)

# 2.3 JS Konstanten
CONST_OLD = '"Pazifik":[-15.0,-170.0]\n};\n\n\n/* =='
CONST_NEW = (
    '"Pazifik":[-15.0,-170.0],\n'
    '  "Demokratische Republik Kongo":[-4.038,21.758],'
    '"Papua-Neuguinea":[-6.315,143.956],\n'
    '  "Moldau":[47.411,28.369],"Mosambik":[-18.665,35.530],'
    '"Bangladesch":[23.685,90.356],\n'
    '  "Myanmar":[21.914,95.956],"Pakistan":[30.375,69.345],'
    '"Irak":[33.223,43.679],"Venezuela":[6.424,-66.589]\n'
    '};\n'
    'const FLUESSE_WS_DATA=PLACEHOLDER_FLUESSE_WS;\n'
    'const FLUESSE_DATA=PLACEHOLDER_FLUESSE;\n'
    '\n\n/* =='
)

# 2.4 _mkWS Init
MKWS_OLD = 'var initGartenWS=_mkWS(GARTEN_WS_DATA,"Garten");'
MKWS_NEW = (
    'var initGartenWS=_mkWS(GARTEN_WS_DATA,"Garten");\n'
    'var initFluessWS=_mkWS(FLUESSE_WS_DATA,"Fluesse");'
)

# 2.5 Generator-Funktionen
GEN_FN_OLD = 'window.genLitPinQ=genLitPinQ;'
GEN_FN_NEW = (
    'window.genLitPinQ=genLitPinQ;\n'
    '\n'
    '/* Phase 443: Flüsse & Gewässer */\n'
    'function genFluessHLExt(field,opts){var o=opts||{};var items=[];var _FD=FLUESSE_DATA;\n'
    '  var _ks=Object.keys(_FD).filter(function(k){return Object.prototype.hasOwnProperty.call(_FD,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_FD[_n][field]);if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" \\u00b7 "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welcher Fluss ist l\\u00e4nger?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"fluss_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genFluessHLExt=genFluessHLExt;\n'
    '\n'
    'function genFluessMatchExt(field,prompt,fixedPool){var _FD=FLUESSE_DATA;\n'
    '  var valid=Object.keys(_FD).filter(function(k){return Object.prototype.hasOwnProperty.call(_FD,k)&&_FD[k][field]!=null&&_FD[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_FD[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_FD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"fluss_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genFluessMatchExt=genFluessMatchExt;\n'
    '\n'
    'function genFlussPinQ(){var _FD=FLUESSE_DATA;\n'
    '  var keys=Object.keys(_FD).filter(function(k){return Object.prototype.hasOwnProperty.call(_FD,k)&&_FD[k].lat&&_FD[k].lng;});\n'
    '  if(keys.length<4)return null;\n'
    '  var idx=~~(rng()*keys.length),name=keys[idx],e=_FD[name];\n'
    '  return{type:"uk_pin",cat:"fluesse",prompt:_tc("Wo liegt die M\\u00fcndung dieses Flusses?"),\n'
    '    subj:name,lat:e.lat,lng:e.lng,lid:"flusspin_"+idx,cc:"de"};\n'
    '}\n'
    'window.genFlussPinQ=genFlussPinQ;'
)

# 2.6 i18n PL
I18N_PL_OLD = (
    '"Aus welcher Region der Welt stammt diese Pflanze?":"Z jakiego regionu świata pochodzi ta roślina?"'
    '},"en":{"Welche Serie'
)
I18N_PL_NEW = (
    '"Aus welcher Region der Welt stammt diese Pflanze?":"Z jakiego regionu świata pochodzi ta roślina?",'
    '"Welcher Fluss ist l\\u00e4nger?":"Która rzeka jest dłuższa?",'
    '"Welcher Fluss hat das größere Einzugsgebiet?":"Która rzeka ma większy obszar dorzecza?",'
    '"Auf welchem Kontinent liegt dieser Fluss?":"Na jakim kontynencie leży ta rzeka?",'
    '"In welchem Land mündet dieser Fluss?":"W jakim kraju wpada ta rzeka?",'
    '"Wohin mündet dieser Fluss?":"Gdzie wpada ta rzeka?",'
    '"Wo liegt die Mündung dieses Flusses?":"Gdzie leży ujście tej rzeki?"'
    '},"en":{"Welche Serie'
)

# 2.7 i18n EN
I18N_EN_OLD = (
    '"Aus welcher Region der Welt stammt diese Pflanze?":"Which region of the world does this plant come from?"'
    '}};'
)
I18N_EN_NEW = (
    '"Aus welcher Region der Welt stammt diese Pflanze?":"Which region of the world does this plant come from?",'
    '"Welcher Fluss ist l\\u00e4nger?":"Which river is longer?",'
    '"Welcher Fluss hat das größere Einzugsgebiet?":"Which river has the larger drainage basin?",'
    '"Auf welchem Kontinent liegt dieser Fluss?":"On which continent is this river located?",'
    '"In welchem Land mündet dieser Fluss?":"In which country does this river empty?",'
    '"Wohin mündet dieser Fluss?":"Where does this river empty into?",'
    '"Wo liegt die Mündung dieses Flusses?":"Where is the mouth of this river?"'
    '}};'
)

# 2.8 MODES
MODES_OLD = (
    '{id:"garten_pin_region",icon:"\\u{1F33F}",title:"Gartenbau: Region pinnen",'
    'group:"gartenbau",prompt:"Aus welcher Region der Welt stammt diese Pflanze?",'
    'desc:"Pinne die Ursprungsregion auf der Weltkarte.",'
    'prompt_en:"Which region of the world does this plant come from?"},'
)
MODES_NEW = (
    MODES_OLD +
    '\n    /* Phase 443: Flüsse & Gewässer */\n'
    '    {id:"hl_fluss_laenge",icon:"\\u{1F30A}",title:"Fl\\u00fcsse: L\\u00e4nge",'
    'group:"fluesse",prompt:"Welcher Fluss ist l\\u00e4nger?",'
    'desc:"Nil, Amazonas, Rhein \\u2014 welcher ist wirklich l\\u00e4nger?",'
    'prompt_en:"Which river is longer?"},\n'
    '    {id:"hl_fluss_einzug",icon:"\\u{1F30A}",title:"Fl\\u00fcsse: Einzugsgebiet",'
    'group:"fluesse",prompt:"Welcher Fluss hat das gr\\u00f6\\u00dfere Einzugsgebiet?",'
    'desc:"Fl\\u00e4che des gesamten Einzugsgebiets in km\\u00b2.",'
    'prompt_en:"Which river has the larger drainage basin?"},\n'
    '    {id:"fluss_match_kontinent",icon:"\\u{1F30D}",title:"Fl\\u00fcsse: Kontinent",'
    'group:"fluesse",prompt:"Auf welchem Kontinent liegt dieser Fluss?",'
    'desc:"Afrika, Asien, Europa \\u2014 erkenne den Kontinent.",'
    'prompt_en:"On which continent is this river located?"},\n'
    '    {id:"fluss_match_land",icon:"\\u{1F30D}",title:"Fl\\u00fcsse: M\\u00fcndungsland",'
    'group:"fluesse",prompt:"In welchem Land m\\u00fcndet dieser Fluss?",'
    'desc:"Wo endet der Fluss \\u2014 im richtigen Land?",'
    'prompt_en:"In which country does this river empty?"},\n'
    '    {id:"fluss_match_muendung",icon:"\\u{1F4A7}",title:"Fl\\u00fcsse: M\\u00fcndung",'
    'group:"fluesse",prompt:"Wohin m\\u00fcndet dieser Fluss?",'
    'desc:"Meer, Ozean oder See \\u2014 das Ziel des Flusses.",'
    'prompt_en:"Where does this river empty into?"},\n'
    '    {id:"fluss_pin_muendung",icon:"\\u{1F4CD}",title:"Fl\\u00fcsse: M\\u00fcndung pinnen",'
    'group:"fluesse",prompt:"Wo liegt die M\\u00fcndung dieses Flusses?",'
    'desc:"Pinne die M\\u00fcndung auf der Weltkarte.",'
    'prompt_en:"Where is the mouth of this river?"},\n'
    '    {id:"ws_fluss_amazonas",icon:"\\u{1F30A}",title:"WS: Amazonas",'
    'group:"fluesse",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus AMAZONAS!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 8 Buchstaben",'
    'prompt_en:"Form words from AMAZONAS!"},'
)

# 2.9 MODE_CATS
CATS_OLD = (
    'gartenbau:{label:"Gartenbau & Botanik",icon:"\\u{1F33F}",'
    'modes:["hl_garten_hoehe","hl_garten_bluete","garten_match_wasser","garten_match_boden",'
    '"garten_match_region","ws_garten_rhodo","ws_garten_strelitzie","garten_pin_region"],cost:0},'
)
CATS_NEW = (
    CATS_OLD +
    '\n  fluesse:{label:"Fl\\u00fcsse & Gew\\u00e4sser",icon:"\\u{1F30A}",'
    'modes:["hl_fluss_laenge","hl_fluss_einzug","fluss_match_kontinent","fluss_match_land",'
    '"fluss_match_muendung","fluss_pin_muendung","ws_fluss_amazonas"],cost:0},'
)

# 2.10 GEN Dispatcher
DISP_OLD = (
    'garten_pin_region:()=>genExtPinByLand(GARTEN_DATA,"ursprungsregion","gartenbau",'
    '_tc("Aus welcher Region der Welt stammt diese Pflanze?"),"gartenpin"),'
)
DISP_NEW = (
    DISP_OLD +
    '\n  /* Phase 443: Flüsse & Gewässer */\n'
    '  hl_fluss_laenge:()=>genFluessHLExt("laenge_km",{unit:"km",prompt:_tc("Welcher Fluss ist l\\u00e4nger?")}),\n'
    '  hl_fluss_einzug:()=>genFluessHLExt("einzugsgebiet_km2",{unit:"km\\u00b2",prompt:_tc("Welcher Fluss hat das gr\\u00f6\\u00dfere Einzugsgebiet?")}),\n'
    '  fluss_match_kontinent:()=>genFluessMatchExt("kontinent",_tc("Auf welchem Kontinent liegt dieser Fluss?"),["Afrika","Asien","Europa","Nordamerika","S\\u00fcdamerika","Australien"]),\n'
    '  fluss_match_land:()=>genFluessMatchExt("hauptland",_tc("In welchem Land m\\u00fcndet dieser Fluss?")),\n'
    '  fluss_match_muendung:()=>genFluessMatchExt("muendung",_tc("Wohin m\\u00fcndet dieser Fluss?")),\n'
    '  fluss_pin_muendung:()=>genFlussPinQ(),\n'
    '  ws_fluss_amazonas:()=>{initFluessWS("amazonas");return null;},'
)

# 2.11 Replace-Kette
REPL_OLD = "  .replace('PLACEHOLDER_GARTEN',         GARTEN_J)"
REPL_NEW = (
    "  .replace('PLACEHOLDER_GARTEN',         GARTEN_J)\n"
    "  .replace('PLACEHOLDER_FLUESSE_WS',     FLUESSE_WS_J)\n"
    "  .replace('PLACEHOLDER_FLUESSE',        FLUESSE_J)"
)

patch(GEN, [
    (LOAD_OLD,   LOAD_NEW,   'Py: fluesse + fluesse_ws laden'),
    (CONST_OLD,  CONST_NEW,  'JS: LAND_LATLON + FLUESSE Konstanten'),
    (MKWS_OLD,   MKWS_NEW,   'JS: initFluessWS'),
    (GEN_FN_OLD, GEN_FN_NEW, 'JS: genFluessHLExt + Match + Pin'),
    (I18N_PL_OLD,I18N_PL_NEW,'i18n PL: 7 Fluss-Strings'),
    (I18N_EN_OLD,I18N_EN_NEW,'i18n EN: 7 Fluss-Strings'),
    (MODES_OLD,  MODES_NEW,  'MODES: 7 Fluss-Modi'),
    (CATS_OLD,   CATS_NEW,   'MODE_CATS: fluesse'),
    (DISP_OLD,   DISP_NEW,   'GEN dispatch: 7 Fluss-Modi'),
    (REPL_OLD,   REPL_NEW,   'Replace-Kette: FLUESSE_WS + FLUESSE'),
])

print('\nPatch 443 fertig!')
