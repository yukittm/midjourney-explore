---
name: mj-style-raw
description: What MJ --style raw / Raw Mode does (V7/V8.1), how it differs from default, raw-vs-CGI-gloss, and the raw x stylize interaction
metadata:
  type: reference
---

Web-verified 2026-06-26 (docs.midjourney.com 403s on direct fetch — used WebSearch verbatim snippets + blakecrosley.com fetched + rareconnections.io fetched). See [[mj-stylize-chaos-hd-params]], [[mj-sref-image-url-behavior]], [[web-access-constraints]].

**What raw IS (official Raw Mode doc, via search snippet):** "Raw Mode reduces automatic beautification, and in most cases, this yields more accurate results when prompting specific styles." In Standard mode MJ auto-adds its own creative touch ("auto-pilot" = the Midjourney Aesthetic: moody/cinematic lighting, painterly finish); Raw turns that off → cleaner/flatter/more literal, closer to the prompt. Invoke via `--raw` (param) or Settings → Mode: Raw. Official Raw doc URL: docs.midjourney.com/hc/en-us/articles/32634113811853-Raw (and ...-Raw-Mode).

**Raw HELPS organic/photographic, fights the plastic/CGI "AI sheen".** V8's default aesthetic is over-polished/hyper-processed (a known V8-alpha issue MJ acknowledged). Practitioner consensus: `--style raw` + LOW `--s` + photo cues is THE recipe to escape glossy/plastic. Raw strips the built-in stylistic bias for more grounded, less-stylized output.

**raw x stylize — sources DISAGREE; the tension is real:**
- blakecrosley (fetched): lists "--style raw + high --s" under PARAMETER CONFLICTS as "contradictory"; recommends raw + LOW stylize (--s 50) for max photorealism.
- rareconnections/community: "adding --raw to a high stylize setting helps restore structure" — image keeps expressive qualities but form/layout/clarity preserved.
- Reconcile: raw and high-stylize pull opposite ways on the literal↔artistic axis, but they're not mutually exclusive — raw acts as a structure/realism anchor while stylize still adds expression. Raw does NOT prevent stylization if style is in the prompt or sref.

**Implication for "organic-but-colorful" goal (cactus-as-color-wave):** dropping raw to get color-flow is a real trade but likely the WRONG lever. Better: re-add `--style raw` to kill the CGI gloss + restore organic plant texture, and carry the COLOR via the sref (raise `--sw`) + explicit color/medium language in the prompt — NOT via high `--stylize`. Stylize competes with the sref (see [[mj-stylize-chaos-hd-params]]); pushing stylize to carry color both washes the sref AND re-adds gloss. Raw + moderate stylize + strong sref + painterly/analog texture cues is the principled combo. No official doc quantifies raw's effect ON the stylize value — treat the interaction guidance as community-level.
