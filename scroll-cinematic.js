/* ============================================================
   Scroll engine — frame-sequence scrub + reveals + counters
   ============================================================ */

/* Gedeelde frame-lader. Alle frames tegelijk opvragen laat ze om bandbreedte
   vechten, waardoor de hero lang op zijn beelden wacht. Daarom één wachtrij met
   een beperkt aantal gelijktijdige downloads: eerst de sectie die in beeld is,
   en per sectie van grof naar fijn (elke 8e, 4e, 2e, dan de rest), zodat de hele
   scrub al vroeg bruikbaar is. Elk frame wordt na het laden vooraf gedecodeerd,
   zodat het tekenen tijdens het scrollen geen haperingen geeft. */
const frameLoader = (() => {
  const MAX = 6;
  const jobs = [];            // { img, src, done, prio() }
  let active = 0;
  function next() {
    while (active < MAX && jobs.length) {
      // hoogste prioriteit eerst; binnen dezelfde prioriteit de volgorde van aanmelden
      let best = 0, bestP = jobs[0].prio();
      for (let i = 1; i < jobs.length && bestP < 2; i++) {
        const pr = jobs[i].prio();
        if (pr > bestP) { best = i; bestP = pr; }
      }
      const job = jobs.splice(best, 1)[0];
      active++;
      const finish = ok => { active--; job.done(ok); next(); };
      job.img.onload = () => {
        const d = job.img.decode ? job.img.decode() : Promise.resolve();
        d.then(() => finish(true), () => finish(true));
      };
      job.img.onerror = () => finish(false);
      job.img.src = job.src;
    }
  }
  return { add(job) { jobs.push(job); }, start: next };
})();

/* Volgorde van grof naar fijn: 0, laatste, dan stappen van 8, 4, 2, 1 */
function coarseToFine(n) {
  const seen = new Set(), order = [];
  const push = i => { if (i >= 0 && i < n && !seen.has(i)) { seen.add(i); order.push(i); } };
  push(0); push(n - 1);
  for (const step of [8, 4, 2, 1]) for (let i = 0; i < n; i += step) push(i);
  return order;
}

