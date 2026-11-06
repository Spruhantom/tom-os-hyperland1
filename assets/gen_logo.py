#!/usr/bin/env python3
"""Generate NeonPunk OS logo: neon hexagon with lightning bolt."""
import glob
from PIL import Image, ImageDraw, ImageFilter, ImageFont

S = 512
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

cx = cy = S // 2
r = 200
# hexagon vertices
pts = []
for i in range(6):
    a = math.radians(60 * i - 30) if False else 0  # noqa
import math
pts = [(cx + r * math.cos(math.radians(60 * i - 90)),
        cy + r * math.sin(math.radians(60 * i - 90))) for i in range(6)]

# glow layers
for width, color in [(26, (255, 45, 150, 60)), (16, (255, 45, 150, 120)), (10, (0, 240, 255, 255))]:
    d.polygon(pts, outline=color, width=width, fill=(10, 6, 20, 200))

# lightning bolt
bolt = [(cx - 40, cy - 130), (cx + 60, cy - 130), (cx + 5, cy - 20),
        (cx + 55, cy - 20), (cx - 55, cy + 130), (cx - 5, cy + 10),
        (cx - 60, cy + 10)]
d.polygon(bolt, fill=(0, 240, 255, 255))

# glow the bolt
glow = img.filter(ImageFilter.GaussianBlur(18))
out = Image.alpha_composite(glow, img)
out = out.resize((256, 256), Image.LANCZOS)
out.save("logo.png")

# simple square banner for GRUB/branding
banner = Image.new("RGBA", (600, 200), (10, 6, 20, 255))
bd = ImageDraw.Draw(banner)
fonts = glob.glob("/home/user/workspace/neonpunk-os/sources/font/*/*.ttf")
font_path = fonts[0] if fonts else None
f1 = ImageFont.truetype(font_path, 64) if font_path else ImageFont.load_default()
f2 = ImageFont.truetype(font_path, 28) if font_path else ImageFont.load_default()
bd.text((30, 40), "NEONPUNK", font=f1, fill=(255, 45, 150, 255))
bd.text((34, 120), "OS // hyprland edition", font=f2, fill=(0, 240, 255, 255))
banner.save("banner.png")
print("logo + banner done")
