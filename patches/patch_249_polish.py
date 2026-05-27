"""
Phase: 249
Date:  2026-05-27
Author: Claude / Andre
Scope: Security-Fix submitRouteResult, PWA-Banner, LocalStorage-TTL, Pipeline-Upgrade

Description:
  Vier Verbesserungen aus dem Mega-Audit-Sprint:

  1. SECURITY: submitRouteResult() extrahiert den State-Mutation-Inline-onclick
     aus dem Reiserouten-Modus in eine dedizierte Funktion und trägt sie in
     _TRUSTED_FNS ein — analog zu submitGridResult().
     WICHTIG: Verwendet Assignment (=), nicht Increment (+=), identisch mit
     dem Original-onclick und submitGridResult()-Pattern. Enthält S.rd=...
     das im Sprint-Brief vergessen wurde.

  2. PWA-BANNER: Das pwa-banner HTML-Element fehlte im DOM — der
     beforeinstallprompt-Handler konnte es nie finden. Fix: Handler ruft
     render() auf; renderPwaBanner() erzeugt das Element dynamisch.

  3. LOCALSTORAGE TTL: Bereinigt Sessions älter als 90 Tage beim Schreiben.
     KORREKTUR gegenüber Sprint-Brief: Sessions nutzen das Feld `date`
     (ISO-String), NICHT `timestamp`. Filter: Date.parse(s.date).

  4. PIPELINE: run_patch.py ruft nach verify.py automatisch
     validate_content.py auf (nicht blockierend, nur informell).

Dependencies: patch_243b_modes_fix.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import pathlib, subprocess

ROOT = pathlib.Path(__file__).parent.parent
gen  = ROOT / "gen.py"
rp   = ROOT / "run_patch.py"
c    = gen.read_text(encoding="utf-8")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 1a: submitRouteResult in _TRUSTED_FNS eintragen
# ══════════════════════════════════════════════════════════════════════════════
old_trusted = '"handleWsCheck","handleSLFSubmit","handleLandHauptstadtSubmit","lvAnswer","syncOfflineData"]'
assert c.count(old_trusted) == 1, f"Anchor not unique: {old_trusted!r}"
new_trusted  = '"handleWsCheck","handleSLFSubmit","handleLandHauptstadtSubmit","lvAnswer","syncOfflineData","submitRouteResult"]'
c = c.replace(old_trusted, new_trusted, 1)
print("  [OK] 1a: submitRouteResult in _TRUSTED_FNS eingetragen")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 1b: submitRouteResult() Funktion definieren (direkt vor submitGridResult)
# ══════════════════════════════════════════════════════════════════════════════
old_sgr = 'function submitGridResult(){if(S.gridData){S.sc=S.gridData.score;S.correct=S.gridData.correctCount;S.rd=S.gridData.correctCount;}finishCustomGame();}'
assert c.count(old_sgr) == 1, f"Anchor not unique: {old_sgr!r}"
new_sgr = ('function submitRouteResult(){if(S.routeData){S.sc=S.routeData.score;'
           'S.correct=S.routeData.steps;S.rd=S.routeData.steps;}finishCustomGame();}\n'
           + old_sgr)
c = c.replace(old_sgr, new_sgr, 1)
print("  [OK] 1b: submitRouteResult() Funktion definiert (Zuweisung = wie submitGridResult)")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 1c: Inline-onclick im Reiserouten-Modus ersetzen
# ══════════════════════════════════════════════════════════════════════════════
old_onclick = ('  <button class="btn-p" onclick="S.sc=S.routeData.score;'
               'S.correct=S.routeData.steps;S.rd=S.routeData.steps;finishCustomGame()">'
               'Ergebnis ansehen</button>`')
assert c.count(old_onclick) == 1, f"Anchor not unique: {old_onclick!r}"
new_onclick = '  <button class="btn-p" onclick="submitRouteResult()">Ergebnis ansehen</button>`'
c = c.replace(old_onclick, new_onclick, 1)
print("  [OK] 1c: Inline-onclick durch submitRouteResult() ersetzt")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 2a: renderPwaBanner() Funktion hinzufügen (vor renderBottomNav)
# ══════════════════════════════════════════════════════════════════════════════
old_rbn_anchor = 'return`<nav class="bottom-nav">'
assert c.count(old_rbn_anchor) == 1, f"Anchor not unique: {old_rbn_anchor!r}"
pwa_fn = (
    'function renderPwaBanner(){\n'
    '  return`<div id="pwa-banner" class="pwa-banner">\n'
    '    <span>\U0001f4f1 GeoQuest als App installieren &mdash; offline spielbar!</span>\n'
    '    <button class="pwa-install-btn" onclick="if(S.pwaPrompt){S.pwaPrompt.prompt();'
    'S.pwaPrompt.userChoice.then(()=>{S.pwaPrompt=null;render();});}">'
    '\U0001f4e5 Installieren</button>\n'
    '  </div>`;\n'
    '}\n'
)
c = c.replace(old_rbn_anchor, pwa_fn + old_rbn_anchor, 1)
print("  [OK] 2a: renderPwaBanner() Funktion hinzugefügt")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 2b: beforeinstallprompt-Handler auf render() umstellen
#   Alter Code versuchte getElementById("pwa-banner") — Element existierte nie im DOM.
#   Neu: render() erzwingt einen Re-Render, renderPwaBanner() baut das Element dann.
# ══════════════════════════════════════════════════════════════════════════════
old_bip = ('  window.addEventListener("beforeinstallprompt",e=>{e.preventDefault();'
           'S.pwaPrompt=e;const b=document.getElementById("pwa-banner");'
           'if(b)b.style.display="flex";});')
assert c.count(old_bip) == 1, f"Anchor not unique: {old_bip!r}"
new_bip = ('  window.addEventListener("beforeinstallprompt",e=>{'
           'e.preventDefault();S.pwaPrompt=e;render();});')
c = c.replace(old_bip, new_bip, 1)
print("  [OK] 2b: beforeinstallprompt-Handler auf render() umgestellt (DOM-Element fix)")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 2c: PWA-Banner in Menu-Render einfügen
# ══════════════════════════════════════════════════════════════════════════════
old_menu_end = '    </div>${renderBottomNav()}`;\n    if(S.tab==="home")setTimeout(_scheduleFilterRefresh,80);\n    return;\n  }'
assert c.count(old_menu_end) == 1, f"Anchor not unique: {old_menu_end!r}"
new_menu_end = ('    </div>${renderBottomNav()}${S.pwaPrompt?renderPwaBanner():""}`;\n'
                '    if(S.tab==="home")setTimeout(_scheduleFilterRefresh,80);\n'
                '    return;\n  }')
c = c.replace(old_menu_end, new_menu_end, 1)
print("  [OK] 2c: PWA-Banner dynamisch in Menu-Render eingefügt")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 3: LocalStorage TTL-Cleanup (90 Tage)
#   KORREKTUR gegenüber Sprint-Brief: Sessions nutzen `date` (ISO-String),
#   NICHT `timestamp`. Filter muss Date.parse(s.date) verwenden.
# ══════════════════════════════════════════════════════════════════════════════
old_loc = ('    const _loc=JSON.parse(localStorage.getItem("gq_sessions_local")||"[]");\n'
           '    _loc.push({mode,score,max:bs,correct,duration_ms:durationMs||0,'
           'date:new Date().toISOString(),device_type:_device});\n'
           '    localStorage.setItem("gq_sessions_local",JSON.stringify(_loc.slice(-50)));')
assert c.count(old_loc) == 1, f"Anchor not unique: {old_loc!r}"
new_loc = (
    '    const _ttl=90*24*60*60*1000;\n'
    '    const _loc=JSON.parse(localStorage.getItem("gq_sessions_local")||"[]")'
    '.filter(s=>s&&s.date&&(Date.now()-Date.parse(s.date))<_ttl);\n'
    '    _loc.push({mode,score,max:bs,correct,duration_ms:durationMs||0,'
    'date:new Date().toISOString(),device_type:_device});\n'
    '    localStorage.setItem("gq_sessions_local",JSON.stringify(_loc.slice(-200)));'
)
c = c.replace(old_loc, new_loc, 1)
print("  [OK] 3: LocalStorage TTL-Filter (90 Tage, Feld 'date' statt 'timestamp'); Limit 50->200")

# ══════════════════════════════════════════════════════════════════════════════
# Patch auf gen.py schreiben
# ══════════════════════════════════════════════════════════════════════════════
gen.write_text(c, encoding="utf-8")
print()
print("patch_249_polish.py (gen.py) erfolgreich angewendet.")

# ══════════════════════════════════════════════════════════════════════════════
# SCHRITT 4: run_patch.py — validate_content.py nach verify.py einfügen
# ══════════════════════════════════════════════════════════════════════════════
rp_text = rp.read_text(encoding="utf-8")

old_rp = ('# ---- 6. Cleanup backup ----\n'
          'os.remove(backup)\n'
          '\n'
          '# ---- 7. Summary ----')
assert rp_text.count(old_rp) == 1, f"run_patch.py anchor not unique: {old_rp!r}"
new_rp = (
    '# ---- 6. Cleanup backup ----\n'
    'os.remove(backup)\n'
    '\n'
    '# ---- 6b. validate_content (non-blocking, info only) ----\n'
    'print("\\n-- Running validate_content.py " + "-" * 26)\n'
    'subprocess.run([sys.executable, "validate_content.py"], text=True)\n'
    'print("[INFO] validate_content.py finished (warnings do not block the build)")\n'
    '\n'
    '# ---- 7. Summary ----'
)
rp_text = rp_text.replace(old_rp, new_rp, 1)
rp.write_text(rp_text, encoding="utf-8")
print("patch_249_polish.py (run_patch.py) erfolgreich angewendet.")
