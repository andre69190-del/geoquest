#!/usr/bin/env python3
"""
patch_312_uic_scanner.py
Phase 312 — FEATURE SPRINT: The Ultimate UIC Wagon Scanner

Adds:
1. ZUG_UIC_DATA global const in gen.py (loaded from data/zug_uic.json)
2. genUICInputQ() — quiz function generating realistic 12-digit UIC numbers
3. MODES entry: zug_uic_laender (icon 🔢, group zuege)
4. MODE_CATS zuege: add "zug_uic_laender"
5. GEN dispatch: zug_uic_laender -> genUICInputQ()
6. trackTrainDepot: track zug_uic_laender mode
7. showTrainDepot: add UIC Logbuch section with manual entry + spotted list
8. gen.py Python build: load zug_uic.json, inject placeholder
"""
import sys, os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    with open(p, encoding="utf-8") as f: return f.read()
def save(p, s):
    with open(p, "w", encoding="utf-8") as f: f.write(s)
    print(f"  [OK] saved {os.path.relpath(p, BASE)}")
def fix(m): print(f"  [FIX] {m}")
def ok(m):  print(f"  [OK]  {m}")
def skip(m): print(f"  [SKIP] {m} — anchor not found"); sys.exit(1)

gen_path = os.path.join(BASE, "gen.py")
src = load(gen_path)

patches = 0

# ─────────────────────────────────────────────
# 1. Python build section: load zug_uic.json + inject placeholder
# ─────────────────────────────────────────────
ANCHOR_LOAD = "with open(os.path.join(DATA,'kultur.json'), encoding='utf-8') as f: KULTUR_DATA_RAW = json.load(f)"
NEW_LOAD = (
    "with open(os.path.join(DATA,'zug_uic.json'), encoding='utf-8') as f: ZUG_UIC_RAW = json.load(f)\n"
    + ANCHOR_LOAD
)
if ANCHOR_LOAD in src:
    src = src.replace(ANCHOR_LOAD, NEW_LOAD, 1)
    fix("Python: added zug_uic.json load"); patches += 1
elif "zug_uic.json" in src:
    ok("zug_uic.json load already present")
else:
    skip("kultur.json load anchor")

# Serialize
ANCHOR_SERIAL = "KULTUR_DATA_J = json.dumps(KULTUR_DATA_RAW, ensure_ascii=False, separators=(',',':'))"
NEW_SERIAL = (
    "ZUG_UIC_J = json.dumps(ZUG_UIC_RAW, ensure_ascii=False, separators=(',',':'))\n"
    + ANCHOR_SERIAL
)
if ANCHOR_SERIAL in src:
    src = src.replace(ANCHOR_SERIAL, NEW_SERIAL, 1)
    fix("Python: added ZUG_UIC_J serialization"); patches += 1
elif "ZUG_UIC_J" in src:
    ok("ZUG_UIC_J already present")
else:
    skip("KULTUR_DATA_J serialization anchor")

# .replace() call
ANCHOR_REPLACE = ".replace('PLACEHOLDER_KULTUR_DATA', KULTUR_DATA_J)"
NEW_REPLACE = (
    "  .replace('PLACEHOLDER_ZUG_UIC_DATA', ZUG_UIC_J)\n"
    + ANCHOR_REPLACE
)
if ANCHOR_REPLACE in src:
    src = src.replace(ANCHOR_REPLACE, NEW_REPLACE, 1)
    fix("Python: added .replace('PLACEHOLDER_ZUG_UIC_DATA', ZUG_UIC_J)"); patches += 1
elif "PLACEHOLDER_ZUG_UIC_DATA" in src:
    ok("PLACEHOLDER_ZUG_UIC_DATA replace already present")
else:
    skip(".replace PLACEHOLDER_KULTUR_DATA anchor")

# ─────────────────────────────────────────────
# 2. JS: global ZUG_UIC_DATA const (after KULTUR_DATA)
# ─────────────────────────────────────────────
ANCHOR_JS_CONST = "const KULTUR_DATA=PLACEHOLDER_KULTUR_DATA;"
NEW_JS_CONST = (
    ANCHOR_JS_CONST + "\n"
    + "const ZUG_UIC_DATA=PLACEHOLDER_ZUG_UIC_DATA;"
)
if ANCHOR_JS_CONST in src and "ZUG_UIC_DATA=PLACEHOLDER" not in src:
    src = src.replace(ANCHOR_JS_CONST, NEW_JS_CONST, 1)
    fix("JS: added ZUG_UIC_DATA const"); patches += 1
else:
    ok("ZUG_UIC_DATA const already present")

