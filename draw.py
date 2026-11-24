#!/usr/bin/env python3
"""news-23 b101 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026 (31 stories).
Entry image 1024x1024. All scenes are drawn illustrations, not photographs.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (179, 18, 46)
DARKRED = (143, 14, 36)
GOLD = (201, 162, 39)
NAVY = (27, 42, 74)
GREEN = (20, 83, 45)
TEAL = (14, 107, 107)
GREY = (85, 85, 85)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text(draw, xy, s, font, fill, anchor="la"):
    draw.text(xy, s, font=font, fill=fill, anchor=anchor)


def fit_lines(draw, text_s, font_sizes, max_w, max_lines, path):
    """Pick the largest font size (from font_sizes, descending) whose wrap fits max_lines."""
    for sz in font_sizes:
        f = F(path, sz)
        lines = wrap(draw, text_s, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
    f = F(path, font_sizes[-1])
    return f, wrap(draw, text_s, f, max_w)[:max_lines]


# ---------- masthead ----------
d.rectangle([0, 0, W, 62], fill=INK)
text(d, (14, 8), "THE WORLD TODAY", F(SERIF_B, 44), (255, 255, 255))
text(d, (1010, 22), "MONDAY 23 NOVEMBER 2026", F(SANS_B, 15), GOLD, anchor="ra")

# ---------- kicker ----------
d.rectangle([0, 62, W, 84], fill=RED)
text(d, (512, 67), "AI rout hits Asia  \u00b7  UN chief urges AI rules  \u00b7  US lead over China at record low  \u00b7  Anthropic IPO $107.3B",
     F(SANS_B, 13), (255, 255, 255), anchor="ma")

# ---------- number strip (2 rows x 5) ----------
NUMBERS = [
    ("-3.3%", "KOSPI", RED),
    ("5.3", "US-CHINA POWER GAP", INK),
    ("11,762", "EBOLA CASES, DRC", INK),
    ("10T won", "SEOUL STABILISATION FUND", (150, 110, 0)),
    ("2%", "BILLIONAIRE TAX IN PARIS", (0, 110, 60)),
    ("$450M", "SKUBAL DEAL", NAVY),
    ("165", "RUSSIAN MISSILES/WEEK", DARKRED),
    ("12,000", "CLEARED IN MANCHESTER", INK),
    ("264 kg", "EXPLOSIVES SEIZED", (150, 110, 0)),
    ("$107.3B", "ANTHROPIC IPO", (0, 110, 60)),
]
cell_w = (W - 16) // 5
for i, (val, lab, col) in enumerate(NUMBERS):
    r, c = divmod(i, 5)
    x0 = 8 + c * cell_w
    y0 = 84 + r * 34
    text(d, (x0 + 4, y0 + 1), val, F(SANS_B, 17), col)
    text(d, (x0 + 4, y0 + 20), lab, F(SANS, 8), GREY)

# ---------- region bar ----------
REGIONS = [("ASIA-PACIFIC 7", 7, (27, 58, 107)), ("AMERICAS 8", 8, (163, 22, 33)),
           ("MIDDLE EAST 6", 6, (176, 141, 11)), ("EUROPE 5", 5, TEAL),
           ("AFRICA 3", 3, (46, 125, 50)), ("WORLD 2", 2, GREY)]
x = 0
tot = sum(n for _, n, _ in REGIONS)
for name, n, col in REGIONS:
    wseg = int(round(W * n / tot))
    d.rectangle([x, 152, x + wseg - 1, 173], fill=col)
    text(d, (x + wseg // 2, 158), name, F(SANS_B, 11), (255, 255, 255), anchor="ma")
    x += wseg

# ---------- UTC strip ----------
d.rectangle([0, 174, W, 189], fill=(233, 227, 210))
text(d, (8, 177), "THE DAY IN UTC", F(SANS_B, 10), INK)
text(d, (150, 177), "~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles",
     F(SANS, 10), (60, 60, 60))
text(d, (1016, 177), "~ APPROX", F(SANS, 9), GREY, anchor="ra")

# ---------- hero scenes ----------
HX = [8, 346, 684]
HW = 330
HY = 190
SCENE_H = 140

# scene 1: Kospi skyline + falling chart
x0 = HX[0]
d.rectangle([x0, HY, x0 + HW, HY + SCENE_H], fill=(22, 35, 63))
import random
random.seed(101)
for bx in range(0, HW, 26):
    bh = random.randint(38, 92)
    d.rectangle([x0 + bx + 2, HY + SCENE_H - bh, x0 + bx + 22, HY + SCENE_H], fill=(13, 22, 44))
    for wy in range(HY + SCENE_H - bh + 6, HY + SCENE_H - 4, 12):
        for wx in range(x0 + bx + 6, x0 + bx + 19, 8):
            if random.random() < 0.55:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=(255, 214, 90))
pts = [(x0 + 12, HY + 34), (x0 + 62, HY + 52), (x0 + 112, HY + 44), (x0 + 162, HY + 66),
       (x0 + 212, HY + 58), (x0 + 262, HY + 84), (x0 + 316, HY + 96)]
d.line(pts, fill=(255, 140, 40), width=3)
for px, py in pts:
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 255, 255), outline=(255, 140, 40))
text(d, (x0 + 12, HY + 6), "-3.3%", F(SANS_B, 26), (255, 255, 255))

# scene 2: Guterres globe + gold text
x0 = HX[1]
d.rectangle([x0, HY, x0 + HW, HY + SCENE_H], fill=GREEN)
text(d, (x0 + 12, HY + 10), "150", F(SANS_B, 44), GOLD)
text(d, (x0 + 12, HY + 58), "DELEGATES", F(SANS_B, 24), GOLD)
text(d, (x0 + 12, HY + 86), "BACK A RISK", F(SANS_B, 24), GOLD)
text(d, (x0 + 12, HY + 114), "FRAMEWORK", F(SANS_B, 24), GOLD)
cx, cy, r = x0 + 268, HY + 66, 46
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(214, 240, 214), outline=(255, 255, 255), width=2)
for k in range(-2, 3):
    d.arc([cx - r + abs(k) * 14, cy - r, cx + r - abs(k) * 14, cy + r], 90, 270, fill=(120, 180, 120))
    d.arc([cx - r + abs(k) * 14, cy - r, cx + r - abs(k) * 14, cy + r], 270, 90, fill=(120, 180, 120))
d.line([cx - r, cy, cx + r, cy], fill=(120, 180, 120))
d.line([cx, cy - r, cx, cy + r], fill=(120, 180, 120))
d.ellipse([cx - r, cy - 12, cx + r, cy + 12], outline=(120, 180, 120))

# scene 3: Power Index bars
x0 = HX[2]
d.rectangle([x0, HY, x0 + HW, HY + SCENE_H], fill=(250, 246, 236))
text(d, (x0 + 10, HY + 6), "NARROWEST SINCE 2018", F(SANS_B, 11), INK)
text(d, (x0 + HW - 10, HY + 6), "GAP 5.3", F(SANS_B, 11), RED, anchor="ra")
bars = [("78.9", "US", NAVY, 78.9), ("73.6", "CHINA", RED, 73.6), ("40.5", "INDIA", GOLD, 40.5)]
base = HY + SCENE_H - 22
for i, (val, lab, col, v) in enumerate(bars):
    bx = x0 + 24 + i * 104
    bh = int(v * 0.85)
    d.rectangle([bx, base - bh, bx + 62, base], fill=col)
    text(d, (bx + 31, base - bh - 20), val, F(SANS_B, 15), INK, anchor="ma")
    text(d, (bx + 31, base - 16), lab, F(SANS_B, 11), (255, 255, 255), anchor="ma")
    if lab == "INDIA":
        text(d, (bx + 31, base - bh - 20), val, F(SANS_B, 15), INK, anchor="ma")

HEROES = [
    ("KOSPI 4,708.54  \u00b7  -161 PTS", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    ("UN  \u00b7  BRIDGETOWN", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 back a risk framework.",
     "UNITED NATIONS"),
    ("ASIA POWER INDEX 2026", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 \u2014 gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for i, (kick, head, body, src) in enumerate(HEROES):
    x0 = HX[i]
    d.rectangle([x0, HY + SCENE_H, x0 + HW, HY + SCENE_H + 18], fill=INK)
    text(d, (x0 + 8, HY + SCENE_H + 3), kick, F(SANS_B, 11), (255, 255, 255))
    hf, hlines = fit_lines(d, head, [23, 21, 19], HW - 12, 2, SERIF_B)
    yy = HY + SCENE_H + 22
    for ln in hlines:
        text(d, (x0 + 4, yy), ln, hf, INK)
        yy += hf.size + 2
    blines = wrap(d, body, F(SANS, 12), HW - 10)[:2]
    yy = HY + SCENE_H + 22 + 2 * (hf.size + 2) + 4
    for ln in blines:
        text(d, (x0 + 4, yy), ln, F(SANS, 12), (40, 40, 40))
        yy += 15
    # source + chip row, fixed near bottom of hero block (below body descenders)
    sy = HY + SCENE_H + 18 + 2 * (23 + 2) + 4 + 2 * 15 + 8
    text(d, (x0 + 4, sy), src, F(SANS, 9), GREY)
    chip = "REPORTED"
    cw = d.textlength(chip, font=F(SANS_B, 9)) + 12
    d.rectangle([x0 + HW - cw - 4, sy - 1, x0 + HW - 4, sy + 12], fill=NAVY)
    text(d, (x0 + HW - cw // 2 - 4, sy + 1), chip, F(SANS_B, 9), (255, 255, 255), anchor="ma")

# ---------- cards ----------
d.rectangle([0, 462, W, 484], fill=INK)
text(d, (8, 467), "MORE OF THE DAY  \u2014  10 STORIES", F(SANS_B, 13), (255, 255, 255))

CARDS = [
    ("AMERICAS", (14, 107, 107), "BESSENT: NVIDIA ANSWERS", "Treasury wants answers.", "Reuters", "REPORTED"),
    ("FBI", (27, 58, 107), "FBI PROBES NCIC HACK", "NCIC database hacked.", "AP", "REPORTED"),
    ("WHITE HOUSE", (176, 141, 11), "TRUMP: IRAN STRIKES MAY RESUME", "May resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", (14, 107, 107), "US FUTURES JUMP 3%", "Holiday rally lifts 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", RED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", RED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice.", "ESPN", "REPORTED"),
    ("LEGAL", (107, 62, 160), "STATES SUE SPACEX", "Ten states sue over AI.", "AP", "REPORTED"),
    ("TECH", (27, 58, 107), "ANTHROPIC IPO: $107.3B", "Raised $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", (14, 107, 107), "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: 3 Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (107, 62, 160), "RUSSIAN NUCLEAR SATELLITE", "May carry a nuke.", "Reuters", "CLAIM"),
]
CW = 197
CGAP = 6
for i, (cat, ccol, head, body, src, chip) in enumerate(CARDS):
    r, c = divmod(i, 5)
    x0 = 8 + c * (CW + CGAP)
    y0 = 488 + r * 74
    d.rectangle([x0, y0, x0 + CW, y0 + 72], outline=(190, 185, 170), width=1)
    d.rectangle([x0, y0, x0 + CW, y0 + 15], fill=ccol)
    text(d, (x0 + 5, y0 + 2), cat, F(SANS_B, 10), (255, 255, 255))
    text(d, (x0 + CW - 5, y0 + 2), str(i + 1), F(SANS_B, 10), (255, 255, 255), anchor="ra")
    hf, hlines = fit_lines(d, head, [12, 11, 10], CW - 10, 2, SANS_B)
    yy = y0 + 18
    for ln in hlines:
        text(d, (x0 + 5, yy), ln, hf, INK)
        yy += hf.size + 1
    # body on its own row, below the actual headline lines
    by = y0 + 18 + len(hlines) * (hf.size + 1) + 1
    text(d, (x0 + 5, by), body, F(SANS, 10), (60, 60, 60))
    # source + chip on the bottom row of the card
    sy = y0 + 72 - 13
    text(d, (x0 + 5, sy), src, F(SANS, 9), GREY)
    cw = d.textlength(chip, font=F(SANS_B, 8)) + 10
    cfill = NAVY if chip == "REPORTED" else RED
    d.rectangle([x0 + CW - cw - 4, sy - 1, x0 + CW - 4, sy + 11], fill=cfill)
    text(d, (x0 + CW - cw // 2 - 4, sy + 1), chip, F(SANS_B, 8), (255, 255, 255), anchor="ma")

# ---------- bottom headers ----------
d.rectangle([0, 632, W, 654], fill=INK)
text(d, (8, 637), "WHERE IT HAPPENED", F(SANS_B, 13), (255, 255, 255))
text(d, (346, 637), "ALSO ON MONDAY", F(SANS_B, 13), (255, 255, 255))

# ---------- map ----------
MX0, MY0, MW, MH = 8, 660, 330, 190
d.rectangle([MX0, MY0, MX0 + MW, MY0 + MH], outline=(190, 185, 170), width=1, fill=(238, 240, 226))
# stylised continents
d.polygon([(MX0 + 18, MY0 + 30), (MX0 + 78, MY0 + 12), (MX0 + 118, MY0 + 26), (MX0 + 108, MY0 + 78),
           (MX0 + 82, MY0 + 132), (MX0 + 52, MY0 + 148), (MX0 + 26, MY0 + 108), (MX0 + 12, MY0 + 62)],
          fill=(196, 222, 178))
d.polygon([(MX0 + 150, MY0 + 22), (MX0 + 196, MY0 + 10), (MX0 + 226, MY0 + 30), (MX0 + 214, MY0 + 66),
           (MX0 + 182, MY0 + 76), (MX0 + 158, MY0 + 52)], fill=(196, 222, 178))
d.polygon([(MX0 + 236, MY0 + 18), (MX0 + 306, MY0 + 8), (MX0 + 322, MY0 + 34), (MX0 + 300, MY0 + 78),
           (MX0 + 262, MY0 + 92), (MX0 + 240, MY0 + 56)], fill=(196, 222, 178))
d.polygon([(MX0 + 96, MY0 + 128), (MX0 + 150, MY0 + 118), (MX0 + 168, MY0 + 142), (MX0 + 132, MY0 + 162),
           (MX0 + 100, MY0 + 152)], fill=(196, 222, 178))
PINS = {
    1: (286, 44), 2: (102, 140), 3: (268, 66), 4: (48, 92), 5: (74, 76),
    6: (196, 44), 7: (64, 108), 8: (26, 80), 9: (46, 124), 10: (80, 132),
    11: (212, 36), 12: (176, 30), 13: (300, 30),
}
for n, (px, py) in PINS.items():
    d.ellipse([MX0 + px - 8, MY0 + py - 8, MX0 + px + 8, MY0 + py + 8], fill=RED, outline=(255, 255, 255), width=1)
    text(d, (MX0 + px, MY0 + py - 5), str(n), F(SANS_B, 9), (255, 255, 255), anchor="ma")
text(d, (MX0 + 6, MY0 + MH - 34), "Pins 1-13: 1 Seoul \u00b7 2 Bridgetown \u00b7 3 Beijing", F(SANS, 9), (60, 60, 60))
text(d, (MX0 + 6, MY0 + MH - 23), "4 Washington \u00b7 5 New York \u00b7 6 Kyiv \u00b7 7 Chicago \u00b7 8 SF", F(SANS, 9), (60, 60, 60))
text(d, (MX0 + 6, MY0 + MH - 12), "9 Denver \u00b7 10 Austin \u00b7 11 Warsaw \u00b7 12 London \u00b7 13 Moscow", F(SANS, 9), (60, 60, 60))

# ---------- ALSO list ----------
ALSO = [
    "Paris: 100+ back 2% billionaire tax",
    "Manchester: 12,000 cleared",
    "Zelenskyy: 165 missiles in a week",
    "COP31: the day after Antalya pact rejected",
    "Benghazi: UN demands probe [CLAIM]",
    "Israel unity talks resume",
    "Gaza: two killed in Israeli strike",
    "West Bank settler attacks",
    "Iran war: no deal in sight",
    "Lebanon seizes 264 kg explosives",
    "Bahrain: strike hits plant, 2 hurt",
    "Sudan: defences down drones [CLAIM]",
    "DRC: fighting traps Ebola teams",
    "Bangladesh: Hasina jailed if she returns",
    "Seoul minister quits in exam row",
    "SK Telecom -7.3% as hype cools",
    "China eases margin rules",
    "Seoul readies 10T-won fund",
]
for i, item in enumerate(ALSO):
    col = i // 9
    row = i % 9
    ax = 346 + col * 340
    ay = 662 + row * 20
    num = 14 + i
    disp = item
    if "[CLAIM]" in item:
        disp = item.replace(" [CLAIM]", "")
        text(d, (ax, ay), f"{num}. {disp} ", F(SANS, 12), INK)
        wpre = d.textlength(f"{num}. {disp} ", font=F(SANS, 12))
        text(d, (ax + wpre, ay), "[CLAIM]", F(SANS_B, 11), RED)
    else:
        text(d, (ax, ay), f"{num}. {item}", F(SANS, 12), INK)

# ---------- DATE CHECK ----------
d.rectangle([8, 856, 1016, 928], outline=RED, width=2)
text(d, (16, 862), "DATE CHECK", F(SANS_B, 14), RED)
text(d, (1008, 862), "READ 23 NOV 2026, 23:59 UTC \u2014 STORIES DATED 23 NOV ONLY", F(SANS_B, 10), RED, anchor="ra")
text(d, (16, 884), "LEFT OUT \u2014 NOT 23 NOV:  Dems 258 seats (22 Nov)  \u00b7  Sparta II fire (22 Nov)  \u00b7  El Chapo (22 Nov)  \u00b7  EU\u2013Indonesia (21 Nov)  \u00b7  Nigeria boat (21 Nov)  \u00b7  ICJ Myanmar (19 Nov)",
     F(SANS, 11), INK)
text(d, (16, 904), "NOT YET \u2014 Dymer search continues (14 missing)  \u00b7  4 House races uncalled  \u00b7  COP32 venue not set  \u00b7  WHO evacuating trapped Ebola staff",
     F(SANS, 11), INK)

# ---------- footer ----------
text(d, (8, 938), "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 AFP \u00b7 Yonhap \u00b7 BBC \u00b7 WSJ \u00b7 ESPN \u00b7 Lowy Institute (Asia Power Index 2026).",
     F(SANS, 10), GREY)
text(d, (8, 954), "CHIPS: REPORTED = confirmed by wires.  CLAIM = one side's claim, not independently confirmed.  ONGOING = still developing.",
     F(SANS, 10), GREY)
text(d, (8, 970), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.",
     F(SANS, 10), GREY)
d.line([8, 988, 1016, 988], fill=GOLD, width=2)
text(d, (512, 996), "THE WORLD TODAY  \u2014  Monday 23 November 2026  \u00b7  31 stories  \u00b7  6 regions",
     F(SANS_B, 12), (150, 110, 0), anchor="ma")

img.save(OUT, optimize=True)
print("saved", OUT, os.path.getsize(OUT), "bytes")
