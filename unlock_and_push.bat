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
git commit -m "Content: Phase 492. Onboarding (Extra 1, bewusst schlank): (a) Gate-Fix - Onboarding erscheint nur noch wenn NICHT onboarded UND nicht eingeloggt (sbUser) UND Auth nicht pending. Eingeloggte auf neuem Geraet sehen die Abfragen nicht mehr, kein Flash waehrend Auth-Check. Direktstart via /play funktioniert weiterhin fuer Erstnutzer. (b) finishOb mappt 'Wer spielt?' automatisch auf Altersstufe: kids->Kinder-Modus+Stufe1, teens->Kinder-Modus+Stufe3, sonst Kinder-Modus aus. KEINE zusaetzliche Onboarding-Frage (bewusst, Anti-Reibung). Themen-Fortschritt + extra Altersfrage verworfen (nicht sinnvoll/nervig). verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
