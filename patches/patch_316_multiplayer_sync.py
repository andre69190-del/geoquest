#!/usr/bin/env python3
"""
patch_316_multiplayer_sync.py
Phase 316 — MULTIPLAYER SPRINT: Synchronous Lock & Reveal

Architecture:
  answer(a, tok)
    → if MP active & not bypassed:
        store S.mpLockAnswer, send ANSWER_LOCKED (no content → anti-cheat)
        if opponent already locked → _mpReveal() immediately
        else render waiting overlay
    → _mpReveal():
        calls real answer(S.mpLockAnswer, tok, _bypassMpLock=true)
        clears lock state

  score_update handler:
    → sets S.mpOppLocked=true
    → if S.mpLockAnswer !== undefined → _mpReveal()

  ANSWER_LOCKED handler (new):
    → sets S.mpOppLocked=true
    → if S.mpLockAnswer !== undefined → _mpReveal()

  Synchronized advancement:
    → MP Host: after fTo fires, sends NEXT_QUESTION before advancing
    → MP Guest: clears own fTo, waits for NEXT_QUESTION then advances

  Overlay in render: if S.mpLockAnswer !== undefined → "Warte auf Gegner…"
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
# 1. Add _bypassMpLock parameter + Lock & Reveal intercept at top of answer()
# ─────────────────────────────────────────────────────────────────────────────
OLD_ANSWER_SIG = '  function answer(a,tok){\n  if(tok!==_secretGameToken){'
NEW_ANSWER_SIG = (
    '  function answer(a,tok,_bypassMpLock){\n'
    '  if(tok!==_secretGameToken){'
)
if OLD_ANSWER_SIG in src and '_bypassMpLock' not in src:
    src = src.replace(OLD_ANSWER_SIG, NEW_ANSWER_SIG, 1)
    fix('answer(): added _bypassMpLock parameter')
    patches += 1
elif '_bypassMpLock' in src:
    ok('_bypassMpLock already present')
else:
    skip('answer() signature anchor')

# Insert MP lock logic after the anti-cheat/guard checks, before clr()
OLD_CLR = (
    '  if(S.qRenderedAt&&Date.now()-S.qRenderedAt<250)return; /* anti-cheat: ignore clicks <250ms after render */\n'
    '  clr();'
)
MP_LOCK_BLOCK = (
    '  if(S.qRenderedAt&&Date.now()-S.qRenderedAt<250)return; /* anti-cheat: ignore clicks <250ms after render */\n'
    '  /* Phase 316: MP Lock & Reveal — intercept before resolving */\n'
    '  if(!_bypassMpLock&&window.mpGameCh&&S.mpOpponent&&S.mpLockAnswer===undefined){\n'
    '    S.mpLockAnswer=a||"__t";\n'
    '    try{window.mpGameCh.send({type:"broadcast",event:"ANSWER_LOCKED",payload:{}});}catch(_e){}\n'
    '    if(S.mpOppLocked){_mpReveal(tok);}else{render();} /* opponent already in → reveal immediately */\n'
    '    return;\n'
    '  }\n'
    '  clr();'
)
if OLD_CLR in src and 'Phase 316: MP Lock' not in src:
    src = src.replace(OLD_CLR, MP_LOCK_BLOCK, 1)
    fix('answer(): inserted MP Lock intercept')
    patches += 1
elif 'Phase 316: MP Lock' in src:
    ok('MP Lock intercept already present')
else:
    skip('clr() anchor in answer()')

# ─────────────────────────────────────────────────────────────────────────────
# 2. Add _mpReveal() function + mpOppLocked state init
#    Insert before the answer() function definition
# ─────────────────────────────────────────────────────────────────────────────
REVEAL_FN = '''
/* Phase 316: MP Reveal — called when both players have locked their answers */
function _mpReveal(tok){
  var myAns=S.mpLockAnswer;
  S.mpLockAnswer=undefined;
  S.mpOppLocked=false;
  if(myAns===undefined)return;
  answer(myAns===\'__t\'?null:myAns,tok,true); /* _bypassMpLock=true */
}
window._mpReveal=_mpReveal;
'''

ANCHOR_BEFORE_ANSWER = '  function answer(a,tok,_bypassMpLock){'
if ANCHOR_BEFORE_ANSWER in src and '_mpReveal' not in src:
    src = src.replace(ANCHOR_BEFORE_ANSWER, REVEAL_FN + '\n' + ANCHOR_BEFORE_ANSWER, 1)
    fix('_mpReveal() function inserted before answer()')
    patches += 1
elif '_mpReveal' in src:
    ok('_mpReveal() already present')
else:
    skip('answer() anchor for _mpReveal insertion')

# ─────────────────────────────────────────────────────────────────────────────
# 3. Modify score_update handler: set mpOppLocked, trigger _mpReveal if ready
# ─────────────────────────────────────────────────────────────────────────────
OLD_SCORE_UPDATE = (
    "_ch.on(\"broadcast\",{event:\"score_update\"},({payload})=>{\n"
    "        S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;"
    "if(\"lid\" in payload){S.mpOppLid=payload.lid;S.mpOppSel=payload.sel;"
    "S.mpOppSelOk=!!payload.selOk;}render();"
)
NEW_SCORE_UPDATE = (
    "_ch.on(\"broadcast\",{event:\"score_update\"},({payload})=>{\n"
    "        S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;"
    "if(\"lid\" in payload){S.mpOppLid=payload.lid;S.mpOppSel=payload.sel;"
    "S.mpOppSelOk=!!payload.selOk;}\n"
    "        /* Phase 316: opponent answered — trigger reveal if we already locked */\n"
    "        S.mpOppLocked=true;\n"
    "        if(S.mpLockAnswer!==undefined){_mpReveal(_secretGameToken);return;}\n"
    "        render();"
)
if OLD_SCORE_UPDATE in src and 'Phase 316: opponent answered' not in src:
    src = src.replace(OLD_SCORE_UPDATE, NEW_SCORE_UPDATE, 1)
    fix('score_update handler: added mpOppLocked + _mpReveal trigger')
    patches += 1
elif 'Phase 316: opponent answered' in src:
    ok('score_update handler already updated')
else:
    skip('score_update handler anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 4. Add ANSWER_LOCKED listener to mpGameCh (after score_update listener)
# ─────────────────────────────────────────────────────────────────────────────
OLD_GAME_OVER_LISTENER = (
    '.on("broadcast",{event:"game_over"},({payload})=>{\n'
    '        S.mpOppFinal=payload;\n'
    '        if(S.ph==="gameover")render();\n'
    '      });'
)
NEW_GAME_OVER_LISTENER = (
    '.on("broadcast",{event:"game_over"},({payload})=>{\n'
    '        S.mpOppFinal=payload;\n'
    '        if(S.ph==="gameover")render();\n'
    '      })\n'
    '      /* Phase 316: ANSWER_LOCKED — opponent has locked, reveal if we also locked */\n'
    '      .on("broadcast",{event:"ANSWER_LOCKED"},()=>{\n'
    '        S.mpOppLocked=true;\n'
    '        if(S.mpLockAnswer!==undefined){_mpReveal(_secretGameToken);return;}\n'
    '        render(); /* show opponent locked indicator */\n'
    '      })\n'
    '      /* Phase 316: NEXT_QUESTION — host signals advance (guest waits for this) */\n'
    '      .on("broadcast",{event:"NEXT_QUESTION"},()=>{\n'
    '        if(S.mp?.role!=="host"){ /* guest: advance on host signal */\n'
    '          clearTimeout(fTo);S.mpOppLocked=false;S.mpLockAnswer=undefined;\n'
    '          const nr=S.rd+1;\n'
    '          if(S.diff!=="survival"&&nr>=ROUNDS){S.ph="gameover";S.scoreSaved=false;'
    'S.convModal=true;soundOver();checkMastery();render();}\n'
    '          else{S.rd=nr;lq();}\n'
    '        }\n'
    '      });'
)
if OLD_GAME_OVER_LISTENER in src and 'Phase 316: ANSWER_LOCKED' not in src:
    src = src.replace(OLD_GAME_OVER_LISTENER, NEW_GAME_OVER_LISTENER, 1)
    fix('mpGameCh: added ANSWER_LOCKED + NEXT_QUESTION listeners')
    patches += 1
elif 'Phase 316: ANSWER_LOCKED' in src:
    ok('ANSWER_LOCKED listener already present')
else:
    skip('game_over listener anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 5. Synchronized advancement: Host sends NEXT_QUESTION before advancing
#    Modify fTo callback to send NEXT_QUESTION when MP host
# ─────────────────────────────────────────────────────────────────────────────
OLD_FTO = (
    'const _qt=S.q&&S.q.type||"";\n'
    '  const _fd=_qt==="iata"?2800:1900;\n'
    '  fTo=setTimeout(()=>{\n'
    '    const nr=S.rd+1;'
)
NEW_FTO = (
    'const _qt=S.q&&S.q.type||"";\n'
    '  /* Phase 316: MP sync — extended reveal delay, guest waits for NEXT_QUESTION */\n'
    '  const _isMpHost=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null;\n'
    '  const _isMpGuest=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null&&S.mp?.role==="guest";\n'
    '  const _fd=_qt==="iata"?2800:(_isMpHost||_isMpGuest)?3500:1900;\n'
    '  fTo=setTimeout(()=>{\n'
    '    if(_isMpGuest){return;} /* Phase 316: guest waits for NEXT_QUESTION from host */\n'
    '    /* Phase 316: host signals advancement to guest */\n'
    '    if(_isMpHost){try{window.mpGameCh.send({type:"broadcast",event:"NEXT_QUESTION",payload:{}});}catch(_e){}}\n'
    '    const nr=S.rd+1;'
)
if OLD_FTO in src and 'Phase 316: MP sync' not in src:
    src = src.replace(OLD_FTO, NEW_FTO, 1)
    fix('fTo: Host sends NEXT_QUESTION, Guest skips own timeout')
    patches += 1
elif 'Phase 316: MP sync' in src:
    ok('fTo sync already present')
else:
    skip('fTo setTimeout anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 6. Reset mpOppLocked + mpLockAnswer on mpLeave() and new game start
# ─────────────────────────────────────────────────────────────────────────────
OLD_MPLEAVE_RESET = 'S.mp=null;S.mpModal=false;S.mpOpponent=null;S.mpSeed=null;render();'
NEW_MPLEAVE_RESET = 'S.mp=null;S.mpModal=false;S.mpOpponent=null;S.mpSeed=null;S.mpLockAnswer=undefined;S.mpOppLocked=false;render();'
if OLD_MPLEAVE_RESET in src and 'S.mpLockAnswer=undefined;S.mpOppLocked=false' not in src:
    src = src.replace(OLD_MPLEAVE_RESET, NEW_MPLEAVE_RESET, 1)
    fix('mpLeave(): clears mpLockAnswer + mpOppLocked')
    patches += 1
else:
    ok('mpLeave reset already updated')

# ─────────────────────────────────────────────────────────────────────────────
# 7. Add "Waiting for opponent" overlay in render output (game screen)
#    Find where S.ph==="feedback" overlay is rendered and add MP waiting state
# ─────────────────────────────────────────────────────────────────────────────
# Find the in-game opponent indicator (already shows mpOppScore etc.)
WAITING_ANCHOR = 'const _scoreIndicator=S.isOffline?'
WAITING_INJECT = (
    '/* Phase 316: MP waiting overlay when answer locked but opponent not yet */\n'
    '  const _mpWaitingOverlay=(window.mpGameCh&&S.mpOpponent&&S.mpLockAnswer!==undefined&&!S.mpOppLocked)\n'
    '    ?\'<div style="position:fixed;bottom:80px;left:50%;transform:translateX(-50%);'
    'background:#1e293b;border:1.5px solid #6366f1;border-radius:12px;padding:10px 20px;'
    'font-size:.85rem;font-weight:700;color:#c4b5fd;z-index:999;display:flex;align-items:center;gap:8px;">'
    '<div style="width:10px;height:10px;border-radius:50%;background:#6366f1;animation:pulse 1s infinite"></div>'
    'Warte auf Gegner…</div>\':\'\';\n  '
    + WAITING_ANCHOR
)
if WAITING_ANCHOR in src and 'Phase 316: MP waiting overlay' not in src:
    src = src.replace(WAITING_ANCHOR, WAITING_INJECT, 1)
    fix('render(): added MP waiting overlay')
    patches += 1
elif 'Phase 316: MP waiting overlay' in src:
    ok('MP waiting overlay already present')
else:
    skip('_scoreIndicator anchor for waiting overlay')

# ─────────────────────────────────────────────────────────────────────────────
# 8. Include _mpWaitingOverlay in the rendered game screen HTML
# ─────────────────────────────────────────────────────────────────────────────
# Find where _scoreIndicator is used in the HTML template
OLD_SCORE_IN_HTML = '${_scoreIndicator}'
NEW_SCORE_IN_HTML = '${_mpWaitingOverlay}${_scoreIndicator}'
count = src.count(OLD_SCORE_IN_HTML)
if count == 1 and '${_mpWaitingOverlay}' not in src:
    src = src.replace(OLD_SCORE_IN_HTML, NEW_SCORE_IN_HTML, 1)
    fix('game screen HTML: added _mpWaitingOverlay')
    patches += 1
elif '${_mpWaitingOverlay}' in src:
    ok('_mpWaitingOverlay already in HTML')
elif count == 0:
    ok('_scoreIndicator not found in template — overlay will still show as fixed overlay')
else:
    ok(f'_scoreIndicator found {count}x — skipping to avoid double-replace')

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
save(os.path.join(BASE, 'gen.py'), src)
print(f'\n  {patches} patch(es) applied.')
print('✅ patch_316_multiplayer_sync.py done — run: python3 gen.py && python3 verify.py')
