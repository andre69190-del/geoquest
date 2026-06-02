#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 429: Kategorie "Serien" (D-A-CH Fokus) — 7 neue Modi.

Bindet data/serien_extended.json (98 Serien, 73x D-A-CH) ein und registriert
die Kategorie `serien` mit 7 Modi (4x H/L, 2x Match, 1x Timeline).
Zero-Bug-Policy: jede Ersetzung via assert count==1.
i18n: alle Gameplay-Prompts via _tc(), Übersetzungen DE/EN/PL ergänzt.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, 'gen.py')
VAL  = os.path.join(ROOT, 'validate_content.py')


def patch_file(path, edits, label):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    for old, new, tag in edits:
        n = c.count(old)
        assert n == 1, f'[{label}] Anchor "{tag}" count={n} (erwartet 1)'
        c = c.replace(old, new)
        print(f'  OK  {label}: {tag}')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)


# ════════════════════════════════════════════════════════════════════════════
# 1) gen.py
# ════════════════════════════════════════════════════════════════════════════

# --- 1a. Loader (innerhalb des bestehenden try-Blocks, nach games_extended) ---
LOAD_ANCHOR = ("        GAMES_EXT_J = __import__('json').dumps(__import__('json')"
               ".load(_gf), ensure_ascii=False, separators=(',',':'))")
LOAD_NEW = LOAD_ANCHOR + (
    "\n    with open(os.path.join(os.path.dirname(__file__), "
    "'data/serien_extended.json'), 'r', encoding='utf-8') as _serf:\n"
    "        SERIEN_EXT_J = __import__('json').dumps(__import__('json')"
    ".load(_serf), ensure_ascii=False, separators=(',',':'))")

# --- 1b. Konstante (nach GAMES_EXT_DATA) ---
CONST_ANCHOR = "const GAMES_EXT_DATA=PLACEHOLDER_GAMES_EXT;"
CONST_NEW = CONST_ANCHOR + "\nconst SERIEN_EXT_DATA=PLACEHOLDER_SERIEN_EXT;"

# --- 1c. Placeholder-Replace (nach GAMES_EXT; eigene, kollisionsfreie Marke) ---
REPL_ANCHOR = "  .replace('PLACEHOLDER_GAMES_EXT',      GAMES_EXT_J)"
REPL_NEW = REPL_ANCHOR + "\n  .replace('PLACEHOLDER_SERIEN_EXT',     SERIEN_EXT_J)"

# --- 1d. MODES-Array (nach letztem Musik-Eintrag) ---
MODES_ANCHOR = 'prompt_en:"Which song is a well-known hit by this artist?"}'
MODES_NEW = MODES_ANCHOR + ''',
    {id:"hl_serie_start",icon:"\\u{1F4C5}",title:"Serien-Quartett: \\u00c4lter",group:"serien",prompt:"Welche Serie startete fr\\u00fcher?",desc:"Von 1970 (Tatort) bis heute \\u2014 wann lief die Serie zuerst?",prompt_en:"Which series started earlier?"},
    {id:"hl_serie_staffeln",icon:"\\u{1F4FA}",title:"Serien-Quartett: Staffeln",group:"serien",prompt:"Welche Serie hat mehr Staffeln?",desc:"Von der Mini-Serie bis zur Dauerl\\u00e4ufer-Soap.",prompt_en:"Which series has more seasons?"},
    {id:"hl_serie_episoden",icon:"\\u{1F3AC}",title:"Serien-Quartett: Episoden",group:"serien",prompt:"Welche Serie hat mehr Episoden?",desc:"Von 3 bis \\u00fcber 7000 Folgen.",prompt_en:"Which series has more episodes?"},
    {id:"hl_serie_imdb",icon:"\\u2B50",title:"Serien-Quartett: IMDb-Rating",group:"serien",prompt:"Welche Serie hat die h\\u00f6here IMDb-Bewertung?",desc:"Das Urteil der Zuschauer \\u2014 von Soap bis Kult.",prompt_en:"Which series has the higher IMDb rating?"},
    {id:"serie_match_land",icon:"\\u{1F30D}",title:"Serien-Quiz: Herkunft",group:"serien",prompt:"Aus welchem Land stammt diese Serie?",desc:"D-A-CH und die Welt \\u2014 erkenne das Produktionsland.",prompt_en:"Which country is this series from?"},
    {id:"serie_match_genre",icon:"\\u{1F3AD}",title:"Serien-Quiz: Genre",group:"serien",prompt:"Welches Genre hat diese Serie?",desc:"Krimi, Comedy, Drama, Sci-Fi/Mystery oder Doku?",prompt_en:"What genre is this series?"},
    {id:"timeline_serie_start",icon:"\\u23F3",title:"Serien-Timeline",group:"serien",prompt:"Welche Serie startete zuerst?",desc:"Bring die Serien in chronologische Startreihenfolge.",prompt_en:"Which series started first?"}'''

