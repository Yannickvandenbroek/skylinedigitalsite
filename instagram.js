/* Instagram-blok: haalt de laatste posts op via /api/instagram (Behold) zodra het blok bijna in beeld is.
   Lukt dat niet, dan blijft het blok verborgen. */
(function () {
  var secs = document.querySelectorAll("[data-instagram]");
  if (!secs.length || !window.fetch) return;
  var lang = (document.documentElement.lang || "nl").slice(0, 2);
  var VIEW = { nl: "Bekijk op Instagram", en: "View on Instagram", it: "Vedi su Instagram", es: "Ver en Instagram" }[lang] || "Bekijk op Instagram";
  var ICON = {
    VIDEO: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5.5v13l11-6.5z"/></svg>',
    CAROUSEL_ALBUM: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 3h11a3 3 0 0 1 3 3v11h-2V6a1 1 0 0 0-1-1H7z"/><rect x="3" y="7" width="14" height="14" rx="3" fill="currentColor"/></svg>'
  };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }
  function render(sec, d) {
    var max = parseInt(sec.getAttribute("data-count") || "6", 10);
    var posts = (d.posts || []).slice(0, max);
    if (!posts.length) return;
    var grid = sec.querySelector("[data-ig-grid]");
    grid.style.setProperty("--n", Math.min(posts.length, max));
    grid.innerHTML = posts.map(function (p) {
      var cap = p.caption.split("\n")[0];
      return '<a class="ig-tile" href="' + esc(p.url) + '" target="_blank" rel="noopener">' +
        '<img src="' + esc(p.image) + '" alt="' + esc(p.alt || cap) + '" loading="lazy" width="700" height="700" />' +
        (ICON[p.type] ? '<span class="ig-badge">' + ICON[p.type] + "</span>" : "") +
        '<span class="ig-over"><span class="ig-cap">' + esc(cap) + '</span><span class="ig-view">' + VIEW + " →</span></span></a>";
    }).join("");
    var f = sec.querySelector("[data-ig-followers]");
    if (f && d.followers) f.textContent = Number(d.followers).toLocaleString(lang === "en" ? "en-GB" : lang + "-" + lang.toUpperCase());
    var av = sec.querySelector("[data-ig-avatar]");
    if (av && d.avatar) { av.src = d.avatar; av.hidden = false; }
    sec.hidden = false;
  }
  var done = false;
  function load() {
    if (done) return; done = true;
    fetch("/api/instagram", { headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d) secs.forEach(function (s) { render(s, d); }); })
      .catch(function () {});
  }
  // het blok is verborgen tot de data er is, dus observeren we de sectie ervoor
  var anchors = []; secs.forEach(function (s) { anchors.push(s.previousElementSibling || s.parentNode); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); load(); } }, { rootMargin: "600px" });
    anchors.forEach(function (a) { io.observe(a); });
  } else { load(); }
})();
