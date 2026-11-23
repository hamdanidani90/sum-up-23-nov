#!/usr/bin/env python3
"""
Sum up 23 November 2026's world news in one image.
Stdlib only. Deterministic PNG, 1024x1024, written to /output/entry.png
(or output/entry.png next to this file when /output does not exist).
Run: python3 main.py [optional-output-path]
"""
import os
import struct
import sys
import zlib

WIDTH = 1024
HEIGHT = 1024

# 5x7 bitmap font. Only uppercase + digits + punctuation are needed;
# all text is rendered upper-cased.
FONT = {
    'A': ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    'B': ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    'C': ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    'D': ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    'E': ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    'F': ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    'G': ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    'H': ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    'I': ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    'J': ["00111", "00010", "00010", "00010", "00010", "10010", "01100"],
    'K': ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    'L': ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    'M': ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    'N': ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    'O': ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    'P': ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    'Q': ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    'R': ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    'S': ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    'T': ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    'U': ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    'V': ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    'W': ["10001", "10001", "10001", "10101", "10101", "11011", "10001"],
    'X': ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    'Y': ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    'Z': ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    '0': ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    '1': ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    '2': ["01110", "10001", "00001", "00110", "01000", "10000", "11111"],
    '3': ["11111", "00010", "00100", "00010", "00001", "10001", "01110"],
    '4': ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    '5': ["11111", "10000", "11110", "00001", "00001", "10001", "01110"],
    '6': ["00110", "01000", "10000", "11110", "10001", "10001", "01110"],
    '7': ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    '8': ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    '9': ["01110", "10001", "10001", "01111", "00001", "00010", "01100"],
    ' ': ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    '.': ["00000", "00000", "00000", "00000", "00000", "01100", "01100"],
    ',': ["00000", "00000", "00000", "00000", "01100", "00100", "01000"],
    ':': ["00000", "01100", "01100", "00000", "01100", "01100", "00000"],
    ';': ["00000", "01100", "01100", "00000", "01100", "00100", "01000"],
    '!': ["00100", "00100", "00100", "00100", "00100", "00000", "00100"],
    '?': ["01110", "10001", "00001", "00110", "00100", "00000", "00100"],
    "'": ["00100", "00100", "01000", "00000", "00000", "00000", "00000"],
    '-': ["00000", "00000", "00000", "01110", "00000", "00000", "00000"],
    '/': ["00001", "00010", "00010", "00100", "01000", "01000", "10000"],
    '%': ["11001", "11010", "00010", "00100", "01000", "01011", "10011"],
    '+': ["00000", "00100", "00100", "11111", "00100", "00100", "00000"],
    '&': ["01100", "10010", "10100", "01000", "10101", "10010", "01101"],
    '$': ["00100", "01111", "10100", "01110", "00101", "11110", "00100"],
    '(': ["00010", "00100", "01000", "01000", "01000", "00100", "00010"],
    ')': ["01000", "00100", "00010", "00010", "00010", "00100", "01000"],
    '\u2022': ["00000", "00000", "01100", "01100", "01100", "00000", "00000"],
}

# Stories verified from UN News, AP, CNN, Reuters, Al Jazeera, Just Security
# on 23 Nov 2026. Wording is attributed where a claim is contested.
STORIES = [
    {
        "cat": "CLIMATE  •  ANTALYA",
        "color": (27, 122, 77),
        "head": "COP31 ENDS WITH NO DEAL",
        "body": "UN climate talks in Antalya closed after two weeks with no overall pact. The draft omitted fossil fuels, and the EU rejected it. The UN chief called it deeply disappointing. It was the longest COP ever.",
    },
    {
        "cat": "WAR  •  UKRAINE - LIBYA",
        "color": (29, 78, 216),
        "head": "UKRAINE HITS RUSSIAN SHIPS IN LIBYA",
        "body": "President Zelenskyy said on Monday that seven Ukrainian sea drones sank the Russian corvette Merkury in Benghazi and hit the cargo ship MV Angara. A Ka-27 helicopter was destroyed. Libya said at least 10 people were wounded.",
    },
    {
        "cat": "MARKETS  •  ASIA",
        "color": (194, 65, 12),
        "head": "ASIAN CHIP STOCKS SLIDE",
        "body": "South Korea's Kospi fell as much as 5.8% on Monday before closing down 3.3%. Samsung fell 3.1% and SK Hynix 2.5% after a Wall Street rout driven by doubts over AI spending.",
    },
    {
        "cat": "MIDDLE EAST  •  IRAN",
        "color": (185, 28, 28),
        "head": "IRAN STRIKES WIDEN; TANKERS HIT",
        "body": "President Trump said on Monday that Iran wants a deal but not one acceptable to him. Iranian attacks hit a civilian site in Bahrain, injuring two, and at least three tankers were attacked in the Strait of Hormuz.",
    },
    {
        "cat": "TRAVEL  •  USA",
        "color": (15, 118, 110),
        "head": "DELTA OUTAGE DELAYS 1,600 FLIGHTS",
        "body": "A weight-and-balance system outage delayed more than 1,600 Delta flights to and from Atlanta as Thanksgiving travel began. About 49% of Delta flights on Sunday were delayed by more than 15 minutes.",
    },
    {
        "cat": "LEBANON  •  CEASEFIRE",
        "color": (109, 40, 217),
        "head": "LEBANESE VILLAGERS RETURN HOME",
        "body": "Villagers began returning to destroyed homes in southern Lebanon after an Israeli military pullback and the deployment of Lebanese Army forces under a pilot ceasefire arrangement.",
    },
]


