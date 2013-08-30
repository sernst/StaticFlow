## soundCloud.mako
## (C)2012
## Eric D. Wills and Scott Ernst

<%inherit file="../divBase.mako" />

<%block name="tagBodyBlock">
    <iframe ${mr.data.write('player') | n}
            src="http://www.slideshare.net/slideshow/embed_code/${mr.data.render['code'] | n}?startSlide=${mr.data.render['start'] | n}"
            frameborder='0' allowCrossDomainXHR='allowCrossDomainXHR'
            sandboxRoot='http://www.slideshare.net/slideshow/embed_code/' documentRoot='app:/'>
    </iframe>
</%block>
