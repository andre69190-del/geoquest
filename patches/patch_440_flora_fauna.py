#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 440: Hunderassen & Gartenbau.

Neue JSON-Dateien:
  data/hunde_extended.json    (40 Eintraege)
  data/gartenbau_extended.json (40 Eintraege)
  data/hunde_ws.json           (BEGLEITHUND, WELPENSCHULE)
  data/gartenbau_ws.json       (RHODODENDRON, STRELITZIE)

Neue MODES (14):
  Hunde:    hl_hund_gewicht, hl_hund_alter, hl_hund_hoehe,
            hund_match_land, hund_match_kategorie,
            ws_hund_begleiter, ws_hund_welpe
  Gartenbau: hl_garten_hoehe, hl_garten_bluete (lowerWins!),
             garten_match_wasser, garten_match_boden,
             garten_match_region, ws_garten_rhodo, ws_garten_strelitzie

Zero-Bug-Policy: assert count==1.
i18n: alle Prompts via _tc(), DE/EN/PL.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, 'gen.py')
VC   = os.path.join(ROOT, 'validate_content.py')


def patch(path, edits):
    c = open(path, 'r', encoding='utf-8').read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, 'Anker "%s" count=%d (erwartet 1)' % (tag, n)
        c = c.replace(old, new)
        print('  OK  ' + tag)
    open(path, 'w', encoding='utf-8').write(c)


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 1: validate_content.py
# ─────────────────────────────────────────────────────────────────────────────
print('\n-- 1. validate_content.py --')

VC_CHECK_ANCHOR = 'def check_autos_extended(filename, data):'
VC_CHECK_NEW = '''\
def check_hunde_extended(filename, data):
    """Validiert data/hunde_extended.json (flaches Dict, 6 Felder)."""
    REQUIRED = ['kategorie', 'max_gewicht_kg', 'lebenserwartung_jahre',
                'widerristhoehe_cm', 'ursprungsland', 'fci_gruppe']
    KAT_ENUM = {'Huetehund', 'Begleithund', 'Jagdhund', 'Terrier', 'Molosser',
                'Hütehund'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'hunde_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, "Feld '%s' fehlt" % f)
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, "'%s' nicht erlaubt" % kat)
        for float_f in ('max_gewicht_kg',):
            v = entry.get(float_f)
            if v is not None and not isinstance(v, (int, float)):
                warn(filename, 'typ:' + float_f, name,
                     'Muss Float sein, ist %s' % type(v).__name__)
        for int_f in ('lebenserwartung_jahre', 'widerristhoehe_cm'):
            v = entry.get(int_f)
            if v is not None and not isinstance(v, int):
                warn(filename, 'typ:' + int_f, name,
                     'Muss Int sein, ist %s' % type(v).__name__)
        fg = entry.get('fci_gruppe')
        if fg is not None and not isinstance(fg, int):
            warn(filename, 'typ:fci_gruppe', name,
                 'Muss Int/null sein, ist %s' % type(fg).__name__)


def check_gartenbau_extended(filename, data):
    """Validiert data/gartenbau_extended.json (flaches Dict, 6 Felder)."""
    REQUIRED = ['kategorie', 'max_wuchshoehe_cm', 'wasserbedarf',
                'bodenanspruch', 'ursprungsregion', 'bluetezeit_start_monat']
    KAT_ENUM   = {'Zierpflanze', 'Nutzpflanze', 'Baum', 'Strauch'}
    WASSER_ENUM = {'Wenig', 'Mittel', 'Hoch'}
    BODEN_ENUM  = {'Sauer', 'Neutral', 'Alkalisch', 'Tolerant'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'gartenbau_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, "Feld '%s' fehlt" % f)
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, "'%s' nicht erlaubt" % kat)
        w = entry.get('wasserbedarf')
        if w is not None and w not in WASSER_ENUM:
            warn(filename, 'enum:wasserbedarf', name, "'%s' nicht erlaubt" % w)
        b = entry.get('bodenanspruch')
        if b is not None and b not in BODEN_ENUM:
            warn(filename, 'enum:bodenanspruch', name, "'%s' nicht erlaubt" % b)
        v = entry.get('max_wuchshoehe_cm')
        if v is not None and not isinstance(v, int):
            warn(filename, 'typ:max_wuchshoehe_cm', name,
                 'Muss Int sein, ist %s' % type(v).__name__)
        m = entry.get('bluetezeit_start_monat')
        if m is not None:
            if not isinstance(m, int):
                warn(filename, 'typ:bluetezeit_start_monat', name,
                     'Muss Int/null sein, ist %s' % type(m).__name__)
            elif not (1 <= m <= 12):
                warn(filename, 'range:bluetezeit_start_monat', name,
                     'Monat muss 1-12 sein, ist %d' % m)


def check_autos_extended(filename, data):'''

