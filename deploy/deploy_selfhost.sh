#!/usr/bin/env bash
# ============================================================================
#  GeoQuest — Deploy auf eigenen Server (Linux / macOS / Git-Bash / WSL, rsync)
#  Voraussetzung: rsync + ssh + SSH-Key auf dem Server (kein Passwort im Skript).
#
#  Vor dem Deploy IMMER:  python3 gen.py && python3 verify.py  (muss gruen sein)
#  Aufruf:  SSH_USER=deinuser ./deploy/deploy_selfhost.sh
#           (oder die Variablen unten fest eintragen)
# ============================================================================
set -euo pipefail

# --- Konfiguration: BITTE anpassen bzw. per Env uebergeben ------------------
SSH_USER="${SSH_USER:-CHANGE_ME}"           # dein SSH-Benutzer auf dem Server
SSH_HOST="${SSH_HOST:-arndt-software.de}"    # oder 159.195.159.150
SSH_PORT="${SSH_PORT:-22}"
REMOTE_DIR="${REMOTE_DIR:-/var/www/geoquest}"
# ---------------------------------------------------------------------------

cd "$(dirname "$0")/.."   # Repo-Wurzel

FILES=(
  index.html landing.html impressum.html datenschutz.html
  google1b9fe4381920a332.html sw.js cities_data.js manifest.json
  icon.svg robots.txt sitemap.xml
  area.json capitals_population.json cities.json cities_clean.json
  currencies.json food.json landmarks.json license_plates.json
  license_plates_salvaged.json neighbors.json parks.json rivers.json
  unesco.json wappen.json world-110m.json
)

for f in "${FILES[@]}"; do
  [ -f "$f" ] || { echo "FEHLT: $f (erst 'python3 gen.py' laufen lassen?)"; exit 1; }
done

echo "Deploy -> ${SSH_USER}@${SSH_HOST}:${REMOTE_DIR} (${#FILES[@]} Dateien)"
ssh -p "$SSH_PORT" "${SSH_USER}@${SSH_HOST}" "mkdir -p '${REMOTE_DIR}'"
rsync -avz --checksum -e "ssh -p ${SSH_PORT}" "${FILES[@]}" "${SSH_USER}@${SSH_HOST}:${REMOTE_DIR}/"
echo "Fertig. Test: https://geoquest.arndt-software.de/play"
echo "Hinweis: nach dem ersten Deploy im Browser einmal den Service-Worker unregistern."
