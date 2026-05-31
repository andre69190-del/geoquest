#!/usr/bin/env python3
"""
patch_319_mp_final_polish.py
Phase 319 — MULTIPLAYER POLISH: Full State Secrecy & Disconnect UX

Fixes:
1. Score-Bar Leak   — buffer S.mpOppScore when S.sel===null
2. Runden-Drift     — buffer S.mpOppRd when S.sel===null
3. Disconnect Toast — show toast + mpLeave() on CHANNEL_ERROR / TIMED_OUT / CLOSED
                      in both lobby and in-game channels
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
# 1 + 2: Buffer score and rd in score_update handler (extend Phase 318 block)
# ─────────────────────────────────────────────────────────────────────────────
OLD_SCORE_LINE = (
    '        S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;\n'
    '        if("lid" in payload){\n'
    '          S.mpOppLid=payload.lid;\n'
    '          /* Phase 318: buffer sel/selOk — only apply after local player has answered */'
)
NEW_SCORE_LINE = (
    '        /* Phase 319: buffer score+rd until local has answered (prevent score-bar/round leak) */\n'
    '        if(S.sel!==null){\n'
    '          S.mpOppScore=payload.score||0;S.mpOppRd=payload.rd||0;\n'
    '        }else{\n'
    '          S._mpPendingOppScore=payload.score||0;S._mpPendingOppRd=payload.rd||0;\n'
    '        }\n'
    '        if("lid" in payload){\n'
    '          S.mpOppLid=payload.lid;\n'
    '          /* Phase 318: buffer sel/selOk — only apply after local player has answered */'
)
if OLD_SCORE_LINE in src and 'Phase 319: buffer score+rd' not in src:
    src = src.replace(OLD_SCORE_LINE, NEW_SCORE_LINE, 1)
    fix('score_update: score+rd buffered when S.sel===null')
    patches += 1
elif 'Phase 319: buffer score+rd' in src:
    ok('score+rd buffer already present')
else:
    skip('score_update Phase-318 handler anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 3: Flush score+rd in _mpReveal() alongside sel/selOk
# ─────────────────────────────────────────────────────────────────────────────
OLD_REVEAL_FLUSH = (
    '  /* Phase 318: flush buffered opponent sel/selOk now that we have answered */\n'
    '  if(S._mpPendingOppSel!==undefined){\n'
    '    S.mpOppSel=S._mpPendingOppSel;S.mpOppSelOk=!!S._mpPendingOppSelOk;\n'
    '    S._mpPendingOppSel=undefined;S._mpPendingOppSelOk=undefined;\n'
    '  }'
)
NEW_REVEAL_FLUSH = (
    '  /* Phase 318: flush buffered opponent sel/selOk now that we have answered */\n'
    '  if(S._mpPendingOppSel!==undefined){\n'
    '    S.mpOppSel=S._mpPendingOppSel;S.mpOppSelOk=!!S._mpPendingOppSelOk;\n'
    '    S._mpPendingOppSel=undefined;S._mpPendingOppSelOk=undefined;\n'
    '  }\n'
    '  /* Phase 319: flush buffered score + rd */\n'
    '  if(S._mpPendingOppScore!==undefined){S.mpOppScore=S._mpPendingOppScore;S._mpPendingOppScore=undefined;}\n'
    '  if(S._mpPendingOppRd!==undefined){S.mpOppRd=S._mpPendingOppRd;S._mpPendingOppRd=undefined;}'
)
if OLD_REVEAL_FLUSH in src and 'Phase 319: flush buffered score' not in src:
    src = src.replace(OLD_REVEAL_FLUSH, NEW_REVEAL_FLUSH, 1)
    fix('_mpReveal(): flushes pending score+rd')
    patches += 1
elif 'Phase 319: flush buffered score' in src:
    ok('_mpReveal score+rd flush already present')
else:
    skip('Phase-318 flush block anchor in _mpReveal()')

# ─────────────────────────────────────────────────────────────────────────────
# 4: Add pending score/rd to startGame reset
# ─────────────────────────────────────────────────────────────────────────────
OLD_RESET = (
    '_mpPendingOppSel:undefined,_mpPendingOppSelOk:undefined});  /* P208/P210 + Phase 318 */'
)
NEW_RESET = (
    '_mpPendingOppSel:undefined,_mpPendingOppSelOk:undefined,'
    '_mpPendingOppScore:undefined,_mpPendingOppRd:undefined});  /* P208/P210 + Phase 318/319 */'
)
if OLD_RESET in src:
    src = src.replace(OLD_RESET, NEW_RESET, 1)
    fix('startGame S-reset: clears pending score+rd')
    patches += 1
else:
    ok('startGame pending score/rd clear already present')

# Also clear in mpLeave()
OLD_LEAVE_CLEAR = 'S._mpPendingOppSel=undefined;S._mpPendingOppSelOk=undefined; /* Phase 318 */render();'
NEW_LEAVE_CLEAR = 'S._mpPendingOppSel=undefined;S._mpPendingOppSelOk=undefined;S._mpPendingOppScore=undefined;S._mpPendingOppRd=undefined; /* Phase 318/319 */render();'
if OLD_LEAVE_CLEAR in src:
    src = src.replace(OLD_LEAVE_CLEAR, NEW_LEAVE_CLEAR, 1)
    fix('mpLeave(): clears pending score+rd')
    patches += 1
else:
    ok('mpLeave pending score/rd clear already present')

# ─────────────────────────────────────────────────────────────────────────────
# 5: Disconnect Toast — HOST lobby channel subscribe
# ─────────────────────────────────────────────────────────────────────────────
OLD_HOST_SUB = (
    '.subscribe((status)=>{\n'
    '      mpLog("host channel status:",status);\n'
    '      if(status==="SUBSCRIBED")render();\n'
    '    });'
)
NEW_HOST_SUB = (
    '.subscribe((status)=>{\n'
    '      mpLog("host channel status:",status);\n'
    '      if(status==="SUBSCRIBED")render();\n'
    '      /* Phase 319: Disconnect detection in lobby */\n'
    '      else if(status==="CHANNEL_ERROR"||status==="TIMED_OUT"||status==="CLOSED"){\n'
    '        mpLog("host channel lost:",status);\n'
    '        if(S.mp){showToast("⚠️ Verbindung zum Raum verloren — bitte neu erstellen.");mpLeave();}\n'
    '      }\n'
    '    });'
)
if OLD_HOST_SUB in src and 'Phase 319: Disconnect detection in lobby' not in src:
    src = src.replace(OLD_HOST_SUB, NEW_HOST_SUB, 1)
    fix('Host lobby subscribe: disconnect toast added')
    patches += 1
elif 'Phase 319: Disconnect detection in lobby' in src:
    ok('Host disconnect toast already present')
else:
    skip('host subscribe anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 6: Disconnect Toast — GUEST lobby channel subscribe
# ─────────────────────────────────────────────────────────────────────────────
OLD_GUEST_SUB = (
    '.subscribe((status)=>{\n'
    '      mpLog("guest channel status:",status);\n'
    '      if(status==="SUBSCRIBED"){\n'
    '        mpSend("player_joined",{name:sbProfile?.username||"Spieler"});\n'
    '        render();\n'
    '      }\n'
    '    });'
)
NEW_GUEST_SUB = (
    '.subscribe((status)=>{\n'
    '      mpLog("guest channel status:",status);\n'
    '      if(status==="SUBSCRIBED"){\n'
    '        mpSend("player_joined",{name:sbProfile?.username||"Spieler"});\n'
    '        render();\n'
    '      }\n'
    '      /* Phase 319: Disconnect detection in lobby */\n'
    '      else if(status==="CHANNEL_ERROR"||status==="TIMED_OUT"||status==="CLOSED"){\n'
    '        mpLog("guest channel lost:",status);\n'
    '        if(S.mp){showToast("⚠️ Verbindung zum Raum verloren — bitte Code neu eingeben.");mpLeave();}\n'
    '      }\n'
    '    });'
)
if OLD_GUEST_SUB in src and 'Phase 319: Disconnect detection in lobby' not in src[src.index('/* GUEST: join room */'):]:
    src = src.replace(OLD_GUEST_SUB, NEW_GUEST_SUB, 1)
    fix('Guest lobby subscribe: disconnect toast added')
    patches += 1
elif 'Phase 319: Disconnect detection in lobby' in src[src.index('/* GUEST: join room */'):]:
    ok('Guest disconnect toast already present')
else:
    skip('guest subscribe anchor')

# ─────────────────────────────────────────────────────────────────────────────
# 7: Disconnect Toast — In-game mpGameCh (after countdown, during game)
#    Supabase Realtime fires system events — add a system event listener
# ─────────────────────────────────────────────────────────────────────────────
OLD_GAMEOVER_SYNC_END = (
    "        if(S.mpRole===\"guest\"&&S.ph!==\"gameover\"){\n"
    "          clearTimeout(fTo);S.mpOppLocked=false;S.mpLockAnswer=undefined;\n"
    "          if(S._mpSoftlockTo){clearTimeout(S._mpSoftlockTo);S._mpSoftlockTo=null;}\n"
    "          S.mpOppFinal=payload;\n"
    "          S.ph=\"gameover\";S.scoreSaved=false;S.convModal=true;\n"
    "          soundOver();checkMastery();render();\n"
    "        }\n"
    "      });"
)
NEW_GAMEOVER_SYNC_END = (
    "        if(S.mpRole===\"guest\"&&S.ph!==\"gameover\"){\n"
    "          clearTimeout(fTo);S.mpOppLocked=false;S.mpLockAnswer=undefined;\n"
    "          if(S._mpSoftlockTo){clearTimeout(S._mpSoftlockTo);S._mpSoftlockTo=null;}\n"
    "          S.mpOppFinal=payload;\n"
    "          S.ph=\"gameover\";S.scoreSaved=false;S.convModal=true;\n"
    "          soundOver();checkMastery();render();\n"
    "        }\n"
    "      })\n"
    "      /* Phase 319: in-game disconnect detection via system events */\n"
    "      .on('system',{},(status)=>{\n"
    "        if(status==='CHANNEL_ERROR'||status==='TIMED_OUT'||status==='CLOSED'){\n"
    "          mpLog('in-game channel lost:',status);\n"
    "          if(S.mpOpponent&&S.ph==='playing'){\n"
    "            showToast('⚠️ Verbindung zum Gegner verloren — Spiel wird beendet.');\n"
    "            /* Force-reveal if waiting, then let game continue solo */\n"
    "            if(S.mpLockAnswer!==undefined){_mpReveal(_secretGameToken);}\n"
    "            window.mpGameCh=null;S.mpOpponent=null;S.mpRole=null;\n"
    "          }\n"
    "        }\n"
    "      });"
)
if OLD_GAMEOVER_SYNC_END in src and 'Phase 319: in-game disconnect' not in src:
    src = src.replace(OLD_GAMEOVER_SYNC_END, NEW_GAMEOVER_SYNC_END, 1)
    fix('mpGameCh: in-game disconnect toast + force-reveal')
    patches += 1
elif 'Phase 319: in-game disconnect' in src:
    ok('In-game disconnect handler already present')
else:
    skip('GAMEOVER_SYNC listener end anchor')

# ─────────────────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────────────────
save(os.path.join(BASE, 'gen.py'), src)
print(f'\n  {patches} patch(es) applied.')
print('✅ patch_319_mp_final_polish.py done — run: python3 gen.py && python3 verify.py')
