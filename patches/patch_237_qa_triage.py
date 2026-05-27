"""
patch_237_qa_triage.py
======================
Phase 237 — QA & Engine Hardening Sprint

Fix 1: _mkMatchQ in gen.py — remove padding loop that duplicates buttons
        when a dataset has <3 unique distractor categories (e.g. Ja/Nein).
        The `while(pool.length<3)` loop is replaced by nothing;
        the render engine already handles 2-button choices fine.

Fix 2: emob_match.json port_position — n and c are swapped.
        n must be the vehicle name (subject), c the port position (category).
        Position labels are normalised by stripping parenthetical qualifiers.

Fix 3: archaeologie_hl.json — rename second occurrences of duplicate names
        "Great Zimbabwe"  →  "Great Zimbabwe (Kernbereich)"
        "Tempel I Tikal"  →  "Tempel I Tikal (Pyramide)"
        so their dedup lids no longer collide.

Fix 4: validate_content.py — raise extreme-value-ratio threshold from
        1 000× to 10 000 000× so legitimate biological/geological ranges
        (Blauwal vs. Seepferd, Nano vs. Megalith) stop generating noise.
"""
import os, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN  = os.path.join(ROOT, 'gen.py')
DATA = os.path.join(ROOT, 'data')
VAL  = os.path.join(ROOT, 'validate_content.py')

# ══════════════════════════════════════════════════════════════════════════════
# FIX 1  — _mkMatchQ engine: drop duplicate-padding while-loop
# ══════════════════════════════════════════════════════════════════════════════
with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

OLD_ENGINE = (
    '      var pool=items.map(function(x){return x.c;}).filter(function(c){return c!==correct.c;});\n'
    '      var seen=new Set();\n'
    '      pool=pool.filter(function(c){if(seen.has(c))return false;seen.add(c);return true;});\n'
    '      while(pool.length<3)pool.push(pool[~~(rng()*pool.length)]||correct.c);\n'
    '      pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);\n'
    '      opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});'
)
NEW_ENGINE = (
    '      var pool=items.map(function(x){return x.c;}).filter(function(c){return c!==correct.c;});\n'
    '      var seen=new Set();\n'
    '      pool=pool.filter(function(c){if(seen.has(c))return false;seen.add(c);return true;});\n'
    '      /* Phase 237: no padding — allow 1-2 distractors for binary/ternary datasets */\n'
    '      pool=pool.sort(function(){return rng()-0.5;}).slice(0,3);\n'
    '      opts=[correct.c].concat(pool).sort(function(){return rng()-0.5;});'
)

count = c.count(OLD_ENGINE)
assert count == 1, f"Anchor not unique: _mkMatchQ pool (found {count})"
c = c.replace(OLD_ENGINE, NEW_ENGINE)

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

print("  [OK] Fix 1: _mkMatchQ padding while-loop removed from gen.py")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 2  — emob_match.json port_position: swap n↔c, normalise positions
# ══════════════════════════════════════════════════════════════════════════════
EMOB_MATCH = os.path.join(DATA, 'emob_match.json')

with open(EMOB_MATCH, 'r', encoding='utf-8') as fh:
    emob = json.load(fh)

pp = emob.get('port_position', {})
items = pp.get('items', [])

def normalise_position(pos: str) -> str:
    """Strip parenthetical qualifiers: 'Hinten Links (Fahrerseite)' → 'Hinten Links'."""
    return re.sub(r'\s*\(.*?\)', '', pos).strip()

new_items = []
for item in items:
    # Current state: n = position label, c = vehicle name  (swapped!)
    vehicle  = item['c']
    position = normalise_position(item['n'])
    # Also strip trailing suffix for NIO entry
    vehicle = vehicle.replace(' (Swap-Port)', '').strip()
    new_items.append({'n': vehicle, 'c': position})

pp['items'] = new_items
emob['port_position'] = pp

with open(EMOB_MATCH, 'w', encoding='utf-8') as fh:
    json.dump(emob, fh, ensure_ascii=False, indent=2)

# Report unique categories after fix
cats = set(it['c'] for it in new_items)
print(f"  [OK] Fix 2: emob_match.json port_position — swapped n↔c, {len(new_items)} items, {len(cats)} unique categories: {sorted(cats)}")

# ══════════════════════════════════════════════════════════════════════════════
# FIX 3  — archaeologie_hl.json: rename second occurrences of duplicate names
# ══════════════════════════════════════════════════════════════════════════════
ARCH_HL = os.path.join(DATA, 'archaeologie_hl.json')

with open(ARCH_HL, 'r', encoding='utf-8') as fh:
    arch = json.load(fh)

renames = {
    'groesse_ruinen': ('Great Zimbabwe',  'Great Zimbabwe (Kernbereich)'),
    'hoehe_bauwerke': ('Tempel I Tikal',  'Tempel I Tikal (Pyramide)'),
}

for section, (original, replacement) in renames.items():
    block = arch.get(section, {})
    items = block.get('items', [])
    first_seen = False
    renamed = 0
    for item in items:
        if item.get('name') == original:
            if first_seen:
                item['name'] = replacement
                renamed += 1
            else:
                first_seen = True
    print(f"  [OK] Fix 3: archaeologie_hl.json › {section}: '{original}' → '{replacement}' ({renamed} renamed)")

with open(ARCH_HL, 'w', encoding='utf-8') as fh:
    json.dump(arch, fh, ensure_ascii=False, indent=2)

# ══════════════════════════════════════════════════════════════════════════════
# FIX 4  — validate_content.py: raise extreme-value-ratio threshold
# ══════════════════════════════════════════════════════════════════════════════
with open(VAL, 'r', encoding='utf-8') as fh:
    v = fh.read()

OLD_RATIO = 'if min_v > 0 and max_v > min_v * 1000:'
NEW_RATIO = 'if min_v > 0 and max_v > min_v * 10_000_000:  # Phase 237: raised for biological/geological ranges'

count = v.count(OLD_RATIO)
assert count == 1, f"Anchor not unique: ratio threshold (found {count})"
v = v.replace(OLD_RATIO, NEW_RATIO)

with open(VAL, 'w', encoding='utf-8') as fh:
    fh.write(v)

print("  [OK] Fix 4: validate_content.py extreme-value threshold raised 1 000× → 10 000 000×")
print()
print("  All Phase 237 fixes applied. Run: python gen.py && python verify.py")
