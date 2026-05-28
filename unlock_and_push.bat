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
git commit -m "FEATURE: Phase 255+256. P255: Onboarding i18n-Fix, Landing-Page, impressum.html, datenschutz.html, robots.txt, sitemap.xml, vercel.json. P256: Text-to-Speech (Auto+Manuell, TTS-Toggle in Settings, clr() Stop), Feedback-Formular (Supabase feedback-Tabelle + Mail-Fallback), 💡+🔊 in allen HUD-Leisten. verify: 89/89."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
