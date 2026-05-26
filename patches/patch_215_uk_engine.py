"""
Phase 215: Typography Hardening — smart language-aware hyphenation
- P1: geoquest_css.txt main .mode-title: word-break→normal + hyphens:auto
- P2: gen.py inline .mode-title (mobile): same fix
- P3: setLanguage() → document.documentElement.lang = lang
- P4: App init → sync html[lang] from S.language on page load
- P5: detectUserCountry → sync html[lang] after auto-detect
"""

import re

# ── geoquest_css.txt ─────────────────────────────────────────────────────────
css = open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/geoquest_css.txt','r',encoding='utf-8').read()
css_orig = len(css)
patches_css = 0

OLD_CSS = '.mode-title{color:var(--text);font-size:.78rem;font-weight:700;line-height:1.2;margin-bottom:2px;word-break:break-word;overflow-wrap:break-word}'
NEW_CSS = '.mode-title{color:var(--text);font-size:.78rem;font-weight:700;line-height:1.3;margin-bottom:2px;word-break:normal;overflow-wrap:break-word;-webkit-hyphens:auto;-moz-hyphens:auto;hyphens:auto}'
if OLD_CSS in css:
    css = css.replace(OLD_CSS, NEW_CSS, 1)
    patches_css += 1
    print("OK    [P1: geoquest_css.txt .mode-title]")
else:
    print("MISS  [P1: geoquest_css.txt .mode-title]")

with open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/geoquest_css.txt','w',encoding='utf-8') as f:
    f.write(css)
print(f"      CSS size delta: {len(css)-css_orig:+d} chars")

# ── gen.py ───────────────────────────────────────────────────────────────────
src = open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py','r',encoding='utf-8').read()
orig_len = len(src)
patches_ok = []

def patch(label, old, new):
    global src
    count = src.count(old)
    if count == 0:
        print(f"MISS  [{label}]")
        return False
    if count > 1:
        print(f"WARN  [{label}] — {count} occurrences, replacing first")
    src = src.replace(old, new, 1)
    patches_ok.append(label)
    print(f"OK    [{label}]")
    return True

# P2: inline .mode-title in gen.py JS template (mobile size .68rem)
patch(
    "P2: gen.py inline .mode-title hyphens",
    '.mode-title{color:var(--text);font-size:.68rem;font-weight:700;line-height:1.2;word-break:break-word;overflow-wrap:break-word}',
    '.mode-title{color:var(--text);font-size:.68rem;font-weight:700;line-height:1.3;word-break:normal;overflow-wrap:break-word;-webkit-hyphens:auto;-moz-hyphens:auto;hyphens:auto}'
)

# P3: setLanguage() — sync document.documentElement.lang
patch(
    "P3: setLanguage sync html[lang]",
    "function setLanguage(lang){\n  if(typeof S!=='undefined')S.language=lang;\n  localStorage.setItem('gq_lang',lang);",
    "function setLanguage(lang){\n  if(typeof S!=='undefined')S.language=lang;\n  document.documentElement.lang=lang;\n  localStorage.setItem('gq_lang',lang);"
)

# P4: App init — set html[lang] right after rng() (S is already initialised)
patch(
    "P4: app-init html[lang] sync",
    "function rng(){return rngSeed!==null?seededRand():Math.random();}\n\nlet PLATES_DATA=",
    "function rng(){return rngSeed!==null?seededRand():Math.random();}\n/* Phase 215: sync html[lang] with active language on page load */\ndocument.documentElement.lang=(typeof S!=='undefined'&&S.language)||localStorage.getItem('gq_lang')||'de';\n\nlet PLATES_DATA="
)

# P5: detectUserCountry — sync html[lang] after auto-detect
patch(
    "P5: detectUserCountry html[lang] sync",
    "S.language=_al;localStorage.setItem('gq_lang',_al);",
    "S.language=_al;localStorage.setItem('gq_lang',_al);document.documentElement.lang=_al;"
)

print(f"\nPatches applied: {len(patches_ok)}/4 (gen.py) + {patches_css}/1 (css)")
print(f"gen.py size delta: {len(src)-orig_len:+d} chars")
with open('/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py','w',encoding='utf-8') as f:
    f.write(src)
print("Written OK")
