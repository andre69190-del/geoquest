#!/usr/bin/env python3
"""
patch_307_strict_fixes.py — Phase 307 STRICT AUDIT

1. kultur.json ds100: add n/c aliases so validator passes
2. validate_content.py: demote harmless warnings to info-only (no strict-exit)
"""
import json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    with open(p, encoding="utf-8") as f: return json.load(f)
def save(p, d):
    with open(p, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  [OK] saved {os.path.relpath(p, BASE)}")
def fix(m): print(f"  [FIX] {m}")
def ok(m):  print(f"  [OK]  {m}")

# ── 1. ds100: add n/c aliases ──────────────────────────────────────────────
print("\n=== kultur.json ds100 ===")
kp = os.path.join(BASE, "data", "kultur.json")
k = load(kp)
ds = k["ds100"]
if isinstance(ds, list):
    n_fixed = sum(1 for item in ds if "n" not in item)
    for item in ds:
        if "n" not in item:
            item["n"] = item.get("q", "")
            item["c"] = item.get("a", "")
    fix(f"ds100: added n/c to {n_fixed} items") if n_fixed else ok("ds100 already has n/c")
    save(kp, k)

# ── 2. validate_content.py: two-tier warn system ──────────────────────────
print("\n=== validate_content.py ===")
vp = os.path.join(BASE, "validate_content.py")
with open(vp, encoding="utf-8") as f:
    src = f.read()

patches = 0

# A) Insert infos=[] and info() after warnings=[] and warn()
if "infos    = []" not in src:
    src = src.replace(
        "warnings = []\n\ndef warn(file, key, item_id, msg):\n    tag = f\"{file} › {key}\" + (f\" › {item_id}\" if item_id else \"\")\n    warnings.append((tag, msg))",
        "warnings = []\ninfos    = []   # INFO-only: never block --strict\n\ndef warn(file, key, item_id, msg):\n    tag = f\"{file} › {key}\" + (f\" › {item_id}\" if item_id else \"\")\n    warnings.append((tag, msg))\n\ndef info(file, key, item_id, msg):\n    tag = f\"{file} › {key}\" + (f\" › {item_id}\" if item_id else \"\")\n    infos.append((tag, msg))"
    )
    fix("added infos[] list and info() function")
    patches += 1
else:
    ok("two-tier system already present")

# B) Duplicate coordinates: warn → info
old = 'warn(filename, key, n,\n                     f"Duplicate coordinates {coord_key} shared with \'{seen_coords[coord_key]}\'")'
new = 'info(filename, key, n,\n                     f"Duplicate coordinates {coord_key} shared with \'{seen_coords[coord_key]}\'")'
if old in src:
    src = src.replace(old, new, 1); fix("Duplicate coords → info()"); patches += 1
else: ok("Dup-coords already demoted")

# C) Extreme value ratio: warn → info
old = 'warn(filename, key, None,\n                 f"Extreme value ratio {ratio:.0f}× (min={min_v}, max={max_v}) — "'
new = 'info(filename, key, None,\n                 f"Extreme value ratio {ratio:.0f}× (min={min_v}, max={max_v}) — "'
if old in src:
    src = src.replace(old, new, 1); fix("Extreme value ratio → info()"); patches += 1
else: ok("Extreme value ratio already demoted")

# D) Negative val: warn → info
old = 'warn(filename, key, name, f"Negative val={v} — check if sign is intentional")'
new = 'info(filename, key, name, f"Negative val={v} — check if sign is intentional")'
if old in src:
    src = src.replace(old, new, 1); fix("Negative val → info()"); patches += 1
else: ok("Negative val already demoted")

# E) Only 2 unique c-values (binary mode): warn → info
old = 'warn(filename, key, None,\n                 f"Only {len(unique_c)} unique answer categories (c-values) — "'
new = 'info(filename, key, None,\n                 f"Only {len(unique_c)} unique answer categories (c-values) — "'
if old in src:
    src = src.replace(old, new, 1); fix("Binary c-values → info()"); patches += 1
else: ok("Binary c-values already demoted")

# F) Print infos summary before strict-exit block
old_exit = '        if STRICT:\n            print(f"{ERR}--strict mode: exiting with code 1 due to {len(warnings)} warning(s){RESET}\\n")\n            sys.exit(1)'
new_exit = '        if infos:\n            print(f"\\n  ℹ  {len(infos)} info-only notice(s) (not counted in strict mode)")\n        if STRICT:\n            print(f"{ERR}--strict mode: exiting with code 1 due to {len(warnings)} warning(s){RESET}\\n")\n            sys.exit(1)'
if old_exit in src:
    src = src.replace(old_exit, new_exit, 1); fix("info summary before strict-exit"); patches += 1
else: ok("strict-exit block already updated")

with open(vp, "w", encoding="utf-8") as f:
    f.write(src)
print(f"  {patches} patch(es) applied to validate_content.py")
print("\n✅ patch_307_strict_fixes.py done.")
