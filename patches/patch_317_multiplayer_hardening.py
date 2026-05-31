#!/usr/bin/env python3
"""
patch_317_multiplayer_hardening.py
Phase 317 — MULTIPLAYER HARDENING: Edge Cases & Anti-Cheat

Fixes four Phase-316 vulnerabilities:
1. Timeout-Fallback   — 15s anti-softlock timer when waiting for opponent answer
2. S.mpRole           — persist role BEFORE S.mp=null; fix S.mp?.role→S.mpRole in NEXT_QUESTION + fTo
3. Gameover-Sync      — Host sends GAMEOVER_SYNC before entering gameover; Guest listens
4. Anti-Cheat         — defer score_update (sel/selOk) to _mpReveal(), send only score/rd/lid from answer()
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
# 1. TIMEOUT FALLBACK — 15s anti-softlock on S.mpLockAnswer
#    Inject into the MP Lock intercept in answer()
# ─────────────────────────────────────────────────────────────────────────────
OLD_LOCK = (
    '  /* Phase 316: MP Lock & Reveal — intercept before resolving */\n'
    '  if(!_bypassMpLock&&window.mpGameCh&&S.mpOpponent&&S.mpLockAnswer===undefined){\n'
    '    S.mpLockAnswer=a||"__t";\n'
    '    try{window.mpGameCh.send({type:"broadcast",event:"ANSWER_LOCKED",payload:{}});}catch(_e){}\n'
    '    if(S.mpOppLocked){_mpReveal(tok);}else{render();} /* opponent already in → reveal immediately */\n'
    '    return;\n'
    '  }'
)
NEW_LOCK = (
    '  /* Phase 316: MP Lock & Reveal — intercept before resolving */\n'
    '  if(!_bypassMpLock&&window.mpGameCh&&S.mpOpponent&&S.mpLockAnswer===undefined){\n'
    '    S.mpLockAnswer=a||"__t";\n'
    '    try{window.mpGameCh.send({type:"broadcast",event:"ANSWER_LOCKED",payload:{}});}catch(_e){}\n'
    '    /* Phase 317: 15s anti-softlock — auto-reveal if opponent disconnects */\n'
    '    if(S._mpSoftlockTo)clearTimeout(S._mpSoftlockTo);\n'
    '    S._mpSoftlockTo=setTimeout(function(){\n'
    '      if(S.mpLockAnswer!==undefined&&!S.mpOppLocked){\n'
    '        console.warn("[MP] Softlock timeout — force-revealing after 15s");\n'
    '        _mpReveal(_secretGameToken);\n'
    '      }\n'
    '    },15000);\n'
    '    if(S.mpOppLocked){clearTimeout(S._mpSoftlockTo);_mpReveal(tok);}else{render();}\n'
    '    return;\n'
    '  }'
)

if OLD_LOCK in src and 'Phase 317: 15s anti-softlock' not in src:
    src = src.replace(OLD_LOCK, NEW_LOCK, 1)
    fix('answer(): 15s anti-softlock timeout added')
    patches += 1
elif 'Phase 317: 15s anti-softlock' in src:
    ok('Anti-softlock already present')
else:
    skip('MP Lock block anchor')

# Also clear the softlock timer in _mpReveal and mpLeave
OLD_REVEAL_BODY = (
    'function _mpReveal(tok){\n'
    '  var myAns=S.mpLockAnswer;\n'
    '  S.mpLockAnswer=undefined;\n'
    '  S.mpOppLocked=false;\n'
    '  if(myAns===undefined)return;\n'
    "  answer(myAns==='__t'?null:myAns,tok,true); /* _bypassMpLock=true */\n"
    '}'
)
NEW_REVEAL_BODY = (
    'function _mpReveal(tok){\n'
    '  var myAns=S.mpLockAnswer;\n'
    '  S.mpLockAnswer=undefined;\n'
    '  S.mpOppLocked=false;\n'
    '  /* Phase 317: clear softlock timer */\n'
    '  if(S._mpSoftlockTo){clearTimeout(S._mpSoftlockTo);S._mpSoftlockTo=null;}\n'
    '  if(myAns===undefined)return;\n'
    "  answer(myAns==='__t'?null:myAns,tok,true); /* _bypassMpLock=true */\n"
    '}'
)
if OLD_REVEAL_BODY in src:
    src = src.replace(OLD_REVEAL_BODY, NEW_REVEAL_BODY, 1)
    fix('_mpReveal(): clears softlock timer')
    patches += 1
else:
    ok('_mpReveal softlock clear already present')

OLD_MPLEAVE = 'S.mp=null;S.mpModal=false;S.mpOpponent=null;S.mpSeed=null;S.mpLockAnswer=undefined;S.mpOppLocked=false;render();'
NEW_MPLEAVE = 'if(S._mpSoftlockTo){clearTimeout(S._mpSoftlockTo);S._mpSoftlockTo=null;}S.mp=null;S.mpModal=false;S.mpOpponent=null;S.mpSeed=null;S.mpRole=null;S.mpLockAnswer=undefined;S.mpOppLocked=false;render();'
if OLD_MPLEAVE in src:
    src = src.replace(OLD_MPLEAVE, NEW_MPLEAVE, 1)
    fix('mpLeave(): clears softlock timer + S.mpRole')
    patches += 1
else:
    ok('mpLeave softlock/role clear already present')

# ─────────────────────────────────────────────────────────────────────────────
# 2. S.mpRole — persist role BEFORE S.mp is set to null in mpCountdown
# ─────────────────────────────────────────────────────────────────────────────
OLD_MP_NULL = '      S.mp=null;\n      /* Sync start – same seed on both sides.'
NEW_MP_NULL = (
    '      /* Phase 317: persist role before S.mp is cleared */\n'
    '      S.mpRole=S.mp.role||"host";\n'
    '      S.mp=null;\n'
    '      /* Sync start – same seed on both sides.'
)
if OLD_MP_NULL in src and 'Phase 317: persist role' not in src:
    src = src.replace(OLD_MP_NULL, NEW_MP_NULL, 1)
    fix('mpCountdown: S.mpRole persisted before S.mp=null')
    patches += 1
elif 'Phase 317: persist role' in src:
    ok('S.mpRole persist already present')
else:
    skip('S.mp=null anchor in mpCountdown')

# Fix NEXT_QUESTION: S.mp?.role → S.mpRole
OLD_NEXT_Q_ROLE = 'if(S.mp?.role!=="host"){ /* guest: advance on host signal */'
NEW_NEXT_Q_ROLE = 'if(S.mpRole==="guest"){ /* Phase 317: use S.mpRole (S.mp is null during game) */'
if OLD_NEXT_Q_ROLE in src:
    src = src.replace(OLD_NEXT_Q_ROLE, NEW_NEXT_Q_ROLE, 1)
    fix('NEXT_QUESTION: S.mp?.role → S.mpRole')
    patches += 1
else:
    ok('NEXT_QUESTION role check already updated')

# Fix fTo _isMpGuest: S.mp?.role → S.mpRole
OLD_IS_GUEST = 'const _isMpGuest=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null&&S.mp?.role==="guest";'
NEW_IS_GUEST = 'const _isMpGuest=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null&&S.mpRole==="guest"; /* Phase 317: use S.mpRole */'
if OLD_IS_GUEST in src:
    src = src.replace(OLD_IS_GUEST, NEW_IS_GUEST, 1)
    fix('fTo _isMpGuest: S.mp?.role → S.mpRole')
    patches += 1
else:
    ok('_isMpGuest role check already updated')

# ─────────────────────────────────────────────────────────────────────────────
# 3. GAMEOVER SYNC — Host sends GAMEOVER_SYNC; Guest listens
#    a) Host: send GAMEOVER_SYNC before entering ph=gameover in fTo
#    b) Guest: handle GAMEOVER_SYNC in NEXT_QUESTION listener (extend it)
# ─────────────────────────────────────────────────────────────────────────────

# a) In fTo: when host reaches gameover (nr>=ROUNDS), send GAMEOVER_SYNC first
OLD_GAMEOVER_IN_FTO = (
    '    if(S.diff\\!=="survival"&&nr>=ROUNDS){\n'
    '      S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();updateDailyStreak();\n'
    '      if(S.isDailyRun&&\\!isDailyDone()){'
)
NEW_GAMEOVER_IN_FTO = (
    '    if(S.diff!=="survival"&&nr>=ROUNDS){\n'
    '      /* Phase 317: host sends GAMEOVER_SYNC so guest leaves waiting state */\n'
    '      if(_isMpHost){try{window.mpGameCh.send({type:"broadcast",event:"GAMEOVER_SYNC",payload:{score:S.sc,rd:nr}});}catch(_e){}}\n'
    '      S.ph="gameover";S.scoreSaved=false;S.convModal=true;soundOver();checkMastery();updateDailyStreak();\n'
    '      if(S.isDailyRun&&!isDailyDone()){'
)
if OLD_GAMEOVER_IN_FTO in src and 'Phase 317: host sends GAMEOVER_SYNC' not in src:
    src = src.replace(OLD_GAMEOVER_IN_FTO, NEW_GAMEOVER_IN_FTO, 1)
    fix('fTo: Host sends GAMEOVER_SYNC before ph=gameover')
    patches += 1
elif 'Phase 317: host sends GAMEOVER_SYNC' in src:
    ok('GAMEOVER_SYNC send already present')
else:
    skip('gameover in fTo anchor')

# b) Add GAMEOVER_SYNC listener in mpGameCh, after NEXT_QUESTION listener
OLD_NEXT_Q_LISTENER_END = (
    '          else{S.rd=nr;lq();}\n'
    '        }\n'
    '      });'
)
NEW_NEXT_Q_LISTENER_END = (
    '          else{S.rd=nr;lq();}\n'
    '        }\n'
    '      })\n'
    '      /* Phase 317: GAMEOVER_SYNC — host finished game, guest must follow */\n'
    '      .on("broadcast",{event:"GAMEOVER_SYNC"},({payload})=>{\n'
    '        if(S.mpRole==="guest"&&S.ph!=="gameover"){\n'
    '          clearTimeout(fTo);S.mpOppLocked=false;S.mpLockAnswer=undefined;\n'
    '          if(S._mpSoftlockTo){clearTimeout(S._mpSoftlockTo);S._mpSoftlockTo=null;}\n'
    '          S.mpOppFinal=payload;\n'
    '          S.ph="gameover";S.scoreSaved=false;S.convModal=true;\n'
    '          soundOver();checkMastery();render();\n'
    '        }\n'
    '      });'
)
if OLD_NEXT_Q_LISTENER_END in src and 'Phase 317: GAMEOVER_SYNC' not in src:
    src = src.replace(OLD_NEXT_Q_LISTENER_END, NEW_NEXT_Q_LISTENER_END, 1)
    fix('mpGameCh: added GAMEOVER_SYNC listener for Guest')
    patches += 1
elif 'Phase 317: GAMEOVER_SYNC' in src:
    ok('GAMEOVER_SYNC listener already present')
else:
    skip('NEXT_QUESTION listener end anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 4. ANTI-CHEAT — defer sel/selOk in score_update to reveal phase
#    In answer(): send only score/rd/correct/lid (no sel/selOk)
#    In _mpReveal(): after answer() runs, send the full score_update with sel/selOk
# ─────────────────────────────────────────────────────────────────────────────

# a) Redact sel/selOk from answer()'s score_update send
OLD_SCORE_SEND = (
    '  if(window.mpGameCh&&S.mpOpponent){\n'
    '    window.mpGameCh.send({type:"broadcast",event:"score_update",\n'
    '      payload:{score:S.sc,rd:S.rd,correct:S.correct,'
    'sel:(typeof a==="undefined"?null:a),selOk:ok,lid:(S.q&&S.q.lid)}}).then(()=>{},()=>{});\n'
    '  }'
)
NEW_SCORE_SEND = (
    '  if(window.mpGameCh&&S.mpOpponent){\n'
    '    /* Phase 317: anti-cheat — omit sel/selOk here; sent after reveal in _mpReveal() */\n'
    '    window.mpGameCh.send({type:"broadcast",event:"score_update",\n'
    '      payload:{score:S.sc,rd:S.rd,correct:S.correct,lid:(S.q&&S.q.lid)}}).then(()=>{},()=>{});\n'
    '  }'
)
if OLD_SCORE_SEND in src and 'Phase 317: anti-cheat' not in src:
    src = src.replace(OLD_SCORE_SEND, NEW_SCORE_SEND, 1)
    fix('answer(): score_update now omits sel/selOk (anti-cheat)')
    patches += 1
elif 'Phase 317: anti-cheat' in src:
    ok('score_update anti-cheat already applied')
else:
    skip('score_update send anchor in answer()')

# b) In _mpReveal(), after calling answer(), send sel/selOk
OLD_REVEAL_CALL = (
    "  answer(myAns==='__t'?null:myAns,tok,true); /* _bypassMpLock=true */\n"
    '}'
)
NEW_REVEAL_CALL = (
    "  answer(myAns==='__t'?null:myAns,tok,true); /* _bypassMpLock=true */\n"
    '  /* Phase 317: now send sel/selOk (answer resolved — safe to reveal) */\n'
    '  if(window.mpGameCh&&S.mpOpponent&&S.q){\n'
    '    var _revAns=myAns==="__t"?null:myAns;\n'
    '    var _revOk=S.ok; /* S.ok set by answer() */\n'
    '    try{window.mpGameCh.send({type:"broadcast",event:"score_update",\n'
    '      payload:{score:S.sc,rd:S.rd,correct:S.correct,sel:_revAns,selOk:_revOk,lid:(S.q&&S.q.lid)}});}catch(_e){}\n'
    '  }\n'
    '}'
)
if OLD_REVEAL_CALL in src and 'Phase 317: now send sel/selOk' not in src:
    src = src.replace(OLD_REVEAL_CALL, NEW_REVEAL_CALL, 1)
    fix('_mpReveal(): sends sel/selOk AFTER reveal (anti-cheat)')
    patches += 1
elif 'Phase 317: now send sel/selOk' in src:
    ok('_mpReveal sel/selOk send already present')
else:
    skip('_mpReveal answer() call anchor')

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
save(os.path.join(BASE, 'gen.py'), src)
print(f'\n  {patches} patch(es) applied.')
print('✅ patch_317_multiplayer_hardening.py done — run: python3 gen.py && python3 verify.py')
