<!DOCTYPE html>
<html>
<head>
    <title>${mr.pageData.get('title') | n}</title>
    <meta property="og:title" content="${mr.pageData.get('title') | n}" />
    <meta HTTP-EQUIV="REFRESH" content="0; url=${mr.pageData.get('REDIRECT_URL') | n}" />
</head>

<body>
    <div style="text-align:center;">
        Redirecting to: <a href="${mr.pageData.get('REDIRECT_URL') | n}">${mr.pageData.get('REDIRECT_URL') | n}</a>
    </div>
</body>
</html>
