(function(){var SFlowApi,_base,_ref;SFlowApi=function(){function SFlowApi(){var sf;sf=SFLOW;this._sf=sf;this.addEventListener=sf.addEventListener;this.removeEventListener=sf.removeEventListener;this.dispatchEvent=sf.dispatchEvent;this._events=sf._events;this._eventCBs=sf._eventCBs;this.CREATED=true;this.INIT=false;this.READY=false;this.SCRIPTS=false;this.mod=sf.mod;this.r=sf.r;window.SFLOW=this;return}SFlowApi.prototype.loadComplete=function(){var sf;sf=SFLOW;$("#mainContainer").show();$("#sf_footer").show();$("#loadBox").remove();sf.SCRIPTS=true;sf.dispatchEvent({id:"SCRIPT:complete",oneShot:true});if(PAGE.ASYNC.length){loadItems(PAGE.ASYNC)}if(PAGE.HTML){sf.addEventListener("DOM:dynamic",function(event){return sf.populateDom(event.data)})}sf.dispatchEvent({id:"DOM:complete",oneShot:true});$(document).foundation();$(window).resize(function(){SFLOW.dispatchEvent({id:"DOM:resize",data:$("body")});return SFLOW.resize()});sf.dispatchEvent({id:"LOAD:complete",oneShot:true});sf.refresh();if(location.hash.length>1){sf.dispatchEvent({id:"PAGE:hashChange",data:location.hash})}};SFlowApi.prototype.resize=function(dom){dom=dom?$(dom):$("body");SFLOW.dispatchEvent({id:"DOM:resize",data:dom});return $(".sfml-aspect").each(function(index,element){var aspect,e;e=$(element);aspect=e.data("aspect");return e.height(Math.floor(e.width()/aspect))})};SFlowApi.prototype.refresh=function(dom){var footerHeight;dom=dom?$(dom):$("body");dom.find(".columns").resize();dom.find('img[data-src!=""]').each(function(index,element){var e,src;e=$(element);src=e.attr("data-src");if(src&&src.length>0&&src.substr(1,1)!=="/"){src=PAGE.CDN_URL+src}e.attr("data-src",null);return e.attr("src",src)});footerHeight=$("#sf_footer").height();$("#sf_footer_push").height(footerHeight);$("#sf_wrapper").css("margin-bottom",footerHeight+"px");SFLOW.resize(dom)};return SFlowApi}();if((_ref=(_base=SFLOW.r).SFlowApi)==null){_base.SFlowApi=SFlowApi}window.SFLOW["class"]=SFLOW.r.SFlowApi}).call(this);