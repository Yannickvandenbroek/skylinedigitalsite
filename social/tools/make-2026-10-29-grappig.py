"""Grappige Instagram-posts (29 okt 2026): 'Als je website een medewerker was', 'Websitetaal, eerlijk vertaald'
en 'POV: je googelt je eigen bedrijf'. Huisstijl: donker, goud, Inter Tight. Uitvoer: social/2026-10-29-grappig/."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(S, "..", ".."))
A = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "social", "2026-10-29-grappig"); os.makedirs(OUT, exist_ok=True)
BG = (7, 8, 11); GOLD = (217, 178, 90); WHITE = (244, 241, 233); DIM = (170, 168, 160); SOFT = (222, 219, 210); RED = (226, 84, 84)
W, H = 1080, 1350
EMOJI = "/System/Library/Fonts/Apple Color Emoji.ttc"

def font(size, weight=800, face="InterTight.ttf"):
    f = ImageFont.truetype(os.path.join(S, face), size)
    try: f.set_variation_by_axes([weight] if face == "InterTight.ttf" else [14, weight])
    except Exception: pass
    return f
def tw(d, t, f): return d.textlength(t, font=f)
def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def logo(img, x, y, w=240):
    lg = Image.open(os.path.join(A, "logo.png")).convert("RGBA")
    lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS); img.paste(lg, (x, y), lg)
def eyebrow(d, x, y, text, col=GOLD):
    d.line([(x, y + 13), (x + 48, y + 13)], fill=col, width=3); d.text((x + 66, y), text, font=font(26, 600), fill=col)
def glow(img, pos=(-300, -380, 700, 420), col=(217, 178, 90, 60)):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse(list(pos), fill=col)
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
def canvas(glowpos=(-300, -380, 700, 420)):
    img = Image.new("RGBA", (W, H), BG + (255,)); glow(img, glowpos); return img, ImageDraw.Draw(img)
def paragraph(d, x, y, text, f, maxw, fill=DIM, lh=58):
    lines = wrap(d, text, f, maxw)
    for i, l in enumerate(lines): d.text((x, y + i * lh), l, font=f, fill=fill)
    return y + len(lines) * lh
def emoji(img, x, y, ch, size=160):
    # Apple Color Emoji bestaat alleen in vaste groottes; op 137 renderen en schalen.
    try:
        f = ImageFont.truetype(EMOJI, 137)
        tmp = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); ImageDraw.Draw(tmp).text((10, 10), ch, font=f, embedded_color=True)
        box = tmp.getbbox()
        if box: tmp = tmp.crop(box)
        tmp = tmp.resize((size, int(tmp.height * size / tmp.width)), Image.LANCZOS); img.alpha_composite(tmp, (x, y))
    except Exception: pass
def counter(d, idx, total):
    t = f"{idx}/{total}"; d.text((W - 90 - tw(d, t, font(28, 600)), 150), t, font=font(28, 600), fill=DIM)
def save(img, name): img.convert("RGB").save(os.path.join(OUT, name), quality=92)
def cta(kop1, kop2, tekst, knop="Link in bio  →", url="skylinedigital.nl", eye="G R A T I S   T E S T W E B S I T E"):
    img, d = canvas(); eyebrow(d, 90, 200, eye)
    big = font(96, 900); d.text((90, 290), kop1, font=big, fill=WHITE); d.text((90, 400), kop2, font=big, fill=GOLD)
    paragraph(d, 90, 600, tekst, font(40, 500, "Inter.ttf"), 880)
    d.rounded_rectangle([90, 900, 640, 1000], 16, fill=GOLD); d.text((130, 925), knop, font=font(40, 800), fill=BG)
    d.text((90, 1060), url, font=font(36, 700), fill=WHITE); logo(img, 90, 1180); return img

# ---------- A: Als je website een medewerker was ----------
MEDEWERKER = [
    ("😴", "Komt pas na 7 seconden opdagen.", "En de helft van je klanten is dan al weg. Laadtijd is geen detail, het is je deurbel."),
    ("👔", "Draagt nog het pak van 2016.", "Het zat toen prima. Nu kijken klanten ernaar zoals jij naar je oude profielfoto."),
    ("📞", "Zegt tegen elke klant: 'bel maar even'.", "Geen prijzen, geen uitleg, geen antwoorden. Alleen een telefoonnummer en veel succes."),
    ("📱", "Werkt niet op de telefoon. Letterlijk.", "Zeven van de tien bezoekers komen via hun telefoon. Die knijpen en zoomen, en gaan dan naar je concurrent."),
    ("🎄", "Laatste nieuws: 'Fijne feestdagen 2021'.", "Een nieuwsrubriek is een belofte. Nakomen of weghalen, allebei prima."),
]
def a_cover():
    img, d = canvas(); eyebrow(d, 90, 150, "E V E N   E E R L I J K")
    big = font(100, 900)
    d.text((90, 250), "Als je website", font=big, fill=WHITE); d.text((90, 365), "een medewerker", font=big, fill=WHITE); d.text((90, 480), "was…", font=big, fill=GOLD)
    paragraph(d, 90, 680, "…had je 'm dan al ontslagen? Vijf collega's die we vaak tegenkomen.", font(40, 500, "Inter.ttf"), 880)
    emoji(img, 90, 820, "😬", 150)
    d.text((90, 1050), "Swipe", font=font(36, 700), fill=WHITE); d.text((205, 1050), "→", font=font(36, 700), fill=GOLD)
    logo(img, 90, 1180); return img
def a_slide(i, em, kop, tekst):
    img, d = canvas(); counter(d, i + 1, 5)
    emoji(img, 90, 130, em, 170)
    d.text((300, 160), f"Collega {i + 1}", font=font(34, 600), fill=GOLD)
    y = 400; kf = font(76, 800)
    for l in wrap(d, kop, kf, 900): d.text((90, y), l, font=kf, fill=WHITE); y += 88
    paragraph(d, 90, y + 30, tekst, font(38, 500, "Inter.ttf"), 900, SOFT, 56)
    logo(img, 90, 1180); return img
save(a_cover(), "medewerker-01.jpg")
for i, m in enumerate(MEDEWERKER): save(a_slide(i, *m), f"medewerker-{i + 2:02d}.jpg")
save(cta("Tijd voor een", "nieuwe collega?", "We bouwen eerst gratis een voorbeeld van je nieuwe website. Bevalt het? Dan gaan we door. Zo niet: geen ontslagvergoeding nodig."), "medewerker-07.jpg")

# ---------- B: Websitetaal, eerlijk vertaald ----------
VERTAAL = [
    ("Innovatieve totaaloplossingen", "We doen van alles."),
    ("Deze pagina is onder constructie", "We zijn het vergeten."),
    ("Bel voor meer informatie", "We noemen liever geen prijzen."),
    ("Bekijk onze laatste projecten", "Uit 2019."),
    ("Wij staan voor kwaliteit", "Verder weten we het ook niet."),
]
def b_cover():
    img, d = canvas(); eyebrow(d, 90, 150, "W O O R D E N B O E K")
    big = font(104, 900)
    d.text((90, 250), "Websitetaal,", font=big, fill=WHITE); d.text((90, 365), "eerlijk", font=big, fill=WHITE); d.text((90, 480), "vertaald.", font=big, fill=GOLD)
    paragraph(d, 90, 680, "Wat er staat, en wat je klant leest. Vijf klassiekers.", font(40, 500, "Inter.ttf"), 880)
    emoji(img, 90, 800, "🔍", 150)
    d.text((90, 1050), "Swipe", font=font(36, 700), fill=WHITE); d.text((205, 1050), "→", font=font(36, 700), fill=GOLD)
    logo(img, 90, 1180); return img
def b_slide(i, staat, leest):
    img, d = canvas(); counter(d, i + 1, 5)
    d.text((90, 170), "Er staat:", font=font(30, 600), fill=DIM)
    y = 225; f1 = font(62, 800)
    for l in wrap(d, f"“{staat}”", f1, 900): d.text((90, y), l, font=f1, fill=WHITE); y += 72
    d.line([(90, y + 40), (W - 90, y + 40)], fill=(60, 60, 68), width=2)
    d.text((90, y + 90), "Je klant leest:", font=font(30, 600), fill=GOLD)
    y2 = y + 145; f2 = font(80, 900)
    for l in wrap(d, leest, f2, 900): d.text((90, y2), l, font=f2, fill=GOLD); y2 += 92
    logo(img, 90, 1180); return img
save(b_cover(), "vertaald-01.jpg")
for i, v in enumerate(VERTAAL): save(b_slide(i, *v), f"vertaald-{i + 2:02d}.jpg")
save(cta("Zeg gewoon", "wat je doet.", "Duidelijke teksten, echte prijzen en een site die klanten wél een antwoord geeft. We laten het eerst gratis zien.", eye="G R A T I S   T E S T W E B S I T E"), "vertaald-07.jpg")

# ---------- C: POV: je googelt je eigen bedrijf ----------
def c_pov():
    img, d = canvas((200, 300, 1300, 1100))
    eyebrow(d, 90, 150, "P O V")
    big = font(92, 900)
    d.text((90, 240), "Je googelt", font=big, fill=WHITE); d.text((90, 345), "je eigen bedrijf.", font=big, fill=WHITE)
    # zoekbalk
    d.rounded_rectangle([90, 520, 990, 610], 45, fill=(24, 25, 30), outline=(60, 60, 68), width=2)
    d.text((140, 545), "loodgieter in de buurt", font=font(34, 500, "Inter.ttf"), fill=SOFT)
    emoji(img, 905, 538, "🔍", 56)
    d.text((90, 700), "Pagina 4.", font=font(170, 900), fill=GOLD)
    paragraph(d, 90, 920, "Je concurrent staat bovenaan. Niet omdat hij beter is, maar omdat Google hem beter begrijpt. Dat is te fixen, en het begint bij je website.", font(36, 500, "Inter.ttf"), 900, SOFT, 52)
    d.text((90, 1130), "SEO vanaf €39 p/m  ·  Link in bio", font=font(34, 700), fill=GOLD)
    logo(img, W - 90 - 220, 1200, 220); return img
save(c_pov(), "pov-pagina4.jpg")

# ---------- Overzicht ----------
files = [f for f in sorted(os.listdir(OUT)) if f.endswith(".jpg") and not f.startswith("_")]
th = 300; tw_ = int(th * W / H); cols = 7; rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tw_ + 10) + 10, rows * (th + 40) + 10), (30, 30, 34)); sd = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(os.path.join(OUT, f)).resize((tw_, th), Image.LANCZOS)
    x = 10 + (i % cols) * (tw_ + 10); y = 10 + (i // cols) * (th + 40)
    sheet.paste(im, (x, y)); sd.text((x, y + th + 8), f, fill=(200, 200, 200), font=font(18, 500, "Inter.ttf"))
sheet.save(os.path.join(OUT, "_overzicht.jpg"), quality=85)
print("klaar:", files)
