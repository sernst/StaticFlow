## youTube.mako
## (C)2012-2013
## Scott Ernst

<%inherit file="../divBase.mako" />

<%block name="tagBodyBlock">
    % if mr.data.render['shrink']:
        <div ${mr.data.write('shrinker') | n}>
    % endif
    <iframe ${mr.data.write('player') | n}
            src="//www.youtube.com/embed/${mr.data.render['code'] | n}?autoplay=${mr.data.render['autoplay']}&autohide=${mr.data.render['autohide'] | n}${mr.data.render['start'] | n}"
            frameborder='0' allowCrossDomainXHR='allowCrossDomainXHR'
            sandboxRoot='//www.youtube.com/embed/' documentRoot='app:/'>
    </iframe>
    % if mr.data.render['shrink']:
        </div>
    % endif
</%block>
