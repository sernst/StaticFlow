## hulu.mako
## (C)2012
## Eric D. Wills and Scott Ernst

<%inherit file="/shared/vml/divBase.mako" />

<%block name="tagBodyBlock">
    <div ${mr.data.write('player') | n}>
    % if mr.data.render['isSecure']:
        <table style="width:100%;height:100%;background-color:black;color:#CCC;">
            <tr style="text-align:center;vertical-align:middle;"><td>
                Hulu does not offer secure content embedding at this time.
            </td></tr>
        </table>
    % else:
        <object style="width:100%;height:100%">
            <param name="movie" value="http://www.hulu.com/embed/${mr.data.render['code'] | n}" />
            <param name="allowFullScreen" value="true" />
            <embed src="http://www.hulu.com/embed/${mr.data.render['code'] | n}" type="application/x-shockwave-flash"  allowFullScreen="true" />
        </object>
    % endif
    </div>
</%block>
