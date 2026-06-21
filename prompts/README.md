---
updated: 2026-06-21
status: active
type: guide
---

# prompts

Prompt templates and experiment logs.

- Lane-based organization (e.g. `editorial/`, `fashion/`, `still-life/`, `texture/`) once lanes emerge.
- A prompt template pins the base structure per the research convention:
  `[medium] of [subject], [scene], [light], [color/mood] --style raw --v 7 --ar X:Y --profile <code>`
- Specify the **subject/scene richly** within the ~40-word budget; the moodboard/sref carries the
  **style** (don't spend words on style). Project convention = detailed/specific prompts —
  see `docs/style/prompting.md`. (Research's ~30-word floor is kept on record at
  `docs/research/2026-05-11_midjourney-prompt-best-practices/01_prompt-anatomy.md`.)

Naming: `<lane>-<intent>.md` for templates; `YYYY-MM-DD_<topic>.md` for experiment logs.
Record `--seed` and the moodboard snapshot code with any output worth reproducing.
