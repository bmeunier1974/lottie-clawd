#!/usr/bin/env python3
"""Make 20 more job Clawds in animations/: the jobs of an AI agent team.

Run:  python3 tools/make_agent_clawds.py

The parts of Clawd come from make_role_clawds.py. The helpers `cast`, `beat`,
`pop`, `cheer` and `taps` come from make_job_clawds.py.
"""
from make_job_clawds import *  # noqa: F401,F403

PURPLE = hexc('7B4FD6')
CREAM = hexc('E7E2D6')
MUTED = hexc('8A8478')
DARK_RED = hexc('B4232A')
SPARK = ['...X...', '...X...', '..XXX..', 'XXXXXXX', '..XXX..', '...X...', '...X...']
CROSS = ['X...X', '.X.X.', '..X..', '.X.X.', 'X...X']
BOB = [(0, 0), (15, -6), (30, 0), (45, -6), (60, 0)]


def shown(until=106):
    """Opacity keys: there from the start, gone 8 frames after `until`."""
    return K([(0, 100, 'hold'), (until, 100), (until + 8, 0)])


def stroke_path(points, tint, w, end=None, dash=None):
    """A line through the points. `end` draws it on, from 0 to 100."""
    n = len(points)
    line = {"ty": "st", "nm": "stroke", "c": prop(tint, 'c'), "o": {"a": 0, "k": 100},
            "w": {"a": 0, "k": w}, "lc": 1, "lj": 1, "ml": 4}
    if dash:
        line["d"] = [{"n": "d", "nm": "dash", "v": {"a": 0, "k": dash[0]}},
                     {"n": "g", "nm": "gap", "v": {"a": 0, "k": dash[1]}},
                     {"n": "o", "nm": "offset", "v": {"a": 0, "k": 0}}]
    it = [{"ty": "sh", "nm": "path", "d": 1,
           "ks": {"a": 0, "k": {"i": [[0, 0]] * n, "o": [[0, 0]] * n,
                                "v": [list(p) for p in points], "c": False}}}]
    if end is not None:
        it.append({"ty": "tm", "nm": "trim", "s": {"a": 0, "k": 0}, "e": prop(end, '1'),
                   "o": {"a": 0, "k": 0}, "m": 1})
    it += [line, {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                  "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0},
                  "o": {"a": 0, "k": 100}}]
    return {"ty": "gr", "nm": "line", "it": it}


def slam(op, *hits, base=-30):
    """Arm keys: lift the arm, then bring it down hard at each hit."""
    keys = [(0, base)]
    for t in hits:
        keys += [(t - 12, base, 'out'), (t - 6, base - 32, 'in'), (t, base + 8, 'out'),
                 (t + 8, base)]
    return keys + [(op, base)]


# ---- 1 prompt engineer ------------------------------------------------------

def prompt_engineer():
    op = 120
    card = layer('prompt', [gr(TEXT, span(-116, -70, -218, -210)),
                            paper(-126, -14, -232, -160)], parent='rig')
    adds = [layer('add-%d' % n, [gr(tint, span(0, w, -4, 4))], p=(-116, y), parent='rig',
                  o=shown(), s=K([(0, (0, 100), 'hold'), (t0, (0, 100), 'lin'), (t1, (100, 100))]))
            for n, (y, w, tint, t0, t1) in enumerate([(-198, 88, ORANGE, 14, 26),
                                                      (-182, 64, TEXT, 28, 38)], 1)]
    dots = [layer('dot-%d' % (n + 1), [gr(MUTED, box(8, 8))], p=(6 + 14 * n, -196), parent='rig',
                  o=K([(0, 25, 'hold'), (42 + 3 * n, 100, 'hold'), (58, 25)])) for n in range(3)]
    edge = K([(0, FRAME), (50, FRAME), (54, GREEN), (106, GREEN), (114, FRAME)])
    tile = layer('answer', [gr(SLATE, box(76, 76, 88, -196), stroke=(edge, 4))], parent='rig')
    meh = layer('meh', [gr(STEEL, *pixels(CROSS, 7))], p=(88, -196), parent='rig',
                o=K([(0, 100, 'hold'), (50, 0, 'hold'), (108, 0), (116, 100)]))
    best = layer('best', [gr(YELLOW, *pixels(SPARK, 7))], p=(88, -196), parent='rig',
                 o=shown(), s=K([(0, 0, 'hold'), (50, 0, 'back'), (57, 100)]))
    look = [(0, (-6, -5)), (40, (-6, -5)), (50, (6, -5)), (70, (6, -5)), (80, (0, 0)),
            (108, (0, 0)), (op, (-6, -5))]
    joy = [(56, -30, 'out'), (63, -62, 'in'), (70, -30)]
    return cast('Prompt Engineer Clawd', op, oy=14, pos=beat(op, [56]),
                top=[best, meh, tile, *dots, *adds, card], look=look,
                arm_l=taps(op, [(14, 38)], after=joy),
                arm_r=taps(op, [(14, 38)], first_down=False, after=joy))


# ---- 2 agent orchestrator ---------------------------------------------------

def agent_orchestrator():
    op = 120
    base = -184
    crew, chips, aim = [], [], [(0, 70)]
    for n, (x, cue, encore, angle) in enumerate(((-84, 12, 84, 40), (0, 36, 87, 57),
                                                 (84, 60, 90, 74))):
        keys = [(0, (x, base))]
        for t in (cue, encore):
            keys += [(t, (x, base), 'out'), (t + 5, (x, base - 18), 'in'), (t + 10, (x, base))]
        crew.append(layer('helper-%d' % (n + 1), [
            gr(INK, box(6, 12, -15, -12), box(6, 12, 15, -12)),
            gr(ORANGE, box(60, 36, 0, -6), box(6, 12, -33, -6), box(6, 12, 33, -6),
               *[box(6, 12, lx, 18) for lx in (-21, -9, 9, 21)]),
        ], p=K(keys + [(op, (x, base))]), parent='rig'))
        chips.append(layer('task-%d' % (n + 1), [
            gr(K([(0, LINE), (cue + 6, LINE), (cue + 12, GREEN), (108, GREEN), (116, LINE)]),
               span(x - 22, x + 22, -150, -144))], parent='rig'))
        aim += [(cue - 6, 70, 'out'), (cue, angle), (cue + 12, 70)]
    aim += [(80, 70, 'out'), (86, 50), (98, 70), (op, 70)]
    shelf = layer('shelf', [gr(EDGE, span(-120, 120, -160, -154))], parent='rig')
    baton = layer('baton', [gr(WHITE, span(-104, -92, -3, 3)),
                            gr(hexc('C99A5B'), span(-92, 0, -3, 3))],
                  p=(165, -50), r=K(aim), parent='bob')
    look = [(0, (0, -5)), (8, (-6, -5)), (30, (0, -5)), (54, (6, -5)), (78, (0, -5)),
            (100, (0, 0)), (112, (0, 0)), (op, (0, -5))]
    return cast('Agent Orchestrator Clawd', op, oy=14, pos=beat(op, [86]),
                top=[baton, *crew, *chips, shelf], look=look, arm_r=-50,
                arm_l=cheer(op, 88), blink=blinks(op, 104))


