## twitter.mako
## (C)2012
## Scott Ernst

<script>VIZME.addEventListener('SCRIPT:loaded:twitter-widget', function(){new TWTR.Widget(${mr.data.render['twitterData'] | n}).render()${ mr.data.render['setUser'] | n}.start();});</script><div ${mr.data.write() | n}></div>
