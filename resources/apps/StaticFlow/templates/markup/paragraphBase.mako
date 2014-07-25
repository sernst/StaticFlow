## paragraphBase.mako
## (C)2013-2014
## Scott Ernst
<p ${mr.data.write() | n}> \
    <%block name="textInsert">${mr.data.render['text'] if 'text' in mr.data.render else u''}</%block> \
    <%block name="tagBodyBlock">${mr.data.content | n}</%block> \
</p>
