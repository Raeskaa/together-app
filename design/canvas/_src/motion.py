import re, sys
P='/Users/design/shared-planner/public/index.html'
s=open(P).read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a)
    if n!=cnt: print('COUNT',n,'expected',cnt,'::',a[:120]); sys.exit(1)
    s=s.replace(a,b)
def rex(pat,fn,cnt=1):
    global s
    m=list(re.finditer(pat,s))
    if len(m)!=cnt: print('REGEX',len(m),'expected',cnt,'::',pat[:100]); sys.exit(1)
    s=re.sub(pat,fn,s,count=cnt)

# ================= CSS =================
rep(":root{",":root{\n  --ease-out:cubic-bezier(.16,1,.3,1); --ease-move:cubic-bezier(.645,.045,.355,1); --ease-pop:cubic-bezier(.34,1.56,.64,1);",1)
# strike-through draws across instead of appearing
rep(".atitle.done{color:#AEB6C1;text-decoration:line-through}",".atitle.done{color:#AEB6C1}")
rep(".ititle.done{color:#AEB6C1;text-decoration:line-through}",".ititle.done{color:#AEB6C1}")
rex(r"\.subrow\.done \.slabel\{color:#AEB6C1;text-decoration:line-through\}", lambda m: ".subrow.done .slabel{color:#AEB6C1}")
rep(".btn:active{transform:scale(.985)}",".btn:active{transform:scale(.97)}")
rep(".pbar>i{display:block;height:100%;background:var(--accent);border-radius:999px}",".pbar>i{display:block;height:100%;background:var(--accent);border-radius:999px;transition:width .4s var(--ease-move)}")
rep(".pbar2 i{display:block;height:100%;background:var(--accent);border-radius:99px}",".pbar2 i{display:block;height:100%;background:var(--accent);border-radius:99px;transition:width .4s var(--ease-move)}")
rep(".ssr i{position:absolute;left:0;top:0;bottom:0;border-radius:99px}",".ssr i{position:absolute;left:0;top:0;bottom:0;border-radius:99px;transition:width .4s var(--ease-move)}")
rep(".pc-tlbar>i{display:block;height:100%;border-radius:999px;background:var(--accent)}",".pc-tlbar>i{display:block;height:100%;border-radius:999px;background:var(--accent);transition:width .4s var(--ease-move)}")
rep(".fill{position:absolute;left:0;height:8px;border-radius:99px;transition:width .5s cubic-bezier(.16,1,.3,1)}",".fill{position:absolute;left:0;height:8px;border-radius:99px;transition:width .6s var(--ease-move)}")
rep(".runner{position:absolute;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center}",".runner{position:absolute;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;transition:left .6s var(--ease-move)}")
motion_css = r"""
/* ---- motion: one set of curves and timings, reused everywhere ---- */
.stk{background:linear-gradient(currentColor,currentColor) no-repeat 0 58%/0 1.5px;-webkit-box-decoration-break:clone;box-decoration-break:clone;transition:background-size .22s var(--ease-out)}
.done .stk,.done.stk{background-size:100% 1.5px}
.check{transition:transform .12s var(--ease-out),background-color .15s,border-color .15s}
.view,.gbtn,.pillbtn,.navcirc,.stepbtn,.addinline,.mini,.morerow,.toast-act,.segc button,.pviews button,.kebab{transition:transform .12s var(--ease-out)}
.check:active,.view:active,.gbtn:active,.pillbtn:active,.navcirc:active,.stepbtn:active,.addinline:active,.mini:active,.morerow:active,.toast-act:active,.segc button:active,.pviews button:active,.kebab:active,.wavefab:active,.whorow:active,.nav:active{transform:scale(.97)}
@media (hover:hover) and (pointer:fine){ .lc2,.pc2,.whocard{transition:border-color .15s,box-shadow .15s,transform .15s var(--ease-out)} .lc2:hover,.pc2:hover{transform:translateY(-1px)} }
@keyframes fadein{from{opacity:0}}
@keyframes fadeout{to{opacity:0}}
@keyframes slideout{to{transform:translateX(34px);opacity:0}}
@keyframes popout{to{transform:scale(.98);opacity:0}}
@keyframes toastout{to{opacity:0;transform:translate(-50%,8px)}}
@keyframes slideup{from{transform:translateY(36px);opacity:0}}
@keyframes slidedown{to{transform:translateY(36px);opacity:0}}
.pov,.overlay{animation:fadein .2s var(--ease-out)}
.pov.closing,.overlay.closing{animation:fadeout .16s var(--ease-out) forwards;pointer-events:none}
.pov.closing .ppanel{animation:slideout .16s var(--ease-out) forwards}
.overlay.closing .modal,.overlay.closing .setmodal{animation:popout .14s var(--ease-out) forwards}
.toast.closing{animation:toastout .16s var(--ease-out) forwards}
@keyframes rowin{from{opacity:0;transform:translateY(6px)}}
.rowin{animation:rowin .2s var(--ease-out)}
.ptchip{position:fixed;z-index:93;pointer-events:none;font-weight:700;font-size:12.5px;color:#fff;background:var(--accent);border-radius:99px;padding:3px 9px;box-shadow:0 6px 16px rgba(31,111,235,.35);font-variant-numeric:tabular-nums;white-space:nowrap}
@keyframes crowndrop{0%{transform:translateY(-14px) rotate(-14deg);opacity:0}60%{transform:translateY(2px) rotate(5deg);opacity:1}100%{transform:none;opacity:1}}
.crownp.fresh svg{animation:crowndrop .6s var(--ease-pop)}
@keyframes leadglow{0%{box-shadow:0 0 0 0 rgba(180,121,43,.55)}100%{box-shadow:0 0 0 12px rgba(180,121,43,0)}}
.crownp.fresh{animation:leadglow 1.1s ease-out}
.flame{display:inline-flex;color:#C2704B;vertical-align:-1px;margin-right:4px}
@keyframes flamebump{0%{transform:scale(1)}40%{transform:scale(1.35)}100%{transform:scale(1)}}
.flame.bump{animation:flamebump .4s var(--ease-pop)}
@keyframes fpulse{0%{box-shadow:0 0 0 0 rgba(46,158,107,.45)}100%{box-shadow:0 0 0 14px rgba(46,158,107,0)}}
.focusw.done{border-color:#BFE3CF;animation:fpulse 1.4s ease-out 2}
.wpart{position:fixed;left:50%;top:56%;font-size:26px;pointer-events:none;z-index:91;opacity:0;animation:wdrift 1.6s var(--ease-out) forwards}
@keyframes wdrift{0%{opacity:0;transform:translate(-50%,0) scale(.6)}15%{opacity:1}100%{opacity:0;transform:translate(calc(-50% + var(--dx)),-170px) scale(1)}}
@media(max-width:820px){
  .ppanel{animation:slideup .26s var(--ease-out)}
  .pov.closing .ppanel{animation:slidedown .18s var(--ease-out) forwards}
  .moresheet,.modal.confirm{animation:slideup .24s var(--ease-out)}
  .overlay.closing .moresheet,.overlay.closing .modal.confirm{animation:slidedown .16s var(--ease-out) forwards}
}
"""
rep("\n/* mobile */\n", motion_css+"\n/* mobile */\n")
# reduced motion: keep the fades that say what changed, drop the travel, skip the decoration
rep("@media(prefers-reduced-motion:reduce){*{transition:none!important;animation:none!important}}",
"""@keyframes rmfade{from{opacity:0}}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition-property:opacity,color,background-color,border-color,box-shadow!important;transition-duration:.12s!important}
  .pov,.overlay,.ppanel,.modal,.setmodal,.moresheet,.toast,.rowin{animation:rmfade .12s linear!important}
  .pov.closing,.overlay.closing,.toast.closing,.pov.closing .ppanel,.overlay.closing .modal,.overlay.closing .setmodal,.overlay.closing .moresheet{animation:fadeout .12s linear forwards!important}
  .wpart,.ptchip,.wavefx{display:none!important}
  .stk{transition:none!important}
}""")

