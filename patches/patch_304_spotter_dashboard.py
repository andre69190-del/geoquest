"""
patch_304_spotter_dashboard.py
Phase 304 — Spotter Dashboard:
1. Depot-Button in renderCollectionScreen mit Fortschritts-Bar (ab 10 Items)
2. i18n-Labels für neue Strings
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
print(" Patch 304 — Spotter Dashboard")
print("=" * 58)

gen_path = os.path.join(BASE, "gen.py")
with open(gen_path, "r", encoding="utf-8") as f: g = f.read()

# =============================================================
# TEIL 1: Depot-Button ersetzen durch Dashboard-Widget
# Total kollektierbare Items: 721
# =============================================================
print("\n[1] Depot Dashboard Widget")

OLD_DEPOT_BTN = 'const _depotBtn=`<div style="text-align:center;margin:8px 0"><button onclick="showTrainDepot()" class="btn-g" style="background:#006064;color:#fff">🚉 \'+_tc("Zum Zug-Depot")+\'</button></div>`;'

NEW_DEPOT_BTN = '''const _trainDepotItems=loadTrainDepot();
  const _trainTotal=721;
  const _trainCount=_trainDepotItems.length;
  const _trainPct=Math.round(_trainCount/_trainTotal*100);
  const _depotBtn=_trainCount>=10?`<div style="background:linear-gradient(135deg,#004d40,#00695c);border-radius:12px;padding:10px 14px;margin:10px 0;display:flex;align-items:center;gap:10px;cursor:pointer" onclick="showTrainDepot()">
    <div style="font-size:1.8rem">🚉</div>
    <div style="flex:1">
      <div style="color:#fff;font-weight:800;font-size:.9rem">${_tc("Zug-Depot")}</div>
      <div style="color:#b2dfdb;font-size:.72rem;margin-top:1px">${_trainCount} / ${_trainTotal} ${_tc("gesammelt")}</div>
      <div style="background:rgba(255,255,255,.2);border-radius:4px;height:5px;margin-top:5px;overflow:hidden">
        <div style="background:#4db6ac;height:100%;width:${_trainPct}%;border-radius:4px;transition:width .4s"></div>
      </div>
    </div>
    <div style="color:#4db6ac;font-weight:900;font-size:.85rem">${_trainPct}%</div>
  </div>`:"";'''

g = patch(g, OLD_DEPOT_BTN, NEW_DEPOT_BTN, "Depot-Button → Dashboard Widget (mit Progress-Bar, ab 10 Items)")

# =============================================================
# TEIL 2: i18n — neue Labels (gesammelt, Dein Fortschritt)
# =============================================================
print("\n[2] i18n — neue Labels")

# EN block anchor
EN_ANCHOR = '"Zum Zug-Depot": "To Train Depot"'
NEW_EN_ENTRY = '"Zum Zug-Depot": "To Train Depot",\n"gesammelt": "collected",\n"Dein Fortschritt": "Your Progress",\n"Sammlung vervollständigen": "Complete the Collection"'
g = patch(g, EN_ANCHOR, NEW_EN_ENTRY, "EN: gesammelt/Fortschritt")

# PL block anchor
PL_ANCHOR = '"Zum Zug-Depot": "Do Depotu Pociągów"'
NEW_PL_ENTRY = '"Zum Zug-Depot": "Do Depotu Pociągów",\n"gesammelt": "zebrane",\n"Dein Fortschritt": "Twój postęp",\n"Sammlung vervollständigen": "Uzupełnij kolekcję"'
g = patch(g, PL_ANCHOR, NEW_PL_ENTRY, "PL: zebrane/postęp")

with open(gen_path, "w", encoding="utf-8") as f: f.write(g)
print("\n[DONE] Jetzt: python gen.py && python verify.py")
