<%inherit file="base.mako" />

<%block name="bottomHead">
<style>
    @keyframes loaderBye {
        from {opacity: 1.0;}
        to {opacity: 0.0;}
}
@-webkit-keyframes loaderBye {
    from {opacity: 1.0;}
    to {opacity: 0.0;}
}
#loadBox { animation:loaderBy 2s; -webkit-animation: loaderBye 1s;
    position:absolute;left:0;top:0;width:100%;height:100%;background-color:#FFFFFF;}
</style>
</%block>

<div id="loadBox"> </div>

<div id="mainContainer">
    <div id="content">${next.body() | n}</div>
</div>

<script>
    function __sfLoad__() {
        document.getElementById('loadBox').height(window.innerHeight);
    }
    __sfLoad__();
</script>
