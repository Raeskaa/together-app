# hate club v2 — Design System (Headspace-derived)

**Written:** 2026-11-19 · Translates Headspace's look-and-feel into build-ready tokens for hate club.
**Sourcing honesty:** Headspace publishes **no** official hex/type spec — their real guidelines (by agency *Order*, type by *Colophon*, 2024 rebrand with *Italic Studio*) are private. Every value below is reverse-engineered from the live site + credible write-ups (It's Nice That, Fast Company, Figma blog), then **tuned for hate club**. Treat as "in the spirit of," not gospel.

---

## The big translation (read this first)
Headspace's warmth is **not** its typeface. It's four things, and we can take all four while keeping hate club's identity:

1. **Cream shell, never cold white.** Warm off-white canvas + warm-grey cards + warm charcoal ink (not black).
2. **Blue is the action color; orange is the brand.** In Headspace's *product* UI the CTA is **blue** (`#0061EF`); orange + warm pastels live in the **brand, mascot, and illustration**. → hate club keeps its **blue `#1F6FEB`** as CTA, and gains **orange for the "moments"** (streak, celebration, mascot). (On their *marketing* site orange leads — but we're a product, so the app model applies.)
3. **Everything generously rounded** — full-pill buttons, big soft cards, huge tap targets.
4. **One-thing-per-moment + a warm voice** — question-as-header, your name in the copy, plain CTAs, soft slow motion.

**The moments-vs-work rule** (how a planner stays Headspace): immersive + gradient + one-thing treatment for the **moments** (onboarding, mood, streak, focus, day-zero, empty states); calm-but-dense for the **work** (tasks, projects) — same cream shell, one accent per object, rounded rows, lots of air, but **never a sunrise gradient behind a task table**.

---

## 1. Type
Headspace's face is a **custom cut of Aperçu** (proprietary, unlicensable). The honest designer call: **keep General Sans** — it's already hate club's identity *and* it's an Aperçu-family geometric-humanist sans, so it reads the way Headspace reads. We get the Headspace feel from color/shape/voice/illustration, not from swapping fonts.

```
--font-ui:      "General Sans", "Inter", system-ui, sans-serif;   /* body + UI (keep identity) */
--font-display: "General Sans", sans-serif;                        /* big headlines, weight 600–700 */
```
- **If you want more roundness in display:** swap `--font-display` to **Nunito** (friendliest, most "Headspace"), or **Hanken Grotesk** (near-Aperçu, warmer than Inter). One-line change — flagged for your call.
- **Scale:** hero 56/700 · page-title 32/700 · section 24/600 · feature 18/600 · body 16/400 · small 14/500 · caption 13/500 · eyebrow 12/600 uppercase +0.08em. Line-height ~1.6 body, ~1.1 display.

## 2. Color — tokens (light)
```
/* Canvas & surface — cream, never cold white */
--canvas:      #FBF5EC;   /* page background */
--canvas-warm: #FDF2E1;   /* deeper cream band (hero) */
--surface:     #FFFFFF;   /* cards / modals */
--surface-alt: #F6F1E8;   /* warm list rows / soft cards */
--line:        #EBE3D5;   /* hairlines on cream */

/* Ink — warm charcoal, not #000 */
--ink:         #1C1C1D;
--ink-muted:   #535253;
--ink-faint:   #8A8784;

/* Action / identity — BLUE (keep hate club) */
--blue:        #1F6FEB;   /* primary CTA, selection, links */
--blue-press:  #1856C2;
--blue-tint:   #E9F0FE;   /* selected-row fill */

/* Warm brand accent — the "moments" (streak, mascot, celebration) */
--warm:        #FF7E1D;   /* orange */
--warm-amber:  #FFAC1D;   /* marigold */
--sunrise-1:   #FFD66E;   /* streak/focus gradient, light → deep */
--sunrise-2:   #FF9E3D;
--sunrise-3:   #FF6B2C;

/* Object accents — one per project / space (warm "rainbow", like Headspace tiles) */
--a-coral: #FF8A78;  --a-mint: #6FC99A;  --a-lav: #B59CE0;
--a-sky:   #6FB7F0;  --a-rose: #F6A5C0;  --a-yolk: #FFC24B;

/* Semantic */
--success: #2FA35A;  --warning: #E08A12;  --danger: #D64545;
```

