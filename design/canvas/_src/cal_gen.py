#!/usr/bin/env python3
# Round 2: H1 with today's habit cards + notes; Calendar day view (+ empty day, phone); Settings › Claude.
import json
SRC = open('/private/tmp/claude-501/-Users-design-trueleap-plus/3e91a764-b2d1-4c81-aa33-4932c9d49dbd/scratchpad/home_gen.py').read().split('# ---------------- write')[0]
exec(SRC)
_full = open('/private/tmp/claude-501/-Users-design-trueleap-plus/3e91a764-b2d1-4c81-aa33-4932c9d49dbd/scratchpad/home_gen.py').read()
exec(_full.split('# ---------------- write')[1].split('\n',1)[1].split('VERS = [')[0])

# ---- today's habit cards + notes, as the app draws them now ----
HAB_CSS = """
.sech{display:flex;justify-content:space-between;align-items:baseline;margin:30px 2px 0}
.sech h3{margin:0;font-size:15px;font-weight:700;color:#15171A}
.view{font-weight:500;font-size:12.5px;color:#195FD0;background:none;border:none;padding:0}
.habs{display:flex;gap:14px;flex-wrap:wrap;margin-top:12px}
.habcard{background:#fff;border:1px solid #E5EAF1;border-radius:18px;padding:18px 20px;box-sizing:border-box}
.hbig{font-weight:700;font-size:34px;color:#2B3440;font-variant-numeric:tabular-nums}
.stepbtn{width:44px;height:44px;border-radius:999px;border:1px solid #DCE3EC;background:#fff;font-size:20px;color:#15171A;line-height:1;padding:0}
.bars{display:flex;align-items:flex-end;gap:6px;height:42px;margin-top:14px}
.bars i{flex:1;border-radius:4px;background:#DCE6F3;display:block}
.bars i.now{background:#1F6FEB}
.hsub{font-weight:400;font-size:11.5px;color:#5E6875}
.drow{display:flex;align-items:center;gap:11px;padding:8px 0}
.notesgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(176px,1fr));gap:14px;margin-top:12px}
.notecd{border:1px solid;border-radius:16px;padding:13px 14px 12px;min-height:148px;box-sizing:border-box;display:flex;flex-direction:column;box-shadow:0 2px 8px rgba(80,70,20,.06);font-size:14px;line-height:1.5}
.addnote{border:1.5px dashed #CBD6E6;background:rgba(255,255,255,.5);border-radius:16px;min-height:148px;display:flex;align-items:center;justify-content:center;gap:8px;font-weight:600;font-size:14px;color:#195FD0}
"""
def habits_cards(phone=False):
    vals=[6,5,7,4,5,4,3]; mx=7
    bars=''.join(f'<i class="{"now" if i==6 else ""}" style="height:{max(8,round(v/mx*100))}%"></i>' for i,v in enumerate(vals))
    count=f'''<section class="habcard" style="flex:2 1 300px;min-width:260px" aria-label="Cigarettes">
<div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-weight:600;font-size:14px">Cigarettes</span><button type="button" class="view">Edit</button></div>
<div class="hsub" style="margin-top:2px;font-weight:500">5 → 1 a day by 30 Nov</div>
<div style="display:flex;align-items:flex-end;gap:12px;margin-top:8px"><div><span class="hbig">3</span><span class="hsub" style="font-size:12px;margin-left:6px;font-weight:500">today · aim ≤ 5</span></div>
<div style="margin-left:auto;display:flex;gap:8px"><button type="button" class="stepbtn" aria-label="One fewer">−</button><button type="button" class="stepbtn" aria-label="One more">+</button></div></div>
<div class="bars" aria-hidden="true">{bars}</div><div class="hsub" style="margin-top:7px">last 7 days</div></section>'''
    def drow(name, done, st):
        s = f'<span style="display:block" class="hsub"><span class="streak" style="font-weight:500">{IC["flame"]}</span>{st}-day streak</span>' if st else ''
        return f'<div class="drow">{chk(name,done)}<span style="flex:1;min-width:0"><span style="font-weight:500;font-size:13.5px">{name}</span>{s}</span><button type="button" class="view">Edit</button></div>'
    daily=f'''<section class="habcard" style="flex:1 1 240px;min-width:220px" aria-label="Daily habits"><span style="font-weight:600;font-size:14px">Daily</span>
{drow("Read · 1 hour",True,6)}{drow("Walk 8k steps",False,0)}{drow("No phone after 11",False,3)}</section>'''
    topic='''<section class="habcard" style="flex:1 1 200px;min-width:190px" aria-label="This week's topic">
<div style="display:flex;justify-content:space-between;align-items:baseline"><span style="font-weight:600;font-size:14px">This week's topic</span><button type="button" class="view">Edit</button></div>
<div style="font-weight:600;font-size:17px;letter-spacing:-.01em;margin-top:8px">Typography for screens</div>
<div class="hsub" style="font-size:12px;margin-top:4px">3 links saved</div></section>'''
    head_ = '<div class="sech"><h3>Habits &amp; focus</h3><button type="button" class="view">+ Add habit</button></div>'
    if phone: return head_ + f'<div class="habs">{daily}</div>'
    return head_ + f'<div class="habs">{count}{daily}{topic}</div>'

