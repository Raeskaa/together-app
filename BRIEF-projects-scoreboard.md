# Brief: Projects redesign · Weekly scoreboard · Per-person login

Mahesh, 5 Nov: *"so much empty space · I hate the projects board · make 4–5 variants before anything · gamify: points, who's winning, who needs help · a week-so-far overview · empty states · table/list view · filters at the top aren't working · a different ID + password for each of us so the dashboard renders for each person."*

Refs (what I take from each):
- **Miro boards list**: "Filter by · Owned by · Sort by" dropdowns, a grid↔list toggle, dense rows (name, last change, owner, ⋯), and an empty state of one line + one action.
- **Voicenotes**: filter chips (All / Shared / Starred / +), and a quiet single-column list.
- **Notion**: a dashboard of small widgets (donut "4 Total", timeline with a today line), the "No matching tasks · + New task" empty state, and the personalise modal (a playful identity pick).

---

## 0 · What's wrong today (from your screenshots of the live site)

| Seen | Why |
|---|---|
| **Top "Me / Partner" looks like a filter and does nothing** | It isn't a filter. It switches *who this device is*. On Projects it changes nothing visible, and "Mine" always meant Mahesh. **The Trust pass (built, not deployed) already removes it from the top bar.** What's still missing is a real filter on Projects. |
| **Every project card says "No timeline yet"** | All 6 projects have a deadline but no start date. The card is built around start→end, so it draws an empty bar on every card. **Design around the deadline, not a timeline.** |
| **Big empty colour band + letter + 0% ring** | None of it answers a question. Most of each card is padding, and the page ends halfway down. |
| **Every project shows "P"** | All 6 are owned by the partner. They were probably created while the old switch was on Partner. **Are they yours?** If so I'll fix them in one go. |
| **Calendar: a huge empty hour grid** | None of your items has a time, so 7am–10pm is blank while the all-day row is crammed. |

## 1 · Projects page: what you come for (in order)

1. Which project is closest to its deadline, or falling behind?
2. What's the next thing to do in each one?
3. Whose is it? (show mine / theirs / both)
4. Open one to work in it.
5. Start a new one.
6. Keep finished ones out of the way.

So the default is **sorted by deadline**. Every row shows **days left + progress + next task**, there's a **real owner filter**, and the layout is dense.

### Five variants to make (one canvas, your real 6 projects + realistic tasks)

| | Direction | Shape | Best at |
|---|---|---|---|
| **A** | **Table** (Miro list) | Columns: Project · Next task · Progress · Deadline · Days left · Owner · ⋯. Controls: Filter by (Active / Finished / All), Owned by (Everyone / You / Them / Both), Sort by (Deadline / Progress / Last activity / A–Z), grid↔list toggle | Scanning everything at once |
| **B** | **Deadline lanes** | Columns: *This week · This month · Later · No deadline*, with compact cards | Seeing urgency at a glance |
| **C** | **Timeline** | Projects as rows across 12 weeks: a diamond at each deadline, a today line, progress beside the name | When things land, and what overlaps |
| **D** | **Next-step list** | Each project is one row with its next 2 open tasks inline and tickable, without opening the project | Doing, not browsing |
| **E** | **Dense cards v2** | 4-up compact cards: deadline chip first, thin progress bar, next task, owner avatars. No colour band | Closest to today's look, minus the waste |

Each variant shows these states:
- default
- **no projects yet**
- **filter matches nothing** ("Nothing here · clear filters · + New project")
- **all finished**
- long names
- 15+ projects
- **phone 375**

**Project page (inside a project):** a **List · Table · Timeline** switch. Table columns: Task · Owner · Due · Status · Subtasks.

## 2 · Gamifying: points, who's winning, who needs help

