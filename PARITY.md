# PARITY: desktop ↔ phone

> One responsive file (`public/index.html`), so "web" = desktop width (>820px) and "mobile" = phone width (≤820px).

**Last reconciled:** 2026-11-08, Home H1 + Calendar Day + Settings › Claude

Legend: ✅ done · 🟡 partial · ⬜ todo · 🚫 deliberately different

## 12 Nov Slice 2 — presence + nudges/boosts — built, not deployed

| Piece | Desktop | Phone | Notes |
|---|---|---|---|
| Partner presence line (`.hm-pres`) | ✅ verified ("Hasn't shown up yet today") | ✅ verified 375px (rail stacks under list) | today's activity + live "Focusing now · label" (pulse dot); no online-tracking |
| Nudge (contextual, once/day) | ✅ verified (send → toast → "Nudged today ✓") | ✅ verified (persists across reload) | shown only when partner did nothing today |
| Cheer / boost | 🟡 code-verified | 🟡 code-verified | shown when partner did ≥1 thing; same send path as nudge |
| Received nudge/boost copy + burst | 🟡 code-verified | 🟡 code-verified | kind-varied copy on the existing `.wavefx` burst |
| 🫶 free-form wave FAB | ✅ unchanged | ✅ unchanged | still there for anytime warmth |

## 12 Nov Slice 1 — shared "us" streak + combined-first score — DEPLOYED LIVE (637df411)

| Piece | Desktop | Phone | Notes |
|---|---|---|---|
| `.usk` streak banner (flame + states) | ✅ verified | ✅ verified 375px (full-width, wraps actions) | top of Today; only on the real today + when a pair |
| Combined-first `ScorePill` | ✅ "You two · N together · split" | ✅ collapses to "You two N →" (split/unit hidden ≤820px) | min-width:0 header holds; greeting not pushed |
| Partner-cover ("I've got today") | ✅ verified (toast + persist) | ✅ shares the banner | at-risk state only |
| Repair ("bring it back") | 🟡 code-verified (mirrors cover) | 🟡 same | not force-triggered locally |
| WeekPage "Together to 200" + chip | ✅ verified | ✅ responsive (same component) | two-runner track kept below (demoted head-to-head) |

## 9 Nov UI language refresh (Sky + moments) — built, not deployed

| Piece | Desktop | Phone | Notes |
|---|---|---|---|
| Themed accent → CTA (`--primary`=`--accent-deep`) | ✅ | ✅ shared tokens | one responsive file; applies both widths automatically |
| General Sans (Fontshare) default font | ✅ | ✅ | `--font` is global |
| Gradient CTA + glow | ✅ verified | ✅ (same classes) | not yet eyeballed at phone width |
| Glass side panel (`.ppanel`) | ✅ verified | 🟡 phone sheet is `width:100%;border-radius:0` — glass applies, re-check the frosted look full-bleed | |
| Jewel discs + dotted dividers (Home) | ✅ verified | 🟡 not yet checked at ≤820px | |

> Tokens are global so the phone inherits the refresh for free, but **nothing was eyeballed at phone width yet** — do a phone pass after deploy.

## Trust pass pieces

| Piece | Desktop | Phone | Notes |
|---|---|---|---|
| From earlier (Today) | ✅ top of the day card | ✅ same, rows wrap | |
| Who's this? | ✅ centred modal | ✅ full screen | |
| ~~This device / Switch~~ | replaced by sign-in (8 Nov) | replaced by sign-in (8 Nov) | |
| Sync status | ✅ sidebar footer line | 🚫 top-bar pill (dot + short word), tap for the full text | no sidebar on the phone |
| Undo / Retry toast | ✅ bottom centre | ✅ above the tab bar | |
| Confirm delete | ✅ centred modal | 🚫 bottom sheet | on purpose |
| Subtask of X (edit sheet) | ✅ | ✅ | |
| Journal saved state | ✅ | ✅ | |
| Projects › Finished | ✅ | ✅ | |

## 8 Nov build

| Piece | Desktop | Phone | Notes |
|---|---|---|---|
| Sign in / setup | ✅ centred card | ✅ same card, full width | |
| Settings › Account | ✅ | ✅ (More › Settings) | |
| This week | ✅ 3-column dashboard | ✅ one column; chart redrawn narrower so its text stays readable | |
| Today score strip | ✅ | ✅ | |
| Projects views | ✅ Table · Lanes · Timeline · Cards | ✅ table → list rows, lanes scroll sideways, timeline scrolls | |
| Project page | ✅ full page | ✅ facts wrap 2-up, table scrolls | |
| Tabs | sidebar + This week | 🚫 Today · Week · Calendar · Projects · More | the bar can't hold 7 |

## Motion pass (8 Nov)

| Piece | Desktop | Phone | Notes |
|---|---|---|---|
| Tick chip, strike, count-up, bars | ✅ | ✅ | |
| Sheets enter / exit | ✅ from the right | 🚫 from the bottom | on purpose |
| Modals, toasts, row fold | ✅ | ✅ | |
| Lead crown, confetti, wave hearts, flame | ✅ | ✅ | |
| Hover lift | ✅ mouse only | 🚫 none | no hover on touch |
| Tick buzz | 🚫 none | 🟡 Android only | iPhones block vibration from websites |

## Home H1 · Calendar Day · Claude (8 Nov)

| Piece | Desktop | Phone | Notes |
|---|---|---|---|
| Score pill | ✅ "X leads by N · a – b" | ✅ "N ahead / behind" | |
| Quick add, list, done fold | ✅ | ✅ | |
| Rail (Partner · Coming up · Tonight) | ✅ beside the list | 🚫 under the list | on purpose |
| Calendar Day | ✅ hour timeline + side lists | 🚫 day strip + list of times | on purpose |
| Drag onto an hour | ✅ drag, or click then click | 🟡 click then click | no drag on touch |
| Settings › Claude | ✅ | ✅ | |

## Known phone gaps (GAPS.md tier 3, not yet done)

| Gap | Phone |
|---|---|
| Not installable (no manifest or icon) | ⬜ |
| Week strip clips Saturday at 375px | ⬜ |
| Calendar week shows 3 of 7 days, no day view | ✅ Day view: day strip + list of times (8 Nov) |
| No add button without scrolling | ⬜ |
| Note colour and delete are hover-only | ⬜ |
