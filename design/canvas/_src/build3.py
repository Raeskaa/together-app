#!/usr/bin/env python3
# Builds the three approved designs into public/index.html: Home H1, Calendar Day, Settings › Claude.
P = '/Users/design/shared-planner/public/index.html'
s = open(P).read()
def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:120])
    s = s.replace(a, b)

# ---------------------------------------------------------------- CSS
CSS = r"""
/* ---- Home H1: one list + a slim rail (8 Nov) ---- */
.hm-grid{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:40px;margin-top:6px;align-items:start}
.hm-qadd{display:flex;align-items:center;gap:10px;border:1px dashed #C9D5E5;border-radius:10px;padding:9px 12px;margin:14px 0 4px;color:#4B5866;background:#fff}
.hm-qadd:focus-within{border-style:solid;border-color:#9DBEF2;box-shadow:0 0 0 3px rgba(31,111,235,.12)}
.hm-qadd input{flex:1;min-width:0;border:0;outline:0;background:transparent;font:inherit;font-size:14px;color:#15171A;padding:0}
.hm-qadd input::placeholder{color:#5E6875}
.hm-qplus{font-size:18px;line-height:1;color:#4B5866;width:16px;text-align:center}
.hm-kbd{font-size:11px;font-weight:500;color:#4B5866;border:1px solid #DCE3EC;border-radius:5px;padding:1px 6px}
.hm-ghd{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:18px 2px 4px}
.hm-glbl{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#3C6FB0}
.hm-gmeta{display:flex;align-items:center;gap:10px;font-size:12.5px;color:#4B5866}
.hm-donel{display:flex;align-items:center;gap:8px;width:100%;padding:11px 2px;border:0;border-top:1px solid var(--line-soft);background:none;font:inherit;font-size:13px;color:#4B5866;cursor:pointer;text-align:left}
.hm-donel svg{transition:transform .15s var(--ease-out)}
.hm-donel.open svg{transform:rotate(180deg)}
.hm-pts{margin-left:auto;font-size:12px;font-weight:600;color:#1D6842;background:#E3F4EA;border-radius:99px;padding:2px 8px;font-variant-numeric:tabular-nums}
.hm-rail{border-left:1px solid var(--line-soft);padding:6px 0 0 28px}
.hm-sec{padding:16px 0;border-top:1px solid var(--line-soft)}
.hm-sec:first-child{border-top:0;padding-top:10px}
.hm-shd{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:9px}
.hm-shd h2{margin:0;font-size:15px;font-weight:700;color:#15171A}
.hm-crow{display:flex;align-items:center;gap:9px;font-size:13px;padding:5px 0;color:#15171A}
.hm-crow .t{flex:1;min-width:0;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hm-cpill{font-size:11.5px;font-weight:600;border-radius:99px;padding:2px 8px;color:#46505D;background:#EEF2F7;white-space:nowrap}
.hm-cpill.soon{color:#85560F;background:#FBF1E6}
.hm-small{display:inline-flex;align-items:center;gap:6px;border:1px solid #DCE3EC;border-radius:8px;background:#fff;color:#15171A;font:inherit;font-weight:600;font-size:12px;padding:5px 9px;cursor:pointer}
.hm-wide{display:flex;align-items:center;justify-content:center;gap:7px;width:100%;border:1px solid #DCE3EC;border-radius:10px;background:#fff;color:#15171A;font:inherit;font-weight:600;font-size:13px;padding:8px 12px;cursor:pointer}
.hm-over{color:#A3392C;font-weight:600}
.scpill{display:inline-flex;align-items:center;gap:8px;border:1px solid #E5EAF1;background:#F7F9FC;border-radius:99px;padding:6px 10px 6px 12px;font:inherit;font-size:13px;font-weight:600;color:#15171A;cursor:pointer;white-space:nowrap}
.scpill:hover{border-color:#BFD5F7}
.scp-crown{display:inline-flex;color:#B4792B}.scp-crown.calm{color:#8A9BB0}
.scp-num{font-weight:500;color:#4B5866;font-variant-numeric:tabular-nums}
.scp-short{display:none}
.scpill.fresh .scp-crown{animation:crowndrop .6s var(--ease-pop)}
@media(max-width:1000px){ .hm-grid{grid-template-columns:1fr;gap:6px} .hm-rail{border-left:0;padding:0;border-top:1px solid var(--line-soft);margin-top:10px} }
@media(max-width:820px){ .scp-long,.scp-num{display:none} .scp-short{display:inline} .scpill{padding:6px 10px} }

/* ---- Calendar · Day (8 Nov) ---- */
.dv-grid{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(260px,1fr);gap:22px;align-items:start}
.dv-allday{display:flex;align-items:center;gap:8px;flex-wrap:wrap;border:1px solid var(--line);border-radius:12px;padding:8px 12px;margin-bottom:10px;font-size:12.5px;min-height:22px}
.dv-allday .k{font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#3C6FB0;width:52px;flex:none}
.dv-chip{display:inline-flex;align-items:center;gap:6px;border:0;border-radius:99px;padding:3px 10px;font:inherit;font-size:12px;font-weight:600;color:#85560F;background:#FBF1E6;cursor:pointer}
.dv-chip.proj{color:#2F343B;background:#EEF2F7}
.dv-chip.ev{color:#4E3A8A;background:#ECE4FF}
.dv-tl{position:relative;border:1px solid var(--line);border-radius:14px;max-height:640px;overflow-y:auto;background:#fff}
.dv-hours{position:relative}
.dv-hr{display:flex;border-top:1px solid var(--line-soft);box-sizing:border-box}
.dv-hr:first-child{border-top:0}
.dv-hr .lab{width:56px;flex:none;text-align:right;padding:0 10px 0 0;box-sizing:border-box;font-size:11.5px;color:#4B5866;font-variant-numeric:tabular-nums;transform:translateY(-8px)}
.dv-hr:first-child .lab{transform:none;padding-top:2px}
.dv-hr .slot{flex:1;cursor:pointer}
.dv-hr .slot:hover{background:#F7FAFF}
.dv-hr .slot.drop{background:#EAF2FF;box-shadow:inset 0 0 0 1.5px #8DB4F2}
.dv-b{position:absolute;border-radius:9px;padding:6px 10px;box-sizing:border-box;font-size:13px;display:flex;align-items:flex-start;gap:8px;overflow:hidden;text-align:left;font-family:inherit;color:#15171A;cursor:pointer;border:1px solid #DCE3EC;background:#fff;box-shadow:0 1px 2px rgba(20,60,130,.06)}
.dv-b .bt{font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.dv-b .bs{font-size:12px;color:#4B5866;font-variant-numeric:tabular-nums;white-space:nowrap}
.dv-b .bx{flex:1;min-width:0}
.dv-b.short{align-items:center}.dv-b.short .bx{display:flex;gap:8px;align-items:baseline}
.dv-b.rt{background:#EEF4FF;border-color:#D3E2FB;box-shadow:none;cursor:default}
.dv-b.ev{background:#F3F5F9;border-color:#DCE3EC;box-shadow:none}
.dv-b.pt{background:#F1F3F7;border-color:#D9DFE8;box-shadow:none}
.dv-b.dn{background:#F7F9FC;border-color:#EEF2F7;box-shadow:none}
.dv-b.dn .bt{color:#6B7480;text-decoration:line-through;text-decoration-color:#AEB8C5;font-weight:500}
.dv-ic{display:inline-flex;color:#3C6FB0;flex:none;margin-top:1px}
.dv-now{position:absolute;left:56px;right:0;height:0;border-top:2px solid #1F6FEB;pointer-events:none;z-index:2}
.dv-now i{position:absolute;left:-5px;top:-6px;width:10px;height:10px;border-radius:99px;background:#1F6FEB}
.dv-now b{position:absolute;right:8px;top:-21px;background:#1F6FEB;color:#fff;font-size:11px;font-weight:600;border-radius:99px;padding:2px 7px;font-variant-numeric:tabular-nums}
.dv-empty{border:1px dashed #C9D5E5;border-radius:14px;padding:48px 24px;text-align:center;background:#FBFCFE}
.dv-empty h3{margin:0;font-size:16px;font-weight:700;color:#15171A}
.dv-empty p{margin:6px auto 0;max-width:440px;font-size:13.5px;line-height:1.5;color:#4B5866}
.dv-empty .row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:16px}
.dv-side .box{border:1px solid var(--line);border-radius:14px;padding:4px 12px 10px;margin-bottom:14px;background:#fff}
.dv-side .hd{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:12px 4px 6px}
.dv-side .hd h2{margin:0;font-size:14px;font-weight:700;color:#15171A}
.dv-side .hd .m{font-size:12px;color:#4B5866}
.dv-row{display:flex;align-items:center;gap:9px;padding:8px 6px;border-radius:9px;border:1px solid transparent;cursor:grab;font-size:13.5px}
.dv-row:hover{background:#F7FAFF}
.dv-row.sel{border-color:#9DBEF2;background:#F3F8FF}
.dv-row .t{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-weight:500}
.dv-row .t.done{color:#6B7480;text-decoration:line-through}
.dv-grip{color:#8A9BB0;display:inline-flex;flex:none}
.dv-hint{display:flex;align-items:flex-start;gap:8px;font-size:12.5px;line-height:1.45;color:#4B5866;background:#F7F9FC;border-radius:10px;padding:9px 12px}
.dv-strip{display:none}
.dv-list{display:none}
@media(max-width:820px){
  .dv-grid{grid-template-columns:1fr}
  .dv-tl{display:none}
  .dv-list{display:block}
  .dv-strip{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:2px;margin:0 0 10px}
  .dv-strip button{border:0;background:none;border-radius:10px;padding:6px 0;display:flex;flex-direction:column;align-items:center;gap:2px;font:inherit;font-size:11px;font-weight:600;color:#3C6FB0;cursor:pointer}
  .dv-strip button b{font-size:15px;color:#2F343B}
  .dv-strip button.on{background:#EEF4FF}.dv-strip button.on b{color:#195FD0}
  .dv-li{display:flex;gap:12px;align-items:stretch;padding:4px 0}
  .dv-li .tm{width:44px;flex:none;text-align:right;font-size:12px;color:#4B5866;padding-top:9px;font-variant-numeric:tabular-nums}
  .dv-li .dv-b{position:static;flex:1;min-width:0}
  .dv-linow{display:flex;align-items:center;gap:8px;margin:6px 0}
  .dv-linow b{width:44px;text-align:right;font-size:11px;font-weight:700;color:#195FD0;font-variant-numeric:tabular-nums}
  .dv-linow span{flex:1;border-top:2px solid #1F6FEB;position:relative}
  .dv-linow i{position:absolute;left:-5px;top:-6px;width:10px;height:10px;border-radius:99px;background:#1F6FEB}
}

/* ---- Settings › Claude (8 Nov) ---- */
.cl-new{font-size:10px;font-weight:700;color:#1D6842;background:#E3F4EA;border-radius:99px;padding:1px 6px;margin-left:6px;vertical-align:1px}
.cl-p{font-size:13px;line-height:1.55;color:#4B5866;margin:0 0 4px}
.cl-link{display:flex;gap:8px}
.cl-link input{flex:1;min-width:0;border:1px solid var(--field);border-radius:10px;padding:9px 12px;font:inherit;font-size:13px;color:#15171A;background:#F7F9FC}
.cl-note{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--line);background:#F7F9FC;border-radius:10px;padding:10px 12px;font-size:12.5px;line-height:1.45;color:#4B5866;margin-top:10px}
.cl-note b{color:#15171A;font-weight:600}
.cl-note svg{flex:none;margin-top:1px;color:#B4792B}
.cl-steps{margin:0;padding-left:18px;font-size:13px;line-height:1.7;color:#2F343B}
.cl-can{display:flex;flex-wrap:wrap;gap:6px}
.cl-can span{font-size:12px;font-weight:500;border:1px solid #DCE3EC;border-radius:99px;padding:4px 10px;color:#2F343B}
.cl-foot{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:18px;padding-top:14px;border-top:1px solid var(--line-soft)}
.cl-danger{color:#A3392C!important}
"""
rep('@keyframes rmfade{from{opacity:0}}', CSS + '@keyframes rmfade{from{opacity:0}}')
# keep the new strike/press motion honest under reduced motion
rep('  .stk{transition:none!important}\n}', '  .stk{transition:none!important}\n  .hm-donel svg{transition:none!important}\n}')

