#!/usr/bin/env python3
"""WEDNESDAY, IN FULL — a one-page typographic broadsheet of the world's news
for Wednesday 25 November 2026, rendered with Pillow.

Editorial angle: NO SAFE DISTANCE. One sky, one sea — the war arrived in
a capital (a drone hits Riyadh's tallest tower), a shipping lane (a Russian
cargo ship hit in the Gulf of Finland, tankers mined off Hormuz) and NATO's
own skies (Russian missiles in Poland, AWACS sent). The Sunlit Crime-Noir
treatment: sun-scorched cream paper, a blazing red sun, hard diagonal
charcoal shadow, one red accent family, condensed editorial type.

The lead is a DRAWN scene, not text alone: the 385 m PIF Tower under a red
sun, smoke over its crown, a hard shadow cutting the panel — the picture a
reader sees in the first three seconds.

Every story comes from fresh web research done in this session (Reuters,
Bloomberg, AP, AFP, NYT, ESPNcricinfo, The Hindu, Fast Company, TechCrunch).
Items that broke before Wednesday carry an explicit day tag (TUE / MON);
Wednesday items are tagged WED. Claims that no outlet could verify are
labelled as claims, never stated as fact. The story count is computed from
the data tables below.
"""

import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (247, 237, 216)        # sun-scorched cream
SAND = (233, 211, 165)         # warm sand panel
SAND_EDGE = (214, 186, 132)    # sand panel border
INK = (28, 25, 22)             # charcoal ink
INK_SOFT = (88, 78, 64)        # soft charcoal for small print
RED = (198, 16, 46)            # the one red accent
RED_DARK = (148, 10, 32)       # red, darker shade (same family)
CREAM = (250, 246, 236)        # text on charcoal
SMOKE = (150, 140, 126)        # smoke grey
SKY = (242, 224, 186)          # pale sky inside the scene panel

# ---------------------------------------------------------------- geometry
W, H = 1024, 1024
MARGIN = 26
COL_W = 320                    # three-column width
GUT = 14                       # gutter between columns
COL_X = [MARGIN, MARGIN + COL_W + GUT, MARGIN + 2 * (COL_W + GUT)]

FONT_DIR = "/usr/share/fonts/truetype"


def _pick(*names):
    """Return the first font file that exists on disk."""
    for name in names:
        path = os.path.join(FONT_DIR, name)
        if os.path.exists(path):
            return path
    raise FileNotFoundError("none of %s found" % (names,))


F_TITLE = _pick("noto/NotoSans-CondensedBlack.ttf")
F_HEAD = _pick("noto/NotoSans-CondensedBold.ttf")
F_KICK = _pick("noto/NotoSans-CondensedBold.ttf")
F_BODY = _pick("noto/NotoSans-Regular.ttf")
F_MED = _pick("noto/NotoSans-Medium.ttf")


def _font(path, size):
    return ImageFont.truetype(path, size)


# ---------------------------------------------------------------- data
# Editorial banner: (big line, subline). The angle, before any story.
ANGLE_BIG = "NO SAFE DISTANCE"
ANGLE_SUB = ("One sky, one sea: the war arrived in a capital, "
             "a shipping lane and NATO's skies.")

# Lead: (kicker, headline, deck). Deck must wrap to at most 4 lines.
LEAD = (
    "LEAD  ·  RIYADH  ·  TUE",
    "DRONE HITS RIYADH'S TALLEST TOWER — 11 WOUNDED",
    "A Houthi drone struck the 385-metre PIF Tower, the Saudi capital's "
    "tallest, on Tuesday — the second hit on the tower in under a week. "
    "The Saudi-led coalition vowed a \"decisive\" response; the Houthis had "
    "not claimed the strike by evening.",
)

# Numbers strip: (big figure, caption)
NUMBERS = [
    ("11", "wounded in the Riyadh tower strike"),
    ("385", "metres — the PIF Tower, Riyadh's tallest"),
    ("3", "Russian missiles landed in Poland"),
    ("14", "AWACS aircraft in NATO's fleet"),
]

