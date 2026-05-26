"""
patch_generator_consolidation.py
=================================
Replaces 16 near-identical generator functions (Tech/Gastro/Arch/Emob × 4)
with 4 factory functions + variable assignments.
Pflanzen generators are left unchanged (different return format).

Saves ~200 lines of gen.py / ~7 KB.
Zero-Bug-Policy: every replace is assert-guarded.
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ── 1. Insert 4 factory functions before genArchPinQ ─────────────────────────
FACTORIES = '''\
/* === Phase QC: Generic category-engine factories (Tech/Gastro/Arch/Emob) === */
function _mkPinQ(DATA){
  return function(cat){
    var d=DATA[cat];
    if(!d||!d.items||!d.items.length)return null;
    var idx=~~(rng()*d.items.length);
    var item=d.items[idx];
    return{type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
      prompt:d.prompt,cat:cat,itemIdx:idx};
  };
}
function _mkHL(DATA){
  return function(key){
    var d=DATA[key];
    if(!d||!d.items||d.items.length<2)return null;
    var len=d.items.length;
    var W=Math.max(1,Math.floor(len*0.1));
    var iA,iB;
    do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
    var a=d.items[iA],b=d.items[iB];
    return{type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
      unit:d.unit,prompt:d.prompt,higherWins:true};
  };
}
function _mkMatchQ(DATA){
  return function(cat){
    var d=DATA[cat];
    if(!d||!d.items||!d.items.length)return null;
    var items=d.items;
    var idx=~~(rng()*items.length);
    var correct=items[idx];
    var opts;
    if(d.fixedOpts){
      opts=d.fixedOpts.slice();
    } else {
      var pool=items.map(function(x){return x.c;}).filter(function(c){return c!==correct.c;});
      var seen=new Set();
      pool=pool.filter(function(c){if(seen.has(c))return false;seen.add(c);return true;});
      while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);
      pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);
      opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});
    }
    return{type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,
      prompt:d.prompt||"Ordne richtig zu:"};
  };
}
function _mkWS(DATA,tag){
  return function(key){
    clearInterval(tIv);_wsDetachKb();
    var entry=DATA[key];
    if(!entry||!entry.validWords){console.warn("[GeoQuest] "+tag+" WS missing:"+key);S.ph="menu";render();return;}
    var userLang=S.language||localStorage.getItem("gq_lang")||"en";
    var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
    var raw=entry.validWords[wsLang];
    var hasOwn=Array.isArray(raw)&&raw.length>0;
    var actualLang=hasOwn?wsLang:"en";
    var src2=hasOwn?raw:(entry.validWords["en"]||[]);
    var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
    if(!words.length){console.warn("[GeoQuest] "+tag+" WS no words:"+key);S.ph="menu";render();return;}
    var usingFallback=actualLang!==userLang;
    S.wsData={tierWsKey:key,city:entry.word,lang:actualLang,usingFallback:usingFallback,
      allWords:words,foundWords:[],input:"",phase:"playing",timeLeft:_WS_TIMER,shakeTs:0};
    S.gameStartTime=Date.now();S.ph="playing";
    tIv=setInterval(function(){
      if(!S.wsData||S.wsData.phase!=="playing"){clearInterval(tIv);return;}
      S.wsData.timeLeft=Math.max(0,(S.wsData.timeLeft||0)-1);
      if(S.wsData.timeLeft<=0){S.wsData.phase="timeout";clearInterval(tIv);_wsDetachKb();}
      render();
    },1000);
    _wsAttachKb();
  };
}
'''

ARCH_BLOCK_START = 'function genArchPinQ(cat){'
assert c.count(ARCH_BLOCK_START) == 1, f"Anchor not unique: {ARCH_BLOCK_START!r}"
c = c.replace(ARCH_BLOCK_START, FACTORIES + ARCH_BLOCK_START)
print("  [OK] Factory functions inserted before genArchPinQ")

# ── 2. Replace the 4 genArch* functions with variable assignments ─────────────
OLD_ARCH = '''\
function genArchPinQ(cat){
  var d=ARCH_PIN_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var idx=~~(rng()*d.items.length);
  var item=d.items[idx];
  return {type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
    prompt:d.prompt,cat:cat,itemIdx:idx};
}'''
NEW_ARCH_PIN = 'var genArchPinQ=_mkPinQ(ARCH_PIN_DATA);'
assert c.count(OLD_ARCH) == 1, f"Anchor not unique: genArchPinQ body"
c = c.replace(OLD_ARCH, NEW_ARCH_PIN)
print("  [OK] genArchPinQ → factory")

OLD_ARCH_HL = '''\
function genArchHL(dataKey){
  var d=ARCH_HL_DATA[dataKey];
  if(!d||!d.items||d.items.length<2)return null;
  var len=d.items.length;
  var W=Math.max(1,Math.floor(len*0.1));
  var iA,iB;
  do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
  var a=d.items[iA],b=d.items[iB];
  return {type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
    unit:d.unit,prompt:d.prompt,higherWins:true};
}'''
assert c.count(OLD_ARCH_HL) == 1, "Anchor not unique: genArchHL body"
c = c.replace(OLD_ARCH_HL, 'var genArchHL=_mkHL(ARCH_HL_DATA);')
print("  [OK] genArchHL → factory")

OLD_ARCH_MATCH_START = '''\
function genArchMatchQ(cat){
  var d=ARCH_MATCH_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var items=d.items;
  var idx=~~(rng()*items.length);
  var correct=items[idx];
  var opts;
  if(d.fixedOpts){
    opts=d.fixedOpts.slice();
  } else {
    var pool=items.map(function(x){return x.c;}).filter(function(c){return c!==correct.c;});
    var seen=new Set();pool=pool.filter(function(c){if(seen.has(c))return false;seen.add(c);return true;});
    while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);
    pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);
    opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});
  }
  return {type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,
    prompt:d.prompt||"Ordne richtig zu:"};
}'''
assert c.count(OLD_ARCH_MATCH_START) == 1, "Anchor not unique: genArchMatchQ body"
c = c.replace(OLD_ARCH_MATCH_START, 'var genArchMatchQ=_mkMatchQ(ARCH_MATCH_DATA);')
print("  [OK] genArchMatchQ → factory")

# initArchWS — find its exact body
OLD_ARCH_WS = '''\
function initArchWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=ARCH_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] ArchWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] ArchWS no words:"+key);S.ph="menu";render();return;}
  var usingFallback=actualLang!==userLang;
  S.wsData={tierWsKey:key,city:entry.word,lang:actualLang,usingFallback:usingFallback,
    allWords:words,foundWords:[],input:"",phase:"playing",timeLeft:_WS_TIMER,shakeTs:0};
  S.gameStartTime=Date.now();S.ph="playing";
  tIv=setInterval(function(){
    if(!S.wsData||S.wsData.phase!=="playing"){clearInterval(tIv);return;}
    S.wsData.timeLeft=Math.max(0,(S.wsData.timeLeft||0)-1);
    if(S.wsData.timeLeft<=0){S.wsData.phase="timeout";clearInterval(tIv);_wsDetachKb();}
    render();
  },1000);
  _wsAttachKb();
}'''
assert c.count(OLD_ARCH_WS) == 1, "Anchor not unique: initArchWS body"
c = c.replace(OLD_ARCH_WS, 'var initArchWS=_mkWS(ARCH_WS_DATA,"Arch");')
print("  [OK] initArchWS → factory")

# ── 3. Replace the 4 genTech* functions ──────────────────────────────────────
for fname, data_obj, tag in [
    ('genTechPinQ',   'TECH_PIN_DATA',   None),
    ('genTechHL',     'TECH_HL_DATA',    None),
    ('genTechMatchQ', 'TECH_MATCH_DATA', None),
    ('initTechWS',    'TECH_WS_DATA',    'Tech'),
]:
    if fname == 'genTechPinQ':
        old = '''\
function genTechPinQ(cat){
  var d=TECH_PIN_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var idx=~~(rng()*d.items.length);
  var item=d.items[idx];
  return {type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
    prompt:d.prompt,cat:cat,itemIdx:idx};
}'''
        new = 'var genTechPinQ=_mkPinQ(TECH_PIN_DATA);'
    elif fname == 'genTechHL':
        old = '''\
function genTechHL(dataKey){
  var d=TECH_HL_DATA[dataKey];
  if(!d||!d.items||d.items.length<2)return null;
  var len=d.items.length;
  var W=Math.max(1,Math.floor(len*0.1));
  var iA,iB;
  do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
  var a=d.items[iA],b=d.items[iB];
  return {type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
    unit:d.unit,prompt:d.prompt,higherWins:true};
}'''
        new = 'var genTechHL=_mkHL(TECH_HL_DATA);'
    elif fname == 'genTechMatchQ':
        old = '''\
function genTechMatchQ(cat){
  var d=TECH_MATCH_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var items=d.items;
  var idx=~~(rng()*items.length);
  var correct=items[idx];
  var opts;
  if(d.fixedOpts){
    opts=d.fixedOpts.slice();
  } else {
    var pool=items.map(function(x){return x.c;}).filter(function(cc){return cc!==correct.c;});
    var seen=new Set();pool=pool.filter(function(cc){if(seen.has(cc))return false;seen.add(cc);return true;});
    while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);
    pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);
    opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});
  }
  return {type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,
    prompt:d.prompt||"Ordne richtig zu:"};
}'''
        new = 'var genTechMatchQ=_mkMatchQ(TECH_MATCH_DATA);'
    else:  # initTechWS
        old = '''\
function initTechWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=TECH_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] TechWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] TechWS no words:"+key);S.ph="menu";render();return;}
  var usingFallback=actualLang!==userLang;
  S.wsData={tierWsKey:key,city:entry.word,lang:actualLang,usingFallback:usingFallback,
    allWords:words,foundWords:[],input:"",phase:"playing",timeLeft:_WS_TIMER,shakeTs:0};
  S.gameStartTime=Date.now();S.ph="playing";
  tIv=setInterval(function(){
    if(!S.wsData||S.wsData.phase!=="playing"){clearInterval(tIv);return;}
    S.wsData.timeLeft=Math.max(0,(S.wsData.timeLeft||0)-1);
    if(S.wsData.timeLeft<=0){S.wsData.phase="timeout";clearInterval(tIv);_wsDetachKb();}
    render();
  },1000);
  _wsAttachKb();
}'''
        new = 'var initTechWS=_mkWS(TECH_WS_DATA,"Tech");'
    assert c.count(old) == 1, f"Anchor not unique: {fname}"
    c = c.replace(old, new)
    print(f"  [OK] {fname} → factory")

# ── 4. Replace the 4 genEmob* functions ──────────────────────────────────────
EMOB_PAIRS = [
    ('genEmobPinQ', 'EMOB_PIN_DATA',
     '''\
function genEmobPinQ(cat){
  var d=EMOB_PIN_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var idx=~~(rng()*d.items.length);
  var item=d.items[idx];
  return {type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
    prompt:d.prompt,cat:cat,itemIdx:idx};
}''',
     'var genEmobPinQ=_mkPinQ(EMOB_PIN_DATA);'),

    ('genEmobHL', 'EMOB_HL_DATA',
     '''\
function genEmobHL(dataKey){
  var d=EMOB_HL_DATA[dataKey];
  if(!d||!d.items||d.items.length<2)return null;
  var len=d.items.length;
  var W=Math.max(1,Math.floor(len*0.1));
  var iA,iB;
  do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
  var a=d.items[iA],b=d.items[iB];
  return {type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
    unit:d.unit,prompt:d.prompt,higherWins:true};
}''',
     'var genEmobHL=_mkHL(EMOB_HL_DATA);'),

    ('genEmobMatchQ', 'EMOB_MATCH_DATA',
     '''\
function genEmobMatchQ(cat){
  var d=EMOB_MATCH_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var items=d.items;
  var idx=~~(rng()*items.length);
  var correct=items[idx];
  var opts;
  if(d.fixedOpts){
    opts=d.fixedOpts.slice();
  } else {
    var pool=items.map(function(x){return x.c;}).filter(function(cc){return cc!==correct.c;});
    var seen=new Set();pool=pool.filter(function(cc){if(seen.has(cc))return false;seen.add(cc);return true;});
    while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);
    pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);
    opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});
  }
  return {type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,
    prompt:d.prompt||"Ordne richtig zu:"};
}''',
     'var genEmobMatchQ=_mkMatchQ(EMOB_MATCH_DATA);'),
]

for fname, data_obj, old, new in EMOB_PAIRS:
    assert c.count(old) == 1, f"Anchor not unique: {fname}"
    c = c.replace(old, new)
    print(f"  [OK] {fname} → factory")

# initEmobWS
OLD_EMOB_WS = '''\
function initEmobWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=EMOB_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] EmobWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] EmobWS no words:"+key);S.ph="menu";render();return;}
  var usingFallback=actualLang!==userLang;
  S.wsData={tierWsKey:key,city:entry.word,lang:actualLang,usingFallback:usingFallback,
    allWords:words,foundWords:[],input:"",phase:"playing",timeLeft:_WS_TIMER,shakeTs:0};
  S.gameStartTime=Date.now();S.ph="playing";
  tIv=setInterval(function(){
    if(!S.wsData||S.wsData.phase!=="playing"){clearInterval(tIv);return;}
    S.wsData.timeLeft=Math.max(0,(S.wsData.timeLeft||0)-1);
    if(S.wsData.timeLeft<=0){S.wsData.phase="timeout";clearInterval(tIv);_wsDetachKb();}
    render();
  },1000);
  _wsAttachKb();
}'''
assert c.count(OLD_EMOB_WS) == 1, "Anchor not unique: initEmobWS body"
c = c.replace(OLD_EMOB_WS, 'var initEmobWS=_mkWS(EMOB_WS_DATA,"Emob");')
print("  [OK] initEmobWS → factory")

# ── 5. Replace the 4 genGastro* functions ────────────────────────────────────
GASTRO_PAIRS = [
    ('genGastroPinQ',
     '''\
function genGastroPinQ(cat){
  var d=GASTRO_PIN_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var idx=~~(rng()*d.items.length);
  var item=d.items[idx];
  return {type:"uk_pin",subj:item.n,lat:item.lat,lng:item.lng,
    prompt:d.prompt,cat:cat,itemIdx:idx};
}''',
     'var genGastroPinQ=_mkPinQ(GASTRO_PIN_DATA);'),

    ('genGastroHL',
     '''\
function genGastroHL(dataKey){
  var d=GASTRO_HL_DATA[dataKey];
  if(!d||!d.items||d.items.length<2)return null;
  var len=d.items.length;
  var W=Math.max(1,Math.floor(len*0.1));
  var iA,iB;
  do{iA=~~(rng()*len);iB=~~(rng()*len);}while(iA===iB||Math.abs(iA-iB)<W);
  var a=d.items[iA],b=d.items[iB];
  return {type:"hl",a:{name:a.name,val:a.val},b:{name:b.name,val:b.val},
    unit:d.unit,prompt:d.prompt,higherWins:true};
}''',
     'var genGastroHL=_mkHL(GASTRO_HL_DATA);'),

    ('genGastroMatchQ',
     '''\
function genGastroMatchQ(cat){
  var d=GASTRO_MATCH_DATA[cat];
  if(!d||!d.items||!d.items.length)return null;
  var items=d.items;
  var idx=~~(rng()*items.length);
  var correct=items[idx];
  var opts;
  if(d.fixedOpts){
    opts=d.fixedOpts.slice();
  } else {
    var pool=items.map(function(x){return x.c;}).filter(function(c){return c!==correct.c;});
    var seen=new Set();pool=pool.filter(function(c){if(seen.has(c))return false;seen.add(c);return true;});
    while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);
    pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);
    opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});
  }
  return {type:"uk_match",subj:correct.n,correct:correct.c,opts:opts,
    prompt:d.prompt||"Ordne richtig zu:"};
}''',
     'var genGastroMatchQ=_mkMatchQ(GASTRO_MATCH_DATA);'),
]

for fname, old, new in GASTRO_PAIRS:
    assert c.count(old) == 1, f"Anchor not unique: {fname}"
    c = c.replace(old, new)
    print(f"  [OK] {fname} → factory")

# initGastroWS
OLD_GASTRO_WS = '''\
function initGastroWS(key){
  clearInterval(tIv);_wsDetachKb();
  var entry=GASTRO_WS_DATA[key];
  if(!entry||!entry.validWords){console.warn("[GeoQuest] GastroWS missing:"+key);S.ph="menu";render();return;}
  var userLang=S.language||localStorage.getItem("gq_lang")||"en";
  var wsLang=_WS_LANGS.has(userLang)?userLang:"en";
  var raw=entry.validWords[wsLang];
  var hasOwn=Array.isArray(raw)&&raw.length>0;
  var actualLang=hasOwn?wsLang:"en";
  var src2=hasOwn?raw:(entry.validWords["en"]||[]);
  var words=src2.map(function(w){return w.toUpperCase();}).filter(function(w){return w.length>=3;});
  if(!words.length){console.warn("[GeoQuest] GastroWS no words:"+key);S.ph="menu";render();return;}
  var usingFallback=actualLang!==userLang;
  S.wsData={tierWsKey:key,city:entry.word,lang:actualLang,usingFallback:usingFallback,
    allWords:words,foundWords:[],input:"",phase:"playing",timeLeft:_WS_TIMER,shakeTs:0};
  S.gameStartTime=Date.now();S.ph="playing";
  tIv=setInterval(function(){
    if(!S.wsData||S.wsData.phase!=="playing"){clearInterval(tIv);return;}
    S.wsData.timeLeft=Math.max(0,(S.wsData.timeLeft||0)-1);
    if(S.wsData.timeLeft<=0){S.wsData.phase="timeout";clearInterval(tIv);_wsDetachKb();}
    render();
  },1000);
  _wsAttachKb();
}'''
assert c.count(OLD_GASTRO_WS) == 1, "Anchor not unique: initGastroWS body"
c = c.replace(OLD_GASTRO_WS, 'var initGastroWS=_mkWS(GASTRO_WS_DATA,"Gastro");')
print("  [OK] initGastroWS → factory")

# ── Write back ────────────────────────────────────────────────────────────────
with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("  [OK] gen.py updated — 16 duplicate functions replaced by factory assignments")
