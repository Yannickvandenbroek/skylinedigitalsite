// Instagram-feed voor de site (Vercel serverless function: /api/instagram).
// Haalt de JSON-feed van Behold op (feed "skylinedigital.nl website") en geeft alleen de velden door die de site nodig heeft.
// De CDN bewaart het antwoord een half uur: snel voor bezoekers en ruim binnen het Behold-weergavelimiet.
const FEED = "https://feeds.behold.so/1ncHhVzmGmSf3deGLmFC";

module.exports = async (req, res) => {
  try {
    const r = await fetch(FEED, { headers: { Accept: "application/json" } });
    if (!r.ok) return res.status(502).json({ error: "feed_" + r.status });
    const d = await r.json();
    res.setHeader("Cache-Control", "public, s-maxage=1800, stale-while-revalidate=86400");
    res.status(200).json({
      username: d.username,
      followers: d.followersCount,
      avatar: d.profilePictureUrl,
      posts: (d.posts || []).filter((p) => p.visibility !== "hidden").slice(0, 12).map((p) => ({
        url: p.permalink,
        type: p.mediaType,
        image: (p.sizes && p.sizes.medium && p.sizes.medium.mediaUrl) || p.thumbnailUrl || p.mediaUrl,
        caption: p.prunedCaption || "",
        alt: p.altText || "",
      })),
    });
  } catch (e) {
    res.status(502).json({ error: "fetch_failed" });
  }
};
