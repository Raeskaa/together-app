# hate club: gap analysis (2026-11-04)

Sources: a hands-on run on local `wrangler dev` (desktop at 1366 and phone at 375) plus a read-only code audit.
`H` = `public/index.html`, `W` = `src/worker.js`. **seen** = reproduced in the browser. **code** = read from the source.
**Status (2026-11-05):** tier 1 (items 1–9) is done in the Trust pass (see `DESIGN-LOG.md`), plus the project Kind fix from item 17. Tiers 2–4 are still open.

## Tier 1: breaks trust (data goes wrong or disappears)

| # | Gap | Evidence | |
|---|---|---|---|
| 1 | **Unfinished work disappears from Today.** Today said "A clear day ✨ · 0 items" while "Draft 1" (planned for Tue, not done) and its subtask (due Tue 9:30pm) were overdue. There is no overdue or carry-over section. Tasks › Overdue only counts deadlines, so a task planned for a past day with no deadline lands under "No deadline". | H:840-846, H:1118 | seen |
| 2 | **The partner's first visit writes as Mahesh.** `sp_who` defaults to `me` and nothing asks "who are you?". Their habit taps, journal saves, waves and focus sessions all go to Mahesh. | H:1640 | code |
| 3 | **Me/Partner are fixed owners, but they're labelled as if relative to the viewer.** When the partner taps "Mine" they see Mahesh's tasks, their owner picker's "Me" assigns to Mahesh, and "Your name" renames Mahesh. Avatars are always M/P. | H:689, 839, 968, 1229, 1499, 618 | code |
| 4 | **The date never rolls over.** `TODAY` is computed once when the page loads. Leave a tab or phone open overnight and journal saves and habit taps land on yesterday. Saving overwrites yesterday's entry. | H:612 | code |
| 5 | **Editing a subtask detaches it.** `saveTask` always writes `parent_id:null`. Subtasks can be opened from Tasks, Today and Calendar, so pressing Save there turns them into top-level tasks. Due subtasks also show twice on Today. | H:1700-1706 | code |
| 6 | **Failed saves vanish silently.** Nothing checks `r.ok`. On a 500 or with no signal, the change shows, then disappears on the next refresh. Journal "Save" gives no confirmation either. | H:1655, 1665 | code |
| 7 | **Delete has no confirmation and no undo** (there's no `confirm(` anywhere). Deleting a project wipes every task, subtask and material in it, the partner's included. | H:1347 → 1720 | code |
| 8 | **Two people's edits overwrite each other.** Every write sends the whole row, and the last one wins. Ticking a task on a screen that hasn't refreshed undoes the partner's rename or date change. Quick ticks flicker back, and cigarette "+" taps get lost. | H:1655, 1695, 889 | code |
| 9 | **One server error blanks the app for up to 20s.** The `{error}` body is stored as state. A delete in that window can orphan data, and a save in that window resets `done`. | H:1655, W:65 | code |

## Tier 2: features that promise more than they do

| # | Gap | Evidence |
|---|---|---|
| 10 | Notifications don't fire in the background or on phones (no service worker). On iOS the toggle switches on and nothing happens. | H:1472, 1659, 1761 |
| 11 | The "Reminder" type and the deadline time don't remind anyone. They are labels only. | H:622, 1116 |
| 12 | The focus timer never actually ends: no alert, the DB stays `running`, every device polls every 5s indefinitely, and Resume re-sends the "started" toast. | H:803, 1691, 1766 |
| 13 | Events and meetings pile up under "To do" forever (timed ones can't be ticked). The sidebar count includes events and subtasks. | H:717, 1128, 1799 |
| 14 | Journal: the draft is lost on a tab switch, you can't edit or backfill past entries, and writing after midnight files the entry under tomorrow. | H:1416-1442 |
| 15 | Habits can only be logged for today, so forgetting last night breaks the streak. | H:1735 |
| 16 | Today's list is in creation order, not time order. Task times are hidden (only events show a time). | H:722, 840 |
| 17 | Projects can't be finished or archived, only deleted. **Kind shows blank** for existing projects (data says `plain`, the options are project/course/branding; seen). Progress counts subtasks while the panel lists only tasks, so it reads "Tasks · 2" next to "1 of 8 done". | H:1341, 703 |
| 18 | Calendar: Month "+N more" opens New Task instead of the hidden items. Week only covers 7am–10pm, every item is a fixed one-hour block, and items at the same time overlap. Nothing scrolls to the current hour (seen at 6:48pm: 7am–5pm visible). | H:935, 1000, 1049 |

## Tier 3: phone (the partner's main device)

| # | Gap | Evidence |
|---|---|---|
| 19 | Not installable: no manifest, no home-screen icon. It opens as a browser tab, which is also why phone notifications can't work. | seen |
| 20 | Today's week strip pushes Saturday off the right edge at 375px. | seen |
| 21 | Calendar Week shows 3 of 7 days, today is off-screen to the right, and there's no Day view. | seen |
| 22 | There's no add button without scrolling. The 6-tab bar is crowded, and the wave button covers content (the topic field, "All tasks"). | seen |
| 23 | A note's colour picker and delete only appear on hover. On touch, the × is invisible but still tappable. | H:435 |

## Tier 4: name and housekeeping

| # | Gap |
|---|---|
| 24 | **Still called "Shared Planner" everywhere**: tab title, passcode gate, page eyebrow, intro ("How Shared Planner works"), sidebar footer, "SP" mark. The product is "hate club". |
| 25 | No git, no backup or export. `deploy.sh` logs you both out (it makes a new secret) and brings back deleted starter habits. |
| 26 | Weak passcode, no limit on login attempts, no log-out button (`/api/logout` exists). |
| 27 | Dead parts: `routines` (no UI, can't be written), `FocusCard`, the sticky-note settings keys, `cigAimToday`, `weekTopic`, `subtodos`, `archived` with no UI. |
| 28 | Missing basics: search, recurring tasks, reordering, editing a material or topic link, clearing a project's dates, a "Today" jump on the week strip. Weeks start on Sunday. |

## Checked and fine
- IST handling: `ymd`/`parseYmd` use local time and nothing parses `new Date('YYYY-MM-DD')`.
- The 20s refresh does not wipe text while you type (journal, notes, settings and modals keep local copies).
