#!/usr/bin/env python3
"""
Phase: 360
Date:  2026-06-01
Author: Claude / Andre
Scope: Gaming-Kategorie — 50 Spiele, 15 Spielmodi

Neue Kategorie "games" mit:
  H/L (7): release, vk_mio, downloads_mio, usk, pegi, metacritic, sequel_count
  Match (5): genre, dev_land (Geography!), kategorie, adaption, plattform
  Pin (1): Entwicklerstudio auf Weltkarte einpinnen
  Baujahr-MC (1): "Wann erschien [Spiel]?" — 4 Jahreszahlen
  Verfilmung-MC (1): "Welches dieser Spiele hat eine Verfilmung?"
  Gesamt: 15 neue Modi

Die inhaltliche Brücke: dev_land/dev_lat/dev_lng → echter GeoQuest-Pin-Modus.
  "Wo sitzt das Studio hinter Minecraft?" → Stockholm, Schweden → Karte.

Dependencies: Patch 354 — games_extended.json (50 Spiele, 22 Felder)
Zero-Bug Policy: assert c.count(old)==1 vor jedem replace()
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, "gen.py")

def patch(c, old, new, label):
    count = c.count(old)
    assert count == 1, f"[FAIL] Anker {count}× gefunden: {old[:70]!r}"
    print(f"  [OK] {label}")
    return c.replace(old, new, 1)

def run(cmd):
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-500:])
    if r.stderr and r.returncode != 0: print(r.stderr[-200:], file=sys.stderr)
    return r.returncode

if __name__ == "__main__":
    print("=" * 62)
    print("PATCH 360 — Gaming-Kategorie: 15 Modi, 50 Spiele")
    print("=" * 62)

    # games_extended.json compact schreiben
    ext_path = os.path.join(ROOT, "data", "games_extended.json")
    with open(ext_path, encoding="utf-8") as f:
        games_data = json.load(f)
    compact = json.dumps(games_data, ensure_ascii=False, separators=(',', ':'))
    with open(ext_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(games_data, ensure_ascii=False, indent=2))
    print(f"  games_extended.json: {len(games_data)} Spiele, {len(compact):,} Bytes (compact)")

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    # ── 1: Python — games_extended.json laden ─────────────────────────────
    OLD_PY = ("with open(os.path.join(os.path.dirname(__file__), "
              "'data/autos_extended.json'), 'r', encoding='utf-8') as _f:\n"
              "    import json as _ejson\n"
              "    AUTOS_EXT_J  = _ejson.dumps(_ejson.load(_f), "
              "ensure_ascii=False, separators=(',',':]')" )

    # Use simpler anchor
    OLD_PY = "AUTOS_EXT_J  = _ejson.dumps(_ejson.load(_f), ensure_ascii=False, separators=(',',':'))"
    NEW_PY = (OLD_PY + "\n"
              "with open(os.path.join(os.path.dirname(__file__), "
              "'data/games_extended.json'), 'r', encoding='utf-8') as _f:\n"
              "    import json as _gjson\n"
              "    GAMES_EXT_J  = _gjson.dumps(_gjson.load(_f), "
              "ensure_ascii=False, separators=(',',':]')" )

    # Simpler: just find autos_ext replace line
    OLD_PY = "AUTOS_EXT_J  = _ejson.dumps(_ejson.load(_f), ensure_ascii=False, separators=(',',':'))"
    NEW_PY = (OLD_PY + "\n"
              "with open(os.path.join(os.path.dirname(__file__), "
              "'data/games_extended.json'), 'r', encoding='utf-8') as _gf:\n"
              "    GAMES_EXT_J  = __import__('json').dumps(__import__('json').load(_gf), "
              "ensure_ascii=False, separators=(',',':'))")
    c = patch(c, OLD_PY, NEW_PY, "Python: games_extended.json laden")

    # ── 2: Python — PLACEHOLDER ersetzen ──────────────────────────────────
    OLD_REPL = ".replace('PLACEHOLDER_AUTOS_EXT',      AUTOS_EXT_J)"
    NEW_REPL = (".replace('PLACEHOLDER_AUTOS_EXT',      AUTOS_EXT_J)\n"
                "  .replace('PLACEHOLDER_GAMES_EXT',      GAMES_EXT_J)")
    c = patch(c, OLD_REPL, NEW_REPL, "Python: replace PLACEHOLDER_GAMES_EXT")

    # ── 3: JS — Konstante + Engines ────────────────────────────────────────
    OLD_CONST = "const AUTOS_EXT_DATA=PLACEHOLDER_AUTOS_EXT;"
    NEW_CONST = ("const AUTOS_EXT_DATA=PLACEHOLDER_AUTOS_EXT;\n"
                 "const GAMES_EXT_DATA=PLACEHOLDER_GAMES_EXT;")
    c = patch(c, OLD_CONST, NEW_CONST, "JS: const GAMES_EXT_DATA")

    # ── 4: JS — Generator-Funktionen ──────────────────────────────────────
    OLD_FN = "/* Phase 353: Generationen-Match"
    NEW_FN = ("""/* Phase 360: Gaming-Engines */

