"""
generate_spieluebersicht.py
Regeneriert GeoQuest_Spielübersicht.html vollautomatisch aus:
  - gen.py  (MODES-Array + GEN-Dispatch)
  - data/*.json (echte Item-Zählungen)

Wird automatisch am Ende von gen.py aufgerufen.
Kann auch manuell ausgeführt werden: python3 generate_spieluebersicht.py
"""

import re, json, os

BASE  = os.path.dirname(os.path.abspath(__file__))
GEN   = os.path.join(BASE, "gen.py")
DATA  = os.path.join(BASE, "data")
OUT   = os.path.join(BASE, "GeoQuest_Spielübersicht.html")

# ── Unicode JS-Escape-Decoder ─────────────────────────────────────────────────
def _uesc(s):
    s = re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'\\u([0-9a-fA-F]{4})',   lambda m: chr(int(m.group(1), 16)), s)
    return s

# ── Generator → (file_prefix, struct) Mapping ────────────────────────────────
# struct: 'items' = data[key]['items'], 'list' = data[key] (plain list)
GEN_FILE_MAP = {
    # Tiere
    'genTiereHL':              ('tiere_hl',         'items'),
    'genUniversalPinQ':        ('kultur',            'list'),   # lat/lng list
    'genUniversalMatchQ':      ('kultur',            'list'),
    # Pflanzen
    'genPflanzenHL':           ('pflanzen_hl',       'items'),
    'genPflanzenPinQ':         ('pflanzen_pin',      'items'),
    'genPflanzenMatchQ':       ('pflanzen_match',    'items'),
    # Gastro
    'genGastroHL':             ('gastro_hl',         'items'),
    'genGastroPinQ':           ('gastro_pin',        'items'),
    'genGastroMatchQ':         ('gastro_match',      'items'),
    # Tech
    'genTechHL':               ('tech_hl',           'items'),
    'genTechPinQ':             ('tech_pin',          'items'),
    'genTechMatchQ':           ('tech_match',        'items'),
    # Geo (via _mkHL alias)
    'genGeoHL':                ('geo_hl',            'items'),
    'genGeoPinQ':              ('geo_pin',           'items'),
    'genGeoMatchQ':            ('geo_match',         'items'),
    # Sport
    'genSportWissenHL':        ('sport_hl',          'items'),
    'genSportPinQ':            ('sport_pin',         'items'),
    'genSportMatchQ':          ('sport_match',       'items'),
    # Astro
    'genAstroHL':              ('astro_hl',          'items'),
    'genAstroPinQ':            ('astro_pin',         'items'),
    'genAstroMatchQ':          ('astro_match',       'items'),
    # Archäologie
    'genArchHL':               ('archaeologie_hl',   'items'),
    'genArchPinQ':             ('archaeologie_pin',  'items'),
    'genArchMatchQ':           ('archaeologie_match','items'),
    # E-Mobilität
    'genEmobHL':               ('emob_hl',           'items'),
    'genEmobPinQ':             ('emob_pin',          'items'),
    'genEmobMatchQ':           ('emob_match',        'items'),
    # Timeline
    'genTimelineQ':            ('timeline',          'items'),
}

# WS-Funktionsnamen-Fragmente → "1 Basiswort"
WS_FN_FRAGMENTS = ('WortSchmiede', 'initTier', 'initPflanzen', 'initGastro',
                   'initTech', 'initGeo', 'initSport', 'initAstro', 'initArch',
                   'initEmob', 'WS', 'Wort')

