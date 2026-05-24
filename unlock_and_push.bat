@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "DATA: Phase 215 — Massive Content Expansion. DE_PLATES: 289->539 (echte Altkennzeichen). AIRPORTS: 40->173 (Top-Weltflughaefen mit IATA+Koordinaten). CURR_REAL: 0->141 (alle aktiven Weltwaehrungen behoben). KULTUR_DATA: 5->30 Eintraege in 6 Kategorien (streetfood, wahrzeichen, museen, getraenke, feste, instrumente) + 40 Wolkenkratzer neu. HL_BETA_DATA: 15->112 Laender (rain/temp/sun/vulc/parks/roads/rail/net/ev/urban/lang/isl/tz/founded/unesco/tour/wm). Also: Phase 219 Catalog Audit, Phase 218 Beta-Labels raus, Phase 217 H/L Proximity."
git push origin main
pause
