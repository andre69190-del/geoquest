#!/usr/bin/env python3
"""
patch_321_zug_routen.py
Phase 321 — FEATURE SPRINT: Zug-Reisezeiten (80 Strecken)

New modes:
  zug_reisezeit_mc  — "Reisezeit-Schätzer" (⏱️) — Multiple Choice: Wie lange dauert die Fahrt?
  zug_reisezeit_hl  — "Strecken-Duell"    (⚖️) — H/L: Welche Fahrt dauert länger?

Also fixes:
  - Removes duplicate "zug_uic_laender" in MODE_CATS zuege

Data: data/zug_reisezeiten.json (80 routes with von/nach/dauer_min/typ)
"""
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    with open(p, encoding='utf-8') as f: return f.read()
def save(p, s):
    with open(p, 'w', encoding='utf-8') as f: f.write(s)
    print(f'  [OK] saved {os.path.relpath(p, BASE)}')
def fix(m):  print(f'  [FIX] {m}')
def ok(m):   print(f'  [OK]  {m}')
def skip(m): print(f'  [SKIP] {m}'); sys.exit(1)

src = load(os.path.join(BASE, 'gen.py'))
patches = 0

# ─────────────────────────────────────────────────────────────────────────────
# 1. Python build: load zug_reisezeiten.json
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR_LOAD = "with open(os.path.join(os.path.dirname(__file__), 'data/zug_uic.json'), 'r', encoding='utf-8') as _f: ZUG_UIC_J = _f.read()"
NEW_LOAD = ANCHOR_LOAD + "\nwith open(os.path.join(os.path.dirname(__file__), 'data/zug_reisezeiten.json'), 'r', encoding='utf-8') as _f: ZUG_REISEZEITEN_J = _f.read()"
if ANCHOR_LOAD in src and 'zug_reisezeiten.json' not in src:
    src = src.replace(ANCHOR_LOAD, NEW_LOAD, 1)
    fix('Python: added zug_reisezeiten.json load'); patches += 1
elif 'zug_reisezeiten.json' in src:
    ok('zug_reisezeiten.json load already present')
