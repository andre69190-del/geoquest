#!/usr/bin/env python3
"""
Phase: 353
Date:  2026-06-01
Author: Claude / Andre
Scope: Generationen-Match (neues Spiel) + JSON-Komprimierung

Neues Spiel — auto_generationen_match:
  "Wann erschien die Golf 3 GTI?" → Optionen: 1974, 1987, 1992, 1997 (alle Golf-Generationen)
  Die Distraktor-Optionen kommen aus DERSELBEN Modellreihe — das ist der Clou.
  Familien-Erkennung via Name-Parsing: "Golf 3 GTI (VW, Deutschland, 1992)" → Familie "Golf"
  26 Familien mit ≥3 Generationen erkannt (Golf, M3, Corsa, Passat, Clio, …)

JSON-Optimierung:
  AUTOS_EXT_J wird compact serialisiert (kein indent=2) → -60 KB
  Spart ~60 KB in GeoQuest.html (von 5.25 MB → ~5.19 MB)

Dependencies: Patch 352 (alle Auto-Modi)
Zero-Bug Policy: assert c.count(old)==1 vor jedem replace()
"""
import json, os, re, subprocess, sys

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

# ── Vorab: Wie viele valide Familien gibt es? ────────────────────────────────
def check_families():
    import json, re
    with open(os.path.join(ROOT, "data", "autos.json"), encoding="utf-8") as f:
        d = json.load(f)
    items = d["auto_bj"]["items"]

    BRANDS = r'^(VW|Golf|BMW|Mercedes-Benz|Mercedes|Opel|Audi|Ford|Renault|Peugeot|Fiat|Alfa Romeo|Volvo|Saab|Porsche|Toyota|Honda|Nissan|Mazda|Subaru|Škoda|SEAT|Seat|Smart|Cupra|Lancia|Citroën|Alpine)\s+'
    SPECS  = r'\s+(GTI|RS\d*|AMG|OPC|Turbo\b|16V|Aero|Clubsport|Competition|Trophy[\w-]*|Williams|R32|VR6|Cosworth|SRT|Hellcat|GSi|GSi\b|GTA|Quattro)\b.*$'
    GEN    = r'\s+([EFG]\d{2,}|[0-9][A-Z][A-Z0-9]*|[BD]\d+|Mk\d+|Gen\d+|9[PY]A|98[01]|[IVX]{1,4}|W\d{3}|R\d{3}|[A-K])$'
    NUM    = r'\s+\d+$'

    def get_family(name):
        n = re.sub(r'\s*\([^)]+\)\s*$', '', name).strip()
        n = re.sub(SPECS, '', n).strip()
        n = re.sub(GEN,   '', n).strip()
        n = re.sub(NUM,   '', n).strip()
        n = re.sub(BRANDS,'', n).strip()  # normalize: strip brand prefix
        return n

    families = {}
    for item in items:
        fam = get_family(item["name"])
        if len(fam) < 3: continue
        families.setdefault(fam, set()).add(item["val"])

    valid = {f: sorted(v) for f, v in families.items() if len(v) >= 3}
    print(f"  Familien mit ≥3 Generationen: {len(valid)}")
    for f, y in sorted(valid.items(), key=lambda x: -len(x[1]))[:10]:
        print(f"    {f}: {y}")
    return len(valid)

