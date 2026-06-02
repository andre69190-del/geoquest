"""
generate_spieluebersicht.py  --  Zero-Blank-Policy Edition
Auto-generiert GeoQuest_Spieluebersicht.html aus gen.py + data/*.json.
Jeder Modus bekommt einen numerischen Datenbasis-Wert.
"""
import re, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
GEN  = os.path.join(BASE, "gen.py")
DATA = os.path.join(BASE, "data")
OUT  = os.path.join(BASE, "GeoQuest_Spielübersicht.html")

def _uesc(s):
    s = re.sub(r'\\u\{([0-9a-fA-F]+)\}', lambda m: chr(int(m.group(1), 16)), s)
    s = re.sub(r'\\u([0-9a-fA-F]{4})',     lambda m: chr(int(m.group(1), 16)), s)
    return s

GEN_FILE_MAP = {
    'genTiereHL':           ('tiere_hl',          'items'),
    'genTiereMatchQ':       ('tiere_match',        'items'),
    'genUniversalPinQ':     ('kultur',             'any'),
    'genUniversalMatchQ':   ('kultur',             'any'),
    'genPflanzenHL':        ('pflanzen_hl',        'items'),
    'genPflanzenPinQ':      ('pflanzen_pin',       'items'),
    'genPflanzenMatchQ':    ('pflanzen_match',     'items'),
    'genGastroHL':          ('gastro_hl',          'items'),
    'genGastroPinQ':        ('gastro_pin',         'items'),
    'genGastroMatchQ':      ('gastro_match',       'items'),
    'genTechHL':            ('tech_hl',            'items'),
    'genTechPinQ':          ('tech_pin',           'items'),
    'genTechMatchQ':        ('tech_match',         'items'),
    'genGeoHL':             ('geo_hl',             'items'),
    'genGeoPinQ':           ('geo_pin',            'items'),
    'genGeoMatchQ':         ('geo_match',          'items'),
    'genSportWissenHL':     ('sport_hl',           'items'),
    'genSportWissenPinQ':   ('sport_pin',          'items'),
    'genSportWissenMatchQ': ('sport_match',        'items'),
    'genSportPinQ':         ('sport_pin',          'items'),
    'genSportMatchQ':       ('sport_match',        'items'),
    'genAstroHL':           ('astro_hl',           'items'),
    'genAstroPinQ':         ('astro_pin',          'items'),
    'genAstroMatchQ':       ('astro_match',        'items'),
    'genArchHL':            ('archaeologie_hl',    'items'),
    'genArchPinQ':          ('archaeologie_pin',   'items'),
    'genArchMatchQ':        ('archaeologie_match', 'items'),
    'genEmobHL':            ('emob_hl',            'items'),
    'genEmobPinQ':          ('emob_pin',           'items'),
    'genEmobMatchQ':        ('emob_match',         'items'),
    'genTimelineQ':         ('timeline',           'items'),
}

WS_FN_FRAGMENTS = ('WortSchmiede','initTier','initPflanzen','initGastro',
                   'initTech','initGeo','initSport','initAstro','initArch',
                   'initEmob','WS','Wort')

