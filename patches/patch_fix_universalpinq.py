"""
patch_fix_universalpinq.py
===========================
Bug: genUniversalPinQ expects KULTUR_DATA[cat] to be a plain array,
     but 6 tiere/pferde entries in kultur.json use {prompt, items} object format
     (added by Phase 227 enrich script). Result: !data.length → always null → game freezes.

Fix: detect both formats; prefer the stored prompt from the object when available.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

OLD = (
    'function genUniversalPinQ(cat){\n'
    '  const data=KULTUR_DATA[cat];\n'
    '  if(!data||!data.length)return null;\n'
    '  const item=data[~~(rng()*data.length)];\n'
    '  const modeObj=(typeof MODES!=="undefined"?MODES:[]).find(m=>m.id==="uk_"+cat.replace(/_/g,""))||\n'
    '    (typeof MODES!=="undefined"?MODES:[]).find(m=>m.id==="uk_"+cat)||{};\n'
    '  /* QA-Fix: tiere group — strip location hints from displayed subject to avoid spoilers */\n'
    '  const _isTiere=modeObj.group==="tiere"||modeObj.group==="pflanzen";\n'
    '  const _displaySubj=_isTiere\n'
    '    ?item.n.replace(/\\s*\\(.*?\\)/g,"").replace(/\\s*\\u2192.*$/,"").trim()\n'
    '    :item.n;\n'
    '  return{type:"uk_pin",cat,prompt:modeObj.prompt||t("q_uk_pin"),subj:_displaySubj,\n'
    '    targetLat:item.lat,targetLng:item.lng,ans:item.n,\n'
    '    lid:"ukp_"+cat+"_"+item.n.replace(/\\s+/g,"_"),cc:null};\n'
    '}'
)

NEW = (
    'function genUniversalPinQ(cat){\n'
    '  const raw=KULTUR_DATA[cat];\n'
    '  if(!raw)return null;\n'
    '  /* Support both plain array and {prompt,items} object format (Phase 227+) */\n'
    '  const data=Array.isArray(raw)?raw:(raw.items||[]);\n'
    '  const storedPrompt=Array.isArray(raw)?null:raw.prompt;\n'
    '  if(!data.length)return null;\n'
    '  const item=data[~~(rng()*data.length)];\n'
    '  const modeObj=(typeof MODES!=="undefined"?MODES:[]).find(m=>m.id==="uk_"+cat.replace(/_/g,""))||\n'
    '    (typeof MODES!=="undefined"?MODES:[]).find(m=>m.id==="uk_"+cat)||{};\n'
    '  /* QA-Fix: tiere group — strip location hints from displayed subject to avoid spoilers */\n'
    '  const _isTiere=modeObj.group==="tiere"||modeObj.group==="pflanzen";\n'
    '  const _displaySubj=_isTiere\n'
    '    ?item.n.replace(/\\s*\\(.*?\\)/g,"").replace(/\\s*\\u2192.*$/,"").trim()\n'
    '    :item.n;\n'
    '  return{type:"uk_pin",cat,prompt:storedPrompt||modeObj.prompt||t("q_uk_pin"),subj:_displaySubj,\n'
    '    targetLat:item.lat,targetLng:item.lng,ans:item.n,\n'
    '    lid:"ukp_"+cat+"_"+item.n.replace(/\\s+/g,"_"),cc:null};\n'
    '}'
)

assert c.count(OLD) == 1, f"Anchor not unique: genUniversalPinQ"
c = c.replace(OLD, NEW)
print("  [OK] genUniversalPinQ patched — now handles both array and {prompt,items} format")

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print("  [OK] gen.py updated")
