% if mr.page.get(('DISQUS', 'SHORT_NAME')):
<div id="disqus_thread"></div>
<script type="text/javascript">
    var disqus_shortname = '${mr.page.get(('DISQUS', 'SHORT_NAME'))}';
    var disqus_url = '${mr.page.targetUrl}';

    ## Retrieves the DISQUS->UID if one exists or the UID for the page if it does not. If for some
    ## reason there is no UID for the page, the fallback is the URL, as suggested by Disqus.
    var disqus_identifier = '${mr.page.get(('DISQUS', 'UID'), mr.page.get('UID', mr.page.targetUrl))}';

    ## Enables developer mode on local deployments to prevent errors when testing locally
    % if mr.site.isLocal:
        var disqus_developer = 1;
    % endif

    (function() {
        var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
        dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
        (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
    })();
</script>
% endif