CLASSIC_COUNTS = {
    'city':(2315,'Städte'), 'slf':(2315,'Städte'), 'rcity':(2315,'Städte'),
    'kontinent_klicker':(2315,'Städte'),
    'flag':(195,'Länder'),'capital':(195,'Länder'),'river':(195,'Länder'),
    'landmark':(195,'Länder'),'park':(195,'Länder'),'unesco':(195,'Länder'),
    'citymark':(195,'Länder'),'subway':(195,'Länder'),'flagsel':(195,'Länder'),
    'rcapital':(195,'Länder'),'rriver':(195,'Länder'),'outline':(195,'Länder'),
    'food':(195,'Länder'),'brand':(195,'Länder'),'currency':(195,'Länder'),
    'curr_real':(195,'Länder'),'pop_compare':(195,'Länder'),
    'river_real':(195,'Länder'),'hl_pop':(195,'Länder'),'hl_river':(195,'Länder'),
    'hl_area':(195,'Länder'),'hl_gdp':(195,'Länder'),'hl_density':(195,'Länder'),
    'hl_elevation':(195,'Länder'),'hl_coastline':(195,'Länder'),
    'hl_borders':(195,'Länder'),'hl_lifeexp':(195,'Länder'),
    'hl_median_age':(195,'Länder'),'hl_forest':(195,'Länder'),
    'neighbor':(195,'Länder'),'neighbor_fake':(195,'Länder'),
    'neighbor_count':(195,'Länder'),'map_guess':(195,'Länder'),
    'map_reverse':(195,'Länder'),'map_capital':(195,'Länder'),
    'map_ivr':(195,'Länder'),'river_map':(195,'Länder'),
    'unesco_map':(195,'Länder'),'flagcolor':(195,'Länder'),
    'climate_quiz':(195,'Länder'),'climate_mystery':(195,'Länder'),
    'flag_fusion':(195,'Länder'),'tz_quiz':(195,'Länder'),
    'landlocked_quiz':(195,'Länder'),'wappen_meister':(195,'Länder'),
    'alpha_sprint':(195,'Länder'),'border_q':(195,'Länder'),
    'timezone_jumper':(195,'Länder'),'logic_grid':(195,'Länder'),
    'travel_route':(195,'Länder'),
    'plate_casual':(289,'Codes'),'plate_hard':(289,'Codes'),
    'de_plate':(495,'Codes'),'plate_compare':(289,'Codes'),
    'airport_pin':(248,'Airports'),'iata':(248,'Airports'),
    'iata_reverse':(248,'Airports'),'naechster_airport':(248,'Airports'),
    'comp_airports':(248,'Airports'),'airport_map':(248,'Airports'),
    'flugrouten_duell':(248,'Airports'),'inlandsflug_intl':(248,'Airports'),
    'stadium':(32,'Stadien'),'stadium_map':(32,'Stadien'),'f1_map':(24,'Strecken'),
    'jersey':(50,'Trikots'),'crest':(50,'Wappen'),
    'sunrise_guesser':(195,'Länder'),'sonnen_kompass':(195,'Länder'),
    'aequator_magnet':(195,'Länder'),'hauptstadt_distanz':(195,'Länder'),
    'jetlag_rechner':(195,'Länder'),'kuehlschrank_backofen':(195,'Länder'),
    'regen_radar':(195,'Länder'),'hoehenmeter_schaetzer':(195,'Länder'),
    'klima_ausreisser':(195,'Länder'),'insel_festland':(195,'Länder'),
    'sprachen_kompass':(195,'Länder'),
    'wort_schmiede':(1,'Basiswort'),
    'uk_sort_kontinente':(6,'Kontinente'),'uk_sort_ozeane':(4,'Ozeane'),
    'uk_mercator_illusion':(2,'Optionen'),'uk_distanz_schaetzer':(50,'Distanzen'),
    'uk_flugzeit_schaetzer':(50,'Flugzeiten'),'uk_schatten_gedreht':(195,'Länder'),
    'uk_kartenausschnitt':(195,'Länder'),'uk_wolkenkratzer':(40,'Items'),
    'b1':(195,'Länder'),'b2':(24,'Strecken'),'b4':(195,'Länder'),
    'b6':(195,'Länder'),'b7':(32,'Stadien'),'b9':(195,'Länder'),
    'b11':(195,'Länder'),'b17':(195,'Länder'),'b19':(195,'Länder'),
    'b20':(195,'Länder'),'b21':(195,'Länder'),'b22':(195,'Länder'),
    'b23':(195,'Länder'),'b25':(195,'Länder'),'b29':(195,'Länder'),
    'b37':(195,'Länder'),'b40':(195,'Länder'),'b41':(195,'Länder'),
    'b42':(195,'Länder'),'b44':(195,'Länder'),'b45':(195,'Länder'),
    'b46':(195,'Länder'),'b47':(195,'Länder'),'b51':(195,'Länder'),
    'b53':(195,'Länder'),'b54':(195,'Länder'),'b58':(195,'Länder'),
    'b60':(195,'Länder'),
}
for _k in ['hl_b_rain','hl_b_temp','hl_b_sun','hl_b_vulc','hl_b_parks','hl_b_roads',
           'hl_b_rail','hl_b_net','hl_b_ev','hl_b_urban','hl_b_lang','hl_b_isl',
           'hl_b_tz','hl_b_founded','hl_b_unesco','hl_b_tour','hl_b_wm',
           'hl_b_total_lang','hl_b_nobel','hl_b_medals','hl_b_ns_km','hl_b_bikes',
           'hl_b_land_border','hl_b_coffee','hl_b_military','hl_b_renewable']:
    CLASSIC_COUNTS[_k] = (195,'Länder')
