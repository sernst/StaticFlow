## paragraphBase.mako
## (C)2013
## Scott Ernst
<p ${mr.data.write() | n}> \
    <%block name="tagBodyBlock">${mr.data.content | n}</%block> \
</p>
