"""
patch_273_schaetzer_fix.py
Phase 273: Distanz-/Flugzeit-Schätzer Fix
- Normalisiert alle c-Werte in kultur.json (konsistentes Format)
- Updated ansPool in gen.py auf alle einzigartigen c-Werte (50 statt 10/8)
- Updated generate_spieluebersicht.py Hardcode auf 50
"""

import json, re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─── 1. Normalisiere kultur.json c-Werte ───────────────────────────────────

def norm_distanz(c):
    """Konvertiert alle Distanzwerte zu deutschem Format mit Punkt-Tausendertrenner."""
    # Entferne bestehende Punkte als Tausendertrenner, dann neu setzen
    raw = c.replace(' km', '').replace('.', '')
    try:
        n = int(raw)
    except ValueError:
        return c  # unbekanntes Format unverändert lassen
    if n >= 1000:
        # Deutschen Tausendertrenner (Punkt) einfügen
        s = f"{n:,}".replace(',', '.')
        return f"{s} km"
    else:
        return f"{n} km"

def norm_flugzeit(c):
    """Entfernt ~ und Zusätze wie (mit Stopp), normalisiert zu 'X Std.'"""
    c = c.strip()
    c = c.lstrip('~').strip()
    # Entferne Klammeranmerkungen wie "(mit Stopp)"
    c = re.sub(r'\s*\(.*?\)', '', c).strip()
    # Sicherstellen dass Format "X Std." ist
    if 'Std.' not in c:
        c = c + ' Std.'
    return c

with open(os.path.join(BASE, 'data', 'kultur.json'), 'r', encoding='utf-8') as f:
    kultur = json.load(f)

# Normalisiere distanz_schaetzer
changed_d = 0
for item in kultur['distanz_schaetzer']:
    orig = item['c']
    item['c'] = norm_distanz(orig)
    if item['c'] != orig:
        changed_d += 1

# Normalisiere flugzeit_schaetzer
changed_f = 0
for item in kultur['flugzeit_schaetzer']:
    orig = item['c']
    item['c'] = norm_flugzeit(orig)
    if item['c'] != orig:
        changed_f += 1

with open(os.path.join(BASE, 'data', 'kultur.json'), 'w', encoding='utf-8') as f:
    json.dump(kultur, f, ensure_ascii=False, indent=2)

print(f"✅ kultur.json: distanz {changed_d} Werte normalisiert, flugzeit {changed_f} Werte normalisiert")

# ─── Reload to get normalized values ───────────────────────────────────────

with open(os.path.join(BASE, 'data', 'kultur.json'), 'r', encoding='utf-8') as f:
    kultur = json.load(f)

distanz_vals = sorted(set(x['c'] for x in kultur['distanz_schaetzer']))
flugzeit_vals = sorted(set(x['c'] for x in kultur['flugzeit_schaetzer']))

print(f"  Unique distanz c-values ({len(distanz_vals)}): {distanz_vals[:5]}...")
print(f"  Unique flugzeit c-values ({len(flugzeit_vals)}): {flugzeit_vals[:5]}...")

# ─── 2. Update gen.py ansPool ───────────────────────────────────────────────

def vals_to_js_array(vals):
    """Konvertiert Python Liste zu JS Array String."""
    items = ','.join(f'"{v}"' for v in vals)
    return f'[{items}]'

distanz_js = vals_to_js_array(distanz_vals)
flugzeit_js = vals_to_js_array(flugzeit_vals)

with open(os.path.join(BASE, 'gen.py'), 'r', encoding='utf-8') as f:
    content = f.read()

# Replace distanz_schaetzer ansPool
OLD_DISTANZ = r'uk_distanz_schaetzer:()=>genFixedPoolMatchQ("distanz_schaetzer",["880 km","3940 km","3290 km","9560 km","7700 km","1140 km","6430 km","1400 km","1760 km","3360 km"])'
NEW_DISTANZ = f'uk_distanz_schaetzer:()=>genFixedPoolMatchQ("distanz_schaetzer",{distanz_js})'

if OLD_DISTANZ not in content:
    print("⚠️ distanz_schaetzer Generator nicht gefunden — suche mit Regex...")
    # Fallback regex
    content, n = re.subn(
        r'uk_distanz_schaetzer:\(\)=>genFixedPoolMatchQ\("distanz_schaetzer",\[.*?\]\)',
        f'uk_distanz_schaetzer:()=>genFixedPoolMatchQ("distanz_schaetzer",{distanz_js})',
        content
    )
    print(f"  Regex-Ersetzungen: {n}")
else:
    content = content.replace(OLD_DISTANZ, NEW_DISTANZ, 1)
    print("✅ distanz_schaetzer ansPool aktualisiert")

# Replace flugzeit_schaetzer ansPool
OLD_FLUGZEIT = r'uk_flugzeit_schaetzer:()=>genFixedPoolMatchQ("flugzeit_schaetzer",["9 Std.","21 Std.","12 Std.","16 Std.","14 Std.","8 Std.","10 Std.","11 Std."])'
NEW_FLUGZEIT = f'uk_flugzeit_schaetzer:()=>genFixedPoolMatchQ("flugzeit_schaetzer",{flugzeit_js})'

if OLD_FLUGZEIT not in content:
    print("⚠️ flugzeit_schaetzer Generator nicht gefunden — suche mit Regex...")
    content, n = re.subn(
        r'uk_flugzeit_schaetzer:\(\)=>genFixedPoolMatchQ\("flugzeit_schaetzer",\[.*?\]\)',
        f'uk_flugzeit_schaetzer:()=>genFixedPoolMatchQ("flugzeit_schaetzer",{flugzeit_js})',
        content
    )
    print(f"  Regex-Ersetzungen: {n}")
else:
    content = content.replace(OLD_FLUGZEIT, NEW_FLUGZEIT, 1)
    print("✅ flugzeit_schaetzer ansPool aktualisiert")

with open(os.path.join(BASE, 'gen.py'), 'w', encoding='utf-8') as f:
    f.write(content)

# ─── 3. Update generate_spieluebersicht.py ─────────────────────────────────

SPIELUE = os.path.join(BASE, 'generate_spieluebersicht.py')
with open(SPIELUE, 'r', encoding='utf-8') as f:
    sp = f.read()

OLD_SP = "'uk_distanz_schaetzer':(10,'Distanzen'),'uk_flugzeit_schaetzer':(8,'Flugzeiten')"
NEW_SP = "'uk_distanz_schaetzer':(50,'Distanzen'),'uk_flugzeit_schaetzer':(50,'Flugzeiten')"

if OLD_SP in sp:
    sp = sp.replace(OLD_SP, NEW_SP, 1)
    with open(SPIELUE, 'w', encoding='utf-8') as f:
        f.write(sp)
    print("✅ generate_spieluebersicht.py: Counts 10→50 und 8→50 aktualisiert")
else:
    print("⚠️ generate_spieluebersicht.py: String nicht gefunden, manuelle Prüfung nötig")
    # Try to find it
    import re as re2
    m = re2.search(r"uk_distanz_schaetzer.*?uk_flugzeit_schaetzer.*?\)", sp)
    if m:
        print(f"  Found: {m.group()}")

print("\n✅ patch_273 fertig. Jetzt: python3 gen.py && python3 generate_spieluebersicht.py")
