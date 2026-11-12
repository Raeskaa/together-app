# hate club — ideas, engagement & flow map

> Cofounder memo. Written 2026-11-12 after a 3-way research sweep: retention mechanics
> (Duolingo/Finch/Habitica/Beeminder/stickK/BeReal), the couple/accountability-app
> landscape (Paired/Cupla/HabitShare/Focusmate/Forest/Sunsama…), and real flows on Mobbin
> (Finch, Paired, Atoms, Tiimo, Jomo, and ~30 more).
>
> This is strategy, not a build. Any item picked to build goes through the design gate first.

---

## 1. The thesis — what hate club actually is

hate club is **not a to-do app with a friend bolted on. It's a care instrument.** Two people
witnessing each other become who they want to be — quitting the cigarettes, keeping the reading,
doing the creative work. The planner is just the *medium*.

So the design test for every mechanic is:

> **Does this make one person feel seen and helped by the other — or measured against them?**

Seen-and-helped = build it. Measured-against = cut it, however well it "retains."

The research is unusually unanimous on what works for an *intimate pair* (vs a solo habit app or a
big social app):

- **Shared fate** beats individual scores — one flame you both feed.
- **Forgiving** beats streak-as-whip — a miss is recoverable, and a partner can cover you.
- **Cooperative** beats competitive — "you two: 142 together," not "Mahesh 80 vs Riya 62."
- **Present** beats surveilling — "she read today ✓" is warm; a tracking dashboard is creepy.

Every genuine 2-person winner (Finch Goal Buddies, Paired, HabitShare) lives here. Every app people
*complain* about (Duolingo guilt-owl, Habitica shared-HP punishment, couple-tracking surveillance)
broke one of those four.

---

## 2. Honest diagnosis — where we are

**Strong already:** the surface is deep — tasks (5 types, subtasks, carry-over), projects (4 views +
itinerary), calendar (week/month/gantt/day), configurable habits + streaks, shared journal + weekly
topics, a shared focus timer, the 🫶 wave, per-action scoring + race-to-100, notifications,
multi-space + invites, personal-items-that-travel, import, themes + motion, a Claude connector.

**The gap:** we have a lot of *surfaces* and a thin *loop*. Right now the daily rhythm is "we each do
our own tasks and occasionally wave." The two people's days run in parallel; they rarely *touch*. The
whole opportunity is to make the two days **visibly shared and forgiving** — that's the engagement
engine we haven't built yet, and it's mostly cheap reframes of things we already have.

---

## 3. Ranked idea backlog

Effort: **cheap** (hours) · **medium** (a day-ish) · **big** (multi-day). Every one is cross-checked
against ≥2 of the three research threads.

### Tier 1 — the engagement core (cheap, highest leverage, do first)

| # | Idea | What it is | Effort | Source |
|---|---|---|---|---|
| 1 | **The "us" streak + combined-first score** | One shared flame both people feed daily (any task/habit counts); lead every score with "you two: N together," individual numbers secondary. Duolingo: shared-streak users +22% daily completion. | cheap | Duolingo Friend Streak, Paired, Love Nudge "love tank" |
| 2 | **Daily question, reveal-after-you-answer** | One synchronized prompt a day; you see your partner's answer only once you've answered; notification fires when they answer. Turns "one for today" from solo trivia into a shared ritual. | cheap–med | Paired (reveal mechanic), BeReal (synced prompt) |
| 3 | **Waves → nudges + boosts** | Keep the warmth, add context: a one-tap **nudge** offered *only* when your partner hasn't logged today; an **auto-boost** wave that fires when they complete something. Rate-limited so it can't become nagging. | cheap | Finch boosts, Duolingo/Future Pro nudge, ApexHabits rate-limit |
| 4 | **Passive presence line** | Ambient "Riya read today ✓ · focusing now" on Today. The cheapest, warmest form of accountability — no check-in required. | cheap–med | HabitShare, Focusmate, Forest |
| 5 | **Forgiving streaks** | Grace day / monthly auto-freeze / **partner can spend a freeze to cover you**; Finch-tone repair ("it's okay to miss a day — you're here today, that's what matters"); first repair free. Add **"Skipped"** as an honest state next to Done; swipe-to-triage carry-overs instead of a guilt pile. | cheap–med | Finch repair, Paired freeze, Structured replan |

