# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
GeoQuest -- Post-Build Integration Selftest  (Phase 225 / Suggestion 3)

Run after every build to catch structural regressions before git push:
    python3 verify.py

Exit 0 = all tests passed.  Exit 1 = one or more failures.

Integrate into unlock_and_push.bat:
    python3 verify.py || (echo VERIFY FAILED && pause && exit /b 1)
"""
import re, json, os, subprocess, sys, tempfile

HTML_FILE = 'GeoQuest.html'
GEN_FILE  = 'gen.py'
DATA_DIR  = 'data'

PASS_LIST = []
FAIL_LIST = []

def ok(msg):
    PASS_LIST.append(msg)
    print("  [OK] " + msg)

def fail(msg):
    FAIL_LIST.append(msg)
    print("  [!!] " + msg)

def section(title):
    pad = '-' * (52 - len(title))
    print("\n-- " + title + " " + pad)

# =============================================================
print("=" * 58)
print(" GeoQuest Build Selftest")
print("=" * 58)

# -- 0. File presence -----------------------------------------
section("0. File presence")
for path in [HTML_FILE, GEN_FILE,
             DATA_DIR + '/kultur.json',
             DATA_DIR + '/tiere_hl.json',
             DATA_DIR + '/tiere_match.json',
             DATA_DIR + '/tiere_ws.json']:
    if os.path.isfile(path):
        ok(path + " exists (" + str(os.path.getsize(path)) + " bytes)")
    else:
        fail(path + " MISSING")

# -- 1. HTML size sanity --------------------------------------
section("1. HTML size sanity")
if not os.path.isfile(HTML_FILE):
    fail("GeoQuest.html not found -- skipping remaining tests")
    sys.exit(1)

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

size = len(html)
if size >= 1_000_000:
    ok("HTML size " + str(size) + " chars (>=1 MB)")
else:
    fail("HTML suspiciously small: " + str(size) + " chars (expected >=1 MB)")

# -- 2. Extract JS --------------------------------------------
section("2. JS extraction")
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
js = '\n'.join(scripts)
if len(js) > 500_000:
    ok("JS extracted: " + str(len(js)) + " chars from " + str(len(scripts)) + " script blocks")
else:
    fail("JS too small: " + str(len(js)) + " chars")

# -- 3. JS syntax check ---------------------------------------
section("3. JS syntax (node --check)")
tmp_fd, tmp = tempfile.mkstemp(suffix='.js', prefix='gq_selftest_')
try:
    with os.fdopen(tmp_fd, 'w', encoding='utf-8') as f:
        f.write(js)
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
finally:
    try: os.remove(tmp)
    except: pass
if r.returncode == 0:
    ok("JS syntax valid")
else:
    fail("JS SYNTAX ERROR:\n      " + r.stderr.strip()[:400])

# -- 4. No unreplaced PLACEHOLDERs ---------------------------
section("4. Placeholder substitution")
orphans = sorted(set(re.findall(r'PLACEHOLDER_\w+', html)))
if not orphans:
    ok("No unreplaced PLACEHOLDERs")
else:
    for p in orphans:
        fail("Unreplaced: " + p)

# -- 5. Required JS data objects ------------------------------
section("5. Required JS data objects")
for name in ['KULTUR_DATA', 'TIER_WS_DATA', 'TIER_HL_DATA', 'TIER_MATCH_DATA',
             'WORTSCHMIEDE_DATA', 'MODES', 'MODE_CATS', 'GEN']:
    if 'const ' + name + '=' in js:
        ok(name + " present")
    else:
        fail(name + " MISSING from output")
# plates is lowercase in this codebase
if 'const plates=' in js or 'const PLATES=' in js:
    ok("plates/PLATES present")
else:
    fail("plates MISSING from output")

# -- 6. MODES count sanity ------------------------------------
section("6. MODES count sanity")
modes_block = re.search(r'const MODES=\[(.*?)\];', js, re.DOTALL)
if modes_block:
    ids_in_modes = re.findall(r'id:"([^"]+)"', modes_block.group(1))
    ok("MODES array: " + str(len(ids_in_modes)) + " entries")
    if len(ids_in_modes) < 200:
        fail("MODES suspiciously short: " + str(len(ids_in_modes)) + " (expected >=200)")
else:
    fail("Could not locate MODES array")

# -- 7. Key generator functions -------------------------------
section("7. Key generator functions")
generators = [
    'genUniversalPinQ',
    'genTiereMatchQ',
    'genTiereHL',
    'initTierWortSchmiede',
    'genHauptstadtDistanzQ',
    'getSmartMatch',
]
for fn in generators:
    if 'function ' + fn + '(' in js:
        ok(fn + "() defined")
    else:
        fail(fn + "() MISSING")

# -- 8. Anti-cheat: spoiler guard in uk_pin -------------------
section("8. Anti-cheat check")
if '_displaySubj' in js and 'subj:_displaySubj' in js:
    ok("uk_pin returns _displaySubj (spoiler-stripped) as subj")
else:
    fail("genUniversalPinQ spoiler-guard missing (_displaySubj)")

# -- 9. Mojibake scan -----------------------------------------
section("9. Encoding / mojibake")
# Known pre-existing legacy patterns (immutable or cosmetic display strings):
#   Â® in _GQ_SALT  -- MUST NOT change, would invalidate all user LocalStorage saves
#   Â² in km-squared display strings
#   Â¥ / Â£  in currency symbols
#   Â±  in algorithm comments
KNOWN_LEGACY_PFX = {'Â®', 'Â²', 'Â¥', 'Â£', 'Â±'}
bad_all  = re.findall(r'[ÃÂ][^\s,;:"\'\]})]{1,3}', js)
bad_new  = [b for b in bad_all if b[:2] not in KNOWN_LEGACY_PFX]
known_cnt = len(bad_all) - len(bad_new)
if not bad_new:
    ok("No new mojibake (" + str(known_cnt) + " known-legacy patterns whitelisted)")
else:
    fail("NEW mojibake patterns: " + str(list(set(bad_new))[:8]))

# -- 10. JSON data files round-trip ---------------------------
section("10. JSON data files validity")
for fname in [
        'kultur.json', 'tiere_hl.json', 'tiere_match.json', 'tiere_ws.json',
        'pflanzen_pin.json', 'pflanzen_hl.json', 'pflanzen_match.json', 'pflanzen_ws.json',
        'gastro_pin.json', 'gastro_hl.json', 'gastro_match.json', 'gastro_ws.json',
        'tech_pin.json', 'tech_hl.json', 'tech_match.json', 'tech_ws.json',
        'emob_pin.json', 'emob_hl.json', 'emob_match.json', 'emob_ws.json',
        'archaeologie_pin.json', 'archaeologie_hl.json', 'archaeologie_match.json', 'archaeologie_ws.json',
    ]:
    path = os.path.join(DATA_DIR, fname)
    if not os.path.isfile(path):
        fail(path + " missing")
        continue
    try:
        with open(path, 'r', encoding='utf-8') as f:
            d = json.load(f)
        keys = list(d.keys()) if isinstance(d, dict) else []
        ok(fname + ": valid JSON, " + str(len(keys)) + " top-level keys")
    except Exception as e:
        fail(fname + ": " + str(e))

# -- 11. _GQ_SALT present -------------------------------------
section("11. Security -- _GQ_SALT present")
if '_GQ_SALT' in html:
    ok("_GQ_SALT present in output")
else:
    fail("_GQ_SALT not found -- LocalStorage saves may be invalidated!")

# =============================================================
print("\n" + "=" * 58)
total = len(PASS_LIST) + len(FAIL_LIST)
print(" Results: " + str(len(PASS_LIST)) + "/" + str(total) + " passed  |  " + str(len(FAIL_LIST)) + " failed")
print("=" * 58)

if FAIL_LIST:
    print("\nFAILURES:")
    for f in FAIL_LIST:
        print("  [!!] " + f)
    sys.exit(1)
else:
    print("\nALL TESTS PASSED -- build is production-ready.")
    sys.exit(0)
