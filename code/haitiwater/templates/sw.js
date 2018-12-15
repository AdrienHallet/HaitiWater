self.addEventListener('fetch', function (event) {
    event.respondWith(fetch(event.request)
            .catch(function () {
                return new Response(
                    "<h1>Oh no!</h1><p>There is no internet connection.</p>",
                    { headers: {'Content-Type': 'text/html'} }
                );
            })
    );
});