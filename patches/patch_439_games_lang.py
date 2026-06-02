#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 439: Brettspiele & Sprachen.

Neue JSON-Dateien:
  data/boardgames_extended.json (80 Eintraege)
  data/sprachen_extended.json   (80 Eintraege)
  data/boardgames_ws.json       (SPIELBRETT, WUERFELWURF)
  data/sprachen_ws.json         (GRAMMATIK, VOKABULAR)

Neue MODES (14):
  Brettspiele: hl_boardgame_jahr (lowerWins!), hl_boardgame_spieler,
               hl_boardgame_dauer, hl_boardgame_rating,
               boardgame_match_autor, boardgame_match_land,
               timeline_boardgame_jahr, ws_boardgame_spielbrett
  Sprachen:    hl_sprache_muttersprachler, hl_sprache_laender,
               sprache_match_familie, sprache_match_schrift,
               sprache_match_region, ws_sprache_grammatik

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

VC_ANCHOR = 'def check_hunde_extended(filename, data):'
VC_NEW = '''\
def check_boardgames_extended(filename, data):
    """Validiert data/boardgames_extended.json (7 Pflichtfelder, Enums, Typen)."""
    REQUIRED = ['kategorie', 'erscheinungsjahr', 'max_spieler', 'spieldauer_min',
                'bgg_rating', 'autor', 'ursprungsland']
    KAT_ENUM = {'Strategie', 'Party', 'Familie', 'Kartenspiel'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'boardgames_extended.json muss ein Dict sein')
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
        for int_f in ('erscheinungsjahr', 'max_spieler', 'spieldauer_min'):
            v = entry.get(int_f)
            if v is not None and not isinstance(v, int):
                warn(filename, 'typ:' + int_f, name,
                     'Muss Int sein, ist %s' % type(v).__name__)
        r = entry.get('bgg_rating')
        if r is not None and not isinstance(r, (int, float)):
            warn(filename, 'typ:bgg_rating', name,
                 'Muss Float sein, ist %s' % type(r).__name__)
        elif r is not None and not (0.0 <= float(r) <= 10.0):
            warn(filename, 'range:bgg_rating', name,
                 'bgg_rating muss 0-10 sein (ist %s)' % r)


def check_sprachen_extended(filename, data):
    """Validiert data/sprachen_extended.json (5 Pflichtfelder, Enums, Typen)."""
    REQUIRED = ['sprachfamilie', 'muttersprachler_mio', 'anzahl_laender',
                'schrift', 'ursprungsregion']
    FAM_ENUM = {
        'Indogermanisch', 'Sino-Tibetisch', 'Afroasiatisch', 'Austronesisch',
        'Isoliert', 'Turkisch', 'Dravidisch', 'Niger-Kongo', 'Uralisch',
        'Kartvelisch', 'Austroasiatisch', 'Kra-Dai', 'Quechua',
        'Uto-Aztekisch', 'Tupisch', 'Kunstsprache',
    }
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'sprachen_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, "Feld '%s' fehlt" % f)
        fam = entry.get('sprachfamilie')
        if fam is not None and fam not in FAM_ENUM:
            warn(filename, 'enum:sprachfamilie', name, "'%s' nicht erlaubt" % fam)
        v = entry.get('muttersprachler_mio')
        if v is not None and not isinstance(v, (int, float)):
            warn(filename, 'typ:muttersprachler_mio', name,
                 'Muss Float sein, ist %s' % type(v).__name__)
        n = entry.get('anzahl_laender')
        if n is not None and not isinstance(n, int):
            warn(filename, 'typ:anzahl_laender', name,
                 'Muss Int sein, ist %s' % type(n).__name__)


def check_hunde_extended(filename, data):'''

VC_DISPATCH_ANCHOR = (
    '    elif name == "hunde_extended.json":\n'
    '        check_hunde_extended(filename, data)'
)
VC_DISPATCH_NEW = (
    '    elif name == "boardgames_extended.json":\n'
    '        check_boardgames_extended(filename, data)\n'
    '    elif name == "sprachen_extended.json":\n'
    '        check_sprachen_extended(filename, data)\n'
    '    elif name == "hunde_extended.json":\n'
    '        check_hunde_extended(filename, data)'
)

