import math, random

COLS, ROWS = 56, 36
PW, PH = 360.0, 450.0  # pixel space covered by the ascii block
RAMP = " .,:;-=+*#%@"


def portrait():
    random.seed(7)
    cw, ch = PW / COLS, PH / ROWS
    lines = []
    L = (-0.55, -0.65, 0.52)  # light dir (upper-left, toward viewer)
    ln = math.sqrt(sum(c * c for c in L)); L = tuple(c / ln for c in L)
    for r in range(ROWS):
        row = []
        for c in range(COLS):
            x = (c + 0.5) * cw
            y = (r + 0.5) * ch
            v = None
            # shoulders / torso
            sx, sy = (x - 180) / 170, (y - 480) / 150
            if sx * sx + sy * sy < 1 and y > 300:
                nz = math.sqrt(max(0, 1 - sx * sx - sy * sy))
                v = 0.25 + 0.55 * max(0, (sx * L[0] + sy * L[1] + nz * L[2]))
                # collar / turtleneck folds
                if abs(x - 180) < 52 and y < 340:
                    v = 0.55 + 0.25 * math.sin(y / 4.0)
            # neck
            if 146 < x < 214 and 240 < y < 320:
                nx = (x - 180) / 34
                v = 0.35 + 0.4 * max(0, nx * L[0] + 0.6)
            # head
            hx, hy = (x - 180) / 80, (y - 165) / 100
            d = hx * hx + hy * hy
            if d < 1:
                nz = math.sqrt(1 - d)
                v = 0.2 + 0.8 * max(0, hx * L[0] + hy * L[1] + nz * L[2])
                # hair: curly top
                hair_line = -0.38 + 0.12 * math.sin(hx * 9)
                if hy < hair_line or (hy < 0.1 and abs(hx) > 0.86):
                    v = 0.55 + 0.35 * (0.5 + 0.5 * math.sin(x / 3.1) * math.cos(y / 2.7))
                # eyebrows / eyes
                for ex in (-0.38, 0.38):
                    if abs(hx - ex) < 0.2 and abs(hy - (-0.12)) < 0.045:
                        v = 0.95
                    if abs(hx - ex) < 0.13 and abs(hy - 0.0) < 0.05:
                        v = 0.08
                # nose shadow
                if abs(hx - 0.06) < 0.06 and 0.05 < hy < 0.32:
                    v = max(0.1, v - 0.35)
                # mouth / smile
                if abs(hy - (0.48 + 0.25 * hx * hx)) < 0.04 and abs(hx) < 0.32:
                    v = 0.1
                # rim
                if d > 0.86:
                    v = max(v, 0.7)
            # ears
            for exc in (100, 260):
                if ((x - exc) / 12) ** 2 + ((y - 175) / 24) ** 2 < 1 and v is None:
                    v = 0.5
            if v is None:
                row.append("." if random.random() < 0.025 else " ")
            else:
                v = min(0.999, max(0.0, v + random.uniform(-0.05, 0.05)))
                row.append(RAMP[1 + int(v * (len(RAMP) - 1))] if v > 0.02 else " ")
        lines.append("".join(row).replace("@@@", "@#@"))
    return lines


if __name__ == "__main__":
    for l in portrait():
        print(l)