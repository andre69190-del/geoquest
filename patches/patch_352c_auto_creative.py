#!/usr/bin/env python3
"""
Phase: 352c
Date:  2026-06-01
Author: Claude / Andre
Scope: Auto-Universum Teil C — 5 kreative Modi + Post-Processing

Neue Modi (5):
  auto_baujahr_mc    — "Wann kam dieses Modell auf den Markt?" (4 Jahreszahlen)
  auto_match_land    — "Aus welchem Land kommt dieses Fahrzeug?" (extrahiert aus Name)
  hl_auto_ps_kg      — Leistungsgewicht PS/kg (berechnet zur Laufzeit)
  hl_auto_co2        — CO₂-Ausstoß g/km (approximiert aus verbrauch_l × 23.5)
  auto_match_dekade  — "Aus welchem Jahrzehnt stammt dieses Auto?" (50er/60er/…)

Dependencies: Patches 352a + 352b
Zero-Bug Policy: assert c.count(old)==1 vor jedem replace()
"""
import os, subprocess, sys

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
    print("PATCH 352c — Auto-Universum: 5 kreative Modi + Post-Processing")
    print("=" * 62)

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    # ── 1: JS — 5 kreative Generator-Funktionen ───────────────────────────
    OLD_FN = "/* Phase 352b: genAutosMatchExt"
    NEW_FN = ("""/* Phase 352c: Kreative Auto-Modi */

/* auto_baujahr_mc — Baujahr Multiple Choice: 4 Jahreszahlen zur Auswahl */
function genAutoBaujahrMC(){
  var _bjItems=AUTOS_DATA["auto_bj"]&&AUTOS_DATA["auto_bj"].items;
  if(!_bjItems||_bjItems.length<8)return null;
  var idx=~~(rng()*_bjItems.length);
  var car=_bjItems[idx];
  var correct=car.val;
  /* Distraktoren: andere Jahre mit Abstand 3–25 Jahre */
  var allYears=_bjItems.map(function(i){return i.val;});
  var pool=allYears.filter(function(y){
    var d=Math.abs(y-correct);
    return d>=3&&d<=25;
  });
  if(pool.length<3){
    pool=allYears.filter(function(y){return y!==correct;}).sort(function(){return rng()-0.5;});
  }
  var p=pool.slice();
  for(var j=p.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=p[j];p[j]=p[k];p[k]=t;}
  var dis=p.slice(0,3);
  var opts=[correct].concat(dis);
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}
  var subj=car.name.replace(/ \\([^)]+\\)$/,"");
  return{type:"uk_match",prompt:"In welchem Jahr kam dieses Modell auf den Markt?",
    subj:subj,ans:String(correct),opts:opts.map(String),
    lid:"abj_mc_"+idx,cc:"de"};
}

/* auto_match_land — Herkunftsland aus dem (Land, Jahr)-Suffix extrahieren */
function genAutoMatchLand(){
  var _bjItems=AUTOS_DATA["auto_bj"]&&AUTOS_DATA["auto_bj"].items;
  if(!_bjItems||_bjItems.length<8)return null;
  /* Extrahiere Land aus Name "(Land, Jahr)" */
  function getLand(name){
    var m=name.match(/\\(([^,)]+),/);
    return m?m[1].trim():null;
  }
  var valid=_bjItems.filter(function(i){return getLand(i.name)!==null;});
  if(valid.length<8)return null;
  var idx=~~(rng()*valid.length);
  var car=valid[idx];
  var correct=getLand(car.name);
  var pool=[...new Set(valid.map(function(i){return getLand(i.name);}))].filter(function(l){return l!==correct;});
  if(pool.length<3)return null;
  var p=pool.slice();
  for(var j=p.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=p[j];p[j]=p[k];p[k]=t;}
  var dis=p.slice(0,3);
  var opts=[correct].concat(dis);
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}
  var subj=car.name.replace(/ \\([^)]+\\)$/,"");
  return{type:"uk_match",prompt:"Aus welchem Land kommt dieses Fahrzeug?",
    subj:subj,ans:correct,opts:opts,lid:"aland_"+idx,cc:"de"};
}

/* hl_auto_ps_kg — Leistungsgewicht PS/kg (berechnet aus extended data) */
function genAutoPsKg(){
  var _AE=AUTOS_EXT_DATA;
  var _ps=AUTOS_DATA["auto_ps"]&&AUTOS_DATA["auto_ps"].items;
  if(!_AE||!_ps)return null;
  var psMap={};
  _ps.forEach(function(i){psMap[i.name]=i.val;});
  var items=[];
  Object.keys(_AE).forEach(function(n){
    var g=_AE[n].gewicht;
    var p=psMap[n];
    if(!g||!p||g<=0||p<=0)return;
    items.push({name:n,val:Math.round((p/g)*100)/100});
  });
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});
  var len=items.length;
  var tries=0;
  while(tries++<40){
    var ai=~~(rng()*len);
    var W=Math.max(1,Math.floor(len*(S.diff==='hardcore'?0.03:0.10)));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];
    for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}
    if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)];
    var a=items[ai],b=items[bi];
    if(a.val===b.val)continue;
    var winner=a.val>b.val?a:b;
    var meta=a.name.split(" (")[0]+": "+a.val+" PS/kg · "+b.name.split(" (")[0]+": "+b.val+" PS/kg";
    return{type:"beta_hl",prompt:"Welches Fahrzeug hat das bessere Leistungsgewicht (PS/kg)?",
      subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,
      lid:"apskq_"+ai+"_"+bi,cc:"de"};
  }
  return null;
}

/* hl_auto_co2 — CO₂-Ausstoß g/km (approximiert: verbrauch_l × 2350 / 10) */
function genAutoCO2(){
  var _AE=AUTOS_EXT_DATA;
  var items=[];
  Object.keys(_AE).forEach(function(n){
    var vl=_AE[n].verbrauch_l;
    if(!vl||vl<=0)return;
    items.push({name:n,val:Math.round(vl*23.5)});
  });
  if(items.length<4)return null;
  items.sort(function(a,b){return a.val-b.val;});
  var len=items.length;
  var tries=0;
  while(tries++<40){
    var ai=~~(rng()*len);
    var W=Math.max(1,Math.floor(len*(S.diff==='hardcore'?0.03:0.10)));
    var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);
    var pool=[];
    for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}
    if(!pool.length)continue;
    var bi=pool[~~(rng()*pool.length)];
    var a=items[ai],b=items[bi];
    if(a.val===b.val)continue;
    var span=items[len-1].val-items[0].val;
    if(span>0&&Math.abs(a.val-b.val)<span*0.02)continue;
    var winner=a.val>b.val?a:b;
    var meta=a.name.split(" (")[0]+": ~"+a.val+" g/km · "+b.name.split(" (")[0]+": ~"+b.val+" g/km";
    return{type:"beta_hl",prompt:"Welches Fahrzeug st\\u00f6\\u00dft mehr CO\\u2082 aus?",
      subj:"",opts:[a.name,b.name],ans:winner.name,meta:meta,
      lid:"aco2_"+ai+"_"+bi,cc:"de"};
  }
  return null;
}

/* auto_match_dekade — Aus welchem Jahrzehnt stammt dieses Auto? */
function genAutoMatchDekade(){
  var _bjItems=AUTOS_DATA["auto_bj"]&&AUTOS_DATA["auto_bj"].items;
  if(!_bjItems||_bjItems.length<8)return null;
  function toDekade(y){return (Math.floor(y/10)*10)+"er";}
  var idx=~~(rng()*_bjItems.length);
  var car=_bjItems[idx];
  var correct=toDekade(car.val);
  var allDekaden=[...new Set(_bjItems.map(function(i){return toDekade(i.val);}))].filter(function(d){return d!==correct;});
  if(allDekaden.length<3)return null;
  var p=allDekaden.slice();
  for(var j=p.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=p[j];p[j]=p[k];p[k]=t;}
  var opts=[correct].concat(p.slice(0,3));
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}
  var subj=car.name.replace(/ \\([^)]+\\)$/,"");
  return{type:"uk_match",prompt:"Aus welchem Jahrzehnt stammt dieses Fahrzeug?",
    subj:subj,ans:correct,opts:opts,lid:"adek_"+idx,cc:"de"};
}

""" + OLD_FN)
    c = patch(c, OLD_FN, NEW_FN, "JS: 5 kreative Funktionen")

    # ── 2: MODES — 5 kreative Modi nach auto_match_sitze ─────────────────
    OLD_MODES = 'prompt_en:"How many seats does this car have?"},'
    NEW_MODES = (OLD_MODES + """
    {id:"auto_baujahr_mc",  icon:"\\u{1F4C5}\\u2753",title:"Auto-Quiz: Baujahr-Raten",    group:"autos",prompt:"In welchem Jahr kam dieses Modell auf den Markt?",desc:"4 Jahreszahlen zur Auswahl \\u2014 welche ist richtig?",       prompt_en:"In which year did this model launch?"},
    {id:"auto_match_land",  icon:"\\u{1F30D}\\u{1F697}",title:"Auto-Quiz: Herkunftsland", group:"autos",prompt:"Aus welchem Land kommt dieses Fahrzeug?",           desc:"Extrahiert aus Fahrzeugnamen \\u2014 431 Modelle",            prompt_en:"Which country is this car from?"},
    {id:"hl_auto_ps_kg",    icon:"\\u{1F3CB}\\uFE0F",title:"Auto-Quartett: Leistungsgewicht",group:"autos",prompt:"Welches hat das bessere Leistungsgewicht (PS/kg)?",desc:"PS dividiert durch Leergewicht \\u2014 berechnet",             prompt_en:"Which car has a better power-to-weight ratio?"},
    {id:"hl_auto_co2",      icon:"\\u{1F333}\\u{1F4A8}",title:"Auto-Quartett: CO\\u2082-Aussto\\u00df",group:"autos",prompt:"Welches Fahrzeug st\\u00f6\\u00dft mehr CO\\u2082 aus?",desc:"Approximiert aus Kraftstoffverbrauch (nur Verbrenner)",  prompt_en:"Which combustion car emits more CO\\u2082?"},
    {id:"auto_match_dekade",icon:"\\u{1F5C3}\\uFE0F",title:"Auto-Quiz: Jahrzehnt",        group:"autos",prompt:"Aus welchem Jahrzehnt stammt dieses Fahrzeug?",    desc:"50er / 60er / 70er / … bis 2020er",                          prompt_en:"From which decade does this car originate?"},""")
    c = patch(c, OLD_MODES, NEW_MODES, "MODES: 5 kreative Modi")

    # ── 3: MODE_CATS — 5 kreative Modi ergänzen ───────────────────────────
    OLD_CATS = ('"auto_match_turbo","auto_match_sitze"],cost:0},')
    NEW_CATS = ('"auto_match_turbo","auto_match_sitze",'
                '"auto_baujahr_mc","auto_match_land",'
                '"hl_auto_ps_kg","hl_auto_co2","auto_match_dekade"],cost:0},')
    c = patch(c, OLD_CATS, NEW_CATS, "MODE_CATS: 5 kreative Modi")

    # ── 4: GEN dispatch ───────────────────────────────────────────────────
    OLD_GEN = ('  auto_match_sitze:()=>genAutosMatchExt("sitze",'
               '"Wie viele Sitzpl\\u00e4tze hat dieses Fahrzeug?",null),')
    NEW_GEN = (OLD_GEN + "\n"
               "  auto_baujahr_mc:()=>genAutoBaujahrMC(),\n"
               "  auto_match_land:()=>genAutoMatchLand(),\n"
               "  hl_auto_ps_kg:()=>genAutoPsKg(),\n"
               "  hl_auto_co2:()=>genAutoCO2(),\n"
               "  auto_match_dekade:()=>genAutoMatchDekade(),")
    c = patch(c, OLD_GEN, NEW_GEN, "GEN dispatch: 5 kreative Modi")

    with open(GEN, "w", encoding="utf-8") as f:
        f.write(c)
    print("  gen.py gespeichert")

    print("\n  Build …")
    if run([sys.executable, "gen.py"]) != 0: sys.exit(1)
    print("  Verify …")
    if run([sys.executable, "verify.py"]) != 0: sys.exit(1)
    run([sys.executable, "validate_content.py"])

    # Post-Phase
    r = subprocess.run([
        sys.executable, "post_phase.py",
        "--phase", "352",
        "--patch", "patches/patch_352c_auto_creative.py",
        "--summary",
        "ENGINE SPRINT 352: Auto-Universum komplett — 25 neue Modi "
        "(12 H/L + 8 Match + 5 kreativ). AUTOS_EXT_DATA (431 Fzg., 22 Felder) "
        "inline. genAutosHLExt + genAutosMatchExt + Baujahr-MC + "
        "Leistungsgewicht + CO2 + Dekaden-Quiz."
    ], cwd=ROOT, capture_output=True, text=True)
    if r.stdout: print(r.stdout[-600:])
    print("\n✅ ENGINE SPRINT 352 komplett!")
