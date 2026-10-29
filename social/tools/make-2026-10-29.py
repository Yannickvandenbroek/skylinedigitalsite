"""Instagram-posts 29 oktober 2026: carrousel 'ChatGPT noemt je bedrijf' (uit de blog van 27-10),
carrousel 'Nog vier websites' (dekgro, lillis, bodyscan, echtgrieks) en losse post 'SEO zelf doen of uitbesteden'.
Zelfde stijl als make-2026-10-26.py (donker, goud, Inter Tight). Uitvoer: social/2026-10-29/."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(S, "..", ".."))
A = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "social", "2026-10-29"); os.makedirs(OUT, exist_ok=True)
BG = (7, 8, 11); GOLD = (217, 178, 90); WHITE = (244, 241, 233); DIM = (170, 168, 160); SOFT = (222, 219, 210)
W, H = 1080, 1350

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
def eyebrow(d, x, y, text):
    d.line([(x, y + 13), (x + 48, y + 13)], fill=GOLD, width=3)
    d.text((x + 66, y), text, font=font(26, 600), fill=GOLD)
def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    out = Image.new("RGBA", im.size); out.paste(im, (0, 0), m); return out
def glow(img, pos=(-300, -380, 700, 420)):
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse(list(pos), fill=(217, 178, 90, 60))
    img.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
def canvas():
    img = Image.new("RGBA", (W, H), BG + (255,)); glow(img); return img, ImageDraw.Draw(img)
def paragraph(d, x, y, text, f, maxw, fill=DIM, lh=58):
    for i, l in enumerate(wrap(d, text, f, maxw)): d.text((x, y + i * lh), l, font=f, fill=fill)
    return y + len(wrap(d, text, f, maxw)) * lh
def counter(d, idx, total):
    t = f"{idx}/{total}"; d.text((W - 90 - tw(d, t, font(28, 600)), 150), t, font=font(28, 600), fill=DIM)
def save(img, name): img.convert("RGB").save(os.path.join(OUT, name), quality=92)

# ---------- Post A: carrousel ChatGPT ----------
TIPS = [
    ("Laat de AI-bots binnen.", "ChatGPT gebruikt een eigen crawler, OAI-SearchBot. Staat die geblokkeerd in je robots.txt, dan kan ChatGPT je site niet noemen. Een wijziging werkt binnen ongeveer 24 uur.", "Bron: OpenAI"),
    ("Zet je belangrijkste info als tekst.", "Prijzen, diensten en werkgebied alleen in een afbeelding of pdf? Dan leest een AI er overheen. Gewone tekst op de pagina is de basis die Google zelf noemt.", "Bron: Google"),
    ("Geen noindex op pagina's die je wilt tonen.", "Controleer in Search Console of je pagina's geïndexeerd zijn en gebruik geen noindex of nosnippet. Niet geïndexeerd betekent ook: niet in AI-antwoorden.", "Bron: Google"),
    ("Beantwoord de vraag direct.", "Een kop die de vraag letterlijk stelt, daaronder een antwoord van één of twee zinnen, daarna pas de uitleg. Prettig voor lezers, en bruikbaar voor een AI-antwoord.", "Zo schrijven wij"),
    ("Geloof geen garanties.", "Niemand kan een vermelding in ChatGPT of Google AI beloven. Google en OpenAI publiceren geen ranglijst. Wees kritisch bij aanbieders die het wel garanderen.", "Bron: Google en OpenAI"),
]
def a_cover():
    img, d = canvas()
    eyebrow(d, 90, 150, "A I - Z O E K M A C H I N E S")
    big = font(104, 900)
    d.text((90, 250), "Wil je dat", font=big, fill=WHITE)
    d.text((90, 365), "ChatGPT jouw", font=big, fill=WHITE)
    d.text((90, 480), "bedrijf noemt?", font=big, fill=GOLD)
    paragraph(d, 90, 680, "Vijf dingen die volgens Google en OpenAI echt het verschil maken. Geen trucs, wel de basis die vaak misgaat.", font(40, 500, "Inter.ttf"), 880)
    d.text((90, 1050), "Swipe", font=font(36, 700), fill=WHITE); d.text((205, 1050), "→", font=font(36, 700), fill=GOLD)
    logo(img, 90, 1180); return img
def a_tip(i, kop, tekst, bron):
    img, d = canvas(); counter(d, i + 1, 5)
    d.text((90, 140), f"0{i + 1}", font=font(140, 900), fill=GOLD)
    y = 420
    kf = font(72, 800)
    for l in wrap(d, kop, kf, 900): d.text((90, y), l, font=kf, fill=WHITE); y += 84
    y = paragraph(d, 90, y + 30, tekst, font(38, 500, "Inter.ttf"), 900, SOFT, 56)
    d.text((90, y + 40), bron, font=font(26, 600), fill=GOLD)
    logo(img, 90, 1180); return img
def a_cta():
    img, d = canvas()
    eyebrow(d, 90, 200, "H E L E   U I T L E G")
    big = font(96, 900)
    d.text((90, 290), "Lees het", font=big, fill=WHITE)
    d.text((90, 400), "volledige artikel.", font=big, fill=GOLD)
    paragraph(d, 90, 600, "Op onze blog staat precies wat Google en OpenAI zelf zeggen over zichtbaarheid in AI-antwoorden, met bronnen. Wil je dat wij het regelen? SEO vanaf €39 per maand.", font(40, 500, "Inter.ttf"), 880)
    d.rounded_rectangle([90, 900, 640, 1000], 16, fill=GOLD); d.text((130, 925), "Link in bio  →", font=font(40, 800), fill=BG)
    d.text((90, 1060), "skylinedigital.nl/blog", font=font(36, 700), fill=WHITE)
    logo(img, 90, 1180); return img
save(a_cover(), "chatgpt-01.jpg")
for i, t in enumerate(TIPS): save(a_tip(i, *t), f"chatgpt-{i + 2:02d}.jpg")
save(a_cta(), "chatgpt-07.jpg")

# ---------- Post B: nog vier websites ----------
CLIENTS = [
    ("dekgro", "Tegeltechniek Dekgro", "Tegelwerk", "Van lokaal vakbedrijf naar een professionele online uitstraling"),
    ("lillis", "Lilli's Schilderwerken", "Schilderwerk", "Stijlvol, persoonlijk en vakkundig in beeld"),
    ("bodyscan", "BodyScan Waalre", "Wellness · Waalre", "Rustig en vertrouwenwekkend, passend bij de praktijk"),
    ("echtgrieks", "Echt Grieks", "Vakantiehuis · Griekenland", "Sfeervolle site die gasten verliefd maakt op Sykia"),
]
def b_cover():
    img, d = canvas()
    eyebrow(d, 90, 150, "P O R T F O L I O   D E E L   2")
    big = font(116, 900)
    d.text((90, 250), "Nog vier", font=big, fill=WHITE)
    d.text((90, 380), "websites", font=big, fill=WHITE)
    d.text((90, 510), "die we bouwden.", font=font(96, 900), fill=GOLD)
    paragraph(d, 90, 700, "Van tegelwerk tot een vakantiehuis in Griekenland. Elke site is maatwerk, snel en gebouwd om gevonden te worden.", font(40, 500, "Inter.ttf"), 880)
    d.text((90, 1050), "Swipe", font=font(36, 700), fill=WHITE); d.text((205, 1050), "→", font=font(36, 700), fill=GOLD)
    logo(img, 90, 1180); return img
def b_client(slug, name, cat, line, idx, total):
    img, d = canvas()
    shot = Image.open(os.path.join(A, f"work-{slug}-m.jpg")).convert("RGB")
    sw = 440; sh = int(shot.height * sw / shot.width); shot = shot.resize((sw, sh), Image.LANCZOS)
    frame = rounded(Image.new("RGBA", (sw + 28, sh + 28), (24, 25, 30, 255)), 58)
    ph = Image.new("RGBA", frame.size, (0, 0, 0, 0)); ph.alpha_composite(frame); ph.alpha_composite(rounded(shot.convert("RGBA"), 44), (14, 14))
    shadow = Image.new("RGBA", (ph.width + 160, ph.height + 160), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([80, 100, 80 + ph.width, 100 + ph.height], 58, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    x = (W - ph.width) // 2; y = 70
    img.alpha_composite(shadow, (x - 80, y - 80)); img.alpha_composite(ph, (x, y))
    grad = Image.new("RGBA", (W, 360), (0, 0, 0, 0)); gd = ImageDraw.Draw(grad)
    for i in range(360): gd.line([(0, i), (W, i)], fill=BG + (int(255 * min(1, i / 140)),))
    img.alpha_composite(grad, (0, H - 360)); d = ImageDraw.Draw(img)
    d.text((90, 1085), f"0{idx}", font=font(30, 700), fill=GOLD); d.text((150, 1085), f"·  {cat}", font=font(30, 500, "Inter.ttf"), fill=DIM)
    nf = font(58, 800) if tw(d, name, font(58, 800)) <= 900 else font(50, 800)
    d.text((90, 1135), name, font=nf, fill=WHITE)
    d.text((90, 1215), line, font=font(32, 500, "Inter.ttf"), fill=DIM)
    t = f"{idx}/{total}"; d.text((W - 90 - tw(d, t, font(28, 600)), 1090), t, font=font(28, 600), fill=DIM)
    return img
def b_cta():
    img, d = canvas()
    eyebrow(d, 90, 200, "G R A T I S   T E S T W E B S I T E")
    big = font(104, 900)
    d.text((90, 300), "Eerst zien,", font=big, fill=WHITE); d.text((90, 420), "dan beslissen.", font=big, fill=GOLD)
    paragraph(d, 90, 620, "Wij bouwen eerst gratis een voorbeeld van jouw nieuwe website. Bevalt het? Dan gaan we door. Websites vanaf €499.", font(40, 500, "Inter.ttf"), 880)
    d.rounded_rectangle([90, 900, 640, 1000], 16, fill=GOLD); d.text((130, 925), "Link in bio  →", font=font(40, 800), fill=BG)
    d.text((90, 1060), "skylinedigital.nl", font=font(36, 700), fill=WHITE)
    logo(img, 90, 1180); return img
save(b_cover(), "websites-01.jpg")
for i, c in enumerate(CLIENTS): save(b_client(*c, idx=i + 1, total=len(CLIENTS)), f"websites-{i + 2:02d}.jpg")
save(b_cta(), "websites-06.jpg")

# ---------- Post C: SEO zelf doen of uitbesteden ----------
def c_seo():
    ph = Image.open(os.path.join(A, "photo-studio-monitor.jpg")).convert("RGB")
    sc = max(W / ph.width, H / ph.height); ph = ph.resize((int(ph.width * sc), int(ph.height * sc)), Image.LANCZOS)
    ph = ph.crop(((ph.width - W) // 2, 0, (ph.width - W) // 2 + W, H)).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for yy in range(H): od.line([(0, yy), (W, yy)], fill=BG + (int(255 * max(0, min(1, (yy - 300) / 620)) * 0.94),))
    ph.alpha_composite(ov)
    top = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); td = ImageDraw.Draw(top)
    for yy in range(300): td.line([(0, yy), (W, yy)], fill=BG + (int(235 * max(0, 1 - yy / 300) ** 0.8),))
    ph.alpha_composite(top); d = ImageDraw.Draw(ph)
    logo(ph, 90, 80, 220)
    eyebrow(d, 90, 640, "S E O")
    big = font(100, 900)
    d.text((90, 700), "Zelf doen", font=big, fill=WHITE); d.text((90, 815), "of uitbesteden?", font=big, fill=GOLD)
    paragraph(d, 90, 970, "Zelf kun je veel: je Google Bedrijfsprofiel, reviews, duidelijke teksten. Het schrijven en bijhouden kost alleen elke week tijd. Dat nemen wij over vanaf €39 per maand.", font(36, 500, "Inter.ttf"), 900, SOFT, 52)
    d.text((90, 1220), "Link in bio  ·  skylinedigital.nl", font=font(34, 700), fill=GOLD)
    return ph
save(c_seo(), "seo-uitbesteden.jpg")

# ---------- Overzichtsblad ----------
files = [f for f in sorted(os.listdir(OUT)) if f.endswith(".jpg") and not f.startswith("_")]
th = 300; tw_ = int(th * W / H); cols = 7; rows = (len(files) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (tw_ + 10) + 10, rows * (th + 40) + 10), (30, 30, 34)); sd = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(os.path.join(OUT, f)).resize((tw_, th), Image.LANCZOS)
    x = 10 + (i % cols) * (tw_ + 10); y = 10 + (i // cols) * (th + 40)
    sheet.paste(im, (x, y)); sd.text((x, y + th + 8), f, fill=(200, 200, 200), font=font(18, 500, "Inter.ttf"))
sheet.save(os.path.join(OUT, "_overzicht.jpg"), quality=85)
print("klaar:", files)
