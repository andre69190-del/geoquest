#!/usr/bin/env python3
"""
patch_318_mp_spoiler_fix.py
Phase 318 — MULTIPLAYER BUGFIX: UI Spoiler Leak

Root cause:
  _mpReveal() sends score_update with sel/selOk to opponent.
  Opponent receives it BEFORE their own click (race condition) →
  score_update handler sets S.mpOppSel immediately → render() shows
  "⚔ Spieler wählte: Topas ✓" and green button marker to the slow player.

Fixes:
1. score_update handler: buffer sel/selOk in S._mpPendingOppSel/SelOk if
   local player hasn't answered yet (S.sel === null). Apply after reveal.
2. _mpReveal(): after answer(), flush pending opp sel into S.mpOppSel/SelOk.
3. Button _omk: guard with S.sel!==null (only show opponent marker post-reveal)
4. "wählte" text: guard with S.sel!==null
5. Reset pending buffer on mpLeave() and new game start.

Additional improvement suggestions identified during audit:
- The waiting overlay should ALSO disable the answer buttons (pointer-events:none)
  so fast-clicking after locking doesn't double-fire. Added to overlay CSS.
- score_update from _mpReveal should be sent BEFORE local render() so opponent
  sees result simultaneously. Already correct in Phase 317 order.
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
# 1. score_update handler: buffer sel/selOk if local hasn't answered yet
# ─────────────────────────────────────────────────────────────────────────────
OLD_SU_HANDLER = (
    'S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;'
    'if("lid" in payload){S.mpOppLid=payload.lid;S.mpOppSel=payload.sel;S.mpOppSelOk=!!payload.selOk;}'
)
NEW_SU_HANDLER = (
    'S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;\n'
    '        if("lid" in payload){\n'
    '          S.mpOppLid=payload.lid;\n'
    '          /* Phase 318: buffer sel/selOk — only apply after local player has answered */\n'
    '          if(S.sel!==null){\n'
    '            S.mpOppSel=payload.sel;S.mpOppSelOk=!!payload.selOk;\n'
    '          }else if(payload.sel!==undefined){\n'
    '            /* Opponent answered before us — store in buffer, apply at reveal */\n'
    '            S._mpPendingOppSel=payload.sel;S._mpPendingOppSelOk=!!payload.selOk;\n'
    '          }\n'
    '        }'
)
if OLD_SU_HANDLER in src and 'Phase 318: buffer sel/selOk' not in src:
    src = src.replace(OLD_SU_HANDLER, NEW_SU_HANDLER, 1)
    fix('score_update: buffer sel/selOk until local answer'); patches += 1
elif 'Phase 318: buffer sel/selOk' in src:
    ok('score_update buffer already present')
else:
    skip('score_update handler anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 2. _mpReveal(): flush pending sel/selOk after answer()
# ─────────────────────────────────────────────────────────────────────────────
OLD_REVEAL_END = (
    "  answer(myAns==='__t'?null:myAns,tok,true); /* _bypassMpLock=true */\n"
    '  /* Phase 317: send sel/selOk AFTER reveal (anti-cheat — opponent gets answer only post-reveal) */'
)
NEW_REVEAL_END = (
    "  answer(myAns==='__t'?null:myAns,tok,true); /* _bypassMpLock=true */\n"
    '  /* Phase 318: flush buffered opponent sel/selOk now that we have answered */\n'
    '  if(S._mpPendingOppSel!==undefined){\n'
    '    S.mpOppSel=S._mpPendingOppSel;S.mpOppSelOk=!!S._mpPendingOppSelOk;\n'
    '    S._mpPendingOppSel=undefined;S._mpPendingOppSelOk=undefined;\n'
    '  }\n'
    '  /* Phase 317: send sel/selOk AFTER reveal (anti-cheat — opponent gets answer only post-reveal) */'
)
if OLD_REVEAL_END in src and 'Phase 318: flush buffered' not in src:
    src = src.replace(OLD_REVEAL_END, NEW_REVEAL_END, 1)
    fix('_mpReveal(): flushes pending sel/selOk after answer()'); patches += 1
elif 'Phase 318: flush buffered' in src:
    ok('_mpReveal flush already present')
else:
    skip('_mpReveal Phase-317 comment anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 3. Button _omk: guard with S.sel!==null
# ─────────────────────────────────────────────────────────────────────────────
OLD_OMK = 'const _omk=(S.mpOpponent&&S.mpOppLid===q.lid&&S.mpOppSel!=null&&o===S.mpOppSel)?'
NEW_OMK = '/* Phase 318: show opp marker only AFTER local has answered */\nconst _omk=(S.mpOpponent&&S.sel!==null&&S.mpOppLid===q.lid&&S.mpOppSel!=null&&o===S.mpOppSel)?'
if OLD_OMK in src and 'Phase 318: show opp marker' not in src:
    src = src.replace(OLD_OMK, NEW_OMK, 1)
    fix('_omk button marker: guarded with S.sel!==null'); patches += 1
elif 'Phase 318: show opp marker' in src:
    ok('_omk guard already present')
else:
    skip('_omk anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 4. "wählte" text: guard with S.sel!==null
# ─────────────────────────────────────────────────────────────────────────────
OLD_WAHLTE = '(S.mpOpponent&&S.mpOppLid===q.lid&&typeof S.mpOppSel!=="undefined")?`<div style="text-align:center;font-size:.72rem;font-weight:800;margin:1px 0 5px;'
NEW_WAHLTE = '/* Phase 318: never show opponent answer before local has answered */\n    (S.mpOpponent&&S.sel!==null&&S.mpOppLid===q.lid&&typeof S.mpOppSel!=="undefined")?`<div style="text-align:center;font-size:.72rem;font-weight:800;margin:1px 0 5px;'
if OLD_WAHLTE in src and 'Phase 318: never show opponent answer' not in src:
    src = src.replace(OLD_WAHLTE, NEW_WAHLTE, 1)
    fix('"wählte" text: guarded with S.sel!==null'); patches += 1
elif 'Phase 318: never show opponent answer' in src:
    ok('"wählte" guard already present')
else:
    skip('"wählte" text anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 5. Reset pending buffer on mpLeave / new game
# ─────────────────────────────────────────────────────────────────────────────
OLD_LEAVE = (
    'if(S._mpSoftlockTo){clearTimeout(S._mpSoftlockTo);S._mpSoftlockTo=null;}'
    'S.mp=null;S.mpModal=false;S.mpOpponent=null;S.mpSeed=null;S.mpRole=null;'
    'S.mpLockAnswer=undefined;S.mpOppLocked=false;render();'
)
NEW_LEAVE = (
    'if(S._mpSoftlockTo){clearTimeout(S._mpSoftlockTo);S._mpSoftlockTo=null;}'
    'S.mp=null;S.mpModal=false;S.mpOpponent=null;S.mpSeed=null;S.mpRole=null;'
    'S.mpLockAnswer=undefined;S.mpOppLocked=false;'
    'S._mpPendingOppSel=undefined;S._mpPendingOppSelOk=undefined; /* Phase 318 */render();'
)
if OLD_LEAVE in src:
    src = src.replace(OLD_LEAVE, NEW_LEAVE, 1)
    fix('mpLeave(): clears pending sel buffer'); patches += 1
else:
    ok('mpLeave pending clear already present')

# Also reset in S initializer (startGame resets mpOppSel, add pending too)
OLD_INIT = 'mpOppSel:null,mpOppLid:null,mpOppSelOk:null});  /* P208/P210: always reset sub-game state on new game */'
NEW_INIT = 'mpOppSel:null,mpOppLid:null,mpOppSelOk:null,_mpPendingOppSel:undefined,_mpPendingOppSelOk:undefined});  /* P208/P210 + Phase 318 */'
if OLD_INIT in src:
    src = src.replace(OLD_INIT, NEW_INIT, 1)
    fix('startGame S-reset: clears pending sel buffer'); patches += 1
else:
    ok('startGame pending clear already present')

# ─────────────────────────────────────────────────────────────────────────────
# 6. Waiting overlay: disable answer buttons (prevent double-fire after lock)
# ─────────────────────────────────────────────────────────────────────────────
OLD_OVERLAY_STYLE = (
    "'<div style=\"position:fixed;bottom:80px;left:50%;transform:translateX(-50%);"
    "background:#1e293b;border:1.5px solid #6366f1;border-radius:12px;padding:10px 20px;"
    "font-size:.85rem;font-weight:700;color:#c4b5fd;z-index:999;display:flex;align-items:center;gap:8px;\">"
    "<div style=\"width:10px;height:10px;border-radius:50%;background:#6366f1;animation:pulse 1s infinite\"></div>"
    "Warte auf Gegner…</div>\\':\'\';"
)
NEW_OVERLAY_STYLE = (
    "'<div style=\"position:fixed;bottom:80px;left:50%;transform:translateX(-50%);"
    "background:#1e293b;border:1.5px solid #6366f1;border-radius:12px;padding:10px 20px;"
    "font-size:.85rem;font-weight:700;color:#c4b5fd;z-index:999;display:flex;align-items:center;gap:8px;\">"
    "<div style=\"width:10px;height:10px;border-radius:50%;background:#6366f1;animation:pulse 1s infinite\"></div>"
    "Warte auf Gegner…</div>"
    # Add button blocker overlay when waiting
    "<div style=\\\"position:fixed;inset:0;z-index:998;pointer-events:all;background:transparent\\\" "
    "onclick=\\\"event.stopPropagation()\\\" ontouchstart=\\\"event.stopPropagation()\\\"></div>"
    "\\':\'\';"
)
if OLD_OVERLAY_STYLE in src and 'pointer-events:all;background:transparent' not in src:
    src = src.replace(OLD_OVERLAY_STYLE, NEW_OVERLAY_STYLE, 1)
    fix('Waiting overlay: added transparent click-blocker div'); patches += 1
else:
    ok('Click-blocker already present or overlay style changed')

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
save(os.path.join(BASE, 'gen.py'), src)
print(f'\n  {patches} patch(es) applied.')
print('✅ patch_318_mp_spoiler_fix.py done — run: python3 gen.py && python3 verify.py')
