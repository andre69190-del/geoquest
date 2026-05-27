"""
Phase: 239
Date:  2026-05-27
Author: Architect
Scope: Offline Graceful Degradation — Auth UX hardening

Description:
  When the Service Worker (Phase 238) intercepts Supabase requests offline,
  the SDK may return an error object with no .message (e.g. {} from a 503
  response body parse failure).  The auth-error box then renders the raw
  object via template literal, producing the literal string "{}".

  Fix 1: Add _authErrMsg() helper — safely extracts message from any error
          shape; falls back to "Verbindungsfehler zum Server." for empties
          and plain objects ({}).

  Fix 2: navigator.onLine guards — early-exit in doLogin, doRegister,
          doForgotPassword, doSetNewPassword before any network attempt.
          Gives the user an immediate, clear offline message without
          waiting for a timeout or a confusing SDK error.

  Fix 3: Harden doLogin if(error) block — guard error?.message with ?. and
          add non-empty fallback at the end of the ternary chain so _m===""
          or _m===undefined never leaks through.

  Fix 4: Replace all bare err.message / e?.message fallbacks in catch blocks
          with _authErrMsg() calls.

  Fix 5: Replace bare error.message (no fallback) in doForgotPassword and
          doSetNewPassword with _authErrMsg(error).
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ==============================================================================
# FIX 1 — Inject _authErrMsg() helper before doRegister
# ==============================================================================
OLD_BEFORE_REGISTER = '/* Phase 27: Register */\nasync function doRegister(){'

NEW_BEFORE_REGISTER = (
    '/* Phase 239: safe auth-error message extractor */\n'
    'function _authErrMsg(err){\n'
    '  if(!err)return\'\';\n'
    '  const m=err?.message||err?.error_description||\'\';\n'
    '  if(m&&m.trim())return m.trim();\n'
    '  /* err exists but has no readable message (e.g. {} from 503 body) */\n'
    '  return\'Verbindungsfehler zum Server.\';\n'
    '}\n'
    '/* Phase 27: Register */\n'
    'async function doRegister(){'
)

assert c.count(OLD_BEFORE_REGISTER) == 1, f'helper insert anchor not unique ({c.count(OLD_BEFORE_REGISTER)})'
c = c.replace(OLD_BEFORE_REGISTER, NEW_BEFORE_REGISTER, 1)
print('  [OK] Fix 1: _authErrMsg() helper injected')

# ==============================================================================
# FIX 2a — navigator.onLine guard in doLogin
# ==============================================================================
OLD_LOGIN_GUARD = (
    'async function doLogin(){\n'
    '  if(!sb){showToast("Supabase nicht verbunden");return;}'
)
NEW_LOGIN_GUARD = (
    'async function doLogin(){\n'
    '  if(!sb){showToast("Supabase nicht verbunden");return;}\n'
    '  if(!navigator.onLine){S.authError="Du bist offline. Anmeldung ohne Internet nicht möglich.";render();return;}'
)

assert c.count(OLD_LOGIN_GUARD) == 1, f'doLogin guard anchor not unique ({c.count(OLD_LOGIN_GUARD)})'
c = c.replace(OLD_LOGIN_GUARD, NEW_LOGIN_GUARD, 1)
print('  [OK] Fix 2a: navigator.onLine guard added to doLogin')

# ==============================================================================
# FIX 2b — navigator.onLine guard in doRegister
# ==============================================================================
OLD_REGISTER_GUARD = (
    'if(!sb){showToast("Supabase nicht verbunden");return;}\n'
    '  const email=S.authEmail.trim();\n'
    '  const pw=S.authPassword;\n'
    '  const uname=S.authUsername'
)
NEW_REGISTER_GUARD = (
    'if(!sb){showToast("Supabase nicht verbunden");return;}\n'
    '  if(!navigator.onLine){S.authError="Du bist offline. Registrierung ohne Internet nicht möglich.";render();return;}\n'
    '  const email=S.authEmail.trim();\n'
    '  const pw=S.authPassword;\n'
    '  const uname=S.authUsername'
)

assert c.count(OLD_REGISTER_GUARD) == 1, f'doRegister guard anchor not unique ({c.count(OLD_REGISTER_GUARD)})'
c = c.replace(OLD_REGISTER_GUARD, NEW_REGISTER_GUARD, 1)
print('  [OK] Fix 2b: navigator.onLine guard added to doRegister')

# ==============================================================================
# FIX 2c — navigator.onLine guard in doForgotPassword  (uses \! for legacy sb check)
# ==============================================================================
OLD_FORGOT_GUARD = (
    'async function doForgotPassword(){\n'
    '  if(\\!sb){showToast("Supabase nicht verbunden");return;}'
)
NEW_FORGOT_GUARD = (
    'async function doForgotPassword(){\n'
    '  if(\\!sb){showToast("Supabase nicht verbunden");return;}\n'
    '  if(!navigator.onLine){S.authError="Du bist offline. Passwort-Reset ohne Internet nicht möglich.";render();return;}'
)

assert c.count(OLD_FORGOT_GUARD) == 1, f'doForgotPassword guard anchor not unique ({c.count(OLD_FORGOT_GUARD)})'
c = c.replace(OLD_FORGOT_GUARD, NEW_FORGOT_GUARD, 1)
print('  [OK] Fix 2c: navigator.onLine guard added to doForgotPassword')

# ==============================================================================
# FIX 2d — navigator.onLine guard in doSetNewPassword
# ==============================================================================
OLD_SETNEW_GUARD = (
    'async function doSetNewPassword(){\n'
    '  if(!sb){showToast("Supabase nicht verbunden");return;}\n'
    '  const pw=S.authPassword;'
)
NEW_SETNEW_GUARD = (
    'async function doSetNewPassword(){\n'
    '  if(!sb){showToast("Supabase nicht verbunden");return;}\n'
    '  if(!navigator.onLine){S.authError="Du bist offline. Passwortänderung ohne Internet nicht möglich.";render();return;}\n'
    '  const pw=S.authPassword;'
)

assert c.count(OLD_SETNEW_GUARD) == 1, f'doSetNewPassword guard anchor not unique ({c.count(OLD_SETNEW_GUARD)})'
c = c.replace(OLD_SETNEW_GUARD, NEW_SETNEW_GUARD, 1)
print('  [OK] Fix 2d: navigator.onLine guard added to doSetNewPassword')

# ==============================================================================
# FIX 3 — Harden doLogin if(error) block: error?.message with fallback
# ==============================================================================
OLD_LOGIN_ERR_MSG = 'const _m=error.message;'
NEW_LOGIN_ERR_MSG = 'const _m=error?.message||"";'

assert c.count(OLD_LOGIN_ERR_MSG) == 1, f'login error.message anchor not unique ({c.count(OLD_LOGIN_ERR_MSG)})'
c = c.replace(OLD_LOGIN_ERR_MSG, NEW_LOGIN_ERR_MSG, 1)

OLD_LOGIN_TERNARY_TAIL = '_m.includes("Too many requests")?"Zu viele Versuche. Bitte kurz warten.":_m;'
NEW_LOGIN_TERNARY_TAIL = '_m.includes("Too many requests")?"Zu viele Versuche. Bitte kurz warten.":_m||"Verbindungsfehler zum Server.";'

assert c.count(OLD_LOGIN_TERNARY_TAIL) == 1, f'login ternary tail anchor not unique ({c.count(OLD_LOGIN_TERNARY_TAIL)})'
c = c.replace(OLD_LOGIN_TERNARY_TAIL, NEW_LOGIN_TERNARY_TAIL, 1)
print('  [OK] Fix 3: doLogin if(error) hardened (?.message, non-empty fallback)')

# ==============================================================================
# FIX 4 — Replace catch fallbacks with _authErrMsg()
# ==============================================================================

# doLogin catch(e)
OLD_LOGIN_CATCH = 'S.authError=e?.message||"Anmeldung fehlgeschlagen.";'
NEW_LOGIN_CATCH  = 'S.authError=_authErrMsg(e)||"Anmeldung fehlgeschlagen.";'

assert c.count(OLD_LOGIN_CATCH) == 1, f'login catch anchor not unique ({c.count(OLD_LOGIN_CATCH)})'
c = c.replace(OLD_LOGIN_CATCH, NEW_LOGIN_CATCH, 1)

# doRegister catch(err) — _em assignment
OLD_REG_CATCH_EM = 'const _em=err.message||"";'
NEW_REG_CATCH_EM  = 'const _em=_authErrMsg(err);'

assert c.count(OLD_REG_CATCH_EM) == 1, f'register catch _em anchor not unique ({c.count(OLD_REG_CATCH_EM)})'
c = c.replace(OLD_REG_CATCH_EM, NEW_REG_CATCH_EM, 1)

# doRegister catch(err) — tail fallback now uses non-empty _em from _authErrMsg
OLD_REG_CATCH_TAIL = '_em||"Unbekannter Fehler.";'
NEW_REG_CATCH_TAIL  = '_em||"Verbindungsfehler zum Server.";'

assert c.count(OLD_REG_CATCH_TAIL) == 1, f'register catch tail anchor not unique ({c.count(OLD_REG_CATCH_TAIL)})'
c = c.replace(OLD_REG_CATCH_TAIL, NEW_REG_CATCH_TAIL, 1)

print('  [OK] Fix 4: catch blocks use _authErrMsg() in doLogin + doRegister')

# ==============================================================================
# FIX 5 — Replace bare error.message (no fallback) in doForgotPassword + doSetNewPassword
# ==============================================================================
OLD_FORGOT_ERR = 'if(error){S.authError=error.message;render();return;}'
NEW_FORGOT_ERR  = 'if(error){S.authError=_authErrMsg(error);render();return;}'

assert c.count(OLD_FORGOT_ERR) == 1, f'forgot error.message anchor not unique ({c.count(OLD_FORGOT_ERR)})'
c = c.replace(OLD_FORGOT_ERR, NEW_FORGOT_ERR, 1)

OLD_SETNEW_ERR = 'if(error){S.authError=error.message;return;}'
NEW_SETNEW_ERR  = 'if(error){S.authError=_authErrMsg(error);return;}'

assert c.count(OLD_SETNEW_ERR) == 1, f'setnew error.message anchor not unique ({c.count(OLD_SETNEW_ERR)})'
c = c.replace(OLD_SETNEW_ERR, NEW_SETNEW_ERR, 1)

print('  [OK] Fix 5: bare error.message → _authErrMsg() in doForgotPassword + doSetNewPassword')

# ==============================================================================
# Write gen.py
# ==============================================================================
with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print()
print('  All Phase 239 fixes applied. Run: python gen.py && python verify.py')
