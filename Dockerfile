# GeoQuest — statische App im Container (fuer Coolify / Docker)
# Coolify-Proxy (Traefik) routet geoquest.arndt-software.de -> diesen Container:80
# und macht HTTPS. Der Container liefert nur die statischen Dateien aus.
FROM nginx:alpine

# Eigene Routing-/Header-Config statt der Standard-default.conf
RUN rm -f /etc/nginx/conf.d/default.conf
COPY deploy/nginx-container.conf /etc/nginx/conf.d/geoquest.conf

# Nur die zur Laufzeit benoetigten Web-Dateien ins Image
WORKDIR /usr/share/nginx/html
COPY index.html landing.html impressum.html datenschutz.html google1b9fe4381920a332.html ./
COPY sw.js cities_data.js manifest.json icon.svg robots.txt sitemap.xml ./
COPY area.json capitals_population.json cities.json cities_clean.json currencies.json \
     food.json landmarks.json license_plates.json license_plates_salvaged.json \
     neighbors.json parks.json rivers.json unesco.json wappen.json world-110m.json ./

EXPOSE 80
