#!/usr/bin/env python3
"""Make the role Clawds in animations/.

Run:  python3 tools/make_role_clawds.py

Each Clawd keeps the shape of clawd-hello.json: a 512 x 512 stage, 30 frames
per second, a body of 300 x 180 and parts of 30 x 60. The props stay on that
grid where they can, so the set reads as one family.
"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / 'animations'
FR, SIZE = 30, 512


def hexc(h):
    h = h.lstrip('#')
    return [round(int(h[i:i + 2], 16) / 255, 4) for i in (0, 2, 4)] + [1]


ORANGE = hexc('D97757')
INK = [0.08, 0.08, 0.075, 1]
WHITE = hexc('FFFFFF')
PINK = hexc('E64980')
MAGENTA = hexc('A61E55')
BLUE = hexc('3D7DD8')
DEEP_BLUE = hexc('2C5AA8')
NAVY = hexc('1E2B5E')
GREEN = hexc('2FA36B')
MINT = hexc('6FD9A6')
GOLD = hexc('F2BF3C')
DEEP_GOLD = hexc('B67C12')

# (out handle, in handle) of each segment, as in a CSS cubic-bezier.
EASE = {
    'io': ((0.58, 0), (0.42, 1)),
    'out': ((0.16, 1), (0.3, 1)),
    'in': ((0.5, 0), (0.85, 0.5)),
    'back': ((0.34, 1.56), (0.64, 1)),
    'lin': ((0.167, 0.167), (0.833, 0.833)),
}


class K(list):
    """Keyframes: (t, value) or (t, value, ease). The ease is for the segment
    that starts at that key. 'hold' keeps the value until the next key."""


def _vec(v, kind):
    if kind == 'p':
        return [v[0], v[1], 0]
    if kind == 's':
        return [v, v, 100] if isinstance(v, (int, float)) else [v[0], v[1], 100]
    if kind == '1':
        return [v]
    return list(v)


def prop(v, kind):
    if not isinstance(v, K):
        return {"a": 0, "k": v if kind == '1' else _vec(v, kind)}
    keys = []
    for n, key in enumerate(v):
        ease = key[2] if len(key) > 2 else 'io'
        kf = {"t": key[0], "s": _vec(key[1], kind)}
        if n < len(v) - 1:
            if ease == 'hold':
                kf["h"] = 1
            elif kind == 'p':
                o, i = EASE[ease]
                kf["i"] = {"x": i[0], "y": i[1]}
                kf["o"] = {"x": o[0], "y": o[1]}
            else:
                o, i = EASE[ease]
                kf["i"] = {"x": [i[0]], "y": [i[1]]}
                kf["o"] = {"x": [o[0]], "y": [o[1]]}
        keys.append(kf)
    return {"a": 1, "k": keys}


# ---- shapes -----------------------------------------------------------------

def box(w, h, cx=0, cy=0):
    return {"ty": "rc", "nm": "rect", "d": 1, "s": {"a": 0, "k": [w, h]},
            "p": {"a": 0, "k": [cx, cy]}, "r": {"a": 0, "k": 0}}


def span(x0, x1, y0, y1):
    return box(x1 - x0, y1 - y0, (x0 + x1) / 2, (y0 + y1) / 2)


def oval(w, h, cx=0, cy=0):
    return {"ty": "el", "nm": "ellipse", "d": 1, "s": {"a": 0, "k": [w, h]},
            "p": {"a": 0, "k": [cx, cy]}}


def gr(color, *shapes, o=100, r=0, stroke=None, nm='g'):
    """A group: shapes with one fill. `stroke` is (color, width)."""
    it = list(shapes)
    if stroke:
        it.append({"ty": "st", "nm": "stroke", "c": prop(stroke[0], 'c'),
                   "o": {"a": 0, "k": 100}, "w": {"a": 0, "k": stroke[1]},
                   "lc": 1, "lj": 1, "ml": 4})
    if color is not None:
        it.append({"ty": "fl", "nm": "fill", "c": prop(color, 'c'),
                   "o": prop(o, '1'), "r": 1})
    it.append({"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
               "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": r},
               "o": {"a": 0, "k": 100}})
    return {"ty": "gr", "nm": nm, "it": it}


def pixels(rows, u, cx=0, cy=0):
    """Rects for a pixel drawing. 'X' is a pixel of size u."""
    w, h = len(rows[0]) * u, len(rows) * u
    out = []
    for j, row in enumerate(rows):
        i = 0
        while i < len(row):
            if row[i] == 'X':
                k = i
                while k < len(row) and row[k] == 'X':
                    k += 1
                out.append(span(cx - w / 2 + i * u, cx - w / 2 + k * u,
                                cy - h / 2 + j * u, cy - h / 2 + (j + 1) * u))
                i = k
            else:
                i += 1
    return out


# ---- layers -----------------------------------------------------------------

def layer(nm, shapes=None, p=(0, 0), a=(0, 0), s=(100, 100), r=0, o=100, parent=None):
    d = {"ddd": 0, "ind": 0, "ty": 3 if shapes is None else 4, "nm": nm, "sr": 1,
         "ks": {"o": prop(o, '1'), "r": prop(r, '1'), "p": prop(p, 'p'),
                "a": {"a": 0, "k": [a[0], a[1], 0]}, "s": prop(s, 's')},
         "ao": 0}
    if shapes is not None:
        d["shapes"] = shapes
    d.update(ip=0, op=0, st=0, bm=0)
    if parent:
        d["parent"] = parent
    return d


def comp(nm, op, layers):
    """The first layer in the list is on top."""
    ind = {l["nm"]: n + 1 for n, l in enumerate(layers)}
    assert len(ind) == len(layers), 'layer names must be different'
    for l in layers:
        l["ind"] = ind[l["nm"]]
        l["op"] = op
        if "parent" in l:
            l["parent"] = ind[l["parent"]]
    return {"v": "5.7.4", "fr": FR, "ip": 0, "op": op, "w": SIZE, "h": SIZE,
            "nm": nm, "ddd": 0, "assets": [], "layers": layers}


def xy(keys, fn):
    """Change each key value with fn. Keep the time and the ease."""
    return K([(k[0], fn(k[1])) + tuple(k[2:]) for k in keys])


# ---- the parts of Clawd -----------------------------------------------------

def rig(ox=0, oy=0):
    return layer('rig', p=(256 + ox, 256 + oy))


def bob(pos, scale=None):
    """pos: keys of the lift (negative is up). The anchor is at the feet, so a
    scale key squashes Clawd against the floor."""
    return layer('bob', p=xy(pos, lambda dy: (0, 120 + dy)), a=(0, 120),
                 s=K(scale) if scale else (100, 100), parent='rig')


def hop(t0, h=36):
    pos = [(t0, 0, 'io'), (t0 + 5, 6, 'out'), (t0 + 12, -h, 'in'), (t0 + 19, 0, 'io')]
    sc = [(t0, (100, 100), 'io'), (t0 + 5, (106, 92), 'out'), (t0 + 12, (96, 106), 'in'),
          (t0 + 19, (108, 90), 'out'), (t0 + 25, (100, 100), 'io')]
    return pos, sc


def blinks(op, *times):
    keys = [(0, (100, 100))]
    for t in times:
        keys += [(t - 4, (100, 100)), (t, (100, 10)), (t + 4, (100, 100))]
    return K(keys + [(op, (100, 100))])


def eye(side, look=None, s=(100, 100)):
    x = -75 if side == 'left' else 75
    p = xy(look, lambda d: (x + d[0], -60 + d[1])) if look else (x, -60)
    return layer('eye-' + side, [gr(INK, box(30, 60))], p=p, s=s, parent='bob')


def body():
    return layer('body', [gr(ORANGE, box(300, 180))], p=(0, -30), parent='bob')


def arm(side, y=-30, parent='bob'):
    x = -165 if side == 'left' else 165
    p = xy(y, lambda v: (x, v)) if isinstance(y, list) else (x, y)
    return layer('arm-' + side, [gr(ORANGE, box(30, 60))], p=p, parent=parent)


def legs(lift=None):
    """lift: {leg number: keys of y}. A leg with no keys stays on the floor."""
    out = []
    for n, x in enumerate((-105, -45, 45, 105), 1):
        keys = (lift or {}).get(n)
        p = xy(keys, lambda v, x=x: (x, v)) if keys else (x, 90)
        out.append(layer('leg-%d' % n, [gr(ORANGE, box(30, 60))], p=p, parent='bob'))
    return out


def shadow(pos):
    s = xy(pos, lambda dy: max(60, min(104, 100 + dy)))
    return layer('shadow', [gr([0, 0, 0, 1], oval(300, 28))], p=(0, 136), s=s,
                 o=14, parent='rig')


def with_hop(op, idle, t0, h=36):
    """Bob keys: the idle keys, then one hop at t0."""
    pos, sc = hop(t0, h)
    pos = idle + pos
    if pos[-1][0] != op:
        pos.append((op, 0))
    return K(pos), [(0, (100, 100))] + sc + [(op, (100, 100))]


# ---- admin ------------------------------------------------------------------

def admin():
    op = 90
    ticks = (10, 28, 46)
    pos, sc = with_hop(op, [(0, 0), (14, -8), (27, 0), (40, -8)], 54)

    def bump(base):
        keys = [(0, base)]
        for t in ticks:
            keys += [(t, base, 'out'), (t + 3, base - 6), (t + 8, base)]
        return keys + [(op, base)]

    look = K([(0, (0, 0)), (4, (0, 0)), (8, (8, 2)), (54, (8, 2)), (60, (0, 0)), (op, (0, 0))])
    blink = blinks(op, 22, 82)

    rows = []
    for n, w in enumerate((36, 26, 32)):
        y = 20 + 30 * n
        rows += [gr(hexc('D9D4C7'), box(16, 16, -25, y)),
                 gr(hexc('C4BDAD'), span(-8, -8 + w, y - 4, y + 4))]
    paper = layer('paper', rows + [gr(hexc('FFFDF7'), span(-37, 37, 0, 100))],
                  p=(0, -46), parent='board',
                  s=K([(0, (100, 100)), (78, (100, 100)), (82, (100, 0)), (86, (100, 100)),
                       (op, (100, 100))]))
    done = [layer('tick-%d' % (n + 1), [gr(GREEN, box(16, 16))], p=(-25, 20 + 30 * n),
                  parent='paper',
                  s=K([(0, 0, 'hold'), (t, 0, 'back'), (t + 6, 100, 'hold'), (82, 0)]))
            for n, t in enumerate(ticks)]
    board = layer('board', [gr(DEEP_BLUE, span(-18, 18, -70, -56)),
                            gr(BLUE, box(90, 120))],
                  p=xy(bump(-20), lambda y: (215, y)), parent='bob')
    headset = layer('headset', [
        gr(NAVY, span(-124, -98, -16, 2)),
        gr(DEEP_BLUE, span(-150, -116, -76, -68), span(-124, -116, -76, -10),
           span(-172, -150, -124, -68), span(150, 172, -124, -68)),
        gr(BLUE, span(-158, 158, -134, -122)),
    ], parent='bob')
    cheer = [(0, -30), (59, -30, 'out'), (66, -62, 'in'), (73, -30), (op, -30)]

    return comp('Admin Clawd', op, [
        rig(-40), bob(pos, sc),
        arm('right', bump(-30)), *done, paper, board, headset,
        eye('left', look, blink), eye('right', look, blink), body(),
        arm('left', cheer), *legs(), shadow(pos),
    ])


# ---- accountant -------------------------------------------------------------

def accountant():
    op = 120
    drops = [4 + 16 * n for n in range(5)]
    lands = [t + 9 for t in drops]
    idle = [(0, 0)]
    for t in lands:
        idle += [(t - 8, -6), (t, 2)]
    pos, sc = with_hop(op, idle, 84)

    coins = []
    for n, t in enumerate(drops):
        rest = 112 - 16 * n
        out = 100 + (4 - n) * 2
        coins.append(layer('coin-%d' % (n + 1), [
            gr(hexc('FFE7A0'), span(-22, -8, -6, -3)),
            gr(GOLD, span(-30, 30, -8, 3)),
            gr(DEEP_GOLD, span(-30, 30, 3, 8)),
        ], parent='rig',
            p=xy([(0, -300, 'hold'), (t, -300, 'in'), (t + 9, rest, 'out'),
                  (t + 12, rest - 5, 'in'), (t + 15, rest, 'hold'),
                  (out, rest, 'out'), (out + 10, rest - 46)], lambda y: (225, y)),
            o=K([(0, 100, 'hold'), (out, 100, 'io'), (out + 10, 0)])))
    coins.reverse()

    look = [(0, (0, 0))]
    for t in drops:
        look += [(t, (9, -8), 'in'), (t + 9, (9, 7))]
    look += [(84, (9, 7)), (90, (0, 0)), (op, (0, 0))]
    look = K(look)
    blink = blinks(op, 112)

    count = [(0, -30)]
    for t in lands:
        count += [(t - 3, -30, 'out'), (t, -48), (t + 5, -30)]
    count += [(89, -30, 'out'), (96, -62, 'in'), (103, -30), (op, -30)]
    cheer = [(0, -30), (89, -30, 'out'), (96, -62, 'in'), (103, -30), (op, -30)]

    visor = layer('visor', [
        gr(hexc('2FBF86'), span(-170, 170, -105, -90), o=82),
        gr(hexc('1B6E49'), span(-150, 150, -120, -105)),
    ], parent='bob')

    return comp('Accountant Clawd', op, [
        rig(-38), bob(pos, sc),
        *coins, visor,
        eye('left', look, blink), eye('right', look, blink), body(),
        arm('left', cheer), arm('right', count), *legs(), shadow(pos),
    ])


# ---- marketing --------------------------------------------------------------

HEART = ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...']


def marketing():
    op = 60
    shouts = (2, 32)
    pos, sc, kick, tilt, pump = [], [], [(0, 100)], [(0, -15)], [(0, -30)]
    for t in shouts:
        pos += [(t - 2, 0), (t, 4, 'out'), (t + 6, -14, 'in'), (t + 13, 0)]
        sc += [(t - 2, (100, 100)), (t, (104, 95), 'out'), (t + 6, (97, 105), 'in'),
               (t + 13, (105, 94), 'out'), (t + 18, (100, 100))]
        kick += [(t, 100, 'out'), (t + 4, 116), (t + 12, 100)]
        tilt += [(t, -15, 'out'), (t + 4, -22), (t + 12, -15)]
        pump += [(t, -30, 'out'), (t + 6, -58, 'in'), (t + 13, -30)]
    pos, sc = K(pos + [(op, 0)]), sc + [(op, (100, 100))]

    def wave(nm, start, end, r):
        p, o = [], [(0, 0)]
        for t in shouts:
            p += [(t, start, 'out'), (t + 14, end, 'hold')]
            o += [(t, 0), (t + 3, 100), (t + 14, 0)]
        return layer(nm, [gr(PINK, box(20, 8))], p=K(p), r=r, o=K(o + [(op, 0)]),
                     parent='megaphone')

    megaphone = layer('megaphone', [
        gr(MAGENTA, span(48, 58, -49, 49), span(-14, 0, -11, 11)),
        gr(hexc('FFD9E5'), span(12, 24, -25, -17)),
        gr(PINK, span(0, 12, -17, 17), span(12, 24, -25, 25), span(24, 36, -33, 33),
           span(36, 48, -41, 41)),
    ], p=(180, -52), s=K(kick + [(op, 100)]), r=K(tilt + [(op, -15)]), parent='bob')

    def heart(nm, u, color, t0, t1, start, end):
        return layer(nm, [gr(color, *pixels(HEART, u))], parent='rig',
                     p=K([(t0, start, 'out'), (t1, end)]),
                     s=K([(0, 0, 'hold'), (t0, 0, 'back'), (t0 + 6, 100)]),
                     o=K([(t0, 100, 'hold'), (t1 - 12, 100), (t1, 0)]))

    lift = [(0, 90), (2, 90, 'out'), (8, 70, 'in'), (15, 90), (op, 90)]
    late = [(0, 90), (32, 90, 'out'), (38, 70, 'in'), (45, 90), (op, 90)]
    look = K([(0, (7, 0)), (op, (7, 0))])
    blink = blinks(op, 24, 54)

    return comp('Marketing Clawd', op, [
        rig(-50), bob(pos, sc),
        heart('heart-1', 7, PINK, 4, 40, (-95, -150), (-112, -222)),
        heart('heart-2', 5, MAGENTA, 28, 60, (20, -145), (36, -215)),
        arm('right', -50),
        wave('wave-up', (62, -34), (88, -52), -28), wave('wave-mid', (66, 0), (96, 0), 0),
        wave('wave-down', (62, 34), (88, 52), 28), megaphone,
        eye('left', look, blink), eye('right', look, blink), body(),
        arm('left', pump + [(op, -30)]),
        *legs({1: lift, 3: lift, 2: late, 4: late}), shadow(pos),
    ])


# ---- ceo --------------------------------------------------------------------

ARROW = ['...X...', '..XXX..', '.XXXXX.', 'XXXXXXX', '..XXX..', '..XXX..', '..XXX..']


def ceo():
    op = 120
    pos, sc = with_hop(op, [(0, 0), (15, -8), (30, 0), (45, -8)], 62, h=40)
    pos = K(pos[:-1] + [(87, 0), (104, -8), (op, 0)])

    gone = K([(0, 100, 'hold'), (104, 100), (114, 0)])
    bars = [layer('bar-%d' % (n + 1), [
        gr(MINT, span(-10, 10, -h, -h + 6)),
        gr(GREEN, span(-10, 10, -h, 0)),
    ], p=(205 + 26 * n, 120), parent='rig', o=gone,
        s=K([(0, (100, 0), 'hold'), (t, (100, 0), 'back'), (t + 14, (100, 100))]))
        for n, (h, t) in enumerate(((70, 10), (120, 24), (180, 38)))]
    arrow = layer('arrow', [gr(GREEN, *pixels(ARROW, 6))], parent='rig', o=gone,
                  p=K([(0, (257, -94)), (63, (257, -94)), (80, (257, -102)), (98, (257, -94))]),
                  s=K([(0, 0, 'hold'), (56, 0, 'back'), (63, 100)]))

    tie = layer('tie', [
        gr(GOLD, span(-20, 20, 20, 28)),
        gr(NAVY, span(-14, 14, -10, 8), span(-20, 20, 8, 48), span(-14, 14, 48, 60),
           span(-7, 7, 60, 70)),
    ], p=(0, -12), parent='bob',
        r=K([(0, 0), (67, 0), (72, -7), (78, 6), (84, -3), (90, 0), (op, 0)]))
    collar = layer('collar', [gr(WHITE, span(-46, -12, -26, -6), span(12, 46, -26, -6))],
                   parent='bob')

    look = K([(0, (0, 0)), (6, (0, 0)), (11, (9, 6)), (56, (9, -6)), (84, (9, -6)),
              (90, (0, 0)), (op, (0, 0))])
    blink = blinks(op, 30)
    wink = K(list(blink[:-1]) + [(92, (100, 100)), (96, (100, 10)), (104, (100, 10)),
                                 (108, (100, 100)), (op, (100, 100))])
    point = [(0, -30), (40, -30), (50, -66), (96, -66), (104, -30), (op, -30)]

    return comp('CEO Clawd', op, [
        rig(-46), bob(pos, sc),
        arrow, *bars, tie, collar,
        eye('left', look, wink), eye('right', look, blink), body(),
        arm('left'), arm('right', point), *legs(), shadow(pos),
    ])


# ---- coder ------------------------------------------------------------------

def coder():
    op = 120
    pos, sc = with_hop(op, [(0, 0), (15, -5), (30, 0), (45, -5), (60, 0), (75, -5)], 92, h=20)

    code = {'pink': hexc('F27BA5'), 'white': hexc('E8E6DF'), 'blue': hexc('6FA8F5'),
            'green': hexc('5BD69A'), 'yellow': hexc('F2BF3C')}
    # (name, x, y, width, colour, first frame, last frame)
    words = [('a', -76, -18, 36, 'pink', 8, 15), ('b', -34, -18, 54, 'white', 16, 26),
             ('c', -62, -2, 28, 'blue', 30, 36), ('d', -28, -2, 66, 'green', 37, 50),
             ('e', -62, 14, 46, 'yellow', 54, 63), ('f', -10, 14, 30, 'white', 64, 72),
             ('g', -76, 30, 22, 'pink', 76, 82)]
    typed = [layer('word-' + nm, [gr(code[c], span(0, w, -4, 4))], p=(x, y), parent='term',
                   s=K([(0, (0, 100), 'hold'), (t0, (0, 100), 'lin'), (t1, (100, 100), 'hold'),
                        (110, (0, 100))]))
             for nm, x, y, w, c, t0, t1 in words]
    caret = [(0, (-76, -18), 'hold')]
    for nm, x, y, w, c, t0, t1 in words:
        caret += [(t0, (x, y), 'lin'), (t1, (x + w, y), 'hold')]
    caret.append((110, (-76, -18)))
    flash = [(n, 100 if i % 2 == 0 else 0, 'hold')
             for i, n in enumerate((0, 4, 8, 84, 88, 94, 98, 104, 108, 110, 114, 118))]
    cursor = layer('cursor', [gr(code['white'], span(2, 9, -5, 5))], p=K(caret),
                   o=K(flash), parent='term')

    edge = K([(0, hexc('565C6B')), (88, hexc('565C6B')), (92, hexc('5BD69A')),
              (106, hexc('5BD69A')), (112, hexc('565C6B'))])
    window = layer('window', [
        gr(hexc('F0625D'), box(8, 8, -93, -39)),
        gr(GOLD, box(8, 8, -80, -39)),
        gr(hexc('5BD69A'), box(8, 8, -67, -39)),
        gr(ORANGE, box(8, 8, -88, -18)),
        gr(edge, span(-105, 105, -48, -30)),
        gr(hexc('1A1C22'), box(210, 96), stroke=(edge, 4)),
    ], parent='term')
    # The window jumps with Clawd, so the head never goes behind it.
    term = layer('term', p=K([(0, (0, -190)), (30, (0, -194)), (60, (0, -190)),
                              (90, (0, -194)), (97, (0, -190), 'out'), (104, (0, -207), 'in'),
                              (111, (0, -190)), (op, (0, -190))]), parent='rig')

    glow = K([(0, WHITE), (88, WHITE), (92, hexc('5BD69A')), (106, hexc('5BD69A')), (112, WHITE)])
    shine = K([(0, 16), (88, 16), (92, 50), (106, 50), (112, 16)])
    glasses = layer('glasses', [
        gr(WHITE, box(8, 8, -89, -87), box(8, 8, 61, -87), o=85),
        gr(None, box(51, 77, -75, -60), box(51, 77, 75, -60), stroke=(hexc('20232B'), 7)),
        gr(hexc('20232B'), span(-44, 44, -70, -63), span(-150, -104, -70, -63),
           span(104, 150, -70, -63)),
        gr(glow, box(44, 70, -75, -60), box(44, 70, 75, -60), o=shine),
    ], parent='bob')

    laptop = layer('laptop', [
        gr(INK, box(4, 8, -8, 58), box(4, 8, 8, 58)),
        gr(ORANGE, box(36, 20, 0, 60), box(4, 8, -20, 60), box(4, 8, 20, 60),
           box(4, 6, -12, 73), box(4, 6, -4, 73), box(4, 6, 4, 73), box(4, 6, 12, 73)),
        gr(hexc('AEB8C9'), span(-90, 90, 6, 12)),
        gr(hexc('8C97AB'), span(-90, 90, 6, 118)),
        gr(hexc('5E687B'), span(-118, 118, 118, 130)),
    ], parent='rig')

    def typing(first_down):
        keys, down = [(0, 30, 'lin')], first_down
        for t0, t1 in ((8, 26), (30, 50), (54, 72), (76, 82)):
            keys.append((t0, 30, 'lin'))
            for t in range(t0 + 3, t1, 3):
                keys.append((t, 37 if down else 23, 'lin'))
                down = not down
            keys.append((t1, 30, 'lin'))
        return keys + [(97, 30, 'out'), (104, -20, 'in'), (111, 30), (op, 30)]

    look = K([(0, (0, 0)), (4, (0, 0)), (8, (-5, -3), 'lin'), (26, (5, -3)),
              (30, (-5, -3), 'lin'), (50, (5, -3)), (54, (-5, -3), 'lin'), (72, (5, -3)),
              (76, (-5, -3), 'lin'), (82, (0, -3)), (88, (0, 0)), (op, (0, 0))])
    blink = blinks(op, 114)

    return comp('Coder Clawd', op, [
        rig(0, 6), bob(pos, sc), term,
        laptop, cursor, *typed, window, glasses,
        eye('left', look, blink), eye('right', look, blink), body(),
        arm('left', typing(True)), arm('right', typing(False)), *legs(), shadow(pos),
    ])


# ---- engineer ---------------------------------------------------------------

def engineer():
    op = 60
    gx, gy, reach = 219, -30, 58
    low, high = gy + reach * 0.3827, gy - reach * 0.3827   # the hand at -22.5 and +22.5 degrees
    turn, swing, hand, pos, jolt, spark_p, spark_o = [], [], [], [], [(0, (0, 0))], [], [(0, 0)]
    for n, t in enumerate((0, 30)):
        turn += [(t, 45 * n), (t + 10, 45 * (n + 1), 'hold')]
        swing += [(t, -22.5), (t + 10, 22.5), (t + 14, 22.5), (t + 24, -22.5)]
        hand += [(t, low), (t + 10, high), (t + 14, high), (t + 24, low)]
        pos += [(t, 0), (t + 10, -6), (t + 24, 0)]
        jolt += [(t + 10, (0, 0), 'out'), (t + 13, (0, -7), 'in'), (t + 17, (0, 0))]
        spark_p += [t + 9]
        spark_o += [(t + 9, 0, 'hold'), (t + 10, 100), (t + 20, 0)]
    pos = K(pos + [(op, 0)])
    steel, dark = hexc('6C86A8'), hexc('425878')

    def spark(nm, start, end):
        p = []
        for t in spark_p:
            p += [(t, start, 'hold'), (t + 1, start, 'out'), (t + 11, end, 'hold')]
        return layer(nm, [gr(hexc('F4B81F'), box(8, 8))], p=K(p), o=K(spark_o + [(op, 0)]),
                     parent='rig')

    gear = layer('gear', [
        gr(dark, oval(34, 34)),
        gr(steel, box(62, 62)),
        gr(steel, box(62, 62), r=45),
    ], p=(gx, gy), r=K(turn + [(op, 90)]), parent='rig')
    wrench = layer('wrench', [
        gr(dark, box(12, 12)),
        gr(hexc('D5DDE7'), box(28, 28), span(-66, -10, -6, 6)),
    ], p=(gx, gy), r=K(swing + [(op, -22.5)]), parent='rig')
    hat = layer('hat', [
        gr(hexc('C98A0B'), span(-13, 13, -196, -134), span(-165, 165, -134, -120)),
        gr(hexc('F4B81F'), span(-75, 75, -196, -180), span(-115, 115, -180, -134)),
    ], p=K(jolt + [(op, (0, 0))]), parent='bob')

    look = K([(0, (8, 2)), (op, (8, 2))])
    blink = blinks(op, 50)

    return comp('Engineer Clawd', op, [
        rig(-41), bob(pos),
        spark('spark-1', (gx - 12, -84), (gx - 20, -112)),
        spark('spark-2', (gx + 18, -80), (gx + 30, -106)),
        arm('right', hand + [(op, low)], parent='rig'), wrench, gear, hat,
        eye('left', look, blink), eye('right', look, blink), body(),
        arm('left'), *legs(), shadow(pos),
    ])


def main():
    for name, make in (('admin', admin), ('accountant', accountant), ('marketing', marketing),
                       ('ceo', ceo), ('coder', coder), ('engineer', engineer)):
        path = OUT / ('clawd-%s.json' % name)
        path.write_text(json.dumps(make(), separators=(',', ':')))
        print(path.relative_to(OUT.parent), path.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
