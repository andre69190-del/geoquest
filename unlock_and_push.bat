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
git commit -m "Content: Phase 454. KRITISCHER FIX + Personalisierung Portion 3/4: Home-Tab rief undefinierte Symbole auf (_getKidsMode, _toggleKidsMode, KIDS_CATS, _getTotalPlays, _getTopCats, _renderPlaylistStrip, PLAYLISTS) -> Laufzeit-ReferenceError, Home crashte (von verify/node nicht erkannt, da nur Syntax). Alle Helfer definiert und mit CAT_META verdrahtet: Kinder-Modus-Toggle (KIDS_CATS aus CAT_META audience), 5 kuratierte Playlists, Für-dich-Empfehlung (top-Kategorien aus Spielhistorie ab 10 Spielen, sonst aus Onboarding-Interessen via _getInterestCats). i18n DE/EN/PL. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
