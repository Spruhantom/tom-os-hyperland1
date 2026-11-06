#!/usr/bin/env python3
"""Generate the second Tom OS wallpaper: 'Neon Eclipse' — glowing ring, hex grid, light rays."""
import math
import random
from PIL import Image, ImageDraw, ImageFilter

import sys
W, H = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (3840, 2160)
S = H / 2160.0  # scale factor for absolute sizes

BG_TOP = (5, 4, 16)
BG_BOT = (30, 8, 52)
RING_CYAN = (0, 229, 255)
RING_MAGENTA = (255, 45, 150)
RING_PURPLE = (180, 80, 255)
STAR = (200, 220, 255)

random.seed(9137)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# vertical gradient
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOT, t ** 0.85))

# stars
for _ in range(int(900 * S * (W / 3840.0 if W > H else 1)) + 100):
    x, y = random.randint(0, W), random.randint(0, int(H * 0.72))
    s = random.choice([1, 1, 1, 2, 2, 3])
    b = random.randint(60, 220)
    d.ellipse([x, y, x + s, y + s], fill=(b, b + 15, min(255, b + int(40 * S))))

cx, cy = int(W * 0.5), int(H * 0.44)
R = int(H * 0.30)

# ---- radial glow behind the ring ----
glow = Image.new("L", (W, H), 0)
gd = ImageDraw.Draw(glow)
for i in range(60):
    r = R + i * 14
    gd.ellipse([cx - r, cy - r, cx + r, cy + r], outline=max(0, 40 - i), width=14)
glow_blur = glow.filter(ImageFilter.GaussianBlur(60))
glow_col = Image.new("RGB", (W, H), (18, 6, int(40 * S)))
img = Image.composite(glow_col, img, glow_blur.point(lambda p: min(255, p * 3)))
d = ImageDraw.Draw(img)

# ---- light rays from the ring center ----
rays = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rd = ImageDraw.Draw(rays)
for a in range(0, 360, 6):
    ang = math.radians(a)
    if 95 < a % 360 < 265:      # rays only upward/outward
        pass
    length = random.randint(int(R * 1.4), int(R * 2.4))
    x2 = cx + math.cos(ang) * length
    y2 = cy + math.sin(ang) * length
    col = RING_CYAN if a % 12 == 0 else (140, 90, 255, int(40 * S))
    rd.line([(cx, cy), (x2, y2)], fill=col + (26,) if isinstance(col, tuple) and len(col) == 3 else col,
            width=random.choice([2, 3, 4]))
rays = rays.filter(ImageFilter.GaussianBlur(8))
img = Image.alpha_composite(img.convert("RGBA"), rays).convert("RGB")
d = ImageDraw.Draw(img)

# ---- the eclipse ring (gradient stroke cyan -> magenta) ----
ring = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rdr = ImageDraw.Draw(ring)
steps = 360
for i in range(steps):
    t = i / steps
    # cyclic gradient: cyan -> magenta -> cyan (no seam)
    tt = (1 - math.cos(2 * math.pi * t)) / 2
    col = lerp(RING_CYAN, RING_MAGENTA, tt)
    rdr.arc([cx - R, cy - R, cx + R, cy + R], i, i + 2, fill=col, width=26)
# glow pass
ring_glow = ring.filter(ImageFilter.GaussianBlur(30))
img = Image.alpha_composite(img.convert("RGBA"), ring_glow)
img = Image.alpha_composite(img, ring)
img = img.convert("RGB")
d = ImageDraw.Draw(img)

# inner dark disc (the "eclipse")
d.ellipse([cx - R + 26, cy - R + 26, cx + R - 26, cy + R - 26], fill=(7, 5, 18))

# second thin ring
R2 = int(R * 1.35)
rdr2 = ImageDraw.Draw(Image.new("RGBA", (W, H)))
d.arc([cx - R2, cy - R2, cx + R2, cy + R2], 0, 360, fill=RING_PURPLE, width=4)

# ---- hex grid floor (bottom third) ----
hexes = Image.new("RGBA", (W, H), (0, 0, 0, 0))
hd = ImageDraw.Draw(hexes)
hex_r = int(90 * S)
floor_y = int(H * 0.80)
for row in range(20):
    yy = floor_y + row * hex_r * 0.95
    if yy > H + hex_r:
        break
    off = (row % 2) * hex_r * 0.87
    fade = max(0, 1 - (yy - floor_y) / (H - floor_y + 1))
    col = (0, 229, 255, int(150 * fade)) if row % 2 else (255, 45, 150, int(120 * fade))
    for xx in range(-2, int(W / (hex_r * 1.74)) + 2):
        x0 = xx * hex_r * 1.74 + off
        pts = [(x0 + hex_r * math.cos(math.radians(60 * k)),
               yy + hex_r * 0.95 * math.sin(math.radians(60 * k))) for k in range(6)]
        hd.polygon(pts, outline=col, width=3)
img = Image.alpha_composite(img.convert("RGBA"), hexes).convert("RGB")
d = ImageDraw.Draw(img)

# ---- wordmark + logo watermark ----
try:
    logo = Image.open("/home/user/workspace/neonpunk-os/assets/logo-tomos-256.png").convert("RGBA")
    ls = int(320 * S)
    logo = logo.resize((ls, ls), Image.LANCZOS)
    # soft white glow behind logo
    lm = logo.split()[3].point(lambda p: p // 3)
    glowpad = Image.new("RGBA", (ls + int(80 * S), ls + int(80 * S)), (0, 0, 0, 0))
    glowpad.paste(Image.new("RGBA", (ls, ls), (120, 200, 255, 90)), (int(40 * S), int(40 * S)), lm)
    glowpad = glowpad.filter(ImageFilter.GaussianBlur(int(20 * S)))
    img.paste(glowpad, (W - ls - int(220 * S), H - ls - int(180 * S)), glowpad)
    img.paste(logo, (W - ls - int(200 * S), H - ls - int(160 * S)), logo)
except Exception as e:
    print("logo skip:", e)

# caption
try:
    from PIL import ImageFont
    f_big = ImageFont.truetype(
        "/home/user/workspace/neonpunk-os/build/config/includes.chroot/usr/share/fonts/truetype/jetbrains-mono-nerd/JetBrainsMonoNerdFont-ExtraBold.ttf", int(88 * S))
    f_sm = ImageFont.truetype(
        "/home/user/workspace/neonpunk-os/build/config/includes.chroot/usr/share/fonts/truetype/jetbrains-mono-nerd/JetBrainsMonoNerdFont-Medium.ttf", int(40 * S))
    d.text((W - int(760 * S), H - int(300 * S)), "TOM OS", font=f_big, fill=(240, 240, 250))
    d.text((W - int(760 * S), H - int(190 * S)), "neon punk edition", font=f_sm, fill=(160, 150, 200))
except Exception as e:
    print("font skip:", e)

import sys as _s
base = _s.argv[3] if len(_s.argv) > 3 else "/home/user/workspace/neonpunk-os/assets/wallpaper-eclipse"
img.save(base + ".png")
print("wrote", base + ".png", img.size)