# ================= JS helpers =================
rep("  // ---- icons ----\n","""  // ---- motion: one-shot moments (CSS handles anything that can be re-triggered mid-way) ----
  var EASE_OUT='cubic-bezier(.16,1,.3,1)', EASE_POP='cubic-bezier(.34,1.56,.64,1)';
  var RM=(function(){ try{ return window.matchMedia('(prefers-reduced-motion: reduce)').matches; }catch(e){ return false; } })();
  var LAST_CHECK={el:null};          // the checkbox that was just tapped, so "+10" can rise from it
  var SEEN={}, APP_READY={v:false};  // rows already on screen when the app loaded don't animate in
  function anim(el,frames,opts){ if(!el||RM||!el.animate) return null; try{ return el.animate(frames,opts); }catch(e){ return null; } }
  function popCheck(el){ anim(el,[{transform:'scale(.8)'},{transform:'scale(1)'}],{duration:180,easing:EASE_POP}); }
  function floatChip(fromEl,text){ if(RM||!fromEl||!fromEl.getBoundingClientRect) return false; var r=fromEl.getBoundingClientRect(); if(!r.width) return false;
    var c=document.createElement('span'); c.className='ptchip'; c.textContent=text; c.style.left=(r.left+r.width/2)+'px'; c.style.top=(r.top-6)+'px'; document.body.appendChild(c);
    var a=anim(c,[{transform:'translate(-50%,0) scale(.8)',opacity:0},{transform:'translate(-50%,-14px) scale(1)',opacity:1,offset:.25},{transform:'translate(-50%,-36px) scale(1)',opacity:0}],{duration:600,easing:EASE_OUT});
    if(a) a.onfinish=function(){ c.remove(); }; else c.remove(); return true; }
  // a row folds away (or a card shrinks away), then the change happens
  function exitThen(el,fn,how){ if(!el||RM||!el.animate){ fn(); return; } var done=false; function go(){ if(done) return; done=true; fn(); }
    var a; if(how==='pop'){ a=anim(el,[{opacity:1,transform:'scale(1)'},{opacity:0,transform:'scale(.92)'}],{duration:160,easing:EASE_OUT,fill:'forwards'}); }
    else { var h=el.getBoundingClientRect().height; el.style.overflow='hidden'; a=anim(el,[{opacity:1,height:h+'px'},{opacity:0,height:'0px',paddingTop:'0px',paddingBottom:'0px',marginTop:'0px',marginBottom:'0px'}],{duration:180,easing:EASE_OUT,fill:'forwards'}); }
    if(a) a.onfinish=go; setTimeout(go,260); }
  function shake(el){ anim(el,[{transform:'translateX(0)'},{transform:'translateX(-6px)'},{transform:'translateX(6px)'},{transform:'translateX(-4px)'},{transform:'translateX(4px)'},{transform:'translateX(0)'}],{duration:320,easing:'ease-in-out'}); }
  function buzz(){ try{ if(navigator.vibrate) navigator.vibrate(10); }catch(e){} }
  // confetti, loaded the first time someone wins
  var confettiP=null;
  function celebrate(colors){ if(RM) return;
    if(!confettiP) confettiP=new Promise(function(res,rej){ var sc=document.createElement('script'); sc.src='https://cdnjs.cloudflare.com/ajax/libs/canvas-confetti/1.9.3/confetti.js'; sc.onload=function(){ res(window.confetti); }; sc.onerror=rej; document.head.appendChild(sc); });
    confettiP.then(function(c){ if(!c) return; var o={particleCount:80,spread:70,startVelocity:42,ticks:220,colors:colors||['#1F6FEB','#15171A','#B4792B'],disableForReducedMotion:true}; c(Object.assign({},o,{angle:60,origin:{x:0,y:.35}})); c(Object.assign({},o,{angle:120,origin:{x:1,y:.35}})); }).catch(function(){ confettiP=null; }); }
  // a number that counts to its new value instead of jumping
  function Num(props){ var v=props.v||0; var sS=useState(v); var shown=sS[0], setShown=sS[1]; var cur=useRef(v);
    useEffect(function(){ if(RM||cur.current===v){ cur.current=v; setShown(v); return; } var a=cur.current, b=v, t0=0, raf;
      function step(now){ if(!t0) t0=now; var k=Math.min(1,(now-t0)/450), e=1-Math.pow(1-k,3), x=Math.round(a+(b-a)*e); cur.current=x; setShown(x); if(k<1) raf=requestAnimationFrame(step); }
      raf=requestAnimationFrame(step); return function(){ cancelAnimationFrame(raf); }; },[v]);
    return html`<span class="tnum">${shown}</span>`; }
  // keep a sheet or modal on screen a moment after it closes, so it can animate out
  function useLinger(v,ms){ var sS=useState(v); var shown=sS[0], setShown=sS[1]; var t=useRef(null);
    useEffect(function(){ clearTimeout(t.current); if(v){ if(shown!==v) setShown(v); } else if(shown){ if(RM){ setShown(null); return; } t.current=setTimeout(function(){ setShown(null); },ms); } },[v]);
    return [v||shown, !v&&!!shown]; }

  // ---- icons ----
""")

