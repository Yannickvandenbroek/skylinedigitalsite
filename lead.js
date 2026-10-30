/* Aanvragen ook naar het CRM (crm.skylinedigital.nl), naast de mail via Formspree.
   Luistert mee op elk formulier dat naar Formspree gaat, leest dezelfde velden en stuurt ze
   naar de edge function website-lead. Bij "Gratis testwebsite" gaan de losse wizard-antwoorden
   (wat het bedrijf doet, stijl, beschrijving, huidige site) en het logo en de foto's mee,
   zodat het CRM meteen een demo kan bouwen. Faalt dit stilletjes, dan merkt de bezoeker niets:
   de mail via Formspree blijft de leidende weg. */
(function () {
  var URL = "https://qccuhmznrlgobfccxiro.supabase.co/functions/v1/website-lead";
  var MAX_TOTAAL = 40 * 1024 * 1024;
  var gestuurd = false;
  function veld(fd, namen) {
    for (var i = 0; i < namen.length; i++) { var v = fd.get(namen[i]); if (v && typeof v === "string" && v.trim()) return v.trim(); }
    return "";
  }
  function waarde(id) { var el = document.getElementById(id); return el && el.value ? String(el.value).trim() : ""; }
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form || !/formspree\.io/.test(form.action || "") || gestuurd) return;
    // Na de eigen afhandeling van de pagina lezen, zodat verborgen velden (diensten, details) al gevuld zijn.
    setTimeout(function () {
      var fd = new FormData(form);
      var email = veld(fd, ["E-mail", "Email", "email"]);
      if (!/\S+@\S+\.\S+/.test(email)) return;
      var naam = veld(fd, ["Naam", "naam"]);
      var diensten = veld(fd, ["Geselecteerde diensten"]);
      var uit = new FormData();
      uit.append("voornaam", veld(fd, ["Voornaam"]) || naam.split(" ")[0] || "");
      uit.append("achternaam", veld(fd, ["Achternaam"]) || naam.split(" ").slice(1).join(" "));
      uit.append("bedrijf", veld(fd, ["Bedrijf"]));
      uit.append("email", email);
      uit.append("telefoon", veld(fd, ["Telefoon", "telefoon"]));
      uit.append("diensten", diensten);
      uit.append("details", veld(fd, ["Projectdetails", "Bericht", "message"]));
      uit.append("pagina", location.pathname);
      uit.append("taal", (document.documentElement.lang || "nl").slice(0, 2));
      uit.append("website_url_check", veld(fd, ["website_url_check"]));
      // Wizard-antwoorden los meesturen (alleen aanwezig op de aanvraagpagina).
      uit.append("branche", waarde("s2-bedrijf"));
      uit.append("bestaand", waarde("s2-bestaand"));
      uit.append("url", waarde("s2-url"));
      uit.append("stijl", waarde("s2-stijl"));
      // Stijlkaarten (gratis testwebsite): de sleutels (strak, warm, donker, speels) en een voorbeeldsite.
      var stijlen = [];
      document.querySelectorAll("#stijl-grid input:checked").forEach(function (i) { stijlen.push(i.value); });
      uit.append("stijlen", stijlen.join(","));
      uit.append("voorbeeld", waarde("s2-voorbeeld"));
      uit.append("beschrijving", waarde("s2-beschrijving"));
      uit.append("start", waarde("s2-start"));
      if (/testwebsite/i.test(diensten)) {
        var totaal = 0;
        ["f-logo", "f-fotos"].forEach(function (id) {
          var inp = document.getElementById(id);
          if (!inp || !inp.files) return;
          for (var i = 0; i < inp.files.length && i < 9; i++) {
            var f = inp.files[i];
            if (totaal + f.size > MAX_TOTAAL) break;
            totaal += f.size;
            uit.append(id === "f-logo" ? "logo" : "foto", f, f.name);
          }
        });
      }
      gestuurd = true;
      try { fetch(URL, { method: "POST", body: uit }).catch(function () {}); } catch (_) {}
    }, 0);
  }, true);
})();
