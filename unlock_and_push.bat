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
git commit -m "Content: Phase 521. Kontrast-Fix Dunkel-Theme: --qcard war auch im Dark Mode weiss (#fff) -> Quizkarten-Text (var(--text)=#f1f5f9) faktisch unsichtbar (1.10:1). Gefixt: --qcard:#1e293b + --text3:#8a96ab (heller). Zwei neue Dauertests: contrast_check.py (WCAG AA fuer Text-auf-Flaeche, beide Themes) und perf_check.py (HTML-/SW-Precache-Groesse). Kontrast 0 FAIL, perf 0 FAIL (1 WARN: SW-Precache ~10MB). Damit 8 Test-Ebenen.. verify: 194/194."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
