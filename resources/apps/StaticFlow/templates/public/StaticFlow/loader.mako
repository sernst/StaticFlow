<%inherit file="base.mako" />

<%block name="bottomHead">
<style>
    @keyframes loaderBye {
        from {opacity: 1.0;} to {opacity: 0.0;} }
    @-webkit-keyframes loaderBye {
        from {opacity: 1.0;} to {opacity: 0.0;} }
    #loadBox { position:absolute; left:0; top:0; width:100%; height:100%; background-color:#FFFFFF;
        opacity:1.0; animation:loaderBy 5s, -webkit-animation:loaderBye 5s; }
</style>
</%block>

<div id="loadBox"> </div>

<div id="mainContainer">
    <div id="content">${next.body() | n}</div>
</div>

<script>
    function __sfLoad__() {
        document.getElementById('loadBox').style.height = window.innerHeight;
    }
    __sfLoad__();
</script>
