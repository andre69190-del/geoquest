"""
patch_298_metro_logos.py
Phase 298.2 — Metro-Logos der Welt (Visuelles SVG-Quiz)
"""
import os, json, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def patch(content, old, new, label):
    if old in content:
        print(f"  [OK] {label}")
        return content.replace(old, new, 1)
    print(f"  [SKIP] {label} — Anker nicht gefunden")
    return content

print("=" * 58)
print(" Patch 298.2 — Metro-Logos der Welt")
print("=" * 58)

# =============================================================
# Validate data file exists
# =============================================================
metro_path = os.path.join(BASE, "data", "metro_logos.json")
if not os.path.isfile(metro_path):
    print("[FAIL] data/metro_logos.json fehlt! Bitte erst erstellen.")
    exit(1)
with open(metro_path, "r", encoding="utf-8") as f:
    metro_data = json.load(f)
print(f"\n[0] data/metro_logos.json: {len(metro_data)} Eintraege OK")

# =============================================================
# TEIL 1: gen.py — Python Build-Abschnitt: METRO_LOGO_DATA laden
# =============================================================
print("\n[1] gen.py — Build-Pipeline")
gen_path = os.path.join(BASE, "gen.py")
with open(gen_path, "r", encoding="utf-8") as f:
    content = f.read()

# Python-Lade-Code nach WPJ-Zuweisung einfuegen
LOAD_ANCHOR = "WPJ = json.dumps(WAPPEN_JSON, separators=(',',':'), ensure_ascii=False)"
LOAD_NEW = """WPJ = json.dumps(WAPPEN_JSON, separators=(',',':'), ensure_ascii=False)

# Phase 298.2: Metro-Logos
METRO_LOGO_JSON = json.load(open(os.path.join(os.path.dirname(__file__), 'data/metro_logos.json'), encoding='utf-8'))
METRO_LOGO_J = json.dumps(METRO_LOGO_JSON, separators=(',',':'), ensure_ascii=False)"""
content = patch(content, LOAD_ANCHOR, LOAD_NEW, "Python: metro_logos.json laden")

# JS Placeholder nach WAPPEN_DATA=PLACEHOLDER_WPJ einfuegen
JS_ANCHOR = "const WAPPEN_DATA=PLACEHOLDER_WPJ"
JS_NEW = """const WAPPEN_DATA=PLACEHOLDER_WPJ
/* Phase 298.2: Metro-Logos */
const METRO_LOGO_DATA=PLACEHOLDER_METRO_LOGO_J"""
content = patch(content, JS_ANCHOR, JS_NEW, "JS: METRO_LOGO_DATA Placeholder")

# Replace-Chain: nach WPJ einfuegen
REPLACE_ANCHOR = ".replace('PLACEHOLDER_WPJ', WPJ)"
REPLACE_NEW = """.replace('PLACEHOLDER_WPJ', WPJ)
  .replace('PLACEHOLDER_METRO_LOGO_J', METRO_LOGO_J)"""
content = patch(content, REPLACE_ANCHOR, REPLACE_NEW, "Replace-Chain: METRO_LOGO_J")

# =============================================================
# TEIL 2: genMetroLogoQ() Funktion
# =============================================================
GEN_FUNC = """
/* Phase 298.2: Metro-Logo Visuelles Quiz */
function genMetroLogoQ(){
  if(!METRO_LOGO_DATA||METRO_LOGO_DATA.length<4)return null;
  const cor=METRO_LOGO_DATA[~~(rng()*METRO_LOGO_DATA.length)];
  const others=sh(METRO_LOGO_DATA.filter(m=>m.city!==cor.city)).slice(0,3);
  if(others.length<3)return null;
  const opts=sh([cor.city,...others.map(m=>m.city)]);
  return{type:"metro_logo",prompt:"Welchem Nahverkehrsnetz gehört dieses Logo?",svg:cor.svg,subj:cor.city,opts,ans:cor.city,lid:"metro_"+cor.cc,cc:"",meta:"🚇 "+cor.city};
}

"""
GENFUNC_ANCHOR = "/* P153: Fallback when Wappen SVG fails to load */"
content = patch(content, GENFUNC_ANCHOR, GEN_FUNC + GENFUNC_ANCHOR, "genMetroLogoQ() Funktion")

# =============================================================
# TEIL 3: type:"metro_logo" Render-Branch in qBody
# =============================================================
RENDER_ANCHOR = '}else if(q.type==="wappen"){'
RENDER_NEW = """}else if(q.type==="metro_logo"){
    qBody=`<div class="qprompt">${q.prompt}</div><div style="display:flex;justify-content:center;align-items:center;margin:12px auto;max-height:25vh;max-width:200px">${q.svg}</div>${sel!==null?`<div class="qmeta">${q.meta||""}</div>`:""}`;
  }else if(q.type==="wappen"){"""
content = patch(content, RENDER_ANCHOR, RENDER_NEW, "qBody: metro_logo Render-Branch")

