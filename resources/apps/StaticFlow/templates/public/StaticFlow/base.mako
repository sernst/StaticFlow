<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />

    % if mr.pageData.rssGenerator:
        <link rel="alternate"
              type="application/rss+xml"
              title="${mr.pageData.rssGenerator.title}"
              href="${mr.pageData.rssGenerator.rssUrl}"
        />
    % endif

    <title>${mr.pageData.title}</title>
    <meta name="description" content="${mr.pageData.description | n}" />
    <meta property="og:title" content="${mr.pageData.title}" />
    <meta property="og:url" content="${mr.pageData.targetUrl}" />
    <meta property="og:image" content="${mr.pageProcessor.getSiteUrl(mr.pageData.get('THUMBNAIL'), forceHttp=True)}" />
    <meta property="og:description" content="${mr.pageData.description}"/>
    <meta property="og:site_name" content="${mr.pageProcessor.siteData.get('TITLE')}"/>
    <meta property="og:type" content="${mr.pageData.get('TYPE', 'website')}"/>
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
<div id="sf_wrapper">
${next.body() | n}
<div id="sf_footer_push"></div>
</div>
<div id="sf_footer" style="display:none;">${mr.pageData.footerDom | n}</div>
</body>
</html>
