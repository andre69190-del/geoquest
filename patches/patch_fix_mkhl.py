"""
patch_fix_mkhl.py
==================
Bug: _mkHL factory returns {type:"hl", a, b, unit, prompt, higherWins:true}
     but the render engine has NO handler for type:"hl".
     Engine only handles: hl_pop, hl_river, hl_area, uk_hl, beta_hl
     Accessing q.opts.map(...) crashes because opts is undefined.

Fix: Rewrite _mkHL to:
  1. Sort items by val (numeric)
  2. Use La-Paz window pool-based selection (like genPflanzenHL)
  3. Check minimum 2% spread to avoid trivial pairings
  4. Return {type:"beta_hl", opts:[a.name,b.name], ans:higher.name, meta:..., lid:..., cc:"de"}

This matches the format expected by the render engine (verified against genPflanzenHL / genTiereHL).
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

OLD = (
    'function _mkHL(DATA){\n'
    '  return function(key){\n'
    '    var d=DATA[key];\n'
    '    if(!d||!d.items||d.items.length<2)return null;\n'
    '    var len=d.items.length;\n'
    '    var W=Math.max(1,Math.floor(len*0.1));\n'
    '    var iA,iB;\n'
    '    do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);\n'
    '    var a=d.items[iA],b=d.items[iB];\n'
    '    return{type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},\n'
    '      unit:d.unit,prompt:d.prompt,higherWins:true};\n'
    '  };\n'
    '}'
)

NEW = (
    'function _mkHL(DATA){\n'
    '  return function(key){\n'
    '    var d=DATA[key];\n'
    '    if(!d||!d.items||d.items.length<2)return null;\n'
    '    var sorted=d.items.slice().sort(function(a,b){return parseFloat(a.val)-parseFloat(b.val);});\n'
    '    var len=sorted.length;\n'
    '    var tries=0;\n'
    '    while(tries++<40){\n'
    '      var ai=~~(rng()*len);\n'
    '      var W=Math.max(1,Math.floor(len*0.1));\n'
    '      var lo=Math.max(0,ai-W),hi=Math.min(len-1,ai+W);\n'
    '      var pool=[];\n'
    '      for(var i=lo;i<=hi;i++){if(i!==ai)pool.push(i);}\n'
    '      if(!pool.length)continue;\n'
    '      var bi=pool[~~(rng()*pool.length)];\n'
    '      var a=sorted[ai],b=sorted[bi];\n'
    '      var va=parseFloat(a.val),vb=parseFloat(b.val);\n'
    '      if(va===vb)continue;\n'
    '      var span=parseFloat(sorted[len-1].val)-parseFloat(sorted[0].val);\n'
    '      if(span>0&&Math.abs(va-vb)<span*0.02)continue;\n'
    '      var higher=va>vb?a:b;\n'
    '      var unit=d.unit||"";\n'
    '      var meta=a.name+": "+a.val+(unit?" "+unit:"")+" \\u00b7 "+b.name+": "+b.val+(unit?" "+unit:"");\n'
    '      var _lid="mhl_"+key+"_"+Math.min(ai,bi)+"_"+Math.max(ai,bi);\n'
    '      return{type:"beta_hl",prompt:d.prompt||"Welches ist mehr?",subj:"",\n'
    '        opts:[a.name,b.name],ans:higher.name,meta:meta,lid:_lid,cc:"de"};\n'
    '    }\n'
    '    return null;\n'
    '  };\n'
    '}'
)

assert c.count(OLD) == 1, f"Anchor not unique: _mkHL\nFound: {c.count(OLD)}"
c = c.replace(OLD, NEW)
print("  [OK] _mkHL patched — now returns type:beta_hl with opts/ans/meta (La-Paz window)")

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print("  [OK] gen.py updated")
