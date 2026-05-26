"""
Phase 216: Procedural fake distractors for Alphabet-Sprint
- All 4 options start with the same letter
- 1 real country (correct), 3 plausibly-named fakes
"""

src = open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py','r',encoding='utf-8').read()
orig_len = len(src)

# ── Helper: _genFakeCountry ───────────────────────────────────────────────────
FAKE_GEN_FN = r'''/* Phase 216: Fake country name generator — keeps first letter, mutates body */
function _genFakeCountry(name,realNamesLC,variant){
  if(!name||name.length<3)return name+'ia';
  const first=name[0];
  const body=name.slice(1);
  const vNext={a:'o',o:'u',u:'e',e:'i',i:'a',A:'O',O:'U',U:'E',E:'I',I:'A',
               ä:'ö',ö:'ü',ü:'ä',Ä:'Ö',Ö:'Ü',Ü:'Ä'};
  const sfx=[
    ['ien','ana'],['ien','istan'],['istan','sien'],['land','lon'],['landen','lona'],
    ['ia','ien'],['ia','ona'],['ia','oa'],['a','ena'],['en','in'],['in','on'],
    ['o','ia'],['e','ia'],['el','al'],['al','ol'],['on','an'],['an','in'],
    ['esch','isch'],['isch','esch'],['urg','org'],['burg','bion'],
    ['and','ond'],['stan','sien'],['ien','ia'],['ina','ien']
  ];
  const cands=[];
  const bLow=body.toLowerCase();
  /* 1. Suffix swaps */
  for(const [fr,to] of sfx){
    if(bLow.endsWith(fr)){
      const c=first+body.slice(0,body.length-fr.length)+to;
      if(c!==name&&!realNamesLC.has(c.toLowerCase()))cands.push(c);
    }
  }
  /* 2. Vowel cycle at each position in body */
  for(let i=0;i<body.length;i++){
    if(vNext[body[i]]){
      const c=first+body.slice(0,i)+vNext[body[i]]+body.slice(i+1);
      if(c!==name&&!realNamesLC.has(c.toLowerCase()))cands.push(c);
    }
  }
  /* 3. Consonant near-swap */
  const cNear={r:'l',l:'r',n:'m',m:'n',b:'p',p:'b',d:'t',t:'d',s:'z',z:'s',
               R:'L',L:'R',N:'M',M:'N',B:'P',P:'B',D:'T',T:'D',S:'Z',Z:'S'};
  for(let i=0;i<body.length;i++){
    if(cNear[body[i]]){
      const c=first+body.slice(0,i)+cNear[body[i]]+body.slice(i+1);
      if(c!==name&&!realNamesLC.has(c.toLowerCase()))cands.push(c);
    }
  }
  if(!cands.length)return name+'ien';
  return cands[(variant||0)%cands.length];
}
'''

# ── Old genAlphaSprintQ (exact) ───────────────────────────────────────────────
OLD_FN = (
    'function genAlphaSprintQ(){\n'
    '  const letters=\'ABCDEFGHIJKLMNOPQRSTUVWXYZ\'.split(\'\');\n'
    '  const usedLetters=new Set([...S.askedLids].filter(l=>l.startsWith(\'alpha_\')).map(l=>l.slice(6)));\n'
    '  const avail=letters.filter(l=>!usedLetters.has(l));\n'
    '  if(!avail.length)return null;\n'
    '  const letter=avail[~~(rng()*avail.length)];\n'
    '  const matching=COUNTRIES.filter(c=>{const n=(displayCountry(c.cc)||c.c).toUpperCase();return n.startsWith(letter);});\n'
    '  if(!matching.length)return null;\n'
    '  const cor=matching[~~(rng()*matching.length)];\n'
    '  const corName=displayCountry(cor.cc)||cor.c;\n'
    '  const others=COUNTRIES.filter(c=>{const n=(displayCountry(c.cc)||c.c).toUpperCase();return !n.startsWith(letter);});\n'
    '  const dis=distractors(others,x=>x.ct===cor.ct,x=>false,x=>displayCountry(x.cc)||x.c);\n'
    '  return{type:"alpha_sprint",prompt:\'Land mit "\'+letter+\'" gesucht – welches?\',subj:\'\U0001f524 \'+letter,ans:corName,opts:sh([corName,...dis]),meta:cor.ct+\' \xb7 \'+cor.sr,lid:\'alpha_\'+letter,cc:cor.cc};\n'
    '}'
)

NEW_FN = (
    FAKE_GEN_FN +
    'function genAlphaSprintQ(){\n'
    '  const letters=\'ABCDEFGHIJKLMNOPQRSTUVWXYZ\'.split(\'\');\n'
    '  const usedLetters=new Set([...S.askedLids].filter(l=>l.startsWith(\'alpha_\')).map(l=>l.slice(6)));\n'
    '  const avail=letters.filter(l=>!usedLetters.has(l));\n'
    '  if(!avail.length)return null;\n'
    '  const letter=avail[~~(rng()*avail.length)];\n'
    '  const matching=COUNTRIES.filter(c=>{const n=(displayCountry(c.cc)||c.c).toUpperCase();return n.startsWith(letter);});\n'
    '  if(!matching.length)return null;\n'
    '  const cor=matching[~~(rng()*matching.length)];\n'
    '  const corName=displayCountry(cor.cc)||cor.c;\n'
    '  /* Phase 216: procedural fake distractors — all start with same letter */\n'
    '  const _sameL=sh(matching.filter(c=>c.cc!==cor.cc)).map(c=>displayCountry(c.cc)||c.c);\n'
    '  const _allLC=new Set(COUNTRIES.map(c=>(displayCountry(c.cc)||c.c).toLowerCase()));\n'
    '  const _bases=[..._sameL,...Array(3).fill(corName)].slice(0,3);\n'
    '  const _used=new Set([corName.toLowerCase()]);\n'
    '  const dis=[];\n'
    '  for(let _bi=0;_bi<_bases.length&&dis.length<3;_bi++){\n'
    '    for(let _v=0;_v<16;_v++){\n'
    '      const _fk=_genFakeCountry(_bases[_bi],_allLC,_v);\n'
    '      if(_fk&&!_used.has(_fk.toLowerCase())&&_fk[0].toUpperCase()===letter){\n'
    '        _used.add(_fk.toLowerCase());dis.push(_fk);break;\n'
    '      }\n'
    '    }\n'
    '  }\n'
    '  while(dis.length<3)dis.push(corName.slice(0,4)+(dis.length+1));\n'
    '  return{type:"alpha_sprint",prompt:\'Welches ist ein echtes Land mit "\'+letter+\'"?\',subj:\'\U0001f524 \'+letter,ans:corName,opts:sh([corName,...dis]),meta:cor.ct+\' \xb7 \'+cor.sr,lid:\'alpha_\'+letter,cc:cor.cc};\n'
    '}'
)

count = src.count(OLD_FN)
print(f"OLD_FN occurrences: {count}")
if count == 1:
    src = src.replace(OLD_FN, NEW_FN, 1)
    print("OK    [Phase 216: _genFakeCountry + new genAlphaSprintQ]")
else:
    # Debug: find where it differs
    idx = src.find('function genAlphaSprintQ')
    end = src.find('\nfunction genRcityQ', idx)
    actual = src[idx:end]
    print("ACTUAL:")
    print(repr(actual[:300]))
    print("EXPECTED:")
    print(repr(OLD_FN[:300]))

print(f"\nSize delta: {len(src)-orig_len:+d} chars")
with open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py','w',encoding='utf-8') as f:
    f.write(src)
print("Written OK")
