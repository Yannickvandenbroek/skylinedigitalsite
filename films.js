/* Films in het portfolio — gedeeld door de video-carousel (portfolio.html)
   en de losse videopagina (video.html?v=<slug>). Bestanden staan in assets/video/. */
window.SKYLINE_FILMS = [
  { slug: 'modern-villa-moraira',  t: 'Modern Villa Moraira',        plaats: 'Moraira, Spanje' },
  { slug: 'casa-pilar-javea',      t: 'Casa Pilar',                  plaats: 'Jávea, Spanje' },
  { slug: 'villa-in-moraira',      t: 'Villa in Moraira',            plaats: 'Moraira, Spanje' },
  { slug: 'villa-maillard',        t: 'Villa Maillard',              plaats: '' },
  { slug: 'luxe-villa-moraira',    t: 'Luxe vakantievilla',          plaats: 'Moraira, Spanje' },
  { slug: 'vakantiewoning-javea',  t: 'Vakantiewoning met zwembad',  plaats: 'Jávea, Spanje' },
  { slug: 'villa-zwembad-moraira', t: 'Villa met privézwembad',      plaats: 'Moraira, Spanje' },
  { slug: 'woning-rosmalen',       t: 'Woning in Rosmalen',          plaats: 'Rosmalen, Nederland' },
];

/* Vertaalde titels/plaatsen voor /en, /it, /es (taal komt uit <html lang>) */
(function () {
  const T = {
    en: { 'Villa in Moraira': 'Villa in Moraira', 'Luxe vakantievilla': 'Luxury holiday villa', 'Vakantiewoning met zwembad': 'Holiday home with pool',
          'Villa met privézwembad': 'Villa with private pool', 'Woning in Rosmalen': 'Home in Rosmalen', 'Spanje': 'Spain', 'Nederland': 'the Netherlands' },
    it: { 'Villa in Moraira': 'Villa a Moraira', 'Luxe vakantievilla': 'Villa vacanze di lusso', 'Vakantiewoning met zwembad': 'Casa vacanze con piscina',
          'Villa met privézwembad': 'Villa con piscina privata', 'Woning in Rosmalen': 'Casa a Rosmalen', 'Spanje': 'Spagna', 'Nederland': 'Paesi Bassi' },
    es: { 'Villa in Moraira': 'Villa en Moraira', 'Luxe vakantievilla': 'Villa vacacional de lujo', 'Vakantiewoning met zwembad': 'Casa vacacional con piscina',
          'Villa met privézwembad': 'Villa con piscina privada', 'Woning in Rosmalen': 'Vivienda en Rosmalen', 'Spanje': 'España', 'Nederland': 'Países Bajos' },
  }[(document.documentElement.lang || 'nl').slice(0, 2)];
  if (!T) return;
  window.SKYLINE_FILMS.forEach(f => {
    f.t = T[f.t] || f.t;
    f.plaats = f.plaats.replace(/[^,]+$/, m => ' ' + (T[m.trim()] || m.trim())).trim();
  });
})();
