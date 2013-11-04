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
    <meta property="og:title" content="${mr.pageProcessor.siteData.get('TITLE')}" />
    <meta property="og:url" content="${mr.pageData.targetUrl}" />
    <meta property="og:image" content="${mr.pageProcessor.cdnRootUrl + mr.pageData.get('THUMBNAIL')}" />
    <meta name="description" content="${mr.pageData.get('description') | n}" />
    <script>
        window.PAGE=${mr.pageVars | n};
    </script>
    <script src="${mr.loader}" async></script>

% if mr.pageData.get(('GOOGLE', 'TRACKING_ID')):
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', '${mr.pageData.get(('GOOGLE', 'TRACKING_ID'))}', '${mr.pageData.get(('GOOGLE', 'TRACKING_DOMAIN'), mr.pageData.get('DOMAIN'))}');
  ga('send', 'pageview');
</script>
% endif
    ${mr.pageData.cssTags | n}
</head>

<body>
${next.body() | n}
</body>
</html>
