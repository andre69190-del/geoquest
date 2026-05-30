#!/usr/bin/env python3
"""
patch_296_train_interactive.py — Phase 296.3
Fügt hinzu:
  kultur.json:  bahnhof_pin (80 Weltbahnhöfe mit Koordinaten)
  gen.py:       genDS100McQ() MC-Generator + 2 neue Modi
  zuege cats:   uk_bahnhof_pin, zug_ds100
"""
import json, sys, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KULTUR = os.path.join(BASE, 'data', 'kultur.json')
GEN    = os.path.join(BASE, 'gen.py')

# ─── 1. BAHNHOF-PIN DATEN (80 Items) ────────────────────────────────────────
BAHNHOF_PIN = [
    # Deutschland (20) — inkl. Pflicht-Einträge
    {"n": "Frankfurt (Main) Hbf", "lat": 50.107, "lng": 8.663},
    {"n": "München Hbf", "lat": 48.140, "lng": 11.558},
    {"n": "Hamburg Hbf", "lat": 53.553, "lng": 10.007},
    {"n": "Berlin Hbf", "lat": 52.525, "lng": 13.369},
    {"n": "Köln Hbf", "lat": 50.943, "lng": 6.959},
    {"n": "Mannheim Hbf", "lat": 49.479, "lng": 8.470},
    {"n": "Heidelberg Hbf", "lat": 49.404, "lng": 8.676},
    {"n": "Wiesloch-Walldorf Bhf", "lat": 49.291, "lng": 8.641},
    {"n": "Stuttgart Hbf", "lat": 48.784, "lng": 9.183},
    {"n": "Düsseldorf Hbf", "lat": 51.220, "lng": 6.794},
    {"n": "Leipzig Hbf", "lat": 51.347, "lng": 12.381},
    {"n": "Nürnberg Hbf", "lat": 49.446, "lng": 11.082},
    {"n": "Dresden Hbf", "lat": 51.040, "lng": 13.733},
    {"n": "Bremen Hbf", "lat": 53.083, "lng": 8.814},
    {"n": "Hannover Hbf", "lat": 52.377, "lng": 9.742},
    {"n": "Dortmund Hbf", "lat": 51.518, "lng": 7.460},
    {"n": "Freiburg (Breisgau) Hbf", "lat": 47.997, "lng": 7.840},
    {"n": "Erfurt Hbf", "lat": 50.972, "lng": 11.038},
    {"n": "Augsburg Hbf", "lat": 48.365, "lng": 10.886},
    {"n": "Karlsruhe Hbf", "lat": 48.994, "lng": 8.401},
    # Österreich (4)
    {"n": "Wien Hbf", "lat": 48.185, "lng": 16.376},
    {"n": "Wien Westbahnhof", "lat": 48.197, "lng": 16.338},
    {"n": "Salzburg Hbf", "lat": 47.813, "lng": 13.045},
    {"n": "Innsbruck Hbf", "lat": 47.263, "lng": 11.401},
    # Schweiz (3)
    {"n": "Zürich HB", "lat": 47.378, "lng": 8.540},
    {"n": "Bern Bahnhof", "lat": 46.949, "lng": 7.440},
    {"n": "Basel SBB", "lat": 47.547, "lng": 7.590},
    # Frankreich (4)
    {"n": "Paris Gare de Lyon", "lat": 48.845, "lng": 2.373},
    {"n": "Paris Gare du Nord", "lat": 48.881, "lng": 2.355},
    {"n": "Lyon Part-Dieu", "lat": 45.760, "lng": 4.860},
    {"n": "Marseille Saint-Charles", "lat": 43.303, "lng": 5.380},
    # UK (3)
    {"n": "London St Pancras International", "lat": 51.532, "lng": -0.123},
    {"n": "London Waterloo", "lat": 51.503, "lng": -0.113},
    {"n": "Edinburgh Waverley", "lat": 55.952, "lng": -3.190},
    # Niederlande / Belgien (3)
    {"n": "Amsterdam Centraal", "lat": 52.379, "lng": 4.900},
    {"n": "Brüssel Midi/Zuid", "lat": 50.836, "lng": 4.337},
    {"n": "Rotterdam Centraal", "lat": 51.924, "lng": 4.469},
    # Spanien / Portugal (3)
    {"n": "Madrid Atocha", "lat": 40.408, "lng": -3.690},
    {"n": "Barcelona Sants", "lat": 41.379, "lng": 2.140},
    {"n": "Lisboa Oriente", "lat": 38.768, "lng": -9.099},
    # Italien (3)
    {"n": "Roma Termini", "lat": 41.901, "lng": 12.501},
    {"n": "Milano Centrale", "lat": 45.486, "lng": 9.205},
    {"n": "Venezia Santa Lucia", "lat": 45.441, "lng": 12.321},
    # Skandinavien (4)
    {"n": "Oslo Sentralstasjon", "lat": 59.909, "lng": 10.750},
    {"n": "Bergen stasjon", "lat": 60.390, "lng": 5.333},
    {"n": "Stockholm Centralstation", "lat": 59.330, "lng": 18.058},
    {"n": "Kopenhagen Hauptbahnhof (København H)", "lat": 55.673, "lng": 12.565},
    # Osteuropa (5)
    {"n": "Praha hlavní nádraží (Prag)", "lat": 50.083, "lng": 14.435},
    {"n": "Kraków Główny (Krakau)", "lat": 50.067, "lng": 19.945},
    {"n": "Warschau Centralny", "lat": 52.229, "lng": 21.003},
    {"n": "Budapest Keleti", "lat": 47.500, "lng": 19.084},
    {"n": "Wien Franz-Josefs-Bahnhof", "lat": 48.232, "lng": 16.360},
    # Russland / Ukraine (2)
    {"n": "Moskau Jaroslawskij-Bahnhof", "lat": 55.774, "lng": 37.656},
    {"n": "Kiew Hauptbahnhof (Kyiv-Pasazhyrskyi)", "lat": 50.441, "lng": 30.487},
    # USA (5)
    {"n": "New York Grand Central Terminal", "lat": 40.753, "lng": -73.977},
    {"n": "Chicago Union Station", "lat": 41.879, "lng": -87.640},
    {"n": "Los Angeles Union Station", "lat": 34.056, "lng": -118.236},
    {"n": "Washington DC Union Station", "lat": 38.898, "lng": -77.007},
    {"n": "San Francisco Caltrain Depot", "lat": 37.776, "lng": -122.395},
    # Kanada (1)
    {"n": "Toronto Union Station", "lat": 43.645, "lng": -79.381},
    # Lateinamerika (3 — Pflichteinträge)
    {"n": "Estação da Luz (São Paulo)", "lat": -23.534, "lng": -46.644},
    {"n": "Central do Brasil (Rio de Janeiro)", "lat": -22.911, "lng": -43.174},
    {"n": "Estación Retiro (Buenos Aires)", "lat": -34.592, "lng": -58.374},
    # Japan (4)
    {"n": "Tokyo Station", "lat": 35.681, "lng": 139.766},
    {"n": "Shinjuku Station", "lat": 35.690, "lng": 139.700},
    {"n": "Osaka Station", "lat": 34.703, "lng": 135.496},
    {"n": "Kyoto Station", "lat": 34.986, "lng": 135.759},
    # China (3)
    {"n": "Beijing West Railway Station", "lat": 39.895, "lng": 116.322},
    {"n": "Shanghai Hongqiao Railway Station", "lat": 31.195, "lng": 121.317},
    {"n": "Guangzhou South Railway Station", "lat": 22.974, "lng": 113.267},
    # Indien (2)
    {"n": "Mumbai Chhatrapati Shivaji Maharaj Terminus", "lat": 18.940, "lng": 72.835},
    {"n": "New Delhi Railway Station", "lat": 28.642, "lng": 77.219},
    # Naher Osten / Afrika (3)
    {"n": "Dubai Union Station (Etihad Rail)", "lat": 25.179, "lng": 55.261},
    {"n": "Casablanca-Voyageurs (Marokko)", "lat": 33.594, "lng": -7.619},
    {"n": "Cairo Ramses Station (Ägypten)", "lat": 30.063, "lng": 31.248},
    # Australien (2)
    {"n": "Sydney Central Station", "lat": -33.883, "lng": 151.206},
    {"n": "Melbourne Southern Cross Station", "lat": -37.818, "lng": 144.953},
    # Türkei (1)
    {"n": "Istanbul Sirkeci (historisch)", "lat": 41.018, "lng": 28.974},
    # Griechenland (1)
    {"n": "Athen Larissa-Bahnhof", "lat": 37.995, "lng": 23.722},
    # Taiwan (1)
    {"n": "Taipei Main Station", "lat": 25.048, "lng": 121.517},
    # Südafrika (1)
    {"n": "Cape Town Station", "lat": -33.923, "lng": 18.424},
]
assert len(BAHNHOF_PIN) >= 80, f"bahnhof_pin: nur {len(BAHNHOF_PIN)} Items"

