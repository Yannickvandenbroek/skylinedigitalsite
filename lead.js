/* Aanvragen ook naar het CRM (crm.skylinedigital.nl), naast de mail via Formspree.
   Luistert mee op elk formulier dat naar Formspree gaat, leest dezelfde velden en stuurt ze
   als JSON naar de edge function website-lead. Faalt dit stilletjes, dan merkt de bezoeker
   niets: de mail via Formspree blijft de leidende weg. */
(function () {
  var URL = "https://qccuhmznrlgobfccxiro.supabase.co/functions/v1/website-lead";
  var gestuurd = false;
  function veld(fd, namen) {
    for (var i = 0; i < namen.length; i++) { var v = fd.get(namen[i]); if (v && String(v).trim()) return String(v).trim(); }
    return "";
  }
  document.addEventListener("submit", function (e) {
    var form = e.target;
    if (!form || !/formspree\.io/.test(form.action || "") || gestuurd) return;
    // Na de eigen afhandeling van de pagina lezen, zodat verborgen velden (diensten, details) al gevuld zijn.
    setTimeout(function () {
      var fd = new FormData(form);
      var email = veld(fd, ["E-mail", "Email", "email"]);
      if (!/\S+@\S+\.\S+/.test(email)) return;
      var naam = veld(fd, ["Naam", "naam"]);
      var payload = {
        voornaam: veld(fd, ["Voornaam"]) || naam.split(" ")[0] || "",
        achternaam: veld(fd, ["Achternaam"]) || naam.split(" ").slice(1).join(" "),
        bedrijf: veld(fd, ["Bedrijf"]),
        email: email,
        telefoon: veld(fd, ["Telefoon", "telefoon"]),
        diensten: veld(fd, ["Geselecteerde diensten"]),
        details: veld(fd, ["Projectdetails", "Bericht", "message"]),
        pagina: location.pathname,
        taal: (document.documentElement.lang || "nl").slice(0, 2),
        website_url_check: veld(fd, ["website_url_check"])
      };
      gestuurd = true;
      try {
        fetch(URL, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload), keepalive: true }).catch(function () {});
      } catch (_) {}
    }, 0);
  }, true);
})();
