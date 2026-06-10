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
git commit -m "Content: Phase 547. Doku-Zugang + Erstnutzer-Hinweise: (1) Prominenter 'Handbuch & Hilfe'-Button im Profil-Tab -> oeffnet renderGuideModal direkt (statt 2 Klicks ueber Hilfe->Mehr). (2) Einmaliger Tipp-Toast beim ERSTEN Oeffnen von 'Region ueben' (openRegionModal, gq_seen_region) und 'Schwaechen ueben' (startSrsReview, gq_seen_srs). i18n DE/EN/PL. Verifiziert: Button da, Toast nur 1x.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