/* genGamesHLExt — H/L aus GAMES_EXT_DATA */
function genGamesHLExt(field,opts){
  var o=opts||{};
  var items=[];
  var _GE=GAMES_EXT_DATA;
  var _ks=Object.keys(_GE);
  for(var _i=0;_i<_ks.length;_i++){
    var _n=_ks[_i];
    var _v=_GE[_n][field];
    if(_v===null||_v===undefined||_v===0||_v===0.0)continue;
    items.push({name:_n,val:+_v});
  }
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});
  var len=items.length;
  var tries=0;
  while(tries++<40){
    var ai=~~(rng()*len);
    var W=Math.max(1,Math.floor(len*(S.diff==='hardcore'?0.03:0.15)));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];
    for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}
    if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)];
    var a=items[ai],b=items[bi];
    if(a.val===b.val)continue;
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"";
    var meta=a.name+": "+a.val+(unit?" "+unit:"")+" · "+b.name+": "+b.val+(unit?" "+unit:"");
    return{type:"beta_hl",prompt:o.prompt||"Welches ist höher?",subj:"",
      opts:[a.name,b.name],ans:winner.name,meta:meta,
      lid:"ghl_"+field+"_"+ai+"_"+bi,cc:"de"};
  }
  return null;
}

/* genGamesMatchExt — Match aus GAMES_EXT_DATA */
function genGamesMatchExt(field,prompt,fixedPool){
  var _GE=GAMES_EXT_DATA;
  var valid=Object.keys(_GE).filter(function(n){
    var v=_GE[n][field];
    return v!==null&&v!==undefined&&v!=="";
  });
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length);
  var game=valid[idx];
  var correct=String(_GE[game][field]);
  var pool=fixedPool
    ?fixedPool.filter(function(v){return v!==correct;})
    :[...new Set(valid.map(function(n){return String(_GE[n][field]);}))].filter(function(v){return v!==correct;});
  if(pool.length<3)return null;
  var p=pool.slice();
  for(var j=p.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=p[j];p[j]=p[k];p[k]=t;}
  var opts=[correct].concat(p.slice(0,3));
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}
  return{type:"uk_match",prompt:prompt||("Was gilt für "+game+"?"),
    subj:game,ans:correct,opts:opts,lid:"gmatch_"+field+"_"+idx,cc:"de"};
}

/* genGamesPinQ — Entwicklerstudio auf Weltkarte einpinnen */
function genGamesPinQ(){
  var _GE=GAMES_EXT_DATA;
  var valid=Object.keys(_GE).filter(function(n){
    var d=_GE[n];
    return d.dev_lat&&d.dev_lng&&d.dev_city&&d.developer;
  });
  if(valid.length<2)return null;
  var idx=~~(rng()*valid.length);
  var game=valid[idx];
  var d=_GE[game];
  var subj="\""+game+"\" ("+d.developer+", "+d.dev_land+")";
  return{type:"uk_pin",
    prompt:"Wo hat das Entwicklerstudio von "+game+" seinen Hauptsitz?",
    subj:subj,ans:game+" → "+d.dev_city,
    targetLat:d.dev_lat,targetLng:d.dev_lng,
    lid:"gpin_"+idx,cc:"de"};
}

/* genGamesBaujahrMC — "Wann erschien dieses Spiel?" */
function genGamesBaujahrMC(){
  var _GE=GAMES_EXT_DATA;
  var keys=Object.keys(_GE);
  if(keys.length<8)return null;
  var idx=~~(rng()*keys.length);
  var game=keys[idx];
  var correct=_GE[game].release;
  var allYears=keys.map(function(n){return _GE[n].release;});
  var pool=allYears.filter(function(y){var d=Math.abs(y-correct);return d>=2&&d<=20;});
  if(pool.length<3)pool=allYears.filter(function(y){return y!==correct;}).sort(function(){return rng()-0.5;});
  var p=pool.slice();
  for(var j=p.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=p[j];p[j]=p[k];p[k]=t;}
  var opts=[correct].concat(p.slice(0,3));
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}
  return{type:"uk_match",prompt:"In welchem Jahr erschien dieses Spiel erstmals?",
    subj:game,ans:String(correct),opts:opts.map(String),
    lid:"gbj_"+idx,cc:"de"};
}

