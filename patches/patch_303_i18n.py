"""
patch_303_i18n.py
Phase 303 — i18n-Fix Züge-Kategorie:
1. _tc() wrapping für hardcodierte DE-Strings in genDS100InputQ() + genMetroLogoQ()
2. EN + PL Übersetzungen in _CONTENT_I18N eintragen
3. showTrainDepot() Labels via _tc() + Übersetzungen
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
print(" Patch 303 — i18n Züge-Kategorie")
print("=" * 58)

gen_path = os.path.join(BASE, "gen.py")
with open(gen_path, "r", encoding="utf-8") as f: g = f.read()

# =============================================================
# TEIL 1: _tc() wrapping — genDS100InputQ
# =============================================================
print("\n[1] genDS100InputQ — _tc() wrapping")
g = patch(g,
    'prompt:"Tippe das DS100-Betriebsstellenkürzel:",',
    'prompt:_tc("Tippe das DS100-Betriebsstellenkürzel:"),',
    "DS100 prompt → _tc()")
g = patch(g,
    'meta:"z.B. FF für Frankfurt, MH für München",',
    'meta:_tc("z.B. FF für Frankfurt, MH für München"),',
    "DS100 meta → _tc()")

# =============================================================
# TEIL 2: _tc() wrapping — genMetroLogoQ
# =============================================================
print("\n[2] genMetroLogoQ — _tc() wrapping")
g = patch(g,
    'prompt:"Welchem Nahverkehrsnetz gehört dieses Logo?",',
    'prompt:_tc("Welchem Nahverkehrsnetz gehört dieses Logo?"),',
    "Metro-Logo prompt → _tc()")

# =============================================================
# TEIL 3: _tc() wrapping — showTrainDepot Labels
# =============================================================
print("\n[3] showTrainDepot — _tc() wrapping")
g = patch(g,
    'var html="<div style=\'padding:12px\'><h2>🚉 Zug-Depot</h2><button onclick=\\"S.tab=\'album\';render()\\" class=\'btn-g\' style=\'margin-bottom:12px\'>← Zurück</button>";',
    'var html="<div style=\'padding:12px\'><h2>🚉 "+_tc("Zug-Depot")+"</h2><button onclick=\\"S.tab=\'album\';render()\\" class=\'btn-g\' style=\'margin-bottom:12px\'>← "+_tc("Zurück")+"</button>";',
    "showTrainDepot H2 + Zurück → _tc()")

g = patch(g,
    'html+=renderSec("Halterkürzel (VKM)",allVkm);',
    'html+=renderSec(_tc("Halterkürzel (VKM)"),allVkm);',
    "VKM Sektion → _tc()")
g = patch(g,
    'html+=renderSec("Panoramabahnen",allPan);',
    'html+=renderSec(_tc("Panoramabahnen"),allPan);',
    "Panorama Sektion → _tc()")
g = patch(g,
    'html+=renderSec("Bahnhofskürzel (DS100)",allDs);',
    'html+=renderSec(_tc("Bahnhofskürzel (DS100)"),allDs);',
    "DS100 Sektion → _tc()")
g = patch(g,
    'html+=renderSec("Legendaere Routen",allRouten);',
    'html+=renderSec(_tc("Legendäre Routen"),allRouten);',
    "Routen Sektion → _tc()")
g = patch(g,
    'html+=renderSec("Bahnhofs-Architektur",allBahnTyp);',
    'html+=renderSec(_tc("Bahnhofs-Architektur"),allBahnTyp);',
    "Architektur Sektion → _tc()")
g = patch(g,
    'html+=renderSec("Zug-Hersteller",allHerst);',
    'html+=renderSec(_tc("Zug-Hersteller"),allHerst);',
    "Hersteller Sektion → _tc()")
g = patch(g,
    'html+=renderSec("Metro-Logos",allMetro);',
    'html+=renderSec(_tc("Metro-Logos"),allMetro);',
    "Metro-Logos Sektion → _tc()")

# =============================================================
# TEIL 4: renderCollectionScreen — Depot-Button
# =============================================================
print("\n[4] Depot-Button → _tc()")
g = patch(g,
    '🚉 Zum Zug-Depot</button>',
    '🚉 \'+_tc("Zum Zug-Depot")+\'</button>',
    "Depot-Button → _tc()")

# =============================================================
# TEIL 5: _CONTENT_I18N erweitern (EN + PL)
# =============================================================
print("\n[5] _CONTENT_I18N — EN + PL Übersetzungen")

NEW_EN = """,
"Tippe das DS100-Betriebsstellenkürzel:": "Type the DS100 station code:",
"z.B. FF für Frankfurt, MH für München": "e.g. FF for Frankfurt, MH for Munich",
"Welchem Nahverkehrsnetz gehört dieses Logo?": "Which public transit network does this logo belong to?",
"Zug-Depot": "Train Depot",
"Zurück": "Back",
"Zum Zug-Depot": "To Train Depot",
"Halterkürzel (VKM)": "Keeper Codes (VKM)",
"Panoramabahnen": "Panoramic Railways",
"Bahnhofskürzel (DS100)": "Station Codes (DS100)",
"Legendäre Routen": "Legendary Routes",
"Bahnhofs-Architektur": "Station Architecture",
"Zug-Hersteller": "Train Manufacturers",
"Metro-Logos": "Metro Logos",
"Aus welchem Land stammt dieses Fahrzeughalter-Kürzel?": "Which country does this vehicle keeper code come from?",
"Welches Betriebsstellenkürzel hat dieser Bahnhof?": "What is the DS100 station code for this station?",
"In welchem Land fährt dieser Panorama- oder Luxuszug?": "Which country does this panoramic or luxury train operate in?",
"Welche Bauform hat dieser Bahnhof?": "What type of station architecture is this?",
"Von welchem Hersteller stammt dieser Zug?": "Which manufacturer built this train?",
"Höhere Taktfrequenz (Züge/Stunde)?": "Higher service frequency (trains/hour)?",
"Wo auf der Karte liegt diese Rekord-Strecke?": "Where on the map is this record-breaking railway route?",
"Wann wurde dieser Bahnhof eroeffnet?": "When did this station open?",
"Chronologisch sortieren — Bahnhofs-Eroeffnungen!": "Sort chronologically — Station openings!",
"Hoehere Taktfrequenz (Zuege pro Stunde)?": "Higher service frequency (trains/hour)?",
"Aus welchem Land faehrt dieser beruehmt Zug?": "Which country does this famous train operate in?",
"Welchem Nahverkehrsnetz gehört dieses Logo?": "Which public transit network does this logo belong to?"
"""

NEW_PL = """,
"Tippe das DS100-Betriebsstellenkürzel:": "Wpisz kod stacji DS100:",
"z.B. FF für Frankfurt, MH für München": "np. FF dla Frankfurtu, MH dla Monachium",
"Welchem Nahverkehrsnetz gehört dieses Logo?": "Do której sieci komunikacji miejskiej należy to logo?",
"Zug-Depot": "Depot Pociągów",
"Zurück": "Wstecz",
"Zum Zug-Depot": "Do Depotu Pociągów",
"Halterkürzel (VKM)": "Kody VKM",
"Panoramabahnen": "Koleje widokowe",
"Bahnhofskürzel (DS100)": "Kody stacji (DS100)",
"Legendäre Routen": "Legendarne trasy",
"Bahnhofs-Architektur": "Architektura dworców",
"Zug-Hersteller": "Producenci pociągów",
"Metro-Logos": "Logo metra",
"Aus welchem Land stammt dieses Fahrzeughalter-Kürzel?": "Z jakiego kraju pochodzi ten kod VKM?",
"Welches Betriebsstellenkürzel hat dieser Bahnhof?": "Jaki jest kod DS100 tej stacji?",
"In welchem Land fährt dieser Panorama- oder Luxuszug?": "W jakim kraju kursuje ten panoramiczny lub luksusowy pociąg?",
"Welche Bauform hat dieser Bahnhof?": "Jaki typ architektoniczny ma ten dworzec?",
"Von welchem Hersteller stammt dieser Zug?": "Który producent zbudował ten pociąg?",
"Höhere Taktfrequenz (Züge/Stunde)?": "Wyższa częstotliwość kursowania (pociągi/godz.)?",
"Wo auf der Karte liegt diese Rekord-Strecke?": "Gdzie na mapie leży ta rekordowa trasa kolejowa?",
"Wann wurde dieser Bahnhof eroeffnet?": "Kiedy otwarto ten dworzec?",
"Chronologisch sortieren — Bahnhofs-Eroeffnungen!": "Sortuj chronologicznie — otwarcia dworców!",
"Hoehere Taktfrequenz (Zuege pro Stunde)?": "Wyższa częstotliwość kursowania (pociągi/godz.)?",
"Aus welchem Land faehrt dieser beruehmt Zug?": "Z jakiego kraju pochodzi ten słynny pociąg?",
"Welchem Nahverkehrsnetz gehört dieses Logo?": "Do której sieci komunikacji miejskiej należy to logo?"
"""

# Insert before the closing of each language block
# EN block ends with: "Südamerika (Argentinien)": "South America (Argentina)"}}
EN_ANCHOR = '"Südamerika (Argentinien)": "South America (Argentina)"}}'
if EN_ANCHOR in g:
    # Insert new EN entries before closing }}
    g = g.replace(
        EN_ANCHOR,
        '"Südamerika (Argentinien)": "South America (Argentina)"' + NEW_EN + "}}",
        1
    )
    print("  [OK] EN-Übersetzungen eingefügt")
else:
    # Try alternate
    alt = '"Suedamerika": "South America"'
    if alt in g:
        print("  [SKIP] EN anchor nicht gefunden, versuche alternativ")
    else:
        print("  [SKIP] EN anchor nicht gefunden")

# PL block — find its end
# PL should end similarly; find the last entry before the pl closing }
# Search for the pattern ending the PL block
pl_match = re.search(r'"Südamerika[^"]*":\s*"[^"]*"\s*\}', g)
# The PL block likely ends before the EN block
# Find PL block end: look for last PL entry
idx_pl = g.find('"pl":')
pl_block_start = g.index("{", idx_pl)

# Find the matching } for PL
depth = 0
for i in range(len(g) - pl_block_start):
    ch = g[pl_block_start + i]
    if ch == '{': depth += 1
    elif ch == '}':
        depth -= 1
        if depth == 0:
            pl_end = pl_block_start + i
            break

pl_last200 = g[pl_end-200:pl_end+5]
print(f"\n  PL block last chars: {repr(pl_last200[-100:])}")

# Find anchor in PL (last entry before closing })
pl_anchor_m = re.search(r'"[^"]+": "[^"]*"(?=\s*\})', g[pl_block_start:pl_end+1])
if pl_anchor_m:
    pl_anchor = pl_anchor_m.group(0)
    # Find the last occurrence
    pl_anchors = list(re.finditer(re.escape(pl_anchor), g[pl_block_start:pl_end+1]))
    if pl_anchors:
        last_match = pl_anchors[-1]
        abs_pos = pl_block_start + last_match.start()
        replacement = pl_anchor + NEW_PL
        g = g[:abs_pos] + replacement + g[abs_pos + len(pl_anchor):]
        print(f"  [OK] PL-Übersetzungen eingefügt (nach: {repr(pl_anchor[:50])})")

with open(gen_path, "w", encoding="utf-8") as f: f.write(g)
print("\n[DONE] Jetzt: python gen.py && python verify.py")