# ---- 3 red teamer -----------------------------------------------------------

def red_teamer():
    op = 120
    pos, sc = with_hop(op, BOB, 66, h=24)
    bricks = []
    for n, y in enumerate((108, 82, 56, 30, 4, -22)):
        cuts = ((190, 230), (234, 274)) if n % 2 == 0 else ((190, 208), (212, 252), (256, 274))
        bricks += [span(x0, x1, y - 12, y + 12) for x0, x1 in cuts if (x0, y) != (212, 30)]
    wall = layer('wall', [gr(STEEL, *bricks)], parent='rig')
    home = (232, 30)
    weak = layer('weak-brick', [gr(K([(0, STEEL), (56, STEEL), (60, RED, 'hold'), (98, GREEN),
                                      (108, GREEN), (116, STEEL)]), box(40, 24))], parent='rig',
                 p=K([(0, home), (66, home, 'in'), (78, (244, 120), 'hold'), (98, home)]),
                 r=K([(0, 0), (66, 0, 'in'), (78, 35, 'hold'), (98, 0)]),
                 o=K([(0, 100, 'hold'), (66, 100), (78, 0, 'hold'), (100, 0), (108, 100)]))
    stops = [(210, 108), (232, 82), (254, 56), home]
    probe = layer('probe', [gr(None, box(46, 30), stroke=(RED, 5))], parent='rig',
                  o=K([(0, 0), (4, 100), (60, 100), (64, 0), (op, 0)]),
                  p=K([(0, stops[0]), (8, stops[0]), (14, stops[1]), (24, stops[1]),
                       (30, stops[2]), (40, stops[2]), (46, stops[3]), (64, stops[3], 'hold'),
                       (66, stops[0])]))
    found = layer('found', [gr(YELLOW, *pixels(GLYPH['!'], 10))], p=(232, -76), parent='rig',
                  **pop(68, 92))
    hood = layer('hood', [
        gr(RED, span(-156, 156, -108, -102)),
        gr(DARK_RED, span(-22, 22, -150, -136), span(-156, 156, -136, -102),
           span(-156, -150, -102, -64), span(150, 156, -102, -64)),
    ], parent='bob')
    jab = [(0, -30)]
    for t in (8, 24, 40, 56):
        jab += [(t, -30, 'out'), (t + 3, -42), (t + 8, -30)]
    look = [(0, (9, 8)), (14, (9, 6)), (30, (9, 3)), (46, (9, 1)), (78, (9, 6)), (88, (0, 0)),
            (110, (0, 0)), (op, (9, 8))]
    return cast('Red Teamer Clawd', op, ox=-46, pos=pos, sc=sc,
                top=[found, probe, weak, wall, hood], look=look, arm_r=jab + [(op, -30)],
                blink=blinks(op, 96))


# ---- 4 fact checker ---------------------------------------------------------

def fact_checker():
    op = 120
    x, y = 228, -26

    def claim(nm, p, o):
        return layer(nm, [gr(TEXT, span(-32, 24, -20, -13), span(-32, 32, -6, 1),
                             span(-32, 8, 8, 15)), paper(-44, 44, -36, 36)],
                     p=K(p), o=K(o), parent='rig')

    first = claim('claim-1', [(0, (x, y)), (44, (x, y), 'in'), (54, (x, y - 50), 'hold'),
                              (108, (x, y + 40), 'out'), (118, (x, y)), (op, (x, y))],
                  [(0, 100), (44, 100), (54, 0), (108, 0), (118, 100), (op, 100)])
    second = claim('claim-2', [(0, (x, y + 40), 'hold'), (56, (x, y + 40), 'out'), (66, (x, y)),
                               (98, (x, y), 'in'), (108, (x, y - 50))],
                   [(0, 0, 'hold'), (56, 0), (66, 100), (98, 100), (108, 0)])

    def stamp(nm, parent, tint, rows, u, r, t, out):
        return layer(nm, [gr(WHITE, *pixels(rows, u)), gr(tint, box(56, 46))], r=r,
                     parent=parent, s=K([(0, 0, 'hold'), (t, (230, 230), 'in'), (t + 6, (100, 100))]),
                     o=K([(0, 0, 'hold'), (t, 0), (t + 3, 100, 'hold'), (out, 100),
                          (out + 10, 0)]))

    true = stamp('true', 'claim-1', GREEN, CHECK, 5, -10, 22, 44)
    false = stamp('false', 'claim-2', RED, CROSS, 6, 8, 76, 98)
    pos = K([(0, 0), (14, -6), (28, 0, 'out'), (31, 4), (37, 0), (52, -6), (66, 0),
             (82, 0, 'out'), (85, 4), (91, 0), (105, -6), (op, 0)])
    look = [(0, (9, -3)), (10, (9, 1)), (22, (9, -1)), (60, (9, -1)), (66, (9, -3)),
            (76, (9, 1)), (op, (9, -3))]
    return cast('Fact Checker Clawd', op, ox=-46, pos=pos, top=[true, first, false, second],
                look=look, arm_r=slam(op, 28, 82), blink=blinks(op, 48, 104))


