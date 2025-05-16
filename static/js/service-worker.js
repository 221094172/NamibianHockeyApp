/**
 * Service Worker for Namibia Hockey Union App
 * Provides offline caching capabilities
 */

// Cache names
const STATIC_CACHE_NAME = 'nhu-static-v1';
const DYNAMIC_CACHE_NAME = 'nhu-dynamic-v1';

// Resources to cache on install
const STATIC_ASSETS = [
    '/',
    '/static/css/custom.css',
    '/static/css/loading-animations.css',
    '/static/js/script.js',
    '/static/js/loading-animations.js',
    '/static/js/offline-manager.js',
    'https://cdn.replit.com/agent/bootstrap-agent-dark-theme.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css',
    '/static/images/offline-banner.png',
    '/static/images/offline-logo.png',
    '/dashboard',
    '/login',
    '/register'
];

// Install event - cache static assets
self.addEventListener('install', event => {
    console.log('Service Worker: Installing');
    
    event.waitUntil(
        caches.open(STATIC_CACHE_NAME)
            .then(cache => {
                console.log('Service Worker: Caching static assets');
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => {
                console.log('Service Worker: Static assets cached');
                return self.skipWaiting();
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
    console.log('Service Worker: Activating');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => {
                        if (
                            cacheName !== STATIC_CACHE_NAME && 
                            cacheName !== DYNAMIC_CACHE_NAME
                        ) {
                            console.log('Service Worker: Deleting old cache', cacheName);
                            return caches.delete(cacheName);
                        }
                    })
                );
            })
            .then(() => {
                console.log('Service Worker: Activated');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache or network
self.addEventListener('fetch', event => {
    // Skip for non-GET requests or cross-origin requests (like API calls)
    if (event.request.method !== 'GET' || !event.request.url.startsWith(self.location.origin)) {
        return;
    }
    
    // Skip service worker requests
    if (event.request.url.includes('/static/js/service-worker.js')) {
        return;
    }
    
    // Handle HTML page requests with network-first strategy
    if (event.request.headers.get('accept').includes('text/html')) {
        event.respondWith(
            fetch(event.request)
                .then(response => {
                    // Clone the response to store in cache
                    const responseClone = response.clone();
                    
                    caches.open(DYNAMIC_CACHE_NAME)
                        .then(cache => {
                            cache.put(event.request, responseClone);
                        });
                    
                    return response;
                })
                .catch(() => {
                    // If network fails, try to serve from cache
                    return caches.match(event.request)
                        .then(cacheResponse => {
                            if (cacheResponse) {
                                return cacheResponse;
                            }
                            
                            // If not in cache, serve offline page
                            return caches.match('/offline');
                        });
                })
        );
        return;
    }
    
    // For all other requests (CSS, JS, images), use cache-first strategy
    event.respondWith(
        caches.match(event.request)
            .then(cacheResponse => {
                // If found in cache, return it
                if (cacheResponse) {
                    return cacheResponse;
                }
                
                // Otherwise make a network request
                return fetch(event.request)
                    .then(response => {
                        // Clone the response to store in cache
                        const responseClone = response.clone();
                        
                        caches.open(DYNAMIC_CACHE_NAME)
                            .then(cache => {
                                cache.put(event.request, responseClone);
                            });
                        
                        return response;
                    })
                    .catch(error => {
                        // For image requests, return a placeholder
                        if (event.request.url.match(/\.(jpg|jpeg|png|gif|svg)$/)) {
                            return caches.match('/static/images/offline-placeholder.png');
                        }
                        
                        console.error('Service Worker: Fetch error', error);
                        return new Response('Network error occurred', {
                            status: 503,
                            statusText: 'Service Unavailable'
                        });
                    });
            })
    );
});

// Handle messages from clients
self.addEventListener('message', event => {
    if (event.data.action === 'skipWaiting') {
        self.skipWaiting();
    }
});