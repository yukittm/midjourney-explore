---
name: caption
description: >-
  Write the Instagram publish-text bundle (caption + hashtags + alt_text) for a
  selected midjourney-explore image in the @tim.bankrupt voice, applying the
  anti-sameness guard against recent posts. Use whenever preparing or revising a
  post's text, drafting a caption, or filling an `automation/published/<id>.yml`
  record — even if the user doesn't say "caption" outright. Triggers: "caption",
  "キャプション", "write the post text", "hashtags for this", "this image's caption".
---

# caption — @tim.bankrupt Instagram post text

Produce one post's text from a selected image: **caption + ≤5 hashtags + alt_text**,
in a constant voice, checked so no post reads like a recent one (the project's #1
fear: sameness at scale).

**Scope:** manual or Claude-in-the-loop. This file is a human-facing method, not a
headless spec — when an automated caption step is built, enforce the recent-post scan
+ tag vetting in code (`automation/igpub/`, like `validate.py`).

**Ownership:** this skill owns the *voice + procedure*. Policy numbers and hard limits
are owned by `docs/marketing/ig-growth-strategy.md` and `automation/igpub/validate.py`;
if they ever disagree with this file, they win. Reference tables (the variation palette,
hashtag library, examples, full constraint list, AI labeling) live in **`reference.md`** —
read it when a section points you there.

## Procedure (in order; steps 1–2 are load-bearing)

1. **Read the image.** Name its real subject, palette, composition. The caption's
   first line must be specific to what's on screen. *(Subject-less image, e.g. a
   color-field: "specific" = its palette / motion / phenomenon, not a subject noun.)*
2. **Scan recent posts.** Read the last ~10 `automation/published/*.yml`, newest first
   by the **filename date prefix** (not `publish_at`, often empty); **include
   `deleted_from_ig: true` records** (the deletion reason is a lesson). Note their
   openings, shapes, **angles**, axis use, emoji, hashtag sets, and **palette + subject**,
   then diverge (→ gate). **"The previous post"** (used by every rotation / divergence
   check below) **= the most-recent _live_ record**; deleted records inform the scan but
   are not the rotation baseline. *First post / empty folder: skip this scan; apply only
   Voice + Form + ≤5 tags.*
3. **Draft the caption** in the Voice + Form below.
4. **Choose ≤5 hashtags** (→ Hashtags).
5. **Write alt_text** (→ Alt text; skip for Reels).
6. **Run the gate** (→ Anti-sameness gate) and revise per its branch.
7. **Emit the bundle** (→ Output): the field values, their yml locations, and one line
   on how this post diverges from the last.

## Voice (the constant — never varies)

Calm, sensory, observational; let the work lead — casual and restrained, never hype or
sales. **Capitalization = standard sentence case:** capitalize the first letter of each
sentence (and the pronoun "I" / proper nouns); everything else lowercase. So `A hot
spring, ringed in quiet color.` and `A river of color through the saguaro desert. Where
does it end?` — never all-lowercase, Title Case, or ALL CAPS. English by default (the
account is EN-primary for reach). **Never** hype, engagement-bait, a hashtag dump in the
body, or 👇-pointer-bait. *(Two things flex on top of this constant voice — the angle and
the warmth of register — see Form. The Voice is the floor they all stand on.)*

## Form — variety from two axes, kept short

Sameness is the enemy, and it has one root cause: **letting both axes default** — the same
grammatical shape, and a flat description of the subject. That reads monotonous and
pretentious at once. So every caption is built by rotating **two independent axes**, then
trimmed to size.

- **Axis 1 — Shape (archetype):** the grammatical form. Five peers in `reference.md`
  (fragment · full sentence · quiet question · first-person · two-line axis-signature).
  No default; they are equals.
