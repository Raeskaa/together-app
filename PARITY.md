# PARITY: desktop ↔ phone

> One responsive file (`public/index.html`), so "web" = desktop width (>820px) and "mobile" = phone width (≤820px).

**Last reconciled:** 2026-11-05, Trust pass

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

## Known phone gaps (GAPS.md tier 3, not yet done)

| Gap | Phone |
|---|---|
| Not installable (no manifest or icon) | ⬜ |
| Week strip clips Saturday at 375px | ⬜ |
| Calendar week shows 3 of 7 days, no day view | ⬜ |
| No add button without scrolling | ⬜ |
| Note colour and delete are hover-only | ⬜ |
