## zurbChunk.mako
## (C)2013
## Scott Ernst

<%inherit file="../divBase.mako" />
<%block name="tagBodyBlock"><div ${mr.data.write('column') | n}>${mr.data.content | n}</div></%block>