# check: pops when ticked, remembers where it was for the "+10"
rep("onClick=${props.onClick}>${props.done?checkMark:null}</button>`; }","onClick=${function(e){ LAST_CHECK.el=e.currentTarget; if(!props.done) popCheck(e.currentTarget); if(props.onClick) props.onClick(e); }}>${props.done?checkMark:null}</button>`; }")

# task rows: drawn strike, arrive softly, can be found to fold away
rep("""    var planned=!t.done && !!t.date && t.date<TODAY;
    return html`<div class="arow">""","""    var planned=!t.done && !!t.date && t.date<TODAY;
    var rowKey=(carry?'c':'d')+t.id, fresh=APP_READY.v&&!SEEN[rowKey]; SEEN[rowKey]=1;
    return html`<div class=${'arow'+(fresh?' rowin':'')} data-row=${rowKey}>""")
rep("""        <div class=${'atitle'+(t.done?' done':'')}>${t.title}</div>""","""        <div class=${'atitle'+(t.done?' done':'')}><span class="stk">${t.title}</span></div>""")
n=s.count('<span class="slabel">${s.title}</span>')
s=s.replace('<span class="slabel">${s.title}</span>','<span class="slabel"><span class="stk">${s.title}</span></span>')
print('subtask labels',n)
rep("""<div class=${'ititle'+(it.done?' done':'')}>${it.title}</div>""","""<div class=${'ititle'+(it.done?' done':'')}><span class="stk">${it.title}</span></div>""")

