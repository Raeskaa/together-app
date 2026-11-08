# DESIGN LOG

> Append-only. Newest at the top. One entry per design pass. Keep it factual: paths, what shipped, what didn't.

---

## 2026-11-08: Home, five versions on the variants canvas (design only, nothing built)

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

## 2026-11-08: Everything picked: own sign-ins, points + This week, Projects views, project page (built, local-verified, not deployed)

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

## 2026-11-08: Spaces structure (data only, screens unchanged)

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

## 2026-11-05: Variants canvas: Projects redesign, This week scoreboard, sign-in (design only, nothing built)

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

## 2026-11-05: Trust pass (GAPS.md tier 1)

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
