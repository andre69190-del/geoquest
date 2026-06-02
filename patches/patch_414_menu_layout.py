"""
Phase 414 — Dual Menu Layout (Akkordeon + Tabs)
- Settings-Toggle: gq_menu_layout = "accordion" | "tabs"
- Tab-Ansicht: 3 Reihen à 8 Kategorien (alle sichtbar, kein Scrollen nötig)
- Akkordeon: unverändert (Carousel bleibt)
- Settings-Modal: visueller Layout-Picker
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def r(p): return open(p, 'r', encoding='utf-8').read()
def w(p, c): open(p, 'w', encoding='utf-8').write(c)
def rpl(c, old, new, label):
    assert c.count(old) == 1, f"ANCHOR {c.count(old)}x: {label!r}"
    return c.replace(old, new)

c = r(os.path.join(ROOT, 'gen.py'))

# ─────────────────────────────────────────────────────────────────────────
# 1. CSS: Tab-Navigation + tabs-mode Overrides
# ─────────────────────────────────────────────────────────────────────────
TAB_CSS = (
    ".tabs-nav{display:flex;flex-wrap:wrap;gap:3px;padding:0 10px 8px;}"
    ".cat-tab{flex:0 0 calc(12.5% - 3px);min-width:0;display:flex;flex-direction:column;"
    "align-items:center;justify-content:center;padding:5px 0;border-radius:8px;"
    "border:1.5px solid var(--border);background:var(--bg2);cursor:pointer;"
    "font-size:.6rem;color:var(--text2);line-height:1.2;transition:all .15s;gap:1px;"
    "touch-action:manipulation;user-select:none;}"
    ".cat-tab .ct-icon{font-size:1.1rem;line-height:1;}"
    ".cat-tab .ct-lbl{font-size:.48rem;white-space:nowrap;overflow:hidden;"
    "text-overflow:ellipsis;width:100%;text-align:center;padding:0 2px;}"
    ".cat-tab.active{background:#7F77DD;border-color:#534AB7;color:#fff;}"
    ".cat-tab.active .ct-lbl{color:#fff;}"
    ".tabs-mode .accordion-header{display:none!important;}"
    ".tabs-mode .accordion-section{margin-bottom:0!important;}"
    ".tabs-mode .accordion-content{border-radius:10px;}"
    ".tabs-mode #mainGamesGrid{padding:0 10px!important;}"
)

c = rpl(c,
    "</style>';",
    TAB_CSS + "</style>';",
    "tab CSS injection")
print("OK 1: CSS eingebettet")

# ─────────────────────────────────────────────────────────────────────────
# 2. renderHomeTab: Tab-Bar + tabs-mode class
# ─────────────────────────────────────────────────────────────────────────

TAB_BAR_JS = r"""
  /* Phase 414: Tab-Ansicht */
  const _menuLayout=(()=>{try{return localStorage.getItem('gq_menu_layout')||'accordion';}catch(e){return 'accordion';}})();
  const _catAbbrev={pure_geo:'Geo',lifestyle:'Kult',eu_plates:'Kz',zuege:'Zug',
    sport:'Sprt',hl_compare:'H/L',comparisons:'Vrgl',airports:'Air',
    neighbors:'Nbr',map_mode:'Map',tiere:'Tier',pflanzen:'Pflz',
    gastronomie:'Gast',technologie:'Tech',emobilitaet:'E-Mob',
    archaeologie:'Arch',astronomie:'Astr',geologie:'Geo-V',
    sport_wissen:'S-W',games:'Game',autos:'Auto',regional:'Reg'};
  const _activeCat=S.filterCat||'pure_geo';
  const _tabNavHtml=_menuLayout==='tabs'?`<div class="tabs-nav">${_CAT_ORDER.filter(k=>MODE_CATS[k]).map(k=>{
    const cat=MODE_CATS[k];
    const abbr=_catAbbrev[k]||(cat.label.split(' ')[0].substring(0,5));
    return`<div class="cat-tab${k===_activeCat?' active':''}" onclick="window.filterByCategory('${k}');render()">
      <span class="ct-icon">${cat.icon}</span>
      <span class="ct-lbl">${abbr}</span>
    </div>`;
  }).join('')}</div>`:'';
  const _tabsModeClass=_menuLayout==='tabs'?' tabs-mode':'';
