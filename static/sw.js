/**
 * sw.js — Swahilipot Hub Portal Service Worker v3
 * • Network-first fetch with cache fallback
 * • Pre-caches key pages + assets on install
 * • Serves /offline/ when network fails for HTML navigation
 * • Handles Web Push notifications
 */

const CACHE = "sph-v3";
const STATIC_CACHE = "sph-static-v3";

// Pages to pre-cache on install
const PRECACHE_PAGES = [
  "/",
  "/attendance/mobile/",
  "/offline/",
];

// Static assets to pre-cache (CSS, key icons)
const PRECACHE_STATIC = [
  "/static/css/portal.css",
  "/static/manifest.json",
  "/static/icons/icon-192x192.png",
  "/static/icons/icon-512x512.png",
];

// ── Install: pre-cache key pages and assets ───────────────────────────────
self.addEventListener("install", (e) => {
  e.waitUntil(
    Promise.all([
      caches.open(CACHE).then((c) =>
        Promise.allSettled(PRECACHE_PAGES.map((url) => c.add(url)))
      ),
      caches.open(STATIC_CACHE).then((c) =>
        Promise.allSettled(PRECACHE_STATIC.map((url) => c.add(url)))
      ),
    ]).then(() => self.skipWaiting())
  );
});

// ── Activate: delete old caches ───────────────────────────────────────────
self.addEventListener("activate", (e) => {
  const KEEP = [CACHE, STATIC_CACHE];
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => !KEEP.includes(k)).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// ── Fetch: network-first, fallback to cache, then offline page ────────────
self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;

  const url = new URL(e.request.url);

  // Only handle same-origin requests
  if (url.origin !== self.location.origin) return;

  // Skip admin, Django internals, and push endpoints
  if (url.pathname.startsWith("/admin/") ||
      url.pathname.startsWith("/communication/push/")) return;

  // Static assets: cache-first
  if (url.pathname.startsWith("/static/")) {
    e.respondWith(
      caches.match(e.request).then((cached) => {
        if (cached) return cached;
        return fetch(e.request).then((r) => {
          if (r.ok) {
            const clone = r.clone();
            caches.open(STATIC_CACHE).then((c) => c.put(e.request, clone));
          }
          return r;
        }).catch(() => caches.match(e.request));
      })
    );
    return;
  }

  // HTML navigation: network-first, serve /offline/ when down
  const isNavigation = e.request.mode === "navigate" ||
    e.request.headers.get("Accept")?.includes("text/html");

  if (isNavigation) {
    e.respondWith(
      fetch(e.request)
        .then((r) => {
          if (r.ok) {
            const clone = r.clone();
            caches.open(CACHE).then((c) => c.put(e.request, clone));
          }
          return r;
        })
        .catch(() =>
          caches.match(e.request)
            .then((cached) => cached || caches.match("/offline/"))
        )
    );
    return;
  }

  // Everything else: network-first with cache fallback
  e.respondWith(
    fetch(e.request)
      .then((r) => {
        if (r.ok) {
          const clone = r.clone();
          caches.open(CACHE).then((c) => c.put(e.request, clone));
        }
        return r;
      })
      .catch(() => caches.match(e.request).then((r) => r || Response.error()))
  );
});

// ── Push event: show notification ─────────────────────────────────────────
self.addEventListener("push", (e) => {
  let data = { title: "Swahilipot Hub Portal", body: "You have a new notification.", link: "/" };
  if (e.data) {
    try { data = { ...data, ...e.data.json() }; } catch (_) {}
  }

  const opts = {
    body: data.body,
    icon: "/static/icons/icon-192x192.png",
    badge: "/static/icons/icon-96x96.png",
    tag: data.tag || "sph-notification",
    renotify: true,
    requireInteraction: data.priority === "critical" || data.priority === "high",
    vibrate: data.priority === "critical" ? [300, 100, 300, 100, 300] :
             data.priority === "high"     ? [200, 100, 200] : [100],
    data: { link: data.link || "/" },
    actions: [
      { action: "open", title: "Open Portal" },
      { action: "dismiss", title: "Dismiss" },
    ],
  };

  e.waitUntil(self.registration.showNotification(data.title, opts));
});

// ── Notification click: open the link ────────────────────────────────────
self.addEventListener("notificationclick", (e) => {
  e.notification.close();
  if (e.action === "dismiss") return;

  const link = (e.notification.data && e.notification.data.link) || "/";

  e.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then((wins) => {
      for (const win of wins) {
        if (win.url.includes(self.location.origin) && "focus" in win) {
          win.navigate(link);
          return win.focus();
        }
      }
      return clients.openWindow(link);
    })
  );
});
