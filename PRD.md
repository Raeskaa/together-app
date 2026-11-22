# hate club — PRD (current app, for the v2 rebuild)

**Written:** 2026-11-17 · **Purpose:** document every feature that exists in the current app, as the spec to rebuild from scratch. This is a *requirements* doc, not a design — the design pass (Claude artifact, mobile + web) comes after, through the design gate.

**Current app:** live at https://shared-planner.mahesh-3dd.workers.dev · repo `/Users/design/shared-planner` + GitHub `Raeskaa/together-app` · stack = Cloudflare Worker + D1 + **single-file Preact/htm** (`public/index.html`). The v2 goal: move off the one-file HTML to a real framework, and open it up so **anyone can sign up and use it** (public multi-tenant).

---

## 1. What it is

A **two-person shared planner** — for a couple, close friends, or accountability partners. Not a team PM tool and not a solo habit app: its thesis is a **"care instrument, not a scoreboard"** — shared-fate, forgiving, cooperative, present. Two people run their days side by side: shared + personal tasks, projects, habits, a gentle game, and a layer of warmth (presence, nudges, a daily question, moods, a shared focus timer).

**Core concepts**
- **Person** — a real account (username + password).
- **Space** — a shared world between people. Kinds: `partner` (2), `friends`, `team`, `solo`. Today every space is **2-person** (teams N>2 deferred). One person can be in **many spaces** and switch between them.
- **Ownership** — every item (task, project, habit, note, topic, journal) belongs to a space; its `owner` is a person or `everyone` (shared). **Personal items** can be flagged "just me — everywhere" and travel across all of that person's spaces (owner-scoped, private).

---

## 2. Auth & onboarding

