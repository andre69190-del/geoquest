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
git commit -m "Content: Phase 483. i18n Einstellungs-Modal: alle Labels (Weitere Einstellungen, Heimatregion, Vorlesen/TTS, Hardcore-Modus, Raster, Reihen, Kategorie-Reihen, Feedback, App installieren, Schliessen, Reset-Toast, 'Nicht gesetzt') -> t() de/en/pl (set_*/ui_close). Nur im isolierten renderSettingsModal-Body ersetzt (Profil-/Home-Duplikate unberuehrt). Install-Button via String-Konkat (single-quoted String). verify 193/193.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