# ---- 5 meeting scribe -------------------------------------------------------

def meeting_scribe():
    op = 120
    speech = layer('speech', [
        gr(WHITE, span(-50, 44, -30, -24), span(-50, 30, -18, -12), span(-50, 48, -6, 0),
           span(-50, 20, 6, 12), span(-50, 40, 18, 24), o=88),
        gr(STEEL, box(124, 84), box(16, 16, 30, 46)),
    ], p=(-70, -200), parent='rig',
        s=K([(0, 0, 'hold'), (4, 0, 'back'), (10, 100), (40, 100), (46, 78), (54, 78), (60, 56),
             (68, 56), (76, 0)]))
    pad = layer('pad', [gr(FRAME, *[box(6, 10, x, -248) for x in range(56, 117, 15)]),
                        paper(46, 126, -244, -152)], parent='rig')
    notes = [layer('note-%d' % (n + 1), [gr(ORANGE, box(8, 8, 4, 0)),
                                         gr(TEXT, span(14, 14 + w, -3, 3))],
                   p=(54, y), parent='rig', o=shown(104),
                   s=K([(0, (0, 100), 'hold'), (t, (0, 100), 'out'), (t + 8, (100, 100))]))
             for n, (y, w, t) in enumerate(((-222, 48, 40), (-198, 38, 54), (-174, 44, 68)))]
    look = [(0, (0, 0)), (6, (-6, -5)), (36, (-6, -5)), (42, (6, -5)), (78, (6, -5)),
            (88, (0, 0)), (op, (0, 0))]
    joy = [(80, -30, 'out'), (87, -62, 'in'), (94, -30)]
    return cast('Meeting Scribe Clawd', op, oy=14, pos=beat(op, [80]),
                top=[*notes, pad, speech], look=look, arm_l=taps(op, [(38, 76)], after=joy),
                arm_r=taps(op, [(38, 76)], first_down=False, after=joy),
                blink=blinks(op, 100))


# ---- 6 librarian ------------------------------------------------------------

def librarian():
    op = 120

    def book(x0, w, h, tint):
        return [gr(WHITE, span(x0 + 4, x0 + w - 4, -142 - h, -136 - h), o=70),
                gr(tint, span(x0, x0 + w, -152 - h, -152))]

    row = [(-108, 22, 64, BLUE), (-84, 18, 56, RED), (-64, 26, 70, NAVY), (-36, 20, 60, YELLOW),
           (-14, 24, 66, PINK), (34, 28, 72, DEEP_BLUE), (64, 18, 54, MAGENTA),
           (84, 24, 62, PURPLE)]
    shelf = layer('shelf', [s for b in row for s in book(*b)] +
                  [gr(WOOD, span(-116, 116, -152, -144))], parent='rig')
    pick = layer('pick', book(12, 20, 58, GREEN), parent='rig',
                 p=K([(0, (0, 0)), (50, (0, 0), 'back'), (58, (0, -26)), (98, (0, -26)),
                      (108, (0, 0)), (op, (0, 0))]))
    stops = [-97, -51, -2, 22]
    finger = layer('finger', [gr(YELLOW, *pixels(['XXXXX', '.XXX.', '..X..'], 5))], parent='rig',
                   o=K([(0, 0), (4, 100), (46, 100), (52, 0), (op, 0)]),
                   p=K([(0, (stops[0], -242)), (8, (stops[0], -242)), (14, (stops[1], -242)),
                        (22, (stops[1], -242)), (28, (stops[2], -242)), (36, (stops[2], -242)),
                        (42, (stops[3], -242)), (54, (stops[3], -242), 'hold'),
                        (56, (stops[0], -242))]))
    shine = layer('shine', [gr(YELLOW, *pixels(SPARK, 4))], p=(50, -246), parent='rig',
                  **pop(60, 90))
    look = [(0, (-6, -5)), (8, (-6, -5)), (14, (-3, -5)), (28, (0, -5)), (42, (2, -5)),
            (70, (2, -5)), (80, (0, 0)), (108, (0, 0)), (op, (-6, -5))]
    return cast('Librarian Clawd', op, oy=14, pos=beat(op, [58]),
                top=[shine, finger, pick, shelf], look=look, arm_r=cheer(op, 60),
                blink=blinks(op, 94))


# ---- 7 database admin -------------------------------------------------------

def database_admin():
    op = 120
    pos, sc = with_hop(op, BOB, 72, h=24)
    tops = (18, 54, 90)
    disks = layer('database', [gr(SKY, *[span(190, 270, t, t + 8) for t in tops]),
                               gr(BLUE, *[span(190, 270, t + 8, t + 30) for t in tops])],
                  parent='rig')
    reads = [layer('read-%d' % (n + 1), [gr(WHITE, span(190, 270, t, t + 30))], parent='rig',
                   o=K([(0, 0), (22 + 6 * n, 0), (25 + 6 * n, 70), (33 + 6 * n, 0), (op, 0)]))
             for n, t in enumerate(tops)]
    query = layer('query', [gr(ORANGE, box(12, 12))], parent='rig',
                  p=K([(10, (184, -30), 'in'), (22, (230, 20))]),
                  o=K([(0, 0, 'hold'), (10, 100, 'hold'), (22, 0)]))
    table = layer('table', [gr(LINE, *[span(194, 266, y - 4, y + 4) for y in (-72, -58, -44, -30)]),
                            gr(FRAME, span(186, 274, -96, -84)), paper(186, 274, -96, -22)],
                  parent='rig')
    scan = layer('scan', [gr(BLUE, span(190, 270, -6, 6), o=24)], parent='rig',
                 o=K([(0, 0), (38, 0), (42, 100), (62, 100), (66, 0), (op, 0)]),
                 p=K([(0, (0, -72)), (40, (0, -72)), (46, (0, -58)), (52, (0, -58)),
                      (58, (0, -44)), (70, (0, -44), 'hold'), (72, (0, -72))]))
    hit = layer('hit', [gr(GREEN, span(0, 72, -4, 4))], p=(194, -44), parent='rig', o=shown(104),
                s=K([(0, (0, 100), 'hold'), (62, (0, 100), 'out'), (70, (100, 100))]))
    look = [(0, (0, 0)), (10, (8, 2)), (22, (9, 7)), (38, (9, 7)), (44, (9, -4)), (62, (9, -2)),
            (84, (0, 0)), (op, (0, 0))]
    return cast('Database Admin Clawd', op, ox=-46, pos=pos, sc=sc,
                top=[hit, scan, table, query, *reads, disks], look=look,
                arm_l=taps(op, [(2, 11)]), arm_r=taps(op, [(2, 11)], first_down=False),
                blink=blinks(op, 100))


