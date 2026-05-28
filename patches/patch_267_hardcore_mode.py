"""
patch_267_hardcore_mode.py — Phase 267: Hardcore-Modus Persistenz + H/L-Fenster + Score-Multiplikator

Änderungen:
  1. S.diff aus localStorage (gq_diffx) laden beim Start
  2. Home-Tab Diff-Buttons: S.diff in localStorage persistieren
  3. H/L-Fenster: 3% im Hardcore, 10% sonst (5 Stellen)
  4. Hardcore-Punkte: flacher 1.5× Multiplikator (Math.ceil)
  5. showPtsPopup: optionaler Suffix (zeigt "(1.5x)" im Hardcore)
  6. Profil-Einstellungen: 🔥 Hardcore-Toggle
  7. Profil-Einstellungen: 💡 Feedback & Kontakt Card
"""
import re, sys, os

GEN = os.path.join(os.path.dirname(__file__), '..', 'gen.py')
GEN = os.path.abspath(GEN)

with open(GEN, 'r', encoding='utf-8') as f:
    src = f.read()

original = src
changes = []

# ── 1. S.diff init from localStorage ────────────────────────────────────────
old = '  ph:"menu",tab:"home",mode:"city",diff:"casual",'
new = '  ph:"menu",tab:"home",mode:"city",diff:(localStorage.getItem(\'gq_diffx\')||"casual"),'
if old in src:
    src = src.replace(old, new, 1)
    changes.append("1. S.diff: init from localStorage gq_diffx")
else:
    print("WARN: Change 1 anchor not found"); sys.exit(1)

# ── 2. Home diff buttons: add localStorage.setItem persistence ───────────────
btn_map = [
    ('onclick="S.diff=\'casual\';render()"',
     'onclick="S.diff=\'casual\';localStorage.setItem(\'gq_diffx\',\'casual\');render()"'),
    ('onclick="S.diff=\'hardcore\';render()"',
     'onclick="S.diff=\'hardcore\';localStorage.setItem(\'gq_diffx\',\'hardcore\');render()"'),
    ('onclick="S.diff=\'survival\';render()"',
     'onclick="S.diff=\'survival\';localStorage.setItem(\'gq_diffx\',\'survival\');render()"'),
    ('onclick="S.diff=\'blitz\';render()"',
     'onclick="S.diff=\'blitz\';localStorage.setItem(\'gq_diffx\',\'blitz\');render()"'),
]
for old_btn, new_btn in btn_map:
    if old_btn in src:
        src = src.replace(old_btn, new_btn, 1)
    else:
        print(f"WARN: Diff button anchor not found: {old_btn[:40]}"); sys.exit(1)
changes.append("2. Diff buttons: localStorage.setItem(gq_diffx) added")

# ── 3. H/L Fenster: 5 Stellen — sorted.length*0.1 (2×) und len*0.1 (3×) ─────
old_sl = 'Math.floor(sorted.length*0.1)'
new_sl = "Math.floor(sorted.length*(S.diff==='hardcore'?0.03:0.10))"
count_sl = src.count(old_sl)
if count_sl != 2:
    print(f"WARN: expected 2 occurrences of sorted.length*0.1, found {count_sl}"); sys.exit(1)
src = src.replace(old_sl, new_sl)

old_len = 'Math.floor(len*0.1)'
new_len = "Math.floor(len*(S.diff==='hardcore'?0.03:0.10))"
count_len = src.count(old_len)
if count_len != 3:
    print(f"WARN: expected 3 occurrences of len*0.1, found {count_len}"); sys.exit(1)
src = src.replace(old_len, new_len)
changes.append(f"3. H/L Fenster: {count_sl+count_len} Stellen auf 3%/10% HC/normal geändert")

# ── 4. Hardcore pts: flacher 1.5× ───────────────────────────────────────────
old_pts = 'pts=Math.round(15*S.hcMult);'
new_pts = 'pts=Math.ceil(10*1.5);'
if old_pts in src:
    src = src.replace(old_pts, new_pts, 1)
    changes.append("4. Hardcore pts: Math.ceil(10*1.5) = 15")
else:
    print("WARN: Change 4 anchor not found"); sys.exit(1)