else:
    skip('zug_uic.json load anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 2. .replace() chain
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR_REPLACE = "  .replace('PLACEHOLDER_ZUG_UIC_DATA', ZUG_UIC_J)"
NEW_REPLACE = ANCHOR_REPLACE + "\n  .replace('PLACEHOLDER_ZUG_REISEZEITEN_DATA', ZUG_REISEZEITEN_J)"
if ANCHOR_REPLACE in src and 'PLACEHOLDER_ZUG_REISEZEITEN_DATA' not in src:
    src = src.replace(ANCHOR_REPLACE, NEW_REPLACE, 1)
    fix('Python: added .replace ZUG_REISEZEITEN_DATA'); patches += 1
elif 'PLACEHOLDER_ZUG_REISEZEITEN_DATA' in src:
    ok('.replace already present')
else:
    skip('.replace ZUG_UIC anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 3. JS global const
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR_JS = 'const ZUG_UIC_DATA=PLACEHOLDER_ZUG_UIC_DATA;'
if ANCHOR_JS in src and 'ZUG_REISEZEITEN_DATA' not in src:
    src = src.replace(ANCHOR_JS, ANCHOR_JS + '\nconst ZUG_REISEZEITEN_DATA=PLACEHOLDER_ZUG_REISEZEITEN_DATA;', 1)
    fix('JS: added ZUG_REISEZEITEN_DATA const'); patches += 1
elif 'ZUG_REISEZEITEN_DATA' in src:
    ok('ZUG_REISEZEITEN_DATA already present')
else:
    skip('ZUG_UIC_DATA const anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Generator functions — insert after window._mpReveal
# ─────────────────────────────────────────────────────────────────────────────
GEN_FUNCTIONS = r"""
/* Phase 321: Zug-Reisezeiten — MC + H/L Generatoren */
function _fmtMin(m){
  var h=Math.floor(m/60),min=m%60;
  return h>0?(h+'h '+String(min).padStart(2,'0')+'m'):min+'m';
}
function genZugReisezeitMC(){
  var pool=ZUG_REISEZEITEN_DATA;
  if(!pool||pool.length<4)return null;
  var cor=pool[~~(rng()*pool.length)];
  var correct=cor.dauer_min;
  /* Plausible distractors: pick from pool with similar duration range */
  var sorted=pool.slice().sort(function(a,b){return Math.abs(a.dauer_min-correct)-Math.abs(b.dauer_min-correct);});
  var candidates=sorted.slice(1,10).filter(function(r){return Math.abs(r.dauer_min-correct)>=15;});
  var dis=[];
  var tries=0;
  while(dis.length<3&&tries<30){
    var c=candidates[~~(rng()*candidates.length)];
    if(c&&dis.indexOf(c.dauer_min)===-1&&c.dauer_min!==correct)dis.push(c.dauer_min);
    tries++;
  }
  /* Fallback: offset-based if pool too similar */
  var offsets=[30,60,90,45,75];
  var oi=0;
  while(dis.length<3&&oi<offsets.length){
    var v=correct+(rng()>0.5?offsets[oi]:-offsets[oi]);
    v=Math.max(20,v);
    if(dis.indexOf(v)===-1&&v!==correct)dis.push(v);
    oi++;
  }
  var opts=sh([correct].concat(dis)).map(function(m){return _fmtMin(m);});
  return{
    type:"uic_mc",
    prompt:_tc("Wie lange dauert die planmäßige Fahrt?"),
    subj:cor.von+" → "+cor.nach,
    meta:cor.typ,
    ans:_fmtMin(correct),
    opts:opts,
    lid:"rzmc_"+cor.von.slice(0,4)+"_"+cor.nach.slice(0,4),
    cc:""
  };
}
window.genZugReisezeitMC=genZugReisezeitMC;

function genZugReisezeitHL(){
  var pool=ZUG_REISEZEITEN_DATA;
  if(!pool||pool.length<4)return null;
  /* Pick two routes with meaningfully different durations (min 15 min apart) */
  var tries=0;var corA,corB;
  while(tries<30){
    corA=pool[~~(rng()*pool.length)];
    corB=pool[~~(rng()*pool.length)];
    if(corA!==corB&&Math.abs(corA.dauer_min-corB.dauer_min)>=15)break;
    tries++;
  }
  if(!corA||!corB)return null;
  var correct=corA.dauer_min>corB.dauer_min?0:1;
  var opts=[corA.von+"→"+corA.nach+" ("+corA.typ+")",corB.von+"→"+corB.nach+" ("+corB.typ+")"];
  return{
    type:"hl",
    prompt:_tc("Welche Zugfahrt dauert länger?"),
    subj:null,
    ans:opts[correct],
    opts:opts,
    meta:_fmtMin(corA.dauer_min)+" vs. "+_fmtMin(corB.dauer_min),
    lid:"rzhl_"+corA.von.slice(0,4)+"_"+corB.von.slice(0,4),
    cc:""
  };
}
window.genZugReisezeitHL=genZugReisezeitHL;
"""

ANCHOR_FN = 'window._mpReveal=_mpReveal;'
if ANCHOR_FN in src and 'genZugReisezeitMC' not in src:
    src = src.replace(ANCHOR_FN, ANCHOR_FN + '\n' + GEN_FUNCTIONS, 1)
    fix('JS: inserted genZugReisezeitMC() + genZugReisezeitHL()'); patches += 1
elif 'genZugReisezeitMC' in src:
    ok('Generator functions already present')
else:
    skip('window._mpReveal anchor for function insertion')

# ─────────────────────────────────────────────────────────────────────────────
# 5. MODES entries — insert before zug_uic_laender entry
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR_MODES = '    {id:"zug_uic_laender",   icon:"\\uD83D\\uDD22"'
NEW_MODES = (
    '    {id:"zug_reisezeit_mc", icon:"\\u23F1\\uFE0F",title:"Reisezeit-Sch\\u00e4tzer",       group:"zuege",'
    'prompt:"Wie lange dauert diese Zugfahrt planm\\u00e4\\u00dfig?",prompt_en:"How long does this train journey take?",'
    'desc:"Sch\\u00e4tze die Reisezeit zwischen europ\\u00e4ischen Bahnhöfen"},\n'
    '    {id:"zug_reisezeit_hl",  icon:"\\u2696\\uFE0F",title:"Strecken-Duell",                 group:"zuege",'
    'prompt:"Welche Zugfahrt dauert l\\u00e4nger?",prompt_en:"Which train journey takes longer?",'
    'desc:"Vergleiche Reisezeiten europäischer Zugstrecken"},\n'
    + ANCHOR_MODES
)
if ANCHOR_MODES in src and '"zug_reisezeit_mc"' not in src:
    src = src.replace(ANCHOR_MODES, NEW_MODES, 1)
    fix('MODES: added zug_reisezeit_mc + zug_reisezeit_hl'); patches += 1
elif '"zug_reisezeit_mc"' in src:
    ok('MODES entries already present')
else:
    skip('zug_uic_laender MODES anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 6. MODE_CATS zuege — add new modes + fix duplicate zug_uic_laender
# ─────────────────────────────────────────────────────────────────────────────
# Fix duplicate first
OLD_DUP = '"zug_ds100","zug_uic_laender","zug_ds100_input","zug_uic_laender","zug_metro_logos"'
NEW_DEDUP = '"zug_ds100","zug_uic_laender","zug_ds100_input","zug_metro_logos"'
if OLD_DUP in src:
    src = src.replace(OLD_DUP, NEW_DEDUP, 1)
    fix('MODE_CATS: removed duplicate zug_uic_laender'); patches += 1
else:
    ok('No duplicate zug_uic_laender found')

# Add new modes before zug_routen
ANCHOR_CAT = '"zug_metro_logos","zug_routen"'
NEW_CAT = '"zug_reisezeit_mc","zug_reisezeit_hl","zug_metro_logos","zug_routen"'
if ANCHOR_CAT in src and '"zug_reisezeit_mc"' not in src[src.find('zuege:{label:'):src.find('zuege:{label:')+800]:
    src = src.replace(ANCHOR_CAT, NEW_CAT, 1)
    fix('MODE_CATS zuege: added zug_reisezeit_mc + zug_reisezeit_hl'); patches += 1
else:
    ok('MODE_CATS zuege already has reisezeit modes')

# ─────────────────────────────────────────────────────────────────────────────
# 7. GEN dispatch
# ─────────────────────────────────────────────────────────────────────────────
ANCHOR_GEN = '  zug_uic_laender:()=>genUICInputQ(),'
NEW_GEN = ANCHOR_GEN + '\n  zug_reisezeit_mc:()=>genZugReisezeitMC(),\n  zug_reisezeit_hl:()=>genZugReisezeitHL(),'
if ANCHOR_GEN in src and 'zug_reisezeit_mc:()=>' not in src:
    src = src.replace(ANCHOR_GEN, NEW_GEN, 1)
    fix('GEN dispatch: added zug_reisezeit_mc + zug_reisezeit_hl'); patches += 1
elif 'zug_reisezeit_mc:()=>' in src:
    ok('GEN dispatch already has reisezeit modes')
else:
    skip('zug_uic_laender GEN dispatch anchor')

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
save(os.path.join(BASE, 'gen.py'), src)
print(f'\n  {patches} patch(es) applied.')
print('✅ patch_321_zug_routen.py done — run: python3 gen.py && python3 verify.py')
