# GeoQuest Self-Hosting — geoquest.arndt-software.de

Ziel: Die App laeuft komplett auf deinem eigenen Server (dieselbe Maschine wie
`supabase.arndt-software.de`, IP **159.195.159.150**) unter
**https://geoquest.arndt-software.de** — kein Vercel mehr.

Was ich schon erledigt habe (im Code/Repo):
- Alle App-URLs von `geoquest-web.vercel.app` auf `geoquest.arndt-software.de`
  umgestellt (Share-Links, sitemap.xml, robots.txt, landing/impressum/datenschutz).
- nginx-Konfiguration, Deploy-Skripte und diese Anleitung erstellt.

Was DU am Server/DNS machen musst (dort habe ich keinen Zugriff): die Schritte 1–6.

---

## 1) DNS-Eintrag setzen
Beim DNS-Verwalter von `arndt-software.de` (dort, wo auch `supabase.` liegt):

```
Typ:  A
Name: geoquest            (ergibt geoquest.arndt-software.de)
Wert: 159.195.159.150
TTL:  3600
```
(Falls der Server IPv6 hat, zusaetzlich ein AAAA-Record.)

Pruefen (nach ein paar Minuten):
```
dig +short geoquest.arndt-software.de     # muss 159.195.159.150 liefern
```

## 2) Verzeichnisse auf dem Server
```
sudo mkdir -p /var/www/geoquest
sudo mkdir -p /var/www/certbot          # fuer Let's-Encrypt-Challenge
sudo chown -R $USER:www-data /var/www/geoquest
```

## 3) nginx-Konfiguration einspielen
`deploy/nginx-geoquest.conf` auf den Server kopieren:
```
sudo cp nginx-geoquest.conf /etc/nginx/sites-available/geoquest.arndt-software.de.conf
sudo ln -s /etc/nginx/sites-available/geoquest.arndt-software.de.conf \
           /etc/nginx/sites-enabled/
```
**Erststart-Reihenfolge (Henne/Ei mit dem Zertifikat):** Der HTTPS-`server`-Block
verweist auf ein Let's-Encrypt-Zertifikat, das es noch nicht gibt. Daher jetzt
zuerst nur den HTTP-Teil aktiv lassen — den kompletten `server { listen 443 ... }`
-Block in der Datei voruebergehend auskommentieren, dann:
```
sudo nginx -t && sudo systemctl reload nginx
```

## 4) TLS-Zertifikat holen (Let's Encrypt)
Variante A — webroot (passt zur mitgelieferten Config):
```
sudo certbot certonly --webroot -w /var/www/certbot -d geoquest.arndt-software.de
```
Variante B — falls das nginx-Plugin installiert ist, macht certbot alles selbst
(dann Schritt 3-Auskommentieren nicht noetig):
```
sudo certbot --nginx -d geoquest.arndt-software.de
```
Danach den HTTPS-`server`-Block wieder einkommentieren (nur bei Variante A) und:
```
sudo nginx -t && sudo systemctl reload nginx
```
Auto-Erneuerung ist bei certbot standardmaessig aktiv (`systemctl status certbot.timer`).

## 5) App-Dateien hochladen
Auf deinem Windows-PC im Projektordner **zuerst bauen und testen**, dann deployen:
```
python3 gen.py
python3 verify.py                 # muss 196/196 (o. mehr) zeigen
```
Deploy (Variablen im Skript-Kopf anpassen: SSH_USER, ggf. SSH_HOST/REMOTE_DIR):
- Windows:  `powershell -ExecutionPolicy Bypass -File .\deploy\deploy_selfhost.ps1`
- Linux/Git-Bash/WSL:  `SSH_USER=deinuser ./deploy/deploy_selfhost.sh`

Das Skript kopiert index.html, landing.html, sw.js, manifest.json, icon.svg,
die zur Laufzeit geladenen *.json (u.a. license_plates.json, world-110m.json)
und cities_data.js nach `/var/www/geoquest/`.

## 6) Supabase-Login auf die neue Domain erlauben  (WICHTIG)
Damit Registrierung/Login + E-Mail-Bestaetigung auf der neuen Domain funktionieren,
in deiner **self-hosted Supabase**-Konfiguration die neue URL erlauben
(GoTrue/`.env` bzw. Studio → Authentication → URL Configuration):
```
SITE_URL = https://geoquest.arndt-software.de
ADDITIONAL_REDIRECT_URLS = https://geoquest.arndt-software.de, https://geoquest.arndt-software.de/play
```
(Die alte vercel.app-URL kannst du entfernen, sobald alles laeuft.)
Falls deine Supabase/Kong-Instanz CORS pro Origin beschraenkt: `https://geoquest.arndt-software.de` als erlaubten Origin ergaenzen.

---

## 7) Testen
```
curl -I https://geoquest.arndt-software.de/          # 200, landing
curl -I https://geoquest.arndt-software.de/play      # 200, Cache-Control: no-cache
```
Im Browser `https://geoquest.arndt-software.de/play` oeffnen, einloggen, ein Spiel
starten. Beim allerersten Aufruf einmal DevTools → Application → Service Workers →
"Unregister" (alter Cache von der vercel-Domain kann sonst stoeren).

## Laufender Betrieb / neuer Deploy
Nach jeder Aenderung Quellcode wie gewohnt via `unlock_and_push.bat` auf GitHub
sichern (dient jetzt nur noch der Versionierung, nicht mehr dem Hosting).
Zum Veroeffentlichen auf den Server gibt es zwei Wege:
- **One-Shot (empfohlen):** `deploy_server.bat` im Projektordner doppelklicken —
  macht Build + verify (Gate) + Upload in einem Rutsch.
- Oder manuell: `python3 gen.py`, `python3 verify.py`, dann das Skript aus Schritt 5.

## 8) (Optional, SPAETER) Alte Vercel-URL dauerhaft umleiten
Sobald `https://geoquest.arndt-software.de` live und getestet ist, kannst du die
alte `geoquest-web.vercel.app` per **301** auf die neue Domain umleiten (fuer alte
Lesezeichen/Links und SEO):
1. `deploy/vercel-redirect.json` nach `vercel.json` kopieren (die bisherige ersetzen).
2. `unlock_and_push.bat` ausfuehren → Vercel deployt dann nur noch den Redirect.
Danach zeigt jeder Aufruf von geoquest-web.vercel.app/... dauerhaft auf
geoquest.arndt-software.de/... (Pfad bleibt erhalten).
WICHTIG: erst NACH dem erfolgreichen Self-Host-Livegang anwenden — sonst leitet die
alte Seite ins Leere.

## Rollback
Die alte Vercel-Seite (`geoquest-web.vercel.app`) bleibt bestehen und funktioniert
weiter, bis du sie abschaltest — falls beim Self-Hosting etwas klemmt, ist sie ein
sofortiges Fallback.

## Hinweis zu vercel.json
`vercel.json` wird beim Self-Hosting nicht mehr benoetigt (nginx uebernimmt Routing
und Header). Die Datei bleibt im Repo, schadet aber nicht.
