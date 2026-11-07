# Brief: more than two people (spaces)

Mahesh, 8 Nov: *"I am user A. A has one romantic love, multiple friends, and A, B, C can also have a team: a shared task inside a shared project inside a team. These structures can be possible in future; right now it's only for two users."*

## Why each kind of group exists (the intent comes first)

| You're with… | What you come for | What it needs | What it doesn't |
|---|---|---|---|
| **Your partner** (2 people) | Share the day, keep each other going, a little competition | Head-to-head score, waves and hearts, a shared calendar, "could use a hand" | Roles, permissions |
| **Friends** (3–8, e.g. a CEED study group) | Accountability: who's on track this week | A leaderboard of everyone, needs a hand, shared projects | Hearts, reading each other's journals |
| **A team** (A, B, C) | Get shared work done | Shared projects, a task given to one person, the deadline view | Being ranked against each other (scores off unless the team turns them on) |
| **Just you** | Private things | Your own tasks, habits and journal | Anyone else seeing them |

## The structure (one rule: everything lives in a space)

```
Person ── belongs to many ──► Space  (kind: partner · friends · team · just me)
                                 └── Projects ── Tasks ── Subtasks
                                 └── Tasks without a project
                                 └── This week board (points earned in this space)
Person ── owns ──► Habits, Journal  (private by default; can be shared into one space)
```

- A task belongs to one space. Its owner is one member, or **Everyone** (today's "Both").
- **Points count on the board of the space the task is in.** The same week can have you ahead with your partner and behind in your study group.
- **Today shows everything that's yours across all spaces.** Each row has a small dot for its space, plus a filter for "All spaces / just this one".
- **Projects and This week are per space.** You switch spaces at the top of the sidebar, like Miro's team picker or Notion's workspace name.

## How the screens we picked stretch

| Picked | 2 people (now) | 3+ people (later) |
|---|---|---|
| This week: S3 + S1 chart + S2 race | You vs {name}, head-to-head | A ranked list. The race track gets one lane per person (up to ~6); "needs a hand" names whoever is behind |
| Owner filter / picker | You · {name} · Both | You · each member's avatar · Everyone |
| Projects views A · B · C · E | No change | An owner column with avatars |
| Waves | Hearts and cheers | Cheers only; hearts stay in partner spaces |

## What changes now, while it's still two people

- **Build the data this way from the start.** Add *people* and *spaces*, give every project, task, habit and note a space, and turn owner `me/partner/shared` into a person's id, or Everyone.
  - Today's data moves into one space ("hate club", kind partner, Mahesh + partner) in a one-time migration. Nothing is lost.
- **The UI stays two-person** until a second space is created. The switcher appears only once you have two spaces, so nothing gets more complicated today.
- **Sign-in has to be a real account**, because "tap one of two names" can't work once there are friends and teams. Each person gets:
  - their own login
  - an invite link or code to join a space
  - a password reset

  **The look waits for your Mobbin references.**

## Decisions for you
1. **Build the spaces structure now, with one space and the same two-person screens** *(recommended: it avoids rewriting everything when the first friend joins)* / keep it two-person and redo the structure later.
2. **Points stay in the space where the task is** *(recommended)* / one total across all spaces.
3. **Teams: scores off by default**, a team can turn them on *(recommended)* / on everywhere.
4. **Journal private by default**, shareable with one space *(recommended)* / always visible to your partner.
5. **Accounts:** a username (or email) + password, joining by invite code. Email resets come later, since they need an email service. Final look after your references.
