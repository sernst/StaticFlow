(function(){var sflow;if(!Function.prototype.bind){Function.prototype.bind=function(oThis){var aArgs,fBound,fNOP,fToBind;aArgs=Array.prototype.slice.call(arguments,1);fToBind=this;fNOP=function(){};fBound=function(){return fToBind.apply(this instanceof fNOP&&oThis?this:oThis,aArgs.concat(Array.prototype.slice.call(arguments)))};fNOP.prototype=this.prototype;fBound.prototype=new fNOP;return fBound}}sflow={mod:{},r:{},_events:{},_eventCBs:{},CREATED:false};window.SFLOW=sflow;sflow.addEventListener=function(id,cb,d){var e,sf,x,_i,_len,_ref,_ref1;sf=window.SFLOW;if(sf._events[id]){cb(sf._events[id],d);return}e=sf._eventCBs;if((_ref=e[id])==null){e[id]=[]}_ref1=e[id];for(_i=0,_len=_ref1.length;_i<_len;_i++){x=_ref1[_i];if(x.cb===cb){return}}e[id].push({cb:cb,data:d})};sflow.removeEventListener=function(id,cb){var e,i,x,_i,_len,_ref;e=window.SFLOW._eventCBs;if(!e[id]){return}i=0;_ref=e[id];for(_i=0,_len=_ref.length;_i<_len;_i++){x=_ref[_i];if(x.cb===cb){e[id].splice(i,1);return}i++}};sflow.dispatchEvent=function(e){var cb,err,id,sf,x,_i,_len,_ref;sf=window.SFLOW;try{id=e.id}catch(_error){err=_error;id=e;e={id:e}}if(e.oneShot){sf._events[id]=e}cb=sf._eventCBs;if(!cb[id]){return false}_ref=cb[id];for(_i=0,_len=_ref.length;_i<_len;_i++){x=_ref[_i];x.cb(e,x.data)}return true};sflow.populateDom=function(dom){$(dom).each(function(i,e){var id;e=$(e);id=e.attr("id");return $("#"+id).replaceWith(e)});return SFLOW.refresh()};window.onhashchange=function(){return SFLOW.dispatchEvent({id:"PAGE:hashChange",data:location.hash})};window.onload=function(){var callback,complete,count,css,cssItem,delta,doc,dyn,head,link,loadItems,lt,pUrl,progress,scripts,_i,_len;doc=document;head=doc.getElementsByTagName("head")[0];progress=[1,1];scripts=PAGE.SCRIPTS;delta=89/scripts.length;css=PAGE.CSS;dyn=PAGE.HTML;count=scripts.length;complete=function(){new SFLOW["class"];SFLOW.loadComplete()};callback=function(){SFLOW.dispatchEvent({id:"SCRIPT:loaded:"+this.i[0],data:this,oneShot:true});if(!this.t){return}progress[0]+=delta;progress[1]=Math.max(progress[0],progress[1]);if(this.t){count--;if(count<=0){complete()}}};loadItems=function(items,sync){var item,script,_i,_len;for(_i=0,_len=items.length;_i<_len;_i++){item=items[_i];script=doc.createElement("script");script.charset="utf-8";script.type="text/javascript";script.id=item[0];script.src=item[1];script.onload=callback.bind({s:script,i:item,t:sync});head.appendChild(script)}};lt=setInterval(function(){var t;t=document.getElementById("loadProgress");if(!t){clearInterval(lt);lt=null;return}progress[1]++;t.style.width=Math.min(100,progress[1])+"%"},125);if(css&&css.length>0){for(_i=0,_len=css.length;_i<_len;_i++){cssItem=css[_i];link=doc.createElement("link");link.rel="stylesheet";link.type="text/css";link.id=cssItem[0];link.href=cssItem[1];head.appendChild(link)}}pUrl=function(u,e,p,os){var pm,r;r=new XMLHttpRequest;r.onreadystatechange=function(){if(r.readyState===4&&r.status===200){SFLOW.dispatchEvent({id:e,data:r.responseText,oneShot:os})}};pm=p?"POST":"GET";r.open(pm,u,true);if(p){r.setRequestHeader("Content-type","application/x-www-form-urlencoded; charset=UTF-8");r.send(p)}else{r.send()}};SFLOW.get=pUrl;if(dyn){pUrl(dyn,"DOM:dynamic",null,true)}if(scripts.length===0){complete()}else{loadItems(scripts,true)}}}).call(this);