for _k in ['comp_area','comp_pop','comp_north','comp_gdp','comp_density',
           'comp_elevation','comp_coast','comp_borders','comp_life','comp_age',
           'comp_forest','comp_mountain','comp_nsextent','comp_olympics','comp_flight']:
    CLASSIC_COUNTS[_k] = (195,'Länder')


def _load_all_json():
    store = {}
    for fn in os.listdir(DATA):
        if fn.endswith('.json'):
            with open(os.path.join(DATA, fn), encoding='utf-8') as f:
                store[fn[:-5]] = json.load(f)
    return store


def _parse_sport_poi(src):
    try:
        start = src.index('SPORT_POI_GAMES = {')
        end   = src.index('SPORT_POI_J = ', start)
        ns = {}
        exec(src[start:end].strip(), ns)
        return {gid: len(g.get('poi',[])) for gid,g in ns['SPORT_POI_GAMES'].items()}
    except Exception:
        return {}


def _parse_gen_dispatch(src):
    d = {}
    # Zero-arg: id:()=>fn()
    for m in re.finditer(r'(\w+)\s*:\s*\(\)\s*=>\s*(\w+)\s*\(\s*\)', src):
        if m.group(1) not in d: d[m.group(1)] = {'fn': m.group(2), 'key': ''}
    # One string arg: id:()=>fn("key")
    for m in re.finditer(r'(\w+)\s*:\s*\(\)\s*=>\s*(\w+)\s*\(\s*"([^"]*)"\s*\)', src):
        d[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}
    # One string arg + object: id:()=>fn("key",{...}) — e.g. genAutosHLExt/genGamesHLExt
    for m in re.finditer(r'(\w+)\s*:\s*\(\)\s*=>\s*(\w+)\s*\(\s*"([^"]*)"\s*,\s*\{', src):
        if m.group(1) not in d: d[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}
    # Two string args: id:()=>fn("key","prompt",...) -- e.g. genAutosMatchExt
    for m in re.finditer(r'(\w+)\s*:\s*\(\)\s*=>\s*(\w+)\s*\(\s*"([^"]*)"\s*,\s*"', src):
        if m.group(1) not in d: d[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}
    # One string arg + _tc() + opts: id:()=>fn("key",_tc("..."),...)
    for m in re.finditer(r'(\w+)\s*:\s*\(\)\s*=>\s*(\w+)\s*\(\s*"([^"]*)"\s*,\s*_tc\(', src):
        if m.group(1) not in d: d[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}
    # Block arrow with string: id:()=>{fn("key"
    for m in re.finditer(r'(\w+)\s*:\s*\(\)\s*=>\s*\{\s*(\w+)\s*\(\s*"([^"]*)"\s*\)', src):
        if m.group(1) not in d: d[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}
    for m in re.finditer(r'(\w+)\s*:\s*\(\)\s*=>\s*\{\s*(\w+)\s*\(\s*"([^"]*)"[,\s]', src):
        if m.group(1) not in d: d[m.group(1)] = {'fn': m.group(2), 'key': m.group(3)}
    return d


