# DESIGN LOG

> **How this file works.** "Where hate club stands" (just below) is rewritten every pass, so a cold session can read it alone. The entries under it are append-only, newest first, one per design pass. Keep it factual: paths, what shipped, what didn't.

## Where hate club stands (refreshed 2026-11-08 night, before an account switch)

**Live:**
- **Site:** https://shared-planner.mahesh-3dd.workers.dev. **Live build = personal-items-travel + import-tasks** (Cloudflare Version `8f429a69`, live sha `71b27edd`), on top of: Multi-space Phase 1 (`2df60c9b`), "One for today" v2 (`0fbd4912`), theme-leak fix (`3dffd8a2`), Today greeting (`96366765`), UI refresh (`5e13d3a8`). (Everything since branch `ui-refresh-and-spaces` commit `2d45471` is **uncommitted**; repo is `main`, no remote.)
- **Hosting:** Cloudflare account `3ddd20c68cd38c9b2dad37782db8a154` (mahesh@trueleap.io, subdomain mahesh-3dd). Mahesh approved this as an exception to the no-Trueleap-deploys rule.
- **Repo:** `/Users/design/shared-planner` (git `main`, no remote). Stack: Cloudflare Worker + D1 + one-file Preact/htm `public/index.html`.

**Every screen, what it is now, and where its design lives**

| Surface | Now (all live) | Design source | Code |
|---|---|---|---|
| Sign in / first-time setup | your own username + password; the shared passcode only opens setup | canvas `Login` · `BRIEF-projects-scoreboard.md` | `SignIn`, `Setup` · worker `/api/login` `/api/setup` `/api/claim` |
| **Home (Today)** | **H1**: score pill in the header, quick add, From earlier, open list + done fold, rail (partner · Coming up · Tonight), habit cards + notes unchanged | canvas `Home-H1-*` · `BRIEF-home.md` | `Today`, `ScorePill` |
| This week | S3 dashboard + S1/S2 parts, points, needs a hand, last week | canvas `Week-S*` | `WeekPage`, `scoreWeek` |
| Calendar | **Day** (new) · Week · Month · Timeline | canvas `Calendar-day*` | `Calendar` (`dv-*`) |
| Projects | Table · Lanes · Timeline · Cards + the project page | canvas `Main`, `Projects-*`, `Project-page-table` | `Projects`, `ProjectPage` |
| Tasks · Journal | table · private journal per person | — | `TasksTable`, `Journal` |
| Settings | Account · Habits · Notifications · **Claude** · Appearance · About | canvas `Settings-claude` | `SettingsModal`, `ClaudeSettings` |
| Claude connector | MCP at `/mcp/<private link>`: list / add / tick off / reopen / move, no delete | entry below (8 Nov) | `src/claude.js`, table `claude_links` |
| Motion | tick chip, count-up, exits, lead crown, confetti, reduced motion | `BRIEF-motion.md` | helpers in `index.html` |

**Canvas:** https://claude.ai/artifact/25zw9iYyovGXj73Yxah5di. It's private to the Claude account that made it. **A full copy is in `design/canvas/`**: every artboard, the index, a README mapping rows → picked / built, and the scripts that made the frames.

**Locked:**
- **Identity:** blue `#1F6FEB` (default accent), ink `#15171A`, **General Sans** (allgreen font; Inter still a font option), sky gradient ground, a white sheet. A rebrand was rejected: "keep the identity same". As of the 9 Nov refresh the accent **travels with the theme** — the primary CTA is now `--accent-deep` (deep blue on Sky, deep orange on Peach, etc.), no longer hardwired ink.
- **Points:** task 10 · subtask 3 · on time +5 · helping +5 · habit 2 · journal 2 · focus 3. The week runs Mon–Sun, the day turns at 4am (IST), and the race is to 100.
- **Home and Calendar:** Home stays a list, because "we both don't have a schedule". The hour timeline lives in Calendar › Day.
- **Multi-space Phase 1 is LIVE (Version `2df60c9b`):** be in multiple 2-person spaces + a sidebar switcher + invite links/codes + new-partner signup-and-join — see the 2026-11-11 (later³) entry. Each space is still 2-person; **teams (N>2) = Phase 2.**
- **Claude connector:** acts as the person; ticking off is "kill", and there's no delete.

**Open, not started (ask before starting any):**
- **People and accounts:** invites / more partners; password reset by email.
- **Calendar:** the calendar week starts Sunday while points run Mon–Sun.
- **Phone:**
  - Today's week strip clips at 375 px
  - not installable yet (no manifest)
  - no check on a real phone so far
- **Claude:** no real connection to the deployed link tested yet.
- **GAPS.md tier 2:** reminders, the background notifications, habits for past days, etc.
- **UI language refresh** (Sky + moments): **LIVE as of 2026-11-10** (Version `5e13d3a8`). Themed accent travels to the CTA, glass side panel, jewel discs, dotted dividers, General Sans — on **Home + the side panel only**. Still to do: real-phone eyeball, then roll the language to Calendar / Projects / Tasks / Journal / Settings. See the 2026-11-09 build entry + `BRIEF-ui-refresh.md`.

**Rules:**
- **Deploying:**
  - deploy = `cd /Users/design/shared-planner && npx wrangler deploy`, then re-check with `?t=` (the edge cache lags)
  - every deploy needs Mahesh's go-ahead
  - **never `deploy.sh`**: it rotates SESSION_SECRET, which logs you both out and kills every Claude link
- **Working:**
  - local dev = launch config `hate-club` (:8787); test sign-ins are in `.dev.vars` comments (git-ignored, never repeat them)
  - design gate: brief → Mahesh's yes → build → log here + `PARITY.md`
  - other files: `GAPS.md` (audit), `BRIEF-*.md` (one per pass)

---

## 2026-11-12 (later): Slice 2 — presence + nudges/boosts — **BUILT, local-verified, NOT deployed**

