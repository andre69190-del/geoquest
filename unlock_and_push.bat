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
git commit -m "Content: Phase 514. LOESBARKEITS-GARANTIE: in lq() sichergestellt, dass bei type:uk_match die richtige Antwort IMMER unter den Optionen ist (sonst wird ein Distraktor durch q.ans ersetzt). Behebt 33 uk_*-Wissensquartett-Modi, deren fixedOpts den korrekten Wert nicht enthielten (z.B. Insektivor/Nektarivor fehlten bei [Omnivor/Herbivor/Karnivor/Frugivor]) -> Frage war unloesbar. Jetzt alle loesbar (verifiziert: roh unloesbar -> nach lq loesbar). HINWEIS: einige Generatoren (z.B. uk_emob_bidirektional) ziehen die Antwort aus einem falschen Datenfeld (Land statt Kategorie) - jetzt loesbar aber inhaltlich schwach, separate Daten-Pruefung empfohlen. verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
