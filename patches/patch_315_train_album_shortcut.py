#!/usr/bin/env python3
"""
patch_315_train_album_shortcut.py
Phase 315 — UI SPRINT: Album-Shortcut in der Züge-Kategorie

Adds a "Waggon-Scanner 📸" shortcut card as index 0 in the Züge & Bahn
category grid, identical in architecture to the Kennzeichen-Album card.
Click opens renderCollectionScreen() with S._spotterTab='waggons' active.
No MODES entry needed — card uses unshift() to inject into cardArr directly,
same pattern as eu_plates album shortcut. verify.py unaffected.
"""
import sys, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load(p):
    with open(p, encoding='utf-8') as f: return f.read()
def save(p, s):
    with open(p, 'w', encoding='utf-8') as f: f.write(s)
    print(f'  [OK] saved {os.path.relpath(p, BASE)}')
def fix(m):  print(f'  [FIX] {m}')
def ok(m):   print(f'  [OK]  {m}')
def skip(m): print(f'  [SKIP] {m}'); sys.exit(1)

src = load(os.path.join(BASE, 'gen.py'))

OLD = (
    "if(catId==='eu_plates')cardArr.push(`"
    "<div class=\"mode-card\" data-category=\"eu_plates\" "
    "onclick=\"S.tab='album';render()\" role=\"button\" "
    "data-title=\"Kennzeichen-Album\" "
    "style=\"background:linear-gradient(135deg,#1d4ed8,#3b82f6);border-color:#3b82f6\">"
    "<span class=\"mode-icon\">\\u{1F4D4}</span>"
    "<div class=\"mode-title\" style=\"color:#fff\">Album</div>"
    "<div class=\"mode-desc\" style=\"color:rgba(255,255,255,.8)\">${S.collectedPlates.length} ges.</div></div>`);"
)

ZUEGE_CARD = """
    if(catId==='zuege'){
      var _uicLogCount=0;try{_uicLogCount=JSON.parse(localStorage.getItem('gq_uic_log')||'[]').length;}catch(_e){}
      cardArr.unshift(`<div class="mode-card" data-category="zuege" onclick="S._spotterTab='waggons';S.tab='album';render()" role="button" data-title="Waggon-Scanner" style="background:linear-gradient(135deg,#0d47a1,#1565c0);border-color:#1565c0"><span class="mode-icon">📸</span><div class="mode-title" style="color:#fff">${_tc('Waggon-Scanner')}</div><div class="mode-desc" style="color:rgba(255,255,255,.8)">${_uicLogCount} ges.</div></div>`);
    }"""

already = "catId==='zuege'" in src[src.find("catId==='eu_plates'"):src.find("catId==='eu_plates'")+600] if "catId==='eu_plates'" in src else False

if already:
    ok("Waggon-Scanner shortcut already present")
elif OLD in src:
    src = src.replace(OLD, OLD + ZUEGE_CARD, 1)
    fix("Added Waggon-Scanner card to zuege category (unshift → index 0)")
    save(os.path.join(BASE, 'gen.py'), src)
else:
    skip("eu_plates album anchor not found")

print("\n✅ patch_315_train_album_shortcut.py done — run: python3 gen.py && python3 verify.py")
