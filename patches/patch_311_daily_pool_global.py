#!/usr/bin/env python3
"""
patch_311_daily_pool_global.py
Phase 311 — CRITICAL HOTFIX: DAILY_POOL ReferenceError

Problem:  DAILY_POOL war als lokale `const` in startDailyChallenge() definiert,
          aber renderDailyHero() referenziert sie außerhalb dieses Scopes.
          → ReferenceError: DAILY_POOL is not defined → App-Crash beim Start.

Fix:      DAILY_POOL in den globalen Scope verschoben (vor startDailyChallenge).
"""
import sys

with open('gen.py', encoding='utf-8') as f:
    src = f.read()

OLD_LOCAL = '''  /* Phase 295: Pool auf 30 Modi erweitert; Auswahl per getDailySeed() statt dayIndex */
  const DAILY_POOL=[
    /* Geografie Kern */
    "city","flag","capital","river","outline","neighbor","map_guess","map_capital",
    /* Higher / Lower */
    "hl_pop","hl_area","hl_gdp","hl_elevation","hl_lifeexp","hl_b_temp","hl_b_rain",
    /* Tiere & Natur */
    "uk_tiere_endemisch","uk_tiere_bigfive","uk_tiere_grosskatzen","hl_tiere_speed_land",
    "uk_tiere_nationaltier_pin","hl_tiere_gewicht_land",
    /* Kultur & Wissen */
    "uk_wahrzeichen","uk_getraenke","food","currency","plate_casual",
    /* Vergleich & Timeline */
    "comp_area","comp_pop","comp_gdp",
    /* Sport & Geo-Wissen */
    "uk_sportwissen_olympia_standort","timeline_geo_erdbeben",
    /* Züge & Bahn (Phase 309) */
    "zug_panorama","zug_vkm","zug_metro_logos","zug_routen","zug_bahnhof_typ",
    "zug_hersteller","hl_zug_speed","hl_zug_taktfrequenz","zug_rekorde_pin",
    "timeline_zug_bahnhof_bau"
  ];'''

NEW_LOCAL = '''  /* Phase 295: Pool auf 30 Modi erweitert; Auswahl per getDailySeed() statt dayIndex */
  /* Phase 311: DAILY_POOL in globalen Scope verschoben — war local var, daher ReferenceError in renderDailyHero */'''

GLOBAL_POOL = '''/* Phase 311: DAILY_POOL global — used by startDailyChallenge() AND renderDailyHero() */
const DAILY_POOL=[
  /* Geografie Kern */
  "city","flag","capital","river","outline","neighbor","map_guess","map_capital",
  /* Higher / Lower */
  "hl_pop","hl_area","hl_gdp","hl_elevation","hl_lifeexp","hl_b_temp","hl_b_rain",
  /* Tiere & Natur */
  "uk_tiere_endemisch","uk_tiere_bigfive","uk_tiere_grosskatzen","hl_tiere_speed_land",
  "uk_tiere_nationaltier_pin","hl_tiere_gewicht_land",
  /* Kultur & Wissen */
  "uk_wahrzeichen","uk_getraenke","food","currency","plate_casual",
  /* Vergleich & Timeline */
  "comp_area","comp_pop","comp_gdp",
  /* Sport & Geo-Wissen */
  "uk_sportwissen_olympia_standort","timeline_geo_erdbeben",
  /* Züge & Bahn (Phase 309) */
  "zug_panorama","zug_vkm","zug_metro_logos","zug_routen","zug_bahnhof_typ",
  "zug_hersteller","hl_zug_speed","hl_zug_taktfrequenz","zug_rekorde_pin",
  "timeline_zug_bahnhof_bau"
];
function startDailyChallenge(){'''

def patch(old, new, label):
    global src
    if old in src:
        src = src.replace(old, new, 1)
        print(f'[OK] {label}')
    else:
        print(f'[SKIP] {label} — anchor not found')
        sys.exit(1)

patch(OLD_LOCAL, NEW_LOCAL, 'Removed local DAILY_POOL from startDailyChallenge()')
patch('function startDailyChallenge(){', GLOBAL_POOL, 'Inserted global DAILY_POOL')

with open('gen.py', 'w', encoding='utf-8') as f:
    f.write(src)
print('[OK] gen.py saved — run: python3 gen.py && python3 verify.py')
