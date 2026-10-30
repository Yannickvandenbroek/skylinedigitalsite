/* Echte voorstellen op de portfolio (30-10-2026).
   Haalt de voorstellen op die Yannick in het CRM op "Toon als voorbeeld op de website" zette
   (rpc website_voorbeelden) en toont per bedrijf de drie ontwerprichtingen met een link naar
   het echte voorstel. Is er niets aangevinkt, dan blijft de sectie onzichtbaar. */
(function () {
  var doel = document.getElementById("voorstellen-live");
  if (!doel) return;
  var RPC = "https://qccuhmznrlgobfccxiro.supabase.co/rest/v1/rpc/website_voorbeelden";
  var ANON = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFjY3VobXpucmxnb2JmY2N4aXJvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODcwNzU0NjMsImV4cCI6MjEwMjY1MTQ2M30.rbErbtKFoU961NggdmRqyCNlHdtqLLHBxzm8uV1pIDg";
  var taal = (document.documentElement.lang || "nl").slice(0, 2);
  var T = {
    nl: { eyebrow: "Echte voorstellen", kop1: "Drie ontwerpen, ", kop2: "binnen 24 uur.", tekst: "Zo ziet een voorstel eruit: drie echt gebouwde richtingen voor één bedrijf, met hun eigen logo, teksten en foto's. De klant kiest, wij maken de site af.", knop: "Bekijk de drie ontwerpen", cta: "Ook drie ontwerpen voor jouw bedrijf? Gratis en vrijblijvend.", ctaKnop: "Vraag ze aan", url: "/aanvraag" },
    en: { eyebrow: "Real proposals", kop1: "Three designs, ", kop2: "within 24 hours.", tekst: "This is what a proposal looks like: three fully built directions for one business, with their own logo, copy and photos. The client picks one, we finish the site.", knop: "View the three designs", cta: "Three designs for your business too? Free and without obligation.", ctaKnop: "Request them", url: "/en/aanvraag" },
    it: { eyebrow: "Proposte reali", kop1: "Tre design, ", kop2: "entro 24 ore.", tekst: "Ecco una proposta: tre direzioni realmente costruite per un'azienda, con il suo logo, i suoi testi e le sue foto. Il cliente sceglie, noi completiamo il sito.", knop: "Guarda i tre design", cta: "Tre design anche per la tua azienda? Gratis e senza impegno.", ctaKnop: "Richiedili", url: "/it/aanvraag" },
    es: { eyebrow: "Propuestas reales", kop1: "Tres diseños, ", kop2: "en 24 horas.", tekst: "Así es una propuesta: tres direcciones realmente construidas para una empresa, con su propio logo, textos y fotos. El cliente elige y nosotros terminamos la web.", knop: "Ver los tres diseños", cta: "¿Tres diseños también para tu empresa? Gratis y sin compromiso.", ctaKnop: "Solicítalos", url: "https://www.skylinedigital.es/solicitud" },
  }[taal] || null;
  var t = T || { eyebrow: "Echte voorstellen", kop1: "Drie ontwerpen, ", kop2: "binnen 24 uur.", tekst: "", knop: "Bekijk de drie ontwerpen", cta: "", ctaKnop: "Vraag ze aan", url: "/aanvraag" };
  function esc(s) { return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  var css = document.createElement("style");
  css.textContent =
    "#voorstellen-live{padding:110px 24px 90px;background:#0b0b0c;color:#fff}" +
    "#voorstellen-live h2{color:#fff}" +
    "#voorstellen-live .vb-head{max-width:760px;margin:0 auto 46px;text-align:center}" +
    "#voorstellen-live .vb-head p.vb-tekst{color:rgba(255,255,255,.65);line-height:1.6;margin-top:14px}" +
    "#voorstellen-live .vb-lijst{max-width:1180px;margin:0 auto;display:grid;gap:34px}" +
    "#voorstellen-live .vb-item{border:1px solid rgba(255,255,255,.09);border-radius:22px;padding:22px;background:rgba(255,255,255,.025)}" +
    "#voorstellen-live .vb-top{display:flex;flex-wrap:wrap;align-items:baseline;justify-content:space-between;gap:10px;margin-bottom:16px}" +
    "#voorstellen-live .vb-naam{font-size:1.25rem;color:#fff;font-weight:600}" +
    "#voorstellen-live .vb-link{color:#e6c463;text-decoration:none;font-size:.92rem}" +
    "#voorstellen-live .vb-link:hover{text-decoration:underline}" +
    "#voorstellen-live .vb-rij{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}" +
    "@media(max-width:760px){#voorstellen-live .vb-rij{grid-template-columns:1fr}}" +
    "#voorstellen-live .vb-kaart{display:block;text-decoration:none;color:#fff}" +
    "#voorstellen-live .vb-kaart img{width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top;border-radius:12px;border:1px solid rgba(255,255,255,.08);display:block;background:#111}" +
    "#voorstellen-live .vb-kaart span{display:block;margin-top:8px;font-size:.9rem;color:rgba(255,255,255,.75)}" +
    "#voorstellen-live .vb-cta{text-align:center;margin-top:44px;color:rgba(255,255,255,.7)}" +
    "#voorstellen-live .vb-cta a{margin-left:10px}";
  document.head.appendChild(css);

  fetch(RPC, { method: "POST", headers: { apikey: ANON, Authorization: "Bearer " + ANON, "Content-Type": "application/json" }, body: "{}" })
    .then(function (r) { return r.ok ? r.json() : []; })
    .then(function (lijst) {
      if (!Array.isArray(lijst) || !lijst.length) return;
      var html = '<div class="vb-head"><div class="gold-rule" style="margin-inline:auto"></div><p class="eyebrow eyebrow-center">' + esc(t.eyebrow) + "</p>" +
        "<h2>" + esc(t.kop1) + '<span class="gold-text">' + esc(t.kop2) + "</span></h2>" +
        (t.tekst ? '<p class="vb-tekst">' + esc(t.tekst) + "</p>" : "") + "</div><div class=\"vb-lijst\">";
      lijst.forEach(function (v) {
        html += '<div class="vb-item"><div class="vb-top"><span class="vb-naam">' + esc(v.naam) + '</span><a class="vb-link" href="' + esc(v.url) + '" target="_blank" rel="noopener">' + esc(t.knop) + " →</a></div><div class=\"vb-rij\">";
        (v.richtingen || []).slice(0, 3).forEach(function (r) {
          html += '<a class="vb-kaart" href="' + esc(r.home || v.url) + '" target="_blank" rel="noopener">' +
            (r.beeld ? '<img loading="lazy" src="' + esc(r.beeld) + '" alt="' + esc(v.naam + " · " + r.naam) + '">' : "") +
            "<span>" + esc(r.naam) + "</span></a>";
        });
        html += "</div></div>";
      });
      html += "</div>" + (t.cta ? '<p class="vb-cta">' + esc(t.cta) + ' <a class="btn btn-gold" href="' + esc(t.url) + '">' + esc(t.ctaKnop) + "</a></p>" : "");
      doel.innerHTML = html;
      doel.hidden = false;
    })
    .catch(function () {});
})();
