# Brief: motion pass (same identity: blue, Inter, sky ground)

Mahesh, 8 Nov: *"keep the identity same but work on animation, transitions etc"*, and earlier *"a bit playful"*.

## Recon (what the code has today)
- **Stack:** Preact + htm in one file; plain CSS `@keyframes` and transitions; no motion library.
- **One house curve:** `cubic-bezier(.16,1,.3,1)`, ×7. Durations 100–250 ms.
- **Moves today:**
  - sheet slide-in (220 ms), modal pop (200 ms), toast rise (250 ms)
  - wave burst (1.7 s)
  - button press `scale(.985)`, card hover lift
  - race bar `width` (500 ms)
- **Missing:**
  - every exit: sheets, modals and toasts vanish on close
  - tick feedback
  - numbers and progress bars jump
  - list rows pop in and out
- **Reduced motion:** one global rule kills *all* motion, including the fades that help comprehension.

## The rule that sorts every moment
Seen **tens of times a day → small and fast, or nothing**. Seen **a few times a day → a clear move**. Seen **rarely → that's where the playfulness goes**. Nothing that's keyboard-driven or happens on every click (switching tabs and views) animates.

## Moments

| # | Moment | How often | Verdict | What moves | Feel |
|---|---|---|---|---|---|
| 1 | **Tick a task** | tens/day | animate, small | Check fills with a pop (`scale .8→1`, 160 ms); the title's strike draws left to right (200 ms); a **"+10" chip floats up** from the box and fades (500 ms). **Replaces today's toast on every tick.** | crisp |
| 2 | Untick | rare | animate, small | The reverse, no chip | crisp |
| 3 | **Score numbers change** (Today strip, sidebar, This week) | few/day | animate | The number counts up (450 ms) | crisp |
| 4 | **Progress bars** (projects, strip, race) | few/day | animate | Width glides to the new value (400 ms, on-screen ease) | crisp |
| 5 | **Race runners** | few/day | animate | Avatar glides along the track to the new score (600 ms) | smooth |
| 6 | **Someone takes the lead** | rare | **delight** | Crown drops onto the new leader with a small bounce (600 ms) + toast "You took the lead" / "{name} took the lead" | playful |
| 7 | **You win the week / finish a project** | rare | **delight** | Confetti from the top, once (1.2 s); in the 2 colours of you two plus blue | playful |
| 8 | **Wave** (🫶) | rare | delight (exists) | Keep the burst; add 5–6 small hearts drifting up | playful |
| 9 | **Streak grows** | daily | delight | The flame bumps (`scale 1→1.25→1`, 400 ms) when the count goes up | playful |
| 10 | Focus timer ends | few/day | animate | Ring completes, then one soft pulse | calm |
| 11 | **Sheets** (add/edit task, project) | few/day | animate + **add exit** | Open: slide from the right (240 ms). Close: slide back out, shorter (160 ms). Phone: from the bottom | crisp |
| 12 | **Modals** (settings, confirm, intro) | occasional | animate + **add exit** | Open: `scale .96→1` + fade (200 ms). Close: fade + `scale .98` (140 ms) | crisp |
| 13 | **Toasts** | few/day | animate + **add exit** | Rise in (240 ms), drop out (160 ms); a new toast replaces the old one by sliding up, no stacking | crisp |
| 14 | **Rows arriving or leaving** (added task, moved to today, deleted with Undo) | few/day | animate | In: fade + 6 px rise (200 ms). Out: fade + collapse (180 ms). Undo brings it back the same way | crisp |
| 15 | Sign-in wrong password | rare | animate | Field shakes 3 times, small (320 ms) | crisp |
| 16 | Button press | many/day | animate, felt not seen | `scale .97` (120 ms), all buttons the same | crisp |
| 17 | Hover on cards and rows | many/day | small | 1–2 px lift / tint (150 ms), mouse only, never on touch | crisp |
| 18 | **Switching tabs** (Today, Week, Projects…) and **project views** (Table / Lanes / …) | tens/day | **cut** | Instant, like Linear. Motion here would make it feel slow | — |
| 19 | Habit +/− | tens/day | **cut** | The number changes instantly | — |
| 20 | Phone buzz on tick | tens/day | optional | One 10 ms vibration (Android only; iPhones don't allow it from a website) | — |

## Tokens (all in one place in the CSS, reused everywhere)
| Token | Value | Used for |
|---|---|---|
| `--ease-out` | `cubic-bezier(.16,1,.3,1)` (the curve already there) | things entering or leaving |
| `--ease-move` | `cubic-bezier(.645,.045,.355,1)` | bars and runners moving on screen |
| `--ease-pop` | `cubic-bezier(.34,1.56,.64,1)` (slight overshoot) | **only** the rare moments: crown, flame, check fill |
| durations | press 120 · hover 150 · exit 140–160 · enter 200–240 · bars 400 · count 450 · chip 500 · crown 600 · confetti 1200 | |

## Reduced motion (replaces the kill-everything rule)
- **Kept:** fades and colour changes (≤150 ms), so you still see what changed.
- **Dropped:** every slide, scale and bounce.
- **Off entirely:** confetti, hearts, chip, shake.
- Numbers and bars jump straight to their new value.

## Stack
- **CSS transitions** for everything that can be re-triggered mid-way (bars, runners, hovers, sheets), because they pick up from where they are.
- **The browser's own animation API** (`element.animate`) for one-shot moments (chip, crown, flame, shake, row in/out).
- **`canvas-confetti`** (~6 KB from cdnjs, loaded only the first time it's needed) for the win moment.
- **No motion framework.**

## Open risks
- **Exits need a short delay before things disappear.** Sheets and modals currently unmount instantly; adding a 140–160 ms close means holding them a moment. I'll check that Undo and quick re-opens don't catch a half-closed sheet.
- **Collapsing rows animates height**, which can stutter on long lists. It's fine for Today's handful; the Tasks table (dozens of rows) gets fade only.
