"""Find clean crop boxes for figures on a smooth studio background.

Background is estimated per row (iteratively re-fitting on background-like
pixels), then each figure boundary is placed on the emptiest column/row inside
a search window, so neighbouring figures and text labels stay outside.

Usage: python -I auto_bbox.py <image_dir> <out_dir>
"""
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw

# key -> dict(src, seed, windows) ; windows: (name, axis, lo, hi)
FIGURES = {
    "amir_front": ("amir.png", (615, 500), {"left": ("x", 455, 500), "right": ("x", 740, 795), "top": ("y", 0, 40), "bottom": ("y", 950, 1010)}),
    "amir_face": ("amir.png", (300, 450), {"left": ("x", 0, 1), "right": ("x", 470, 505), "top": ("y", 160, 200), "bottom": ("y", 1000, 1024)}),
    "maliheh_front": ("malihe.png", (560, 500), {"left": ("x", 410, 450), "right": ("x", 670, 715), "top": ("y", 0, 40), "bottom": ("y", 950, 1010)}),
    "maliheh_face": ("malihe.png", (250, 450), {"left": ("x", 0, 1), "right": ("x", 415, 450), "top": ("y", 138, 175), "bottom": ("y", 1000, 1024)}),
    "nosratollah_front": ("haj-nosratollah.png", (270, 300), {"left": ("x", 100, 140), "right": ("x", 395, 440), "top": ("y", 10, 40), "bottom": ("y", 590, 615)}),
    "nosratollah_3q": ("haj-nosratollah.png", (560, 300), {"left": ("x", 430, 475), "right": ("x", 640, 690), "top": ("y", 10, 40), "bottom": ("y", 590, 615)}),
}
FG_THR = 22.0


def estimate_background(rgb: np.ndarray) -> np.ndarray:
    h, w, _ = rgb.shape
    q = (rgb // 12).astype(np.int32)
    keys = q[..., 0] * 4096 + q[..., 1] * 64 + q[..., 2]
    bg = np.zeros((h, 3))
    for y in range(h):
        vals, counts = np.unique(keys[y], return_counts=True)
        sel = keys[y] == vals[counts.argmax()]
        bg[y] = rgb[y][sel].mean(axis=0)
    k = 25
    pad = np.pad(bg, ((k, k), (0, 0)), mode="edge")
    bg = np.stack([np.convolve(pad[:, c], np.ones(2 * k + 1) / (2 * k + 1), mode="valid") for c in range(3)], axis=1)
    # Iteratively refit on background-like pixels only.
    for _ in range(4):
        dist = np.sqrt(((rgb - bg[:, None, :]) ** 2).sum(axis=2))
        like = dist < 10
        cnt = like.sum(axis=1)
        mean = np.where(like[..., None], rgb, 0).sum(axis=1) / np.maximum(cnt, 1)[:, None]
        weak = cnt < w * 0.15
        mean[weak] = bg[weak]
        pad = np.pad(mean, ((k, k), (0, 0)), mode="edge")
        bg = np.stack([np.convolve(pad[:, c], np.ones(2 * k + 1) / (2 * k + 1), mode="valid") for c in range(3)], axis=1)
    return bg


def main(argv: list[str]) -> int:
    src_dir, out_dir = pathlib.Path(argv[0]), pathlib.Path(argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    cache: dict[str, tuple[Image.Image, np.ndarray]] = {}
    boxes: dict[str, tuple[str, tuple[int, int, int, int]]] = {}
    for name, (src, seed, windows) in FIGURES.items():
        if src not in cache:
            im = Image.open(src_dir / src).convert("RGB")
            rgb = np.asarray(im, dtype=np.float64)
            bg = estimate_background(rgb)
            dist = np.sqrt(((rgb - bg[:, None, :]) ** 2).sum(axis=2))
            cache[src] = (im, dist)
        im, dist = cache[src]
        fg = dist > FG_THR
        h, w = fg.shape
        bounds = {}
        for side, (axis, lo, hi) in windows.items():
            if axis == "x":
                scores = fg[:, lo:hi].sum(axis=0)
                idx = lo + int(scores.argmin())
            else:
                scores = fg[lo:hi, :].sum(axis=1)
                idx = lo + int(scores.argmin())
            bounds[side] = idx
        x0, x1 = bounds["left"], bounds["right"]
        y0, y1 = bounds["top"], bounds["bottom"]
        boxes[name] = (src, (x0, y0, x1, y1))
        print(f"{name}: {src} box=({x0}, {y0}, {x1}, {y1}) size={x1 - x0}x{y1 - y0} bgfrac_in_box={1 - fg[y0:y1, x0:x1].mean():.2f}")
    for src, (im, dist) in cache.items():
        qa = im.copy()
        d = ImageDraw.Draw(qa)
        for name, (s, (x0, y0, x1, y1)) in boxes.items():
            if s != src:
                continue
            d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=(255, 0, 255), width=3)
        target = out_dir / f"bbox_{src}"
        qa.save(target)
        mask = Image.fromarray((np.clip(dist / 60, 0, 1) * 255).astype(np.uint8))
        mask.save(out_dir / f"mask_{src}")
        print(f"qa images: {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