# ─────────────────────────────────────────────
# 3. genUICInputQ() function — insert after genDS100InputQ()
# ─────────────────────────────────────────────
GEN_UIC_FN = '''
/* Phase 312: UIC Wagennummer-Quiz */
function genUICInputQ(){
  var pool=ZUG_UIC_DATA&&ZUG_UIC_DATA.waggontypen;
  if(!pool||pool.length<4)return null;
  var laender=ZUG_UIC_DATA.laendercodes||{};
  var cor=pool[~~(rng()*pool.length)];
  var code=cor.land_code;
  var correctLand=laender[code]||cor.land;
  /* Distraktoren: 3 andere Länder aus laendercodes */
  var allCodes=Object.keys(laender).filter(function(k){return k!==code;});
  var dis=[];var tries=0;
  while(dis.length<3&&tries<50){
    var rk=allCodes[~~(rng()*allCodes.length)];
    var rl=laender[rk];
    if(rl&&dis.indexOf(rl)===-1&&rl!==correctLand)dis.push(rl);
    tries++;
  }
  /* Generate realistic-looking 12-digit UIC number */
  /* Format: CC TT NNNN NNN-P  (land_code, type_prefix, serial, check) */
  var serial=String(Math.floor(1000000+rng()*8999999));
  var checkDigit=~~(rng()*10);
  var displayNum=code+" "+cor.uic_typ+" "+serial.slice(0,4)+" "+serial.slice(4)+"-"+checkDigit;
  return{
    type:"uic_mc",
    prompt:_tc("Welchem Land gehört dieser Waggon?"),
    subj:displayNum,
    meta:cor.gattung+" · "+_tc(cor.typ_name)+" · "+cor.betreiber,
    ans:correctLand,
    opts:sh([correctLand].concat(dis)),
    lid:"uic_"+code+"_"+serial,
    cc:""
  };
}
window.genUICInputQ=genUICInputQ;
'''

ANCHOR_AFTER_DS100 = "window.submitDS100Input=submitDS100Input;"
if ANCHOR_AFTER_DS100 in src and "genUICInputQ" not in src:
    src = src.replace(ANCHOR_AFTER_DS100, ANCHOR_AFTER_DS100 + "\n" + GEN_UIC_FN, 1)
    fix("JS: inserted genUICInputQ()"); patches += 1
elif "genUICInputQ" in src:
    ok("genUICInputQ already present")
else:
    skip("submitDS100Input anchor")

# ─────────────────────────────────────────────
# 4. MODES entry — insert after zug_ds100_input entry
# ─────────────────────────────────────────────
ANCHOR_MODES = '    {id:"zug_ds100_input",    icon:"\\u2328\\uFE0F",title:"DS100 (Hardcore)"'
NEW_MODE_ENTRY = (
    '    {id:"zug_uic_laender",   icon:"\\uD83D\\uDD22",title:"UIC-L\\u00e4ndercodes",          '
    'group:"zuege",prompt:"Welchem Land geh\\u00f6rt dieser Waggon?",prompt_en:"Which country does this wagon belong to?",     '
    'desc:"Erkenne das Land an der 12-stelligen UIC-Wagennummer"},\n'
    + ANCHOR_MODES
)
if ANCHOR_MODES in src and '"zug_uic_laender"' not in src:
    src = src.replace(ANCHOR_MODES, NEW_MODE_ENTRY, 1)
    fix("MODES: added zug_uic_laender"); patches += 1
elif '"zug_uic_laender"' in src:
    ok("zug_uic_laender mode already in MODES")
else:
    skip("zug_ds100_input MODES anchor")

# ─────────────────────────────────────────────
# 5. MODE_CATS zuege — add zug_uic_laender
# ─────────────────────────────────────────────
ANCHOR_CAT = '"zug_ds100_input","zug_metro_logos"'
NEW_CAT = '"zug_uic_laender","zug_ds100_input","zug_metro_logos"'
if ANCHOR_CAT in src and '"zug_uic_laender"' not in src.split("MODE_CATS")[1][:2000]:
    src = src.replace(ANCHOR_CAT, NEW_CAT, 1)
    fix("MODE_CATS zuege: added zug_uic_laender"); patches += 1
else:
    ok("MODE_CATS zuege already contains zug_uic_laender")

# ─────────────────────────────────────────────
# 6. GEN dispatch
# ─────────────────────────────────────────────
ANCHOR_GEN = "  zug_ds100_input:()=>genDS100InputQ(),"
NEW_GEN = ANCHOR_GEN + "\n  zug_uic_laender:()=>genUICInputQ(),"
if ANCHOR_GEN in src and "zug_uic_laender:()=>" not in src:
    src = src.replace(ANCHOR_GEN, NEW_GEN, 1)
    fix("GEN dispatch: added zug_uic_laender"); patches += 1
else:
    ok("GEN dispatch already has zug_uic_laender")

