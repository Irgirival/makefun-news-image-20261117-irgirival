"""Render the front page for Tuesday, 17 November 2026.

Draws a one-page newspaper front page with PIL: a masthead, the date,
one lead story (Kerch Bridge) with a small drawn illustration, six
story panels across regions and fields, and a ticker of further news
from the same day. Every fact is an event reported on 17 November 2026.

Run:  python3 render.py            -> writes entry.png beside this file
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1024, 1024

PAPER = (246, 241, 229)
INK = (20, 32, 43)
NAVY = (15, 43, 70)
NAVY_DARK = (10, 30, 50)
RED = (166, 30, 30)
GOLD = (200, 162, 74)
MUTED = (90, 100, 112)
CARD = (255, 255, 255)
BORDER = (205, 198, 182)
SKY = (220, 232, 240)
SEA = (46, 107, 138)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(text, fnt, max_w):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, fnt, fill, anchor="la"):
    draw.text(xy, s, font=fnt, fill=fill, anchor=anchor)


def spaced(s):
    """Fake letterspacing for kickers."""
    return " ".join(list(s.replace(" ", "   ")))


def draw_bridge(draw, x0, y0, x1, y1):
    """A small bridge with its middle span collapsed into the water."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY)
    horizon = y0 + int((y1 - y0) * 0.62)
    draw.rectangle([x0, horizon, x1, y1], fill=SEA)
    # sun
    draw.ellipse([x1 - 52, y0 + 14, x1 - 22, y0 + 44], fill=(240, 200, 90))
    # waves
    for i, wy in enumerate((horizon + 22, horizon + 52, horizon + 82)):
        for k in range(4):
            wx = x0 + 18 + k * 72 + (14 if i % 2 else 0)
            draw.arc([wx, wy, wx + 44, wy + 16], 0, 180, fill=(255, 255, 255), width=3)
    # pylons
    for px in (x0 + 52, x1 - 62):
        draw.rectangle([px, y0 + 46, px + 10, horizon], fill=NAVY_DARK)
    # deck: left segment intact, right segment broken and tilted down
    deck_y = y0 + 96
    draw.rectangle([x0 + 8, deck_y, x0 + 132, deck_y + 10], fill=(70, 70, 70))
    draw.rectangle([x0 + 142, deck_y, x0 + 178, deck_y + 10], fill=(70, 70, 70))
    # fallen span sinking into the water
    draw.polygon(
        [(x0 + 186, deck_y + 4), (x0 + 258, deck_y + 52),
         (x0 + 258, deck_y + 62), (x0 + 186, deck_y + 14)],
        fill=(70, 70, 70),
    )
    # cables from pylons to deck
    for cx in (x0 + 30, x0 + 60, x0 + 90, x0 + 118):
        draw.line([x0 + 57, y0 + 50, cx, deck_y], fill=NAVY_DARK, width=2)
    for cx in (x1 - 40, x1 - 66):
        draw.line([x1 - 57, y0 + 50, cx, deck_y], fill=NAVY_DARK, width=2)
    # splash where the span fell
    for sx in (x0 + 226, x0 + 246, x0 + 266):
        draw.arc([sx, horizon + 2, sx + 22, horizon + 22], 180, 360,
                 fill=(255, 255, 255), width=3)
    draw.rectangle([x0, y0, x1, y1], outline=BORDER, width=2)