NOTES=[('#FFF3BE','#F1DE84','#6E5810','Ask Pratul if the SOP can go over 800 words.'),
       ('#FFE1EC','#F6C0D4','#8A2F55','Kimondo: try the warmer grey on the deck cover.'),
       ('#DCEBFF','#B9D4F6','#1C4E8A','Book the print shop for the zine before the 20th.')]
def notes_grid():
    h='<div class="sech"><h3>On your mind</h3><button type="button" class="view">+ Add note</button></div><div class="notesgrid">'
    for bg,bd,fg,t in NOTES: h+=f'<div class="notecd" style="background:{bg};border-color:{bd};color:{fg}">{t}</div>'
    return h+f'<button type="button" class="addnote"><span style="font-size:18px;line-height:1">+</span> Add a note</button></div>'

def h1v2_desktop():
    m = head('Today', score_pill()) + week()
    left = qadd()
    left += '<div class="ghd"><span class="lbl">From earlier · 1</span><a class="lnk" href="#">Move to today</a></div>' + CARRY
    left += '<div class="ghd"><span class="lbl">Today · 4 left</span><span class="muted" style="font-size:12.5px">2 routines</span></div>' + TODAY_ROWS
    left += f'<button type="button" class="donel">{IC["chevd"]}2 done today<span class="pts earned" style="margin-left:auto">+25</span></button>'
    rail = '<aside class="rail" aria-label="Around today">'
    rail += f'''<div class="rsec"><div class="rhd"><h2>Partner</h2><span class="av ap">P</span></div>
<div class="muted" style="font-size:13px;line-height:1.5">4 of 6 done today · <b style="color:#A3392C;font-weight:600">2 overdue</b></div>
<div style="display:flex;gap:8px;margin-top:10px"><button type="button" class="btns">{IC["hand"]}Give a hand · +5</button></div></div>'''
    rail += '<div class="rsec"><div class="rhd"><h2>Coming up</h2><a class="lnk" href="#">All tasks</a></div>'
    for n,d,dt in [('Statement of Purpose','1d','Fri 13 Nov'),('D&amp;AD New Blood','6d','Wed 18 Nov'),('Portfolio site','21d','Thu 3 Dec')]:
        rail += f'<div class="crow"><span class="dot" style="background:{PC[n]}"></span><span class="tt" style="flex:1">{n}</span><span class="pill {"soon" if d=="1d" else "calm"}">{d}</span></div>'
    rail += '</div>'
    rail += f'<div class="rsec"><div class="rhd"><h2>Tonight</h2></div><button type="button" class="btng" style="width:100%;justify-content:center">{IC["pen"]}Write tonight\'s journal</button></div>'
    rail += '</aside>'
    m += f'<div class="h1g"><section aria-label="Your day">{left}</section>{rail}</div>'
    m += habits_cards() + notes_grid() + wave()
    return m

def h1v2_phone():
    b = week(True) + qadd('Add a task')
    b += '<div class="ghd"><span class="lbl">From earlier · 1</span><a class="lnk" href="#">Move</a></div>' + CARRY.replace(proj('Portfolio site'),'')
    b += '<div class="ghd"><span class="lbl">Today · 4 left</span></div>'
    b += trow('Finish Statement of Purpose draft',None,'<span class="pill soon">Tomorrow</span>')
    b += trow('Kimondo moodboard v2',None,'','b')
    b += trow("Read 2 chapters for Pratul's class")
    b += f'<button type="button" class="donel">{IC["chevd"]}1 more · 2 done<span class="pts earned" style="margin-left:auto">+25</span></button>'
    b += habits_cards(True)
    pill = f'<a class="spill" href="#" style="padding:6px 10px">{IC["crown"]}6 behind</a>'
    return f'<div class="ph">{phtop(pill)}<div class="phbody">{b}</div>{tabs()}</div>'