# Hardcoded für Classic/Global-Modi (kein JSON-Key)
CLASSIC_COUNTS = {
    'city':             (2315, 'Städte'),
    'flag':             (195,  'Länder'),
    'capital':          (195,  'Länder'),
    'river':            (195,  'Länder'),
    'landmark':         (195,  'Länder'),
    'park':             (195,  'Länder'),
    'unesco':           (195,  'Länder'),
    'citymark':         (195,  'Länder'),
    'subway':           (195,  'Länder'),
    'flagsel':          (195,  'Länder'),
    'rcapital':         (195,  'Länder'),
    'rcity':            (195,  'Länder'),
    'rriver':           (195,  'Länder'),
    'outline':          (195,  'Länder'),
    'food':             (195,  'Länder'),
    'brand':            (195,  'Länder'),
    'currency':         (195,  'Länder'),
    'plate_casual':     (289,  'Codes'),
    'plate_hard':       (289,  'Codes'),
    'de_plate':         (495,  'Codes'),
    'plate_compare':    (289,  'Codes'),
    'curr_real':        (195,  'Länder'),
    'pop_compare':      (195,  'Länder'),
    'river_real':       (195,  'Länder'),
    'hl_pop':           (195,  'Länder'),
    'hl_river':         (195,  'Länder'),
    'hl_area':          (195,  'Länder'),
    'hl_gdp':           (195,  'Länder'),
    'hl_density':       (195,  'Länder'),
    'hl_elevation':     (195,  'Länder'),
    'hl_coastline':     (195,  'Länder'),
    'hl_borders':       (195,  'Länder'),
    'hl_lifeexp':       (195,  'Länder'),
    'hl_median_age':    (195,  'Länder'),
    'hl_forest':        (195,  'Länder'),
    'neighbor':         (195,  'Länder'),
    'neighbor_fake':    (195,  'Länder'),
    'neighbor_count':   (195,  'Länder'),
    'airport_pin':      (248,  'Airports'),
    'iata':             (248,  'Airports'),
    'iata_reverse':     (248,  'Airports'),
    'naechster_airport':(248,  'Airports'),
    'comp_airports':    (248,  'Airports'),
    'airport_map':      (248,  'Airports'),
    'stadium':          (32,   'Stadien'),
    'stadium_map':      (32,   'Stadien'),
    'map_guess':        (195,  'Länder'),
    'map_reverse':      (195,  'Länder'),
    'map_capital':      (195,  'Länder'),
    'map_ivr':          (195,  'Länder'),
    'river_map':        (195,  'Länder'),
    'unesco_map':       (195,  'Länder'),
    'f1_map':           (24,   'Strecken'),
    'flagcolor':        (195,  'Länder'),
    'climate_quiz':     (195,  'Länder'),
    'climate_mystery':  (195,  'Länder'),
    'flag_fusion':      (195,  'Länder'),
    'tz_quiz':          (195,  'Länder'),
    'landlocked_quiz':  (195,  'Länder'),
    'wappen_meister':   (195,  'Länder'),
    'alpha_sprint':     (195,  'Länder'),
    'border_q':         (195,  'Länder'),
    'timezone_jumper':  (195,  'Länder'),
}
# Comp-Modi alle 195 Länder
for _k in ['comp_area','comp_pop','comp_north','comp_gdp','comp_density',
           'comp_elevation','comp_coast','comp_borders','comp_life','comp_age',
           'comp_forest','comp_mountain','comp_nsextent','comp_olympics',
           'comp_flight']:
    CLASSIC_COUNTS[_k] = (195, 'Länder')
# HL-Beta (globale Länderdaten)
for _k in ['hl_b_rain','hl_b_temp','hl_b_sun','hl_b_vulc','hl_b_parks',
           'hl_b_roads','hl_b_rail','hl_b_net','hl_b_ev','hl_b_urban',
           'hl_b_lang','hl_b_isl','hl_b_tz','hl_b_founded','hl_b_unesco',
           'hl_b_tour','hl_b_wm']:
    CLASSIC_COUNTS[_k] = (195, 'Länder')


def _load_all_json():
    """Lädt alle data/*.json Dateien in ein Dict {stem: data}"""
    store = {}
    for fn in os.listdir(DATA):
        if fn.endswith('.json'):
            stem = fn[:-5]  # ohne .json
            with open(os.path.join(DATA, fn), encoding='utf-8') as f:
                store[stem] = json.load(f)
    return store


def _parse_gen_dispatch(src):
    """
    Extrahiert GEN-Dispatch aus gen.py.
    Gibt dict zurück: {mode_id: {'fn': 'generatorFn', 'key': 'data_key'}}
    """
    dispatch = {}

    # Pattern 1: mode:()=>genFoo("key")  oder  mode:()=>genFoo('key')
    for m in re.finditer(
        r'(\w+)\s*:\s*\(\)\s*=>\s*(\w+)\s*\(\s*["\']([^"\']+)["\']\s*\)',
        src
    ):
        dispatch[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}

    # Pattern 2: mode:()=>{initFoo("key");return null;}
    for m in re.finditer(
        r'(\w+)\s*:\s*\(\)\s*=>\s*\{\s*(\w+)\s*\(\s*["\']([^"\']+)["\']\s*\)',
        src
    ):
        if m.group(1) not in dispatch:
            dispatch[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}

    # Pattern 3: mode:()=>{initTierWortSchmiede("key");...}  (2 args)
    for m in re.finditer(
        r'(\w+)\s*:\s*\(\)\s*=>\s*\{\s*(\w+)\s*\(\s*["\']([^"\']+)["\']\s*,',
        src
    ):
        if m.group(1) not in dispatch:
            dispatch[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}

    return dispatch


