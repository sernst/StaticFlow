## text.mako
## (C)2014
## Scott Ernst
<span ${mr.data.write() | n}> \
    <%block name="textInsert">${mr.data.render['text'] if 'text' in mr.data.render else u''}</%block> \
</span>
