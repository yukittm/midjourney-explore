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
if they ever disagree with this file, they win. Reference tables (hashtag library,
examples, templates, full constraint list, AI labeling) live in **`reference.md`** —
read it when a section points you there.

## Procedure (in order; steps 1–2 are load-bearing)

1. **Read the image.** Name its real subject, palette, composition. The caption's
   first line must be specific to what's on screen. *(Subject-less image, e.g. a
   color-field: "specific" = its palette / motion / phenomenon, not a subject noun.)*
2. **Scan recent posts.** Read the last ~10 `automation/published/*.yml`, newest first
   by the **filename date prefix** (not `publish_at`, often empty); **include
   `deleted_from_ig: true` records** (the deletion reason is a lesson). Note their
   openings, phrasings, axis use, emoji, hashtag sets, and **palette + subject**, then
   diverge (→ gate). **"The previous post"** (used by every rotation / divergence check
   below) **= the most-recent _live_ record**; deleted records inform the scan but are
   not the rotation baseline. *First post / empty folder: skip this scan; apply only
   Voice + content-aware + ≤5 tags.*
3. **Draft the caption** in the Voice and Form below.
4. **Choose ≤5 hashtags** (→ Hashtags).
5. **Write alt_text** (→ Alt text; skip for Reels).
6. **Run the gate** (→ Anti-sameness gate) and revise per its branch.
7. **Emit the bundle** (→ Output): the field values, their yml locations, and one line
   on how this post diverges from the last.

## Voice (constant — never varies)

Calm, sensory, observational; let the work lead. Casual, restrained, lowercase-leaning.
English by default (the account is EN-primary for reach). Never: hype, engagement-bait,
a hashtag dump in the body, or 👇-style pointer-bait.

## Form (PROVISIONAL — n=1; revisit after ~10 posts with save/send data)

The default below comes from one live post (`long-way-home`) and has no engagement data
yet. Vary the *expression*, never the Voice.

- **One line** — a single fresh sensory line about this image (`Home, the long way.`).
- **Casual, approach-based** — hint at what you chased, not a product pitch.
- **Axis ~80/20.** The series axis is **Geometry / Wavelength / Objects**. ~80% of posts
  **absorb** it (felt, not named); ~20% state it in a second line (`Geometry, holding a
  wavelength.`). *Test: if any of the three words or an obvious synonym appears, it's
  "stated"; otherwise "absorbed." Default to absorbed.*
- **Shape rotates** — don't repeat the previous post's shape back-to-back (shape =
  line-count / structure, i.e. one-line ↔ two-line; not which template).
- **Emoji optional, rotated** — calm / nature-leaning only (e.g. 🌊); never 🔥/✨/👇, never
  mandatory.
- **≤1 CTA or question** — never both; for art, SAVE / SHARE compound.

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

## Anti-sameness gate

Two failure classes — handle them differently.

**Text-fixable** — revise the text, then re-check:
- [ ] Voice holds (calm / sensory / observational / casual; no hype / bait / dump / 👇).
- [ ] Diverged from the last ~10: opening, phrasing, axis use, and emoji are not a repeat
      of the previous post.
- [ ] First line is specific to this image.
- [ ] ≤1 CTA or question.
- [ ] Hashtags pass the Hashtags rules (≤5, no `#`, neutral, ordered, rotated, vetted).
- [ ] alt_text set per image (none for Reels).

**Not text-fixable — STOP and surface to the user** (no caption edit fixes these):
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
  doubled `''` for apostrophes). **Caption ≤ 2200 chars.**
- `hashtags:` → top-level list, bare tags (no `#`).
- `alt_text:` → under each image asset as `assets[i].alt_text` (one per image; none for
  Reels).

Then validate: `PYTHONPATH=automation python3 -m unittest discover -s automation/tests`.
End with one line on how this post diverges from the last (shape, opening, palette,
hashtag rotation). *Optional:* persist it as a `divergence_note` in the record.
