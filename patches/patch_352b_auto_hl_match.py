#!/usr/bin/env python3
"""
Phase: 352b
Date:  2026-06-01
Author: Claude / Andre
Scope: Auto-Universum Teil B — 6 spezielle H/L + genAutosMatchExt + 8 Match-Modi

Neue H/L-Modi (6):
  hl_auto_tank        — Welches hat mehr Tankvolumen? (nur ICE, filter 0)
  hl_auto_akku        — Welche EV-Batterie ist größer? (nur EV, filter 0)
  hl_auto_reichweite  — Welches EV hat mehr Reichweite? (filter 0)
  hl_auto_verbrauch_l — Welcher Verbrenner ist sparsamer? (NIEDRIGERER gewinnt)
  hl_auto_verbrauch_e — Welches EV verbraucht weniger? (NIEDRIGERER gewinnt)
  hl_auto_zylinder    — Welches hat mehr Zylinder? (filter 0)

Neue Match-Modi (8):
  auto_match_antrieb      — Front / Heck / Allrad?
  auto_match_karosserie   — Hatchback / SUV / Kombi / …?
  auto_match_antriebsart  — Benzin / Diesel / EV / Hybrid?
  auto_match_motorbauart  — Reihe / V / Boxer / Wankel?
  auto_match_konzern      — VW / BMW / Mercedes / …?
  auto_match_getriebe     — Handschalter / Automatik / E-Getriebe?
  auto_match_turbo        — Welches dieser Autos hat einen Turbo/Kompressor?
  auto_match_sitze        — Wie viele Sitzplätze hat dieses Fahrzeug?

Dependencies: Patch 352a
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
    if r.stdout: print(r.stdout[-400:])
    if r.stderr and r.returncode != 0: print(r.stderr[-200:], file=sys.stderr)
    return r.returncode

if __name__ == "__main__":
    print("=" * 62)
    print("PATCH 352b — 6 spez. H/L + genAutosMatchExt + 8 Match-Modi")
    print("=" * 62)

    with open(GEN, encoding="utf-8") as f:
        c = f.read()

    # ── 1: JS — genAutosMatchExt Funktion ─────────────────────────────────
    OLD_GEN_FN = "/* Phase 352a: genAutosHLExt"
    NEW_GEN_FN = ("""/* Phase 352b: genAutosMatchExt — Match-Quiz aus AUTOS_EXT_DATA */
