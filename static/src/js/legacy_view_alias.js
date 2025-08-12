/**
 * Normalize legacy view_type=tree to list in the webclient URL hash.
 * Works on first load and on any subsequent hash changes.
 * This avoids the client asking the server for a non-existent 'tree' view type in Odoo 18.
 */
(function () {
  const KEY = 'view_type';
  const LEGACY = 'tree';
  const MODERN = 'list';
  let busy = false;

  function normalizeHash() {
    if (busy) return false;
    const h = window.location.hash || '';
    if (!h) return false;
    // Simple check first to keep it cheap
    if (!h.includes(KEY + '=' + LEGACY)) return false;
    try {
      // Replace "view_type=tree" with "view_type=list" (only within the hash)
      const newHash = h.replace(new RegExp('(^|[&#])' + KEY + '=tree(?![\\/%\w-])', 'g'), (m, p1) => `${p1}${KEY}=${MODERN}`);
      if (newHash !== h) {
        busy = true;
        window.location.hash = newHash;
        // Allow the browser to complete navigation before unlocking
        setTimeout(() => (busy = false), 50);
        return true;
      }
    } catch (e) {
      // Non-fatal
      busy = false;
    }
    return false;
  }

  // Run as early as possible
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', normalizeHash, { once: true });
  } else {
    normalizeHash();
  }

  // Also fix on subsequent navigation inside the SPA
  window.addEventListener('hashchange', () => {
    normalizeHash();
  }, false);
})();