# streak flame bumps when the count goes up
rep("""${st>0?html`<span style=${{display:'block',fontWeight:400,fontSize:'11.5px',color:'#8A93A0'}}>${st}-day streak</span>`:null}</span>""",
    """${st>0?html`<span style=${{display:'block',fontWeight:400,fontSize:'11.5px',color:'#8A93A0'}}><span key=${h.id+'-'+st} class=${'flame'+(grewStreak(h.id,st)?' bump':'')}><svg width="12" height="12" viewBox="0 0 24 24" fill="none" aria-hidden="true">${svgFlame}</svg></span>${st}-day streak</span>`:null}</span>""")
rep("""    var countH=myHabits.filter(function(h){return h.kind==='count';});""","""    var countH=myHabits.filter(function(h){return h.kind==='count';});
    var prevStreak=useRef({});
    function grewStreak(id,st){ var p=prevStreak.current[id]; return p!=null && st>p; }""")
rep("""    var myNotes=(notes||[]).filter(function(n){return n.owner===whoami;});""","""    var myNotes=(notes||[]).filter(function(n){return n.owner===whoami;});
    useEffect(function(){ checkH.forEach(function(h){ prevStreak.current[h.id]=streak(h.id); }); });""")

# focus: show "Time's up" a moment with a soft pulse before resetting
rep("return html`<div class=${'focusw'+(active?' active':'')}>","return html`<div class=${'focusw'+(active?' active':'')+(done?' done':'')}>")
rep("var ms=f.ends_at-Date.now(); if(ms<=0){ finish(); return; } var tm=setTimeout(finish,ms+300); return function(){ clearTimeout(tm); };",
    "var ms=f.ends_at-Date.now()+2200; if(ms<=0){ finish(); return; } var tm=setTimeout(finish,ms); return function(){ clearTimeout(tm); };")

# numbers count up; the crown drops when the lead changes
rep("""<span class=${'crownp'+(lead?'':' calm')}>""","""<span class=${'crownp'+(lead?'':' calm')+(lead&&props.fresh?' fresh':'')}>""")
rep("""<span class="sstxt">You ${me.points} · ${nameOf(ot.id)} ${ot.points}</span>""","""<span class="sstxt">You <${Num} v=${me.points} /> · ${nameOf(ot.id)} <${Num} v=${ot.points} /></span>""")
rep("""${sc.leader?html`<span class="crownp">${crownGlyph}""","""${sc.leader?html`<span class=${'crownp'+(props.fresh?' fresh':'')}>${crownGlyph}""")
rep("""<span class="rv">${v}</span>""","""<span class="rv"><${Num} v=${v} /></span>""")
rep("""${sc.leader===p.id?html`<span class="crownp">${crownGlyph}${p.points}</span>`:html`<span class="lbp">${p.points}</span>`}""",
    """${sc.leader===p.id?html`<span class=${'crownp'+(props.fresh?' fresh':'')}>${crownGlyph}<${Num} v=${p.points} /></span>`:html`<span class="lbp"><${Num} v=${p.points} /></span>`}""")
