<!DOCTYPE html>
<html>
<head>
    <title>${mr.page.title}</title>
    <meta property="og:title" content="${mr.page.title}" />
    <meta HTTP-EQUIV="REFRESH" content="0; url=${mr.page.get('REDIRECT_URL') | n}" />
</head>

<body>
    <div style="text-align:center;">
        Redirecting to: <a href="${mr.page.get('REDIRECT_URL') | n}">${mr.page.get('REDIRECT_URL') | n}</a>
    </div>
</body>
</html>