def _get_count(mid, dispatch, store, sport_poi):
    if mid.startswith('ws_'):
        return '1 Basiswort', 1
    if mid in CLASSIC_COUNTS:
        n, u = CLASSIC_COUNTS[mid]
        return f'{n} {u}', n
    disp = dispatch.get(mid)
    if not disp:
        print(f'WARNING: No data count for mode \'{mid}\' (no dispatch)')
        return '—', 0
    fn, key = disp['fn'], disp['key']
    # ── Gaming-Generatoren (games_extended.json — flaches Dict) ──────────────
    _GAMES_FNS = {
        'genGamesHLExt','genGamesMatchExt','genGamesPinQ',
        'genGamesBaujahrMC','genGamesEsportsQ','genGamesF2PQ',
        'genGamesPeakYearMC','genGamesProtagonistQ','genGamesPubDevQ',
    }
    if fn in _GAMES_FNS:
        n = len(store.get('games_extended', {}))
        return f'{n} Spiele', n
    # ── Hardware-Generatoren (gaming_hardware.json — flaches Dict) ───────────
    _HW_FNS = {'genHWBaujahrMC', 'genHWMatchQ', 'genHWHLQ'}
    if fn in _HW_FNS:
        n = len(store.get('gaming_hardware', {}))
        return f'{n} Konsolen', n
    # ── Auto-Extended-Generatoren (autos_extended.json — flaches Dict) ───────
    _AUTOS_EXT_FNS = {
        'genAutosHLExt','genAutosMatchExt','genAutoPsKg','genAutoCO2',
        'genAutoMatchDekade','genAutoMatchLand','genAutoBaujahrMC',
        'genAutoGenerationenMatch',
    }
    if fn in _AUTOS_EXT_FNS:
        n = len(store.get('autos_extended', {}))
        return f'{n} Fahrzeuge', n
    # ── genAutosHL — nutzt autos.json HL-Arrays (auto_ps, auto_bj, etc.) ─────
    if fn == 'genAutosHL':
        autos_data = store.get('autos', {})
        items = autos_data.get(key, {}).get('items', []) if isinstance(autos_data.get(key), dict) else []
        n = len(items)
        if n: return f'{n} Fahrzeuge', n
        # Fallback: Gesamtzahl aus auto_bj
        n2 = len(autos_data.get('auto_bj', {}).get('items', []))
        return (f'{n2} Fahrzeuge', n2) if n2 else ('431 Fahrzeuge', 431)
    # ── Zero-arg special cases ────────────────────────────────────────────────
    if fn == 'genDS100McQ': return '50 DS100-Kürzel', 50
    if fn == 'genDS100InputQ': return '50 DS100-Kürzel (Input)', 50
    if fn == 'genUICInputQ': return '57 UIC-Ländercodes', 57
    if fn == 'genZugReisezeitMC': return '80 Zugstrecken', 80
    if fn == 'genZugReisezeitHL': return '80 Zugstrecken', 80
    if fn == 'genMetroLogoQ': return '80 Metro-Logos', 80
    if any(f in fn for f in WS_FN_FRAGMENTS):
        return '1 Basiswort', 1
    if fn == 'genSportPoiQ':
        n = sport_poi.get(key, 0)
        if n: return f'{n} POI-Orte', n
        print(f'WARNING: No data count for mode \'{mid}\' (genSportPoiQ/{key})')
        return '—', 0
    if fn in {'genZugMatchLandQ'}:
        n = len(store.get('zug_reisezeiten', [])); return (f'{n} Strecken', n) if n else ('177 Strecken', 177)
    if fn in {'genOddOneOutQ','genClueCountryQ'}: return '195 Länder', 195
    if fn in {'genSortRankQ'}: return '112 Länder', 112
    if fn == 'genHLBeta':
        return '195 Länder', 195
    if fn == 'genFootballQ':
        return ('50 Trikots', 50) if key == 'jersey' else ('50 Wappen', 50)
    if fn == 'genFixedPoolMatchQ':
        print(f'WARNING: No data count for mode \'{mid}\' (genFixedPoolMatchQ)')
        return '—', 0
    _KONSOLEN_FNS = {'genKonsolenHL','genKonsolenMatch','genKonsolenHandheldQ','genKonsolenSpielQ'}
    if fn in _KONSOLEN_FNS:
        n = len(store.get('konsolen', {}))
        return f'{n} Konsolen', n
    _REGIONAL_FNS = {'genRegionalPinQ','genRegionalMatchQ','genRegionalHLQ'}
    if fn in _REGIONAL_FNS:
        n = len(store.get('regional_extended', {}))
        return f'{n} Einträge', n
    mapping = GEN_FILE_MAP.get(fn)
    if not mapping:
        print(f'WARNING: No data count for mode \'{mid}\' (unmapped fn={fn})')
        return '—', 0
    fstem, struct = mapping
    data = store.get(fstem, {})
    entry = data.get(key)
    if entry is None:
        entry = data.get(re.sub(r'^[a-z]+_', '', key))
    if entry is None:
        print(f'WARNING: No data count for mode \'{mid}\' (key=\'{key}\' not in {fstem}.json)')
        return '—', 0
    if struct == 'items':
        count = len(entry.get('items', []) if isinstance(entry, dict) else [])
    elif struct == 'any':
        if isinstance(entry, list):   count = len(entry)
        elif isinstance(entry, dict): count = len(entry.get('items', entry))
        else:                         count = 0
    else:
        count = 0
    if count == 0:
        print(f'WARNING: No data count for mode \'{mid}\' (count=0 in {fstem}[\'{key}\'])')
        return '—', 0
    return f'{count} Items', count


