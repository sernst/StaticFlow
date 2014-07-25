## font.mako
## (C)2014
## Scott Ernst
<%inherit file="../spanBase.mako"></%inherit>
<%block name="tagBodyBlock">
    <%block name="textInsert">${mr.data.render['text'] if 'text' in mr.data.render else u''}</%block> \
    <%block name="content">${mr.data.content | n}</%block> \
</%block>
