#!/usr/bin/env python3
"""Generate the NeonPunk OS wallpaper: synthwave grid, neon sun, city skyline."""
import math
import random
from PIL import Image, ImageDraw, ImageFilter

W, H = 3840, 2160
HORIZON = int(H * 0.62)

# Palette
BG_TOP = (6, 4, 14)
BG_BOT = (26, 10, 46)
SUN_COLORS = [(255, 45, 120), (255, 90, 60), (255, 190, 60)]  # magenta -> orange -> yellow
GRID_PINK = (255, 45, 150)
GRID_CYAN = (0, 240, 255)
CITY = (10, 6, 20)

random.seed(4224)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_gradient(img):
    d = ImageDraw.Draw(img)
    for y in range(HORIZON + 1):
        t = y / HORIZON
        d.line([(0, y), (W, y)], fill=lerp(BG_TOP, BG_BOT, t ** 0.8))


def stars(img):
    d = ImageDraw.Draw(img)
    for _ in range(1400):
        x = random.randint(0, W)
        y = random.randint(0, HORIZON - 120)
        s = random.choice([1, 1, 1, 2])
        b = random.randint(120, 255)
        c = random.choice([(b, b, b), (b, b, 255), (255, b, b), (b, 255, b)])
        d.ellipse([x, y, x + s, y + s], fill=c)


def draw_sun(img):
    cx, cy, r = W // 2, HORIZON - int(H * 0.05), int(H * 0.30)
    sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sun)
    for i in range(r, 0, -1):
        t = 1 - i / r
        if t < 0.5:
            c = lerp(SUN_COLORS[0], SUN_COLORS[1], t * 2)
        else:
            c = lerp(SUN_COLORS[1], SUN_COLORS[2], (t - 0.5) * 2)
        d.ellipse([cx - i, cy - i, cx + i, cy + i], fill=(*c, 255))
    # retro horizontal stripes on lower half
    stripe_h = 10
    gap_growth = 1.16
    y = cy + 10
    h = stripe_h
    while y < cy + r:
        d.rectangle([cx - r - 4, y, cx + r + 4, y + h], fill=(6, 4, 14, 255))
        y += h + max(6, int(h * 0.45))
        h = int(h * gap_growth)
    # mask below horizon
    mask = Image.new("L", (W, H), 0)
    md = ImageDraw.Draw(mask)
    md.rectangle([0, HORIZON, W, H], fill=255)
    sun = Image.composite(Image.new("RGBA", (W, H), (0, 0, 0, 0)), sun, mask)
    # glow
    glow = sun.filter(ImageFilter.GaussianBlur(60))
    img.paste(glow, (0, 0), glow)
    img.paste(sun, (0, 0), sun)


def draw_grid(img):
    d = ImageDraw.Draw(img)
    vx = W // 2
    # vertical rays
    for i in range(-16, 17):
        x2 = vx + i * (W // 8)
        d.line([(vx, HORIZON), (x2, H)], fill=GRID_PINK, width=3)
    # horizontal lines with exponential spacing
    y = HORIZON + 4
    step = 6
    while y < H:
        d.line([(0, y), (W, y)], fill=GRID_CYAN, width=3)
        step = int(step * 1.28)
        y += step
    # horizon glow line
    d.line([(0, HORIZON), (W, HORIZON)], fill=GRID_PINK, width=8)


def draw_city(img):
    d = ImageDraw.Draw(img)
    x = 0
    while x < W:
        bw = random.randint(60, 220)
        bh = random.randint(40, 300)
        top = HORIZON - bh
        d.rectangle([x, top, x + bw, HORIZON], fill=CITY)
        # neon window dots
        for _ in range(random.randint(2, 14)):
            wx = random.randint(x + 8, x + bw - 12)
            wy = random.randint(top + 10, HORIZON - 12)
            c = random.choice([GRID_PINK, GRID_CYAN, (255, 225, 77)])
            d.rectangle([wx, wy, wx + 6, wy + 8], fill=c)
        x += bw + random.randint(8, 60)
    # reflection hint under city
    d.line([(0, HORIZON - 2), (W, HORIZON - 2)], fill=(255, 45, 150))


def vignette(img):
    v = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(v)
    vd.rectangle([0, 0, W, H], fill=255)
    vd.ellipse([-W * 0.25, -H * 0.35, W * 1.25, H * 1.35], fill=0)
    v = v.filter(ImageFilter.GaussianBlur(400))
    black = Image.new("RGB", (W, H), (0, 0, 0))
    img.paste(black, (0, 0), v.point(lambda p: int(p * 0.45)))


def main():
    img = Image.new("RGB", (W, H))
    sky_gradient(img)
    stars(img)
    draw_sun(img)
    draw_city(img)
    draw_grid(img)
    vignette(img)
    img.save("wallpaper.png", optimize=True)
    # downscaled variant for small screens
    img.resize((1920, 1080), Image.LANCZOS).save("wallpaper-1080.png", optimize=True)
    print("wallpaper done")


if __name__ == "__main__":
    main()
