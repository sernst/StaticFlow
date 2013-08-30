## soundCloud.mako
## (C)2012
## Eric D. Wills and Scott Ernst

<%inherit file="../divBase.mako" />

<%block name="tagBodyBlock">
    <iframe ${mr.data.write('player') | n}
            src="http://w.soundcloud.com/player/?url=http%3A%2F%2Fapi.soundcloud.com%2F${mr.data.render['type'] | n}%2F${mr.data.render['code'] | n}&auto_play=${mr.data.render['autoplay']}&show_artwork=${mr.data.render['artwork']}&show_comments=${mr.data.render['comments']}&color=${mr.data.render['color'] | n}"
            frameborder='0' allowCrossDomainXHR='allowCrossDomainXHR'
            sandboxRoot='http://w.soundcloud.com/player/' documentRoot='app:/'>
    </iframe>
</%block>
