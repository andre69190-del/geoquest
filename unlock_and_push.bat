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
git commit -m "Content: Phase 516. Datenreparatur tiere_match.ernaehrung: 20 vertauschte Eintraege (n=Nahrung/c=Tiername) richtiggestellt (n=Tier, c=Ernaehrungstyp), alle c auf 8 kanonische Typen normalisiert (Karnivor/Herbivor/Omnivor/Frugivor/Aasfresser/Insektivor/Nektarivor/Filtrierer), 2 Dubletten entfernt (80->78), fixedOpts entfernt. genTiereMatchQ-Fallback zieht Distraktoren jetzt NUR aus derselben Kategorie (keine fremden Tiernamen mehr als Optionen). Ergebnis: kohaerente Fragen (Koala->Herbivor), 0 unloesbar ueber 2480 Stichproben. gastro_gewuerzmischungen geprueft = stimmig (X->Herkunft).. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
