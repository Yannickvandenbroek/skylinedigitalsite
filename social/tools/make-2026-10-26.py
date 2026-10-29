import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S = os.path.dirname(os.path.abspath(__file__))
A = "/Users/yannickvandenbroek/Documents/Skylinedigital/own site/skyline-digital/assets"
OUT = os.path.join(S, "out"); os.makedirs(OUT, exist_ok=True)
BG = (7, 8, 11); GOLD = (217, 178, 90); GOLDHI = (247, 227, 161); WHITE = (244, 241, 233); DIM = (170, 168, 160)
W, H = 1080, 1350

def font(size, weight=800, face="InterTight.ttf"):
    f = ImageFont.truetype(os.path.join(S, face), size)
    try: f.set_variation_by_axes([weight] if face == "InterTight.ttf" else [14, weight])
    except Exception: pass
    return f

def text_w(d, t, f): return d.textlength(t, font=f)

def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(d, t, f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def logo(img, x, y, w=240):
    lg = Image.open(os.path.join(A, "logo.png")).convert("RGBA")
    lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS)
    img.paste(lg, (x, y), lg)

def eyebrow(d, x, y, text):
    d.line([(x, y + 13), (x + 48, y + 13)], fill=GOLD, width=3)
    d.text((x + 66, y), text, font=font(26, 600), fill=GOLD, spacing=4)

def rounded(im, r):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    out = Image.new("RGBA", im.size); out.paste(im, (0, 0), m); return out

def glow(img):
    # zachte gouden gloed linksboven, zoals op de site
    g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    gd.ellipse([-300, -380, 700, 420], fill=(217, 178, 90, 60))
    g = g.filter(ImageFilter.GaussianBlur(160)); img.alpha_composite(g)

# ---------- Carrousel: websites die we bouwden ----------
def cover():
    img = Image.new("RGBA", (W, H), BG + (255,)); glow(img); d = ImageDraw.Draw(img)
    eyebrow(d, 90, 150, "P O R T F O L I O")
    big = font(120, 900)
    d.text((90, 250), "Websites", font=big, fill=WHITE)
    d.text((90, 380), "die we", font=big, fill=WHITE)
    d.text((90, 510), "bouwden.", font=big, fill=GOLD)
    sub = font(40, 500, "Inter.ttf")
    for i, l in enumerate(wrap(d, "Maatwerk websites voor ondernemers in heel Nederland. Snel, vindbaar en gebouwd om klanten op te leveren.", sub, 860)):
        d.text((90, 720 + i * 58), l, font=sub, fill=DIM)
    d.text((90, 1050), "Swipe", font=font(36, 700), fill=WHITE); d.text((205, 1050), "→", font=font(36, 700), fill=GOLD)
    logo(img, 90, 1180)
    return img