# Middle stories: (kicker with day tag, headline, deck <= 2 lines).
MIDDLE = [
    ("UKRAINE  ·  TUE",
     "ZELENSKIY: \u2018WE DID EVERYTHING RIGHT\u2019",
     "Kyiv confirmed the drone hit on the Russian ship Sparta II; Norway "
     "urged caution."),
    ("POLAND  ·  MON",
     "NATO SENDS ITS EYES TO POLAND",
     "An AWACS aircraft goes to Poland after three Russian Kh-101 missiles "
     "landed there on Friday."),
    ("MOSCOW  ·  TUE",
     "PUTIN: RETALIATION \u2018INEVITABLE\u2019",
     "After Ukraine struck Russian oil plants; both sides traded "
     "accusations at the UN."),
    ("HORMUZ  ·  TUE",
     "IRAN CLAIMS A FOURTH TANKER MINED",
     "The IRGC Navy says a tanker hit a mine on Tuesday; five claimed in "
     "two days. Unverified."),
    ("WASHINGTON  ·  TUE",
     "CIA AND ODNI BREACHED",
     "Hackers hit an unclassified intelligence network; no classified "
     "systems were touched."),
    ("PARIS  ·  TUE",
     "SARKOZY AND BRUNI ORDERED TO TRIAL",
     "A witness-tampering case over the 2007 campaign goes to court; 11 "
     "defendants face 10 years."),
    ("MARKETS  ·  TUE",
     "NVIDIA GIVES BACK A THIRD OF ITS SURGE",
     "Shares fell about 7% on Tuesday after Monday's 31% jump; lawmakers "
     "questioned the return."),
    ("MARKETS  ·  TUE",
     "ANTHROPIC SLIPS BELOW ITS $83 IPO PRICE",
     "Down about 6.5% four days after a $111.50 debut — the largest IPO "
     "ever, at $81.3 billion."),
    ("MARKETS  ·  TUE",
     "DELL DOUBLES SALES ON AI SERVERS",
     "Revenue hit $54.9bn in Q3; the AI-server forecast rose to $78bn, "
     "with a $25bn buyback."),
]

# One-line grid: (tag, line). Each must wrap to at most 2 lines.
LINES = [
    ("ADEN, TUE", "Houthis are 60 km from Aden but will not take the city, "
     "Yemen's military says."),
    ("TARIFFS, TUE", "Trump readies new Section 301 tariffs; China, the EU "
     "and 14 others are in view."),
    ("GIULIANI, TUE", "Trump awards Rudy Giuliani the Presidential Medal of "
     "Freedom."),
    ("TURKEYS, TUE", "Freedom and Feathers are pardoned on Thanksgiving "
     "eve."),
    ("SWEDEN, WED", "Parliament votes today on whether Kristersson stays "
     "prime minister."),
    ("NEPAL, TUE", "A 5.6 quake shakes Taplejung near the Tibet border; no "
     "casualties are reported."),
    ("INDIA, WED", "BJP and Akali Dal reunite for the 2027 Punjab polls "
     "after a six-year split."),
    ("FORT HOOD, TUE", "Hasan seeks a stay of execution set for next week, "
     "court records show."),
    ("O'HARE, TUE", "A radar fault delays flights at Chicago O'Hare, the "
     "FAA says."),
    ("GAZA, TUE", "A US envoy is 'not certain' military aid to Israel ends "
     "this year as promised."),
    ("IRAQ, TUE", "Baghdad is ordered to run Kurdish oilfields; the Kurds "
     "reject the move."),
    ("WOMEN, WED", "Today is the International Day for the Elimination of "
     "Violence against Women."),
    ("SENSEX, TUE", "Sensex drops 1,484 points; the Nifty slips below "
     "25,400."),
    ("GERMANY, TUE", "Modi holds talks with Chancellor Merz on the "
     "India–Germany partnership."),
    ("HORMUZ, TUE", "Crude shipments through the strait appear down since "
     "early November."),
    ("ZIMBABWE, TUE", "A Zimbabwean is convicted in South Africa of trying "
     "to fight in Ukraine."),
    ("POLAND, TUE", "Prosecutors say the missiles were made in Dubna, "
     "Russia, in Oct–Nov 2026."),
    ("UK, TUE", "Ministers consult the public on changing the age of "
     "consent."),
    ("UK, TUE", "Nuclear test veterans will get the 'full truth', PM "
     "Burnham says."),
    ("SARKOZY, TUE", "The appeal verdict in the Libya financing case is due "
     "on 30 November."),
    ("NVIDIA, TUE", "Huang is due to testify to the Senate Banking "
     "Committee on 3 December."),
    ("MAN UTD, TUE", "Pochettino fumes at the handling of Yoro's red "
     "card."),
    ("HP, TUE", "Shares jump 14% after hours; Emma Walmsley is named chief "
     "executive."),
    ("KYIV, TUE", "Kyiv says the Sparta II was carrying weapons; Bloomberg "
     "could not verify the claim."),
]

