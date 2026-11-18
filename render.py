#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news infographic (1024x1024 PNG).

Stories (all verified against news search, events of Wed 18 Nov 2026):
1. Gulf: Kuwait's air defences engage hostile drones early Wed; Bahrain
   all-clear after a new threat alert (Al Jazeera 00:24 UTC, Reuters 00:16 UTC).
2. APEC summit opens in Shenzhen (33rd leaders' meeting, 18-19 Nov).
3. Trump meets Marcos in Manila (bilateral + state lunch, Wed 18 Nov).
4. Cyclone Akvan: severe cyclone bearing down on India's east coast,
   heavy rain today, landfall 20 Nov (IMD).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

BG = (246, 241, 231)
NAVY = (27, 42, 74)
NAVY_SUB = (185, 196, 214)
RULE = (192, 57, 43)
CARD_BG = (255, 253, 248)
CARD_BORDER = (221, 213, 195)
INK = (26, 26, 26)
SUBINK = (90, 90, 90)
FOOT = (122, 117, 106)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_drone(d, cx, cy, s, color):
    """Small quadcopter drone, centred at (cx, cy), scale s."""
    arm = int(34 * s)
    r = int(13 * s)
    d.line([cx - arm, cy - arm, cx, cy], fill=color, width=int(5 * s))
    d.line([cx + arm, cy - arm, cx, cy], fill=color, width=int(5 * s))
    d.line([cx - arm, cy + arm, cx, cy], fill=color, width=int(5 * s))
    d.line([cx + arm, cy + arm, cx, cy], fill=color, width=int(5 * s))
    for dx, dy in ((-arm, -arm), (arm, -arm), (-arm, arm), (arm, arm)):
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  outline=color, width=int(4 * s))
    d.rounded_rectangle([cx - int(22 * s), cy - int(10 * s),
                         cx + int(22 * s), cy + int(10 * s)],
                        radius=int(8 * s), fill=color)
    d.ellipse([cx - int(5 * s), cy - int(5 * s), cx + int(5 * s), cy + int(5 * s)],
              fill=BG)


def draw_skyline(d, cx, cy, s, color):
    """City skyline: three towers with windows, centred at (cx, cy)."""
    base = cy + int(38 * s)
    towers = [(-42, 58, 26), (-12, 84, 30), (22, 66, 26)]
    for dx, h, w in towers:
        x0 = cx + int(dx * s)
        y0 = base - int(h * s)
        x1 = x0 + int(w * s)
        d.rectangle([x0, y0, x1, base], fill=color)
        for wy in range(y0 + int(10 * s), base - int(8 * s), int(16 * s)):
            for wx in range(x0 + int(6 * s), x1 - int(5 * s), int(12 * s)):
                d.rectangle([wx, wy, wx + int(4 * s), wy + int(4 * s)],
                            fill=CARD_BG)
    # antenna on the tallest tower
    tx = cx + int(3 * s)
    d.line([tx, base - int(84 * s), tx, base - int(98 * s)],
           fill=color, width=int(3 * s))
    d.ellipse([tx - int(3 * s), base - int(102 * s),
               tx + int(3 * s), base - int(96 * s)], fill=color)


def draw_globe(d, cx, cy, s, color):
    """Globe with meridians and a small star, centred at (cx, cy)."""
    r = int(40 * s)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color,
              width=int(5 * s))
    d.ellipse([cx - int(18 * s), cy - r, cx + int(18 * s), cy + r],
              outline=color, width=int(3 * s))
    d.line([cx - r, cy, cx + r, cy], fill=color, width=int(3 * s))
    d.arc([cx - r, cy - int(20 * s), cx + r, cy + int(20 * s)], 0, 180,
          fill=color, width=int(3 * s))
    # small four-point star at upper right
    sx, sy, sr = cx + int(34 * s), cy - int(34 * s), int(9 * s)
    d.polygon([(sx, sy - sr), (sx + int(3 * s), sy - int(3 * s)),
               (sx + sr, sy), (sx + int(3 * s), sy + int(3 * s)),
               (sx, sy + sr), (sx - int(3 * s), sy + int(3 * s)),
               (sx - sr, sy), (sx - int(3 * s), sy - int(3 * s))],
              fill=color)


