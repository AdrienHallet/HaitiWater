const cacheVersion = 'v1.1';

self.addEventListener('install', function (event) {
    event.waitUntil(
        caches.open(cacheVersion).then(function (cache) {
            return cache.add('/offline/');
        })
    );
});

self.addEventListener('fetch', function (event) {
    if (event.request.url.includes("/static/")) {
        event.respondWith(
            caches.match(event.request).then(function (cacheResponse) {
                return cacheResponse || fetch(event.request).then(function (networkResponse) {
                    const clonedResponse = networkResponse.clone();
                    caches.open(cacheVersion).then(function (cache) {
                        cache.put(event.request, clonedResponse);
                    });
                    return networkResponse;
                });
            })
        );
    } else {
        event.respondWith(
            // Only (non-static) cached page should be the offline page
            caches.match(event.request).then(function (cacheResponse) {
                return cacheResponse || fetch(event.request).then(function (response) {
                    return response;
                }).catch(function () {
                    return Response.redirect('/offline/');
                });
            })
        );
    }

});
