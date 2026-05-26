#!/usr/bin/env python3
import sys
path = "/sessions/trusting-upbeat-lovelace/mnt/Desktop/Cowork/Geoquest/gen.py"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

OLD = "    const swSrc=`const CACHE='gq-v9';\n/* Phase 99: passiver SW – kein fetch-Handler, blockt NIE Netzwerk-Requests */\nself.addEventListener('install',function(){self.skipWaiting();});\nself.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));});`;"

NEW = "    const swSrc=`const CACHE='gq-v10';\n/* Phase 221: Offline-Modus — network-first mit Cache-Fallback */\nself.addEventListener('install',function(){self.skipWaiting();});\nself.addEventListener('activate',function(e){e.waitUntil(caches.keys().then(function(ks){return Promise.all(ks.filter(function(k){return k!==CACHE;}).map(function(k){return caches.delete(k);}));}).then(function(){return self.clients.claim();}));});\nself.addEventListener('fetch',function(e){if(e.request.mode==='navigate'||e.request.destination==='document'){e.respondWith(fetch(e.request).then(function(resp){var r=resp.clone();caches.open(CACHE).then(function(c){c.put(e.request,r);});return resp;}).catch(function(){return caches.match(e.request).then(function(r){return r||new Response('<h2>GeoQuest — Offline</h2><p>Keine Verbindung. Bitte zuerst mit Internet starten.</p>',{headers:{'Content-Type':'text/html'}});});}));}});\`;`;"

if OLD not in content:
    print("ERROR: OLD pattern not found!")
    # Show nearby context
    idx = content.find("swSrc=")
    print(repr(content[idx:idx+300]))
    sys.exit(1)

content = content.replace(OLD, NEW, 1)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("OK: Service Worker upgraded to gq-v10 with offline fetch handler")