Second engagement slice (his picks: one-tap cheer / nudge once-a-day / activity-only presence no "last online" / enrich the rail). Makes each person's day visible and the wave contextual — all grown from the existing `sendWave`/`waves`/`.wavefx` + `focus` plumbing.
- **Presence line** — the Today rail's partner block (`.hm-pres`) now reads from *today's activity only*: "Riya · read today ✓ · 2 done", live "**Focusing now** · label" (pulse dot `.hm-pdot`, from the active-space `focus` row), or "Hasn't shown up yet today". Computed in App as `partner={done,kept,journaled,focusing,late,anything}` (tasks done_at today · habits kept · `jdays[TODAY+'|'+id]` · focus.started_by===other), passed to Today.
- **Nudge** — a one-tap "Nudge <name>" in the rail, shown **only when the partner has done nothing today** (`!anything`); **capped once/day** via `localStorage sp_nudge_<space>_<TODAY>` → becomes "Nudged today ✓" (disabled). The 🫶 FAB stays for free-form warmth.
- **Cheer (boost)** — a one-tap "Cheer <name> on" shown when the partner `anything`.
- **Wave kinds** — `sendWave(emoji,kind,note)`; waves row gained `kind` ('wave'|'nudge'|'boost') + `note` (lazy `ensureWaveKind` ALTER, gated `wave_kind_ready`; `kind`/`note` added to TABLES.waves whitelist + schema). The receive `useEffect` now varies copy by kind: nudge → "<name> is rooting for you — do your one thing?", boost → "<name> cheered you on 👏", wave → unchanged, each on the existing center-burst + notify.
- **Verified local** (wrangler dev, desktop + 375px, as Mahesh): rail shows "Hasn't shown up yet today" + "Nudge Riya"; tap → toast "👋 Nudged Riya" + button "Nudged today ✓" (persists across reload); no console errors; mobile rail stacks clean. **Code-verified (not force-triggered):** the Cheer branch + the received nudge/boost copy/burst (same plumbing as the working nudge send + the pre-existing wave burst).
- **Files:** `public/index.html` (sendWave kinds + sendNudge/sendBoost + partner presence + rail block + receive-copy + `.hm-pres`/`.hm-pact` CSS), `src/worker.js` (ensureWaveKind + TABLES.waves + loadState call), `schema.sql` (waves kind/note). **Deploy = `npx wrangler deploy`** (worker+frontend; waves columns self-migrate via ensureWaveKind, no script). Next: Slice 3 (daily question, reveal-after-answer).

## 2026-11-12: Engagement program kickoff + Slice 1 — shared "us" streak + combined-first score — **DEPLOYED LIVE** (Version `637df411`)

After a 3-thread research sweep (retention mechanics · couple/accountability apps · Mobbin flows → `IDEAS.md`), Mahesh said "we'll do all." Locked an 11-slice roadmap (research-ordered); each slice goes through the gate one at a time. Roadmap: **1** us-streak+combined score · 2 presence+nudges/boosts · 3 daily question (reveal-after-answer) · 4 check-in upgrades · 5 the grow-a-thing (signature) · 6 bookended ritual · 7 per-item privacy · 8 milestones+keepsake · 9 onboarding+pledge · 10 weekly recap · 11 PWA+widget · later: monetization (cosmetics only), teams N>2.

**Slice 1 built** (his picks: either-feeds / combined-first keep-split / all-3-forgiveness / confetti at 7·30·100). The app's posture flips from head-to-head → "we're in this together."
- **Shared "us" streak** — computed from the SAME signals as `scoreWeek` (task done_at, kept habit, journal day, focus) via new `dayActivity`/`usStreak`; no new content query. Either person feeds it; **both = a double-day ✨**; **one missed day/month auto-freezes** (a rule, no state). Shows as the `.usk` flame banner at the top of Today (states: start · building · at-risk · fed · double · broken).
- **Combined-first score** — `ScorePill` now leads "You two · N together", the you–them split demoted but kept (hidden on phone). `WeekPage` race retitled **"Together to {2×100} this week"** + a "You two · N together" chip; the two-runner track stays as the demoted head-to-head.
- **Forgiveness** — auto-freeze (above) + **partner-cover** ("I've got today" when at-risk) + **first-repair-free** ("bring it back"). New `streak_state(space_id PK, covered_days, repairs)` table, lazy `ensureStreak` (gated `streak_ready`, self-applies on first load like ensurePersonal/ensureImport); endpoints `POST /api/space/cover` + `/api/space/repair` (membership-gated). `repairOffer` computes the gap days to fill. Milestone confetti at 7/30/100 via `celebrate()`, once each (`sp_uskm_<space>_<n>`).
- **Verified local** (wrangler dev, desktop + 375px, as Mahesh): banner at-risk→cover→"2 days · together · Fed today", toast "💛 Covered today — the streak's safe", combined pill, Week "Together to 200", no console errors, phone pill collapses to "You two N" without pushing the greeting. Streak is space-state so it's shared/symmetric (Riya sees the same). Repair + milestone paths are code-verified (mirror the working cover path), not force-triggered.
- **Files:** `public/index.html` (usStreak/dayActivity/repairOffer/UsStreak + `.usk` CSS + ScorePill/Week edits + App wiring), `src/worker.js` (ensureStreak + loadState + 2 endpoints), `schema.sql` (streak_state). **DEPLOYED LIVE 2026-11-12 (Version `637df411`)** via `npx wrangler deploy`; live-verified: usk/scp-together/usStreak markers in HTML, `/api/space/cover` + `/api/space/repair` → 401 signed-out, streak_state self-creates on first authed load. Git still uncommitted. Next: Slice 2 (presence + nudges/boosts).

## 2026-11-11 (later⁵): Import your tasks into a space — **DEPLOYED LIVE** (Version `8f429a69`, with later⁴)

**Request:** on a new space, a button to pull in my existing tasks ("importing basically"). Confirmed: **copy** (one-time), **open tasks only**, source = a **picker with per-space counts + "All"**, **drop project links** for v1.

**Built — backend (`src/worker.js`):** `copied_from` column on `tasks` (lazy `ensureImport()`, gated by `import_ready`). `POST /api/space/import {target, source}` (source = a space id or `'all'`): copies my open, top-level, non-event tasks (+ their open subtasks) from the source space(s) into target — new rows, `space_id`=target, owner=me, project dropped, `copied_from`=original id. Dedups against target rows whose `copied_from` is already set. Cap 300.

**Built — frontend (`public/index.html`):** `nsImport(source)` → `/api/space/import` + refresh + toast; an **Import sheet** (reuses `.nsmodal`): lists your other spaces with per-space open-task counts + an "All my spaces" row (when >1 source). Entry points: a button on the **empty Today state** ("Import N tasks from your other spaces", via `importCount`/`onImport` props) and an **"Import your tasks here"** item in the space switcher — both shown only when you have open tasks elsewhere.

**Verified** in local dev as Mahesh: added 3 open tasks to hate club → switched to the empty "Mahesh & Riya" → the empty-state button showed "Import 3 tasks" → sheet showed "hate club · 3 tasks" → imported → all 3 copied in (owned by me, "TODAY · 3 LEFT"); re-importing showed **"Nothing new to import"** (dedup works, no duplicates). Originals untouched. No feature console errors (transient 401s during logout→login only).

**DEPLOYED LIVE 2026-11-11** (Version `8f429a69`, live sha `71b27edd`) once the Cloudflare Workers incident cleared — shipped together with later⁴. Verified live: `improw`/"Import your tasks here"/"Bring your tasks into" markup + `POST /api/space/import` → 401 (exists). `copied_from` self-applies via `ensureImport` on the next authed load.

