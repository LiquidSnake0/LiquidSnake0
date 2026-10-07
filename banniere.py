#!/usr/bin/env python3
"""Bannière du profil GitHub : le buste de marbre (la photo de profil) et la pluie
de code binaire verte de Matrix. Fond noir, un seul accent vert (charte Lens).
Entrée : assets/avatar.jpg (la photo de profil GitHub). Sortie : assets/banner.png."""
import random
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance, ImageChops, ImageFilter

K = 2                                   # rendu en 2x
W, H = 1280 * K, 320 * K
VERT, VERT_CLAIR, VERT_SOMBRE = (95, 168, 123), (214, 245, 224), (29, 80, 48)
MARBRE, GRIS = (232, 229, 222), (138, 138, 138)
MONO = "/usr/share/fonts/TTF/DejaVuSansMono.ttf"
SERIF = "/usr/share/fonts/noto/NotoSerif-Bold.ttf"
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


fond = Image.new("RGBA", (W, H), (0, 0, 0, 255))

# 1. La pluie de fond : discrète derrière le texte, plus dense vers le buste.
fond.alpha_composite(pluie(0.35, 0.35, 0, W // 2))
fond.alpha_composite(pluie(0.75, 0.8, W // 2, W))

# 2. Le buste : la photo en niveaux de gris, contrastée, posée à droite ; elle
#    s'éclaircit seulement là où elle est plus claire que la pluie (mode « lighten »).
buste = Image.open("assets/avatar.jpg").convert("L")
buste = ImageEnhance.Contrast(buste).enhance(1.25)
taille = H
buste = buste.resize((taille, taille), Image.LANCZOS).convert("RGBA")
bx = W - taille - 40 * K
zone = fond.crop((bx, 0, bx + taille, H))
zone = ImageChops.lighter(zone, buste)
fond.paste(zone, (bx, 0))

# 3. La statue se dissout dans le code : une seconde pluie, plus claire, par-dessus
#    le bas et la gauche du buste.
devant = pluie(0.55, 0.7, bx - 60 * K, bx + taille // 2)
masque = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(masque)
md.rectangle((bx - 60 * K, H // 3, bx + taille // 2, H), fill=255)
masque = masque.filter(ImageFilter.GaussianBlur(40 * K))
devant.putalpha(ImageChops.multiply(devant.getchannel("A"), masque))
fond.alpha_composite(devant)

# 4. Le voile qui garde le texte lisible, puis le texte.
voile = Image.new("L", (W, H), 0)
ImageDraw.Draw(voile).rectangle((0, 0, int(W * 0.52), H), fill=170)
voile = voile.filter(ImageFilter.GaussianBlur(60 * K))
noir = Image.new("RGBA", (W, H), (0, 0, 0, 255)); noir.putalpha(voile)
fond.alpha_composite(noir)

d = ImageDraw.Draw(fond)
titre = ImageFont.truetype(SERIF, 64 * K)
x, y = 72 * K, 84 * K
for lettre in "SELIM":                       # capitales espacées, façon inscription
    d.text((x, y), lettre, font=titre, fill=MARBRE)
    x += d.textlength(lettre, font=titre) + 14 * K
meandre(d, 74 * K, 172 * K, 9, 7 * K, GRIS)
mono = ImageFont.truetype(MONO, 17 * K)
d.text((74 * K, 214 * K), "backend .NET engineer", font=mono, fill=VERT_CLAIR)
d.text((74 * K, 242 * K), "reads binaries · ships services · plays vinyl", font=mono, fill=VERT)

fond.convert("RGB").save("assets/banner.png", optimize=True)
print("ok")