# --- 1e. MODE_CATS (neue Kategorie nach musik) ---
CATS_ANCHOR = '"musik_match_hit"],cost:0},'
CATS_NEW = CATS_ANCHOR + '  serien:{label:"Serien",icon:"\\u{1F4FA}",modes:["hl_serie_start","hl_serie_staffeln","hl_serie_episoden","hl_serie_imdb","serie_match_land","serie_match_genre","timeline_serie_start"],cost:0},'

# --- 1f. Generatoren (nach genMusikMatchExt) ---
GEN_FN_ANCHOR = "window.genMusikMatchExt=genMusikMatchExt;"
GEN_FN_NEW = GEN_FN_ANCHOR + r"""

/* Phase 429: genSerienHLExt -- H/L ueber numerische Serien-Felder */
function genSerienHLExt(field,opts){
  var o=opts||{};var items=[];
  var _SD=SERIEN_EXT_DATA;
  var _ks=Object.keys(_SD).filter(function(k){return Object.prototype.hasOwnProperty.call(_SD,k);});
  for(var _i=0;_i<_ks.length;_i++){
    var _n=_ks[_i],_v=+(_SD[_n][field]);
    if(!isNaN(_v)&&_v>0)items.push({name:_n,val:_v});
  }
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});
  var len=items.length,tries=0;
  while(tries++<40){
    var ai=~~(rng()*len),W=Math.max(1,Math.floor(len*0.15));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}
    if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)];
    var a=items[ai],b=items[bi];
    if(a.val===b.val)continue;
    var span=items[len-1].val-items[0].val;
    if(span>0&&Math.abs(a.val-b.val)<span*0.01)continue;
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"";
    var meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");
    return{type:"beta_hl",prompt:o.prompt||_tc("Welche Serie hat mehr Staffeln?"),subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,lid:"serhl_"+field+"_"+ai+"_"+bi,cc:"de"};
  }
  return null;
}
window.genSerienHLExt=genSerienHLExt;

/* Phase 429: genSerienMatchExt -- Match ueber kategoriale Serien-Felder */
function genSerienMatchExt(field,prompt,fixedPool){
  var _SD=SERIEN_EXT_DATA;
  var valid=Object.keys(_SD).filter(function(k){return Object.prototype.hasOwnProperty.call(_SD,k)&&_SD[k][field]!=null&&_SD[k][field]!=="";});
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length),serie=valid[idx];
  var correct=String(_SD[serie][field]);
  var pool=fixedPool
    ?fixedPool.filter(function(v){return v!==correct;})
    :valid.map(function(n){return String(_SD[n][field]);}).filter(function(v,i,a){return a.indexOf(v)===i&&v!==correct;});
  if(pool.length<3)return null;
  for(var k=pool.length-1;k>0;k--){var t=~~(rng()*(k+1));var tmp=pool[k];pool[k]=pool[t];pool[t]=tmp;}
  var opts=[correct].concat(pool.slice(0,3));
  for(var m=opts.length-1;m>0;m--){var t2=~~(rng()*(m+1));var tm=opts[m];opts[m]=opts[t2];opts[t2]=tm;}
  return{type:"uk_match",prompt:prompt,subj:serie,ans:correct,opts:opts,lid:"sermatch_"+field+"_"+idx,cc:"de"};
}
window.genSerienMatchExt=genSerienMatchExt;

/* Phase 429: genSerienTimelineQ -- Startjahre chronologisch sortieren */
function genSerienTimelineQ(){
  var _SD=SERIEN_EXT_DATA;
  var keys=Object.keys(_SD).filter(function(k){return Object.prototype.hasOwnProperty.call(_SD,k)&&_SD[k].start_jahr;});
  if(keys.length<4)return null;
  var arr=keys.map(function(k){return{n:k,year:+_SD[k].start_jahr};});
  var pool=sh(arr.slice());
  var seen={},picked=[];
  for(var _i=0;_i<pool.length&&picked.length<5;_i++){var yr=pool[_i].year;if(!seen[yr]){seen[yr]=1;picked.push(pool[_i]);}}
  if(picked.length<4)return null;
  var items=picked.slice(0,rng()<.4&&picked.length>=5?5:4);
  var sorted=items.slice().sort(function(a,b){return a.year-b.year;});
  var ans=sorted.map(function(it){return it.n;});
  var lid='tl_serie_'+ans.join('|').replace(/[^a-zA-Z0-9_|]/g,'').slice(0,40);
  return{type:'timeline',prompt:_tc("Welche Serie startete zuerst?"),items:items,ans:ans,unit:'Jahr',lid:lid,cc:null};
}
window.genSerienTimelineQ=genSerienTimelineQ;
"""