# =============================================================
# TEIL 4: MODES Eintrag
# =============================================================
MODES_ANCHOR = '{id:"zug_routen",'
MODES_NEW = """{id:"zug_metro_logos", icon:"\\u{1F687}",title:"Metro-Logos weltweit",  group:"zuege",prompt:"Welchem Nahverkehrsnetz gehört dieses Logo?",desc:"Underground, Métro, U-Bahn — erkennst du die Logos der Weltmetropolen?"},
    {id:"zug_routen","""
content = patch(content, MODES_ANCHOR, MODES_NEW, "MODES: zug_metro_logos Eintrag")

# =============================================================
# TEIL 5: GEN dispatch
# =============================================================
GEN_ANCHOR = "zug_routen:()=>genUniversalMatchQ(\"zug_routen\"),"
GEN_NEW = """zug_metro_logos:()=>genMetroLogoQ(),
  zug_routen:()=>genUniversalMatchQ("zug_routen"),"""
content = patch(content, GEN_ANCHOR, GEN_NEW, "GEN dispatch: zug_metro_logos")

# =============================================================
# TEIL 6: MODE_CATS zuege erweitern
# =============================================================
CATS_ANCHOR = '"zug_ds100","zug_ds100_input","zug_routen","zug_bahnhof_typ","zug_hersteller"]'
CATS_NEW = '"zug_ds100","zug_ds100_input","zug_metro_logos","zug_routen","zug_bahnhof_typ","zug_hersteller"]'
content = patch(content, CATS_ANCHOR, CATS_NEW, "MODE_CATS: zuege")

# =============================================================
# TEIL 7: trackTrainDepot — zug_metro_logos hinzufuegen
# =============================================================
TRACK_ANCHOR = 'var trainModes=["zug_vkm","zug_panorama","zug_ds100","zug_ds100_input","zug_routen","zug_bahnhof_typ","zug_hersteller"];'
TRACK_NEW = 'var trainModes=["zug_vkm","zug_panorama","zug_ds100","zug_ds100_input","zug_metro_logos","zug_routen","zug_bahnhof_typ","zug_hersteller"];'
content = patch(content, TRACK_ANCHOR, TRACK_NEW, "trackTrainDepot: zug_metro_logos")

# =============================================================
# TEIL 8: showTrainDepot — Metro-Sektion hinzufuegen
# Wir lesen city-Labels aus METRO_LOGO_DATA (nicht SVG!)
# =============================================================
DEPOT_ANCHOR = "var allRouten=(KULT.zug_routen||[]).map(function(i){return i.n||"
DEPOT_NEW = """var allMetro=(typeof METRO_LOGO_DATA!=="undefined"?METRO_LOGO_DATA:[]).map(function(i){return i.city||"";}).filter(Boolean);
  var allRouten=(KULT.zug_routen||[]).map(function(i){return i.n||"""
content = patch(content, DEPOT_ANCHOR, DEPOT_NEW, "showTrainDepot: Metro-Daten")

RENDER_DEPOT_ANCHOR = 'html+=renderSec("Legendaere Routen",allRouten);'
RENDER_DEPOT_NEW = """html+=renderSec("Metro-Logos",allMetro);
  html+=renderSec("Legendaere Routen",allRouten);"""
content = patch(content, RENDER_DEPOT_ANCHOR, RENDER_DEPOT_NEW, "showTrainDepot: Metro-Sektion rendern")

with open(gen_path, "w", encoding="utf-8") as f:
    f.write(content)

# =============================================================
# TEIL 9: verify.py — Sektion 19g
# =============================================================
print("\n[2] verify.py — Sektion 19g")
verify_path = os.path.join(BASE, "verify.py")
with open(verify_path, "r", encoding="utf-8") as f:
    vc = f.read()

VERIFY_NEW = """
# -- 19g. Metro-Logos (Phase 298.2) ----------------------------
section("19g. Metro-Logos weltweit (Phase 298.2)")
import json as _json2
_metro = _json2.load(open("data/metro_logos.json", encoding="utf-8"))
if len(_metro) >= 30:
    ok("data/metro_logos.json: " + str(len(_metro)) + " Metro-Logos OK")
else:
    fail("data/metro_logos.json: nur " + str(len(_metro)) + " Eintraege (min 30)")
_bad_svg = [m['city'] for m in _metro if not m.get('svg','').startswith('<svg')]
if not _bad_svg:
    ok("Alle Metro-Logos haben gueltigen SVG-Code")
else:
    fail("SVG-Fehler bei: " + str(_bad_svg[:3]))
if "genMetroLogoQ" in js:
    ok("genMetroLogoQ() im JS vorhanden")
else:
    fail("genMetroLogoQ() fehlt im JS")
if "zug_metro_logos" in js:
    ok("Modus zug_metro_logos im JS registriert")
else:
    fail("zug_metro_logos fehlt im JS")

"""
VERIFY_ANCHOR = "# =============================================================\nprint(\"\\n\" + \"=\" * 58)"
if "19g. Metro-Logos" not in vc:
    vc = vc.replace(VERIFY_ANCHOR, VERIFY_NEW + VERIFY_ANCHOR, 1)
    with open(verify_path, "w", encoding="utf-8") as f:
        f.write(vc)
    print("  [OK] Sektion 19g eingefuegt")
else:
    print("  [SKIP] Sektion 19g bereits vorhanden")

print("\n[DONE] Jetzt: python gen.py && python verify.py")