# ---- 8 data engineer --------------------------------------------------------

def data_engineer():
    op = 60

    def block(nm, x, tint, r):
        return layer(nm, [gr(tint, box(20, 20))], r=r, parent='rig',
                     p=K([(0, (x, -188), 'lin'), (op, (x + 80, -188))]))

    raw = [block('raw-%d' % (n + 1), x, MUTED, r)
           for n, (x, r) in enumerate(((-280, 20), (-200, -15), (-120, 35)))]
    clean = [block('clean-%d' % (n + 1), x, GREEN, 0) for n, x in enumerate((40, 120, 200))]
    rail = layer('rail', [gr(STEEL, span(-256, 256, -176, -170))], parent='rig')
    machine = layer('machine', [gr(SLATE, box(44, 44, 0, -198)),
                                gr(BLUE, span(-56, 56, -236, -226)),
                                gr(DEEP_BLUE, span(-56, 56, -236, -164))], parent='rig')
    gear = layer('gear', [gr(SLATE, oval(10, 10)), gr(SKY, box(24, 24)),
                          gr(SKY, box(24, 24), r=45)], p=(0, -198), parent='rig',
                 r=K([(0, 0, 'lin'), (op, 90)]))
    crank_l = [(0, -30), (15, -42), (30, -30), (45, -18), (op, -30)]
    crank_r = [(0, -30), (15, -18), (30, -30), (45, -42), (op, -30)]
    look = [(0, (-6, -5), 'lin'), (48, (6, -5)), (op, (-6, -5))]
    return cast('Data Engineer Clawd', op, oy=14, pos=idle(op, 6),
                top=[gear, machine, *raw, *clean, rail], look=look, arm_l=crank_l,
                arm_r=crank_r, blink=blinks(op, 54))


# ---- 9 software architect ---------------------------------------------------

def software_architect():
    op = 120
    sheet = layer('blueprint', [
        gr(SKY, *[box(4, 4, x, y) for x in range(-100, 101, 40) for y in (-232, -198, -164)],
           o=45),
        gr(hexc('234E9E'), span(-120, 120, -250, -146)),
    ], parent='rig')

    def part(nm, x, y, t):
        return layer(nm, [gr(WHITE, box(60, 28), o=14, stroke=(WHITE, 4))], p=(x, y),
                     parent='rig', **pop(t, 106))

    def wire(nm, x, t):
        return layer(nm, [stroke_path([(x, -208), (x, -170), (30 if x > 0 else -30, -170)],
                                      WHITE, 4, end=K([(0, 0, 'hold'), (t, 0, 'lin'),
                                                       (t + 12, 100)]))],
                     o=shown(), parent='rig')

    core = layer('core', [gr(ORANGE, box(52, 20))], p=(0, -170), parent='rig', **pop(80, 106))
    look = [(0, (0, -5)), (8, (-5, -6)), (22, (5, -6)), (36, (0, -4)), (62, (4, -5)),
            (80, (0, -4)), (90, (0, 0)), (110, (0, 0)), (op, (0, -5))]
    point = [(0, -30)]
    for t in (8, 22, 36):
        point += [(t - 4, -30, 'out'), (t, -50), (t + 8, -30)]
    return cast('Software Architect Clawd', op, oy=14, pos=beat(op, [80]),
                top=[core, part('box-a', -70, -222, 8), part('box-b', 70, -222, 22),
                     part('box-c', 0, -170, 36), wire('wire-a', -70, 48), wire('wire-b', 70, 62),
                     sheet],
                look=look, arm_r=point + [(82, -30, 'out'), (89, -62, 'in'), (96, -30), (op, -30)],
                arm_l=cheer(op, 82), blink=blinks(op, 100))


# ---- 10 release manager -----------------------------------------------------

def release_manager():
    op = 120
    pos, sc = with_hop(op, BOB, 66, h=24)
    pad_at = (232, 108)
    rocket = layer('rocket', [
        gr(SKY, box(14, 14, 0, -52)),
        gr(RED, span(-8, 8, -96, -84), span(-14, 14, -84, -72), span(-32, -20, -30, 0),
           span(20, 32, -30, 0)),
        gr(hexc('AEB8C9'), span(-20, 20, -72, -10)),
        gr(FRAME, span(-12, 12, -10, 0)),
    ], s=(130, 130), parent='rig',
        p=K([(0, pad_at), (56, pad_at, 'lin'), (58, (235, 108), 'lin'), (60, (229, 108), 'lin'),
             (62, (234, 108), 'lin'), (64, pad_at, 'in'), (88, (232, -380), 'hold'),
             (100, pad_at)]),
        o=K([(0, 100, 'hold'), (88, 0, 'hold'), (102, 0), (112, 100)]))
    flicker = [(t, (100, 100 if n % 2 else 135), 'lin') for n, t in enumerate(range(56, 89, 3))]
    flame = layer('flame', [gr(YELLOW, span(-6, 6, 0, 16)), gr(ORANGE, span(-10, 10, 0, 26))],
                  parent='rocket', s=K(flicker), o=K([(0, 0, 'hold'), (56, 100, 'hold'), (88, 0)]))
    pad = layer('pad', [gr(FRAME, span(196, 268, 108, 120))], parent='rig')

    def puff(nm, start, end):
        return layer(nm, [gr(LINE, box(26, 20))], parent='rig',
                     p=K([(60, start, 'out'), (84, end)]), s=K([(60, 100, 'out'), (84, 190)]),
                     o=K([(0, 0, 'hold'), (60, 90), (84, 0)]))

    count = [layer('count-' + d, [gr(YELLOW, *pixels(GLYPH[d], 9))], p=(232, -84), parent='rig',
                   s=K([(0, 0, 'hold'), (t, 0, 'back'), (t + 5, 100)]),
                   o=K([(0, 100, 'hold'), (t + 16, 0)]))
             for d, t in (('3', 10), ('2', 26), ('1', 42))]
    look = [(0, (0, 0)), (8, (9, -3)), (62, (9, 0)), (84, (7, -8)), (96, (0, 0)), (op, (0, 0))]
    return cast('Release Manager Clawd', op, ox=-46, pos=pos, sc=sc,
                top=[*count, puff('smoke-left', (208, 104), (186, 94)),
                     puff('smoke-right', (256, 104), (280, 94)), rocket, flame, pad],
                look=look, arm_r=slam(op, 58), blink=blinks(op, 104))


