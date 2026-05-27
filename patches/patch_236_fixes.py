"""
patch_236_fixes.py
==================
Fix 1: Remove duplicate subjects in archaeologie_match.json (keep first occurrence per `n` value)
Fix 2: Fix validate_content.py false positives for kultur.json
         — detect item type by lat/lng vs c field presence
"""
import os, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ══════════════════════════════════════════════════════════════════════════════
# FIX 1: Deduplicate archaeologie_match.json items by `n` field
# ══════════════════════════════════════════════════════════════════════════════
ARCH_MATCH = os.path.join(ROOT, 'data', 'archaeologie_match.json')

with open(ARCH_MATCH, 'r', encoding='utf-8') as fh:
    data = json.load(fh)

total_removed = 0
for key, block in data.items():
    items = block.get('items', []) if isinstance(block, dict) else []
    seen = set()
    new_items = []
    removed = 0
    for item in items:
        n = item.get('n', '')
        if n in seen:
            removed += 1
        else:
            seen.add(n)
            new_items.append(item)
    if removed:
        block['items'] = new_items
        print(f"  [OK] archaeologie_match.json › {key}: {removed} duplicate(s) removed")
        total_removed += removed

with open(ARCH_MATCH, 'w', encoding='utf-8') as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)

print(f"  [OK] Fix 1: {total_removed} total duplicates removed from archaeologie_match.json")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 2: Fix validate_content.py — kultur.json pin/match detection
# In the detect_and_check() function, the dispatch for kultur.json checks
# `items[0]` for `"val"` (HL) or `"c"` (match), but does not check for
# `"lat"` / `"lng"` (pin). This means pin data is routed to check_match()
# and flagged as missing required `c` field.
# Fix: Add lat/lng detection in the kultur.json branch.
# ══════════════════════════════════════════════════════════════════════════════
VALIDATOR = os.path.join(ROOT, 'validate_content.py')

with open(VALIDATOR, 'r', encoding='utf-8') as fh:
    c = fh.read()

OLD = (
    '        for key, block in obj_keys.items():\n'
    '                items = block.get("items", [])\n'
    '                if items and "val" in items[0]:\n'
    '                    check_hl(filename, {key: block})\n'
    '                elif items and "c" in items[0]:\n'
    '                    check_match(filename, {key: block})'
)
NEW = (
    '        for key, block in obj_keys.items():\n'
    '                items = block.get("items", [])\n'
    '                if items and "val" in items[0]:\n'
    '                    check_hl(filename, {key: block})\n'
    '                elif items and ("lat" in items[0] or "lng" in items[0]):\n'
    '                    check_pin(filename, {key: block})\n'
    '                elif items and "c" in items[0]:\n'
    '                    check_match(filename, {key: block})'
)

count = c.count(OLD)
assert count == 1, f"Anchor not unique: kultur.json dispatch (found {count})"
c = c.replace(OLD, NEW)

with open(VALIDATOR, 'w', encoding='utf-8') as fh:
    fh.write(c)

print("  [OK] Fix 2: validate_content.py kultur.json dispatch now detects pin items (lat/lng check)")
print("  [OK] validate_content.py updated")