rep("""(thisWeek.people[whoami].points+' · '+thisWeek.people[other].points)""","""html`<${Num} v=${thisWeek.people[whoami].points} /> · <${Num} v=${thisWeek.people[other].points} />`""")

# sign in: the field shakes on a wrong password
rep("""    var cd=useCountdown(); var wait=cd[0], setWait=cd[1];
    function submit(e){""","""    var cd=useCountdown(); var wait=cd[0], setWait=cd[1];
    useEffect(function(){ if(err) shake(document.querySelector('.authcard .pwf')); },[err]);
    function submit(e){""")
rep("""    useEffect(function(){ if(props.claimable){ setList(props.claimable); setStep('pick'); } },[props.claimable]);""","""    useEffect(function(){ if(props.claimable){ setList(props.claimable); setStep('pick'); } },[props.claimable]);
    useEffect(function(){ if(err) shake(document.querySelector('.authcard .pwf')||document.querySelector('.authcard .autherr')); },[err]);""")

# sheets + modals can close with an animation
rep("""<div class="pov" style=${{zIndex:62}} onClick=${function(e){if(e.target===e.currentTarget)props.onClose();}}>""","""<div class=${'pov'+(props.closing?' closing':'')} style=${{zIndex:62}} onClick=${function(e){if(e.target===e.currentTarget)props.onClose();}}>""",2)
rep("""<div class="overlay" style=${{zIndex:80}} onClick=""","""<div class=${'overlay'+(props.closing?' closing':'')} style=${{zIndex:80}} onClick=""")
rep("""<div class="overlay" onClick=${function(e){if(e.target===e.currentTarget)props.onClose();}}>""","""<div class=${'overlay'+(props.closing?' closing':'')} onClick=${function(e){if(e.target===e.currentTarget)props.onClose();}}>""",2)
rep("""<div class="overlay confirmov" onClick=""","""<div class=${'overlay confirmov'+(props.closing?' closing':'')} onClick=""")
rep("""<div class="overlay moreov" onClick=""","""<div class=${'overlay moreov'+(props.closing?' closing':'')} onClick=""")

# notes shrink away when deleted
rep("""<div class="notecd" style=${{background:c.bg,borderColor:c.bd}}>""","""<div class="notecd" data-row=${'n'+n.id} style=${{background:c.bg,borderColor:c.bd}}>""")

# ================= App =================
rep("""    var cfS=useState(null); var confirmBox=cfS[0], setConfirm=cfS[1];""","""    var cfS=useState(null); var confirmBox=cfS[0], setConfirm=cfS[1];
    var lfS=useState(0); var leadFlash=lfS[0], setLeadFlash=lfS[1];   // the crown drops when the lead changes""")
rep("""    var editingTask=modal&&modal.editing;""","""    var editingTask=modalV&&modalV.editing;""")
# lingering copies (placed right after the toast state so every value exists)
rep("""    var waveOpenS=useState(false); var waveOpen=waveOpenS[0], setWaveOpen=waveOpenS[1];""","""    var waveOpenS=useState(false); var waveOpen=waveOpenS[0], setWaveOpen=waveOpenS[1];
    // each overlay stays a moment after it closes, so it can animate out
    var lg=useLinger(modal,170), modalV=lg[0], modalClosing=lg[1];
    lg=useLinger(pEdit,170); var pEditV=lg[0], pEditClosing=lg[1];
    lg=useLinger(habitEdit,150); var habitV=lg[0], habitClosing=lg[1];
    lg=useLinger(settingsOpen,150); var setV=lg[0], setClosing=lg[1];
    lg=useLinger(confirmBox,150); var confirmV=lg[0], confirmClosing=lg[1];
    lg=useLinger(showIntro,150); var introV=lg[0], introClosing=lg[1];
    lg=useLinger(moreOpen,170); var moreV=lg[0], moreClosing=lg[1];
    lg=useLinger(toast,170); var toastV=lg[0], toastClosing=lg[1];""")
