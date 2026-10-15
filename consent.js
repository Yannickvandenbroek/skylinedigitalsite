/* Cookiemelding voor Google Analytics (toestemmingsmodus v2).
   De standaard staat in de <head> op "denied"; pas na "Akkoord" mag Analytics cookies plaatsen.
   De keuze staat in localStorage (sky_consent) en kan via een link met data-cookie-settings opnieuw worden geopend. */
(function () {
  var KEY = "sky_consent";
  var lang = (document.documentElement.lang || "nl").slice(0, 2);
  var T = {
    nl: { text: "We gebruiken analytische cookies (Google Analytics) om te zien hoe de site wordt gebruikt — alleen met jouw toestemming.", ok: "Akkoord", no: "Weigeren", more: "Cookiebeleid" },
    en: { text: "We use analytics cookies (Google Analytics) to understand how the site is used — only with your consent.", ok: "Accept", no: "Decline", more: "Cookie policy" },
    it: { text: "Usiamo cookie analitici (Google Analytics) per capire come viene usato il sito, solo con il tuo consenso.", ok: "Accetta", no: "Rifiuta", more: "Cookie policy" },
    es: { text: "Usamos cookies analíticas (Google Analytics) para entender cómo se usa la web, solo con tu consentimiento.", ok: "Aceptar", no: "Rechazar", more: "Política de cookies" },
  }[lang] || null;
  if (!T) T = { text: "", ok: "", no: "", more: "" };

  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  function apply(v) {
    if (typeof window.gtag === "function") window.gtag("consent", "update", { analytics_storage: v === "granted" ? "granted" : "denied" });
    if (v !== "granted") {
      // eerder geplaatste Analytics-cookies opruimen
      var host = location.hostname.replace(/^www\./, "");
      document.cookie.split(";").forEach(function (c) {
        var name = c.split("=")[0].trim();
        if (name.indexOf("_ga") === 0) {
          ["", "; domain=" + host, "; domain=." + host].forEach(function (d) {
            document.cookie = name + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + d;
          });
        }
      });
    }
  }

  var box = null;
  function build() {
    var style = document.createElement("style");
    style.textContent =
      ".sky-cookie{position:fixed;left:20px;bottom:20px;z-index:9999;max-width:420px;padding:20px 22px;border-radius:18px;" +
      "background:#0d0e14;color:#f4f1e9;border:1px solid rgba(255,255,255,.12);box-shadow:0 24px 60px rgba(0,0,0,.45);" +
      "font:400 14px/1.55 Inter,system-ui,sans-serif;opacity:0;transform:translateY(12px);transition:opacity .35s,transform .35s}" +
      ".sky-cookie.show{opacity:1;transform:none}" +
      ".sky-cookie p{margin:0 0 14px;color:rgba(244,241,233,.82)}" +
      ".sky-cookie a{color:#f7e3a1;text-decoration:underline;text-underline-offset:3px}" +
      ".sky-cookie-row{display:flex;gap:10px;align-items:center;flex-wrap:wrap}" +
      ".sky-cookie button{cursor:pointer;border-radius:10px;padding:10px 18px;font:700 12px/1 'Inter Tight',Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase}" +
      ".sky-cookie .ok{background:#d9b25a;color:#0d0e14;border:1px solid #d9b25a}" +
      ".sky-cookie .no{background:transparent;color:#f4f1e9;border:1px solid rgba(244,241,233,.35)}" +
      ".sky-cookie .more{margin-left:auto;font-size:12px}" +
      "@media (max-width:600px){.sky-cookie{left:12px;right:12px;bottom:12px;max-width:none}}";
    document.head.appendChild(style);
    box = document.createElement("div");
    box.className = "sky-cookie notranslate";
    box.setAttribute("role", "dialog");
    box.setAttribute("aria-live", "polite");
    box.setAttribute("aria-label", T.more);
    box.innerHTML = "<p>" + T.text + "</p><div class=\"sky-cookie-row\">" +
      "<button type=\"button\" class=\"ok\">" + T.ok + "</button>" +
      "<button type=\"button\" class=\"no\">" + T.no + "</button>" +
      "<a class=\"more\" href=\"/cookiebeleid\">" + T.more + "</a></div>";
    box.querySelector(".ok").addEventListener("click", function () { choose("granted"); });
    box.querySelector(".no").addEventListener("click", function () { choose("denied"); });
    document.body.appendChild(box);
  }
  function show() {
    if (!box) build();
    box.style.display = "";
    requestAnimationFrame(function () { box.classList.add("show"); });
  }
  function hide() {
    if (!box) return;
    box.classList.remove("show");
    setTimeout(function () { box.style.display = "none"; }, 350);
  }
  function choose(v) { set(v); apply(v); hide(); }

  window.skyCookieSettings = show;
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-cookie-settings]");
    if (a) { e.preventDefault(); show(); }
  });

  if (!get()) {
    // pas tonen als de laadanimatie van de homepage klaar is
    var tries = 0;
    (function wait() {
      if (document.documentElement.classList.contains("is-loading") && tries++ < 50) return setTimeout(wait, 300);
      show();
    })();
  }
})();
