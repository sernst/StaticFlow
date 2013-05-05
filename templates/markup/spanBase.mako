## spanBase.mako
## (C)2012
## Scott Ernst
<span ${mr.data.write() | n}>${ '<span ' + mr.data.write('styled') + '>' if mr.data.themeChanged else '' | n}<%block name="tagBodyBlock">${mr.data.content | n}</%block>${ '</span>' if mr.data.themeChanged else '' | n}</span>