def panel(draw, x, y, w, h, accent, kicker, headline, body):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=BORDER, width=2)
    draw.rectangle([x, y, x + w, y + 7], fill=accent)
    cx = x + 16
    text(draw, (cx, y + 18), spaced(kicker), SANS_B(13), accent)
    lines = wrap(headline, SANS_B(20), w - 32)
    ly = y + 44
    for ln in lines[:2]:
        text(draw, (cx, ly), ln, SANS_B(20), INK)
        ly += 25
    blines = wrap(body, SANS(15), w - 32)
    by = ly + 6
    for ln in blines[:4]:
        text(draw, (cx, by), ln, SANS(15), (52, 60, 70))
        by += 19


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead -------------------------------------------------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    text(d, (W // 2, 16), spaced("THE WORLD IN ONE PAGE"), SANS_B(14), GOLD, anchor="ma")
    text(d, (W // 2, 38), "THE DAY IN REVIEW", SERIF_B(56), (255, 255, 255), anchor="ma")
    d.line([28, 118, W - 28, 118], fill=RED, width=4)

    # ---- date strip ----------------------------------------------
    text(d, (W // 2, 132), "TUESDAY, NOVEMBER 17, 2026", SERIF_B(33), INK, anchor="ma")
    text(d, (W // 2, 172), "Six stories from five continents \u2014 the day as the world reported it",
         SANS(16), MUTED, anchor="ma")

    # ---- lead story ----------------------------------------------
    lx, ly, lw, lh = 28, 200, 968, 258
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=BORDER, width=2)
    d.rectangle([lx, ly, lx + lw, ly + 7], fill=RED)
    tx = lx + 24
    text(d, (tx, ly + 20), spaced("UKRAINE \u2014 WAR IN EUROPE"), SANS_B(14), RED)
    head = ["Kerch Bridge hit again \u2014",
            "road span falls into the sea"]
    hy = ly + 48
    for ln in head:
        text(d, (tx, hy), ln, SERIF_B(36), INK)
        hy += 44
    body = ("Ukrainian forces struck the bridge linking Russia to occupied "
            "Crimea for a second straight day. Footage verified by CNN shows "
            "a road section collapsed into the water; rail traffic halted.")
    by = hy + 6
    for ln in wrap(body, SANS(17), 588):
        text(d, (tx, by), ln, SANS(17), (52, 60, 70))
        by += 23
    draw_bridge(d, lx + 636, ly + 20, lx + lw - 24, ly + lh - 20)

    # ---- story grid: 2 rows x 3 -----------------------------------
    stories = [
        ((0, 128, 128), "ASIA\u2013PACIFIC",
         "Trump opens Asia trip in Manila",
         "Quad summit opens his first Asia tour since returning to office, "
         "with a Thailand trade pledge. Talks with Xi and Putin due "
         "in Shenzhen Nov 19."),
        ((166, 30, 30), "MIDDLE EAST",
         "Iran drones target US base in Bahrain",
         "Bahrain says its defences stopped drones aimed at a US radar "
         "site; no casualties. A fourth tanker burned in the Strait "
         "of Hormuz in 24 hours."),
        ((30, 90, 160), "EUROPE",
         "Five EU states plan Rwanda return hub",
         "Austria, Denmark, Germany, Greece and the Netherlands would send "
         "rejected asylum seekers to Rwanda. Transfers could begin in 2027."),
        ((190, 110, 20), "GAZA",
         "West urges Israel to open Gaza crossings",
         "Britain, Australia, Canada and Italy call the situation "
         "catastrophic. UN agencies warn 1.7 million people remain "
         "displaced as winter sets in."),
        ((110, 60, 140), "TRADE & TECH",
         "US closes chip-export loophole",
         "A new Commerce rule targets data centres renting computing power "
         "to China. Malaysia, Indonesia and Thailand face new limits."),
        ((120, 85, 50), "COURTS",
         "Depardieu admits sexual assault charge",
         "The French actor drops his appeal before a Paris court, pleading "
         "guilty in a case that has gripped France for years."),
    ]
    pw, ph, gx, gy = 312, 192, 16, 16
    for i, (accent, kicker, headline, body) in enumerate(stories):
        px = 28 + (i % 3) * (pw + gx)
        py = 474 + (i // 3) * (ph + gy)
        panel(d, px, py, pw, ph, accent, kicker, headline, body)

    # ---- ticker ---------------------------------------------------
    tx0, ty0, tx1, ty1 = 28, 890, 996, 956
    d.rectangle([tx0, ty0, tx1, ty1], fill=NAVY)
    text(d, (tx0 + 16, ty0 + 10), "ALSO TODAY", SANS_B(14), GOLD)
    ticker = ("Mongolia's president resigns amid a corruption scandal  \u2022  "
              "COP31 climate talks enter a decisive phase in Antalya  \u2022  "
              "Japan scrambles jets as Russian aircraft enter its airspace  \u2022  "
              "WHO: Eritrea eliminates trachoma")
    ty = ty0 + 30
    for ln in wrap(ticker, SANS(14), tx1 - tx0 - 32):
        text(d, (tx0 + 16, ty), ln, SANS(14), (235, 238, 242))
        ty += 19

    # ---- footer ---------------------------------------------------
    text(d, (W // 2, 972),
         "Events of Tuesday, 17 November 2026, as reported that day.",
         SANS(13), MUTED, anchor="ma")

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
