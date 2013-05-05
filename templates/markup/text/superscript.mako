## superscript.mako
## (C)2012
## Scott Ernst
<${'span' if mr.data.themeChanged else 'sup'} ${mr.data.write() | n}>${ '<sup ' + mr.data.write('styled') + '>' if mr.data.themeChanged else '' | n}<%block name="tagBodyBlock">${mr.data.content | n}</%block>${ '</sup>' if mr.data.themeChanged else '' | n}</${'span' if mr.data.themeChanged else 'sup'}>
