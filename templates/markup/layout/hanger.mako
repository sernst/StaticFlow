## vml/hanger.mako
## (C)2012
## Scott Ernst

% if mr.data.render['hangerActive']:
    <div ${mr.data.write('resizer') | n}></div>
% endif
<div ${mr.data.write() | n}>
    % if mr.data.themeChanged:
        <div ${mr.data.write('styled') | n}>
    % endif
        <%block name="tagBodyBlock">${mr.data.content | n}</%block>
    % if mr.data.themeChanged:
        </div>
    % endif
</div>