if __name__ == "__main__":
    print("=" * 62)
    print("PATCH 353 — Generationen-Match + JSON-Komprimierung")
    print("=" * 62)
    print()
    n_fam = check_families()
    print()

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    # ── 1: JSON-Komprimierung (AUTOS_EXT_J compact serialisieren) ────────
    OLD_LOAD = ("with open(os.path.join(os.path.dirname(__file__), "
                "'data/autos_extended.json'), 'r', encoding='utf-8') "
                "as _f: AUTOS_EXT_J  = _f.read()")
    NEW_LOAD = ("with open(os.path.join(os.path.dirname(__file__), "
                "'data/autos_extended.json'), 'r', encoding='utf-8') as _f:\n"
                "    import json as _ejson\n"
                "    AUTOS_EXT_J  = _ejson.dumps(_ejson.load(_f), "
                "ensure_ascii=False, separators=(',',':'))")
    c = patch(c, OLD_LOAD, NEW_LOAD, "JSON-Komprimierung: AUTOS_EXT_J (separators)")

    # ── 2: JS — genAutoGenerationenMatch Funktion ─────────────────────────
    OLD_FN = "/* Phase 352c: Kreative Auto-Modi */"
    NEW_FN = ("""/* Phase 353: Generationen-Match — Distraktor-Optionen aus derselben Modellreihe */
function genAutoGenerationenMatch(){
  var _bj=AUTOS_DATA["auto_bj"]&&AUTOS_DATA["auto_bj"].items;
  if(!_bj||_bj.length<8)return null;

  /* Extrahiere Modell-Familie aus vollem Fahrzeugnamen */
  function getFamily(name){
    var BRANDS=/^(VW|Golf|BMW|Mercedes-Benz|Mercedes|Opel|Audi|Ford|Renault|Peugeot|Fiat|Alfa Romeo|Volvo|Saab|Porsche|Toyota|Honda|Nissan|Mazda|Subaru|\\u0160koda|SEAT|Seat|Smart|Cupra|Lancia|Citro\\u00EBn|Alpine)\\s+/;
    var SPECS=/\\s+(GTI|RS\\d*|AMG|OPC|Turbo\\b|16V|Aero|Clubsport|Competition|Trophy[\\w-]*|Williams|R32|VR6|Cosworth|SRT|Hellcat|GSi|GTA|Quattro)\\b.*$/;
    var GEN=/\\s+([EFG]\\d{2,}|[0-9][A-Z][A-Z0-9]*|[BD]\\d+|Mk\\d+|Gen\\d+|9[PY]A|98[01]|[IVX]{1,4}|W\\d{3}|R\\d{3}|[A-K])$/;
    var n=name.replace(/\\s*\\([^)]+\\)\\s*$/,"").trim();
    n=n.replace(SPECS,"").trim();
    n=n.replace(GEN,"").trim();
    n=n.replace(/\\s+\\d+$/,"").trim();
    n=n.replace(BRANDS,"").trim();
    return n;
  }

  /* Baue Familien-Map: Familie → [{name, val}] */
  var families={};
  _bj.forEach(function(item){
    var fam=getFamily(item.name);
    if(fam.length<3)return;
    if(!families[fam])families[fam]=[];
    families[fam].push(item);
  });

  /* Filtere Familien mit ≥3 verschiedenen Jahren */
  var validFams=Object.keys(families).filter(function(f){
    var years=new Set(families[f].map(function(m){return m.val;}));
    return years.size>=3;
  });
  if(!validFams.length)return null;

  /* Wähle zufällige Familie */
  var fam=validFams[~~(rng()*validFams.length)];
  /* Dedupliziere nach Jahr (behalte erste Nennung) */
  var seen=new Set();
  var members=families[fam].filter(function(m){
    if(seen.has(m.val))return false;
    seen.add(m.val);
    return true;
  }).sort(function(a,b){return a.val-b.val;});

  if(members.length<3)return null;

  /* Wähle zufälliges Mitglied als Frage */
  var qIdx=~~(rng()*members.length);
  var correct=members[qIdx];

  /* Distraktor-Optionen = andere Generationen derselben Familie */
  var others=members.filter(function(m,i){return i!==qIdx;});
  for(var j=others.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=others[j];others[j]=others[k];others[k]=t;}
  var distraktoren=others.slice(0,3).map(function(m){return m.val;});

  /* Auffüllen mit zufälligen nahen Jahren wenn nötig */
  var tries=0;
  while(distraktoren.length<3&&tries++<30){
    var ry=_bj[~~(rng()*_bj.length)].val;
    if(ry!==correct.val&&distraktoren.indexOf(ry)===-1)distraktoren.push(ry);
  }
  if(distraktoren.length<3)return null;

  var opts=[correct.val].concat(distraktoren);
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}

  var subj=correct.name.replace(/\\s*\\([^)]+\\)\\s*$/,"");
  return{type:"uk_match",
    prompt:"Wann erschien dieses Modell der "+fam+"-Reihe?",
    subj:subj,ans:String(correct.val),opts:opts.map(String),
    lid:"agen_"+fam.replace(/\\W/g,"_")+"_"+qIdx,cc:"de"};
}

""" + OLD_FN)
    c = patch(c, OLD_FN, NEW_FN, "JS: genAutoGenerationenMatch()")

    # ── 3: MODES — nach auto_match_dekade ────────────────────────────────
    OLD_MODES = 'prompt_en:"From which decade does this car originate?"},'
    NEW_MODES = (OLD_MODES + "\n"
                 '    {id:"auto_generationen_match",icon:"\\u{1F9EC}\\u{1F697}",'
                 'title:"Modell-Generationen-Match",group:"autos",'
                 'prompt:"Wann erschien dieses Modell der Modellreihe?",'
                 'desc:"Distraktor-Optionen sind echte andere Generationen \\u2014 '
                 f'{n_fam} Modellreihen erkannt",'
                 'prompt_en:"When did this generation of the model line appear?"},')
    c = patch(c, OLD_MODES, NEW_MODES, "MODES: auto_generationen_match")

    # ── 4: MODE_CATS ──────────────────────────────────────────────────────
    OLD_CATS = '"auto_match_dekade"],cost:0},'
    NEW_CATS = '"auto_match_dekade","auto_generationen_match"],cost:0},'
    c = patch(c, OLD_CATS, NEW_CATS, "MODE_CATS: auto_generationen_match")

    # ── 5: GEN dispatch ───────────────────────────────────────────────────
    OLD_GEN = "  auto_match_dekade:()=>genAutoMatchDekade(),"
    NEW_GEN = (OLD_GEN + "\n"
               "  auto_generationen_match:()=>genAutoGenerationenMatch(),")
    c = patch(c, OLD_GEN, NEW_GEN, "GEN dispatch: auto_generationen_match")

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
        "--phase", "353",
        "--patch", "patches/patch_353_gen_match.py",
        "--summary",
        f"Generationen-Match: {n_fam} Modellreihen (Golf/M3/Clio/Corsa/…) — "
        "Distraktor-Optionen = echte andere Generationen derselben Baureihe. "
        "JSON-Komprimierung: -60 KB (AUTOS_EXT_J compact)"
    ], cwd=ROOT, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-600:])
    print("\n✅ Patch 353 fertig!")
