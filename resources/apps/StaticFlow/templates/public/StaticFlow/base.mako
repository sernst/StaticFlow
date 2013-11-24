<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />

    % if mr.page.rssLinkSource:
        <link rel="alternate"
              type="application/rss+xml"
              title="${mr.page.rssLinkSource.title}"
              href="${mr.page.rssLinkSource.rssUrl}"
        />
    % endif

    <title>${mr.page.title}</title>
    <meta name="description" content="${mr.page.description | n}" />
    <meta property="og:title" content="${mr.page.title}" />
    <meta property="og:url" content="${mr.page.targetUrl}" />
    <meta property="og:image" content="${mr.page.thumbnail.getUrl(forceHttp=True)}" />
    <meta property="og:description" content="${mr.page.description}"/>
    <meta property="og:site_name" content="${mr.site.get('TITLE')}"/>
    <meta property="og:type" content="${mr.page.get('TYPE', 'website')}"/>

    <meta name="twitter:card" content="summary">
    <meta name="twitter:url" content="${mr.page.targetUrl}">
    <meta name="twitter:title" content="${mr.page.title}">
    <meta name="twitter:description" content="${mr.page.description}">

    <link rel="canonical" href="${mr.page.targetUrl}"/>
    % if mr.page.author.gplusAuthorUrl:
        <link rel="author" href="${mr.page.author.gplusAuthorUrl}"/>
    % endif

    <script>
        window.PAGE=${mr.pageVars | n};
    </script>
    <script src="${mr.loader}" async></script>

% if mr.page.get(('GOOGLE', 'TRACKING_ID')):
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
  ga('create', '${mr.page.get(('GOOGLE', 'TRACKING_ID'))}', '${mr.page.get(('GOOGLE', 'TRACKING_DOMAIN'), mr.page.get('DOMAIN'))}');
  ga('send', 'pageview');
</script>
% endif
    ${mr.page.cssTags | n}
</head>

<body>
<div id="sf_wrapper">
${next.body() | n}
<div id="sf_footer_push"></div>
</div>
<div id="sf_footer" style="display:none;">${mr.page.footerDom | n}</div>
</body>
</html>
