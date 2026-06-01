#!/usr/bin/env python3
"""
Phase: 352a
Date:  2026-06-01
Author: Claude / Andre
Scope: Auto-Universum Teil A — AUTOS_EXT_DATA + genAutosHLExt + 6 H/L-Modi

Neue Modi (6):
  hl_auto_gewicht     — Welches Fahrzeug ist schwerer? (kg)
  hl_auto_drehmoment  — Welches hat mehr Drehmoment? (Nm)
  hl_auto_cw          — Welches ist aerodynamischer? (NIEDRIGERER cw gewinnt)
  hl_auto_kofferraum  — Welches hat mehr Kofferraum? (L)
  hl_auto_laenge      — Welches ist länger? (mm)
  hl_auto_neupreis    — Welches war teurer bei Einführung? (EUR)

Architektur: INLINE-Injektion (Option A) — konsistent mit bestehender Architektur.
  AUTOS_EXT_DATA wird als PLACEHOLDER_AUTOS_EXT in gen.py eingefügt.

Dependencies: Phase 351 (autos_extended.json mit 431 Fahrzeugen)
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
    if r.stdout: print(r.stdout[-400:])
    if r.stderr and r.returncode != 0: print(r.stderr[-200:], file=sys.stderr)
    return r.returncode

if __name__ == "__main__":
    print("=" * 62)
    print("PATCH 352a — Auto-Universum: AUTOS_EXT_DATA + 6 H/L-Modi")
    print("=" * 62)

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    # ── 1: Python — autos_extended.json laden ─────────────────────────────
    OLD_PY = ("with open(os.path.join(os.path.dirname(__file__), "
              "'data/autos.json'),       'r', encoding='utf-8') "
              "as _f: AUTOS_J       = _f.read()")
    NEW_PY = (OLD_PY + "\n"
              "with open(os.path.join(os.path.dirname(__file__), "
              "'data/autos_extended.json'), 'r', encoding='utf-8') "
              "as _f: AUTOS_EXT_J  = _f.read()")
    c = patch(c, OLD_PY, NEW_PY, "Python: autos_extended.json laden")

    # ── 2: Python — PLACEHOLDER_AUTOS_EXT ersetzen registrieren ──────────
    # WICHTIG: AUTOS_EXT zuerst ersetzen (vermeidet Prefix-Kollision mit AUTOS)
    OLD_REPL = ".replace('PLACEHOLDER_AUTOS',          AUTOS_J)"
    NEW_REPL = (".replace('PLACEHOLDER_AUTOS_EXT',      AUTOS_EXT_J)\n"
                "  .replace('PLACEHOLDER_AUTOS',          AUTOS_J)")
    c = patch(c, OLD_REPL, NEW_REPL, "Python: replace PLACEHOLDER_AUTOS_EXT")

    # ── 3: JS — AUTOS_EXT_DATA Konstante ──────────────────────────────────
    OLD_CONST = "const AUTOS_DATA=PLACEHOLDER_AUTOS;"
    NEW_CONST = ("const AUTOS_DATA=PLACEHOLDER_AUTOS;\n"
                 "const AUTOS_EXT_DATA=PLACEHOLDER_AUTOS_EXT;")
    c = patch(c, OLD_CONST, NEW_CONST, "JS: const AUTOS_EXT_DATA")

    # ── 4: JS — genAutosHLExt Funktion ────────────────────────────────────
    OLD_GEN_AUTOS = "var genAutosHL=_mkHL(AUTOS_DATA);"
    NEW_GEN_AUTOS = (OLD_GEN_AUTOS + """
