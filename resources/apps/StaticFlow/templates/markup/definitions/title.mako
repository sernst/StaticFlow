<h${mr.data.render['level'] | n} ${mr.data.write() | n}> \
    <%block name="textInsert">${mr.data.render['text'] if 'text' in mr.data.render else u''}</%block> \
    <%block name="tagBodyBlock">${mr.data.content | n}</%block> \
</h${mr.data.render['level'] | n}>
