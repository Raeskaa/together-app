# Brief: Trust pass (GAPS.md tier 1, items 1–9)

**Goal:** you can rely on what the app shows. Nothing you owe goes missing. Each of you is yourself. Nothing you save is lost without you knowing.
**Not in this pass:** tier 2–4 (reminders, phone install, rename, and so on).
**Layout rule:** everything goes inside the existing frames. Anything that moves or removes a control is a decision below, not something I do quietly.

---

## 1 · Unfinished work comes with you to Today

**What you ask when you open Today, in order**
1. What's on today?
2. What did I not finish?
3. What's coming?

**Cases**
| Case | Shows as |
|---|---|
| Task planned for an earlier day, not done, no deadline | *Carried over* · "planned Tue" (muted) |
| Task or subtask whose deadline has passed, not done | *Overdue* · "due Tue 9:30pm" (amber, the existing due pill) |
| Event or meeting in the past | **Not carried.** It happened or it didn't |
| The other person's carried items | Follow the All / Mine filter like everything else |
| 6 or more carried items | First 5, then "Show 4 more" |
| Viewing a past or future day in the week strip | No carry-over group (it belongs to today only) |

**Flow:** Today › day card › a **"From earlier · N"** group at the top of the list, above today's items, inside the same card.
Actions on each row:
- tick done
- **Today** (moves it to today)
- **Pick a day** (the existing date field)
- **Unplan** (clears the day, so it goes back to Calendar › To schedule)

Group action: **Move all to today**.

**States**
- Today has items and there are carry-overs: group, then today's list
- Today is empty but there are carry-overs: group, then a one-line "Nothing new today"
- Both are empty: "A clear day ✨" (unchanged)
- Long list: collapsed after 5

**Also:** Tasks table › "Overdue" now includes tasks planned for a past day that have no deadline, labelled "planned Tue". Today they fall under "No deadline".

## 2 · Each of you is yourself

**Cases**
- Partner opens the link for the first time
- Mahesh on a new phone
- Someone taps the wrong person by mistake
- The partner's name is still "Partner"

**Flow (first run):** passcode › **"Who's this?"** with two large cards: **Mahesh** · **{partner name}**. If the partner's name is still "Partner", their card reads "Not Mahesh? Tap and add your name" and opens a name field. Then "How it works" (the existing intro).
- Only runs when this device has never picked.
- Data stays as it is. Nothing is migrated.

