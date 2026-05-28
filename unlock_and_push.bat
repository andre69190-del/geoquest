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
git commit -m "UX: Phase 257. HUD-Cleanup: Fehler-Button entfernt. TTS+Feedback-Buttons im HUD. Startseite: 💡 Feedback-Button neben Coins. TTS 🔊 grün wenn aktiv. verify: 89/89."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds.
pause
