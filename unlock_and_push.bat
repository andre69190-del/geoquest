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
git commit -m "Content: Phase 548. Neues Stufe-1-Spiel 'Tierkinder' (tiere_baby, Kategorie tiere, Level 1): Emoji-Tier zeigen, Tierkind aus 4 waehlen (Welpe/Kaetzchen/...). Template fuer altersgerechte Kinderspiele: sprachneutrale Emoji-Frage + i18n-Optionen (_tc) -> automatisch DE/EN/PL. Inline-Daten. In L1-Liste, tiere-modes, GEN. 1090->1091 Modi. Verifiziert: Level 1, loesbar, EN/PL.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
