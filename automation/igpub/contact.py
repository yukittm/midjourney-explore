"""Candidate contact-sheet — pure grouping + HTML rendering (no I/O, no network).

Triage tool for the raw generation pool (`outputs/candidates/`, ~hundreds of files): render every
candidate as a visual grid, grouped by subject (the prompt-prefix before Midjourney's UUID), so the
director can eyeball variations at a glance and decide which to crop into `outputs/selects/`.

Read-only by design: it does NOT move or crop files (cropping is the director's manual call; moving a
raw PNG into selects/ would break the "selects = cropped JPEG" contract). The CLI
(`automation/contact_sheet.py`) scans the folder, writes the HTML, opens it.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass

# Midjourney download names end with `_<uuid>_<variation>.<ext>`; strip that to get the subject.
_UUID_TAIL = re.compile(
    r"_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}_\d+\.[A-Za-z0-9]+$")
_IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")
# Clean the subject for grouping: drop Midjourney flags (`--chaos 10 --ar 45 …`) and the noise
# prefixes MJ prepends (`Yuki `, an `httpss.mj.run<id>` URL token), then lowercase — so trivial
# prefix differences (Yuki/non-Yuki) collapse into one readable group instead of fragmenting.
_PARAMS = re.compile(r"\s*--.*$")                                  # everything from the first `--`
_JUNK_PREFIX = re.compile(r"^(?:yuki|https*[.\s]*mj[.\s]*run\S*)\s+", re.I)


@dataclass
class Candidate:
    filename: str
    subject: str    # grouping key (human-readable prompt prefix)


def subject_of(filename: str) -> str:
    m = _UUID_TAIL.search(filename)
    base = filename[: m.start()] if m else filename.rsplit(".", 1)[0]
    base = base.strip("_").replace("_", " ")
    base = _PARAMS.sub("", base)          # drop `--chaos 10 --ar 45 …`
    base = _JUNK_PREFIX.sub("", base)     # drop leading `Yuki ` / `httpss.mj.run<id> `
    base = re.sub(r"\s+", " ", base).strip().lower()
    return base or "(misc)"


def build_candidates(filenames) -> list[Candidate]:
    return [Candidate(f, subject_of(f))
            for f in sorted(filenames) if f.lower().endswith(_IMG_EXT)]


def group(cands) -> list[tuple[str, list[Candidate]]]:
    """Group by subject; biggest sets first (where the most pruning is needed), then alphabetical."""
    groups: dict[str, list[Candidate]] = {}
    for c in cands:
        groups.setdefault(c.subject, []).append(c)
    return sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))


def render_html(groups, *, total: int, generated_at: str = "", img_prefix: str = "") -> str:
    """Self-contained HTML (inline CSS, no deps). Dense responsive grid; each tile links to the full
    image; the filename shows on hover so you know which file to crop into selects/."""
    sections = []
    for subject, cands in groups:
        tiles = []
        for c in cands:
            src = html.escape(img_prefix + c.filename)
            fn = html.escape(c.filename)
            tiles.append(
                f"<a class='tile' href='{src}' target='_blank' title='{fn}'>"
                f"<img loading='lazy' src='{src}' alt=''></a>")
        sections.append(
            f"<section><h2>{html.escape(subject)} <span class='n'>×{len(cands)}</span></h2>"
            f"<div class='grid'>{''.join(tiles)}</div></section>")
    body = "\n".join(sections) or "<p class='muted'>No candidate images found in outputs/candidates/.</p>"
    gen = html.escape(generated_at)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Candidates — triage</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; background:#0b0b0d; color:#e8e8ea;
         font:13px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; }}
  header {{ position:sticky; top:0; z-index:1; background:#0b0b0dcc; backdrop-filter:blur(8px);
            padding:12px 18px; border-bottom:1px solid #222; }}
  h1 {{ font-size:15px; margin:0; font-weight:600; }}
  .meta {{ color:#9a9aa2; font-size:12px; margin-top:3px; }}
  .wrap {{ padding:8px 16px 40px; }}
  section {{ margin:18px 0; }}
  h2 {{ font-size:13px; font-weight:600; color:#cfcfd6; margin:0 0 8px;
        position:sticky; top:52px; background:#0b0b0d; padding:4px 0; }}
  .n {{ color:#777; font-weight:400; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:4px; }}
  .tile {{ display:block; aspect-ratio:1/1; background:#16161a; overflow:hidden; border-radius:3px; }}
  .tile img {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .tile:hover {{ outline:2px solid #3aa3ff; outline-offset:-2px; }}
  .muted {{ color:#777; }}
</style></head>
<body>
<header>
  <h1>Candidates — triage</h1>
  <div class="meta">{total} images · {len(groups)} subjects · grouped, biggest sets first · click a tile to open full · hover for filename{' · ' + gen if gen else ''}</div>
</header>
<div class="wrap">
{body}
</div>
</body></html>
"""
