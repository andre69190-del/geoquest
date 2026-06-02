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