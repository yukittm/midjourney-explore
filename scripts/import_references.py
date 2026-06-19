#!/usr/bin/env python3
"""Import manually-downloaded reference images/videos into references/<handle>/.

Usage: python3 scripts/import_references.py <source_dir>

Self-contained to THIS project. Copies (non-destructive) media from <source_dir>
into references/<handle>/ and appends provenance to references/manifest.jsonl.

Attribution: Instagram media filenames embed an owner-id group; RULES map a known
filename substring to a handle. Files matching no rule go to references/_unsorted/
(e.g. videos whose filenames carry no owner id). Idempotent: a file whose sha256 is
already in the manifest is skipped.
"""
import sys, json, hashlib, shutil, datetime, pathlib

# Project-specific filename-substring -> handle. Verified by viewing samples (2026-06-20).
RULES = {
    "301672": "giz.akdag",
    "024697": "marianopeccinetti",
}
PROJECT = pathlib.Path(__file__).resolve().parents[1]
REF = PROJECT / "references"
MANIFEST = REF / "manifest.jsonl"
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}
VID_EXT = {".mp4", ".mov"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def handle_for(name):
    for sub, handle in RULES.items():
        if sub in name:
            return handle
    return "_unsorted"


def load_seen():
    seen = set()
    if MANIFEST.exists():
        for line in MANIFEST.read_text().splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                seen.add(json.loads(line)["sha256"])
            except Exception:
                pass
    return seen


def main():
    if len(sys.argv) < 2:
        print("usage: import_references.py <source_dir>")
        sys.exit(1)
    src = pathlib.Path(sys.argv[1]).expanduser()
    if not src.is_dir():
        print(f"source dir not found: {src}")
        sys.exit(1)
    seen = load_seen()
    today = datetime.date.today().isoformat()
    entries, added, skipped = [], 0, 0
    for p in sorted(src.iterdir()):
        if not p.is_file() or p.name == ".DS_Store":
            continue
        ext = p.suffix.lower()
        kind = "image" if ext in IMG_EXT else "video" if ext in VID_EXT else None
        if kind is None:
            continue
        digest = sha256(p)
        if digest in seen:
            skipped += 1
            continue
        handle = handle_for(p.name)
        dest_dir = REF / handle
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, dest_dir / p.name)
        entries.append({
            "imported_at": today,
            "handle": handle,
            "kind": kind,
            "filename": str((dest_dir / p.name).relative_to(REF)),
            "source_filename": p.name,
            "bytes": p.stat().st_size,
            "sha256": digest,
            "source": "manual IG download via ~/Desktop/reference",
            "attribution": "by IG media-id group; samples visually verified 2026-06-20",
        })
        seen.add(digest)
        added += 1
    if entries:
        with open(MANIFEST, "a") as f:
            for e in entries:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
    print(f"added={added} skipped(dupe)={skipped} -> {REF}")


if __name__ == "__main__":
    main()
