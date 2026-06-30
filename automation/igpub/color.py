"""Computed palette for an image — deterministic, free, idempotent. Color is photometric, not
semantic, so it is COMPUTED from pixels (not vision-tagged): a dominant + accent hue family from a
fixed 8-family set, plus an 8-bin hue-proportion vector. The vector powers a palette-collision
distance check between adjacent feed tiles (a published post was deleted for reading too
color-similar to its neighbor). PIL + stdlib only; no numpy, no network, no LLM.

Split: family_of / classify_palette / color_distance are PURE (unit-tested); extract_rgb_counts is
the only I/O (PIL quantize)."""
from __future__ import annotations

import colorsys

# 7 hue partitions of the wheel + neutral (low saturation/value). Names are illustrative; the hue
# bands are the contract. coral/salmon falls in red-orange by hue.
FAMILIES = ("red-orange", "yellow", "green", "teal", "blue", "violet", "magenta", "neutral")
_HUE_BANDS = (  # (lo_deg, hi_deg exclusive, family)
    (0, 40, "red-orange"), (40, 70, "yellow"), (70, 165, "green"), (165, 200, "teal"),
    (200, 255, "blue"), (255, 290, "violet"), (290, 360, "magenta"),
)
_SAT_MIN = 0.18   # below this saturation -> neutral (greys/earth/black/white)
_VAL_MIN = 0.12   # below this value -> neutral (near-black)


def family_of(rgb) -> str:
    """Map an (r,g,b) 0..255 tuple to one of FAMILIES via HSV."""
    r, g, b = (c / 255 for c in rgb[:3])
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < _SAT_MIN or v < _VAL_MIN:
        return "neutral"
    deg = h * 360
    for lo, hi, fam in _HUE_BANDS:
        if lo <= deg < hi:
            return fam
    return "red-orange"   # the hue==360 edge wraps to red


def classify_palette(rgb_counts) -> dict:
    """rgb_counts: iterable of (count, (r,g,b)). Returns {dominant, accent, vector} where vector is a
    normalized fraction per family (sums to ~1). dominant/accent are the two largest NON-neutral
    families (accent falls back to dominant when the image is effectively single-family)."""
    bins = {f: 0 for f in FAMILIES}
    total = 0
    for count, rgb in rgb_counts:
        bins[family_of(rgb)] += count
        total += count
    if total == 0:
        return {"dominant": "neutral", "accent": "neutral", "vector": {f: 0.0 for f in FAMILIES}}
    vector = {f: round(bins[f] / total, 4) for f in FAMILIES}
    ranked = sorted(((frac, f) for f, frac in vector.items() if f != "neutral"), reverse=True)
    dominant = ranked[0][1] if ranked and ranked[0][0] > 0 else "neutral"
    accent = next((f for frac, f in ranked if f != dominant and frac > 0), dominant)
    return {"dominant": dominant, "accent": accent, "vector": vector}


def color_distance(vec_a: dict, vec_b: dict) -> float:
    """L1 distance over the 8-bin hue vectors (0..2). Deterministic; simple. A ring-aware EMD is a
    future upgrade if near-duplicate palettes slip through. Lower = more color-similar."""
    return sum(abs(vec_a.get(f, 0.0) - vec_b.get(f, 0.0)) for f in FAMILIES)


def extract_rgb_counts(path: str, *, resize: int = 100, colors: int = 8):
    """I/O: downsample + median-cut quantize to `colors` swatches; return [(count, (r,g,b)), ...]."""
    from PIL import Image
    with Image.open(path) as im:
        im = im.convert("RGB")
        im.thumbnail((resize, resize))
        q = im.quantize(colors=colors, method=Image.MEDIANCUT)
        pal = q.getpalette() or []
        out = []
        for cnt, idx in (q.getcolors() or []):
            out.append((cnt, tuple(pal[idx * 3: idx * 3 + 3])))
        return out


def palette_of(path: str) -> dict:
    """Convenience: extract + classify in one call (I/O)."""
    return classify_palette(extract_rgb_counts(path))
