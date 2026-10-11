/* Cinematic Frontends - motion engine + dark Plotly helpers.
   Include after Plotly. Call Cine.init() once on load.
   Markup hooks:
     .reveal                      -> fade/rise in on scroll
     data-countup="290.8"         -> count up when visible (data-prefix, data-suffix, data-decimals)
     data-parallax="0.12"         -> translateY on scroll
     #prog                        -> scroll progress bar (optional element)
   Charts: Cine.layout(extra), Cine.config, Cine.whenVisible(id, fn). */
(function(){
  "use strict";
  var C={
    tokens:{acc:"#c6ff3a",acc2:"#5c78ff",ink:"#f5f7fa",mut:"#9aa0a8",bg:"#0f0f0f",grid:"rgba(255,255,255,0.06)"},
    config:{displayModeBar:false,responsive:true}
  };

  function ease(t){return 1-Math.pow(1-t,3);}

  C.layout=function(extra){
    var t=C.tokens;
    var base={
      paper_bgcolor:t.bg, plot_bgcolor:t.bg,
      font:{color:t.mut,family:"Inter, sans-serif",size:12},
      margin:{l:54,r:24,t:16,b:44},
      xaxis:{gridcolor:t.grid,zeroline:false,linecolor:t.grid,tickcolor:t.grid},
      yaxis:{gridcolor:t.grid,zeroline:false,linecolor:t.grid,tickcolor:t.grid},
      hoverlabel:{bgcolor:"#171717",bordercolor:t.grid,font:{color:t.ink}}
    };
    if(extra){for(var k in extra) base[k]=extra[k];}
    return base;
  };

  C.countUp=function(el){
    var to=parseFloat(el.getAttribute("data-countup"))||0,
        pre=el.getAttribute("data-prefix")||"",
        suf=el.getAttribute("data-suffix")||"",
        dec=parseInt(el.getAttribute("data-decimals")||"1",10),
        s=performance.now();
    (function go(n){var p=Math.min((n-s)/1700,1);
      el.textContent=pre+(to*ease(p)).toFixed(dec)+suf;
      if(p<1)requestAnimationFrame(go);})(s);
  };

  C.whenVisible=function(id,fn,threshold){
    var node=typeof id==="string"?document.getElementById(id):id;
    if(!node)return;
    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){fn(node);io.unobserve(e.target);}});
    },{threshold:threshold||0.25});
    io.observe(node);
  };

  C.init=function(){
    var prog=document.getElementById("prog");
    var px=[].slice.call(document.querySelectorAll("[data-parallax]"));
    function onScroll(){
      if(prog){var h=document.documentElement.scrollHeight-innerHeight;
        prog.style.width=(h>0?(scrollY/h*100):0)+"%";}
      px.forEach(function(el){
        var f=parseFloat(el.getAttribute("data-parallax"))||0.1;
        var r=el.getBoundingClientRect();
        el.style.transform="translateY("+((r.top-innerHeight/2)*f*-1)+"px)";
      });
    }
    addEventListener("scroll",onScroll,{passive:true}); onScroll();

    var io=new IntersectionObserver(function(es){
      es.forEach(function(e){if(e.isIntersecting){e.target.classList.add("in");io.unobserve(e.target);}});
    },{threshold:0.18});
    document.querySelectorAll(".reveal").forEach(function(el,i){
      if(!el.style.transitionDelay) el.style.transitionDelay=((i%4)*0.06)+"s";
      io.observe(el);
    });

    document.querySelectorAll("[data-countup]").forEach(function(el){
      C.whenVisible(el,function(n){C.countUp(n);},0.5);
    });

    addEventListener("resize",function(){
      if(typeof Plotly==="undefined")return;
      document.querySelectorAll(".plot").forEach(function(el){if(el.data)Plotly.Plots.resize(el);});
    });
  };

  window.Cine=C;
  if(document.readyState!=="loading") C.init();
  else document.addEventListener("DOMContentLoaded",C.init);
})();
