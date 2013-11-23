<%page args="entry" />
<item>
    <title>${entry.title}</title>
    <link>${entry.url}</link>
    <description>${entry.description}</description>
    <pubDate>${entry.publishedDate}</pubDate>
    <guid>${entry.url}</guid>
    % if entry.thumbnailUrl:
        ${entry.createThumbnailMediaTag() | n}
    % endif
</item>
