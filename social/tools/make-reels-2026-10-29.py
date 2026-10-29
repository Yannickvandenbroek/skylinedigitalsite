"""Drie Reels (9:16) uit bestaande video's, zonder Higgsfield: Van Hees Cooking (bedrijfsvideo),
autodetailing (bedrijfsvideo) en Villa Maillard (villafilm). Hook in beeld vanaf frame 1, kleine
regel eronder, eindkaart in huisstijl. Overlays met Pillow, montage met ffmpeg.
Gebruik: python3 make-reels-2026-10-29.py <map met bronvideo's>  → social/2026-10-29-reels/"""
import os, sys, subprocess, json
from PIL import Image, ImageDraw, ImageFont
S = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(S, "..", ".."))
A = os.path.join(ROOT, "assets")
SRC = sys.argv[1]
OUT = os.path.join(ROOT, "social", "2026-10-29-reels"); os.makedirs(OUT, exist_ok=True)
TMP = os.path.join(SRC, "tmp"); os.makedirs(TMP, exist_ok=True)
MUZIEK = "/Users/yannickvandenbroek/Documents/Skylinedigital/skylinedigitalcrm/scripts/muziek/standaard.mp3"
W, H = 1080, 1920
BG = (7, 8, 11); GOLD = (217, 178, 90); WHITE = (244, 241, 233); SOFT = (222, 219, 210)

def font(size, weight=800, face="InterTight.ttf"):
    f = ImageFont.truetype(os.path.join(S, face), size)
    try: f.set_variation_by_axes([weight] if face == "InterTight.ttf" else [14, weight])
    except Exception: pass
    return f
def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
def logo(img, x, y, w=220):
    lg = Image.open(os.path.join(A, "logo.png")).convert("RGBA")
    lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS); img.paste(lg, (x, y), lg)
def shadowed(d, xy, text, f, fill):
    x, y = xy
    for dx, dy in ((3, 3), (-2, 2), (2, -2)): d.text((x + dx, y + dy), text, font=f, fill=(0, 0, 0, 200))
    d.text((x, y), text, font=f, fill=fill)

