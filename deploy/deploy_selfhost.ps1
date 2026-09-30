# ============================================================================
#  GeoQuest — Deploy auf eigenen Server (Windows / PowerShell, via scp)
#  Voraussetzung: OpenSSH-Client (in Win10/11 enthalten) + SSH-Key auf dem
#  Server hinterlegt (kein Passwort im Skript!).
#
#  Vor dem Deploy IMMER:  python3 gen.py ; python3 verify.py  (muss gruen sein)
#  Aufruf:  .\deploy\deploy_selfhost.ps1   (ggf. Variablen unten anpassen)
# ============================================================================

# --- Konfiguration: BITTE anpassen -----------------------------------------
$SSH_USER   = "CHANGE_ME"                 # dein SSH-Benutzer auf dem Server
$SSH_HOST   = "arndt-software.de"         # oder die IP 159.195.159.150
$SSH_PORT   = 22
$REMOTE_DIR = "/var/www/geoquest"
# ---------------------------------------------------------------------------

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot   # Repo-Wurzel (eine Ebene ueber deploy\)

$files = @(
  "index.html","landing.html","impressum.html","datenschutz.html",
  "google1b9fe4381920a332.html","sw.js","cities_data.js","manifest.json",
  "icon.svg","robots.txt","sitemap.xml",
  "area.json","capitals_population.json","cities.json","cities_clean.json",
  "currencies.json","food.json","landmarks.json","license_plates.json",
  "license_plates_salvaged.json","neighbors.json","parks.json","rivers.json",
  "unesco.json","wappen.json","world-110m.json"
)

# Existenz pruefen
$paths = @()
foreach ($f in $files) {
  $p = Join-Path $root $f
  if (-not (Test-Path $p)) { throw "Datei fehlt: $p (erst 'python3 gen.py' laufen lassen?)" }
  $paths += $p
}

Write-Host "Deploy -> ${SSH_USER}@${SSH_HOST}:${REMOTE_DIR}  ($($paths.Count) Dateien)"
ssh -p $SSH_PORT "$SSH_USER@$SSH_HOST" "mkdir -p $REMOTE_DIR"
scp -P $SSH_PORT $paths "${SSH_USER}@${SSH_HOST}:${REMOTE_DIR}/"
Write-Host "Fertig. Test: https://geoquest.arndt-software.de/play"
Write-Host "Hinweis: Nach dem ersten Deploy im Browser einmal Service-Worker unregistern (Cache)."
