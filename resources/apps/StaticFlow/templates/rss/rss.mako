<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>${mr.rss.title}</title>
    <link>${mr.rss.homeUrl}</link>
    <description>${mr.rss.description}</description>
    <language>en-us</language>
    <pubDate>${mr.rss.lastModifiedTimestamp}</pubDate>
    <lastBuildDate>${mr.rss.compiledTimestamp}</lastBuildDate>
    <image>
        <url>${mr.rss.thumbnail}</url>
        <title>${mr.rss.title}</title>
        <link>${mr.rss.homeUrl}</link>
    </image>
    <atom:link href="${mr.rss.rssUrl}" rel="self" type="application/rss+xml" />

    % for entry in mr.rss.entries:
        <%include file="rssEntry.mako" args="entry=entry" />
    % endfor
</channel>
</rss>