VC_DISPATCH_ANCHOR = (
    '    elif name == "kunst_extended.json":\n'
    '        check_kunst_extended(filename, data)\n'
    '    elif name == "autos_extended.json":'
)
VC_DISPATCH_NEW = (
    '    elif name == "kunst_extended.json":\n'
    '        check_kunst_extended(filename, data)\n'
    '    elif name == "hunde_extended.json":\n'
    '        check_hunde_extended(filename, data)\n'
    '    elif name == "gartenbau_extended.json":\n'
    '        check_gartenbau_extended(filename, data)\n'
    '    elif name == "autos_extended.json":'
)

patch(VC, [
    (VC_CHECK_ANCHOR,    VC_CHECK_NEW,    'VC: check_hunde + check_gartenbau'),
    (VC_DISPATCH_ANCHOR, VC_DISPATCH_NEW, 'VC: dispatch hunde + gartenbau'),
])


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 2: gen.py — 9 Sub-Patches
# ─────────────────────────────────────────────────────────────────────────────
print('\n-- 2. gen.py --')

# ── 2.1 Python Loader ────────────────────────────────────────────────────────
LOAD_OLD = (
    "        KUNST_WS_J = __import__('json').dumps(__import__('json').load(_kwf),"
    " ensure_ascii=False, separators=(',','::'))"
)
# Might be single colon — detect
raw = open(GEN, encoding='utf-8').read()
if LOAD_OLD not in raw:
    LOAD_OLD = (
        "        KUNST_WS_J = __import__('json').dumps(__import__('json').load(_kwf),"
        " ensure_ascii=False, separators=(',',':'))"
    )

LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/hunde_extended.json'), 'r', encoding='utf-8') as _hdf:\n"
    "        HUNDE_J = __import__('json').dumps(__import__('json').load(_hdf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/gartenbau_extended.json'), 'r', encoding='utf-8') as _gbf:\n"
    "        GARTEN_J = __import__('json').dumps(__import__('json').load(_gbf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/hunde_ws.json'), 'r', encoding='utf-8') as _hwf:\n"
    "        HUNDE_WS_J = __import__('json').dumps(__import__('json').load(_hwf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/gartenbau_ws.json'), 'r', encoding='utf-8') as _gwf:\n"
    "        GARTEN_WS_J = __import__('json').dumps(__import__('json').load(_gwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

# ── 2.2 JS Konstanten ────────────────────────────────────────────────────────
CONST_OLD = "const KUNST_DATA=PLACEHOLDER_KUNST;"
CONST_NEW = (
    "const KUNST_DATA=PLACEHOLDER_KUNST;\n"
    "const HUNDE_WS_DATA=PLACEHOLDER_HUNDE_WS;\n"
    "const HUNDE_DATA=PLACEHOLDER_HUNDE;\n"
    "const GARTEN_WS_DATA=PLACEHOLDER_GARTEN_WS;\n"
    "const GARTEN_DATA=PLACEHOLDER_GARTEN;"
)

# ── 2.3 _mkWS Inits ──────────────────────────────────────────────────────────
MKWS_OLD = 'var initKunstWS=_mkWS(KUNST_WS_DATA,"Kunst");'
MKWS_NEW = (
    'var initKunstWS=_mkWS(KUNST_WS_DATA,"Kunst");\n'
    'var initHundeWS=_mkWS(HUNDE_WS_DATA,"Hunde");\n'
    'var initGartenWS=_mkWS(GARTEN_WS_DATA,"Garten");'
)