- **Axis 2 — Angle (lens):** the angle of meaning — *whose view, what it's about*. Palette
  in `reference.md`. **Favor the human / playful angles** (a character's thought, a
  daily-life hook, a real question, a deadpan travelogue, a dry juxtaposition, light
  wordplay); keep meta / feeling / wry in the mix; use **plain subject-description only
  sparingly**. Description-as-default IS the monotony to kill.
- **Use the two axes as a generation MENU — then check by READING, not by ticking labels.**
  Pick a shape + an angle to *generate* from. But the bar is **not** "a different label from
  last time" — it's that the finished caption **reads differently from the recent grid**. The
  real failure is the grid forming a visible pattern (an every-few-posts rotor, or
  all-description, or all-wistful) — and a mechanical label-rotation *creates* exactly that.
  So vary the **opening move** and the **rhetorical move**, judged by reading the recent
  captions, not by trusting your own category labels.
- **Single post vs batch.** *Single post* (the default): differ from the **last ~6 live posts**
  (from the step-2 scan) on opening move, rhetorical move, shape, and angle. *Batch (writing
  several at once):* also spread shapes + angles across the set — none adjacent alike and no
  obvious rotor across the whole set; with more posts than shapes the shapes WILL repeat
  (that's fine — keep repeats non-adjacent and every opening distinct).

Then trim every caption to these:

- **Short** — ~6–14 words; one line unless the shape needs two.
- **Keyword first** — the first ~125 chars carry one real noun (place / phenomenon /
  medium, e.g. *hot spring, canyon, saguaro desert, peloton*). The angle can lead, but the
  noun must be there — it's what makes the post discoverable.
- **Register — calm stays the MAJORITY; rotate warmth in (~1 in 3), don't let it take over.**
  Calm/observational is the baseline and the majority voice; roughly every third caption
  lands **warm / friendly / casual** (talk like a person, not a placard) — present, not
  dominant. Both extremes are wrong: a batch that's uniformly wistful/poetic, AND one that's
  all quippy/casual. The friendly note is spice, not the default.
- **Axis ~80/20** — series axis = **Geometry / Wavelength / Objects**. ~80% absorb it (felt,
  not named); ~20% state it (the two-line shape's job). *Test: any of the three words or an
  obvious synonym appears → "stated"; else "absorbed."*
- **Emoji — rare and single.** Most captions have none; at most ~1 in 5 ends the FINAL
  sentence with exactly ONE calm/nature emoji (🌊). Never more than one, never mid-caption,
  never 🔥/✨/👇, never as decoration or bait.
- **≤1 question or CTA** per caption (see Reach for the cap).

## Reach (evidence-based; tasteful, never bait)

Few things actually move reach (per the strategy doc): **sends > saves > likes**, and
**keywords (caption first line + alt text) > hashtags**. So:
- Front-load the keyword (above) and fill **alt_text with plain keywords** — the free SEO
  channel that lets the visible caption stay literary (see Alt text).
- Occasionally earn a *send/save*: ~1 in 5 posts may add ONE short genuine **save/send
  line** ("one to keep for a grey day") OR use the **quiet-question** shape — never both,
  never baity (no "comment below / tag / double-tap"). Don't optimize for likes or hashtags.

## Post types

- **Single image** (default) — one caption, one alt_text.
- **Carousel (2..N images)** — one caption for the set; a distinct alt_text per image;
  the scan applies to the whole set. All images must share one aspect ratio (image-level
  → gate).
- **Reels (1 video)** — caption only, **no alt_text**; hashtags still in the caption.
- **Stories** — out of scope (no caption / hashtags via the API).

## Hashtags

- **≤5**, all relevant, in the caption. **No leading `#`** — the pipeline adds it; a
  leading `#` fails `validate.py`.
- **Neutral medium / technique descriptors only** (e.g. `digitalart`, `abstractart`,
  `generativeart`, `midjourneyart`). **No self-praising / aesthetic-quality tags** —
  e.g. `surrealart`; calling your own work "surreal" reads as self-flattery.
- **Order general → specific, kept consistent across posts** (broad medium → genre →
  technique → tool; any community tag last). Rotation changes *which* tags, not the order.
- **Rotate vs the previous post:** the full set must differ from the last post's;
  partial overlap is fine. The vetted pool is small — expand it as you vet, rather than
  forcing a total swap.
- **Vetting:** manual path — check each tag in-app (a banned tag wastes 1/5 of the
  budget). Headless — use only the vetted library in `reference.md`, flag any new tag for
  human vetting, and never ship an unvetted or invented tag.
- Hashtags are a topical **label, not a reach lever** (Mosseri: they don't boost reach).
  **Vetted library → `reference.md`.**

## Alt text (literal, not poetic; skip for Reels)

Describe the actual scene for accessibility + SEO: subject + colors + composition,
plainly. One per image asset. Keep the poetry in the caption. Example → `reference.md`.
**⚠️ `validate.py` does NOT enforce non-empty alt_text on images** (it only rejects alt on
video) — an empty alt passes silently, so never rely on validation to catch a missing one;
it's your strongest free SEO lever, always write it.

## Anti-sameness gate

Two failure classes — handle them differently.

**Text-fixable** — revise the text, then re-check:
- [ ] Voice holds (calm / sensory / observational / casual; no hype / bait / dump / 👇).
- [ ] **Reads different from the recent grid — judged by READING, not by labels.** Differs
      from each of the last ~6 live posts (and any batch siblings) on **opening move**,
      **rhetorical move / angle**, and **shape** — not just a different category name on a
      similar sentence (a relabel is not a diverge).
- [ ] **No visible rotor, no single-register grid.** The recent set isn't an obvious cycle
      (fragment→question→…) and isn't all-description or all-wistful; calm stays the majority
      and warmth is present (~1 in 3, not dominant).
- [ ] **Short** (~6–14 words) and the **first ~125 chars carry a keyword**.
- [ ] Diverged from the last ~10: opening, phrasing, axis use, and emoji are not a repeat
      of the previous post.
- [ ] First line is specific to this image.
- [ ] ≤1 CTA or question (reach beats ~1 in 5 posts max).
- [ ] Hashtags pass the Hashtags rules (≤5, no `#`, neutral, ordered, rotated, vetted).
- [ ] alt_text set per image (none for Reels).

**Not text-fixable — STOP and surface to the user** (no caption edit fixes these; both are
image-level, so you can check them up front at step 1 before drafting):
- [ ] **Palette / subject collides with the previous post.** The image is already chosen
      → recommend holding or reordering it. (This is what got post #1 deleted.)
- [ ] **Carousel images don't share one aspect ratio** → pre-crop the set.

*Every ~10 posts:* check whether the provisional Form still fits the latest save/send
data; revise the default if not.

## Output

Emit the field **values** (not a paste-ready yml block) and write them into the post's
record — normally the **`automation/queue/<id>.yml` draft** (created by
`automation/new_post.py`) before approval; an already-posted record lives in
`automation/published/<id>.yml`. Match an existing record's shape (e.g.
`automation/published/2026-06-27_long-way-home.yml`):

- `caption:` → top-level. A multi-line caption needs yml quoting (a quoted scalar;
  doubled `''` for apostrophes). **Caption + hashtags ≤ 2200 combined** — `validate.py`
  budgets the *assembled* string (caption + blank line + space-joined `#tags`), not the
  caption alone. (Our captions are short, so this is slack; stated for correctness.)
- `hashtags:` → top-level list, bare tags (no `#`).
- `alt_text:` → under each image asset as `assets[i].alt_text` (one per image; none for
  Reels).

Then validate: `PYTHONPATH=automation python3 -m unittest discover -s automation/tests`.
End with one line on how this post diverges from the last (shape, angle, opening, palette,
hashtag rotation). *Optional:* persist it as a `divergence_note` in the record.
