---
updated: 2026-06-23
status: active
type: guide
---

# prompts

Prompt templates and experiment logs.

- Register-based organization (`R1-color-block-terrain/`, `R2-geometric-landform/`,
  `R3-chromatic-wave/`, `explore/`) once templates emerge — the registers from
  `docs/style/style-definition.md`.
- A prompt template pins the base structure on the realism **kernel** + a single bold image `--sref`:
  `[shot] of [photoreal subject + action], [real terrain/phenomenon = the register], editorial photograph, [lens], [film stock] --style raw --s ~110 --sref <bold image URL> --sw 150–250 --sv 7 --ar 4:5 --no painting, illustration, 3d render, cgi`
- Specify the **subject + the real background noun richly**; the **`--sref`** carries the color, the
  kernel carries realism — don't spend words on style and **don't chase a word count** (length is not
  the lever). See `docs/style/prompting.md` §7.

Naming: `<register>-<intent>.md` for templates; `YYYY-MM-DD_<topic>.md` for experiment logs.
Record `--seed` and the `--sref` image used with any output worth reproducing.
