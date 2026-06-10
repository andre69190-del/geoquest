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
git commit -m "Content: Phase 528. Globales Render-Sicherheitsnetz: render() in Wrapper mit try/catch gekapselt (render->_renderInner + Wrapper). Bei JEDEM Render-Fehler erscheint ein sanfter Fallback (Ueberspringen via clr()+nextRound() / Zum Menue) statt White-Screen-Absturz 'GeoQuest ist abgestuerzt'. Fallback i18n DE/EN/PL. Verifiziert: Wrapper faengt echten Render-Fehler ab (loggt '[GQ] render error', kein Throw); 955 Render OK, keine Regression. Das faengt kuenftige unbekannte Render-Ursachen generell ab.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