patch(VC, [
    (VC_ANCHOR,          VC_NEW,          'VC: check_boardgames + check_sprachen'),
    (VC_DISPATCH_ANCHOR, VC_DISPATCH_NEW, 'VC: dispatch boardgames + sprachen'),
])


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 2: gen.py — 10 Sub-Patches
# ─────────────────────────────────────────────────────────────────────────────
print('\n-- 2. gen.py --')

# ── 2.1 Python Loader ────────────────────────────────────────────────────────
LOAD_OLD = (
    "        KUNST_WS_J = __import__('json').dumps(__import__('json').load(_kwf),"
    " ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = LOAD_OLD + (
    "\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/boardgames_extended.json'), 'r', encoding='utf-8') as _bgf:\n"
    "        BOARDGAMES_J = __import__('json').dumps(__import__('json').load(_bgf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/sprachen_extended.json'), 'r', encoding='utf-8') as _spf:\n"
    "        SPRACHEN_J = __import__('json').dumps(__import__('json').load(_spf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/boardgames_ws.json'), 'r', encoding='utf-8') as _bgwf:\n"
    "        BOARDGAMES_WS_J = __import__('json').dumps(__import__('json').load(_bgwf),"
    " ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__),"
    " 'data/sprachen_ws.json'), 'r', encoding='utf-8') as _spwf:\n"
    "        SPRACHEN_WS_J = __import__('json').dumps(__import__('json').load(_spwf),"
    " ensure_ascii=False, separators=(',',':'))"
)

# ── 2.2 JS Konstanten ────────────────────────────────────────────────────────
CONST_OLD = "const KUNST_DATA=PLACEHOLDER_KUNST;"
CONST_NEW = (
    "const KUNST_DATA=PLACEHOLDER_KUNST;\n"
    "const BOARDGAMES_WS_DATA=PLACEHOLDER_BOARDGAMES_WS;\n"
    "const BOARDGAMES_DATA=PLACEHOLDER_BOARDGAMES;\n"
    "const SPRACHEN_WS_DATA=PLACEHOLDER_SPRACHEN_WS;\n"
    "const SPRACHEN_DATA=PLACEHOLDER_SPRACHEN;"
)

# ── 2.3 _mkWS Inits ──────────────────────────────────────────────────────────
MKWS_OLD = 'var initKunstWS=_mkWS(KUNST_WS_DATA,"Kunst");'
MKWS_NEW = (
    'var initKunstWS=_mkWS(KUNST_WS_DATA,"Kunst");\n'
    'var initBoardgamesWS=_mkWS(BOARDGAMES_WS_DATA,"Boardgames");\n'
    'var initSprachenWS=_mkWS(SPRACHEN_WS_DATA,"Sprachen");'
)