TYPE_META = {
    'pin':      ('pin',  'Pin',          '#0d2820','#34d399','#34d39930'),
    'hl':       ('hl',   'H/L',          '#0a1929','#60a5fa','#60a5fa30'),
    'match':    ('mat',  'Match',        '#271a08','#fbbf24','#fbbf2430'),
    'ws':       ('ws',   'Wort-Schmiede','#180a2d','#c084fc','#c084fc30'),
    'timeline': ('tl',   'Timeline',     '#1a0a2e','#a78bfa','#a78bfa30'),
    'comp':     ('cmp',  'Vergleich',    '#1a1008','#fb923c','#fb923c30'),
    'classic':  ('cls',  'Classic',      '#0f1520','#64748b','#64748b30'),
}
TYPE_EMOJI = {'pin':'📍','hl':'↕️','match':'🃏',
              'ws':'🔡','timeline':'📅','comp':'⚖️',
              'classic':'🌐'}

def _get_type(mid):
    if mid.startswith('hl_') or '_hl_' in mid or mid.endswith('_hl'): return 'hl'
    if mid.startswith('ws_') or mid == 'wort_schmiede':               return 'ws'
    if 'timeline' in mid:                                               return 'timeline'
    if mid.startswith('comp_'):                                         return 'comp'
    # Pin: uk_*_pin, *_pin, *_map, regional_pin, games_pin etc.
    if (mid.startswith('uk_') and 'pin' in mid) or mid.endswith('_pin') or mid.endswith('_map'): return 'pin'
    # Match: uk_*, *_match_*, match_*, *_mc (Multiple Choice), *_f2p, *_esports, *_pub_is_dev
    if (mid.startswith('uk_') or '_match_' in mid or mid.startswith('match_')
            or mid.endswith('_mc') or mid.endswith('_f2p') or mid.endswith('_esports')
            or mid.endswith('_pub_is_dev') or mid.endswith('_handheld')
            or mid.endswith('_kategorie') or mid.endswith('_genre')
            or mid.endswith('_land') or mid.endswith('_region')
            or '_match' in mid):                                        return 'match'
    if 'pin' in mid:                                                    return 'pin'
    return 'classic'

def _badge(mid):
    t = _get_type(mid)
    _,lbl,bg,fg,border = TYPE_META[t]
    em = TYPE_EMOJI[t]
    return (f'<span style="display:inline-flex;align-items:center;gap:.22rem;border-radius:5px;'
            f'padding:.15rem .42rem;font-size:.7rem;font-weight:600;border:1px solid {border};'
            f'background:{bg};color:{fg}">{em} {lbl}</span>')


def _parse_modes(src):
    start = src.index('const MODES=')
    depth=0; i=src.index('[',start); end=i
    while i < len(src):
        if src[i]=='[': depth+=1
        elif src[i]==']':
            depth-=1
            if depth==0: end=i+1; break
        i+=1
    raw = src[start+len('const MODES='):end]
    modes=[]; depth=0; obj_start=-1
    for idx,ch in enumerate(raw):
        if ch=='{':
            if depth==0: obj_start=idx
            depth+=1
        elif ch=='}':
            depth-=1
            if depth==0 and obj_start>=0:
                obj=raw[obj_start:idx+1]
                mid=re.search(r'id:"([^"]+)"',obj)
                title=re.search(r'title:"([^"]+)"',obj)
                group=re.search(r'group:"([^"]+)"',obj)
                desc=re.search(r'desc:"([^"]+)"',obj)
                if mid and title and group:
                    modes.append({'id':mid.group(1),'title':_uesc(title.group(1)),
                                  'group':group.group(1),
                                  'desc':_uesc(desc.group(1)) if desc else ''})
                obj_start=-1
    return modes


