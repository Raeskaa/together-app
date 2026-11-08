#!/usr/bin/env python3
# Builds the five Home versions (desktop + phone) as .dc.html artboards, plus plain preview pages.
import os, json, sys
SP = '/private/tmp/claude-501/-Users-design-trueleap-plus/3e91a764-b2d1-4c81-aa33-4932c9d49dbd/scratchpad'
ROOT = SP + '/home-canvas'
PREV = SP + '/home-preview'
os.makedirs(ROOT + '/project', exist_ok=True); os.makedirs(PREV, exist_ok=True)

FONT = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;display=swap" rel="stylesheet">'

BASE = """
body{margin:0;font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;color:#15171A;-webkit-font-smoothing:antialiased;background:#EAF3FF}
a{color:#195FD0;text-decoration:none}a:hover{color:#15171A}
button{font-family:inherit;cursor:pointer}
.app{display:flex;flex-wrap:wrap;align-items:stretch;min-height:960px;background:radial-gradient(1100px 760px at 78% 12%,rgba(255,255,255,.9),transparent 60%),radial-gradient(900px 680px at 12% 82%,rgba(255,255,255,.5),transparent 55%),linear-gradient(162deg,#3FA0FF 0%,#6FBAFF 20%,#A6D5FF 40%,#D6ECFF 62%,#F5FAFF 85%)}
.side{flex:1 0 232px;max-width:232px;box-sizing:border-box;padding:16px 10px;display:flex;flex-direction:column;gap:2px}
.prof{display:flex;align-items:center;gap:10px;padding:4px 10px 12px;font-weight:600;font-size:14px}
.pav{width:26px;height:26px;border-radius:99px;background:#15171A;color:#fff;font-size:11px;font-weight:600;display:inline-flex;align-items:center;justify-content:center}
.addb{display:flex;align-items:center;gap:10px;padding:7px 10px;font-weight:600;font-size:14px;color:#195FD0;border:0;background:none;text-align:left}
.nav{display:flex;align-items:center;gap:11px;padding:7px 10px;border-radius:8px;font-size:14px;font-weight:500;color:#2F343B;border:0;background:none;width:100%;text-align:left;box-sizing:border-box}
.nav svg{color:#54606E;flex:none}
.nav.on{background:#fff;color:#195FD0;font-weight:600;box-shadow:0 1px 3px rgba(20,60,130,.12)}
.nav.on svg{color:#195FD0}
.cnt{margin-left:auto;font-size:12px;font-weight:500;color:#4B5866;font-variant-numeric:tabular-nums}
.sec{font-size:10.5px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#3C5F8C;padding:16px 10px 4px}
.dot{width:8px;height:8px;border-radius:99px;display:inline-block;flex:none}
.sfoot{margin-top:auto;display:flex;flex-direction:column;gap:2px;padding-top:12px}
.sfoot .nav{font-size:13.5px}
.club{display:flex;align-items:center;gap:8px;padding:10px 10px 4px;font-size:12px;color:#3F4B59}
.main{flex:999 1 560px;min-width:0;box-sizing:border-box;margin:10px;background:#fff;border:1px solid #E5EAF1;border-radius:16px;box-shadow:0 12px 40px rgba(20,60,130,.12);padding:28px 36px 44px;position:relative}
.top{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.brandrow{display:flex;align-items:center;gap:14px}
.mark{width:40px;height:40px;border-radius:11px;background:#15171A;color:#fff;font-weight:700;font-size:14px;display:flex;align-items:center;justify-content:center;letter-spacing:-.02em;flex:none}
.eyebrow{font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:#3C6FB0}
h1{margin:0;font-size:28px;font-weight:700;letter-spacing:-.02em;line-height:1.15}
h2{margin:0;font-size:15px;font-weight:700;letter-spacing:-.005em}
.btnp{display:inline-flex;align-items:center;gap:8px;border:0;border-radius:10px;background:#15171A;color:#fff;font-weight:600;font-size:13px;padding:9px 14px;white-space:nowrap}
.btng{display:inline-flex;align-items:center;gap:7px;border:1px solid #DCE3EC;border-radius:10px;background:#fff;color:#15171A;font-weight:600;font-size:13px;padding:8px 12px;white-space:nowrap}
.btns{display:inline-flex;align-items:center;gap:6px;border:1px solid #DCE3EC;border-radius:8px;background:#fff;color:#15171A;font-weight:600;font-size:12px;padding:5px 9px;white-space:nowrap}
.av{width:24px;height:24px;border-radius:99px;color:#fff;font-size:10.5px;font-weight:600;display:inline-flex;align-items:center;justify-content:center;flex:none;box-shadow:0 0 0 2px #fff}
.am{background:#15171A}.ap{background:#5B6B86}
.avs{display:inline-flex}.avs .av+.av{margin-left:-8px}
.pill{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:600;border-radius:99px;padding:3px 9px;white-space:nowrap}
.soon{color:#85560F;background:#FBF1E6}
.calm{color:#46505D;background:#EEF2F7}
.over{color:#A3392C;background:#FCEAE7}
.okp{color:#1D6842;background:#E3F4EA}
.muted{color:#4B5866}
.tnum{font-variant-numeric:tabular-nums}
.chk{width:18px;height:18px;border-radius:99px;border:1.6px solid #AEB8C5;background:#fff;flex:none;box-sizing:border-box;padding:0;display:inline-flex;align-items:center;justify-content:center}
.chk.on{background:#1F6FEB;border-color:#1F6FEB}
.seg{display:inline-flex;align-items:center;gap:2px;background:#F1F4F8;border-radius:999px;padding:3px}
.seg button{border:0;background:none;border-radius:999px;padding:6px 13px;font-weight:500;font-size:12.5px;color:#3A4350}
.seg button.on{background:#fff;color:#15171A;font-weight:600;box-shadow:0 1px 2px rgba(0,0,0,.08)}
.lbl{font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:#3C6FB0}
.lnk{font-size:12.5px;font-weight:600;color:#195FD0;display:inline-flex;align-items:center;gap:3px;white-space:nowrap}
/* week strip */
.wks{display:grid;grid-template-columns:auto repeat(7,minmax(0,1fr)) auto;gap:6px;align-items:center;margin-top:20px}
.wkn{width:28px;height:28px;border-radius:8px;border:0;background:none;color:#4B5866;display:flex;align-items:center;justify-content:center;padding:0}
.wd{border:0;background:none;border-radius:10px;padding:7px 0 6px;display:flex;flex-direction:column;align-items:center;gap:2px;font-size:11px;font-weight:600;color:#3C6FB0}
.wd b{font-size:15px;font-weight:600;color:#2F343B;font-variant-numeric:tabular-nums}
.wd i{width:4px;height:4px;border-radius:99px;background:#9DB3CF;display:block}
.wd i.no{background:transparent}
.wd.t{background:#EEF4FF}.wd.t b{color:#195FD0}.wd.t i{background:#1F6FEB}
/* rows */
.ghd{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:18px 2px 6px}
.trow{display:flex;align-items:center;gap:12px;padding:10px 2px;border-top:1px solid #EEF2F7;font-size:14px;min-height:24px}
.ghd+.trow{border-top:0}
.tt{flex:1;min-width:0;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tt.done{color:#6B7480;text-decoration:line-through;text-decoration-color:#AEB8C5}
.proj{display:inline-flex;align-items:center;gap:6px;font-size:12.5px;color:#4B5866;white-space:nowrap}
.time{width:92px;flex:none;font-size:12.5px;color:#4B5866;font-variant-numeric:tabular-nums;white-space:nowrap}
.rt{width:18px;height:18px;flex:none;display:inline-flex;align-items:center;justify-content:center;color:#3C6FB0}
.pts{font-size:12px;font-weight:600;color:#1D6842;font-variant-numeric:tabular-nums;white-space:nowrap}
.pts.earned{background:#E3F4EA;border-radius:99px;padding:2px 8px}
.qadd{display:flex;align-items:center;gap:10px;border:1px dashed #C9D5E5;border-radius:10px;padding:9px 12px;color:#4B5866;font-size:14px;margin-top:18px}
.qadd label{flex:1;display:flex}
.qadd input{flex:1;border:0;outline:0;font:inherit;background:transparent;color:#15171A;padding:0}
.qadd input::placeholder{color:#5E6875}
.kbd{font-size:11px;color:#4B5866;border:1px solid #DCE3EC;border-radius:5px;padding:1px 6px;font-weight:500}
.donel{display:flex;align-items:center;gap:8px;padding:11px 2px;border-top:1px solid #EEF2F7;font-size:13px;color:#4B5866;width:100%;border-left:0;border-right:0;border-bottom:0;background:none;text-align:left}
/* habits */
.hchips{display:flex;flex-wrap:wrap;gap:8px}
.hchip{display:inline-flex;align-items:center;gap:8px;border:1px solid #DCE3EC;border-radius:99px;padding:5px 12px 5px 6px;font-size:13px;font-weight:500;background:#fff;color:#15171A;white-space:nowrap;min-height:24px}
.hchip .chk{width:18px;height:18px}
.hchip.on{background:#F3F8FF;border-color:#BFD5F7}
.streak{display:inline-flex;align-items:center;gap:3px;font-size:12px;color:#A8501F;font-weight:600}
.step{width:24px;height:24px;border-radius:99px;border:1px solid #DCE3EC;background:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:14px;line-height:1;color:#15171A;padding:0}
.cnum{font-size:14px;font-weight:700;font-variant-numeric:tabular-nums}
.note{background:linear-gradient(180deg,#FFF3BE,#FFEEA6);border:1px solid #F1DE84;border-radius:12px;padding:10px 12px;font-size:13px;line-height:1.45;color:#3B3520}
.wave{position:absolute;right:24px;bottom:24px;width:44px;height:44px;border-radius:99px;border:1px solid #DCE3EC;background:#fff;box-shadow:0 6px 18px rgba(20,60,130,.14);display:flex;align-items:center;justify-content:center;color:#C2496B;padding:0}
.card{border:1px solid #E5EAF1;border-radius:14px;padding:4px 18px 10px;background:#fff}
.cardhd{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 0 6px}
/* race */
.track{position:relative;height:28px}
.track .ln{position:absolute;left:0;right:0;top:13px;height:2px;background:#E3E9F1;border-radius:2px}
.track .fl{position:absolute;right:-2px;top:5px;color:#4B5866}
.track .rn{position:absolute;top:2px;transform:translateX(-50%)}
.mbar{height:6px;border-radius:99px;background:#E8EDF4;position:relative;overflow:hidden}
.mbar i{position:absolute;left:0;top:0;bottom:0;border-radius:99px;display:block}
/* phone */
.ph{width:390px;height:844px;box-sizing:border-box;background:#fff;position:relative;overflow:hidden;display:flex;flex-direction:column}
.phtop{padding:16px 16px 0;display:flex;align-items:center;justify-content:space-between;gap:10px}
.phtop h1{font-size:24px}
.phbody{flex:1;overflow:hidden;padding:0 16px}
.tabs{display:flex;border-top:1px solid #E5EAF1;background:#FBFDFF;padding:8px 0 22px;flex:none}
.tab{flex:1;display:flex;flex-direction:column;align-items:center;gap:4px;border:0;background:none;font-size:10.5px;font-weight:500;color:#5E6875;min-height:44px}
.tab.on{color:#195FD0;font-weight:600}
.ph .wks{grid-template-columns:repeat(7,minmax(0,1fr));margin-top:14px;gap:2px}
.ph .trow{min-height:30px}
.addc{width:44px;height:44px;border-radius:99px;border:0;background:#15171A;color:#fff;display:flex;align-items:center;justify-content:center;padding:0;flex:none}
"""

