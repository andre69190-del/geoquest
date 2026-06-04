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
git commit -m "Content: Phase 493. FIX (Regression aus 492): Onboarding-Gate unterdrueckte ALLE, weil die App jeden Besucher anonym anmeldet (signInAnonymously) -> sbUser immer gesetzt. Gate prueft jetzt sbUser.is_anonymous: Onboarding erscheint wenn nicht-onboarded UND (kein User ODER anonymer User) UND Auth nicht pending. Registrierte ueberspringen, Erst-/Anonymnutzer (auch Inkognito) sehen es. verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