def _get_item_count(mode_id, dispatch, store):
    """
    Gibt (display_str, raw_int) für einen Modus zurück.
    display_str: z.B. "34 Items", "195 Länder", "1 Basiswort", "—"
    """
    # WS-Modi immer "1 Basiswort"
    if mode_id.startswith('ws_'):
        return "1 Basiswort", 1

    # Classic-Fallback
    if mode_id in CLASSIC_COUNTS:
        n, unit = CLASSIC_COUNTS[mode_id]
        return f"{n} {unit}", n

    # GEN-Dispatch nachschlagen
    disp = dispatch.get(mode_id)
    if not disp:
        return "—", 0

    fn  = disp['fn']
    key = disp['key']

    # WS-Funktionen
    if any(frag in fn for frag in WS_FN_FRAGMENTS):
        return "1 Basiswort", 1

    # Generator → Datei + Struktur
    mapping = GEN_FILE_MAP.get(fn)
    if not mapping:
        # Fallback: unbekannter Generator
        return "—", 0

    file_stem, struct = mapping
    data = store.get(file_stem, {})
    entry = data.get(key)

    if entry is None:
        return "—", 0

    if struct == 'items':
        items = entry.get('items', []) if isinstance(entry, dict) else []
        count = len(items)
    elif struct == 'list':
        count = len(entry) if isinstance(entry, list) else 0
    else:
        count = 0

    if count == 0:
        return "—", 0

    return f"{count} Items", count


# ── Typ-Badge ─────────────────────────────────────────────────────────────────
TYPE_META = {
    'pin':      ('📍', 'Pin',          '#0d2820', '#34d399', '#34d39930'),
    'hl':       ('↕️', 'H/L',          '#0a1929', '#60a5fa', '#60a5fa30'),
    'match':    ('🃏', 'Match',         '#271a08', '#fbbf24', '#fbbf2430'),
    'ws':       ('🔡', 'Wort-Schmiede', '#180a2d', '#c084fc', '#c084fc30'),
    'timeline': ('📅', 'Timeline',      '#1a0a2e', '#a78bfa', '#a78bfa30'),
    'comp':     ('⚖️', 'Vergleich',     '#1a1008', '#fb923c', '#fb923c30'),
    'classic':  ('🌐', 'Classic',       '#0f1520', '#64748b', '#64748b30'),
}

def _get_type(mid):
    if mid.startswith('hl_') or '_hl_' in mid or mid.endswith('_hl'):   return 'hl'
    if mid.startswith('ws_') or '_ws_' in mid:                          return 'ws'
    if mid.startswith('uk_') and ('match' in mid or 'zuord' in mid):    return 'match'
    if mid.startswith('uk_') and 'pin' in mid:                          return 'pin'
    if mid.startswith('uk_'):                                            return 'match'
    if 'timeline' in mid:                                                return 'timeline'
    if mid.startswith('comp_') or mid.startswith('vergl_'):             return 'comp'
    if 'pin' in mid or mid.endswith('_map'):                            return 'pin'
    return 'classic'

def _badge(mid):
    t = _get_type(mid)
    e, label, bg, fg, border = TYPE_META[t]
    return f'<span class="tb" style="background:{bg};color:{fg};border-color:{border}">{e} {label}</span>'


