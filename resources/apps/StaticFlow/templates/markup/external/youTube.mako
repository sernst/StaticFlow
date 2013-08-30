## youTube.mako
## (C)2012
## Scott Ernst

<%inherit file="../divBase.mako" />

<%block name="tagBodyBlock">
    <iframe ${mr.data.write('player') | n}
            src="${mr.data.render['protocol']}://www.youtube.com/embed/${mr.data.render['code'] | n}?autoplay=${mr.data.render['autoplay']}&autohide=${mr.data.render['autohide'] | n}${mr.data.render['start'] | n}"
            frameborder='0' allowCrossDomainXHR='allowCrossDomainXHR'
            sandboxRoot='${mr.data.render['protocol']}://www.youtube.com/embed/' documentRoot='app:/'>
    </iframe>
</%block>
