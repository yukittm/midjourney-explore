#!/usr/bin/env python3
"""Feed Studio — a LOCAL, run-on-demand console (stdlib http.server, 127.0.0.1) to curate + plan the
IG feed entirely in the browser:

  • browse the raw candidate pool (outputs/candidates/), switch the grouping axis,
  • "→ selects" a candidate (PNG→JPEG convert into outputs/selects/; no crop — composition is yours),
  • "→ queue" a select (scaffold a draft post via the existing pipeline),
  • see the projected profile grid = upcoming (queue) + live (published), newest top-left, full images,
  • click any image for an in-tab full-size popup.

Read/writes only the local repo; nothing runs on the publish path. Run from the repo root:

  python automation/studio.py          # opens http://127.0.0.1:8765
"""
from __future__ import annotations

import argparse
import json
import mimetypes
import os
import sys
import threading
import webbrowser
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # make `import igpub` work

from igpub.queue import PUBLISHED_DIR, QUEUE_DIR, list_posts  # noqa: E402
from igpub.scaffold import ScaffoldError, scaffold_post  # noqa: E402
from igpub.studio_logic import ALLOWED_ROOTS, assemble_board, safe_path, slugify  # noqa: E402

REPO_ROOT = os.getcwd()
STATIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "studio", "static")
_IMG_EXT = (".png", ".jpg", ".jpeg", ".webp", ".gif")
ORDER_FILE = os.path.join("outputs", "selects", ".order.json")  # local selects arrangement (gitignored)
_ORDER_LOCK = threading.Lock()  # serialize all .order.json read-modify-write across request threads


def _load_order() -> list:
    try:
        with open(os.path.join(REPO_ROOT, ORDER_FILE), "r", encoding="utf-8") as f:
            return json.load(f).get("order", [])
    except (FileNotFoundError, ValueError):
        return []


