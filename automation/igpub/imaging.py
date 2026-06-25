"""Stdlib-only JPEG inspection — read dimensions without Pillow + the IG aspect rule.

Dependency-free so validation runs anywhere (CI included) with no image library.
"""
from __future__ import annotations

import struct

# Instagram feed: portrait 4:5 (0.8) .. landscape 1.91:1. 1:1 is inside the range. (width/height)
MIN_ASPECT = 4 / 5     # 0.8
MAX_ASPECT = 1.91
_EPS = 1e-3


def aspect_ok(width: int, height: int) -> bool:
    if width <= 0 or height <= 0:
        return False
    ratio = width / height
    return (MIN_ASPECT - _EPS) <= ratio <= (MAX_ASPECT + _EPS)


def read_jpeg_size(path: str) -> tuple[int, int]:
    """Return (width, height) for a JPEG by scanning to the SOF marker. Raises ValueError if not JPEG."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"\xff\xd8":
        raise ValueError("not a JPEG (missing SOI marker)")
    i, n = 2, len(data)
    while i + 9 < n:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        # SOF0..SOF15 carry the frame size; exclude the non-SOF markers in that range.
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            height, width = struct.unpack(">HH", data[i + 5:i + 9])
            return width, height
        if i + 4 > n:
            break
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        if seg_len < 2:
            break
        i += 2 + seg_len
    raise ValueError("could not find JPEG SOF marker")
