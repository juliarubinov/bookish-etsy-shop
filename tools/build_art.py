#!/usr/bin/env python3
"""Render print-ready artwork for the Department of Yearning collection.

Everything is drawn directly at the final pixel size of each print area (type,
shapes and rules are drawn by code, never upscaled). If Printify's real print-area
size differs, change SPECS below and re-run:

    python3 tools/build_art.py

Outputs:  products/<slug>/art/<slug>-print.png   (transparent, sRGB, 300 DPI tag)
"""
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"

# Brand palette (see brand/README.md)
INK = (42, 26, 31, 255)       # #2A1A1F
WINE = (122, 35, 56, 255)     # #7A2338
ROSE = (201, 103, 122, 255)   # #C9677A

# Print-area sizes in px at 300 DPI. UNVERIFIED: see research/verification-needed.md
SPECS = {
    "ruined-by-chapter-twelve-tee": (4500, 5100),        # Comfort Colors 1717 front
    "yearning-night-shift-sweatshirt": (4200, 4800),     # Gildan 18000 front
    "yearning-morning-shift-mug": (2475, 1155),          # 11oz ceramic mug wrap
    "contents-tote": (3000, 3600),                       # S&S Bags natural tote front (10x12 in assumed)
}


def font(name, size, variation=None):
    f = ImageFont.truetype(str(FONTS / name), size)
    if variation:
        f.set_variation_by_name(variation)
    return f


def DM(size):
    return font("DMSerifDisplay-Regular.ttf", size)


def PF_ITALIC(size, weight="SemiBold Italic"):
    return font("PlayfairDisplay-Italic[wght].ttf", size, weight)


def INTER(size):
    return font("Inter-SemiBold.otf", size)


# ---------------------------------------------------------------- text helpers
def text_width(f, s, tracking=0):
    if not tracking:
        return f.getlength(s)
    return sum(f.getlength(c) for c in s) + tracking * (len(s) - 1)


TEXT_LOG = []  # (text, font px) for every text element of the design being built


def draw_text(d, cx, y, s, f, fill, tracking=0):
    """Draw s horizontally centred on cx with its baseline at y."""
    TEXT_LOG.append((s, f.size))
    w = text_width(f, s, tracking)
    x = cx - w / 2
    if not tracking:
        d.text((x, y), s, font=f, fill=fill, anchor="ls")
        return
    for c in s:
        d.text((x, y), c, font=f, fill=fill, anchor="ls")
        x += f.getlength(c) + tracking


def fit_size(maker, s, max_w, start, tracking_ratio=0.0):
    size = start
    while size > 10:
        f = maker(size)
        if text_width(f, s, size * tracking_ratio) <= max_w:
            return f, size
        size -= 4
    return maker(size), size


def ring_text(img, center, radius, s, f, fill, start_deg, clockwise=True, tracking=0):
    """Write s along a circle. start_deg: angle (0 = top, clockwise) of the text's
    centre. Top arcs read clockwise; bottom arcs read counter-clockwise so
    both read left-to-right."""
    TEXT_LOG.append((s, f.size))
    cx, cy = center
    widths = [f.getlength(c) + tracking for c in s]
    total = sum(widths) - tracking
    total_deg = math.degrees(total / radius)
    sign = 1 if clockwise else -1
    a = start_deg - sign * total_deg / 2
    for c, w in zip(s, widths):
        step = math.degrees(w / radius)
        mid = a + sign * math.degrees((w - tracking) / 2 / radius)
        # Rotate a coverage mask, then fill with the exact ink colour, so rotation
        # never blends in off-palette colours.
        mask = Image.new("L", (int(f.size * 2), int(f.size * 2)), 0)
        ImageDraw.Draw(mask).text((mask.width / 2, mask.height / 2), c, font=f, fill=255, anchor="mm")
        rot = -mid if clockwise else -(mid + 180)
        mask = mask.rotate(rot, resample=Image.BICUBIC, expand=True)
        rad = math.radians(mid)
        px = cx + radius * math.sin(rad)
        py = cy - radius * math.cos(rad)
        tile = Image.new("RGBA", mask.size, fill)
        tile.putalpha(mask)
        img.alpha_composite(tile, (int(px - tile.width / 2), int(py - tile.height / 2)))
        a += sign * step


