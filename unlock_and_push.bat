@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
python3 verify.py || (echo. && echo [ABORT] verify.py FAILED - fix errors before pushing! && pause && exit /b 1)
echo.
git add -A
git commit -m "BUGFIX+LANDING: Phase 255. Onboarding i18n-Fix: Weiter-Button setzt S.language=S.obLang+localStorage -> Schwierigkeits-Screen in korrekter Sprache. Landing: UTF-8 Umlaute, impressum.html, datenschutz.html, robots.txt, sitemap.xml, vercel.json. gen.py Trailing-Paren-Fix. verify: 89/89."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
