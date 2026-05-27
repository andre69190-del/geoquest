"""
Phase: 241
Date:  2026-05-27
Author: Architect
Scope: Security cap, End-Screen Offline-UX, verify.py Section-0 dynamisiert

Description:
  Fix 1 - Security Cap in syncOfflineData() (gen.py)
    pendingScore: max 100_000 (5 Sessions x 21_780 max Hardcore-Score)
    pendingCoins: max 1_000  (Math.floor(100000/100))
    Basis: BASE=100, TB=10, ROUNDS=10 -> max/Session = ceil(10*(100+120)*9*1.1) = 21_780

  Fix 2 - Offline-Banner im Gameover End-Screen (gen.py)
    S.isOffline -> oranges Banner | sbOK -> original check/saving | else ""
    Pre-computed _scoreIndicator variable before app.innerHTML to avoid
    nested template-literal JS SyntaxError.

  Fix 3 - verify.py Section 0 dynamisiert (already applied in prior run)
    HTML_FILE + GEN_FILE fixed, dann os.listdir('data/') fuer alle *.json.
    Checksumme steigt von 56 auf 76.

  Zero-Bug Policy: assert c.count(old)==1 vor jedem replace.
"""

import os

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.dirname(HERE)
GEN    = os.path.join(ROOT, 'gen.py')
VERIFY = os.path.join(ROOT, 'verify.py')

# -- Read gen.py ---------------------------------------------------------------
with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ==============================================================================
# FIX 1 - Security Cap in syncOfflineData()
# ==============================================================================
OLD_SYNC = (
    "if(!_q.pendingScore&&!_q.pendingCoins)return;\n"
    "    await sb.rpc('add_score',{p_user_id:sbUser.id,"
    "p_score:_q.pendingScore||0,p_coins:_q.pendingCoins||0,"
    "p_rounds:0,p_duration_ms:0});"
)
NEW_SYNC = (
    "if(!_q.pendingScore&&!_q.pendingCoins)return;\n"
    "    /* Phase 241: client-side cap - prevents manipulated localStorage"
    " from inflating cloud score */\n"
    "    _q.pendingScore=Math.min(_q.pendingScore||0,100000);\n"
    "    _q.pendingCoins=Math.min(_q.pendingCoins||0,1000);\n"
    "    await sb.rpc('add_score',{p_user_id:sbUser.id,"
    "p_score:_q.pendingScore||0,p_coins:_q.pendingCoins||0,"
    "p_rounds:0,p_duration_ms:0});"
)

assert c.count(OLD_SYNC) == 1, f'Fix 1 anchor not unique ({c.count(OLD_SYNC)})'
c = c.replace(OLD_SYNC, NEW_SYNC, 1)
print('  [OK] Fix 1: pendingScore/Coins cap (100000/1000) added to syncOfflineData()')

# ==============================================================================
# FIX 2 - Offline-Banner im Gameover End-Screen
#   Strategy: pre-compute _scoreIndicator before app.innerHTML=`...` to avoid
#   JS SyntaxError from nested template literals.
#   Offline branch uses a plain JS single-quoted string (no backtick nesting).
#   Online branch uses one backtick level which is safe.
# ==============================================================================

# Fix 2a: Insert _scoreIndicator variable declaration before app.innerHTML
OLD_2A = '      </div>`:"";' + '\n' + 'app.innerHTML=`<div class="scr">'

_off = (
    'S.isOffline'
    + "?'<div style=\"background:#f97316;color:#fff;border-radius:8px;"
    + "padding:7px 12px;margin-top:5px;font-size:.74rem;font-weight:600;"
    + "text-align:center\">&#x1F50C; Ergebnis lokal gespeichert "
    + "&mdash; wird beim n&auml;chsten Online-Start synchronisiert.</div>'"
)
_on = (
    ':(sbOK?`<div style="font-size:.76rem;color:${S.scoreSaved?"#34d399":"var(--text3)"}">'
    + '${S.scoreSaved?"\\u2713 Score gespeichert":"Speichere \\u2026"}</div>`'
    + ":'');"
)
NEW_2A = (
    '      </div>`:"";' + '\n'
    + 'const _scoreIndicator=' + _off + _on + '\n'
    + 'app.innerHTML=`<div class="scr">'
)

assert c.count(OLD_2A) == 1, f'Fix 2a anchor not unique ({c.count(OLD_2A)})'
c = c.replace(OLD_2A, NEW_2A, 1)
print('  [OK] Fix 2a: _scoreIndicator variable inserted before gameover template')

# Fix 2b: Replace old ${sbOK?...} expression with ${_scoreIndicator}
OLD_2B = (
    '        ${sbOK?`<div style="font-size:.76rem;color:'
    + '${S.scoreSaved?"#34d399":"var(--text3)"}">'
    + '${S.scoreSaved?"\\u2713 Score gespeichert":"Speichere \\u2026"}</div>`:""}' + '\n'
    + '      </div>'
)
NEW_2B = '        ${_scoreIndicator}' + '\n' + '      </div>'

assert c.count(OLD_2B) == 1, f'Fix 2b anchor not unique ({c.count(OLD_2B)})'
c = c.replace(OLD_2B, NEW_2B, 1)
print('  [OK] Fix 2b: offline banner expression wired into gameover template')

# -- Write gen.py --------------------------------------------------------------
with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

# -- Fix 3: verify.py already updated in prior run (os.listdir dynamic check) --
print('  [OK] Fix 3: verify.py Section 0 already dynamisiert (skipped)')

print()
print('  All Phase 241 fixes applied. Run: python gen.py && python verify.py')
