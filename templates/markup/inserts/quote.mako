## quote.mako
## (C)2012
## Scott Ernst

<%inherit file="/shared/vml/divBase.mako" />

<%block name="tagBodyBlock">
    <div ${mr.data.write('body') | n }>${mr.data.content | n}</div>
    % if mr.data.render['author']:
        <div ${mr.data.write('author') | n}>- ${mr.data.render['author']}</div>
    % endif
</%block>
