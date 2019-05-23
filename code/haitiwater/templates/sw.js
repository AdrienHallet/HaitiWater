const cacheVersion = 'v4';

self.addEventListener('install', function (event) {
    // Cache the offline page by default
    event.waitUntil(
        caches.open(cacheVersion).then(function (cache) {
            return cache.addAll([
                '/offline/',
                '/static/report.js',
                '/static/monthlyReportFormHandler.js',
                '/static/monthlyReportEditFormHandler.js',
                '/static/vendor/bootstrap-wizard/jquery.bootstrap.wizard.js',
                '/static/vendor/bootstrap-multiselect/bootstrap-multiselect.js'
            ]).catch(function (error) {
                console.error(error)
            });
        }).catch(function (error) {
            console.error(error)
        })
    );
});

self.addEventListener('fetch', function (event) {
    if (event.request.url.includes("/static/")) {
        // For static elements, try to match in the cache, else fetch and cache
        event.respondWith(
            caches.match(event.request).then(function (cacheResponse) {
                return cacheResponse || fetch(event.request).then(function (networkResponse) {
                    const clonedResponse = networkResponse.clone();
                    caches.open(cacheVersion).then(function (cache) {
                        cache.put(event.request, clonedResponse).catch(function (error) {
                            console.error(error)
                        });
                    });
                    return networkResponse;
                }).catch(function (error) {
                    console.error(error)
                });
            })
        );
    } else {
        // For non-static elements, the only cached element should be the offline page
        // Try to fetch or redirect to offline page
        event.respondWith(
            caches.match(event.request).then(function (cacheResponse) {
                return cacheResponse || fetch(event.request).catch(function () {
                    return Response.redirect('/offline/');
                });
            })
        );
    }

});