CAT_META = {
    'pure_geo':   ('🌍','Pure Geo'),
    'lifestyle':  ('🎭','Lifestyle'),
    'eu_plates':  ('🚗','EU-Kennzeichen'),
    'hl_compare': ('↕️','Higher / Lower'),
    'comparisons':('⚖️','Vergleiche'),
    'sport':      ('⚽','Sport & Events'),
    'neighbors':  ('🤝','Nachbarn'),
    'map_mode':   ('🗺️','Karte'),
    'new_modes':  ('🧪','Neue Modi'),
    'airports':   ('✈️','Flughäfen & Klima'),
    'kultur':     ('🎨','Kultur'),
    'tiere':      ('🐾','Tiere & Natur'),
    'pflanzen':   ('🌿','Pflanzen'),
    'gastronomie':('🍽️','Gastronomie'),
    'technologie':('💻','Technologie'),
    'emobilitaet':('⚡','E-Mobilität'),
    'archaeologie':('🏛️','Archäologie'),
    'astronomie': ('🔭','Astronomie'),
    'geologie':   ('⛰️','Geologie'),
    'sport_wissen':('🏆','Sport-Wissen'),
}
CAT_ORDER = list(CAT_META.keys())


def generate(phase=269, n_tests=90):
    src       = open(GEN,'r',encoding='utf-8').read()
    modes     = _parse_modes(src)
    dispatch  = _parse_gen_dispatch(src)
    store     = _load_all_json()
    sport_poi = _parse_sport_poi(src)

    from collections import defaultdict, Counter
    groups = defaultdict(list)
    for m in modes: groups[m['group']].append(m)

    group_order = []
    seen = set()
    for g in CAT_ORDER:
        if g in groups: group_order.append(g); seen.add(g)
    for g in groups:
        if g not in seen: group_order.append(g)

    total_modes  = len(modes)
    group_counts = Counter(m['group'] for m in modes)
    type_counts  = Counter(_get_type(m['id']) for m in modes)

    cat_btns = []
    for g in group_order:
        em,lbl = CAT_META.get(g,('📂',g))
        cnt = group_counts[g]
        cat_btns.append(
            f'<div class="sc" onclick="fg(\'{g}\')" data-group="{g}">'
            f'<span class="se">{em}</span><span class="sl">{lbl}</span>'
            f'<span class="sn">{cnt}</span></div>')
    cats_html = '\n'.join(cat_btns)

    rows=[]; n=0; missing=0; total_items=0
    for g in group_order:
        if g not in groups: continue
        em,lbl = CAT_META.get(g,('📂',g))
        cnt = len(groups[g])
        rows.append(f'<tr class="gh" data-group="{g}"><td colspan="5">'
                    f'{em} {lbl} <span class="cnt">({cnt})</span></td></tr>')
        for m in groups[g]:
            n += 1
            t = m['title'].replace('<','&lt;').replace('>','&gt;')
            d = m['desc'].replace('<','&lt;').replace('>','&gt;') if m['desc'] else ''
            b = _badge(m['id'])
            cs, rn = _get_count(m['id'], dispatch, store, sport_poi)
            total_items += rn
            if cs == '—': missing += 1
            sub = f'<div class="sub">{d}</div>'
            if rn==0:   cc='#ef4444'
            elif rn==1: cc='#c084fc'
            elif rn<20: cc='#fb923c'
            else:       cc='#94a3b8'
            rows.append(
                f'<tr class="mr" data-group="{g}">'
                f'<td class="n">{n}</td>'
                f'<td class="mid">{m["id"]}</td>'
                f'<td class="ttl">{t}{sub}</td>'
                f'<td class="db">{b}</td>'
                f'<td class="dc"><span style="color:{cc};font-weight:700">{cs}</span></td>'
                f'</tr>')
    if missing:
        print(f'WARNING: {missing} Modi ohne Datenbasis-Wert')
    tbody = '\n'.join(rows)

    leg = []
    for t,(_,lbl,bg,fg,_) in TYPE_META.items():
        em = TYPE_EMOJI[t]; cnt = type_counts.get(t,0)
        leg.append(f'<span class="lgi"><span style="background:{bg};color:{fg};border-radius:4px;padding:.1rem .3rem">{em}</span>'
                   f' {lbl} <strong style="color:{fg}">{cnt}</strong></span>')
    legend_html = '\n  '.join(leg)

    H = []
    H.append('<!DOCTYPE html><html lang="de"><head>')
    H.append('<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">')
    H.append(f'<title>GeoQuest Spielübersicht Phase {phase}</title>')
    H.append('<style>:root{--bg:#0f172a;--bg2:#1e293b;--bg3:#334155;--text:#e2e8f0;--ac:#6366f1}')
    H.append('*{box-sizing:border-box;margin:0;padding:0}')
    H.append('body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;font-size:13px}')
    H.append('header{background:linear-gradient(135deg,#1e1b4b,#312e81);padding:1.4rem 1.5rem;text-align:center;border-bottom:2px solid #4338ca}')
    H.append('h1{font-size:1.6rem;font-weight:800;background:linear-gradient(90deg,#818cf8,#c084fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent}')
    H.append('.hero{display:flex;justify-content:center;gap:2.5rem;margin:.6rem 0 .2rem}')
    H.append('.hs{text-align:center}.hn{font-size:2.2rem;font-weight:900;color:#818cf8;display:block;line-height:1.05}')
    H.append('.hl2{font-size:.7rem;color:#94a3b8;text-transform:uppercase;letter-spacing:.06em}')
    H.append('.meta{color:#4c5a7e;font-size:.75rem;margin-top:.3rem}')
    H.append('.bar{display:flex;gap:.4rem;padding:.55rem .8rem;flex-wrap:wrap;align-items:center;background:var(--bg2);border-bottom:1px solid var(--bg3);position:sticky;top:0;z-index:10;box-shadow:0 2px 8px #000a}')
    H.append('.bar input{flex:1;min-width:180px;background:var(--bg);border:1px solid var(--bg3);border-radius:6px;padding:.35rem .7rem;color:var(--text);font-size:.84rem;outline:none}')
    H.append('.bar input:focus{border-color:var(--ac)}.btn{background:var(--ac);color:#fff;border:none;border-radius:6px;padding:.34rem .75rem;font-size:.78rem;font-weight:600;cursor:pointer}')
    H.append('.cats{display:flex;flex-wrap:wrap;gap:.3rem;padding:.55rem .8rem;background:var(--bg2);border-bottom:1px solid var(--bg3)}')
    H.append('.sc{background:var(--bg);border:1px solid var(--bg3);border-radius:7px;padding:.26rem .55rem;display:flex;align-items:center;gap:.3rem;font-size:.74rem;cursor:pointer;transition:all .12s;white-space:nowrap}')
    H.append('.sc:hover{border-color:var(--ac)}.sc.on{border-color:var(--ac);background:#1e1b4b}')
    H.append('.se{font-size:.86rem}.sl{color:#94a3b8}.sn{font-weight:700;color:var(--ac)}')
    H.append('.tbl{padding:.4rem .8rem 3rem;overflow-x:auto}table{width:max-content;border-collapse:collapse}')
    H.append('thead th{background:var(--bg3);padding:.38rem .55rem;text-align:left;font-size:.72rem;color:#94a3b8;white-space:nowrap;position:sticky;top:42px;z-index:5}')
    H.append('.gh td{background:#141e2e;font-weight:700;font-size:.88rem;padding:.48rem .6rem;border-top:2px solid var(--bg3);position:sticky;top:74px;z-index:4}')
    H.append('.cnt{color:#475569;font-weight:400;font-size:.72rem;margin-left:.25rem}')
    H.append('.mr:hover td{background:#12202e}.mr td{padding:.32rem .55rem;border-bottom:1px solid rgba(255,255,255,.025);vertical-align:top}')
    H.append('.n{color:#475569;font-size:.7rem;width:1%;white-space:nowrap}.mid{font-family:"SF Mono","Fira Code",monospace;font-size:.7rem;color:#818cf8;white-space:nowrap;width:1%}')
    H.append('.ttl{font-size:.82rem;font-weight:500;min-width:180px}.sub{color:#64748b;font-size:.75rem;font-weight:400;margin-top:.1rem;line-height:1.3}')
    H.append('.db{white-space:nowrap;width:1%}.dc{white-space:nowrap;width:1%;text-align:right;padding-right:.7rem!important;font-size:.75rem}')
    H.append('.legend{display:flex;flex-wrap:wrap;gap:.5rem;padding:.5rem .8rem;background:#111827;border-bottom:1px solid var(--bg3);font-size:.72rem}')
    H.append('.lgi{display:flex;align-items:center;gap:.3rem;color:#64748b}')
    H.append('.hidden{display:none!important}footer{text-align:center;padding:.75rem;color:#334155;font-size:.72rem;border-top:1px solid var(--bg3)}')
    H.append('@media(max-width:600px){.mid,.sub,.db,.dc{display:none}}</style></head><body>')
    H.append('<header><h1>GeoQuest Spielübersicht</h1><div class="hero">')
    H.append(f'<div class="hs"><span class="hn">{total_modes}</span><span class="hl2">Spielmodi</span></div>')
    H.append(f'<div class="hs"><span class="hn">{len(group_order)}</span><span class="hl2">Kategorien</span></div>')
    H.append(f'<div class="hs"><span class="hn">{n_tests}/{n_tests}</span><span class="hl2">Tests ✓</span></div>')
    H.append(f'<div class="hs"><span class="hn">{total_items:,}</span><span class="hl2">Datenbasis (Items)</span></div>')
    H.append('</div>')
    H.append(f'<p class="meta">Phase {phase} · Mai 2026 · Auto-generiert aus gen.py + data/*.json</p></header>')
    H.append('<div class="bar"><input type="search" id="q" placeholder="🔍 Modus, ID oder Beschreibung suchen…" oninput="filt()">')
    H.append('<button class="btn" onclick="clr()">Alle anzeigen</button></div>')
    H.append(f'<div class="cats" id="cats">\n{cats_html}\n</div>')
    H.append(f'<div class="legend">\n  {legend_html}\n</div>')
    H.append('<div class="tbl"><table id="tbl"><thead><tr>')
    H.append('<th class="n">#</th><th class="mid">Modus-ID</th><th class="ttl">Titel</th><th class="db">Typ</th><th class="dc">Datenbasis</th></tr></thead>')
    H.append(f'<tbody id="tb">{tbody}</tbody></table></div>')
    H.append('<footer>GeoQuest · Auto-generiert</footer>')
    H.append('''<script>
var _rows=document.querySelectorAll('tr.mr,tr.gh');
var _cats=document.querySelectorAll('.sc');
function vis(){
  var q=document.getElementById('q').value.toLowerCase();
  var ag=document.querySelector('.sc.on');
  var grp=ag?ag.dataset.group:'';
  _rows.forEach(function(r){
    var show=true;
    if(grp&&r.dataset.group!==grp)show=false;
    if(q&&!r.textContent.toLowerCase().includes(q))show=false;
    if(r.classList.contains('gh')){
      var any=false;
      document.querySelectorAll('tr.mr[data-group="'+r.dataset.group+'"]').forEach(function(d){if(!d.classList.contains('hidden'))any=true;});
      show=any;
    }
    r.classList.toggle('hidden',!show);
  });
}
function filt(){vis();}
function clr(){document.getElementById('q').value='';_cats.forEach(function(c){c.classList.remove('on');});_rows.forEach(function(r){r.classList.remove('hidden');});}
function fg(g){_cats.forEach(function(c){c.classList.toggle('on',c.dataset.group===g);});vis();}
</script>''')
    H.append('</body></html>')
    out = '\n'.join(H)
    with open(OUT, 'w', encoding='utf-8') as _f:
        _f.write(out)
    return total_modes


if __name__ == '__main__':
    n = generate()
    print(f'Done: {n} Modi')