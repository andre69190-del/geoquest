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
4. Check verify.py output: 33/33 [OK]
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