# ---- Calendar · Day ----
CAL_CSS = H4_CSS + """
.cbar{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:20px}
.navb{width:30px;height:30px;border-radius:8px;border:1px solid #DCE3EC;background:#fff;color:#2F343B;display:inline-flex;align-items:center;justify-content:center;padding:0}
.dd{display:inline-flex;align-items:center;gap:8px;border:1px solid #DCE3EC;border-radius:99px;background:#fff;padding:6px 12px;font-size:12.5px;font-weight:500;color:#15171A}
.dttl{font-size:15px;font-weight:700;margin-left:6px}
.cg{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(280px,1fr);gap:24px;margin-top:16px;align-items:start}
.allday{display:flex;align-items:center;gap:10px;flex-wrap:wrap;border:1px solid #E5EAF1;border-radius:12px;padding:9px 12px;margin-bottom:10px;font-size:13px}
.allday .lbl{width:52px}
.b-pt{background:#F1F3F7;border:1px solid #D9DFE8}
.side3 .sbox{border:1px solid #E5EAF1;border-radius:14px;padding:4px 16px 12px;margin-bottom:14px}
.emptyday{border:1px dashed #C9D5E5;border-radius:14px;padding:56px 24px;text-align:center;background:#FBFCFE}
@media (max-width:1000px){.cg{grid-template-columns:1fr}}
"""
def cal_head(day_on=True):
    seg = '<div class="seg" role="group" aria-label="View">' + ''.join(f'<button type="button" class="{"on" if l=="Day" else ""}">{l}</button>' for l in ['Day','Week','Month','Timeline']) + '</div>'
    return f'''<div class="top"><div class="brandrow"><span class="mark">hc</span><div><div class="eyebrow">hate club</div><h1>Calendar</h1></div></div></div>
<div class="cbar">{seg}<button type="button" class="navb" aria-label="Previous day">{IC["chevl"]}</button><button type="button" class="navb" aria-label="Next day">{IC["chevr"]}</button><button type="button" class="btns">Today</button><span class="dttl">Thursday, 12 November</span>
<span style="flex:1"></span><button type="button" class="btns">{IC["plus"]}Project from dates</button><button type="button" class="dd">Everyone{IC["chevd"]}</button><button type="button" class="dd">All projects{IC["chevd"]}</button></div>'''

def side_lists():
    def arow(t,p,pill='',who='m'):
        return trow(t,None,pill,who).replace('<div class="trow">',f'<div class="trow"><span class="grip" aria-hidden="true">{IC["grip"]}</span>',1).replace('<span class="tt">',f'<span class="dot" style="background:{PC[p]}" title="{p}"></span><span class="tt">',1)
    s = '<aside class="side3" aria-label="Not on the clock">'
    s += '<section class="sbox"><div class="ghd" style="padding-top:12px"><h2>Anytime today · 4</h2><a class="lnk" href="#">+ Add</a></div>'
    s += arow('Reply to Sajal about the case study','Portfolio site','<span class="pill over">Since Tue</span>')
    s += arow('Finish Statement of Purpose draft','Statement of Purpose','<span class="pill soon">Tomorrow</span>')
    s += arow('Kimondo moodboard v2','Kimondo','','b')
    s += arow("Read 2 chapters for Pratul's class",'Assignments')
    s += '</section>'
    s += '<section class="sbox"><div class="ghd" style="padding-top:12px"><h2>To schedule · 2</h2><span class="muted" style="font-size:12.5px">no day yet</span></div>'
    s += arow('Find a printer for the zine','D&amp;AD New Blood','','p')
    s += arow('Book a call with Pratul','Assignments')
    s += '</section>'
    s += f'<div class="hint">{IC["grip"]}Drag anything onto an hour to give it a time, or onto another day in Week.</div>'
    return s + '</aside>'

