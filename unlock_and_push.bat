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
git commit -m "Content: Phase 510. ABSTURZ-FIX: 4 Generatoren (genInselnMatchExt/genGipfelMatchExt/genKlimaMatchExt/genOzeaneMatchExt) lieferten type:'match' mit Feldern subject/choices/answer - aber der Spiel-Renderer hat keinen 'match'-Zweig und macht q.opts.map(...) -> 'Cannot read properties of undefined (reading map)' = App-Absturz beim Spielen (Klima-Zone, Inseln-Ozean, Gipfel-Gebirge, Ozean-Typ). Auf uk_match-Schema umgestellt (subj=Item, opts=4 Attributwerte, ans=korrekt). Frage wird jetzt korrekt dargestellt statt grosses '1/10'. verify 193/193, 0 THROW.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
