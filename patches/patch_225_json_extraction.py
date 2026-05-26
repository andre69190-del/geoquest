#!/usr/bin/env python3
"""
Phase 225 — Data-Logic Separation
Extracts the 4 giant JS data objects from gen.py into data/*.json,
then patches gen.py to load and inject them via the existing PLACEHOLDER pattern.

Run from the GeoQuest project directory:
    python3 phase225_extract.py
"""
import re, json, os, subprocess, sys

GEN      = 'gen.py'
DATA_DIR = 'data'
os.makedirs(DATA_DIR, exist_ok=True)

with open(GEN, 'r', encoding='utf-8') as f:
    c = f.read()

orig_len = len(c)
print(f"gen.py loaded: {orig_len:,} chars\n")

# ──────────────────────────────────────────────────────────────
# 1. Brace-counting extractor
# ──────────────────────────────────────────────────────────────
def extract_object_bounds(text, const_name):
    """
    Finds 'const NAME={' in text, then walks forward counting braces
    to locate the matching closing '}', then the trailing ';'.
    Returns (start_idx, end_idx) of the whole 'const NAME={...};' span.
    """
    marker = f'const {const_name}={{'
    idx = text.find(marker)
    if idx == -1:
        raise ValueError(f"Marker not found: const {const_name}={{")
    # The '{' we need is the last char of marker
    brace_pos = idx + len(marker) - 1
    depth = 0
    i = brace_pos
    while i < len(text):
        ch = text[i]
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                # Skip optional whitespace then ';'
                end = i + 1
                while end < len(text) and text[end] in ' \t\n':
                    end += 1
                if end < len(text) and text[end] == ';':
                    end += 1   # include the semicolon
                return idx, end
        i += 1
    raise ValueError(f"Unmatched brace for const {const_name}")

# ──────────────────────────────────────────────────────────────
# 2. Extract each block → JSON file
# ──────────────────────────────────────────────────────────────
BLOCKS = [
    ('TIER_WS_DATA',    'tiere_ws.json'),
    ('KULTUR_DATA',     'kultur.json'),
    ('TIER_HL_DATA',    'tiere_hl.json'),
    ('TIER_MATCH_DATA', 'tiere_match.json'),
]

block_info = {}   # name → (start, end)

for const_name, json_file in BLOCKS:
    print(f"Extracting {const_name}...")
    start, end = extract_object_bounds(c, const_name)
    raw_block   = c[start:end]   # "const NAME={...};"
    # Object literal: strip "const NAME=" prefix and trailing ";"
    obj_literal = raw_block[len(f'const {const_name}='):-1].strip()
    print(f"  Span: chars {start:,} – {end:,}  ({end-start:,} chars)")

    # Write object literal to a temp .js file for Node.js to parse
    tmp_js = f'/tmp/gq_{const_name}.js'
    with open(tmp_js, 'w', encoding='utf-8') as f:
        # Strip JS block comments before eval to avoid /* ... */ inside strings
        # (Node handles them fine in code execution anyway)
        f.write(f"var _x = {obj_literal};\n"
                f"process.stdout.write(JSON.stringify(_x, null, 2));\n")

    result = subprocess.run(
        ['node', tmp_js],
        capture_output=True, text=True, encoding='utf-8'
    )
    if result.returncode != 0:
        print(f"  ✗ Node.js error:\n{result.stderr[:800]}")
        sys.exit(1)

    json_str = result.stdout
    # Validate round-trip
    try:
        json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"  ✗ JSON validation failed: {e}")
        sys.exit(1)

    out_path = os.path.join(DATA_DIR, json_file)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(json_str)
    print(f"  ✓ Saved {out_path}  ({len(json_str):,} chars)")

    block_info[const_name] = (start, end)

print()

# ──────────────────────────────────────────────────────────────
# 3. Patch gen.py — replace each block with a PLACEHOLDER line
#    Process in REVERSE order so earlier indices stay valid
# ──────────────────────────────────────────────────────────────
print("Patching gen.py — replacing data blocks with PLACEHOLDERs...")

# Sort by start position, descending
for const_name, _ in sorted(BLOCKS, key=lambda t: block_info[t[0]][0], reverse=True):
    start, end = block_info[const_name]
    placeholder_line = f'const {const_name}=PLACEHOLDER_{const_name};'
    c = c[:start] + placeholder_line + c[end:]
    print(f"  Replaced {const_name} ({end-start:,} chars → {len(placeholder_line)} chars)")

# ──────────────────────────────────────────────────────────────
# 4. Add JSON-loading Python code after the CJ = json.dumps line
# ──────────────────────────────────────────────────────────────
load_lines = [
    "",
    "# ─── DATA JSON FILES ─── Phase 225: Data-Logic Separation ───────────────────",
]
for const_name, json_file in BLOCKS:
    varname = const_name + '_J'
    load_lines.append(
        f"with open(os.path.join(os.path.dirname(__file__), 'data/{json_file}'), "
        f"'r', encoding='utf-8') as _f: {varname} = _f.read()"
    )
load_lines.append("")
load_block = "\n".join(load_lines) + "\n"

anchor_cj = "CJ = json.dumps(cities_slim, separators=(',',':'), ensure_ascii=False)\n"
assert c.count(anchor_cj) == 1, f"Anchor not unique: {anchor_cj!r}"
c = c.replace(anchor_cj, anchor_cj + load_block, 1)
print("\n  Added JSON-loading block after CJ assignment")

# ──────────────────────────────────────────────────────────────
# 5. Extend the PLACEHOLDER .replace() chain
# ──────────────────────────────────────────────────────────────
chain_end = "  .replace('PLACEHOLDER_SPORTPOI', SPORT_POI_J)\n)"
assert c.count(chain_end) == 1, f"Chain-end anchor not unique!"

extra_replaces = ""
for const_name, _ in BLOCKS:
    varname = const_name + '_J'
    extra_replaces += f"\n  .replace('PLACEHOLDER_{const_name}', {varname})"

new_chain_end = f"  .replace('PLACEHOLDER_SPORTPOI', SPORT_POI_J){extra_replaces}\n)"
c = c.replace(chain_end, new_chain_end, 1)
print("  Extended PLACEHOLDER .replace() chain")

# ──────────────────────────────────────────────────────────────
# 6. Write patched gen.py
# ──────────────────────────────────────────────────────────────
with open(GEN, 'w', encoding='utf-8') as f:
    f.write(c)

print(f"\ngen.py: {orig_len:,} → {len(c):,} chars  (Δ {len(c)-orig_len:+,})")
print(f"\nCreated files:")
for _, json_file in BLOCKS:
    path = os.path.join(DATA_DIR, json_file)
    print(f"  {path}  ({os.path.getsize(path):,} bytes)")

print("\n✓ Phase 225 extraction complete. Run: python3 gen.py")