# ---- 11 IT helpdesk ---------------------------------------------------------

def it_helpdesk():
    op = 120
    desk = layer('desk', [gr(FRAME, span(226, 238, 18, 34), span(212, 252, 30, 34)),
                          gr(hexc('A9743A'), span(182, 282, 34, 44)),
                          gr(WOOD, span(190, 198, 44, 120), span(266, 274, 44, 120))],
                 parent='rig')
    case = layer('monitor', [gr(SLATE, span(186, 278, -56, 18), stroke=(FRAME, 4))], parent='rig')
    broken = layer('screen-error', [gr(WHITE, *pixels(CROSS, 6, 232, -19)),
                                    gr(RED, span(192, 272, -50, 12))], parent='rig',
                   o=K([(0, 100, 'hold'), (36, 0, 'hold'), (112, 100)]))
    boot = K([(0, 0, 'hold'), (62, 100, 'hold'), (86, 0)])
    track = layer('boot-track', [gr(FRAME, span(204, 260, -23, -15))], o=boot, parent='rig')
    fill = layer('boot-fill', [gr(LEAF, span(0, 56, -4, 4))], p=(204, -19), o=boot, parent='rig',
                 s=K([(0, (0, 100), 'hold'), (64, (0, 100), 'lin'), (84, (100, 100))]))
    fine = layer('screen-ok', [gr(WHITE, *pixels(CHECK, 6, 232, -19)),
                               gr(GREEN, span(192, 272, -50, 12))], parent='rig',
                 o=K([(0, 0, 'hold'), (86, 100, 'hold'), (112, 0)]))
    power = layer('power', [gr(FRAME, span(230, 234, 44, 92)),
                            gr(CREAM, span(212, 252, 104, 120), stroke=(EDGE, 3))], parent='rig')
    plug = layer('plug', [gr(FRAME, span(222, 242, 90, 106))], parent='rig',
                 p=K([(0, (0, 0)), (28, (0, 0), 'out'), (34, (0, -16)), (56, (0, -16), 'in'),
                      (62, (0, 0)), (op, (0, 0))]))
    reach = [(0, -30), (24, -30), (30, -10), (36, -30), (52, -30), (58, -10), (64, -30),
             (op, -30)]
    jump = K([(0, (100, 100)), (40, (100, 100)), (44, (100, 10)), (48, (100, 100)),
              (112, (100, 100), 'out'), (115, (116, 116)), (op, (100, 100))])
    look = [(0, (9, 0)), (24, (9, 0)), (30, (9, 7)), (60, (9, 7)), (66, (9, 0)), (92, (0, 0)),
            (108, (0, 0)), (114, (9, 0)), (op, (9, 0))]
    return cast('IT Helpdesk Clawd', op, ox=-48, pos=beat(op, [88]),
                top=[fine, fill, track, broken, case, plug, power, desk], look=look,
                arm_r=reach, blink=jump)


# ---- 12 financial analyst ---------------------------------------------------

def financial_analyst():
    op = 120
    panel = layer('chart', [gr(TEXT, span(-106, -103, -240, -158), span(-106, 106, -161, -158)),
                            paper(-120, 120, -250, -146)], parent='rig')
    actual = layer('actual', [stroke_path(
        [(-98, -172), (-70, -190), (-44, -180), (-14, -204), (14, -196), (40, -214)], BLUE, 6,
        end=K([(0, 0, 'hold'), (8, 0, 'lin'), (50, 100)]))], o=shown(), parent='rig')
    forecast = layer('forecast', [stroke_path(
        [(40, -214), (68, -224), (98, -238)], GREEN, 6, dash=(8, 7),
        end=K([(0, 0, 'hold'), (56, 0, 'lin'), (78, 100)]))], o=shown(), parent='rig')
    target = layer('target', [gr(GREEN, box(14, 14))], p=(98, -238), parent='rig', **pop(78, 106))
    look = [(0, (-6, -4)), (8, (-6, -4), 'lin'), (50, (2, -6), 'lin'), (78, (6, -7)),
            (90, (0, 0)), (110, (0, 0)), (op, (-6, -4))]
    return cast('Financial Analyst Clawd', op, oy=14, pos=beat(op, [80]),
                top=[target, forecast, actual, panel], look=look, arm_l=cheer(op, 82),
                arm_r=cheer(op, 82), blink=blinks(op, 100))


# ---- 13 compliance officer --------------------------------------------------

