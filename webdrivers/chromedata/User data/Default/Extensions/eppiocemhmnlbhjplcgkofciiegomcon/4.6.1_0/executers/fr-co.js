(()=>{var t,e=null!==(t=sessionStorage.getItem("bis_data"))?JSON.parse(t):null,i=document.querySelector("script[bis_id]");window.bisData={id:i?i.getAttribute("bis_id")+"_w":null,html5TargetUrlDetectionConfig:e?e.config.html5TargetUrlDetectionConfig:null};var n=window.bisData.html5TargetUrlDetectionConfig,o=window.bisData.id;function a(){return(Math.random().toString(36).substring(2,15)+Math.random().toString(36).substring(2,15)+Math.random().toString(36).substring(2,15)).substring(0,22)}window.addEventListener("message",(function(t){try{var e=o,i=t.data;if(function(t){return void 0!==t&&void 0!==t.posdMessageId&&void 0!==t.from&&void 0!==t.to&&void 0!==t.type&&void 0!==t.content&&"PANELOS_MESSAGE"===t.posdMessageId}(i)&&i.to===e)if("GET_WINDOW_TARGET_URL"===i.type){var r=GetWindowEmbeddedTargetUrlDataList(e,window,n);if(r.length){var s={posdMessageId:"PANELOS_MESSAGE",posdHash:a(),type:"GET_WINDOW_TARGET_URL_RESPOND",from:e,to:e.substring(0,e.length-2),content:r};document.body&&document.body.setAttribute&&document.body.setAttribute("bis_mes_to_fr",JSON.stringify(s)),t.source.postMessage&&t.source.postMessage(s,t.origin)}}else if("GET_WINDOW_CLICK_TARGET_URL"===i.type){if(window.bisData.clickTargetUrlProcessed)return;if(function(){if(window.bisData){var t=window.bisData.html5TargetUrlDetectionConfig.TARGET_URL_CLICK_ELEMENTS_SELECTOR,e=document.querySelectorAll(t);if(e.length){window.bisData.origWindowOpen=window.open,window.bisData.elementSquare=0,window.bisData.clickTargetUrl=[],window.bisData.clickTargetUrlProcessed=!1;var i=function(t,e,i){return window.bisData.clickTargetUrl.push({href:t,square:window.bisData.elementSquare}),null};window.open=i;for(var n=0;n<e.length&&0===window.bisData.clickTargetUrl.length;n++)try{if(e[n]&&e[n].click&&e[n].getBoundingClientRect){var o=e[n].getBoundingClientRect();o.width>40&&o.height>40&&(window.bisData.elementSquare=o.width*o.height,window.open==i&&e[n].click())}}catch(t){}setTimeout((function(){window.open=window.bisData.origWindowOpen}),1e3),window.bisData.clickTargetUrlProcessed=!0}}}(),window.bisData&&window.bisData.clickTargetUrl&&window.bisData.clickTargetUrl.length){var d={posdMessageId:"PANELOS_MESSAGE",posdHash:a(),type:"GET_WINDOW_CLICK_TARGET_URL_RESPOND",from:e,to:e.substring(0,e.length-2),content:{chainId:i.content.chainId,clickTargetUrl:window.bisData.clickTargetUrl}};document.body&&document.body.setAttribute&&document.body.setAttribute("bis_mes_to_fr",JSON.stringify(d)),t.source.postMessage&&t.source.postMessage(d,t.origin)}}}catch(t){}}),!1)})();