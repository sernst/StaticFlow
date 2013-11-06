## imageBase.mako
## (C)2012-2013
## Scott Ernst

<%inherit file="../divBase.mako" />

<%block name="tagBodyBlock"><div ${mr.data.write('imageBox') | n}><img ${mr.data.write('image') | n} /></div></%block>