""" + OLD_FN)
    c = patch(c, OLD_FN, NEW_FN, "JS: 5 Gaming-Funktionen")

    # ── 5: MODES — 15 neue Games-Modi ────────────────────────────────────
    OLD_MODES = 'prompt_en:"When did this generation of the model line appear?"},'
    NEW_MODES = (OLD_MODES + """
    {id:"games_pin",          icon:"\\u{1F579}\\uFE0F",title:"Game-Studio pinnen",        group:"games",prompt:"Wo hat das Entwicklerstudio dieses Spiels seinen Hauptsitz?",      desc:"50 Studios weltweit \\u2014 von Tokyo bis Helsinki",         prompt_en:"Where is the game's developer studio located?"},
    {id:"games_match_land",   icon:"\\u{1F30D}\\u{1F3AE}",title:"Game-Studio: Herkunftsland",group:"games",prompt:"Aus welchem Land kommt das Studio hinter diesem Spiel?",        desc:"Japan, USA, Schweden, Polen \\u2014 50 Studios",              prompt_en:"Which country is this game studio from?"},
    {id:"games_match_genre",  icon:"\\u{1F3AE}",title:"Spielgenre zuordnen",               group:"games",prompt:"Welchem Genre geh\\u00f6rt dieses Spiel an?",                    desc:"Battle Royale, RPG, MOBA, Sandbox \\u2014 15 Genres",        prompt_en:"Which genre does this game belong to?"},
    {id:"games_match_adaption",icon:"\\u{1F3AC}",title:"Game-Verfilmung",                  group:"games",prompt:"Wurde dieses Spiel verfilmt oder als Serie adaptiert?",           desc:"Film / Serie / Anime \\u2014 oder kein Remake?",             prompt_en:"Has this game been adapted as film or series?"},
    {id:"games_match_plattform",icon:"\\u{1F4BB}",title:"Spielplattform",                  group:"games",prompt:"F\\u00fcr welche Plattform erschien dieses Spiel prim\\u00e4r?",  desc:"PC / Konsole / Mobil / Multiplattform",                      prompt_en:"On which platform did this game primarily release?"},
    {id:"games_match_kategorie",icon:"\\u{1F4C2}",title:"Gaming-\\u00c4ra",               group:"games",prompt:"Zu welcher Gaming-Kategorie geh\\u00f6rt dieses Spiel?",          desc:"Modern Youth / Global Mobile / Klassiker",                   prompt_en:"Which gaming era does this game belong to?"},
    {id:"hl_games_release",   icon:"\\u{1F4C5}",title:"Game-Quartett: Erscheinungsjahr",   group:"games",prompt:"Welches Spiel erschien sp\\u00e4ter?",                           desc:"Von Pac-Man (1980) bis EA FC 24 (2023)",                     prompt_en:"Which game was released later?"},
    {id:"hl_games_vk",        icon:"\\u{1F4B0}",title:"Game-Quartett: Verkaufszahlen",     group:"games",prompt:"Welches Spiel wurde h\\u00e4ufiger verkauft?",                   desc:"Nur Kaufspiele \\u2014 in Millionen verkaufter Exemplare",    prompt_en:"Which game sold more copies?"},
    {id:"hl_games_downloads",  icon:"\\u{1F4F1}",title:"Game-Quartett: Downloads",         group:"games",prompt:"Welches F2P-Spiel wurde \\u00f6fter heruntergeladen?",            desc:"Nur Free-to-Play \\u2014 in Millionen Downloads",             prompt_en:"Which F2P game has more downloads?"},
    {id:"hl_games_metacritic", icon:"\\u2B50",   title:"Game-Quartett: Metacritic",        group:"games",prompt:"Welches Spiel wurde von Kritikern besser bewertet?",              desc:"Nur Spiele mit offiziellem Metacritic-Score",                 prompt_en:"Which game has a higher Metacritic score?"},
    {id:"hl_games_usk",       icon:"\\u{1F51E}",title:"Game-Quartett: Altersfreigabe USK", group:"games",prompt:"Welches Spiel hat eine h\\u00f6here USK-Freigabe?",              desc:"USK 0 / 6 / 12 / 16 / 18",                                   prompt_en:"Which game has a higher USK age rating?"},
    {id:"hl_games_sequel",    icon:"\\u{1F522}",title:"Game-Quartett: Teile-Anzahl",       group:"games",prompt:"Welche Spielserie hat mehr direkte Nachfolger?",                  desc:"Anzahl direkter Hauptteile nach diesem Spiel",               prompt_en:"Which game franchise has more sequels?"},
    {id:"games_baujahr_mc",   icon:"\\u{1F5D3}\\uFE0F\\u2753",title:"Gaming: Erscheinungsjahr raten",group:"games",prompt:"In welchem Jahr erschien dieses Spiel erstmals?",  desc:"4 Jahreszahlen \\u2014 welche ist die richtige?",             prompt_en:"In which year was this game first released?"},""")
    c = patch(c, OLD_MODES, NEW_MODES, "MODES: 13 Gaming-Modi")

    # ── 6: MODE_CATS — neue Gruppe "games" ────────────────────────────────
    OLD_CATS = ('autos:{label:"Auto-Quartett",icon:"\\u{1F3CE}\\uFE0F",'
                'modes:[')
    NEW_CATS = ('games:{label:"Gaming",icon:"\\u{1F3AE}",'
                'modes:["games_pin","games_match_land","games_match_genre",'
                '"games_match_adaption","games_match_plattform","games_match_kategorie",'
                '"hl_games_release","hl_games_vk","hl_games_downloads",'
                '"hl_games_metacritic","hl_games_usk","hl_games_sequel",'
                '"games_baujahr_mc"],cost:0},\n  '
                + OLD_CATS)
    c = patch(c, OLD_CATS, NEW_CATS, "MODE_CATS: Gaming-Gruppe")

    # ── 7: GEN dispatch ───────────────────────────────────────────────────
    OLD_GEN = "  auto_generationen_match:()=>genAutoGenerationenMatch(),"
    NEW_GEN = (OLD_GEN + "\n"
               "  games_pin:()=>genGamesPinQ(),\n"
               "  games_match_land:()=>genGamesMatchExt(\"dev_land\","
               "\"Aus welchem Land kommt das Studio hinter diesem Spiel?\",null),\n"
               "  games_match_genre:()=>genGamesMatchExt(\"genre\","
               "\"Welchem Genre geh\\u00f6rt dieses Spiel an?\",null),\n"
               "  games_match_adaption:()=>genGamesMatchExt(\"adaption\","
               "\"Wurde dieses Spiel verfilmt?\","
               "[\"Film\",\"Serie\",\"Anime\"]),\n"
               "  games_match_plattform:()=>genGamesMatchExt(\"plattform\","
               "\"Auf welcher Plattform l\\u00e4uft dieses Spiel?\","
               "[\"PC\",\"Konsole\",\"Mobil\",\"Multiplattform\"]),\n"
               "  games_match_kategorie:()=>genGamesMatchExt(\"kategorie\","
               "\"Zu welcher Gaming-\\u00c4ra geh\\u00f6rt dieses Spiel?\","
               "[\"Modern Youth\",\"Global Mobile\",\"Klassiker\"]),\n"
               "  hl_games_release:()=>genGamesHLExt(\"release\","
               "{unit:\"Jahr\",prompt:\"Welches Spiel erschien sp\\u00e4ter?\"}),\n"
               "  hl_games_vk:()=>genGamesHLExt(\"vk_mio\","
               "{unit:\"Mio. Exemplare\",prompt:\"Welches Spiel wurde h\\u00e4ufiger verkauft?\"}),\n"
               "  hl_games_downloads:()=>genGamesHLExt(\"downloads_mio\","
               "{unit:\"Mio. Downloads\",prompt:\"Welches F2P-Spiel wurde \\u00f6fter heruntergeladen?\"}),\n"
               "  hl_games_metacritic:()=>genGamesHLExt(\"metacritic\","
               "{unit:\"Punkte\",prompt:\"Welches Spiel wurde besser bewertet?\"}),\n"
               "  hl_games_usk:()=>genGamesHLExt(\"usk\","
               "{unit:\"USK\",prompt:\"Welches Spiel hat eine h\\u00f6here Altersfreigabe?\"}),\n"
               "  hl_games_sequel:()=>genGamesHLExt(\"sequel_count\","
               "{unit:\"Teile\",prompt:\"Welche Spielserie hat mehr direkte Nachfolger?\"}),\n"
               "  games_baujahr_mc:()=>genGamesBaujahrMC(),")
    c = patch(c, OLD_GEN, NEW_GEN, "GEN dispatch: 13 Gaming-Modi")

    with open(GEN, "w", encoding="utf-8") as f:
        f.write(c)
    print("\n  gen.py gespeichert")

    print("\n  Build …")
    if run([sys.executable, "gen.py"]) != 0: sys.exit(1)
    print("  Verify …")
    if run([sys.executable, "verify.py"]) != 0: sys.exit(1)
    run([sys.executable, "validate_content.py"])

    r = subprocess.run([
        sys.executable, "post_phase.py",
        "--phase", "360",
        "--patch", "patches/patch_360_games_engine.py",
        "--summary",
        "Gaming-Kategorie: 50 Spiele (30 Modern/Mobile + 20 Klassiker), "
        "13 Modi (games_pin, genre/land/adaption-Match, H/L release/vk/metacritic/usk, "
        "Baujahr-MC). Bridge: dev_lat/dev_lng → echter GeoQuest-Pin-Modus."
    ], cwd=ROOT, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-600:])
    print("\n✅ Phase 360 — Gaming-Kategorie live!")
