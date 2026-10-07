#!/usr/bin/env python3
"""Bannière du profil GitHub, charte Lens (gris + un accent vert, Montserrat).
Produit assets/banner-light.png et assets/banner-dark.png (rendu par rsvg-convert)."""
import math, subprocess, os

W, H = 1280, 320
THEMES = {
    "light": dict(fond="#ffffff", lavis="#f2f2f2", encre="#1a1a1a", gris="#555555", pale="#8a8a8a",
                  ligne="#c9c9c9", sillon="#d8d8d8", disque="#1f1f1f", accent="#2d7548", accent_encre="#1d5030", etiquette_txt="#e7f0ea", bras="#b9b9b9"),
    "dark":  dict(fond="#0f1110", lavis="#171a18", encre="#ececec", gris="#b4b4b4", pale="#8a8a8a",
                  ligne="#333733", sillon="#2b2e2c", disque="#050505", accent="#5fa87b", accent_encre="#7cc79a", etiquette_txt="#0f1110", bras="#b4b4b4"),
}


def svg(t):
    c = THEMES[t]
    cx, cy, r = 1105, 160, 230          # le disque, coupé par le bord droit
    sillons = []
    for i in range(46):
        rr = 78 + i * 3.3
        op = 0.35 + 0.5 * ((i * 7) % 5) / 4
        sillons.append(f'<circle cx="{cx}" cy="{cy}" r="{rr:.1f}" fill="none" stroke="{c["sillon"]}" stroke-width="0.8" opacity="{op:.2f}"/>')
    # un reflet : deux arcs plus clairs
    def arc(r0, a0, a1):
        x0, y0 = cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)
        x1, y1 = cx + r0 * math.cos(a1), cy + r0 * math.sin(a1)
        return f'M{x0:.1f},{y0:.1f} A{r0},{r0} 0 0 1 {x1:.1f},{y1:.1f}'
    reflet = "".join(f'<path d="{arc(rr, math.radians(200), math.radians(240))}" fill="none" stroke="{c["ligne"]}" stroke-width="1.2" opacity="0.55"/>'
                     for rr in range(110, 220, 9))
    # le bras de lecture, posé sur le disque
    bras = (f'<g stroke="{c["bras"]}" stroke-linecap="round" fill="none">'
            f'<path d="M905,24 L930,24" stroke-width="10"/>'
            f'<path d="M918,24 L968,190 L992,214" stroke-width="5"/>'
            f'<rect x="984" y="208" width="22" height="12" rx="2" transform="rotate(45 995 214)" fill="{c["bras"]}" stroke="none"/>'
            f'</g><circle cx="918" cy="24" r="13" fill="{c["lavis"]}" stroke="{c["bras"]}" stroke-width="2"/>')
    # une forme d'onde sous le texte, faite de barres : la seule touche d'accent hors étiquette
    barres = []
    x = 72
    for i in range(64):
        a = abs(math.sin(i * 0.37) * math.cos(i * 0.11)) * 0.85 + 0.15 * abs(math.sin(i * 1.7))
        h = 6 + a * 34
        coul = c["accent"] if 22 <= i <= 33 else c["ligne"]
        barres.append(f'<rect x="{x}" y="{252 - h / 2:.1f}" width="5" height="{h:.1f}" rx="1" fill="{coul}"/>')
        x += 9
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <rect width="{W}" height="{H}" fill="{c["fond"]}"/>
  <rect x="0" y="{H - 2}" width="{W}" height="2" fill="{c["ligne"]}"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{c["disque"]}"/>
  {"".join(sillons)}
  {reflet}
  <circle cx="{cx}" cy="{cy}" r="62" fill="{c["accent"]}"/>
  <circle cx="{cx}" cy="{cy}" r="5" fill="{c["fond"]}"/>
  <text x="{cx}" y="{cy - 22}" text-anchor="middle" font-family="Montserrat" font-weight="700" font-size="13" letter-spacing="2" fill="{c["etiquette_txt"]}">SIDE A</text>
  <text x="{cx}" y="{cy + 32}" text-anchor="middle" font-family="DejaVu Sans Mono" font-size="12" fill="{c["etiquette_txt"]}">33 rpm · C#</text>
  {bras}
  <text x="72" y="118" font-family="Montserrat" font-weight="700" font-size="64" letter-spacing="-1" fill="{c["encre"]}">Selim Selimi</text>
  <text x="74" y="162" font-family="Montserrat" font-weight="500" font-size="24" fill="{c["gris"]}">Backend .NET engineer · Geneva</text>
  <text x="74" y="198" font-family="DejaVu Sans Mono" font-size="16" fill="{c["accent_encre"]}">reads binaries, ships services, plays vinyl</text>
  {"".join(barres)}
</svg>'''


os.makedirs("assets", exist_ok=True)
for t in THEMES:
    p = f"assets/banner-{t}.svg"
    open(p, "w").write(svg(t))
    subprocess.run(["rsvg-convert", "-z", "2", "-o", f"assets/banner-{t}.png", p], check=True)
    os.remove(p)
print("ok")
