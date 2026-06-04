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
git commit -m "Content: Phase 509. Hochstufen-System (cleveren Kindern, nicht streng nach Alter): _kidLevelMax nutzt jetzt gq_kid_boost (effektive Stufe = Basis+Boost). Kind-Knopf '🚀 Schwerere Fragen' am Spielende (nur Kinder-Modus, bei >=8/10 richtig, solange Cap nicht erreicht) erhoeht Boost um 1. Cap: Basis-Stufe <3 -> max 4 (nie 16+); Basis-Stufe >=3 (11-13/14-15) -> bis 5 (16+) erreichbar, AUSSER gq_block_adult gesetzt. Eltern-Schalter in Einstellungen '16+ ab Stufe 11-13 zulassen' (PIN-gesichert via pinMode adultblock, falls PIN gesetzt) + Schwierigkeit-Reset. Grade-Wechsel setzt Boost zurueck. i18n de/en/pl. verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
