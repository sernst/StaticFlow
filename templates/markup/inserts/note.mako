## note.mako
## (C)2012
## Scott Ernst

<%inherit file="/shared/vml/divBase.mako" />

<%block name="tagBodyBlock">
    <div class="markupNoteBody">${mr.data.content | n}</div>
</%block>