def draw_cyclone(d, cx, cy, s, color):
    """Spiral storm with rain drops, centred at (cx, cy)."""
    start = 200
    for i, rad in enumerate((12, 20, 28, 36)):
        r = int(rad * s)
        d.arc([cx - r, cy - r, cx + r, cy + r], start + i * 55,
              start + i * 55 + 250, fill=color, width=int(5 * s))
    d.ellipse([cx - int(6 * s), cy - int(6 * s), cx + int(6 * s), cy + int(6 * s)],
              fill=color)
    # rain drops below
    for dx in (-30, 0, 30):
        x = cx + int(dx * s)
        y = cy + int(52 * s)
        d.ellipse([x - int(5 * s), y, x + int(5 * s), y + int(10 * s)],
                  fill=color)
        d.polygon([(x - int(5 * s), y + int(4 * s)), (x + int(5 * s), y + int(4 * s)),
                   (x, y - int(8 * s))], fill=color)


CARDS = [
    dict(kicker="MIDDLE EAST · WAR", color=(179, 64, 47), icon=draw_drone,
         headline="Kuwait's defences engage hostile drones",
         sub="Gulf exchange widens; Bahrain all-clear after alert."),
    dict(kicker="CHINA · APEC", color=(14, 122, 107), icon=draw_skyline,
         headline="APEC summit opens in Shenzhen",
         sub="Leaders gather; Trump due Thursday for Xi–Putin talks."),
    dict(kicker="PHILIPPINES · DIPLOMACY", color=(107, 63, 160), icon=draw_globe,
         headline="Trump meets Marcos in Manila",
         sub="Bilateral talks and state lunch; then on to China."),
    dict(kicker="ASIA · WEATHER", color=(31, 95, 168), icon=draw_cyclone,
         headline="Cyclone Akvan bears down on India",
         sub="Severe storm; heavy rain today, landfall 20 Nov."),
]


def draw_card(d, x0, y0, w, h, card):
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=10,
                        fill=CARD_BG, outline=CARD_BORDER, width=2)
    # left accent bar
    d.rounded_rectangle([x0, y0, x0 + 10, y0 + h], radius=5,
                        fill=card["color"])
    f_kick = font(FONT_BOLD, 23)
    f_head = font(FONT_BOLD, 37)
    f_sub = font(FONT_REG, 25)
    # kicker
    d.text((x0 + 26, y0 + 26), card["kicker"], font=f_kick, fill=card["color"])
    # icon (left) + headline (right of icon)
    icon_cx, icon_cy = x0 + 26 + 48, y0 + 66 + 48
    card["icon"](d, icon_cx, icon_cy, 1.0, card["color"])
    head_w = w - 26 - 96 - 16 - 22
    lines = wrap(card["headline"], f_head, head_w)
    y = y0 + 62
    for ln in lines:
        d.text((x0 + 138, y), ln, font=f_head, fill=INK)
        y += 46
    # sub-line goes below BOTH the headline block and the icon,
    # so it can never overlap a 3-line headline
    head_bottom = y0 + 62 + len(lines) * 46
    icon_bottom = y0 + 62 + 96
    sub_lines = wrap(card["sub"], f_sub, w - 52)
    y = max(head_bottom, icon_bottom) + 20
    for ln in sub_lines:
        d.text((x0 + 26, y), ln, font=f_sub, fill=SUBINK)
        y += 33


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 180], fill=NAVY)
    d.text((W // 2, 34), "18 NOVEMBER 2026", font=font(FONT_BOLD, 80),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 128), "WEDNESDAY · THE WORLD'S NEWS IN ONE IMAGE",
           font=font(FONT_BOLD, 26), fill=NAVY_SUB, anchor="ma")
    d.rectangle([0, 180, W, 186], fill=RULE)
    # 2x2 card grid
    margin = 24
    gap = 20
    cw = (W - margin * 2 - gap) // 2
    ch = 340
    grid_top = 186 + 24
    for i, card in enumerate(CARDS):
        cx = margin + (i % 2) * (cw + gap)
        cy = grid_top + (i // 2) * (ch + gap)
        draw_card(d, cx, cy, cw, ch, card)
    # footer
    fy = grid_top + 2 * ch + gap + 18
    d.text((W // 2, fy), "As reported on 18 November 2026 · Sources: Al Jazeera, Reuters, AP, IMD",
           font=font(FONT_REG, 20), fill=FOOT, anchor="ma")
    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