def compliance_officer():
    op = 120
    pos, sc = with_hop(op, [(0, 0), (15, -6), (30, 0), (45, -6)], 54, h=24)
    lamps = ((-62, RED, 0, 20), (-17, YELLOW, 20, 50), (28, LEAF, 50, 100))
    post = layer('light', [
        *[gr(tint, oval(34, 34, 230, y), o=22) for y, tint, on, off in lamps],
        gr(SLATE, span(202, 258, -96, 62), stroke=(FRAME, 4)),
        gr(FRAME, span(226, 234, 62, 112), span(210, 250, 112, 120)),
    ], parent='rig')
    lit = []
    for n, (y, tint, on, off) in enumerate(lamps):
        o = [(0, 100, 'hold'), (off, 0, 'hold'), (100, 100)] if on == 0 else \
            [(0, 0, 'hold'), (on, 100, 'hold'), (off, 0)]
        s = [(0, 100)] + ([(on, 100, 'out'), (on + 3, 126), (on + 10, 100)] if on else []) + \
            [(op, 100)]
        lit.append(layer('lamp-%d' % (n + 1), [gr(tint, oval(34, 34))], p=(230, y), o=K(o),
                         s=K(s), parent='rig'))
    badge = layer('badge', [
        gr(DEEP_GOLD, box(10, 10, -104, -2)),
        gr(YELLOW, span(-116, -92, -14, 8), span(-112, -96, 8, 16), span(-108, -100, 16, 22)),
    ], parent='bob')
    look = [(0, (9, -3)), (20, (9, -1)), (50, (9, 2)), (64, (0, 0)), (96, (0, 0)),
            (104, (9, -3)), (op, (9, -3))]
    return cast('Compliance Officer Clawd', op, ox=-44, pos=pos, sc=sc, top=[*lit, post, badge],
                look=look, arm_l=taps(op, [(4, 18), (30, 48)]),
                arm_r=taps(op, [(4, 18), (30, 48)], first_down=False), blink=blinks(op, 90))


# ---- 14 buyer ---------------------------------------------------------------

def buyer():
    op = 120
    rail = layer('rail', [gr(STEEL, span(-116, 116, -254, -249))], parent='rig')
    dim = K([(0, 100), (62, 100), (70, 35), (104, 35), (114, 100), (op, 100)])
    tags = []
    for n, (x, d) in enumerate(((-80, '3'), (0, '2'), (80, '1'))):
        a = 3 if n % 2 == 0 else -3
        best = n == 2
        back = K([(0, PAPER), (62, PAPER), (68, GREEN), (104, GREEN), (112, PAPER)]) if best \
            else PAPER
        ink = K([(0, TEXT), (62, TEXT), (68, WHITE), (104, WHITE), (112, TEXT)]) if best else TEXT
        tags.append(layer('tag-%d' % (n + 1), [
            gr(FRAME, box(8, 8, 0, 26)),
            gr(ink, *pixels(GLYPH[d], 7, 0, 60)),
            gr(back, span(-30, 30, 16, 94), stroke=(EDGE, 4)),
            gr(STEEL, span(-1.5, 1.5, 0, 16)),
        ], p=(x, -249), parent='rig', o=100 if best else dim,
            r=K([(0, a), (30, -a), (60, a), (90, -a), (op, a)]),
            s=K([(0, 100), (62, 100, 'back'), (70, 110), (104, 110), (112, 100), (op, 100)])
            if best else (100, 100)))
    ring = layer('ring', [gr(None, box(72, 90), stroke=(
        K([(0, DEEP_BLUE), (60, DEEP_BLUE), (66, GREEN), (104, GREEN), (114, DEEP_BLUE)]), 6))],
        parent='rig', o=K([(0, 100), (58, 100), (64, 0), (104, 0), (112, 100), (op, 100)]),
        p=K([(0, (-80, -194)), (14, (-80, -194)), (22, (0, -194)), (36, (0, -194)),
             (44, (80, -194)), (104, (80, -194)), (116, (-80, -194)), (op, (-80, -194))]))
    look = [(0, (-6, -5)), (14, (-6, -5)), (22, (0, -5)), (36, (0, -5)), (44, (6, -5)),
            (74, (6, -5)), (84, (0, 0)), (104, (0, 0)), (116, (-6, -5)), (op, (-6, -5))]
    return cast('Buyer Clawd', op, oy=14, pos=beat(op, [64]), top=[ring, *tags, rail],
                look=look, arm_l=cheer(op, 66), arm_r=cheer(op, 66), blink=blinks(op, 94))


# ---- 15 customer success ----------------------------------------------------

FACES = {
    'sad': ['.......', '.X...X.', '.X...X.', '.......', '.XXXXX.', 'X.....X', '.......'],
    'flat': ['.......', '.X...X.', '.X...X.', '.......', '.......', '.XXXXX.', '.......'],
    'glad': ['.......', '.X...X.', '.X...X.', '.......', 'X.....X', '.XXXXX.', '.......'],
}


def customer_success():
    op = 120
    pos, sc = with_hop(op, [(0, 0), (15, -6), (30, 0), (45, -6)], 56, h=24)
    frame = layer('meter', [paper(212, 248, -70, 96)], parent='rig')
    level = layer('level', [gr(K([(0, RED), (20, RED), (28, YELLOW), (52, YELLOW), (60, GREEN),
                                  (104, GREEN), (114, RED)]), span(-12, 12, -158, 0))],
                  p=(230, 92), parent='rig',
                  s=K([(0, (100, 20)), (20, (100, 20), 'back'), (28, (100, 58)),
                       (52, (100, 58), 'back'), (60, (100, 100)), (104, (100, 100)),
                       (114, (100, 20)), (op, (100, 20))]))
    moods = [layer('mood-' + nm, [gr(tint, *pixels(FACES[nm], 6))], p=(230, -100), parent='rig',
                   o=K(o))
             for nm, tint, o in (('sad', RED, [(0, 100, 'hold'), (24, 0, 'hold'), (112, 100)]),
                                 ('flat', YELLOW, [(0, 0, 'hold'), (24, 100, 'hold'), (56, 0)]),
                                 ('glad', GREEN, [(0, 0, 'hold'), (56, 100, 'hold'), (112, 0)]))]
    care = [layer('care-%d' % (n + 1), [gr(PINK, *pixels(HEART, 4))], parent='rig',
                  p=K([(t, (176, -74), 'out'), (t + 12, (214, y))]),
                  o=K([(0, 0, 'hold'), (t, 100, 'hold'), (t + 12, 0)]))
            for n, (t, y) in enumerate(((8, 50), (40, -6)))]
    wave = [(0, -30)]
    for t in (8, 40):
        wave += [(t - 6, -30, 'out'), (t, -56), (t + 10, -30)]
    look = [(0, (9, 4)), (20, (9, 4)), (28, (9, 0)), (52, (9, 0)), (60, (9, -5)), (72, (0, 0)),
            (104, (0, 0)), (112, (9, 4)), (op, (9, 4))]
    return cast('Customer Success Clawd', op, ox=-44, pos=pos, sc=sc,
                top=[*care, *moods, level, frame], look=look, arm_r=wave + [(op, -30)],
                arm_l=cheer(op, 61), blink=blinks(op, 96))


