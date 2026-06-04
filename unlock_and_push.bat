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
git commit -m "Content: Phase 491. Lern-Erklaerungen (Extra 2): die 5 neuen Lernspiele liefern jetzt meta-Erklaerungen nach der Antwort (Kontinent: Land->Kontinent, Tiere: Emoji->Lebensraum, Ozeane: ocf_*-Fakten, Jahreszeiten: Suedhalbkugel-Hinweis, Kompass: Karten-Tipp). uk_match-Renderer zeigt q.meta jetzt nach Antwort (sel!=null) - war vorher unsichtbar. i18n kompass_meta/ocf_*/jahr_meta_south de/en/pl. verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