**Labels follow the viewer** (stored owners don't change):
| Stored as | Mahesh sees | Partner sees |
|---|---|---|
| owned by Mahesh | You | Mahesh |
| owned by the partner | {partner name} | You |
| shared | Both | Both |

These labels apply in:
- the owner picker in every create/edit sheet
- "Mine"
- the Calendar and Tasks owner filters
- the project panel
- journal tags
- the wave ("Wave to {other}")
- the notifications text
- Settings › People ("Your name" / "Their name" edit the right person)
- avatars, which show real initials instead of M/P

## 3 · The day turns over

**Cases**
- The tab is left open overnight
- The phone is asleep, then opened next morning
- Journaling at 00:30

**Flow:** the app re-checks the date whenever you come back to it and once a minute. If you were on today, it moves you to the new day. Journal, habits and new tasks always use the real current day.
(The turn-over hour is **D2**.)

## 4 · Subtasks stay subtasks

**Cases:** a subtask opened from Tasks, Today or Calendar.

**Flow:** the edit sheet shows **"Subtask of *Draft 1*"** under the title (tap it to open the parent) and hides the subtasks section. Saving keeps the parent link.

**Also:** a subtask due today shows **once** on Today.
- If its parent is in today's list, it shows nested under the parent.
- Otherwise it shows alone, with "in Draft 1".

## 5 · Saving you can trust

**Cases**
- Saved
- Slow connection
- Offline on the phone
- Server error
- Passcode session expired
- Ticking three things quickly
- Both of you editing the same task

**Flow**
- Changes show instantly, as now.
- Each change waits in a small **outbox** until the server confirms it. It retries by itself and is **never** visually undone by a refresh.
- **Sync status:**
  - Desktop: one quiet line at the bottom of the sidebar, under your name.
  - Phone: a dot in the top bar.

| State | Shows |
|---|---|
| All saved | nothing (quiet) |
| Saving | "Saving…" (only if it takes longer than 1s) |
| Offline | "Offline · 2 changes waiting", which send when you're back |
| Server error after retries | toast "Couldn't save *Draft 1*" · **Retry** |
| Session expired | passcode screen. Waiting changes are kept and sent after you sign in |
| Journal | "Saved · 7:42pm" under the button; the draft survives a tab switch |

**Underneath (no UI):**
- A save sends only the fields you changed, so ticking a task can't undo the other person's rename.
- Cigarette +/− sends "+1", not a total, so taps aren't lost.
- A refresh that started before your change is ignored.
- A server error keeps the last good data on screen instead of blanking the app.

## 6 · Delete with a way back

| What | Pattern |
|---|---|
| Task, subtask, note, material, topic link | Deletes at once. Toast: "Deleted *Draft 1* · **Undo**" (6s). Toasts get an action button; the existing `.toast` gains one slot |
| Task with subtasks | The same, with "and its 3 subtasks" |
| Project | Confirm first: "Delete *Statement of Purpose*? This removes 6 tasks (2 are {partner}'s) and 1 link." · **Delete** · Cancel. Then the undo toast |
| Habit with history | Confirm first: "This removes 23 days of history." Then the undo toast |

**Underneath:** a project delete removes its tasks and materials **in one server step**, so nothing is left orphaned.

---

## States checklist
- **Today:** with carry-over · carry-over only · long carry-over · all clear · past day · future day
- **Who's this:** partner name unset · set · switching later
- **Sync:** saved · saving · offline + N · error + retry · expired
- **Delete:** undo toast · confirm (project, habit) · undone
- **Journal:** draft · saved at · failed
- **Subtask sheet:** with parent link

## Design system: reused, nothing invented
- Accent `#1F6FEB` / `--accent-wash`, ink `#15171A`, Inter. The amber due pill already exists.
- `.toast` (gains one action button), `.modal` (confirm, "Who's this?"), `.ppanel` sheet, `TaskRow`, `Avatar`, `OwnerSeg`, `IconBadge`, and the existing day-card list.
- No new colours, radii or type sizes.

## Desktop ↔ phone (one responsive file)
| Piece | Desktop | Phone (375) |
|---|---|---|
| From earlier | top of the day card | same, full width |
| Who's this | centred modal | full screen |
| Sync status | sidebar footer line | top-bar dot, tap for the text |
| Undo and error toasts | bottom centre | above the tab bar |
| Confirm delete | centred modal | bottom sheet |

## Decisions for you
- **D1 · The Me / Partner switch in the top bar.** Today one tap silently changes who you are.
  - (a) Keep it, labelled with names.
  - (b) **Move it into Settings › People as "This device is Mahesh · Switch"** *(recommended: it's set once per device)*. This removes a control from the top bar.
- **D2 · When the day turns over.** (a) Midnight. (b) **4am** *(recommended: a 00:30 journal still counts as "tonight")*.
- **D3 · Does "Mine" include shared items?** **Yes** *(recommended: it does today)* / No.
- **D4 · The project delete dialog.** Also offer **"Finish it instead"** (keeps everything and hides it from the active list; uses the unused `archived` column) / not in this pass.
- **D5 · Partner's real name**, if you want it set now.
- **D6 · OK to `git init` + make a first commit before I touch the code?** *(recommended: the repo has no history and this pass changes how saving works)*

## Build order after your OK
git commit → 5 (saving, because everything else depends on it) → 3 → 4 → 1 → 2 → 6. Then a walkthrough on local desktop + phone with both identities, then you deploy with `npx wrangler deploy` (the worker changes too, but there's no schema change).