# ---------------------------------------------------------------- Score pill (header)
rep('  // ---- This week ----\n  function WeekPage(props){', r'''  // the score as one pill in the Today header: who leads, by how much, tap for the week
  function ScorePill(props){ var sc=props.score, me=sc.people[VIEW.who], ot=sc.people[otherOf(VIEW.who)]; if(!me||!ot) return null;
    var lead=sc.leader, gap=Math.abs(me.points-ot.points);
    var long=lead===VIEW.who?('You lead by '+gap):(lead?(nameOf(lead)+' leads by '+gap):(me.points?'Level':'A fresh week'));
    var short=lead===VIEW.who?(gap+' ahead'):(lead?(gap+' behind'):'Level');
    return html`<button type="button" class=${'scpill'+(lead&&props.fresh?' fresh':'')} onClick=${props.onOpen} aria-label=${long+'. You '+me.points+', '+nameOf(ot.id)+' '+ot.points+'. Open This week'}>
      <span class=${'scp-crown'+(lead?'':' calm')}>${crownGlyph}</span><span class="scp-long">${long}</span><span class="scp-short">${short}</span>
      <span class="scp-num"><${Num} v=${me.points} /> – <${Num} v=${ot.points} /></span>
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M9 6l6 6-6 6" stroke="#5B6B86" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>`; }

  // ---- This week ----
  function WeekPage(props){''')