# ── 2.4 Generator-Funktionen ─────────────────────────────────────────────────
GEN_ANCHOR = 'window.genKunstMatchExt=genKunstMatchExt;'
GEN_NEW = (
    'window.genKunstMatchExt=genKunstMatchExt;\n'
    '\n'
    '/* Phase 440: genHundeHLExt / genHundeMatchExt */\n'
    'function genHundeHLExt(field,opts){var o=opts||{};var items=[];var _HD=HUNDE_DATA;\n'
    '  var _ks=Object.keys(_HD).filter(function(k){return Object.prototype.hasOwnProperty.call(_HD,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_HD[_n][field]);if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welche Hunderasse ist schwerer?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"hund_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genHundeHLExt=genHundeHLExt;\n'
    '\n'
    'function genHundeMatchExt(field,prompt,fixedPool){var _HD=HUNDE_DATA;\n'
    '  var valid=Object.keys(_HD).filter(function(k){return Object.prototype.hasOwnProperty.call(_HD,k)&&_HD[k][field]!=null&&_HD[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_HD[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_HD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"hund_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genHundeMatchExt=genHundeMatchExt;\n'
    '\n'
    '/* Phase 440: genGartenHLExt / genGartenMatchExt */\n'
    'function genGartenHLExt(field,opts){var o=opts||{};var items=[];var _GD=GARTEN_DATA;\n'
    '  var _ks=Object.keys(_GD).filter(function(k){return Object.prototype.hasOwnProperty.call(_GD,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_GD[_n][field]);if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welche Pflanze wächst höher?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"garten_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genGartenHLExt=genGartenHLExt;\n'
    '\n'
    'function genGartenMatchExt(field,prompt,fixedPool){var _GD=GARTEN_DATA;\n'
    '  var valid=Object.keys(_GD).filter(function(k){return Object.prototype.hasOwnProperty.call(_GD,k)&&_GD[k][field]!=null&&_GD[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_GD[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_GD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"garten_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genGartenMatchExt=genGartenMatchExt;'
)

# ── 2.5 i18n PL ──────────────────────────────────────────────────────────────
I18N_PL_OLD = (
    '"In welchem Museum befindet sich dieses Werk?":"W którym muzeum znajduje się to dzieło?"},"en"'
)
I18N_PL_NEW = (
    '"In welchem Museum befindet sich dieses Werk?":"W którym muzeum znajduje się to dzieło?",'
    '"Welche Hunderasse ist schwerer?":"Która rasa psów jest cięższa?",'
    '"Welche Hunderasse lebt länger?":"Która rasa psów żyje dłużej?",'
    '"Welche Hunderasse ist größer?":"Która rasa psów jest większa?",'
    '"Aus welchem Land stammt diese Hunderasse?":"Z jakiego kraju pochodzi ta rasa psów?",'
    '"Welcher Gruppe gehört diese Hunderasse an?":"Do jakiej grupy należy ta rasa psów?",'
    '"Welche Pflanze wächst höher?":"Która roślina rośnie wyżej?",'
    '"Welche Pflanze blüht früher im Jahr?":"Która roślina kwitnie wcześniej w roku?",'
    '"Welchen Wasserbedarf hat diese Pflanze?":"Jakie jest zapotrzebowanie tej rośliny na wodę?",'
    '"Welchen Bodenanspruch hat diese Pflanze?":"Jakie są wymagania glebowe tej rośliny?",'
    '"Aus welcher Region stammt diese Pflanze?":"Z jakiego regionu pochodzi ta roślina?"'
    '},"en"'
)