# ── 5. showPtsPopup: optionaler Suffix ──────────────────────────────────────
old_popup = 'function showPtsPopup(pts){const el=document.createElement("div");el.className="pts-popup";el.textContent="+"+pts;'
new_popup = 'function showPtsPopup(pts,suf){const el=document.createElement("div");el.className="pts-popup";el.textContent="+"+pts+(suf?" "+suf:"");'
if old_popup in src:
    src = src.replace(old_popup, new_popup, 1)
    changes.append("5. showPtsPopup: suf parameter added")
else:
    print("WARN: Change 5 anchor not found"); sys.exit(1)

# ── 6. answer(): Pass "(1.5x)" suffix bei Hardcore ──────────────────────────
old_call = "showPtsPopup(pts);if(navigator.vibrate)navigator.vibrate([50]);}"
new_call = "showPtsPopup(pts,S.diff==='hardcore'?'(1.5x)':'');if(navigator.vibrate)navigator.vibrate([50]);}"
if old_call in src:
    src = src.replace(old_call, new_call, 1)
    changes.append("6. answer(): showPtsPopup passes '(1.5x)' in hardcore")
else:
    print("WARN: Change 6 anchor not found"); sys.exit(1)

# ── 7. Profil-Einstellungen: 🔥 Hardcore-Toggle row ─────────────────────────
# Insert after the Dark Mode row (closing </div>) and before the grid settings block
old_dm = (
    '      <button onclick="S.darkMode=!S.darkMode;applyTheme();render()" class="btn-g" '
    'style="width:auto;padding:.4rem .85rem;margin-bottom:0;font-size:.8rem">'
    "${S.darkMode?'An':'Aus'}</button>\n    </div>\n"
    "    ${(()=>{"
)
new_dm = (
    '      <button onclick="S.darkMode=!S.darkMode;applyTheme();render()" class="btn-g" '
    'style="width:auto;padding:.4rem .85rem;margin-bottom:0;font-size:.8rem">'
    "${S.darkMode?'An':'Aus'}</button>\n    </div>\n"
    '    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:.75rem">\n'
    '      <div style="font-weight:700">\\u{1F525} Hardcore-Modus</div>\n'
    "      <button onclick=\"S.diff=(S.diff==='hardcore'?'casual':'hardcore');localStorage.setItem('gq_diffx',S.diff);render()\" "
    'class="btn-g" style="width:auto;padding:.4rem .85rem;margin-bottom:0;font-size:.8rem">'
    "${S.diff==='hardcore'?'An':'Aus'}</button>\n    </div>\n"
    "    ${(()=>{"
)
if old_dm in src:
    src = src.replace(old_dm, new_dm, 1)
    changes.append("7. Profil: 🔥 Hardcore-Toggle row added")
else:
    print("WARN: Change 7 anchor not found"); sys.exit(1)

# ── 8. Profil-Einstellungen: 💡 Feedback & Kontakt Card ─────────────────────
old_close = '    <button class="btn-g" style="margin-bottom:0" onclick="S.settingsModal=false;render()">Schlie\\u00dfen</button>'
new_close = (
    '    <div onclick="S.settingsModal=false;openFeedback();render()" '
    'style="display:flex;align-items:center;gap:.6rem;padding:.6rem .85rem;border-radius:10px;'
    'background:var(--bg3);cursor:pointer;margin-bottom:.75rem;border:1px solid var(--border)">\n'
    '      <span style="font-size:1.2rem">\\u{1F4A1}</span>\n'
    '      <div><div style="font-weight:700;font-size:.85rem">Feedback &amp; Kontakt</div>'
    '<div style="font-size:.75rem;color:var(--text3)">Fehler melden, Ideen einreichen</div></div>\n'
    '    </div>\n'
    '    <button class="btn-g" style="margin-bottom:0" onclick="S.settingsModal=false;render()">Schlie\\u00dfen</button>'
)
if old_close in src:
    src = src.replace(old_close, new_close, 1)
    changes.append("8. Profil: 💡 Feedback & Kontakt Card added")
else:
    print("WARN: Change 8 anchor not found"); sys.exit(1)

# ── Write back ───────────────────────────────────────────────────────────────
if src == original:
    print("ERROR: No changes made!"); sys.exit(1)

with open(GEN, 'w', encoding='utf-8') as f:
    f.write(src)

print(f"patch_267_hardcore_mode.py: {len(changes)} Änderungen angewendet")
for i, c in enumerate(changes, 1):
    print(f"  ✓ {c}")