def clean(text):
    return (
        text.replace("\u2019", "'")
        .replace("\u2018", "'")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .upper()
    )


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def text(self, x, y, s, scale, color):
        s = clean(s)
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT['?'])
            for r in range(7):
                row = glyph[r]
                for c in range(5):
                    if row[c] == '1':
                        for dy in range(scale):
                            for dx in range(scale):
                                self.set(cx + c * scale + dx, y + r * scale + dy, color)
            cx += 6 * scale
        return cx

    def text_width(self, s, scale):
        return len(clean(s)) * 6 * scale - scale


def wrap(text, max_chars):
    words = clean(text).split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_card(cv, x, y, w, h, story):
    # card background + border
    cv.rect(x, y, w, h, (255, 255, 255))
    cv.rect(x, y, w, 2, (217, 210, 197))
    cv.rect(x, y + h - 2, w, 2, (217, 210, 197))
    cv.rect(x, y, 2, h, (217, 210, 197))
    cv.rect(x + w - 2, y, 2, h, (217, 210, 197))
    # colour bar
    cv.rect(x, y, w, 8, story["color"])
    # category
    cv.text(x + 16, y + 20, story["cat"], 2, story["color"])
    # headline, max 2 lines
    head_lines = wrap(story["head"], 25)
    hy = y + 46
    for line in head_lines[:2]:
        cv.text(x + 16, hy, line, 3, (26, 26, 26))
        hy += 24
    # body, max 7 lines
    body_lines = wrap(story["body"], 36)
    by = hy + 10
    for line in body_lines[:7]:
        cv.text(x + 16, by, line, 2, (58, 58, 58))
        by += 18


def build_image():
    cv = Canvas(WIDTH, HEIGHT, (247, 243, 236))
    # header
    cv.rect(0, 0, WIDTH, 148, (16, 42, 67))
    cv.rect(0, 148, WIDTH, 6, (201, 162, 39))
    cv.text(32, 22, "THE WORLD TODAY", 5, (255, 255, 255))
    cv.text(32, 70, "MONDAY, 23 NOVEMBER 2026", 3, (242, 217, 140))
    cv.text(32, 108, "WORLD NEWS IN ONE IMAGE  •  6 STORIES", 2, (203, 213, 225))
    # info strip
    cv.text(32, 168, "CLIMATE  •  WAR  •  MARKETS  •  MIDDLE EAST  •  TRAVEL  •  LEBANON", 2, (90, 90, 90))
    # grid 2 x 3
    card_w = 472
    card_h = 250
    xs = [32, 520]
    ys = [200, 466, 732]
    idx = 0
    for r in range(3):
        for c in range(2):
            draw_card(cv, xs[c], ys[r], card_w, card_h, STORIES[idx])
            idx += 1
    # footer
    cv.text(32, 996, "SOURCES: UN NEWS  •  AP  •  CNN  •  REUTERS  •  AL JAZEERA", 2, (90, 90, 90))
    return cv


def png_bytes(cv):
    raw = bytearray()
    stride = WIDTH * 3
    for y in range(HEIGHT):
        raw.append(0)  # filter: None
        raw += cv.px[y * stride:(y + 1) * stride]

    def chunk(ctype, data):
        c = struct.pack(">I", len(data)) + ctype + data
        c += struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
        return c

    ihdr = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )


def main():
    out = None
    if len(sys.argv) > 1:
        out = sys.argv[1]
    elif os.path.isdir("/output"):
        out = "/output/entry.png"
    else:
        here = os.path.dirname(os.path.abspath(__file__))
        out = os.path.join(here, "output", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    data = png_bytes(build_image())
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))


if __name__ == "__main__":
    main()