# ── 2.6 i18n EN ──────────────────────────────────────────────────────────────
I18N_EN_OLD = (
    '"In welchem Museum befindet sich dieses Werk?":"In which museum is this work located?"}};'
)
I18N_EN_NEW = (
    '"In welchem Museum befindet sich dieses Werk?":"In which museum is this work located?",'
    '"Welche Hunderasse ist schwerer?":"Which dog breed is heavier?",'
    '"Welche Hunderasse lebt länger?":"Which dog breed lives longer?",'
    '"Welche Hunderasse ist größer?":"Which dog breed is taller?",'
    '"Aus welchem Land stammt diese Hunderasse?":"Which country does this dog breed come from?",'
    '"Welcher Gruppe gehört diese Hunderasse an?":"Which group does this dog breed belong to?",'
    '"Welche Pflanze wächst höher?":"Which plant grows taller?",'
    '"Welche Pflanze blüht früher im Jahr?":"Which plant blooms earlier in the year?",'
    '"Welchen Wasserbedarf hat diese Pflanze?":"What water requirements does this plant have?",'
    '"Welchen Bodenanspruch hat diese Pflanze?":"What soil requirements does this plant have?",'
    '"Aus welcher Region stammt diese Pflanze?":"Which region does this plant come from?"'
    '}};'
)

# ── 2.7 MODES Array ──────────────────────────────────────────────────────────
MODES_ANCHOR = (
    '    {id:"ws_kunst_renaissance",icon:"\\u{1F3AD}",title:"WS: Renaissance",'
    'group:"kunst",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus RENAISSANCE!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben",'
    'prompt_en:"Form words from RENAISSANCE!"},'
)
MODES_NEW = (
    MODES_ANCHOR +
    '\n    /* Phase 440: Hunderassen */\n'
    '    {id:"hl_hund_gewicht",icon:"\\u{1F436}",title:"Hunde: Gewicht",'
    'group:"hunde",prompt:"Welche Hunderasse ist schwerer?",'
    'desc:"Max. Gewicht in kg \\u2014 vom Chihuahua bis zum Bernhardiner.",'
    'prompt_en:"Which dog breed is heavier?"},\n'
    '    {id:"hl_hund_alter",icon:"\\u{1F436}",title:"Hunde: Lebenserwartung",'
    'group:"hunde",prompt:"Welche Hunderasse lebt l\\u00e4nger?",'
    'desc:"Durchschnittliche Lebenserwartung in Jahren.",'
    'prompt_en:"Which dog breed lives longer?"},\n'
    '    {id:"hl_hund_hoehe",icon:"\\u{1F436}",title:"Hunde: Widerristhoehe",'
    'group:"hunde",prompt:"Welche Hunderasse ist gr\\u00f6\\u00dfer?",'
    'desc:"Widerristhoehe in cm \\u2014 von Chihuahua bis Irischem Wolfshund.",'
    'prompt_en:"Which dog breed is taller?"},\n'
    '    {id:"hund_match_land",icon:"\\u{1F30D}",title:"Hunde: Ursprungsland",'
    'group:"hunde",prompt:"Aus welchem Land stammt diese Hunderasse?",'
    'desc:"Von Deutschland bis Japan \\u2014 erkenne die Herkunft.",'
    'prompt_en:"Which country does this dog breed come from?"},\n'
    '    {id:"hund_match_kategorie",icon:"\\u{1F9AE}",title:"Hunde: Gruppe",'
    'group:"hunde",prompt:"Welcher Gruppe geh\\u00f6rt diese Hunderasse an?",'
    'desc:"H\\u00fctehund, Jagdhund, Molosser, Terrier oder Begleithund?",'
    'prompt_en:"Which group does this dog breed belong to?"},\n'
    '    {id:"ws_hund_begleiter",icon:"\\u{1F436}",title:"WS: Begleithund",'
    'group:"hunde",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus BEGLEITHUND!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 11 Buchstaben",'
    'prompt_en:"Form words from BEGLEITHUND!"},\n'
    '    {id:"ws_hund_welpe",icon:"\\u{1F436}",title:"WS: Welpenschule",'
    'group:"hunde",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus WELPENSCHULE!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 12 Buchstaben",'
    'prompt_en:"Form words from WELPENSCHULE!"},\n'
    '    /* Phase 440: Gartenbau & Botanik */\n'
    '    {id:"hl_garten_hoehe",icon:"\\u{1F33F}",title:"Gartenbau: Wuchshoehe",'
    'group:"gartenbau",prompt:"Welche Pflanze w\\u00e4chst h\\u00f6her?",'
    'desc:"Max. Wuchshoehe in cm \\u2014 von Erdbeere bis Eiche.",'
    'prompt_en:"Which plant grows taller?"},\n'
    '    {id:"hl_garten_bluete",icon:"\\u{1F338}",title:"Gartenbau: Fr\\u00fchster Bl\\u00fcher",'
    'group:"gartenbau",prompt:"Welche Pflanze bl\\u00fcht fr\\u00fcher im Jahr?",'
    'desc:"Monatszahl (1=Januar) \\u2014 fr\\u00fchere Bl\\u00fcte gewinnt.",'
    'prompt_en:"Which plant blooms earlier in the year?"},\n'
    '    {id:"garten_match_wasser",icon:"\\u{1F4A7}",title:"Gartenbau: Wasserbedarf",'
    'group:"gartenbau",prompt:"Welchen Wasserbedarf hat diese Pflanze?",'
    'desc:"Wenig, Mittel oder Hoch \\u2014 richtig g\\u00ie\\u00dfen!",'
    'prompt_en:"What water requirements does this plant have?"},\n'
    '    {id:"garten_match_boden",icon:"\\u{1F331}",title:"Gartenbau: Bodenanspruch",'
    'group:"gartenbau",prompt:"Welchen Bodenanspruch hat diese Pflanze?",'
    'desc:"Sauer, Neutral, Alkalisch oder Tolerant.",'
    'prompt_en:"What soil requirements does this plant have?"},\n'
    '    {id:"garten_match_region",icon:"\\u{1F30D}",title:"Gartenbau: Ursprungsregion",'
    'group:"gartenbau",prompt:"Aus welcher Region stammt diese Pflanze?",'
    'desc:"Von Ostasien bis Nordamerika \\u2014 erkenne die Herkunft.",'
    'prompt_en:"Which region does this plant come from?"},\n'
    '    {id:"ws_garten_rhodo",icon:"\\u{1F33A}",title:"WS: Rhododendron",'
    'group:"gartenbau",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus RHODODENDRON!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 12 Buchstaben",'
    'prompt_en:"Form words from RHODODENDRON!"},\n'
    '    {id:"ws_garten_strelitzie",icon:"\\u{1F33A}",title:"WS: Strelitzie",'
    'group:"gartenbau",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus STRELITZIE!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben",'
    'prompt_en:"Form words from STRELITZIE!"},'
)

