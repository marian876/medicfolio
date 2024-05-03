// Define el nombre de tu caché
const CACHE_NAME = 'version-1';
const urlsToCache = ['index.html', 'offline.html'];

// Instala el service worker y pre-caché los recursos clave
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Opened cache');
                return cache.addAll(urlsToCache);
            })
    );
});

// Intercepta las solicitudes de red y proporciona una respuesta desde el caché o la red
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Devuelve la respuesta del caché o busca en la red si no está en caché
                return response || fetch(event.request).catch(() => caches.match('offline.html'));
            })
    );
});

// Limpia los cachés antiguos durante la activación del SW
self.addEventListener('activate', (event) => {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then((cacheNames) => Promise.all(
            cacheNames.map((cacheName) => {
                if (!cacheWhitelist.includes(cacheName)) {
                    return caches.delete(cacheName);
                }
            })
        ))
    );
});
