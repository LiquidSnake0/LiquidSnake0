#!/usr/bin/env python3
"""Bannière du profil GitHub : un temple grec en marbre, grainé comme la photo de
profil, traversé par la pluie de code binaire verte de Matrix. Fond noir, un seul
accent vert (charte Lens). Sortie : assets/banner-temple.png."""
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

K = 2                                   # rendu en 2x
W, H = 1280 * K, 320 * K
VERT, VERT_CLAIR, VERT_SOMBRE = (95, 168, 123), (214, 245, 224), (29, 80, 48)
GRIS = (138, 138, 138)
MONO = "/usr/share/fonts/TTF/DejaVuSansMono.ttf"
rnd = random.Random(1203)


def pluie(densite, lumiere, x0=0, x1=W):
    """Colonnes de 0 et de 1 qui tombent : une tête claire, une traîne qui s'éteint."""
    calque = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(calque)
    f = ImageFont.truetype(MONO, 13 * K)
    pas = 15 * K
    for x in range(x0, x1, pas):
        if rnd.random() > densite:
            continue
        for _ in range(rnd.choice((1, 1, 2))):
            tete = rnd.randint(-H // 4, H + H // 3)
            long = rnd.randint(6, 22)
            for i in range(long):
                y = tete - i * pas
                if y < -pas or y > H:
                    continue
                t = i / long
                if i == 0:
                    coul, a = VERT_CLAIR, 255
                else:
                    coul = tuple(int(VERT[c] + (VERT_SOMBRE[c] - VERT[c]) * t) for c in range(3))
                    a = int(230 * (1 - t) ** 1.4)
                d.text((x, y), rnd.choice("01"), font=f, fill=coul + (int(a * lumiere),))
    return calque


def meandre(d, x, y, n, u, coul):
    """Une frise grecque (méandre) : une ligne de base, et sur elle n spirales carrées
    de module u (largeur 4u, hauteur 4u)."""
    w = max(2, u // 3)
    d.line([(x, y + 4 * u), (x + n * 4 * u, y + 4 * u)], fill=coul, width=w)
    for k in range(n):
        o = x + k * 4 * u
        d.line([(o, y + 4 * u), (o, y), (o + 3 * u, y), (o + 3 * u, y + 3 * u), (o + u, y + 3 * u),
                (o + u, y + u), (o + 2 * u, y + u), (o + 2 * u, y + 2 * u)], fill=coul, width=w, joint="curve")


def temple(w, h):
    """Un temple dorique en niveaux de gris, éclairé par la gauche, grainé."""
    g = np.zeros((h, w), np.float32)
    u, v = w / 100.0, h / 100.0                                  # unités : largeur, hauteur

    def rect(x0, y0, x1, y1, val):
        g[max(0, int(y0)):max(0, int(y1)), max(0, int(x0)):int(x1)] = val

    def colonne(x0, y0, x1, y1, haut=0.95, bas=0.35):
        xs = np.linspace(0, 1, int(x1) - int(x0))
        prof = haut - (haut - bas) * xs ** 1.3                       # lumière à gauche
        cannelures = 0.9 + 0.1 * np.cos(xs * np.pi * 2 * 6)          # six cannelures visibles
        g[max(0, int(y0)):int(y1), int(x0):int(x1)] = (prof * cannelures)[None, :]

    y = h                                                        # trois marches
    for m, val in ((0, 0.62), (2.5, 0.72), (5, 0.8)):
        rect(m * u, y - 3.2 * v, w - m * u, y, val)
        y -= 3.2 * v
    sol = y
    haut_col = 46 * v                                            # six colonnes, chapiteau
    for c in range(6):
        cx = 10 * u + c * 14.6 * u
        colonne(cx, sol - haut_col, cx + 8 * u, sol)
        rect(cx - 0.6 * u, sol - haut_col - 2 * v, cx + 8.6 * u, sol - haut_col, 0.72)
        rect(cx - 1.4 * u, sol - haut_col - 4 * v, cx + 9.4 * u, sol - haut_col - 2 * v, 0.9)
    top = sol - haut_col - 4 * v
    rect(6 * u, top - 6 * v, w - 6 * u, top, 0.84)               # architrave
    rect(6 * u, top - 13 * v, w - 6 * u, top - 6 * v, 0.7)       # frise
    for t in range(12):                                          # triglyphes
        x = 9 * u + t * 7.4 * u
        for r in range(3):
            rect(x + r * 1.2 * u, top - 12.2 * v, x + r * 1.2 * u + 0.6 * u, top - 6.8 * v, 0.4)
    rect(3 * u, top - 16 * v, w - 3 * u, top - 13 * v, 0.92)     # corniche
    base, pic = top - 16 * v, top - 35 * v                       # fronton et tympan
    for yy in range(max(0, int(pic)), int(base)):
        f = (yy - pic) / (base - pic)
        demi = f * (w / 2 - 3 * u)
        x0, x1 = int(w / 2 - demi), int(w / 2 + demi)
        if x1 > x0:
            g[yy, x0:x1] = np.linspace(0.93, 0.55, x1 - x0)
        demi2 = demi - 4 * u
        if f > 0.25 and yy < base - 2 * v and demi2 > 0:
            a, b = int(w / 2 - demi2), int(w / 2 + demi2)
            g[yy, a:b] = np.linspace(0.58, 0.36, b - a)
    rng = np.random.default_rng(1203)                            # grain, comme la photo tramée
    g = np.where(g > 0, np.clip(g + rng.normal(0, 0.09, g.shape), 0.05, 1), 0)
    return Image.fromarray((g ** 1.1 * 240).astype(np.uint8), "L")


fond = Image.new("RGBA", (W, H), (0, 0, 0, 255))

# 1. La pluie de fond : discrète derrière le texte, plus dense vers le temple.
fond.alpha_composite(pluie(0.35, 0.35, 0, W // 2))
fond.alpha_composite(pluie(0.75, 0.8, W // 2, W))

# 2. Le temple, posé en mode « lighten » : la pluie reste visible dans ses ombres.
tw, th = 440 * K, 300 * K
bx, by = W - tw - 60 * K, H - th
zone = fond.crop((bx, by, bx + tw, H))
fond.paste(ImageChops.lighter(zone, temple(tw, th).convert("RGBA")), (bx, by))

# 3. Le temple se dissout dans le code : une seconde pluie, plus claire, sur son
#    bas et sa gauche.
devant = pluie(0.55, 0.7, bx - 60 * K, bx + tw // 2)
masque = Image.new("L", (W, H), 0)
ImageDraw.Draw(masque).rectangle((bx - 60 * K, H // 3, bx + tw // 2, H), fill=255)
masque = masque.filter(ImageFilter.GaussianBlur(40 * K))
devant.putalpha(ImageChops.multiply(devant.getchannel("A"), masque))
fond.alpha_composite(devant)

# 4. Le voile qui garde le texte lisible, puis le texte entre deux frises.
voile = Image.new("L", (W, H), 0)
ImageDraw.Draw(voile).rectangle((0, 0, int(W * 0.45), H), fill=170)
voile = voile.filter(ImageFilter.GaussianBlur(60 * K))
noir = Image.new("RGBA", (W, H), (0, 0, 0, 255))
noir.putalpha(voile)
fond.alpha_composite(noir)

d = ImageDraw.Draw(fond)
mono = ImageFont.truetype(MONO, 26 * K)
meandre(d, 74 * K, 92 * K, 13, 7 * K, GRIS)
d.text((74 * K, 146 * K), "backend .NET engineer", font=mono, fill=VERT_CLAIR)
d.text((74 * K, 184 * K), "reads binaries · ships services", font=mono, fill=VERT)
meandre(d, 74 * K, 236 * K, 13, 7 * K, GRIS)

fond.convert("RGB").save("assets/banner-temple.png", optimize=True)
print("ok")