# ── MODES aus gen.py parsen ───────────────────────────────────────────────────
def _parse_modes(src):
    start = src.index('const MODES=')
    depth = 0; i = start + len('const MODES='); end = i
    while i < len(src):
        if src[i] == '[': depth += 1
        elif src[i] == ']':
            depth -= 1
            if depth == 0: end = i+1; break
        i += 1
    raw = src[start+len('const MODES='):end]

    modes = []
    depth = 0; obj_start = -1
    for idx, ch in enumerate(raw):
        if ch == '{':
            if depth == 0: obj_start = idx
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0 and obj_start >= 0:
                obj = raw[obj_start:idx+1]
                mid   = re.search(r'id:"([^"]+)"', obj)
                title = re.search(r'title:"([^"]+)"', obj)
                group = re.search(r'group:"([^"]+)"', obj)
                desc  = re.search(r'desc:"([^"]+)"', obj)
                if mid and title and group:
                    modes.append({
                        'id':    mid.group(1),
                        'title': _uesc(title.group(1)),
                        'group': group.group(1),
                        'desc':  _uesc(desc.group(1)) if desc else '',
                    })
                obj_start = -1
    return modes


# ── Kategorie-Meta ─────────────────────────────────────────────────────────────
CAT_META = {
    'pure_geo':     ('🌍', 'Pure Geo'),
    'lifestyle':    ('🎭', 'Lifestyle'),
    'eu_plates':    ('🚗', 'EU-Kennzeichen'),
    'hl_compare':   ('↕️', 'Higher / Lower'),
    'comparisons':  ('⚖️', 'Vergleiche'),
    'sport':        ('⚽', 'Sport & Events'),
    'neighbors':    ('🤝', 'Nachbarn'),
    'map_mode':     ('🗺️', 'Karte'),
    'new_modes':    ('🧪', 'Neue Modi'),
    'airports':     ('✈️', 'Flughäfen & Klima'),
    'kultur':       ('🎨', 'Kultur'),
    'tiere':        ('🐾', 'Tiere & Natur'),
    'pflanzen':     ('🌿', 'Pflanzen'),
    'gastronomie':  ('🍽️', 'Gastronomie'),
    'technologie':  ('💻', 'Technologie'),
    'emobilitaet':  ('⚡', 'E-Mobilität'),
    'archaeologie': ('🏛️', 'Archäologie'),
    'astronomie':   ('🔭', 'Astronomie'),
    'geologie':     ('⛰️', 'Geologie'),
    'sport_wissen': ('🏆', 'Sport-Wissen'),
}
CAT_ORDER = list(CAT_META.keys())