- **Sign up / sign in** — own username + password (PBKDF2, 50k rounds). A shared passcode only opens *setup* (first account creation); all data endpoints require a real session (signed cookie, 180d). Brute-force lock: 5 fails → 60s.
- **Join by invite** — a space owner shares an invite **link or code**; a new person signs up and lands directly in that space. Signed-in users auto-accept.
- **Onboarding** — a first-run **"How it works"** intro (icon-badge rows per feature) + a **"Get started" 3-step stepper** on the empty Today (create project / add task / journal — each ticks from real data).
- *v2 new:* public multi-tenant sign-up (today it's gated by a shared passcode), password reset by email (not built), account management.

---

## 3. Surfaces (screens) & features

### 3.1 Home — "Today"
The daily home. A list (deliberately not a schedule — "we both don't have a schedule").
- **Greeting** — time-of-day + name, functional subline ("let's finish X first · N to go"), daily-rotating tone.
- **Score pill** — "You two · N together" (combined-first; the you↔them split is demoted, hidden on phone).
- **Us-streak banner** — a shared streak fed by either person's activity; both active = a double day; states: start / building / at-risk / fed / double / broken. Lottie flame, themed.
- **Mood row** — one-tap 😣😕😐🙂😄.
- **Quick add** — inline add a task/event for today.
- **From earlier** — carried-over unfinished items (Today / Pick a day / Unplan / Edit / Drop).
- **Open list + done fold** — today's tasks; ticked rows fold away after a beat.
- **Rail** — partner **presence** ("read today ✓ · 2 done" / "Focusing now · label" / "hasn't shown up yet"), **Coming up** (soonest deadlines), **Tonight**.
- **Habit cards** — today's habits (check / count), done·skipped·pending.
- **Notes board** — "On your mind": colored note cards each person adds.
- **Daily question** — one shared prompt/day; see your partner's answer only after you answer (server-enforced reveal).
- **One for today** — a random fact + a line (Fraunces italic, attributed).

### 3.2 This Week
- **Points scoreboard** — combined "together to 200 this week" race + the demoted head-to-head; points so far, habits kept, "needs a hand", last week, leaderboard.
- **Points:** task **10** · subtask **3** · on-time **+5** · helping **+5** · habit **2** · journal **2** · focus **3**. Week runs **Mon–Sun**; the day rolls over at **4am**; race target **100** each (200 combined).

### 3.3 Calendar
- Views: **Day** (hour timeline) · **Week** (time-grid, now-line) · **Month** (project-timeline lane) · **Timeline** (gantt of projects).
- **Filters** — owner (Everyone/Me/Partner/Shared) + project.
- **Click-to-schedule** — select an unscheduled task → click a day/slot to set date+time (no drag).
- **Range → project** — drag a date range on Month → create a project across it (+ an Airbnb-style range picker in the editor).

### 3.4 Projects
- **Views of one page:** Table · Lanes · Timeline · Cards.
- **Project page** — List / Table / Timeline (trip-style itinerary: Started → dated tasks → Deadline as nodes), a **properties rail** (deadline / days left / started / owner), **subtasks with their own deadlines**, **materials/links**, description.
- **Kinds:** plain · course · branding. Start/end dates, color, archive ("Finish it instead" → archived, Reopen).

### 3.5 Tasks (table)
- All tasks in a spreadsheet view: filters (owner / project / status), grouped by due bucket (Overdue / Today / This week / Later / No deadline / Done).
- **Task types:** task · reminder · milestone (task-like) · event · meeting (event-like), each colored.
- Fields: title, project, owner, deadline **date + time**, scheduled date+time, subtasks (parent_id), personal flag.

### 3.6 Journal
- Private per-person daily journaling (space-scoped; a person's journal is theirs).

### 3.7 The care layer (the differentiator)
- **Waves** — a bottom-right 🫶 FAB → send an emoji (💛👋✨☕💪🫶); kinds **wave / nudge / boost**; receiver gets a center-burst + toast.
- **Nudge** — one-tap "Nudge <name>", shown only when they've done nothing today, capped once/day.
- **Cheer (boost)** — one-tap "Cheer <name> on" when they've been active.
- **Presence** — today's-activity-only line (no "last online").
- **Shared focus / pomodoro** — one timer per space (25/50/15), both see the SAME countdown (absolute end-time + ~5s poll); started-by name; "time's up ✨". Compact widget in the sidebar.
- **Moods · daily question · notes board** — see Home.

### 3.8 Settings (modal, grouped left-nav)
- **Account / People** — your name, partner name, "this device is X · switch".
- **Habits** — add/edit/delete habit definitions.
- **Notifications** — browser notifications opt-in (toasts always on).
- **Claude** — make your private connector link.
- **Appearance** — **9 backgrounds** (solids + gradients + 2 dark grounds), **4 fonts** (General Sans default · Inter · Fraunces · Jakarta · Grotesk), **3 corner radii**. Theme is shared; the accent travels to the primary CTA.
- **About** — reopen the intro / sharing.

### 3.9 Spaces & switching
- Sidebar space switcher; create a new space; invite (link/code) while < 2 members; each space is its own isolated world.
- **Import** — pull your own open tasks from another space into a new one (one-time copy, dedup, drops shared/others'-project items).

### 3.10 Claude connector (MCP)
- A private per-person link `/mcp/<link>` exposing tools: **list · add · tick off · reopen · move** (no delete). Lets Claude read/add tasks on that person's behalf.

### 3.11 System-wide
- **Notifications** — in-app toasts (always) + browser notifications (opt-in); triggers: partner wave/nudge, partner starting a focus session.
- **Motion** — tick chip, count-up numbers, exit animations, lead crown, **confetti at 7/30/100**, **Breathe** Lottie loader (theme-colored), **Streak** Lottie flame; all reduced-motion safe. (Frequent actions — tabs, habit +/− — are deliberately instant.)
- **Realtime** — a client outbox + replay model; shared state (focus, waves, streak) syncs via short polling, not websockets.

---

## 4. Data model (D1 tables, current)

`people` · `login_attempts` · `spaces` · `members` · `invites` · `settings` · `projects` · `project_materials` · `routines` · `tasks` · `journal` · `habits` · `habit_logs` · `topics` · `topic_links` · `notes` · `focus` · `waves` · `focus_log` · `claude_links` · `streak_state` · `daily_answers` · `moods`.

(Full column definitions in `schema.sql`. Tasks carry: project, owner, type, date, time, due, due_time, parent_id, personal, done/done_at/done_by. Projects: kind, start/end, description, archived, materials. Habits: check/count, target, unit, caption, logs keyed by date+habit.)

---

## 5. Known gaps / not yet built

From `GAPS.md` + the engagement roadmap (`IDEAS.md`, 11 slices — 1–4 built):
- **Phone:** week strip clips at 375px · **not installable (no PWA manifest)** · no real-device testing.
- **Accounts:** password reset by email · richer account management · public sign-up.
- **Reminders & background notifications** (due-time reminders, push).
- **Habits for past days**, calendar week-start (Sunday) vs points (Mon–Sun) mismatch.
- **Roadmap slices 5–11 (designed, not built):** 5 grow-a-thing (signature plant/thing) · 6 bookended ritual · 7 per-item privacy · 8 milestones + keepsake · 9 onboarding + pledge · 10 weekly recap · 11 PWA + widget.
- **Later:** monetization (one per-pair sub, cosmetics only) · **teams (N>2)** (research says don't rush — the pair is the moat).

---

## 6. Rebuild notes (v2)

- **Keep:** the thesis (care instrument), the two-person/spaces model, the data model (it's solid — spaces M:N, personal-travels, points, streak), the care layer (this is the moat), the design identity (blue `#1F6FEB` / General Sans / sky — a rebrand was rejected before).
- **Rethink:** move from one `index.html` to a real **component framework**; decide **v2 scope** (the current app grew 20+ features organically — rebuild should cut to the core, not port everything); the **public multi-tenant** shift (real sign-up, onboarding, privacy, abuse, support) is the biggest new surface.
- **Stack (decide at the end of design, not now):** recommended **React (Next.js or React Router) + Tailwind + shadcn/ui, responsive web**, on **Cloudflare (Workers + D1)** to reuse what's paid-for and known — or Postgres (Neon/Supabase) if richer queries are wanted. "Website anyone can log in" = web-first, responsive; native (Expo) is a later, bigger lift.
- **DB migration** (current D1 → v2) is deferred — plan it once the v2 schema is set.
- **Process:** PRD (this) → design the whole system in a Claude artifact (mobile + web) **through the design gate** → Mahesh's OK → build feature by feature → deploy.
