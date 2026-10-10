#!/usr/bin/env python3
"""Make the job Clawds in animations/. Each job is one an AI agent can do.

Run:  python3 tools/make_job_clawds.py

The parts of Clawd and the shape helpers come from make_role_clawds.py.
A prop goes in one of three places: at the right of Clawd, above the head,
or in front of the legs. A Clawd with a prop above the head does not hop,
so the head never goes behind the prop.
"""
import math

from make_role_clawds import *  # noqa: F401,F403

RED = hexc('E5484D')
PAPER = hexc('FFFDF7')
EDGE = hexc('B9B1A0')
LINE = hexc('C4BDAD')
TEXT = hexc('6E6A61')
SLATE = hexc('1A1C22')
FRAME = hexc('565C6B')
STEEL = hexc('8E96A8')
YELLOW = hexc('F4B81F')
WOOD = hexc('8A5A2B')
SKY = hexc('6FA8F5')
LEAF = hexc('5BD69A')

GLYPH = {
    '1': ['.X.', 'XX.', '.X.', '.X.', 'XXX'],
    '2': ['XXX', '..X', 'XXX', 'X..', 'XXX'],
    '3': ['XXX', '..X', 'XXX', '..X', 'XXX'],
    '+': ['...', '.X.', 'XXX', '.X.', '...'],
    '=': ['...', 'XXX', '...', 'XXX', '...'],
    'A': ['.X.', 'X.X', 'XXX', 'X.X', 'X.X'],
    '!': ['X', 'X', 'X', '.', 'X'],
    'wen': ['...X...', 'XXXXXXX', '.X...X.', '..X.X..', '...X...', '..X.X..', 'XX...XX'],
}
CHECK = ['.....XX', '....XX.', 'XX.XX..', '.XXX...', '..X....']


# ---- helpers ----------------------------------------------------------------

def idle(op, amp=8):
    keys = []
    for t in range(0, op, 30):
        keys += [(t, 0), (t + 15, -amp)]
    return K(keys + [(op, 0)])


def beat(op, hits, amp=6):
    """The idle bob, with one small bounce at each hit."""
    keys = {t: (0 if t % 30 == 0 else -amp, 'io') for t in range(0, op + 1, 15)}
    for h in hits:
        for t in list(keys):
            if h - 10 < t < h + 22 and t not in (0, op):
                del keys[t]
        keys.update({h: (0, 'io'), h + 4: (4, 'out'), h + 9: (-12, 'in'), h + 15: (0, 'io')})
    return K([(t,) + keys[t] for t in sorted(keys)])


def pop(t, out=None):
    """Scale keys that pop a layer in at t. `out` is the frame where it fades."""
    d = {'s': K([(0, 0, 'hold'), (t, 0, 'back'), (t + 6, 100)])}
    if out is not None:
        d['o'] = K([(0, 100, 'hold'), (out, 100), (out + 8, 0)])
    return d


def cheer(op, t, base=-30, up=-62):
    return [(0, base), (t, base, 'out'), (t + 7, up, 'in'), (t + 14, base), (op, base)]


def taps(op, spans, base=-30, first_down=True, after=()):
    """Arm keys for typing in each (start, end) span."""
    keys, down = [(0, base, 'lin')], first_down
    for t0, t1 in spans:
        keys.append((t0, base, 'lin'))
        for t in range(t0 + 3, t1, 3):
            keys.append((t, base + (7 if down else -7), 'lin'))
            down = not down
        keys.append((t1, base, 'lin'))
    return keys + list(after) + [(op, base)]


def paper(x0, x1, y0, y1, w=4):
    return gr(PAPER, span(x0, x1, y0, y1), stroke=(EDGE, w))


def still(v, op):
    return K([(0, v), (op, v)])


def headset(band, cups, mic):
    return layer('headset', [
        gr(mic, span(-124, -98, -16, 2)),
        gr(cups, span(-150, -116, -76, -68), span(-124, -116, -76, -10),
           span(-172, -150, -124, -68), span(150, 172, -124, -68)),
        gr(band, span(-158, 158, -134, -122)),
    ], parent='bob')


def cast(nm, op, ox=0, oy=0, pos=None, sc=None, top=(), look=None, blink=None, eyes=None,
         arm_l=-30, arm_r=-30, lift=None, skin=None, bob_layer=None, shadow_layer=None):
    """Put a Clawd together. `top` is the list of layers in front of Clawd."""
    pos = K(pos) if pos is not None else idle(op)
    if eyes is None:
        blink = blink or blinks(op, op - 10)
        look = K(look) if look else None
        eyes = [eye('left', look, blink), eye('right', look, blink)]
    arms = [arm(side, y) for side, y in (('left', arm_l), ('right', arm_r)) if y is not None]
    trunk = [body(), *arms, *legs(lift)]
    if skin is not None:
        for part in trunk:
            part['shapes'][0]['it'][-2]['c'] = prop(skin, 'c')
    return comp(nm, op, [rig(ox, oy), bob_layer or bob(pos, sc), *top, *eyes, *trunk,
                         shadow_layer or shadow(pos)])


# ---- 1 researcher -----------------------------------------------------------

def researcher():
    op = 120
    pos, sc = with_hop(op, [(0, 0), (15, -6), (30, 0), (45, -6), (60, 0)], 66, h=20)
    look = K([(0, (-5, 0), 'lin'), (18, (5, 0)), (22, (-5, 2), 'lin'), (40, (5, 2)),
              (44, (-5, 3), 'lin'), (60, (5, 3)), (66, (0, 0)), (112, (0, 0)), (op, (-5, 0))])
    blink = blinks(op, 104)
    big = K([(k[0], (k[1][0] * 1.4, k[1][1] * 1.4)) for k in blink])
    lens = layer('lens', [
        gr(WHITE, box(10, 10, -18, -20), o=80),
        gr(None, oval(96, 96), stroke=(DEEP_BLUE, 9)),
        gr(WOOD, span(50, 104, -7, 7), r=28),
        gr(WHITE, oval(96, 96), o=18),
    ], p=(75, -60), parent='bob')
    mark = layer('mark', [gr(YELLOW, *pixels(GLYPH['!'], 10))], p=(75, -196), parent='bob',
                 **pop(72, 98))
    return cast('Researcher Clawd', op, ox=-8, oy=16, pos=pos, sc=sc,
                top=[mark, arm('right', -12), lens],
                eyes=[eye('left', look, blink), eye('right', look, big)],
                arm_l=cheer(op, 71), arm_r=None)


