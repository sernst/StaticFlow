<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
% for entry in mr.sitemap.entries:
    <url>
        <loc>${entry.url | n}</loc>
        <lastmod>${entry.lastModifiedTimestamp | n}</lastmod>
        <changefreq>${entry.changeFrequency | n}</changefreq>
        <priority>${entry.priority}</priority>
    </url>
% endfor
</urlset>