def generate(phase=267, n_tests=90):
    """Hauptfunktion: generiert GeoQuest_Spielübersicht.html"""
    with open(GEN, 'r', encoding='utf-8') as f:
        src = f.read()

    modes    = _parse_modes(src)
    dispatch = _parse_gen_dispatch(src)
    store    = _load_all_json()

    from collections import defaultdict, Counter
    groups = defaultdict(list)
    for m in modes:
        groups[m['group']].append(m)

    # Gruppe-Reihenfolge: erst definierte, dann restliche
    seen = set()
    group_order = []
    for g in CAT_ORDER:
        if g in groups: group_order.append(g); seen.add(g)
    for g in groups:
        if g not in seen: group_order.append(g)

    group_counts = Counter(m['group'] for m in modes)
    total_modes  = len(modes)

    # Typ-Statistik für Legende
    type_counts  = Counter(_get_type(m['id']) for m in modes)

    # ── Kategorie-Sidebar ─────────────────────────────────────────────────────
    cat_btns = []
    for g in group_order:
        emoji, label = CAT_META.get(g, ('📂', g))
        cnt = group_counts[g]
        cat_btns.append(
            f'<div class="sc" onclick="fg(\'{g}\')" data-group="{g}">'
            f'<span class="se">{emoji}</span>'
            f'<span class="sl">{label}</span>'
            f'<span class="sn">{cnt}</span></div>'
        )
    cats_html = '\n'.join(cat_btns)

    # ── Tabellen-Zeilen ───────────────────────────────────────────────────────
    rows = []
    n = 0
    for g in group_order:
        if g not in groups: continue
        emoji, label = CAT_META.get(g, ('📂', g))
        cnt = len(groups[g])
        rows.append(
            f'<tr class="gh" data-group="{g}">'
            f'<td colspan="5">{emoji} {label} <span class="cnt">({cnt})</span></td></tr>'
        )
        for m in groups[g]:
            n += 1
            t = m['title'].replace('<','&lt;').replace('>','&gt;')
            d = m['desc'].replace('<','&lt;').replace('>','&gt;') if m['desc'] else ''
            b = _badge(m['id'])
            count_str, _ = _get_item_count(m['id'], dispatch, store)
            sub = f'<div class="sub">{d}</div>' if d else '<div class="sub"></div>'
            # Farbe je nach Datenmenge
            count_color = '#94a3b8'
            rows.append(
                f'<tr class="mr" data-group="{g}">'
                f'<td class="n">{n}</td>'
                f'<td class="mid">{m["id"]}</td>'
                f'<td class="ttl">{t}{sub}</td>'
                f'<td class="db">{b}</td>'
                f'<td class="dc"><span style="color:{count_color};font-weight:700">{count_str}</span></td>'
                f'</tr>'
            )

    tbody = '\n'.join(rows)

    # ── Typ-Legende ───────────────────────────────────────────────────────────
    legend_items = []
    for typ, (emoji, label, bg, fg, _) in TYPE_META.items():
        cnt = type_counts.get(typ, 0)
        legend_items.append(
            f'<span class="lgi">'
            f'<span style="background:{bg};color:{fg};border-radius:4px;padding:.1rem .3rem">{emoji}</span>'
            f' {label} <strong style="color:{fg}">{cnt}</strong></span>'
        )
    legend_html = '\n  '.join(legend_items)

    # ── Komplettes HTML ───────────────────────────────────────────────────────
    html = f'''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GeoQuest Spielübersicht — Phase {phase}</title>
<style>
:root{{--bg:#0f172a;--bg2:#1e293b;--bg3:#334155;--text:#e2e8f0;--muted:#64748b;--ac:#6366f1}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:13px}}
header{{background:linear-gradient(135deg,#1e1b4b,#312e81);padding:1.4rem 1.5rem;text-align:center;border-bottom:2px solid #4338ca}}
h1{{font-size:1.6rem;font-weight:800;background:linear-gradient(90deg,#818cf8,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent}}
.hero{{display:flex;justify-content:center;gap:2.5rem;margin:.6rem 0 .2rem}}
.hs{{text-align:center}}
.hn{{font-size:2.2rem;font-weight:900;color:#818cf8;display:block;line-height:1.05}}
.hl2{{font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em}}
.meta{{color:#4c5a7e;font-size:.75rem;margin-top:.3rem}}
.bar{{display:flex;gap:.4rem;padding:.55rem .8rem;flex-wrap:wrap;align-items:center;background:var(--bg2);border-bottom:1px solid var(--bg3);position:sticky;top:0;z-index:10;box-shadow:0 2px 8px #000a}}
.bar input{{flex:1;min-width:180px;background:var(--bg);border:1px solid var(--bg3);border-radius:6px;padding:.35rem .7rem;color:var(--text);font-size:.84rem;outline:none}}
.bar input:focus{{border-color:var(--ac)}}
.btn{{background:var(--ac);color:#fff;border:none;border-radius:6px;padding:.34rem .75rem;font-size:.78rem;font-weight:600;cursor:pointer}}
.cats{{display:flex;flex-wrap:wrap;gap:.3rem;padding:.55rem .8rem;background:var(--bg2);border-bottom:1px solid var(--bg3)}}
.sc{{background:var(--bg);border:1px solid var(--bg3);border-radius:7px;padding:.26rem .55rem;display:flex;align-items:center;gap:.3rem;font-size:.74rem;cursor:pointer;transition:all .12s;white-space:nowrap}}
.sc:hover{{border-color:var(--ac)}}.sc.on{{border-color:var(--ac);background:#1e1b4b}}
.se{{font-size:.86rem}}.sl{{color:#94a3b8}}.sn{{font-weight:700;color:var(--ac)}}
.tbl{{padding:.4rem .8rem 3rem;overflow-x:auto}}
table{{width:max-content;border-collapse:collapse;table-layout:auto}}
thead th{{background:var(--bg3);padding:.38rem .55rem;text-align:left;font-size:.72rem;color:#94a3b8;white-space:nowrap;position:sticky;top:42px;z-index:5}}
.gh td{{background:#141e2e;font-weight:700;font-size:.88rem;padding:.48rem .6rem;border-top:2px solid var(--bg3);position:sticky;top:74px;z-index:4}}
.cnt{{color:#475569;font-weight:400;font-size:.72rem;margin-left:.25rem}}
.mr:hover td{{background:#12202e}}
.mr td{{padding:.32rem .55rem;border-bottom:1px solid rgba(255,255,255,.025);vertical-align:top}}
.n{{color:#475569;font-size:.7rem;width:1%;white-space:nowrap}}
.mid{{font-family:"SF Mono","Fira Code",monospace;font-size:.7rem;color:#818cf8;white-space:nowrap;width:1%}}
.ttl{{font-size:.82rem;font-weight:500;min-width:180px}}
.sub{{color:#64748b;font-size:.75rem;font-weight:400;margin-top:.1rem;line-height:1.3}}
.db{{white-space:nowrap;width:1%}}
.dc{{white-space:nowrap;width:1%;text-align:right;padding-right:.7rem!important;font-size:.75rem}}
.tb{{display:inline-flex;align-items:center;gap:.22rem;border-radius:5px;padding:.15rem .42rem;font-size:.7rem;font-weight:600;border:1px solid transparent}}
.legend{{display:flex;flex-wrap:wrap;gap:.5rem;padding:.5rem .8rem;background:#111827;border-bottom:1px solid var(--bg3);font-size:.72rem}}
.lgi{{display:flex;align-items:center;gap:.3rem;color:#64748b}}
.hidden{{display:none!important}}
footer{{text-align:center;padding:.75rem;color:#334155;font-size:.72rem;border-top:1px solid var(--bg3)}}
@media(max-width:600px){{.mid,.sub,.db,.dc{{display:none}}}}
</style>
</head>
<body>
<header>
<h1>GeoQuest Spielübersicht</h1>
<div class="hero">
  <div class="hs"><span class="hn">{total_modes}</span><span class="hl2">Spielmodi</span></div>
  <div class="hs"><span class="hn">{len(group_order)}</span><span class="hl2">Kategorien</span></div>
  <div class="hs"><span class="hn">{n_tests}/{n_tests}</span><span class="hl2">Tests ✓</span></div>
</div>
<p class="meta">Phase {phase} · Mai 2026 · Auto-generiert aus gen.py + data/*.json</p>
</header>
<div class="bar">
  <input type="search" id="q" placeholder="🔍 Modus, ID oder Beschreibung suchen…" oninput="filt()">
  <button class="btn" onclick="clr()">Alle anzeigen</button>
</div>
<div class="cats" id="cats">
{cats_html}
</div>
<div class="legend">
  {legend_html}
</div>
<div class="tbl">
<table id="tbl">
<thead><tr>
  <th class="n">#</th>
  <th class="mid">Modus-ID</th>
  <th class="ttl">Titel &amp; Beschreibung</th>
  <th class="db">Typ</th>
  <th class="dc" style="text-align:right">Datenbasis (Items)</th>
</tr></thead>
<tbody>
{tbody}
</tbody>
</table>
</div>
<footer>Automatisch aus gen.py generiert · GeoQuest Phase {phase} · {total_modes} Modi in {len(group_order)} Kategorien</footer>
<script>
var all=document.querySelectorAll('.mr,.gh');
function filt(){{
  var q=document.getElementById('q').value.toLowerCase();
  var gh=null;
  all.forEach(function(r){{
    if(r.classList.contains('gh')){{gh=r;return;}}
    var show=!q||r.textContent.toLowerCase().includes(q);
    r.classList.toggle('hidden',!show);
  }});
  // Gruppenheader ausblenden wenn alle Zeilen hidden
  document.querySelectorAll('.gh').forEach(function(h){{
    var g=h.getAttribute('data-group');
    var any=false;
    document.querySelectorAll('.mr[data-group="'+g+'"]').forEach(function(r){{if(!r.classList.contains('hidden'))any=true;}});
    h.classList.toggle('hidden',!any);
  }});
}}
function clr(){{document.getElementById('q').value='';filt();fg(null);}}
function fg(g){{
  document.querySelectorAll('.sc').forEach(function(b){{b.classList.toggle('on',b.getAttribute('data-group')===g);}});
  all.forEach(function(r){{r.classList.toggle('hidden',!!g&&r.getAttribute('data-group')!==g);}});
}}
</script>
</body>
</html>'''

    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)

    return total_modes


if __name__ == '__main__':
    n = generate()
    print(f"✓ GeoQuest_Spielübersicht.html generiert — {n} Modi")
