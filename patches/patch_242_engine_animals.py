"""
Phase: 242
Date:  2026-05-27
Author: Claude / Andre
Scope: ENGINE & DATA SPRINT — Tiere-Pin data, Daily rotation, Blitz mode

Description:
  Fix 1 — Tiere-Pin JSON integration (3 anchors)
    Load data/tiere_pin.json as TIER_PIN_J in Python.
    Inject as PLACEHOLDER_TIER_PIN constant in JS, then Object.assign(KULTUR_DATA, TIER_PIN_DATA)
    so all 10 uk_tiere_*_pin modes work without GEN changes.

  Fix 2 — Daily Challenge rotation (1 anchor)
    Replace hardcoded S.mode="city" with 5-mode pool:
    ["city","flag","uk_wahrzeichen","uk_getraenke","uk_tiere_endemisch"]
    Rotated daily via Math.floor(Date.now()/86400000) % pool.length.

  Fix 3 — Blitz-Modus: 60-second speed round (10 anchors)
    New difficulty "blitz": 60s total time, no feedback screen, instant next question.
    Flash border green/red on answer. Gameover when blitzTimeLeft hits 0.
    LANG: add diff_desc_blitz to DE+EN. Diff button: Blitz.
    Scoring: same as casual (10pts per correct answer).

Dependencies: patch_241_security_ux.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import os

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.dirname(HERE)
GEN    = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ==============================================================================
# FIX 1a — Load tiere_pin.json in Python section
# ==============================================================================
OLD_1A = "with open(os.path.join(os.path.dirname(__file__), 'data/archaeologie_ws.json'), 'r', encoding='utf-8') as _f: ARCH_WS_J = _f.read()"
NEW_1A = (OLD_1A + "\n"
          "with open(os.path.join(os.path.dirname(__file__), 'data/tiere_pin.json'), 'r', encoding='utf-8') as _f: TIER_PIN_J = _f.read()")
assert c.count(OLD_1A) == 1, f'Fix 1a anchor not unique ({c.count(OLD_1A)})'
c = c.replace(OLD_1A, NEW_1A, 1)
print('  [OK] Fix 1a: tiere_pin.json loaded as TIER_PIN_J')

# ==============================================================================
# FIX 1b — Inject JS constant + Object.assign merge
# ==============================================================================
OLD_1B = 'const KULTUR_DATA=PLACEHOLDER_KULTUR_DATA;'
NEW_1B = ('const KULTUR_DATA=PLACEHOLDER_KULTUR_DATA;\n'
          'const TIER_PIN_DATA=PLACEHOLDER_TIER_PIN;\n'
          'Object.assign(KULTUR_DATA,TIER_PIN_DATA);')
assert c.count(OLD_1B) == 1, f'Fix 1b anchor not unique ({c.count(OLD_1B)})'
c = c.replace(OLD_1B, NEW_1B, 1)
print('  [OK] Fix 1b: TIER_PIN_DATA const + Object.assign injected')

# ==============================================================================
# FIX 1c — Python substitution
# ==============================================================================
OLD_1C = "  .replace('PLACEHOLDER_KULTUR_DATA', KULTUR_DATA_J)"
NEW_1C = ("  .replace('PLACEHOLDER_KULTUR_DATA', KULTUR_DATA_J)\n"
          "  .replace('PLACEHOLDER_TIER_PIN', TIER_PIN_J)")
assert c.count(OLD_1C) == 1, f'Fix 1c anchor not unique ({c.count(OLD_1C)})'
c = c.replace(OLD_1C, NEW_1C, 1)
print('  [OK] Fix 1c: PLACEHOLDER_TIER_PIN substitution added')

# ==============================================================================
# FIX 2 — Daily Challenge rotation (5-mode pool)
# ==============================================================================
OLD_2 = 'S.mode="city";S.diff="casual";S.isDailyRun=true;'
NEW_2 = ('const DAILY_POOL=["city","flag","uk_wahrzeichen","uk_getraenke","uk_tiere_endemisch"];'
         'const dayIndex=Math.floor(Date.now()/86400000);'
         'S.mode=DAILY_POOL[dayIndex%DAILY_POOL.length];'
         'S.diff="casual";S.isDailyRun=true;')
assert c.count(OLD_2) == 1, f'Fix 2 anchor not unique ({c.count(OLD_2)})'
c = c.replace(OLD_2, NEW_2, 1)
print('  [OK] Fix 2: Daily rotation pool (5 modes)')

# ==============================================================================
# FIX 3a — LANG DE: add diff_desc_blitz
# ==============================================================================
OLD_3A = 'diff_desc_surv:"\\u{1F480} Survival: Gegen die Uhr \\u00b7 8 Sekunden \\u00b7 3 Leben",'
NEW_3A = (OLD_3A
          + 'diff_desc_blitz:"\\u26A1 Blitz: 60 Sekunden \\u00b7 So viele Fragen wie m\\u00f6glich",')
assert c.count(OLD_3A) == 1, f'Fix 3a anchor not unique ({c.count(OLD_3A)})'
c = c.replace(OLD_3A, NEW_3A, 1)
print('  [OK] Fix 3a: diff_desc_blitz added to DE LANG')

# ==============================================================================
# FIX 3b — LANG EN: add diff_desc_blitz
# ==============================================================================
OLD_3B = 'diff_desc_surv:"\\u{1F480} Survival: Against the clock \\u00b7 8s \\u00b7 3 Lives",'
NEW_3B = (OLD_3B
          + 'diff_desc_blitz:"\\u26A1 Blitz: 60 seconds \\u00b7 Answer as many as you can",')
assert c.count(OLD_3B) == 1, f'Fix 3b anchor not unique ({c.count(OLD_3B)})'
c = c.replace(OLD_3B, NEW_3B, 1)
print('  [OK] Fix 3b: diff_desc_blitz added to EN LANG')

# ==============================================================================
# FIX 3c — Difficulty buttons: add Blitz button after Survival
# ==============================================================================
OLD_3C = '<button class="diff-btn ${S.diff==="survival"?"active":""}" onclick="S.diff=\'survival\';render()">💀 Survival</button>'
NEW_3C = (OLD_3C + '\n'
          '      <button class="diff-btn ${S.diff==="blitz"?"active":""}" '
          'onclick="S.diff=\'blitz\';render()">\\u26A1 Blitz</button>')
assert c.count(OLD_3C) == 1, f'Fix 3c anchor not unique ({c.count(OLD_3C)})'
c = c.replace(OLD_3C, NEW_3C, 1)
print('  [OK] Fix 3c: Blitz button added after Survival')

# ==============================================================================
# FIX 3d — Diff desc rendering: add blitz case
# ==============================================================================
OLD_3D = 't(S.diff==="casual"?"diff_desc_casual":S.diff==="hardcore"?"diff_desc_hc":"diff_desc_surv")'
NEW_3D = 't(S.diff==="casual"?"diff_desc_casual":S.diff==="hardcore"?"diff_desc_hc":S.diff==="blitz"?"diff_desc_blitz":"diff_desc_surv")'
assert c.count(OLD_3D) == 1, f'Fix 3d anchor not unique ({c.count(OLD_3D)})'
c = c.replace(OLD_3D, NEW_3D, 1)
print('  [OK] Fix 3d: blitz case in diff description rendering')

# ==============================================================================
# FIX 3e — startGame(): add blitzTimeLeft state field
# ==============================================================================
OLD_3E = 'survTimeBonusTotal:0,lives:S.diff==="casual"?999:3,'
NEW_3E = 'survTimeBonusTotal:0,blitzTimeLeft:S.diff==="blitz"?60:0,lives:S.diff==="casual"?999:3,'
assert c.count(OLD_3E) == 1, f'Fix 3e anchor not unique ({c.count(OLD_3E)})'
c = c.replace(OLD_3E, NEW_3E, 1)
print('  [OK] Fix 3e: blitzTimeLeft added to startGame()')

# ==============================================================================
# FIX 3f — lq(): dur = blitzTimeLeft for blitz mode
# ==============================================================================
OLD_3F = 'const _mCfg=(typeof GAME_MODES!=="undefined"?GAME_MODES:[]).find(m=>m.id===S.mode);const dur=S.diff==="survival"?8:(_mCfg&&_mCfg.time)||12;'
NEW_3F = 'const _mCfg=(typeof GAME_MODES!=="undefined"?GAME_MODES:[]).find(m=>m.id===S.mode);const dur=S.diff==="blitz"?(S.blitzTimeLeft>0?S.blitzTimeLeft:60):S.diff==="survival"?8:(_mCfg&&_mCfg.time)||12;'
assert c.count(OLD_3F) == 1, f'Fix 3f anchor not unique ({c.count(OLD_3F)})'
c = c.replace(OLD_3F, NEW_3F, 1)
print('  [OK] Fix 3f: lq() dur uses blitzTimeLeft for blitz mode')

# ==============================================================================
# FIX 3g — lq() timer interval: blitz tracks global time, gameover on timeout
# ==============================================================================
OLD_3G = 'tIv=setInterval(()=>{  /* P208: redundant clearInterval removed; self-cancel below */S.tm--;if(S.tm===3)soundWarn(); render();if(S.tm<=0){clearInterval(tIv);if(S.q)answer(null,_secretGameToken);} },1000);'
NEW_3G = ('tIv=setInterval(()=>{  /* P208: redundant clearInterval removed; self-cancel below */'
          'S.tm--;if(S.diff==="blitz")S.blitzTimeLeft=S.tm;if(S.tm===3)soundWarn(); render();'
          'if(S.tm<=0){clearInterval(tIv);if(S.diff==="blitz"){'
          'S.ph="gameover";S.scoreSaved=false;soundOver();checkMastery();updateDailyStreak();'
          'saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:S.rd,date:Date.now(),'
          'answers:S.sessionAnswers.map(a=>({cc:a.cc,correct:a.correct}))});'
          'if(sbOK)saveSession(S.mode,S.sc,S.bs,S.correct,Date.now()-(S.gameStartTime||Date.now()))'
          '.then(()=>{S.scoreSaved=true;render();},()=>{});render();'
          '}else if(S.q)answer(null,_secretGameToken);} },1000);')
assert c.count(OLD_3G) == 1, f'Fix 3g anchor not unique ({c.count(OLD_3G)})'
c = c.replace(OLD_3G, NEW_3G, 1)
print('  [OK] Fix 3g: lq() timer handles blitz gameover on timeout')

# ==============================================================================
# FIX 3h — answer(): blitz scores same as casual
# ==============================================================================
OLD_3H = 'if(S.diff==="casual"){pts=10;}'
NEW_3H = 'if(S.diff==="casual"||S.diff==="blitz"){pts=10;}'
assert c.count(OLD_3H) == 1, f'Fix 3h anchor not unique ({c.count(OLD_3H)})'
c = c.replace(OLD_3H, NEW_3H, 1)
print('  [OK] Fix 3h: blitz scores 10pts per correct answer')

# ==============================================================================
# FIX 3i — answer(): blitz bypasses feedback screen, flash border, instant next
# ==============================================================================
OLD_3I = 'S.pts=pts;S.lid=S.q.lid;S.ph="feedback";render();'
NEW_3I = (
    'if(S.diff==="blitz"){'
    'S.rd++;S.pts=pts;S.lid=S.q.lid;'
    "const _bApp=document.getElementById('app');"
    "if(_bApp){_bApp.style.outline=ok?'3px solid #34d399':'3px solid #ef4444';"
    "setTimeout(()=>{_bApp.style.outline='';},350);}"
    'if(S.blitzTimeLeft>0)lq();'
    'else{clearInterval(tIv);S.ph="gameover";S.scoreSaved=false;soundOver();'
    'checkMastery();updateDailyStreak();'
    'saveHistory({mode:S.mode,score:S.sc,correct:S.correct,rounds:S.rd,'
    'date:Date.now(),answers:S.sessionAnswers.map(a=>({cc:a.cc,correct:a.correct}))});'
    'if(sbOK)saveSession(S.mode,S.sc,S.bs,S.correct,Date.now()-(S.gameStartTime||Date.now()))'
    '.then(()=>{S.scoreSaved=true;render();},()=>{});render();}'
    'return;}\n'
    'S.pts=pts;S.lid=S.q.lid;S.ph="feedback";render();'
)
assert c.count(OLD_3I) == 1, f'Fix 3i anchor not unique ({c.count(OLD_3I)})'
c = c.replace(OLD_3I, NEW_3I, 1)
print('  [OK] Fix 3i: blitz bypasses feedback, flash border, instant next question')

# ==============================================================================
# FIX 3j — nextRound(): blitz excluded from ROUNDS end condition
# ==============================================================================
OLD_3J = 'if(S.diff!=="survival"&&nr>=ROUNDS){'
NEW_3J = 'if(S.diff!=="survival"&&S.diff!=="blitz"&&nr>=ROUNDS){'
assert c.count(OLD_3J) == 1, f'Fix 3j anchor not unique ({c.count(OLD_3J)})'
c = c.replace(OLD_3J, NEW_3J, 1)
print('  [OK] Fix 3j: blitz excluded from ROUNDS end condition')

# ==============================================================================
# Write gen.py
# ==============================================================================
with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print()
print('  All Phase 242 fixes applied (13 anchors).')
print('  Run: python3 gen.py && python3 verify.py')