/* Phase 352a: genAutosHLExt — H/L aus AUTOS_EXT_DATA mit La-Paz-Fenster */
function genAutosHLExt(field,opts){
  var o=opts||{};
  var items=[];
  var _AE=AUTOS_EXT_DATA;
  var _ks=Object.keys(_AE);
  for(var _i=0;_i<_ks.length;_i++){
    var _n=_ks[_i];
    var _v=+(_AE[_n][field]);
    if(!_v||isNaN(_v)||_v<=0)continue;
    items.push({name:_n,val:_v});
  }
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
    var winner=o.lowerWins?(a.val<b.val?a:b):(a.val>b.val?a:b);
    var unit=o.unit||"";
    var meta=a.name.split(" (")[0]+": "+a.val+(unit?" "+unit:"")+" · "+b.name.split(" (")[0]+": "+b.val+(unit?" "+unit:"");
    return{type:"beta_hl",prompt:o.prompt||"Welches ist höher?",subj:"",
      opts:[a.name,b.name],ans:winner.name,meta:meta,
      lid:"ahlx_"+field+"_"+ai+"_"+bi,cc:"de"};
  }
  return null;
}""")
    c = patch(c, OLD_GEN_AUTOS, NEW_GEN_AUTOS, "JS: genAutosHLExt() eingefügt")

    # ── 5: MODES — 6 neue H/L-Einträge nach hl_auto_bj ──────────────────
    OLD_MODES = 'prompt_en:"Which car was built LATER?"},'
    NEW_MODES = (OLD_MODES + """
    {id:"hl_auto_gewicht",    icon:"\\u2696\\uFE0F",title:"Auto-Quartett: Gewicht",      group:"autos",prompt:"Welches Fahrzeug ist schwerer?",         desc:"Leergewicht in kg \\u2014 495 bis 2.300 kg",           prompt_en:"Which car is heavier?"},
    {id:"hl_auto_drehmoment", icon:"\\u{1F300}",  title:"Auto-Quartett: Drehmoment",  group:"autos",prompt:"Welches hat mehr Drehmoment?",            desc:"Max. Drehmoment in Nm",                                prompt_en:"Which car has more torque?"},
    {id:"hl_auto_cw",         icon:"\\u{1F4A8}",  title:"Auto-Quartett: Aerodynamik", group:"autos",prompt:"Welches ist aerodynamischer (cw)?",        desc:"NIEDRIGERER cw-Wert gewinnt \\u2014 weniger Luftwiderstand", prompt_en:"Which car is more aerodynamic (lower cw)?"},
    {id:"hl_auto_kofferraum", icon:"\\u{1F9F3}",  title:"Auto-Quartett: Kofferraum",  group:"autos",prompt:"Welches hat mehr Kofferraum?",             desc:"VDA-Volumen in Litern hinter den R\\u00fccksitzen",     prompt_en:"Which car has more trunk space?"},
    {id:"hl_auto_laenge",     icon:"\\u{1F4CF}",  title:"Auto-Quartett: L\\u00e4nge", group:"autos",prompt:"Welches Fahrzeug ist l\\u00e4nger?",       desc:"Fahrzeug-L\\u00e4nge in mm",                           prompt_en:"Which car is longer?"},
    {id:"hl_auto_neupreis",   icon:"\\u{1F4B0}",  title:"Auto-Quartett: Neupreis",    group:"autos",prompt:"Welches war bei Einf\\u00fchrung teurer?",  desc:"Historischer Basis-UVP in EUR (nicht inflationsbereinigt)", prompt_en:"Which car had a higher launch price?"},""")
    c = patch(c, OLD_MODES, NEW_MODES, "MODES: 6 neue H/L-Modi")

    # ── 6: MODE_CATS — autos erweitern ────────────────────────────────────
    OLD_CATS = ('autos:{label:"Auto-Quartett",icon:"\\u{1F3CE}\\uFE0F",'
                'modes:["hl_auto_ps","hl_auto_vmax","hl_auto_accel",'
                '"hl_auto_ccm","hl_auto_bj"],cost:0},')
    NEW_CATS = ('autos:{label:"Auto-Quartett",icon:"\\u{1F3CE}\\uFE0F",'
                'modes:["hl_auto_ps","hl_auto_vmax","hl_auto_accel",'
                '"hl_auto_ccm","hl_auto_bj",'
                '"hl_auto_gewicht","hl_auto_drehmoment","hl_auto_cw",'
                '"hl_auto_kofferraum","hl_auto_laenge","hl_auto_neupreis"],cost:0},')
    c = patch(c, OLD_CATS, NEW_CATS, "MODE_CATS: 6 neue Modi")

    # ── 7: GEN dispatch — 6 neue Einträge nach hl_auto_bj ────────────────
    OLD_GEN = "  hl_auto_bj:()=>genAutosHL(\"auto_bj\"),"
    NEW_GEN = (OLD_GEN + "\n"
               "  hl_auto_gewicht:()=>genAutosHLExt(\"gewicht\",{unit:\"kg\",prompt:\"Welches Fahrzeug ist schwerer?\"}),\n"
               "  hl_auto_drehmoment:()=>genAutosHLExt(\"drehmoment\",{unit:\"Nm\",prompt:\"Welches hat mehr Drehmoment?\"}),\n"
               "  hl_auto_cw:()=>genAutosHLExt(\"cw\",{lowerWins:true,prompt:\"Welches ist aerodynamischer (niedrigerer cw)?\"}),\n"
               "  hl_auto_kofferraum:()=>genAutosHLExt(\"kofferraum\",{unit:\"L\",prompt:\"Welches hat mehr Kofferraum?\"}),\n"
               "  hl_auto_laenge:()=>genAutosHLExt(\"laenge\",{unit:\"mm\",prompt:\"Welches Fahrzeug ist l\\u00e4nger?\"}),\n"
               "  hl_auto_neupreis:()=>genAutosHLExt(\"neupreis_eur\",{unit:\"EUR\",prompt:\"Welches war bei Einf\\u00fchrung teurer?\"}),")
    c = patch(c, OLD_GEN, NEW_GEN, "GEN dispatch: 6 neue H/L-Modi")

    with open(GEN, "w", encoding="utf-8") as f:
        f.write(c)
    print("  gen.py gespeichert")

    print("\n  Build …")
    if run([sys.executable, "gen.py"]) != 0: sys.exit(1)
    print("  Verify …")
    if run([sys.executable, "verify.py"]) != 0: sys.exit(1)
    run([sys.executable, "validate_content.py"])
    print("✅ Patch 352a OK")