rep('''            ${v==='today'&&!openProj?html`<div class="seg" role="group" aria-label="Filter">''',
    '''            ${v==='today'&&!openProj&&thisWeek?html`<${ScorePill} score=${thisWeek} fresh=${!!leadFlash} onOpen=${function(){setView2('week');}} />`:null}
            ${v==='today'&&!openProj?html`<div class="seg" role="group" aria-label="Filter">''')

# ---------------------------------------------------------------- Today → H1
OLD_TODAY_HEAD = s[s.index('    return html`<${Fragment}>\n      ${props.score?html`<${ScoreStrip}'):s.index("      <div style=${{display:'flex',justifyContent:'space-between',alignItems:'baseline',margin:'26px 2px 0'}}>\n        <h3 style=${{fontWeight:700,fontSize:'15px',color:'#15171A',margin:0}}>Habits & focus</h3>")]
NEW_TODAY_HEAD = r'''    // H1: open tasks first; a task you just ticked stays a moment (so the tick is seen), then folds into "done"
    var openT=dayTasks.filter(function(t){ return !t.done || kept(t); });
    var doneT=dayTasks.filter(function(t){ return t.done && !kept(t); });
    var earned=doneT.reduce(function(n,t){ return (t.done_by===whoami&&t.done_at)?n+taskPoints(t,dayOfMs(t.done_at),t.done_by).n:n; },0);
    var other=otherOf(whoami);
    var otToday=(tasks||[]).filter(function(t){ return t.owner===other && !t.parent_id && !isEventType(t.type) && (t.date===TODAY||(t.due===TODAY)); });
    var otDone=otToday.filter(function(t){ return t.done; }).length;
    var otLate=other?overdueOf(tasks,other):[];
    var dayLbl=isToday?'Today':longDay(parseYmd(sel));
    return html`<${Fragment}>
      <div class="hm-grid">
      <section class="hm-list" aria-label=${dayLbl}>
        <form class="hm-qadd" onSubmit=${function(e){ e.preventDefault(); var v=qa.trim(); if(!v) return; props.onQuickAdd(v,sel); setQa(''); }}>
          <span class="hm-qplus" aria-hidden="true">+</span>
          <label class="sr" for="hm-qadd">New task for ${dayLbl}</label>
          <input id="hm-qadd" type="text" autocomplete="off" value=${qa} placeholder=${isToday?'Add a task for today':('Add a task for '+shortDate(sel))} onInput=${function(e){setQa(e.target.value);}} />
          <span class="hm-kbd" aria-hidden="true">Enter</span>
        </form>
        ${carried.length?html`<div class="carry">
          <div class="carryhd"><span class="carryttl">From earlier · ${carried.length}</span><button class="view" onClick=${function(){props.onMoveAllToday(carried);}}>Move all to today</button></div>
          ${carryShown.map(function(t){ return html`<${TaskRow} t=${t} tasks=${tasks} proj=${projMap[t.project]} parent=${t.parent_id?taskMap[t.parent_id]:null} carry=${props.carry} onToggle=${props.onToggle} onEdit=${props.onEdit} key=${'c'+t.id} />`; })}
          ${carried.length>5?html`<button class="view carrymore" onClick=${function(){setCarryAll(!carryAll);}}>${carryAll?'Show fewer':('Show '+(carried.length-5)+' more')}</button>`:null}
        </div>`:null}
        <div class="hm-ghd"><span class="hm-glbl">${dayLbl} · ${openT.filter(function(t){return !t.done;}).length} left</span><span class="hm-gmeta">${isToday&&dayRoutines.length?(dayRoutines.length+' routine'+(dayRoutines.length>1?'s':'')):''}<button class="addinline" aria-label=${'Add something for '+dayLbl} onClick=${function(){props.onAdd(sel);}}>+</button></span></div>
        ${isToday ? dayRoutines.map(function(r){ var sh=+r.start.split(':')[0]; var eh=+r.end.split(':')[0]; var now=nowHour>=sh&&nowHour<eh; return html`<${Block} r=${r} dur=${durOf(r)} now=${now} key=${r.id} />`; }) : null}
        ${openT.map(function(t){ return html`<${TaskRow} t=${t} tasks=${tasks} proj=${projMap[t.project]} parent=${t.parent_id?taskMap[t.parent_id]:null} onToggle=${props.onToggle} onEdit=${props.onEdit} key=${t.id} />`; })}
        ${doneT.length?html`<button type="button" class=${'hm-donel'+(showDone?' open':'')} aria-expanded=${showDone} onClick=${function(){setShowDone(!showDone);}}><svg width="14" height="14" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>${doneT.length} done${isToday?' today':''}${earned?html`<span class="hm-pts">+${earned}</span>`:null}</button>`:null}
        ${showDone?doneT.map(function(t){ return html`<${TaskRow} t=${t} tasks=${tasks} proj=${projMap[t.project]} parent=${t.parent_id?taskMap[t.parent_id]:null} onToggle=${props.onToggle} onEdit=${props.onEdit} key=${t.id} />`; }):null}
        ${(dayTasks.length===0 && !(isToday&&dayRoutines.length))?(carried.length?html`<div class="carryempty">Nothing new today.</div>`:html`<div class="empty"><div class="big">A clear day ✨</div><div class="sub">Nothing planned. Enjoy the space, and add something above whenever you like.</div></div>`):null}
      </section>
      <aside class="hm-rail" aria-label="Around today">
        ${other?html`<div class="hm-sec"><div class="hm-shd"><h2>${nameOf(other)}</h2><${Avatar} owner=${other} /></div>
          <div style=${{fontSize:'13px',lineHeight:1.5,color:'#4B5866'}}>${otToday.length?(otDone+' of '+otToday.length+' done today'):'Nothing planned today'}${otLate.length?html` · <span class="hm-over">${otLate.length} overdue</span>`:null}</div>
          ${(props.help===other||otLate.length)?html`<div style=${{marginTop:'10px'}}><button type="button" class="hm-small" onClick=${props.onOpenWeek}>Give a hand · +5</button></div>`:null}
        </div>`:null}
        <div class="hm-sec"><div class="hm-shd"><h2>Coming up</h2><button class="view" onClick=${function(){props.onShowAll&&props.onShowAll();}}>All tasks</button></div>
          ${up.length?up.map(function(d){ var c=d.isproj?(d.color||'#1F6FEB'):personColor(d.owner); var u=fmtUntil(d.date);
            return html`<div class="hm-crow" key=${d.id}><span class="dot" style=${{background:c}}></span><span class="t">${d.title}</span><span class=${'hm-cpill'+(d.date<=ymd(addDays(parseYmd(TODAY),2))?' soon':'')} title=${shortDate(d.date)}>${u}</span></div>`; })
            :html`<div style=${{fontSize:'13px',color:'#4B5866'}}>No deadlines ahead.</div>`}
        </div>
        <div class="hm-sec"><div class="hm-shd"><h2>Tonight</h2></div><button type="button" class="hm-wide" onClick=${props.onGoJournal}>Write tonight’s journal</button></div>
      </aside>
      </div>

'''
assert OLD_TODAY_HEAD.count('${props.score?html`<${ScoreStrip}')==1
s = s.replace(OLD_TODAY_HEAD, NEW_TODAY_HEAD, 1)
# Today: local state for the quick add, the done fold, and the "just ticked" hold
rep('''    var cmS=useState(false); var carryAll=cmS[0], setCarryAll=cmS[1];''',
    '''    var cmS=useState(false); var carryAll=cmS[0], setCarryAll=cmS[1];
    var qaS=useState(''); var qa=qaS[0], setQa=qaS[1];
    var sdS=useState(false); var showDone=sdS[0], setShowDone=sdS[1];
    var bumpS=useState(0); var bump=bumpS[1];
    var wasOpen=useRef({}), heldAt=useRef({});
    // ticked a moment ago? keep it in the list for 1.6 s so the strike and the +points are seen
    (dayTasks||[]).forEach(function(t){ if(!t.done){ wasOpen.current[t.id]=1; delete heldAt.current[t.id]; } else if(wasOpen.current[t.id]){ delete wasOpen.current[t.id]; heldAt.current[t.id]=Date.now(); setTimeout(function(){ bump(function(x){return x+1;}); },1650); } });
    function kept(t){ var at=heldAt.current[t.id]; return !!at && Date.now()-at<1600; }''')
