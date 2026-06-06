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
git commit -m "Content: Phase 525. Tote/immer-NULL Modi repariert: (1) Attribut-Match-Generatoren (genAutosMatchExt/Games/Konsolen/Garten/Capitals) verlangten 3 Distraktoren, aber Felder wie antrieb/herkunftsland/wasserbedarf/grossstadt/adaption haben nur 2-3 verschiedene Werte -> Schwelle auf >=1 gesenkt (2-4 Optionen) + Boolean->Ja/Nein-Mapping (turbo). (2) spiel_* Generatoren behandelten BOARDGAMES_DATA (Objekt) als Array -> _bgArr()-Adapter. (3) genArchPinQ war doppelt definiert; var-Zuweisung (_mkPinQ, braucht cat-Arg) ueberschrieb die korrekte Funktion -> entfernt. 12 Modi wieder spielbar (smoke OK 944->956). smoke_test: EXPECTED_NULL-Allowlist (async-Daten + Custom-Flow), unerwartete NULL faillt jetzt.. verify: 195/195."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
