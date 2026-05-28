"""
patch_277_zindex_fix.py
Phase 277: Z-Index Bleeding Fix (Bottom Navigation vs. Karten-Buttons)

Probleme:
  - .bottom-nav hat z-index:300, Fav/Info-Buttons haben z-index:99999
    → Buttons "bleeden" über die fixierte Tab-Bar hinaus beim Scrollen
  - body padding-bottom:68px kaum ausreichend (nav height 62px)
    → unterste Kartenreihe teils hinter der Nav verdeckt

Fixes:
  1. .bottom-nav z-index: 300 → 1000
  2. Fav-Button   z-index: 99999 → 2
  3. Info-Button  z-index: 99999 → 2
  4. body padding-bottom: 68px → 80px
"""

import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEN  = os.path.join(BASE, 'gen.py')

with open(GEN, 'r', encoding='utf-8') as f:
    src = f.read()

changes = 0

# ── 1. Bottom-Nav z-index: 300 → 1000 ─────────────────────────────────────
OLD1 = '.bottom-nav{position:fixed;bottom:0;left:0;right:0;height:62px;background:var(--bg2);border-top:1px solid var(--border);display:flex;z-index:300;transition:background .25s;padding-bottom:env(safe-area-inset-bottom)}'
NEW1 = '.bottom-nav{position:fixed;bottom:0;left:0;right:0;height:62px;background:var(--bg2);border-top:1px solid var(--border);display:flex;z-index:1000;transition:background .25s;padding-bottom:env(safe-area-inset-bottom)}'
if OLD1 in src:
    src = src.replace(OLD1, NEW1, 1)
    print('✅  .bottom-nav z-index 300 → 1000')
    changes += 1
else:
    print('⚠️  .bottom-nav-String nicht gefunden – Regex-Fallback...')
    src, n = re.subn(
        r'(\.bottom-nav\{[^}]*?)z-index:300(;[^}]*\})',
        r'\g<1>z-index:1000\2',
        src
    )
    if n:
        print(f'   Regex: {n} Ersetzung(en)')
        changes += n
    else:
        print('❌  .bottom-nav NICHT gepatcht!')

# ── 2. Fav-Button z-index: 99999 → 2 ──────────────────────────────────────
# Das Inline-Style enthält: ...z-index:99999;width:28px...
OLD2 = 'z-index:99999;width:28px;height:28px;background:transparent;border:none;font-size:.75rem;cursor:pointer;line-height:1;padding:0;touch-action:manipulation'
NEW2 = 'z-index:2;width:28px;height:28px;background:transparent;border:none;font-size:.75rem;cursor:pointer;line-height:1;padding:0;touch-action:manipulation'
if OLD2 in src:
    src = src.replace(OLD2, NEW2, 1)
    print('✅  Fav-Button  z-index 99999 → 2')
    changes += 1
else:
    print('⚠️  Fav-Button-String nicht gefunden – Regex-Fallback...')
    src, n = re.subn(
        r'(fav-btn[^>]*z-index:)99999(;width:28px)',
        r'\g<1>2\2',
        src
    )
    print(f'   Regex: {n} Ersetzung(en)')
    changes += n

# ── 3. Info-Button z-index: 99999 → 2 ─────────────────────────────────────
# Das Inline-Style enthält: ...z-index:99999;width:32px...
OLD3 = 'z-index:99999;width:32px;height:32px;background:#3b82f6;color:#fff;border:none;border-radius:8px;font-size:.75rem;font-weight:900;cursor:pointer;line-height:1;padding:0;touch-action:manipulation'
NEW3 = 'z-index:2;width:32px;height:32px;background:#3b82f6;color:#fff;border:none;border-radius:8px;font-size:.75rem;font-weight:900;cursor:pointer;line-height:1;padding:0;touch-action:manipulation'
if OLD3 in src:
    src = src.replace(OLD3, NEW3, 1)
    print('✅  Info-Button z-index 99999 → 2')
    changes += 1
else:
    print('⚠️  Info-Button-String nicht gefunden – Regex-Fallback...')
    src, n = re.subn(
        r'(info-btn-fix[^>]*z-index:)99999(;width:32px)',
        r'\g<1>2\2',
        src
    )
    print(f'   Regex: {n} Ersetzung(en)')
    changes += n

# ── 4. Body padding-bottom: 68px → 80px ───────────────────────────────────
OLD4 = 'body{padding-top:50px;padding-bottom:68px}'
NEW4 = 'body{padding-top:50px;padding-bottom:80px}'
if OLD4 in src:
    src = src.replace(OLD4, NEW4, 1)
    print('✅  body padding-bottom 68px → 80px')
    changes += 1
else:
    print('⚠️  body padding-string nicht gefunden – Regex-Fallback...')
    src, n = re.subn(
        r'(body\{padding-top:50px;padding-bottom:)\d+px(\})',
        r'\g<1>80px\2',
        src
    )
    print(f'   Regex: {n} Ersetzung(en)')
    changes += n

# ── Speichern ──────────────────────────────────────────────────────────────
if changes == 0:
    print('\n❌  Keine Änderungen – bitte gen.py manuell prüfen!')
else:
    with open(GEN, 'w', encoding='utf-8') as f:
        f.write(src)
    print(f'\n✅  patch_277 fertig ({changes} Änderungen). Jetzt: python3 gen.py && python3 verify.py')