# ---- 16 community moderator -------------------------------------------------

def community_moderator():
    op = 120

    def message(nm, x, tint, inner, **keys):
        return layer(nm, inner + [gr(tint, box(70, 56), box(14, 14, 0, 32))], p=(x, -200),
                     parent='rig', **keys)

    lines = [gr(WHITE, span(-22, 22, -12, -6), span(-22, 8, 2, 8), o=90)]
    left = message('message-left', -80, BLUE, lines)
    right = message('message-right', 80, PURPLE, lines)
    rude = message('message-bad', 0, RED,
                   [gr(WHITE, *pixels(['X.X.X.X', '.X.X.X.', 'X.X.X.X'], 6))],
                   s=K([(0, 0, 'hold'), (14, 0, 'back'), (20, 100), (36, 100, 'in'), (46, 0)]),
                   r=K([(0, 0), (20, 0, 'lin'), (23, -6, 'lin'), (26, 6, 'lin'), (29, -4, 'lin'),
                        (32, 0), (36, 0, 'in'), (46, 60)]))
    kind = message('message-good', 0, GREEN, [gr(WHITE, *pixels(HEART, 5))], **pop(56, 104))
    look = [(0, (0, 0)), (14, (0, -6)), (46, (0, -6)), (52, (0, 0)), (58, (0, -5)), (74, (0, 0)),
            (op, (0, 0))]
    return cast('Community Moderator Clawd', op, oy=14, pos=beat(op, [60]),
                top=[kind, rude, left, right], look=look, arm_r=slam(op, 36),
                arm_l=cheer(op, 62), blink=blinks(op, 92))


# ---- 17 SEO specialist ------------------------------------------------------

def seo_specialist():
    op = 120
    pos, sc = with_hop(op, BOB, 70, h=24)
    x, (one, two, three) = 238, (-52, -22, 8)
    page = layer('results', [
        gr(TEXT, box(6, 6, 200, -81), *pixels(GLYPH['1'], 3, 198, one),
           *pixels(GLYPH['2'], 3, 198, two), *pixels(GLYPH['3'], 3, 198, three)),
        gr(CREAM, span(192, 268, -88, -74)),
        paper(184, 276, -96, 40),
    ], parent='rig')

    def result(nm, tint, keys):
        return layer(nm, [gr(tint, span(-28, 28, -7, 7))], p=K(keys), parent='rig')

    ours = result('our-page', ORANGE, [
        (0, (x, three)), (24, (x, three), 'out'), (31, (x + 8, (two + three) / 2), 'in'),
        (38, (x, two)), (54, (x, two), 'out'), (61, (x + 8, (one + two) / 2), 'in'),
        (68, (x, one)), (100, (x, one)), (114, (x, three)), (op, (x, three))])
    second = result('result-2', LINE, [(0, (x, two)), (24, (x, two)), (38, (x, three)),
                                       (100, (x, three)), (114, (x, two)), (op, (x, two))])
    first = result('result-1', LINE, [(0, (x, one)), (54, (x, one)), (68, (x, two)),
                                      (100, (x, two)), (114, (x, one)), (op, (x, one))])
    top_spot = layer('top-spot', [gr(YELLOW, *pixels(SPARK, 4))], p=(272, -104), parent='rig',
                     **pop(70, 92))
    look = [(0, (9, 4)), (24, (9, 4)), (38, (9, 1)), (54, (9, 1)), (68, (9, -3)), (84, (0, 0)),
            (104, (0, 0)), (114, (9, 4)), (op, (9, 4))]
    push = [(0, -30)]
    for t in (24, 54):
        push += [(t, -30, 'out'), (t + 6, -46), (t + 14, -30)]
    return cast('SEO Specialist Clawd', op, ox=-48, pos=pos, sc=sc,
                top=[top_spot, ours, second, first, page], look=look,
                arm_r=push + [(op, -30)], blink=blinks(op, 98))


# ---- 18 UX researcher -------------------------------------------------------

def ux_researcher():
    op = 120
    pos, sc = with_hop(op, BOB, 80, h=22)
    window = layer('window', [
        gr(LINE, span(190, 250, -8, -3), span(190, 236, 2, 7)),
        gr(CREAM, span(190, 270, -78, -58), span(190, 226, -52, -16), span(234, 270, -52, -16)),
        gr(LINE, span(182, 278, -96, -84)),
        paper(182, 278, -96, 44),
    ], parent='rig')
    button = layer('button', [gr(K([(0, BLUE), (76, BLUE), (80, GREEN), (106, GREEN),
                                    (114, BLUE)]), span(232, 270, 18, 36))], parent='rig')
    arrow = ['X....', 'XX...', 'XXX..', 'XXXX.', 'XXXXX', 'XXX..', 'X.XX.', '..XX.']
    cursor = layer('cursor', [gr(INK, *pixels(arrow, 4, 10, 16))], parent='rig',
                   p=K([(0, (200, -72)), (8, (200, -72)), (20, (248, -40)), (32, (206, -30)),
                        (40, (212, -4)), (44, (202, 0), 'lin'), (48, (220, -2), 'lin'),
                        (52, (204, 2), 'lin'), (56, (212, 0)), (64, (212, 0)), (76, (248, 22)),
                        (104, (248, 22)), (116, (200, -72)), (op, (200, -72))]))
    flag = layer('flag', [gr(DARK_RED, box(4, 10, 0, 10)), gr(RED, box(14, 14))], p=(196, 20),
                 parent='rig', **pop(58, 104))
    click = layer('click', [gr(None, box(46, 26), stroke=(GREEN, 4))], p=(251, 27), parent='rig',
                  s=K([(78, 100, 'out'), (90, 160)]), o=K([(0, 0, 'hold'), (78, 100), (90, 0)]))
    look = [(0, (8, -6)), (20, (9, -3)), (32, (8, -2)), (40, (8, 1)), (64, (8, 1)), (76, (9, 3)),
            (92, (0, 0)), (108, (0, 0)), (op, (8, -6))]
    return cast('UX Researcher Clawd', op, ox=-48, pos=pos, sc=sc,
                top=[click, cursor, flag, button, window], look=look,
                arm_r=taps(op, [(56, 66)]), blink=blinks(op, 100))