function initScrub(cfg) {
  const section = document.querySelector(cfg.section);
  const canvas  = section.querySelector("canvas");
  const ctx     = canvas.getContext("2d", { alpha: false });
  const lines   = [...section.querySelectorAll(".reveal-line")];
  const moments = [...section.querySelectorAll(".moment")];
  const bgFill  = cfg.bg || "#0a0a12";
  const n       = cfg.frameCount;

  /* Niet-lineaire scroll→frame-koppeling (optioneel): cfg.segments = [[van, tot, gewicht], …]
     in frames. Een hoger gewicht geeft dat stuk meer scrollafstand, zodat de film daar
     vertraagt en de tekst leesbaar blijft; een laag gewicht laat een overgang vlot lopen. */
  const segs = cfg.segments || [[0, n - 1, 1]];
  const cum = [0]; let totalW = 0;
  for (const [a, b, w] of segs) { totalW += (b - a) * w; cum.push(totalW); }
  function progressToFrame(p) {
    const target = p * totalW;
    for (let k = 0; k < segs.length; k++) {
      if (target <= cum[k + 1] || k === segs.length - 1) {
        const [a, , w] = segs[k];
        return Math.min(n - 1, a + (target - cum[k]) / w);
      }
    }
    return n - 1;
  }
  // Zichtbaarheid van een tekstmoment in frame-ruimte: in- en uitfaden over 12% van het venster
  function momentOpacity(f, from, to) {
    const fade = Math.max(3, (to - from) * 0.12);
    if (f <= from || f >= to) return 0;
    return Math.max(0, Math.min(1, Math.min((f - from) / fade, (to - f) / fade)));
  }

  // Canvas start onzichtbaar zodat de CSS-posterafbeelding zichtbaar is
  canvas.style.opacity = "0";
  canvas.style.transition = "opacity 0.4s";

  const images = new Array(n);
  const ready  = new Array(n).fill(false);
  let pos = 0, drawn = "", near = false, settled = 0;   // pos = fractionele framepositie

  // 2 = in of vlak bij beeld, 1 = eerste sectie van de pagina, 0 = later
  const prio = () => (near ? 2 : cfg.first ? 1 : 0);
  for (const i of coarseToFine(n)) {
    const img = new Image();
    img.decoding = "async";
    images[i] = img;
    frameLoader.add({
      img, src: cfg.framePath(i + 1), prio,
      done(ok) {
        settled++;
        if (cfg.onProgress) cfg.onProgress(settled, n);
        if (!ok) return;
        ready[i] = true;
        if (!drawn) canvas.style.opacity = "1";
        paint();                      // verfijnt het beeld zodra een beter frame binnen is
      }
    });
  }

  // Dichtstbijzijnde frame dat al geladen is, zodat het beeld nooit blijft hangen
  function nearestReady(idx) {
    if (ready[idx]) return idx;
    for (let d = 1; d < n; d++) {
      if (idx - d >= 0 && ready[idx - d]) return idx - d;
      if (idx + d < n  && ready[idx + d]) return idx + d;
    }
    return -1;
  }

  function blit(img, alpha) {
    const cw = canvas.clientWidth, ch = canvas.clientHeight;
    const ir = img.naturalWidth / img.naturalHeight, cr = cw / ch;
    let dw, dh, dx, dy;
    if (ir > cr) { dh = ch; dw = ch * ir; dx = (cw - dw) / 2; dy = 0; }
    else         { dw = cw; dh = cw / ir; dx = 0; dy = (ch - dh) / 2; }
    ctx.globalAlpha = alpha;
    ctx.drawImage(img, dx, dy, dw, dh);
    ctx.globalAlpha = 1;
  }

  /* Tekent de positie tussen twee frames in: het volgende frame vloeit over het
     huidige heen, zodat de beweging doorloopt in plaats van per frame te verspringen. */
  function paint(force) {
    const base = Math.min(n - 1, Math.floor(pos));
    let a = base, mix = 0;
    if (ready[base] && base + 1 < n && ready[base + 1]) mix = Math.round((pos - base) * 16) / 16;
    else { a = nearestReady(Math.round(pos)); if (a < 0) return; }
    const key = a + ":" + mix;
    if (key === drawn && !force) return;
    ctx.fillStyle = bgFill; ctx.fillRect(0, 0, canvas.clientWidth, canvas.clientHeight);
    blit(images[a], 1);
    if (mix > 0) blit(images[a + 1], mix);
    drawn = key;
  }

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width  = canvas.clientWidth  * dpr;
    canvas.height = canvas.clientHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    // Bewust geen imageSmoothingQuality "high": op retina-schermen kost dat per
    // getekend frame zoveel rekentijd dat het scrollen terugvalt naar ~12 fps.
    paint(true);
  }

  function update() {
    const rect = section.getBoundingClientRect();
    const vh = window.innerHeight;
    // binnen anderhalf scherm afstand: deze sectie krijgt voorrang in de wachtrij
    near = rect.top < vh * 2.5 && rect.bottom > -vh * 1.5;
    if (rect.bottom < -vh || rect.top > vh) return;
    const scrollable = rect.height - vh;
    const p = Math.min(Math.max(-rect.top / scrollable, 0), 1);

    pos = progressToFrame(p);
    paint();

    for (const el of moments) {
      const from = parseFloat(el.dataset.from), to = parseFloat(el.dataset.to);
      const hold = el.classList.contains("final") && pos >= to;   // slotmoment blijft staan
      const o = hold ? 1 : momentOpacity(pos, from, to);
      el.style.opacity = o.toFixed(3);
      el.style.transform = `translateY(${((1 - o) * 24).toFixed(1)}px)`;
      el.style.pointerEvents = o > 0.5 ? "auto" : "none";
    }
    if (cfg.onScrub) cfg.onScrub(p, pos);

    for (const el of lines) {
      const a = parseFloat(el.dataset.in), b = parseFloat(el.dataset.out);
      const mid = (a + b) / 2, half = (b - a) / 2;
      const raw = Math.max(-1, Math.min(1, (p - mid) / half));
      const o = Math.max(0, 1 - Math.abs(raw));
      el.style.opacity = o.toFixed(3);
      el.style.transform = `translateY(${(-raw * 30).toFixed(1)}px)`;
    }
  }

  window.addEventListener("resize", resize);
  resize();
  return { update, resize };
}

