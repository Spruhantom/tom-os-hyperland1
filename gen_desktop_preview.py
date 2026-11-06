#!/usr/bin/env python3
"""Render a faithful preview of the Tom OS Hyprland desktop (waybar + kitty)."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = "/home/user/workspace/neonpunk-os"
FONT_DIR = ROOT + "/build/config/includes.chroot/usr/share/fonts/truetype/jetbrains-mono-nerd"
W, H = 1920, 1080

base = Image.open(ROOT + "/assets/wallpaper-eclipse-1080.png").convert("RGBA")
img = base.copy()

JBM = FONT_DIR + "/JetBrainsMonoNerdFont-Medium.ttf"
JBM_BOLD = FONT_DIR + "/JetBrainsMonoNerdFont-Bold.ttf"
JBM_XB = FONT_DIR + "/JetBrainsMonoNerdFont-ExtraBold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------------- waybar ----------------
BAR_H, BAR_MARGIN_X, BAR_MARGIN_Y = 34, 12, 8
bar_x0, bar_x1 = BAR_MARGIN_X, W - BAR_MARGIN_X
bar_y0, bar_y1 = BAR_MARGIN_Y, BAR_MARGIN_Y + BAR_H

overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(overlay)

bar_fill = (10, 10, 18, 217)        # rgba(10,10,18,0.85)
bar_border = (255, 45, 150, 140)   # rgba(255,45,150,0.55)
od.rounded_rectangle([bar_x0, bar_y0, bar_x1, bar_y1], radius=14, fill=bar_fill)

# border with glow: draw a blurred magenta rounded rect behind the bar
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.rounded_rectangle([bar_x0 - 2, bar_y0 - 2, bar_x1 + 2, bar_y1 + 2], radius=15,
                     outline=(255, 45, 150, 130), width=2)
glow = glow.filter(ImageFilter.GaussianBlur(6))
img = Image.alpha_composite(img, glow)
img.paste(overlay.crop((0, 0, W, bar_y1 + 2)), (0, 0), overlay.crop((0, 0, W, bar_y1 + 2)))

d = ImageDraw.Draw(img)
# re-draw crisp border on top
d.rounded_rectangle([bar_x0, bar_y0, bar_x1, bar_y1], radius=14,
                    outline=(255, 45, 150, 200), width=2)

cy = (bar_y0 + bar_y1) // 2
f_bar = font(JBM_BOLD, 14)

def text_center(y, s, f, fill):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=fill)

def vcenter(x, s, f, fill):
    bbox = f.getbbox(s)
    d.text((x, cy - (bbox[3] - bbox[1]) / 2 - bbox[1]), s, font=f, fill=fill)

# left: logo
lx = bar_x0 + 12
vcenter(lx, "TOM OS", f_bar, (255, 45, 150, 255))
lx += d.textlength("TOM OS", font=f_bar) + 16

# workspaces chip
ws_x0 = lx
ws_width = 5 * 30 + 10
od2 = ImageDraw.Draw(img)
od2.rounded_rectangle([ws_x0, bar_y0 + 5, ws_x0 + ws_width, bar_y1 - 5], radius=10,
                      fill=(20, 20, 31, 160))
for i in range(1, 6):
    cx = ws_x0 + 5 + (i - 1) * 30 + 15
    if i == 1:  # active: magenta->purple gradient chip
        chip = Image.new("RGBA", (26, 24), (0, 0, 0, 0))
        cd = ImageDraw.Draw(chip)
        for x in range(26):
            t = x / 25
            col = (int(255 + (199 - 255) * t), int(45 + (76 - 45) * t),
                   int(150 + (255 - 150) * t), 255)
            cd.line([(x, 0), (x, 24)], fill=col)
        mask = Image.new("L", (26, 24), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 25, 23], radius=8, fill=255)
        img.paste(chip, (int(cx - 13), int(bar_y0 + 6)), mask)
        d.text((cx, cy), str(i), font=f_bar, fill=(10, 10, 18, 255), anchor="mm")
    else:
        d.text((cx, cy), str(i), font=f_bar, fill=(138, 138, 160, 255), anchor="mm")
lx = ws_x0 + ws_width + 14

# window title
vcenter(lx, "tom@tomos: ~", font(JBM, 13), (176, 176, 200, 255))

# center: clock
text_center(bar_y0, "  08:15  06/11", f_bar, (0, 240, 255, 255))

# right side modules
f_r = font(JBM, 13)
mods = [
    ("  85%", (0, 240, 255, 255)),
    ("  TOMNET-5G (86%) 5.8GHz", (0, 229, 255, 255)),
    ("  12%", (255, 225, 77, 255)),
    ("  47%", (192, 76, 255, 255)),
    ("  98%", (0, 255, 156, 255)),
]
rx = bar_x1 - 14
tray = "......"
d.text((rx, cy), tray, font=f_r, fill=(138, 138, 160, 255), anchor="rm")
rx -= d.textlength(tray, font=f_r) + 18
for label, col in reversed(mods):
    d.text((rx, cy), label, font=f_r, fill=col, anchor="rm")
    rx -= d.textlength(label, font=f_r) + 14

# ---------------- kitty terminal ----------------
TW, TH = 900, 470
tx, ty = (W - TW) // 2, int(H * 0.30)
# soft glow behind window
win_glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(win_glow).rounded_rectangle(
    [tx - 4, ty - 4, tx + TW + 4, ty + TH + 4], radius=16, fill=(0, 229, 255, 60))
win_glow = win_glow.filter(ImageFilter.GaussianBlur(18))
img = Image.alpha_composite(img, win_glow)

# window body: #0a0a12 at 88% opacity
win = Image.new("RGBA", (TW, TH), (10, 10, 18, 224))
win_mask = Image.new("L", (TW, TH), 0)
ImageDraw.Draw(win_mask).rounded_rectangle([0, 0, TW - 1, TH - 1], radius=14, fill=255)
img.paste(win, (tx, ty), win_mask)
d = ImageDraw.Draw(img)
d.rounded_rectangle([tx, ty, tx + TW, ty + TH], radius=14,
                    outline=(0, 229, 255, 120), width=2)

# terminal content
pad = 22
line_h = 26
f_term = font(JBM, 17)
f_tip = font(JBM, 15)
y = ty + pad

def tline(x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill)

# banner — TOM OS in block letters drawn as pixel cells (like terminal art)
LETTERS = {
    "T": ["█████", "  █  ", "  █  ", "  █  ", "  █  "],
    "O": [" ███ ", "█   █", "█   █", "█   █", " ███ "],
    "M": ["█   █", "██ ██", "█ █ █", "█   █", "█   █"],
    "S": [" ████", "█    ", " ███ ", "    █", "████ "],
}

def draw_block_text(x, y, word, cell, col):
    cx = x
    for ch in word:
        rows = LETTERS[ch]
        for r, row in enumerate(rows):
            for c, v in enumerate(row):
                if v == "█":
                    d.rectangle([cx + c * cell, y + r * cell,
                                 cx + (c + 1) * cell - 1, y + (r + 1) * cell - 1], fill=col)
        cx += 6 * cell + cell  # 5-wide + gap
    return cx

banner_cell = 9
banner_y = y
draw_block_text(tx + pad, banner_y, "TOM", banner_cell, (255, 45, 150, 255))
draw_block_text(tx + pad + d.textlength("TOM   ", font=f_term) * 0 + (6 * banner_cell + banner_cell) * 3 + 14,
                banner_y, "OS", banner_cell, (0, 229, 255, 255))
y = banner_y + 5 * banner_cell + 16
tline(tx + pad, y, "welcome to TOM OS", font(JBM_XB, 18), (255, 95, 210, 255))
tline(tx + pad + d.textlength("welcome to TOM OS", font=font(JBM_XB, 18)) + 10, y,
      "// neon punk edition", f_term, (102, 242, 255, 255))
y += line_h + 8

# tip line
gray = (138, 138, 160, 255)
pink = (199, 76, 255, 255)
tip_f = f_tip
tline(tx + pad, y, "tip:", tip_f, gray)
x = tx + pad + d.textlength("tip:", font=tip_f) + 8
for seg, col in [("SUPER+ENTER", pink), (" kitty ", gray), ("|", gray), (" SUPER+D", pink),
                 (" apps ", gray), ("|", gray), (" SUPER+W", pink), (" WordCraft", gray)]:
    tline(x, y, seg, tip_f, col)
    x += d.textlength(seg, font=tip_f)
y += line_h + 16

# prompt lines
tline(tx + pad, y, "tom@tomos:~$ fastfetch", f_term, (232, 232, 240, 255))
y += line_h
tline(tx + pad, y, "  OS      Tom OS 26.10 (neon punk edition)", f_term, (176, 176, 200, 255))
y += line_h
tline(tx + pad, y, "  Kernel  7.2.6-070206-generic", f_term, (0, 255, 156, 255))
y += line_h
tline(tx + pad, y, "  WM      Hyprland 0.53.3 (Wayland)", f_term, (0, 229, 255, 255))
y += line_h
tline(tx + pad, y, "  Shell   kitty + bash  |  DM TDM  |  CPU 2%", f_term, (255, 225, 77, 255))
y += line_h + 10
# blinking prompt
d.ellipse([tx + pad, y + 6, tx + pad + 9, y + 15], fill=(0, 240, 255, 255))

img.convert("RGB").save(ROOT + "/desktop-preview.png", quality=95)
print("wrote", ROOT + "/desktop-preview.png")
