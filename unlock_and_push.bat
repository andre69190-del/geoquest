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
git commit -m "Content: Phase 487. Lernspiel 2/5: Kontinente-Finder (kontinent_finder, Kategorie pure_geo). genKontinentFinderQ: Flaggen-Emoji + lokalisierter Laendername -> auf welchem Kontinent? (uk_match, 4 Kontinent-Optionen). Waechst mit Alter: Stufe 1 nur sehr bekannte Laender (kuratierte cc-Liste), ab Stufe 2 alle ~181. Laenderuebergreifend. COUNTRIES-Schema {c,cc,ct,sr} genutzt (ct=Kontinent). i18n mt_kontinent/kontinent_prompt/cont_* de/en/pl. Lehrplan KS1 '7 Kontinente'. Rauchtest fand+fixte Schema-Bug (continent->ct). verify 193/193, 0 THROW, 1001 Modi.. verify: 193/193."
git push origin main
echo.
echo Done! Vercel will deploy in ~60 seconds