rep('''    var dayTasks=tops.concat(loneSubs);
''', '''    var dayTasks=tops.concat(loneSubs);
''')  # (anchor check only)

# App: quick add for a day, and pass it in
rep('''    function addProjectItem(pid,title,due){''', '''    function quickAdd(title,ds){ var t=baseTask({ title:title.trim(), date:ds||TODAY }); commit([{op:'upsert',table:'tasks',row:t,_label:t.title}]); }
    function addProjectItem(pid,title,due){''')
rep('''onOpenWeek=${function(){setView2('week');}} /><//>`; }''', '''onOpenWeek=${function(){setView2('week');}} onQuickAdd=${quickAdd} /><//>`; }''')

# ---------------------------------------------------------------- Calendar → Day mode
rep('''    var modeS=useState('week'); var mode=modeS[0], setMode=modeS[1];''',
    '''    var modeS=useState(function(){ var m=lsGet('sp_calmode','week'); return ['day','week','month','timeline'].indexOf(m)>=0?m:'week'; }); var mode=modeS[0], setMode0=modeS[1];
    function setMode(m){ setMode0(m); lsSet('sp_calmode',m); }
    var dragS=useState(null); var dragOver=dragS[0], setDragOver=dragS[1];
    var dvRef=useRef(null);''')
