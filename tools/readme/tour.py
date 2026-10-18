"""Build an animated WebP tour of screenshots inside a browser window.

usage: python3 tour.py tour.json out.webp
tour.json: {"fonts": {"semibold": "...ttf", "regular": "...ttf"},
            "shots": [{"image": "...", "url": "sky.obelisk.ar/app", "caption": "..."}]}
Needs Pillow. See development-style/readme-showcase.md.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

cfg = json.load(open(sys.argv[1])); out_path = sys.argv[2]
shots = cfg['shots']
fs = ImageFont.truetype(cfg['fonts']['semibold'], 22)
fu = ImageFont.truetype(cfg['fonts']['regular'], 15)
W, CH, BAR, PAD = 1120, 700, 46, 22          # content 16:10, browser bar, outer padding
HOLD, FADE_FRAMES, FADE_MS = 2600, 5, 60
TW, TH = W + PAD * 2, CH + BAR + PAD * 2

def cover(im):
    r = max(W / im.width, CH / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    x, y = (im.width - W) // 2, (im.height - CH) // 2
    return im.crop((x, y, x + W, y + CH))

# Sky gradient background with a soft window shadow
bg = Image.new('RGB', (TW, TH)); d = ImageDraw.Draw(bg)
for y in range(TH):
    t = y / TH
    d.line([(0, y), (TW, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip((143, 211, 255), (232, 246, 255))))
sh = Image.new('L', (TW, TH), 0)
ImageDraw.Draw(sh).rounded_rectangle([PAD, PAD + 10, PAD + W, PAD + BAR + CH + 6], 18, fill=110)
bg.paste((15, 42, 68), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
mask = Image.new('L', (W, BAR + CH), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, W - 1, BAR + CH - 1], 16, fill=255)

def frame(i, shot):
    win = Image.new('RGB', (W, BAR + CH), (24, 27, 34)); wd = ImageDraw.Draw(win)
    for k, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        wd.ellipse([18 + k * 22, 17, 30 + k * 22, 29], fill=c)
    wd.rounded_rectangle([W // 2 - 200, 10, W // 2 + 200, 36], 13, fill=(42, 46, 56))
    wd.text((W // 2, 23), shot['url'], font=fu, fill=(210, 216, 226), anchor='mm')
    win.paste(cover(Image.open(shot['image']).convert('RGB')), (0, BAR))
    cap = shot['caption']; tw = wd.textlength(cap, font=fs); x0, y0 = 24, BAR + CH - 72
    ov = Image.new('RGBA', win.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.rounded_rectangle([x0, y0, x0 + tw + 64, y0 + 48], 24, fill=(15, 42, 68, 230))
    od.ellipse([x0 + 18, y0 + 18, x0 + 30, y0 + 30], fill=(197, 255, 110, 255))
    od.text((x0 + 42, y0 + 24), cap, font=fs, fill=(255, 255, 255, 255), anchor='lm')
    n = len(shots); dx = W - 24 - n * 18
    for k in range(n):
        od.ellipse([dx + k * 18, y0 + 19, dx + k * 18 + 10, y0 + 29], fill=(197, 255, 110, 255) if k == i else (255, 255, 255, 150))
    win = Image.alpha_composite(win.convert('RGBA'), ov).convert('RGB')
    out = bg.copy(); out.paste(win, (PAD, PAD), mask); return out

frames = [frame(i, s) for i, s in enumerate(shots)]
seq, dur = [], []
for i, f in enumerate(frames):
    seq.append(f); dur.append(HOLD)
    nxt = frames[(i + 1) % len(frames)]
    for s in range(1, FADE_FRAMES + 1):
        seq.append(Image.blend(f, nxt, s / (FADE_FRAMES + 1))); dur.append(FADE_MS)
seq[0].save(out_path, save_all=True, append_images=seq[1:], duration=dur, loop=0, quality=78, method=4)
print(f'{out_path}: {os.path.getsize(out_path) // 1024} KB, {len(seq)} frames, {TW}x{TH}')
