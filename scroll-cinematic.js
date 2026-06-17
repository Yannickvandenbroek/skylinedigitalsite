/* ============================================================
   PRISM — scroll engine
   Multiple canvas frame-sequence scrub sections + scroll reveals + counters
   ============================================================ */
function initScrub(cfg) {
  const section = document.querySelector(cfg.section);
  const canvas  = section.querySelector("canvas");
  const ctx     = canvas.getContext("2d", { alpha: false });
  const lines   = [...section.querySelectorAll(".reveal-line")];
  const bgFill  = cfg.bg || "#0a0a12";
  const images = [];
  let firstDrawn = false;
  for (let i = 0; i < cfg.frameCount; i++) {
    const img = new Image();
    img.src = cfg.framePath(i + 1);
    img.onload = () => { if (!firstDrawn) { firstDrawn = true; draw(0); } };
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
    draw(current < 0 ? 0 : current);
  }
  function update() {
    const rect = section.getBoundingClientRect();
    if (rect.bottom < -window.innerHeight || rect.top > window.innerHeight) return;
    const scrollable = rect.height - window.innerHeight;
    const p = Math.min(Math.max(-rect.top / scrollable, 0), 1);
    const idx = Math.min(cfg.frameCount - 1, Math.floor(p * (cfg.frameCount - 1)));
    if (idx !== current) { current = idx; draw(idx); }
    for (const el of lines) {
      const a = parseFloat(el.dataset.in), b = parseFloat(el.dataset.out);
      const mid = (a + b) / 2, half = (b - a) / 2;
      let o = 1 - Math.abs(p - mid) / half;
      o = Math.max(0, Math.min(1, o));
      el.style.opacity = o.toFixed(3);
      el.style.transform = `translateY(${(1 - o) * 30}px)`;
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
    el.textContent = (target % 1 === 0 ? Math.round(target*eased) : (target*eased).toFixed(1)) + suffix;
    if (k < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

document.addEventListener("DOMContentLoaded", () => {
  const scrubs = (window.SCRUB_SECTIONS || [])
    .filter(c => document.querySelector(c.section))
    .map(initScrub);

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
  }, { threshold: 0.25 });
  document.querySelectorAll(".reveal, .stat-num").forEach((el) => io.observe(el));

  const nav = document.getElementById("nav");
  const heroSection = document.querySelector("#hero");
  // The full-bleed hero the nav sits over: stay transparent until scrolled past it.
  const navHero = document.querySelector("#hero") || document.querySelector(".page-hero");
  function setNavState() {
    if (!nav) return;
    const solid = navHero ? (navHero.getBoundingClientRect().bottom <= 80) : (window.scrollY > 40);
    nav.classList.toggle("scrolled", solid);
  }
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
      // Fade the static hero intro out over the first ~22% of the scrub.
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

  // Magnetic primary buttons
  document.querySelectorAll(".btn-gold, .btn-dark").forEach(btn => {
    btn.addEventListener("mousemove", e => {
      const r = btn.getBoundingClientRect();
      const x = e.clientX - r.left - r.width / 2;
      const y = e.clientY - r.top - r.height / 2;
      btn.style.transform = `translate(${(x * 0.25).toFixed(1)}px, ${(y * 0.4).toFixed(1)}px)`;
    });
    btn.addEventListener("mouseleave", () => { btn.style.transform = ""; });
  });

  // Keyword marquee, injected after the hero on every page
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
});