rep('''      <div class="seg"><button class=${mode==='week'?'on':''} onClick=${function(){setMode('week');}}>Week</button>''',
    '''      <div class="seg"><button class=${mode==='day'?'on':''} onClick=${function(){setMode('day');}}>Day</button><button class=${mode==='week'?'on':''} onClick=${function(){setMode('week');}}>Week</button>''')
rep('''      <button class="navcirc" aria-label="Previous" onClick=${function(){setCur(mode==='week'?addDays(cur,-7):addMonths(cur,-1));}}>${chevL}</button>
      <button class="navcirc" aria-label="Next" onClick=${function(){setCur(mode==='week'?addDays(cur,7):addMonths(cur,1));}}>${chevR}</button>''',
    '''      <button class="navcirc" aria-label=${mode==='day'?'Previous day':'Previous'} onClick=${function(){setCur(mode==='day'?addDays(cur,-1):mode==='week'?addDays(cur,-7):addMonths(cur,-1));}}>${chevL}</button>
      <button class="navcirc" aria-label=${mode==='day'?'Next day':'Next'} onClick=${function(){setCur(mode==='day'?addDays(cur,1):mode==='week'?addDays(cur,7):addMonths(cur,1));}}>${chevR}</button>''')
rep('''${mode==='week'?('Week of '+shortDate(ymd(startOfWeek(cur)))):monthY(cur)}</span>''',
    '''${mode==='day'?longDay(cur):mode==='week'?('Week of '+shortDate(ymd(startOfWeek(cur)))):monthY(cur)}</span>''')

