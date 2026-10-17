"""Generate Luffy 64x128 walk sheet (rows: down, left, right, up; 4 frames each).
Run: python tools/make_luffy_sprites.py  -> assets/sprites/player/player_sheet.png
Shading is automatic: base-colour pixels with empty right/below neighbour get the shade
colour (top-left light), so the right-facing row is the left one flipped before shading.
"""
from PIL import Image

W, H = 16, 32
K = (0, 0, 0, 255)
SKIN, STRAW, RED, BLUE = (255, 205, 160, 255), (240, 200, 90, 255), (215, 50, 50, 255), (55, 100, 210, 255)
SHADE = {SKIN: (222, 160, 115, 255), STRAW: (200, 150, 55, 255), RED: (160, 30, 38, 255), BLUE: (35, 65, 155, 255)}
HAIR, SAND, BAND, SCAR, EYE = (45, 35, 50, 255), (135, 85, 50, 255), (190, 35, 40, 255), (170, 50, 50, 255), (30, 20, 30, 255)


class Cell:
    def __init__(s):
        s.p = {}

    def r(s, x0, y0, x1, y1, c, oy=0):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.p[(x, y + oy)] = c

    def dot(s, x, y, c, oy=0):
        s.p[(x, y + oy)] = c

    def image(s, flip=False):
        src = {(W - 1 - x if flip else x, y): c for (x, y), c in s.p.items()}
        p = dict(src)
        for (x, y), c in src.items():  # shade pass
            if c in SHADE and ((x + 1, y) not in src or (x, y + 1) not in src):
                p[(x, y)] = SHADE[c]
        for (x, y) in list(p):  # outline pass
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (x + dx, y + dy)
                if q not in p and 0 <= q[0] < W and 0 <= q[1] < H:
                    p[q] = K
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for (x, y), c in p.items():
            if 0 <= x < W and 0 <= y < H:
                im.putpixel((x, y), c)
        return im


def hat(c, oy, x0=4, x1=11, bx0=2, bx1=13):
    c.r(x0 + 1, 1, x1 - 1, 1, STRAW, oy)
    c.r(x0, 2, x1, 4, STRAW, oy)
    c.r(x0, 5, x1, 5, BAND, oy)
    c.r(bx0, 6, bx1, 7, STRAW, oy)


def legs_front(c, ph):
    # ph 0/2 contact (one leg forward), 1/3 passing
    if ph in (1, 3):
        for x0 in (5, 9):
            c.r(x0, 28, x0 + 1, 29, SKIN); c.r(x0, 30, x0 + 1, 30, SAND)
        return
    fwd, back = (5, 9) if ph == 0 else (9, 5)
    c.r(fwd, 29, fwd + 1, 29, SKIN); c.r(fwd, 30, fwd + 1, 30, SAND)
    c.r(back, 29, back + 1, 29, SAND)


def front(ph, back=False):
    c = Cell()
    oy = 1 if ph in (0, 2) else 0
    legs_front(c, ph)
    c.r(5, 24, 10, 27, BLUE, oy)
    swing = {0: (0, 1), 1: (0, 0), 2: (1, 0), 3: (0, 0)}[ph]  # (left arm dy, right arm dy)
    c.r(3, 16 + swing[0], 4, 22 + swing[0], SKIN, oy)
    c.r(11, 16 + swing[1], 12, 22 + swing[1], SKIN, oy)
    if back:
        c.r(5, 15, 10, 23, RED, oy)
        c.r(4, 8, 11, 13, HAIR, oy); c.r(6, 14, 9, 14, SKIN, oy)
    else:
        c.r(5, 15, 10, 23, RED, oy); c.r(7, 15, 8, 23, SKIN, oy)
        c.r(4, 8, 11, 14, SKIN, oy)
        c.r(4, 8, 11, 8, HAIR, oy); c.r(4, 9, 4, 10, HAIR, oy); c.r(11, 9, 11, 10, HAIR, oy)
        c.dot(5, 11, EYE, oy); c.dot(10, 11, EYE, oy); c.dot(5, 12, SCAR, oy)
        c.r(7, 13, 8, 13, SCAR, oy)
    hat(c, oy)
    return c


def side(ph):
    c = Cell()
    oy = 1 if ph in (0, 2) else 0
    # legs: 2-wide, top at hip, foot offset by stride
    off = {0: (-2, 2), 1: (0, 0), 2: (2, -2), 3: (0, 0)}[ph]
    for o, hx in zip(off, (6, 8)):
        top = 28 + oy
        c.r(hx, top, hx + 1, 29, SKIN)
        c.r(hx + o, 30, hx + o + 1, 30, SAND)
        if o:
            c.r(hx + o // 2, 29, hx + o // 2 + 1, 29, SKIN)
    ax = {0: (5, 9), 1: (7, 7), 2: (9, 5), 3: (7, 7)}[ph]
    c.r(ax[1], 16, ax[1] + 1, 22, SKIN, oy)  # back arm
    c.r(5, 24, 10, 27, BLUE, oy)
    c.r(5, 15, 10, 23, RED, oy)
    c.r(5, 15, 5, 23, SKIN, oy)  # chest edge
    c.r(ax[0], 16, ax[0] + 1, 22, SKIN, oy)  # front arm
    c.r(4, 8, 11, 14, SKIN, oy)
    c.r(4, 8, 11, 8, HAIR, oy); c.r(9, 9, 11, 12, HAIR, oy)
    c.dot(3, 11, SKIN, oy)
    c.dot(5, 10, EYE, oy); c.dot(5, 11, SCAR, oy); c.r(4, 13, 5, 13, SCAR, oy)
    hat(c, oy, 4, 11, 1, 13)
    return c


def build():
    sheet = Image.new("RGBA", (W * 4, H * 4), (0, 0, 0, 0))
    for ph in range(4):
        f, sd, b = front(ph), side(ph), front(ph, back=True)
        sheet.paste(f.image(), (ph * W, 0))
        sheet.paste(sd.image(), (ph * W, H))
        sheet.paste(sd.image(flip=True), (ph * W, 2 * H))
        sheet.paste(b.image(), (ph * W, 3 * H))
    return sheet


if __name__ == "__main__":
    s = build()
    s.save("assets/sprites/player/player_sheet.png")
    s.resize((s.width * 6, s.height * 6), Image.NEAREST).save("tools/_preview.png")
    print(s.size)