### Tier 2 — the warmth + ritual layer

| # | Idea | What it is | Effort | Source |
|---|---|---|---|---|
| 6 | **A shared thing that grows** | The signature feature. A garden / plant / the cigarette-count-as-a-living-thing that thrives on the *pair's combined* consistency, grows slower on a lapse, and **never dies or scolds**. This is our core warmth lever and a natural home for the cig glide-down. | med–big | Finch pet, Forest trees |
| 7 | **Bookended daily ritual** | Morning: "your one thing today." Evening: a review that moves leftovers and closes with "everything's handled — rest." Weekly: pick the **3 shared goals**. A real home for journal + tasks + score. | med | Sunsama, Tiimo, Life Reset |
| 8 | **Per-item share/private toggle** | On any shared task/habit, choose what the partner sees. Symmetric, opt-in. The single biggest trust lever and the direct antidote to "feels like surveillance." (We have personal-travel + private journal; this generalizes it.) | med | HabitShare, Cupla |
| 9 | **Shared milestones + a keepsake** | Named-count confetti ("3 smoke-free days together"), a **pair** badge at 7/30/100, and a small shared collectible you unlock together — honor the *relationship*, not the app. | cheap–med | Finch stars, Opal gems, Ahead |

### Tier 3 — growth + longevity

| # | Idea | What it is | Effort | Source |
|---|---|---|---|---|
| 10 | **Onboarding that teaches pairing + a pledge** | Create/claim the first shared habit *before* signup; Finch-style invite (pending → expiry → accept/decline) with a pre-filled message; a day-one pair pledge/contract; the "just watch vs do-it-together" fork. | med | Atoms, Finch, Me+ |
| 11 | **Weekly recap you read together** | A gentle shared card: both your wins, the cig trend, the streak kept — celebration, never a report card. | med | Duolingo perfect-week, stoic. |
| 12 | **PWA + a calm widget** | Installable to the home screen + a pushr-style quiet week-dots widget ("your partner's waiting," not a guilt-owl). Also closes a known phone GAPS item. | med | pushr widget, Duolingo (lightly) |
| 13 | **Monetization (later)** | If it ever charges: **one per-pair subscription** (not per-seat), generous free core, gate cosmetics/extras — **never** the emotional core. Paired's #1 one-star complaint is paywalling the heart of it. | — | Paired, Cupla, Locket |

### Deliberately NOT now: teams (Phase 2, N>2)

The research argues *against* rushing it. The magic is the intimate pair; team/competitive framing is
exactly where resentment and churn live. The pair is the moat. Build the engagement loop first;
generalize to N only when a real group asks.

---

## 4. Full flow map (what a pair actually does)

Existing flows marked ✅; proposed new/reworked marked ➕.

**A · Onboarding & pairing**
- ✅ Join via link/code · create space · import tasks
- ➕ Create/claim first shared habit *before* account (value before signup)
- ➕ Invite partner: pick → pre-filled message → **pending (expires)** → accept/decline
- ➕ Day-one **pledge/contract** (both sign)
- ➕ "How can X help?" fork: **just watch** (accountability) vs **do it together**

**B · The daily loop**
- ✅ Open → greeting → tasks → habit check-ins → focus timer → journal → "one for today"
- ➕ Morning: **your one thing** + **presence** ("Riya's up, read already")
- ➕ **Daily question** (reveal-after-answer) as the shared moment
- ➕ Habit check-in upgrades: **press-and-hold** to log, **Done/Skipped**, one-tap **mood**
- ➕ Focus: **join your partner's live session** (presence dot)
- ➕ **Nudge / boost** in place of a bare wave
- ➕ Evening: **review & triage leftovers** → close state ("everything's handled, rest")

**C · Streak & recovery**
- ✅ Per-person streaks
- ➕ **Shared "us" streak**, individual streaks as two chips
- ➕ Miss → **auto-freeze / grace day / partner covers**
- ➕ **Repair** flow (forgiving tone, first free) · celebrate *recovery*