## 2b. Color — dark (deep & calm, keep the blue CTA)
```
--canvas:#161514; --canvas-warm:#1E1B18; --surface:#201D1A; --surface-alt:#262320; --line:#332E29;
--ink:#F3EDE3;  --ink-muted:#B7B0A6;  --ink-faint:#857F77;
--blue:#4C8DFF; --blue-press:#6AA0FF; --blue-tint:#1C2740;
/* --warm / accents carry over, nudged ~8% less saturated */
```

## 3. Shape
```
--r-xs:8px;  --r-input:16px;  --r-card:20px;  --r-hero:28px;  --r-pill:999px;
```
- **Buttons = full pill.** Primary = `--blue` fill, white text, 48px tall (56px large). Secondary = transparent + 1.5px `--ink` outline, pill. Tertiary = plain blue text.
- **Inputs = 16px radius** (so they read as fields, not buttons), 1px `--line`, 2px `--blue` focus ring.
- **Cards = 20px**, near-flat (shadows are rare and soft). Illustrations bleed edge-to-edge.
- **Select rows** (onboarding/lists) = pill or 16px, big targets, selected = `--blue-tint` fill + blue check.
- **The curved-horizon motif** for moments: a colored field up top, content area curving over it in an arc.

## 4. Space (4px base)
`4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64`. Generous. Section padding 48–64px, card padding 16–24px, max content width ~1120px. One idea per screen in the moments.

## 5. Motion — soft, slow, never springy
```
--ease:    cubic-bezier(.4,0,.2,1);     /* general */
--breathe: cubic-bezier(.37,0,.63,1);   /* streak + focus: slow in/out */
```
- Transitions 400–600ms fades, nothing snappy. The streak flame + focus timer **breathe** (slow asymmetric in/out, warm↔cool). hate club already has a Breathe loader + streak flame — same DNA.

## 6. Illustration (corrected: flat-vector + soft gradient, NOT claymation)
- **Flat-vector blob with a face** — fully rounded silhouette, dot eyes, one simple smile-curve, one warm fill. A small hate club mascot can live here (a little flame/blob). Keep faces **slightly restrained**, not grinning — it makes warmth credible and leaves room for hard days.
- **Soft-gradient orbs** (Headspace's "Ebb") — 2–3-stop warm gradients (pink→yellow, orange→coral), soft blob shapes, slight blur. Doable in pure CSS/SVG radial gradients — this is the **streak/focus/celebration** visual.
- No clay renders, no stock 3D.

## 7. Voice (name + question + reassurance; plain CTAs)
Warm, plain-spoken, a calm friend — not a guru. Ask *why/how are you* before *what*. Light, never saccharine; leaves room for a bad day.

hate club microcopy, in this voice:
| Surface | Copy |
|---|---|
| Onboarding Q1 | **"Who's hate club for?"** · Just me / Me and someone |
| Invite | **"Who are you doing this with?"** |
| Mood (Today) | **"How are you today, Mahesh?"** |
| Day-zero Today | "Good evening, Mahesh. Let's start small." |
| Streak building | "Two days. You're building something." |
| Streak at-risk | "Still time to keep the streak alive." |
| Wave received | "Sajal left you a wave 💛" |
| Empty project | "Nothing here yet — add the first thing." |
| CTAs | **Continue · Add it · I'm in · Start · Done for today** |

---

## Open picks (small — everything else is decided above)
- **Font:** keep **General Sans** (rec — it's identity *and* Aperçu-family), or go **Nunito/Hanken** for more Headspace roundness.
- Everything else (cream shell · blue CTA · orange moments · pills · soft motion · flat-vector blobs) → proposed as above; say the word and it's what the artifact is built on.
