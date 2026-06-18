/* ============================================================
   Scroll engine — frame-sequence scrub + reveals + counters
   ============================================================ */

function initScrub(cfg) {
  const section = document.querySelector(cfg.section);
  const canvas  = section.querySelector("canvas");
  const ctx     = canvas.getContext("2d", { alpha: false });
  const lines   = [...section.querySelectorAll(".reveal-line")];
  const bgFill  = cfg.bg || "#0a0a12";

  // Canvas start onzichtbaar zodat de CSS-posterafbeelding zichtbaar is
  canvas.style.opacity = "0";
  canvas.style.transition = "opacity 0.4s";

  // Frames vooraf laden — getekend uit het geheugen is direct (= soepel)
  const images = new Array(cfg.frameCount);
  let firstDrawn = false;
  for (let i = 0; i < cfg.frameCount; i++) {
    const img = new Image();
    img.src = cfg.framePath(i + 1);
    img.onload = () => {
      if (!firstDrawn) { firstDrawn = true; draw(0); canvas.style.opacity = "1"; }
    };
    images[i] = img;
  }

  let current = -1;

  function draw(index) {
    const img = images[index];
    if (!img || !img.complete || !img.naturalWidth) return;
    const cw = canvas.clientWidth, ch = canvas.clientHeight;
    const ir = img.naturalWidth / img.naturalHeight, cr = cw / ch;
    let dw, dh, dx, dy;
    if (ir > cr) { dh = ch; dw = ch * ir; dx = (cw - dw) / 2; dy = 0; }
    else         { dw = cw; dh = cw / ir; dx = 0; dy = (ch - dh) / 2; }
    ctx.fillStyle = bgFill; ctx.fillRect(0, 0, cw, ch);
    ctx.drawImage(img, dx, dy, dw, dh);
  }

  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width  = canvas.clientWidth  * dpr;
    canvas.height = canvas.clientHeight * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    draw(current < 0 ? 0 : current);
  }

  function update() {
    const rect = section.getBoundingClientRect();
    if (rect.bottom < -window.innerHeight || rect.top > window.innerHeight) return;
    const scrollable = rect.height - window.innerHeight;
    const p = Math.min(Math.max(-rect.top / scrollable, 0), 1);

    const idx = Math.min(cfg.frameCount - 1, Math.round(p * (cfg.frameCount - 1)));
    if (idx !== current) { current = idx; draw(idx); }

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
  const scrubs = (window.SCRUB_SECTIONS || [])
    .filter(c => document.querySelector(c.section))
    .map(c => initScrub(c));

  const lenis = new Lenis({ lerp: 0.085, smoothWheel: true });
  window.__lenis = lenis;
  function raf(t) { lenis.raf(t); scrubs.forEach(s => s.update()); requestAnimationFrame(raf); }
  requestAnimationFrame(raf);

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
  const parallaxEls = [...document.querySelectorAll("[data-parallax], .frow-media .media-frame")];
  const vh = () => window.innerHeight;

  function applyParallax() {
    for (const el of parallaxEls) {
      const r = el.getBoundingClientRect();
      if (r.bottom < 0 || r.top > vh()) continue;
      const off = ((r.top + r.height / 2) - vh() / 2) / vh();
      el.style.transform = `translate3d(0, ${(off * -26).toFixed(1)}px, 0)`;
    }
  }

  lenis.on("scroll", () => {
    setNavState();
    applyParallax();
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

  applyParallax();
  setNavState();
  window.addEventListener("resize", setNavState);

  // Magnetic buttons
  document.querySelectorAll(".btn-gold, .btn-dark").forEach(btn => {
    btn.addEventListener("mousemove", e => {
      const r = btn.getBoundingClientRect();
      const x = e.clientX - r.left - r.width / 2;
      const y = e.clientY - r.top - r.height / 2;
      btn.style.transform = `translate(${(x * 0.25).toFixed(1)}px, ${(y * 0.4).toFixed(1)}px)`;
    });
    btn.addEventListener("mouseleave", () => { btn.style.transform = ""; });
  });

  // Keyword marquee
  const firstSection = document.querySelector("section");
  if (firstSection && !document.querySelector(".marquee")) {
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
  lenis.on("scroll", updBar); updBar();

  const fine = window.matchMedia("(hover: hover) and (pointer: fine)").matches;

  // Gold cursor glow (desktop only)
  if (fine) {
    const glow = document.createElement("div"); glow.id = "cursor-glow"; document.body.appendChild(glow);
    let gx = window.innerWidth / 2, gy = window.innerHeight / 2, tx = gx, ty = gy, started = false;
    window.addEventListener("mousemove", e => {
      tx = e.clientX; ty = e.clientY;
      if (!started) { started = true; glow.classList.add("on"); }
    });
    (function follow() {
      gx += (tx - gx) * 0.12; gy += (ty - gy) * 0.12;
      glow.style.transform = `translate3d(${gx.toFixed(1)}px, ${gy.toFixed(1)}px, 0)`;
      requestAnimationFrame(follow);
    })();
  }

  // 3D tilt on cards (desktop only)
  if (fine) {
    document.querySelectorAll(".fcard, .price, .gitem, .quote").forEach(card => {
      card.addEventListener("mousemove", e => {
        const r = card.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        card.style.transform = `perspective(900px) rotateY(${(px * 6).toFixed(2)}deg) rotateX(${(-py * 6).toFixed(2)}deg) translateY(-6px)`;
      });
      card.addEventListener("mouseleave", () => { card.style.transform = ""; });
    });
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
