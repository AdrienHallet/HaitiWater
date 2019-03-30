const cacheVersion = 'v1';

self.addEventListener('install', function (event) {
    // Cache the offline page by default
    event.waitUntil(
        caches.open(cacheVersion).then(function (cache) {
            return cache.add('/offline/');
        })
    );
});

self.addEventListener('fetch', function (event) {
    if (event.request.url.startsWith("/static/")) {
        // For static elements, try to match in the cache, else fetch and cache
        event.respondWith(
            caches.match(event.request).then(function (cacheResponse) {
                return cacheResponse || fetch(event.request).then(function (networkResponse) {
                    const clonedResponse = networkResponse.clone();
                    caches.open(cacheVersion).then(function (cache) {
                        cache.put(event.request, clonedResponse).catch(function (error) {
                            console.log(error)
                        });
                    });
                    return networkResponse;
                });
            })
        );
    } else {
        // For non-static elements, the only cached element should be the offline page
        // Try to fetch or redirect to offline page
        event.respondWith(
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
