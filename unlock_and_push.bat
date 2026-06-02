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
git commit -m "Content: Phase 441. Audit-Fixes: (1) Build-Breaker behoben — ungueltiger Unicode-Escape im Wort gießen (Modus garten_match_wasser), verify war 172/173 JS-Syntaxfehler. (2) 13 fehlende PL-Uebersetzungen in _CONTENT_I18N ergaenzt (Film-/Musik-Kategorie: Regisseur, IMDb, Oscars, Grammys, Streams, Tontraeger u.a.). verify 173/173, validate 74/74 0 Warnings, check_session 15/15.. verify: 173/173."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
