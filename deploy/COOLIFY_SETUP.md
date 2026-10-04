# GeoQuest über Coolify hosten — geoquest.arndt-software.de

Dein Server nutzt **Coolify** (der `coolify-proxy`/Traefik hält Port 80+443 und macht
HTTPS automatisch). Deshalb wird GeoQuest NICHT mit eigenem nginx/certbot betrieben,
sondern als App in Coolify. Coolify baut das mitgelieferte `Dockerfile`, startet den
Container und routet `geoquest.arndt-software.de` inkl. Let's-Encrypt-Zertifikat selbst.

> Die Dateien `nginx-geoquest.conf`, `deploy_selfhost.*`, `deploy_server.bat` sind damit
> für diesen Server NICHT nötig (sie waren für einen Server OHNE Coolify). Maßgeblich sind
> `Dockerfile` (Repo-Wurzel) + `deploy/nginx-container.conf`.

## Voraussetzungen (einmalig)
- DNS: `geoquest.arndt-software.de` A-Record auf 159.195.159.150, **„Nur DNS"** (erledigt).
- Code mit `Dockerfile` ist auf GitHub gepusht (`unlock_and_push.bat` einmal laufen lassen).

## Schritt A — Neue Resource in Coolify anlegen
1. Auf `https://coolify.arndt-software.de` einloggen.
2. Ein Projekt wählen (oder **+ New Project**), dann **+ New Resource**.
3. Quelle wählen:
   - Ist das GitHub-Repo **public**: **Public Repository** →
     `https://github.com/andre69190-del/geoquest` → Branch **main**.
   - Ist es **privat**: zuerst **Sources → GitHub App** verbinden, dann das Repo wählen.
4. **Build Pack: Dockerfile** auswählen (Coolify erkennt die `Dockerfile` in der Wurzel;
   falls gefragt: Dockerfile-Pfad `/Dockerfile`, Base Directory `/`).

## Schritt B — Domain & Port
1. Im Feld **Domains** eintragen: `https://geoquest.arndt-software.de`
   (mit `https://` — dann erzeugt Coolify automatisch das TLS-Zertifikat).
2. **Ports Exposes**: `80` (entspricht `EXPOSE 80` im Dockerfile).
3. Speichern.

## Schritt C — Deployen
1. **Deploy** klicken. Coolify baut das Image und startet den Container.
2. Im Deploy-Log auf „New container started" / „Healthy" warten (1–3 Min).
3. (Optional) **Automatic Deployment** aktivieren → bei jedem GitHub-Push auf `main`
   deployt Coolify automatisch neu.

## Schritt D — Supabase-Login erlauben (wichtig)
Damit Registrierung/Login auf der neuen Domain funktioniert, in Supabase die URL erlauben
(Supabase-Studio → Authentication → URL Configuration, oder GoTrue-`.env`):
```
SITE_URL = https://geoquest.arndt-software.de
ADDITIONAL_REDIRECT_URLS = https://geoquest.arndt-software.de, https://geoquest.arndt-software.de/play
```
Speichern (bei `.env`: Supabase-Auth-Service neu starten).

## Schritt E — Testen
`https://geoquest.arndt-software.de/play` im Browser öffnen (Schloss/HTTPS da?),
einloggen, ein Spiel starten. Beim ersten Mal: F12 → Application → Service Workers →
„Unregister", dann neu laden (alter Cache von der vercel-Domain).

Prüfen, ob die Startseite stimmt: `/` muss die Landing-Seite zeigen, `/play` die App,
`/impressum.html` und `/datenschutz.html` müssen erreichbar sein.

## Laufender Betrieb (neuer Deploy)
1. Lokal: `python3 gen.py`, `python3 verify.py` (grün), dann `unlock_and_push.bat` (GitHub).
2. In Coolify **Redeploy** klicken — oder, wenn „Automatic Deployment" an ist, passiert
   das automatisch.

## Schritt F — (Optional, später) alte Vercel-URL umleiten
Wenn alles läuft: `deploy/vercel-redirect.json` → `vercel.json` kopieren, `unlock_and_push.bat`.
Dann leitet `geoquest-web.vercel.app` dauerhaft (301) auf die neue Domain um.

## Aufräumen (optional)
Die vorhin angelegten Ordner werden nicht gebraucht:
```
sudo rmdir /var/www/geoquest /var/www/certbot 2>/dev/null
```