# --- 1g. GEN-Dispatcher (nach timeline_musik_gruendung) ---
DISP_ANCHOR = 'timeline_musik_gruendung:()=>genTimelineQ("musik_gruendung"),'
DISP_NEW = DISP_ANCHOR + '''
  hl_serie_start:()=>genSerienHLExt("start_jahr",{lowerWins:true,unit:"",prompt:_tc("Welche Serie startete fr\\u00fcher?")}),
  hl_serie_staffeln:()=>genSerienHLExt("staffeln",{unit:"Staffeln",prompt:_tc("Welche Serie hat mehr Staffeln?")}),
  hl_serie_episoden:()=>genSerienHLExt("episoden",{unit:"Episoden",prompt:_tc("Welche Serie hat mehr Episoden?")}),
  hl_serie_imdb:()=>genSerienHLExt("imdb_rating",{unit:"\\u2605",prompt:_tc("Welche Serie hat die h\\u00f6here IMDb-Bewertung?")}),
  serie_match_land:()=>genSerienMatchExt("produktionsland",_tc("Aus welchem Land stammt diese Serie?"),["Deutschland","\\u00d6sterreich","Schweiz","Vereinigte Staaten","Vereinigtes K\\u00f6nigreich","Frankreich","Spanien","S\\u00fcdkorea"]),
  serie_match_genre:()=>genSerienMatchExt("genre",_tc("Welches Genre hat diese Serie?"),["Krimi","Comedy","Drama","Sci-Fi/Mystery","Doku"]),
  timeline_serie_start:()=>genSerienTimelineQ(),'''

# --- 1h. i18n: PL- und EN-Übersetzungen der neuen _tc-Prompts ---
PL_ANCHOR = '_CONTENT_I18N={"pl":{'
PL_NEW = PL_ANCHOR + (
    '"Welche Serie startete früher?":"Który serial wystartował wcześniej?",'
    '"Welche Serie hat mehr Staffeln?":"Który serial ma więcej sezonów?",'
    '"Welche Serie hat mehr Episoden?":"Który serial ma więcej odcinków?",'
    '"Welche Serie hat die höhere IMDb-Bewertung?":"Który serial ma wyższą ocenę IMDb?",'
    '"Aus welchem Land stammt diese Serie?":"Z jakiego kraju pochodzi ten serial?",'
    '"Welches Genre hat diese Serie?":"Jaki gatunek ma ten serial?",'
    '"Welche Serie startete zuerst?":"Który serial wystartował jako pierwszy?",')

EN_ANCHOR = ',"en":{'
EN_NEW = EN_ANCHOR + (
    '"Welche Serie startete früher?":"Which series started earlier?",'
    '"Welche Serie hat mehr Staffeln?":"Which series has more seasons?",'
    '"Welche Serie hat mehr Episoden?":"Which series has more episodes?",'
    '"Welche Serie hat die höhere IMDb-Bewertung?":"Which series has the higher IMDb rating?",'
    '"Aus welchem Land stammt diese Serie?":"Which country is this series from?",'
    '"Welches Genre hat diese Serie?":"What genre is this series?",'
    '"Welche Serie startete zuerst?":"Which series started first?",')

