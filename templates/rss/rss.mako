<rss version="2.0">
    <channel>
        <title>${mr.rss.title}</title>
        <link>${mr.rss.homeUrl}</link>
        <description>${mr.rss.description}</description>
        <language>en-us</language>
        <pubDate>${mr.rss.lastModifiedTimestamp}</pubDate>
        <lastBuildDate>${mr.rss.compiledTimestamp}</lastBuildDate>
        % for entry in mr.rss.entries:
            <%include file="rssEntry.mako" args="entry=entry" />
        % endfor
    </channel>
</rss>
