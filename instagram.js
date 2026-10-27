/* Instagram-blok (donker, award-patroon zoals noow.co): staande kaarten in verspringende kolommen,
   Reels spelen bij hover, kolommen bewegen licht tegen elkaar in bij scrollen.
   Data via /api/instagram (Behold). Lukt het ophalen niet, dan blijft het blok verborgen. */
(function () {
  var secs = document.querySelectorAll("[data-instagram]");
  if (!secs.length || !window.fetch) return;
  var lang = (document.documentElement.lang || "nl").slice(0, 2);
  var T = {
    nl: { view: "Bekijk op Instagram", reel: "Reel", album: "foto's" },
    en: { view: "View on Instagram", reel: "Reel", album: "photos" },
    it: { view: "Vedi su Instagram", reel: "Reel", album: "foto" },
    es: { view: "Ver en Instagram", reel: "Reel", album: "fotos" },
  }[lang] || { view: "Bekijk op Instagram", reel: "Reel", album: "foto's" };
  var ICON = {
    VIDEO: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M8 5.5v13l11-6.5z"/></svg>',
    CAROUSEL_ALBUM: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M7 3h11a3 3 0 0 1 3 3v11h-2V6a1 1 0 0 0-1-1H7z"/><rect x="3" y="7" width="14" height="14" rx="3" fill="currentColor"/></svg>',
    IG: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.3" cy="6.7" r="1.1" fill="currentColor"/></svg>'
  };
  var reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  function card(p, d, i) {
    var cap = (p.caption || "").split("\n")[0];
    var tag = p.type === "VIDEO" ? T.reel : p.type === "CAROUSEL_ALBUM" ? (p.slides + " " + T.album) : "";
    return '<a class="ig-card" style="order:' + i + '" href="' + esc(p.url) + '" target="_blank" rel="noopener"' + (p.video ? ' data-video="' + esc(p.video) + '"' : "") + ">" +
      '<span class="ig-media"><img src="' + esc(p.image) + '" alt="' + esc(p.alt || cap) + '" loading="lazy" referrerpolicy="no-referrer" onerror="if(this.dataset.f!==\'1\'){this.dataset.f=\'1\';this.src=\'' + esc(p.square) + '\'}" />' +
      (ICON[p.type] ? '<span class="ig-badge" title="' + esc(tag) + '">' + ICON[p.type] + "</span>" : "") + "</span>" +
      '<span class="ig-foot"><span class="ig-cap">' + esc(cap) + '</span><span class="ig-view">' + ICON.IG + T.view + "</span></span></a>";
  }

  function render(sec, d) {
    var max = parseInt(sec.getAttribute("data-count") || "6", 10);
    var posts = (d.posts || []).slice(0, max);
    if (!posts.length) return;
    var grid = sec.querySelector("[data-ig-grid]");
    var ncol = Math.min(3, posts.length);
    var cols = []; for (var i = 0; i < ncol; i++) cols.push([]);
    posts.forEach(function (p, i) { cols[i % ncol].push(card(p, d, i)); }); // order houdt de volgorde goed in de mobiele swipe-rij
    grid.style.setProperty("--cols", ncol);
    grid.innerHTML = cols.map(function (c, i) { return '<div class="ig-col" data-col="' + i + '">' + c.join("") + "</div>"; }).join("");
    var f = sec.querySelector("[data-ig-followers]");
    if (f && d.followers) f.textContent = Number(d.followers).toLocaleString(lang === "en" ? "en-GB" : lang + "-" + lang.toUpperCase());
    var av = sec.querySelector("[data-ig-avatar]");
    if (av && d.avatar) { av.src = d.avatar; av.hidden = false; }
    sec.hidden = false;
    // Reels: video afspelen bij hover (alleen apparaten met muis)
    if (!reduce && matchMedia("(hover: hover)").matches) {
      grid.querySelectorAll(".ig-card[data-video]").forEach(function (a) {
        var v;
        a.addEventListener("mouseenter", function () {
          if (!v) { v = document.createElement("video"); v.src = a.dataset.video; v.muted = true; v.loop = true; v.playsInline = true; v.className = "ig-video"; var m = a.querySelector(".ig-media"); m.insertBefore(v, m.children[1]); }
          v.play().catch(function () {});
          a.classList.add("is-playing");
        });
        a.addEventListener("mouseleave", function () { if (v) v.pause(); a.classList.remove("is-playing"); });
      });
    }
    // Kolommen bewegen licht tegen elkaar in bij scrollen
    if (!reduce && ncol > 1) {
      var colEls = grid.querySelectorAll(".ig-col"), ticking = false;
      var onScroll = function () {
        if (ticking) return; ticking = true;
        requestAnimationFrame(function () {
          ticking = false;
          var r = grid.getBoundingClientRect(), vh = innerHeight;
          if (r.bottom < 0 || r.top > vh) return;
          var t = (r.top + r.height / 2 - vh / 2) / vh; // -1..1 rond het midden van het scherm
          colEls.forEach(function (c, i) { var dir = i % 2 ? 1 : -1; c.style.transform = "translate3d(0," + (dir * t * 40).toFixed(1) + "px,0)"; });
        });
      };
      addEventListener("scroll", onScroll, { passive: true }); onScroll();
    }
  }

  var done = false;
  function load() {
    if (done) return; done = true;
    // op skylinedigital.es draait de API niet zelf: dan de .nl aanspreken
    fetch((/skylinedigital\.es$/.test(location.hostname) ? "https://www.skylinedigital.nl" : "") + "/api/instagram", { headers: { Accept: "application/json" } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) { if (d) secs.forEach(function (s) { render(s, d); }); })
      .catch(function () {});
  }
  var anchors = []; secs.forEach(function (s) { anchors.push(s.previousElementSibling || s.parentNode); });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) { if (es.some(function (e) { return e.isIntersecting; })) { io.disconnect(); load(); } }, { rootMargin: "600px" });
    anchors.forEach(function (a) { io.observe(a); });
  } else { load(); }
})();
