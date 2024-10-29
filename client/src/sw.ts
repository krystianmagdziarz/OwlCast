const CACHE_NAME = 'statcollector-cache-v1';

self.addEventListener('install', (event: ExtendableEvent) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(['/']);
    })
  );
});

self.addEventListener('fetch', (event: FetchEvent) => {
  if (event.request.method === 'POST' && event.request.url.includes('/statistics')) {
    if (!navigator.onLine) {
      event.respondWith(
        new Response(JSON.stringify({ status: 'queued' }), {
          headers: { 'Content-Type': 'application/json' },
        })
      );
    }
  }
});

self.addEventListener('sync', (event: SyncEvent) => {
  if (event.tag === 'sync-statistics') {
    event.waitUntil(syncStatistics());
  }
});

async function syncStatistics(): Promise<void> {
  const offlineData = JSON.parse(localStorage.getItem('sc_offline_data') || '[]');
  if (offlineData.length === 0) return;

  try {
    await Promise.all(
      offlineData.map((data) =>
        fetch('/api/v1/statistics', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(data),
        })
      )
    );
    localStorage.removeItem('sc_offline_data');
  } catch (error) {
    console.error('Failed to sync statistics:', error);
  }
}
