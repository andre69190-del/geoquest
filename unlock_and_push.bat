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
git commit -m "Content: Phase 490. Lernspiel 5/5: Jahreszeiten & Halbkugeln (jahreszeit_halbkugel, Kategorie klima). genJahreszeitQ: Flagge+Land + Monat -> welche Jahreszeit? (uk_match, 4 Jahreszeiten). Internationaler Twist: Suedhalbkugel umgekehrt (NZ Sept=Fruehling, Chile Aug=Winter). Mitwachsend: Stufe 1 nur Nordhalbkugel (einfach), ab Stufe 2 auch Suedhalbkugel. i18n mt_jahr/jahr_prompt/sea_*/mon_1..12 de/en/pl. Lehrplan KS2 Halbkugeln. ALLE 5 Lernspiele fertig. verify 193/193, 0 THROW, 1004 Modi.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
