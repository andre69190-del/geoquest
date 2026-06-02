#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 438 - gen.py Integration (JSON/VC bereits gepatcht).
   Integriert Freizeitparks & Kunstgeschichte in gen.py.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, 'gen.py')


def patch(path, edits):
    c = open(path, 'r', encoding='utf-8').read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, 'Anker "%s" count=%d (erwartet 1)' % (tag, n)
        c = c.replace(old, new)
        print('  OK  ' + tag)
    open(path, 'w', encoding='utf-8').write(c)


# ── 1. Python-Loader ─────────────────────────────────────────────────────────
LOAD_OLD = (
    "        SERIEN_EXT_J = __import__('json').dumps(__import__('json').load(_serf),"
    " ensure_ascii=False, separators=(',','::'))"
)
# Fix: check if it uses single or double colon separator
import re
raw = open(GEN, encoding='utf-8').read()
m = re.search(r"SERIEN_EXT_J = __import__\('json'\)\.dumps.*?separators=\('[^']*','([^']*)'\)\)", raw)
sep = m.group(1) if m else ':'
LOAD_OLD = (
    "        SERIEN_EXT_J = __import__('json').dumps(__import__('json').load(_serf),"
    " ensure_ascii=False, separators=(',','" + sep + "'))"
)
LOAD_NEW = (
    "        SERIEN_EXT_J = __import__('json').dumps(__import__('json').load(_serf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/themeparks_extended.json'), 'r', encoding='utf-8') as _tpf:\n"
    "        PARKS_J = __import__('json').dumps(__import__('json').load(_tpf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/kunst_extended.json'), 'r', encoding='utf-8') as _kef:\n"
    "        KUNST_J = __import__('json').dumps(__import__('json').load(_kef),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/themeparks_ws.json'), 'r', encoding='utf-8') as _tpwf:\n"
    "        PARKS_WS_J = __import__('json').dumps(__import__('json').load(_tpwf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/kunst_ws.json'), 'r', encoding='utf-8') as _kwf:\n"
    "        KUNST_WS_J = __import__('json').dumps(__import__('json').load(_kwf),"
    " ensure_ascii=False, separators=(',','::'))"
)
LOAD_NEW = LOAD_NEW.replace(" separators=(',','::'))", " separators=(',','::'))")
LOAD_NEW = (
    "        SERIEN_EXT_J = __import__('json').dumps(__import__('json').load(_serf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/themeparks_extended.json'), 'r', encoding='utf-8') as _tpf:\n"
    "        PARKS_J = __import__('json').dumps(__import__('json').load(_tpf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/kunst_extended.json'), 'r', encoding='utf-8') as _kef:\n"
    "        KUNST_J = __import__('json').dumps(__import__('json').load(_kef),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/themeparks_ws.json'), 'r', encoding='utf-8') as _tpwf:\n"
    "        PARKS_WS_J = __import__('json').dumps(__import__('json').load(_tpwf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/kunst_ws.json'), 'r', encoding='utf-8') as _kwf:\n"
    "        KUNST_WS_J = __import__('json').dumps(__import__('json').load(_kwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

# ── 2. JS-Konstanten ─────────────────────────────────────────────────────────
CONST_OLD = "const TIMELINE_DATA=PLACEHOLDER_TIMELINE;"
CONST_NEW = (
    "const TIMELINE_DATA=PLACEHOLDER_TIMELINE;\n"
    "const PARKS_WS_DATA=PLACEHOLDER_PARKS_WS;\n"
    "const PARKS_DATA=PLACEHOLDER_PARKS;\n"
    "const KUNST_WS_DATA=PLACEHOLDER_KUNST_WS;\n"
    "const KUNST_DATA=PLACEHOLDER_KUNST;"
)

# ── 3. _mkWS Inits ───────────────────────────────────────────────────────────
MKWS_OLD = 'var initArchitekturWS=_mkWS(ARCHITEKTUR_WS_DATA,"Architektur");'
MKWS_NEW = (
    'var initArchitekturWS=_mkWS(ARCHITEKTUR_WS_DATA,"Architektur");\n'
    'var initParksWS=_mkWS(PARKS_WS_DATA,"Parks");\n'
    'var initKunstWS=_mkWS(KUNST_WS_DATA,"Kunst");'
)

# ── 4. Generator-Funktionen ──────────────────────────────────────────────────
GEN_ANCHOR = 'window.genSerienMatchExt=genSerienMatchExt;'
GEN_NEW = (
    'window.genSerienMatchExt=genSerienMatchExt;\n'
    '\n'
    '/* Phase 438: genParksHLExt / genParksMatchExt */\n'
    'function genParksHLExt(field,opts){var o=opts||{};var items=[];var _PD=PARKS_DATA;\n'
    '  var _ks=Object.keys(_PD).filter(function(k){return Object.prototype.hasOwnProperty.call(_PD,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_PD[_n][field]);if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welcher Park ist h\\u00f6her?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"park_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genParksHLExt=genParksHLExt;\n'
    '\n'
    'function genParksMatchExt(field,prompt,fixedPool){var _PD=PARKS_DATA;\n'
    '  var valid=Object.keys(_PD).filter(function(k){return Object.prototype.hasOwnProperty.call(_PD,k)&&_PD[k][field]!=null&&_PD[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_PD[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_PD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"park_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genParksMatchExt=genParksMatchExt;\n'
    '\n'
    '/* Phase 438: genKunstHLExt / genKunstMatchExt */\n'
    'function genKunstHLExt(field,opts){var o=opts||{};var items=[];var _KD=KUNST_DATA;\n'
    '  var _ks=Object.keys(_KD).filter(function(k){return Object.prototype.hasOwnProperty.call(_KD,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_KD[_n][field]);\n'
    '    if(!isNaN(_v)&&_v!==0)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.3));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"";\n'
    '    var fa=a.val<0?Math.abs(a.val)+" v.Chr.":a.val+(unit?" "+unit:"");\n'
    '    var fb=b.val<0?Math.abs(b.val)+" v.Chr.":b.val+(unit?" "+unit:"");\n'
    '    var meta=a.name+": "+fa+" · "+b.name+": "+fb;\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welches Kunstwerk ist \\u00e4lter?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"kunst_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genKunstHLExt=genKunstHLExt;\n'
    '\n'
    'function genKunstMatchExt(field,prompt,fixedPool){var _KD=KUNST_DATA;\n'
    '  var valid=Object.keys(_KD).filter(function(k){return Object.prototype.hasOwnProperty.call(_KD,k)&&_KD[k][field]!=null&&_KD[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_KD[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_KD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"kunst_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genKunstMatchExt=genKunstMatchExt;'
)

# ── 5. i18n PL ───────────────────────────────────────────────────────────────
I18N_PL_OLD = (
    '"Welches Tier ist mit dieser Gottheit verbunden?":"Jakie zwierzę jest związane z tym bóstwem?"},"en"'
)
I18N_PL_NEW = (
    '"Welches Tier ist mit dieser Gottheit verbunden?":"Jakie zwierzę jest związane z tym bóstwem?",'
    '"Welche Achterbahn ist schneller?":"Który roller coaster jest szybszy?",'
    '"Welcher Freizeitpark ist höher?":"Który park rozrywki jest wyższy?",'
    '"Welche Achterbahn hat mehr Inversionen?":"Który roller coaster ma więcej inwersji?",'
    '"Welcher Freizeitpark ist älter?":"Który park rozrywki jest starszy?",'
    '"Aus welchem Land stammt dieser Freizeitpark?":"Z jakiego kraju pochodzi ten park rozrywki?",'
    '"Welchem Typ gehört diese Attraktion an?":"Do jakiego typu należy ta atrakcja?",'
    '"Welches Kunstwerk ist älter?":"Które dzieło sztuki jest starsze?",'
    '"Welches Kunstwerk hat einen höheren Schätzwert?":"Które dzieło sztuki ma wyższą wartość?",'
    '"Wer hat dieses Kunstwerk erschaffen?":"Kto stworzył to dzieło sztuki?",'
    '"Welcher Kunstepoche gehört dieses Werk an?":"Do jakiej epoki artystycznej należy to dzieło?",'
    '"In welchem Museum befindet sich dieses Werk?":"W którym muzeum znajduje się to dzieło?"'
    '},"en"'
)

# ── 6. i18n EN ───────────────────────────────────────────────────────────────
I18N_EN_OLD = (
    '"Welches Tier ist mit dieser Gottheit verbunden?":"Which animal is associated with this deity?"}};'
)
I18N_EN_NEW = (
    '"Welches Tier ist mit dieser Gottheit verbunden?":"Which animal is associated with this deity?",'
    '"Welche Achterbahn ist schneller?":"Which roller coaster is faster?",'
    '"Welcher Freizeitpark ist höher?":"Which amusement park ride is higher?",'
    '"Welche Achterbahn hat mehr Inversionen?":"Which roller coaster has more inversions?",'
    '"Welcher Freizeitpark ist älter?":"Which amusement park is older?",'
    '"Aus welchem Land stammt dieser Freizeitpark?":"Which country is this amusement park from?",'
    '"Welchem Typ gehört diese Attraktion an?":"Which type does this attraction belong to?",'
    '"Welches Kunstwerk ist älter?":"Which artwork is older?",'
    '"Welches Kunstwerk hat einen höheren Schätzwert?":"Which artwork has a higher estimated value?",'
    '"Wer hat dieses Kunstwerk erschaffen?":"Who created this artwork?",'
    '"Welcher Kunstepoche gehört dieses Werk an?":"Which art epoch does this work belong to?",'
    '"In welchem Museum befindet sich dieses Werk?":"In which museum is this work located?"'
    '}};'
)

# ── 7. MODES Array ───────────────────────────────────────────────────────────
MODES_ANCHOR = (
    '    {id:"myth_match_tier",icon:"\\u{1F98A}",title:"Mythologie: Tier-Symbol",'
    'group:"mythologie",prompt:"Welches Tier ist mit dieser Gottheit verbunden?",'
    'desc:"Adler, Eule, Schlange \\u2014 erkenne das Tier-Symbol.",'
    'prompt_en:"Which animal is associated with this deity?"},'
)
MODES_NEW = (
    MODES_ANCHOR +
    '\n    /* Phase 438: Freizeitparks & Achterbahnen */\n'
    '    {id:"hl_park_speed",icon:"\\u{1F3A2}",title:"Freizeitpark: Topspeed",'
    'group:"themeparks",prompt:"Welche Achterbahn ist schneller?",'
    'desc:"km/h \\u2014 von Steel Vengeance bis Formula Rossa.",'
    'prompt_en:"Which roller coaster is faster?"},\n'
    '    {id:"hl_park_hoehe",icon:"\\u{1F3A2}",title:"Freizeitpark: H\\u00f6he",'
    'group:"themeparks",prompt:"Welcher Freizeitpark ist h\\u00f6her?",'
    'desc:"H\\u00f6he der Anlage in Metern.",'
    'prompt_en:"Which amusement park ride is higher?"},\n'
    '    {id:"hl_park_inversionen",icon:"\\u{1F503}",title:"Freizeitpark: Inversionen",'
    'group:"themeparks",prompt:"Welche Achterbahn hat mehr Inversionen?",'
    'desc:"Loopings & Korkenzieher z\\u00e4hlen!",'
    'prompt_en:"Which roller coaster has more inversions?"},\n'
    '    {id:"hl_park_baujahr",icon:"\\u{1F4C5}",title:"Freizeitpark: \\u00c4ltester Park",'
    'group:"themeparks",prompt:"Welcher Freizeitpark ist \\u00e4lter?",'
    'desc:"Fr\\u00fcheres Baujahr = Sieger (lowerWins).",'
    'prompt_en:"Which amusement park is older?"},\n'
    '    {id:"park_match_land",icon:"\\u{1F30D}",title:"Freizeitpark: Land",'
    'group:"themeparks",prompt:"Aus welchem Land stammt dieser Freizeitpark?",'
    'desc:"Von DACH bis Japan \\u2014 erkenne das Herkunftsland.",'
    'prompt_en:"Which country is this amusement park from?"},\n'
    '    {id:"park_match_kategorie",icon:"\\u{1F3A0}",title:"Freizeitpark: Typ",'
    'group:"themeparks",prompt:"Welchem Typ geh\\u00f6rt diese Attraktion an?",'
    'desc:"Achterbahn, Wasserbahn, Darkride oder Park?",'
    'prompt_en:"Which type does this attraction belong to?"},\n'
    '    {id:"timeline_park_baujahr",icon:"\\u{1F3A2}",title:"Freizeitpark-Timeline",'
    'group:"themeparks",prompt:"Welcher Park / welche Bahn ist \\u00e4lter?",'
    'desc:"Von Tivoli 1843 bis Movie Park 1996.",'
    'prompt_en:"Which park/coaster is older?"},\n'
    '    {id:"ws_park_achterbahn",icon:"\\u{1F3A2}",title:"WS: Achterbahn",'
    'group:"themeparks",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus ACHTERBAHN!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben",'
    'prompt_en:"Form words from ACHTERBAHN!"},\n'
    '    /* Phase 438: Kunstgeschichte */\n'
    '    {id:"hl_kunst_jahr",icon:"\\u{1F5BC}\\uFE0F",title:"Kunstgeschichte: \\u00c4lteres Werk",'
    'group:"kunst",prompt:"Welches Kunstwerk ist \\u00e4lter?",'
    'desc:"Fr\\u00fcheres Entstehungsjahr = Sieger. Auch v.Chr.!",'
    'prompt_en:"Which artwork is older?"},\n'
    '    {id:"hl_kunst_wert",icon:"\\u{1F4B0}",title:"Kunstgeschichte: Sch\\u00e4tzwert",'
    'group:"kunst",prompt:"Welches Kunstwerk hat einen h\\u00f6heren Sch\\u00e4tzwert?",'
    'desc:"Gesch\\u00e4tzter Marktwert in Mio. USD.",'
    'prompt_en:"Which artwork has a higher estimated value?"},\n'
    '    {id:"kunst_match_kuenstler",icon:"\\u{1F58C}\\uFE0F",title:"Kunstgeschichte: K\\u00fcnstler",'
    'group:"kunst",prompt:"Wer hat dieses Kunstwerk erschaffen?",'
    'desc:"Von Da Vinci bis Banksy \\u2014 erkenne den K\\u00fcnstler.",'
    'prompt_en:"Who created this artwork?"},\n'
    '    {id:"kunst_match_epoche",icon:"\\u{1F3DB}\\uFE0F",title:"Kunstgeschichte: Epoche",'
    'group:"kunst",prompt:"Welcher Kunstepoche geh\\u00f6rt dieses Werk an?",'
    'desc:"Renaissance, Barock, Impressionismus & Co.",'
    'prompt_en:"Which art epoch does this work belong to?"},\n'
    '    {id:"kunst_match_museum",icon:"\\u{1F3DB}\\uFE0F",title:"Kunstgeschichte: Museum",'
    'group:"kunst",prompt:"In welchem Museum befindet sich dieses Werk?",'
    'desc:"Louvre, Prado, MoMA \\u2014 erkenne den Standort.",'
    'prompt_en:"In which museum is this work located?"},\n'
    '    {id:"timeline_kunst_jahr",icon:"\\u{1F5BC}\\uFE0F",title:"Kunst-Timeline",'
    'group:"kunst",prompt:"Welches Kunstwerk ist \\u00e4lter?",'
    'desc:"Von der Antike bis zur Moderne \\u2014 Kunstgeschichte sortieren.",'
    'prompt_en:"Which artwork is older?"},\n'
    '    {id:"ws_kunst_renaissance",icon:"\\u{1F3AD}",title:"WS: Renaissance",'
    'group:"kunst",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus RENAISSANCE!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben",'
    'prompt_en:"Form words from RENAISSANCE!"},'
)

# ── 8. MODE_CATS ─────────────────────────────────────────────────────────────
CATS_ANCHOR = (
    '  webkultur:{label:"Webkultur & Social Media",icon:"\\u{1F4F1}",'
    'modes:["hl_web_reichweite","hl_web_start","web_match_land","web_match_kategorie",'
    '"timeline_web_start","ws_web_algorithmus"],cost:0},'
)
CATS_NEW = (
    CATS_ANCHOR + '\n'
    '  themeparks:{label:"Freizeitparks & Achterbahnen",icon:"\\u{1F3A2}",'
    'modes:["hl_park_speed","hl_park_hoehe","hl_park_inversionen","hl_park_baujahr",'
    '"park_match_land","park_match_kategorie","timeline_park_baujahr","ws_park_achterbahn"],cost:0},\n'
    '  kunst:{label:"Kunstgeschichte",icon:"\\u{1F5BC}\\uFE0F",'
    'modes:["hl_kunst_jahr","hl_kunst_wert","kunst_match_kuenstler","kunst_match_epoche",'
    '"kunst_match_museum","timeline_kunst_jahr","ws_kunst_renaissance"],cost:0},'
)

# ── 9. Dispatcher ────────────────────────────────────────────────────────────
DISP_ANCHOR = '  ws_arch_fundament:()=>{initArchitekturWS("fundament");return null;},'
DISP_NEW = (
    '  ws_arch_fundament:()=>{initArchitekturWS("fundament");return null;},\n'
    '  /* Phase 438: Freizeitparks */\n'
    '  hl_park_speed:()=>genParksHLExt("max_speed_kmh",{unit:"km/h",'
    'prompt:_tc("Welche Achterbahn ist schneller?")}),\n'
    '  hl_park_hoehe:()=>genParksHLExt("max_hoehe_m",{unit:"m",'
    'prompt:_tc("Welcher Freizeitpark ist h\\u00f6her?")}),\n'
    '  hl_park_inversionen:()=>genParksHLExt("inversionen",{unit:"",'
    'prompt:_tc("Welche Achterbahn hat mehr Inversionen?")}),\n'
    '  hl_park_baujahr:()=>genParksHLExt("baujahr",{lowerWins:true,unit:"",'
    'prompt:_tc("Welcher Freizeitpark ist \\u00e4lter?")}),\n'
    '  park_match_land:()=>genParksMatchExt("park_land",'
    '_tc("Aus welchem Land stammt dieser Freizeitpark?")),\n'
    '  park_match_kategorie:()=>genParksMatchExt("kategorie",'
    '_tc("Welchem Typ geh\\u00f6rt diese Attraktion an?"),'
    '["Achterbahn","Wasserbahn","Darkride","Park"]),\n'
    '  timeline_park_baujahr:()=>genTimelineQ("park_baujahr"),\n'
    '  ws_park_achterbahn:()=>{initParksWS("achterbahn");return null;},\n'
    '  /* Phase 438: Kunstgeschichte */\n'
    '  hl_kunst_jahr:()=>genKunstHLExt("entstehungsjahr",{lowerWins:true,unit:"",'
    'prompt:_tc("Welches Kunstwerk ist \\u00e4lter?")}),\n'
    '  hl_kunst_wert:()=>genKunstHLExt("schaetzwert_mio_usd",{unit:"Mio. USD",'
    'prompt:_tc("Welches Kunstwerk hat einen h\\u00f6heren Sch\\u00e4tzwert?")}),\n'
    '  kunst_match_kuenstler:()=>genKunstMatchExt("kuenstler",'
    '_tc("Wer hat dieses Kunstwerk erschaffen?")),\n'
    '  kunst_match_epoche:()=>genKunstMatchExt("epoche",'
    '_tc("Welcher Kunstepoche geh\\u00f6rt dieses Werk an?")),\n'
    '  kunst_match_museum:()=>genKunstMatchExt("standort_museum",'
    '_tc("In welchem Museum befindet sich dieses Werk?")),\n'
    '  timeline_kunst_jahr:()=>genTimelineQ("kunst_jahr"),\n'
    '  ws_kunst_renaissance:()=>{initKunstWS("renaissance");return null;},'
)

# ── 10. Replace-Kette ────────────────────────────────────────────────────────
REPL_OLD = "  .replace('PLACEHOLDER_AUTOS',          AUTOS_J)"
REPL_NEW = (
    "  .replace('PLACEHOLDER_AUTOS',          AUTOS_J)\n"
    "  .replace('PLACEHOLDER_PARKS_WS',       PARKS_WS_J)\n"
    "  .replace('PLACEHOLDER_PARKS',          PARKS_J)\n"
    "  .replace('PLACEHOLDER_KUNST_WS',       KUNST_WS_J)\n"
    "  .replace('PLACEHOLDER_KUNST',          KUNST_J)"
)

patch(GEN, [
    (LOAD_OLD,       LOAD_NEW,       'Py: 4 neue Dateien laden'),
    (CONST_OLD,      CONST_NEW,      'JS: PARKS/KUNST Konstanten'),
    (MKWS_OLD,       MKWS_NEW,       'JS: initParksWS + initKunstWS'),
    (GEN_ANCHOR,     GEN_NEW,        'JS: Generator-Funktionen Parks/Kunst'),
    (I18N_PL_OLD,    I18N_PL_NEW,    'i18n PL: 12 neue Strings'),
    (I18N_EN_OLD,    I18N_EN_NEW,    'i18n EN: 12 neue Strings'),
    (MODES_ANCHOR,   MODES_NEW,      'MODES: 15 neue Modi'),
    (CATS_ANCHOR,    CATS_NEW,       'MODE_CATS: themeparks + kunst'),
    (DISP_ANCHOR,    DISP_NEW,       'GEN dispatch: 15 neue Eintraege'),
    (REPL_OLD,       REPL_NEW,       'Replace-Kette: PARKS_WS/PARKS/KUNST_WS/KUNST'),
])

print('\nPatch 438 gen.py: fertig!')