# ─── 2. KULTURDATEN PATCHEN ──────────────────────────────────────────────────
print("=" * 58)
print(" Phase 296.3 — Bahnhof-Pin & DS100-Modi")
print("=" * 58)

print("\n[1/3] kultur.json — bahnhof_pin ...")
with open(KULTUR, 'r', encoding='utf-8') as f:
    data = json.load(f)

if 'bahnhof_pin' in data:
    print("  [SKIP] bahnhof_pin already exists")
else:
    data['bahnhof_pin'] = BAHNHOF_PIN
    print(f"  [OK] bahnhof_pin: {len(BAHNHOF_PIN)} Bahnhöfe auf 5 Kontinenten")

with open(KULTUR, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("  [OK] kultur.json gespeichert")

# ─── 3. GEN.PY PATCHEN ───────────────────────────────────────────────────────
print("\n[2/3] gen.py — genDS100McQ() + MODES + dispatch ...")
with open(GEN, 'r', encoding='utf-8') as f:
    content = f.read()

already = 'uk_bahnhof_pin' in content

if already:
    print("  [SKIP] Modi bereits vorhanden")
else:
    # A: Generator-Funktion genDS100McQ() nach genUniversalMatchQ einfügen
    # DS100-Daten liegen in KULTUR_DATA.ds100 als [{q:"...", a:"..."}]
    DS100_FN = r"""
/* Phase 296.3: DS100 Multiple-Choice-Modus
   Zeigt Bahnhofsnamen → Spieler wählt das richtige Kürzel (4 ähnliche Optionen) */
function genDS100McQ(){
  const pool=KULTUR_DATA.ds100;
  if(!pool||pool.length<4)return null;
  const cor=pool[~~(rng()*pool.length)];
  if(!cor||!cor.q||!cor.a)return null;
  /* Distraktoren: gleicher Länder-Prefix bevorzugt (z.B. F* für FF) */
  const prefix=cor.a[0];
  const samePfx=pool.filter(x=>x.a!==cor.a&&x.a[0]===prefix);
  const others=sh(pool.filter(x=>x.a!==cor.a));
  const disPfx=sh(samePfx).slice(0,2).map(x=>x.a);
  const disRnd=sh(others.filter(x=>!disPfx.includes(x.a))).slice(0,3-disPfx.length).map(x=>x.a);
  const dis=sh([...disPfx,...disRnd]).slice(0,3);
  if(dis.length<3)return null;
  return{
    type:"ds100_mc",
    prompt:"Welches DS100-Betriebsstellenkürzel gehört zu diesem Bahnhof?",
    subj:cor.q,
    ans:cor.a,
    opts:sh([cor.a,...dis]),
    meta:"Deutsches Betriebsstellenkürzel",
    lid:"ds100_"+cor.a,
    cc:""
  };
}
"""
    # Füge nach der letzten genUniversalMatchQ-ähnlichen Funktion ein
    anchor_fn = '/* Phase 295: removed dead legacy quiz renderers'
    if anchor_fn in content:
        idx = content.find(anchor_fn)
        content = content[:idx] + DS100_FN + content[idx:]
        print("  [OK] genDS100McQ() Funktion eingefügt")
    else:
        # Alternative: nach genUniversalMatchQ Funktion
        anchor2 = 'function genUniversalMatchQ('
        idx2 = content.find(anchor2)
        end2 = content.find('\nfunction ', idx2 + 10)
        content = content[:end2] + DS100_FN + content[end2:]
        print("  [OK] genDS100McQ() Funktion eingefügt (alt anchor)")

    # B: Render-Zweig für ds100_mc in renderQ
    # ds100_mc ist ähnlich wie "de_plate" — zeigt Text, 4 Button-Optionen
    # → verwendet den Standard-MC-Pfad (qBody + opts buttons), kein neuer Zweig nötig
    # Wir registrieren ds100_mc als normaler MC-Typ indem wir qBody setzen
    # Das geschieht automatisch über den default renderQ Pfad

    # C: MODES Einträge
    ANCHOR_MODES = '{id:"zug_ds100"'
    if ANCHOR_MODES not in content:
        anchor_m = '{id:"ws_zug_acela"'
        if anchor_m in content:
            idx_m = content.find(anchor_m)
            line_end = content.find('\n', idx_m)
            NEW_MODES = (
                '\n    {id:"uk_bahnhof_pin",   icon:"\\u{1F689}",title:"Bahnhöfe weltweit",             '
                'group:"zuege",prompt:"\\u{1F4CD} Wo auf der Karte liegt dieser Bahnhof?",       '
                'desc:"Grand Central, Tokyo Station, Estação da Luz & 77 weitere"},\n'
                '    {id:"zug_ds100",          icon:"\\u{1F3AB}",title:"DS100 Kürzel-Quiz",              '
                'group:"zuege",prompt:"Welches Betriebsstellenkürzel hat dieser Bahnhof?",        '
                'desc:"FF=Frankfurt, MH=München — das Alphabet der Eisenbahn"},'
            )
            content = content[:line_end] + NEW_MODES + content[line_end:]
            print("  [OK] MODES Einträge eingefügt")
        else:
            print("  [WARN] MODES anchor nicht gefunden")

    # D: GEN dispatch
    ANCHOR_GEN = 'ws_zug_acela:()=>initTierWortSchmiede("zug_acela")'
    if ANCHOR_GEN in content:
        idx_g = content.find(ANCHOR_GEN)
        line_end_g = content.find('\n', idx_g)
        NEW_GEN = (
            '\n  uk_bahnhof_pin:()=>genUniversalPinQ("bahnhof_pin"),'
            '\n  zug_ds100:()=>genDS100McQ(),'
        )
        content = content[:line_end_g] + NEW_GEN + content[line_end_g:]
        print("  [OK] GEN dispatch eingefügt")
    else:
        print("  [WARN] GEN anchor nicht gefunden")

    # E: MODE_CATS zuege erweitern
    old_cats_end = '"ws_zug_acela"'
    if old_cats_end in content:
        # Finde die Stelle in MODE_CATS (nicht in MODES)
        cats_start = content.find('zuege:{label:')
        if cats_start > 0:
            cats_line_end = content.find('},', cats_start)
            # Prüfe ob uk_bahnhof_pin schon drin ist
            cats_snippet = content[cats_start:cats_line_end]
            if 'uk_bahnhof_pin' not in cats_snippet:
                insert_pos = content.rfind('"ws_zug_acela"', cats_start, cats_line_end)
                if insert_pos > 0:
                    after = insert_pos + len('"ws_zug_acela"')
                    content = content[:after] + ',"uk_bahnhof_pin","zug_ds100"' + content[after:]
                    print("  [OK] MODE_CATS zuege erweitert")
                else:
                    print("  [WARN] ws_zug_acela in cats nicht gefunden")

with open(GEN, 'w', encoding='utf-8') as f:
    f.write(content)

# ─── 4. VALIDIERUNG ──────────────────────────────────────────────────────────
print("\n[3/3] Validierung ...")
with open(GEN) as f: c2 = f.read()
checks = {
    'genDS100McQ() defined':      'function genDS100McQ(' in c2,
    'uk_bahnhof_pin MODES':       'id:"uk_bahnhof_pin"' in c2,
    'zug_ds100 MODES':            'id:"zug_ds100"' in c2,
    'uk_bahnhof_pin GEN':         'uk_bahnhof_pin:()=>genUniversalPinQ' in c2,
    'zug_ds100 GEN':              'zug_ds100:()=>genDS100McQ' in c2,
}

# Pflicht-Bahnhöfe prüfen
pflicht = ['Mannheim Hbf', 'Heidelberg Hbf', 'Wiesloch-Walldorf',
           'Praha hlavní', 'Kraków Główny', 'Oslo Sentralstasjon',
           'Bergen stasjon', 'Estação da Luz', 'Central do Brasil']
with open(KULTUR) as f: kd = json.load(f)
bp_names = [x['n'] for x in kd.get('bahnhof_pin', [])]
for p in pflicht:
    found = any(p.lower() in n.lower() for n in bp_names)
    checks[f'Pflicht: {p[:20]}'] = found

all_ok = True
for k, v in checks.items():
    print(f"  {'[OK]' if v else '[!!]'} {k}")
    if not v: all_ok = False

if all_ok:
    print("\nPATCH ABGESCHLOSSEN!")
else:
    print("\nFEHLER — prüfen!")
    sys.exit(1)
