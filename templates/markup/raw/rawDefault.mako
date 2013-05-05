## rawDefault.mako
## (C)2012
## Scott Ernst

<%inherit file="/shared/vml/divBase.mako" />

<%block name="tagBodyBlock"> \
    % if mr.data.render.get('title'):
        <div ${mr.data.write('title') | n}>${mr.data.render['title']}</div> \
    % endif
<pre class="rawBody">${mr.data.content | h}</pre></%block>
