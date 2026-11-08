# Brief: Home, a few versions (design only, on the variants canvas)

Mahesh, 8 Nov: *"use claude artifact and create some better UI of home, how can home be, some versions"*.

## What Home is today (Today page, live build `af592a6`)
- **Seven blocks of equal weight, stacked:**
  1. week strip
  2. Get started
  3. score strip
  4. Coming up chips
  5. the day card
  6. Habits & focus
  7. On your mind notes
- **The day's tasks are 5th down.** On a 1000 px screen they sit below the fold when Get started is showing.
- **Who's winning is one thin line.** You said it's the important part.
- **Your partner's day isn't on Home at all.** That includes "needs a hand", which earns help points.
- **The column is narrow inside a wide sheet**, so the sides are empty. This is the same "so much empty space" complaint as Projects.
- **A clear day** is a huge empty card.

## What people come to Home for
| # | Job | How often |
|---|---|---|
| 1 | What do I do today (incl. carried over and due soon) | every open |
| 2 | Tick things off and see the points land | tens a day |
| 3 | Who's ahead this week, by how much | every open |
| 4 | Does my partner need a hand (overdue → help = +5) | daily |
| 5 | Log habits | daily |
| 6 | Start a focus timer | few a day |
| 7 | Jot a note / write tonight's journal | daily |
| 8 | Look at or plan another day | few a week |
| 9 | Wave 🫶 | rare |

## The versions (one realistic Thursday, the same data in all five)
| | Version | Idea | Like |
|---|---|---|---|
| **H1** | **One list** | The day is the hero at the top. The score becomes a compact pill in the header. Habits are one row of chips under the list. Notes and the topic go to a slim right rail. | Things 3 Today |
| **H2** | **Me \| Us** | Two columns that fill the width. Left: my day (tasks, then habits). Right: us (the race to 100, the partner's day with a "Give a hand" button on overdue items, Coming up, Wave). | Linear Inbox + side panel |
| **H3** | **Game board** | The head-to-head leads, with points so far. Every task row shows what it's worth (+10, +5 on time). A "Best next move" card suggests the task that scores most. Most playful. | Duolingo home, Fitbod |
| **H4** | **Day plan** | The hours run down the left. Routines and timed tasks sit in place, with a now-line. Untimed tasks go in an "Anytime" list beside it. The score is in the header. | Sunsama, Structured |
| **H5** | **Bento** | Tiles: the day list is large, plus score, partner, habits, focus, Coming up and a note. Glanceable and fills the width. Risk: everything weighs the same again. | Apple widgets, Amie |

- **Each version gets a desktop frame (1440) and a phone frame (390×844).** That's 10 frames, in a new row on the existing canvas under "Home · five ways".
- **The states come after you pick one:**
  - day zero / Get started
  - clear day
  - heavy day (15+ with carried over)
  - you behind
  - tied
  - Sunday last day
  - offline

## Design system (no new tokens)
- **Same identity:** blue `#1F6FEB`, ink `#15171A`, Inter, the sky gradient ground, the white sheet (radius 16), pills, avatars, the existing points colours.
- **Normal sizes**, per your earlier feedback: 16 px icons, small buttons, no giant tiles.
- **Reuses the canvas's own parts:** the sidebar, ScoreStrip, TaskRow, habit card, `.pill`.

## Parity
- **One responsive file**, so every version shows both widths.
- **The phone keeps the 5-tab bar** (Today · Week · Calendar · Projects · More).
- **H2's right column** stacks under the list on the phone. **H4's hours** become a vertical list.

## Decisions for you
1. **The five versions above**: go as they are? (I'd say yes.)
2. **Notes ("On your mind")**: keep them on Home, or move them to Journal? (I'd move them; Home is about today and the two of you.)
3. **Get started**: keep it on Home until it's done? (Yes, but as a one-line bar, not a card.)
