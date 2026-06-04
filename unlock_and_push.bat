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
git commit -m "Content: Phase 489. Lernspiel 4/5: Tiere & Lebensraeume (tier_lebensraum, Kategorie tiere). genTierLebensraumQ: Tier-Emoji -> Lebensraum antippen (uk_match, 7 Lebensraeume: Wueste/Ozean/Polar/Regenwald/Savanne/Wald/Gebirge). Mitwachsend: Stufe 1 nur 10 sehr bekannte Tiere, ab Stufe 2 alle 25 (international). Spracharm (Emoji). i18n mt_tier/tier_prompt/hab_* de/en/pl. Lehrplan KS1/KS2 Habitate. verify 193/193, 0 THROW, 1003 Modi.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
