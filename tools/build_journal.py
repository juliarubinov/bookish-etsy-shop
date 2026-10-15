#!/usr/bin/env python3
"""Build 'The Yearning Log' printable romance reading journal (digital product).

    python3 tools/build_journal.py

Outputs US Letter and A4 PDFs in products/yearning-log-printable/files/.
All page wording is original. Trope names are generic genre terms.
"""
from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "tools" / "fonts"
OUT = ROOT / "products" / "yearning-log-printable" / "files"

pdfmetrics.registerFont(TTFont("DM", str(FONTS / "DMSerifDisplay-Regular.ttf")))
pdfmetrics.registerFont(TTFont("DMI", str(FONTS / "DMSerifDisplay-Italic.ttf")))
# Lato (OFL) for small labels: Inter ships as CFF .otf, which reportlab can't embed.
pdfmetrics.registerFont(TTFont("Lato", str(FONTS / "Lato-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Lato-Bold", str(FONTS / "Lato-Bold.ttf")))
SANS = "Lato"
SANS_B = "Lato-Bold"

INK = Color(42 / 255, 26 / 255, 31 / 255)
WINE = Color(122 / 255, 35 / 255, 56 / 255)
BLUSH = Color(242 / 255, 201 / 255, 207 / 255)
LINE = Color(42 / 255, 26 / 255, 31 / 255, alpha=0.35)

TROPES = [
    "Enemies to lovers", "Friends to lovers", "Slow burn", "Second chance",
    "Fake dating", "Forced proximity", "Grumpy / sunshine", "Only one bed",
    "Marriage of convenience", "Workplace romance", "Small town", "Opposites attract",
    "Secret identity", "Found family", "Rivals", "Forbidden love",
]


def heart(c, x, y, s, fill=True):
    p = c.beginPath()
    p.moveTo(x, y - s * 0.45)
    p.curveTo(x - s * 0.9, y + s * 0.05, x - s * 0.45, y + s * 0.65, x, y + s * 0.25)
    p.curveTo(x + s * 0.45, y + s * 0.65, x + s * 0.9, y + s * 0.05, x, y - s * 0.45)
    p.close()
    c.drawPath(p, fill=1 if fill else 0, stroke=0 if fill else 1)


def flame(c, x, y, s):
    p = c.beginPath()
    p.moveTo(x, y - s * 0.5)
    p.curveTo(x - s * 0.55, y - s * 0.4, x - s * 0.45, y + s * 0.15, x, y + s * 0.6)
    p.curveTo(x + s * 0.05, y + s * 0.2, x + s * 0.45, y + s * 0.2, x + s * 0.3, y - s * 0.1)
    p.curveTo(x + s * 0.5, y - s * 0.35, x + s * 0.25, y - s * 0.5, x, y - s * 0.5)
    p.close()
    c.drawPath(p, fill=0, stroke=1)


class Book:
    def __init__(self, path, size):
        self.W, self.H = size
        self.c = canvas.Canvas(str(path), pagesize=size, initialFontName="Lato", initialFontSize=10)
        self.c.setTitle("The Yearning Log — Romance Reading Journal")
        self.c.setAuthor("Department of Yearning")
        self.m = 0.6 * inch
        self.page_no = 0

    # chrome shared by inner pages
    def header(self, title, kicker):
        c, W, H, m = self.c, self.W, self.H, self.m
        c.setFillColor(WINE)
        c.setFont(SANS_B, 8)
        c.drawString(m, H - m, kicker.upper())
        c.setFillColor(INK)
        c.setFont("DM", 30)
        c.drawString(m, H - m - 36, title)
        c.setStrokeColor(INK)
        c.setLineWidth(0.8)
        c.line(m, H - m - 50, W - m, H - m - 50)
        return H - m - 78

    def footer(self):
        self.page_no += 1
        c = self.c
        c.setFont(SANS, 7.5)
        c.setFillColor(INK)
        c.drawCentredString(self.W / 2, self.m * 0.55,
                            "THE YEARNING LOG  ·  DEPT. OF YEARNING  ·  FOR PERSONAL USE")
        c.showPage()

    def lines(self, x0, x1, y_top, n, gap=22):
        c = self.c
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        for i in range(n):
            y = y_top - i * gap
            c.line(x0, y, x1, y)
        return y_top - n * gap

    def label(self, x, y, text):
        c = self.c
        c.setFillColor(WINE)
        c.setFont(SANS_B, 7.5)
        c.drawString(x, y, text.upper())
        c.setFillColor(INK)

    def field(self, x, y, w, text):
        self.label(x, y + 4, text)
        c = self.c
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(x, y - 14, x + w, y - 14)

    # pages
    def cover(self):
        c, W, H = self.c, self.W, self.H
        c.setFillColor(BLUSH)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setStrokeColor(INK)
        c.setLineWidth(1.4)
        c.circle(W / 2, H * 0.66, 86)
        c.setLineWidth(0.7)
        c.circle(W / 2, H * 0.66, 62)
        c.setFillColor(WINE)
        heart(c, W / 2, H * 0.66 - 4, 46)
        c.setFillColor(INK)
        c.setFont(SANS_B, 9)
        c.drawCentredString(W / 2, H * 0.66 + 102, "DEPARTMENT OF YEARNING")
        c.drawCentredString(W / 2, H * 0.66 - 110, "OFFICIAL RECORDS")
        c.setFont("DM", 54)
        c.drawCentredString(W / 2, H * 0.43, "The Yearning Log")
        c.setFillColor(WINE)
        c.setFont("DMI", 20)
        c.drawCentredString(W / 2, H * 0.43 - 34, "a reading journal for romance readers")
        c.setFillColor(INK)
        c.setFont("DMI", 14)
        c.drawCentredString(W / 2, H * 0.22, "This log belongs to")
        c.setLineWidth(0.8)
        c.line(W / 2 - 150, H * 0.22 - 30, W / 2 + 150, H * 0.22 - 30)
        c.showPage()

    def how_to(self):
        c, m, W = self.c, self.m, self.W
        y = self.header("How to use this log", "Orientation")
        paras = [
            ("Book Records", "One page per book. Rate the yearning, the spice and the ending, "
             "and note the moment you had to put the book down and stare at a wall."),
            ("Trope Tracker", "Tick a trope every time you finish a book that uses it. By December "
             "you'll know exactly what you can't resist."),
            ("Spine Shelf", "Colour one spine for each book you finish this year."),
            ("TBR & Wishlist", "For the books you've been meaning to read and the ones you want next."),
            ("Printing", "Print at 100% / Actual size. Prints well on plain paper; 32 lb (120 gsm) paper "
             "takes pens better. Print the Book Record page as often as you like for personal use."),
        ]
        for title, body in paras:
            c.setFillColor(WINE)
            c.setFont("DM", 16)
            c.drawString(m, y, title)
            y -= 18
            c.setFillColor(INK)
            c.setFont(SANS, 10)
            for line in wrap(body, SANS, 10, W - 2 * m):
                c.drawString(m, y, line)
                y -= 14
            y -= 14
        self.footer()

    def book_record(self):
        c, m, W = self.c, self.m, self.W
        y = self.header("Book Record", "Case file no. ______")
        col = (W - 2 * m - 20) / 2
        self.field(m, y, W - 2 * m, "Title")
        y -= 40
        self.field(m, y, col, "Author")
        self.field(m + col + 20, y, col, "Series / no.")
        y -= 40
        self.field(m, y, col * 0.62, "Started")
        self.field(m + col * 0.66, y, col * 0.62, "Finished")
        self.label(m + col * 1.35 + 20, y + 4, "Format")
        c.setFont(SANS, 9)
        x = m + col * 1.35 + 20
        for fmt in ("Print", "E-book", "Audio"):
            c.setStrokeColor(INK)
            c.rect(x, y - 16, 8, 8, stroke=1, fill=0)
            c.drawString(x + 12, y - 15, fmt)
            x += 52
        y -= 50
        # ratings
        rows = [("Yearning", "heart"), ("Spice", "flame"), ("Overall", "heart")]
        for name, icon in rows:
            self.label(m, y, name)
            for i in range(5):
                cx = m + 110 + i * 26
                c.setStrokeColor(WINE)
                c.setLineWidth(1)
                if icon == "heart":
                    c.setFillColor(WINE)
                    heart(c, cx, y + 2, 16, fill=False)
                else:
                    flame(c, cx, y + 2, 16)
            y -= 28
        # ending
        self.label(m, y, "The ending")
        x = m + 110
        c.setFont(SANS, 9)
        for opt in ("HEA", "HFN", "Cliffhanger", "Still recovering"):
            c.setStrokeColor(INK)
            c.rect(x, y - 1, 8, 8, stroke=1, fill=0)
            c.drawString(x + 12, y, opt)
            x += c.stringWidth(opt, SANS, 9) + 32
        y -= 34
        self.label(m, y, "Tropes spotted")
        y = self.lines(m, W - m, y - 20, 2)
        y -= 14
        self.label(m, y, "The moment I had to put the book down")
        y = self.lines(m, W - m, y - 20, 4)
        y -= 14
        self.label(m, y, "What I'd tell a friend (no spoilers)")
        y = self.lines(m, W - m, y - 20, 4)
        y -= 14
        self.label(m, y, "Would re-read?")
        c.setFont(SANS, 9)
        x = m + 110
        for opt in ("Immediately", "Someday", "Once was enough"):
            c.rect(x, y - 1, 8, 8, stroke=1, fill=0)
            c.drawString(x + 12, y, opt)
            x += c.stringWidth(opt, SANS, 9) + 32
        self.footer()

    def trope_tracker(self):
        c, m, W = self.c, self.m, self.W
        y = self.header("Trope Tracker", "Annual review")
        c.setFont(SANS, 9.5)
        c.drawString(m, y, "One mark per finished book. Blank rows are for your own favourites.")
        y -= 26
        rows = TROPES + [""] * 4
        boxes = 12
        name_w = 150
        bw = (W - 2 * m - name_w) / boxes
        for t in rows:
            c.setFont("DM", 12)
            c.setFillColor(INK)
            if t:
                c.drawString(m, y, t)
            else:
                c.setStrokeColor(LINE)
                c.line(m, y - 2, m + name_w - 14, y - 2)
            c.setStrokeColor(LINE)
            c.setLineWidth(0.6)
            for i in range(boxes):
                c.rect(m + name_w + i * bw + 2, y - 4, bw - 4, 14, stroke=1, fill=0)
            y -= 27
        self.footer()

    def spine_shelf(self):
        c, m, W = self.c, self.m, self.W
        y = self.header("Spine Shelf", "Books finished this year")
        c.setFont(SANS, 9.5)
        c.drawString(m, y, "Colour a spine for every book you finish. Write the title down the spine.")
        y -= 30
        per_row, shelves = 13, 4
        sw = (W - 2 * m) / per_row
        sh = (y - self.m * 1.4) / shelves - 16
        c.setStrokeColor(INK)
        for s in range(shelves):
            top = y - s * (sh + 16)
            for i in range(per_row):
                h = sh * (0.78 + 0.22 * ((i * 7 + s * 3) % 5) / 4)
                c.setLineWidth(0.7)
                c.rect(m + i * sw + 3, top - sh, sw - 6, h, stroke=1, fill=0)
            c.setLineWidth(2.2)
            c.line(m - 4, top - sh - 2, W - m + 4, top - sh - 2)
        self.footer()

    def tbr(self):
        c, m, W = self.c, self.m, self.W
        y = self.header("TBR & Wishlist", "Pending review")
        col = (W - 2 * m - 24) / 2
        for k, title in enumerate(("To be read", "Wishlist")):
            x = m + k * (col + 24)
            c.setFillColor(WINE)
            c.setFont("DM", 16)
            c.drawString(x, y, title)
            c.setFillColor(INK)
            yy = y - 26
            c.setStrokeColor(LINE)
            for i in range(24):
                c.rect(x, yy - 2, 8, 8, stroke=1, fill=0)
                c.line(x + 14, yy - 3, x + col, yy - 3)
                yy -= 23
        self.footer()

    def save(self):
        self.c.save()


def wrap(text, font, size, width):
    from reportlab.pdfbase.pdfmetrics import stringWidth
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if stringWidth(t, font, size) <= width:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def build(path, size):
    b = Book(path, size)
    b.cover()
    b.how_to()
    for _ in range(4):
        b.book_record()
    b.trope_tracker()
    b.spine_shelf()
    b.tbr()
    b.save()
    return path


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, size in (("US-Letter", letter), ("A4", A4)):
        p = build(OUT / f"yearning-log-{name}.pdf", size)
        print(p.relative_to(ROOT))
