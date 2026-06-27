---
updated: 2026-06-27
status: active
type: guide
---

# automation

Instagram auto-upload pipeline (code). **Architecture decided 2026-06-25 → see [`ig-publish-pipeline.md`](ig-publish-pipeline.md)** (Option 1: self-owned DIY — git-file queue + Python Graph publisher + GitHub Pages host (R2/Cloudinary swappable later, esp. video); manual-first → scheduled-auto, no connectors on the publish path). **Phase-0 pipeline complete, tested + PROVEN on 2 published posts** (2026-06-25 `color-window`, 2026-06-27 `long-way-home`; `igpub/` + `validate.py`/`plan.py`/`publish.py`/`new_post.py` CLIs + CI). The enqueue flow: pick from `outputs/selects/` → `python automation/new_post.py --image … --slug …` scaffolds a draft `automation/queue/<id>.yml` + asset → write caption/alt via the `caption` skill → `status: approved` → `plan.py` → `publish.py`. Go-live prerequisites met (token active, GitHub Pages live); manual `publish.py` cadence now underway.

## North star & policy (decided 2026-06-23; the publish pipeline is BUILT + live — what's "not yet built" below is the full Claude-driven *automation loop*)

**End goal:** near-full automation — theme/prompt generation → Claude-driven Midjourney operation
(Claude-in-Chrome) → Instagram publishing. **Roles:** the **user is the creative director** (reacts to
themes + selects images — "this / that"); **Claude autonomously generates the patterns/combinations**.
Selections double as the like/dislike training signal for the consistency stack.

**Hard constraints (from `docs/style/style-definition.md` + the V8.1 research):**
- **One-pass generation only** in the automated path. V8.1 realism is global (no per-region), so any look
  that needs compositing/inpaint (pure non-representational backgrounds) is **manual curation only** —
  the V8.1 web Editor runs on the V6.1 model, there is **no official MJ API**, and unofficial wrappers
  carry ToS/ban risk. See `.claude/agent-memory/researcher/reference_mj-api-automation-state.md`.
- **Consistency stack** to apply: trained Personalization `--p` (taste) + a fixed image `--sref`
  (`--sw`, palette; **omit `--sv`** on V8.1) + a deterministic **post-grade LUT/preset** (the only exact color lock).
- **Home base deferred** — the register mix emerges from the user's selections, not pre-set.
- **"Claude-alone" boundary (honest scope).** Claude automates **ideation → prompt-string generation →
  reward-gate self-scoring** and the **post-grade LUT**. **Human / assisted:** uploading the `--sref` image
  (browser-only; the `file_upload` tool is blocked), driving/repairing the MJ web UI, training `--p`, the
  **final selection**, and **publishing**. "Near-full automation" = the prompt-gen + grade steps; it is **not**
  a hands-off loop.

Pipeline shape: pick `(subject, register ∈ {R1,R2,R3}, decisive light, optional seed)` → kernel + `--sref` →
generate HD (one pass) → **reward-gate score** ([[../docs/style/style-definition]] → the reward) → user selects
→ apply LUT → publish. (The `../archive/2026-05-13_mj-moodboard-automation-idea.md` is an archived V7-era
moodboard idea — historical, NOT the active plan.)

**Verification:** `PYTHONPATH=automation python3 -m unittest discover -s automation/tests` (92 tests; install
deps first: `pip install -r automation/requirements.txt`) — also set in `CLAUDE.md` + `.claude/PROGRESS.md`.
Keep secrets in `.env` (git-ignored), never committed.