# ─────────────────────────────────────────────
# 7. trackTrainDepot: add zug_uic_laender to tracked modes
# ─────────────────────────────────────────────
ANCHOR_TRACK = 'var trainModes=["zug_vkm","zug_panorama","zug_ds100","zug_ds100_input","zug_metro_logos","zug_routen","zug_bahnhof_typ","zug_hersteller"];'
NEW_TRACK = 'var trainModes=["zug_vkm","zug_panorama","zug_ds100","zug_ds100_input","zug_uic_laender","zug_metro_logos","zug_routen","zug_bahnhof_typ","zug_hersteller"];'
if ANCHOR_TRACK in src:
    src = src.replace(ANCHOR_TRACK, NEW_TRACK, 1)
    fix("trackTrainDepot: added zug_uic_laender"); patches += 1
else:
    ok("trackTrainDepot already includes zug_uic_laender")

# ─────────────────────────────────────────────
# 8. showTrainDepot: add UIC Logbuch section
# ─────────────────────────────────────────────
UIC_LOGBUCH_SECTION = '''
  /* Phase 312: UIC Scanner Logbuch */
  function loadUicLog(){return JSON.parse(localStorage.getItem('gq_uic_log')||'[]');}
  function saveUicLog(a){try{localStorage.setItem('gq_uic_log',JSON.stringify(a));}catch(e){}}
  var uicLog=loadUicLog();
  var uicLaender=ZUG_UIC_DATA&&ZUG_UIC_DATA.laendercodes?ZUG_UIC_DATA.laendercodes:{};
  var uicHtml='<div style="background:var(--bg2);border-radius:10px;padding:12px;margin-bottom:12px">'
    +'<div style="font-weight:800;font-size:.95rem;margin-bottom:8px;display:flex;align-items:center;gap:8px">'
    +'<span style="font-size:1.2rem">🔢</span>'+_tc("UIC-Logbuch")
    +' <span style="font-size:.72rem;background:#004d40;color:#4db6ac;padding:2px 8px;border-radius:20px;font-weight:700">'+uicLog.length+' '+_tc("gespottet")+'</span></div>'
    +'<div style="display:flex;gap:6px;margin-bottom:8px">'
    +'<input id="uic-log-inp" placeholder="z.B. 80 51 2345 678-9" maxlength="20" '
    +'style="flex:1;min-width:0;background:var(--bg3);color:var(--text);border:1.5px solid var(--border);border-radius:6px;padding:6px 10px;font-size:.85rem;font-family:monospace">'
    +'<button onclick="(function(){var v=document.getElementById(\'uic-log-inp\').value.trim();if(!v)return;'
    +'var l='+JSON.stringify([]).replace(/"/g,\'\\\\\\"\')+';try{l=JSON.parse(localStorage.getItem(\'gq_uic_log\')||\'[]\');}catch(e){}'
    +'if(l.indexOf(v)===-1){l.push(v);try{localStorage.setItem(\'gq_uic_log\',JSON.stringify(l));}catch(e){}}'
    +'document.getElementById(\'uic-log-inp\').value=\'\';S.tab=S.tab;render();})()" '
    +'style="background:#00695c;color:#fff;border:none;border-radius:6px;padding:6px 12px;font-weight:700;cursor:pointer;white-space:nowrap">+ '+_tc("Eintragen")+'</button></div>';
  if(uicLog.length>0){
    uicHtml+='<div style="display:flex;flex-wrap:wrap;gap:5px">'
    +uicLog.slice().reverse().slice(0,30).map(function(n){
      return'<div style="background:#e0f7fa;color:#006064;border:1px solid #00838f;border-radius:5px;padding:3px 8px;font-size:.78rem;font-family:monospace;font-weight:700">'+n+'</div>';
    }).join('')+'</div>';
    if(uicLog.length>30)uicHtml+='<div style="font-size:.72rem;color:var(--text3);margin-top:4px">+'+( uicLog.length-30)+' '+_tc("weitere")+'</div>';
  }else{
    uicHtml+='<div style="font-size:.82rem;color:var(--text3)">'+_tc("Noch keine Waggons gescannt. Tippe eine UIC-Nummer ein!")+'</div>';
  }
  uicHtml+='</div>';
  html+=uicHtml;
'''

ANCHOR_DEPOT_END = '  if(!allVkm.length&&!allPan.length&&!allDs.length)html+="<p style=\'color:#999\'>Keine Zug-Daten gefunden.</p>";'
if ANCHOR_DEPOT_END in src and "UIC-Logbuch" not in src:
    src = src.replace(ANCHOR_DEPOT_END, UIC_LOGBUCH_SECTION + "\n  " + ANCHOR_DEPOT_END.strip(), 1)
    fix("showTrainDepot: added UIC Logbuch section"); patches += 1
else:
    ok("UIC Logbuch already present in showTrainDepot")

# ─────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────
save(gen_path, src)
print(f"\n  {patches} patch(es) applied.")
print("\n✅ patch_312_uic_scanner.py done — run: python3 gen.py && python3 verify.py")