def overlay_hook(name, hook_wit, hook_goud, sub):
    """Hooktekst boven de video (0-3,5 s) + kleine regel eronder (hele tijd)."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    logo(img, 70, 110, 200)
    f = font(84, 900); y = 330
    for l in wrap(d, hook_wit, f, 940): shadowed(d, (70, y), l, f, WHITE); y += 96
    for l in wrap(d, hook_goud, f, 940): shadowed(d, (70, y), l, f, GOLD); y += 96
    img.save(os.path.join(TMP, f"{name}-hook.png"))
    sub_img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d2 = ImageDraw.Draw(sub_img)
    logo(sub_img, 70, 110, 200)
    fs = font(44, 500, "Inter.ttf"); y = 1310
    for l in wrap(d2, sub, fs, 940): shadowed(d2, (70, y), l, fs, SOFT); y += 60
    sub_img.save(os.path.join(TMP, f"{name}-sub.png"))

def overlay_end(name, kop1, kop2, regel, cta):
    img = Image.new("RGBA", (W, H), BG + (235,)); d = ImageDraw.Draw(img)
    logo(img, 70, 160, 260)
    f = font(104, 900); d.text((70, 560), kop1, font=f, fill=WHITE); d.text((70, 680), kop2, font=f, fill=GOLD)
    fs = font(44, 500, "Inter.ttf"); y = 860
    for l in wrap(d, regel, fs, 940): d.text((70, y), l, font=fs, fill=SOFT); y += 60
    d.rounded_rectangle([70, y + 60, 640, y + 160], 18, fill=GOLD); d.text((110, y + 86), cta, font=font(40, 800), fill=BG)
    d.text((70, y + 220), "skylinedigital.nl", font=font(36, 700), fill=WHITE)
    img.save(os.path.join(TMP, f"{name}-end.png"))

def duur(pad):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", pad]).decode().strip())

def maak(name, bron, hook_wit, hook_goud, sub, end, muziek=True):
    overlay_hook(name, hook_wit, hook_goud, sub); overlay_end(name, *end)
    D = duur(bron); hook_tot = 3.5; end_vanaf = D - 2.0
    hook = os.path.join(TMP, f"{name}-hook.png"); subp = os.path.join(TMP, f"{name}-sub.png"); endp = os.path.join(TMP, f"{name}-end.png")
    uit = os.path.join(OUT, f"reel-{name}.mp4")
    # achtergrond: dezelfde video vullend, geblurd en donker; voorgrond: video op 1080 breed in het midden
    fc = (
        f"[0:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:5,eq=brightness=-0.25[bg];"
        f"[0:v]scale={W}:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2[v0];"
        f"[v0][1:v]overlay=0:0:enable='between(t,0,{hook_tot})'[v1];"
        f"[v1][2:v]overlay=0:0:enable='between(t,{hook_tot},{end_vanaf})'[v2];"
        f"[3:v]format=rgba,fade=t=in:st={end_vanaf}:d=0.6:alpha=1[endf];"
        f"[v2][endf]overlay=0:0:enable='gte(t,{end_vanaf})'[vout]"
    )
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", bron, "-loop", "1", "-i", hook, "-loop", "1", "-i", subp, "-loop", "1", "-i", endp]
    if muziek: cmd += ["-i", MUZIEK]
    cmd += ["-filter_complex", fc, "-map", "[vout]"]
    if muziek: cmd += ["-map", "4:a", "-af", f"afade=t=out:st={D-1.5}:d=1.5", "-shortest"]
    else: cmd += ["-map", "0:a?", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-t", f"{D:.2f}", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "19", "-preset", "medium", "-movflags", "+faststart"]
    if muziek: cmd += ["-c:a", "aac", "-b:a", "192k"]
    cmd += [uit]
    subprocess.run(cmd, check=True)
    # cover (frame op 1 s) voor het overzicht
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "1", "-i", uit, "-frames:v", "1", os.path.join(OUT, f"reel-{name}-cover.jpg")], check=True)
    print("klaar:", uit, f"{duur(uit):.1f}s")

maak("vanhees", os.path.join(SRC, "vanhees.mp4"),
     "Deze bedrijfsvideo", "kostte €50.",
     "Geen filmploeg, geen opnamedag. Eén foto van de chef was genoeg. Van Hees Cooking, catering in Brabant.",
     ("Jouw bedrijf", "ook in beeld?", "AI-bedrijfsvideo vanaf €50. Echte shoot met drone vanaf €250. Je ziet eerst een voorbeeld.", "Link in bio  →"))

maak("detailing", os.path.join(SRC, "wa.mp4"),
     "Dit is geen", "BMW-reclame.",
     "Dit is een detailingbedrijf. Video gemaakt zonder camera, zonder opnamedag.",
     ("Zo ziet jouw", "bedrijf eruit.", "AI-bedrijfsvideo vanaf €50. Echte shoot met drone vanaf €250. Je ziet eerst een voorbeeld.", "Link in bio  →"))

maak("pilar", os.path.join(SRC, "pilar.mp4"),
     "Zo boek je je villa vol", "vóór het seizoen begint.",
     "Casa Pilar, Jávea. Eén fotoshoot, één film, geen drone nodig.",
     ("Jouw villa", "ook zo in beeld?", "Vraag een gratis voorbeeldvideo aan. Bevalt het? Dan pas betalen.", "Link in bio  →"), muziek=False)

# overzicht van de covers + een frame halverwege
files = sorted(f for f in os.listdir(OUT) if f.endswith(".mp4"))
sheet = Image.new("RGB", (len(files) * 2 * 330 + 10, 600 + 50), (30, 30, 34)); sd = ImageDraw.Draw(sheet)
x = 10
for f in files:
    for t in (1, duur(os.path.join(OUT, f)) - 1):
        fr = os.path.join(TMP, "fr.jpg")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.2f}", "-i", os.path.join(OUT, f), "-frames:v", "1", fr], check=True)
        im = Image.open(fr).resize((320, 569), Image.LANCZOS); sheet.paste(im, (x, 10)); sd.text((x, 590), f"{f} @{t:.0f}s", fill=(200, 200, 200), font=font(18, 500, "Inter.ttf")); x += 330
sheet.save(os.path.join(OUT, "_overzicht.jpg"), quality=85)