---

## 2026-11-11 (later⁴): Personal items that travel across your spaces — **DEPLOYED LIVE** (Version `8f429a69`)

**Request:** don't recreate my tasks/habits in every space — sync them, e.g. Mahesh↔A and Mahesh↔B should share his stuff. Cofounder reframe: **what travels is YOU** (personal habits/tasks), while shared/co-owned items stay per-space. He picked **Model A** (a "Just me — everywhere" flag, auto-travel), habits default ON + tasks default OFF, personal = private to you.

**Grounded:** `space_id = NULL` already meant "show in every space" (loader + `inSpace`), and `habit_logs` is keyed by habit id alone (streaks already global). So small addition, not a rebuild.

**Built — backend (`src/worker.js`):**
- New `personal` column on `tasks` + `habits` (added lazily by `ensurePersonal()`, gated by a `personal_ready` settings flag so it runs once; also migrates existing person-owned habits → `personal=1`). Added `personal` to the TABLES whitelists.
- Loader `inMineP` for tasks + habits: also pulls `(personal=1 AND owner=?me)` — **owner-scoped so personal items stay private** (a partner's client never receives them).

**Built — frontend (`public/index.html`):**
- `inSpace(r)` now returns true for `r.personal` → personal items show in every space.
- A **"Where it lives: This space / Just me · everywhere"** toggle (reuses `.ownerseg`) in both the task editor (default This space) and habit editor (default Just me), with a privacy hint. `personal` threaded through `baseTask`, `TASK_FIELDS`, `saveTask`, `HABIT_FIELDS`, `saveHabit`, and both editors' form state.

**Verified** in local dev as Mahesh: his 3 existing habits **auto-migrated to personal** and now appear in the "Mahesh & Riya" space (was "No habits yet") with full config + shared streak; the habit editor shows "Just me · everywhere" selected + the privacy hint; the task editor has the toggle defaulting to "This space"; "Whose" correctly lists Riya. No feature console errors (transient 401s during logout→login only). Privacy: personal items are owner-scoped, so Riya never loads Mahesh's.

**DEPLOYED LIVE 2026-11-11** (Version `8f429a69`). The `personal` columns + the habit migration self-apply once on the remote via `ensurePersonal` on the next authed load. (The "Copy into a space" follow-up became later⁵, the import feature.)

---

## 2026-11-11 (later³): Multi-space Phase 1 — multiple partnerships + switcher + invites — **DEPLOYED LIVE** (Version `2df60c9b`)

**Context:** he wants to partner with multiple people (and later, teams). Cofounder analysis first (the DB was already schema v3 "spaces" — spaces+members many-to-many, content space-scoped, owners person-id based, `scoresOn()` already turns the race off for `kind:team`). Decision: **generalize the Space** — a partnership is a 2-member space, a team is an N-member space. **Phase 1 = multiple 2-person partnerships only** (no de-assume-2 / teams yet). His picks: invite by **link/code** (works for new people), switcher at **sidebar top**, **each space its own world**.

**Built — backend (`src/worker.js`, `schema.sql`):**
- `invites(code, space_id, invited_by, status, created_at, used_at, used_by)` — created lazily via `ensureInvites()` (no migration step; self-creates on remote).
- Public endpoints (before the auth gate): `GET /api/invite/peek?code=` (inviter + space name), `POST /api/invite/signup` (brand-new person makes an account + joins + gets a session).
- Authed endpoints: `POST /api/space/create`, `/api/space/invite` (reuses one open code per space), `/api/invite/accept` (signed-in join), `/api/space/leave`. (The generic commit still blocks spaces/members; these are dedicated.)

**Built — frontend (`public/index.html`):**
- The content was *already* space-scoped via `inSp()`/`inSpace`. Added `switchSpace()` (persists `sp_space`), the **sidebar space switcher** (`.spacesw*`: current space + member avatars + chevron → your spaces + "New space"; "Invite someone" shows only while a space has <2 members, keeping Phase 1 strictly 2-person).
- **New-space + Invite modal** (`.nsmodal`): name it → create → auto-switch → shows the invite **link + code** with Copy.
- **`JoinInvite`** screen: opening `?invite=CODE` while signed-out peeks the invite and offers name/username/password → signup+join (matches the real auth-card styling). Signed-in, a `useEffect` auto-accepts the code and hops into the space. "Already have an account? Sign in" bypass via `wantSignIn`.
- `s_hateclub` stays the default; nothing migrates.

**Verified** in local dev, full flow: switcher + menu, created "Mahesh & Riya" (auto-switched, **isolated/empty**, race hidden at 1 member), invite link/code shown, signed out, opened the link → JoinInvite → made a new account "Riya" → landed **in the space, 2 people, race live** ("Mahesh leads by 2"); Riya's switcher shows **only** her space (membership isolation). No feature console errors (transient 401s only during the sign-out→join moment).

**DEPLOYED LIVE 2026-11-11** (Version `2df60c9b`, live sha `e68f3108`). Verified live: switcher/JoinInvite/nsmodal markup present, and `GET /api/invite/peek?code=zzz` → `{ok:false,error:"bad_code"}` (so the remote `invites` table self-created; existing hate club space/data untouched). **Phase 2 (teams, N>2)** is the de-assume-2 work (`otherOf`, scoring→leaderboard/off, rail/journal-share/waves for N, roles).

---

## 2026-11-11 (later²): "One for today" — random fact + line of the day — **DEPLOYED LIVE** (Version `0fbd4912`)

> **Redesigned same day (his feedback: boxed card "too shitty", drop the header):** stripped to a borderless close — no card/tint/border, no "ONE FOR TODAY" header, no category tag. Just the fact, then the line in Fraunces italic + author, and a faint "Another". And **changed the pick to random on every page load** (`useState(pick)`) instead of the date-seeded daily — so it's no longer a shared daily pair (both people now see their own, fresh each refresh); "Another" reshuffles in place. Deployed Version `0fbd4912` (live sha `8cf2df0d`). (First build was the boxed/daily version, Version `496544ba`.)


**Request:** a notebook-back-page random fact (nature/animals/space/art/world/movements…) + a "line of the day". Picks: curated local pack (massive, no repeats for ≥30–60 days), lines = poetry + witty + wisdom, placed at the bottom of Today, daily + a shuffle.

**Built** in `public/index.html`:
- `FACTS` (**86**, tagged by category) + `LINES` (**65**, poet/author/wit, each with attribution) — baked in, internet-sourced but hand-picked and fact-checked (speculative ones hedged).
- `OneForToday` component: date-seeded daily pick (`fact = dayNum % 86`, `line = (dayNum*7+3) % 65`) so **both people see the same pair each day** (shared ritual), with **"Another →"** to shuffle (random, local-only) and **"today's pick"** to reset.
- Card at the very bottom of Today, after "On your mind": soft `--accent-wash` tint (tracks theme), category tag, the fact, a dotted divider, then the line in **Fraunces italic** with its author. Borderless-soft, matches the new language.
- No repeats for ~86 days (facts) / 65 (lines); trivial to grow the arrays.

**Verified** in local dev on Mint (card renders, daily pick, shuffle + reset, theme-tinted, no console errors), then **DEPLOYED LIVE 2026-11-11** (Version `496544ba`, live sha `e71f86ff`; verified live: `OneForToday`, `.oft`, 86 facts, the lines).

---

## 2026-11-11 (later): Theme leak fix — all chrome accents now track the theme — **DEPLOYED LIVE** (Version `3dffd8a2`)

**Request:** on Mint, the "Add task" plus icon (and other bits) were still blue — "make sure the themes are only that colors."

**Cause:** stray hardcoded accent hexes that never went through the theme vars — plus-icon SVG `fill="#1F6FEB"`, selected nav icons `#195FD0`, `+ New project`, profile avatar gradient (`#3FA0FF`), and ~13 muted-blue labels (`#3C6FB0`: eyebrow, section headers, day letters, loading, calendar now-line, week-chart marks).

**Fix (all in `public/index.html`):**
- New token **`--accent-muted: color-mix(in srgb, var(--accent-deep) 60%, #8A93A0)`** — auto-tracks the theme; replaced every `#3C6FB0` label.
- Routed to vars: plus icon + `.dv-now`/`.dv-linow`/donut/focus-ring/`.hk.k` → `var(--accent)`; selected nav icons + `+ New project` + week-chart selected day + `.dv-strip.on` → `var(--accent-deep)`; profile avatar → accent gradient; `.pc-glyph` shadow → `var(--glow)`.
- **Kept as semantic/identity (by the "colors only as dots" rule):** project dots + timelines (`PROJ_COLORS`, `p.color`), person avatars (`personColor`), task-type colors (Task blue / Event purple), done-green `#2E9E6B`, overdue-red `#C64A3B`, note colors, confetti.

**Verified** in local dev on **Peach and Mint** (plus icon, avatar, nav, labels, Save/CTA all retint; project dots keep their colors; `color-mix` resolves; no console errors), then **DEPLOYED LIVE 2026-11-11** (Version `3dffd8a2`, live sha `087cfb3e`; verified live: `--accent-muted` token, themed plus icon/nav/avatar, zero stray `#3C6FB0`).

---

## 2026-11-11: Today header → personalized greeting — **DEPLOYED LIVE** (Version `96366765`)

**Request:** make the Today "Today" H1 functional + empathetic — "hey mahesh, let's finish 'X' first" / "Mahesh!!!! we have work to do". Picked **structure A** (short hook H1 + functional subline).

**Built** in `public/index.html` (Today view only; other view titles unchanged):
- Eyebrow → **the date** ("WED · 11 NOV"); H1 → a **time-of-day greeting with the first name**; new `.hgsub` subline → the functional line (next task + count).
- `greet()` computed in the App shell from real data: `nameOf(whoami)` first name, `new Date().getHours()` (morning/afternoon/evening/night), `counts.today`, `carriedFrom()` (top rolled-over task), today's first non-event task title, `doneToday`.
- **States:** has-work (greeting + *Let's finish "X" first — N to go* / carried variant) · all-done (*That's the lot, {name} ✨*) · clear-day (*A clear day, {name}* — nothing planned). Top task = carried first, else today's first.
- **Daily-rotating** copy: `vary = parseInt(YYYYMMDD)%2` picks between two phrasings per state (stable within a day) — so the warm + cheeky registers he liked both show.
- Renders on web + phone (shared topbar); task title bolded in the subline.

**Verified** in local dev (all three states + date eyebrow, no console errors) and then **DEPLOYED LIVE 2026-11-11** (Version `96366765`, live sha `e54119a4`; verified live markers `.hgsub`, `greet()`, all three state strings). Copy is easily tuned in the `greet()` arrays if he wants a different tone.

---

## 2026-11-09 (later): UI refresh BUILT — Sky + moments → **DEPLOYED LIVE 2026-11-10** (Version `5e13d3a8`)

> **Deployed 2026-11-10** on Mahesh's go-ahead via `npx wrangler deploy`. Verified on the live URL (cache-busted): Fontshare/General Sans, `--primary:var(--accent-deep)`, `--radius-sheet`, glass `blur(26px)`, the Peach accent trio — all present. Lab source copied to `design/ui-lab.html`.


**Pick:** Mahesh chose **Sky + moments** from the lab. Built into `public/index.html` the same session.

**What changed (Home + side panel first, plus the cross-cutting theme/font fix):**
- **Accent travels with the theme.** The real bug behind "I change to orange and the CTA stays blue": the primary CTA was hardwired to `--primary:#15171A` (ink). Now `--primary:var(--accent-deep)`, and each ground preset carries an `ac:[accent, accent-deep, accent-wash, glow]` trio that the theme-apply `useEffect` sets on `<html>` (neutral presets reset to the Sky default). Verified end-to-end: Sky → CTA `#195FD0`; Peach → CTA `#C4471C` (deep orange) + orange glow; reverts clean.
- **Primary CTA** (`.btn.primary`, `.savebtn`): gradient `accent → accent-deep` + `--glow` shadow + inner highlight, instead of flat ink.
- **Font:** **General Sans** via Fontshare (`api.fontshare.com`), set as the default (`theme_font` default `inter → general`; Inter kept as an option). Confirmed loaded (`document.fonts.check` true), not a fallback.
- **Glass side panel** (`.ppanel`, his chosen surface): `rgba(255,255,255,.60)` + `backdrop-filter:blur(26px) saturate(175%)` + glass border + glow + radius `var(--radius-sheet)=22`. Dark grounds get a dark-glass variant.
- **Jewel discs** (`.check` / `.check.on`): frosted empty disc with inner highlight → fills `--accent` with `--glow` when done.
- **Dotted dividers** on Home task rows (`.arow`: `1px dotted var(--dot)`), matching the "My Tasks" reference.
- New `:root` tokens: `--glow`, `--glass`, `--glass-line`, `--dot`, `--radius-sheet`. 5 colored presets got `ac` trios (lavender, peach, mint, rose, slate); ink + midnight got light-on-dark trios; cream/ice/white stay on the Sky-blue accent.

**Glass reach = moments only** (his pick): glass on the sheet, discs, CTA glow — the dense task list stays crisp. Dense-rows mode from the lab was *not* ported.

**Verified in local dev** (`:8787`, test sign-in): sign-in, Home (jewel discs + dotted divider + gradient CTA), the glass add-task side panel, done-state jewel, and the Peach-accent CTA swap. No JS errors from the edits (only the expected pre-auth 401s).

**Not done:** not deployed (needs his go-ahead); not checked on a real phone; other surfaces (Calendar, Projects, Tasks, Journal, Settings) still on the old borders — this pass was Home + side panel by his instruction. Lab source still in session scratchpad (copy into `design/` with deploy).

---

## 2026-11-09: UI language refresh — direction confirmed, lab built (design only, nothing in the app)

**Request:** evolve the UI. Refs: glassmorphism (image 1 "My Tasks") + borderless softness & the font (image 8 "allgreen"); detailing cues from Todoist/Attio/Amie/Linear. "Design in a Claude artifact first", then update the web.

**Confirmed (his words):**
1. **Themes recolor ground AND CTA together** — not just the background; the primary action changes to a deep complement of the hue (orange→deep-orange, etc.), derived shadcn/tweakcn-style. Sky stays default. Evolution, not a rebrand.
2. **Font** = the allgreen one (General Sans/Satoshi family); lab uses Hanken Grotesk (Google-Fonts match), General Sans self-hosts on the web build.
3. **Glass** — show both moments-only and dense-rows; he decides after seeing them.
4. **First surface** — Home + the add/edit side sheet.

**The language:** borderless soft surfaces (shadow + tint, dotted dividers, radius 20–22); a glass recipe (blur + inner highlight + colored glow) on the moments; **status discs become "jewels" colored by task state** (done=accent, to-do=frosted, due-soon=amber, routine=green) — state, not project, so the no-random-project-colors rule holds.

**Lab:** interactive artifact **https://claude.ai/artifact/EgVnNAipiz6NW3SKFMxnVT** — style tiles + Home + add sheet + phone, live theme switcher (Sky/Sunset/Grape/Meadow/Rose) + glass toggle, on real content. Full detail in `BRIEF-ui-refresh.md`. Source in session scratchpad (copy into `design/` once picks land).

**Open:** his picks → theme set, glass reach, confirm font → then port tokens into `public/index.html` (THEMES table replaces bg-only presets; accent tracks theme; self-host General Sans) → PARITY → deploy on his go-ahead. **Not built into the app.**

---

## 2026-11-08: Built: Home H1, Calendar Day, Settings › Claude: LIVE (`0b402bc`; the live page matches, `/mcp` answers from the new worker)

**Request:** "Yes, build all 3".

**Home (H1)** in `Today`:
- **Header:** a score pill sits beside All · Mine ("Tester leads by 4 · 18 – 22", or "6 ahead" on the phone). It opens This week, and the crown drops when the lead changes. The old score strip and the "Coming up" chip row are gone from Home.
- **Quick add** (Enter) adds a task to the selected day.
- **The list:** From earlier stays as it was. Then "Today · N left", where events don't count toward "left". Then routines, then open tasks.
- **Done tasks** fold into "N done today · +pts". A task you just ticked stays 1.6 s, so the strike and the +points chip are seen, then it folds away.
- **The rail:** your partner (done today, overdue, Give a hand · +5 → This week) · Coming up · Tonight (journal).
- **Below,** full width: Habits & focus and On your mind, unchanged ("like how it is rn").
- **Under 1000 px** the rail stacks under the list.

**Calendar · Day** (a new first button; the mode is remembered in `sp_calmode`):
- **The timeline (07–23):** routines, timed tasks and events. Overlaps sit side by side, your partner's items are grey, and the now-line has a time label.
- **All day row:** due dates, project starts and deadlines, untimed events.
- **Beside it:** "Anytime today" and "To schedule". Drag a task onto an hour, or click it and then an hour.
- **Nothing timed:** an empty card with "Add with a time" and "Show the hours".
- **The phone:** a 7-day strip, then the day as a list of times with the now-line.
- **Routines** are now passed to the Calendar.

**Settings › Claude** (`ClaudeSettings`, General › Claude · New):
- **Off:** "Make my private link".
- **On:**
  - the link, masked, shown in full on focus, with Copy
  - a neutral warning, the 3 steps, what Claude can do, Last used
  - Make a new link (asks first, because the old link dies) and Turn off
- **If the server can't be reached:** an error with Try again.

**Verified locally** on seeded data, now deleted:
- **Home:** the pill, quick add, the tick → hold → fold (+10 chip, "You took the lead" toast), and the rail.
- **Day view:**
  - timed and partner items, the now-line, pick-then-click to 15:00, drag-drop to 20:00
  - the empty day
  - the phone list
- **Settings:** off → on.
- **Phone:** no horizontal overflow on Calendar Day. A grid min-width bug was fixed on the way.
- No console errors.

**Not checked:**
- a real Android/iPhone
- real Claude connecting to the deployed link (needs the deploy)

**Known:** the Today week strip still clips at 375 px (an old PARITY gap, not new).

**Deploy:** frontend plus worker, no migration (`claude_links` creates itself). Command: `cd /Users/design/shared-planner && npx wrangler deploy`.

---

## 2026-11-08: H1 picked · Calendar day view · Claude connector (designs on the canvas; the connector built here; all live in the entry above)

**Request:**
> "I like H1 but the habit cards and the on your mind has to be like how it is rn, I like the card layouts rather than just pills" · "the H4 one, the calendar is so beautiful, can we add it to the calendar page … the home like this wouldn't work because we both actually don't have a schedule" · "can we make a claude MCP? which can create a kill tasks when done"

**Designs** (canvas https://claude.ai/artifact/25zw9iYyovGXj73Yxah5di, Page 1)
- **H1 (picked):**
  - redrawn with today's habit cards (count card with 7-day bars and the 44 px −/+, Daily card with streaks, This week's topic) and today's On your mind note cards, full width under the list and rail
  - the rail keeps Partner, Coming up, Tonight
  - the phone frame shows the Daily card
- **Calendar · Day:**
  - a 4th mode next to Week · Month · Timeline: the H4 hour timeline (now-line, both of you side by side, all-day row for deadlines), with "Anytime today" and "To schedule" lists to drag from
  - **Calendar · Day, nothing timed:** the day you'll usually have ("That's normal for you two"), with "Add with a time" and "Show the hours"
  - **phone:** day strip, a vertical list of times, Anytime. This also fills the PARITY gap "Calendar week shows 3 of 7 days, no day view".
- **Settings › Claude:**
  - a new item under General: your private link with Copy, a neutral warning ("Anyone with this link can add and finish tasks as you"), 3 steps to add it to Claude, what Claude can do, Last used
  - buttons: Make a new link · Turn off
- Every frame was rendered and checked before publishing. The phone row moved down to make room for the taller H1.

**Claude connector (built in `src/claude.js`, wired in `src/worker.js`; local-verified, NOT deployed)**
- **MCP over Streamable HTTP**, stateless JSON, at `/mcp/<private link>` (also `/mcp` with a bearer token, for Claude Code).
- **Tools:**
  - `list_tasks` (today / overdue / upcoming / no_date / done_today / all_open; who; project)
  - `add_task` (title, date, time, due, project by name, who, subtask_of)
  - `complete_task`
  - `reopen_task`
  - `move_task`
- **There's no delete tool, on purpose.** "Kill" means tick off.
- **Writes go through `opStatements`,** so the server stamps `done_by` / `done_at` and points work as in the app. Claude's reply states the points (+10, on time +5, help +5).
- **Dates:** in IST (Asia/Kolkata), and a day starts at 4am like the app. It reads "today", "tomorrow", weekdays and YYYY-MM-DD.
- **The link:**
  - it is `hc_<person>.<HMAC(SESSION_SECRET, claude:person:ver)>`, kept in `claude_links` (version and on/off; the table is created if missing, so there's no migration)
  - "Make a new link" and "Turn off" bump the version, so old links die
  - a wrong link answers 404
  - it breaks if SESSION_SECRET is rotated, which is one more reason never to run `deploy.sh`
- **`/api/claude`** (signed in): GET gives the status and link, POST `{action:'new'|'off'}` changes it.
- **Verified locally:**
  - initialize (2025-06-18), the initialized notification (202), tools/list
  - add, a bad day, today, tick off by words (+15 on time), helping your partner (+15), done today
  - two matches ask which one
  - reopen, move to Friday
  - last-used saved, bearer ping, GET is 405, off kills the link
  - the state shows `done_by` = you
  - test tasks deleted
- **Not built yet:** the Settings › Claude screen, so after deploying there's no button to get a link yet.

**Next:** Mahesh says yes to the three designs. Then build H1 + Calendar Day + Settings › Claude, then deploy it all together.

---

## 2026-11-08: Home, five versions on the variants canvas (design only; H1 picked next)

**Request:** "use claude artifact and create some better UI of home - how can home be some versions". Brief: `BRIEF-home.md`, approved with "Yes, build all 5".

**Made** (canvas https://claude.ai/artifact/25zw9iYyovGXj73Yxah5di, Page 1, rows "Home · five ways" and "Home · on the phone"). The same Thursday in all of them: Partner leads 64–58, 2 overdue.
- **H1 · One list:** the day leads, the score is a pill, habits are chips, slim right rail (Partner, Coming up, topic, notes, journal)
- **H2 · Me | Us:** my day on the left, then Us on the right (race to 100, points by day, Partner's day with "Give a hand · +5", Coming up, Wave back)
- **H3 · Game board:** the head-to-head band, a "Best next move" card, points on every row, Points so far, Partner could use a hand, Streaks
- **H4 · Day plan:** an hour timeline with a now-line, plus an Anytime list beside it ("drag onto a time")
- **H5 · Bento:** tiles for Today, Race, Partner, Habits, Focus, Coming up, Topic, Notes

Each has a desktop frame (1440) and a phone frame (390×844).

**Assumed** (Mahesh didn't answer brief decisions 2–3):
- notes stay in H1 and H5 only, so the pick also answers the notes question
- Get started isn't shown, because it's a day-zero state

**Checked:**
- rendered every frame locally before publishing
- fixed:
  - routine rows didn't line up with task rows
  - "Partner" was clipped in the race
  - H3 total said 41, corrected to 45
  - in H4 the now-label covered 15:00 and the focus block was clipped
  - the H5 wave overlapped a tile
- references: Mobbin's Hilos ("Recommended next"), Plain (quick add), Attio home

**Canvas:** Mahesh had added a Page 2 (Artboard 1) meanwhile. The index was rebuilt on his version, so nothing of his was lost.

**Next:** Mahesh picks a version (or mixes). Then draw its states (day zero, clear day, heavy day, behind, tied, Sunday, offline), then build.

---

## 2026-11-08: Motion pass, same identity (LIVE 8 Nov: the live page matches `af592a6`)

**Request:** "keep the identity same but work on animation, transitions etc". Brief: `BRIEF-motion.md`, approved with "Yes, build it". Same blue, Inter, sky ground. Only movement changed.

**Shipped (20 moments in the brief)**
- **Tick:** the check pops, the strike draws left to right, a "+N" chip floats up from the box. It replaces the toast on every tick. Untick reverses it, with no chip.
- **Numbers count up** (450 ms): Today strip, sidebar, This week, leaderboard.
- **Bars and runners glide:** project bars, strip, race and timeline. Runners take 600 ms on the on-screen curve.
- **Lead change:** the crown drops onto the new leader with a small bounce, plus a toast: "You took the lead" or "{name} took the lead".
- **Confetti** in your two colours plus blue, when you win the week (shown once, on the Monday after) or finish a project.
- **Wave:** the burst stays, and 6 small hearts drift up.
- **Streak grows:** the flame bumps.
- **Focus ends:** the ring completes, then one soft pulse, then it resets.
- **Every exit now animates:**
  - sheets slide back out (from the bottom on the phone)
  - modals fade and shrink slightly
  - toasts drop out
  - rows fold away when deleted or moved to today, and Undo brings them back
- **Small touches:**
  - a wrong password shakes the field
  - every button presses to `scale .97`
  - a 10 ms buzz on Android, only straight after a real tap
- **Cut, on purpose:** switching tabs and project views, and habit +/−, stay instant.

**How**
- **Tokens in `:root`:**
  - `--ease-out` (the curve that was already there)
  - `--ease-move`
  - `--ease-pop` (rare moments only)
- **CSS transitions** for anything that can be re-triggered; `element.animate` for one-shot moments.
- **`useLinger`** holds a closing sheet, modal or toast for its exit, then unmounts it. A quick reopen lands fully open.
- **`canvas-confetti` 1.9.3**, loaded from jsdelivr only the first time it's needed. No motion library.
- **Reduced motion:** fades and colour changes stay. Slides, scales and bounces go. Confetti, hearts, chip and shake are off. Numbers and bars jump to their value.

**Fixed while verifying**
- cdnjs serves only the CommonJS build of canvas-confetti (`module is not defined`). Switched to jsdelivr `dist/confetti.browser.js`.
- New-row arrival lost its class on quick re-renders. Now each row is timestamped the first time it's seen, and only rows from the last 400 ms animate in. Rows on first load don't animate.

**Verified locally:**
- tick → chip, strike, score 8 → 18, server `done_by` set
- sheet close and quick reopen; settings exit
- note delete + Undo
- carry fold, row arrival
- lead toast + crown
- wave hearts
- confetti on Finish project
- the reduced-motion rule present
- no console errors beyond the browser refusing vibrate on synthetic clicks

**Not checked:** the phone slide-up on a real device. Test data was cleaned up.

**Design system:** no new colours, sizes or components. Only motion tokens and classes were added: `.stk`, `.ptchip`, `.wpart`, `.closing`, `.fresh`, `.bump`, `.rowin`.

**Parity impact:** both widths. The phone sheets enter from the bottom instead of the right, on purpose (see `PARITY.md`).

---

## 2026-11-08: Everything picked: own sign-ins, points + This week, Projects views, project page: LIVE (8 Nov 01:55 IST, via `migrate4.sh`)

**Request:** "complete all, dont wait for mobbin things". Built from the approved briefs and canvas picks. Sign-in is my own design, since the Mobbin refs never came.

**Shipped**
- **Sign-in:** one calm card at normal sizes.
  - username + password with a show/hide eye; the last username is remembered
  - errors spelled out: "4 tries left before a 1-minute wait", a lock countdown, and an offline message
  - **first-time setup**: the shared passcode once → "Which one is you?" (only people without a sign-in) → name if unset → username + password ("username taken" handled)
  - Settings › Account: your name, @username, change password, people in the space ("Has a sign-in / Not set up yet"), Sign out
  - the "Who's this?" picker and the device switch are gone
- **Server:**
  - PBKDF2-SHA256 at 50k rounds (~4 ms) with a salt per person
  - v2 cookies carry the person; the old passcode cookie only opens setup
  - 5 wrong tries → 1-minute lock, per username, and per IP for the passcode
  - `done_by` / `done_at` set **by the server** when a task is ticked
  - you can only rename yourself
  - state is scoped to your spaces; private journal entries are only sent to their owner, with `journal_days` (dates only) so they still score
  - password fields never leave the server
- **Points** (per space, Mon–Sun, the day turning at 4am):
  - task +10, subtask +3, on time +5, helping +5
  - habit kept +2 (count habits: ≤ aim), journal +2, finished focus +3
  - teams have scores off unless turned on
  - "needs a hand" = 3+ overdue, or under half of the week's tasks by Thursday
- **This week** = S3 base + S1 + S2:
  - race to 100 with a dashed pace line
  - needs-a-hand card: Take one (moves it to Both, with Undo) · Send a cheer
  - fresh-week card with last week's result
  - points so far (lines plus pace; labels kept apart)
  - leaderboard with weeks won
  - points by day, habits kept (per-day dots), tasks this week (donut), still open (table)
  - a This week / Last week switch
- **Today:** score strip ("You're ahead by N", tap for the week), and a "+N · done on time · you helped" toast on every tick. Sidebar: "This week 5 · 22".
- **Projects:**
  - one page with a **Table · Lanes · Timeline · Cards** switch (remembered)
  - Filter by Active / Finished / All, Owned by, Sort by Deadline / Progress / Name / Newest; summary line
  - empty states: none · filter matches nothing · all finished
  - table: grouped by deadline, next task tickable, the row opens the project, the ⋯ menu edits
  - timeline: 12 weeks from Monday, runway bars, deadline diamonds, task dots, today line
  - phone: the table becomes a list and lanes scroll sideways
  - progress counts tasks only (gap #22)
- **Inside a project:** a full page instead of the side panel: breadcrumb, Edit / Finish project / Reopen, facts row, **List · Table · Timeline**, materials. The table has expandable subtasks and Done / on time / Overdue status.
- **Calendar:** a week with nothing timed folds the hour grid ("Show the hours"); otherwise it scrolls to the first timed item or to now; it opens on the 4am day.
- **Journal:** private by default; "Share tonight's entry with {name}"; your private entries are marked "Only you".
- **Focus:** a finished session is logged once (by whoever started it) and the timer resets. The 5-second polling stops when time is up (gap #20).
- **Phone:** tabs are Today · Week · Calendar · Projects · More (Tasks, Journal, Settings, How it works).
- **Name:** "hate club" everywhere (title, top bar, footer, intro).

**Verified (local, desktop 1280 + phone 375, as both people)**
- setup with a v1 cookie, and with no cookie (wrong passcode, name required, username taken)
- sign out → wrong password → sign in
- ticks score correctly (+3 subtask; +20 = task + on time + help), with `done_by` from the server
- a private journal entry stays private but counts (+2)
- a focus session logged after its end time passed
- all four Projects views, the project page Table view, the calendar fold, the More sheet
- no script errors (only the 401/409 responses the tests triggered on purpose)

**Fixed in testing:**
- the server was putting private journal entries into the space
- the points-chart labels overlapped
- the open-tasks table clipped its Status column
- the timeline Today pill covered the first week label
- the phone chart text was unreadable
- "No tasks yet" showed on projects whose tasks were all done
- the calendar opened on the next week after midnight

**Not done:**
- invites and new spaces (the switcher appears with the second space)
- password reset by email (for now Mahesh resets one by clearing that person's sign-in)
- Calendar and the Today date strip still start weeks on Sunday, while points use Mon–Sun (weekly topics are keyed by Sunday)

## 2026-11-08: Spaces structure (data only, screens unchanged): LIVE (via `migrate4.sh`, which includes migrate3)

**Request:** "Yes, build it now" (`BRIEF-people-spaces.md` decision 1): build for partner / friends / teams now, keep the two-person screens.

**Shipped (local-verified, not deployed)**
- New tables `people`, `spaces`, `members`. Every project, task, habit, note, topic and journal entry has `space_id`. Owners are a person id or `everyone`. The focus timer and the wave are one row per space.
- `migrate3.sql` + `migrate3.sh` move today's data into one space, "hate club" (kind partner; Mahesh + partner, names taken from the old settings). It's additive and safe to re-run; checked by running it twice locally.
- App:
  - names and colours come from people; "Both" becomes "Everyone" once a space has 3+ members
  - the owner picker and filters list every member
  - Who's this? shows one card per member and saves a new name to the person
  - new rows carry the space
  - a device that remembered `me` / `partner` is mapped once
- Worker: translates what a tab on the old build writes (`me` / `partner` / `shared`, focus `shared`, wave `latest`, journal `<date>_me`, the `meName` / `partnerName` settings).
- Caught and fixed in testing: the journal-id rule turned `<date>_p_partner` into `<date>_p_p_partner`; it now matches only exact old ids.

**Not done:** the space switcher (it appears with the second space), invites, real accounts (the sign-in redesign waits for Mahesh's Mobbin refs), and brief decisions 2–4 (they only matter once a second space exists; the journal stays visible inside the space, as before).

## 2026-11-05: Variants canvas: Projects redesign, This week scoreboard, sign-in (design only; picks built and live 8 Nov)

**Surface:** both (desktop frames + one phone frame)
**Request:** "I hate the projects board · make 4–5 variants before anything · gamify, who's winning, who needs help · empty states · table/list · ID + password each". Brief `BRIEF-projects-scoreboard.md`, approved with the recommended answers.

**Shipped (canvas)**
- Canvas: https://claude.ai/artifact/25zw9iYyovGXj73Yxah5di (Design type, 16 artboards; source in session scratchpad only)
- Projects: A Table · B Deadline lanes · C Timeline (12 weeks, runway to each deadline) · D Next-step list · E Dense cards
- Projects states: no projects yet · filter matches nothing · all finished · phone list (chips All/Mine/Theirs/Both/Finished)
- Inside a project: List · Table · Timeline switch, shown as a table with subtasks
- This week: S1 head-to-head · S2 race to 100 with a pace line · S3 dashboard widgets · Today score strip with the "+15" moment · Monday-morning empty week
- Sign in: who → password → wrong password (4 tries left, then a 1-minute wait)

**Design system**
- used: the app's own look (sky ground, white canvas, `#1F6FEB`, ink, Inter, pills)
- small-text greys were darkened to `#4B5866` to pass 4.5:1
- added: nothing to the system

**Assumptions to confirm**
- owners are shown as a mix (live data has all 6 as Partner's)
- task names "Home page copy", "Case study images", "Brand moodboard" are samples
- every score is a sample week
- phone tabs proposed as Today · Calendar · Week · Projects · More

**Picked (Mahesh, 8 Nov)**
- Projects: **A Table, B Lanes, C Timeline and E Cards all ship, as views of one page** (a view switch). D is dropped.
- Empty states: approved. Inside a project (List · Table · Timeline): approved.
- This week: **S3 dashboard is the base.** Keep its points so far, habits kept, needs a hand, leaderboard and open tasks. Add **S1's points-by-day chart and its "could use a hand" card**, and **S2's "race to 100 by Sunday" track**.
- Sign-in: **rejected ("shitty")**. Mahesh is sending Mobbin references; redesign after those arrive.
- New requirement: **more than one partner**. A has one romantic partner, several friends, and teams with B and C, so a shared task lives in a shared project inside a team. It's two people for now, but the structure must allow this later (`BRIEF-people-spaces.md`).

## 2026-11-05: Trust pass (GAPS.md tier 1): LIVE (`978f10d`)

**Surface:** both (one responsive file, `public/index.html`), plus the worker (`src/worker.js`)
**Request:** "find gaps, analyze first" → Trust pass first → brief `BRIEF-trust-pass.md` → approved with all recommended answers (D1–D6)

**Shipped**
- **From earlier** group on Today:
  - missed plans ("planned Tue") and missed deadlines
  - row actions: Today · Pick a day · Unplan, plus a group-level Move all to today (with Undo)
  - collapses after 5
  - "Nothing new today" when only carry-overs remain
  - the Today badge counts carry-overs
  - Tasks › Overdue now includes missed plans
- **Who's this?** on a device's first open: two name cards; if the partner has no name yet, their card asks for one. The phone version is full-screen.
- **Labels from the viewer's side:**
  - You / {other} / Both in the owner picker, the Calendar and Tasks filters, the project panel, the journal, the wave and the focus timer
  - "Mine" is the viewer's own tasks
  - avatars use real initials
- **D1:** the Me/Partner switch moved out of the top bar into Settings › People ("This device is Mahesh · Switch to …"). "Your name" and "Their name" edit the right person.
- **D2:** the day turns over at 4am. The app re-checks on focus and every minute, and Today follows if you were on it.
- **Subtasks:**
  - the edit sheet shows "Subtask of *X* →" and saving keeps the parent
  - a subtask due today shows once (nested under its parent, or on its own with "in X")
  - the parent opens by itself when a subtask is due
- **Saving:**
  - an outbox kept on the device (`sp_outbox`), sent in one batch to the new `/api/ops`
  - edits send only the fields that changed
  - habit +/− sends a delta that the server adds up
  - refreshes started before a save are ignored
  - a bad response keeps the last good data on screen
- **Sync status:**
  - sidebar footer line: Saving… / Offline · N waiting / Couldn't save · Retry
  - phone: a pill in the top bar
  - error toast with Retry
  - Journal says "Saved · 7:42pm", "Not saved yet" or "Not sent yet", and the draft survives a tab switch
- **Delete:**
  - task, note, link: Undo toast (the server delete waits 6.5s; leaving the page sends it)
  - project: confirm with counts ("2 are {other}'s") plus **Finish it instead** (D4)
  - habit with history: confirm with the number of days
  - the server deletes children in the same batch
- **Projects › Finished · N** list, with Reopen in the panel.
- Fixed: project Kind showed blank for old `plain` projects. Notes no longer overwrite the other device's edit.

**States verified (local wrangler dev, desktop 1280 + phone 375, both identities)**
- carry-over present, carry-over only, all clear
- partner first run: name unset → name entered
- switching device identity
- offline (change waiting → sent on reconnect)
- server error: Retry toast, Retry sends it
- failed refresh doesn't blank the app
- note delete, Undo, then a real delete
- project confirm → Finish → Finished list → Reopen
- habit ±3 lands on the server as ±3
- clock moved +1 day → Today moved
- journal draft kept, then "Saved"
- confirm as a bottom sheet on the phone
- no console errors

**Design system**
- used: `.toast`, `.modal`, `.overlay`, `.ppanel` sheet, `TaskRow`, `Avatar`, `OwnerSeg`, `.pill`/`.pill.due`, `.view`, `.gbtn`, accent `#1F6FEB`, ink, existing red `#C64A3B`, existing amber `#B4792B`/`#C2704B`
- added (built from those):
  - `.toast-act` (action slot)
  - `.btn.danger` (existing red)
  - `.btn:disabled`
  - the `.carry*`, `.sync*`, `.who*` and `.cf*` classes
  - `.daypick`, `.devrow`, `.finhd`
  - no new colours or type sizes

**Decisions locked**
- D1 the switch lives in Settings · D2 4am · D3 "Mine" includes Both · D4 "Finish it instead" · D6 git first (commit `28333f8`)
- The phone sync indicator is a dot **plus a short word** ("Offline · 1"), not a bare dot as the brief said: a bare dot didn't read on its own.

**Deferred / not done**
- D5: partner's real name. They'll be asked on their first open.
- Tier 2–4 in `GAPS.md`.
- Two people creating the same week's topic at the same moment can still make two rows. That's rare and left alone.
- Habit +/− sends a delta. If a response is lost after the server applied it, the retry counts it twice. That's rare too.

**Parity impact**
- See `PARITY.md`. Everything in this pass ships on both widths.