# carried rows fold away before they move
rep("""    var carry={ onToday:function(t){ patchTask(t,{date:TODAY}); }, onPick:function(t,ds){ patchTask(t,{date:ds}); }, onUnplan:function(t){ patchTask(t,{date:'',time:''}); } };""",
    """    function rowEl(k){ return document.querySelector('[data-row="'+k+'"]'); }
    var carry={ onToday:function(t){ exitThen(rowEl('c'+t.id),function(){ patchTask(t,{date:TODAY}); }); }, onPick:function(t,ds){ exitThen(rowEl('c'+t.id),function(){ patchTask(t,{date:ds}); }); }, onUnplan:function(t){ exitThen(rowEl('c'+t.id),function(){ patchTask(t,{date:'',time:''}); }); } };""")
rex(r"""    function toggleTask\(t\)\{\n      // the moment: ticking shows what it earned\n[^\n]*\n      patchTask\(t,\{done:!t\.done\}\); \}""", lambda m: """    function toggleTask(t){
      var el=LAST_CHECK.el; LAST_CHECK.el=null;
      var ticking=!t.done && !isEventType(t.type);
      if(ticking){
        buzz();
        // the moment: "+10" rises from the box you ticked
        if(showScores){ var r=taskPoints(t,TODAY,whoami); if(!(el&&document.body.contains(el)&&floatChip(el,'+'+r.n))) showToast({text:'+'+r.n+(r.onTime?' · done on time':'')+(r.helped?' · you helped':'')}); }
        // the last open task of a project: offer to finish it
        if(t.project&&!t.parent_id){ var left=(tasks||[]).filter(function(x){ return x.project===t.project&&!x.parent_id&&!x.done&&x.id!==t.id&&!isEventType(x.type); }).length; var pj=(projects||[]).filter(function(x){return x.id===t.project;})[0];
          if(!left&&pj&&!pj.archived) setTimeout(function(){ showToast({text:'Every task in “'+pj.name+'” is done',action:{label:'Finish project',fn:function(){ finishProject(pj); }},ms:7000}); },420); }
      }
      // ticked in "From earlier": the row folds away first
      var row=ticking&&el&&el.closest?el.closest('[data-row^="c"]'):null;
      if(row) exitThen(row,function(){ patchTask(t,{done:true}); }); else patchTask(t,{done:!t.done}); }""")
rex(r"""    function deleteTask\(id\)\{\n      var t=findTask\(id\); setModal\(null\); if\(!t\) return;\n""", lambda m: """    function deleteTask(id){
      var t=findTask(id); setModal(null); if(!t) return;
      delete SEEN['d'+id]; delete SEEN['c'+id];   // so Undo brings it back the same way
""")
rex(r"""      holdDelete\(\[\{op:'delete',table:'tasks',id:id,_label:t\.title\}\],('Deleted “'\+t\.title\+'”'\+\(kids\?\(' and its '\+kids\+' subtask'\+\(kids>1\?'s':''\)\):''\))\);""",
    lambda m: "      var go=function(){ holdDelete([{op:'delete',table:'tasks',id:id,_label:t.title}],"+m.group(1)+"); };\n      exitThen(rowEl('d'+id)||rowEl('c'+id),go);")
rep("""    function deleteNote(n){ holdDelete([{op:'delete',table:'notes',id:n.id,_label:'a note'}],'Deleted a note'); }""",
    """    function deleteNote(n){ exitThen(document.querySelector('[data-row="n'+n.id+'"]'),function(){ holdDelete([{op:'delete',table:'notes',id:n.id,_label:'a note'}],'Deleted a note'); },'pop'); }""")