### Proposed points (simple enough to explain on one line)
| You… | Points |
|---|---|
| finish a task | **+10** |
| …on or before its deadline | **+5** bonus |
| finish a subtask | +3 |
| keep a habit that day (tick it, or stay ≤ your cigarette aim) | +2 |
| write the journal | +2 |
| finish a focus session | +3 |
| **help**: finish a task that was theirs or shared | **+5** bonus |
| leave something overdue | 0. No minus points; it shows as "not done" |

- **Weekly**: resets every week. "Weeks won" carries over (e.g. *Mahesh 3 – 2 Partner*).
- **Who needs a hand** shows when someone has **3+ overdue** or is **under half their week's tasks by Thursday**. The other person sees a card: *"{name} has 4 overdue · Take one · Send 💪"*. "Take one" moves a task to *Both*.
- **The moment**: ticking a task pops "+10" and the score updates live. The week's leader gets a small crown on their avatar everywhere.

### "This week" page: what you come for
1. Who's ahead, and by how much?
2. My done vs not done, theirs too.
3. Does anyone need help?
4. How did each day go?
5. What's still open before the week ends?

**Three variants:**
- **S1 head-to-head**: two columns, You vs Them. Big points, done / not done / overdue, a crown on the leader, a needs-a-hand card, and daily bars underneath.
- **S2 race**: one track Mon → today with both of you moving along it, plus this week's wins and misses for each person.
- **S3 dashboard**: Notion-style widgets. A done-vs-not-done donut, points per day, and a table of open tasks by person.

Plus a **slim scoreboard strip on Today**: *"This week · You 42 · {name} 35 · 👑 you"*. Tapping it opens the page.

**Empty states**
- Monday morning: "A fresh week. First tick takes the lead."
- Nothing planned yet.
- One person hasn't started.
- A tie.

**What this needs underneath:** tasks don't record *when* or *by whom* they were finished. I'll add `done_at` and `done_by`, plus a small focus-session log. That's an additive migration you run once. **Points count from that day on**, because older ticks have no date.

## 3 · Login: each person with their own ID + password

**Flow**
1. Open the site. The screen asks "Who's signing in?" with two name buttons: **Mahesh · {partner}**.
2. Tap your name, enter your password, and you're in.

What follows from that:
- The server knows who you are, so the dashboard, "You", the default owner and **who ticked what** come from your login. That's what makes the scores honest.
- The "Who's this?" picker and Settings › Switch go away. **Sign out** replaces them.
- You set both passwords yourself; I can't type passwords for you. Run `wrangler secret put PASS_MAHESH` and `PASS_PARTNER`.
- Logins stay 180 days. Wrong attempts are rate-limited.

**States:** wrong password · too many tries (wait 1 min) · signed out on another device · session expired with unsaved changes (they're kept and sent after sign-in).

## 4 · Calendar: the empty space
- **Collapse the hour grid when the week has no timed items.** Show the all-day lanes full height, plus one line: "Nothing has a time this week · add a time to see it on the grid".
- When there are timed items, **scroll to the first one** (or to now).

---

## Decisions for you
1. **Variants as one design canvas (claude.ai artifact) with your real projects:** **yes** *(recommended: fast, nothing touches the live app)* / build them in code behind a switch.
2. **Login:** **name buttons + password** *(recommended: one field on a phone)* / an ID field + password.
3. **Points table:** OK as is / change some.
4. **Words:** "winning / losing" as you said / **"ahead / needs a hand"** *(recommended: keeps it friendly when someone has a bad week)*.
5. **Week runs:** **Mon–Sun** *(recommended for a scoreboard)* / Sun–Sat (what the app uses now).
6. **The 6 projects showing "P":** are they yours? I'll move them to you or Both in one go.
7. **Deploy the Trust pass now?** It removes the confusing top switch today, and your partner gets the safer saving. *(recommended: yes; the login change comes later in one pass)*

## Order after your OK
Canvas: Projects A–E + project page views + empty states + phone, then This week S1–S3 → **you pick** → build: login (first, because scoring depends on it) → the Projects variant you pick → scoring + This week → calendar fix.