# ---- 19 travel planner ------------------------------------------------------

def travel_planner():
    op = 120
    stops = [(-80, -178), (4, -222), (80, -188)]
    world = layer('map', [
        gr(hexc('BFD9A6'), span(-112, -40, -206, -154), span(-30, 40, -244, -196),
           span(44, 112, -214, -160)),
        gr(hexc('CFE4F5'), span(-120, 120, -250, -146), stroke=(EDGE, 4)),
    ], parent='rig')
    pins = [layer('pin-%d' % (n + 1), [gr(DARK_RED, box(4, 8, 0, 9)), gr(RED, box(14, 14))],
                  p=at, parent='rig', **pop(10 + 14 * n, 106)) for n, at in enumerate(stops)]
    route = layer('route', [stroke_path(stops, TEXT, 4, dash=(7, 6),
                                        end=K([(0, 0, 'hold'), (44, 0, 'lin'), (68, 100)]))],
                  o=shown(), parent='rig')
    plane = layer('plane', [gr(DEEP_BLUE, span(-14, 14, -3, 3), span(-3, 3, -12, 12),
                               span(-14, -10, -7, 7))], parent='rig',
                  p=K([(0, stops[0], 'hold'), (70, stops[0], 'lin'), (84, stops[1], 'lin'),
                       (98, stops[2])]),
                  r=K([(0, -28, 'hold'), (82, -28), (86, 24)]),
                  o=K([(0, 0, 'hold'), (68, 100, 'hold'), (98, 100), (106, 0)]))
    look = [(0, (0, -5)), (10, (-5, -5)), (24, (0, -6)), (38, (5, -5)), (70, (-5, -5)),
            (84, (0, -6)), (98, (5, -5)), (108, (0, 0)), (op, (0, -5))]
    point = [(0, -30)]
    for t in (10, 24, 38):
        point += [(t - 4, -30, 'out'), (t, -50), (t + 8, -30)]
    return cast('Travel Planner Clawd', op, oy=14, pos=beat(op, [98]),
                top=[plane, *pins, route, world], look=look, arm_r=point + [(op, -30)],
                arm_l=cheer(op, 100), blink=blinks(op, 60))


# ---- 20 game master ---------------------------------------------------------

def game_master():
    op = 90
    pos, sc = with_hop(op, [(0, 0), (15, -6), (30, 0)], 48, h=18)
    hat = layer('hat', [
        gr(YELLOW, span(-70, 70, -146, -134), box(10, 10, 12, -170), box(8, 8, -8, -194)),
        gr(PURPLE, span(-110, 110, -134, -120), span(-70, 70, -158, -134),
           span(-46, 46, -182, -158), span(-24, 24, -206, -182), span(-8, 8, -224, -206)),
    ], parent='bob')
    hand = (196, -36)
    die = layer('die', [gr(PAPER, box(48, 48), stroke=(EDGE, 4))], parent='rig',
                p=K([(0, hand), (8, hand, 'out'), (22, (232, -120), 'in'), (34, (238, 96), 'out'),
                     (40, (242, 72), 'in'), (46, (244, 96), 'hold'), (84, hand)]),
                r=K([(0, 0, 'hold'), (8, 0, 'lin'), (46, 720, 'hold'), (84, 0)]),
                o=K([(0, 100, 'hold'), (74, 100), (82, 0, 'hold'), (84, 0), (op, 100)]))
    a, b = -13, 13
    sides = [('1', [(0, 0)], [(0, 100, 'hold'), (14, 0, 'hold'), (84, 100)]),
             ('5', [(a, a), (b, a), (0, 0), (a, b), (b, b)],
              [(0, 0, 'hold'), (14, 100, 'hold'), (22, 0)]),
             ('3', [(a, a), (0, 0), (b, b)], [(0, 0, 'hold'), (22, 100, 'hold'), (30, 0)]),
             ('6', [(a, a), (b, a), (a, 0), (b, 0), (a, b), (b, b)],
              [(0, 0, 'hold'), (30, 100, 'hold'), (74, 100), (82, 0)])]
    faces = [layer('face-' + nm, [gr(INK, *[oval(9, 9, x, y) for x, y in dots])], parent='die',
                   o=K(o)) for nm, dots, o in sides]
    crit = layer('crit', [gr(YELLOW, *pixels(SPARK, 5))], p=(244, 38), parent='rig',
                 **pop(48, 68))
    toss = [(0, -30), (4, -22, 'out'), (9, -54), (18, -30), (op, -30)]
    look = [(0, (8, 0)), (8, (8, 0)), (22, (8, -7)), (34, (9, 7)), (52, (9, 7)), (60, (0, 0)),
            (84, (0, 0)), (op, (8, 0))]
    return cast('Game Master Clawd', op, ox=-44, oy=16, pos=pos, sc=sc,
                top=[crit, *faces, die, hat], look=look, arm_r=toss, blink=blinks(op, 72))


JOBS = [
    ('prompt-engineer', prompt_engineer), ('agent-orchestrator', agent_orchestrator),
    ('red-teamer', red_teamer), ('fact-checker', fact_checker),
    ('meeting-scribe', meeting_scribe), ('librarian', librarian),
    ('database-admin', database_admin), ('data-engineer', data_engineer),
    ('software-architect', software_architect), ('release-manager', release_manager),
    ('it-helpdesk', it_helpdesk), ('financial-analyst', financial_analyst),
    ('compliance-officer', compliance_officer), ('buyer', buyer),
    ('customer-success', customer_success), ('community-moderator', community_moderator),
    ('seo-specialist', seo_specialist), ('ux-researcher', ux_researcher),
    ('travel-planner', travel_planner), ('game-master', game_master),
]


def main():
    for name, make in JOBS:
        path = OUT / ('clawd-%s.json' % name)
        path.write_text(json.dumps(make(), separators=(',', ':')))
        print(path.relative_to(OUT.parent), path.stat().st_size, 'bytes')


if __name__ == '__main__':
    main()
