(function(){'use strict';var opt=window.ltgG3SliderOpt;if(!opt||'undefined'===typeof window.Swiper){return;}
var sliderEl=document.querySelector(opt.selector);if(!sliderEl){return;}
var swiper=new window.Swiper(sliderEl,opt.params);if(opt.instance){window[opt.instance]=swiper;}
if(!swiper.autoplay){return;}
if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){swiper.autoplay.stop();}
var toggle=sliderEl.querySelector('.ltg-slide-autoplay-toggle');if(!toggle){return;}
var stopSet=toggle.querySelector('.ltg-slide-autoplay-toggle-stop');var startSet=toggle.querySelector('.ltg-slide-autoplay-toggle-start');if(!stopSet||!startSet){return;}
function syncToggle(isPlaying){stopSet.hidden=!isPlaying;startSet.hidden=isPlaying;}
syncToggle(!!swiper.autoplay.running);swiper.on('autoplayStart',function(){syncToggle(true);});swiper.on('autoplayStop',function(){syncToggle(false);});toggle.addEventListener('click',function(event){event.preventDefault();event.stopPropagation();if(swiper.autoplay.running){swiper.autoplay.stop();}else{swiper.autoplay.start();}});toggle.hidden=false;})();