# ── 2.8 MODE_CATS ────────────────────────────────────────────────────────────
CATS_ANCHOR = (
    '  kunst:{label:"Kunstgeschichte",icon:"\\u{1F5BC}\\uFE0F",'
    'modes:["hl_kunst_jahr","hl_kunst_wert","kunst_match_kuenstler","kunst_match_epoche",'
    '"kunst_match_museum","timeline_kunst_jahr","ws_kunst_renaissance"],cost:0},'
)
CATS_NEW = (
    CATS_ANCHOR + '\n'
    '  hunde:{label:"Hunderassen",icon:"\\u{1F436}",'
    'modes:["hl_hund_gewicht","hl_hund_alter","hl_hund_hoehe","hund_match_land",'
    '"hund_match_kategorie","ws_hund_begleiter","ws_hund_welpe"],cost:0},\n'
    '  gartenbau:{label:"Gartenbau & Botanik",icon:"\\u{1F33F}",'
    'modes:["hl_garten_hoehe","hl_garten_bluete","garten_match_wasser","garten_match_boden",'
    '"garten_match_region","ws_garten_rhodo","ws_garten_strelitzie"],cost:0},'
)

# ── 2.9 Dispatcher ───────────────────────────────────────────────────────────
DISP_ANCHOR = '  ws_kunst_renaissance:()=>{initKunstWS("renaissance");return null;},'
DISP_NEW = (
    '  ws_kunst_renaissance:()=>{initKunstWS("renaissance");return null;},\n'
    '  /* Phase 440: Hunderassen */\n'
    '  hl_hund_gewicht:()=>genHundeHLExt("max_gewicht_kg",{unit:"kg",'
    'prompt:_tc("Welche Hunderasse ist schwerer?")}),\n'
    '  hl_hund_alter:()=>genHundeHLExt("lebenserwartung_jahre",{unit:"J.",'
    'prompt:_tc("Welche Hunderasse lebt länger?")}),\n'
    '  hl_hund_hoehe:()=>genHundeHLExt("widerristhoehe_cm",{unit:"cm",'
    'prompt:_tc("Welche Hunderasse ist größer?")}),\n'
    '  hund_match_land:()=>genHundeMatchExt("ursprungsland",'
    '_tc("Aus welchem Land stammt diese Hunderasse?")),\n'
    '  hund_match_kategorie:()=>genHundeMatchExt("kategorie",'
    '_tc("Welcher Gruppe gehört diese Hunderasse an?"),'
    '["Hütehund","Begleithund","Jagdhund","Terrier","Molosser"]),\n'
    '  ws_hund_begleiter:()=>{initHundeWS("begleithund");return null;},\n'
    '  ws_hund_welpe:()=>{initHundeWS("welpenschule");return null;},\n'
    '  /* Phase 440: Gartenbau & Botanik */\n'
    '  hl_garten_hoehe:()=>genGartenHLExt("max_wuchshoehe_cm",{unit:"cm",'
    'prompt:_tc("Welche Pflanze wächst höher?")}),\n'
    '  hl_garten_bluete:()=>genGartenHLExt("bluetezeit_start_monat",{lowerWins:true,unit:"",'
    'prompt:_tc("Welche Pflanze blüht früher im Jahr?")}),\n'
    '  garten_match_wasser:()=>genGartenMatchExt("wasserbedarf",'
    '_tc("Welchen Wasserbedarf hat diese Pflanze?"),["Wenig","Mittel","Hoch"]),\n'
    '  garten_match_boden:()=>genGartenMatchExt("bodenanspruch",'
    '_tc("Welchen Bodenanspruch hat diese Pflanze?"),["Sauer","Neutral","Alkalisch","Tolerant"]),\n'
    '  garten_match_region:()=>genGartenMatchExt("ursprungsregion",'
    '_tc("Aus welcher Region stammt diese Pflanze?")),\n'
    '  ws_garten_rhodo:()=>{initGartenWS("rhododendron");return null;},\n'
    '  ws_garten_strelitzie:()=>{initGartenWS("strelitzie");return null;},'
)

