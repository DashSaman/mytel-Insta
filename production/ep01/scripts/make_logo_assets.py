"""Build overlay assets from the OFFICIAL Mytel logo file (never AI-generated).

Source: branding/mytel-logo-HOME-EXACT-512.png, downloaded from mytel.one
(https://mytel.one/wp-content/uploads/2026/08/mytel-logo-HOME-EXACT-512.png).
The artwork is not redrawn: the dark navy background is made transparent by a
luminance key so the same logo can sit on video, and a soft badge is composed
around it.

Usage: python -I make_logo_assets.py <branding_dir>
"""
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw

NAVY = (6, 16, 36)


def lockup_rgba(src: Image.Image) -> Image.Image:
    rgb = np.asarray(src.convert("RGB"), dtype=np.float64) / 255.0
    value = rgb.max(axis=2)
    bright = value > 0.30
    ys, xs = np.where(bright)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    crop = rgb[y0:y1, x0:x1]
    v = crop.max(axis=2)
    # Smooth luminance key: below 0.12 fully transparent, above 0.40 fully opaque.
    a = np.clip((v - 0.12) / (0.40 - 0.12), 0.0, 1.0)
    a = a * a * (3 - 2 * a)  # smoothstep
    bg = np.array(NAVY, dtype=np.float64) / 255.0
    aa = np.maximum(a, 1e-3)[..., None]
    colour = np.clip((crop - (1 - a[..., None]) * bg) / aa, 0, 1)
    # The emblem's dark disc sits inside the ring: it is dark like the background but
    # enclosed by it, so it must stay opaque with its own colour.
    dark = a < 0.5
    hgt, wid = dark.shape
    outside = np.zeros_like(dark)
    stack = [(0, x) for x in range(wid) if dark[0, x]] + [(hgt - 1, x) for x in range(wid) if dark[hgt - 1, x]]
    stack += [(y, 0) for y in range(hgt) if dark[y, 0]] + [(y, wid - 1) for y in range(hgt) if dark[y, wid - 1]]
    while stack:
        y, x = stack.pop()
        if outside[y, x] or not dark[y, x]:
            continue
        outside[y, x] = True
        if y > 0:
            stack.append((y - 1, x))
        if y < hgt - 1:
            stack.append((y + 1, x))
        if x > 0:
            stack.append((y, x - 1))
        if x < wid - 1:
            stack.append((y, x + 1))
    interior = dark & ~outside
    if interior.any():
        a[interior] = 1.0
        colour[interior] = crop[interior]
    out = np.concatenate([colour, a[..., None]], axis=2)
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8), "RGBA")


def badge(logo: Image.Image, width: int, alpha: int, radius_ratio: float = 0.16) -> Image.Image:
    """Navy rounded pill behind the logo, for readability on any footage."""
    scale = width / logo.width
    logo = logo.resize((width, max(1, round(logo.height * scale))), Image.LANCZOS)
    pad_x, pad_y = round(width * 0.10), round(logo.height * 0.16)
    w, h = logo.width + 2 * pad_x, logo.height + 2 * pad_y
    canvas = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], radius=round(h * radius_ratio), fill=alpha)
    canvas.paste(Image.new("RGBA", (w, h), NAVY + (255,)), (0, 0), mask)
    canvas.alpha_composite(logo, (pad_x, pad_y))
    return canvas


def main(argv: list[str]) -> int:
    branding = pathlib.Path(argv[0])
    src = Image.open(branding / "mytel-logo-HOME-EXACT-512.png")
    logo = lockup_rgba(src)
    logo.save(branding / "mytel_logo_transparent.png")
    print("transparent logo:", logo.size)
    badge(logo, 640, 150).save(branding / "mytel_logo_badge.png")
    print("badge:", Image.open(branding / "mytel_logo_badge.png").size)
    # Review sheet: logo over a light and a dark background to check the key.
    w, h = logo.width, logo.height
    sheet = Image.new("RGB", (w, 2 * h), (255, 255, 255))
    ImageDraw.Draw(sheet).rectangle([0, h, w, 2 * h], fill=(235, 200, 150))
    sheet.paste(logo, (0, 0), logo)
    sheet.paste(logo, (0, h), logo)
    sheet.save(branding / "_qa_logo_key.png")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
