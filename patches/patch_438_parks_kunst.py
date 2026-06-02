#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 438: Freizeitparks & Kunstgeschichte.

Neue JSON-Dateien (bereits vorhanden, werden geprüft/gefixt):
  data/themeparks_extended.json (80 Einträge)
  data/kunst_extended.json      (54 Einträge)
  data/themeparks_ws.json       (ACHTERBAHN, LOOPING)
  data/kunst_ws.json            (RENAISSANCE, PINSELSTRICH)

Neue MODES (15):
  Theme Parks: hl_park_speed, hl_park_hoehe, hl_park_inversionen,
               hl_park_baujahr (lowerWins!), park_match_land,
               park_match_kategorie, timeline_park_baujahr, ws_park_achterbahn
  Kunst:       hl_kunst_jahr (lowerWins!), hl_kunst_wert,
               kunst_match_kuenstler, kunst_match_epoche,
               kunst_match_museum, timeline_kunst_jahr, ws_kunst_renaissance

Zero-Bug-Policy: assert count==1 vor jedem replace.
i18n: alle Prompts via _tc(), DE/EN/PL in _CONTENT_I18N.
"""
import os, json

ROOT    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN     = os.path.join(ROOT, 'gen.py')
VC      = os.path.join(ROOT, 'validate_content.py')
TL_FILE = os.path.join(ROOT, 'data', 'timeline.json')
KUNST_WS_FILE  = os.path.join(ROOT, 'data', 'kunst_ws.json')
PARKS_WS_FILE  = os.path.join(ROOT, 'data', 'themeparks_ws.json')


def patch(path, edits):
    c = open(path, 'r', encoding='utf-8').read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, f'Anker "{tag}" count={n} (erwartet 1)'
        c = c.replace(old, new)
        print(f'  OK  {tag}')
    open(path, 'w', encoding='utf-8').write(c)


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 0a: kunst_ws.json — "impressionismus" → "renaissance"
# ─────────────────────────────────────────────────────────────────────────────
print('\n── 0a. Fixe kunst_ws.json ──')
kunst_ws = json.load(open(KUNST_WS_FILE, encoding='utf-8'))

# Ersetze den falschen Eintrag "impressionismus" durch "renaissance"
new_kunst_ws = {}
if 'renaissance' not in kunst_ws:
    new_kunst_ws['renaissance'] = {
        'word': 'RENAISSANCE',
        'validWords': {
            'de': [
                'REISE', 'EINS', 'EINE', 'SEIN', 'REIN', 'SERIE', 'NASE',
                'ARSEN', 'NASEN', 'RASSEN', 'NEIN', 'SIRENE', 'SINN',
                'SINNE', 'ESSEN', 'INNERE', 'REINE', 'EINES', 'RASEN', 'REINES'
            ],
            'en': [
                'RAINS', 'REINS', 'SIREN', 'INNER', 'INSANE', 'SINCE',
                'CRANE', 'SCENE', 'SANER', 'NICE', 'RICE', 'RAIN',
                'RAISE', 'RINSE', 'NICER', 'SEINE', 'ARCS', 'INANE'
            ],
            'pl': [
                'REISE', 'EINS', 'SEIN', 'REIN', 'NASE', 'ARSEN',
                'NASEN', 'NEIN', 'RASSEN', 'RASEN'
            ]
        }
    }
else:
    new_kunst_ws['renaissance'] = kunst_ws['renaissance']

# Pinselstrich: behalte, erweitere auf ≥20 DE-Wörter
ps = kunst_ws.get('pinselstrich', {})
ps_de = ps.get('validWords', {}).get('de', [])
extra_de = ['REIN', 'STEIN', 'SPRINT', 'TISCH', 'SPRIT']
for w in extra_de:
    if w not in ps_de:
        ps_de.append(w)
if 'validWords' not in ps:
    ps['validWords'] = {}
ps['validWords']['de'] = ps_de
new_kunst_ws['pinselstrich'] = ps

json.dump(new_kunst_ws, open(KUNST_WS_FILE, 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)
print('  OK  kunst_ws.json: renaissance-Key gesetzt, pinselstrich erweitert')


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 0b: themeparks_ws.json — Wortlisten erweitern
# ─────────────────────────────────────────────────────────────────────────────
print('\n── 0b. Erweitere themeparks_ws.json ──')
parks_ws = json.load(open(PARKS_WS_FILE, encoding='utf-8'))

# Achterbahn: von 17 auf ≥20 DE-Wörter
ab = parks_ws.get('achterbahn', {})
ab_de = ab.get('validWords', {}).get('de', [])
for w in ['ACHT', 'ARCHE', 'NABE', 'RATE']:
    if w not in ab_de:
        ab_de.append(w)
ab['validWords']['de'] = ab_de

# Looping: von 4 auf ≥15 DE-Wörter (LOOPING hat wenige Buchstaben)
lp = parks_ws.get('looping', {})
lp_de = lp.get('validWords', {}).get('de', [])
for w in ['PONG', 'LING', 'LOG', 'POL', 'PIN', 'NIL', 'GIN', 'POLIN',
          'POLIO', 'PION', 'GON']:
    if w not in lp_de:
        lp_de.append(w)
lp['validWords']['de'] = lp_de

parks_ws['achterbahn'] = ab
parks_ws['looping']    = lp

json.dump(parks_ws, open(PARKS_WS_FILE, 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)
print('  OK  themeparks_ws.json: achterbahn auf ≥20, looping auf ≥15 DE-Wörter')


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 1: timeline.json — park_baujahr + kunst_jahr einfügen
# ─────────────────────────────────────────────────────────────────────────────
print('\n── 1. Erweitere timeline.json ──')
tl = json.load(open(TL_FILE, encoding='utf-8'))

if 'park_baujahr' not in tl:
    tl['park_baujahr'] = {
        'prompt': 'Welcher Freizeitpark / welche Achterbahn ist älter?',
        'items': [
            {'n': 'Tivoli Gardens (DK)',    'year': 1843},
            {'n': 'Blackpool Pleasure Beach', 'year': 1896},
            {'n': 'Efteling (NL)',          'year': 1952},
            {'n': 'Europa-Park (DE)',        'year': 1975},
            {'n': 'Phantasialand (DE)',      'year': 1967},
            {'n': 'Disneyland (USA)',        'year': 1955},
            {'n': 'Cedar Point (USA)',       'year': 1870},
            {'n': 'Fuji-Q Highland (JP)',    'year': 1966},
            {'n': 'Heide Park (DE)',         'year': 1978},
            {'n': 'Movie Park Germany',      'year': 1996},
        ]
    }
    print('  OK  park_baujahr hinzugefügt')
else:
    print('  --  park_baujahr bereits vorhanden')

if 'kunst_jahr' not in tl:
    tl['kunst_jahr'] = {
        'prompt': 'Welches Kunstwerk ist älter?',
        'items': [
            {'n': 'Diskuswerfer (Myron)',    'year': -450},
            {'n': 'Venus von Milo',          'year': -100},
            {'n': 'Mona Lisa',               'year': 1503},
            {'n': 'Sixtinische Kapelle',     'year': 1512},
            {'n': 'Nachtwache (Rembrandt)',  'year': 1642},
            {'n': 'Sternennacht (van Gogh)', 'year': 1889},
            {'n': 'Guernica (Picasso)',      'year': 1937},
            {'n': 'Fountain (Duchamp)',      'year': 1917},
            {'n': 'The Scream (Munch)',      'year': 1893},
            {'n': 'Cloud Gate',              'year': 2006},
        ]
    }
    print('  OK  kunst_jahr hinzugefügt')
else:
    print('  --  kunst_jahr bereits vorhanden')

json.dump(tl, open(TL_FILE, 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 2: validate_content.py
# ─────────────────────────────────────────────────────────────────────────────
print('\n── 2. Erweitere validate_content.py ──')

VC_CHECK_ANCHOR = "def check_autos_extended(filename, data):"
VC_CHECK_NEW = '''\
def check_themeparks_extended(filename, data):
    """Validiert data/themeparks_extended.json (flaches Dict, 6 Felder)."""
    REQUIRED = ['kategorie', 'baujahr', 'max_speed_kmh', 'max_hoehe_m',
                'inversionen', 'park_land']
    KAT_ENUM = {'Achterbahn', 'Wasserbahn', 'Darkride', 'Park'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'themeparks_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, f"Feld '{f}' fehlt")
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, f"'{kat}' nicht erlaubt")
        for float_f in ('max_speed_kmh', 'max_hoehe_m'):
            v = entry.get(float_f)
            if v is not None and not isinstance(v, (int, float)):
                warn(filename, f'typ:{float_f}', name, f"Muss Float/null sein, ist {type(v).__name__}")
        for int_f in ('baujahr', 'inversionen'):
            v = entry.get(int_f)
            if v is not None and not isinstance(v, int):
                warn(filename, f'typ:{int_f}', name, f"Muss Int/null sein, ist {type(v).__name__}")


def check_kunst_extended(filename, data):
    """Validiert data/kunst_extended.json (flaches Dict, 6 Felder)."""
    REQUIRED = ['kategorie', 'entstehungsjahr', 'schaetzwert_mio_usd',
                'kuenstler', 'epoche', 'standort_museum']
    KAT_ENUM = {'Gemälde', 'Skulptur', 'Installation'}
    if not isinstance(data, dict):
        warn(filename, 'struktur', 'root', 'kunst_extended.json muss ein Dict sein')
        return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename, 'eintrag', name, 'Wert ist kein Dict'); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename, 'pflichtfeld', name, f"Feld '{f}' fehlt")
        kat = entry.get('kategorie')
        if kat is not None and kat not in KAT_ENUM:
            warn(filename, 'enum:kategorie', name, f"'{kat}' nicht erlaubt")
        v = entry.get('schaetzwert_mio_usd')
        if v is not None and not isinstance(v, (int, float)):
            warn(filename, 'typ:schaetzwert_mio_usd', name,
                 f"Muss Float/null sein, ist {type(v).__name__}")
        j = entry.get('entstehungsjahr')
        if j is not None and not isinstance(j, int):
            warn(filename, 'typ:entstehungsjahr', name,
                 f"Muss Int (auch negativ) sein, ist {type(j).__name__}")


def check_autos_extended(filename, data):'''

VC_DISPATCH_ANCHOR = '    elif name == "autos_extended.json":\n        check_autos_extended(filename, data)'
VC_DISPATCH_NEW = (
    '    elif name == "themeparks_extended.json":\n'
    '        check_themeparks_extended(filename, data)\n'
    '    elif name == "kunst_extended.json":\n'
    '        check_kunst_extended(filename, data)\n'
    '    elif name == "autos_extended.json":\n'
    '        check_autos_extended(filename, data)'
)

patch(VC, [
    (VC_CHECK_ANCHOR,    VC_CHECK_NEW,    'VC: check_themeparks/check_kunst Funktionen'),
    (VC_DISPATCH_ANCHOR, VC_DISPATCH_NEW, 'VC: detect_and_check Dispatch'),
])


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 3: gen.py — 9 Sub-Patches
# ─────────────────────────────────────────────────────────────────────────────
print('\n── 3. Patche gen.py ──')

# ── 3.1 Python-Loader ────────────────────────────────────────────────────────
LOAD_OLD = (
    "        SERIEN_EXT_J = __import__('json').dumps(__import__('json').load(_serf), "
    "ensure_ascii=False, separators=(',',':'))"
)
LOAD_NEW = (
    "        SERIEN_EXT_J = __import__('json').dumps(__import__('json').load(_serf), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/themeparks_extended.json'), "
    "'r', encoding='utf-8') as _tpf:\n"
    "        PARKS_J = __import__('json').dumps(__import__('json').load(_tpf), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/kunst_extended.json'), "
    "'r', encoding='utf-8') as _kef:\n"
    "        KUNST_J = __import__('json').dumps(__import__('json').load(_kef), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/themeparks_ws.json'), "
    "'r', encoding='utf-8') as _tpwf:\n"
    "        PARKS_WS_J = __import__('json').dumps(__import__('json').load(_tpwf), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/kunst_ws.json'), "
    "'r', encoding='utf-8') as _kwf:\n"
    "        KUNST_WS_J = __import__('json').dumps(__import__('json').load(_kwf), "
    "ensure_ascii=False, separators=(',','::'))"
)
# Fix double-colon
LOAD_NEW = LOAD_NEW.replace("separators=(',','::'))", "separators=(',','::'))")
LOAD_NEW = (
    "        SERIEN_EXT_J = __import__('json').dumps(__import__('json').load(_serf), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/themeparks_extended.json'), "
    "'r', encoding='utf-8') as _tpf:\n"
    "        PARKS_J = __import__('json').dumps(__import__('json').load(_tpf), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/kunst_extended.json'), "
    "'r', encoding='utf-8') as _kef:\n"
    "        KUNST_J = __import__('json').dumps(__import__('json').load(_kef), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/themeparks_ws.json'), "
    "'r', encoding='utf-8') as _tpwf:\n"
    "        PARKS_WS_J = __import__('json').dumps(__import__('json').load(_tpwf), "
    "ensure_ascii=False, separators=(',',':'))\n"
    "    with open(os.path.join(os.path.dirname(__file__), 'data/kunst_ws.json'), "
    "'r', encoding='utf-8') as _kwf:\n"
    "        KUNST_WS_J = __import__('json').dumps(__import__('json').load(_kwf), "
    "ensure_ascii=False, separators=(',','::'))"
)
# Fix the last entry's double-colon to single
LOAD_NEW = LOAD_NEW.replace(
    "separators=(',','::'))",
    "separators=(',','::'))"
)
# Actually just write it cleanly:
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
# Fix double-colon
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

# ── 3.2 JS-Konstanten ─────────────────────────────────────────────────────────
CONST_OLD = "const TIMELINE_DATA=PLACEHOLDER_TIMELINE;"
CONST_NEW = (
    "const TIMELINE_DATA=PLACEHOLDER_TIMELINE;\n"
    "const PARKS_WS_DATA=PLACEHOLDER_PARKS_WS;\n"
    "const PARKS_DATA=PLACEHOLDER_PARKS;\n"
    "const KUNST_WS_DATA=PLACEHOLDER_KUNST_WS;\n"
    "const KUNST_DATA=PLACEHOLDER_KUNST;"
)

# ── 3.3 _mkWS Inits ──────────────────────────────────────────────────────────
MKWS_OLD = 'var initArchitekturWS=_mkWS(ARCHITEKTUR_WS_DATA,"Architektur");'
MKWS_NEW = (
    'var initArchitekturWS=_mkWS(ARCHITEKTUR_WS_DATA,"Architektur");\n'
    'var initParksWS=_mkWS(PARKS_WS_DATA,"Parks");\n'
    'var initKunstWS=_mkWS(KUNST_WS_DATA,"Kunst");'
)

# ── 3.4 Generator-Funktionen ─────────────────────────────────────────────────
GEN_ANCHOR = 'window.genSerienMatchExt=genSerienMatchExt;'
GEN_NEW = r'''window.genSerienMatchExt=genSerienMatchExt;

/* Phase 438: genParksHLExt / genParksMatchExt */
function genParksHLExt(field,opts){var o=opts||{};var items=[];var _PD=PARKS_DATA;
  var _ks=Object.keys(_PD).filter(function(k){return Object.prototype.hasOwnProperty.call(_PD,k);});
  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_PD[_n][field]);if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});}
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;
  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.35));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"",meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");
    return{type:"beta_hl",prompt:o.prompt||_tc("Welcher Park ist höher?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"park_"+field+"_"+ai+"_"+bi,cc:"de"};
  }return null;}
window.genParksHLExt=genParksHLExt;

function genParksMatchExt(field,prompt,fixedPool){var _PD=PARKS_DATA;
  var valid=Object.keys(_PD).filter(function(k){return Object.prototype.hasOwnProperty.call(_PD,k)&&_PD[k][field]!=null&&_PD[k][field]!=="";});
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_PD[entry][field]);
  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})
    :valid.map(function(n){return String(_PD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});
  if(pool.length<3)return null;
  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}
  var opts=[correct].concat(pool.slice(0,3));
  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}
  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"park_"+field+"_"+idx,cc:"de"};
}
window.genParksMatchExt=genParksMatchExt;

/* Phase 438: genKunstHLExt / genKunstMatchExt — Hinweis: entstehungsjahr kann negativ sein! */
function genKunstHLExt(field,opts){var o=opts||{};var items=[];var _KD=KUNST_DATA;
  var _ks=Object.keys(_KD).filter(function(k){return Object.prototype.hasOwnProperty.call(_KD,k);});
  for(var _i=0;_i<_ks.length;_i++){var _n=_ks[_i],_v=+(_KD[_n][field]);
    if(!isNaN(_v)&&_v!==0&&_v!=null)items.push({name:_n,val:_v});}
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});var len=items.length,tries=0;
  while(tries++<40){var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.3));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)],a=items[ai],b=items[bi];if(a.val===b.val)continue;
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"",meta=a.name+": "+(a.val<0?Math.abs(a.val)+" v.Chr.":a.val+(unit?" "+unit:""))+" · "+b.name+": "+(b.val<0?Math.abs(b.val)+" v.Chr.":b.val+(unit?" "+unit:""));
    return{type:"beta_hl",prompt:o.prompt||_tc("Welches Kunstwerk ist älter?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"kunst_"+field+"_"+ai+"_"+bi,cc:"de"};
  }return null;}
window.genKunstHLExt=genKunstHLExt;

function genKunstMatchExt(field,prompt,fixedPool){var _KD=KUNST_DATA;
  var valid=Object.keys(_KD).filter(function(k){return Object.prototype.hasOwnProperty.call(_KD,k)&&_KD[k][field]!=null&&_KD[k][field]!=="";});
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length),entry=valid[idx],correct=String(_KD[entry][field]);
  var pool=fixedPool?fixedPool.filter(function(v){return v!==correct;})
    :valid.map(function(n){return String(_KD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});
  if(pool.length<3)return null;
  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}
  var opts=[correct].concat(pool.slice(0,3));
  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}
  return{type:"uk_match",prompt:prompt,subj:entry,ans:correct,opts:opts,lid:"kunst_"+field+"_"+idx,cc:"de"};
}
window.genKunstMatchExt=genKunstMatchExt;'''

# ── 3.5 i18n Strings ─────────────────────────────────────────────────────────
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

# ── 3.6 MODES Array ───────────────────────────────────────────────────────────
MODES_ANCHOR = (
    '    {id:"myth_match_tier",icon:"\\u{1F98A}",title:"Mythologie: Tier-Symbol",'
    'group:"mythologie",prompt:"Welches Tier ist mit dieser Gottheit verbunden?",'
    'desc:"Adler, Eule, Schlange \\u2014 erkenne das Tier-Symbol.",prompt_en:"Which animal is associated with this deity?"},'
)
MODES_NEW = MODES_ANCHOR + """
    /* Phase 438: Freizeitparks & Achterbahnen */
    {id:"hl_park_speed",icon:"\\u{1F3A2}",title:"Freizeitpark: Topspeed",group:"themeparks",prompt:"Welche Achterbahn ist schneller?",desc:"km/h — von Steel Vengeance bis Formula Rossa.",prompt_en:"Which roller coaster is faster?"},
    {id:"hl_park_hoehe",icon:"\\u{1F3A2}",title:"Freizeitpark: Höhe",group:"themeparks",prompt:"Welcher Freizeitpark ist höher?",desc:"Höhe der Anlage in Metern.",prompt_en:"Which amusement park ride is higher?"},
    {id:"hl_park_inversionen",icon:"\\u{1F503}",title:"Freizeitpark: Inversionen",group:"themeparks",prompt:"Welche Achterbahn hat mehr Inversionen?",desc:"Loopings & Korkenzieher zählen!",prompt_en:"Which roller coaster has more inversions?"},
    {id:"hl_park_baujahr",icon:"\\u{1F4C5}",title:"Freizeitpark: Ältester Park",group:"themeparks",prompt:"Welcher Freizeitpark ist älter?",desc:"Früheres Baujahr = Sieger.",prompt_en:"Which amusement park is older?"},
    {id:"park_match_land",icon:"\\u{1F30D}",title:"Freizeitpark: Land",group:"themeparks",prompt:"Aus welchem Land stammt dieser Freizeitpark?",desc:"Von DACH bis Japan — erkenne das Herkunftsland.",prompt_en:"Which country is this amusement park from?"},
    {id:"park_match_kategorie",icon:"\\u{1F3A0}",title:"Freizeitpark: Typ",group:"themeparks",prompt:"Welchem Typ gehört diese Attraktion an?",desc:"Achterbahn, Wasserbahn, Darkride oder Park?",prompt_en:"Which type does this attraction belong to?"},
    {id:"timeline_park_baujahr",icon:"\\u{1F3A2}",title:"Freizeitpark-Timeline",group:"themeparks",prompt:"Welcher Park / welche Bahn ist älter?",desc:"Von Tivoli 1843 bis Movie Park 1996.",prompt_en:"Which park/coaster is older?"},
    {id:"ws_park_achterbahn",icon:"\\u{1F3A2}",title:"WS: Achterbahn",group:"themeparks",noMultiplayer:true,prompt:"Bilde Wörter aus ACHTERBAHN!",desc:"Anagramm-Rätsel — 10 Buchstaben",prompt_en:"Form words from ACHTERBAHN!"},
    /* Phase 438: Kunstgeschichte */
    {id:"hl_kunst_jahr",icon:"\\u{1F5BC}\\uFE0F",title:"Kunstgeschichte: Älteres Werk",group:"kunst",prompt:"Welches Kunstwerk ist älter?",desc:"Früheres Entstehungsjahr = Sieger. Auch v.Chr.!",prompt_en:"Which artwork is older?"},
    {id:"hl_kunst_wert",icon:"\\u{1F4B0}",title:"Kunstgeschichte: Schätzwert",group:"kunst",prompt:"Welches Kunstwerk hat einen höheren Schätzwert?",desc:"Geschätzter Marktwert in Mio. USD.",prompt_en:"Which artwork has a higher estimated value?"},
    {id:"kunst_match_kuenstler",icon:"\\u{1F58C}\\uFE0F",title:"Kunstgeschichte: Künstler",group:"kunst",prompt:"Wer hat dieses Kunstwerk erschaffen?",desc:"Von Da Vinci bis Banksy — erkenne den Künstler.",prompt_en:"Who created this artwork?"},
    {id:"kunst_match_epoche",icon:"\\u{1F3DB}\\uFE0F",title:"Kunstgeschichte: Epoche",group:"kunst",prompt:"Welcher Kunstepoche gehört dieses Werk an?",desc:"Renaissance, Barock, Impressionismus & Co.",prompt_en:"Which art epoch does this work belong to?"},
    {id:"kunst_match_museum",icon:"\\u{1F3DB}\\uFE0F",title:"Kunstgeschichte: Museum",group:"kunst",prompt:"In welchem Museum befindet sich dieses Werk?",desc:"Louvre, Prado, MoMA — erkenne den Standort.",prompt_en:"In which museum is this work located?"},
    {id:"timeline_kunst_jahr",icon:"\\u{1F5BC}\\uFE0F",title:"Kunst-Timeline",group:"kunst",prompt:"Welches Kunstwerk ist älter?",desc:"Von der Antike bis zur Moderne — Kunstgeschichte sortieren.",prompt_en:"Which artwork is older?"},
    {id:"ws_kunst_renaissance",icon:"\\u{1F3AD}",title:"WS: Renaissance",group:"kunst",noMultiplayer:true,prompt:"Bilde Wörter aus RENAISSANCE!",desc:"Anagramm-Rätsel — 11 Buchstaben",prompt_en:"Form words from RENAISSANCE!"},"""

# ── 3.7 MODE_CATS ─────────────────────────────────────────────────────────────
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

# ── 3.8 Dispatcher ────────────────────────────────────────────────────────────
DISP_ANCHOR = '  ws_arch_fundament:()=>{initArchitekturWS("fundament");return null;},'
DISP_NEW = (
    '  ws_arch_fundament:()=>{initArchitekturWS("fundament");return null;},\n'
    '  /* Phase 438: Freizeitparks */\n'
    '  hl_park_speed:()=>genParksHLExt("max_speed_kmh",{unit:"km/h",'
    'prompt:_tc("Welche Achterbahn ist schneller?")}),\n'
    '  hl_park_hoehe:()=>genParksHLExt("max_hoehe_m",{unit:"m",'
    'prompt:_tc("Welcher Freizeitpark ist höher?")}),\n'
    '  hl_park_inversionen:()=>genParksHLExt("inversionen",{unit:"",'
    'prompt:_tc("Welche Achterbahn hat mehr Inversionen?")}),\n'
    '  hl_park_baujahr:()=>genParksHLExt("baujahr",{lowerWins:true,unit:"",'
    'prompt:_tc("Welcher Freizeitpark ist älter?")}),\n'
    '  park_match_land:()=>genParksMatchExt("park_land",'
    '_tc("Aus welchem Land stammt dieser Freizeitpark?")),\n'
    '  park_match_kategorie:()=>genParksMatchExt("kategorie",'
    '_tc("Welchem Typ gehört diese Attraktion an?"),'
    '["Achterbahn","Wasserbahn","Darkride","Park"]),\n'
    '  timeline_park_baujahr:()=>genTimelineQ("park_baujahr"),\n'
    '  ws_park_achterbahn:()=>{initParksWS("achterbahn");return null;},\n'
    '  /* Phase 438: Kunstgeschichte */\n'
    '  hl_kunst_jahr:()=>genKunstHLExt("entstehungsjahr",{lowerWins:true,unit:"",'
    'prompt:_tc("Welches Kunstwerk ist älter?")}),\n'
    '  hl_kunst_wert:()=>genKunstHLExt("schaetzwert_mio_usd",{unit:"Mio. USD",'
    'prompt:_tc("Welches Kunstwerk hat einen höheren Schätzwert?")}),\n'
    '  kunst_match_kuenstler:()=>genKunstMatchExt("kuenstler",'
    '_tc("Wer hat dieses Kunstwerk erschaffen?")),\n'
    '  kunst_match_epoche:()=>genKunstMatchExt("epoche",'
    '_tc("Welcher Kunstepoche gehört dieses Werk an?")),\n'
    '  kunst_match_museum:()=>genKunstMatchExt("standort_museum",'
    '_tc("In welchem Museum befindet sich dieses Werk?")),\n'
    '  timeline_kunst_jahr:()=>genTimelineQ("kunst_jahr"),\n'
    '  ws_kunst_renaissance:()=>{initKunstWS("renaissance");return null;},'
)

# ── 3.9 Replace-Kette ─────────────────────────────────────────────────────────
REPL_OLD = "  .replace('PLACEHOLDER_AUTOS',          AUTOS_J)"
REPL_NEW = (
    "  .replace('PLACEHOLDER_AUTOS',          AUTOS_J)\n"
    "  .replace('PLACEHOLDER_PARKS_WS',       PARKS_WS_J)\n"
    "  .replace('PLACEHOLDER_PARKS',          PARKS_J)\n"
    "  .replace('PLACEHOLDER_KUNST_WS',       KUNST_WS_J)\n"
    "  .replace('PLACEHOLDER_KUNST',          KUNST_J)"
)

patch(GEN, [
    (LOAD_OLD,        LOAD_NEW,        'Py: 4 neue Dateien laden'),
    (CONST_OLD,       CONST_NEW,       'JS: PARKS/KUNST Konstanten'),
    (MKWS_OLD,        MKWS_NEW,        'JS: initParksWS + initKunstWS'),
    (GEN_ANCHOR,      GEN_NEW,         'JS: Generator-Funktionen Parks/Kunst'),
    (I18N_PL_OLD,     I18N_PL_NEW,     'i18n PL: 11 neue Strings'),
    (I18N_EN_OLD,     I18N_EN_NEW,     'i18n EN: 11 neue Strings'),
    (MODES_ANCHOR,    MODES_NEW,       'MODES: 15 neue Modi'),
    (CATS_ANCHOR,     CATS_NEW,        'MODE_CATS: themeparks + kunst'),
    (DISP_ANCHOR,     DISP_NEW,        'GEN dispatch: 15 neue Einträge'),
    (REPL_OLD,        REPL_NEW,        'Replace-Kette: PARKS_WS/PARKS/KUNST_WS/KUNST'),
])

print('\n✅ Patch 438 abgeschlossen! Führe jetzt `python3 check_session.py` aus