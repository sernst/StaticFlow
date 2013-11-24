## listBase.mako
## (C)2012
## Scott Ernst

<%inherit file="../divBase.mako" />

<%block name="tagBodyBlock">
    <${mr.data.render['listTag'] | n} ${mr.data.write('list') | n}>${mr.data.content | n}</${mr.data.render['listTag'] | n}>
</%block>
