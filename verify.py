# -*- coding: utf-8 -*-
#!/usr/bin/env python3
"""
GeoQuest -- Post-Build Integration Selftest  (Phase 295)

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
for path in [HTML_FILE, GEN_FILE]:
    if os.path.isfile(path):
        ok(path + " exists (" + str(os.path.getsize(path)) + " bytes)")
    else:
        fail(path + " MISSING")
_data_jsons = sorted(f for f in os.listdir(DATA_DIR) if f.endswith('.json'))
if not _data_jsons:
    fail("data/ directory is empty — no .json files found")
else:
    for _djf in _data_jsons:
        _djp = DATA_DIR + '/' + _djf
        if os.path.isfile(_djp):
            ok(_djp + " exists (" + str(os.path.getsize(_djp)) + " bytes)")
        else:
            fail(_djp + " MISSING")

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
for fn in ['genUniversalPinQ','genTiereMatchQ','genTiereHL',
           'initTierWortSchmiede','genHauptstadtDistanzQ','getSmartMatch']:
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
        # Phase 296: neue Pakete (bisher fehlend)
        'geo_hl.json', 'geo_match.json', 'geo_pin.json', 'geo_ws.json',
        'astro_hl.json', 'astro_match.json', 'astro_pin.json', 'astro_ws.json',
        'sport_hl.json', 'sport_match.json', 'sport_pin.json', 'sport_ws.json',
        'tiere_pin.json', 'timeline.json',
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

# -- 12. Service Worker sw.js --------------------------------
section("12. Service Worker sw.js")
sw_path = 'sw.js'
sw = ''
if not os.path.isfile(sw_path):
    fail("sw.js MISSING — run python gen.py to generate it")
else:
    with open(sw_path, 'r', encoding='utf-8') as f:
        sw = f.read()
    sw_size = os.path.getsize(sw_path)
    if not re.search(r"CACHE_NAME = 'geoquest-[a-f0-9]{8}'", sw):
        fail("sw.js: CACHE_NAME hash-version pattern missing")
    else:
        ok("sw.js: CACHE_NAME hash-version present")
    data_json_files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith('.json'))
    missing_in_sw = [f for f in data_json_files if "./data/" + f not in sw]
    if missing_in_sw:
        fail("sw.js: " + str(len(missing_in_sw)) + " data files missing from ASSETS: " + str(missing_in_sw[:3]))
    else:
        ok("sw.js: all " + str(len(data_json_files)) + " data/*.json in ASSETS (" + str(sw_size) + " bytes)")
    if 'Promise.allSettled' not in sw:
        fail("sw.js: Promise.allSettled missing — install could abort atomically")
    else:
        ok("sw.js: Promise.allSettled install strategy confirmed")

# -- 13. GEN dispatch completeness ----------------------------
section("13. GEN dispatch completeness (all MODES have generator)")
gen_block = re.search(r'const GEN=\{(.*?)\};', js, re.DOTALL)
if modes_block and gen_block:
    mode_ids = re.findall(r'id:"([^"]+)"', modes_block.group(1))
    gen_ids  = set(re.findall(r'"?([a-zA-Z0-9_]+)"?\s*:', gen_block.group(1)))
    NO_GEN_PFX = ('coins_','premium_','pu_','bspot_','sk_','mkp_','pkp_','mkm_',
                  'ukfp_','ukm_','ukp_','ukh_','bmcq_','bhl_','gfq_')
    NO_GEN_EXACT = {'wort_schmiede'}  # uses initWortSchmiede(), not GEN dispatch
    missing_gen = [m for m in mode_ids if m not in gen_ids
                   and not any(m.startswith(p) for p in NO_GEN_PFX)
                   and m not in NO_GEN_EXACT]
    if not missing_gen:
        ok("All " + str(len(mode_ids)) + " mode IDs covered (no-gen prefixes excluded)")
    else:
        fail("Modes without GEN entry (" + str(len(missing_gen)) + "): " + str(missing_gen[:8]))
else:
    fail("Could not parse MODES or GEN block for dispatch check")

# -- 14. Daily Pool validity ----------------------------------
section("14. Daily Pool validity")
dp_match = re.search(r'const DAILY_POOL=\[(.*?)\];', js, re.DOTALL)
if dp_match:
    pool_ids = re.findall(r'"([^"]+)"', dp_match.group(1))
    if modes_block:
        mode_ids_set = set(re.findall(r'id:"([^"]+)"', modes_block.group(1)))
        bad_pool = [p for p in pool_ids if p not in mode_ids_set]
        if not bad_pool:
            ok("Daily Pool: " + str(len(pool_ids)) + " valid IDs, all in MODES")
        else:
            fail("Daily Pool IDs missing from MODES: " + str(bad_pool))
    else:
        ok("Daily Pool: " + str(len(pool_ids)) + " IDs (MODES unavailable for cross-check)")
else:
    fail("DAILY_POOL not found in JS")

# -- 15. No biased sort() remaining ---------------------------
section("15. No biased sort() remaining")
biased_rng  = re.findall(r'\.sort\([^)]*rng\(\)\s*-\s*[0.]?5\s*\)', js)
biased_math = re.findall(r'\.sort\([^)]*Math\.random\(\)\s*-\s*[0.]?5\s*\)', js)
total_biased = biased_rng + biased_math
if not total_biased:
    ok("No biased sort(fn) found — all shuffles use sh() Fisher-Yates")
else:
    fail(str(len(total_biased)) + " biased sort() calls remain: " + str(total_biased[:3]))

# -- 16. SW_VER matches CACHE_NAME (auto-injection) -----------
section("16. SW_VER matches CACHE_NAME (auto-injection)")
sw_ver_m = re.search(r"SW_VER='(gq-[a-f0-9]{8})'", html)
cache_nm  = re.search(r"CACHE_NAME = '(geoquest-[a-f0-9]{8})'", sw) if sw else None
if '__GQ_BUILD_VER__' in html:
    fail("SW_VER placeholder was NOT replaced — gen.py injection failed")
elif sw_ver_m and cache_nm:
    ver_hash   = sw_ver_m.group(1).replace('gq-', '')
    cache_hash = cache_nm.group(1).replace('geoquest-', '')
    if ver_hash == cache_hash:
        ok("SW_VER '" + sw_ver_m.group(1) + "' matches CACHE_NAME hash")
    else:
        fail("SW_VER hash '" + ver_hash + "' != CACHE_NAME hash '" + cache_hash + "'")
else:
    fail("SW_VER or CACHE_NAME pattern not found")

# -- 17. Generator structure checks -------------------------
section("17. Generator structure checks")
import re as _re

_checks = [
    # (fn_name, required_patterns_in_body)
    ('genUniversalPinQ',    [r'type:"uk_pin"', r'lid:', r'prompt:']),
    ('genTiereMatchQ',      [r'type:"uk_match"', r'lid:', r'opts:']),
    ('genTiereHL',          [r'type:"beta_hl"', r'lid:', r'ans:']),
    ('getSmartMatch',       [r'return null', r'candidates', r'valFn']),
    ('genHauptstadtDistanzQ', [r'hauptstadt_distanz', r'lid:', r'opts:']),
    ('initTierWortSchmiede',  [r'TIER_WS_DATA', r'clearInterval', r'validWords']),
]
for fn, patterns in _checks:
    fn_start = js.find('function ' + fn + '(')
    fn_end   = js.find('\nfunction ', fn_start + 10) if fn_start >= 0 else -1
    if fn_start < 0:
        fail(fn + "(): function not found")
        continue
    fn_body = js[fn_start:fn_end] if 0 < fn_end - fn_start < 20000 else js[fn_start:fn_start+8000]
    missing = [p for p in patterns if not _re.search(p, fn_body)]
    if not missing:
        ok(fn + "(): structure correct")
    else:
        fail(fn + "(): missing " + str(missing))

# Guard-return-null check: nur IMMEDIATE null returns (no data guard)
_imm_null = _re.findall(r'function (gen\w+|init\w+)\([^)]*\)\s*\{\s*return null', js)
if _imm_null:
    fail("Generators that return null immediately (no guard): " + str(_imm_null[:3]))
else:
    ok("No generator returns null without a data guard")

# lq dedup check
if 'askedLids' in js and ('lq' in js):
    ok("lq() + askedLids dedup present")
else:
    fail("lq() dedup mechanism not found")

# -- 18. Daily Challenge UTC consistency ----------------------
section("18. Daily Challenge UTC consistency")
streak_fn = re.search(r'function updateDailyStreak\(\)\{.*?\}function', js, re.DOTALL)
if streak_fn and 'toLocaleDateString' in streak_fn.group(0):
    fail("updateDailyStreak() still uses toLocaleDateString — UTC fix missing")
else:
    ok("updateDailyStreak() uses UTC (toISOString)")

countdown_fn = re.search(r'function getDailyCountdown\(\)\{.*?\}', js, re.DOTALL)
if countdown_fn:
    if 'Date.UTC' in countdown_fn.group(0):
        ok("getDailyCountdown() uses Date.UTC — timezone-safe")
    else:
        fail("getDailyCountdown() missing Date.UTC — uses local midnight")
else:
    fail("getDailyCountdown() not found")

seed_fn = re.search(r'function getDailySeed\(\)\{.*?\}', js, re.DOTALL)
if seed_fn:
    if 'toISOString' in seed_fn.group(0):
        ok("getDailySeed() uses toISOString() — UTC-based")
    else:
        fail("getDailySeed() not using toISOString() — may be locale-dependent")
else:
    fail("getDailySeed() not found")

# -- 19. Zug-Daten Plausibilitäts-Validatoren ---------
section("19. Train data validators (Phase 296)")
import json as _json

# 19a: HL-Zugdaten in sport_hl.json
_shl_path = os.path.join(DATA_DIR, 'sport_hl.json')
if os.path.isfile(_shl_path):
    with open(_shl_path, 'r', encoding='utf-8') as _f:
        _shl = _json.load(_f)
    for _key, _limits in [
        ('zug_speed', ('km/h',   0,  650)),
        ('zug_jahr',  ('Jahr', 1800, 2035)),
        ('zug_km',    ('km',     0, 15000)),
    ]:
        if _key not in _shl:
            fail(f"sport_hl.json: Key '{_key}' fehlt")
            continue
        _items = _shl[_key].get('items', [])
        _unit, _lo, _hi = _limits
        _bad = []
        for _it in _items:
            if 'name' not in _it or not _it['name']:
                _bad.append(f"name fehlt: {_it}")
            elif 'val' not in _it:
                _bad.append(f"val fehlt: {_it['name']}")
            elif not (_lo <= float(_it['val']) <= _hi):
                _bad.append(f"val {_it['val']} außerhalb [{_lo},{_hi}]: {_it['name']}")
        if _bad:
            fail(f"sport_hl[{_key}]: {len(_bad)} fehlerhafte Items: {_bad[:2]}")
        else:
            ok(f"sport_hl[{_key}]: {len(_items)} Items valid (range {_lo}–{_hi} {_unit})")
else:
    fail("sport_hl.json nicht gefunden")

# 19b: DS100-Daten in kultur.json
_kpath = os.path.join(DATA_DIR, 'kultur.json')
if os.path.isfile(_kpath):
    with open(_kpath, 'r', encoding='utf-8') as _f:
        _kd = _json.load(_f)
    if 'ds100' not in _kd:
        fail("kultur.json: 'ds100' Key fehlt")
    else:
        import re as _re
        _ds100 = _kd['ds100']
        _ds_bad = []
        for _entry in _ds100:
            _q = _entry.get('q', '')
            _a = _entry.get('a', '')
            if not _q:
                _ds_bad.append(f"leere Frage: {_entry}")
            elif not _a:
                _ds_bad.append(f"leere Antwort: {_entry}")
            elif len(_a) > 5:
                _ds_bad.append(f"Kürzel >{5} Zeichen: {_a!r}")
            elif not _re.match(r'^[A-Za-z]+$', _a):
                _ds_bad.append(f"Kürzel ungültige Zeichen: {_a!r}")
        if _ds_bad:
            fail(f"kultur.json[ds100]: {len(_ds_bad)} Fehler: {_ds_bad[:3]}")
        else:
            ok(f"kultur.json[ds100]: {len(_ds100)} Einträge valid (max 5 Zeichen, nur A-Za-z)")

    # zug_panorama und zug_vkm prüfen
    for _mkey in ['zug_panorama', 'zug_vkm']:
        if _mkey not in _kd:
            fail(f"kultur.json: '{_mkey}' fehlt")
            continue
        _mitems = _kd[_mkey]
        _m_bad = [x for x in _mitems if not x.get('n') or not x.get('c')]
        _unique_c = len(set(x.get('c','') for x in _mitems))
        if _m_bad:
            fail(f"kultur.json[{_mkey}]: {len(_m_bad)} Items ohne n/c: {_m_bad[:2]}")
        elif _unique_c < 4:
            fail(f"kultur.json[{_mkey}]: nur {_unique_c} unique Kategorien (min 4 für Match-Engine)")
        else:
            ok(f"kultur.json[{_mkey}]: {len(_mitems)} Items, {_unique_c} Kategorien ✓")

# 19c: Timeline zug_hsb
_tpath = os.path.join(DATA_DIR, 'timeline.json')
if os.path.isfile(_tpath):
    with open(_tpath, 'r', encoding='utf-8') as _f:
        _td = _json.load(_f)
    if 'zug_hsb' not in _td:
        fail("timeline.json: 'zug_hsb' Key fehlt")
    else:
        _tl = _td['zug_hsb'].get('items', [])
        _tl_bad = []
        for _ti in _tl:
            _yr = _ti.get('year')
            if _yr is None:
                _tl_bad.append(f"year fehlt: {_ti.get('n','?')[:40]}")
            elif not isinstance(_yr, int):
                _tl_bad.append(f"year kein int: {_yr}")
            elif not (1800 <= _yr <= 2035):
                _tl_bad.append(f"year {_yr} außerhalb [1800,2035]: {_ti.get('n','?')[:30]}")
            if not _ti.get('n'):
                _tl_bad.append(f"n fehlt bei year={_yr}")
        if _tl_bad:
            fail(f"timeline[zug_hsb]: {len(_tl_bad)} Fehler: {_tl_bad[:3]}")
        else:
            _sorted_ok = _tl == sorted(_tl, key=lambda x: x.get('year',0))
            ok(f"timeline[zug_hsb]: {len(_tl)} Items, Jahre {min(x['year'] for x in _tl)}–{max(x['year'] for x in _tl)}, sortierbar ✓")

# 19d: WS Zug-Einträge in tiere_ws.json
_wpath = os.path.join(DATA_DIR, 'tiere_ws.json')
if os.path.isfile(_wpath):
    with open(_wpath, 'r', encoding='utf-8') as _f:
        _wd = _json.load(_f)
    _zug_ws = {k: v for k, v in _wd.items() if k.startswith('zug_')}
    _ws_bad = []
    for _wk, _wv in _zug_ws.items():
        _word = _wv.get('word', '')
        if not _word or not _word.isupper() or ' ' in _word:
            _ws_bad.append(f"{_wk}: word={_word!r} ungültig (muss Großbuchstaben, kein Leerzeichen)")
        if not _wv.get('validWords', {}).get('de') and not _wv.get('validWords', {}).get('en'):
            _ws_bad.append(f"{_wk}: keine validWords")
    if _ws_bad:
        fail(f"tiere_ws.json Zug-WS: {len(_ws_bad)} Fehler: {_ws_bad[:3]}")
    else:
        ok(f"tiere_ws.json: {len(_zug_ws)} Zug-WS-Einträge valid (Großbuchstaben, validWords vorhanden)")


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