# ---------------------------------------------------------------- motif helpers
def heart(d, cx, cy, size, fill):
    """Smooth parametric heart, size = overall width."""
    pts = []
    for i in range(240):
        t = 2 * math.pi * i / 240
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((cx + x * size / 34, cy - y * size / 34))
    d.polygon(pts, fill=fill)


def bezier(p0, p1, p2, n=60):
    return [((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0],
             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])
            for t in (i / n for i in range(n + 1))]


def open_book(d, cx, cy, w, fill, stroke):
    """Open book outline: two page curves meeting at a spine."""
    h = w * 0.36
    left_top = bezier((cx - w / 2, cy - h * 0.55), (cx - w / 4, cy - h * 0.95), (cx, cy - h * 0.55))
    right_top = bezier((cx, cy - h * 0.55), (cx + w / 4, cy - h * 0.95), (cx + w / 2, cy - h * 0.55))
    left_bot = bezier((cx - w / 2, cy + h * 0.45), (cx - w / 4, cy + h * 0.05), (cx, cy + h * 0.45))
    right_bot = bezier((cx, cy + h * 0.45), (cx + w / 4, cy + h * 0.05), (cx + w / 2, cy + h * 0.45))
    d.line(left_top + [left_bot[-1]] + left_bot[::-1] + [left_top[0]], fill=fill, width=stroke, joint="curve")
    d.line(right_top + right_bot[::-1][0:1] + right_bot[::-1] + [right_top[0]], fill=fill, width=stroke, joint="curve")
    d.line([(cx - w / 2, cy - h * 0.55), (cx - w / 2, cy + h * 0.45)], fill=fill, width=stroke)
    d.line([(cx + w / 2, cy - h * 0.55), (cx + w / 2, cy + h * 0.45)], fill=fill, width=stroke)
    d.line([(cx, cy - h * 0.55), (cx, cy + h * 0.45)], fill=fill, width=stroke)
    # page lines
    for k in (0.25, 0.5):
        off = h * k * 0.9
        d.line(bezier((cx - w * 0.40, cy - h * 0.5 + off + h * 0.1), (cx - w * 0.22, cy - h * 0.82 + off + h * 0.1),
                      (cx - w * 0.08, cy - h * 0.5 + off + h * 0.12)), fill=fill, width=max(2, stroke // 2))
        d.line(bezier((cx + w * 0.08, cy - h * 0.5 + off + h * 0.12), (cx + w * 0.22, cy - h * 0.82 + off + h * 0.1),
                      (cx + w * 0.40, cy - h * 0.5 + off + h * 0.1)), fill=fill, width=max(2, stroke // 2))


def crescent(img, cx, cy, r, fill):
    m = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(m)
    md.ellipse((cx - r, cy - r, cx + r, cy + r), fill=255)
    md.ellipse((cx - r * 0.45, cy - r * 1.05, cx + r * 1.45, cy + r * 0.85), fill=0)
    layer = Image.new("RGBA", img.size, fill)
    img.paste(layer, (0, 0), m)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(8):
        rr = r if i % 2 == 0 else r * 0.32
        a = math.pi / 4 * i
        pts.append((cx + rr * math.sin(a), cy - rr * math.cos(a)))
    d.polygon(pts, fill=fill)


def mug_icon(d, cx, cy, w, fill, stroke):
    """Teacup on a saucer, with a heart for steam."""
    h = w * 0.62
    top_y, bot_y = cy - h * 0.35, cy + h * 0.45
    x0, x1 = cx - w * 0.40, cx + w * 0.28
    taper = w * 0.08
    body = [(x0, top_y)] + bezier((x0, top_y), (x0 + taper * 0.2, bot_y + h * 0.05),
                                  ((x0 + x1) / 2, bot_y)) + \
           bezier(((x0 + x1) / 2, bot_y), (x1 - taper * 0.2, bot_y + h * 0.05), (x1, top_y))
    d.polygon(body, fill=fill)
    d.arc((x1 - w * 0.10, top_y + h * 0.10, x1 + w * 0.20, top_y + h * 0.55), -80, 100, fill=fill, width=stroke)
    sy = bot_y + h * 0.16
    d.rounded_rectangle((cx - w * 0.52, sy, cx + w * 0.44, sy + stroke * 1.4), radius=stroke, fill=fill)
    heart(d, (x0 + x1) / 2, top_y - h * 0.42, w * 0.26, fill)


def seal(img, cx, cy, r, top, bottom, centre, color, accent):
    d = ImageDraw.Draw(img)
    s_out = max(8, int(r * 0.022))
    s_in = max(6, int(r * 0.012))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=color, width=s_out)
    ri = r * 0.70
    d.ellipse((cx - ri, cy - ri, cx + ri, cy + ri), outline=color, width=s_in)
    f = INTER(int(r * 0.125))
    rt = (r + ri) / 2
    ring_text(img, (cx, cy), rt - f.size * 0.36, top, f, color, 0, True, tracking=int(r * 0.03))
    ring_text(img, (cx, cy), rt + f.size * 0.36, bottom, f, color, 180, False, tracking=int(r * 0.03))
    for ang in (90, 270):
        a = math.radians(ang)
        heart(d, cx + rt * math.sin(a), cy - rt * math.cos(a), r * 0.07, accent)
    centre(img, d, cx, cy, ri)


# ---------------------------------------------------------------- designs
def tee(size):
    W, H = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = W / 2
    content_w = W * 0.80                      # 12 in of a 15 in print area
    # motif: open book with a rising heart
    open_book(d, cx, 840, 1000, INK, 34)
    heart(d, cx, 380, 260, WINE)
    # RUINED BY
    f, _ = fit_size(DM, "RUINED BY", content_w * 0.78, 900, 0.08)
    draw_text(d, cx, 1900, "RUINED BY", f, INK, tracking=f.size * 0.08)
    # Chapter Twelve
    f2, _ = fit_size(PF_ITALIC, "Chapter Twelve", content_w, 1100)
    draw_text(d, cx, 2900, "Chapter Twelve", f2, WINE)
    # rule with heart
    y = 3250
    d.line([(cx - content_w * 0.38, y), (cx - 120, y)], fill=INK, width=18)
    d.line([(cx + 120, y), (cx + content_w * 0.38, y)], fill=INK, width=18)
    heart(d, cx, y, 150, WINE)
    f3, _ = fit_size(INTER, "AND I'D READ IT AGAIN", content_w * 0.70, 220, 0.18)
    draw_text(d, cx, 3600, "AND I'D READ IT AGAIN", f3, INK, tracking=f3.size * 0.18)
    return img


def sweatshirt(size):
    W, H = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = W / 2

    def moon_centre(img, d, x, y, ri):
        crescent(img, x - ri * 0.08, y, ri * 0.55, WINE)
        star(d, x + ri * 0.42, y - ri * 0.32, ri * 0.13, INK)
        star(d, x + ri * 0.22, y + ri * 0.40, ri * 0.08, INK)

    seal(img, cx, 1250, 1050, "DEPARTMENT OF YEARNING", "EST. CHAPTER ONE", moon_centre, INK, WINE)
    d = ImageDraw.Draw(img)
    f, _ = fit_size(PF_ITALIC, "Night Shift", W * 0.80, 1000)
    draw_text(d, cx, 3350, "Night Shift", f, WINE)
    f3, _ = fit_size(INTER, "OPEN UNTIL THE LAST PAGE", W * 0.62, 200, 0.18)
    draw_text(d, cx, 3720, "OPEN UNTIL THE LAST PAGE", f3, INK, tracking=f3.size * 0.18)
    return img


def mug(size):
    W, H = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    # Side A (centre at 25 % of wrap): seal
    ax, bx = W * 0.25, W * 0.75
    r = H * 0.39

    def cup_centre(img, d, x, y, ri):
        mug_icon(d, x, y + ri * 0.12, ri * 0.85, WINE, max(8, int(ri * 0.07)))

    seal(img, ax, H / 2, r, "DEPARTMENT OF YEARNING", "MORNING SHIFT", cup_centre, INK, WINE)
    d = ImageDraw.Draw(img)
    # Side B: wording
    col_w = W * 0.36
    f1, _ = fit_size(DM, "Coffee first.", col_w, 300)
    draw_text(d, bx, H * 0.42, "Coffee first.", f1, INK)
    f2, _ = fit_size(PF_ITALIC, "Then yearning.", col_w, 300)
    draw_text(d, bx, H * 0.64, "Then yearning.", f2, WINE)
    f3, _ = fit_size(INTER, "DEPT. OF YEARNING", col_w * 0.70, 64, 0.16)
    draw_text(d, bx, H * 0.80, "DEPT. OF YEARNING", f3, INK, tracking=f3.size * 0.16)
    return img


def tote(size):
    W, H = size
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    cx = W / 2
    left, right = W * 0.10, W * 0.90
    f0, _ = fit_size(INTER, "DEPT. OF YEARNING — ISSUED BAG", right - left, 150, 0.16)
    draw_text(d, cx, 400, "DEPT. OF YEARNING — ISSUED BAG", f0, INK, tracking=f0.size * 0.16)
    d.line([(left, 540), (right, 540)], fill=INK, width=16)
    f1, _ = fit_size(PF_ITALIC, "Contents:", (right - left) * 0.80, 700)
    d.text((left, 1260), "Contents:", font=f1, fill=WINE, anchor="ls")
    TEXT_LOG.append(("Contents:", f1.size))
    items = ["Books (too many)", "Snacks", "Unresolved tension"]
    box = 210
    gap = 90
    longest = max(items, key=lambda t: DM(100).getlength(t))
    fi, _ = fit_size(DM, longest, right - left - box - gap - 20, 280)
    y = 1700
    for it in items:
        bx0 = left + 10
        d.rounded_rectangle((bx0, y - box, bx0 + box, y), radius=26, outline=INK, width=20)
        d.line([(bx0 + box * 0.18, y - box * 0.52), (bx0 + box * 0.42, y - box * 0.22),
                (bx0 + box * 0.95, y - box * 1.05)], fill=WINE, width=38, joint="curve")
        d.text((bx0 + box + gap, y), it, font=fi, fill=INK, anchor="ls")
        TEXT_LOG.append((it, fi.size))
        y += 430
    y_rule = y - 140
    d.line([(left, y_rule), (right, y_rule)], fill=INK, width=16)
    f3, _ = fit_size(INTER, "PLEASE HANDLE WITH FEELINGS", (right - left) * 0.85, 140, 0.18)
    draw_text(d, cx, y_rule + 230, "PLEASE HANDLE WITH FEELINGS", f3, INK, tracking=f3.size * 0.18)
    heart(d, cx, y_rule + 450, 150, WINE)
    return img


BUILDERS = {
    "ruined-by-chapter-twelve-tee": tee,
    "yearning-night-shift-sweatshirt": sweatshirt,
    "yearning-morning-shift-mug": mug,
    "contents-tote": tote,
}


def main():
    import json
    for slug, build in BUILDERS.items():
        TEXT_LOG.clear()
        out = ROOT / "products" / slug / "art"
        out.mkdir(parents=True, exist_ok=True)
        img = build(SPECS[slug])
        path = out / f"{slug}-print.png"
        img.save(path, dpi=(300, 300), optimize=True)
        (out / "text-sizes.json").write_text(json.dumps(
            [{"text": t, "font_px": px} for t, px in TEXT_LOG], indent=1))
        print(f"{path.relative_to(ROOT)}  {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
