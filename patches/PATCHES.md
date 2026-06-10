# GeoQuest Patch Convention
## Phase 225 / Suggestion 1 — Migrations System

This directory contains all patch scripts that modify `gen.py`.
Every sprint that changes `gen.py` must add a patch file here.

---

## File Naming

```
patch_NNN[suffix]_short_description.py
```

| Part | Rule |
|------|------|
| `NNN` | Phase number (3 digits, zero-padded) |
| `[suffix]` | Optional letter `a/b/c` for multi-part phases |
| `short_description` | Snake_case, under 30 chars |

**Examples**
```
patch_225_json_extraction.py
patch_227a_tiere_routing.py
patch_227b_tiere_data_part1.py
patch_228_new_feature.py
```

---

## Required Header

Every patch file must begin with a docstring containing these fields:

```python
"""
Phase: 228
Date:  2026-05-26
Author: Claude / Andre
Scope: Short one-line summary of what this patch does.

Description:
  Longer explanation. What problem does it solve?
  What anchors does it use? Are there dependencies on other patches?

Dependencies: patch_225_json_extraction.py
Zero-Bug Policy: All c.replace() calls use assert c.count(old)==1
"""
```

---

## Zero-Bug Policy (Non-Negotiable)

Every `c.replace(old, new)` call MUST be preceded by a uniqueness assertion:

```python
assert c.count(old) == 1, f"Anchor not unique: {old!r}"
c = c.replace(old, new, 1)
```

Never use `replace_all=True` on gen.py anchors.
Never edit gen.py directly — always through a patch script.

---

## Running a Patch

```bash
# From the GeoQuest project directory:
cd C:\Users\Andre\Desktop\Cowork\Geoquest

# Run a single patch:
python3 patches/patch_228_new_feature.py

# Or use the runner (validates, runs, rebuilds, verifies):
python3 run_patch.py patches/patch_228_new_feature.py
```

---

## Full Sprint Workflow

```
1. Write patch script  →  patches/patch_NNN_description.py
2. python3 run_patch.py patches/patch_NNN_description.py
3. (Runner auto-runs: gen.py + verify.py)
4. Check verify.py output: 76/76 [OK]
5. Update unlock_and_push.bat commit message
6. Run unlock_and_push.bat
```

---

## Patch Archive

