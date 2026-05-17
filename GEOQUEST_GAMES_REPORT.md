# 🗺️ GeoQuest — Integritäts- & Spielebericht

> Generiert von fix99.py | 55 Modi total

## Vollständige Liste aller deklarierten Spielmodi

| # | Modus-ID | Kategorie | Engine / Bemerkung |
| --: | :--- | :--- | :--- |
| 1 | `city` | ✅ Produktion | Reguläre Engine-Pipeline |
| 2 | `flag` | ✅ Produktion | Reguläre Engine-Pipeline |
| 3 | `capital` | ✅ Produktion | Reguläre Engine-Pipeline |
| 4 | `river` | ✅ Produktion | Reguläre Engine-Pipeline |
| 5 | `landmark` | ✅ Produktion | Reguläre Engine-Pipeline |
| 6 | `park` | ✅ Produktion | Reguläre Engine-Pipeline |
| 7 | `unesco` | ✅ Produktion | Reguläre Engine-Pipeline |
| 8 | `citymark` | ✅ Produktion | Reguläre Engine-Pipeline |
| 9 | `subway` | ✅ Produktion | Reguläre Engine-Pipeline |
| 10 | `flagsel` | ✅ Produktion | Reguläre Engine-Pipeline |
| 11 | `rcapital` | ✅ Produktion | Reguläre Engine-Pipeline |
| 12 | `rcity` | ✅ Produktion | Reguläre Engine-Pipeline |
| 13 | `rriver` | ✅ Produktion | Reguläre Engine-Pipeline |
| 14 | `outline` | ✅ Produktion | Reguläre Engine-Pipeline |
| 15 | `food` | ✅ Produktion | Reguläre Engine-Pipeline |
| 16 | `brand` | ✅ Produktion | Reguläre Engine-Pipeline |
| 17 | `currency` | ✅ Produktion | Reguläre Engine-Pipeline |
| 18 | `plate_casual` | ✅ Produktion | Reguläre Engine-Pipeline |
| 19 | `plate_hard` | ✅ Produktion | Reguläre Engine-Pipeline |
| 20 | `curr_real` | ✅ Produktion | Reguläre Engine-Pipeline |
| 21 | `pop_compare` | ✅ Produktion | Reguläre Engine-Pipeline |
| 22 | `river_real` | ✅ Produktion | Reguläre Engine-Pipeline |
| 23 | `hl_pop` | ✅ Produktion | Reguläre Engine-Pipeline |
| 24 | `hl_river` | ✅ Produktion | Reguläre Engine-Pipeline |
| 25 | `hl_area` | ✅ Produktion | Reguläre Engine-Pipeline |
| 26 | `comp_area` | ✅ Produktion | Reguläre Engine-Pipeline |
| 27 | `comp_pop` | ✅ Produktion | Reguläre Engine-Pipeline |
| 28 | `comp_north` | ✅ Produktion | Reguläre Engine-Pipeline |
| 29 | `comp_gdp` | ✅ Produktion | Reguläre Engine-Pipeline |
| 30 | `comp_density` | ✅ Produktion | Reguläre Engine-Pipeline |
| 31 | `comp_elevation` | ✅ Produktion | Reguläre Engine-Pipeline |
| 32 | `comp_coast` | ✅ Produktion | Reguläre Engine-Pipeline |
| 33 | `comp_borders` | ✅ Produktion | Reguläre Engine-Pipeline |
| 34 | `comp_life` | ✅ Produktion | Reguläre Engine-Pipeline |
| 35 | `comp_age` | ✅ Produktion | Reguläre Engine-Pipeline |
| 36 | `comp_forest` | ✅ Produktion | Reguläre Engine-Pipeline |
| 37 | `neighbor` | ✅ Produktion | Reguläre Engine-Pipeline |
| 38 | `map_guess` | ✅ Produktion | Reguläre Engine-Pipeline |
| 39 | `logic_grid` | 🔧 Spezialmodus (eigener Lifecycle) | Eigene `init*()`-Funktion, nicht über `GEN`-Pipeline |
| 40 | `travel_route` | 🔧 Spezialmodus (eigener Lifecycle) | Eigene `init*()`-Funktion, nicht über `GEN`-Pipeline |
| 41 | `wappen_meister` | ✅ Produktion | Reguläre Engine-Pipeline |
| 42 | `slf` | 🔧 Spezialmodus (eigener Lifecycle) | Eigene `init*()`-Funktion, nicht über `GEN`-Pipeline |
| 43 | `comp_airports` | ✅ Produktion | Reguläre Engine-Pipeline |
| 44 | `iata` | ✅ Produktion | Reguläre Engine-Pipeline |
| 45 | `beta_timezone` | 🔬 Beta | Reguläre Engine — experimentell, möglicherweise unfertig |
| 46 | `beta_climate` | 🔬 Beta | Reguläre Engine — experimentell, möglicherweise unfertig |
| 47 | `beta_flagcolor` | 🔬 Beta | Reguläre Engine — experimentell, möglicherweise unfertig |
| 48 | `comp_flight` | ✅ Produktion | Reguläre Engine-Pipeline |
| 49 | `comp_mountain` | ✅ Produktion | Reguläre Engine-Pipeline |
| 50 | `beta_landlocked` | 🔬 Beta | Reguläre Engine — experimentell, möglicherweise unfertig |
| 51 | `comp_nsextent` | ✅ Produktion | Reguläre Engine-Pipeline |
| 52 | `comp_olympics` | ✅ Produktion | Reguläre Engine-Pipeline |
| 53 | `climate_mystery` | ♻️ Alias (P139) | Zeigt auf bestehenden Generator (Wiederverwendung) |
| 54 | `flag_fusion` | ♻️ Alias (P139) | Zeigt auf bestehenden Generator (Wiederverwendung) |
| 55 | `timezone_jumper` | ♻️ Alias (P139) | Zeigt auf bestehenden Generator (Wiederverwendung) |

## Kategorien-Zusammenfassung

- **✅ Produktion**: 45 Modi
- **🔬 Beta**: 4 Modi
- **🔧 Spezialmodus (eigener Lifecycle)**: 3 Modi
- **♻️ Alias (P139)**: 3 Modi

## Patches dieser Session

| Phase | Beschreibung |
| :--- | :--- |
| P150 | Standard-Timer 12s, Logic-Grid 90s Countdown |
| P151 | Ads deaktiviert (ENABLE_ADS=false) |
| P153 | Wappen Scaling (100%/180px) + wappenErr() Fallback |
| P154 | Crash-Shield (window.onerror) + Mojibake Lokalisierung |
