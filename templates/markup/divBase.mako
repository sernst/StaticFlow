<%block name="tagPreBlock"></%block> \
<div ${mr.data.write() | n}>
% if mr.data.themeChanged:
<div ${mr.data.write('styled') | n}> \
% endif
<%block name="tagBodyBlock">${mr.data.content | n}</%block> \
% if mr.data.themeChanged:
</div> \
% endif
</div> \
<%block name="tagPostBlock"></%block>