DAY = r'''
    // ---- Day: one day by the hour, with what has no time beside it ----
    if(mode==='day'){
      var ds=ymd(cur), isTd=ds===TODAY, me=VIEW.who;
      var DH0=7, DH1=23, DROW=48;
      var rts=(props.routines||[]).filter(function(r){ return (!r.days||r.days==='daily') && r.start && r.end; });
      var tItems=timed(ds).map(function(t){ var p=t.time.split(':'), st=(+p[0])*60+(+p[1]); return {t:t, st:st, en:st+(isEventType(t.type)?60:45)}; });
      var rItems=rts.map(function(r){ var a=r.start.split(':'), b=r.end.split(':'); return {r:r, st:(+a[0])*60+(+a[1]), en:(+b[0])*60+(+b[1])}; }).filter(function(x){ return x.en>x.st; });
      var items=rItems.concat(tItems).sort(function(a,b){ return a.st-b.st||b.en-a.en; });
      // side by side when two things overlap
      var lanesEnd=[], cluster=[], clusterEnd=-1;
      function closeCluster(){ var n=Math.max(1,lanesEnd.length); cluster.forEach(function(x){ x.lanes=n; }); cluster=[]; lanesEnd=[]; }
      items.forEach(function(x){ if(x.st>=clusterEnd) closeCluster(); var l=0; while(l<lanesEnd.length&&lanesEnd[l]>x.st) l++; lanesEnd[l]=x.en; x.lane=l; cluster.push(x); clusterEnd=Math.max(clusterEnd,x.en); });
      closeCluster();
      var hasTimed=items.length>0, fold=!hasTimed&&!showHours;
      var anyT=allday(ds).filter(function(t){ return !isEventType(t.type); }).sort(function(a,b){ return (a.done?1:0)-(b.done?1:0); });
      var anyOpen=anyT.filter(function(t){ return !t.done; });
      var evAll=allday(ds).filter(function(t){ return isEventType(t.type); });
      var dueD=dues(ds);
      var projD=(projects||[]).filter(function(p){ return !p.archived && projPass(p) && (p.end_date===ds||p.start_date===ds); });
      var nowD=new Date(), nowMin=nowD.getHours()*60+nowD.getMinutes();
      var showNowD=isTd && nowMin>=DH0*60 && nowMin<=DH1*60;
      var hrs=[]; for(var h2=DH0;h2<DH1;h2++){ hrs.push(h2); }
      function y(min){ return (min/60-DH0)*DROW; }
      function hm(min){ return pad2(Math.floor(min/60))+':'+pad2(min%60); }
      function who(o){ return (o&&o!==me&&o!==EVERYONE)?' pt':''; }
      function kindOf(x){ if(x.r) return 'rt'; if(x.t.done) return 'dn'; if(isEventType(x.t.type)) return 'ev'+who(x.t.owner); return who(x.t.owner)||''; }
      function body(x){
        if(x.r) return html`<span class="dv-ic" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M17 2l3 3-3 3M4 11V9a4 4 0 014-4h12M7 22l-3-3 3-3M20 13v2a4 4 0 01-4 4H4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg></span><span class="bx"><span class="bt">${x.r.title}</span> <span class="bs">${x.r.start}–${x.r.end}</span></span>`;
        var t=x.t, ev=isEventType(t.type);
        return html`${ev?null:html`<${Check} sm=${true} done=${t.done} label=${t.title} onClick=${function(e){ e.stopPropagation(); props.onToggle(t); }} />`}<span class="bx"><span class="bt">${t.title}</span> <span class="bs">${t.time}</span></span><${Avatar} owner=${t.owner} />`;
      }
      function onDropAt(e,time){ e.preventDefault(); setDragOver(null); var id=e.dataTransfer.getData('text/plain'); var t=(tasks||[]).filter(function(x){ return x.id===id; })[0]; if(t) props.onSchedule(t,ds,time); }
      function dragRow(t){ return {draggable:true, onDragStart:function(e){ e.dataTransfer.setData('text/plain',t.id); e.dataTransfer.effectAllowed='move'; }}; }
      function sideRow(t){ var p=projMap[t.project]; var dr=dragRow(t);
        return html`<div class=${'dv-row'+(selId===t.id?' sel':'')} key=${t.id} draggable=${dr.draggable} onDragStart=${dr.onDragStart} onClick=${function(){ setSel(selId===t.id?null:t.id); }} title="Drag onto an hour, or click it and then an hour">
          <span class="dv-grip" aria-hidden="true"><svg width="14" height="14" viewBox="0 0 24 24" fill="none"><circle cx="9" cy="6" r="1.4" fill="currentColor"/><circle cx="15" cy="6" r="1.4" fill="currentColor"/><circle cx="9" cy="12" r="1.4" fill="currentColor"/><circle cx="15" cy="12" r="1.4" fill="currentColor"/><circle cx="9" cy="18" r="1.4" fill="currentColor"/><circle cx="15" cy="18" r="1.4" fill="currentColor"/></svg></span>
          <${Check} sm=${true} done=${t.done} label=${t.title} onClick=${function(e){ e.stopPropagation(); props.onToggle(t); }} />
          ${p?html`<span class="dot" style=${{background:p.color}} title=${p.name}></span>`:null}
          <span class=${'t'+(t.done?' done':'')} onDblClick=${function(e){ e.stopPropagation(); props.onEditTask(t); }}>${t.title}</span>
          ${t.due&&!t.done?html`<span class=${'hm-cpill'+(t.due<=TODAY?' soon':'')}>${fmtUntil(t.due)}</span>`:null}
          <${Avatar} owner=${t.owner} />
        </div>`; }
      var allDayRow=html`<div class="dv-allday"><span class="k">All day</span>
        ${dueD.map(function(t){ return html`<button class="dv-chip" key=${'d'+t.id} onClick=${function(){props.onEditTask(t);}}>${t.title} · due${t.owner!==me?html` <${Avatar} owner=${t.owner} />`:null}</button>`; })}
        ${projD.map(function(p){ return html`<button class="dv-chip proj" key=${'p'+p.id} onClick=${function(){props.onOpenProject(p.id);}}><span class="dot" style=${{background:p.color}}></span>${p.name} · ${p.end_date===ds?'deadline':'starts'}</button>`; })}
        ${evAll.map(function(t){ return html`<button class="dv-chip ev" key=${'e'+t.id} onClick=${function(){props.onEditTask(t);}}>${t.title}</button>`; })}
        ${!dueD.length&&!projD.length&&!evAll.length?html`<span style=${{color:'#4B5866'}}>Nothing due ${isTd?'today':'this day'}</span>`:null}
      </div>`;
      var gridTl = fold ? html`<section class="dv-empty" aria-label=${longDay(cur)+' by the hour'}>
          <h3>Nothing has a time on ${longDay(cur).split(',')[0]}</h3>
          <p>That’s normal for you two. Drag a task from the right onto the day to give it a time, or add one with a time.</p>
          <div class="row"><button class="btn ghost" style=${{padding:'8px 14px'}} onClick=${function(){ var hNext=Math.min(DH1-1,Math.max(DH0,nowD.getHours()+1)); props.onAddSlot(ds,pad2(hNext)+':00'); }}>+ Add with a time</button><button class="btn ghost" style=${{padding:'8px 14px'}} onClick=${function(){setShowHours(true);}}>Show the hours</button></div>
        </section>`
        : html`<div class="dv-tl" ref=${dvRef}><div class="dv-hours" style=${{height:((DH1-DH0)*DROW)+'px'}}>
          ${hrs.map(function(h){ var tm=pad2(h)+':00'; return html`<div class="dv-hr" key=${h} style=${{height:DROW+'px'}}><span class="lab">${tm}</span><div class=${'slot'+(dragOver===tm?' drop':'')} onClick=${function(){ slotClick(ds,tm); }} onDragOver=${function(e){ e.preventDefault(); if(dragOver!==tm) setDragOver(tm); }} onDragLeave=${function(){ if(dragOver===tm) setDragOver(null); }} onDrop=${function(e){ onDropAt(e,tm); }}></div></div>`; })}
          ${items.map(function(x){ var top=Math.max(0,y(x.st))+2, ht=Math.max(26,(x.en-x.st)/60*DROW-4), short=ht<40; var k=kindOf(x);
            var st={top:top+'px',height:ht+'px',left:'calc(62px + (100% - 70px) * '+(x.lane/x.lanes)+')',width:'calc((100% - 70px) / '+x.lanes+' - 4px)'};
            return x.r ? html`<div class=${'dv-b rt'+(short?' short':'')} key=${'r'+x.r.id} style=${st}>${body(x)}</div>`
                       : html`<button type="button" class=${'dv-b '+k+(short?' short':'')} key=${x.t.id} style=${st} onClick=${function(){ props.onEditTask(x.t); }}>${body(x)}</button>`; })}
          ${showNowD?html`<div class="dv-now" style=${{top:y(nowMin)+'px'}}><i></i><b>${hm(nowMin)}</b></div>`:null}
        </div></div>`;
      // the phone: the same day as a list of times
      var listRows=[]; var nowPlaced=!showNowD;
      items.forEach(function(x){ if(!nowPlaced&&x.st>nowMin){ listRows.push(html`<div class="dv-linow" key="now"><b>${hm(nowMin)}</b><span><i></i></span></div>`); nowPlaced=true; }
        var k=kindOf(x); listRows.push(html`<div class="dv-li" key=${x.r?('r'+x.r.id):x.t.id}><span class="tm">${hm(x.st)}</span>${x.r?html`<div class="dv-b rt">${body(x)}</div>`:html`<button type="button" class=${'dv-b '+k} onClick=${function(){ props.onEditTask(x.t); }}>${body(x)}</button>`}</div>`); });
      if(!nowPlaced&&items.length) listRows.push(html`<div class="dv-linow" key="now"><b>${hm(nowMin)}</b><span><i></i></span></div>`);
      var w0=startOfWeek(cur), strip=[]; for(var si=0;si<7;si++){ strip.push(addDays(w0,si)); }
      var dayMain = html`<${Fragment}>
        ${toolbar}
        <div class="dv-strip" role="group" aria-label="Pick a day">${strip.map(function(d){ var dd=ymd(d); return html`<button key=${dd} class=${dd===ds?'on':''} aria-current=${dd===TODAY?'date':null} onClick=${function(){ setCur(d); }}>${DOWL[d.getDay()]}<b>${d.getDate()}</b></button>`; })}</div>
        <div class="dv-grid">
          <div>${allDayRow}${gridTl}${hasTimed?html`<div class="dv-list">${listRows}</div>`:(fold?null:html`<div class="dv-list"><p style=${{fontSize:'13px',color:'#4B5866'}}>Nothing has a time yet.</p></div>`)}</div>
          <aside class="dv-side" aria-label="Not on the clock">
            <section class="box"><div class="hd"><h2>${isTd?'Anytime today':'Anytime'} · ${anyOpen.length}</h2><button class="view" onClick=${function(){ props.onAddDay(ds); }}>+ Add</button></div>
              ${anyT.length?anyT.map(sideRow):html`<p style=${{fontSize:'12.5px',color:'#4B5866',margin:'2px 6px 8px'}}>Nothing else on this day.</p>`}</section>
            <section class="box"><div class="hd"><h2>To schedule · ${unsched.length}</h2><span class="m">no day yet</span></div>
              ${unsched.length?unsched.map(sideRow):html`<p style=${{fontSize:'12.5px',color:'#4B5866',margin:'2px 6px 8px'}}>Every task has a day.</p>`}</section>
            <div class="dv-hint">${selTask?html`<span>Now click an hour to place “${selTask.title}”. <button class="linkbtn" style=${{padding:0}} onClick=${function(){setSel(null);}}>cancel</button></span>`:html`<span>Drag a task onto an hour to give it a time, or click it and then an hour.</span>`}</div>
          </aside>
        </div>
      <//>`;
      return dayMain;
    }
'''
rep('''    var main;
    if(mode==='month'){''', DAY + '''    var main;
    if(mode==='month'){''')
