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
