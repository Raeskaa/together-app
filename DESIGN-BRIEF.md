# hate club v2 — Design Brief

**Written:** 2026-11-19 · **For:** the rebuild (PRD.md → this brief → Claude artifact → build → deploy).
**Gate note:** run manually — your `~/.claude/skills/design/SKILL.md` is missing, so no banner. This follows the 8-step gate from CLAUDE.md (context → use cases → flows → states → DS audit → web↔mobile parity → brief → **your confirm** → build). **Nothing gets drawn until you confirm this.**

---

## 0. What we're designing
The whole hate club system, redesigned from scratch, as **one clickable Claude artifact (web + mobile)** before any code is written. The artifact is the design — screens, states, the shell, light + dark — enough to click through and feel it. Spec = `PRD.md`. Direction = your "just UI" Mobbin board.

---

## 1. Direction — RESOLVED: Headspace-derived (see `HEADSPACE-DS.md` for tokens)
Mahesh picked **Headspace** as the reference for the whole design system (2026-11-19). Studied it deep. The system: **cream shell (never cold white) · warm charcoal ink · blue `#1F6FEB` as the CTA (Headspace's product CTA is blue too) · orange + warm pastels for the "moments" (streak, mascot, celebration) · full-pill buttons, big radii · one-thing-per-moment · soft slow motion · warm name+question voice.** Keeps hate club's blue identity — it's literally the Headspace product model, not a recolor.
- **General Sans stays** (it's Aperçu-family, like Headspace's custom font) — the Headspace feel comes from color/shape/voice, not the typeface. Open pick: Nunito/Hanken for more roundness.
- **Illustration = flat-vector blobs + soft-gradient orbs** (corrected — Headspace is NOT claymation).
- **Light + dark** from day one.
- The moments-vs-work rule: gradient/immersive for the moments, calm-but-dense for the tables.

---

## 2. Use cases (who, and the jobs)
| Who | The job |
|---|---|
| Two people (couple / close friends / accountability partners) | Run our days side by side — see today together, not manage a project |
| The active one | Add + tick tasks, keep our streak alive, send a wave, log a mood, journal |
| The quiet one | Get a gentle nudge, see what's coming, feel present without pressure |
| A newcomer (public) | Sign up, start a space, invite my person, learn it in 30 seconds |

**Thesis to protect:** care instrument, not a scoreboard. Forgiving, cooperative, present.

---

## 3. The scope cut (the big decision)
v1 grew to 20+ features organically. A rebuild is the chance to **cut to the core**, not port everything.

| SHIP in v2 (the core) | CUT / DEFER |
|---|---|
| Auth + onboarding (sign up · "just you / invite" · how-it-works · first Today) | Calendar's 4 views → **DECISION B** below |
| **Today** — the heart (greeting · mood · partner presence · quick-add · open list + done-fold · streak · notes board · daily question) | Projects' 4 views (Table/Lanes/Timeline/Cards) → **one** view |
| **This Week** — points scoreboard (combined-first) | Appearance: 9 backgrounds / 5 fonts / 3 radii → **one** theme + dark |
| **Projects** — one list/table view + a project detail | Roadmap slices 5–11 (grow-a-thing, ritual, keepsake, weekly recap…) |
| **Tasks** — one grouped list | Import-from-another-space |
| **Journal** | Claude connector UI (keep the data hooks, build the screen later) |
| **Care layer** — waves / nudge / cheer + shared focus timer | |
| **Settings** — lean (account · partner · habits · notifications · dark) | |
| **Spaces** — switch + invite | |

→ **DECISION B (Calendar):** you did a lot of calendar work in v1. For v2 I'd ship **one simple Month + Agenda**, and defer Day/Week/Timeline/gantt to v2.1. Keep that, or cut calendar entirely from v2, or keep more? 

---

## 4. The flows the artifact will cover
1. **Land → sign up → onboarding** — Dropbox-style "Just you / Invite someone" → Cloaked-style how-it-works → first Today (day-zero).
2. **Invite a partner** — share link/code → they sign up → you're paired.
3. **Daily loop** — open Today → mood → see partner presence → quick-add → tick → wave/nudge → journal.
4. **Projects & tasks** — make a project → add tasks w/ deadlines → see them in the week.
5. **Focus together** — start the shared timer, both see the same countdown.

---

## 5. Shell + web↔mobile parity
| | Web | Mobile |
|---|---|---|
| Nav | Left rail (Matter-style) | Bottom tabs: Today · Week · Projects · More + a ⊕ quick-add (your mobile "model A" pick) |
| Today | Content column + a right rail (presence · coming-up · tonight) | Single column; the right-rail cards stack as bento |
| Home | Today | Today |
| Bento/widgets | Multi-column | Stack to one column |
| Reach | Responsive from 375px up | — |

Same surfaces, same data, one design — the layout reflows. Parity is a non-negotiable (it's in your CLAUDE.md).

---

## 6. States & variants (designed, not assumed)
- **Day-zero**: brand-new, no partner yet (solo) · partner invited but not joined.
- **Streak**: start · building · at-risk · fed · double-day · broken.
- **Empty**: no projects · no tasks today · empty journal.
- **System**: loading (Breathe loader) · signed-out · error.
- **Theme**: light + dark.

---

## 7. What the artifact will actually show (step 3)
A single HTML artifact with a little nav to flip between: **Onboarding → Today (web) → Today (mobile) → This Week → Projects → a Project detail → Tasks → Journal → Settings**, each in light; a dark toggle; and the key day-zero + streak states. Real copy, real layout — clickable enough to judge the feel, not a dead mockup.

---

## 8. Open decisions
- **A. Direction — RESOLVED:** Headspace-derived system, blue kept (`HEADSPACE-DS.md`).
- **A2. Font (small pick):** keep General Sans (rec), or Nunito/Hanken for more roundness.
- **B. Calendar in v2** = one Month + Agenda, defer the rest? (my rec: yes)
- **C.** Anything in the CUT column you want to pull back into v2?

**Stop here.** Confirm B (and A2/C if any), and the artifact is the next turn.
