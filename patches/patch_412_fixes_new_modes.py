"""Phase 412 — Bugfixes + 6 neue Konsolen-Modi"""
import os, json, re, ast
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def r(p): return open(p,'r',encoding='utf-8').read()
def w(p,c): open(p,'w',encoding='utf-8').write(c)
def rpl(c, old, new, label):
    assert c.count(old)==1, f"ANCHOR {c.count(old)}x: {label!r}"
    return c.replace(old, new)

c = r(os.path.join(ROOT,'gen.py'))

# ─────────────────────────────────────────────────────────────────────────
# FIX 1: match_konsolen_handheld → Ja/Nein
# ─────────────────────────────────────────────────────────────────────────
c = rpl(c,
    'match_konsolen_handheld:()=>genKonsolenMatch("handheld",_tc("Heimkonsole oder Handheld?")),\n',
    'match_konsolen_handheld:()=>genKonsolenHandheldQ(),\n',
    "handheld dispatch")

HANDHELD_FN = """
/* Phase 412: genKonsolenHandheldQ -- Ja/Nein wie genGamesF2PQ */
function genKonsolenHandheldQ(){
  var _KD=KONSOLEN_DATA;
  var keys=Object.keys(_KD).filter(function(k){return Object.prototype.hasOwnProperty.call(_KD,k)});
  if(keys.length<4)return null;
  var idx=~~(rng()*keys.length);
  var cons=keys[idx];
  var isHandheld=_KD[cons].handheld===true;
  var correct=_tc(isHandheld?"Handheld":"Heimkonsole");
  var other=_tc(isHandheld?"Heimkonsole":"Handheld");
  var opts=[correct,other];
  for(var j=opts.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=opts[j];opts[j]=opts[k];opts[k]=t;}
  return{type:"uk_match",prompt:_tc("Heimkonsole oder Handheld?"),
    subj:cons,ans:correct,opts:opts,lid:"khand_"+idx,cc:"de"};
}
"""
c = rpl(c, "/* === Phase 228: Pflanzen-Generatoren === */",
        HANDHELD_FN + "/* === Phase 228: Pflanzen-Generatoren === */",
        "genKonsolenHandheldQ fn")
print("OK 1: match_konsolen_handheld -> Ja/Nein")

# ─────────────────────────────────────────────────────────────────────────
# FIX 2: timeline_auto_bj
# ─────────────────────────────────────────────────────────────────────────
# Find hl_auto_bj MODES entry
idx = c.find('{id:"hl_auto_bj"')
end = c.find('},', idx) + 2
bj_entry = c[idx:end]

TL_AUTO_ENTRY = (
    '\n    {id:"timeline_auto_bj",'
    'icon:"\\u{1F4C5}",'
    'title:"Timeline: Auto-Evolution",'
    'group:"autos",'
    'prompt:"Sortiere die Autos nach Baujahr (\\u00e4ltestes zuerst)!",'
    'desc:"Von Oldtimern bis E-Autos \\u2014 die Geschichte auf R\\u00e4dern.",'
    'prompt_en:"Sort the cars by year of manufacture (oldest first)!",'
    'time:24},'
)
assert c.count(bj_entry) == 1
c = c.replace(bj_entry, bj_entry + TL_AUTO_ENTRY, 1)

c = rpl(c,
    'hl_auto_bj:()=>genAutosHL("auto_bj"),\n',
    'hl_auto_bj:()=>genAutosHL("auto_bj"),\n  timeline_auto_bj:()=>genTimelineQ("auto_bj"),\n',
    "timeline_auto_bj dispatch")

c = rpl(c, '"hl_auto_bj","hl_auto_gewicht"', '"hl_auto_bj","timeline_auto_bj","hl_auto_gewicht"',
        "autos MODE_CATS")

