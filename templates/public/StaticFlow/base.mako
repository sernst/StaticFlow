<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />

    % if mr.pageData.rssGenerator:
        <link rel="alternate"
              type="application/rss+xml"
              title="${mr.pageData.rssGenerator.title}"
              href="${mr.pageData.rssGenerator.homeUrl}"
        />
    % endif

    <title>${mr.pageData.get('title') | n}</title>
    <meta name="description" content="${mr.pageData.get('description') | n}" />
    <script>
        window.PAGE=${mr.pageVars | n};
    </script>
    <script src="${mr.loader}" async></script>
</head>

<body>
${next.body() | n}
</body>
</html>
