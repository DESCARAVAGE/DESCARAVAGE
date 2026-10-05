"""Génère dark.svg et light.svg — banner de profil GitHub animé (SMIL pur)."""
import random
from xml.sax.saxutils import escape
from ascii import portrait

# ============ CONTENU (modifiable) ============
NAME = "DESCARAVAGE"
HANDLE = "descaravage"
GREETING = "Salut 👋, moi c'est Daniel"
ROLES = ["Développeur Frontend React / TypeScript", "Développeur Fullstack · Bac+5",
         "Workflows agentiques & IA", "Disponible immédiatement"]
INFO = [  # (libellé, valeur) — pas d'email ni de téléphone
    ("Localisation", "Tours · ouvert à la mobilité"),
    ("Expérience", "2 ans frontend en alternance · Enedis"),
    ("Formation", "Bac+5 RNCP 7 · Skolæ / CEFIM"),
    ("En ce moment", "Système agentique de génération de sites"),
    ("GitHub", "github.com/DESCARAVAGE"),
]
SKILLS = ["React", "TypeScript", "Next.js", "Vite", "Tailwind", "Node.js",
          "PostgreSQL", "Docker", "Playwright", "Jest", "Claude Code", "Figma"]
STATUS = "disponible immédiatement"
SOCIALS = ["github", "linkedin", "web"]

W, H = 1180, 610
MONO = "ui-monospace, SFMono-Regular, 'JetBrains Mono', Menlo, Consolas, monospace"
SANS = "Inter, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

PALETTES = {
    "dark": dict(bg="#030712", panel="#0F172A", panel_op=0.72, border="#FFFFFF", border_op=0.08,
                 text="#F8FAFC", muted="#94A3B8", a1="#7C3AED", a2="#22D3EE", a3="#10B981",
                 asc1="#22D3EE", asc2="#A78BFA", asc3="#7C3AED",
                 blobs=[("#3B82F6", .22), ("#7C3AED", .22), ("#10B981", .14)],
                 glow=1.0, shadow="#000000", shadow_op=.55, noise=.055, part="#E2E8F0",
                 reflect=.06, pill_bg="#0B1222", scan=.10, dot=("#FF5F57", "#FEBC2E", "#28C840")),
    "light": dict(bg="#FFFFFF", panel="#F8FAFC", panel_op=0.82, border="#0F172A", border_op=0.08,
                  text="#0F172A", muted="#475569", a1="#2563EB", a2="#06B6D4", a3="#10B981",
                  asc1="#2563EB", asc2="#06B6D4", asc3="#0EA5E9",
                  blobs=[("#60A5FA", .16), ("#A5B4FC", .14), ("#6EE7B7", .12)],
                  glow=.45, shadow="#0F172A", shadow_op=.10, noise=.03, part="#64748B",
                  reflect=.45, pill_bg="#FFFFFF", scan=.06, dot=("#FF5F57", "#FEBC2E", "#28C840")),
}


def typing_keyframes(phrases, cw, type_dt=0.075, hold=1.9, erase_dt=0.035, gap=0.45):
    ev, t = [], 0.0  # (t, idx, n)
    for i, p in enumerate(phrases):
        for n in range(len(p) + 1):
            ev.append((t, i, n)); t += type_dt
        t += hold - type_dt
        for n in range(len(p) - 1, -1, -1):
            ev.append((t, i, n)); t += erase_dt
        t += gap
    T = t

    def anim(valfn):
        kt, vals, last = [], [], None
        for (tt, i, n) in ev:
            v = valfn(i, n)
            if v != last:
                kt.append(tt / T); vals.append(v); last = v
        kt[0] = 0
        return ";".join(f"{k:.5f}" for k in kt), ";".join(f"{v:g}" for v in vals)

    return T, anim


