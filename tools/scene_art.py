"""Vector placeholders for the office scene -> <mod>/scene/natural/*.svg.

Usage: scene_art.py <mod>/scene

The natural office: off-white walls, an oak floor, white and wood furniture, green plants,
a muted slate blue for the accents.

Every asset is drawn in scene units (1 unit = U px at runtime) with the floor (or the
thing it stands on) at the bottom edge of its viewBox. scene.ts lists them with the same
w x h; to replace one with a drawn image later, export a PNG of the same aspect ratio and
point its `src` in scene.ts at it.
"""
import os, sys

OUT = f"{sys.argv[1]}/natural"
os.makedirs(OUT, exist_ok=True)

# Colours by role: LAV is the desks, couch and clock; MINT the door, counter, lamp and
# leaves; SKY the water and glass; BUTTER the bells and knobs; PEACH the flower pot; WOOD the
# floor and boxes. The wall and floor drawn as divs are in scene.ts and must match.
INK = "#4a4038"      # outline
SW = 0.45            # stroke width in units
CREAM, CREAM2 = "#fbf8f2", "#e8e1d6"
PINK, PINK2, PINK3 = "#dfe6ee", "#9fb3c8", "#4f6b8a"
LAV, LAV2, LAV3 = "#eceae6", "#d8d3cb", "#8c8478"
MINT, MINT2, MINT3 = "#e3ebe0", "#a9c2a0", "#6f8f69"
SKY, SKY2 = "#d6ecff", "#a9d3f5"
BUTTER, BUTTER2 = "#f6ecc8", "#e2c879"
PEACH, PEACH2 = "#e8c9b0", "#c98f6b"
WOOD, WOOD2 = "#d9b98f", "#c19a6b"
WALL = "#f1ede6"
FLOOR_SHINE = "#e6cba4"
SCREEN_C, SCREEN_C2 = "#2f3a45", "#45525f"
CURTAIN = "#e6e1d8"

def s(fill, extra=""):
    return f'fill="{fill}" stroke="{INK}" stroke-width="{SW}" stroke-linejoin="round" stroke-linecap="round" {extra}'

def write(name, w, h, body, turns=False):
    """<name>.svg faces right. Things that turn around (turns=True, only the cat so far) also
    get <name>_l.svg, their mirror image: Herdr can't flip an element when drawing it."""
    head = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w * 8}" height="{h * 8}">'
    open(f"{OUT}/{name}.svg", "w").write(f"{head}{body}</svg>")
    if turns:
        open(f"{OUT}/{name}_l.svg", "w").write(f'{head}<g transform="translate({w} 0) scale(-1 1)">{body}</g></svg>')

