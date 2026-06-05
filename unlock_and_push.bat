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
git commit -m "Content: Phase 512. Admin: Altersstufen-Vorschau-Schalter in Einstellungen, nur sichtbar fuer sbUser.email=andre69190@gmail.com. 6 Buttons: Erwachsen / 1(6-8) / 2(8-10) / 3(11-13) / 4(14-15) / 16+(Boost). Setzt gq_kids_mode+gq_kids_grade(+boost), schliesst Settings -> Home zeigt die jeweilige Stufe. Damit kann der Admin jede Altersstufe separat ansehen. verify 193/193.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
