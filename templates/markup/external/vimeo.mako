## vimeo.mako
## (C)2012
## Eric D. Wills and Scott Ernst

<%inherit file="/shared/vml/divBase.mako" />

<%block name="tagBodyBlock">
    <iframe ${mr.data.write('player') | n}
            src="http://player.vimeo.com/video/${mr.data.render['code'] | n}?autoplay=${mr.data.render['autoplay']}&color=${mr.data.render['color'] | n}"
            frameborder='0' allowCrossDomainXHR='allowCrossDomainXHR'
            sandboxRoot='http://player.vimeo.com/video/' documentRoot='app:/'>
    </iframe>
</%block>
