## subscript.mako
## (C)2012
## Scott Ernst
<${'span' if mr.data.themeChanged else 'sub'} ${mr.data.write() | n}> \
    ${ '<sub ' + mr.data.write('styled') + '>' if mr.data.themeChanged else '' | n} \
    <%block name="tagBodyBlock">${mr.data.content | n}</%block> \
    ${ '</sub>' if mr.data.themeChanged else '' | n} \
</${'span' if mr.data.themeChanged else 'sub'}>