def svg(d, w=16, sw=1.8, extra=''):
    return f'<svg width="{w}" height="{w}" viewBox="0 0 24 24" fill="none" aria-hidden="true">{d}</svg>'
def P(d, sw=1.8):
    return f'<path d="{d}" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"></path>'

IC = {
 'home': svg(P('M4 11.5 12 4.5l8 7M6 10v9a1 1 0 001 1h10a1 1 0 001-1v-9',1.7),18),
 'week': svg(P('M8 4h8v5a4 4 0 01-8 0V4zM8 6H5a3 3 0 003 4M16 6h3a3 3 0 01-3 4M12 13v4M8.5 20h7',1.7),18),
 'tasks': svg(P('M9 6h11M9 12h11M9 18h7',1.7)+P('M4 5.6l1.3 1.4L7.7 4M4 11.6l1.3 1.4L7.7 10',1.7),18),
 'cal': svg('<rect x="4" y="5" width="16" height="15" rx="2.5" stroke="currentColor" stroke-width="1.7"></rect>'+P('M4 9.5h16M8 3v4M16 3v4',1.7),18),
 'proj': svg(P('M4 7.5A1.5 1.5 0 015.5 6h3.2a1.5 1.5 0 011.2.6l.9 1.2a1.5 1.5 0 001.2.6H18.5A1.5 1.5 0 0120 9.9V18a1.5 1.5 0 01-1.5 1.5h-13A1.5 1.5 0 014 18V7.5z',1.6),18),
 'journal': svg(P('M5 4.5h10a2 2 0 012 2V20l-6-2.5V4.5z',1.7)+P('M5 4.5a2 2 0 00-2 2V18l2-.8',1.7),18),
 'more': svg('<circle cx="5" cy="12" r="1.7" fill="currentColor"></circle><circle cx="12" cy="12" r="1.7" fill="currentColor"></circle><circle cx="19" cy="12" r="1.7" fill="currentColor"></circle>',18),
 'clock': svg('<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.8"></circle>'+P('M12 7.5V12l3 2'),16),
 'help': svg('<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.7"></circle>'+P('M9.6 9.3a2.5 2.5 0 014.8.9c0 1.7-2.4 2-2.4 3.6M12 17h.01',1.7),18),
 'gear': svg('<circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="1.7"></circle>'+P('M12 3v2M12 19v2M3 12h2M19 12h2M5.6 5.6l1.4 1.4M17 17l1.4 1.4M5.6 18.4L7 17M17 7l1.4-1.4',1.7),18),
 'plus': svg(P('M12 5v14M5 12h14',2),16),
 'plusc': '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="#1F6FEB"></circle><path d="M12 8v8M8 12h8" stroke="#fff" stroke-width="2" stroke-linecap="round"></path></svg>',
 'tick': '<svg width="10" height="10" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2.5 6.2l2.2 2.2 4.8-5" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"></path></svg>',
 'crown': svg(P('M4 18l-1-10 5 4 4-7 4 7 5-4-1 10z'),14),
 'flame': svg(P('M12 3c1 3 4 4.6 4 9a4 4 0 01-8 0c0-2 1-3.2 1-3.2s.6 2.2 2 2.2c0-3-1.2-5 1-8z',1.9),12),
 'heart': svg(P('M12 20s-7-4.4-7-10a4 4 0 017-2.6A4 4 0 0119 10c0 5.6-7 10-7 10z',1.9),18),
 'chev': svg(P('M9 6l6 6-6 6',2),14),
 'chevl': svg(P('M15 6l-6 6 6 6',2),16),
 'chevr': svg(P('M9 6l6 6-6 6',2),16),
 'chevd': svg(P('M6 9l6 6 6-6',2),14),
 'hand': svg(P('M8 13V6.5a1.5 1.5 0 013 0V12M11 6.5V5a1.5 1.5 0 013 0v7M14 6.5a1.5 1.5 0 013 0V14a6 6 0 01-6 6h-.6a6 6 0 01-4.8-2.4L4.3 15a1.5 1.5 0 012.3-1.9L8 14.5',1.7),14),
 'flag': svg(P('M6 21V4M6 4h11l-2.2 4L17 12H6',1.8),16),
 'grip': svg(''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="currentColor"></circle>' for x in (9,15) for y in (6,12,18)),16),
 'repeat': svg(P('M17 2l3 3-3 3M4 11V9a4 4 0 014-4h12M7 22l-3-3 3-3M20 13v2a4 4 0 01-4 4H4',1.7),14),
 'bolt': svg(P('M13 3L5 13.5h6L10 21l8-10.5h-6L13 3z',1.7),16),
 'arrowr': svg(P('M5 12h14M13 6l6 6-6 6',1.9),14),
 'pen': svg(P('M4 20h4L19 9l-4-4L4 16v4z',1.7),14),
}

PROJECTS = [('Statement of Purpose','#2E9E6B','1d'),('D&amp;AD New Blood','#4F5B76','6d'),('Kimondo','#1F6FEB','10d'),('Assignments','#B0529E','13d'),('Portfolio site','#C2704B','21d')]
PC = {n:c for n,c,_ in PROJECTS}

def side():
    navs = [('home','Today','5',True),('week','This week','58 · 64',False),('tasks','Tasks','9',False),('cal','Calendar','',False),('proj','Projects','5',False),('journal','Journal','',False)]
    h = '<aside class="side" aria-label="Main">\n<div class="prof"><span class="pav">M</span>Mahesh</div>\n'
    h += f'<button type="button" class="addb">{IC["plusc"]}Add task</button>\n'
    for ic,l,c,on in navs:
        h += f'<button type="button" class="nav{" on" if on else ""}">{IC[ic]}{l}' + (f'<span class="cnt">{c}</span>' if c else '') + '</button>\n'
    h += '<div class="sec">Projects</div>\n'
    for n,c,d in PROJECTS:
        h += f'<button type="button" class="nav"><span class="dot" style="background:{c}"></span>{n}<span class="cnt">{d}</span></button>\n'
    h += '<div class="sfoot">'
    h += f'<button type="button" class="nav">{IC["clock"]}Focus timer</button>'
    h += f'<button type="button" class="nav">{IC["help"]}How it works</button>'
    h += f'<button type="button" class="nav">{IC["gear"]}Settings</button>'
    h += '<div class="club"><span class="avs"><span class="av am">M</span><span class="av ap">P</span></span>hate club</div></div>\n</aside>\n'
    return h

def head(title='Today', right=''):
    return f'''<div class="top">
<div class="brandrow"><span class="mark">hc</span><div><div class="eyebrow">Thursday, 12 November</div><h1>{title}</h1></div></div>
<div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">{right}<div class="seg" role="group" aria-label="Show"><button type="button" class="on">All</button><button type="button">Mine</button></div></div>
</div>\n'''

def week(phone=False):
    days = [('Mon',9,1),('Tue',10,1),('Wed',11,1),('Thu',12,1),('Fri',13,1),('Sat',14,0),('Sun',15,0)]
    h = '<nav class="wks" aria-label="Pick a day">'
    if not phone: h += f'<button type="button" class="wkn" aria-label="Last week">{IC["chevl"]}</button>'
    for d,n,has in days:
        lab = d[0] if phone else d
        h += f'<button type="button" class="wd{" t" if n==12 else ""}"' + (' aria-current="date"' if n==12 else '') + f'>{lab}<b>{n}</b><i class="{"" if has else "no"}"></i></button>'
    if not phone: h += f'<button type="button" class="wkn" aria-label="Next week">{IC["chevr"]}</button>'
    return h + '</nav>\n'

def chk(label, on=False):
    return f'<button type="button" class="chk{" on" if on else ""}" aria-label="Mark {label} {"not done" if on else "done"}">{IC["tick"] if on else ""}</button>'

def proj(n):
    return f'<span class="proj"><span class="dot" style="background:{PC[n]}"></span>{n}</span>'

def trow(title, p=None, pill='', who='m', done=False, pts='', time=''):
    av = {'m':'<span class="av am">M</span>','p':'<span class="av ap">P</span>','b':'<span class="avs"><span class="av am">M</span><span class="av ap">P</span></span>'}[who]
    h = '<div class="trow">'
    if time: h += f'<span class="time">{time}</span>'
    h += chk(title, done) + f'<span class="tt{" done" if done else ""}">{title}</span>'
    if p: h += proj(p)
    if pill: h += pill
    if pts: h += pts
    h += av + '</div>\n'
    return h

def routine(time, title, sub=''):
    return f'<div class="trow"><span class="rt">{IC["repeat"]}</span><span class="tt" style="color:#2F343B">{title}' + (f'<span class="muted" style="font-weight:400"> · {sub}</span>' if sub else '') + f'</span><span class="time" style="text-align:right;width:auto">{time}</span></div>\n'

def qadd(ph='Add a task for today'):
    return f'<div class="qadd">{IC["plus"]}<label><span style="position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)">New task</span><input type="text" placeholder="{ph}"></label><span class="kbd">Enter</span></div>\n'

def habits_chips(focus=True):
    h = '<div class="hchips">'
    h += f'<span class="hchip on">{chk("Read 1 hour", True)}Read 1 hour<span class="streak">{IC["flame"]}6</span></span>'
    h += f'<span class="hchip">{chk("Walk 8k steps")}Walk 8k steps</span>'
    h += f'<span class="hchip">{chk("No phone after 11")}No phone after 11<span class="streak">{IC["flame"]}3</span></span>'
    h += '<span class="hchip" style="padding-left:12px">Cigarettes <span class="cnum">3</span><span class="muted" style="font-size:12px">aim ≤ 5</span><button type="button" class="step" aria-label="One fewer">−</button><button type="button" class="step" aria-label="One more">+</button></span>'
    if focus: h += f'<button type="button" class="hchip" style="padding-left:10px;color:#195FD0;font-weight:600">{IC["clock"]}Focus 25 min</button>'
    return h + '</div>\n'

ADD_BTN = '<button type="button" class="addc" aria-label="Add a task">' + IC['plus'].replace('width="16" height="16"','width="20" height="20"') + '</button>'
def wave(): return f'<button type="button" class="wave" aria-label="Send Partner a wave">{IC["heart"]}</button>'

def tabs(on='Today'):
    items=[('home','Today'),('week','Week'),('cal','Calendar'),('proj','Projects'),('more','More')]
    big = lambda i: IC[i].replace('width="18" height="18"','width="20" height="20"')
    return '<nav class="tabs" aria-label="Main">' + ''.join('<button type="button" class="tab' + (' on' if l==on else '') + '">' + big(i) + l + '</button>' for i,l in items) + '</nav>\n'

def phtop(right):
    return f'<div class="phtop"><div class="brandrow" style="gap:12px"><span class="mark" style="width:36px;height:36px">hc</span><div><div class="eyebrow">Thu, 12 November</div><h1>Today</h1></div></div>{right}</div>\n'

def score_pill():
    return f'<a class="spill" href="#">{IC["crown"]}<span>Partner leads by 6</span><span class="muted tnum" style="font-weight:500">58 – 64</span>{IC["chev"]}</a>'

PILL_CSS = """.spill{display:inline-flex;align-items:center;gap:8px;border:1px solid #E5EAF1;background:#F7F9FC;border-radius:99px;padding:6px 12px;font-size:13px;font-weight:600;color:#15171A;white-space:nowrap}
.spill svg{color:#5B6B86}.spill:hover{border-color:#BFD5F7;color:#15171A}"""

TODAY_ROWS = (
    routine('10:00–13:00','Studio','Room 4') +
    trow('Finish Statement of Purpose draft','Statement of Purpose','<span class="pill soon">Due tomorrow</span>') +
    trow('Kimondo moodboard v2','Kimondo','', 'b') +
    trow("Read 2 chapters for Pratul's class",'Assignments') +
    routine('14:00–16:00','Class · Interaction design') +
    trow('Call with the Kimondo team','Kimondo','<span class="pill calm">17:30</span>','b')
)
CARRY = trow('Reply to Sajal about the case study','Portfolio site','<span class="pill over">Since Tue</span>')

# ---------------- H1 · One list ----------------
H1_CSS = PILL_CSS + """
.h1g{display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:44px;margin-top:4px}
.rail{border-left:1px solid #EEF2F7;padding-left:28px;padding-top:6px}
.rsec{padding:16px 0;border-top:1px solid #EEF2F7}
.rsec:first-child{border-top:0;padding-top:12px}
.rhd{display:flex;align-items:center;justify-content:space-between;margin-bottom:10px}
.crow{display:flex;align-items:center;gap:9px;font-size:13px;padding:5px 0}
.crow .tt{font-weight:500}
@media (max-width:1000px){.h1g{grid-template-columns:1fr}.rail{border-left:0;padding-left:0}}
"""
def h1_desktop():
    m = head('Today', score_pill()) + week()
    left = qadd()
    left += f'<div class="ghd"><span class="lbl">From earlier · 1</span><a class="lnk" href="#">Move to today</a></div>' + CARRY
    left += f'<div class="ghd"><span class="lbl">Today · 4 left</span><span class="muted" style="font-size:12.5px">2 routines</span></div>' + TODAY_ROWS
    left += f'<button type="button" class="donel">{IC["chevd"]}2 done today<span class="pts earned" style="margin-left:auto">+25</span></button>'
    left += '<div class="ghd" style="padding-top:22px"><span class="lbl">Habits</span><a class="lnk" href="#">+ Add habit</a></div>' + habits_chips()
    rail = '<aside class="rail" aria-label="Around today">'
    rail += f'''<div class="rsec"><div class="rhd"><h2>Partner</h2><span class="av ap">P</span></div>
<div class="muted" style="font-size:13px;line-height:1.5">4 of 6 done today · <b style="color:#A3392C;font-weight:600">2 overdue</b></div>
<div style="display:flex;gap:8px;margin-top:10px"><button type="button" class="btns">{IC["hand"]}Give a hand · +5</button></div></div>'''
    rail += '<div class="rsec"><div class="rhd"><h2>Coming up</h2><a class="lnk" href="#">All tasks</a></div>'
    for n,d,dt in [('Statement of Purpose','1d','Fri 13 Nov'),('D&amp;AD New Blood','6d','Wed 18 Nov'),('Portfolio site','21d','Thu 3 Dec')]:
        rail += f'<div class="crow"><span class="dot" style="background:{PC[n]}"></span><span class="tt" style="flex:1">{n}</span><span class="pill {"soon" if d=="1d" else "calm"}">{d}</span></div>'
    rail += '</div>'
    rail += '<div class="rsec"><div class="rhd"><h2>This week\'s topic</h2><a class="lnk" href="#">Open</a></div><div style="font-size:15px;font-weight:600">Typography for screens</div><div class="muted" style="font-size:12.5px;margin-top:3px">3 links saved</div></div>'
    rail += '<div class="rsec"><div class="rhd"><h2>On your mind</h2><a class="lnk" href="#">+ Note</a></div><div class="note">Ask Pratul if the SOP can go over 800 words.</div><div class="note" style="margin-top:8px">Kimondo: try the warmer grey on the deck cover.</div></div>'
    rail += f'<div class="rsec"><div class="rhd"><h2>Tonight</h2></div><button type="button" class="btng" style="width:100%;justify-content:center">{IC["pen"]}Write tonight\'s journal</button></div>'
    rail += '</aside>'
    m += f'<div class="h1g"><section aria-label="Your day">{left}</section>{rail}</div>' + wave()
    return m

def h1_phone():
    b = week(True) + qadd('Add a task')
    b += '<div class="ghd"><span class="lbl">From earlier · 1</span><a class="lnk" href="#">Move</a></div>' + CARRY.replace(proj('Portfolio site'),'')
    b += '<div class="ghd"><span class="lbl">Today · 4 left</span></div>'
    b += trow('Finish Statement of Purpose draft',None,'<span class="pill soon">Tomorrow</span>')
    b += trow('Kimondo moodboard v2',None,'','b')
    b += trow("Read 2 chapters for Pratul's class")
    b += routine('14:00','Class')
    b += trow('Call with the Kimondo team',None,'<span class="pill calm">17:30</span>','b')
    b += f'<button type="button" class="donel">{IC["chevd"]}2 done today<span class="pts earned" style="margin-left:auto">+25</span></button>'
    b += '<div class="ghd"><span class="lbl">Habits</span></div><div class="hchips" style="flex-wrap:nowrap;overflow:hidden">' + habits_chips(False)[len('<div class="hchips">'):]
    pill = f'<a class="spill" href="#" style="padding:6px 10px">{IC["crown"]}6 behind</a>'
    return f'<div class="ph">{phtop(pill)}<div class="phbody">{b}</div>{tabs()}</div>'

# ---------------- H2 · Me | Us ----------------
H2_CSS = """
.h2g{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:24px;margin-top:20px;align-items:start}
.us{background:#F7FAFF;border:1px solid #DDE8F7;border-radius:14px;padding:4px 18px 16px}
.us .sub{border-top:1px solid #E1EAF6;padding-top:14px;margin-top:14px}
.race{display:grid;grid-template-columns:92px 1fr 34px;align-items:center;gap:10px;font-size:13px;font-weight:600;margin-top:6px}
.race .tnum{text-align:right}
.days{display:grid;grid-template-columns:repeat(7,1fr);gap:8px;align-items:end;height:84px;margin-top:10px}
.days .c{display:flex;flex-direction:column;align-items:center;gap:5px;height:100%;justify-content:flex-end}
.days .bb{display:flex;gap:3px;align-items:flex-end;height:60px}
.days .bb i{width:9px;border-radius:3px 3px 0 0;display:block}
.days .c span{font-size:11px;font-weight:600;color:#4B5866}
.days .c.t span{color:#195FD0}
.days .e{width:21px;height:60px;border:1px dashed #C9D5E5;border-radius:4px;box-sizing:border-box}
.prow{display:flex;align-items:center;gap:10px;padding:9px 0;border-top:1px solid #E1EAF6;font-size:13.5px}
.prow:first-of-type{border-top:0}
.lg{display:inline-flex;align-items:center;gap:6px;font-size:12px;color:#4B5866;margin-right:12px}
.lg i{width:9px;height:9px;border-radius:3px;display:inline-block}
@media (max-width:1000px){.h2g{grid-template-columns:1fr}}
"""
def race_rows():
    return f'''<div class="race"><span style="display:flex;align-items:center;gap:7px"><span class="av am">M</span>You</span><div class="mbar" style="height:8px"><i style="width:58%;background:#15171A"></i></div><span class="tnum">58</span></div>
<div class="race"><span style="display:flex;align-items:center;gap:7px"><span class="av ap">P</span>Partner</span><div class="mbar" style="height:8px"><i style="width:64%;background:#5B6B86"></i></div><span class="tnum">64</span></div>'''
def h2_desktop():
    m = head('Today') + week()
    me = f'<section class="card" aria-label="My day"><div class="cardhd"><h2>My day</h2><span style="display:flex;align-items:center;gap:10px"><span class="muted" style="font-size:12.5px">4 left · 2 done</span><button type="button" class="btns" aria-label="Add a task">{IC["plus"]}Add</button></span></div>'
    me += '<div class="ghd" style="padding-top:8px"><span class="lbl">From earlier · 1</span><a class="lnk" href="#">Move to today</a></div>' + CARRY
    me += '<div class="ghd"><span class="lbl">Today</span></div>' + TODAY_ROWS
    me += f'<button type="button" class="donel">{IC["chevd"]}2 done today<span class="pts earned" style="margin-left:auto">+25</span></button>'
    me += '<div class="ghd" style="padding-top:18px"><span class="lbl">My habits</span><a class="lnk" href="#">+ Add</a></div>' + habits_chips() + '<div style="height:8px"></div></section>'
    us = '<section class="us" aria-label="Us this week">'
    us += f'<div class="cardhd"><h2>Us · race to 100</h2><a class="lnk" href="#">This week {IC["chev"]}</a></div>'
    us += race_rows()
    us += '<div class="muted" style="font-size:12.5px;margin-top:10px;line-height:1.5">Partner leads by 6, with 3 days left. Finishing the SOP draft on time (+15) puts you ahead.</div>'
    us += '<div class="sub"><div style="display:flex;justify-content:space-between;align-items:center"><span class="lbl">Points by day</span><span><span class="lg"><i style="background:#15171A"></i>You</span><span class="lg" style="margin-right:0"><i style="background:#5B6B86"></i>Partner</span></span></div><div class="days" aria-hidden="true">'
    for d,a,b,t in [('M',12,18,0),('T',20,14,0),('W',16,22,0),('T',10,10,1)]:
        us += f'<div class="c{" t" if t else ""}"><div class="bb"><i style="height:{a*2.6:.0f}px;background:#15171A"></i><i style="height:{b*2.6:.0f}px;background:#5B6B86"></i></div><span>{d}</span></div>'
    for d in ['F','S','S']:
        us += f'<div class="c"><div class="bb"><span class="e"></span></div><span>{d}</span></div>'
    us += '</div></div>'
    us += '<div class="sub"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px"><span class="lbl">Partner\'s day</span><span class="muted" style="font-size:12.5px">4 of 6 done</span></div>'
    for t,state in [('Email the Kimondo brief','Since Tue'),('Portfolio proofs to print','Since Wed')]:
        us += f'<div class="prow"><span class="chk" aria-hidden="true"></span><span class="tt">{t}</span><span class="pill over">{state}</span><button type="button" class="btns">{IC["hand"]}Give a hand · +5</button></div>'
    us += f'<div class="prow"><span class="chk" aria-hidden="true"></span><span class="tt">Assignments reading notes</span><span class="pill calm">Today</span></div>'
    us += f'<div class="prow"><span class="chk on" aria-hidden="true">{IC["tick"]}</span><span class="tt done">Kimondo copy deck</span><span class="pts earned">+15</span></div>'
    us += '</div>'
    us += '<div class="sub"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><span class="lbl">Coming up</span><a class="lnk" href="#">All</a></div>'
    for n,d,dt in [('Statement of Purpose','1d','Fri 13 Nov'),('D&amp;AD New Blood','6d','Wed 18 Nov'),('Portfolio site','21d','Thu 3 Dec')]:
        us += f'<div class="prow" style="border-top:0;padding:6px 0"><span class="dot" style="background:{PC[n]}"></span><span class="tt">{n}</span><span class="muted" style="font-size:12.5px">{dt}</span><span class="pill {"soon" if d=="1d" else "calm"}">{d}</span></div>'
    us += '</div>'
    us += f'<div class="sub" style="display:flex;align-items:center;justify-content:space-between;gap:10px"><span class="muted" style="font-size:12.5px">Partner waved at 9:12</span><button type="button" class="btng" style="color:#C2496B">{IC["heart"].replace("18","16")}Wave back</button></div>'
    us += '</section>'
    m += f'<div class="h2g">{me}{us}</div>'
    return m

def h2_phone():
    b = week(True)
    b += f'<div class="ghd" style="padding-top:14px"><h2>My day</h2><span class="muted" style="font-size:12.5px">4 left · 2 done</span></div>'
    b += CARRY.replace(proj('Portfolio site'),'')
    b += trow('Finish Statement of Purpose draft',None,'<span class="pill soon">Tomorrow</span>')
    b += trow('Kimondo moodboard v2',None,'','b')
    b += trow("Read 2 chapters for Pratul's class")
    b += f'<button type="button" class="donel">{IC["chevd"]}2 more · 2 done</button>'
    b += f'''<section class="us" aria-label="Us this week" style="margin-top:10px;padding:2px 14px 14px"><div class="cardhd"><h2>Us · race to 100</h2><a class="lnk" href="#">Week {IC["chev"]}</a></div>{race_rows()}
<div class="muted" style="font-size:12.5px;margin-top:8px">Partner leads by 6 · 3 days left</div>
<div class="sub" style="margin-top:12px;padding-top:10px"><span class="lbl">Partner needs a hand · 2</span>
<div class="prow" style="border-top:0"><span class="tt">Email the Kimondo brief</span><button type="button" class="btns">{IC["hand"]}+5</button></div>
<div class="prow"><span class="tt">Portfolio proofs to print</span><button type="button" class="btns">{IC["hand"]}+5</button></div></div></section>'''
    return f'<div class="ph">{phtop(ADD_BTN)}<div class="phbody">{b}</div>{tabs()}</div>'

# ---------------- H3 · Game board ----------------
H3_CSS = """
.board{margin-top:20px;border:1px solid #E5EAF1;background:#F7F9FC;border-radius:16px;padding:20px 24px;display:grid;grid-template-columns:1fr minmax(260px,1.3fr) 1fr;gap:24px;align-items:center}
.side2{display:flex;align-items:center;gap:14px}
.side2.r{justify-content:flex-end;text-align:right}
.bigav{width:44px;height:44px;border-radius:99px;color:#fff;font-weight:700;font-size:16px;display:flex;align-items:center;justify-content:center;flex:none;position:relative}
.bigav .cr{position:absolute;top:-13px;left:50%;transform:translateX(-50%);color:#C2873B}
.bignum{font-size:40px;font-weight:700;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.who{font-size:12.5px;font-weight:600;color:#4B5866;margin-bottom:4px}
.mid{text-align:center}
.mid .gap{font-size:17px;font-weight:700}
.h3g{display:grid;grid-template-columns:minmax(0,1.45fr) minmax(0,1fr);gap:28px;margin-top:22px;align-items:start}
.move{border:1px solid #BFD5F7;background:#F3F8FF;border-radius:14px;padding:16px 18px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
.move .bx{flex:1;min-width:240px}
.move .t{font-size:16px;font-weight:700;margin-top:4px}
.ptab{width:100%;border-collapse:collapse;font-size:13px}
.ptab th{font-size:11px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;color:#4B5866;text-align:right;padding:0 0 8px}
.ptab th:first-child{text-align:left}
.ptab td{padding:8px 0;border-top:1px solid #EEF2F7;text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.ptab td:first-child{text-align:left;font-weight:500;color:#2F343B}
.ptab td.lead{color:#1D6842}
.ptab tr.tot td{font-weight:700;font-size:14px;color:#15171A}
.hand{border:1px solid #F0D9D4;background:#FFF8F6;border-radius:14px;padding:14px 16px;margin-top:16px}
.hrow{display:flex;align-items:center;gap:10px;padding:8px 0;font-size:13.5px;border-top:1px solid #F3E3DF}
.hrow:first-of-type{border-top:0}
@media (max-width:1000px){.board{grid-template-columns:1fr}.side2.r{justify-content:flex-start;text-align:left}.h3g{grid-template-columns:1fr}}
"""
def track(you=58, them=64, w=None):
    return f'''<div class="track" aria-hidden="true"><span class="ln"></span><span class="fl">{IC["flag"]}</span>
<span class="rn" style="left:{you}%"><span class="av am">M</span></span><span class="rn" style="left:{them}%"><span class="av ap">P</span></span></div>'''
def h3_desktop():
    m = head('Today')
    m += f'''<section class="board" aria-label="This week so far">
<div class="side2"><span class="bigav" style="background:#15171A">M</span><div><div class="who">You</div><div class="bignum">58</div></div></div>
<div class="mid"><div class="gap">6 behind</div><div class="muted" style="font-size:12.5px;margin:3px 0 10px">3 days left · first to 100 wins the week</div>{track()}</div>
<div class="side2 r"><div><div class="who">Partner</div><div class="bignum">64</div></div><span class="bigav" style="background:#5B6B86"><span class="cr">{IC["crown"]}</span>P</span></div>
</section>'''
    left = f'''<div class="move"><div class="bx"><span class="lbl">Best next move</span><div class="t">Finish Statement of Purpose draft</div><div class="muted" style="font-size:13px;margin-top:3px">+10 task, +5 for on time = <b style="color:#1D6842">+15</b>. That puts you 9 ahead.</div></div>
<div style="display:flex;gap:8px"><button type="button" class="btnp">{IC["clock"]}Focus 50 min</button><button type="button" class="btng">Mark done</button></div></div>'''
    left += '<div class="ghd" style="padding-top:20px"><span class="lbl">Today · worth 45 more</span><a class="lnk" href="#">+ Add a task</a></div>'
    left += trow('Reply to Sajal about the case study','Portfolio site','<span class="pill over">Since Tue</span>','m',False,'<span class="pts">+10</span>')
    left += trow('Finish Statement of Purpose draft','Statement of Purpose','<span class="pill soon">Due tomorrow</span>','m',False,'<span class="pts">+15</span>')
    left += trow('Kimondo moodboard v2','Kimondo','','b',False,'<span class="pts">+10</span>')
    left += trow("Read 2 chapters for Pratul's class",'Assignments','','m',False,'<span class="pts">+10</span>')
    left += trow('D&amp;AD brief: pick a category','D&amp;AD New Blood','','m',True,'<span class="pts earned">+15</span>')
    left += trow('Kimondo font licence','Kimondo','','m',True,'<span class="pts earned">+10</span>')
    left += '<div class="ghd" style="padding-top:20px"><span class="lbl">Habits · +2 each</span><span class="pts">1 of 3 kept</span></div>' + habits_chips(False)
    right = '<section class="card" aria-label="Points so far"><div class="cardhd"><h2>Points so far</h2><a class="lnk" href="#">The week</a></div>'
    right += '<table class="ptab"><thead><tr><th scope="col">From</th><th scope="col">You</th><th scope="col">Partner</th></tr></thead><tbody>'
    for k,a,b in [('Tasks done',30,40),('On time',10,5),('Habits kept',14,12),('Focus sessions',0,3),('Journal',4,4),('Helped out',0,0)]:
        right += f'<tr><td>{k}</td><td class="{"lead" if a>b else ""}">{a}</td><td class="{"lead" if b>a else ""}">{b}</td></tr>'
    right += '<tr class="tot"><td>Total</td><td>58</td><td>64</td></tr></tbody></table><div style="height:8px"></div></section>'
    right += f'''<section class="hand" aria-label="Partner could use a hand"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px"><h2>Partner could use a hand</h2><span class="pts">+5 each</span></div>
<div class="hrow"><span class="tt">Email the Kimondo brief</span><span class="pill over">Since Tue</span><button type="button" class="btns">{IC["hand"]}Help</button></div>
<div class="hrow"><span class="tt">Portfolio proofs to print</span><span class="pill over">Since Wed</span><button type="button" class="btns">{IC["hand"]}Help</button></div></section>'''
    right += '<div class="card" style="margin-top:16px"><div class="cardhd"><h2>Streaks</h2></div>'
    for n,s in [('Read 1 hour',6),('No phone after 11',3)]:
        right += f'<div class="trow" style="border-top:1px solid #EEF2F7"><span class="tt">{n}</span><span class="streak">{IC["flame"]}{s} days</span></div>'
    right += '<div style="height:6px"></div></div>'
    m += f'<div class="h3g"><section aria-label="Your day">{left}</section><div>{right}</div></div>' + wave()
    return m

def h3_phone():
    b = f'''<section class="board" aria-label="This week so far" style="grid-template-columns:1fr auto 1fr;padding:14px 14px 12px;gap:8px;margin-top:14px">
<div><div class="who">You</div><div class="bignum" style="font-size:30px">58</div></div>
<div class="mid"><div class="gap" style="font-size:14px">6 behind</div><div class="muted" style="font-size:11.5px">3 days left</div></div>
<div style="text-align:right"><div class="who">Partner</div><div class="bignum" style="font-size:30px">64</div></div>
<div style="grid-column:1 / -1">{track()}</div></section>'''
    b += f'''<div class="move" style="margin-top:12px;padding:12px 14px;gap:10px"><div class="bx" style="min-width:0"><span class="lbl">Best next move · +15</span><div class="t" style="font-size:15px">Finish Statement of Purpose draft</div><div class="muted" style="font-size:12.5px;margin-top:2px">Puts you 9 ahead.</div></div>
<div style="display:flex;gap:8px;width:100%"><button type="button" class="btnp" style="flex:1;justify-content:center">{IC["clock"]}Focus 50 min</button><button type="button" class="btng">Done</button></div></div>'''
    b += '<div class="ghd"><span class="lbl">Today · worth 45 more</span></div>'
    b += trow('Reply to Sajal about the case study',None,'<span class="pill over">Tue</span>','m',False,'<span class="pts">+10</span>')
    b += trow('Kimondo moodboard v2',None,'','b',False,'<span class="pts">+10</span>')
    b += trow("Read 2 chapters for Pratul's class",None,'','m',False,'<span class="pts">+10</span>')
    b += trow('D&amp;AD brief: pick a category',None,'','m',True,'<span class="pts earned">+15</span>')
    b += f'<div class="hand" style="margin-top:12px;padding:10px 14px"><div class="hrow" style="border-top:0;padding:4px 0"><span class="tt" style="font-weight:600">Partner could use a hand · 2</span><button type="button" class="btns">{IC["hand"]}+5</button></div></div>'
    return f'<div class="ph">{phtop(ADD_BTN)}<div class="phbody">{b}</div>{tabs()}</div>'

# ---------------- H4 · Day plan ----------------
HOUR = 46
H4_CSS = PILL_CSS + f"""
.h4g{{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:28px;margin-top:18px;align-items:start}}
.tl{{position:relative;border:1px solid #E5EAF1;border-radius:14px;padding:10px 14px 10px 0;height:{HOUR*14+20}px;box-sizing:border-box;overflow:hidden}}
.hr{{position:absolute;left:0;right:0;height:{HOUR}px;border-top:1px solid #EEF2F7;display:flex}}
.hr span{{width:60px;flex:none;text-align:right;padding-right:12px;box-sizing:border-box;font-size:11.5px;color:#4B5866;font-variant-numeric:tabular-nums;transform:translateY(-8px);background:#fff;height:16px}}
.hr:first-child{{border-top:0}}
.blk{{position:absolute;left:68px;right:14px;border-radius:9px;padding:7px 11px;box-sizing:border-box;font-size:13px;display:flex;align-items:flex-start;gap:9px;overflow:hidden}}
.blk .bt{{font-weight:600}}
.blk .bs{{font-size:12px;color:#4B5866;font-variant-numeric:tabular-nums}}
.b-rt{{background:#EEF4FF;border:1px solid #D3E2FB}}
.b-cl{{background:#F3F5F9;border:1px solid #DCE3EC}}
.b-fo{{background:#fff;border:1.5px dashed #8DB4F2}}
.b-tk{{background:#fff;border:1px solid #DCE3EC;box-shadow:0 1px 2px rgba(20,60,130,.06);align-items:center}}
.b-dn{{background:#F7F9FC;border:1px solid #EEF2F7;align-items:center}}
.now{{position:absolute;left:60px;right:0;height:0;border-top:2px solid #1F6FEB}}
.now b{{position:absolute;right:8px;top:-21px;background:#1F6FEB;color:#fff;font-size:11px;font-weight:600;border-radius:99px;padding:2px 7px;font-variant-numeric:tabular-nums}}
.now i{{position:absolute;left:-5px;top:-6px;width:10px;height:10px;border-radius:99px;background:#1F6FEB}}
.any .trow{{padding:9px 2px}}
.grip{{color:#8A9BB0;display:flex;flex:none}}
.hint{{display:flex;align-items:center;gap:8px;font-size:12.5px;color:#4B5866;background:#F7F9FC;border-radius:10px;padding:9px 12px;margin-top:12px}}
@media (max-width:1000px){{.h4g{{grid-template-columns:1fr}}}}
"""
def at(h, m=0): return round((h-8+m/60)*HOUR)+10
def h4_desktop():
    m = head('Today', score_pill()) + week()
    tl = '<section class="tl" aria-label="Schedule">'
    for i,h in enumerate(range(8,22)):
        tl += f'<div class="hr" style="top:{i*HOUR+10}px"><span>{h:02d}:00</span></div>'
    tl += f'<div class="blk b-dn" style="top:{at(9)}px;height:{HOUR-6}px">{chk("D&amp;AD brief: pick a category",True)}<span class="bt tt done" style="font-weight:500">D&amp;AD brief: pick a category</span><span class="pts earned">+15</span></div>'
    tl += f'<div class="blk b-rt" style="top:{at(10)}px;height:{HOUR*3-4}px"><span class="rt">{IC["repeat"]}</span><div><div class="bt">Studio</div><div class="bs">10:00–13:00 · Room 4 · every weekday</div></div></div>'
    tl += f'<div class="blk b-cl" style="top:{at(14)}px;height:{HOUR*2-4}px"><span class="rt">{IC["repeat"]}</span><div><div class="bt">Class · Interaction design</div><div class="bs">14:00–16:00</div></div></div>'
    tl += f'<div class="blk b-fo" style="top:{at(16,20)}px;height:{round(HOUR*50/60)-4}px;color:#195FD0;align-items:center"><span class="rt" style="color:#195FD0">{IC["clock"]}</span><span class="bt">Focus · SOP draft</span><span class="bs" style="color:#195FD0">16:20–17:10 · planned</span></div>'
    tl += f'<div class="blk b-tk" style="top:{at(17,30)}px;height:{round(HOUR*0.75)}px">{chk("Call with the Kimondo team")}<span class="bt">Call with the Kimondo team</span><span class="bs">17:30</span><span class="avs" style="margin-left:auto"><span class="av am">M</span><span class="av ap">P</span></span></div>'
    tl += f'<div class="blk b-rt" style="top:{at(19)}px;height:{HOUR-6}px;align-items:center"><span class="rt">{IC["repeat"]}</span><span class="bt">Walk 8k steps</span><span class="bs">habit</span></div>'
    tl += f'<div class="now" style="top:{at(15,10)}px"><b>15:10</b><i></i></div>'
    tl += '</section>'
    any_ = '<section class="any" aria-label="Anytime today">'
    any_ += '<div class="ghd" style="padding-top:4px"><h2>Anytime · 4</h2><a class="lnk" href="#">+ Add</a></div>'
    def arow(t,p,pill='',who='m'):
        return trow(t,None,pill,who).replace('<div class="trow">',f'<div class="trow"><span class="grip" aria-hidden="true">{IC["grip"]}</span>',1).replace('<span class="tt">',f'<span class="dot" style="background:{PC[p]}" title="{p}"></span><span class="tt">',1)
    any_ += arow('Reply to Sajal about the case study','Portfolio site','<span class="pill over">Since Tue</span>')
    any_ += arow('Finish Statement of Purpose draft','Statement of Purpose','<span class="pill soon">Tomorrow</span>')
    any_ += arow('Kimondo moodboard v2','Kimondo','','b')
    any_ += arow("Read 2 chapters for Pratul's class",'Assignments')
    any_ += '<div class="hint">' + IC['grip'] + 'Drag a task onto a time to plan it. It stays a task, with a time.</div>'
    any_ += '<div class="ghd" style="padding-top:22px"><h2>Habits</h2><span class="pts">1 of 3 kept</span></div>' + habits_chips(False)
    any_ += f'''<div class="ghd" style="padding-top:22px"><h2>Partner's day</h2><span class="muted" style="font-size:12.5px">4 of 6 done</span></div>
<div class="trow" style="border-top:0"><span class="av ap">P</span><span class="tt">In class until 16:00, then free</span></div>
<div class="trow"><span class="pill over">2 overdue</span><span class="tt muted" style="font-weight:400">Kimondo brief, portfolio proofs</span><button type="button" class="btns">{IC["hand"]}Give a hand</button></div>'''
    any_ += '</section>'
    m += f'<div class="h4g">{tl}{any_}</div>' + wave()
    return m

def h4_phone():
    b = week(True)
    def item(time, body, cls=''):
        return f'<div style="display:flex;gap:12px;align-items:stretch;padding:5px 0"><span class="tnum muted" style="width:44px;flex:none;font-size:12px;padding-top:9px;text-align:right">{time}</span><div class="blk {cls}" style="position:static;flex:1;min-width:0">{body}</div></div>'
    b += '<div style="margin-top:12px">'
    b += item('09:00', f'{chk("D&amp;AD brief",True)}<span class="tt done" style="font-weight:500">D&amp;AD brief: pick a category</span><span class="pts earned">+15</span>','b-dn')
    b += item('10:00', f'<span class="rt">{IC["repeat"]}</span><div><div class="bt">Studio</div><div class="bs">10:00–13:00</div></div>','b-rt')
    b += item('14:00', f'<span class="rt">{IC["repeat"]}</span><div><div class="bt">Class</div><div class="bs">14:00–16:00</div></div>','b-cl')
    b += '<div style="display:flex;align-items:center;gap:8px;margin:6px 0"><span style="width:44px;text-align:right;font-size:11px;font-weight:700;color:#195FD0" class="tnum">15:10</span><span style="flex:1;border-top:2px solid #1F6FEB;position:relative"><i style="position:absolute;left:-5px;top:-6px;width:10px;height:10px;border-radius:99px;background:#1F6FEB"></i></span></div>'
    b += item('16:20', f'<span class="rt" style="color:#195FD0">{IC["clock"]}</span><div><div class="bt" style="color:#195FD0">Focus · SOP draft</div><div class="bs" style="color:#195FD0">planned, 50 min</div></div>','b-fo')
    b += item('17:30', f'{chk("Call with the Kimondo team")}<span class="bt tt">Call with the Kimondo team</span>','b-tk')
    b += '</div>'
    b += '<div class="ghd"><span class="lbl">Anytime · 4</span><a class="lnk" href="#">+ Add</a></div>'
    b += trow('Reply to Sajal about the case study',None,'<span class="pill over">Tue</span>')
    b += trow('Finish Statement of Purpose draft',None,'<span class="pill soon">Tomorrow</span>')
    b += trow('Kimondo moodboard v2',None,'','b')
    b += trow("Read 2 chapters for Pratul's class")
    pill = f'<a class="spill" href="#" style="padding:6px 10px">{IC["crown"]}6 behind</a>'
    return f'<div class="ph">{phtop(pill)}<div class="phbody">{b}</div>{tabs()}</div>'

# ---------------- H5 · Bento ----------------
H5_CSS = """
.bento{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:16px;margin-top:20px}
.tile{border:1px solid #E5EAF1;border-radius:14px;padding:14px 16px;background:#fff;min-width:0;box-sizing:border-box}
.tile .th{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
.s7{grid-column:span 7}.s5{grid-column:span 5}.s4{grid-column:span 4}.s3{grid-column:span 3}.s8{grid-column:span 8}.s6{grid-column:span 6}
.r2{grid-row:span 2}
.tile .th+.trow{border-top:0}
.ring{position:relative;width:96px;height:96px;margin:2px auto 10px}
.ring b{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;font-variant-numeric:tabular-nums}
.sc2{display:flex;align-items:flex-end;gap:18px;margin:4px 0 12px}
.sc2 .n{font-size:32px;font-weight:700;letter-spacing:-.03em;line-height:1;font-variant-numeric:tabular-nums}
.sc2 .w{font-size:12px;font-weight:600;color:#4B5866;margin-bottom:4px}
.hl{display:flex;align-items:center;gap:10px;padding:7px 0;font-size:13.5px}
@media (max-width:1000px){.s7,.s5,.s4,.s3,.s8,.s6{grid-column:span 12}.r2{grid-row:auto}}
"""
def ring(p=0, label='25:00'):
    r=40; c=2*3.14159*r
    return f'<div class="ring" aria-hidden="true"><svg width="96" height="96" viewBox="0 0 96 96"><circle cx="48" cy="48" r="{r}" stroke="#E8EDF4" stroke-width="7" fill="none"></circle><circle cx="48" cy="48" r="{r}" stroke="#1F6FEB" stroke-width="7" fill="none" stroke-linecap="round" stroke-dasharray="{c:.1f}" stroke-dashoffset="{c*(1-p):.1f}" transform="rotate(-90 48 48)"></circle></svg><b>{label}</b></div>'
def h5_desktop():
    m = head('Today') + week()
    t = '<div class="bento">'
    t += '<section class="tile s7 r2" aria-label="Today"><div class="th"><h2>Today · 4 left</h2><span class="muted" style="font-size:12.5px">2 done · +25</span></div>'
    t += CARRY + TODAY_ROWS + qadd() + '</section>'
    t += f'<section class="tile s5" aria-label="This week"><div class="th"><h2>Race to 100</h2><a class="lnk" href="#">This week {IC["chev"]}</a></div>'
    t += '<div class="sc2"><div><div class="w">You</div><div class="n">58</div></div><div><div class="w">Partner</div><div class="n" style="color:#5B6B86">64</div></div><div class="muted" style="font-size:12.5px;margin-left:auto;text-align:right;margin-bottom:3px">6 behind<br>3 days left</div></div>' + track() + f'<div style="display:flex;justify-content:flex-end;margin-top:10px"><button type="button" class="btns" style="color:#C2496B">{IC["heart"].replace("18","14")}Wave</button></div></section>'
    t += f'''<section class="tile s5" aria-label="Partner"><div class="th"><h2>Partner could use a hand</h2><span class="pts">+5 each</span></div>
<div class="hl"><span class="tt">Email the Kimondo brief</span><span class="pill over">Since Tue</span><button type="button" class="btns">{IC["hand"]}Help</button></div>
<div class="hl" style="border-top:1px solid #EEF2F7"><span class="tt">Portfolio proofs to print</span><span class="pill over">Since Wed</span><button type="button" class="btns">{IC["hand"]}Help</button></div></section>'''
    t += '<section class="tile s4" aria-label="Habits"><div class="th"><h2>Habits</h2><span class="pts">1 of 3</span></div>'
    t += f'<div class="hl">{chk("Read 1 hour",True)}<span class="tt">Read 1 hour</span><span class="streak">{IC["flame"]}6</span></div>'
    t += f'<div class="hl">{chk("Walk 8k steps")}<span class="tt">Walk 8k steps</span></div>'
    t += f'<div class="hl">{chk("No phone after 11")}<span class="tt">No phone after 11</span><span class="streak">{IC["flame"]}3</span></div>'
    t += '<div class="hl" style="border-top:1px solid #EEF2F7;padding-top:10px"><span class="tt">Cigarettes <b class="cnum">3</b> <span class="muted" style="font-size:12px;font-weight:400">aim ≤ 5</span></span><button type="button" class="step" aria-label="One fewer">−</button><button type="button" class="step" aria-label="One more">+</button></div></section>'
    t += f'<section class="tile s3" aria-label="Focus" style="text-align:center"><div class="th"><h2>Focus</h2></div>{ring()}<button type="button" class="btnp" style="width:100%;justify-content:center">Start 25 min</button></section>'
    t += '<section class="tile s5" aria-label="Coming up"><div class="th"><h2>Coming up</h2><a class="lnk" href="#">All</a></div>'
    for n,d,dt in [('Statement of Purpose','1d','Fri 13 Nov'),('D&amp;AD New Blood','6d','Wed 18 Nov'),('Portfolio site','21d','Thu 3 Dec')]:
        t += f'<div class="hl"><span class="dot" style="background:{PC[n]}"></span><span class="tt">{n}</span><span class="muted" style="font-size:12.5px">{dt}</span><span class="pill {"soon" if d=="1d" else "calm"}">{d}</span></div>'
    t += '</section>'
    t += '<section class="tile s4" aria-label="This week\'s topic"><div class="th"><h2>This week\'s topic</h2><a class="lnk" href="#">Open</a></div><div style="font-size:16px;font-weight:600">Typography for screens</div><div class="muted" style="font-size:12.5px;margin-top:4px">3 links saved</div></section>'
    t += f'<section class="tile s8" aria-label="On your mind"><div class="th"><h2>On your mind</h2><a class="lnk" href="#">+ Note</a></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px"><div class="note">Ask Pratul if the SOP can go over 800 words.</div><div class="note">Kimondo: try the warmer grey on the deck cover.</div></div></section>'
    t += '</div>'
    return m + t

def h5_phone():
    b = '<div class="bento" style="gap:10px;margin-top:14px">'
    b += '<section class="tile" style="grid-column:span 12;padding:10px 14px 4px" aria-label="Today"><div class="th" style="margin-bottom:2px"><h2>Today · 4 left</h2><span class="muted" style="font-size:12px">2 done</span></div>'
    b += CARRY.replace(proj('Portfolio site'),'') + trow('Finish Statement of Purpose draft',None,'<span class="pill soon">Tomorrow</span>') + trow('Kimondo moodboard v2',None,'','b')
    b += '<a class="lnk" href="#" style="padding:8px 0 10px">1 more</a></section>'
    b += f'<section class="tile" style="grid-column:span 6;padding:12px" aria-label="Race"><div class="w muted" style="font-size:11px;font-weight:600">RACE TO 100</div><div style="display:flex;align-items:baseline;gap:6px;margin:6px 0 2px"><span class="cnum" style="font-size:24px">58</span><span class="muted" style="font-size:12px">vs 64</span></div><div class="muted" style="font-size:12px">6 behind</div></section>'
    b += f'<section class="tile" style="grid-column:span 6;padding:12px;background:#FFF8F6;border-color:#F0D9D4" aria-label="Partner"><div class="muted" style="font-size:11px;font-weight:600">PARTNER</div><div style="font-size:14px;font-weight:600;margin:6px 0 6px">2 overdue</div><button type="button" class="btns">{IC["hand"]}Help · +5</button></section>'
    b += f'<section class="tile" style="grid-column:span 6;padding:12px" aria-label="Habits"><div class="muted" style="font-size:11px;font-weight:600">HABITS · 1 OF 3</div><div class="hl" style="padding:6px 0 0">{chk("Read 1 hour",True)}<span class="tt" style="font-size:13px">Read 1h</span><span class="streak">{IC["flame"]}6</span></div><div class="hl" style="padding:6px 0 0">{chk("Walk 8k steps")}<span class="tt" style="font-size:13px">Walk 8k</span></div><div class="hl" style="padding:6px 0 0">{chk("No phone after 11")}<span class="tt" style="font-size:13px">No phone</span></div></section>'
    b += f'<section class="tile" style="grid-column:span 6;padding:12px;text-align:center" aria-label="Focus"><div class="muted" style="font-size:11px;font-weight:600;text-align:left">FOCUS</div><div style="transform:scale(.7);margin:-14px 0 -18px">{ring()}</div><button type="button" class="btnp" style="width:100%;justify-content:center;padding:8px">Start 25 min</button></section>'
    b += '<section class="tile" style="grid-column:span 12;padding:10px 14px" aria-label="Coming up"><div class="muted" style="font-size:11px;font-weight:600">COMING UP</div>'
    for n,d,dt in [('Statement of Purpose','1d','Fri 13 Nov'),('D&amp;AD New Blood','6d','Wed 18 Nov')]:
        b += f'<div class="hl"><span class="dot" style="background:{PC[n]}"></span><span class="tt">{n}</span><span class="pill {"soon" if d=="1d" else "calm"}">{d}</span></div>'
    b += '</section></div>'
    return f'<div class="ph">{phtop(ADD_BTN)}<div class="phbody">{b}</div>{tabs()}</div>'

# ---------------- write ----------------
def desktop_page(inner): return f'<div class="app">\n{side()}<main class="main">\n{inner}\n</main>\n</div>'

def dc(title, css, body, w, h):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT}
<style>
{BASE}
</style>
<style>
{css}
</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":{w},"height":{h}}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
'''

def preview(title, css, body, w):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{title}</title>{FONT}<style>{BASE}</style><style>{css}</style></head><body style="width:{w}px">{body}</body></html>'

VERS = [
 ('H1','one-list','H1 · One list',H1_CSS,h1_desktop,h1_phone,1000),
 ('H2','me-us','H2 · Me | Us',H2_CSS,h2_desktop,h2_phone,1080),
 ('H3','game-board','H3 · Game board',H3_CSS,h3_desktop,h3_phone,1080),
 ('H4','day-plan','H4 · Day plan',H4_CSS,h4_desktop,h4_phone,1000),
 ('H5','bento','H5 · Bento',H5_CSS,h5_desktop,h5_phone,1000),
]
out = {}
for i,(k,slug,title,css,fd,fp,h) in enumerate(VERS):
    dname = f'Home-{k}-{slug}.dc.html'; pname = f'Home-{k}-phone.dc.html'
    dbody = desktop_page(fd()); pbody = fp()
    open(f'{ROOT}/project/{dname}','w').write(dc(title, css, dbody, 1440, h))
    open(f'{ROOT}/project/{pname}','w').write(dc(title+' · phone', css, pbody, 390, 844))
    open(f'{PREV}/{k}-desktop.html','w').write(preview(title, css, dbody, 1440))
    open(f'{PREV}/{k}-phone.html','w').write(preview(title, css, pbody, 390))
    out[k] = (dname, pname, title, h, i)
json.dump({k:list(v) for k,v in out.items()}, open(SP+'/home_out.json','w'))
print('ok', list(out))
