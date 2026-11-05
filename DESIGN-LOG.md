# DESIGN LOG

> Append-only. Newest at the top. One entry per design pass. Keep it factual: paths, what shipped, what didn't.

---

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