# Build timeline.json auto_bj entries
tl_path = os.path.join(ROOT,'data','timeline.json')
tl = json.loads(r(tl_path))
if 'auto_bj' not in tl:
    ae = json.loads(r(os.path.join(ROOT,'data','autos_extended.json')))
    items = []
    for name in ae:
        m = re.search(r',\s*(\d{4})\)', name)
        if m:
            year = int(m.group(1))
            if 1920 <= year <= 2023:
                short = re.sub(r'\s*\([^)]+\)$', '', name)
                items.append({"n": short, "year": year, "hint": f"Baujahr {year}"})
    by_decade = defaultdict(list)
    for it in items:
        by_decade[it['year'] // 10].append(it)
    selected = [by_decade[d][0] for d in sorted(by_decade)][:20]
    tl['auto_bj'] = {
        "prompt": "Sortiere die Autos nach Baujahr (ältestes zuerst)!",
        "unit": "Jahr",
        "items": selected
    }
    w(tl_path, json.dumps(tl, ensure_ascii=False, indent=2))
    print(f"  timeline.json: auto_bj mit {len(selected)} Einträgen")
print("OK 2: timeline_auto_bj")

# ─────────────────────────────────────────────────────────────────────────
# FIX 3: generate_spieluebersicht.py Syntax-Error check
# ─────────────────────────────────────────────────────────────────────────
sp_path = os.path.join(ROOT,'generate_spieluebersicht.py')
sp = r(sp_path)
try:
    ast.parse(sp)
    print("OK 3: generate_spieluebersicht.py hat keinen Syntax-Error")
except SyntaxError as e:
    print(f"  Syntax-Error Zeile {e.lineno}: {e.msg}")
    lines = sp.splitlines()
    start = max(0, e.lineno - 3)
    for i, line in enumerate(lines[start:e.lineno+1], start+1):
        print(f"  {i}: {line}")
    # Try to fix: common issue is unterminated string
    # Show surrounding context
    idx_err = sum(len(l)+1 for l in lines[:e.lineno-1])
    print("  context:", repr(sp[idx_err-50:idx_err+100]))

# ─────────────────────────────────────────────────────────────────────────
# NEW MODES 4-7: hl_konsolen_ram, hl_konsolen_cpu, match_konsolen_generation, match_konsolen_land
# ─────────────────────────────────────────────────────────────────────────

NEW_MODES = (
    '\n    {id:"hl_konsolen_ram",'
    'icon:"\\u{1F4BE}",'
    'title:"Konsolen-Quartett: RAM",'
    'group:"games",'
    'prompt:"Welche Konsole hat mehr Arbeitsspeicher?",'
    'desc:"128 Byte bis 16 GB \\u2014 die gr\\u00f6\\u00dfte H/L-Spanne im Spiel.",'
    'prompt_en:"Which console has more RAM?"},'
    '\n    {id:"hl_konsolen_cpu",'
    'icon:"\\u{1F9E0}",'
    'title:"Konsolen-Quartett: CPU",'
    'group:"games",'
    'prompt:"Welche Konsole hat den schnelleren Prozessor?",'
    'desc:"1 MHz bis 3.800 MHz \\u2014 40 Jahre CPU-Evolution.",'
    'prompt_en:"Which console has the faster CPU?"},'
    '\n    {id:"match_konsolen_generation",'
    'icon:"\\u{1F522}",'
    'title:"Konsole: Generation",'
    'group:"games",'
    'prompt:"Welcher Konsolengeneration geh\\u00f6rt dieses Modell an?",'
    'desc:"Gen 2 (Atari) bis Gen 9 (PS5/Xbox Series X).",'
    'prompt_en:"Which console generation does this model belong to?"},'
    '\n    {id:"match_konsolen_land",'
    'icon:"\\u{1F30D}",'
    'title:"Konsole: Herkunftsland",'
    'group:"games",'
    'prompt:"Aus welchem Land stammt diese Konsole?",'
    'desc:"Japan oder USA? Die gro\\u00dfen Konsolen-Nationen.",'
    'prompt_en:"Which country does this console come from?"},'
)

# Insert after the last konsolen MODES entry (match_konsolen_handheld)
c = rpl(c,
    '},\n\n    {id:"uk_hafen_world"',
    NEW_MODES + '\n\n    {id:"uk_hafen_world"',
    "new konsolen MODES entries")

# Add to games MODE_CATS
c = rpl(c,
    '"match_konsolen_handheld","hw_baujahr_mc"',
    '"match_konsolen_handheld","hl_konsolen_ram","hl_konsolen_cpu","match_konsolen_generation","match_konsolen_land","hw_baujahr_mc"',
    "games MODE_CATS new modes")

# Dispatch entries
NEW_DISPATCH = (
    '  hl_konsolen_ram:()=>genKonsolenHL("ram_kb",{unit:"KB",'
    'prompt:_tc("Welche Konsole hat mehr Arbeitsspeicher?")}),\n'
    '  hl_konsolen_cpu:()=>genKonsolenHL("cpu_mhz",{unit:"MHz",'
    'prompt:_tc("Welche Konsole hat den schnelleren Prozessor?")}),\n'
    '  match_konsolen_generation:()=>genKonsolenMatch("generation",'
    '_tc("Welcher Konsolengeneration geh\\u00f6rt dieses Modell an?"),'
    '["1","2","3","4","5","6","7","8","9"]),\n'
    '  match_konsolen_land:()=>genKonsolenMatch("herkunftsland",'
    '_tc("Aus welchem Land stammt diese Konsole?"),'
    '["Japan","USA"]),\n'
)
c = rpl(c,
    '  match_konsolen_handheld:()=>genKonsolenHandheldQ(),\n',
    '  match_konsolen_handheld:()=>genKonsolenHandheldQ(),\n' + NEW_DISPATCH,
    "new konsolen dispatch")

# i18n EN
EN_NEW = (
    '"Welche Konsole hat mehr Arbeitsspeicher?":"Which console has more RAM?",'
    '"Welche Konsole hat den schnelleren Prozessor?":"Which console has the faster CPU?",'
    '"Welcher Konsolengeneration geh\\u00f6rt dieses Modell an?":"Which console generation does this model belong to?",'
    '"Aus welchem Land stammt diese Konsole?":"Which country does this console come from?",'
)
c = rpl(c,
    '"Welche Konsole hat mehr Einheiten verkauft?":"Which console sold more units?"',
    EN_NEW + '"Welche Konsole hat mehr Einheiten verkauft?":"Which console sold more units?"',
    "i18n EN new modes")

# i18n PL
PL_NEW = (
    '"Welche Konsole hat mehr Arbeitsspeicher?":"Która konsola ma więcej pamięci RAM?",'
    '"Welche Konsole hat den schnelleren Prozessor?":"Która konsola ma szybszy procesor?",'
    '"Welcher Konsolengeneration gehört dieses Modell an?":"Do której generacji konsol należy ten model?",'
    '"Aus welchem Land stammt diese Konsole?":"Z jakiego kraju pochodzi ta konsola?",'
)
c = rpl(c,
    '"Welche Konsole hat mehr Einheiten verkauft?":"Która konsola sprzedała się w większej liczbie egzemplarzy?"',
    PL_NEW + '"Welche Konsole hat mehr Einheiten verkauft?":"Która konsola sprzedała się w większej liczbie egzemplarzy?"',
    "i18n PL new modes")

print("OK 4-7: hl_konsolen_ram, hl_konsolen_cpu, match_konsolen_generation, match_konsolen_land")

w(os.path.join(ROOT,'gen.py'), c)
print("gen.py gespeichert")
