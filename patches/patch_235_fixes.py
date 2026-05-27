"""
patch_235_fixes.py
==================
Fix 1: Strip all [BETA] tags from MODES array titles in gen.py
Fix 2: Uppercase all validWords in WS JSON files
Fix 3: Remove invalid anagram words (use letters not in base word)
Fix 4: Add q.ans fallback guard in render() feedback to prevent empty "Falsch →" text
"""
import os, json, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')

# ══════════════════════════════════════════════════════════════════════════════
# FIX 1: Strip [BETA] from all MODES titles in gen.py
# ══════════════════════════════════════════════════════════════════════════════
with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

before = c.count('[BETA]')
c = c.replace('"[BETA] ', '"')  # remove "[BETA] " prefix in double-quoted titles
c = c.replace("'[BETA] ", "'")  # single-quoted just in case
# Edge case: [BETA] at start of desc field (no space after)
c = c.replace('"[BETA]', '"')
after = c.count('[BETA]')

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print(f"  [OK] Fix 1: {before - after} [BETA] tags stripped from gen.py ({after} remaining)")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 2 + 3: Uppercase validWords and remove invalid anagrams in WS JSON files
# ══════════════════════════════════════════════════════════════════════════════
DATA = os.path.join(ROOT, 'data')
ws_files = sorted(f for f in os.listdir(DATA) if f.endswith('_ws.json'))

total_uppercased = 0
total_removed    = 0

def can_spell(word, base_counter):
    wc = Counter(word.upper())
    for ch, cnt in wc.items():
        if base_counter[ch] < cnt:
            return False
    return True

for fn in ws_files:
    path = os.path.join(DATA, fn)
    with open(path, 'r', encoding='utf-8') as fh:
        d = json.load(fh)

    file_up = 0
    file_rm = 0

    for key, block in d.items():
        base = block.get('word', '')
        if not base:
            continue
        base_counter = Counter(base.upper())
        vw = block.get('validWords', {})

        if isinstance(vw, dict):
            for lang in list(vw.keys()):
                words = vw[lang]
                new_words = []
                for w in words:
                    wu = w.upper()
                    if wu != w:
                        file_up += 1
                    # Remove if invalid anagram (uses letters not in base)
                    if not can_spell(wu, base_counter):
                        file_rm += 1
                        continue
                    # Remove if has spaces or non-alpha
                    if ' ' in wu or not wu.replace('-', '').isalpha():
                        file_rm += 1
                        continue
                    # Remove duplicates (keep first occurrence)
                    if wu not in new_words:
                        new_words.append(wu)
                    else:
                        file_rm += 1  # duplicate
                vw[lang] = new_words
        elif isinstance(vw, list):
            new_words = []
            for w in vw:
                wu = w.upper()
                if wu != w:
                    file_up += 1
                if not can_spell(wu, base_counter):
                    file_rm += 1
                    continue
                if ' ' in wu or not wu.replace('-', '').isalpha():
                    file_rm += 1
                    continue
                if wu not in new_words:
                    new_words.append(wu)
                else:
                    file_rm += 1
            block['validWords'] = new_words

    with open(path, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)

    print(f"  [OK] {fn}: {file_up} uppercased, {file_rm} invalid/duplicate removed")
    total_uppercased += file_up
    total_removed    += file_rm

print(f"  [OK] Fix 2+3 total: {total_uppercased} words uppercased, {total_removed} removed")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 4: Add q.ans guard in render() feedback — show "[unbekannt]" if ans undefined
# (prevents empty "✗ Falsch → " with blank correct answer)
# ══════════════════════════════════════════════════════════════════════════════
with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

OLD = (
    'if(S.ph==="feedback"){const cls=ok?"fb ok":"fb ng";let al=q.ans;'
    'if(q.type==="flagsel"){'
)
NEW = (
    'if(S.ph==="feedback"){const cls=ok?"fb ok":"fb ng";let al=q.ans!=null?q.ans:"?";'
    'if(q.type==="flagsel"){'
)

count = c.count(OLD)
assert count == 1, f"Anchor not unique: feedback ans guard (found {count})"
c = c.replace(OLD, NEW)
print("  [OK] Fix 4: feedback banner uses '?' fallback if q.ans is undefined")

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)
print("  [OK] gen.py updated")