# ── 2.4 Generator-Funktionen ─────────────────────────────────────────────────
GEN_ANCHOR = 'window.genKunstMatchExt=genKunstMatchExt;'
GEN_NEW = (
    'window.genKunstMatchExt=genKunstMatchExt;\n'
    '\n'
    '/* Phase 439: genBoardgamesHLExt / genBoardgamesMatchExt */\n'
    'function genBoardgamesHLExt(field,opts){var o=opts||{};var items=[];var _BD=BOARDGAMES_DATA;\n'
    '  var _ks=Object.keys(_BD).filter(function(k){return Object.prototype.hasOwnProperty.call(_BD,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_BD[_n][field]);\n'
    '    if(!isNaN(_v)&&_v!==null)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" \\u00b7 "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welches Spiel ist \\u00e4lter?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"bg_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genBoardgamesHLExt=genBoardgamesHLExt;\n'
    '\n'
    'function genBoardgamesMatchExt(field,prompt,fixedPool){var _BD=BOARDGAMES_DATA;\n'
    '  var valid=Object.keys(_BD).filter(function(k){return Object.prototype.hasOwnProperty.call(_BD,k)&&_BD[k][field]!=null&&_BD[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_BD[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_BD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"bg_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genBoardgamesMatchExt=genBoardgamesMatchExt;\n'
    '\n'
    '/* Phase 439: genSprachenHLExt / genSprachenMatchExt */\n'
    'function genSprachenHLExt(field,opts){var o=opts||{};var items=[];var _SD=SPRACHEN_DATA;\n'
    '  var _ks=Object.keys(_SD).filter(function(k){return Object.prototype.hasOwnProperty.call(_SD,k);});\n'
    '  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_SD[_n][field]);\n'
    '    if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}\n'
    '  if(items.length<4)return null;\n'
    '  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;\n'
    '  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));\n'
    '    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;\n'
    '    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;\n'
    '    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);\n'
    '    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" \\u00b7 "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '    return{type:"beta_hl",prompt:o.prompt||_tc("Welche Sprache hat mehr Muttersprachler?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"spr_"+field+"_"+ai+"_"+bi,cc:"de"};\n'
    '  }return null;}\n'
    'window.genSprachenHLExt=genSprachenHLExt;\n'
    '\n'
    'function genSprachenMatchExt(field,prompt,fixedPool){var _SD=SPRACHEN_DATA;\n'
    '  var valid=Object.keys(_SD).filter(function(k){return Object.prototype.hasOwnProperty.call(_SD,k)&&_SD[k][field]!=null&&_SD[k][field]!=="";});\n'
    '  if(valid.length<4)return null;\n'
    '  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_SD[entry][field]);\n'
    '  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})\n'
    '    :valid.map(function(n){return String(_SD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});\n'
    '  if(pool.length<3)return null;\n'
    '  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}\n'
    '  var opts=[correct].concat(pool.slice(0,3));\n'
    '  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}\n'
    '  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"spr_"+field+"_"+idx,cc:"de"};\n'
    '}\n'
    'window.genSprachenMatchExt=genSprachenMatchExt;'
)

# ── 2.5 i18n PL ──────────────────────────────────────────────────────────────
I18N_PL_OLD = (
    '"Aus welcher Region stammt diese Pflanze?":"Z jakiego regionu pochodzi ta roślina?"},"en"'
)
I18N_PL_NEW = (
    '"In welchem Museum befindet sich dieses Werk?":"W którym muzeum znajduje się to dzieło?",'
    '"Welches Brettspiel ist älter?":"Która gra planszowa jest starsza?",'
    '"Welches Spiel hat mehr Spieler?":"Która gra ma więcej graczy?",'
    '"Welches Spiel hat die längere Spieldauer?":"Która gra trwa dłużej?",'
    '"Welches Spiel hat die höhere BGG-Wertung?":"Która gra ma wyższą ocenę BGG?",'
    '"Wer hat dieses Spiel erfunden?":"Kto wynalazł tę grę?",'
    '"Aus welchem Land stammt dieses Brettspiel?":"Z jakiego kraju pochodzi ta gra planszowa?",'
    '"Welche Sprache hat mehr Muttersprachler?":"Który język ma więcej rodzimych użytkowników?",'
    '"Welche Sprache wird in mehr Ländern gesprochen?":"W ilu krajach mówi się tym językiem?",'
    '"Welcher Sprachfamilie gehört diese Sprache an?":"Do jakiej rodziny językowej należy ten język?",'
    '"Welche Schrift verwendet diese Sprache?":"Jakiego pisma używa ten język?",'
    '"Aus welcher Region stammt diese Sprache?":"Z jakiego regionu pochodzi ten język?"'
    '},"en"'
)

# ── 2.6 i18n EN ──────────────────────────────────────────────────────────────
I18N_EN_OLD = (
    '"Aus welcher Region stammt diese Pflanze?":"Which region does this plant come from?"}};'
)
I18N_EN_NEW = (
    '"In welchem Museum befindet sich dieses Werk?":"In which museum is this work located?",'
    '"Welches Brettspiel ist älter?":"Which board game is older?",'
    '"Welches Spiel hat mehr Spieler?":"Which game has more players?",'
    '"Welches Spiel hat die längere Spieldauer?":"Which game has the longer play time?",'
    '"Welches Spiel hat die höhere BGG-Wertung?":"Which game has the higher BGG rating?",'
    '"Wer hat dieses Spiel erfunden?":"Who invented this game?",'
    '"Aus welchem Land stammt dieses Brettspiel?":"Which country does this board game come from?",'
    '"Welche Sprache hat mehr Muttersprachler?":"Which language has more native speakers?",'
    '"Welche Sprache wird in mehr Ländern gesprochen?":"In which countries is this language spoken?",'
    '"Welcher Sprachfamilie gehört diese Sprache an?":"Which language family does this language belong to?",'
    '"Welche Schrift verwendet diese Sprache?":"Which script does this language use?",'
    '"Aus welcher Region stammt diese Sprache?":"Which region does this language come from?"'
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
    '\n    /* Phase 439: Brettspiele & Gesellschaftsspiele */\n'
    '    {id:"hl_boardgame_jahr",icon:"\\u{1F3B2}",title:"Brettspiele: \\u00c4lteres Spiel",'
    'group:"boardgames",prompt:"Welches Brettspiel ist \\u00e4lter?",'
    'desc:"Fr\\u00fcheres Erscheinungsjahr = Sieger (lowerWins).",'
    'prompt_en:"Which board game is older?"},\n'
    '    {id:"hl_boardgame_spieler",icon:"\\u{1F465}",title:"Brettspiele: Maximale Spieler",'
    'group:"boardgames",prompt:"Welches Spiel hat mehr Spieler?",'
    'desc:"Von 2 (Schach) bis 300 (Kahoot!) \\u2014 max. Spielerzahl.",'
    'prompt_en:"Which game has more players?"},\n'
    '    {id:"hl_boardgame_dauer",icon:"\\u23F1\\uFE0F",title:"Brettspiele: Spieldauer",'
    'group:"boardgames",prompt:"Welches Spiel hat die l\\u00e4ngere Spieldauer?",'
    'desc:"In Minuten \\u2014 von Dobble (15) bis D&D (240+).",'
    'prompt_en:"Which game has the longer play time?"},\n'
    '    {id:"hl_boardgame_rating",icon:"\\u2B50",title:"Brettspiele: BGG-Wertung",'
    'group:"boardgames",prompt:"Welches Spiel hat die h\\u00f6here BGG-Wertung?",'
    'desc:"BoardGameGeek-Rating von 1-10.",'
    'prompt_en:"Which game has the higher BGG rating?"},\n'
    '    {id:"boardgame_match_autor",icon:"\\u270D\\uFE0F",title:"Brettspiele: Autor",'
    'group:"boardgames",prompt:"Wer hat dieses Spiel erfunden?",'
    'desc:"Von Klaus Teuber bis Reiner Knizia \\u2014 erkenne den Spieleautor.",'
    'prompt_en:"Who invented this game?"},\n'
    '    {id:"boardgame_match_land",icon:"\\u{1F30D}",title:"Brettspiele: Ursprungsland",'
    'group:"boardgames",prompt:"Aus welchem Land stammt dieses Brettspiel?",'
    'desc:"Von Deutschland bis Japan \\u2014 erkenne die Spieleheimat.",'
    'prompt_en:"Which country does this board game come from?"},\n'
    '    {id:"timeline_boardgame_jahr",icon:"\\u{1F3B2}",title:"Brettspiele-Timeline",'
    'group:"boardgames",prompt:"Welches Spiel ist \\u00e4lter?",'
    'desc:"Von Go (2000 v.Chr.) bis Wingspan (2019) \\u2014 Spielegeschichte.",'
    'prompt_en:"Which game is older?"},\n'
    '    {id:"ws_boardgame_spielbrett",icon:"\\u{1F3B2}",title:"WS: Spielbrett",'
    'group:"boardgames",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus SPIELBRETT!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 10 Buchstaben",'
    'prompt_en:"Form words from SPIELBRETT!"},\n'
    '    /* Phase 439: Sprachen & Linguistik */\n'
    '    {id:"hl_sprache_muttersprachler",icon:"\\u{1F5E3}\\uFE0F",title:"Sprachen: Muttersprachler",'
    'group:"sprachen",prompt:"Welche Sprache hat mehr Muttersprachler?",'
    'desc:"In Millionen \\u2014 von Baskisch bis Mandarin.",'
    'prompt_en:"Which language has more native speakers?"},\n'
    '    {id:"hl_sprache_laender",icon:"\\u{1F30D}",title:"Sprachen: L\\u00e4nder",'
    'group:"sprachen",prompt:"Welche Sprache wird in mehr L\\u00e4ndern gesprochen?",'
    'desc:"Englisch (67 L\\u00e4nder) vs. Mandarin (3 L\\u00e4nder).",'
    'prompt_en:"Which language is spoken in more countries?"},\n'
    '    {id:"sprache_match_familie",icon:"\\u{1F9EC}",title:"Sprachen: Sprachfamilie",'
    'group:"sprachen",prompt:"Welcher Sprachfamilie geh\\u00f6rt diese Sprache an?",'
    'desc:"Indogermanisch, Sino-Tibetisch, Afroasiatisch & mehr.",'
    'prompt_en:"Which language family does this language belong to?"},\n'
    '    {id:"sprache_match_schrift",icon:"\\u270F\\uFE0F",title:"Sprachen: Schriftsystem",'
    'group:"sprachen",prompt:"Welche Schrift verwendet diese Sprache?",'
    'desc:"Lateinisch, Arabisch, Devanagari, Kyrillisch & mehr.",'
    'prompt_en:"Which script does this language use?"},\n'
    '    {id:"sprache_match_region",icon:"\\u{1F5FA}\\uFE0F",title:"Sprachen: Herkunftsregion",'
    'group:"sprachen",prompt:"Aus welcher Region stammt diese Sprache?",'
    'desc:"Von Mitteleuropa bis Ostasien \\u2014 erkenne die Sprachregion.",'
    'prompt_en:"Which region does this language come from?"},\n'
    '    {id:"ws_sprache_grammatik",icon:"\\u{1F4D6}",title:"WS: Grammatik",'
    'group:"sprachen",noMultiplayer:true,prompt:"Bilde W\\u00f6rter aus GRAMMATIK!",'
    'desc:"Anagramm-R\\u00e4tsel \\u2014 9 Buchstaben",'
    'prompt_en:"Form words from GRAMMATIK!"},'
)

# ── 2.8 MODE_CATS ────────────────────────────────────────────────────────────
CATS_ANCHOR = (
    '  kunst:{label:"Kunstgeschichte",icon:"\\u{1F5BC}\\uFE0F",'
    'modes:["hl_kunst_jahr","hl_kunst_wert","kunst_match_kuenstler","kunst_match_epoche",'
    '"kunst_match_museum","timeline_kunst_jahr","ws_kunst_renaissance"],cost:0},'
)
CATS_NEW = (
    CATS_ANCHOR + '\n'
    '  boardgames:{label:"Brettspiele & Gesellschaft",icon:"\\u{1F3B2}",'
    'modes:["hl_boardgame_jahr","hl_boardgame_spieler","hl_boardgame_dauer","hl_boardgame_rating",'
    '"boardgame_match_autor","boardgame_match_land","timeline_boardgame_jahr","ws_boardgame_spielbrett"],cost:0},\n'
    '  sprachen:{label:"Sprachen & Linguistik",icon:"\\u{1F5E3}\\uFE0F",'
    'modes:["hl_sprache_muttersprachler","hl_sprache_laender","sprache_match_familie",'
    '"sprache_match_schrift","sprache_match_region","ws_sprache_grammatik"],cost:0},'
)

# ── 2.9 Dispatcher ───────────────────────────────────────────────────────────
DISP_ANCHOR = '  ws_kunst_renaissance:()=>{initKunstWS("renaissance");return null;},'
DISP_NEW = (
    '  ws_kunst_renaissance:()=>{initKunstWS("renaissance");return null;},\n'
    '  /* Phase 439: Brettspiele */\n'
    '  hl_boardgame_jahr:()=>genBoardgamesHLExt("erscheinungsjahr",{lowerWins:true,unit:"",'
    'prompt:_tc("Welches Brettspiel ist \\u00e4lter?")}),\n'
    '  hl_boardgame_spieler:()=>genBoardgamesHLExt("max_spieler",{unit:"Spieler",'
    'prompt:_tc("Welches Spiel hat mehr Spieler?")}),\n'
    '  hl_boardgame_dauer:()=>genBoardgamesHLExt("spieldauer_min",{unit:"min",'
    'prompt:_tc("Welches Spiel hat die l\\u00e4ngere Spieldauer?")}),\n'
    '  hl_boardgame_rating:()=>genBoardgamesHLExt("bgg_rating",{unit:"\\u2605",'
    'prompt:_tc("Welches Spiel hat die h\\u00f6here BGG-Wertung?")}),\n'
    '  boardgame_match_autor:()=>genBoardgamesMatchExt("autor",'
    '_tc("Wer hat dieses Spiel erfunden?")),\n'
    '  boardgame_match_land:()=>genBoardgamesMatchExt("ursprungsland",'
    '_tc("Aus welchem Land stammt dieses Brettspiel?")),\n'
    '  timeline_boardgame_jahr:()=>genTimelineQ("boardgame_jahr"),\n'
    '  ws_boardgame_spielbrett:()=>{initBoardgamesWS("spielbrett");return null;},\n'
    '  /* Phase 439: Sprachen */\n'
    '  hl_sprache_muttersprachler:()=>genSprachenHLExt("muttersprachler_mio",{unit:"Mio.",'
    'prompt:_tc("Welche Sprache hat mehr Muttersprachler?")}),\n'
    '  hl_sprache_laender:()=>genSprachenHLExt("anzahl_laender",{unit:"L\\u00e4nder",'
    'prompt:_tc("Welche Sprache wird in mehr L\\u00e4ndern gesprochen?")}),\n'
    '  sprache_match_familie:()=>genSprachenMatchExt("sprachfamilie",'
    '_tc("Welcher Sprachfamilie geh\\u00f6rt diese Sprache an?")),\n'
    '  sprache_match_schrift:()=>genSprachenMatchExt("schrift",'
    '_tc("Welche Schrift verwendet diese Sprache?")),\n'
    '  sprache_match_region:()=>genSprachenMatchExt("ursprungsregion",'
    '_tc("Aus welcher Region stammt diese Sprache?")),\n'
    '  ws_sprache_grammatik:()=>{initSprachenWS("grammatik");return null;},'
)

# ── 2.10 Replace-Kette ───────────────────────────────────────────────────────
REPL_OLD = "  .replace('PLACEHOLDER_KUNST',          KUNST_J)"
REPL_NEW = (
    "  .replace('PLACEHOLDER_KUNST',          KUNST_J)\n"
    "  .replace('PLACEHOLDER_BOARDGAMES_WS',  BOARDGAMES_WS_J)\n"
    "  .replace('PLACEHOLDER_BOARDGAMES',     BOARDGAMES_J)\n"
    "  .replace('PLACEHOLDER_SPRACHEN_WS',    SPRACHEN_WS_J)\n"
    "  .replace('PLACEHOLDER_SPRACHEN',       SPRACHEN_J)"
)

patch(GEN, [
    (LOAD_OLD,       LOAD_NEW,       'Py: 4 neue Dateien laden'),
    (CONST_OLD,      CONST_NEW,      'JS: BOARDGAMES/SPRACHEN Konstanten'),
    (MKWS_OLD,       MKWS_NEW,       'JS: initBoardgamesWS + initSprachenWS'),
    (GEN_ANCHOR,     GEN_NEW,        'JS: Generator-Funktionen BG/Sprachen'),
    (I18N_PL_OLD,    I18N_PL_NEW,    'i18n PL: 12 neue Strings'),
    (I18N_EN_OLD,    I18N_EN_NEW,    'i18n EN: 12 neue Strings'),
    (MODES_ANCHOR,   MODES_NEW,      'MODES: 14 neue Modi'),
    (CATS_ANCHOR,    CATS_NEW,       'MODE_CATS: boardgames + sprachen'),
    (DISP_ANCHOR,    DISP_NEW,       'GEN dispatch: 14 neue Eintraege'),
    (REPL_OLD,       REPL_NEW,       'Replace-Kette: BOARDGAMES/SPRACHEN'),
])

# ── Timeline-Eintrag ─────────────────────────────────────────────────────────
import json
tl_path = os.path.join(ROOT, 'data', 'timeline.json')
tl = json.load(open(tl_path, encoding='utf-8'))
if 'boardgame_jahr' not in tl:
    tl['boardgame_jahr'] = {
        'prompt': 'Welches Brettspiel ist älter?',
        'items': [
            {'n': 'Go',              'year': -2000},
            {'n': 'Backgammon',      'year': -3000},
            {'n': 'Schach',          'year': 600},
            {'n': 'Mah-Jong',        'year': 1850},
            {'n': 'Monopoly',        'year': 1935},
            {'n': 'Risk',            'year': 1957},
            {'n': 'Dungeons and Dragons', 'year': 1974},
            {'n': 'Siedler von Catan', 'year': 1995},
            {'n': 'Codenames',       'year': 2015},
            {'n': 'Wingspan',        'year': 2019},
        ]
    }
    json.dump(tl, open(tl_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('  OK  timeline.json: boardgame_jahr hinzugefügt')

print('\nPatch 439 fertig!')
