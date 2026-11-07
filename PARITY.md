# PARITY: desktop ↔ phone

> One responsive file (`public/index.html`), so "web" = desktop width (>820px) and "mobile" = phone width (≤820px).

**Last reconciled:** 2026-11-08, own sign-ins + This week + Projects views

Legend: ✅ done · 🟡 partial · ⬜ todo · 🚫 deliberately different

## Trust pass pieces

| Piece | Desktop | Phone | Notes |
|---|---|---|---|
| From earlier (Today) | ✅ top of the day card | ✅ same, rows wrap | |
| Who's this? | ✅ centred modal | ✅ full screen | |
| This device / Switch | ✅ Settings › People | ✅ Settings tab › People | |
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

## Known phone gaps (GAPS.md tier 3, not yet done)

| Gap | Phone |
|---|---|
| Not installable (no manifest or icon) | ⬜ |
| Week strip clips Saturday at 375px | ⬜ |
| Calendar week shows 3 of 7 days, no day view | ⬜ |
| No add button without scrolling | ⬜ |
| Note colour and delete are hover-only | ⬜ |
