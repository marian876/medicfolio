var CACHE_NAME = 'mi-site-cache-v1';
var urlsToCache = [
  '/',
  // Añade aquí otras URLs que quieras almacenar en caché
];

self.addEventListener('install', function(event) {
  // Realizar la instalación
  // Carga la caché inicial
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('Opened cache');
        return cache.addAll(urlsToCache);
      })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // La caché tiene la respuesta, la devuelve
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
