"""Dimensions, polices, palettes et icônes de la bannière."""

W, H = 1180, 610
MONO = "ui-monospace,SFMono-Regular,'JetBrains Mono',Menlo,Consolas,monospace"
SANS = "Inter,-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
DOTS = ("#FF5F57", "#FEBC2E", "#28C840")

PALETTES = {
    "dark": dict(bg="#030712", panel="#0F172A", panel_op=.72, border="#FFFFFF", border_op=.08,
                 text="#F8FAFC", muted="#94A3B8", a1="#7C3AED", a2="#22D3EE", a3="#10B981",
                 asc=("#22D3EE", "#A78BFA", "#7C3AED"),
                 blobs=(("#3B82F6", .22), ("#7C3AED", .22), ("#10B981", .14)),
                 glow=1.0, shadow="#000000", shadow_op=.55, noise=.055, part="#E2E8F0",
                 reflect=.06, highlight=.07, crt=.035, pill_bg="#0B1222", scan=.10,
                 pulse=.55, beam=.25),
    "light": dict(bg="#FFFFFF", panel="#F8FAFC", panel_op=.82, border="#0F172A", border_op=.08,
                  text="#0F172A", muted="#475569", a1="#2563EB", a2="#06B6D4", a3="#10B981",
                  asc=("#2563EB", "#06B6D4", "#0EA5E9"),
                  blobs=(("#60A5FA", .16), ("#A5B4FC", .14), ("#6EE7B7", .12)),
                  glow=.45, shadow="#0F172A", shadow_op=.10, noise=.03, part="#64748B",
                  reflect=.45, highlight=.9, crt=.025, pill_bg="#FFFFFF", scan=.06,
                  pulse=.35, beam=.15),
}

# icônes centrées sur (0,0), ~16 px ; « C » = couleur du texte
ICONS = {
    "github": '<path transform="translate(-8 -8)" fill="C" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"/>',
    "linkedin": '<rect x="-7.5" y="-7.5" width="15" height="15" rx="3" fill="none" stroke="C" stroke-width="1.5"/><g fill="C"><rect x="-4.3" y="-1.2" width="1.8" height="5.4"/><circle cx="-3.4" cy="-3.6" r="1.1"/><path d="M-.6 4.2V-1.2h1.7v.8c.4-.6 1-.95 1.9-.95 1.5 0 2.1 1 2.1 2.5v3.05H3.3V1.5c0-.8-.3-1.3-1-1.3-.75 0-1.15.55-1.15 1.35v2.65z"/></g>',
    "x": '<path d="M-6.5-7H-2.5L7 7H3z" fill="none" stroke="C" stroke-width="1.4" stroke-linejoin="round"/><path d="M6.5-7 1-.8M-6.5 7-1 .8" stroke="C" stroke-width="1.6" stroke-linecap="round"/>',
    "web": '<g fill="none" stroke="C"><circle r="7.5" stroke-width="1.4"/><ellipse rx="3.4" ry="7.5" stroke-width="1.2"/><path d="M-7.5 0H7.5M-6.5-3.8H6.5M-6.5 3.8H6.5"/></g>',
}