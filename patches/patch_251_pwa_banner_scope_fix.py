"""
Phase: 251
Date:  2026-05-27
Author: Claude / Andre
Scope: HOTFIX — move renderPwaBanner() from nested-local to top-level scope.

Description:
  Phase 249 accidentally placed renderPwaBanner() as a nested function INSIDE
  renderBottomNav(). This made it invisible outside that function, causing:

    Uncaught ReferenceError: renderPwaBanner is not defined
    at render (Index):43753:35

  This patch extracts renderPwaBanner() from inside renderBottomNav() and
  re-inserts it as a standalone top-level function immediately before
  renderBottomNav(), so render() can call it without error.

Dependencies: patch_249_polish.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""

import re, sys, pathlib

ROOT = pathlib.Path(__file__).parent.parent
GEN  = ROOT / "gen.py"

c = GEN.read_text(encoding="utf-8")
original_len = len(c)

# ── Step 1: Remove the nested renderPwaBanner definition from inside
#            renderBottomNav(). The exact block is lines 11204-11209.
# ─────────────────────────────────────────────────────────────────────
OLD_NESTED = (
    '  function renderPwaBanner(){\n'
    '  return`<div id="pwa-banner" class="pwa-banner">\n'
    '    <span>📱 GeoQuest als App installieren &mdash; offline spielbar!</span>\n'
    '    <button class="pwa-install-btn" onclick="if(S.pwaPrompt){S.pwaPrompt.prompt();S.pwaPrompt.userChoice.then(()=>{S.pwaPrompt=null;render();});}">📥 Installieren</button>\n'
    '  </div>`;\n'
    '}\n'
)
assert c.count(OLD_NESTED) == 1, f"Anchor not unique (OLD_NESTED): {OLD_NESTED!r}"
c = c.replace(OLD_NESTED, '', 1)

print("✓ Step 1: nested renderPwaBanner() removed from renderBottomNav()")

# ── Step 2: Insert renderPwaBanner() as a top-level function just before
#            the /* BOTTOM NAV */ comment block.
# ─────────────────────────────────────────────────────────────────────
OLD_SECTION_HEADER = '/* BOTTOM NAV */\nfunction renderBottomNav(){'
NEW_SECTION_HEADER = (
    '/* BOTTOM NAV */\n'
    'function renderPwaBanner(){\n'
    '  return`<div id="pwa-banner" class="pwa-banner">\n'
    '    <span>📱 GeoQuest als App installieren &mdash; offline spielbar!</span>\n'
    '    <button class="pwa-install-btn" onclick="if(S.pwaPrompt){S.pwaPrompt.prompt();S.pwaPrompt.userChoice.then(()=>{S.pwaPrompt=null;render();});}">📥 Installieren</button>\n'
    '  </div>`;\n'
    '}\n'
    'function renderBottomNav(){'
)
assert c.count(OLD_SECTION_HEADER) == 1, f"Anchor not unique (OLD_SECTION_HEADER): {OLD_SECTION_HEADER!r}"
c = c.replace(OLD_SECTION_HEADER, NEW_SECTION_HEADER, 1)

print("✓ Step 2: renderPwaBanner() inserted as top-level function before renderBottomNav()")

# ── Write back ────────────────────────────────────────────────────────
GEN.write_text(c, encoding="utf-8")
print(f"✓ gen.py updated ({original_len} → {len(c)} bytes, Δ={len(c)-original_len:+d})")
print("✓ patch_251_pwa_banner_scope_fix.py DONE — run verify.py next")
