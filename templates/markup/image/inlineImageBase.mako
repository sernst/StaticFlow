## inlineImageBase.mako
## (C)2012-2013
## Scott Ernst

<%inherit file="/shared/vml/divBase.mako" />

<%block name="tagBodyBlock"><img ${mr.data.write('image') | n} /></%block>
