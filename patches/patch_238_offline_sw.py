"""
Phase: 238
Date:  2026-05-27
Author: Architect
Scope: PWA Service Worker — full offline support via external sw.js

Description:
  Fix 1: Replace blob-based inline SW (Phase 221, cache=gq-v10) with
          navigator.serviceWorker.register('./sw.js') in gen.py JS block.
          Blob SW could not cache cross-origin data/*.json files; external
          sw.js has full origin access.

  Fix 2: Inject sw.js generator into gen.py Python build step.
          - Dynamically lists all data/*.json (sorted, deterministic)
          - Hash-versioned CACHE_NAME (geoquest-<md5[:8]>) — auto-busts on change
          - Promise.allSettled per asset — non-atomic, one 404 won't abort install
          - Network-first for Supabase; Cache-first for everything else
          - Offline fallback: returns cached GeoQuest.html
          - cities_data.js (3.8 MB) excluded from ASSETS — lazy-cached by fetch handler

  Fix 3: Inject manifest.json generator into gen.py Python build step.
          - theme_color synced to CSS --accent: #10b981 (was #3b82f6 blue)
          - icons: icon.svg only (icon-192.png / icon-512.png don't exist)

  Fix 4: Add verify.py section 12 — sw.js existence and content validation:
          - File exists
          - CACHE_NAME matches hash-version pattern geoquest-[a-f0-9]{8}
          - All 24 data/*.json files listed in ASSETS
          - Promise.allSettled strategy present
"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GEN    = os.path.join(ROOT, 'gen.py')
VERIFY = os.path.join(ROOT, 'verify.py')

# ── Read gen.py ────────────────────────────────────────────────────────────────
with open(GEN, 'r', encoding='utf-8') as fh:
    c = fh.read()

# ==============================================================================
# FIX 1 — Replace blob SW try-catch with external ./sw.js registration
# ==============================================================================
# Unique anchor confirmed: r'  try\{\n    const swSrc.*?  \}catch\(e\)\{\}' → 1 match
old_blob_re = re.compile(r'  try\{\n    const swSrc.*?  \}catch\(e\)\{\}', re.DOTALL)

found = old_blob_re.findall(c)
assert len(found) == 1, f'SW blob anchor not unique (found {len(found)})'

new_register = (
    '  try{\n'
    "    navigator.serviceWorker.register('./sw.js').catch(function(){});\n"
    '  }catch(e){}'
)

c = old_blob_re.sub(new_register, c, count=1)
print('  [OK] Fix 1: Blob SW (gq-v10) replaced with register(\'./sw.js\')')

# ==============================================================================
# FIX 2+3 — Inject sw.js + manifest.json generators before GeoQuest.html write
# ==============================================================================
OLD_BUILD = "with open(out, 'w', encoding='utf-8') as _f:"
assert c.count(OLD_BUILD) == 1, f'Build trigger anchor not unique (found {c.count(OLD_BUILD)})'

# NOTE on escaping in the block string below:
#   \\n  →  \n written to gen.py  →  newline char in SW output at build time
#   '...' inner strings avoid collision with the outer """ triple-quote
GENERATORS = """\
# ── Phase 238: Generate sw.js (hash-versioned, all data/*.json) ────────────────────
import hashlib as _hashlib
_data_files = sorted('./data/' + f for f in _os.listdir('data') if f.endswith('.json'))
_cache_assets = ['./GeoQuest.html', './index.html', './manifest.json', './icon.svg'] + _data_files
_cache_hash = _hashlib.md5(''.join(_cache_assets).encode()).hexdigest()[:8]
_cache_name = 'geoquest-' + _cache_hash
_assets_js = ',\\n  '.join("'" + a + "'" for a in _cache_assets)
_sw_content = (
    "const CACHE_NAME = '" + _cache_name + "';\\n"
    "/* Phase 238: full offline cache — auto-versioned from asset hash */\\n"
    "const ASSETS = [\\n  " + _assets_js + "\\n];\\n\\n"
    "self.addEventListener('install', function(e) {\\n"
    "  e.waitUntil(\\n"
    "    caches.open(CACHE_NAME).then(function(cache) {\\n"
    "      return Promise.allSettled(\\n"
    "        ASSETS.map(function(url) {\\n"
    "          return cache.add(url).catch(function(err) {\\n"
    "            console.warn('SW: skipped', url, err);\\n"
    "          });\\n"
    "        })\\n"
    "      );\\n"
    "    }).then(function() { return self.skipWaiting(); })\\n"
    "  );\\n"
    "});\\n\\n"
    "self.addEventListener('activate', function(e) {\\n"
    "  e.waitUntil(\\n"
    "    caches.keys().then(function(keys) {\\n"
    "      return Promise.all(\\n"
    "        keys.filter(function(k) { return k !== CACHE_NAME; })\\n"
    "            .map(function(k) { return caches.delete(k); })\\n"
    "      );\\n"
    "    }).then(function() { return self.clients.claim(); })\\n"
    "  );\\n"
    "});\\n\\n"
    "self.addEventListener('fetch', function(e) {\\n"
    "  if (e.request.url.includes('supabase.co')) {\\n"
    "    e.respondWith(fetch(e.request).catch(function() {\\n"
    "      return new Response('', {status: 503});\\n"
    "    }));\\n"
    "    return;\\n"
    "  }\\n"
    "  e.respondWith(\\n"
    "    caches.match(e.request).then(function(cached) {\\n"
    "      if (cached) return cached;\\n"
    "      return fetch(e.request).then(function(response) {\\n"
    "        if (!response || response.status !== 200) return response;\\n"
    "        var clone = response.clone();\\n"
    "        caches.open(CACHE_NAME).then(function(cache) {\\n"
    "          cache.put(e.request, clone);\\n"
    "        });\\n"
    "        return response;\\n"
    "      }).catch(function() {\\n"
    "        return caches.match('./GeoQuest.html');\\n"
    "      });\\n"
    "    })\\n"
    "  );\\n"
    "});\\n"
)
with open('sw.js', 'w', encoding='utf-8') as _sw_f:
    _sw_f.write(_sw_content)
print('Written: sw.js (cache=' + _cache_name + ', ' + str(len(_data_files)) + ' data files)')

# ── Phase 238: Generate manifest.json (synced theme_color + SVG icon) ──────────────
import json as _json_m
_manifest = {
    'name': 'GeoQuest',
    'short_name': 'GeoQuest',
    'description': 'Das ultimative Geographie-Quiz \\u2013 St\\u00e4dte, Flaggen, Hauptst\\u00e4dte, Fl\\u00fcsse & Sehensw\\u00fcrdigkeiten',
    'start_url': './GeoQuest.html',
    'display': 'standalone',
    'background_color': '#0f172a',
    'theme_color': '#10b981',
    'orientation': 'portrait-primary',
    'icons': [{'src': 'icon.svg', 'sizes': 'any', 'type': 'image/svg+xml', 'purpose': 'any maskable'}],
    'categories': ['games', 'education'],
    'lang': 'de',
    'scope': './'
}
with open('manifest.json', 'w', encoding='utf-8') as _mf:
    _json_m.dump(_manifest, _mf, ensure_ascii=False, indent=2)
print('Written: manifest.json (theme_color=#10b981, icon.svg only)')

""" + OLD_BUILD

