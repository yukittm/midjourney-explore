# prompts

Prompt templates and experiment logs.

- Lane-based organization (e.g. `editorial/`, `fashion/`, `still-life/`, `texture/`) once lanes emerge.
- A prompt template pins the base structure per the research convention:
  `[medium] of [subject], [scene], [light], [color/mood] --style raw --v 7 --ar X:Y --profile <code>`
- Keep the textual prompt short (~30 words) when a moodboard/sref is attached — see
  `docs/research/2026-05-11_midjourney-prompt-best-practices/01_prompt-anatomy.md`.

Naming: `<lane>-<intent>.md` for templates; `YYYY-MM-DD_<topic>.md` for experiment logs.
Record `--seed` and the moodboard snapshot code with any output worth reproducing.
