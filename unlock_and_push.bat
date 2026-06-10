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
git commit -m "Content: Phase 533. Daily Challenge: teilbares Emoji-Ergebnis (Worldle-Stil) ergaenzt. Pro Runde wird ✓/✗ in S.dailyMarks getrackt (answer + answerAirportPin), in Daily-Progress + markDailyDone persistiert. Im 'erledigt'-Hero: 10-Felder Emoji-Raster (🟩/🟥) + Teilen-Button -> shareDailyResult() nutzt navigator.share bzw. Clipboard (Text: Datum, Emoji, X/10, Streak, URL). i18n DE/EN/PL. Bestehende Daily-Mechanik (Seed/Pool/Resume/7-Tage-Streak) war schon da; das virale Teilen fehlte.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
