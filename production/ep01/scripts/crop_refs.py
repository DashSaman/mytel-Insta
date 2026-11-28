"""Extract clean reference views (crops) from the approved character sheets.

The original PNGs are never modified. Each crop is written to <out_dir>/<name>.png.
Boxes were chosen from a visual QA pass (see scripts/auto_bbox.py) so that
neighbouring figures, card frames and Persian text labels stay outside.

The one exception is the Nosratollah front view: its text label sits in open
background ~25 px left of the cap, so the label is repainted with the row's own
background colour (no figure pixel lies inside that rectangle).

Usage: python -I crop_refs.py <characters_dir> <out_dir>
"""
import pathlib
import sys

import numpy as np
from PIL import Image

# name -> (source file, (left, top, right, bottom))
CROPS = {
    # Human sheets: front full-body view + large face close-up, no typography.
    "amir_front": ("amir.png", (500, 16, 758, 985)),
    "amir_face": ("amir.png", (0, 163, 497, 1024)),
    "maliheh_front": ("malihe.png", (443, 12, 693, 985)),
    "maliheh_face": ("malihe.png", (0, 141, 438, 1024)),
    "nosratollah_front": ("haj-nosratollah.png", (116, 8, 420, 608)),
    "nosratollah_three_quarter": ("haj-nosratollah.png", (444, 10, 668, 606)),
    "nosratollah_head": ("haj-nosratollah.png", (1262, 22, 1530, 368)),
    # Non-human characters: single figures on a plain background; only stray
    # edge strips (and a second plug tip at the bottom of simo.png) are trimmed.
    "zangi": ("mr-zangi.png", (0, 0, 768, 497)),
    "simo": ("simo.png", (0, 0, 768, 484)),
    "dokmei": ("mrs-dokmei.png", (4, 0, 764, 512)),
    "ghodrati": ("ghodrati.png", (3, 0, 765, 512)),
}

# source file -> rectangles (in source coordinates) that contain only label + background.
# Nosratollah: the name pill ends at x~207 for y 14-62 and the second text line sits at
# x 88-150, y 66-90; the cap starts at x~222 below y 33 and the hair at x~208 below y 72.
LABEL_RECTS = {"haj-nosratollah.png": [(0, 8, 214, 66), (60, 62, 200, 96)]}
LABEL_THR = 14.0


def remove_label(im: Image.Image, rects: list[tuple[int, int, int, int]]) -> Image.Image:
    rgb = np.asarray(im.convert("RGB"), dtype=np.float64).copy()
    for rect in rects:
        _paint_label(rgb, rect)
    return Image.fromarray(rgb.astype(np.uint8))


def _paint_label(rgb: np.ndarray, rect: tuple[int, int, int, int]) -> None:
    """Replace label pixels inside rect with a smooth fit of the surrounding background."""
    x0, y0, x1, y1 = rect
    pad = 24
    X0, Y0, X1, Y1 = max(0, x0 - pad), max(0, y0 - pad), min(rgb.shape[1], x1 + pad), min(rgb.shape[0], y1 + pad)
    patch = rgb[Y0:Y1, X0:X1]
    h, w, _ = patch.shape
    yy, xx = np.mgrid[Y0:Y1, X0:X1]
    inside = (xx >= x0 - 4) & (xx < x1 + 4) & (yy >= y0 - 4) & (yy < y1 + 4)
    # The figure begins ~10 px right of each rectangle; keep it out of the samples.
    inside |= xx >= x1 - 10
    bg_samples = patch[~inside].reshape(-1, 3)
    # Robust background samples: drop the 15% darkest / most saturated pixels.
    lum = bg_samples.mean(axis=1)
    keep = lum > np.percentile(lum, 15)
    bg_samples = bg_samples[keep]
    sx = ((xx - X0) / max(w, 1))[~inside][keep]
    sy = ((yy - Y0) / max(h, 1))[~inside][keep]
    A = np.stack([np.ones_like(sx), sx, sy, sx * sx, sx * sy, sy * sy], axis=1)
    coef, *_ = np.linalg.lstsq(A, bg_samples, rcond=None)

    def design(a: np.ndarray, b: np.ndarray) -> np.ndarray:
        return np.stack([np.ones_like(a), a, b, a * a, a * b, b * b], axis=1)

    for y in range(y0, y1):
        row = rgb[y]
        q = (row // 12).astype(np.int64)
        keys = q[..., 0] * 4096 + q[..., 1] * 64 + q[..., 2]
        vals, counts = np.unique(keys, return_counts=True)
        bg = row[keys == vals[counts.argmax()]].mean(axis=0)
        dist = np.sqrt(((row - bg) ** 2).sum(axis=1))
        mask = dist > LABEL_THR
        # Dilate the mask by 2 px so soft edges of the label go too.
        dil = mask.copy()
        for shift in (1, 2):
            dil[shift:] |= mask[:-shift]
            dil[:-shift] |= mask[shift:]
        sel = dil.copy()
        sel[:x0] = False
        sel[x1:] = False
        cols = np.where(sel)[0]
        if cols.size:
            fit = design((cols - X0) / max(w, 1), np.full(cols.shape, (y - Y0) / max(h, 1))) @ coef
            row[cols] = fit


def main(argv: list[str]) -> int:
    src_dir, out_dir = pathlib.Path(argv[0]), pathlib.Path(argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    cleaned: dict[str, Image.Image] = {}
    for name, (src, box) in CROPS.items():
        if src not in cleaned:
            base = Image.open(src_dir / src)
            cleaned[src] = remove_label(base, LABEL_RECTS[src]) if src in LABEL_RECTS else base
        crop = cleaned[src].convert("RGB").crop(box)
        target = out_dir / f"{name}.png"
        crop.save(target, format="PNG")
        print(f"{name}: {src} {box} -> {crop.size[0]}x{crop.size[1]} {target.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
