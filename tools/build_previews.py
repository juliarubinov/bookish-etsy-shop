#!/usr/bin/env python3
"""Flat, to-scale previews of each print file on its blank.

    python3 tools/build_previews.py

These are ILLUSTRATIVE previews to judge size, placement and colour, drawn to
the assumed print area. They are NOT production mockups: final listing photos
should come from Printify's mockup generator after the files are uploaded.
Garment shapes and colours are approximate.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "tools" / "fonts" / "Inter-Medium.otf"
PPI = 40  # preview pixels per real inch

from qc import BLANK_COLOURS  # noqa: E402


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def shade(rgb, k):
    return tuple(max(0, min(255, int(c * k))) for c in rgb)


def label(img, text):
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(str(FONT), 18)
    d.rectangle((0, img.height - 34, img.width, img.height), fill=(42, 26, 31))
    d.text((12, img.height - 27), text, font=f, fill=(247, 239, 228))


def garment(art_path, colour, chest_in, length_in, sleeve, print_w_in, top_in, name):
    """Front view. chest_in = flat body width; print area placed top_in below collar."""
    W = int((chest_in + 2 * sleeve * 0.8 + 2) * PPI)
    H = int((length_in + 4) * PPI) + 34
    img = Image.new("RGB", (W, H), (246, 244, 240))
    d = ImageDraw.Draw(img)
    c = hex_rgb(colour)
    cx = W / 2
    bw = chest_in * PPI
    top = 2 * PPI
    neck = 3.6 * PPI
    sh = 1.3 * PPI
    body = [(cx - bw / 2, top + sh * 1.6), (cx - bw / 2 - 0.4 * PPI, top + sh),  # left shoulder
            (cx - neck, top), (cx + neck, top),
            (cx + bw / 2 + 0.4 * PPI, top + sh), (cx + bw / 2, top + sh * 1.6),
            (cx + bw / 2, top + length_in * PPI), (cx - bw / 2, top + length_in * PPI)]
    sl = sleeve * PPI
    lsleeve = [(cx - bw / 2 - 0.4 * PPI, top + sh), (cx - bw / 2 - sl * 0.75, top + sh + sl),
               (cx - bw / 2 - sl * 0.75 + 2.6 * PPI, top + sh + sl + 1.1 * PPI), (cx - bw / 2, top + sh * 3.2)]
    rsleeve = [(W - x, y) for x, y in lsleeve]
    for poly in (lsleeve, rsleeve, body):
        d.polygon(poly, fill=c, outline=shade(c, 0.82))
    d.chord((cx - neck, top - neck * 0.55, cx + neck, top + neck * 0.55), 0, 180, fill=shade(c, 0.9),
            outline=shade(c, 0.78), width=3)
    art = Image.open(art_path)
    scale = print_w_in * PPI / art.width
    art = art.resize((int(art.width * scale), int(art.height * scale)), Image.LANCZOS)
    img.paste(art, (int(cx - art.width / 2), int(top + top_in * PPI)), art)
    label(img, f"{name} — illustrative to-scale preview, not a production mockup")
    return img


def tote_preview(art_path, colour, name):
    bag_w, bag_h, pw = 15, 16, 10
    W, H = int((bag_w + 4) * PPI), int((bag_h + 12) * PPI) + 34
    img = Image.new("RGB", (W, H), (246, 244, 240))
    d = ImageDraw.Draw(img)
    c = hex_rgb(colour)
    x0, y0 = 2 * PPI, 9 * PPI
    for sx in (4.0, bag_w - 4.0 - 0.0):
        # strap: a tall arch above the bag mouth
        d.arc((x0 + (sx - 2.2) * PPI, y0 - 7 * PPI, x0 + (sx + 2.2) * PPI, y0 + 7 * PPI), 180, 360,
              fill=shade(c, 0.8), width=int(1.0 * PPI))
    d.rectangle((x0, y0, x0 + bag_w * PPI, y0 + bag_h * PPI), fill=c, outline=shade(c, 0.82), width=3)
    art = Image.open(art_path)
    scale = pw * PPI / art.width
    art = art.resize((int(art.width * scale), int(art.height * scale)), Image.LANCZOS)
    img.paste(art, (int(x0 + (bag_w - pw) / 2 * PPI), int(y0 + 2 * PPI)), art)
    label(img, f"{name} — illustrative to-scale preview, not a production mockup")
    return img


def mug_preview(art_path, name):
    """Shows each half of the wrap as one face of the mug, side by side."""
    PPI = 90
    art = Image.open(art_path)
    wrap_w_in = 8.25
    s = wrap_w_in * PPI / art.width
    art = art.resize((int(art.width * s), int(art.height * s)), Image.LANCZOS)
    half = art.width // 2
    mug_w = int(3.25 * PPI)  # visible face of a 3.25 in diameter mug
    mug_h = int(3.8 * PPI)
    W, H = mug_w * 2 + 7 * PPI, mug_h + 3 * PPI + 34
    img = Image.new("RGB", (W, H), (246, 244, 240))
    d = ImageDraw.Draw(img)
    for i, (face, handle_side) in enumerate(((art.crop((0, 0, half, art.height)), "right"),
                                             (art.crop((half, 0, art.width, art.height)), "left"))):
        x = int(1.5 * PPI + i * (mug_w + 4 * PPI))
        y = int(1.5 * PPI)
        hx = x + mug_w if handle_side == "right" else x - int(1.3 * PPI)
        d.rounded_rectangle((hx, y + 0.6 * PPI, hx + 1.3 * PPI, y + mug_h - 0.9 * PPI), radius=int(0.6 * PPI),
                            outline=(225, 225, 225), width=int(0.32 * PPI))
        d.rounded_rectangle((x, y, x + mug_w, y + mug_h), radius=10, fill=(255, 255, 255), outline=(215, 215, 215), width=2)
        f = face.resize((mug_w - 8, int(face.height * (mug_w - 8) / face.width)), Image.LANCZOS)
        img.paste(f, (x + 4, int(y + (mug_h - f.height) / 2)), f)
    label(img, f"{name} — each face ≈ visible half of wrap; illustrative only")
    return img


def main():
    jobs = {
        "ruined-by-chapter-twelve-tee": lambda p, col, n: garment(p, col, 22, 29, 8, 15, 3.0, n),
        "yearning-night-shift-sweatshirt": lambda p, col, n: garment(p, col, 23, 28, 22, 14, 3.0, n),
        "will-they-tee": lambda p, col, n: garment(p, col, 22, 29, 8, 15, 3.0, n),
        "pining-professionally-sweatshirt": lambda p, col, n: garment(p, col, 23, 28, 22, 14, 3.0, n),
    }
    for slug, fn in jobs.items():
        art = ROOT / "products" / slug / "art" / f"{slug}-print.png"
        out = ROOT / "products" / slug / "previews"
        out.mkdir(exist_ok=True)
        for cname, hx in BLANK_COLOURS[slug].items():
            img = fn(art, hx, f"{cname}, size L")
            img.save(out / f"{slug}-{cname.lower().replace(' ', '-')}.jpg", quality=88)
    slug = "contents-tote"
    out = ROOT / "products" / slug / "previews"
    out.mkdir(exist_ok=True)
    tote_preview(ROOT / "products" / slug / "art" / f"{slug}-print.png", BLANK_COLOURS[slug]["Natural"],
                 "Natural canvas tote 15×16 in").save(out / f"{slug}-natural.jpg", quality=88)
    slug = "yearning-morning-shift-mug"
    out = ROOT / "products" / slug / "previews"
    out.mkdir(exist_ok=True)
    mug_preview(ROOT / "products" / slug / "art" / f"{slug}-print.png", "11oz white mug").save(
        out / f"{slug}-both-sides.jpg", quality=88)
    for p in sorted(ROOT.glob("products/*/previews/*.jpg")):
        print(p.relative_to(ROOT))


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(ROOT / "tools"))
    main()