def cal_day_desktop():
    m = cal_head()
    tl = '<div><div class="allday"><span class="lbl">All day</span>'
    tl += '<span class="pill soon">Statement of Purpose · due tomorrow</span><span class="pill calm"><span class="av ap" style="width:16px;height:16px;font-size:9px;box-shadow:none">P</span>Portfolio proofs to print · due</span></div>'
    tl += '<section class="tl" aria-label="Thursday by the hour">'
    for i,h in enumerate(range(8,22)):
        tl += f'<div class="hr" style="top:{i*HOUR+10}px"><span>{h:02d}:00</span></div>'
    tl += f'<div class="blk b-dn" style="top:{at(9)}px;height:{HOUR-6}px">{chk("D&amp;AD brief: pick a category",True)}<span class="bt tt done" style="font-weight:500">D&amp;AD brief: pick a category</span><span class="pts earned">+15</span><span class="av am">M</span></div>'
    tl += f'<div class="blk b-rt" style="top:{at(10)}px;height:{HOUR*2-4}px;right:50%"><span class="rt">{IC["repeat"]}</span><div><div class="bt">Studio</div><div class="bs">10:00–12:00 · every weekday</div></div></div>'
    tl += f'<div class="blk b-pt" style="top:{at(10,30)}px;height:{HOUR*2-4}px;left:calc(50% + 4px)"><span class="av ap">P</span><div><div class="bt">Print shop · proofs</div><div class="bs">10:30–12:30 · Partner</div></div></div>'
    tl += f'<div class="blk b-cl" style="top:{at(14)}px;height:{HOUR*2-4}px"><span class="rt">{IC["repeat"]}</span><div><div class="bt">Class · Interaction design</div><div class="bs">14:00–16:00 · you both</div></div><span class="avs" style="margin-left:auto"><span class="av am">M</span><span class="av ap">P</span></span></div>'
    tl += f'<div class="blk b-fo" style="top:{at(16,20)}px;height:{round(HOUR*50/60)-4}px;color:#195FD0;align-items:center"><span class="rt" style="color:#195FD0">{IC["clock"]}</span><span class="bt">Focus · SOP draft</span><span class="bs" style="color:#195FD0">16:20–17:10 · planned</span></div>'
    tl += f'<div class="blk b-tk" style="top:{at(17,30)}px;height:{round(HOUR*0.75)}px">{chk("Call with the Kimondo team")}<span class="bt">Call with the Kimondo team</span><span class="bs">17:30</span><span class="avs" style="margin-left:auto"><span class="av am">M</span><span class="av ap">P</span></span></div>'
    tl += f'<div class="now" style="top:{at(15,10)}px"><b>15:10</b><i></i></div>'
    tl += '</section></div>'
    return m + f'<div class="cg">{tl}{side_lists()}</div>'

def cal_empty_desktop():
    m = cal_head()
    left = '<div><div class="allday"><span class="lbl">All day</span><span class="muted">Nothing due today</span></div>'
    left += f'''<section class="emptyday" aria-label="Thursday by the hour"><div style="font-size:16px;font-weight:700">Nothing has a time on Thursday</div>
<div class="muted" style="font-size:13.5px;margin-top:6px;line-height:1.5">That's normal for you two. Drag a task from the right onto the day to give it a time,<br>or add one with a time.</div>
<div style="display:flex;gap:10px;justify-content:center;margin-top:16px"><button type="button" class="btng">{IC["plus"]}Add with a time</button><button type="button" class="btng">Show the hours</button></div></section></div>'''
    return m + f'<div class="cg">{left}{side_lists()}</div>'

