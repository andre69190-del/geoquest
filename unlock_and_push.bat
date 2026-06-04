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
git commit -m "Content: Phase 469. Ausfuehrliches Handbuch (renderGuideModal): 2 Tabs 'Fuer Kinder' (kindgerecht: Wie spiele ich, Spielarten, Punkte/Streak/Sticker, Tipps) + 'Fuer Eltern & alle' (Kinder-Modus, Klassenstufen, Eltern-PIN, Mehrspieler, Bestenlisten/Fairness/Uebungsmodus, weitere Funktionen). Erreichbar via Einstellungen-Button + Link aus Hilfe-Overlay. Texte DE/EN/PL in LANG (guide_*), uebrige Sprachen Fallback EN. State S.guideModal/guideTab. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