def build(mode):
    P = PALETTES[mode]
    rnd = random.Random(42)
    o = []
    a = o.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
      f'role="img" aria-label="{NAME} — {ROLES[0]}">')
    a(f'<title>{NAME} — {ROLES[0]}</title>')
    # ---------- CSS (hover : fonctionne si le SVG est ouvert directement) ----------
    a('<style>'
      '.pill{transition:transform .25s ease, filter .25s ease;transform-box:fill-box;transform-origin:center}'
      '.pill:hover{transform:scale(1.08);filter:url(#glowStrong)}'
      '.soc{transition:transform .25s ease;transform-box:fill-box;transform-origin:center}'
      '.soc:hover{transform:scale(1.12)}'
      '</style>')
    # ================= DEFS =================
    a('<defs>')
    a(f'<clipPath id="card"><rect x="0" y="0" width="{W}" height="{H}" rx="28"/></clipPath>')
    # accent gradient (animé)
    a(f'<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">'
      f'<stop offset="0" stop-color="{P["a1"]}"><animate attributeName="stop-color" values="{P["a1"]};{P["a2"]};{P["a3"]};{P["a1"]}" dur="9s" repeatCount="indefinite"/></stop>'
      f'<stop offset=".5" stop-color="{P["a2"]}"><animate attributeName="stop-color" values="{P["a2"]};{P["a3"]};{P["a1"]};{P["a2"]}" dur="9s" repeatCount="indefinite"/></stop>'
      f'<stop offset="1" stop-color="{P["a3"]}"><animate attributeName="stop-color" values="{P["a3"]};{P["a1"]};{P["a2"]};{P["a3"]}" dur="9s" repeatCount="indefinite"/></stop>'
      '</linearGradient>')
    # nom : dégradé statique (lisible) qui glisse
    a(f'<linearGradient id="nameGrad" gradientUnits="userSpaceOnUse" x1="500" y1="0" x2="900" y2="0" spreadMethod="reflect">'
      f'<stop offset="0" stop-color="{P["text"]}"/><stop offset=".55" stop-color="{P["a2"]}"/><stop offset="1" stop-color="{P["a1"]}"/>'
      '<animateTransform attributeName="gradientTransform" type="translate" values="0 0;400 0;0 0" dur="8s" repeatCount="indefinite"/>'
      '</linearGradient>')
    # ASCII gradient mobile
    a(f'<linearGradient id="asciiGrad" gradientUnits="userSpaceOnUse" x1="40" y1="60" x2="440" y2="520" spreadMethod="reflect">'
      f'<stop offset="0" stop-color="{P["asc1"]}"/><stop offset=".5" stop-color="{P["asc2"]}"/><stop offset="1" stop-color="{P["asc3"]}"/>'
      '<animateTransform attributeName="gradientTransform" type="translate" values="0 0;300 380;0 0" dur="10s" repeatCount="indefinite"/>'
      '</linearGradient>')
    # bordure shimmer
    a(f'<linearGradient id="shimmer" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">'
      f'<stop offset="0" stop-color="{P["border"]}" stop-opacity="{P["border_op"]}"/>'
      f'<stop offset=".42" stop-color="{P["border"]}" stop-opacity="{P["border_op"]}"/>'
      f'<stop offset=".5" stop-color="{P["a2"]}" stop-opacity=".9"/>'
      f'<stop offset=".58" stop-color="{P["border"]}" stop-opacity="{P["border_op"]}"/>'
      f'<stop offset="1" stop-color="{P["border"]}" stop-opacity="{P["border_op"]}"/>'
      f'<animateTransform attributeName="gradientTransform" type="translate" values="-{W} -{H};{W} {H}" dur="6s" repeatCount="indefinite"/>'
      '</linearGradient>')
    # reflet verre
    a(f'<linearGradient id="reflect" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H*0.6:.0f}">'
      f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/>'
      f'<stop offset=".46" stop-color="#FFFFFF" stop-opacity="0"/>'
      f'<stop offset=".5" stop-color="#FFFFFF" stop-opacity="{P["reflect"]}"/>'
      f'<stop offset=".54" stop-color="#FFFFFF" stop-opacity="0"/>'
      f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>'
      f'<animateTransform attributeName="gradientTransform" type="translate" values="-{W} 0;-{W} 0;{W} 0" keyTimes="0;.55;1" dur="9s" repeatCount="indefinite"/>'
      '</linearGradient>')
    # panneau verre (haut plus clair)
    a(f'<linearGradient id="glass" x1="0" y1="0" x2="0" y2="1">'
      f'<stop offset="0" stop-color="{P["panel"]}" stop-opacity="{min(1, P["panel_op"]+.08):.2f}"/>'
      f'<stop offset="1" stop-color="{P["panel"]}" stop-opacity="{P["panel_op"]-.08:.2f}"/></linearGradient>')
    a(f'<linearGradient id="hl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="{.07 if mode=="dark" else .9}"/><stop offset=".25" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>')
    # scanline
    a(f'<linearGradient id="scanG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["a2"]}" stop-opacity="0"/>'
      f'<stop offset=".5" stop-color="{P["a2"]}" stop-opacity="{P["scan"]}"/><stop offset="1" stop-color="{P["a2"]}" stop-opacity="0"/></linearGradient>')
    # lignes CRT
    a(f'<pattern id="crt" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{P["text"]}" opacity="{.035 if mode=="dark" else .025}"/></pattern>')
    # blobs
    for i, (c, op) in enumerate(P["blobs"]):
        a(f'<radialGradient id="blob{i}"><stop offset="0" stop-color="{c}" stop-opacity="{op}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
    a(f'<radialGradient id="dotG"><stop offset="0" stop-color="{P["a2"]}" stop-opacity=".9"/><stop offset="1" stop-color="{P["a2"]}" stop-opacity="0"/></radialGradient>')
    # filtres
    g = P["glow"]
    a(f'<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="{2.2*g:.2f}" result="b"/>'
      f'<feComponentTransfer in="b" result="b2"><feFuncA type="linear" slope="{.9*g:.2f}"/></feComponentTransfer>'
      '<feMerge><feMergeNode in="b2"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a(f'<filter id="glowStrong" x="-40%" y="-80%" width="180%" height="260%"><feGaussianBlur stdDeviation="{4*g+1:.2f}" result="b"/>'
      '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    a(f'<filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="18" stdDeviation="22" flood-color="{P["shadow"]}" flood-opacity="{P["shadow_op"]}"/></filter>')
    a('<filter id="noise" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch" result="n">'
      '<animate attributeName="baseFrequency" values=".85;.9;.85" dur="2s" repeatCount="indefinite"/></feTurbulence>'
      '<feColorMatrix type="saturate" values="0"/></filter>')
    a('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="30"/></filter>')
    a('</defs>')

    # ================= FOND =================
    a('<g clip-path="url(#card)">')
    a(f'<rect width="{W}" height="{H}" fill="{P["bg"]}"/>')
    blobs = [(260, 150, 330, "0 0;60 40;0 0", 18), (900, 420, 360, "0 0;-70 -30;0 0", 22), (640, 80, 260, "0 0;40 60;0 0", 16)]
    for i, (cx, cy, r, vals, d) in enumerate(blobs):
        a(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#blob{i})"><animateTransform attributeName="transform" type="translate" values="{vals}" dur="{d}s" repeatCount="indefinite"/>'
          f'<animate attributeName="r" values="{r};{r*1.12:.0f};{r}" dur="{d*0.7:.1f}s" repeatCount="indefinite"/></circle>')
    # grille subtile
    a(f'<g opacity="{.05 if mode=="dark" else .05}" stroke="{P["text"]}" stroke-width=".5">')
    for x in range(40, W, 40):
        a(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>')
    for y in range(40, H, 40):
        a(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>')
    a('</g>')
    # particules
    for _ in range(26):
        x, y = rnd.uniform(20, W - 20), rnd.uniform(40, H - 10)
        r_, d, b = rnd.uniform(.6, 1.7), rnd.uniform(7, 14), rnd.uniform(0, 8)
        dy = rnd.uniform(40, 110)
        a(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r_:.1f}" fill="{P["part"]}" opacity="0">'
          f'<animate attributeName="opacity" values="0;.7;0" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/>'
          f'<animateTransform attributeName="transform" type="translate" values="0 0;{rnd.uniform(-15,15):.0f} -{dy:.0f}" dur="{d:.1f}s" begin="{b:.1f}s" repeatCount="indefinite"/></circle>')

    # ================= PANNEAU GAUCHE (ASCII) =================
    LX, LY, LW, LH = 30, 30, 420, 550
    a('<g>')
    a(f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="7s" repeatCount="indefinite"/>')
    a(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="20" fill="url(#glass)" filter="url(#shadow)"/>')
    a(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="20" fill="url(#hl)"/>')
    a(f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="20" fill="url(#crt)"/>')
    a(f'<rect x="{LX+.5}" y="{LY+.5}" width="{LW-1}" height="{LH-1}" rx="19.5" fill="none" stroke="url(#shimmer)"/>')
    # header
    a(f'<text x="{LX+22}" y="{LY+30}" font-family="{MONO}" font-size="11.5" fill="{P["muted"]}" letter-spacing=".5">~/portrait.ascii</text>')
    a(f'<g transform="translate({LX+LW-74} {LY+21})"><rect width="54" height="18" rx="9" fill="none" stroke="{P["a3"]}" stroke-opacity=".5"/>'
      f'<circle cx="11" cy="9" r="3" fill="{P["a3"]}"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></circle>'
      f'<text x="19" y="12.8" font-family="{MONO}" font-size="9.5" fill="{P["a3"]}">LIVE</text></g>')
    a(f'<line x1="{LX+20}" y1="{LY+46}" x2="{LX+LW-20}" y2="{LY+46}" stroke="{P["border"]}" stroke-opacity="{P["border_op"]*1.2:.2f}"/>')
    # ascii
    lines = portrait()
    AX, AY, AW, LHt = LX + 30, LY + 74, 360, 12.4
    a(f'<clipPath id="leftClip"><rect x="{LX}" y="{LY+47}" width="{LW}" height="{LH-47}" rx="20"/></clipPath>')
    a('<g clip-path="url(#leftClip)">')
    a('<g>')
    a('<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="5s" repeatCount="indefinite"/>')
    a(f'<g font-family="{MONO}" font-size="10.4" fill="url(#asciiGrad)" filter="url(#glow)" xml:space="preserve">')
    for i, l in enumerate(lines):
        if not l.strip():
            continue
        b = 0.4 + i * 0.07
        a(f'<text x="{AX}" y="{AY + i*LHt:.1f}" textLength="{AW}" lengthAdjust="spacingAndGlyphs" opacity="0">{escape(l).replace(' ', chr(160))}'
          f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur=".25s" fill="freeze"/></text>')
    a('</g>')
    # curseur qui descend pendant le reveal puis clignote
    end = 0.4 + len(lines) * 0.07
    a(f'<rect x="{AX+AW+4}" y="{AY-10}" width="7" height="12" fill="{P["a2"]}">'
      f'<animate attributeName="y" from="{AY-10}" to="{AY + (len(lines)-1)*LHt - 10:.1f}" dur="{end-0.4:.2f}s" begin=".4s" fill="freeze"/>'
      f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></rect>')
    a('</g>')
    # scanline
    a(f'<rect x="{LX}" y="{LY}" width="{LW}" height="70" fill="url(#scanG)">'
      f'<animate attributeName="y" values="{LY-70};{LY+LH}" dur="4.5s" repeatCount="indefinite"/></rect>')
    a('</g>')
    a(f'<text x="{LX+22}" y="{LY+LH-20}" font-family="{MONO}" font-size="11" fill="{P["muted"]}" opacity="0">'
      f'<tspan fill="{P["a3"]}">✓</tspan> render complete · {len(lines)} lines'
      f'<animate attributeName="opacity" from="0" to="1" begin="{end:.2f}s" dur=".4s" fill="freeze"/></text>')
    a('</g>')

    # ================= PANNEAU DROIT (TERMINAL) =================
    RX, RY, RW, RH = 470, 30, 680, 550
    CX = RX + 34
    a('<g>')
    a(f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="8s" begin="1s" repeatCount="indefinite"/>')
    a(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="20" fill="url(#glass)" filter="url(#shadow)"/>')
    a(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="20" fill="url(#hl)"/>')
    a(f'<rect x="{RX+.5}" y="{RY+.5}" width="{RW-1}" height="{RH-1}" rx="19.5" fill="none" stroke="url(#shimmer)"/>')
    # barre de titre
    for i, c in enumerate(P["dot"]):
        a(f'<circle cx="{RX+24+i*18}" cy="{RY+22}" r="5.5" fill="{c}" opacity=".9"/>')
    a(f'<text x="{RX+RW/2}" y="{RY+26}" text-anchor="middle" font-family="{MONO}" font-size="11.5" fill="{P["muted"]}">{HANDLE}@github: ~/profile</text>')
    a(f'<text x="{RX+RW-24}" y="{RY+26}" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{P["muted"]}" opacity=".7">zsh</text>')
    a(f'<line x1="{RX}" y1="{RY+44}" x2="{RX+RW}" y2="{RY+44}" stroke="{P["border"]}" stroke-opacity="{P["border_op"]*1.2:.2f}"/>')

    # $ whoami (typing une fois)
    cmd, cwm = "whoami", 8.4
    a(f'<text x="{CX}" y="{RY+80}" font-family="{MONO}" font-size="14" fill="{P["a3"]}">➜</text>')
    a(f'<text x="{CX+20}" y="{RY+80}" font-family="{MONO}" font-size="14" fill="{P["a2"]}">~</text>')
    a(f'<clipPath id="cmdClip"><rect x="{CX+40}" y="{RY+60}" width="0" height="30">'
      f'<animate attributeName="width" values="{";".join(str(round(n*cwm,1)) for n in range(len(cmd)+1))}" '
      f'keyTimes="{";".join(f"{n/(len(cmd)+1):.3f}" for n in range(len(cmd)+1))}" calcMode="discrete" begin=".3s" dur=".6s" fill="freeze"/></rect></clipPath>')
    a(f'<text x="{CX+40}" y="{RY+80}" font-family="{MONO}" font-size="14" fill="{P["text"]}" textLength="{len(cmd)*cwm}" lengthAdjust="spacingAndGlyphs" clip-path="url(#cmdClip)">{cmd}</text>')

    def fade(begin, dy=8, dur=.6):
        return (f'<animate attributeName="opacity" from="0" to="1" begin="{begin}s" dur="{dur}s" fill="freeze"/>'
                f'<animateTransform attributeName="transform" type="translate" from="0 {dy}" to="0 0" begin="{begin}s" dur="{dur}s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/>')

    # salutation
    a(f'<g opacity="0">{fade(1.0)}<text x="{CX}" y="{RY+122}" font-family="{SANS}" font-size="20" fill="{P["muted"]}">{escape(GREETING)}</text></g>')
    a(f'<g opacity="0">{fade(1.3, 12, .8)}<text x="{CX-2}" y="{RY+176}" font-family="{SANS}" font-size="50" font-weight="800" letter-spacing="1" fill="url(#nameGrad)" filter="url(#glow)">{NAME}</text></g>')

    # rôles qui tapent
    rw = 12.0
    T, anim = typing_keyframes(ROLES, rw)
    ry = RY + 216
    a(f'<g opacity="0">{fade(1.8, 0, .4)}')
    a(f'<text x="{CX}" y="{ry}" font-family="{MONO}" font-size="19" fill="{P["a1"]}">❯</text>')
    rx0 = CX + 24
    for i, ph in enumerate(ROLES):
        kt, vals = anim(lambda j, n, i=i: n * rw if j == i else 0)
        a(f'<clipPath id="role{i}"><rect x="{rx0}" y="{ry-22}" width="0" height="30">'
          f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{T:.2f}s" begin="2s" repeatCount="indefinite"/></rect></clipPath>')
        a(f'<text x="{rx0}" y="{ry}" font-family="{MONO}" font-size="19" font-weight="600" fill="url(#accent)" '
          f'textLength="{len(ph)*rw:g}" lengthAdjust="spacingAndGlyphs" clip-path="url(#role{i})">{escape(ph)}</text>')
    kt, vals = anim(lambda j, n: rx0 + n * rw + 2)
    a(f'<rect x="{rx0+2}" y="{ry-17}" width="2.5" height="21" fill="{P["a2"]}">'
      f'<animate attributeName="x" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{T:.2f}s" begin="2s" repeatCount="indefinite"/>'
      f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" repeatCount="indefinite"/></rect>')
    a('</g>')

    # séparateur
    a(f'<rect x="{CX}" y="{RY+240}" width="0" height="1" fill="url(#accent)" opacity=".6">'
      f'<animate attributeName="width" from="0" to="{RW-68}" begin="2.1s" dur="1s" fill="freeze" calcMode="spline" keySplines=".2 .8 .2 1" keyTimes="0;1"/></rect>')

    # infos séquentielles
    for i, (k, v) in enumerate(INFO):
        y = RY + 272 + i * 25
        b = 2.4 + i * 0.22
        a(f'<g opacity="0">{fade(b, 0, .45)}<animateTransform attributeName="transform" type="translate" from="-10 0" to="0 0" begin="{b}s" dur=".45s" fill="freeze"/>'
          f'<text x="{CX}" y="{y}" font-family="{MONO}" font-size="13.5"><tspan fill="{P["a2"]}">›</tspan>'
          f'<tspan x="{CX+18}" fill="{P["muted"]}">{escape(k)}</tspan>'
          f'<tspan x="{CX+150}" fill="{P["text"]}">{escape(v)}</tspan></text></g>')

    # compétences
    sy = RY + 272 + len(INFO) * 25 + 8
    a(f'<g opacity="0">{fade(3.6, 0, .4)}<text x="{CX}" y="{sy}" font-family="{MONO}" font-size="11" letter-spacing="2" fill="{P["muted"]}">STACK TECHNIQUE</text></g>')
    px, py, row = CX, sy + 14, 0
    maxx = RX + RW - 34
    for i, s in enumerate(SKILLS):
        pw = len(s) * 7.6 + 30
        if px + pw > maxx:
            px, py = CX, py + 36
        b = 3.8 + i * 0.09
        dur = 3 + (i % 4) * .6
        a(f'<g class="pill" opacity="0">'
          f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur=".4s" fill="freeze"/>'
          f'<animateTransform attributeName="transform" type="translate" from="0 6" to="0 0" begin="{b:.2f}s" dur=".4s" fill="freeze"/>'
          f'<rect x="{px:.1f}" y="{py}" width="{pw:.1f}" height="26" rx="13" fill="{P["pill_bg"]}" fill-opacity=".7" stroke="url(#accent)" stroke-opacity=".55"/>'
          f'<rect x="{px:.1f}" y="{py}" width="{pw:.1f}" height="26" rx="13" fill="none" stroke="url(#accent)" stroke-width="1.5" filter="url(#glowStrong)" opacity="0">'
          f'<animate attributeName="opacity" values="0;{.55 if mode=="dark" else .35};0" dur="{dur:.1f}s" begin="{b+.6+i*.3:.2f}s" repeatCount="indefinite"/></rect>'
          f'<circle cx="{px+13:.1f}" cy="{py+13}" r="2.6" fill="url(#accent)"/>'
          f'<text x="{px+21:.1f}" y="{py+17.2}" font-family="{SANS}" font-size="12.5" font-weight="500" fill="{P["text"]}">{escape(s)}</text></g>')
        px += pw + 9

    # social
    soy = RY + RH - 34
    icons = {
        "github": '<path transform="translate(-8 -8)" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" fill="CUR"/>',
        "linkedin": '<rect x="-7.5" y="-7.5" width="15" height="15" rx="3" fill="none" stroke="CUR" stroke-width="1.5"/><rect x="-4.3" y="-1.2" width="1.8" height="5.4" fill="CUR"/><circle cx="-3.4" cy="-3.6" r="1.1" fill="CUR"/><path d="M-0.6 4.2V-1.2h1.7v.8c.4-.6 1-.95 1.9-.95 1.5 0 2.1 1 2.1 2.5v3.05H3.3V1.5c0-.8-.3-1.3-1-1.3-.75 0-1.15.55-1.15 1.35v2.65z" fill="CUR"/>',
        "x": '<path d="M-6.5 -7H-2.5L7 7H3z" fill="none" stroke="CUR" stroke-width="1.4" stroke-linejoin="round"/><path d="M6.5 -7L1 -0.8M-6.5 7L-1 0.8" stroke="CUR" stroke-width="1.6" stroke-linecap="round"/>',
        "web": '<circle r="7.5" fill="none" stroke="CUR" stroke-width="1.4"/><ellipse rx="3.4" ry="7.5" fill="none" stroke="CUR" stroke-width="1.2"/><path d="M-7.5 0H7.5M-6.5 -3.8H6.5M-6.5 3.8H6.5" stroke="CUR" stroke-width="1"/>',
    }
    a(f'<line x1="{CX}" y1="{soy-27}" x2="{RX+RW-34}" y2="{soy-27}" stroke="{P["border"]}" stroke-opacity="{P["border_op"]*1.2:.2f}" opacity="0"><animate attributeName="opacity" from="0" to="1" begin="4.8s" dur=".5s" fill="freeze"/></line>')
    a(f'<g opacity="0">{fade(5.0, 0, .5)}<text x="{CX}" y="{soy+4.5}" font-family="{MONO}" font-size="12" fill="{P["muted"]}">'
      f'<tspan fill="{P["a3"]}">●</tspan> {STATUS}</text></g>')
    for i, s in enumerate(SOCIALS):
        cx = RX + RW - 52 - (len(SOCIALS) - 1 - i) * 46
        b = 5.0 + i * 0.12
        a(f'<g class="soc" opacity="0">'
          f'<animate attributeName="opacity" from="0" to="1" begin="{b:.2f}s" dur=".4s" fill="freeze"/>'
          f'<g transform="translate({cx} {soy})">'
          f'<circle r="17" fill="{P["pill_bg"]}" fill-opacity=".7" stroke="url(#accent)" stroke-opacity=".5"/>'
          f'<circle r="17" fill="none" stroke="url(#accent)" stroke-width="1.5" filter="url(#glowStrong)" opacity="0">'
          f'<animate attributeName="opacity" values="0;{.6 if mode=="dark" else .35};0" dur="3.2s" begin="{b+1+i*.5:.2f}s" repeatCount="indefinite"/></circle>'
          + icons[s].replace("CUR", P["text"]) + '</g></g>')
    a('</g>')

    # ================= OVERLAYS =================
    a(f'<rect width="{W}" height="{H}" fill="url(#reflect)" pointer-events="none"/>')
    a(f'<rect width="{W}" height="{H}" filter="url(#noise)" opacity="{P["noise"]}" pointer-events="none"/>')
    a(f'<rect width="{W}" height="2" fill="{P["a2"]}" opacity="{.25 if mode=="dark" else .15}" pointer-events="none">'
      f'<animate attributeName="y" values="-2;{H}" dur="7s" repeatCount="indefinite"/></rect>')
    a('</g>')
    # bordure globale shimmer
    a(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="27.5" fill="none" stroke="url(#shimmer)"/>')
    a('</svg>')
    return "\n".join(o)


if __name__ == "__main__":
    import os
    os.makedirs("assets", exist_ok=True)
    for m in ("dark", "light"):
        s = build(m)
        open(f"assets/{m}.svg", "w", encoding="utf-8").write(s)
        print(m, len(s) // 1024, "KB")