def cal_phone():
    seg = '<div class="seg" role="group" aria-label="View" style="display:flex;margin-top:12px">' + ''.join(f'<button type="button" class="{"on" if l=="Day" else ""}" style="flex:1">{l}</button>' for l in ['Day','Week','Month']) + '</div>'
    b = seg + week(True)
    def item(time, body, cls=''):
        return f'<div style="display:flex;gap:12px;align-items:stretch;padding:4px 0"><span class="tnum muted" style="width:44px;flex:none;font-size:12px;padding-top:9px;text-align:right">{time}</span><div class="blk {cls}" style="position:static;flex:1;min-width:0">{body}</div></div>'
    b += '<div style="margin-top:8px">'
    b += item('09:00', f'{chk("D&amp;AD brief",True)}<span class="tt done" style="font-weight:500">D&amp;AD brief: pick a category</span><span class="pts earned">+15</span>','b-dn')
    b += item('10:00', f'<span class="rt">{IC["repeat"]}</span><div><div class="bt">Studio</div><div class="bs">10:00–12:00</div></div>','b-rt')
    b += item('10:30', f'<span class="av ap">P</span><div><div class="bt">Print shop · proofs</div><div class="bs">Partner · 10:30–12:30</div></div>','b-pt')
    b += item('14:00', f'<span class="rt">{IC["repeat"]}</span><div><div class="bt">Class</div><div class="bs">14:00–16:00 · you both</div></div>','b-cl')
    b += '<div style="display:flex;align-items:center;gap:8px;margin:6px 0"><span style="width:44px;text-align:right;font-size:11px;font-weight:700;color:#195FD0" class="tnum">15:10</span><span style="flex:1;border-top:2px solid #1F6FEB;position:relative"><i style="position:absolute;left:-5px;top:-6px;width:10px;height:10px;border-radius:99px;background:#1F6FEB"></i></span></div>'
    b += item('16:20', f'<span class="rt" style="color:#195FD0">{IC["clock"]}</span><div><div class="bt" style="color:#195FD0">Focus · SOP draft</div><div class="bs" style="color:#195FD0">planned, 50 min</div></div>','b-fo')
    b += item('17:30', f'{chk("Call with the Kimondo team")}<span class="bt tt">Call with the Kimondo team</span>','b-tk')
    b += '</div><div class="ghd"><span class="lbl">Anytime today · 4</span><a class="lnk" href="#">+ Add</a></div>'
    b += trow('Reply to Sajal about the case study',None,'<span class="pill over">Tue</span>')
    b += trow('Finish Statement of Purpose draft',None,'<span class="pill soon">Tomorrow</span>')
    top = '<div class="phtop"><div class="brandrow" style="gap:12px"><span class="mark" style="width:36px;height:36px">hc</span><div><div class="eyebrow">hate club</div><h1>Calendar</h1></div></div>' + ADD_BTN + '</div>'
    return f'<div class="ph">{top}<div class="phbody">{b}</div>{tabs("Calendar")}</div>'