"""

c = rpl(c,
    "function renderHomeTab(){\n  const _CAT_ORDER",
    "function renderHomeTab(){\n  const _CAT_ORDER",  # no-op check
    "renderHomeTab exists")

# Insert tab logic after _CAT_ORDER definition
c = rpl(c,
    "  // Build accordion sections — Pure Geo auto-open, others closed\n  const _favs",
    TAB_BAR_JS + "  // Build accordion sections — Pure Geo auto-open, others closed\n  const _favs",
    "tab bar JS insertion")

# Inject tab bar + tabs-mode class into the homeHTML
c = rpl(c,
    '<div id="mainGamesGrid" style="padding:0 15px">${_accordionHTML}</div>',
    '${_tabNavHtml}<div id="mainGamesGrid" class="accordion-grid${_tabsModeClass}" style="padding:0 15px">${_accordionHTML}</div>',
    "tab bar + tabs-mode in homeHTML")

print("OK 2: renderHomeTab (Tab-Bar + tabs-mode class)")

# ─────────────────────────────────────────────────────────────────────────
# 3. renderSettingsModal: Layout-Picker
# ─────────────────────────────────────────────────────────────────────────

LAYOUT_PICKER = (
    "    <div style=\"margin-bottom:.9rem\">"
    "<div style=\"font-weight:700;margin-bottom:.5rem\">"
    "\\u{1F4CB} Men\\u00fc-Ansicht</div>"
    "<div style=\"display:flex;gap:8px\">"
    # Akkordeon card
    "<div onclick=\"localStorage.setItem('gq_menu_layout','accordion');render()\" "
    "style=\"flex:1;border:2px solid "
    "${(()=>{try{return localStorage.getItem('gq_menu_layout')||'accordion';}catch(e){return 'accordion';}})()==='accordion'?"
    "'#7F77DD':'var(--border)'};"
    "border-radius:10px;padding:8px;cursor:pointer;background:var(--bg2);text-align:center\">"
    "<div style=\"font-size:.7rem;margin-bottom:4px\">Akkordeon</div>"
    "<div style=\"display:flex;flex-direction:column;gap:2px\">"
    "${['','open','',''].map(t=>`<div style=\"height:${t?'14':'7'}px;background:${t?'#EEEDFE':'var(--bg)'};border:1px solid ${t?'#AFA9EC':'var(--border)'};border-radius:3px\"></div>`).join('')}"
    "</div></div>"
    # Tabs card
    "<div onclick=\"localStorage.setItem('gq_menu_layout','tabs');render()\" "
    "style=\"flex:1;border:2px solid "
    "${(()=>{try{return localStorage.getItem('gq_menu_layout')||'accordion';}catch(e){return 'accordion';}})()==='tabs'?"
    "'#7F77DD':'var(--border)'};"
    "border-radius:10px;padding:8px;cursor:pointer;background:var(--bg2);text-align:center\">"
    "<div style=\"font-size:.7rem;margin-bottom:4px\">Tabs</div>"
    "<div style=\"display:flex;flex-wrap:wrap;gap:2px\">"
    "${Array.from({length:8}).map((_,i)=>`<div style=\"width:10px;height:10px;background:${i===0?'#7F77DD':'var(--bg)'};border:1px solid ${i===0?'#534AB7':'var(--border)'};border-radius:2px\"></div>`).join('')}"
    "<div style=\"width:100%;height:20px;background:var(--bg);border:1px solid var(--border);border-radius:3px;margin-top:2px\"></div>"
    "</div></div>"
    "</div></div>"
)

c = rpl(c,
    '  </div></div>`;\n}\n\n/* LEADERBOARD helper (used from home) */',
    LAYOUT_PICKER + '  </div></div>`;\n}\n\n/* LEADERBOARD helper (used from home) */',
    "settings layout picker")

print("OK 3: Settings-Modal Layout-Picker")

w(os.path.join(ROOT, 'gen.py'), c)
print("gen.py gespeichert")