# open the day grid at the first item or at the current hour
rep('''      el.scrollTop=Math.max(0,((first!=null?first:new Date().getHours())-H0)*ROW-24); },[mode, ymd(cur), showHours]);''',
    '''      el.scrollTop=Math.max(0,((first!=null?first:new Date().getHours())-H0)*ROW-24); },[mode, ymd(cur), showHours]);
    useEffect(function(){ var el=dvRef.current; if(!el||mode!=='day') return; var ds0=ymd(cur), first=null;
      timed(ds0).forEach(function(t){ var hh=+t.time.split(':')[0]; if(first==null||hh<first) first=hh; });
      (props.routines||[]).forEach(function(r){ if(r.start&&(!r.days||r.days==='daily')){ var hh=+r.start.split(':')[0]; if(first==null||hh<first) first=hh; } });
      var target=ds0===TODAY?Math.max(7,new Date().getHours()-2):(first!=null?first:9);
      el.scrollTop=Math.max(0,(target-7)*48-8); },[mode, ymd(cur), showHours]);''')
rep('''onSchedule=${scheduleTask} onNewProject=${function(s,e){setPEdit({start_date:s,end_date:e});}} />`; }''',
    '''onSchedule=${scheduleTask} onNewProject=${function(s,e){setPEdit({start_date:s,end_date:e});}} routines=${routines} />`; }''')

# ---------------------------------------------------------------- Settings › Claude
rep('''            <button class=${tab==='notifs'?'on':''} onClick=${function(){setTab('notifs');}}>Notifications</button>
          </div>''', '''            <button class=${tab==='notifs'?'on':''} onClick=${function(){setTab('notifs');}}>Notifications</button>
            <button class=${tab==='claude'?'on':''} onClick=${function(){setTab('claude');}}>Claude<span class="cl-new">New</span></button>
          </div>''')
rep('''({people:'Account',habits:'Habits',notifs:'Notifications',appearance:'Appearance',about:'About & sharing'})[tab]''',
    '''({people:'Account',habits:'Habits',notifs:'Notifications',claude:'Claude',appearance:'Appearance',about:'About & sharing'})[tab]''')
