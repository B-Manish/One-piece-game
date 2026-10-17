"""Child Luffy 64x128 walk sheet (rows: down, left, right, up). Reuses Cell/shading of make_luffy_sprites.
Run from project root: python tools/make_child_luffy_sprites.py <out.png>
"""
import sys
sys.path.insert(0, "tools")
import make_luffy_sprites as m
from PIL import Image

W, H = m.W, m.H
SKIN, HAIR, SAND, EYE = m.SKIN, m.HAIR, m.SAND, m.EYE
WHITE, PURPLE, BLUE, CUFF = (245, 245, 245, 255), (110, 70, 150, 255), m.BLUE, (150, 190, 235, 255)
TEETH, MOUTH, RED = (252, 252, 252, 255), (120, 30, 35, 255), m.RED
m.SHADE.update({WHITE: (200, 205, 225, 255), PURPLE: (75, 45, 105, 255), CUFF: (105, 145, 205, 255)})
Cell = m.Cell


def spikes(c, oy):
    for x in (4, 7, 10):
        c.dot(x, 8, HAIR, oy)


def legs(c, ph):
    if ph in (1, 3):
        for x in (5, 9):
            c.r(x, 27, x + 1, 29, SKIN); c.r(x, 30, x + 1, 30, SAND)
        return
    fwd, back = (5, 9) if ph == 0 else (9, 5)
    c.r(fwd, 27, fwd + 1, 29, SKIN); c.r(fwd, 30, fwd + 1, 30, SAND)
    c.r(back, 27, back + 1, 28, SKIN)


def shorts(c, oy, x0=4, x1=11):
    c.r(x0, 24, x1, 25, BLUE, oy); c.r(x0, 26, x1, 26, CUFF, oy)


def front(ph, back=False):
    c = Cell()
    oy = 1 if ph in (0, 2) else 0
    legs(c, ph)
    shorts(c, oy)
    sw = {0: (0, 1), 1: (0, 0), 2: (1, 0), 3: (0, 0)}[ph]
    for x0, d in ((2, sw[0]), (12, sw[1])):
        c.r(x0, 18 + d, x0 + 1, 19 + d, WHITE, oy); c.r(x0, 20 + d, x0 + 1, 20 + d, PURPLE, oy)
        c.r(x0, 21 + d, x0 + 1, 22 + d, SKIN, oy)
    c.r(4, 18, 11, 23, WHITE, oy)
    if back:
        c.r(7, 18, 8, 18, PURPLE, oy)
        c.r(3, 9, 12, 16, HAIR, oy); c.r(5, 17, 10, 17, SKIN, oy)
    else:
        c.r(7, 18, 8, 18, PURPLE, oy); c.r(7, 21, 8, 21, RED, oy)
        c.r(3, 11, 12, 17, SKIN, oy)
        c.r(3, 9, 12, 10, HAIR, oy); c.r(3, 11, 4, 11, HAIR, oy); c.r(11, 11, 12, 11, HAIR, oy)
        c.r(7, 11, 8, 11, HAIR, oy)
        c.dot(5, 13, EYE, oy); c.dot(10, 13, EYE, oy)
        c.r(5, 15, 10, 15, TEETH, oy); c.r(6, 16, 9, 16, MOUTH, oy)
    spikes(c, oy)
    return c


def side(ph):
    c = Cell()
    oy = 1 if ph in (0, 2) else 0
    off = {0: (-2, 2), 1: (0, 0), 2: (2, -2), 3: (0, 0)}[ph]
    for o, hx in zip(off, (6, 8)):
        c.r(hx, 27, hx + 1, 29, SKIN)
        c.r(hx + o, 30, hx + o + 1, 30, SAND)
        if o:
            c.r(hx + o // 2, 29, hx + o // 2 + 1, 29, SKIN)
    ax = {0: (5, 9), 1: (7, 7), 2: (9, 5), 3: (7, 7)}[ph]

    def arm(x):
        c.r(x, 18, x + 1, 19, WHITE, oy); c.r(x, 20, x + 1, 20, PURPLE, oy); c.r(x, 21, x + 1, 22, SKIN, oy)
    arm(ax[1])
    shorts(c, oy, 5, 10)
    c.r(5, 18, 10, 23, WHITE, oy)
    arm(ax[0])
    c.r(4, 11, 11, 17, SKIN, oy)
    c.r(4, 9, 11, 10, HAIR, oy); c.r(8, 11, 11, 14, HAIR, oy)
    c.dot(3, 14, SKIN, oy)
    c.dot(5, 13, EYE, oy)
    c.r(4, 15, 6, 15, TEETH, oy); c.r(5, 16, 6, 16, MOUTH, oy)
    spikes(c, oy)
    return c


sheet = Image.new("RGBA", (W * 4, H * 4), (0, 0, 0, 0))
for ph in range(4):
    f, sd, b = front(ph), side(ph), front(ph, back=True)
    sheet.paste(f.image(), (ph * W, 0))
    sheet.paste(sd.image(), (ph * W, H))
    sheet.paste(sd.image(flip=True), (ph * W, 2 * H))
    sheet.paste(b.image(), (ph * W, 3 * H))
sheet.save(sys.argv[1])
print(sheet.size)
