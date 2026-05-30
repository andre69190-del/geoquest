const CACHE_NAME = 'geoquest-6c62b252';
/* Phase 238: full offline cache — auto-versioned from asset hash */
const ASSETS = [
  './GeoQuest.html',
  './index.html',
  './manifest.json',
  './icon.svg',
  './data/archaeologie_hl.json',
  './data/archaeologie_match.json',
  './data/archaeologie_pin.json',
  './data/archaeologie_ws.json',
  './data/astro_hl.json',
  './data/astro_match.json',
  './data/astro_pin.json',
  './data/astro_ws.json',
  './data/emob_hl.json',
  './data/emob_match.json',
  './data/emob_pin.json',
  './data/emob_ws.json',
  './data/gastro_hl.json',
  './data/gastro_match.json',
  './data/gastro_pin.json',
  './data/gastro_ws.json',
  './data/geo_hl.json',
  './data/geo_match.json',
  './data/geo_pin.json',
  './data/geo_ws.json',
  './data/kultur.json',
  './data/metro_logos.json',
  './data/pflanzen_hl.json',
  './data/pflanzen_match.json',
  './data/pflanzen_pin.json',
  './data/pflanzen_ws.json',
  './data/sport_hl.json',
  './data/sport_match.json',
  './data/sport_pin.json',
  './data/sport_ws.json',
  './data/tech_hl.json',
  './data/tech_match.json',
  './data/tech_pin.json',
  './data/tech_ws.json',
  './data/tiere_hl.json',
  './data/tiere_match.json',
  './data/tiere_pin.json',
  './data/tiere_ws.json',
  './data/timeline.json'
];

self.addEventListener('install', function(e) {
  e.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return Promise.allSettled(
        ASSETS.map(function(url) {
          return cache.add(url).catch(function(err) {
            console.warn('SW: skipped', url, err);
          });
        })
      );
    }).then(function() { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function(e) {
  e.waitUntil(
    caches.keys().then(function(keys) {
      return Promise.all(
        keys.filter(function(k) { return k !== CACHE_NAME; })
            .map(function(k) { return caches.delete(k); })
      );
    }).then(function() { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function(e) {
  if (e.request.url.includes('supabase.co')) {
    e.respondWith(fetch(e.request).catch(function() {
      return new Response('', {status: 503});
    }));
    return;
  }
  e.respondWith(
    caches.match(e.request).then(function(cached) {
      if (cached) return cached;
      return fetch(e.request).then(function(response) {
        if (!response || response.status !== 200) return response;
        var clone = response.clone();
        caches.open(CACHE_NAME).then(function(cache) {
          cache.put(e.request, clone);
        });
        return response;
      }).catch(function() {
        return caches.match('./GeoQuest.html');
      });
    })
  );
});
