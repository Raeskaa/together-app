# Design canvas: what's on it and where each piece went

**Live canvas:** https://claude.ai/artifact/25zw9iYyovGXj73Yxah5di (Claude "Design" canvas type, private).
- It belongs to the Claude account it was made on: hello@trueleap.io, from the session of 5–8 Nov.
- Another Claude account can't open or edit it until it's shared from the canvas's Share menu.

**This folder** is a full copy of the canvas, exported 8 Nov 2026 (version `1794124002-9484`):
- `canvas.json` is the index: positions, titles, pages.
- There is one `*.dc.html` file per artboard. Each opens in a browser on its own. The files expect the canvas's `support.js`, so open them through the canvas, or read them as HTML/CSS.
- `_src/` holds the scripts that produced the frames from 8 Nov (`home_gen.py` makes the Home ×5, `cal_gen.py` makes H1-picked, Calendar Day and Settings › Claude), the app patch `build3.py`, and the motion patch `motion.py`.
  - They have absolute scratchpad paths in them. Treat them as a reference, not something to run as-is.

**Recreating the canvas on a new account:**
1. Create a new canvas from the Design type, named "hate club · Projects + This week".
2. Publish these files to it under `project/`: `canvas.json` plus every `.dc.html`.

## Rows (Page 1, top to bottom)

| Row (canvas y) | Artboards | Outcome |
|---|---|---|
| **Projects · five ways** (300) | `Main` (A Table) · `Projects-B-lanes` · `Projects-C-timeline` · `Projects-D-nextsteps` · `Projects-E-cards` | **A, B, C and E picked as views** (built: Table · Lanes · Timeline · Cards). D was not picked. |
| **Projects · empty, phone, inside** (2000) | `Projects-empty-none` · `-empty-filter` · `-empty-finished` · `Projects-phone` · `Project-page-table` | Built (empty states, phone list, the project page). |
| **This week · who's ahead** (3380) | `Week-S1-head-to-head` · `Week-S2-race` · `Week-S3-dashboard` · `Week-today-strip` · `Week-empty-monday` | **S3 base + parts of S1/S2** were built as This week. The Today score strip was built, then replaced by the H1 score pill on 8 Nov. |
| **Sign in · one each** (5000) | `Login` | Built as its own design (the Mobbin refs never came). |
| **Home · five ways** (6500) | `Home-H1-one-list` **(picked)** · `Home-H2-me-us` · `Home-H3-game-board` · `Home-H4-day-plan` · `Home-H5-bento` | **H1 picked and built (live).** H1 was redrawn with today's habit cards and note cards. H4's timeline moved to Calendar › Day. H2, H3 and H5 were not picked. |
| **Home · on the phone** (8400) | `Home-H1-phone` … `Home-H5-phone` | H1's phone frame was built. |
| **Calendar · day view · Claude** (9800) | `Calendar-day` · `Calendar-day-empty` · `Calendar-day-phone` · `Settings-claude` | **All built (live).** |

Page 2 holds `Artboard-v10d`, an empty artboard Mahesh added himself. Keep it.

**Losers:** the frames that weren't picked are still on the canvas for reference. Delete them only on Mahesh's yes.