# ── 2.10 Replace-Kette ───────────────────────────────────────────────────────
REPL_OLD = "  .replace('PLACEHOLDER_KUNST',          KUNST_J)"
REPL_NEW = (
    "  .replace('PLACEHOLDER_KUNST',          KUNST_J)\n"
    "  .replace('PLACEHOLDER_HUNDE_WS',       HUNDE_WS_J)\n"
    "  .replace('PLACEHOLDER_HUNDE',          HUNDE_J)\n"
    "  .replace('PLACEHOLDER_GARTEN_WS',      GARTEN_WS_J)\n"
    "  .replace('PLACEHOLDER_GARTEN',         GARTEN_J)"
)

patch(GEN, [
    (LOAD_OLD,       LOAD_NEW,       'Py: 4 neue Dateien laden'),
    (CONST_OLD,      CONST_NEW,      'JS: HUNDE/GARTEN Konstanten'),
    (MKWS_OLD,       MKWS_NEW,       'JS: initHundeWS + initGartenWS'),
    (GEN_ANCHOR,     GEN_NEW,        'JS: Generator-Funktionen Hunde/Garten'),
    (I18N_PL_OLD,    I18N_PL_NEW,    'i18n PL: 11 neue Strings'),
    (I18N_EN_OLD,    I18N_EN_NEW,    'i18n EN: 11 neue Strings'),
    (MODES_ANCHOR,   MODES_NEW,      'MODES: 14 neue Modi'),
    (CATS_ANCHOR,    CATS_NEW,       'MODE_CATS: hunde + gartenbau'),
    (DISP_ANCHOR,    DISP_NEW,       'GEN dispatch: 14 neue Eintraege'),
    (REPL_OLD,       REPL_NEW,       'Replace-Kette: HUNDE_WS/HUNDE/GARTEN_WS/GARTEN'),
])

print('\nPatch 440 fertig!')