c = c.replace(OLD_BUILD, GENERATORS, 1)
print('  [OK] Fix 2: sw.js generator injected into gen.py build step')
print('  [OK] Fix 3: manifest.json generator injected into gen.py build step')

with open(GEN, 'w', encoding='utf-8') as fh:
    fh.write(c)

# ==============================================================================
# FIX 4 — Add verify.py section 12: sw.js validation
# ==============================================================================
with open(VERIFY, 'r', encoding='utf-8') as fh:
    v = fh.read()

OLD_RESULTS = '# =============================================================\nprint("\\n" + "=" * 58)'
assert v.count(OLD_RESULTS) == 1, f'verify.py results anchor not unique (found {v.count(OLD_RESULTS)})'

NEW_SECTION_12 = """\
# -- 12. Service Worker sw.js --------------------------------
section("12. Service Worker sw.js")
sw_path = 'sw.js'
if not os.path.isfile(sw_path):
    fail("sw.js MISSING — run python gen.py to generate it")
else:
    with open(sw_path, 'r', encoding='utf-8') as f:
        sw = f.read()
    sw_size = os.path.getsize(sw_path)
    # Must contain a hash-versioned cache name
    if not re.search(r"CACHE_NAME = 'geoquest-[a-f0-9]{8}'", sw):
        fail("sw.js: CACHE_NAME hash-version pattern missing")
    else:
        ok("sw.js: CACHE_NAME hash-version present")
    # Must list all data/*.json files
    data_json_files = sorted(f for f in os.listdir(DATA_DIR) if f.endswith('.json'))
    missing_in_sw = [f for f in data_json_files if "./data/" + f not in sw]
    if missing_in_sw:
        fail("sw.js: " + str(len(missing_in_sw)) + " data files missing from ASSETS: " + str(missing_in_sw[:3]))
    else:
        ok("sw.js: all " + str(len(data_json_files)) + " data/*.json in ASSETS (" + str(sw_size) + " bytes)")
    # Must use Promise.allSettled (non-atomic install)
    if 'Promise.allSettled' not in sw:
        fail("sw.js: Promise.allSettled missing — install could abort atomically")
    else:
        ok("sw.js: Promise.allSettled install strategy confirmed")

""" + OLD_RESULTS

v = v.replace(OLD_RESULTS, NEW_SECTION_12, 1)

with open(VERIFY, 'w', encoding='utf-8') as fh:
    fh.write(v)

print('  [OK] Fix 4: verify.py section 12 (sw.js validation) added')
print()
print('  All Phase 238 fixes applied. Run: python gen.py && python verify.py')
