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
      posts: (d.posts || []).filter((p) => p.visibility !== "hidden").slice(0, 12).map((p) => {
        const sq = p.sizes && p.sizes.large && p.sizes.large.mediaUrl;
        // Staand origineel (Instagram-CDN, verloopt na enkele dagen; wij verversen elk halfuur) met vierkant van Behold als reserve
        const first = p.mediaType === "CAROUSEL_ALBUM" && p.children && p.children[0];
        const portrait = p.mediaType === "VIDEO" ? p.thumbnailUrl : (first ? first.mediaUrl : p.mediaUrl);
        return {
          url: p.permalink,
          type: p.mediaType,
          image: portrait || sq,
          square: sq || portrait,
          video: p.mediaType === "VIDEO" ? p.mediaUrl : null,
          caption: p.prunedCaption || "",
          alt: p.altText || "",
          slides: p.children ? p.children.length : 0,
        };
      }),
    });
  } catch (e) {
    res.status(502).json({ error: "fetch_failed" });
  }
};
