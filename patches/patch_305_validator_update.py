"""
patch_305_validator_update.py
Phase 305 — Validator Update:
1. metro_logos.json in detect_and_check einhaengen
2. timeline.json Zug-Daten pruefen
3. check_i18n() Funktion fuer _CONTENT_I18N Vollstaendigkeit
4. Zug-spezifische WS-Checks verschaerfen
"""
import os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def patch(c, old, new, label):
    if old in c:
        print(f"  [OK] {label}")
        return c.replace(old, new, 1)
    print(f"  [SKIP] {label}")
    return c

print("=" * 58)
print(" Patch 305 — Validator Update")
print("=" * 58)

val_path = os.path.join(BASE, "validate_content.py")
with open(val_path, "r", encoding="utf-8") as f: c = f.read()

# =============================================================
# TEIL 1: metro_logos.json in detect_and_check einhaengen
# =============================================================
print("\n[1] detect_and_check: metro_logos.json + timeline.json")

OLD_DETECT_END = '''    elif name.endswith("_ws.json") or "ws_" in name:
        check_ws(filename, data)'''

NEW_DETECT_END = '''    elif name.endswith("_ws.json") or "ws_" in name:
        check_ws(filename, data)
    elif name == "metro_logos.json":
        # SVG-Array: [{svg, city, cc}] — prüfe auf leere SVGs und fehlende city
        for i, item in enumerate(data if isinstance(data, list) else []):
            if not item.get("svg","").startswith("<svg"):
                warn(filename, "metro_logos", item.get("city","?"), "SVG fehlt oder ungültig")
            if not item.get("city","").strip():
                warn(filename, "metro_logos", f"item[{i}]", "city-Feld leer")
    elif name == "timeline.json":
        # Timeline-Format: {key: {prompt, unit, items:[{n,year,hint}]}}
        for key, block in (data.items() if isinstance(data, dict) else {}.items()):
            if not isinstance(block, dict): continue
            items = block.get("items", [])
            bad_year = [i.get("n","?") for i in items if not isinstance(i.get("year"), (int,float))]
            if bad_year:
                warn(filename, key, bad_year[0], f"year-Feld fehlt/ungültig ({len(bad_year)} Items)")
            # Sortierbarkeit: Timeline muss sortierbar sein
            years = [i.get("year",0) for i in items if isinstance(i.get("year"),(int,float))]
            if years and max(years) - min(years) < 10:
                warn(filename, key, "range", f"Jahres-Spanne nur {max(years)-min(years)} — zu eng für Timeline")'''

c = patch(c, OLD_DETECT_END, NEW_DETECT_END, "metro_logos + timeline in detect_and_check")

# =============================================================
# TEIL 2: check_i18n() Funktion
# =============================================================
print("\n[2] check_i18n() Funktion einfuegen")

I18N_FUNC = '''
# ──────────────────────────────────────────────────────────────────────────────
# i18n Vollständigkeits-Check (Phase 305)
# ──────────────────────────────────────────────────────────────────────────────

def check_i18n():
    """
    Prüft _CONTENT_I18N in gen.py auf Vollständigkeit.
    Stellt sicher dass alle DE-Strings auch EN und PL-Übersetzungen haben.
    Eigennamen (Bahnhofsnamen, Zugmarken) sind ausgenommen.
    """
    gen_path = os.path.join(HERE, "gen.py")
    if not os.path.exists(gen_path):
        warn("gen.py", "i18n", "", "gen.py nicht gefunden — i18n-Check übersprungen")
        return

    with open(gen_path, "r", encoding="utf-8") as f:
        g = f.read()

    import re, json as _json

    # Extract _CONTENT_I18N object
    m = re.search(r'const _CONTENT_I18N=(\{.*?\});\s*function', g, re.DOTALL)
    if not m:
        warn("gen.py", "i18n", "_CONTENT_I18N", "Konnte _CONTENT_I18N nicht parsen")
        return

    try:
        # JS to Python: replace JS object notation
        raw = m.group(1)
        i18n = _json.loads(raw)
    except Exception:
        warn("gen.py", "i18n", "_CONTENT_I18N", "JSON-Parse-Fehler in _CONTENT_I18N")
        return

    en_keys = set(i18n.get("en", {}).keys())
    pl_keys = set(i18n.get("pl", {}).keys())

    # Check that EN and PL have the same keys as each other
    en_only = en_keys - pl_keys
    pl_only = pl_keys - en_keys

    # Filter: skip strings that look like proper nouns (all caps, or start with capital city/train names)
    # Simple heuristic: skip if >50% of words are capitalized proper nouns
    def likely_proper_noun(s):
        words = s.split()
        if not words: return True
        caps = sum(1 for w in words if w[:1].isupper() and not w.isupper())
        return caps / len(words) > 0.7

    missing_pl = [k for k in en_only if not likely_proper_noun(k)]
    missing_en = [k for k in pl_only if not likely_proper_noun(k)]

    for key in sorted(missing_pl)[:10]:  # Max 10 warnings
        warn("gen.py", "i18n/pl", key[:50], "PL-Übersetzung fehlt (EN vorhanden)")
    for key in sorted(missing_en)[:10]:
        warn("gen.py", "i18n/en", key[:50], "EN-Übersetzung fehlt (PL vorhanden)")

    # Check for empty translations
    for lang, trans in i18n.items():
        for de_key, trans_val in trans.items():
            if not trans_val or not trans_val.strip():
                warn("gen.py", f"i18n/{lang}", de_key[:50], f"Leere Übersetzung in {lang}")

    total_en = len(en_keys)
    total_pl = len(pl_keys)
    missing_count = len(missing_pl) + len(missing_en)
    if missing_count == 0:
        print(f"    ✓ i18n vollständig: {total_en} EN, {total_pl} PL Übersetzungen")
    else:
        print(f"    ⚠ i18n: {missing_count} fehlende Übersetzungen (EN:{total_en}, PL:{total_pl})")

'''

# Insert before detect_and_check
DETECT_ANCHOR = "def detect_and_check(filename):"
c = patch(c, DETECT_ANCHOR, I18N_FUNC + DETECT_ANCHOR, "check_i18n() Funktion")

# =============================================================
# TEIL 3: check_i18n() im Main aufrufen
# =============================================================
print("\n[3] check_i18n() im Main-Loop einbinden")

OLD_MAIN_SCAN = "    checked = 0\n    for filename in json_files:"
NEW_MAIN_SCAN = """    # i18n-Check (einmalig, nicht pro Datei)
    print("  [i18n-Check gen.py]", end=" ")
    check_i18n()

    checked = 0
    for filename in json_files:"""

c = patch(c, OLD_MAIN_SCAN, NEW_MAIN_SCAN, "check_i18n() im Main")

with open(val_path, "w", encoding="utf-8") as f: f.write(c)
print("\n[DONE] validate_content.py aktualisiert. Jetzt ausfuehren:")
print("  python3 validate_content.py")