function animateCount(el) {
  const target = parseFloat(el.dataset.count), suffix = el.dataset.suffix || "";
  const dur = 1500, t0 = performance.now();
  function step(t) {
    const k = Math.min((t - t0) / dur, 1), eased = 1 - Math.pow(1 - k, 3);
    el.textContent = (target % 1 === 0 ? Math.round(target * eased) : (target * eased).toFixed(1)) + suffix;
    if (k < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

document.addEventListener("DOMContentLoaded", () => {
  /* Laadscherm (alleen als de pagina er een heeft): blijft staan tot alle frames
     van de eerste animatie binnen zijn, zodat scrollen direct soepel is. */
  const loader = document.getElementById("loader");
  const loaderFill = document.getElementById("loader-fill");
  const loaderPct  = document.getElementById("loader-pct");
  let loaderDone = !loader;
  function hideLoader() {
    if (loaderDone) return;
    loaderDone = true;
    loader.classList.add("done");
    document.documentElement.classList.remove("is-loading");
    if (window.__lenis) window.__lenis.start();
    setTimeout(() => loader.remove(), 700);
  }
  function heroProgress(done, total) {
    if (loaderDone) return;
    const pct = Math.round((done / total) * 100);
    if (loaderFill) loaderFill.style.width = pct + "%";
    if (loaderPct)  loaderPct.textContent = pct + "%";
    if (done >= total) hideLoader();
  }
  if (loader) setTimeout(hideLoader, 12000);   // failsafe: nooit blijven hangen

  const scrubs = (window.SCRUB_SECTIONS || [])
    .filter(c => document.querySelector(c.section))
    .map((c, i) => initScrub({ ...c, first: i === 0, onProgress: i === 0 ? heroProgress : null }));
  scrubs.forEach(s => s.update());   // bepaalt welke sectie in beeld is vóór het laden start
  frameLoader.start();

  /* Smooth scroll (Lenis) alleen op een pagina met een scroll-animatie; alle
     gewone pagina's scrollen met de standaard browserscroll. */
  let lenis = null;
  if (scrubs.length && window.Lenis) {
    lenis = new Lenis({ lerp: 0.085, smoothWheel: true });
    window.__lenis = lenis;
    if (!loaderDone) lenis.stop();
    const raf = t => { lenis.raf(t); scrubs.forEach(s => s.update()); requestAnimationFrame(raf); };
    requestAnimationFrame(raf);
  }
  const onScroll = fn => lenis ? lenis.on("scroll", fn) : window.addEventListener("scroll", fn, { passive: true });

  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("in");
      if (e.target.classList.contains("stat-num")) animateCount(e.target);
      io.unobserve(e.target);
    });
  }, { threshold: 0, rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".reveal, .stat-num").forEach((el) => io.observe(el));

  const nav = document.getElementById("nav");
  const navHero = document.querySelector("#hero") || document.querySelector(".page-hero");
  function setNavState() {
    if (!nav) return;
    const solid = navHero ? (navHero.getBoundingClientRect().bottom <= 80) : (window.scrollY > 40);
    nav.classList.toggle("scrolled", solid);
  }

  const heroSection = document.querySelector("#hero");
  const progressFill = document.getElementById("progress-fill");
  const heroFades = [...document.querySelectorAll(".hero-fade")];
  onScroll(() => {
    setNavState();
    if (heroSection) {
      const rect = heroSection.getBoundingClientRect();
      const p = Math.min(Math.max(-rect.top / (rect.height - window.innerHeight), 0), 1);
      if (progressFill) progressFill.style.width = (p * 100).toFixed(1) + "%";
      const o = Math.max(0, Math.min(1, 1 - p / 0.22));
      heroFades.forEach(el => {
        el.style.opacity = o.toFixed(3);
        el.style.transform = `translateY(${(1 - o) * -40}px)`;
        el.style.pointerEvents = o < 0.05 ? "none" : "";
      });
    }
  });

  setNavState();
  window.addEventListener("resize", setNavState);

  // Keyword marquee
  const firstSection = document.querySelector("section");
  if (firstSection && !document.querySelector(".marquee") && !("noMarquee" in document.body.dataset)) {
    const words = ["Webdesign", "SEO", "Drone", "Video", "Social Media", "AI Content", "Branding", "Strategie", "Fotografie", "Montage"];
    const m = document.createElement("div"); m.className = "marquee";
    const track = document.createElement("div"); track.className = "marquee-track";
    const group = () => {
      const g = document.createElement("div"); g.className = "marquee-group";
      words.forEach(w => { const s = document.createElement("span"); s.textContent = w; g.appendChild(s); });
      return g;
    };
    track.appendChild(group()); track.appendChild(group());
    m.appendChild(track);
    firstSection.insertAdjacentElement("afterend", m);
  }

  // Top scroll-progress bar
  const bar = document.createElement("div"); bar.id = "scroll-bar"; document.body.appendChild(bar);
  function updBar() {
    const h = document.documentElement.scrollHeight - window.innerHeight;
    bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0).toFixed(2) + "%";
  }
  onScroll(updBar); updBar();

  /* ============================================================
     Awards-laag: woordonthulling, spookwoorden, spotlight, cursor,
     parallax, kanteling, kinetische kop
     ============================================================ */
  const fineInput = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Koppen opsplitsen in woorden die één voor één omhoog schuiven
  document.querySelectorAll(".page-hero h1, .section-head h2, .frow-copy h2, .cta-band h2, .over-copy h2, .fgrid-head h2").forEach(h => {
    if (h.closest(".pf-h1, .moment")) return;
    let i = 0;
    const wrap = node => {
      if (node.nodeType === 3) {
        const frag = document.createDocumentFragment();
        node.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(" ")); return; }
          const w = document.createElement("span"); w.className = "w";
          const inner = document.createElement("span"); inner.textContent = part; inner.style.setProperty("--i", i++);
          // goudkleur zit als achtergrond-clip op de ouder; losse woorden moeten hem zelf dragen
          if (node.parentElement && node.parentElement !== h && node.parentElement.classList.contains("gold-text")) inner.classList.add("gold-text");
          w.appendChild(inner); frag.appendChild(w);
        });
        node.replaceWith(frag);
      } else if (node.nodeType === 1 && node.tagName !== "BR") {
        [...node.childNodes].forEach(wrap);
      }
    };
    [...h.childNodes].forEach(wrap);
    h.querySelectorAll(".gold-text").forEach(el => { if (el.querySelector(".w")) el.classList.replace("gold-text", "gold-wrap"); });
    h.classList.add("split");
    const hero = h.closest(".page-hero");
    if (hero) { requestAnimationFrame(() => requestAnimationFrame(() => { h.classList.add("in-now"); hero.classList.add("in-now"); })); }
    else io.observe(h);
  });

  // Spookwoord achter de paginahero: het eerste woord van de kop, enorm en omlijnd
  const pageHero = document.querySelector(".page-hero");
  if (pageHero) {
    const h1 = pageHero.querySelector("h1");
    const word = (h1 ? h1.textContent.trim().split(/\s+/).find(w => w.length > 3) : "") || "Skyline";
    const g = document.createElement("div"); g.className = "ghost notranslate"; g.setAttribute("aria-hidden", "true");
    g.textContent = word.replace(/[^\p{L}\p{N}]/gu, "").toUpperCase();
    pageHero.appendChild(g);
  }

  // Groot omlijnd woordmerk boven de footer
  const footer = document.querySelector(".footer");
  if (footer) {
    const big = document.createElement("div"); big.className = "footer-big notranslate"; big.setAttribute("aria-hidden", "true"); big.textContent = "SKYLINE DIGITAL";
    footer.insertBefore(big, footer.firstChild);
  }

  // Spotlight + 3D-kanteling op kaarten
  if (fineInput && !reduceMotion) {
    document.querySelectorAll(".fcard, .price, .quote, .gitem").forEach(card => {
      card.addEventListener("pointermove", e => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width, py = (e.clientY - r.top) / r.height;
        card.style.setProperty("--mx", (px * 100).toFixed(1) + "%");
        card.style.setProperty("--my", (py * 100).toFixed(1) + "%");
        card.style.transform = `perspective(900px) rotateY(${((px - .5) * 9).toFixed(2)}deg) rotateX(${((.5 - py) * 9).toFixed(2)}deg) translateY(-10px)`;
      });
      card.addEventListener("pointerleave", () => { card.style.transform = ""; });
    });
  }

  // Eigen cursor
  if (fineInput && !reduceMotion) {
    const dot = document.createElement("div"); dot.id = "cursor";
    const ring = document.createElement("div"); ring.id = "cursor-ring";
    document.body.append(dot, ring);
    let tx = innerWidth / 2, ty = innerHeight / 2, rx = tx, ry = ty, shown = false;
    window.addEventListener("pointermove", e => {
      tx = e.clientX; ty = e.clientY;
      if (!shown) { shown = true; document.documentElement.classList.add("has-cursor"); }
      const t = e.target;
      document.documentElement.classList.toggle("cur-media", !!t.closest(".media-frame, .gitem, .pf-card, .pv-card, .hero-card"));
      document.documentElement.classList.toggle("cur-link", !t.closest(".media-frame, .gitem, .pf-card, .pv-card, .hero-card") && !!t.closest("a, button, .fcard, .price"));
    });
    document.addEventListener("mouseleave", () => document.documentElement.classList.remove("has-cursor"));
    (function follow(){
      rx += (tx - rx) * .16; ry += (ty - ry) * .16;
      dot.style.transform = `translate3d(${tx}px, ${ty}px, 0)`;
      ring.style.transform = `translate3d(${rx.toFixed(1)}px, ${ry.toFixed(1)}px, 0)`;
      requestAnimationFrame(follow);
    })();
  }

  // Parallax op hero-achtergrond, spookwoorden en sectienummers + kinetische kop
  if (!reduceMotion) {
    const heroBg = document.querySelector(".page-hero-bg img");
    const ghost = document.querySelector(".page-hero .ghost");
    const heroH1 = document.querySelector(".page-hero h1");
    const frames = [...document.querySelectorAll(".frow-media .media-frame, .over-media .media-frame")];
    let ticking = false;
    function parallax() {
      ticking = false;
      const y = window.scrollY, vh = innerHeight;
      if (heroBg) heroBg.style.transform = `scale(1.08) translate3d(0, ${(y * .22).toFixed(1)}px, 0)`;
      if (ghost) ghost.style.transform = `translate3d(${(-y * .12).toFixed(1)}px, ${(-y * .18).toFixed(1)}px, 0)`;
      if (heroH1) heroH1.style.setProperty("--wght", Math.round(Math.max(500, 900 - y * .55)));
      for (const el of frames) {
        const r = el.getBoundingClientRect();
        if (r.bottom < 0 || r.top > vh) continue;
        const off = ((r.top + r.height / 2) - vh / 2) / vh;
        el.style.transform = `translate3d(0, ${(off * -40).toFixed(1)}px, 0)`;
      }
    }
    window.addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(parallax); } }, { passive: true });
    parallax();
  }

  // Marquee versnelt mee met de scrollsnelheid
  const track = document.querySelector(".marquee-track");
  if (track && !reduceMotion) {
    let lastY = scrollY, vel = 0;
    window.addEventListener("scroll", () => { vel = Math.min(4, Math.abs(scrollY - lastY) / 40); lastY = scrollY; }, { passive: true });
    (function spin(){ vel *= .92; track.style.animationDuration = (36 / (1 + vel * 2)).toFixed(1) + "s"; requestAnimationFrame(spin); })();
  }

  // Taalkeuze in de header: Nederlands is de brontaal; andere talen via Google Translate.
  // De keuze staat in de cookie "googtrans" (/nl/<taal>), die Google zelf ook leest.
  const FLAGS = {
    nl: '<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#21468B"/><rect width="24" height="10.7" fill="#fff"/><rect width="24" height="5.3" fill="#AE1C28"/></svg>',
    en: '<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#012169"/><path d="M0 0l24 16M24 0L0 16" stroke="#fff" stroke-width="3.2"/><path d="M0 0l24 16M24 0L0 16" stroke="#C8102E" stroke-width="1.2"/><path d="M12 0v16M0 8h24" stroke="#fff" stroke-width="5"/><path d="M12 0v16M0 8h24" stroke="#C8102E" stroke-width="2.6"/></svg>',
    it: '<svg viewBox="0 0 24 16"><rect width="8" height="16" fill="#009246"/><rect x="8" width="8" height="16" fill="#fff"/><rect x="16" width="8" height="16" fill="#CE2B37"/></svg>',
    es: '<svg viewBox="0 0 24 16"><rect width="24" height="16" fill="#AA151B"/><rect y="4" width="24" height="8" fill="#F1BF00"/></svg>',
  };
  const LANGS = [["nl", "Nederlands"], ["en", "English"], ["it", "Italiano"], ["es", "Español"]];
  const curLang = (document.cookie.match(/(?:^|; )googtrans=\/nl\/([a-z]{2})/) || [])[1] || "nl";
  function setLang(code) {
    const host = location.hostname.replace(/^www\./, "");
    const kill = "googtrans=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";
    document.cookie = kill; document.cookie = kill + "; domain=" + host; document.cookie = kill + "; domain=." + host;
    if (code !== "nl") {
      const val = "googtrans=/nl/" + code + "; path=/; max-age=31536000";
      document.cookie = val; document.cookie = val + "; domain=." + host;
    }
    location.reload();
  }
  if (nav) {
    const lang = document.createElement("div"); lang.className = "lang notranslate";
    lang.innerHTML = '<button type="button" class="lang-btn" aria-haspopup="listbox" aria-expanded="false" aria-label="Taal kiezen">' +
      '<span class="flag">' + FLAGS[curLang] + '</span><span class="lang-code">' + curLang.toUpperCase() + '</span></button>' +
      '<ul class="lang-menu" role="listbox">' + LANGS.map(([c, n]) =>
        '<li><button type="button" role="option" data-lang="' + c + '" aria-selected="' + (c === curLang) + '"><span class="flag">' + FLAGS[c] + '</span>' + n + '</button></li>').join("") + '</ul>';
    const cta = nav.querySelector(".nav-cta");
    cta ? nav.insertBefore(lang, cta) : nav.appendChild(lang);
    const btn = lang.querySelector(".lang-btn");
    btn.addEventListener("click", (e) => { e.stopPropagation(); const open = lang.classList.toggle("open"); btn.setAttribute("aria-expanded", open); });
    lang.querySelectorAll("[data-lang]").forEach(b => b.addEventListener("click", () => setLang(b.dataset.lang)));
    document.addEventListener("click", (e) => { if (!lang.contains(e.target)) lang.classList.remove("open"); });
  }
  if (curLang !== "nl") {
    const holder = document.createElement("div"); holder.id = "google_translate_element"; holder.hidden = true; document.body.appendChild(holder);
    window.googleTranslateElementInit = function () {
      new google.translate.TranslateElement({ pageLanguage: "nl", includedLanguages: "nl,en,it,es", autoDisplay: false }, "google_translate_element");
    };
    const gt = document.createElement("script"); gt.src = "https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"; document.head.appendChild(gt);
  }

  // Mobile nav toggle
  const navToggle = document.getElementById("nav-toggle");
  const navLinksEl = document.getElementById("nav-links");
  if (navToggle && navLinksEl && nav) {
    const closeMenu = () => {
      navLinksEl.classList.remove("open"); navToggle.classList.remove("open");
      nav.classList.remove("menu-open"); navToggle.setAttribute("aria-expanded", "false");
    };
    navToggle.addEventListener("click", (e) => {
      e.stopPropagation();
      const open = navLinksEl.classList.toggle("open");
      navToggle.classList.toggle("open", open);
      nav.classList.toggle("menu-open", open);
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    navLinksEl.querySelectorAll("a").forEach(a => a.addEventListener("click", closeMenu));
    document.addEventListener("click", (e) => {
      if (navLinksEl.classList.contains("open") && !navLinksEl.contains(e.target) && !navToggle.contains(e.target)) closeMenu();
    });
  }
});