| File | Phase | Summary |
|------|-------|---------|
| patch_212_kultur_modes.py | 212 | 27 Kultur/Lifestyle universal modes |
| patch_213_perf_daily_1v1.py | 213 | Performance + Daily history + 1v1 selector CSS |
| patch_214_routing_audit.py | 214 | Routing regression audit + fixes |
| patch_215_uk_engine.py | 215 | UK engine modes registration |
| patch_216_universal_engine.py | 216 | Universal engine + custom mechanics |
| patch_220_security_audit.py | 220 | 5-pillar security & stability audit fixes |
| patch_221a_service_worker.py | 221a | Offline mode / Service Worker cache |
| patch_221b_ws_multilingual.py | 221b | Wort-Schmiede multilingual bonus |
| patch_221c_kompass_mode.py | 221c | Sonnen-Kompass Ratsel new mode |
| patch_222_stadion_hl.py | 222 | Dynamic Stadion-Hoehe HL generator |
| patch_223_map_zoom_fix.py | 223 | Map zoom + D3 lid-binding fix |
| patch_223_tiere_data_expand.py | 223 | Scale Tiere/Pferde datasets 20->68 entries |
| patch_225_json_extraction.py | 225 | Extract data blocks to data/*.json |
| patch_226_ux_fixes.py | 226 | UX fixes: search, HUD, HL buttons |
| patch_227a_tiere_routing.py | 227a | 21 Tiere Modi routing registration |
| patch_227b_tiere_data_part1.py | 227b | Tiere Pin + HL data + generators |
| patch_227c_tiere_data_part2.py | 227c | Tiere Match data + generator |
| patch_227d_pferde_dlc.py | 227d | Pferde DLC: Rassen, Fachbegriffe, Stockmass, Fluesterer |
| patch_228_pflanzen.py | 228 | Pflanzen-Kategorie (4 JSON-Dateien, ~55 Modi) |
| patch_229_gastronomie.py | 229 | Gastronomie-Kategorie (4 JSON-Dateien, ~51 Modi) |
| patch_230_tech_emob.py | 230 | Tech + E-Mobilitaet (8 JSON-Dateien, ~110 Modi) |
| patch_231_archaeologie.py | 231 | Archaeologie (4 JSON-Dateien, ~60 Modi) |
| patch_235_fixes.py | 235 | Qualitaets-Patch: BETA-Tags, Pflanzen-Gruppe, Datendichte |
| patch_236_fixes.py | 236 | Weitere QA-Fixes |
| patch_237_qa_triage.py | 237 | QA-Triage: Duplikate, WS-Validierung, Koordinaten |
| patch_238_offline_sw.py | 238 | SW blob→sw.js, hash-versioned cache, manifest.json, verify Section 12 |
| patch_239_offline_ux.py | 239 | Auth-UX: _authErrMsg(), navigator.onLine guards (4 Funktionen) |
| patch_240_offline_sync.py | 240 | isOffline state, online/offline listeners, Score-Queue, syncOfflineData() |
| patch_241_security_ux.py | 241 | Security cap (100k/1k), Gameover Offline-Banner, verify.py Section-0 dynamisch |
| patch_242_engine_animals.py | 242 | Tiere-Pin JSON, Daily 5-mode rotation, Blitz-Modus (60s speed round) |
| patch_243_new_worlds.py | 243 | 3 Neue Welten: Astronomie, Geologie, Sport-Wissen (12 JSON, 32 Modi) |
| (hotfix) data/*.json    | 245 | WS-Halluzinationen, tiere/astro/geo/sport _pin Struktur, WS-Duplikate |
| (improve) validate_content.py | 246 | Duplikat-Scope per Kategorie, WS-Mindestwoerter, WS-Duplikat-Check, Match-Schwellwert |
| patch_243b_modes_fix.py | 243b | 32 fehlende MODES-Eintraege fuer Astro/Geo/Sport (leere Akkordeons gefixt) |
| (hotfix) data/*_hl.json | 247 | 16 HL-Ausreisser z>4sigma entfernt (Sauerbraten, Balsamico, TPU-Pod u.a.) |
| (hotfix) data/astro_ws.json, geo_ws.json, sport_ws.json | 248 | WS-EN-Fallback: validWords.en fuer 9 Modi (Astro/Geo/Sport) ergaenzt |
| (hotfix) data/pflanzen_match.json, pflanzen_pin.json | 248 | bestuaeber-Korruption gefixt, Mais-Duplikat entfernt, nationalblumen wiederhergestellt |
| patch_249_polish.py | 249 | Security: submitRouteResult() in _TRUSTED_FNS. PWA-Banner fix (DOM-Element). LS-TTL 90d. run_patch.py Pipeline-Upgrade |
| patch_250_accordion_fix.py | 250 | Akkordeon-Fix: toggleAccordion() delegiert an filterByCategory() — Astro/Geo/Sport-Kategorien zuverlässig öffenbar |
| patch_251_pwa_banner_scope_fix.py | 251 | HOTFIX: renderPwaBanner() aus renderBottomNav() herausgelöst → Top-Level-Funktion (ReferenceError gefixt) |
| patch_252_astro_expansion.py | 252 | Astronomie Expansion: 17 neue Modi — 4 Pin, 6 HL, 6 Match, 1 WS (SCHWARZESLOCH) |
| patch_253_geo_expansion.py | 253 | Geologie & Vulkane Expansion: 40 neue Modi — 12 Pin, 10 HL, 12 Match, 6 WS. MODES: 607→647 |
| patch_254_sport_expansion.py | 254 | Sport-Wissen Expansion: 30 neue Modi — 8 Pin, 8 HL, 8 Match, 6 WS. MODES: 647→677 |
| patch_284_daily_exploit.py | 284 | Daily-Challenge Exploit-Fix: Start-Flag (gq_daily_prog_YYYY-MM-DD) sofort beim Start + saveDailyProgress nach jeder Antwort + Resume-Logik + markDailyDone räumt Progress-Key. Kein Score-Reset durch Neustart mehr. verify: 90/90 |
| patch_285_mp_sync.py | 285 | 1v1-Online-Sync-Fix ("Höheres BIP" unterschiedliche Fragen): filter+diff im game_start-Payload synchronisiert (Host autoritativ, _compPick/getSmartMatch hingen daran) + Seed an startGame übergeben → Runde 1 nicht mehr per Math.random(). verify: 90/90 |
| patch_286_mp_show_opp_answer.py | 286 | 1v1-Online: Gegner-Auswahl sichtbar. score_update überträgt {sel,selOk,lid}; Anzeige bei lid-Match als Duell-Zeile + Schwert-Marker auf gewähltem Button. verify: 90/90, node --check OK |
| patch_287_i18n_de_en_pl.py | 287 | i18n de/en/pl: 15 hartkodierte deutsche Prompts → t() (de aus Original, en+pl ergänzt); LANG.pl 115→158 komplettiert inkl. Wort-Schmiede. de/en/pl vollständig (0 Lücken), übrige 21 Sprachen Fallback EN. verify: 90/90, node --check OK |
| patch_288_pl_content_i18n.py | 288 | Polnische Spielinhalte (E-Mob, Archäologie, Astronomie, Geologie, Sport): erweiterbares _CONTENT_I18N{pl:{}} + _tc(); 196 Prompts + 54 Einheiten + 79 Match-Buttons/Länder übersetzt; in _mkPinQ/_mkHL/_mkMatchQ verdrahtet (opts+ans konsistent). Eigennamen fallen durch. verify: 90/90, node --check OK |
| patch_289_comp_i18n.py | 289 | comparisons (comp_*) de/en/pl: _compQ + 5 Spezial-Generatoren über _tc; _CONTENT_I18N auf JSON normalisiert. +16 en/pl. verify: 90/90 |
| patch_290_beta_i18n.py | 290 | HL-Beta (26) + Beta-MCQ (100) + Beta-HL (3) Prompts de/en/pl über _tc; 129 Strings → en+pl. verify: 90/90, node OK |
| patch_291_en_5cats.py | 291 | Englisch für die 5 Rubriken: _CONTENT_I18N.en += 329 (Prompts/Einheiten/fixedOpts). 5 Rubriken jetzt de/en/pl. verify: 90/90, node OK. Audit: GeoQuest_i18n_Audit.md |
| patch_292_tpgt_i18n.py | 292 | Tiere/Pflanzen/Gastro/Tech de/en/pl: genTiere*/genPflanzen*/genUniversal* mit _tc gewrappt; +337 en/pl (162 Prompts + 36 Einheiten + 139 fixedOpts). verify: 90/90, node OK |
| patch_293_country_answers.py | 293 | _tcc(): dt. Ländername→cc→displayCountry für Match-opts/ans (astro/geo/sport, lifestyle/airports). verify: 90/90, node OK |
| patch_294_clean_c_categories.py | 294 | Saubere .c-Kategorien de/en/pl: Gesteinsklassen, Kristallsysteme, Erdzeitalter, Sternenhimmel, Kontinente (101 Werte). verify: 90/90, node OK |
| (data) patches/games_batch1.py | 360 | Gaming-Kategorie: 31 Spiele (Modern Youth + Global Mobile) als games_extended.json Einträge. 28 Datenkorrekturen (Fall Guys publisher/land, Brawl Stars genre/usk, Clash pegi, Among Us downloads, Roblox peak, Koordinaten) |
| (data) patches/games_batch2.py | 360 | Gaming-Kategorie: 20 Spiele (Klassiker) als games_extended.json Einträge. GTA V, Witcher 3, Pokémon, Zelda, Half-Life u.a. |
| (audit) PHASE400_SYSTEM_AUDIT.md | 400 | Phase 400 Full-Architecture & Security Review: XSS, Zero-Trap, Biased Sort, Spread-Operator, Placeholder-Reihenfolge, validate_content-Lücken, Performance-Analyse. 10 Findings (3 kritisch, 2 hoch, 3 mittel, 2 low) |
| (inline) gen.py direkt | 401 | Phase 401 Audit-Fixes: 7× XSS esc(q.subj) in innerHTML-Pfaden; Zero-Trap USK/pegi/sequel_count=0 erlaubt; 2× Biased sort→Schwartzian Transform; 3× Spread→ES5-indexOf; Adaption+Turbo fixedPool→null |
| (inline) validate_content.py | 401 | check_games_extended() + Routing + Cross-Validation für games_extended.json: 22 Pflichtfelder, Enums, Typ-Checks, Koordinaten, F2P-Logik. validate: 44/44 ✓ |
| (inline) verify.py | 401 | games_extended.json in Section 10 JSON-Roundtrip-Test aufgenommen |
| (inline) gen.py direkt | 402 | Phase 402 neue Gaming-Modi: games_match_publisher, games_match_f2p (genGamesF2PQ mit Ja/Nein-UI), hl_games_peak (peak_concurrent_mio), hl_games_dev_lat (Studio-Latitude). MODE_CATS games: 13→17 Modi. MODES: 765→769 |
| patches/patch_403_audit_polish.py | 403 | Audit-Polish: JSON-Parser try/except fuer autos_extended+games_extended; Prototype-Pollution hasOwnProperty-Guard in 10 Object.keys()-Aufrufen (genGamesHLExt, Match, Pin, Baujahr, F2P, genAutosHLExt, forEach x2, Match) |
| (inline) gen.py direkt | 404 | 2 neue Gaming-Modi: games_match_esports (genGamesEsportsQ Ja/Nein) + hl_games_pegi (PEGI H/L). i18n +4 Strings. MODE_CATS games: 17->19. MODES: 769->771 |
| (inline) post_phase.py | 404 | Backup-Policy: Nur loeschen wenn >=2 neuere Backups vorhanden (Sicherheitsnetz). MODES-Count aus gen.py statt JSON-Keys |
| check_session.py | 404 | Neues Session-End-Check Script: verify+validate+Dokumente-Sync+MODES-Konsistenz+Backup-Status in einem Rutsch |
| CLAUDE_SESSION_STARTER.md | 403/404 | i18n-Mandat (_tc Pflicht), Validator-Sync-Regel, H/L-Inversions-Falle-Merksatz eingefuegt |
| patches/games_batch3.py | 405 | Batch 3: 20 Indie/Klassiker-Spiele (Stardew Valley, Hollow Knight, Celeste, Elden Ring, Baldurs Gate 3 u.a.). Neue Kategorie Indie. 50->70 Spiele in games_extended.json |
| (inline) games_extended.json | 405 | peak_year + publisher_lat/lng zu allen 70 Eintraegen |
| (inline) gen.py direkt | 405 | 3 neue Modi: hl_games_peak_year, hl_games_publisher_lat, games_peak_year_mc (genGamesPeakYearMC). i18n +6 Strings. MODES: 771->774 |
| (inline) validate_content.py | 405 | Indie zu KATEGORIE-Enum, optionale Typ-Checks fuer peak_year/publisher_lat/lng |
| (inline) gen.py direkt | 406 | BUG: genGamesPinQ subj enthielt Developer+Land (Spoiler auf Karte) → nur noch game-Name. BUG: games_match_kategorie immer null (fixedPool 3 Einträge → nach Entfernen richtiger Antwort nur 2 Distraktoren, <3 → return null) → Indie als 4. Option. catLabels["games"] fehlte → Gaming-Suche blind. hl_games_dev_lat Syntaxfehler (fehlende Klammern). JS 143/143 |
| generate_spieluebersicht.py | 407 | Dispatch-Regex 4 neue Muster (fn("key",{), fn("key","str",...), fn("key",_tc()), Block-Arrow). Special Cases: genGamesHLExt/Match/Pin/F2P/Esports/etc.→70 Spiele, genAutosHLExt/Match/etc.→431 Fahrzeuge, genAutosHL→autos.json Items. 0 von 774 Modi ohne Datenbasis-Badge |
| generate_spieluebersicht.py | 407 | Dispatch-Regex 4 neue Muster; genGamesHLExt/Match→70 Spiele; genAutosHLExt/Match→431 Fahrzeuge; genAutosHL→autos.json. 0 von 774 Modi ohne Badge |
| (inline) gen.py direkt | 408 | UX: _exitToMenu() — zentraler Exit-Handler: speichert Modus-Gruppe in S.filterCat, scrollt smooth zur Akkordeon-Sektion. 11x Exit-Button ersetzt. verify: 143/143 |
| (inline) gen.py direkt | 409/410 | UX: _trackPlayedMode() speichert gq_played+gq_recent (localStorage). renderRecentBar() zeigt letzte 5 Modi als Schnellstart-Leiste. Fortschritts-Badge X/Y + Fortschrittsbalken im Akkordeon-Header. Carousel-Grid-Reinit-Fix (doppeltes setTimeout). verify: 143/143 |
| (data) games_extended.json | 410 | protagonist (42/70 benannt: Link, Geralt, Lara Croft, Arthur Morgan, ...) + howlong_h (37/70: HowLongToBeat Hauptstory-Dauer) |
| (inline) gen.py direkt | 410 | 3 neue Modi: games_match_protagonist (Erkenne den Protagonist), games_match_pub_is_dev (Publisher=Developer?), hl_games_howlong (Spielzeit H/L). i18n +6. MODES: 774->777 |
| (data) autos_extended.json | 411 | wendekreis_m (Wendekreis in m, 91/431 gefüllt) + zuladung_kg (Nutzlast in kg, 74/431 gefüllt) |
| (inline) gen.py direkt | 411 | 2 neue Auto-Modi: hl_auto_wendekreis (lowerWins! Smart 8.75m bis F-150 14m), hl_auto_zuladung. i18n +4 Strings. MODES: 777->779 |

| patch_412_fixes_new_modes.py | 412 | Bugfixes (handheld Ja/Nein, timeline_auto_bj, spieluebersicht Syntax-Fix) + 4 neue Konsolen-Modi (hl_ram/cpu, match_generation/land) + iOS Timeline-Bug (5 Fixes). MODES: 791→796 |
| patch_413_regional_kultur.py | 413 | Neue Kategorie Regionale Kultur & Kulinarik: 30 D-A-CH Einträge, 6 Modi (Pin + 3 Match + 2 H/L), validate_content, i18n DE/EN/PL. MODES: 796→802 |
| patch_414_menu_layout.py | 414 | Dual Menu Layout: Tab-Ansicht (3 Reihen × 8 Kategorien) + Settings-Toggle (gq_menu_layout accordion/tabs). CSS tabs-mode, bestehende Carousel-Logik unverändert. verify: 146/146 |
| patch_415_settings_consolidation.py | 415 | Settings konsolidiert: block4+block5 zu einem EINSTELLUNGEN-Block (Design-Segmented, Sprache, Menü-Ansicht-Toggle inline). Spielübersicht: _get_type() Match/Pin-Fix, Konsolen/Regional Datenbasis-Badges, return len(rows). 14/14 session checks |
| patch_416_tabs_pwa.py | 416 | Tab-Ansicht: Inline-Grid + Accordion-Header im JS ausgeblendet. PWA: Schließen-Button Android/Desktop, gq_pwa_dismissed, Reaktivierung in Einstellungen. verify: 146/146 |
| patch_417_settings_cleanup.py | 417 | Settings-Modal: Dark Mode entfernt (doppelt), Untertitel. Tab-Ansicht inline-Grid fix + Accordion-Header JS-Rendering fix. PWA-Banner Schließen-Button + gq_pwa_dismissed. verify: 146/146 |
| patch_418_modal_final.py | 418 | Modal final: Menü-Ansicht raus, App installieren vor Schließen, Reihenfolge: Heimatregion→TTS→Hardcore→Raster→Feedback→App→Schließen. verify: 146/146 |
| patch_419_modal_appbtn_fix.py | 419 | App-installieren Button im Modal korrigiert (war in onclick eingebettet), IIFE-Pattern. verify: 146/146 |
| (inline) gen.py direkt | 420 | UX: Kategorie-Nav als wischbares Carousel (data-cat="_catnav", bestehende Carousel-Engine), 4 Spalten × konfigurierbare Reihen, volle Kategorienamen statt Abkürzungen. Neue Einstellung geoquest_catnav_rows (2-6, Standard 3). verify: 146/146 |
| (inline) geoquest_css.txt + gen.py | 421 | UI-Feinschliff Spielkarten: mode-card kompakter (.6/.4/30px→.5/.32/28px, Radius 12→11px), mode-icon 1.4→1.25rem, mode-desc .65→.68rem, Info-Button (i) 32→28px. verify: 146/146 |
| (inline) gen.py + geoquest_css.txt | 422 | Tech-Debt: totes <style>-CSS-Duplikat (~555 Zeilen) aus _HTML_HEAD entfernt (echte Quelle geoquest_css.txt). UX/A11y: Kategorie-Chips role=button/tabindex/aria-label/Tastatur (Enter/Space). Tooling: post_phase.py aktualisiert nun auch CLAUDE_SESSION_STARTER.md; check_session.py prüft dessen Aktualität. verify: 146/146 |
| (inline) gen.py direkt | 423 | Hilfe-Funktion: dauerhaftes Hilfe-Overlay per ?-Button im Header (renderHelpModal, S.helpModal). Kindgerechte Erklärung der Spiel-Typen (H/L, Match, Pin, Wort-Schmiede, MC), Schwierigkeit (Casual/Hardcore/Survival), Coins, Favoriten, Suche, Kategorie-Leiste. i18n DE/EN/PL (19 Keys je Sprache). verify: 146/146 |
| (inline) gen.py direkt | 424 | Erstnutzer-Tour: kurze 3-Slide-Einführung (renderTourModal/finishTour, ueberspringbar) per ?-Hilfe abrufbar (Button help_tour_btn, kein Auto-Start). Onboarding-Modi-Slide: veraltete Hardcodes (19 Modi / 16 weitere) durch dynamische MODES.length-Berechnung ersetzt + ?-Hilfe-Hinweis (ob_help_hint). i18n DE/EN/PL. verify: 146/146 |
| (inline) gen.py direkt | 425 | Hilfe-Button sichtbar: ?-Button zusaetzlich in die sichtbare Home-Kopfzeile (_hdr, eingeloggt + Gast) neben das Feedback-Symbol gesetzt. Vorher nur in der GEOQUEST-Logo-Leiste (auf Home-Tab nicht sichtbar) → Hilfe wurde nicht gefunden. verify: 146/146 |
| (inline) gen.py direkt | 426 | Home-Kopfzeile entzerrt (war gequetscht): einheitliche runde 34px-Icons (?/Feedback), Streak-Pille nowrap (kein Umbruch '3/Tage'), Gast-Variante: 'Fortschritt sichern' jetzt eigene volle Zeile. verify: 146/146 || patch_413_neue_modi.py + inline | 413 | 8 neue Modi aus ungenutzten Datenfeldern: hl_konsolen_erscheinungsjahr, hl_konsolen_eingestellt, konsolen_match_spiel (Reverse-Quiz: Spiel→Konsole, neue genKonsolenSpielQ), konsolen_match_aufloesung, hl_auto_nordschleife (lowerWins, 17 Einträge), hl_auto_baujahr_ende (373 Einträge), games_match_publisher_land, hl_games_publisher_lng. generate_spieluebersicht: genKonsolenSpielQ zu _KONSOLEN_FNS. MODES: 802→810. verify: 146/146 |
| inline gen.py | 424 | 4 neue Geo/Zug-Modi: zug_match_land (177 Strecken→Landzuordnung), odd_one_out (6 Kategorien: EU/NATO/Insel/Binnenstaat/G7/Euro), clue_country (progressive Hinweise Kontinent→Hauptstadt→Währung, neues type:"clue_country"), sort_rank (4 Länder nach Metrik klicken, neues type:"sort_rank"). generate_spieluebersicht.py: 4 neue Generator-Sonderfälle. MODES 810→814. verify: 146/146 |
| inline gen.py + neue JSONs | 427 | 2 neue Kategorien "Kino 
| patch_430_lit_robotik_ws.py | 430 | Wort-Schmiede Literatur & Robotik: ws_lit_protagonist (TINTENHERZ) + ws_robot_name (MASCHINENLERNEN). data/literatur_ws.json + data/robotik_ws.json. verify: 155/155. MODES: 859→861 |

| patch_431_med_eco.py | 431 | Kategorien Anatomie & Medizin + Wirtschaft & Marken. 13 neue Modi, 4 neue JSON-Dateien (medizin_extended 40, wirtschaft_extended 40, 2x WS). Timeline: med_meilensteine + eco_gruendung. verify: 159/159. MODES: 861→874 |

| patch_432_regional_bugfix (inline) | 432 | Bugfix: match_regional_land öffnete sich nie (genRegionalMatchQ pool.length<3, D-A-CH hat nur 3 Länder → nach Filterung 2<3 → null). Fix: Threshold auf 2, dis=p.slice(0,Math.min(3)). verify: 160/160. MODES: 874 |

| inline gen.py + regional_extended.json + validate_content.py | 433 | EU-Erweiterung Regionale Kulinarik: 30→80 Einträge, 22 Länder (DE/AT/CH + 19 EU). Bugfix: match_regional_land fixedPool entfernt → echte Datenländer als Pool. Label: Regionale & EU-Kulinarik. validate LAND-Enum EU-weit. verify: 160/160 |

| inline | 434 | Datenbasis-Upgrade: generate_spieluebersicht.py 3 neue Fn-Mappings (0 Warnings). literatur_extended 40→80. robotik_extended 40→80. timeline robot_jahr auf 80. verify: 160/160 |

| patch_432_hist_web (inline) | 435 | Kategorien Weltgeschichte & Imperien + Webkultur & Social Media. 12 Modi (hl_hist_ausdehnung/dauer/start, hist_match_figur, timeline_hist_start, ws_hist_renaissance, hl_web_reichweite/start, web_match_land/kategorie, timeline_web_start, ws_web_algorithmus). timeline hist_start+web_start. verify: 163/163. MODES: 874→886 |

| inline gen.py | 436 | WS Mythologie (PANTHEON+UNTERWELT) + WS Architektur (WOLKENKRATZER+FUNDAMENT) + hl_arch_laenge + timeline_arch_baujahr + myth_match_tier. 7 Modi. post_phase.py: landing.html Auto-Update. Substring-Fix: MYTH_WS/ARCHITEKTUR_WS vor MYTH/ARCH in Replace-Kette. verify: 165/165. MODES: 886→893 |

| inline data/*.json | 437 | Datenbasis-Erweiterung: Serien 98→105, Filme 40→46, Musik 40→46, Webkultur 40→52, Wirtschaft 40→49. Enum-Fix Serien. Timeline eco+web refreshed. verify: 165/165 |

## Phase 438 — Freizeitparks & Kunstgeschichte
**Datum:** 2026-06-02
**Modi:** 15 neue (hl_park_speed, hl_park_hoehe, hl_park_inversionen, hl_park_baujahr, park_match_land, park_match_kategorie, timeline_park_baujahr, ws_park_achterbahn, hl_kunst_jahr, hl_kunst_wert, kunst_match_kuenstler, kunst_match_epoche, kunst_match_museum, timeline_kunst_jahr, ws_kunst_renaissance)
**Daten:** themeparks_extended.json (80), kunst_extended.json (54), themeparks_ws.json, kunst_ws.json
**Total:** 908 Modi

## Phase 439 — Brettspiele & Sprachen
**Datum:** 2026-06-02
**Modi:** 14 neue (hl_boardgame_jahr, hl_boardgame_spieler, hl_boardgame_dauer, hl_boardgame_rating, boardgame_match_autor, boardgame_match_land, timeline_boardgame_jahr, ws_boardgame_spielbrett, hl_sprache_muttersprachler, hl_sprache_laender, sprache_match_familie, sprache_match_schrift, sprache_match_region, ws_sprache_grammatik)
**Daten:** boardgames_extended.json (80), sprachen_extended.json (80), boardgames_ws.json, sprachen_ws.json
**Total:** 922 Modi

## Phase 440 — Hunderassen & Gartenbau
**Datum:** 2026-06-02
**Modi:** 14 neue (hl_hund_gewicht, hl_hund_alter, hl_hund_hoehe, hund_match_land, hund_match_kategorie, ws_hund_begleiter, ws_hund_welpe, hl_garten_hoehe, hl_garten_bluete, garten_match_wasser, garten_match_boden, garten_match_region, ws_garten_rhodo, ws_garten_strelitzie)
**Daten:** hunde_extended.json (80), gartenbau_extended.json (80), hunde_ws.json, gartenbau_ws.json
**Total:** 936 Modi

## Phase 441 — Audit-Fixes (Build-Breaker + i18n)
**Datum:** 2026-06-02
**Fixes:** (1) Build-Breaker: ungültiger Unicode-Escape im Wort „gießen" (Modus garten_match_wasser, Phase 440) → JS-Syntaxfehler behoben (verify 172/173 → 177/177). (2) 13 fehlende PL-Übersetzungen in _CONTENT_I18N ergänzt (Film-/Musik-Kategorie: Regisseur, IMDb, Oscars, Grammys, Streams, Tonträger u.a.) → validate 0 Warnings.
**Doku:** AUDIT-UMFANG (9 Dimensionen) in CLAUDE_SESSION_STARTER.md dokumentiert; GeoQuest_Audit_Phase438.md erstellt. verify 177/177, validate 78/78, check_session 15/15.

## Phase 442 — Geo-Pin-Welle (13 neue Pin-Modi)
**Datum:** 2026-06-02
**Modi:** 13 neue (hund_pin_land, boardgame_pin_land, robot_pin_land, serie_pin_land, musik_pin_land, web_pin_land, lit_pin_land, park_pin_land, eco_pin_land, film_pin_land, konsole_pin_land, hw_pin_land, garten_pin_region)
**Infrastruktur:** LAND_LATLON Lookup-Tabelle (65 Länder+Regionen), genExtPinByLand() Universalgenerator, genLitPinQ()
**Bugfix:** SPRACHEN_KOMPASS_DATA Umbenennung (pre-existing duplicate const SPRACHEN_DATA)
**Total:** 949 Modi

## Phase 443 — Flüsse & Gewässer
**Datum:** 2026-06-02
**Modi:** 7 neue (hl_fluss_laenge, hl_fluss_einzug, fluss_match_kontinent, fluss_match_land, fluss_match_muendung, fluss_pin_muendung, ws_fluss_amazonas)
**Daten:** fluesse_extended.json (80 Weltflüsse), fluesse_ws.json. LAND_LATLON +9 Länder.
**Total:** 956 Modi

## Phase 444 — Nationalparks weltweit
**Datum:** 2026-06-02
**Modi:** 7 neue (hl_npark_flaeche, hl_npark_gruendung, npark_match_land, npark_match_kontinent, npark_match_oekosystem, npark_pin_lage, ws_npark_yellowstone)
**Daten:** nparks_extended.json (80 Parks), nparks_ws.json. LAND_LATLON +14 Länder.
**Bugfix:** i18n-Doppelquote in dynamischen replace()-Ankern (Y muss mit , nicht " beginnen).
**Total:** 963 Modi

## Phase 445 — Hauptstädte weltweit
**Datum:** 2026-06-02
**Modi:** 7 neue (hl_capital_einwohner, hl_capital_hoehe, capital_match_kontinent, capital_match_grossstadt, capital_pin_lage, hl_capital_aequator, ws_capital_reykjavik)
**Daten:** capitals_extended.json (80 Hauptstädte mit dist_aequator-Feld), capitals_ws.json.
**Bugfix:** IIFE in GEN-Dispatcher vermieden (}; bricht GEN-Regex ab) — dist_aequator-Feld stattdessen.
**Total:** 970 Modi

## Phase 446 — Inseln weltweit
**Datum:** 2026-06-02
**Modi:** 7 neue (hl_insel_flaeche, hl_insel_einwohner, insel_match_ozean, insel_match_kontinent, insel_pin_lage, hl_insel_aequator, ws_insel_groenland)
**Daten:** inseln_extended.json (80 Inseln), inseln_ws.json.
**Total:** 977 Modi

## Phase 447 — Gipfel & Berge
**Datum:** 2026-06-02
**Modi:** 7 neue (hl_gipfel_hoehe, gipfel_match_gebirge, gipfel_match_kontinent, gipfel_pin_lage, hl_gipfel_erstbesteigung, timeline_gipfel_besteigung, ws_gipfel_himalaya)
**Daten:** gipfel_extended.json (80 Gipfel), gipfel_ws.json.
**Total:** 984 Modi

## Phase 448 — Klimazonen weltweit
**Datum:** 2026-06-02
**Modi:** 7 neue (klima_match_zone, klima_match_kontinent, hl_klima_temp, hl_klima_niederschlag, klima_pin_land, hl_klima_temp_diff, ws_klima_monsun)
**Daten:** klima_extended.json (80 Länder), klima_ws.json.
**Total:** 991 Modi

## Phase 449 — Ozeane & Meere
**Datum:** 2026-06-02
**Modi:** 8 neue (hl_ozean_flaeche, hl_ozean_tiefe, ozean_match_typ, ozean_match_kontinent, hl_ozean_flaeche_klein, ozean_match_name, ws_ozean_atlantik, hl_ozean_tiefe_klein)
**Daten:** ozeane_extended.json (80 Gewässer), ozeane_ws.json.
**Meilenstein:** 999 Modi erreicht!
**Total:** 999 Modi

## Phase 452 — Personalisierung Portion 1+2
**Datum:** 2026-06-02
**Portion 1:** CAT_META-Konstante (audience kids/teens/adults + interests geo/natur/mint/pop/kultur/sport/alltag je Kategorie) als Filter-Basis. Reine Daten, keine UI-Wirkung.
**Portion 2:** Onboarding auf 4 Schritte erweitert (Willkommen+Sprache → „Wer spielt?" → „Was interessiert dich?" Mehrfachauswahl → „Wie viel Zeit?") statt Schwierigkeits-/Modi-Slides. Speichert gq_audience/gq_interests/gq_time, überspringbar, i18n DE/EN/PL (23 Keys/Sprache).
**Sonstiges:** eu_plates (Kennzeichen-Sammeln) auf alle Altersstufen getaggt.
**Offen (Roadmap):** Portion 3 „Für dich"-Filter (weich) + Mode-Level-Schwierigkeit; Portion 4 Empfehlungen („ähnliche Spiele"); In-Auto-Hinweis (geolocation speed). verify 191/191, validate 0 Warnings.

## Phase 453 — Querformat-Notausgang (Plan B)
**Datum:** 2026-06-02
**Fix:** Auf dem "Bitte Gerät drehen"-Screen neuer Button "Trotzdem im Hochformat spielen" (setzt S.ignoreLandscape) + Hinweis auf OS-Bildschirmsperre. Behebt das Festhängen, wenn die Display-Rotation gesperrt ist (Drehen wirkt dann nicht → Nutzer war ausgesperrt). waitingForLandscape-Gate + updateOrientationWarning respektieren das Override. Bonus: hartkodierter deutscher Dreh-Text → t() (i18n DE/EN/PL). Erkennung _isPortrait() bleibt 3-stufig (screen.orientation → window.orientation → Dimensions-Fallback, Android+iOS). verify 191/191, validate 0 Warnings.

## Phase 454 — KRITISCHER FIX: Kinder-Modus/Playlists vervollständigt
**Datum:** 2026-06-02
**Bug:** renderHomeTab rief 7 undefinierte Symbole auf (_getKidsMode, _toggleKidsMode, KIDS_CATS, _getTotalPlays, _getTopCats, _renderPlaylistStrip, PLAYLISTS) → Laufzeit-ReferenceError → Home-Tab crashte. Von verify/node --check NICHT erkannt (nur Syntax, kein Runtime). Scaffold war angelegt, Implementierung fehlte.
**Fix:** Alle Helfer definiert, verdrahtet mit CAT_META (Phase 452) als einziger Quelle: KIDS_CATS = Kategorien mit audience 'kids'; _getKidsMode/_toggleKidsMode (localStorage gq_kids_mode); _getTotalPlays/_getTopCats (Spielhistorie gq_played); 5 kuratierte PLAYLISTS; _renderPlaylistStrip (horizontale Kategorie-Leiste). „Für dich": top-Kategorien ab 10 Spielen, sonst aus Onboarding-Interessen (_getInterestCats). i18n DE/EN/PL (kids_mode_on/off, pl_foryou, pl_geo/natur/mint/pop/kultur). verify 191/191, validate 0 Warnings.

## Phase 455 — Spiel-Ebene-Filter (Kinder-Modus)
**Datum:** 2026-06-02
**Feature:** _modeLevel(m) klassifiziert jeden Modus heuristisch (1=leicht/Match, 2=mittel/H-L, 3=schwer/Wort-Schmiede + harte Keywords wie Metacritic/PEGI/Hubraum/BGG/Oscars). _kidHidden(m)=KidsMode && Level>=3. catModes-Filter blendet diese im Kinder-Modus aus — auch INNERHALB erlaubter Kategorien (löst „Auto-Hubraum/Game-Metacritic für Kinder zu schwer"). verify 191/191, validate 0 Warnings.

## Phase 455b — Spielübersicht: Zielgruppen-Auswertung
**Datum:** 2026-06-02
**Tooling:** generate_spieluebersicht.py: pro Modus 🧒-Marker (kindgeeignet) + Legende „Kindgeeignet X/999". Abgeleitet aus CAT_META-audience + Schwierigkeits-Heuristik (_mode_level/_mode_kidsafe) — selbst-aktualisierend. Aktuell: 348/999 kindgeeignet (35%).

## Phase 456 — Lehrplan-konforme Kinder-Tags
**Datum:** 2026-06-02
**Pädagogik:** Recherche Grundschul-Sachunterricht (Kl. 1-4): Pflanzenwelt, Jahreszeiten/Wetter, Raum/Karten, Sonne/Mond. → CAT_META audience +'kids' für pflanzen, gartenbau, klima, fluesse, gipfel. Kinder-geeignet 348→410/999. Per-Mode-Level-Filter (Phase 455) blendet schwere Modi innerhalb weiter aus. Spielübersicht zählt automatisch (🧒 + „Kindgeeignet 410/999").

## Phase 457 — Sticker-Sammlung + Header-Entzerrung + Status-Auto-Stempel
**Datum:** 2026-06-02
**Features:** (1) Sticker-Sammlung (renderStickerModal): pro Kategorie ein Sticker, freigespielt = farbig, sonst 🔒; abgeleitet aus gq_played; Eintrag im Einstellungs-Modal; i18n DE/EN/PL. (2) Header-Icons app-weit 34→30px + Abstände enger (entzerrt; alle ≥24px WCAG). (3) Tooling: post_phase.py stempelt jetzt automatisch PERSONALISIERUNG_STATUS.md (Reset-Sicherheitsnetz). verify 191/191, validate 0 Warnings.

## Phase 458 — Antwort-Audit-Fix (Kinder)
**Datum:** 2026-06-02
**Audit:** 24 Kinder-Modi (Level 1-2) verlangten Zahl/Jahr-Antwort (Auto-Baujahr, Game-Release, Zug-Reisezeit, Breitengrad …) — für Kinder zu schwer. _modeLevel um ID-Signale (_bj/baujahr/release/peak_year/erscheinungsjahr/reisezeit/breitengrad/_dekade → Level 3) erweitert → im Kinder-Modus ausgeblendet, Erwachsene unberührt. verify 191/191, validate 0 Warnings.

## Phase 459 — Unterwegs-Vorschlag (Geolocation, opt-in)
**Datum:** 2026-06-02
**Feature:** _initTravelHint/_travelBanner/_dismissTravel — opt-in (gq_travel_hint, Standard AUS): watchPosition, bei coords.speed>9 m/s (3 Messungen) einmaliger Banner „Unterwegs? 🚗 Kennzeichen / 🚆 Waggons" (Nutzer wählt, keine Auto-Erkennung). Einstellungs-Toggle, i18n DE/EN/PL. Standard AUS = null Risiko für bestehende Nutzer. Mobil-Test ausstehend. verify 191/191, validate 0 Warnings.

## Phase 460 — Familienduell (Hot-Seat-Rubrik)
**Datum:** 2026-06-03
**Feature:** initLV(family); im Familien-Modus generiert _lvNext pro Zug eine frische Frage (kein roundQ-Reuse) mit Level-Filter — Spieler 1 (Kind) = Level 1 + kindersicher, Spieler 2 (Erwachsen) = Level≥2. Button „👨‍👩‍👧 Familienduell" im LV-Setup; Gameover-Nochmal behält family. Normaler 1:1-Pfad unverändert. i18n DE/EN/PL. verify 191/191, validate 0 Warnings.

## Phase 461 — Home-Hero: Duell-Modi als Paar
**Datum:** 2026-06-03
**Layout:** Live 1vs1 + Lokal Hot-Seat nebeneinander (je halbe Breite, kompakte vertikale Karten, Untertitel weg). Daily Challenge bleibt voll breit (Haupt-Hero). Spart Höhe → „Empfohlen für dich" rückt nach oben. verify 191/191, validate 0 Warnings.

## Phase 462 — Klassenstufen (Kinder-Feinabstufung)
**Datum:** 2026-06-03
**Feature:** _kidLevelMax() (gq_kids_grade: '1'=6-8 J./Kl.1-2 → max Level 1; sonst 2=8-10 J./Kl.3-4 → max Level 2). _kidHidden blendet >Schwelle aus. Auswahl im Einstellungs-Modal (i18n DE/EN/PL). Junge Kinder bekommen nur leichteste Spiele. Standard=2 → kein Regress. verify 191/191, validate 0 Warnings.

## Phase 463 — Eltern-PIN (Kinder-Modus sichern)
**Datum:** 2026-06-03
**Feature:** _toggleKidsMode fragt beim Ausschalten den 4-stelligen PIN ab (renderPinModal mit Modus set/check, _pinSubmit/_pinRemove/_hasPin, gq_kids_pin). Setzen/Ändern/Entfernen im Einstellungs-Modal. Kinder können den Kinder-Modus nicht mehr selbst deaktivieren. i18n DE/EN/PL. verify 191/191, validate 0 Warnings.

## Phase 464 — Übungsmodus + Bestenlisten-Fairness-Analyse
**Datum:** 2026-06-03
**Analyse:** Bestenlisten lesen aus `leaderboard_weekly` STRENG pro Modus (`.eq("mode",mode)`) + feste 10 Runden; keine globale Rangliste → strukturell fair. Getrennte Kinder-Bestenliste unnötig.
**Feature:** Übungsmodus (gq_practice-Toggle): saveSession() schreibt nur lokale Historie, bricht VOR Leaderboard-Insert/Offline-Queue ab. Keine ROUNDS-/Struktur-Änderung → Fairness unberührt. i18n DE/EN/PL. verify 191/191, validate 0 Warnings.

## Phase 465 — Home-Strips poliert
**Datum:** 2026-06-03
**UX:** (1) Zuletzt-gespielt zeigt Titelteil nach ': ' (unterscheidbar statt 4× „Regionale Kultur: …"). (2) „Für dich" via _forYouCats() auf ~6 aufgefüllt (topCats + _getInterestCats + populäre Fallbacks, kindgefiltert, dedupliziert). (3) Begrüßung umbruchfähig statt abgeschnitten (nowrap/ellipsis entfernt). verify 191/191, validate 0 Warnings.

## Phase 466 — UX-Review Paket 1+2+3 (Kontrast/Karten/Spacing)
**Datum:** 2026-06-03
**UX:** (1) Kontrast: geoquest_css.txt --text3 #94a3b8→#64748b (Light, war WCAG-Fail), .mode-desc #64748b→#475569. (2) Mode-Karten: Info-i runder Badge oben rechts (22px/50%), Favoriten-Herz Outline 🤍/❤️ oben links, padding-bottom-Reserve (28px) entfernt → Titel-Platz unten. (3) Suchleisten-Spacing 15/12→20/16. verify 191/191, validate 0 Warnings.

## Phase 467 — UX-Review Paket 4+6 + Greeting-Fix
**Datum:** 2026-06-03
**UX:** (4) Zuletzt-gespielt: breite horizontale Wisch-Karten (152px, Icon links + 2-Zeilen-Text rechts). (6) _catTint(k): Pastell-rgba-Tönung pro Kategorie aus CAT_META-Interesse (geo/natur/mint/pop/kultur/sport/alltag), hell+dunkel-tauglich, gegen „Box-in-Box". (Fix) Begrüßung wieder einzeilig (white-space:nowrap zurück), 🌍 aus Gast-Gruß entfernt (war durch Phase-466-Umbruch in 2. Zeile gerutscht). verify 191/191, validate 0 Warnings.

## Phase 468 — Greeting i18n-Fix
**Datum:** 2026-06-03
Phase 467 hatte die 🌍 nur aus DE/EN `home_guest` entfernt → PL/FR/ES/IT/BG hätten dasselbe Umbruch-Problem. Globe nun aus allen 7 Sprachen raus + polnische Korruption „GoŚ›ciu" → „Gościu" repariert. Alle Gast-Grüße einzeilig. verify 191/191, validate 0 Warnings.

## Phase 469 — Ausführliches Handbuch (Profil/Einstellungen)
**Datum:** 2026-06-03
Neues `renderGuideModal()` — zweigeteiltes Nachschlagewerk, ergänzt das knappe Hilfe-Overlay. Tab „Für Kinder" (kindgerechte Sprache: Spielablauf, Spielarten, Punkte/Streak/Sticker, Tipps) + Tab „Für Eltern & alle" (Kinder-Modus & Filter, Klassenstufen/Lehrplan, Eltern-PIN, Mehrspieler, Bestenlisten & Fairness + Übungsmodus, weitere Funktionen). Öffnet über Button in den Einstellungen und Link im Hilfe-Overlay. Texte in `guide_*` (DE/EN/PL, Rest Fallback EN), State `S.guideModal`/`S.guideTab`. verify 191/191, validate 0 Warnings.

## Phase 470 — Zuletzt-gespielt: Pastell + sauberer Anschnitt
**Datum:** 2026-06-03
Recent-Leiste an den neuen Pastell-Look angeglichen: Helper `_recCat(mid)` ermittelt die Kategorie des Modus aus MODE_CATS, `_catTint` tönt jede Karte wie die Kategorie-/Empfehlungskarten. Anschnitt der letzten Karte entschärft: rechter Verlauf 32→52px + ab 70% deckend (kein harter Wort-Abriss), `scroll-snap-type:x proximity` + `scroll-snap-align:start` fürs Wischen. verify 191/191, validate 0 Warnings.

## Phase 471 — BUGFIX: Kategorie-Karten reagierten nicht
**Datum:** 2026-06-03
Klick auf die Pastell-Kategorie-Strips (`#gq-playlists`) rief `filterByCategory()`, das die Zielsektion zwar aufklappte, aber weit unten im `#mainGamesGrid` außerhalb des Sichtfelds → wirkte wie „passiert nichts". Neuer Helper `window._goCat(k)`: setzt `S.filterCat`, rendert (Filter greift über `_scheduleFilterRefresh`) und scrollt die aufgeklappte `.accordion-section[data-cat=k]` sanft ins Bild. Playlist-Karten-onclick auf `_goCat` umgestellt. verify 191/191, validate 0 Warnings.

## Phase 472 — DEPLOY-FIX: PWA Stale-Cache (vercel.json Cache-Control)
**Datum:** 2026-06-03
Ursache, warum deployte Änderungen „nicht ankamen": `vercel.json` hatte keine Cache-Control-Header. Der cache-first Service Worker + Browser-Cache lieferten ewig die alte `index.html`/`sw.js` aus — Symptom: ALLE neuen Features gleichzeitig weg (konsistent mit einer einzigen alten gecachten HTML). Fix: `Cache-Control: no-cache` auf `/sw.js` (+`no-store, must-revalidate`), `/index.html` (`/play` + Catch-all), `/manifest.json`. Session-Starter um „Deploy-/Cache-Falle" ergänzt. Keine gen.py-Änderung. vercel.json wird host-seitig vom .bat committet (Mount-Truncation im Sandbox).

## Phase 473 — Onboarding-Tipp korrigiert
**Datum:** 2026-06-03
`ob_help_hint` verwies auf „oben rechts auf ❓ tippen", aber das Header-❓ ist während des Onboardings nicht sichtbar. Umformuliert als Hinweis auf später/in der App (de/en/pl). verify 191/191, validate 0 Warnings.

## Phase 474 — Kategorie-Strips: weicher Auslauf statt harter Abschnitt
**Datum:** 2026-06-03
`_renderPlaylistStrip` (Empfohlen + Gruppen) lief rechts hart abgeschnitten aus. Jetzt wie die Recent-Leiste: weicher rechter Verlauf (46px, ab 72% deckend), `padding-right:40px` als Anschnitt-Hinweis, `scroll-snap` fürs Wischen. verify 191/191, validate 0 Warnings.

## Phase 475 — FIX kaputte vercel.json + _goCat robuster
**Datum:** 2026-06-03
(1) Die in 473/474 mit-committete `vercel.json` war die abgeschnittene 1817-B-Sandbox-Version (invalides JSON) → hätte den Vercel-Deploy gebrochen. Sandbox-seitig neu geschrieben (2054 B, valide, 14 Routes, Cache-Control intakt). (2) `_goCat`: garantiert `filterByCategory(k)` + Retry-Loop + harter `window.scrollTo`-Fallback, weil `scrollIntoView({behavior:'smooth'})` in der installierten PWA evtl. nicht scrollte (Sektion klappte unsichtbar weit unten auf = „nichts passiert"). verify 191/191, validate 0 Warnings.

## Phase 476 — SW-Cache verschlankt (QuotaExceededError behoben)
**Datum:** 2026-06-03
Der Service Worker cachte `GeoQuest.html` UND das byte-identische `index.html` (2× 6 MB) → sprengte das Storage-Quota (`QuotaExceededError`, v.a. Inkognito), einzelne data/*.json wurden beim Install übersprungen. Fix: `index.html` aus `_cache_assets` entfernt; `GeoQuest.html` bleibt Precache + Offline-Fallback, `/play` wird zur Laufzeit gecacht. Cache-Hash ändert sich → alter Cache wird ersetzt. verify 191/191, validate 0 Warnings.

## Phase 477 — Kategorie-Reihen am Desktop scrollbar (Mausrad → horizontal)
**Datum:** 2026-06-03
Symptom „wischen geht nicht": Am Desktop kein Touch + keine sichtbare Scrollbar → angeschnittene Kacheln unerreichbar. `onwheel`-Handler auf Playlist- und Recent-Leisten wandelt vertikales Mausrad in horizontales Scrollen (`scrollLeft+=deltaY`); `preventDefault` nur, solange die Leiste tatsächlich scrollt (am Ende bleibt Seiten-Scroll frei). `cursor:grab` als Hinweis. Touch-Wischen unverändert nativ. verify 191/191, validate 0 Warnings.

## Phase 478 — BUGFIX: „Land pinnen"-Spiele crashten (undefinierte Daten-Variablen)
**Datum:** 2026-06-03
5 `*_pin_land`-Generatoren referenzierten nicht existierende Daten-Vars → `ReferenceError` → `lq() exhausted` → Spiel startete nicht. Fix: `park_pin_land` THEMEPARKS_DATA→PARKS_DATA · `serie_pin_land` SERIEN_DATA→SERIEN_EXT_DATA · `musik_pin_land` MUSIK_DATA→MUSIK_EXT_DATA · `web_pin_land` WEBKULTUR_DATA→WEB_DATA · `film_pin_land` FILME_DATA→FILME_EXT_DATA. Felder verifiziert. Voll-Audit: keine weiteren undefinierten/ungeschützten `*_DATA`-Referenzen (TECH_DATA ist `typeof`-guarded). verify 191/191, validate 0 Warnings.

## Phase 479 — verify.py-Check (Daten-Variablen) + großes Audit
**Datum:** 2026-06-03
`verify.py` Check 20 ergänzt: jede genutzte `*_DATA` muss definiert oder `typeof`-guarded sein (192/192). Großes 9-Dimensionen-Audit (Build, Sicherheit, Runtime-Refs, i18n, Generatoren, Daten, UX, Fairness, Performance) nach Umbau 467–478 — alle grün, keine offenen 🔴/🟠. Bericht: PHASE479_AUDIT.md.

## Phase 480 — Spiel-Empfehlungen (einzelne Spiele statt nur Kategorien)
**Datum:** 2026-06-03
`_forYouGames()`: schlägt einzelne Spiele vor — ab 5 gespielten Runden, Mix ~60% neu / 40% bewährt aus Top-Kategorien (`gq_played`) + Interessen, mit Kinder-Filter (`_kidHidden`) und nur spielbare (`GEN`). Neue Home-Leiste „🎯 Empfohlene Spiele" (`_renderGameStrip`, Pastell-Tint, Mausrad/Touch-Scroll, weicher Auslauf). Abschaltbar über Einstellungs-Schalter `gq_rec_games` (Standard an). i18n `rec_games_title/rec_setting/rec_sub` de/en/pl. Best-Practice-konform (wischbare Liste, kein Auto-Play, abschaltbar). verify 192/192, validate 0 Warnings.

## Phase 481 — RUNTIME-CRASH-FIX: viele Spiele + Zukunfts-Schutz
**Datum:** 2026-06-03
**Bugs (betraf viele Spiele):**
- `_mkHLQ` war nie definiert → ALLE HL-Vergleichsspiele in Inseln/Gipfel/Klima/Ozeane crashten (`ReferenceError` → `lq() exhausted`). Jetzt definiert: 2-Optionen-`beta_hl`, respektiert `lowerWins`/`unit`.
- `genKlimaPinQ` las `window.LAND_LATLON` — `const LAND_LATLON` liegt NICHT auf `window` → coords immer null → `klima_pin_land` leer. Auf echtes `LAND_LATLON` umgestellt.
- `_trackCatPlay` undefiniert (in try/catch, still) → implementiert (zählt Kategorie-Plays in `gq_catplays`).

**Lehre / Zukunfts-Schutz:** `verify.py` prüfte nur Syntax/Struktur, nicht ob Generatoren laufen → diese Crashes waren unsichtbar. Neu: **Check 20** (undefinierte `*_DATA`) + **Check 21** (undefinierte Helfer-Funktionen, Block-Kommentare ignoriert). Beide Fehlerklassen werden jetzt beim Build erkannt. verify **193/193**, validate 0 Warnings.

## Phase 482 — i18n Hot-Seat-Screen + Zurück rechts
**Datum:** 2026-06-03
Alle hartkodierten DE-Strings im Hot-Seat (renderLVSetup/Handoff/Gameover) → `t()` (de/en/pl, `lv_*`-Keys + `ui_on/ui_off`). „Zurück" von links nach rechts (`align-self:flex-end`). verify 193/193, validate 0 Warnings.

## Phase 483 — i18n Einstellungs-Modal
**Datum:** 2026-06-03
Alle sichtbaren Labels im `renderSettingsModal` → `t()` (de/en/pl, `set_*` + `ui_close`). Nur im isolierten Funktionskörper ersetzt, damit gleichnamige Strings in Profil-Tab/Home-Schwierigkeitsschalter unberührt bleiben. Install-Button via String-Konkatenation (steht in single-quoted JS-String, kein Template-Literal). Verbleibend: An/Aus-Toggle-Texte (ui_on/ui_off-Keys liegen bereit). verify 193/193, validate 0 Warnings.

## Phase 484 — Generator-Rauchtest + hl_river-Fix
**Datum:** 2026-06-03
Neues `smoke_test.js`: lädt `GeoQuest.html` in eine Node-VM mit Browser-Stubs, ruft **jeden** GEN-Modus 6× auf und meldet `THROW` (Crash) + persistentes `NULL`. Fand + fixte **`hl_river`** (`genHLRiverQ`: lokale `const RIVERS_REAL=_rvPool` überschattete die globale `RIVERS_REAL` → TDZ-Crash „before initialization"; lokalen Schatten entfernt, durchgängig `_rvPool`). Ergebnis: 998 getestet, 859 OK, **0 THROW**, 120 `ws_`-NULL (erwartet), 19 NULL (brauchen Live-Daten/Spielzustand → Sichtungsliste). verify 193/193, validate 0 Warnings.

## Phase 485 — Altersstufen 3+4 (11–13 / 14–15)
**Datum:** 2026-06-03
`_kidLevelMax` 1→4 (`gq_kids_grade` 1/2/3/4). `_modeLevel`: Erwachsenen-Trivia (HARD-Keywords + Jahr/Metacritic-ID-Signale) → **Level 5** statt 3, bleibt damit selbst für Stufe 4 (14–15) ausgeblendet (nur 16+). Grade-Selektor auf 4 Stufen erweitert (6–8 · 8–10 · 11–13 · 14–15) + flex-wrap, i18n `kids_grade_t3/t4` de/en/pl. verify 193/193, validate 0, Rauchtest 0 THROW.

## Phase 486 — Lernspiel 1/5: Kompass & Himmelsrichtungen
**Datum:** 2026-06-03
`kompass_richtung` (map_mode): Pfeil-Emoji → Himmelsrichtung antippen (`uk_match`). Mitwachsend: Stufe 1 = 4 Hauptrichtungen, ab Stufe 2 alle 8. Generativ/spracharm, länderübergreifend. i18n `mt_kompass`/`kompass_prompt`/`dir_*` (de/en/pl), `_modeLevel=1`. Lehrplan KS1/KS2 Karten-Orientierung. 999→1000 Modi. verify 193/193, Rauchtest 0 THROW.

## Phase 487 — Lernspiel 2/5: Kontinente-Finder
**Datum:** 2026-06-03
`kontinent_finder` (pure_geo): Flaggen-Emoji + lokalisierter Ländername → „Auf welchem Kontinent?" (`uk_match`, 4 Kontinent-Optionen). Mitwachsend: Stufe 1 nur sehr bekannte Länder (kuratierte cc-Liste), ab Stufe 2 alle ~181. Nutzt COUNTRIES-Schema `{c,cc,ct,sr}` (ct=Kontinent). i18n `mt_kontinent`/`kontinent_prompt`/`cont_*` de/en/pl. Lehrplan KS1. **Rauchtest fand+fixte Schema-Bug** (`continent`→`ct`, sonst immer null). verify 193/193, 0 THROW, 1000→1001 Modi.

## Phase 488 — Lernspiel 3/5: Die 5 Ozeane
**Datum:** 2026-06-03
`ozean_finder` (ozeane): Frage (größter/tiefster/umgibt Antarktis/Nordpol/bei Indien/zwischen Amerika+Europa) → Ozean-Name antippen (`uk_match`, 🌊). Mitwachsend: Stufe 1 nur 3 einfache Fragen, ab Stufe 2 alle 7. i18n `mt_ozean`/`ocn_*`/`ocq_*` de/en/pl. Lehrplan KS1. verify 193/193, 0 THROW, 1001→1002 Modi.

## Phase 489 — Lernspiel 4/5: Tiere & Lebensräume
**Datum:** 2026-06-03
`tier_lebensraum` (tiere): Tier-Emoji → Lebensraum (`uk_match`, 7 Habitate). Mitwachsend: Stufe 1 = 10 bekannte Tiere, ab Stufe 2 alle 25, international, spracharm. i18n `mt_tier`/`tier_prompt`/`hab_*` de/en/pl. Lehrplan KS1/KS2. verify 193/193, 0 THROW, 1002→1003 Modi.

## Phase 490 — Lernspiel 5/5: Jahreszeiten & Halbkugeln
**Datum:** 2026-06-03
`jahreszeit_halbkugel` (klima): Flagge+Land + Monat → Jahreszeit (`uk_match`). Internationaler Twist: Südhalbkugel umgekehrt (NZ Sept=Frühling, Chile Aug=Winter). Mitwachsend: Stufe 1 nur Nordhalbkugel, ab Stufe 2 auch Süd. i18n `mt_jahr`/`jahr_prompt`/`sea_*`/`mon_1..12` de/en/pl. Lehrplan KS2. **Alle 5 Lernspiele fertig.** verify 193/193, 0 THROW, 1003→1004 Modi.

## Phase 491 — Lern-Erklärungen (Extra 2)
**Datum:** 2026-06-03
Die 5 Lernspiele liefern jetzt `meta`-Erklärungen nach der Antwort (Kontinent: Land→Kontinent · Tiere: Emoji→Lebensraum · Ozeane: `ocf_*`-Fakten · Jahreszeiten: Südhalbkugel-Hinweis · Kompass: Karten-Tipp). `uk_match`-Renderer zeigt `q.meta` jetzt nach der Antwort (`sel!==null`) — war vorher gar nicht gerendert. i18n `kompass_meta`/`ocf_*`/`jahr_meta_south` de/en/pl. verify 193/193, 0 THROW.

## Phase 492 — Onboarding: Gate-Fix + Audience→Stufe (Extra 1, schlank)
**Datum:** 2026-06-03
(a) **Gate-Fix:** Onboarding nur noch wenn nicht onboarded UND `!sbUser` UND `!sbAuthPending` → Eingeloggte (auch auf neuem Gerät) sehen die Abfragen nicht, kein Flash während Auth-Check; Direktstart via `/play` für Erstnutzer bleibt. (b) `finishOb` mappt „Wer spielt?" automatisch auf Stufe: kids→Kinder-Modus+Stufe 1, teens→Kinder-Modus+Stufe 3, sonst aus. **Keine extra Onboarding-Frage** (bewusst, Anti-Reibung). Themen-Fortschritt + separate Altersfrage **verworfen** (Aufwand/Nutzen, Reibung). verify 193/193, 0 THROW.

## Phase 493 — FIX: Onboarding-Gate (anonyme = Erstnutzer)
**Datum:** 2026-06-03
Regression aus Phase 492: Die App meldet jeden Besucher anonym an (`signInAnonymously`) → `sbUser` ist immer gesetzt → `!sbUser`-Gate unterdrückte das Onboarding für ALLE (Symptom: in Inkognito kein Onboarding). Fix: Gate prüft `sbUser.is_anonymous` → Onboarding wenn nicht-onboarded UND (kein User ODER anonym) UND `!sbAuthPending`. Registrierte überspringen, Erst-/Anonymnutzer sehen es. verify 193/193, 0 THROW.

## Phase 494 — Onboarding-Alter + btn_next-Fix + Landing-Kontrast
**Datum:** 2026-06-03
(1) **Alters-Auswahl im Onboarding:** Bei „Kind"/„Jugendlich" erscheint darunter eine Stufen-Auswahl (Kind: 6–8/8–10 · Jugendlich: 11–13/14–15) → setzt `gq_kids_grade` präzise via `S.obGrade`; nur bei Kind/Jugendlich sichtbar (keine Reibung für Erwachsene). `finishOb` validiert die Stufe je Audience. (2) `btn_next`: überflüssiges `’` nach dem Pfeil in allen Sprachen entfernt. (3) **landing.html:** `.nav-cta`-Kontrast gefixt — `.nav-links a` (spezifischer) überschrieb `color:#fff`; jetzt `.nav-links a.nav-cta` → weißer Text auf Grün lesbar. verify 193/193, 0 THROW.

## Phase 495 — Tippfehler: `→’` → `→` global
**Datum:** 2026-06-03
Überflüssiges `’` nach dem Pfeil auch in Modus-Namen entfernt (z. B. „Stadt →' Land" → „Stadt → Land"), alle Sprachen. verify 193/193, 0 THROW.

## Phase 496 — Altersstufen-Inhaltsprüfung: Stufe 1 (6–8 J.)
**Datum:** 2026-06-03
Inhaltliche Prüfung pro Stufe (jüngste zuerst). Befund: `_modeLevel` stufte alle `match/_mc/timeline` pauschal als Level 1 ein → 6–8-Jährige sahen 77 Modi, fast alle zu schwer (z. B. Motorbauart, Konsolengeneration, röm. Mythologie-Gegenstücke, Fluss-Mündungsländer). Fix: `match/_mc/timeline` Standard → **Level 2** statt 1. Stufe 1 zeigt jetzt nur die 5 verständlichen Lehrplan-Spiele. Schwerere wandern nach oben (Stufe 2–4-Prüfung folgt). verify 193/193, 0 THROW.

## Phase 497 — Altersstufen-Inhaltsprüfung: Stufe 2 (8–10 J.)
**Datum:** 2026-06-03
Nicht-curriculare Trivia-Kategorien (Games, Autos, Mythologie, Literatur, Brettspiele, Züge/Bahn-Technik, Konsolen) + Zeitleisten → **Level 3** (Teens), via Token-Treffer im Modus-Namen (`auto/games/konsole/hw_/myth/lit_/boardgame/zug/bahn/timeline`, fängt auch `hl_`-Varianten). Stufe 2 zeigt jetzt Geografie + Natur (Flaggen, Hauptstädte, Flüsse, Kontinente, Tiere, Pflanzen, Themenparks, Hunde, Astro/Geo-Vergleiche). verify 193/193, 0 THROW.

## Phase 508 — UX: leere Kategorien im Kinder-Modus ausblenden
**Datum:** 2026-06-03
Neuer Helfer `_catKidCount(k)` (zählt nicht-`_kidHidden` Modi einer Kategorie). `_CAT_ORDER`-Kinderfilter blendet Kategorien mit 0 sichtbaren Modi für die aktuelle Stufe aus. Stufe 1: 14 statt 24 Kategorien (keine leeren Inseln/Gipfel/Autos/Games), Stufe 2: 22, Stufe 3/4: alle. Kein Kind landet mehr auf einer leeren Kategorie; Kategorien erscheinen mit dem Alter. verify 193/193, 0 THROW.

## Phase 509 — Hochstufen-System für clevere Kinder (nicht streng nach Alter)
**Datum:** 2026-06-03
`_kidLevelMax` = Basis-Stufe + `gq_kid_boost` (gedeckelt). Kind-Knopf „🚀 Schwerere Fragen" am Spielende (Kinder-Modus, ≥8/10, solange Cap nicht erreicht) erhöht Boost +1. **Cap:** Basis <3 → max 4 (nie 16+); Basis ≥3 (11–15) → bis 5 (16+) erreichbar, AUSSER `gq_block_adult` gesetzt. Eltern-Schalter „16+ ab Stufe 11–13 zulassen" (PIN-gesichert via `pinMode='adultblock'`) + Schwierigkeit-Reset in Einstellungen. Grade-Wechsel resettet Boost. i18n de/en/pl. verify 193/193, 0 THROW.

## Phase 510 — ABSTURZ-FIX: type:"match"-Modi (undefined.map)
**Datum:** 2026-06-03
4 Generatoren (`genInselnMatchExt`, `genGipfelMatchExt`, `genKlimaMatchExt`, `genOzeaneMatchExt`) lieferten `type:"match"` mit `subject/choices/answer`. Der Spiel-Renderer hat keinen `match`-Zweig → `q.opts.map(...)` auf `undefined` → **App-Absturz** („Cannot read properties of undefined (reading 'map')") beim Spielen (Klima-Zone, Inseln→Ozean, Gipfel→Gebirge, Ozean-Typ); zeigte vorher großes „1/10". Auf `uk_match` umgestellt (subj=Item, 4 Attribut-Optionen, korrekte Antwort). verify 193/193, 0 THROW.

## Phase 511 — GROSSER ABSTURZ-FIX: 74 Kinder-Spiele (Schema-Normalisierung)
**Datum:** 2026-06-03
Die parallel (Phase 505) ergänzten einfachen Kinder-Modi gaben `type:"uk_match"` mit **falschen Feldnamen** (`question/options/correct` statt `subj/opts/ans`) zurück → Renderer `q.subj.replace(undefined)` → **App-Absturz beim Spielen** (74 Spiele). Fix: zentrale **Schema-Normalisierung in `lq()`** (question→subj, options→opts, correct→ans, fehlender `prompt` aus Modus-Titel, `lid` generiert, timeline-items `label`→`n`). Außerdem Optionen-Render gehärtet (`String(o).replace` → numerische Optionen wie FCI-Gruppe). Neuer In-Game-Render-Test (alle 1088 Modi im Spiel-Screen) bestätigt: 0 echte Render-Fehler. verify 193/193, 0 THROW.

## Phase 512 — Admin: Altersstufen-Vorschau-Schalter
**Datum:** 2026-06-03
In den Einstellungen nur für `sbUser.email==='andre69190@gmail.com'` sichtbarer Schalter mit 6 Buttons (Erwachsen / 1 · 6–8 / 2 · 8–10 / 3 · 11–13 / 4 · 14–15 / 16+ Boost). Klick setzt `gq_kids_mode`+`gq_kids_grade`(+`gq_kid_boost`), schließt Settings → Home zeigt die gewählte Stufe. Admin kann jede Altersstufe separat ansehen. verify 193/193, 0 THROW.

## Phase 513 — Test-Suite gehärtet + dokumentiert
**Datum:** 2026-06-03
`ingame_render_test.js` verfeinert (Timeline-Feedback übersprungen, `ans-in-opts` nur für `uk_match` mit Klammer-Bereinigung → Info: 31 Treffer). Session-Starter um **TEST-SUITE**-Sektion ergänzt (verify.py + validate_content.py + smoke_test.js + ingame_render_test.js, Sollwerte + Bug-Klassen). 4-Ebenen-Absicherung gegen Struktur-, Generator-, Render- und Anzeigefehler.

## Phase 514 — Lösbarkeits-Garantie (uk_match: ans immer in opts)
**Datum:** 2026-06-03
`lq()` stellt jetzt sicher: bei `type:"uk_match"` ist die richtige Antwort IMMER unter den Optionen (sonst wird ein Distraktor durch `q.ans` ersetzt). Behebt 33 `uk_*`-Wissensquartett-Modi, deren `fixedOpts` den korrekten Wert nicht enthielten (z. B. „Insektivor"/„Nektarivor" fehlten) → Frage war **unlösbar**. Verifiziert: roh unlösbar → nach lq lösbar. **Hinweis:** einige Generatoren (z. B. `uk_emob_bidirektional`) ziehen die Antwort aus einem falschen Datenfeld (Land statt Kategorie) → jetzt lösbar, aber inhaltlich schwach (separate Datenprüfung empfohlen). verify 193/193, 0 THROW.

## Phase 515 — Gezielte Reparatur: unlösbare uk_match-Fragen am Generator
**Datum:** 2026-06-03
`_mkMatchQ` (emob/gastro/arch/…), `genTiereMatchQ`, `genPflanzenMatchQ`: `fixedOpts` wird nur noch verwendet, wenn die richtige Antwort (`cor.c`) enthalten ist; sonst Optionen **dynamisch aus den echten Werten dieses Modus** (gleiche Art wie die Antwort) → konsistent + lösbar. `ans-nicht-in-opts` 33 → **0** (mehrere Zufallsläufe). Zusammen mit der `lq()`-Garantie (Phase 514) doppelt abgesichert. verify 193/193, 0 THROW, 0 Render-Fehler.

## Phase 516 — Datenreparatur: tiere_match.ernaehrung + genTiereMatchQ-Distraktoren
**Datum:** 2026-06-03
20 vertauschte Einträge (n=Nahrung/c=Tiername) richtiggestellt → n=Tier, c=Ernährungstyp; alle `c` auf 8 kanonische Typen normalisiert; 2 Dubletten entfernt (80→78); `fixedOpts` entfernt. `genTiereMatchQ` baut Distraktoren jetzt **nur aus derselben Kategorie** (keine fremden Tiernamen mehr als Optionen). Ergebnis: kohärent („Koala → Herbivor"), 0 unlösbar über 2480 Stichproben. `gastro_gewuerzmischungen` geprüft = stimmig.

## Phase 517 — Options-Qualität: doppelte Optionen behoben + Dauertest
**Datum:** 2026-06-03
4 Jahr-MC-Generatoren (`genAutoBaujahrMC`/`genGamesBaujahrMC`/`genHWBaujahrMC`/`genGamesPeakYearMC`) + `genSubwayQ` zeigten **doppelte Optionen** (z. B. `1999/1999`; subway sogar die Antwort `12` doppelt), weil die Distraktor-Pools nicht dedupliziert wurden. Fix: Pool per `Set` deduplizieren und die Antwort ausschließen. Neuer Dauertest **`option_quality_test.js`** (5. Test-Ebene) prüft alle MC-Modi auf doppelte/einzelne Optionen. Ergebnis: **0 DUP, 0 SINGLE**.

## Phase 519 — i18n-Vollständigkeit (EN/PL) + Dauertest
**Datum:** 2026-06-03
704 bisher unübersetzte, tatsächlich genutzte Prompt-Strings nach **EN + PL** übersetzt (`data/i18n_extra.json`), zur Laufzeit per `Object.assign` in `_CONTENT_I18N` gemergt (`gen.py` lädt die Datei + `PLACEHOLDER_I18N_EXTRA`, Merge hinter `_tcc`-Def). `build_i18n_extra.py` erzeugt die Datei reproduzierbar (inkl. Auto-Template „Bilde Wörter aus X!"). Lücke en/pl: **0** (vorher 702/704). Neuer Dauertest **`i18n_test.js`** (6. Ebene): jeder genutzte `_tc/_tcc`-String + `MODES.prompt` muss in `en` UND `pl` existieren. verify 194/194, validate 0 Warnungen.

## Phase 521 — Kontrast-Fix Dunkel-Theme + Kontrast-/Performance-Tests
**Datum:** 2026-06-03
Der neue `contrast_check.py` deckte auf: im **Dunkel-Theme** blieb `--qcard:#fff` (weiß) bei `--text:#f1f5f9` → Quizkarten-Text faktisch unsichtbar (**1.10:1**). Fix: `--qcard:#1e293b`, `--text3:#8a96ab` (heller). Zwei neue Dauertests: **`contrast_check.py`** (WCAG AA für Text-auf-Fläche, Hell+Dunkel) und **`perf_check.py`** (HTML-/SW-Precache-Größe). Kontrast 0 FAIL, perf 0 FAIL (1 WARN: SW-Precache ~10 MB). Test-Suite jetzt **8 Ebenen**.

## Phase 522 — Service-Worker-Precache verschlankt (App-Shell statt alles)
**Datum:** 2026-06-03
Beim Install wird nur noch die **App-Shell** (`GeoQuest.html`/`manifest`/`icon`, ~6.1 MB) vorab gecacht; alle `data/*.json` werden vom bestehenden Fetch-Handler **bei Bedarf zur Laufzeit** gecacht (`cache.put`). Hash bleibt über ALLE Assets (inkl. Daten) → `CACHE_NAME` bumpt bei Datenänderung, alte Runtime-Caches werden in `activate` gelöscht (kein veraltetes Offline-Datum). SW-Precache **10.1 → 6.1 MB** (Quota-Risiko weg). verify-Check 12 angepasst (Shell + Runtime-Cache statt „alle Daten im Precache"). `perf_check.py` 0 WARN.

## Phase 523 — uk_pin Feedback-Bug (0 km fälschlich falsch)
**Datum:** 2026-06-03
Bei Zeitablauf wurde eine Pin-Frage über das generische `answer(null)` beantwortet (`S.sel="__t"`), `airportPinDist` blieb ungesetzt → Anzeige „✗ 0 km entfernt" (widersprüchlich, 0 km wäre perfekt). Fix: Pin-Feedback prüft `S.sel==='coord'` (echter Pin gesetzt); sonst Meldung „Zeit abgelaufen – kein Pin gesetzt" (DE/EN/PL). `build_i18n_extra.py` um `EXTRA_UI` erweitert.

## Phase 524 — Pin-Modus komplett kaputt (lat/lng vs targetLat/targetLng)
**Datum:** 2026-06-03
Echte Ursache des „0 km ✗"-Bugs: `genCapitalsPinQ` (u. a.) liefert `lat/lng`, aber uk_pin-**Scoring & Kartenmarker** lesen `targetLat/targetLng` → Distanz `NaN` → **jede** Pin-Eingabe „✗ 0 km entfernt" (Hauptstädte-Pin völlig unspielbar). Fix in der Schema-Normalisierung (`nextQ`): `uk_pin`/`airport_pin` erhalten `targetLat/targetLng` als Fallback aus `lat/lng` (+ `ans` aus `subj`) → deckt **alle** Pin-Generatoren ab. Verifiziert: Capitals-Pin self-dist 0, ok=true.

## Phase 525 — Tote Spielmodi repariert (12 Modi) + smoke-Gate
**Datum:** 2026-06-03
Drei Ursachen für immer-NULL: (1) Attribut-Match-Generatoren (`genAutosMatchExt`/Games/Konsolen/Garten/Capitals) verlangten 3 Distraktoren, aber Felder wie `antrieb`/`herkunftsland`/`wasserbedarf`/`grossstadt`/`adaption` haben nur 2–3 verschiedene Werte → Schwelle `pool<3`→`<1` (2–4 Optionen) + Boolean→Ja/Nein-Mapping (turbo). (2) `spiel_*` behandelten `BOARDGAMES_DATA` (Objekt) als Array → `_bgArr()`-Adapter. (3) `genArchPinQ` doppelt definiert — die `var`-Zuweisung (`_mkPinQ`, braucht `cat`-Arg) überschrieb die korrekte Funktion → entfernt. **12 Modi wieder spielbar** (smoke OK 944→956). `smoke_test.js` mit `EXPECTED_NULL`-Allowlist (async-Daten + Custom-Flow); unerwartete NULL lässt den Test jetzt fehlschlagen. Fehlalarme: 8 async-Daten-Modi (license_plates/rivers/neighbors/area.json) + 3 Custom-Flow-Modi (logic_grid/travel_route/slf).

## Phase 526 — Rest-i18n: spielerseitige UI-Labels
**Datum:** 2026-06-03
Verbleibende hartkodierte deutsche UI-Labels auf Spieler-Screens (Wortschmiede/Logik-Gitter/Navigation) in `_tc()` gewrappt: „Verfügbare Buchstaben:", „Überprüfen", „Schließen", „WÖRTER", „Keine Wörter gefunden", „Länder"/„Städte", „Zum Menü". EN/PL in `i18n_extra.json` + `build_i18n_extra.py` EXTRA_UI (reproduzierbar). i18n 0 Lücken. Bewusst nicht übersetzt (Edge/intern): Admin-Panel, Ad-Platzhalter, Absturz-Screen.

## Phase 527 — White-Screen-Crash behoben (.map auf undefined im Render)
**Datum:** 2026-06-03
Der Render rief `.map` auf evtl. undefinierten Feldern auf (`q.hints`, `q.countries`, `q.opts` in 2 Zweigen, `q._tlUserOrder`, `q.ans`). Bei Modi, die der Render-Test überspringt (async-Daten: border_q/neighbor/plate/river — headless = null), konnte das die **ganze App** abstürzen lassen („Cannot read properties of undefined (reading 'map')"). Alle `q.X.map`-Aufrufe im Render mit `||[]`/`Array.isArray` abgesichert (0 ungeschützt). Generatoren von `sort_rank`/`clue_country` setzen ihre Felder korrekt — der Guard ist reine Absicherung gegen White-Screens.

## Phase 528 — Globales Render-Sicherheitsnetz (kein White-Screen mehr)
**Datum:** 2026-06-03
`render()` ist jetzt ein Wrapper mit `try/catch` um `_renderInner()`. Bei **jedem** Render-Fehler erscheint ein sanfter Fallback („Überspringen" via `clr()+nextRound()` / „Zum Menü") statt des kompletten App-Absturzes („GeoQuest ist abgestürzt"). Fallback-Texte DE/EN/PL. Verifiziert: Wrapper fängt echten Render-Fehler ab (loggt `[GQ] render error`, propagiert nicht); 955 Render OK, keine Regression. Fängt künftige unbekannte Render-Ursachen generell ab — Ergänzung zu den `.map`-Guards (Phase 527).

## Phase 529 — Testlücke async-Modi geschlossen
**Datum:** 2026-06-03
`ingame_render_test.js` seedet jetzt die async geladenen Daten: `NEIGHBORS=_DEFAULT_NEIGHBORS` (Live-Fallback, da `neighbors.json` leere `neighbors` enthält) und transformiert `rivers/license_plates/area.json` direkt ins Zielformat (die Parser sind inner-scoped, nicht von außen aufrufbar). Damit werden `border_q`/`neighbor`/`river_real`/`plate_*`/`hl_area` **wirklich gerendert** (955→**962 OK**, 0 Render-Fehler) — genau die Modi, über die der White-Screen-Crash durchrutschte.

## Phase 530 — Barrierefreiheit (alt + aria-label) + Dauertest
**Datum:** 2026-06-03
7 Flaggen-`<img>` ohne `alt` → `alt="Flagge"` ergänzt (0 verbleibend). `aria-label` für Icon-only-Buttons: HUD (Vorlesen/Feedback/Beenden/Einstellungen, 27×) + Löschen/Bestätigen/Aktualisieren/Schließen (7×). Neuer Dauertest **`a11y_check.py`** (9. Ebene): **FAIL** bei `<img>` ohne `alt`, **WARN** bei Icon-only-Buttons ohne Label. Ergebnis: 0 FAIL, 69→3 WARN.

## Phase 531 — Performance: license_plates.json nicht-blockierend laden
**Datum:** 2026-06-03
`license_plates.json` (3,2 MB) war die **erste** sequenzielle `await`-Fetch beim Start (18 %) und blockierte die App-Initialisierung. Jetzt **nicht-blockierend** nachgeladen: App startet sofort, `PLATES_DATA` wird per `fetch().then()` befüllt, sobald die Datei da ist. Plate-Modi liefern bis dahin `null` (graceful, identisch zum Ladefehler-Fall) und funktionieren danach. Verifiziert: vor Load `null`, nach Load OK. SW-Runtime-Cache übernimmt die Datei nach dem ersten Laden.

## Phase 532 — Inhaltsfeinschliff emob_match (bidirektional + level_autonomy)
**Datum:** 2026-06-03
`bidirektional`: `c` enthielt echten Müll (`Deutschland`, `Wirtschaftlichkeit`, `Batterieverschleiß`) und Varianten (`V2H Backup`, `V2G Japan`, `V2L KIA`) → n-basiert auf saubere **V2H/V2G/V2L/V2V** normalisiert. `level_autonomy`: Varianten (`Level 4`, `Level 5`, `Level 2+`, `Level 0`, `Level 4 (begrenzt)`) → die 4 Stufen. Beide jetzt 100 % in `fixedOpts` → klare 4-Optionen-Fragen. **Bewusst belassen:** `stecker`/`zellchemie`/`motorentypen`/… — ihre reicheren `c`-Werte (J1772/NACS/…) sind *korrekter* als ein Zwang in 4 Buckets und liefern seit Phase 515 bereits präzise Fragen.

## Phase 533 — Daily Challenge: teilbares Emoji-Ergebnis (Worldle-Stil)
**Datum:** 2026-06-03
Die Daily Challenge (Seed/Pool/Resume/7-Tage-Streak) existierte bereits — es fehlte der **virale Kern**. Ergänzt: pro Runde ✓/✗ in `S.dailyMarks` (in `answer`+`answerAirportPin`), persistiert in Daily-Progress + `markDailyDone`. Im „erledigt"-Hero: 10-Felder-Emoji-Raster (🟩/🟥) + **Teilen-Button** → `shareDailyResult()` (navigator.share bzw. Clipboard; Text: Datum, Emoji, X/10, Streak 🔥, URL). i18n DE/EN/PL. Verifiziert: Emoji/Share/Persistenz korrekt.

## Phase 534 — Spaced Repetition / Fehler-Training (Leitner)
**Datum:** 2026-06-03
Falsch beantwortete Fragen werden als **Snapshot** in `gq_srs` erfasst (`answer`+`answerAirportPin`, nur replaybare Typen MC/HL/Pin). Leitner-Boxen 1–5 mit Intervallen (0/0/2/5/12 Tage), Box 5 = gemeistert (entfernt). Neuer Modus **„Schwächen üben"** (`startSrsReview`/`srsNext`) spielt fällige Items wieder; `nextRound` erkennt `S.srsRun`. Home-Card `renderSrsHero` zeigt die Fälligkeits-Zahl (nur wenn > 0). i18n DE/EN/PL. Verifiziert: Erfassen/Box-Logik/Mastery/Review-Start korrekt. Adressiert den häufigsten App-Store-Wunsch („smart review statt Zufall").
