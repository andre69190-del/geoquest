#!/usr/bin/env python3
"""
patch_295_avatar_encoding.py
Behebt doppelt-UTF-8-kodiertes ⏳ (Sanduhr-Emoji) in gen.py.
Betroffen: MP-Lobby-Screen (Zeilen 5083/5088) + Kennzeichen-Album (Zeile 11823).
Die Bytes â\x8f³ (U+00E2 U+008F U+00B3) entstehen wenn E2 8F B3 (UTF-8 von ⏳)
als Latin-1 gelesen und dann nochmal als UTF-8 geschrieben wird.
"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

GEN = os.path.join(os.path.dirname(__file__), '..', 'gen.py')

with open(GEN, 'r', encoding='utf-8') as f:
    content = f.read()

# â\x8f³ = doppelt-kodiertes ⏳ — ersetze durch sauberes Unicode-Escape
BAD   = 'â³'   # die drei falschen Zeichen
GOOD  = '\\u{23F3}'            # sauberes JS-Unicode-Escape für ⏳

count = content.count(BAD)
if count == 0:
    print('[SKIP] Kein doppelt-kodiertes ⏳ gefunden — bereits gepatcht?')
    sys.exit(0)

content = content.replace(BAD, GOOD)

with open(GEN, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'[OK] {count}x â\\x8f³ → \\u{{23F3}} (⏳) in gen.py ersetzt')
