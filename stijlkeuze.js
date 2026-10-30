/* Stijlkeuze met echte voorbeeldsites (31-10-2026), zoals Kas/SiteJob het bij hun voorstellen doet:
   twaalf bestaande websites in vier stijlen. De bezoeker vinkt aan welke hem aanspreken en
   per site wat precies (kleuren, letters, beeld, opbouw). De bouwer maakt de drie ontwerpen
   op die keuze. aanvraag.html roept window.skyStijlkeuze(element) aan zodra stap 2 er staat;
   lead.js leest window.skyStijlkeuzeWaarde() en stuurt de keuze naar het CRM. */
(function () {
  var BEELD = "https://www.skylinedigital.nl/assets/referenties/";
  var taal = (document.documentElement.lang || "nl").slice(0, 2);
  var L = {
    nl: { groep: { strak: "Strak en zakelijk", warm: "Warm en ambachtelijk", donker: "Donker en krachtig", speels: "Licht en speels" },
      spreekt: "Spreekt me aan", wat: "Wat vind je er goed aan?", el: ["Kleuren", "Letters", "Foto's en beeld", "Opbouw"], bekijk: "bekijk site" },
    en: { groep: { strak: "Clean and professional", warm: "Warm and crafted", donker: "Dark and bold", speels: "Light and playful" },
      spreekt: "I like this", wat: "What do you like about it?", el: ["Colours", "Fonts", "Photos and imagery", "Layout"], bekijk: "view site" },
    it: { groep: { strak: "Pulito e professionale", warm: "Caldo e artigianale", donker: "Scuro e deciso", speels: "Leggero e giocoso" },
      spreekt: "Mi piace", wat: "Cosa ti piace?", el: ["Colori", "Caratteri", "Foto e immagini", "Struttura"], bekijk: "vedi sito" },
    es: { groep: { strak: "Limpio y profesional", warm: "Cálido y artesanal", donker: "Oscuro y potente", speels: "Ligero y divertido" },
      spreekt: "Me gusta", wat: "¿Qué te gusta?", el: ["Colores", "Tipografía", "Fotos e imágenes", "Estructura"], bekijk: "ver web" },
  }[taal] || null;
  var t = L || { groep: { strak: "Strak en zakelijk", warm: "Warm en ambachtelijk", donker: "Donker en krachtig", speels: "Licht en speels" }, spreekt: "Spreekt me aan", wat: "Wat vind je er goed aan?", el: ["Kleuren", "Letters", "Foto's en beeld", "Opbouw"], bekijk: "bekijk site" };
  var EL_SLEUTELS = ["kleuren", "letters", "beeld", "opbouw"];
  var SITES = [
    { id: "coolblue", naam: "Coolblue", url: "https://www.coolblue.nl", stijl: "strak" },
    { id: "kemkens", naam: "Kemkens", url: "https://www.kemkens.nl", stijl: "strak" },
    { id: "linear", naam: "Linear", url: "https://linear.app", stijl: "strak" },
    { id: "dille-kamille", naam: "Dille & Kamille", url: "https://www.dille-kamille.nl", stijl: "warm" },
    { id: "tonys", naam: "Tony's Chocolonely", url: "https://www.tonyschocolonely.com/nl/nl", stijl: "warm" },
    { id: "studio-henk", naam: "Studio HENK", url: "https://www.studio-henk.nl", stijl: "warm" },
    { id: "porsche", naam: "Porsche", url: "https://www.porsche.com/netherlands/nl/", stijl: "donker" },
    { id: "rapha", naam: "Rapha", url: "https://www.rapha.cc", stijl: "donker" },
    { id: "nike", naam: "Nike", url: "https://www.nike.com/nl", stijl: "donker" },
    { id: "picnic", naam: "Picnic", url: "https://picnic.app/nl/", stijl: "speels" },
    { id: "oatly", naam: "Oatly", url: "https://www.oatly.com", stijl: "speels" },
    { id: "headspace", naam: "Headspace", url: "https://www.headspace.com", stijl: "speels" },
  ];
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); }

  var css = document.createElement("style");
  css.textContent =
    ".ref-groep{margin:18px 0 6px;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:#d4a23f}" +
    ".ref-rij{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;align-items:start}" +
    "@media(max-width:640px){.ref-rij{grid-template-columns:1fr}}" +
    ".ref-kaart{border:1px solid rgba(255,255,255,.1);border-radius:14px;overflow:hidden;background:rgba(255,255,255,.03);transition:border-color .2s,box-shadow .2s;text-transform:none;letter-spacing:normal}" +
    ".ref-kaart.aan{border-color:#d4a23f;box-shadow:0 0 0 1px #d4a23f inset}" +
    ".ref-kaart img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;object-position:top;background:#111}" +
    ".ref-onder{padding:10px 12px 12px}" +
    ".ref-kop{display:flex;justify-content:space-between;align-items:baseline;gap:8px}" +
    ".ref-kop strong{color:#fff;font-size:.92rem;font-weight:600}" +
    ".ref-kop a{color:rgba(255,255,255,.45);font-size:.72rem;text-decoration:underline}" +
    ".ref-knop{margin-top:8px;width:100%;padding:8px 10px;border-radius:999px;border:1px solid rgba(255,255,255,.2);background:transparent;color:#fff;font:inherit;font-size:.82rem;cursor:pointer}" +
    ".ref-kaart.aan .ref-knop{background:#d4a23f;border-color:#d4a23f;color:#1a1408;font-weight:600}" +
    ".ref-el{display:none;margin-top:8px}" +
    ".ref-kaart.aan .ref-el{display:block}" +
    ".ref-el p{margin:0 0 6px;font-size:.74rem;color:rgba(255,255,255,.55)}" +
    ".ref-chip{display:inline-block;margin:0 6px 6px 0;padding:5px 10px;border-radius:999px;border:1px solid rgba(255,255,255,.18);font-size:.74rem;color:rgba(255,255,255,.8);cursor:pointer;user-select:none}" +
    ".ref-chip.aan{border-color:#d4a23f;color:#f3d680;background:rgba(212,162,63,.12)}";
  document.head.appendChild(css);

  function vulVerborgen() {
    var h = document.getElementById("s2-stijl");
    if (h) h.value = window.skyStijlkeuzeWaarde().map(function (s) { return s.naam + (s.elementen.length ? " (" + s.elementen.join(", ") + ")" : ""); }).join("; ");
  }

  window.skyStijlkeuze = function (doel) {
    if (!doel) return;
    var html = "";
    ["strak", "warm", "donker", "speels"].forEach(function (g) {
      html += '<div class="ref-groep">' + esc(t.groep[g]) + '</div><div class="ref-rij">';
      SITES.filter(function (s) { return s.stijl === g; }).forEach(function (s) {
        html += '<div class="ref-kaart" data-id="' + s.id + '">' +
          '<img loading="lazy" src="' + BEELD + s.id + '.jpg" alt="' + esc(s.naam) + '">' +
          '<div class="ref-onder"><div class="ref-kop"><strong>' + esc(s.naam) + '</strong><a href="' + s.url + '" target="_blank" rel="noopener">' + esc(t.bekijk) + "</a></div>" +
          '<button type="button" class="ref-knop">' + esc(t.spreekt) + "</button>" +
          '<div class="ref-el"><p>' + esc(t.wat) + "</p>" +
          t.el.map(function (e, i) { return '<span class="ref-chip" data-el="' + EL_SLEUTELS[i] + '">' + esc(e) + "</span>"; }).join("") +
          "</div></div></div>";
      });
      html += "</div>";
    });
    doel.innerHTML = html;
    doel.addEventListener("click", function (e) {
      var knop = e.target.closest(".ref-knop");
      var chip = e.target.closest(".ref-chip");
      if (knop) knop.closest(".ref-kaart").classList.toggle("aan");
      if (chip) chip.classList.toggle("aan");
      if (knop || chip) vulVerborgen();
    });
  };

  // [{ id, naam, url, stijl, elementen: ["kleuren", …] }] van de aangevinkte sites.
  window.skyStijlkeuzeWaarde = function () {
    return Array.prototype.slice.call(document.querySelectorAll("#stijl-grid .ref-kaart.aan")).map(function (k) {
      var s = SITES.filter(function (x) { return x.id === k.getAttribute("data-id"); })[0];
      var el = Array.prototype.slice.call(k.querySelectorAll(".ref-chip.aan")).map(function (c) { return c.getAttribute("data-el"); });
      return { id: s.id, naam: s.naam, url: s.url, stijl: s.stijl, elementen: el };
    });
  };
})();