CLIENTS = [
    ("lassie", "Keukenmontage Lassie", "Veendam", "Cinematische site met scroll-animatie"),
    ("dejonge", "De Jonge Elektrotechniek", "Nijkerk", "Krachtige site, gebouwd om gevonden te worden"),
    ("palmyra", "Palmyra Coaching", "Oss", "Rust, balans en vertrouwen in beeld"),
    ("elektropost", "Elektropost", "Woudenberg", "Fris, persoonlijk en helder"),
    ("carslease", "CarsLease", "Eindhoven", "Leaseplatform met calculator"),
]
def client_slide(slug, name, city, line, idx, total):
    img = Image.new("RGBA", (W, H), BG + (255,)); glow(img); d = ImageDraw.Draw(img)
    shot = Image.open(os.path.join(A, f"work-{slug}-m.jpg")).convert("RGB")
    sw = 440; sh = int(shot.height * sw / shot.width)          # 440 x 953
    shot = shot.resize((sw, sh), Image.LANCZOS)
    # telefoonframe
    frame = Image.new("RGBA", (sw + 28, sh + 28), (24, 25, 30, 255)); frame = rounded(frame, 58)
    ph = Image.new("RGBA", frame.size, (0, 0, 0, 0)); ph.alpha_composite(frame)
    ph.alpha_composite(rounded(shot.convert("RGBA"), 44), (14, 14))
    shadow = Image.new("RGBA", (ph.width + 160, ph.height + 160), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle([80, 100, 80 + ph.width, 100 + ph.height], 58, fill=(0, 0, 0, 170))
    shadow = shadow.filter(ImageFilter.GaussianBlur(40))
    x = (W - ph.width) // 2; y = 70
    img.alpha_composite(shadow, (x - 80, y - 80)); img.alpha_composite(ph, (x, y))
    # onderbalk met tekst
    grad = Image.new("RGBA", (W, 360), (0, 0, 0, 0)); gd = ImageDraw.Draw(grad)
    for i in range(360): gd.line([(0, i), (W, i)], fill=BG + (int(255 * min(1, i / 140)),))
    img.alpha_composite(grad, (0, H - 360)); d = ImageDraw.Draw(img)
    d.text((90, 1085), f"0{idx}", font=font(30, 700), fill=GOLD)
    d.text((150, 1085), f"·  {city}", font=font(30, 500, "Inter.ttf"), fill=DIM)
    nf = font(58, 800)
    if text_w(d, name, nf) > 900: nf = font(50, 800)
    d.text((90, 1135), name, font=nf, fill=WHITE)
    d.text((90, 1215), line, font=font(34, 500, "Inter.ttf"), fill=DIM)
    d.text((W - 90 - text_w(d, f"{idx}/{total}", font(28, 600)), 1090), f"{idx}/{total}", font=font(28, 600), fill=DIM)
    return img

def cta_slide():
    img = Image.new("RGBA", (W, H), BG + (255,)); glow(img); d = ImageDraw.Draw(img)
    eyebrow(d, 90, 200, "G R A T I S   T E S T W E B S I T E")
    big = font(104, 900)
    d.text((90, 300), "Jouw bedrijf", font=big, fill=WHITE)
    d.text((90, 420), "als volgende?", font=big, fill=GOLD)
    sub = font(40, 500, "Inter.ttf")
    for i, l in enumerate(wrap(d, "Wij bouwen eerst gratis een voorbeeld van jouw nieuwe website. Bevalt het? Dan gaan we door. Websites vanaf €499.", sub, 880)):
        d.text((90, 620 + i * 58), l, font=sub, fill=DIM)
    # knop
    d.rounded_rectangle([90, 900, 640, 1000], 16, fill=GOLD)
    d.text((130, 925), "Link in bio  →", font=font(40, 800), fill=BG)
    d.text((90, 1060), "skylinedigital.nl", font=font(36, 700), fill=WHITE)
    logo(img, 90, 1180)
    return img

slides = [cover()] + [client_slide(*c, idx=i + 1, total=len(CLIENTS)) for i, c in enumerate(CLIENTS)] + [cta_slide()]
for i, s in enumerate(slides, 1):
    s.convert("RGB").save(os.path.join(OUT, f"carrousel-{i:02d}.jpg"), quality=92)

# ---------- Post: gratis testwebsite ----------
def testsite():
    ph = Image.open(os.path.join(A, "photo-laptop-desk.jpg")).convert("RGB")
    sc = max(W / ph.width, H / ph.height); ph = ph.resize((int(ph.width * sc), int(ph.height * sc)), Image.LANCZOS)
    ph = ph.crop(((ph.width - W) // 2, 0, (ph.width - W) // 2 + W, H)).convert("RGBA")
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    for yy in range(H):
        a = int(255 * max(0, min(1, (yy - 330) / 620)) * 0.94)
        od.line([(0, yy), (W, yy)], fill=BG + (a,))
    ph.alpha_composite(ov)
    top = Image.new("RGBA", (W, 300), (0, 0, 0, 0)); td = ImageDraw.Draw(top)
    for yy in range(300): td.line([(0, yy), (W, yy)], fill=BG + (int(235 * max(0, 1 - yy / 300) ** 0.8),))
    ph.alpha_composite(top); d = ImageDraw.Draw(ph)
    logo(ph, 90, 80, 220)
    eyebrow(d, 90, 700, "G R A T I S   T E S T W E B S I T E")
    big = font(108, 900)
    d.text((90, 760), "Eerst zien,", font=big, fill=WHITE)
    d.text((90, 880), "dan beslissen.", font=big, fill=GOLD)
    sub = font(38, 500, "Inter.ttf")
    for i, l in enumerate(wrap(d, "Wij bouwen gratis een voorbeeld van jouw nieuwe website. Bevalt het? Dan gaan we door — vanaf €499.", sub, 900)):
        d.text((90, 1035 + i * 54), l, font=sub, fill=(222, 219, 210))
    d.text((90, 1220), "Link in bio  ·  skylinedigital.nl", font=font(34, 700), fill=GOLD)
    return ph
testsite().convert("RGB").save(os.path.join(OUT, "testwebsite.jpg"), quality=92)

# ---------- Teksten voor de Reel (overlay-PNG's) ----------
def reel_overlay():
    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    logo(img, 80, 140, 230)
    eyebrow(d, 80, 300, "V I L L A - F I L M")
    d.text((80, 360), "Modern Villa", font=font(96, 900), fill=WHITE)
    d.text((80, 470), "Moraira.", font=font(96, 900), fill=GOLD)
    sub = font(40, 500, "Inter.ttf")
    d.text((80, 1450), "Jouw villa ook zo in beeld?", font=font(54, 800), fill=WHITE)
    for i, l in enumerate(wrap(d, "Vraag een gratis voorbeeldvideo aan. Link in bio.", sub, 920)):
        d.text((80, 1530 + i * 56), l, font=sub, fill=(222, 219, 210))
    d.text((80, 1680), "skylinedigital.nl", font=font(38, 700), fill=GOLD)
    return img
reel_overlay().save(os.path.join(OUT, "reel-overlay.png"))
print("klaar:", sorted(os.listdir(OUT)))
