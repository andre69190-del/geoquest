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
git commit -m "Content: Phase 466. UX-Review Paket 1+2+3: (1) Kontrast: --text3 #94a3b8->#64748b (war WCAG-Fail ~2.8:1), mode-desc #64748b->#475569. (2) Mode-Karten: Info-i als runder Badge oben rechts (22px, border-radius 50%), Favoriten-Herz als Outline (🤍/❤️) oben links, 28px-Boden-Reserve entfernt -> Titel hat untere Haelfte frei. (3) Spacing: Suchleiste mehr Luft. verify 191/191, validate 0 Warnings.. verify: 191/191."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
