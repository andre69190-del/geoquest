#!/usr/bin/env python3
"""
patch_320_mp_read_time.py
Phase 320 — MULTIPLAYER POLISH: Extended Reveal Read Time

Changes:
1. MP reveal delay: 3500ms → 5500ms (both host and guest)
2. Fix: _isMpGuest now uses S.mpRole (S.mp is null during game — Phase 317 missed this)
3. Fix: _isMpHost also uses S.mpRole guard for consistency
   Solo: IATA questions 2800ms, all others 1900ms — unchanged.
"""
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    with open(p, encoding='utf-8') as f: return f.read()
def save(p, s):
    with open(p, 'w', encoding='utf-8') as f: f.write(s)
    print(f'  [OK] saved {os.path.relpath(p, BASE)}')

src = load(os.path.join(BASE, 'gen.py'))

OLD = (
    '  const _isMpHost=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null;\n'
    '  const _isMpGuest=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null&&S.mp?.role==="guest"; /* Phase 317/320: use S.mpRole */\n'
    '  /* Phase 320: MP reveal delay extended to 5500ms so players can read both answers */\n'
    '  const _fd=(_isMpHost||_isMpGuest)?5500:(_qt==="iata"?2800:1900);'
)

if OLD in src:
    print('  [OK]  patch_320 already applied — all values correct')
else:
    # Fresh apply
    OLD2 = (
        '  const _isMpHost=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null;\n'
        '  const _isMpGuest=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null&&S.mp?.role==="guest";\n'
        '  const _fd=_qt==="iata"?2800:(_isMpHost||_isMpGuest)?3500:1900;'
    )
    NEW = (
        '  const _isMpHost=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null&&S.mpRole!=="guest";\n'
        '  const _isMpGuest=window.mpGameCh&&S.mpOpponent&&S.mpSeed!==null&&S.mpRole==="guest"; /* Phase 317/320: use S.mpRole */\n'
        '  /* Phase 320: MP reveal delay extended to 5500ms so players can read both answers */\n'
        '  const _fd=(_isMpHost||_isMpGuest)?5500:(_qt==="iata"?2800:1900);'
    )
    if OLD2 in src:
        src = src.replace(OLD2, NEW, 1)
        print('  [FIX] MP delay 3500 → 5500ms + _isMpGuest uses S.mpRole')
        save(os.path.join(BASE, 'gen.py'), src)
    else:
        print('  [SKIP] anchor not found — may already be patched or structure changed')
        sys.exit(1)

print('\n✅ patch_320_mp_read_time.py done')
