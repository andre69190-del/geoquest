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
git commit -m "Content: Phase 519. i18n-Vollstaendigkeit: 704 bisher unuebersetzte, tatsaechlich genutzte Prompt-Strings nach EN+PL uebersetzt (data/i18n_extra.json), per Object.assign in _CONTENT_I18N gemergt (gen.py laedt + PLACEHOLDER_I18N_EXTRA). build_i18n_extra.py erzeugt die Datei reproduzierbar (inkl. Auto-Template fuer 'Bilde Woerter aus X!'). Luecke en/pl: 0 (vorher 702/704). Neuer Dauertest i18n_test.js (6. Ebene): jeder genutzte _tc/_tcc-String + MODES.prompt muss in en UND pl existieren. verify 194/194, validate 0 Warnungen, 0 Render-/Options-Fehler.. verify: 194/194."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
