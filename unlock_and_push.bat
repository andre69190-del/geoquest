@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py
if errorlevel 1 (
    echo.
    echo ABORT: verify.py FAILED - fix errors before pushing!
    pause
    exit /b 1
)
echo.
git add -A
git commit -m "Content: Phase 486. Lernspiel 1/5: Kompass & Himmelsrichtungen (kompass_richtung, Kategorie map_mode). genKompassQ: Pfeil-Emoji -> Himmelsrichtung antippen (uk_match-Typ). Waechst mit Alter: Stufe 1 nur 4 Hauptrichtungen, ab Stufe 2 alle 8 (N/NO/O/SO/S/SW/W/NW). Spracharm/generativ, laenderuebergreifend. i18n mt_kompass/kompass_prompt/dir_* de/en/pl. _modeLevel=1 (skaliert selbst). Lehrplan KS1/KS2 Karten-Orientierung. verify 193/193, Rauchtest 0 THROW, 1000 Modi.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
