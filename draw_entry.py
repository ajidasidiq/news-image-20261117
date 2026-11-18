#!/usr/bin/env python3
"""Draw the news-image-20261117 entry: a newspaper front page summing up
Tuesday 17 November 2026. Written from scratch with PIL. Output: entry.png
(1024x1024, one day's world news, no photos, no copied artwork)."""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 22)
NAVY = (18, 38, 66)
RED = (176, 42, 48)
GOLD = (184, 134, 11)
GREY = (90, 88, 82)
LIGHT_LINE = (200, 192, 175)
CARD_BG = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, max_w, fill=INK, spacing=4):
    lines = wrap(draw, text, fnt, max_w)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + spacing
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- Masthead ----------
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.text((W // 2, 16), "THE WORLD TODAY", font=font(SERIF, 58),
           fill=(250, 246, 235), anchor="ma")
    d.text((W // 2, 88), "ONE DAY IN WORLD NEWS",
           font=font(SANS_B, 20), fill=(212, 175, 90), anchor="ma")
    d.rectangle([36, 148, W - 36, 152], fill=GOLD)
    d.text((W // 2, 166), "TUESDAY 17 NOVEMBER 2026",
           font=font(SANS_B, 42), fill=RED, anchor="ma")
    d.text((W // 2, 220), "Every story below happened or was first reported on this day",
           font=font(SANS_I, 19), fill=GREY, anchor="ma")
    d.line([36, 252, W - 36, 252], fill=INK, width=3)

    # ---------- Lead story: Kerch Bridge ----------
    y0 = 268
    d.text((36, y0), "LEAD STORY  •  UKRAINE", font=font(SANS_B, 18), fill=RED)
    d.text((36, y0 + 26), "UKRAINE STRIKES", font=font(SANS_B, 38), fill=INK)
    d.text((36, y0 + 70), "KERCH BRIDGE AGAIN", font=font(SANS_B, 38), fill=INK)
    lead = ("Kyiv hit the bridge to Crimea for a second day running; "
            "Russia struck bridges in Kyiv. Zelenskyy hailed an "
            "\u201cunprecedented operation\u201d.")
    draw_wrapped(d, 36, y0 + 122, lead, font(SANS, 21), 600, spacing=5)

    # Bridge illustration (right of lead text): deck, arch, towers, water, burst
    bx, by = 668, 268
    d.rectangle([bx, by, bx + 320, by + 180], fill=(226, 234, 240),
                outline=NAVY, width=2)
    d.rectangle([bx, by + 140, bx + 320, by + 180], fill=(120, 165, 200))
    for wx in range(bx + 12, bx + 310, 36):  # water ripples
        d.arc([wx, by + 148, wx + 26, by + 162], 0, 180, fill=(255, 255, 255), width=2)
    d.rectangle([bx + 30, by + 86, bx + 44, by + 140], fill=NAVY)   # tower
    d.rectangle([bx + 276, by + 86, bx + 290, by + 140], fill=NAVY)  # tower
    d.arc([bx + 30, by + 10, bx + 290, by + 140], 180, 360, fill=NAVY, width=5)
    d.rectangle([bx + 10, by + 86, bx + 310, by + 96], fill=NAVY)   # deck
    for cx in (bx + 90, bx + 160, bx + 230):  # cables
        d.line([cx, by + 96, cx, by + 36], fill=NAVY, width=2)
    # explosion burst over the deck
    cx, cy = bx + 160, by + 52
    for ang in range(0, 360, 30):
        r1, r2 = 12, 30
        x1 = cx + r1 * math.cos(math.radians(ang))
        y1 = cy + r1 * math.sin(math.radians(ang))
        x2 = cx + r2 * math.cos(math.radians(ang))
        y2 = cy + r2 * math.sin(math.radians(ang))
        d.line([x1, y1, x2, y2], fill=RED, width=4)
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=RED)
    d.text((bx, by + 186), "The Kerch Bridge, linking Russia to Crimea",
           font=font(SANS_I, 15), fill=GREY)

    d.line([36, 478, W - 36, 478], fill=INK, width=2)

    # ---------- Story grid: 3 x 3 ----------
    stories = [
        ("GULF  •  IRAN", "MINES HIT TANKERS\nNEAR HORMUZ",
         "Mines hit tankers near the Strait of Hormuz. Iran fired drones at a US radar base in Bahrain; all intercepted, no casualties."),
        ("ASIA  •  CHINA", "XI, TRUMP AND PUTIN\nTO MEET THURSDAY",
         "First three-way meeting confirmed for 19 November in Shenzhen, on the APEC sidelines. Trump was in Manila for ASEAN."),
        ("EUROPE  •  ESTONIA", "ESTONIA TO SHUT\nRUSSIAN BORDER",
         "Crossings close from 1 December, Tallinn said, citing a foiled Russian plot to bomb a drone plant."),
        ("ASIA  •  JAPAN", "JAPAN SCRAMBLES\nFIGHTER JETS",
         "Jets scrambled after suspected Russian aircraft violated Japanese airspace."),
        ("MIDDLE EAST  •  YEMEN", "HOUTHIS ADVANCE\nIN YEMEN",
         "Houthi forces advanced as Saudi-backed troops pulled back from the Red Sea coast to defend Aden."),
        ("BRITAIN  •  GAZA", "UK SANCTIONS\nSETTLEMENT FIRMS",
         "Britain sanctioned eight settlement construction firms; with Australia, Canada and Italy it urged Israel to open Gaza crossings for aid."),
        ("FRANCE", "DEPARDIEU ADMITS\nASSAULT CHARGE",
         "Actor G\u00e9rard Depardieu dropped his appeal and admitted a sexual assault charge in a Paris court."),
        ("TECHNOLOGY", "MICROSOFT EXPLAINS\nGLOBAL OUTAGE",
         "Last week\u2019s worldwide outage was caused by a latent defect plus increased load, the company said."),
        ("UNITED NATIONS", "128 STATES TALK BAN\nON KILLER ROBOTS",
         "Delegates met at the UN in Geneva on banning lethal autonomous weapons."),
    ]

    gx, gy = 36, 494
    cw, ch, gap = 304, 140, 18
    for i, (kicker, headline, summary) in enumerate(stories):
        col, row = i % 3, i // 3
        x = gx + col * (cw + gap)
        y = gy + row * (ch + gap)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD_BG, outline=LIGHT_LINE, width=1)
        d.rectangle([x, y, x + cw, y + 5], fill=RED)
        d.text((x + 12, y + 12), kicker, font=font(SANS_B, 14), fill=RED)
        hy = y + 32
        for line in headline.split("\n"):
            d.text((x + 12, hy), line, font=font(SANS_B, 19), fill=INK)
            hy += 23
        draw_wrapped(d, x + 12, hy + 2, summary, font(SANS, 15), cw - 24, spacing=2)

    # ---------- Allegation box ----------
    ay = 494 + 3 * ch + 2 * gap + 10  # 956
    d.rectangle([36, ay, W - 36, ay + 42], outline=RED, width=2)
    d.text((48, ay + 4), "ALSO REPORTED \u2014 CLAIM, NOT CONFIRMED:",
           font=font(SANS_B, 15), fill=RED)
    d.text((48, ay + 23),
           "US intelligence claims Iran is plotting a \u201cdirty bomb\u201d attack in Washington.",
           font=font(SANS, 16), fill=INK)

    # ---------- Footer ----------
    d.text((W // 2, 1006), "All stories reported on Tuesday 17 November 2026  •  THE WORLD TODAY",
           font=font(SANS, 13), fill=GREY, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
