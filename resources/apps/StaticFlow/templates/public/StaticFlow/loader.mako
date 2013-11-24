<%inherit file="base.mako" />

<div id="loadBox" style="text-align:center;margin:100px auto;width:50%;min-width:300px;max-width:500px;color:#666;">
    <div style="font-size:1.6em;">L O A D I N G</div>
    <div style="padding:2px;margin-top:10px;background-color:#EEE;border:2px solid #666;">
        <div id="loadProgress" style="background-color:#666;width:1%;height:0.5em;"></div>
    </div>
    <div style="margin-top:10px;font-size:1.1em;">${mr.page.description}</div>
</div>

<div id="mainContainer" style="display:none">
    <div id="content">${next.body() | n}</div>
</div>
