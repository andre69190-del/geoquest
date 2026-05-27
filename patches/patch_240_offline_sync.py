"""
Phase: 240
Date:  2026-05-27
Author: Architect
Scope: Full Offline Sync — isOffline state, event listeners, optimistic queue, syncOfflineData(), UI banner

Description:
  Builds on Phase 238 (sw.js) + Phase 239 (auth UX guards) to give the app
  complete offline resilience for score saving.

  Fix 1: Add isOffline:!navigator.onLine to global S state object (not guarded
         by anti-cheat proxy — event listeners need free write access).

  Fix 2: Add "syncOfflineData" to _TRUSTED_FNS so the anti-cheat proxy
         allows score writes from the sync function.

  Fix 3: Add window online/offline event listeners after the load listener:
         - offline: sets S.isOffline=true, re-renders
         - online:  sets S.isOffline=false, re-renders, calls syncOfflineData()

  Fix 4: Replace the bare early-exit guard in saveSession with an offline queue:
         When !sb || !sbUser?.id || !navigator.onLine, if score>0 accumulate
         {pendingScore, pendingCoins} in localStorage key 'gq_offline_queue',
         then return. Online play continues to Supabase as before.

  Fix 5: Inject syncOfflineData() async function after saveSession:
         Reads gq_offline_queue, calls add_score RPC with accumulated totals,
         clears the queue, updates sbProfile in-memory, shows a toast.

  Fix 6: Add offline indicator banner to renderProfilTab — a red bar shown
         when S.isOffline is true, prepended to the existing return div.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ==============================================================================
# FIX 1 — Add isOffline to S state object
# ==============================================================================
OLD_S_END = '  carouselPages:{},\n};'
NEW_S_END = (
    '  carouselPages:{},\n'
    '  isOffline:!navigator.onLine,\n'
    '};'
)

assert c.count(OLD_S_END) == 1, f'S carouselPages anchor not unique ({c.count(OLD_S_END)})'
c = c.replace(OLD_S_END, NEW_S_END, 1)
print('  [OK] Fix 1: isOffline:!navigator.onLine added to S state')

# ==============================================================================
# FIX 2 — Add "syncOfflineData" to _TRUSTED_FNS
# ==============================================================================
OLD_TRUSTED_TAIL = '"answerByIdx","handleWsCheck","handleSLFSubmit","handleLandHauptstadtSubmit","lvAnswer"];'
NEW_TRUSTED_TAIL = '"answerByIdx","handleWsCheck","handleSLFSubmit","handleLandHauptstadtSubmit","lvAnswer","syncOfflineData"];'

assert c.count(OLD_TRUSTED_TAIL) == 1, f'_TRUSTED_FNS tail anchor not unique ({c.count(OLD_TRUSTED_TAIL)})'
c = c.replace(OLD_TRUSTED_TAIL, NEW_TRUSTED_TAIL, 1)
print('  [OK] Fix 2: syncOfflineData added to _TRUSTED_FNS')

# ==============================================================================
# FIX 3 — Add online/offline event listeners after load listener
# ==============================================================================
OLD_LOAD_LISTENER = "window.addEventListener('load',function(){initAntiCheat();});"
NEW_LOAD_LISTENER = (
    "window.addEventListener('load',function(){initAntiCheat();});\n"
    "/* Phase 240: track online/offline state */\n"
    "window.addEventListener('offline',function(){S.isOffline=true;render();});\n"
    "window.addEventListener('online',function(){S.isOffline=false;render();syncOfflineData();});"
)

assert c.count(OLD_LOAD_LISTENER) == 1, f'load listener anchor not unique ({c.count(OLD_LOAD_LISTENER)})'
c = c.replace(OLD_LOAD_LISTENER, NEW_LOAD_LISTENER, 1)
print('  [OK] Fix 3: online/offline event listeners added')

# ==============================================================================
# FIX 4 — Replace saveSession early-exit with offline queue
# ==============================================================================
OLD_SAVE_GUARD = '  if(!sb||!sbUser?.id)return;\n  try{await sb.from("game_sessions")'
NEW_SAVE_GUARD = (
    '  /* Phase 240: offline queue — accumulate score locally when no connection */\n'
    '  if(!sb||!sbUser?.id||!navigator.onLine){\n'
    '    if(score>0){\n'
    '      try{\n'
    '        const _q=JSON.parse(localStorage.getItem(\'gq_offline_queue\')||\'{"pendingScore":0,"pendingCoins":0}\');\n'
    '        _q.pendingScore=(_q.pendingScore||0)+score;\n'
    '        _q.pendingCoins=(_q.pendingCoins||0)+Math.floor(score/100);\n'
    '        localStorage.setItem(\'gq_offline_queue\',JSON.stringify(_q));\n'
    '      }catch(_qe){}\n'
    '    }\n'
    '    return;\n'
    '  }\n'
    '  try{await sb.from("game_sessions")'
)

assert c.count(OLD_SAVE_GUARD) == 1, f'saveSession guard anchor not unique ({c.count(OLD_SAVE_GUARD)})'
c = c.replace(OLD_SAVE_GUARD, NEW_SAVE_GUARD, 1)
print('  [OK] Fix 4: saveSession offline queue added')

# ==============================================================================
# FIX 5 — Inject syncOfflineData() after saveSession (before fetchLeaderboard)
# ==============================================================================
OLD_AFTER_SAVE = (
    '  if(sbProfile)checkTitleUp(sbProfile.total_score||0).catch(()=>{});\n'
    '}\nasync function fetchLeaderboard'
)
NEW_AFTER_SAVE = (
    '  if(sbProfile)checkTitleUp(sbProfile.total_score||0).catch(()=>{});\n'
    '}\n'
    '/* Phase 240: sync accumulated offline scores to Supabase on reconnect */\n'
    'async function syncOfflineData(){\n'
    '  if(!sb||!sbUser?.id||!navigator.onLine)return;\n'
    '  try{\n'
    '    const _raw=localStorage.getItem(\'gq_offline_queue\');\n'
    '    if(!_raw)return;\n'
    '    const _q=JSON.parse(_raw);\n'
    '    if(!_q.pendingScore&&!_q.pendingCoins)return;\n'
    '    await sb.rpc(\'add_score\',{p_user_id:sbUser.id,p_score:_q.pendingScore||0,p_coins:_q.pendingCoins||0,p_rounds:0,p_duration_ms:0});\n'
    '    localStorage.removeItem(\'gq_offline_queue\');\n'
    '    if(sbProfile){\n'
    '      sbProfile.total_score=(sbProfile.total_score||0)+(_q.pendingScore||0);\n'
    '      sbProfile.games_played=(sbProfile.games_played||0)+1;\n'
    '    }\n'
    '    showToast(\'\\u2705 Offline-Ergebnisse synchronisiert!\');\n'
    '    render();\n'
    '  }catch(_se){\n'
    '    console.warn(\'syncOfflineData failed\',_se);\n'
    '  }\n'
    '}\n'
    'async function fetchLeaderboard'
)

assert c.count(OLD_AFTER_SAVE) == 1, f'after-saveSession anchor not unique ({c.count(OLD_AFTER_SAVE)})'
c = c.replace(OLD_AFTER_SAVE, NEW_AFTER_SAVE, 1)
print('  [OK] Fix 5: syncOfflineData() function injected after saveSession')

# ==============================================================================
# FIX 6 — Add offline banner to renderProfilTab
# ==============================================================================
OLD_PROFIL_RETURN = (
    '  return \'<div style="padding-bottom:100px">\'+block1+block2+block3+block4+block5+block6+\'</div>\';'
)
NEW_PROFIL_RETURN = (
    '  const _offlineBanner=S.isOffline\n'
    '    ?\'<div style="background:#ef4444;color:#fff;padding:10px 16px;border-radius:8px;'
    'margin-bottom:12px;font-weight:600;text-align:center">&#x1F4F5; Du bist offline. '
    'Ergebnisse werden lokal gespeichert und beim n\\u00e4chsten Online-Start automatisch synchronisiert.</div>\'\n'
    '    :\'\';\n'
    '  return \'<div style="padding-bottom:100px">\'+_offlineBanner+block1+block2+block3+block4+block5+block6+\'</div>\';'
)

assert c.count(OLD_PROFIL_RETURN) == 1, f'renderProfilTab return anchor not unique ({c.count(OLD_PROFIL_RETURN)})'
c = c.replace(OLD_PROFIL_RETURN, NEW_PROFIL_RETURN, 1)
print('  [OK] Fix 6: offline banner added to renderProfilTab')

# ==============================================================================
# Write gen.py
# ==============================================================================
with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print()
print('  All Phase 240 fixes applied. Run: python gen.py && python verify.py')