# Sport strip: terse one-liners, at most 2 lines each.
SPORT = [
    "CRICKET — Donald 85 (32) and Salt 58 (30) power England past "
    "Australia by 8 wickets; 185 chased in 13.1 overs.",
    "CRICKET — New Zealand hold India to a draw in the first Test in "
    "Wellington.",
    "CRICKET — Sooryavanshi smashes the fastest List A double hundred.",
]

FOOTER = ("TUE = Tuesday 24 Nov  ·  MON = Monday 23 Nov  ·  WED = today, 25 Nov  ·  "
          "Sources: Reuters, Bloomberg, AP, AFP, NYT, ESPNcricinfo, The Hindu, "
          "Fast Company. Claims are labelled as claims.")

SCENE_CAPTION = "The 385 m PIF Tower, Riyadh — drawn scene"


# ---------------------------------------------------------------- helpers
def wrap_text(draw, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width`."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # a single over-long word is hard-split by characters
            while draw.textlength(word, font=font) > width:
                cut = len(word)
                while cut > 1 and draw.textlength(word[:cut], font=font) > width:
                    cut -= 1
                lines.append(word[:cut])
                word = word[cut:]
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_rule(draw, x0, x1, y, width=2, colour=INK):
    draw.line([(x0, y), (x1, y)], fill=colour, width=width)


def section_head(draw, y, title):
    """Red square + condensed title + hairline rule. Returns next y."""
    draw.rectangle([MARGIN, y + 3, MARGIN + 12, y + 15], fill=RED)
    draw.text((MARGIN + 20, y), title, font=_font(F_HEAD, 19), fill=INK)
    draw_rule(draw, MARGIN + 20 + draw.textlength(title, font=_font(F_HEAD, 19)) + 12,
              W - MARGIN, y + 9, width=1)
    return y + 24


def story_block(draw, x, y, width, kicker, headline, deck, max_head_lines=2,
                max_deck_lines=2):
    """One middle story: red kicker, condensed headline, short deck.

    Raises loudly if anything overflows its line budget.
    """
    kick_f = _font(F_KICK, 12)
    head_f = _font(F_HEAD, 19)
    deck_f = _font(F_BODY, 12)
    draw.text((x, y), kicker, font=kick_f, fill=RED)
    y += 15
    head_lines = wrap_text(draw, headline, head_f, width)
    if len(head_lines) > max_head_lines:
        raise AssertionError("headline overflows: %r -> %d lines"
                             % (headline, len(head_lines)))
    for line in head_lines:
        draw.text((x, y), line, font=head_f, fill=INK)
        y += 21
    deck_lines = wrap_text(draw, deck, deck_f, width)
    if len(deck_lines) > max_deck_lines:
        raise AssertionError("deck overflows: %r -> %d lines"
                             % (deck, len(deck_lines)))
    for line in deck_lines:
        draw.text((x, y), line, font=deck_f, fill=INK_SOFT)
        y += 14
    return y


def draw_tower_scene(draw, x0, y0, x1, y1):
    """Drawn scene: the PIF Tower under a blazing sun, smoke over its
    crown, a hard diagonal shadow across the panel. Pure vector shapes.
    The tower is drawn AFTER the shadow, with a cream outline, so the
    charcoal shaft never merges into the charcoal shadow."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY, outline=SAND_EDGE, width=1)
    # blazing red sun, top right
    sun_cx, sun_cy, sun_r = x1 - 42, y0 + 34, 26
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r,
                  sun_cx + sun_r, sun_cy + sun_r], fill=RED)
    # hard diagonal shadow band first, so the tower can stand on top of it
    draw.polygon([(x0, y1), (x0 + 120, y1), (x0 + 260, y0 + 62),
                  (x0 + 200, y0 + 62)], fill=INK)
    # low skyline blocks, left and right of the tower
    base_y = y1 - 14
    draw.rectangle([x0 + 8, base_y - 26, x0 + 62, base_y], fill=INK)
    draw.rectangle([x0 + 178, base_y - 38, x0 + 224, base_y], fill=INK)
    draw.rectangle([x0 + 234, base_y - 18, x0 + 268, base_y], fill=INK)
    # the tower: tapered shaft with setback crown, cream-outlined
    top_y = y0 + 20
    draw.polygon([(x0 + 84, base_y), (x0 + 98, top_y + 26),
                  (x0 + 138, top_y + 26), (x0 + 152, base_y)],
                 fill=INK, outline=CREAM, width=2)
    draw.rectangle([x0 + 102, top_y + 12, x0 + 134, top_y + 28],
                   fill=INK, outline=CREAM, width=2)
    draw.rectangle([x0 + 108, top_y, x0 + 128, top_y + 14],
                   fill=INK, outline=CREAM, width=2)
    # lit windows: thin cream slits down the shaft
    for wy in range(top_y + 36, base_y - 6, 12):
        draw.line([(x0 + 106, wy), (x0 + 130, wy)], fill=CREAM, width=1)
    # red wound: a small gash where the drone struck, upper shaft
    draw.polygon([(x0 + 98, top_y + 46), (x0 + 118, top_y + 42),
                  (x0 + 110, top_y + 58)], fill=RED)
    # smoke puffs over the tower crown
    smoke_cx = x0 + 118
    for dx, dy, r in ((-14, -5, 8), (0, -10, 10), (14, -5, 8), (5, 2, 7)):
        draw.ellipse([smoke_cx + dx - r, y0 + 16 + dy - r,
                      smoke_cx + dx + r, y0 + 16 + dy + r], fill=SMOKE)
    # caption bar: thin red rule + caption text under the panel
    draw_rule(draw, x0, x1, y1 + 4, width=2, colour=RED)
    draw.text((x0, y1 + 8), SCENE_CAPTION, font=_font(F_BODY, 10),
              fill=INK_SOFT)


# ---------------------------------------------------------------- render
def render(out_path):
    story_total = 1 + len(MIDDLE) + len(LINES) + len(SPORT)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- top red bar -----------------------------------------------------
    draw.rectangle([0, 0, W, 6], fill=RED)

    # --- masthead: sun disc cut by a hard diagonal shadow ----------------
    sun_cx, sun_cy, sun_r = 912, 74, 50
    draw.ellipse([sun_cx - sun_r, sun_cy - sun_r,
                  sun_cx + sun_r, sun_cy + sun_r], fill=RED)
    draw.polygon([(848, 0), (904, 0), (996, 142), (940, 142)], fill=INK)

    draw.text((MARGIN, 14), "THE WORLD IN ONE PAGE",
              font=_font(F_KICK, 14), fill=RED)
    draw.text((MARGIN, 30), "WEDNESDAY, IN FULL",
              font=_font(F_TITLE, 60), fill=INK)
    dateline = ("WEDNESDAY 25 NOVEMBER 2026  ·  %d STORIES  ·  "
                "THE DAY'S WORLD NEWS" % story_total)
    draw.text((MARGIN, 102), dateline, font=_font(F_HEAD, 17), fill=INK_SOFT)
    draw_rule(draw, MARGIN, W - MARGIN, 126, width=2)

    # --- editorial angle -------------------------------------------------
    angle_y = 136
    draw.text((MARGIN, angle_y), ANGLE_BIG, font=_font(F_TITLE, 30), fill=RED)
    sub_w = draw.textlength(ANGLE_SUB, font=_font(F_BODY, 15))
    draw.text((MARGIN, angle_y + 36), ANGLE_SUB, font=_font(F_BODY, 15),
              fill=INK)
    if sub_w > W - 2 * MARGIN:
        raise AssertionError("angle subline too wide: %d" % sub_w)
    draw_rule(draw, MARGIN, W - MARGIN, angle_y + 58, width=1, colour=SAND_EDGE)

    # --- lead ------------------------------------------------------------
    lead_y = 200
    lead_w = 600
    draw.text((MARGIN, lead_y), LEAD[0], font=_font(F_KICK, 13), fill=RED)
    y = lead_y + 18
    head_lines = wrap_text(draw, LEAD[1], _font(F_TITLE, 32), lead_w)
    if len(head_lines) > 2:
        raise AssertionError("lead headline overflows: %d lines" % len(head_lines))
    for line in head_lines:
        draw.text((MARGIN, y), line, font=_font(F_TITLE, 32), fill=INK)
        y += 36
    y += 2
    deck_lines = wrap_text(draw, LEAD[2], _font(F_BODY, 14), lead_w)
    if len(deck_lines) > 4:
        raise AssertionError("lead deck overflows: %d lines" % len(deck_lines))
    for line in deck_lines:
        draw.text((MARGIN, y), line, font=_font(F_BODY, 14), fill=INK)
        y += 17
    lead_bottom = y
    if lead_bottom > 348:
        raise AssertionError("lead block too tall: bottom %d" % lead_bottom)

    # drawn scene panel: right of the lead text
    sx0, sx1 = 660, W - MARGIN
    sy0, sy1 = lead_y, 330
    draw_tower_scene(draw, sx0, sy0, sx1, sy1)

    # --- numbers strip: horizontal sand band ------------------------------
    band_y = 352
    draw.rectangle([MARGIN, band_y, W - MARGIN, band_y + 48], fill=SAND,
                   outline=SAND_EDGE, width=1)
    cell_w = (W - 2 * MARGIN) // 4
    for i, (big, caption) in enumerate(NUMBERS):
        cx = MARGIN + i * cell_w
        if i > 0:
            draw.line([(cx, band_y + 8), (cx, band_y + 40)], fill=SAND_EDGE,
                      width=1)
        draw.text((cx + 12, band_y + 6), big, font=_font(F_TITLE, 24), fill=INK)
        cap_lines = wrap_text(draw, caption, _font(F_BODY, 11),
                              cell_w - 92)
        if len(cap_lines) > 2:
            raise AssertionError("number caption overflows: %r" % caption)
        cy = band_y + 10
        for cline in cap_lines:
            draw.text((cx + 78, cy), cline, font=_font(F_BODY, 11),
                      fill=INK_SOFT)
            cy += 13

    # --- middle stories: three columns, three each -----------------------
    y = section_head(draw, 414, "THE DAY'S BIG STORIES")
    if len(MIDDLE) != 9:
        raise AssertionError("expected 9 middle stories, got %d" % len(MIDDLE))
    col_bottoms = []
    for ci in range(3):
        cy = y
        for si in range(3):
            kicker, headline, deck = MIDDLE[ci * 3 + si]
            cy = story_block(draw, COL_X[ci], cy, COL_W, kicker, headline, deck)
            cy += 8
        col_bottoms.append(cy)
    mid_bottom = max(col_bottoms)
    if mid_bottom > 700:
        raise AssertionError("middle section too tall: bottom %d" % mid_bottom)

    # --- one-line grid: three columns, eight rows ------------------------
    y = section_head(draw, mid_bottom + 6, "THE DAY IN LINES")
    if len(LINES) != 24:
        raise AssertionError("expected 24 line items, got %d" % len(LINES))
    line_f = _font(F_BODY, 11)
    tag_f = _font(F_KICK, 11)
    row_h = 25
    for ri in range(8):
        for ci in range(3):
            tag, line = LINES[ri * 3 + ci]
            x = COL_X[ci]
            draw.rectangle([x, y + 4, x + 7, y + 11], fill=RED)
            tag_w = draw.textlength(tag + "  ", font=tag_f)
            draw.text((x + 12, y), tag, font=tag_f, fill=RED_DARK)
            wrapped = wrap_text(draw, line, line_f, COL_W - 12 - tag_w)
            if len(wrapped) > 2:
                raise AssertionError("line item overflows: %r -> %d lines"
                                     % (line, len(wrapped)))
            ly = y
            for wline in wrapped:
                draw.text((x + 12 + tag_w, ly), wline, font=line_f, fill=INK)
                ly += 12
        y += row_h
    if y > 940:
        raise AssertionError("lines section too tall: bottom %d" % y)

    # --- sport strip: charcoal band --------------------------------------
    band_y = y + 6
    draw.rectangle([MARGIN, band_y, W - MARGIN, band_y + 40], fill=INK)
    sport_f = _font(F_MED, 11)
    for ci, item in enumerate(SPORT):
        wrapped = wrap_text(draw, item, sport_f, COL_W - 8)
        if len(wrapped) > 2:
            raise AssertionError("sport item overflows: %r" % item)
        sy = band_y + 6
        for wline in wrapped:
            draw.text((COL_X[ci], sy), wline, font=sport_f, fill=CREAM)
            sy += 14

    # --- footer ----------------------------------------------------------
    foot_f = _font(F_BODY, 10)
    foot_lines = wrap_text(draw, FOOTER, foot_f, W - 2 * MARGIN)
    if len(foot_lines) > 2:
        raise AssertionError("footer too long: %d lines" % len(foot_lines))
    fy = band_y + 48
    for fline in foot_lines:
        fw = draw.textlength(fline, font=foot_f)
        draw.text(((W - fw) / 2, fy), fline, font=foot_f, fill=INK_SOFT)
        fy += 13
    page_bottom = fy
    if page_bottom > H - 8:
        raise AssertionError("page bottom out of bounds: %d" % page_bottom)
    # bottom red bar, mirroring the top bar
    draw.rectangle([0, H - 6, W, H], fill=RED)

    img.save(out_path, "PNG")
    size = os.path.getsize(out_path)
    digest = hashlib.sha256(open(out_path, "rb").read()).hexdigest()
    print("rendered %s" % out_path)
    print("stories: lead 1 + middle %d + lines %d + sport %d = %d"
          % (len(MIDDLE), len(LINES), len(SPORT), story_total))
    print("sections: lead bottom %d, middle bottom %d, lines bottom %d, "
          "sport band %d-%d, page bottom %d"
          % (lead_bottom, mid_bottom, y, band_y, band_y + 40, page_bottom))
    print("size: %d bytes (limit 1048576), sha256: %s" % (size, digest))
    if size > 1048576:
        raise AssertionError("entry.png exceeds 1 MiB")
    return story_total, size, digest


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    render(target)
