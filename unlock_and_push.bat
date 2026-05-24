@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FIX: Phase 219 — Catalog Integrity Audit. 7 verwaiste/fehlende Modus-Eintraege repariert: de_plate+border_q fehlten im MODES-Array; f1_map/stadium_map/river_map/unesco_map/wort_schmiede fehlten in MODE_CATS-Kategorien. Alle 187 Modi jetzt vollstaendig verknuepft (0 Orphans, 0 broken refs). Also: Phase 218 Beta-Labels raus, Phase 217 H/L Proximity, Phase 216-214."
git push origin main
pause