**D · The weekly loop**
- ✅ Weekly topic + links · race-to-100 · week recap chart
- ➕ Pick the week's **3 shared goals**
- ➕ Reframe race-to-100 as a **combined** target (cooperative, not head-to-head)
- ➕ **Weekly recap read together**

**E · Celebration & milestones**
- ✅ Confetti on ticks
- ➕ Named-count confetti · **pair** badge at 7/30/100 · shared collectible unlock

**F · Trust & privacy**
- ✅ Personal-items-travel · private journal
- ➕ **Per-item share/private toggle** · symmetric visibility

**G · Multi-space** — ✅ switch / create / invite / import (keep as is)

**H · Growth & longevity**
- ➕ Shame-free **re-engagement after a lapse**
- ➕ **PWA install + widget**
- ➕ Upgrade/paywall (later; cosmetics only)

---

## 5. Competitive teardown — steal / avoid

| App | What it nails | Steal | Avoid |
|---|---|---|---|
| **Finch** | Goal Buddies, boosts, forgiving repair, never-punishing pet | the *entire* buddy model + repair tone + grow-a-thing | over-customization / Skinner-box checking |
| **Paired** | per-partner streaks side-by-side, reveal-after-answer question, monthly auto-freeze | reveal mechanic, freeze, dual-streak chips | paywalling the emotional core; hetero-couple assumption; questions repeat ~monthly |
| **Duolingo** | Friend Streaks (+22%), nudge, ML-timed reminder | shared streak, one-tap nudge, *one* calm daily reminder | guilt/"you let Duo down" tone, streak-anxiety, loss-aversion widgets |
| **HabitShare** | notify-on-partner-check-off, **per-habit privacy** | passive presence + per-item privacy | needing to drag friends in (keep solo value) |
| **Focusmate / Forest** | live co-presence, intention→report loop | "working now" presence, start-intention/end-checkin | Forest's "someone leaves → tree dies" punishment |
| **Sunsama / Tiimo** | morning-plan / evening-review ritual, warm close | bookended ritual + "everything's handled, rest" | ritual fragility (must survive gaps) |
| **Beeminder / stickK / Spar** | commitment contracts, stakes | *optional, symbolic* stake your partner verifies | stakes/anti-charity as a default — off-brand for warm |
| **Habitica** | party quests | cooperative weekly quest | shared-HP punishment between two intimate people |
| **Atoms** | value-before-signup, identity framing | "votes toward who you're becoming," pre-filled invite | — |

---

## 6. Dark patterns to design against (all three threads flagged these)

1. **Guilt / passive-aggressive notifications** — memed, and users literally report doing *less*.
2. **Shared punishment** — one person's miss damaging the other's progress breeds resentment. Share the *streak*, never the *punishment*.
3. **Streak-anxiety as the main driver** — once the number's big, fear of losing it beats the habit, and people fake logs or password-share to "streak-sit." Keep streaks secondary + always recoverable.
4. **Competitive ranking between the two** — lead with the cooperative total.
5. **Surveillance / control feel** — symmetric, opt-in, "shared by choice." Never always-on tracking.
6. **Nagging** — rate-limit everything; let the *receiver* tune frequency.
7. **Paywalling the heart** — if it ever charges, gate cosmetics, not care.
8. **Ritual fragility** — re-entry after a gap must be effortless and shame-free.

---

## 7. Recommended first three builds

1. **The "us" streak + combined-first score** (Tier 1 #1) — cheap, and it reframes the product's
   whole emotional posture from "scoreboard" to "we're in this together" in one move.
2. **Daily question, reveal-after-you-answer** (Tier 1 #2) — the missing daily *shared moment*;
   reuses the "one for today" slot and the journal plumbing.
3. **Waves → nudges + boosts + presence** (Tier 1 #3–4) — makes the existing wave actually *do*
   something and makes each person's day visible to the other.

All three are cheap, mutually reinforcing, and turn the parallel-lives problem into a shared loop.
Then the signature **grow-a-thing** (Tier 2 #6) becomes the thing worth telling people about.

> Before coding any of these: design gate — flows → states → brief → confirm → build.