# ---- 2 writer ---------------------------------------------------------------

def writer():
    op = 120
    rows = [(-56, 60, 8, 22), (-36, 52, 28, 42), (-16, 64, 48, 62), (4, 36, 68, 78)]
    page_o = K([(0, 100), (86, 100), (98, 0), (100, 0), (112, 100), (op, 100)])
    page = layer('page', [paper(182, 270, -80, 36)], parent='rig', o=page_o,
                 p=K([(0, (0, 0)), (86, (0, 0), 'in'), (98, (0, -60), 'hold'),
                      (100, (0, 40), 'out'), (112, (0, 0)), (op, (0, 0))]))
    lines = [layer('line-%d' % n, [gr(TEXT, span(0, w, -4, 4))], p=(194, y), parent='page',
                   o=page_o, s=K([(0, (0, 100), 'hold'), (t0, (0, 100), 'lin'),
                                  (t1, (100, 100), 'hold'), (99, (0, 100))]))
             for n, (y, w, t0, t1) in enumerate(rows, 1)]
    tip, wob, hand = [(0, (194, -56), 'hold')], [(0, -70)], [(0, -30)]
    for y, w, t0, t1 in rows:
        tip += [(t0, (194, y), 'lin'), (t1, (194 + w, y))]
        for n, t in enumerate(range(t0, t1, 3)):
            wob.append((t, -64 if n % 2 else -76, 'lin'))
        wob.append((t1, -70))
        hand += [(t0, -30), ((t0 + t1) // 2, -38), (t1, -30)]
    tip += [(90, (250, -34)), (op, (194, -56))]
    pencil = layer('pencil', [
        gr(INK, span(0, 8, -4, 4)),
        gr(hexc('E8C9A0'), span(8, 18, -6, 6)),
        gr(PINK, span(68, 78, -7, 7)),
        gr(EDGE, span(62, 68, -7, 7)),
        gr(YELLOW, span(18, 62, -7, 7)),
    ], p=K(tip), r=K(wob + [(op, -70)]), parent='rig')
    look = [(0, (8, -4)), (22, (9, -4)), (42, (9, -1)), (62, (9, 2)), (78, (9, 5)),
            (86, (9, 5)), (96, (6, -8)), (110, (8, -4)), (op, (8, -4))]
    return cast('Writer Clawd', op, ox=-46, pos=beat(op, [86]), top=[pencil, *lines, page],
                look=look, arm_r=hand + [(op, -30)])


# ---- 3 editor ---------------------------------------------------------------

def editor():
    op = 120
    words = [(-103, 44), (-49, 36), (63, 40)]
    strip = layer('strip', [gr(TEXT, *[span(x, x + w, -196, -184) for x, w in words]),
                            paper(-125, 125, -218, -162)], parent='rig')
    gone = K([(0, 100, 'hold'), (40, 100), (50, 0)])
    old = layer('old-word', [gr(K([(0, TEXT), (30, TEXT), (36, RED)]), span(0, 56, -6, 6))],
                parent='rig', o=gone,
                p=K([(0, (-3, -190)), (40, (-3, -190), 'in'), (50, (-3, -160))]))
    strike = layer('strike', [gr(RED, span(0, 64, -3, 3))], p=(-4, 0), parent='old-word',
                   o=gone, s=K([(0, (0, 100), 'hold'), (20, (0, 100), 'out'), (30, (100, 100))]))
    new = layer('new-word', [gr(K([(0, GREEN), (100, GREEN), (110, TEXT)]), span(0, 56, -6, 6))],
                parent='rig', o=K([(0, 0, 'hold'), (52, 100)]),
                p=K([(0, (-3, -226), 'hold'), (52, (-3, -226), 'back'), (62, (-3, -190))]))
    pen = layer('pen', [
        gr(INK, span(0, 8, -3, 3)),
        gr(hexc('B4232A'), span(60, 74, -6, 6)),
        gr(RED, span(8, 60, -6, 6)),
    ], r=50, parent='rig',
        p=K([(0, (146, -166)), (14, (146, -166)), (20, (-7, -190), 'out'), (30, (57, -190)),
             (40, (146, -166)), (op, (146, -166))]))
    look = [(0, (0, -5)), (18, (-1, -6)), (30, (5, -6)), (52, (2, -7)), (66, (2, -5)),
            (80, (0, 0)), (110, (0, 0)), (op, (0, -5))]
    return cast('Editor Clawd', op, oy=14, pos=beat(op, [64]), top=[pen, strike, old, new, strip],
                look=look, arm_r=-60, arm_l=cheer(op, 66))


# ---- 4 translator -----------------------------------------------------------

def translator():
    op = 120
    fade = K([(0, 100, 'hold'), (50, 100), (58, 0, 'hold'), (60, 100, 'hold'), (110, 100),
              (118, 0)])

    def bubble(nm, x, tint, rows, u, a, b):
        tail = 30 if x < 0 else -30
        return layer(nm, [gr(WHITE, *pixels(rows, u)),
                          gr(tint, box(110, 80), box(16, 16, tail, 46))],
                     p=(x, -200), parent='rig', o=fade,
                     s=K([(0, 0, 'hold'), (a, 0, 'back'), (a + 6, 100, 'hold'), (60, 0, 'hold'),
                          (b, 0, 'back'), (b + 6, 100)]))

    dots = [layer('dot-%d' % (n + 1), [gr(hexc('8A8478'), box(8, 8))], p=(-14 + 14 * n, -200),
                  parent='rig',
                  o=K([(0, 0, 'hold'), (16 + 6 * n, 100, 'hold'), (50, 0, 'hold'),
                       (76 + 6 * (2 - n), 100, 'hold'), (110, 0)]))
            for n in range(3)]
    look = [(0, (0, 0)), (6, (-6, -5)), (30, (-6, -5)), (38, (6, -5)), (90, (6, -5)),
            (98, (-6, -5)), (112, (-6, -5)), (op, (0, 0))]
    say_l = [(0, -30), (6, -30, 'out'), (12, -48), (22, -30), (96, -30, 'out'), (102, -48),
             (112, -30), (op, -30)]
    say_r = [(0, -30), (36, -30, 'out'), (42, -48), (52, -30), (66, -30, 'out'), (72, -48),
             (82, -30), (op, -30)]
    return cast('Translator Clawd', op, oy=14, pos=idle(op, 6),
                top=[*dots, bubble('bubble-left', -80, BLUE, GLYPH['A'], 10, 6, 96),
                     bubble('bubble-right', 80, PINK, GLYPH['wen'], 7, 36, 66)],
                look=look, arm_l=say_l, arm_r=say_r)


# ---- 5 data analyst ---------------------------------------------------------

def data_analyst():
    op = 120
    xs, base = [-84, -42, 0, 42, 84], -146
    heights = {'a': 60, 'b': 30, 'c': 90, 'd': 45, 'e': 75}
    order, moves = list('abcde'), {k: [] for k in 'abcde'}
    for t, (i, j) in zip((10, 30, 50, 70), ((0, 1), (1, 3), (2, 3), (3, 4))):
        moves[order[i]].append((t, i, j))
        moves[order[j]].append((t, j, i))
        order[i], order[j] = order[j], order[i]
    tint = K([(0, BLUE), (86, BLUE), (92, GREEN, 'hold'), (118, BLUE)])
    show = K([(0, 0), (8, 100), (108, 100), (116, 0), (op, 0)])
    bars = []
    for n, k in enumerate('abcde'):
        keys = [(0, (xs[n], base))]
        for t, i, j in moves[k]:
            if j > i:   # the bar that goes right jumps over the other bar
                keys += [(t, (xs[i], base), 'out'), (t + 7, ((xs[i] + xs[j]) / 2, base - 18), 'in'),
                         (t + 14, (xs[j], base))]
            else:
                keys += [(t, (xs[i], base)), (t + 14, (xs[j], base))]
        if moves[k]:
            keys[-1] += ('hold',)
            keys.append((118, (xs[n], base)))
        bars.append(layer('bar-' + k, [gr(tint, span(-15, 15, -heights[k], 0))],
                          p=K(keys) if moves[k] else (xs[n], base), o=show, parent='rig'))
    floor = layer('floor', [gr(EDGE, span(-112, 112, -146, -140))], parent='rig')
    look = [(0, (0, -5)), (10, (-6, -5)), (30, (0, -5)), (50, (3, -5)), (70, (6, -5)),
            (90, (0, -5)), (96, (0, 0)), (112, (0, 0)), (op, (0, -5))]
    return cast('Data Analyst Clawd', op, oy=14, pos=beat(op, [90]), top=[*bars, floor],
                look=look, arm_l=cheer(op, 92), arm_r=cheer(op, 92))


# ---- 6 QA tester ------------------------------------------------------------

def qa_tester():
    op = 120
    # (frame, (x, lift), (scale x, scale y), ease): Clawd jumps on the bug, then jumps back.
    path = [(0, (0, 0), (100, 100), 'io'), (44, (0, 0), (100, 100), 'io'),
            (49, (0, 6), (106, 92), 'out'), (56, (20, -44), (96, 106), 'in'),
            (63, (40, 0), (108, 90), 'out'), (69, (40, 0), (100, 100), 'io'),
            (80, (40, 0), (100, 100), 'io'), (85, (40, 6), (106, 92), 'out'),
            (92, (20, -40), (96, 106), 'in'), (99, (0, 0), (108, 90), 'out'),
            (105, (0, 0), (100, 100), 'io'), (op, (0, 0), (100, 100), 'io')]
    hopper = layer('bob', p=K([(t, (x, 120 + y), e) for t, (x, y), s, e in path]), a=(0, 120),
                   s=K([(t, s, e) for t, p, s, e in path]), parent='rig')
    under = layer('shadow', [gr([0, 0, 0, 1], oval(300, 28))], o=14, parent='rig',
                  p=K([(t, (x, 136), e) for t, (x, y), s, e in path]),
                  s=K([(t, max(60, min(104, 100 + y)), e) for t, (x, y), s, e in path]))
    walk = [(t, (350 - 190 * t / 40, 120 - (2 if n % 2 else 0)), 'lin')
            for n, t in enumerate(range(0, 41, 4))]
    bug = layer('bug', [
        gr(INK, span(-20, -10, -16, -4), span(-22, -18, -22, -16), span(-8, -4, -4, 0),
           span(0, 4, -4, 0), span(8, 12, -4, 0), box(4, 4, -2, -13), box(4, 4, 8, -11)),
        gr(RED, span(-12, 16, -20, -4)),
    ], p=K(walk), parent='rig', s=K([(0, (220, 220), 'hold'), (63, (290, 35))]),
        o=K([(0, 100, 'hold'), (70, 100), (78, 0)]))
    passed = layer('passed', [gr(GREEN, *pixels(CHECK, 7))], p=(232, -70), parent='rig',
                   **pop(66, 96))
    look = [(0, (0, 0)), (12, (0, 0)), (20, (9, 6)), (44, (9, 6)), (56, (6, 8)), (66, (0, 0)),
            (op, (0, 0))]
    return cast('QA Tester Clawd', op, ox=-30, top=[passed, bug], look=look,
                blink=blinks(op, 74, 112), bob_layer=hopper, shadow_layer=under)


# ---- 7 code reviewer --------------------------------------------------------

def code_reviewer():
    op = 120
    pos, sc = with_hop(op, [(0, 0), (15, -6), (30, 0), (45, -6), (60, 0)], 80, h=24)
    diff = layer('diff', [
        gr(STEEL, span(192, 242, -61, -55), span(192, 228, 11, 17)),
        gr(RED, span(196, 236, -43, -37)),
        gr(LEAF, span(196, 252, -25, -19), span(196, 240, -7, -1)),
        gr(RED, span(186, 270, -47, -33), o=30),
        gr(LEAF, span(186, 270, -29, -15), span(186, 270, -11, 3), o=26),
        gr(FRAME, span(182, 274, -86, -72)),
        gr(SLATE, span(182, 274, -86, 38), stroke=(FRAME, 4)),
    ], parent='rig', p=K([(0, (0, 0)), (76, (0, 0), 'lin'), (78, (4, 3), 'lin'),
                          (80, (-3, -1), 'lin'), (82, (0, 0)), (op, (0, 0))]))
    scan = layer('scan', [gr(WHITE, span(186, 270, -7, 7), o=16)], parent='diff',
                 o=K([(0, 0), (6, 100), (64, 100), (70, 0), (op, 0)]),
                 p=K([(0, (0, -58)), (8, (0, -58)), (14, (0, -40)), (22, (0, -40)), (28, (0, -22)),
                      (36, (0, -22)), (42, (0, -4)), (50, (0, -4)), (56, (0, 14)),
                      (70, (0, 14), 'hold'), (72, (0, -58))]))
    stamp = layer('stamp', [gr(WHITE, *pixels(CHECK, 6)), gr(GREEN, box(64, 56))],
                  p=(228, -24), r=-10, parent='diff',
                  s=K([(0, 0, 'hold'), (70, (230, 230), 'in'), (76, (100, 100))]),
                  o=K([(0, 0, 'hold'), (70, 0), (73, 100, 'hold'), (104, 100), (112, 0)]))
    look = [(0, (8, -4)), (14, (9, -2)), (28, (9, 0)), (42, (9, 2)), (56, (9, 4)), (76, (9, 0)),
            (90, (0, 0)), (112, (0, 0)), (op, (8, -4))]
    slam = [(0, -30), (62, -30, 'out'), (70, -64, 'in'), (76, -22, 'out'), (84, -30), (op, -30)]
    return cast('Code Reviewer Clawd', op, ox=-47, pos=pos, sc=sc, top=[stamp, scan, diff],
                look=look, arm_r=slam, blink=blinks(op, 106))


# ---- 8 support agent --------------------------------------------------------

def support_agent():
    op = 60
    fade = K([(0, 100, 'hold'), (48, 100), (58, 0)])
    bubble = layer('bubble', [gr(K([(0, BLUE), (38, BLUE), (42, GREEN, 'hold'), (59, BLUE)]),
                               box(110, 70, 40, -43), box(16, 16, 0, -4))],
                   parent='rig', o=fade, s=K([(0, 0, 'hold'), (4, 0, 'back'), (10, 100)]),
                   p=K([(0, (180, -124)), (48, (180, -124), 'in'), (58, (180, -160), 'hold'),
                        (59, (180, -124))]))
    dots = []
    for n in range(3):
        x, keys = 16 + 24 * n, []
        for k in range(3):
            t = 11 + 9 * k + 3 * n
            keys += [(t, (x, -43), 'out'), (t + 3, (x, -52), 'in'), (t + 6, (x, -43))]
        dots.append(layer('dot-%d' % (n + 1), [gr(WHITE, box(12, 12))], p=K(keys),
                          parent='bubble', o=K([(0, 100, 'hold'), (40, 0)])))
    sent = layer('sent', [gr(WHITE, *pixels(CHECK, 6))], p=(40, -43), parent='bubble', o=fade,
                 s=K([(0, 0, 'hold'), (40, 0, 'back'), (46, 100)]))
    look = still((7, -4), op)
    return cast('Support Agent Clawd', op, ox=-50, pos=idle(op, 6),
                top=[sent, *dots, bubble, headset(GREEN, hexc('1B6E49'), NAVY)], look=look,
                blink=blinks(op, 52), arm_l=taps(op, [(11, 38)]),
                arm_r=taps(op, [(11, 38)], first_down=False))


# ---- 9 sales rep ------------------------------------------------------------

def sales_rep():
    op = 60
    bow = layer('bow-tie', [
        gr(NAVY, box(14, 14, 0, -8)),
        gr(BLUE, span(-36, -22, -24, 8), span(-22, -7, -18, 2), span(7, 22, -18, 2),
           span(22, 36, -24, 8)),
    ], parent='bob')
    counter = layer('counter', [gr(hexc('A9743A'), span(180, 264, 36, 46)),
                                gr(WOOD, span(188, 196, 46, 120), span(248, 256, 46, 120))],
                    parent='rig')
    bell = layer('bell', [
        gr(DEEP_GOLD, span(-5, 5, -40, -32), span(-32, 32, -6, 0)),
        gr(GOLD, span(-18, 18, -32, -20), span(-26, 26, -20, -6)),
    ], p=(222, 36), parent='rig',
        s=K([(0, (100, 100)), (20, (100, 100), 'out'), (23, (110, 84)), (30, (100, 100)),
             (op, (100, 100))]))

    def ring(nm, start, end, r):
        return layer(nm, [gr(YELLOW, box(8, 18))], r=r, parent='rig',
                     p=K([(20, start, 'out'), (34, end)]),
                     o=K([(0, 0), (20, 0), (23, 100), (34, 0), (op, 0)]))

    won = layer('plus-one', [gr(GREEN, *pixels([a + '.' + b for a, b in
                                                 zip(GLYPH['+'], GLYPH['1'])], 7))],
                parent='rig', p=K([(24, (222, -62), 'out'), (50, (222, -112))]), **pop(24, 40))
    slap = [(0, -30), (10, -30, 'out'), (16, -58, 'in'), (20, -12, 'out'), (28, -30), (op, -30)]
    pos = K([(0, 0), (12, -6), (20, 0, 'out'), (23, 5), (30, 0), (45, -6), (op, 0)])
    return cast('Sales Rep Clawd', op, ox=-41, pos=pos,
                top=[won, ring('ring-left', (204, -12), (196, -36), -20),
                     ring('ring-mid', (222, -18), (222, -46), 0),
                     ring('ring-right', (240, -12), (248, -36), 20), bell, counter, bow],
                look=still((9, 2), op), blink=blinks(op, 48), arm_r=slap)


# ---- 10 recruiter -----------------------------------------------------------

def recruiter():
    op = 120
    dim = K([(0, 100), (72, 100), (80, 35), (106, 35), (116, 100), (op, 100)])
    up = K([(0, (0, -194)), (72, (0, -194), 'back'), (80, (0, -206)), (106, (0, -206)),
            (116, (0, -194)), (op, (0, -194))])
    cards = [layer('card-%d' % (n + 1), [
        gr(tint, box(18, 18, 0, -20), box(36, 14, 0, -1)),
        gr(LINE, box(40, 6, 0, 20), box(28, 6, 0, 31)),
        gr(PAPER, box(66, 84), stroke=(EDGE, 4)),
    ], p=up if n == 1 else (x, -194), o=100 if n == 1 else dim, parent='rig')
        for n, (x, tint) in enumerate(((-78, BLUE), (0, PINK), (78, GREEN)))]
    ring = layer('ring', [gr(None, box(76, 94), stroke=(
        K([(0, DEEP_BLUE), (70, DEEP_BLUE), (76, GREEN), (106, GREEN), (116, DEEP_BLUE)]), 6))],
        parent='rig',
        p=K([(0, (-78, -194)), (14, (-78, -194)), (22, (0, -194)), (36, (0, -194)),
             (44, (78, -194)), (58, (78, -194)), (66, (0, -194)), (72, (0, -194), 'back'),
             (80, (0, -206)), (106, (0, -206)), (116, (-78, -194)), (op, (-78, -194))]))
    badge = layer('badge', [gr(WHITE, *pixels(CHECK, 3)), gr(GREEN, box(28, 24))],
                  p=(33, -244), parent='rig', **pop(78, 100))
    look = [(0, (-6, -5)), (14, (-6, -5)), (22, (0, -5)), (36, (0, -5)), (44, (6, -5)),
            (58, (6, -5)), (66, (0, -5)), (84, (0, 0)), (106, (0, 0)), (116, (-6, -5)),
            (op, (-6, -5))]
    return cast('Recruiter Clawd', op, oy=14, pos=beat(op, [76]), top=[badge, ring, *cards],
                look=look, arm_l=cheer(op, 78), arm_r=cheer(op, 78), blink=blinks(op, 96))


# ---- 11 legal reviewer ------------------------------------------------------

def legal_reviewer():
    op = 120
    tilt = [(0, -12), (20, -12), (34, 10), (46, -6), (56, 3), (66, 0), (104, 0), (116, -12),
            (op, -12)]

    def pan(nm, side, load):
        return layer(nm, load + [gr(DEEP_GOLD, span(-26, 26, 40, 48), span(-22, -19, 0, 40),
                                    span(19, 22, 0, 40))], parent='rig',
                     p=K([(t, (side * 80, -226 + side * 80 * math.sin(math.radians(a))))
                          for t, a in tilt]))

    beam = layer('beam', [gr(YELLOW, box(176, 8))], p=(0, -226), r=K(tilt), parent='rig')
    post = layer('post', [gr(DEEP_GOLD, box(18, 10, 0, -236), span(-32, 32, -150, -142)),
                          gr(YELLOW, span(-4, 4, -232, -150))], parent='rig')
    contract = [gr(LINE, span(-7, 7, 20, 23), span(-7, 4, 27, 30)),
                gr(PAPER, span(-12, 12, 12, 40), stroke=(EDGE, 3))]
    weight = [gr(FRAME, span(-12, 12, 24, 40), span(-5, 5, 17, 24))]
    fair = layer('fair', [gr(GREEN, *pixels(CHECK, 6))], p=(152, -196), parent='rig',
                 **pop(68, 96))
    look = [(0, (-5, -5)), (20, (-5, -5)), (34, (5, -5)), (46, (-3, -5)), (56, (2, -5)),
            (66, (0, -5)), (74, (0, 0)), (104, (0, 0)), (116, (-5, -5)), (op, (-5, -5))]
    return cast('Legal Reviewer Clawd', op, oy=14, pos=beat(op, [68]),
                top=[fair, pan('pan-left', -1, contract), pan('pan-right', 1, weight), beam, post],
                look=look, arm_r=cheer(op, 70), blink=blinks(op, 90))


# ---- 12 project manager -----------------------------------------------------

def project_manager():
    op = 120
    cols, slots = [-80, 0, 80], [-212, -190, -168]
    tints = [YELLOW, BLUE, GREEN]   # to do, doing, done
    # card: first slot, then moves of (frame, column, slot)
    plan = {'a': (0, [(10, 1, 0), (40, 2, 0)]), 'b': (1, [(30, 1, 1), (64, 2, 1)]),
            'c': (2, [(56, 1, 0), (86, 2, 2)])}
    show = K([(0, 0), (8, 100), (106, 100), (114, 0), (op, 0)])
    cards = []
    for nm, (slot, moves) in plan.items():
        home = cur = (cols[0], slots[slot])
        p, c = [(0, home)], [(0, tints[0])]
        for t, col, s in moves:
            nxt = (cols[col], slots[s])
            p += [(t, cur, 'out'), (t + 6, ((cur[0] + nxt[0]) / 2, min(cur[1], nxt[1]) - 10), 'in'),
                  (t + 12, nxt)]
            c += [(t, tints[col - 1]), (t + 12, tints[col])]
            cur = nxt
        p[-1] += ('hold',)
        c[-1] += ('hold',)
        cards.append(layer('card-' + nm, [gr(K(c + [(118, tints[0])]), box(60, 16))],
                           p=K(p + [(118, home)]), o=show, parent='rig'))
    board = layer('board', [
        gr(TEXT, box(50, 6, -80, -234)), gr(BLUE, box(50, 6, 0, -234)),
        gr(GREEN, box(50, 6, 80, -234)),
        gr(LINE, span(-41, -39, -240, -152), span(39, 41, -240, -152)),
        paper(-122, 122, -246, -146),
    ], parent='rig')
    look = [(0, (-5, -5)), (40, (0, -5)), (70, (4, -5)), (98, (6, -5)), (104, (0, 0)),
            (114, (0, 0)), (op, (-5, -5))]
    return cast('Project Manager Clawd', op, oy=14, pos=beat(op, [100]), top=[*cards, board],
                look=look, arm_l=cheer(op, 100), arm_r=cheer(op, 100), blink=blinks(op, 84))


# ---- 13 product manager -----------------------------------------------------

def product_manager():
    op = 120
    pos, sc = with_hop(op, [(0, 0), (15, -6), (30, 0), (45, -6), (60, 0)], 68, h=24)
    x, (top, mid, low) = 228, (-74, -24, 26)

    def note(nm, tint, r, keys):
        return layer(nm, [gr(TEXT, box(44, 5, 0, -6), box(30, 5, -7, 6), o=55),
                          gr(tint, box(70, 40))], p=K(keys), r=r, parent='rig')

    def over(a, b):
        return (x + 26, (a + b) / 2)

    blue = note('note-blue', hexc('8CBCF7'), -2, [
        (0, (x, low)), (20, (x, low), 'out'), (28, over(low, top), 'in'), (36, (x, top)),
        (100, (x, top), 'out'), (108, over(low, top), 'in'), (116, (x, low)), (op, (x, low))])
    pink = note('note-pink', hexc('F59AB8'), 2, [
        (0, (x, mid)), (20, (x, mid)), (36, (x, low)), (50, (x, low), 'out'),
        (57, over(low, mid), 'in'), (64, (x, mid)), (op, (x, mid))])
    yellow = note('note-yellow', hexc('F7D154'), -3, [
        (0, (x, top)), (20, (x, top)), (36, (x, mid)), (50, (x, mid)), (64, (x, low)),
        (100, (x, low)), (116, (x, top)), (op, (x, top))])
    pin = layer('pin', [gr(hexc('B4232A'), box(6, 6, 2, 2)), gr(RED, box(14, 14))],
                p=(x, top - 16), parent='rig', **pop(68, 92))
    push = [(0, -30)]
    for t in (20, 50, 100):
        push += [(t, -30, 'out'), (t + 6, -46), (t + 14, -30)]
    look = [(0, (9, 4)), (20, (9, 4)), (36, (9, -4)), (64, (9, 0)), (72, (9, -4)), (96, (9, -4)),
            (116, (9, 4)), (op, (9, 4))]
    return cast('Product Manager Clawd', op, ox=-46, pos=pos, sc=sc,
                top=[pin, blue, pink, yellow], look=look, arm_r=push + [(op, -30)],
                blink=blinks(op, 94))


# ---- 14 designer ------------------------------------------------------------

def designer():
    op = 120
    tints = [ORANGE, hexc('E8709A'), hexc('5B93E6'), hexc('43B581')]
    picks, paints = (20, 50, 80, 106), (24, 54, 84, 110)
    skin, sc, point = [(0, tints[0])], [(0, (100, 100))], [(0, -30)]
    for n, t in enumerate(paints):
        skin += [(t, tints[n]), (t + 6, tints[(n + 1) % 4])]
        sc += [(t, (100, 100), 'out'), (t + 3, (106, 94)), (t + 9, (100, 100))]
        point += [(t - 6, -30, 'out'), (t, -56), (t + 9, -30)]
    swatches = []
    for n, tint in enumerate(tints):
        on, off = picks[n - 1], picks[n]   # the frame where it gets big, then small again
        if n == 0:
            keys = [(0, 125), (off, 125), (off + 6, 100), (on, 100, 'back'), (on + 6, 125),
                    (op, 125)]
        else:
            keys = [(0, 100), (on, 100, 'back'), (on + 6, 125), (off, 125), (off + 6, 100),
                    (op, 100)]
        swatches.append(layer('swatch-%d' % (n + 1), [gr(tint, box(40, 40))],
                              p=(-75 + 50 * n, -212), s=K(keys), parent='rig'))
    beret = layer('beret', [
        gr(NAVY, span(10, 18, -172, -162), span(-100, 100, -128, -120)),
        gr(DEEP_BLUE, span(-60, 90, -162, -152), span(-90, 112, -152, -128)),
    ], parent='bob')
    look = [(0, (0, 0)), (18, (0, 0)), (22, (-2, -5)), (32, (0, 0)), (48, (0, 0)), (52, (1, -5)),
            (62, (0, 0)), (78, (0, 0)), (82, (3, -5)), (92, (0, 0)), (102, (0, 0)),
            (106, (-3, -5)), (116, (0, 0)), (op, (0, 0))]
    return cast('Designer Clawd', op, oy=14, pos=idle(op, 6), sc=sc + [(op, (100, 100))],
                top=[*swatches, beret], look=look, arm_r=point + [(op, -30)],
                skin=K(skin + [(op, tints[0])]), blink=blinks(op, 40, 100))


# ---- 15 security analyst ----------------------------------------------------

def security_analyst():
    op = 60
    hits = (12, 30, 48)
    dark = hexc('16171A')
    shades = layer('shades', [
        gr(WHITE, box(8, 8, -94, -82), box(8, 8, -86, -74), box(8, 8, 56, -82),
           box(8, 8, 64, -74), o=75),
        gr(dark, span(-106, -44, -94, -28), span(44, 106, -94, -28), span(-44, 44, -88, -78),
           span(-150, -106, -88, -78), span(106, 150, -88, -78)),
    ], parent='bob')
    pulse, lean = [(0, 100)], [(0, 0)]
    for h in hits:
        pulse += [(h, 100, 'out'), (h + 3, 112), (h + 9, 100)]
        lean += [(h, 0, 'out'), (h + 3, 4), (h + 9, 0)]
    shield = layer('shield', [
        gr(None, box(16, 16, 0, -12), stroke=(WHITE, 5)),
        gr(WHITE, box(26, 20, 0, 4)),
        gr(BLUE, span(-28, 28, -38, 8), span(-22, 22, 8, 22), span(-12, 12, 22, 32)),
        gr(DEEP_BLUE, span(-34, 34, -44, 10), span(-28, 28, 10, 26), span(-18, 18, 26, 38),
           span(-8, 8, 38, 46)),
    ], p=(214, -28), s=K(pulse + [(op, 100)]), parent='bob')
    packets = [layer('packet-%d' % (n + 1), [gr(RED, box(18, 18))], parent='rig',
                     p=K([(h - 10, (334, y), 'lin'), (h, (261, y), 'out'), (h + 12, (304, y + dy))]),
                     r=K([(h, 0), (h + 12, 160)]),
                     o=K([(0, 100, 'hold'), (h, 100), (h + 12, 0)]))
               for n, (h, y, dy) in enumerate(zip(hits, (-52, -14, 16), (-34, 30, 36)))]
    return cast('Security Analyst Clawd', op, ox=-36, pos=K(lean + [(op, 0)]),
                top=[*packets, arm('right'), shield, shades], eyes=[], arm_r=None)


# ---- 16 devops --------------------------------------------------------------

def devops():
    op = 120
    ys = [-16, 20, 56, 92]
    rack = layer('rack', [
        gr(STEEL, *[r for y in ys for r in (span(232, 262, y - 6, y - 2),
                                             span(232, 254, y + 2, y + 6))]),
        gr(hexc('2B2F38'), *[box(68, 26, 230, y) for y in ys]),
        gr(SLATE, span(188, 272, -40, 120), stroke=(FRAME, 4)),
    ], parent='rig')
    alarm = [(n, 100 if i % 2 == 0 else 20, 'hold') for i, n in enumerate(range(30, 72, 4))]
    leds = []
    for n, y in enumerate(ys):
        if n == 1:   # this one fails
            tint = K([(0, LEAF, 'hold'), (30, RED, 'hold'), (72, LEAF)])
            o = K([(0, 100, 'hold')] + alarm + [(72, 100)])
        else:
            a = 14 + 22 * n
            tint = LEAF
            o = K([(0, 100, 'hold'), (a, 30, 'hold'), (a + 4, 100, 'hold'), (a + 40, 30, 'hold'),
                   (a + 44, 100)])
        leds.append(layer('led-%d' % (n + 1), [gr(tint, box(8, 8))], p=(204, y), o=o,
                          parent='rig'))
    alert = layer('alert', [gr(RED, *pixels(GLYPH['!'], 10))], p=(230, -80), parent='rig',
                  s=K([(0, 0, 'hold'), (30, 0, 'back'), (36, 100)]), o=K([(0, 100, 'hold'), (72, 0)]))
    fixed = layer('fixed', [gr(GREEN, *pixels(CHECK, 6))], p=(230, -74), parent='rig',
                  **pop(72, 98))
    pos = K([(0, 0), (15, -6), (30, 0, 'out'), (34, -16, 'in'), (40, 0), (76, 0), (88, -8),
             (100, 0), (op, 0)])
    wide = K([(0, (100, 100)), (30, (100, 100), 'out'), (33, (118, 118)), (44, (100, 100)),
              (104, (100, 100)), (108, (100, 10)), (112, (100, 100)), (op, (100, 100))])
    look = [(0, (0, 0)), (28, (0, 0)), (33, (9, 0)), (72, (9, 2)), (84, (0, 0)), (op, (0, 0))]
    return cast('DevOps Clawd', op, ox=-47, pos=pos, top=[fixed, alert, *leds, rack],
                look=look, blink=wide, arm_l=taps(op, [(46, 70)]),
                arm_r=taps(op, [(46, 70)], first_down=False))


# ---- 17 technical writer ----------------------------------------------------

def technical_writer():
    op = 120
    book = layer('book', [
        gr(hexc('F27BA5'), span(-102, -62, 37, 43)), gr(SKY, span(-94, -38, 51, 57)),
        gr(LEAF, span(-94, -50, 65, 71)), gr(GOLD, span(-102, -72, 79, 85)),
        gr(hexc('E8E6DF'), span(-102, -52, 93, 99)),
        gr(SLATE, span(-110, -10, 26, 106)),
        gr(PAPER, span(-116, -4, 20, 112), span(4, 116, 20, 112)),
        gr(DEEP_BLUE, span(-124, 124, 14, 118)),
    ], parent='rig')
    flip = K([(0, (100, 100)), (100, (100, 100)), (106, (0, 100)), (112, (100, 100)),
              (op, (100, 100))])
    page = layer('page', [gr(PAPER, span(0, 112, 20, 112))], p=(4, 0), s=flip, parent='rig')
    rows = [(52, 88, 22, 34), (64, 80, 38, 50), (76, 90, 54, 66), (88, 60, 70, 80)]
    lines = [layer('line-%d' % n, [gr(TEXT, span(0, w, -3, 3))], p=(10, y), parent='page',
                   s=K([(0, (0, 100), 'hold'), (t0, (0, 100), 'lin'), (t1, (100, 100), 'hold'),
                        (106, (0, 100))]))
             for n, (y, w, t0, t1) in enumerate(rows, 1)]
    title = layer('title', [gr(ORANGE, span(0, 56, -5, 5))], p=(10, 35), parent='page',
                  s=K([(0, (0, 100), 'hold'), (10, (0, 100), 'out'), (18, (100, 100), 'hold'),
                       (106, (0, 100))]))
    ribbon = layer('ribbon', [gr(RED, span(-5, 5, 14, 48))], parent='rig')
    look = [(0, (0, 7)), (10, (3, 7)), (34, (7, 6)), (38, (3, 7)), (50, (7, 7)), (54, (3, 8)),
            (66, (7, 8)), (70, (3, 8)), (80, (6, 8)), (88, (0, 0)), (100, (0, 0)), (op, (0, 7))]
    return cast('Technical Writer Clawd', op, pos=beat(op, [84]),
                top=[ribbon, title, *lines, page, book], look=look, arm_l=20, arm_r=20,
                blink=blinks(op, 96))


# ---- 18 social media manager ------------------------------------------------

def social_media_manager():
    op = 90
    buzzes = (16, 34, 52)
    shake, pos = [(0, 0)], [(0, 0), (8, -5)]
    for n, t in enumerate(buzzes):
        shake += [(t, 0, 'lin'), (t + 2, -5, 'lin'), (t + 4, 5, 'lin'), (t + 6, -3, 'lin'),
                  (t + 8, 0)]
        pos += [(t, 0, 'out'), (t + 3, -9 - 3 * n, 'in'), (t + 9, 0)]
    phone = layer('phone', [
        gr(PINK, *pixels(HEART, 3, -14, 24)),
        gr(LINE, box(22, 5, 10, 24)),
        gr(hexc('F5F4EE'), span(-28, 28, -52, 52)),
        gr(SLATE, span(-34, 34, -62, 62), stroke=(FRAME, 4)),
    ], p=(222, -30), r=K(shake + [(op, 0)]), parent='bob')
    post = layer('post', [gr(WHITE, box(10, 10, 10, -12), o=75), gr(SKY, box(48, 54))],
                 p=(0, -19), parent='phone',
                 s=K([(0, 100), (68, 100, 'in'), (72, 0, 'back'), (80, 100), (op, 100)]))
    badge = layer('badge', [gr(RED, oval(34, 34))], p=(32, -60), parent='phone',
                  s=K([(0, 0, 'hold'), (16, 0, 'back'), (22, 100), (34, 100, 'out'), (37, 130),
                       (42, 100), (52, 100, 'out'), (55, 130), (60, 100), (68, 100, 'in'),
                       (74, 0)]))
    count = [layer('count-%s' % d, [gr(WHITE, *pixels(GLYPH[d], 4))], parent='badge', o=K(o))
             for d, o in (('1', [(0, 100, 'hold'), (34, 0)]),
                          ('2', [(0, 0, 'hold'), (34, 100, 'hold'), (52, 0)]),
                          ('3', [(0, 0, 'hold'), (52, 100, 'hold'), (74, 0)]))]
    tap = [(0, -30), (64, -30, 'out'), (68, -44), (74, -30), (op, -30)]
    return cast('Social Media Manager Clawd', op, ox=-46, pos=K(pos + [(75, -5), (op, 0)]),
                top=[*count, badge, post, phone], look=still((9, 0), op),
                blink=blinks(op, 28, 82), arm_r=tap)


# ---- 19 assistant -----------------------------------------------------------

def assistant():
    op = 120
    pos, sc = with_hop(op, [(0, 0), (15, -6), (30, 0), (45, -6), (60, 0)], 76, h=28)
    booked = [(14, (0, 20), BLUE), (38, (28, 48), PINK), (62, (-28, 76), GREEN)]
    head = layer('calendar', [gr(FRAME, span(-26, -18, -68, -52), span(18, 26, -68, -52)),
                              gr(RED, span(-48, 48, -60, -36))], p=(228, -24), parent='rig')
    page = layer('cal-page', [
        gr(hexc('E7E2D6'), *[box(22, 22, x, y) for y in (20, 48, 76) for x in (-28, 0, 28)]),
        paper(-46, 46, 0, 94),
    ], p=(0, -36), parent='calendar',
        s=K([(0, (100, 100)), (102, (100, 100)), (106, (100, 0)), (110, (100, 100)),
             (op, (100, 100))]))
    slots = [layer('slot-%d' % (n + 1), [gr(tint, box(22, 22))], p=at, parent='cal-page',
                   s=K([(0, 0, 'hold'), (t, 0, 'back'), (t + 6, 100, 'hold'), (106, 0)]))
             for n, (t, at, tint) in enumerate(booked)]
    book = [(0, -30)]
    for t, at, tint in booked:
        book += [(t - 4, -30, 'out'), (t, -46), (t + 8, -30)]
    look = [(0, (0, 0)), (6, (0, 0)), (12, (9, -2)), (38, (9, 0)), (62, (9, 3)), (76, (9, 0)),
            (84, (0, 0)), (op, (0, 0))]
    return cast('Assistant Clawd', op, ox=-47, pos=pos, sc=sc, top=[head, *slots, page],
                look=look, arm_l=cheer(op, 81), arm_r=book + [(op, -30)],
                blink=blinks(op, 108))


# ---- 20 tutor ---------------------------------------------------------------

def tutor():
    op = 120
    chalk = hexc('F5F4EE')
    sums = [('one', '1', -78, 10, chalk), ('plus', '+', -39, 22, chalk),
            ('one-more', '1', 0, 34, chalk), ('equals', '=', 39, 46, chalk),
            ('two', '2', 78, 70, YELLOW)]
    marks = [layer(nm, [gr(tint, *pixels(GLYPH[g], 9))], p=(x, -198), parent='rig',
                   **pop(t, 104)) for nm, g, x, t, tint in sums]
    board = layer('board', [gr(hexc('2D5A45'), span(-110, 110, -242, -154)),
                            gr(WOOD, span(-118, 118, -250, -146))], parent='rig')
    aim = [(0, 57)]
    for nm, g, x, t, tint in sums:
        aim += [(t - 4, 57, 'out'), (t, 49), (t + 5, 57)]
    pointer = layer('pointer', [gr(WHITE, span(-112, -100, -4, 4)),
                                gr(hexc('C99A5B'), span(-100, 0, -4, 4))],
                    p=(165, -50), r=K(aim + [(op, 57)]), parent='bob')
    look = [(0, (0, -5)), (10, (-5, -5)), (22, (-2, -5)), (34, (0, -5)), (46, (3, -5)),
            (70, (5, -5)), (80, (0, 0)), (104, (0, 0)), (op, (0, -5))]
    return cast('Tutor Clawd', op, oy=14, pos=beat(op, [70]), top=[pointer, *marks, board],
                look=look, arm_l=cheer(op, 72), arm_r=-50, blink=blinks(op, 92))


JOBS = [
    ('researcher', researcher), ('writer', writer), ('editor', editor),
    ('translator', translator), ('data-analyst', data_analyst), ('qa-tester', qa_tester),
    ('code-reviewer', code_reviewer), ('support-agent', support_agent),
    ('sales-rep', sales_rep), ('recruiter', recruiter), ('legal-reviewer', legal_reviewer),
    ('project-manager', project_manager), ('product-manager', product_manager),
    ('designer', designer), ('security-analyst', security_analyst), ('devops', devops),
    ('technical-writer', technical_writer), ('social-media-manager', social_media_manager),
    ('assistant', assistant), ('tutor', tutor),
]


def main():
    for name, make in JOBS:
        path = OUT / ('clawd-%s.json' % name)
        path.write_text(json.dumps(make(), separators=(',', ':')))
        print(path.relative_to(OUT.parent), path.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
