"""Rendu SVG de la bannière (animations SMIL uniquement, compatible GitHub)."""
import random
from xml.sax.saxutils import escape

from theme import DOTS, H, ICONS, MONO, PALETTES, SANS, W

LP = (30, 30, 420, 550)            # panneau portrait : x, y, largeur, hauteur
TP = (470, 30, 680, 550)           # panneau terminal
NBSP = " "


def n(x):
    """Nombre compact : 12.50 -> 12.5, 3.0 -> 3."""
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def fade(begin, dy=8, dur=.6):
    return (f'<animate attributeName="opacity" from="0" to="1" begin="{n(begin)}s" dur="{n(dur)}s" fill="freeze"/>'
            f'<animateTransform attributeName="transform" type="translate" from="0 {n(dy)}" to="0 0" begin="{n(begin)}s" '
            f'dur="{n(dur)}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/>')


def float_y(dy, dur, begin=0):
    b = f' begin="{n(begin)}s"' if begin else ""
    return f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {n(dy)};0 0" dur="{n(dur)}s"{b} repeatCount="indefinite"/>'


def blink(attr="opacity"):
    return f'<animate attributeName="{attr}" values="1;0" keyTimes="0;.5" calcMode="discrete" dur="1s" repeatCount="indefinite"/>'


def glass_panel(x, y, w, h, crt=False):
    r = f'x="{x}" y="{y}" width="{w}" height="{h}" rx="20"'
    return (f'<rect {r} fill="url(#glass)" filter="url(#shadow)"/><rect {r} fill="url(#hl)"/>'
            + (f'<rect {r} fill="url(#crt)"/>' if crt else "")
            + f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="19.5" fill="none" stroke="url(#shimmer)"/>')


def hline(x1, x2, y, P, anim=""):
    attrs = f'x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{P["border"]}" stroke-opacity="{n(P["border_op"] * 1.2)}"'
    return f'<line {attrs} opacity="0">{anim}</line>' if anim else f'<line {attrs}/>'


# ---------------------------------------------------------------- définitions
def stop(offset, color, opacity=None, anim=""):
    op = "" if opacity is None else f' stop-opacity="{opacity}"'
    return f'<stop offset="{offset}" stop-color="{color}"{op}>{anim}</stop>' if anim else f'<stop offset="{offset}" stop-color="{color}"{op}/>'


def slide(values, dur, key_times=None):
    """Déplacement continu d'un dégradé."""
    kt = f' keyTimes="{key_times}"' if key_times else ""
    return f'<animateTransform attributeName="gradientTransform" type="translate" values="{values}"{kt} dur="{dur}s" repeatCount="indefinite"/>'


def cycle(*colors):
    return f'<animate attributeName="stop-color" values="{";".join(colors)}" dur="9s" repeatCount="indefinite"/>'


def defs(P):
    a1, a2, a3, g = P["a1"], P["a2"], P["a3"], P["glow"]
    border = lambda o: stop(o, P["border"], P["border_op"])  # noqa: E731
    white = lambda o, op: stop(o, "#FFF", op)                # noqa: E731
    out = [
        f'<style>.m{{font-family:{MONO}}}.s{{font-family:{SANS}}}</style>',
        f'<clipPath id="card"><rect width="{W}" height="{H}" rx="28"/></clipPath>',
        '<linearGradient id="accent">'
        f'{stop(0, a1, anim=cycle(a1, a2, a3, a1))}{stop(.5, a2, anim=cycle(a2, a3, a1, a2))}{stop(1, a3, anim=cycle(a3, a1, a2, a3))}</linearGradient>',
        '<linearGradient id="nameGrad" gradientUnits="userSpaceOnUse" x1="500" x2="900" spreadMethod="reflect">'
        f'{stop(0, P["text"])}{stop(.55, a2)}{stop(1, a1)}{slide("0 0;400 0;0 0", 8)}</linearGradient>',
        '<linearGradient id="asciiGrad" gradientUnits="userSpaceOnUse" x1="40" y1="60" x2="440" y2="520" spreadMethod="reflect">'
        f'{"".join(stop(o, c) for o, c in zip((0, .5, 1), P["asc"]))}{slide("0 0;300 380;0 0", 10)}</linearGradient>',
        f'<linearGradient id="shimmer" gradientUnits="userSpaceOnUse" x2="{W}" y2="{H}">{border(0)}{border(.42)}'
        f'{stop(.5, a2, .9)}{border(.58)}{border(1)}{slide(f"-{W} -{H};{W} {H}", 6)}</linearGradient>',
        f'<linearGradient id="reflect" gradientUnits="userSpaceOnUse" x2="{W}" y2="{int(H * .6)}">'
        f'{white(.46, 0)}{white(.5, P["reflect"])}{white(.54, 0)}{slide(f"-{W} 0;-{W} 0;{W} 0", 9, "0;.55;1")}</linearGradient>',
        f'<linearGradient id="glass" x2="0" y2="1">{stop(0, P["panel"], n(min(1, P["panel_op"] + .08)))}{stop(1, P["panel"], n(P["panel_op"] - .08))}</linearGradient>',
        f'<linearGradient id="hl" x2="0" y2="1">{white(0, P["highlight"])}{white(.25, 0)}</linearGradient>',
        f'<linearGradient id="scanG" x2="0" y2="1">{stop(0, a2, 0)}{stop(.5, a2, P["scan"])}{stop(1, a2, 0)}</linearGradient>',
        f'<pattern id="crt" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{P["text"]}" opacity="{P["crt"]}"/></pattern>',
        f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0V40H0" fill="none" stroke="{P["text"]}" stroke-width=".5"/></pattern>',
        *(f'<radialGradient id="blob{i}">{stop(0, c, op)}{stop(1, c, 0)}</radialGradient>'
          for i, (c, op) in enumerate(P["blobs"])),
        f'<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{n(2.2 * g)}" result="b"/>'
        f'<feComponentTransfer in="b" result="b2"><feFuncA type="linear" slope="{n(.9 * g)}"/></feComponentTransfer>'
        '<feMerge><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        f'<filter id="glowStrong" x="-40%" y="-80%" width="180%" height="260%"><feGaussianBlur stdDeviation="{n(4 * g + 1)}" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>',
        f'<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dy="18" stdDeviation="22" flood-color="{P["shadow"]}" flood-opacity="{P["shadow_op"]}"/></filter>',
        '<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch">'
        '<animate attributeName="baseFrequency" values=".85;.9;.85" dur="2s" repeatCount="indefinite"/></feTurbulence>'
        '<feColorMatrix type="saturate" values="0"/></filter>',
    ]
    return "<defs>" + "".join(out) + "</defs>"


# ---------------------------------------------------------------- fond
def background(P):
    out = [f'<rect width="{W}" height="{H}" fill="{P["bg"]}"/>']
    for i, (cx, cy, r, v, d) in enumerate([(260, 150, 330, "60 40", 18), (900, 420, 360, "-70 -30", 22), (640, 80, 260, "40 60", 16)]):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#blob{i})">'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;{v};0 0" dur="{d}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="r" values="{r};{round(r * 1.12)};{r}" dur="{n(d * .7)}s" repeatCount="indefinite"/></circle>')
    out.append(f'<rect width="{W}" height="{H}" fill="url(#grid)" opacity=".05"/>')
    rnd = random.Random(42)
    for _ in range(26):                                  # particules qui montent
        x, y = rnd.uniform(20, W - 20), rnd.uniform(40, H - 10)
        r, d, b, dy, dx = rnd.uniform(.6, 1.7), rnd.uniform(7, 14), rnd.uniform(0, 8), rnd.uniform(40, 110), rnd.uniform(-15, 15)
        t = f'dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"'
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{P["part"]}" opacity="0">'
                   f'<animate attributeName="opacity" values="0;.7;0" {t}/>'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;{dx:.0f} -{dy:.0f}" {t}/></circle>')
    return "".join(out)


# ---------------------------------------------------------------- panneau portrait
def portrait_panel(P, lines):
    x, y, w, h = LP
    ax, ay, aw, lh = x + 30, y + 70, 360, 9.0
    cw = aw / max(len(l) for l in lines)
    reveal = 2.5
    out = ['<g>', float_y(-4, 7), glass_panel(x, y, w, h, crt=True),
           f'<text class="m" x="{x + 22}" y="{y + 30}" font-size="11.5" fill="{P["muted"]}" letter-spacing=".5">~/portrait.ascii</text>',
           f'<g transform="translate({x + w - 74} {y + 21})"><rect width="54" height="18" rx="9" fill="none" stroke="{P["a3"]}" stroke-opacity=".5"/>'
           f'<circle cx="11" cy="9" r="3" fill="{P["a3"]}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
           f'<text class="m" x="19" y="12.8" font-size="9.5" fill="{P["a3"]}">LIVE</text></g>',
           hline(x + 20, x + w - 20, y + 46, P),
           f'<clipPath id="leftClip"><rect x="{x}" y="{y + 47}" width="{w}" height="{h - 47}" rx="20"/></clipPath>',
           '<g clip-path="url(#leftClip)"><g>', float_y(-5, 5),
           '<g class="m" font-size="7.6" fill="url(#asciiGrad)" filter="url(#glow)">']
    for i, line in enumerate(lines):                     # révélation ligne par ligne
        body = line.strip()
        if not body:
            continue
        lead = len(line) - len(line.lstrip())
        out.append(f'<text x="{n(ax + lead * cw)}" y="{n(ay + i * lh)}" textLength="{n(len(body) * cw)}" lengthAdjust="spacingAndGlyphs" opacity="0">'
                   f'{escape(body).replace(" ", NBSP)}<animate attributeName="opacity" to="1" begin="{n(.4 + i * reveal / len(lines))}s" dur=".25s" fill="freeze"/></text>')
    out += ['</g>',
            f'<rect x="{ax + aw + 4}" y="{ay - 10}" width="7" height="12" fill="{P["a2"]}">'   # curseur qui descend puis clignote
            f'<animate attributeName="y" to="{n(ay + (len(lines) - 1) * lh - 10)}" dur="{reveal}s" begin=".4s" fill="freeze"/>{blink()}</rect>',
            '</g>',
            f'<rect x="{x}" y="{y}" width="{w}" height="70" fill="url(#scanG)"><animate attributeName="y" values="{y - 70};{y + h}" dur="4.5s" repeatCount="indefinite"/></rect>',
            '</g>',
            f'<text class="m" x="{x + 22}" y="{y + h - 20}" font-size="11" fill="{P["muted"]}" opacity="0">'
            f'<tspan fill="{P["a3"]}">✓</tspan> rendered successfully · {len(lines)} lines'
            f'<animate attributeName="opacity" to="1" begin="{n(.4 + reveal)}s" dur=".4s" fill="freeze"/></text>',
            '</g>']
    return "".join(out)


# ---------------------------------------------------------------- rôles tapés
def typed_roles(P, roles, x, y, cw=12.0, start=2.0, type_dt=.075, hold=1.9, erase_dt=.035, gap=.45):
    """Chaque caractère a sa propre animation courte (robuste sur tous les navigateurs)."""
    char_iv, cursor_iv, t = [], {}, 0.0
    for i, role in enumerate(roles):
        L = len(role)
        t_erase = t + L * type_dt + hold
        for k in range(L):
            char_iv.append((i, k, t + (k + 1) * type_dt, t_erase + (L - 1 - k) * erase_dt))
        states = [(t + m * type_dt, m) for m in range(L + 1)] + [(t_erase + j * erase_dt, L - 1 - j) for j in range(L)]
        t = t_erase + L * erase_dt + gap
        for (t0, m), (t1, _) in zip(states, states[1:] + [(t, 0)]):
            cursor_iv.setdefault(m, []).append((t0, t1))
    T = t

    def vis(intervals, attr="opacity"):
        kt, vals = [0.0], ["0"]
        for s0, s1 in sorted(intervals):
            s0, s1 = s0 / T, s1 / T
            if s0 <= kt[-1] + 1e-6:
                vals[-1] = "1"
            else:
                kt.append(s0); vals.append("1")
            if s1 < 1 - 1e-6:
                kt.append(s1); vals.append("0")
        return (f'<animate attributeName="{attr}" values="{";".join(vals)}" keyTimes="{";".join(f"{k:.4f}".rstrip("0").rstrip(".") or "0" for k in kt)}" '
                f'calcMode="discrete" dur="{n(T)}s" begin="{n(start)}s" repeatCount="indefinite"/>')

    out = ['<g class="m" font-size="19" font-weight="600" fill="url(#accent)">']
    for i, role in enumerate(roles):
        spans = []
        for k, ch in enumerate(role):
            if ch == " ":
                spans.append(NBSP)
                continue
            iv = [(s, e) for (j, kk, s, e) in char_iv if j == i and kk == k]
            spans.append(f'<tspan fill-opacity="0">{escape(ch)}{vis(iv, "fill-opacity")}</tspan>')
        out.append(f'<text x="{x}" y="{y}" textLength="{n(len(role) * cw)}" lengthAdjust="spacingAndGlyphs">{"".join(spans)}</text>')
    out.append(f'</g><g fill="{P["a2"]}">{blink()}')
    for m, iv in sorted(cursor_iv.items()):
        out.append(f'<rect x="{n(x + m * cw + 2)}" y="{y - 17}" width="2.5" height="21" opacity="0">{vis(iv)}</rect>')
    return "".join(out) + "</g>"


# ---------------------------------------------------------------- terminal
def terminal(P, cfg):
    x, y, w, h = TP
    cx = x + 34
    out = ['<g>', float_y(-3, 8, 1), glass_panel(x, y, w, h)]
    out += [f'<circle cx="{x + 24 + i * 18}" cy="{y + 22}" r="5.5" fill="{c}" opacity=".9"/>' for i, c in enumerate(DOTS)]
    out += [f'<text class="m" x="{x + w / 2:g}" y="{y + 26}" text-anchor="middle" font-size="11.5" fill="{P["muted"]}">: ~/profile</text>',
            f'<text class="m" x="{x + w - 24}" y="{y + 26}" text-anchor="end" font-size="10.5" fill="{P["muted"]}" opacity=".7">zsh</text>',
            hline(x, x + w, y + 44, P)]

    # ➜ ~ whoami (tapé une fois)
    cmd, cmw = "whoami", 8.4
    steps = range(len(cmd) + 1)
    out += [f'<text class="m" y="{y + 80}" font-size="14"><tspan x="{cx}" fill="{P["a3"]}">➜</tspan><tspan x="{cx + 20}" fill="{P["a2"]}">~</tspan></text>',
            f'<clipPath id="cmdClip"><rect x="{cx + 40}" y="{y + 60}" width="0" height="30">'
            f'<animate attributeName="width" values="{";".join(n(i * cmw) for i in steps)}" keyTimes="{";".join(n(i / len(steps)) for i in steps)}" '
            f'calcMode="discrete" begin=".3s" dur=".6s" fill="freeze"/></rect></clipPath>',
            f'<text class="m" x="{cx + 40}" y="{y + 80}" font-size="14" fill="{P["text"]}" textLength="{n(len(cmd) * cmw)}" lengthAdjust="spacingAndGlyphs" clip-path="url(#cmdClip)">{cmd}</text>']

    # salutation, nom, rôles
    out += [f'<g opacity="0">{fade(1.0)}<text class="s" x="{cx}" y="{y + 122}" font-size="20" fill="{P["muted"]}">{escape(cfg.greeting)}</text></g>',
            f'<g opacity="0">{fade(1.3, 12, .8)}<text class="s" x="{cx - 2}" y="{y + 176}" font-size="50" font-weight="800" letter-spacing="1" fill="url(#nameGrad)" filter="url(#glow)">{escape(cfg.name)}</text></g>',
            f'<g opacity="0">{fade(1.8, 0, .4)}<text class="m" x="{cx}" y="{y + 216}" font-size="19" fill="{P["a1"]}">❯</text>',
            typed_roles(P, cfg.roles, cx + 24, y + 216), '</g>',
            f'<rect x="{cx}" y="{y + 240}" width="0" height="1" fill="url(#accent)" opacity=".6">'
            f'<animate attributeName="width" to="{w - 68}" begin="2.1s" dur="1s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>']

    # infos, une ligne après l'autre
    for i, (k, v) in enumerate(cfg.info):
        b = 2.4 + i * .22
        out.append(f'<g opacity="0">{fade(b, 0, .45)}<animateTransform attributeName="transform" type="translate" from="-10 0" to="0 0" begin="{n(b)}s" dur=".45s" fill="freeze"/>'
                   f'<text class="m" y="{y + 272 + i * 25}" font-size="13.5"><tspan x="{cx}" fill="{P["a2"]}">›</tspan>'
                   f'<tspan x="{cx + 18}" fill="{P["muted"]}">{escape(k)}</tspan><tspan x="{cx + 150}" fill="{P["text"]}">{escape(v)}</tspan></text></g>')

    # compétences
    sy = y + 272 + len(cfg.info) * 25 + 8
    out.append(f'<g opacity="0">{fade(3.6, 0, .4)}<text class="m" x="{cx}" y="{sy}" font-size="11" letter-spacing="2" fill="{P["muted"]}">HARD SKILLS</text></g>')
    px, py = cx, sy + 14
    for i, s in enumerate(cfg.skills):
        pw = len(s) * 7.6 + 30
        if px + pw > x + w - 34:
            px, py = cx, py + 36
            if py > sy + 50:
                print(f"⚠️  trop de compétences : {s!r} passe sur une 3e ligne et chevauche le bas")
        b = 3.8 + i * .09
        r = f'x="{n(px)}" y="{py}" width="{n(pw)}" height="26" rx="13"'
        out.append(f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{n(b)}s" dur=".4s" fill="freeze"/>'
                   f'<animateTransform attributeName="transform" type="translate" from="0 6" to="0 0" begin="{n(b)}s" dur=".4s" fill="freeze"/>'
                   f'<rect {r} fill="{P["pill_bg"]}" fill-opacity=".7" stroke="url(#accent)" stroke-opacity=".55"/>'
                   f'<rect {r} fill="none" stroke="url(#accent)" stroke-width="1.5" filter="url(#glowStrong)" opacity="0">'
                   f'<animate attributeName="opacity" values="0;{P["pulse"]};0" dur="{n(3 + i % 4 * .6)}s" begin="{n(b + .6 + i * .3)}s" repeatCount="indefinite"/></rect>'
                   f'<circle cx="{n(px + 13)}" cy="{py + 13}" r="2.6" fill="url(#accent)"/>'
                   f'<text class="s" x="{n(px + 21)}" y="{n(py + 17.2)}" font-size="12.5" font-weight="500" fill="{P["text"]}">{escape(s)}</text></g>')
        px += pw + 9

    # statut + réseaux
    soy = y + h - 34
    out += [hline(cx, x + w - 34, soy - 27, P, '<animate attributeName="opacity" to="1" begin="4.8s" dur=".5s" fill="freeze"/>'),
            f'<g opacity="0">{fade(5.0, 0, .5)}<text class="m" x="{cx}" y="{soy + 4.5}" font-size="12" fill="{P["muted"]}">'
            f'<tspan fill="{P["a3"]}">●</tspan> {escape(cfg.status)}</text></g>']
    for i, s in enumerate(cfg.socials):
        b = 5.0 + i * .12
        out.append(f'<g opacity="0"><animate attributeName="opacity" to="1" begin="{n(b)}s" dur=".4s" fill="freeze"/>'
                   f'<g transform="translate({x + w - 52 - (len(cfg.socials) - 1 - i) * 46} {soy})">'
                   f'<circle r="17" fill="{P["pill_bg"]}" fill-opacity=".7" stroke="url(#accent)" stroke-opacity=".5"/>'
                   f'<circle r="17" fill="none" stroke="url(#accent)" stroke-width="1.5" filter="url(#glowStrong)" opacity="0">'
                   f'<animate attributeName="opacity" values="0;{P["pulse"] + .05:g};0" dur="3.2s" begin="{n(b + 1 + i * .5)}s" repeatCount="indefinite"/></circle>'
                   + ICONS[s].replace('"C"', f'"{P["text"]}"') + '</g></g>')
    return "".join(out) + "</g>"


# ---------------------------------------------------------------- assemblage
def render(cfg, lines, mode):
    P = PALETTES[mode]
    label = escape(f"{cfg.name} — {cfg.roles[0]}")
    return "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{label}">',
        f'<title>{label}</title>', defs(P),
        '<g clip-path="url(#card)">', background(P), portrait_panel(P, lines), terminal(P, cfg),
        f'<rect width="{W}" height="{H}" fill="url(#reflect)"/>',
        f'<rect width="{W}" height="{H}" filter="url(#noise)" opacity="{P["noise"]}"/>',
        f'<rect width="{W}" height="2" fill="{P["a2"]}" opacity="{P["beam"]}"><animate attributeName="y" values="-2;{H}" dur="7s" repeatCount="indefinite"/></rect>',
        '</g>',
        f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="27.5" fill="none" stroke="url(#shimmer)"/>',
        '</svg>'])