function genAutosMatchExt(field,prompt,fixedPool){
  var _AE=AUTOS_EXT_DATA;
  var valid=Object.keys(_AE).filter(function(n){
    var v=_AE[n][field];
    return v!==undefined&&v!==null&&v!==""&&v!==0&&v!==0.0;
  });
  if(valid.length<4)return null;
  var idx=~~(rng()*valid.length);
  var car=valid[idx];
  var correct=String(_AE[car][field]);
  var pool=fixedPool
    ?fixedPool.filter(function(v){return v!==correct;})
    :[...new Set(valid.map(function(n){return String(_AE[n][field]);}))].filter(function(v){return v!==correct;});
  if(pool.length<3)return null;
  var p=pool.slice();
  for(var j=p.length-1;j>0;j--){var k=~~(rng()*(j+1));var t=p[j];p[j]=p[k];p[k]=t;}
  var dis=p.slice(0,3);
  var opts=[correct].concat(dis);
  for(var j2=opts.length-1;j2>0;j2--){var k2=~~(rng()*(j2+1));var t2=opts[j2];opts[j2]=opts[k2];opts[k2]=t2;}
  var subj=car.replace(/ \\([^)]+\\)$/,""); /* Ohne (Land, Jahr) */
  return{type:"uk_match",prompt:prompt||("Welche Eigenschaft hat "+subj+"?"),
    subj:subj,ans:correct,opts:opts,lid:"amatch_"+field+"_"+idx,cc:"de"};
}
""" + OLD_GEN_FN)
    c = patch(c, OLD_GEN_FN, NEW_GEN_FN, "JS: genAutosMatchExt() eingefügt")

    # ── 2: MODES — 6 spez. H/L + 8 Match nach neupreis ───────────────────
    OLD_MODES = 'prompt_en:"Which car had a higher launch price?"},'
    NEW_MODES = (OLD_MODES + """
    {id:"hl_auto_tank",        icon:"\\u26FD",     title:"Auto-Quartett: Tank",          group:"autos",prompt:"Welches hat mehr Tankvolumen?",           desc:"Nur Verbrenner \\u2014 Tankvolumen in Litern (filter: EVs)",      prompt_en:"Which car has a larger fuel tank?"},
    {id:"hl_auto_akku",        icon:"\\u{1F50B}",  title:"Auto-Quartett: Batterie",      group:"autos",prompt:"Welche EV-Batterie ist gr\\u00f6\\u00dfer?", desc:"Nur Elektroautos \\u2014 Netto-Kapazit\\u00e4t in kWh",          prompt_en:"Which EV has a larger battery?"},
    {id:"hl_auto_reichweite",  icon:"\\u{1F30D}",  title:"Auto-Quartett: EV-Reichweite", group:"autos",prompt:"Welches EV hat mehr Reichweite?",           desc:"WLTP/NEFZ-Reichweite in km \\u2014 nur Elektroautos",           prompt_en:"Which EV has more range?"},
    {id:"hl_auto_verbrauch_l", icon:"\\u{1F6E2}\\uFE0F",title:"Auto-Quartett: Verbrauch L",  group:"autos",prompt:"Welcher Verbrenner verbraucht WENIGER?",  desc:"L/100 km \\u2014 niedrigerer Wert gewinnt",                     prompt_en:"Which combustion car consumes LESS fuel?"},
    {id:"hl_auto_verbrauch_e", icon:"\\u26A1",     title:"Auto-Quartett: Verbrauch kWh", group:"autos",prompt:"Welches EV verbraucht WENIGER Strom?",       desc:"kWh/100 km \\u2014 niedrigerer Wert gewinnt",                   prompt_en:"Which EV consumes LESS energy?"},
    {id:"hl_auto_zylinder",    icon:"\\u{1F527}",  title:"Auto-Quartett: Zylinder",      group:"autos",prompt:"Welches hat mehr Zylinder?",                desc:"Nur Verbrenner (EVs/Wankel ausgefiltert)",                      prompt_en:"Which car has more cylinders?"},
    {id:"auto_match_antrieb",     icon:"\\u{1F6E3}\\uFE0F",title:"Auto-Quiz: Antriebskonzept", group:"autos",prompt:"Welches Antriebskonzept hat dieses Fahrzeug?",   desc:"Front / Heck / Allrad",                           prompt_en:"What drivetrain does this car have?"},
    {id:"auto_match_karosserie",  icon:"\\u{1F699}",title:"Auto-Quiz: Karosserieform",    group:"autos",prompt:"Welche Karosserieform hat dieses Fahrzeug?",    desc:"Hatchback / SUV / Kombi / Coupé / …",             prompt_en:"What body style does this car have?"},
    {id:"auto_match_antriebsart", icon:"\\u{1F4A1}",title:"Auto-Quiz: Antriebsart",      group:"autos",prompt:"Womit wird dieses Fahrzeug angetrieben?",       desc:"Benzin / Diesel / EV / Hybrid / PHEV",            prompt_en:"How is this car powered?"},
    {id:"auto_match_motorbauart", icon:"\\u2699\\uFE0F",title:"Auto-Quiz: Motorbauart",   group:"autos",prompt:"Welche Motorbauart hat dieses Fahrzeug?",       desc:"Reihe / V / Boxer / Wankel / E-Motor",            prompt_en:"What engine layout does this car use?"},
    {id:"auto_match_konzern",     icon:"\\u{1F3E2}",title:"Auto-Quiz: Konzern",           group:"autos",prompt:"Zu welchem Konzern geh\\u00f6rte dieses Fahrzeug bei Produktion?", desc:"VW / BMW / Mercedes / Stellantis / Ford / …",   prompt_en:"Which group owned this car brand?"},
    {id:"auto_match_getriebe",    icon:"\\u{1F504}",title:"Auto-Quiz: Getriebe",          group:"autos",prompt:"Welches Getriebe hat dieses Fahrzeug?",         desc:"Handschalter / Automatik / E-Getriebe",           prompt_en:"What transmission does this car have?"},
    {id:"auto_match_turbo",       icon:"\\u{1F32C}\\uFE0F",title:"Auto-Quiz: Aufladung",  group:"autos",prompt:"Hat dieses Fahrzeug einen Turbo oder Kompressor ab Werk?", desc:"true = Turbo/Kompressor vorhanden",              prompt_en:"Does this car have a turbo or supercharger?"},
    {id:"auto_match_sitze",       icon:"\\u{1F4BA}",title:"Auto-Quiz: Sitzpl\\u00e4tze", group:"autos",prompt:"Wie viele Sitzpl\\u00e4tze hat dieses Fahrzeug?",  desc:"Von 2 bis 7 Sitzpl\\u00e4tze",                    prompt_en:"How many seats does this car have?"},""")
    c = patch(c, OLD_MODES, NEW_MODES, "MODES: 6 H/L + 8 Match")

    # ── 3: MODE_CATS — erweitern ───────────────────────────────────────────
    OLD_CATS = ('"hl_auto_gewicht","hl_auto_drehmoment","hl_auto_cw",'
                '"hl_auto_kofferraum","hl_auto_laenge","hl_auto_neupreis"],cost:0},')
    NEW_CATS = ('"hl_auto_gewicht","hl_auto_drehmoment","hl_auto_cw",'
                '"hl_auto_kofferraum","hl_auto_laenge","hl_auto_neupreis",'
                '"hl_auto_tank","hl_auto_akku","hl_auto_reichweite",'
                '"hl_auto_verbrauch_l","hl_auto_verbrauch_e","hl_auto_zylinder",'
                '"auto_match_antrieb","auto_match_karosserie","auto_match_antriebsart",'
                '"auto_match_motorbauart","auto_match_konzern","auto_match_getriebe",'
                '"auto_match_turbo","auto_match_sitze"],cost:0},')
    c = patch(c, OLD_CATS, NEW_CATS, "MODE_CATS: 14 neue Modi")

    # ── 4: GEN dispatch ───────────────────────────────────────────────────
    OLD_GEN = ('  hl_auto_neupreis:()=>genAutosHLExt("neupreis_eur",'
               '{unit:"EUR",prompt:"Welches war bei Einf\\u00fchrung teurer?"}),')
    NEW_GEN = (OLD_GEN + "\n"
               '  hl_auto_tank:()=>genAutosHLExt("tank",{unit:"L",'
               'prompt:"Welches hat mehr Tankvolumen?"}),\n'
               '  hl_auto_akku:()=>genAutosHLExt("akku",{unit:"kWh",'
               'prompt:"Welche EV-Batterie ist gr\\u00f6\\u00dfer?"}),\n'
               '  hl_auto_reichweite:()=>genAutosHLExt("reichweite_km",{unit:"km",'
               'prompt:"Welches EV hat mehr Reichweite?"}),\n'
               '  hl_auto_verbrauch_l:()=>genAutosHLExt("verbrauch_l",{lowerWins:true,'
               'unit:"L/100km",prompt:"Welcher Verbrenner verbraucht WENIGER?"}),\n'
               '  hl_auto_verbrauch_e:()=>genAutosHLExt("verbrauch_kwh",{lowerWins:true,'
               'unit:"kWh/100km",prompt:"Welches EV verbraucht WENIGER Strom?"}),\n'
               '  hl_auto_zylinder:()=>genAutosHLExt("zylinder",{unit:"Zyl.",'
               'prompt:"Welches hat mehr Zylinder?"}),\n'
               '  auto_match_antrieb:()=>genAutosMatchExt("antrieb",'
               '"Welches Antriebskonzept hat dieses Fahrzeug?",'
               '["Front","Heck","Allrad"]),\n'
               '  auto_match_karosserie:()=>genAutosMatchExt("karosserie",'
               '"Welche Karosserieform hat dieses Fahrzeug?",'
               '["Hatchback","Limousine","Kombi","SUV","Coupé","Cabrio","Roadster","Sportwagen"]),\n'
               '  auto_match_antriebsart:()=>genAutosMatchExt("antriebsart",'
               '"Womit wird dieses Fahrzeug angetrieben?",'
               '["Benzin","Diesel","EV","Hybrid","PHEV","MHEV"]),\n'
               '  auto_match_motorbauart:()=>genAutosMatchExt("motorbauart",'
               '"Welche Motorbauart hat dieses Fahrzeug?",'
               '["Reihe","V","Boxer","Wankel","E-Motor"]),\n'
               '  auto_match_konzern:()=>genAutosMatchExt("konzern",'
               '"Zu welchem Konzern geh\\u00f6rte dieses Fahrzeug?",'
               '["VW","BMW","Mercedes","Stellantis","Ford","Renault-Nissan",'
               '"Toyota","Hyundai-Kia","Geely","Honda","unabh\\u00e4ngig"]),\n'
               '  auto_match_getriebe:()=>genAutosMatchExt("getriebe",'
               '"Welches Getriebe hat dieses Fahrzeug?",'
               '["Handschalter","Automatik","E-Getriebe"]),\n'
               '  auto_match_turbo:()=>genAutosMatchExt("turbo",'
               '"Hat dieses Fahrzeug einen Turbo/Kompressor ab Werk?",'
               '["true","false"]),\n'
               '  auto_match_sitze:()=>genAutosMatchExt("sitze",'
               '"Wie viele Sitzpl\\u00e4tze hat dieses Fahrzeug?",null),')
    c = patch(c, OLD_GEN, NEW_GEN, "GEN dispatch: 6 H/L + 8 Match")

    with open(GEN, "w", encoding="utf-8") as f:
        f.write(c)
    print("  gen.py gespeichert")

    print("\n  Build …")
    if run([sys.executable, "gen.py"]) != 0: sys.exit(1)
    print("  Verify …")
    if run([sys.executable, "verify.py"]) != 0: sys.exit(1)
    run([sys.executable, "validate_content.py"])
    print("✅ Patch 352b OK")