# ---- Settings › Claude ----
SET_CSS = """
.dim{width:1120px;height:720px;background:rgba(21,23,26,.38);display:flex;align-items:center;justify-content:center}
.modal{width:860px;background:#fff;border-radius:16px;box-shadow:0 24px 60px rgba(10,20,40,.28);display:flex;overflow:hidden}
.mrail{width:200px;flex:none;background:#F7F9FC;padding:18px 10px;box-sizing:border-box;border-right:1px solid #EEF2F7}
.mrail .grp{font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#4B5866;padding:14px 10px 4px}
.mrail .it{display:flex;align-items:center;gap:8px;width:100%;border:0;background:none;text-align:left;padding:7px 10px;border-radius:8px;font-size:13.5px;font-weight:500;color:#2F343B}
.mrail .it.on{background:#EAF1FD;color:#195FD0;font-weight:600}
.new{font-size:10px;font-weight:700;color:#1D6842;background:#E3F4EA;border-radius:99px;padding:1px 6px;margin-left:auto}
.mbody{flex:1;padding:20px 24px 22px;box-sizing:border-box;min-width:0}
.mlbl{font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#4B5866;margin:18px 0 7px}
.linkf{display:flex;gap:8px}
.linkf input{flex:1;min-width:0;border:1px solid #DCE3EC;border-radius:10px;padding:9px 12px;font:inherit;font-size:13px;color:#15171A;background:#F7F9FC;font-variant-numeric:tabular-nums}
.notice{display:flex;gap:10px;align-items:flex-start;border:1px solid #E5EAF1;background:#F7F9FC;border-radius:10px;padding:10px 12px;font-size:12.5px;color:#4B5866;margin-top:10px;line-height:1.45}
.notice b{color:#15171A;font-weight:600}
.steps{margin:0;padding-left:18px;font-size:13px;line-height:1.7;color:#2F343B}
.can{display:flex;flex-wrap:wrap;gap:6px}
.can span{font-size:12px;font-weight:500;border:1px solid #DCE3EC;border-radius:99px;padding:4px 10px;color:#2F343B}
.danger{color:#A3392C}
"""
def settings_claude():
    rail = '<nav class="mrail" aria-label="Settings"><div class="lbl" style="padding:0 10px">Settings</div><div class="grp">General</div>'
    rail += '<button type="button" class="it">Account</button><button type="button" class="it">Habits</button><button type="button" class="it">Notifications</button>'
    rail += '<button type="button" class="it on">Claude<span class="new">New</span></button>'
    rail += '<div class="grp">Personalize</div><button type="button" class="it">Appearance</button><div class="grp">About</div><button type="button" class="it">About &amp; sharing</button></nav>'
    warn = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" aria-hidden="true" style="flex:none;margin-top:1px;color:#B4792B"><path d="M12 3l9.5 17h-19L12 3z" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"></path><path d="M12 10v4M12 17h.01" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"></path></svg>'
    body = f'''<div class="mbody"><div style="display:flex;justify-content:space-between;align-items:center"><h2 style="font-size:17px">Claude</h2><button type="button" class="navb" aria-label="Close">×</button></div>
<div class="muted" style="font-size:13px;margin-top:4px;line-height:1.5">Let Claude add your tasks and tick them off when you tell it they're done. It acts as you, so the points are yours.</div>
<div class="mlbl">Your private link</div>
<div class="linkf"><label style="flex:1;display:flex"><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">Your private Claude link</span><input type="text" readonly value="https://shared-planner.mahesh-3dd.workers.dev/mcp/hc_••••••••••••3f9a"></label><button type="button" class="btnp">Copy</button></div>
<div class="notice">{warn}<span><b>Anyone with this link can add and finish tasks as you.</b> Keep it to yourself. If it leaks, make a new one and the old one stops working.</span></div>
<div class="mlbl">Add it to Claude</div>
<ol class="steps"><li>In Claude, open Settings › Connectors › Add custom connector.</li><li>Name it <b>hate club</b> and paste the link.</li><li>Ask it: "add 'call Pratul' for tomorrow", or "I finished the SOP draft".</li></ol>
<div class="mlbl">Claude can</div>
<div class="can"><span>See your tasks</span><span>Add a task</span><span>Tick a task off</span><span>Reopen a task</span><span>Move a task to another day</span></div>
<div class="mlbl">Last used</div><div style="font-size:13px">Today 15:02 · ticked off "Kimondo font licence"</div>
<div style="display:flex;gap:10px;margin-top:18px;padding-top:14px;border-top:1px solid #EEF2F7"><button type="button" class="btng">Make a new link</button><button type="button" class="btng danger">Turn off</button></div></div>'''
    return f'<div class="dim"><div class="modal" role="dialog" aria-label="Settings">{rail}{body}</div></div>'

BOARDS = [
 ('Home-H1-one-list.dc.html','H1 · One list (picked)', HAB_CSS+H1_CSS, lambda: desktop_page(h1v2_desktop()), 1440, 1500, 'H1-desktop'),
 ('Home-H1-phone.dc.html','H1 · phone', HAB_CSS+H1_CSS, h1v2_phone, 390, 844, 'H1-phone'),
 ('Calendar-day.dc.html','Calendar · Day', CAL_CSS, lambda: desktop_page(cal_day_desktop()).replace('<button type="button" class="nav on">','<button type="button" class="nav">').replace('<button type="button" class="nav">'+IC['cal'],'<button type="button" class="nav on">'+IC['cal']), 1440, 1000, 'cal-day'),
 ('Calendar-day-empty.dc.html','Calendar · Day, nothing timed', CAL_CSS, lambda: desktop_page(cal_empty_desktop()).replace('<button type="button" class="nav on">','<button type="button" class="nav">').replace('<button type="button" class="nav">'+IC['cal'],'<button type="button" class="nav on">'+IC['cal']), 1440, 760, 'cal-empty'),
 ('Calendar-day-phone.dc.html','Calendar · Day · phone', CAL_CSS, cal_phone, 390, 844, 'cal-phone'),
 ('Settings-claude.dc.html','Settings › Claude', CAL_CSS+SET_CSS, settings_claude, 1120, 720, 'settings-claude'),
]
for fn,title,css,f,w,h,pv in BOARDS:
    body=f()
    open(f'{ROOT}/project/{fn}','w').write(dc(title, css, body, w, h))
    open(f'{PREV}/{pv}.html','w').write(preview(title, css, body, w))
json.dump([[fn,title,w,h] for fn,title,css,f,w,h,pv in BOARDS], open(SP+'/cal_out.json','w'))
print('ok', [b[0] for b in BOARDS])