def _save_order(order: list) -> None:
    path = os.path.join(REPO_ROOT, ORDER_FILE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump({"order": list(order)}, f)
    os.replace(tmp, path)   # atomic: a crash mid-write never leaves a truncated file


def _list_images(rel_dir: str) -> list[str]:
    d = os.path.join(REPO_ROOT, rel_dir)
    if not os.path.isdir(d):
        return []
    return [f for f in os.listdir(d) if not f.startswith(".") and f.lower().endswith(_IMG_EXT)]


def _candidate_dims(names: list[str]) -> dict:
    """(w,h) per candidate via Pillow — only needed for the 'aspect' axis."""
    from PIL import Image  # lazy; Pillow is a studio-only dep
    out = {}
    for n in names:
        p = safe_path(REPO_ROOT, "candidates", n)
        if not p:
            continue
        try:
            with Image.open(p) as im:
                out[n] = im.size
        except Exception:  # noqa: BLE001 — a bad file just drops to 'unknown'
            pass
    return out


def _build_board(axis: str) -> dict:
    cand = _list_images(ALLOWED_ROOTS["candidates"])
    sel = _list_images(ALLOWED_ROOTS["selects"])
    posts = list_posts(REPO_ROOT, QUEUE_DIR) + list_posts(REPO_ROOT, PUBLISHED_DIR)
    dims = _candidate_dims(cand) if axis == "aspect" else None
    return assemble_board(cand, sel, posts, axis=axis, dims=dims, selects_order=_load_order())


def _reorder(order: list) -> dict:
    """Persist a new selects order (only names that are real current selects are kept)."""
    present = set(_list_images(ALLOWED_ROOTS["selects"]))
    _save_order([n for n in (order or []) if n in present])
    return {"ok": True}


def _to_selects(name: str) -> dict:
    """Convert a candidate (any image) → a JPEG in outputs/selects/ (format-only; no crop)."""
    src = safe_path(REPO_ROOT, "candidates", name)
    if not src or not os.path.isfile(src):
        raise ValueError(f"candidate not found: {name}")
    from PIL import Image  # lazy
    stem = slugify(os.path.splitext(os.path.basename(name))[0])
    sel_dir = os.path.join(REPO_ROOT, ALLOWED_ROOTS["selects"])
    os.makedirs(sel_dir, exist_ok=True)
    with _ORDER_LOCK:
        dest_name = f"{stem}.jpg"
        i = 2
        while os.path.exists(os.path.join(sel_dir, dest_name)):
            dest_name = f"{stem}-{i}.jpg"
            i += 1
        with Image.open(src) as im:
            im.convert("RGB").save(os.path.join(sel_dir, dest_name), "JPEG", quality=92)
        _save_order([dest_name] + [n for n in _load_order() if n != dest_name])  # newest → grid top-left
    return {"ok": True, "select": dest_name}


def _from_selects(name: str) -> dict:
    """Return a select to the pool: delete the selects/ JPEG + drop it from the order. The raw
    candidate in outputs/candidates/ is untouched (to-selects only ever copied it)."""
    p = safe_path(REPO_ROOT, "selects", name)
    if not p or not os.path.isfile(p):
        raise ValueError(f"select not found: {name}")
    with _ORDER_LOCK:
        os.remove(p)
        _save_order([n for n in _load_order() if n != name])
    return {"ok": True}


def _commit(select: str, slug: str) -> dict:
    src = safe_path(REPO_ROOT, "selects", select)
    if not src or not os.path.isfile(src):
        raise ValueError(f"select not found: {select}")
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with _ORDER_LOCK:
        order = _load_order()
        idx = order.index(select) if select in order else len(order) - 1
        # The select NEAREST the live block (bottom of the grid = end of the order) is next to publish.
        # So priority increases toward that end: top-left (index 0) publishes last, bottom publishes first.
        priority = idx + 1
        r = scaffold_post(image=src, slug=slugify(slug or os.path.splitext(select)[0]),
                          date_str=date_str, repo_root=REPO_ROOT, priority=priority, remove_select=True)
        _save_order([n for n in order if n != select])
    return {"ok": True, "id": r.id, "priority": priority,
            "image_status": r.image_status, "validation_errors": r.validation_errors}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):  # quiet
        pass

    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(code, json.dumps(obj).encode("utf-8"), "application/json; charset=utf-8")

    def _qs(self):
        from urllib.parse import urlparse, parse_qs
        return parse_qs(urlparse(self.path).query)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/":
            try:
                with open(os.path.join(STATIC, "index.html"), "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            except FileNotFoundError:
                self._send(500, b"index.html missing", "text/plain")
            return
        if path.startswith("/vendor/"):
            full = os.path.realpath(os.path.join(STATIC, path.lstrip("/")))
            if not full.startswith(os.path.realpath(STATIC) + os.sep) or not os.path.isfile(full):
                self._send(404, b"not found", "text/plain")
                return
            ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
            with open(full, "rb") as f:
                self._send(200, f.read(), ctype)
            return
        if path == "/api/board":
            axis = (self._qs().get("axis", ["subject"])[0])
            try:
                self._json(_build_board(axis))
            except Exception as e:  # noqa: BLE001
                self._json({"error": str(e)}, 500)
            return
        if path == "/img":
            q = self._qs()
            full = safe_path(REPO_ROOT, q.get("root", [""])[0], q.get("name", [""])[0])
            if not full or not os.path.isfile(full):
                self._send(404, b"not found", "text/plain")
                return
            ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
            with open(full, "rb") as f:
                self._send(200, f.read(), ctype)
            return
        self._send(404, b"not found", "text/plain")

    def _read_json(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n) or b"{}")

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            body = self._read_json()
            if path == "/api/to-selects":
                self._json(_to_selects(body.get("name", "")))
            elif path == "/api/order":
                self._json(_reorder(body.get("order", [])))
            elif path == "/api/from-selects":
                self._json(_from_selects(body.get("name", "")))
            elif path == "/api/commit":
                self._json(_commit(body.get("select", ""), body.get("slug", "")))
            else:
                self._send(404, b"not found", "text/plain")
        except (ValueError, ScaffoldError) as e:
            self._json({"error": str(e)}, 400)
        except Exception as e:  # noqa: BLE001
            self._json({"error": str(e)}, 500)


def main() -> int:
    ap = argparse.ArgumentParser(description="Feed Studio — local curation/planning console.")
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--no-open", action="store_true", help="don't auto-open the browser")
    args = ap.parse_args()

    url = f"http://127.0.0.1:{args.port}"
    httpd = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"Feed Studio → {url}   (Ctrl-C to stop)")
    if not args.no_open:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        httpd.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
