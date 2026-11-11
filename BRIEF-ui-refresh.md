# BRIEF: UI language refresh (glass · soft · themes · allgreen font)

**Opened:** 2026-11-09 · **Status:** ✅ **DONE** — Sky + moments built + verified + **DEPLOYED LIVE 2026-11-10** (Version `5e13d3a8`). Scope was Home + side panel; next is a real-phone pass, then roll to the other surfaces.

## What Mahesh asked
Evolve hate club's UI. Refs he gave (8 screens): wants the **glassmorphism** from the "My Tasks" shot (image 1) and the **no-border softness + the font** from the allgreen reservation shot (image 8); the rest (Todoist, Attio, Amie, card-create, Linear, Attio doc) as "how detailing happens while staying beautiful UX". Design in a Claude artifact first, then update the web.

## Decisions (his words, 2026-11-09)
1. **Themes — ground AND CTA move together.** Today only the background changes; the primary action stays blue. He wants each theme to recolor **both**: orange ground → deep-orange CTA, purple → deep-purple, etc., derived systematically (he said "tweak CN's color" = tweakcn/shadcn). Sky stays the default and the one he likes. It's an **evolution**, not a rebrand (keep the IA).
2. **Font — the allgreen one, pinned.** Warm geometric sans (General Sans / Satoshi family). Lab uses **Hanken Grotesk** (closest Google-Fonts match, the only host artifacts allow); the literal **General Sans** self-hosts on the web build.
3. **Glass reach — show both.** He wants to see **moments-only** and **dense-rows** side by side before deciding. Lab has a live toggle.
4. **First surface — Home + the side panel (add/edit sheet).** Prove the language there, then judge and roll out.

## The language (what "evolution" means)
- **Surfaces:** retire 1px borders → soft shadow + background-tint grouping; **dotted dividers** between rows; radius 16 → 20–22.
- **Glass recipe:** translucent white + blur(22) saturate + inner highlight + soft colored outer-glow. On the moments (status discs, score pill, FAB, floating sheets) always; on dense rows only in that mode.
- **Status "jewels":** disc color = **task state**, not project (keeps the no-random-project-colors-in-chrome rule): Done = theme accent, To-do = frosted ring, Due-soon = amber, Routine = green. Project stays a small dot in the row meta.
- **CTA:** gradient accent→accent-deep, glass variant for quick actions.

## 5 themes in the lab
Sky (default) · Sunset (orange) · Grape (purple) · Meadow (green) · Rose (pink). Each = ground gradient + {accent, accent-deep, accent-wash, glow}.

## The lab
Interactive Claude artifact: **https://claude.ai/artifact/EgVnNAipiz6NW3SKFMxnVT** — style tiles + Home (Today) + the add sheet + phone frames, all recolor with the theme and flip with the glass toggle. Built on his real content (Overwhelmed book, portfolio, STP, cigarette glide, reading streak). Source in session scratchpad; copy into `design/` once picks land.

## Built (2026-11-09, pick = Sky + moments)
Done in `public/index.html`, verified in local dev:
- `--primary` → `var(--accent-deep)`; each ground preset carries `ac:[accent, accent-deep, accent-wash, glow]`; theme-apply effect sets them (neutrals reset to Sky). Peach CTA = `#C4471C` confirmed.
- Primary CTA = gradient accent→accent-deep + glow. General Sans via Fontshare (default font). Glass side panel (blur 26 / rgba .60 / radius 22). Jewel discs. Dotted dividers on Home rows. New tokens `--glow --glass --glass-line --dot --radius-sheet`.
- Moments reach only (dense-rows not ported). Surface scope = Home + side panel, per his instruction.
See DESIGN-LOG "2026-11-09 (later): UI refresh BUILT".

## Next
1. ~~Deploy~~ ✅ done 2026-11-10 (Version `5e13d3a8`). ~~Copy lab into design/~~ ✅ `design/ui-lab.html`.
2. **Real-phone pass** — glass sheet full-bleed + jewel discs + dotted dividers at ≤820px (verified in emulation, not on a device).
3. After he lives with Home + side panel: roll the language to Calendar, Projects, Tasks, Journal, Settings.
