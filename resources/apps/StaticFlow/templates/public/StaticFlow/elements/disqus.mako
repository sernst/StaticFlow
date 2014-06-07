% if mr.page.get(('DISQUS', 'SHORT_NAME')):
<div id="disqus_thread"
    data-discus-shortname="${mr.page.get(('DISQUS', 'SHORT_NAME'))}"
    data-discus-url="${mr.page.targetUrl}"
    data-discus-id="'${mr.page.get(('DISQUS', 'UID'), mr.page.get('UID', mr.page.targetUrl))}'"
    data-discus-local=${1 if mr.site.isLocal else 0}></div>
% endif