rep('''          ${tab==='people'?html`<${Fragment}>
            <label class="lbl" style=${{marginTop:0}} for="acct-name">Your name</label>''',
    '''          ${tab==='claude'?html`<${ClaudeSettings} />`:null}
          ${tab==='people'?html`<${Fragment}>
            <label class="lbl" style=${{marginTop:0}} for="acct-name">Your name</label>''')
rep('''  function HabitEditor(props){''', r'''  // Settings › Claude: your private connector link (the worker's /api/claude and /mcp)
  function ClaudeSettings(){
    var dS=useState(null); var d=dS[0], setD=dS[1];
    var eS=useState(''); var err=eS[0], setErr=eS[1];
    var bS=useState(false); var busy=bS[0], setBusy=bS[1];
    var cS=useState(false); var copied=cS[0], setCopied=cS[1];
    var aS=useState(false); var asking=aS[0], setAsking=aS[1];
    function call(body){ setBusy(true); setErr('');
      return fetch('/api/claude',body?{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body),credentials:'same-origin'}:{credentials:'same-origin'})
        .then(function(r){ if(!r.ok) throw new Error(r.status); return r.json(); })
        .then(function(j){ setD(j); setBusy(false); setAsking(false); })
        .catch(function(){ setErr('Couldn’t reach hate club. Check your connection and try again.'); setBusy(false); }); }
    useEffect(function(){ call(null); },[]);
    function copy(){ if(!d||!d.link) return; var done=function(){ setCopied(true); setTimeout(function(){ setCopied(false); },1800); };
      try{ navigator.clipboard.writeText(d.link).then(done,function(){ var el=document.getElementById('cl-link'); if(el){ el.value=d.link; el.select(); document.execCommand('copy'); done(); } }); }catch(e){} }
    var masked=d&&d.link?d.link.replace(/(\/mcp\/hc_)[^.]+\.([0-9a-f]{36})([0-9a-f]{4})$/,'$1••••••••••••$3'):'';
    function when(ms){ if(!ms) return ''; var dd=new Date(ms), ds=dayOfMs(ms); return (ds===TODAY?'Today':shortDate(ds))+' '+pad2(dd.getHours())+':'+pad2(dd.getMinutes()); }
    var warn=html`<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M12 3l9.5 17h-19L12 3z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 10v4M12 17h.01" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>`;
    return html`<${Fragment}>
      <p class="cl-p">Let Claude add your tasks and tick them off when you tell it they’re done. It acts as you, so the points are yours.</p>
      ${err?html`<div class="cl-note" role="alert">${warn}<span>${err} <button class="linkbtn" style=${{padding:0}} onClick=${function(){ call(null); }}>Try again</button></span></div>`:null}
      ${!d&&!err?html`<p class="cl-p" aria-live="polite">Loading…</p>`:null}
      ${d&&!d.active?html`<div style=${{marginTop:'14px'}}><button class="btn primary" style=${{padding:'9px 16px'}} disabled=${busy} onClick=${function(){ call({action:'new'}); }}>${busy?'Making your link…':'Make my private link'}</button></div>`:null}
      ${d&&d.active?html`<${Fragment}>
        <label class="lbl" for="cl-link">Your private link</label>
        <div class="cl-link"><input id="cl-link" type="text" readonly value=${masked} onFocus=${function(e){ e.target.value=d.link; e.target.select(); }} onBlur=${function(e){ e.target.value=masked; }} /><button class="btn primary" style=${{flex:'none',padding:'9px 16px'}} onClick=${copy}>${copied?'Copied':'Copy'}</button></div>
        <span class="sr" aria-live="polite">${copied?'Link copied':''}</span>
        <div class="cl-note">${warn}<span><b>Anyone with this link can add and finish tasks as you.</b> Keep it to yourself. If it leaks, make a new one and the old one stops working.</span></div>
        <label class="lbl">Add it to Claude</label>
        <ol class="cl-steps"><li>In Claude, open Settings › Connectors › Add custom connector.</li><li>Name it <b>hate club</b> and paste the link.</li><li>Ask it: “add ‘call Pratul’ for tomorrow”, or “I finished the SOP draft”.</li></ol>
        <label class="lbl">Claude can</label>
        <div class="cl-can"><span>See your tasks</span><span>Add a task</span><span>Tick a task off</span><span>Reopen a task</span><span>Move a task to another day</span></div>
        <label class="lbl">Last used</label>
        <div style=${{fontSize:'13px',color:'#15171A'}}>${d.last_used_at?(when(d.last_used_at)+(d.last_action?(' · '+d.last_action):'')):'Not yet'}</div>
        <div class="cl-foot">
          ${asking?html`<${Fragment}><span style=${{fontSize:'13px',color:'#15171A'}}>The old link stops working. Make a new one?</span><button class="btn primary" style=${{padding:'7px 14px'}} disabled=${busy} onClick=${function(){ call({action:'new'}); }}>Make a new link</button><button class="btn ghost" style=${{padding:'7px 14px'}} onClick=${function(){ setAsking(false); }}>Cancel</button><//>`
            :html`<${Fragment}><button class="btn ghost" style=${{padding:'8px 14px'}} disabled=${busy} onClick=${function(){ setAsking(true); }}>Make a new link</button><button class="btn ghost cl-danger" style=${{padding:'8px 14px'}} disabled=${busy} onClick=${function(){ call({action:'off'}); }}>Turn off</button><//>`}
        </div>
      <//>`:null}
    <//>`;
  }

  function HabitEditor(props){''')

open(P, 'w').write(s)
print('patched', len(s))