rep("""    function finishProject(p){ setPEdit(null); setPanel(null); commit(""","""    function finishProject(p){ celebrate([p.color||'#1F6FEB',personColor(whoami),'#B4792B']); setPEdit(null); setPanel(null); commit(""")
# lead changes + last week's result, once, after data has loaded
rep("""    var helpFor=null; if(thisWeek){""","""    var leadRef=useRef(undefined);
    useEffect(function(){ if(!thisWeek) return; var L=thisWeek.leader;
      if(leadRef.current!==undefined && L && L!==leadRef.current){ setLeadFlash(Date.now()); showToast({text:L===whoami?'You took the lead':(nameOf(L)+' took the lead'),ms:4000}); var tm=setTimeout(function(){ setLeadFlash(0); },1400); leadRef.current=L; return function(){ clearTimeout(tm); }; }
      leadRef.current=L; },[thisWeek&&thisWeek.leader]);
    useEffect(function(){ if(!store||!showScores) return; var lw=ymd(addDays(parseYmd(mondayOf(TODAY)),-7)), key='sp_won_'+lw+'_'+whoami; if(lsGet(key,'')) return;
      var r=scoreWeek(wkData,lw); lsSet(key,r.leader||'-'); if(!r.leader) return;
      var line=r.ranked[0].points+'–'+r.ranked[1].points;
      if(r.leader===whoami){ celebrate([personColor(whoami),'#1F6FEB','#B4792B']); showToast({text:'You won last week, '+line,ms:5000}); }
      else showToast({text:nameOf(r.leader)+' won last week, '+line+'. New week, fresh start.',ms:5000}); },[!!store, showScores, whoami]);
    useEffect(function(){ if(store&&!APP_READY.v){ var tm=setTimeout(function(){ APP_READY.v=true; },400); return function(){ clearTimeout(tm); }; } },[!!store]);
    var helpFor=null; if(thisWeek){""")
rep("""score=${thisWeek} help=${helpFor} onOpenWeek=""","""score=${thisWeek} help=${helpFor} fresh=${!!leadFlash} onOpenWeek=""")
rep("""content=html`<${WeekPage} data=${wkData}""","""content=html`<${WeekPage} fresh=${!!leadFlash} data=${wkData}""")
rep("""<${ScoreStrip} score=${props.score} help=${props.help} onOpen=${props.onOpenWeek} />""","""<${ScoreStrip} score=${props.score} help=${props.help} fresh=${props.fresh} onOpen=${props.onOpenWeek} />""")

# render: overlays use their lingering copies
rex(r"""\$\{modal\?html`<\$\{TaskModal\}([^\n]*)""", lambda m: "${modalV?html`<${TaskModal} closing=${modalClosing}"+m.group(1).replace("editing=${modal.editing}","editing=${modalV.editing}").replace("modal.defaultDate","modalV.defaultDate").replace("modal.defaultTime","modalV.defaultTime").replace("modal.defaultType","modalV.defaultType").replace("modal.defaultProject","modalV.defaultProject"))
rep("""${pEdit?html`<${ProjectEditor} editing=${pEdit}""","""${pEditV?html`<${ProjectEditor} closing=${pEditClosing} editing=${pEditV}""")
rep("""${showIntro?html`<${Intro} onClose=""","""${introV?html`<${Intro} closing=${introClosing} onClose=""")
rep("""${settingsOpen?html`<${SettingsModal}""","""${setV?html`<${SettingsModal} closing=${setClosing}""")
rep("""${habitEdit?html`<${HabitEditor} editing=${habitEdit.id?habitEdit:null}""","""${habitV?html`<${HabitEditor} closing=${habitClosing} editing=${habitV.id?habitV:null}""")
rex(r"""\$\{toast\?html`<div class=\$\{'toast'\+\(toast\.big\?' big':''\)\}([^\n]*)""", lambda m: "${toastV?html`<div class=${'toast'+(toastV.big?' big':'')+(toastClosing?' closing':'')}"+m.group(1).replace("toast.","toastV."))
rex(r"""\$\{confirmBox\?html`<\$\{ConfirmModal\} ([^\n]*)""", lambda m: "${confirmV?html`<${ConfirmModal} closing=${confirmClosing} "+m.group(1).replace("confirmBox.","confirmV."))
rep("""${moreOpen?html`<${MoreSheet}""","""${moreV?html`<${MoreSheet} closing=${moreClosing}""")
# the wave: the burst plus a few of the same emoji drifting up
rep("""${toast&&toast.big?html`<div class="wavefx" key=${'fx'+toast.t}>${toast.emoji}</div>`:null}""",
    """${toast&&toast.big?html`<div class="wavefx" key=${'fx'+toast.t}>${toast.emoji}</div>`:null}
      ${toast&&toast.big?[-96,-54,-18,18,54,96].map(function(dx,i){ return html`<span class="wpart" key=${'wp'+toast.t+i} style=${{'--dx':dx+'px',animationDelay:(120+i*70)+'ms'}} aria-hidden="true">${toast.emoji}</span>`; }):null}""")
open(P,'w').write(s); print('motion ok', len(s))
