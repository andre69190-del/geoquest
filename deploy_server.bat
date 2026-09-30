@echo off
REM ===========================================================================
REM  GeoQuest — One-Shot Self-Host-Deploy (Build + Verify + Upload)
REM  Baut die App, prueft sie (Gate) und laedt sie auf den eigenen Server.
REM  Voraussetzung: SSH_USER in deploy\deploy_selfhost.ps1 einmalig eintragen.
REM ===========================================================================
cd /d "%~dp0"

echo [1/3] Build...
python3 gen.py
if errorlevel 1 ( echo. & echo ABBRUCH: gen.py fehlgeschlagen. & pause & exit /b 1 )

echo.
echo [2/3] Verify (Gate)...
python3 verify.py
if errorlevel 1 ( echo. & echo ABBRUCH: verify.py FAILED - erst Fehler beheben! & pause & exit /b 1 )

echo.
echo [3/3] Upload auf geoquest.arndt-software.de...
powershell -ExecutionPolicy Bypass -File "%~dp0deploy\deploy_selfhost.ps1"
if errorlevel 1 ( echo. & echo ABBRUCH: Upload fehlgeschlagen. & pause & exit /b 1 )

echo.
echo Fertig. Test: https://geoquest.arndt-software.de/play
pause
