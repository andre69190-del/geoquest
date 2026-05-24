@echo off
cd /d "%~dp0"
echo Removing stale git locks...
if exist ".git\index.lock" del /f /q ".git\index.lock"
if exist ".git\HEAD.lock" del /f /q ".git\HEAD.lock"
if exist ".git\refs\heads\main.lock" del /f /q ".git\refs\heads\main.lock"
echo.
git add -A
git commit -m "FEAT/UI: Phase 209 — H/L river static fallback via RIVERS_GEO_DATA, new Airport-Pin mode (40 airports, D3 coordinate click, haversine scoring), WORTSCHMIEDE expanded to 13 cities (London, Barcelona, Tokio, NewYork, BuenosAires, Sydney, Istanbul, Mumbai, Vienna, Dubai — all words letter-validated), map mobile fix + pin drop-shadow visibility."
git push origin main
pause
