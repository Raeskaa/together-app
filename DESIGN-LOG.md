# DESIGN LOG

> Append-only. Newest at the top. One entry per design pass. Keep it factual: paths, what shipped, what didn't.

---

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