patch_file(GEN, [
    (LOAD_ANCHOR,  LOAD_NEW,  '1a loader'),
    (CONST_ANCHOR, CONST_NEW, '1b const'),
    (REPL_ANCHOR,  REPL_NEW,  '1c placeholder'),
    (MODES_ANCHOR, MODES_NEW, '1d MODES'),
    (CATS_ANCHOR,  CATS_NEW,  '1e MODE_CATS'),
    (GEN_FN_ANCHOR, GEN_FN_NEW, '1f generators'),
    (DISP_ANCHOR,  DISP_NEW,  '1g dispatcher'),
    (PL_ANCHOR,    PL_NEW,    '1h i18n PL'),
    (EN_ANCHOR,    EN_NEW,    '1h i18n EN'),
], 'gen.py')


# ════════════════════════════════════════════════════════════════════════════
# 2) validate_content.py — check_serien_extended + Dispatch
# ════════════════════════════════════════════════════════════════════════════

CHECK_FN = '''def check_serien_extended(filename, data):
    """Validiert data/serien_extended.json (7 Pflichtfelder, Enums, Typen)."""
    GENRE  = {"Krimi","Comedy","Drama","Sci-Fi/Mystery","Doku"}
    EPOCHE = {"Gegenwart","Historisch","Zukunft"}
    REQUIRED = ["genre","start_jahr","staffeln","episoden",
                "produktionsland","imdb_rating","epochen_setting"]
    if not isinstance(data, dict):
        warn(filename,"struktur","root","serien_extended.json muss ein Dict sein"); return
    for name, entry in data.items():
        if not isinstance(entry, dict):
            warn(filename,"eintrag",name,"Wert ist kein Dict"); continue
        for f in REQUIRED:
            if f not in entry:
                warn(filename,"pflichtfeld",name,f"Feld '{f}' fehlt")
        g = entry.get("genre")
        if g not in GENRE:
            warn(filename,"enum:genre",name,f"Wert {g!r} nicht erlaubt. Erlaubt: {sorted(GENRE)}")
        ep = entry.get("epochen_setting")
        if ep not in EPOCHE:
            warn(filename,"enum:epochen_setting",name,f"Wert {ep!r} nicht erlaubt. Erlaubt: {sorted(EPOCHE)}")
        for field in ("start_jahr","staffeln","episoden"):
            v = entry.get(field)
            if not isinstance(v, int) or isinstance(v, bool):
                warn(filename,f"typ:{field}",name,f"{field} muss int sein")
            elif v <= 0:
                warn(filename,f"wert:{field}",name,f"{field} muss > 0 sein (ist {v})")
        r = entry.get("imdb_rating")
        if not isinstance(r,(int,float)) or isinstance(r, bool):
            warn(filename,"typ:imdb_rating",name,"imdb_rating muss float sein")
        elif not (0.0 <= r <= 10.0):
            warn(filename,"wert:imdb_rating",name,f"imdb_rating ausserhalb 0-10 (ist {r})")
        if not isinstance(entry.get("produktionsland"), str) or not entry.get("produktionsland","").strip():
            warn(filename,"typ:produktionsland",name,"produktionsland muss nicht-leerer str sein")


def check_musik_extended(filename, data):'''

patch_file(VAL, [
    # Check-Funktion vor check_musik_extended einfügen
    ('def check_musik_extended(filename, data):', CHECK_FN, '2a check_serien_extended'),
    # Dispatch-Branch ergänzen
    ('    elif name == "musik_extended.json":\n        check_musik_extended(filename, data)',
     '    elif name == "serien_extended.json":\n        check_serien_extended(filename, data)\n'
     '    elif name == "musik_extended.json":\n        check_musik_extended(filename, data)',
     '2b dispatch'),
], 'validate_content.py')

print('\\nPatch 429 angewendet — Kategorie "Serien" (7 Modi) integriert.')