def rect(x, y, w, h, fill, rx=0.6, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" {s(fill, extra)}/>'

def circ(cx, cy, r, fill, stroke=True):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" ' + (s(fill) if stroke else f'fill="{fill}"') + '/>'

# --- desk: front of the desk, drawn over a seated doll. Top surface at height 12. --------
# 29 x 14, placed at desk x + 10 units.
write("desk", 29, 14, "".join([
    rect(0.9, 3, 1.6, 10.6, LAV2, 0.6),                        # left leg; the doll's legs show beside it
    rect(17.6, 3, 10.4, 10.6, LAV, 1),                         # drawer unit
    rect(18.8, 4.4, 8, 3.6, LAV2, 0.8), rect(18.8, 8.6, 8, 3.6, LAV2, 0.8),
    circ(22.8, 6.2, 0.55, PINK3), circ(22.8, 10.4, 0.55, PINK3),
    rect(0.3, 1.4, 28.4, 2.2, CREAM, 1.1),                     # table top
    rect(1.2, 0.4, 7, 1.2, PINK, 0.5),                         # keyboard under her hands (slot x 11-18)
    *[f'<rect x="{2.0 + k * 1.2}" y="0.75" width="0.7" height="0.4" rx="0.15" fill="{PINK3}"/>' for k in range(5)],
]))
DESK_X = 10  # units from the desk slot's left edge

# cat shelf: 14 x 5, a plank on the wall for the cat, top at y 0.6, two brackets under it and
# a paw print on its front. Put up in the gaps between the things on the wall.
def paw(cx, cy, r, fill):
    return (f'<ellipse cx="{cx}" cy="{cy + r * 0.35}" rx="{r * 0.7}" ry="{r * 0.55}" fill="{fill}"/>'
            + "".join(circ(cx + dx * r, cy - 0.55 * r, r * 0.26, fill, False) for dx in (-0.7, -0.24, 0.24, 0.7)))
write("catshelf", 14, 5, "".join([
    f'<path d="M3 2.2 v2.4 l1.8 -2.4 Z" {s(WOOD2)}/>',
    f'<path d="M11 2.2 v2.4 l-1.8 -2.4 Z" {s(WOOD2)}/>',
    rect(0.4, 0.6, 13.2, 1.6, PINK, 0.5),
    paw(7, 1.45, 0.62, PINK3),
]))

# lamp: stands on the desk top, 5 x 9, at slot x 34
write("lamp", 5, 9, "".join([
    f'<path d="M2.5 8.5 L2.5 3.5" stroke="{INK}" stroke-width="{SW * 1.6}" stroke-linecap="round"/>',
    rect(1, 8, 3, 1, MINT2, 0.4),
    f'<path d="M0.4 4 Q2.5 -0.6 4.6 4 Z" {s(MINT)}/>',
    circ(2.5, 1.3, 0.35, PINK2, False),
]))

# monitor: 14 x 13, bottom on the desk top, at slot x 21. Screen hole at (1.6,1.6) 10.8 x 7.4.
SCREEN = (1.6, 1.6, 10.8, 7.4)
write("monitor", 14, 13, "".join([
    # cat ears
    f'<path d="M2 2 L3.2 -0.2 L5 1.6 Z" {s(SCREEN_C)}/>', f'<path d="M12 2 L10.8 -0.2 L9 1.6 Z" {s(SCREEN_C)}/>',
    f'<path d="M2.9 1.4 L3.3 0.6 L4 1.3 Z" fill="{PINK2}"/>', f'<path d="M11.1 1.4 L10.7 0.6 L10 1.3 Z" fill="{PINK2}"/>',
    f'<path d="M0.6 1.2 h12.8 a0.9 0.9 0 0 1 0.9 0.9 v8 a0.9 0.9 0 0 1 -0.9 0.9 h-12.8 a0.9 0.9 0 0 1 -0.9 -0.9 v-8 a0.9 0.9 0 0 1 0.9 -0.9 Z '
    f'M1.6 1.6 v7.4 h10.8 v-7.4 Z" fill-rule="evenodd" {s(SCREEN_C)}/>',
    rect(6, 10.9, 2, 1.2, SCREEN_C, 0.2), rect(4, 12, 6, 0.9, SCREEN_C2, 0.45),
    circ(7, 10.1, 0.35, PINK2, False),
]))

# chair: 12 x 20, behind the seated doll, at slot x 2. Seat top at height 7.
write("chair", 12, 20, "".join([
    f'<path d="M1.4 3.2 L1.6 1 L3 2.4 Z" {s(PINK2)}/>', f'<path d="M4.6 2.4 L5.8 1 L5.9 3.2 Z" {s(PINK2)}/>',
    rect(0.8, 2.2, 5.6, 11, PINK, 2.4),                        # back
    rect(1, 12, 10.4, 2.2, PINK2, 1.1),                        # seat
    rect(5.2, 14.2, 1.6, 3.6, CREAM2, 0.3),
    f'<path d="M1.6 18.6 Q6 16.8 10.4 18.6" fill="none" stroke="{INK}" stroke-width="{SW * 1.6}" stroke-linecap="round"/>',
    circ(1.8, 19.2, 0.6, LAV2), circ(10.2, 19.2, 0.6, LAV2), circ(6, 19.2, 0.6, LAV2),
]))

# couch: 36 x 17, seat top at height 7.
write("couch", 36, 17, "".join([
    rect(2.5, 1, 31, 10, LAV, 3),                              # back
    *[f'<path d="M{x} 2.6 v7" stroke="{LAV2}" stroke-width="0.5" stroke-linecap="round"/>' for x in (12.8, 23.2)],
    rect(2.2, 9.4, 31.6, 4.4, LAV2, 1.6),                      # seat
    rect(0.2, 6.2, 4.2, 8.6, LAV, 2),  rect(31.6, 6.2, 4.2, 8.6, LAV, 2),  # arms
    rect(3.6, 14.6, 1.4, 2, WOOD2, 0.4), rect(31, 14.6, 1.4, 2, WOOD2, 0.4),
]))

# water cooler: 11 x 25
write("cooler", 11, 25, "".join([
    rect(2.6, 0.6, 5.8, 8.6, SKY, 2.4),                        # bottle
    f'<path d="M3.6 2.4 v4.6" stroke="#ffffff" stroke-width="0.6" stroke-linecap="round"/>',
    rect(1, 9, 9, 15.4, CREAM, 1.6),
    rect(2.6, 11.4, 5.8, 3.4, MINT, 0.8),
    circ(4, 13.1, 0.55, PINK3), circ(7, 13.1, 0.55, SKY2),
    rect(2.6, 19, 5.8, 3.6, CREAM2, 0.8),
    rect(9.6, 13, 1.2, 5, "#ffffff", 0.3),
]))

# counter: 36 x 21, top at height 11. On it, left to right: a coffee machine, a plate of
# cookies (the tea-time cake goes here, x 10.5 to 20.5), a tea set, and a dessert case.
COUNTER_TOP = 11
write("counter", 36, 21, "".join([
    rect(0.6, 10.6, 34.8, 10, MINT, 1),
    rect(2, 12.6, 10, 6.8, MINT2, 0.8), rect(13, 12.6, 10, 6.8, MINT2, 0.8), rect(24, 12.6, 10, 6.8, MINT2, 0.8),
    rect(0, 9.6, 36, 1.6, CREAM, 0.8),
    # coffee machine (cat ears), a cup under the spout
    f'<path d="M2.4 2.4 L3.2 0.6 L4.4 2 Z" {s(PINK2)}/>', f'<path d="M8.6 2.4 L7.8 0.6 L6.6 2 Z" {s(PINK2)}/>',
    rect(1.8, 1.6, 7.4, 8, PINK, 1.4),
    rect(3, 3, 5, 2, CREAM, 0.6), circ(4, 4, 0.35, MINT3, False), circ(5.5, 4, 0.35, PINK3, False),
    rect(3.4, 6.2, 4.2, 0.8, CREAM2, 0.3), rect(4.4, 7.6, 2.2, 2, CREAM, 0.4),
    # cookies on a plate
    f'<ellipse cx="15.5" cy="9.4" rx="3.4" ry="0.5" {s(CREAM)}/>',
    circ(14.2, 8.6, 0.8, WOOD2), circ(16, 8.4, 0.8, WOOD), circ(15.1, 7.6, 0.75, WOOD2),
    # tea set: a teapot and a cup on a saucer
    f'<path d="M20.6 6.6 q-1.2 -0.4 -1.5 1.4" fill="none" stroke="{INK}" stroke-width="0.5" stroke-linecap="round"/>',
    f'<path d="M25.6 6.4 q1.4 0.4 0.9 2" fill="none" stroke="{INK}" stroke-width="0.5" stroke-linecap="round"/>',
    f'<ellipse cx="23" cy="7.6" rx="2.6" ry="2" {s(CREAM)}/>',
    f'<path d="M21.2 5.8 q1.8 -1.2 3.6 0 Z" {s(PINK2)}/>', circ(23, 4.8, 0.45, PINK3),
    f'<ellipse cx="23" cy="9.5" rx="2.2" ry="0.35" fill="{CREAM2}"/>',
    # dessert case: two glass shelves of cake slices
    rect(27.2, 2.6, 8, 7, SKY, 0.6, 'fill-opacity="0.55"'),
    f'<path d="M27.4 6.2 h7.6" stroke="{INK}" stroke-width="0.3"/>',
    *[f'<path d="M{x} {y} l1.5 -1.4 l0.2 1.4 Z" {s(c)}/>' for x, y, c in
      [(28, 5.8, PINK2), (30.4, 5.8, BUTTER2), (32.8, 5.8, CREAM), (28.4, 9.2, CREAM), (30.8, 9.2, PINK2), (33.2, 9.2, WOOD2)]],
    rect(26.9, 2.2, 8.6, 0.8, PINK2, 0.4),
]))
# tea time: a cake on the counter, 10 x 5 (bottom on the counter top), and its box, carried, 9 x 3
write("cake", 10, 5, "".join([
    f'<ellipse cx="5" cy="4.6" rx="4.8" ry="0.4" {s(CREAM2)}/>',
    rect(1, 2.4, 8, 2.2, CREAM, 0.6),
    f'<path d="M1 3 q1 0.8 2 0 q1 0.8 2 0 q1 0.8 2 0 q1 0.8 2 0" fill="none" stroke="{PINK2}" stroke-width="0.6" stroke-linecap="round"/>',
    rect(2.6, 0.8, 4.8, 1.7, PINK, 0.6),
    circ(3.6, 0.6, 0.5, "#ef5b6f"), circ(5, 0.5, 0.5, "#ef5b6f"), circ(6.4, 0.6, 0.5, "#ef5b6f"),
]))
write("cake_carry", 9, 3, rect(0.3, 0.3, 8.4, 2.4, CREAM, 0.5) + f'<path d="M4.5 0.3 v2.4" stroke="{PINK3}" stroke-width="0.6"/>')

# bookshelf: 14 x 26, at the right end of the room. Books, and plushies on the shelves.
BOOKS = [PINK2, SKY2, MINT2, BUTTER2, LAV2, PEACH2, PINK3, CREAM2]
def books(x0, y, n, seed):
    out, x = [], x0
    for k in range(n):
        w, h = 0.9 + ((seed + k * 7) % 3) * 0.25, 3.6 + ((seed + k * 5) % 4) * 0.4
        out.append(rect(x, y - h, w, h, BOOKS[(seed + k) % len(BOOKS)], 0.2))
        x += w + 0.1
    return "".join(out)
def bear(cx, by, r, fill):
    """A small plush bear sitting with its bottom at by."""
    return "".join([circ(cx - r * 0.8, by - r * 2.6, r * 0.38, fill), circ(cx + r * 0.8, by - r * 2.6, r * 0.38, fill),
                    f'<ellipse cx="{cx}" cy="{by - r * 0.75}" rx="{r * 0.95}" ry="{r * 0.8}" {s(fill)}/>',
                    circ(cx, by - r * 2.05, r * 0.85, fill),
                    circ(cx - r * 0.3, by - r * 2.1, r * 0.1, INK, False), circ(cx + r * 0.3, by - r * 2.1, r * 0.1, INK, False),
                    f'<ellipse cx="{cx}" cy="{by - r * 1.75}" rx="{r * 0.3}" ry="{r * 0.2}" fill="{CREAM}"/>'])
write("bookshelf", 14, 26, "".join([
    rect(0.4, 0.6, 13.2, 25, LAV, 0.8), rect(1.4, 1.6, 11.2, 23, LAV2, 0.4),
    *[rect(1.2, y, 11.6, 0.8, LAV, 0.3) for y in (7.6, 13.8, 20)],
    books(1.8, 7.6, 6, 1), bear(10.4, 7.6, 1.2, PEACH2),
    bear(3.2, 13.8, 1.1, PINK2), books(5.2, 13.8, 5, 4),  # 5 books fit inside the frame (ends at x 11.7)
    books(1.8, 20, 4, 2), f'<ellipse cx="9.4" cy="18.6" rx="2.2" ry="1.4" {s(CREAM)}/>', circ(10.8, 17.2, 0.9, CREAM),
    circ(11.1, 17, 0.12, INK, False),  # a sleeping plush cat
    rect(0.6, 25, 12.8, 0.8, LAV2, 0.3),
]))

# Desk things, two per character, standing on the desk top (y 10) from slot x 31 to 39: a
# small one in front of the monitor's right corner (x 0 to 3, up to 2.6 tall), a taller one
# beside the monitor (x 4 to 8).
def carton(x, fill, cap):
    return rect(x, 7.4, 2, 2.6, fill, 0.3) + f'<path d="M{x} 7.4 l1 -0.8 l1 0.8" {s(cap)}/>'
def can(x, fill):
    return rect(x, 7.3, 1.6, 2.7, fill, 0.4) + f'<path d="M{x + 0.9} 7.9 l-0.4 0.8 h0.5 l-0.4 0.8" fill="none" stroke="{BUTTER2}" stroke-width="0.3"/>'
def cat_plush(cx, fill):
    return "".join([f'<path d="M{cx - 1.3} 6.2 l0.2 -1.3 l0.9 0.8 Z" {s(fill)}/>', f'<path d="M{cx + 1.3} 6.2 l-0.2 -1.3 l-0.9 0.8 Z" {s(fill)}/>',
                    f'<ellipse cx="{cx}" cy="8.8" rx="1.5" ry="1.2" {s(fill)}/>', circ(cx, 6.6, 1.4, fill),
                    circ(cx - 0.5, 6.6, 0.14, INK, False), circ(cx + 0.5, 6.6, 0.14, INK, False),
                    f'<path d="M{cx - 0.25} 7.1 q0.25 0.25 0.5 0" fill="none" stroke="{INK}" stroke-width="0.15"/>'])
SETS = {
    "jirai": [  # strawberry milk, a bear
        carton(0.4, PINK, PINK2),
        bear(6, 10, 1.15, PINK2),
    ],
    "intern": [  # a juice box, a pencil cup
        carton(0.4, BUTTER2, BUTTER) + f'<path d="M1.8 6.8 v-1.2 l0.6 -0.4" fill="none" stroke="{INK}" stroke-width="0.3"/>',
        *[f'<path d="M{x} 7.4 l{d} -2.6" stroke="{c}" stroke-width="0.45" stroke-linecap="round"/>' for x, d, c in [(5.3, -0.3, PINK3), (5.8, 0, BUTTER2), (6.3, 0.4, SKY2)]],
        rect(4.8, 7.4, 2.2, 2.6, CREAM, 0.3),
    ],
    "designer-cute": [  # a cup of tea, a tulip in a vase
        f'<ellipse cx="1.6" cy="9.8" rx="1.5" ry="0.3" {s(CREAM2)}/>', f'<path d="M0.6 8 h2 l-0.3 1.6 h-1.4 Z" {s(CREAM)}/>',
        f'<path d="M2.6 8.3 q0.7 0.2 0.1 0.9" fill="none" stroke="{INK}" stroke-width="0.3"/>',
        f'<path d="M6 8 Q5.8 5.6 6 4.2" fill="none" stroke="{MINT3}" stroke-width="0.4"/>',
        f'<path d="M5.1 4.6 q0.9 -2 1.8 0 q-0.9 0.8 -1.8 0 Z" {s(PINK2)}/>',
        f'<path d="M5.2 10 q-0.6 -1.6 0.3 -2.4 h1 q0.9 0.8 0.3 2.4 Z" {s(SKY)}/>',
    ],
    "engineer-hoodie": [  # an energy drink, a grey cat plush
        can(0.6, SKY2), cat_plush(6, "#c8c5d6"),
    ],
    "wavy-blouse": [  # a pudding, a hand mirror
        f'<path d="M0.4 8 h2.6 l-0.35 2 h-1.9 Z" {s(BUTTER)}/>', f'<path d="M0.4 8 q1.3 -0.9 2.6 0 Z" {s("#c98a5a")}/>',
        circ(1.7, 7.3, 0.4, PINK3),
        rect(5.6, 7.4, 0.8, 2.6, PINK2, 0.3), circ(6, 5.8, 1.7, PINK2), circ(6, 5.8, 1.15, SKY, False),
        f'<path d="M5.5 5.3 l0.5 -0.4" stroke="#ffffff" stroke-width="0.3" stroke-linecap="round"/>',
    ],
    "twintail-blazer": [  # a cat mug, a photo frame
        f'<path d="M2.6 8.3 q0.9 0.2 0.2 1.1" fill="none" stroke="{INK}" stroke-width="0.3"/>',
        f'<path d="M0.5 7.6 l0.3 -0.8 l0.5 0.8 Z M2.6 7.6 l-0.3 -0.8 l-0.5 0.8 Z" {s(CREAM)}/>',
        rect(0.4, 7.5, 2.3, 2.5, CREAM, 0.3),
        circ(1.15, 8.5, 0.13, INK, False), circ(1.95, 8.5, 0.13, INK, False),
        rect(4.6, 4.8, 3.2, 4.4, PINK2, 0.3), rect(5.1, 5.3, 2.2, 3.4, SKY, 0.2),
        f'<path d="M5.4 9.2 l-0.4 0.8 M7 9.2 l0.4 0.8" stroke="{INK}" stroke-width="0.3" stroke-linecap="round"/>',
    ],
    "bob-jacket": [  # a handheld game, a bunny plush
        rect(0.2, 7.8, 3.2, 2.2, LAV2, 0.5), rect(1.1, 8.15, 1.4, 1.1, MINT, 0.15),
        circ(0.65, 8.9, 0.22, PINK3, False), circ(2.95, 8.7, 0.18, BUTTER2, False), circ(2.95, 9.25, 0.18, SKY2, False),
        f'<path d="M5.3 6.4 q-0.5 -2.6 0.4 -2.8 q0.6 0.4 0.3 2.8 Z" {s(CREAM)}/>',
        f'<path d="M6.7 6.4 q-0.1 -2.6 0.6 -2.8 q0.8 0.3 0 2.8 Z" {s(CREAM)}/>',
        f'<ellipse cx="6.2" cy="8.9" rx="1.6" ry="1.2" {s(CREAM)}/>', circ(6.2, 7, 1.35, CREAM),
        circ(5.7, 7, 0.14, INK, False), circ(6.7, 7, 0.14, INK, False), circ(5.4, 7.4, 0.25, PINK2, False), circ(7, 7.4, 0.25, PINK2, False),
    ],
}
for who, parts in SETS.items():
    write(f"set_{who}", 8, 10, "".join(parts))

# moving box: 7 x 6
write("box", 7, 6, "".join([
    f'<path d="M2.4 1.6 q-0.4 -1.6 0.6 -1.4 q0.8 0.4 0.2 1.4 Z" {s(MINT2)}/>',
    rect(0.3, 1.6, 6.4, 4.1, WOOD, 0.4), f'<path d="M0.3 2.6 h6.4" stroke="{INK}" stroke-width="{SW}"/>',
]))

# plant: 10 x 20
write("plant", 10, 20, "".join([
    f'<path d="M5 13 Q4.6 7 5 3" fill="none" stroke="{MINT3}" stroke-width="0.6"/>',
    *[f'<ellipse cx="{x}" cy="{y}" rx="2.1" ry="1.3" transform="rotate({r} {x} {y})" {s(c)}/>'
      for x, y, r, c in [(3, 9.6, -30, MINT2), (7, 8.4, 30, MINT2), (3.4, 6, -40, MINT), (6.6, 4.8, 40, MINT), (5, 2.4, 0, MINT2)]],
    f'<path d="M1.6 12.6 h6.8 l-0.8 6.8 a0.6 0.6 0 0 1 -0.6 0.5 h-4 a0.6 0.6 0 0 1 -0.6 -0.5 Z" {s(PEACH)}/>',
    rect(1, 12, 8, 1.6, PEACH2, 0.6),
    circ(3.9, 16, 0.3, INK, False), circ(6.1, 16, 0.3, INK, False),
    f'<path d="M4.4 17 q0.6 0.6 1.2 0" fill="none" stroke="{INK}" stroke-width="0.3" stroke-linecap="round"/>',
    circ(3.2, 16.8, 0.4, PINK2, False), circ(6.8, 16.8, 0.4, PINK2, False),
]))

# door: 17 x 29 (bottom at the wall's foot)
def arch(x, y, w, h, fill):
    r = w / 2
    return f'<path d="M{x} {y + h} V{y + r} A{r} {r} 0 0 1 {x + w} {y + r} V{y + h} Z" {s(fill)}/>'
def door(open_):
    inner = (arch(2.2, 2.6, 12.6, 26, SCREEN_C) + rect(2.2, 23.6, 12.6, 5, "#7d6a88", 0.2)) if open_ else "".join([
        arch(2.2, 2.6, 12.6, 26, MINT),
        circ(8.5, 9.4, 3, SKY),
        rect(4.4, 15.4, 8.2, 9.6, MINT2, 1),
        circ(12.6, 17.6, 0.7, BUTTER2),
    ])
    return "".join([arch(0.6, 0.6, 15.8, 28.4, CREAM), inner,
                    f'<path d="M2.2 28.6 h12.6" stroke="{INK}" stroke-width="{SW}"/>'])
write("door", 17, 29, door(False))
write("door_open", 17, 29, door(True))
# a little sign above the door: 12 x 4
write("door_sign", 12, 4, rect(0.3, 0.3, 11.4, 3.4, PINK, 1.6))

# window frame: 30 x 26, a square hole (glass) over the sky divs; the rest is wall colour.
# Glass: x 3..27, y 3..23.
GLASS = (3, 3, 24, 20)
hole = "M3 3 H27 V23 H3 Z"
write("window", 30, 26, "".join([
    f'<path d="M0 0 H30 V26 H0 Z {hole}" fill="{WALL}" fill-rule="evenodd"/>',
    f'<path d="M2.4 1.6 H27.6 Q28.4 1.6 28.4 2.4 V24.4 H1.6 V2.4 Q1.6 1.6 2.4 1.6 Z {hole}" fill-rule="evenodd" {s(CREAM)}/>',
    f'<path d="M15 3.2 V23 M3 15 H27" stroke="{CREAM}" stroke-width="1"/>',
    f'<path d="M15 3.2 V23 M3 15 H27" stroke="{INK}" stroke-width="0.25" stroke-dasharray="0"/>',
    rect(0.6, 23.2, 28.8, 2.2, CREAM2, 1),                     # sill
    # curtains
    f'<path d="M1.2 4 Q5.6 3 6.2 6 Q4 13 7 20 Q3.6 21 1.2 24 Z" {s(CURTAIN)}/>',
    f'<path d="M28.8 4 Q24.4 3 23.8 6 Q26 13 23 20 Q26.4 21 28.8 24 Z" {s(CURTAIN)}/>',
    rect(0.6, 2.4, 28.8, 1.4, LAV2, 0.7),                      # rod
    circ(0.9, 3.1, 0.9, BUTTER2), circ(29.1, 3.1, 0.9, BUTTER2),
]))

# clock: 14 x 16 cat clock with an analog face; the hands are separate files, one per angle,
# laid over the face (clock/h_<0..47>.svg every 15 minutes, clock/m_<0..59>.svg every minute).
import math
write("clock", 14, 16, "".join([
    f'<path d="M2 4.6 L2.6 0.6 L5.6 3 Z" {s(LAV2)}/>', f'<path d="M12 4.6 L11.4 0.6 L8.4 3 Z" {s(LAV2)}/>',
    circ(7, 8.4, 6.4, LAV2), circ(7, 8.4, 5, CREAM),
    *[circ(7 + 4.1 * math.sin(k * math.pi / 6), 8.4 - 4.1 * math.cos(k * math.pi / 6), 0.45 if k % 3 == 0 else 0.25,
           PINK3 if k % 3 == 0 else LAV3, False) for k in range(12)],
    f'<path d="M6 15.6 q1 -1.6 2 0" {s(LAV2)}/>',
]))
os.makedirs(f"{OUT}/clock", exist_ok=True)
def hand(name, angle, length, width, colour):
    x, y = 7 + length * math.sin(angle), 8.4 - length * math.cos(angle)
    open(f"{OUT}/clock/{name}.svg", "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 16" width="112" height="128">'
        f'<path d="M7 8.4 L{x:.2f} {y:.2f}" stroke="{colour}" stroke-width="{width}" stroke-linecap="round"/>'
        f'<circle cx="7" cy="8.4" r="0.7" fill="{PINK3}"/></svg>')
for k in range(48): hand(f"h_{k}", k * math.pi / 24, 2.6, 0.9, INK)
for k in range(60): hand(f"m_{k}", k * math.pi / 30, 3.9, 0.55, LAV3)

# calendar: 13 x 16, the clock's size (drawn at the clock's scale, at the same height). The
# page is x 1.4 to 11.6: a header band y 3.4 to 7 (the month goes there), then the paper (the
# day, then the weekday; scene.ts writes them).
write("calendar", 13, 16, "".join([
    rect(1.4, 3.4, 10.2, 12.2, CREAM, 1.2),
    f'<path d="M1.4 7 V4.6 a1.2 1.2 0 0 1 1.2 -1.2 h7.8 a1.2 1.2 0 0 1 1.2 1.2 V7 Z" {s(PINK3)}/>',
    circ(4, 3.5, 0.45, CREAM2), circ(9, 3.5, 0.45, CREAM2),
    f'<path d="M11.6 13.6 L9.6 15.6 L11.6 15.6 Z" fill="{CREAM2}"/>',  # a page curl
]))

# floor tile 32 x 8 (the wall is a plain div in scene.ts)
write("floor", 32, 8, "".join([
    f'<rect width="32" height="8" fill="{WOOD}"/>',
    f'<path d="M0 7.8 H32 M10 0 V7.8 M26 0 V7.8" stroke="{WOOD2}" stroke-width="0.35"/>',
    f'<path d="M3 3.2 h4" stroke="{FLOOR_SHINE}" stroke-width="0.5" stroke-linecap="round"/>',
    f'<path d="M15 5 h6" stroke="{FLOOR_SHINE}" stroke-width="0.5" stroke-linecap="round"/>',
]))
# rug under the couch area: 40 x 5
write("rug", 40, 5, f'<ellipse cx="20" cy="2.5" rx="19.6" ry="2.3" {s(LAV)}/>'
      f'<ellipse cx="20" cy="2.5" rx="16" ry="1.5" fill="none" stroke="{CREAM}" stroke-width="0.5" stroke-dasharray="1 0.8"/>')

# cat: 14 x 11, facing right. A chubby orange tabby: round body, white belly and muzzle.
CAT, CAT2, CAT3, BELLY = "#ffb15c", "#f08a3c", "#ffd29a", "#fff4e4"
def cat_head(x, y):
    return "".join([
        f'<path d="M{x - 2.8} {y - 0.8} L{x - 2.5} {y - 3.6} L{x - 0.5} {y - 2.3} Z" {s(CAT)}/>',
        f'<path d="M{x + 2.8} {y - 0.8} L{x + 2.5} {y - 3.6} L{x + 0.5} {y - 2.3} Z" {s(CAT)}/>',
        f'<path d="M{x - 2.2} {y - 1.4} L{x - 2.1} {y - 2.9} L{x - 1.1} {y - 2.2} Z" fill="{PINK2}"/>',
        f'<path d="M{x + 2.2} {y - 1.4} L{x + 2.1} {y - 2.9} L{x + 1.1} {y - 2.2} Z" fill="{PINK2}"/>',
        f'<ellipse cx="{x}" cy="{y}" rx="3.4" ry="2.7" {s(CAT)}/>',
        f'<path d="M{x - 0.9} {y - 2.6} v1.1 M{x} {y - 2.7} v1.3 M{x + 0.9} {y - 2.6} v1.1" stroke="{CAT2}" stroke-width="0.4" stroke-linecap="round"/>',
        f'<ellipse cx="{x + 0.1}" cy="{y + 1}" rx="1.5" ry="1" fill="{BELLY}"/>',
        circ(x - 1.2, y - 0.1, 0.38, INK, False), circ(x + 1.4, y - 0.1, 0.38, INK, False),
        circ(x - 1.1, y - 0.25, 0.12, "#ffffff", False), circ(x + 1.5, y - 0.25, 0.12, "#ffffff", False),
        circ(x - 2.1, y + 0.8, 0.45, PINK2, False), circ(x + 2.3, y + 0.8, 0.45, PINK2, False),
        f'<path d="M{x - 0.4} {y + 0.8} q0.4 0.45 0.5 0 q0.1 0.45 0.5 0" fill="none" stroke="{INK}" stroke-width="0.22" stroke-linecap="round"/>',
    ])
def tail(d):
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="{CAT}" stroke-width="1.1" stroke-linecap="round"/>')
write("cat_sit", 14, 11, "".join([
    tail("M3.4 10.2 Q0.6 10.2 0.9 7"),
    f'<ellipse cx="6.4" cy="7.9" rx="4.4" ry="3" {s(CAT)}/>',
    f'<path d="M3.2 6.4 q0.8 0.8 0 1.8 M4.4 5.6 q0.8 0.9 0 2" fill="none" stroke="{CAT2}" stroke-width="0.45" stroke-linecap="round"/>',
    f'<ellipse cx="7.6" cy="8.4" rx="2" ry="2.1" fill="{BELLY}"/>',
    f'<ellipse cx="6.6" cy="10.5" rx="1.1" ry="0.55" {s(CAT3)}/>', f'<ellipse cx="9" cy="10.5" rx="1.1" ry="0.55" {s(CAT3)}/>',
    cat_head(8.2, 4.2),
]), turns=True)
write("cat_sleep", 14, 11, "".join([
    tail("M2.2 10.2 Q0.6 9.6 1.4 8"),
    f'<ellipse cx="6.6" cy="8.3" rx="5.8" ry="2.6" {s(CAT)}/>',
    f'<path d="M3.4 6.2 q0.7 0.9 0 1.8 M5 5.8 q0.7 0.9 0 1.9 M6.6 5.8 q0.7 0.9 0 1.8" fill="none" stroke="{CAT2}" stroke-width="0.45" stroke-linecap="round"/>',
    f'<path d="M9.6 6.8 L9.7 4.8 L11 5.9 Z" {s(CAT)}/>', f'<path d="M12.6 7 L13 5 L11.6 5.9 Z" {s(CAT)}/>',
    f'<ellipse cx="11.2" cy="8" rx="2.6" ry="2.1" {s(CAT)}/>',
    f'<ellipse cx="11.4" cy="8.9" rx="1.3" ry="0.8" fill="{BELLY}"/>',
    f'<path d="M9.9 7.8 q0.45 0.35 0.9 0 M11.6 7.8 q0.45 0.35 0.9 0" fill="none" stroke="{INK}" stroke-width="0.24" stroke-linecap="round"/>',
    circ(12.9, 8.6, 0.4, PINK2, False),
    f'<ellipse cx="9" cy="10.4" rx="1.1" ry="0.5" {s(CAT3)}/>',
]), turns=True)
def cat_walk(k):
    legs = [(4.2, 0.5), (9, -0.5)] if k == 0 else [(4.2, -0.5), (9, 0.5)]
    return "".join([
        *[f'<path d="M{x} 8.6 L{x + d} 10.4" stroke="{INK}" stroke-width="1.5" stroke-linecap="round"/>'
          f'<path d="M{x} 8.6 L{x + d} 10.4" stroke="{CAT}" stroke-width="0.9" stroke-linecap="round"/>' for x, d in legs],
        tail("M2.4 7 Q0.4 5.4 1.2 3.4"),
        f'<ellipse cx="6.6" cy="7.3" rx="4.8" ry="2.9" {s(CAT)}/>',
        f'<path d="M4.4 4.8 q0.7 0.9 0 1.9 M6 4.5 q0.7 0.9 0 2 M7.6 4.6 q0.7 0.9 0 1.9" fill="none" stroke="{CAT2}" stroke-width="0.45" stroke-linecap="round"/>',
        f'<ellipse cx="7" cy="8.9" rx="3.2" ry="1.1" fill="{BELLY}"/>',
        cat_head(10.6, 4.9),
    ])
write("cat_walk_0", 14, 11, cat_walk(0), turns=True)
write("cat_walk_1", 14, 11, cat_walk(1), turns=True)

# interns: stool 9 x 7 (seat top at 7, like the chair) and a laptop on the lap 6 x 4
write("stool", 9, 7, rect(0.4, 0.4, 8.2, 1.6, MINT2, 0.8) + rect(1.4, 2, 1, 4.8, CREAM2, 0.3) + rect(6.6, 2, 1, 4.8, CREAM2, 0.3))
write("laptop", 6, 4, f'<path d="M0.4 3.4 h4.6 L5.6 0.4 L1.2 0.4 Z" {s(LAV)}/>')

print("wrote", len(os.listdir(OUT)), "files to", OUT)
