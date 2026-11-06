#!/usr/bin/env python3
"""Tom OS — Keyboard Shortcuts reference card (neon-punk themed PDF)."""
import urllib.request
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, KeepTogether)
from reportlab.lib.styles import ParagraphStyle

ROOT = Path("/home/user/workspace/neonpunk-os")
FONT_DIR = ROOT / "build/config/includes.chroot/usr/share/fonts/truetype/jetbrains-mono-nerd"
OUT = ROOT / "TomOS-Keyboard-Shortcuts.pdf"

# ---------- fonts ----------
pdfmetrics.registerFont(TTFont("JBM", str(FONT_DIR / "JetBrainsMonoNerdFont-Regular.ttf")))
pdfmetrics.registerFont(TTFont("JBM-Bold", str(FONT_DIR / "JetBrainsMonoNerdFont-Bold.ttf")))
pdfmetrics.registerFont(TTFont("JBM-Med", str(FONT_DIR / "JetBrainsMonoNerdFont-Medium.ttf")))

inter_path = Path("/tmp/fonts/Inter.ttf")
inter_bold = Path("/tmp/fonts/Inter-Bold.ttf")
try:
    if not inter_path.exists():
        urllib.request.urlretrieve(
            "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
            inter_path)
    if not inter_bold.exists():
        urllib.request.urlretrieve(
            "https://github.com/google/fonts/raw/main/ofl/inter/Inter-Italic%5Bopsz%2Cwght%5D.ttf",
            inter_bold)
    pdfmetrics.registerFont(TTFont("Inter", str(inter_path)))
    pdfmetrics.registerFont(TTFont("Inter-Bold", str(inter_bold)))
    BODY_FONT, BODY_BOLD = "Inter", "Inter-Bold"
except Exception:
    BODY_FONT, BODY_BOLD = "Helvetica", "Helvetica-Bold"

# ---------- palette (Tom OS neon punk) ----------
BG        = HexColor("#12101C")   # page background
SURFACE   = HexColor("#1A1826")  # row surface
BORDER    = HexColor("#2E2B44")
TEXT      = HexColor("#E8E8F2")  # body text
MUTED     = HexColor("#9B97B5")
MAGENTA   = HexColor("#FF5FD2")  # accent 1
CYAN      = HexColor("#2DE2E6")  # accent 2
KEY_BG    = HexColor("#2DE2E6")
KEY_FG    = HexColor("#0B0A14")

PAGE_W, PAGE_H = A4
M_L, M_R, M_T, M_B = 16*mm, 16*mm, 16*mm, 20*mm

# ---------- styles ----------
key_style = ParagraphStyle("key", fontName="JBM-Bold", fontSize=9.5, leading=13,
                           textColor=KEY_FG, backColor=KEY_BG, borderPadding=(3, 4, 3, 4),
                           alignment=TA_LEFT)
act_style = ParagraphStyle("act", fontName=BODY_FONT, fontSize=10, leading=13.5,
                           textColor=TEXT)
sec_style = ParagraphStyle("sec", fontName="JBM-Bold", fontSize=11.5, leading=15,
                           textColor=HexColor("#12101C"), backColor=MAGENTA,
                           borderPadding=(3, 6, 3, 6))
title_style = ParagraphStyle("title", fontName="JBM-Bold", fontSize=26, leading=30,
                            textColor=TEXT)
sub_style = ParagraphStyle("sub", fontName=BODY_FONT, fontSize=10.5, leading=14,
                           textColor=MUTED)
note_style = ParagraphStyle("note", fontName=BODY_FONT, fontSize=8.5, leading=12,
                            textColor=MUTED)

def K(text):
    return Paragraph(text, key_style)

def A(text):
    return Paragraph(text, act_style)

def section(title):
    return Paragraph(title, sec_style)

# ---------- content ----------
rows = []          # list of (type, cells)
def add_section(title):
    rows.append(("section", [section(title), ""]))
def add(keys, action):
    rows.append(("row", [K(keys), A(action)]))

add_section("Applications")
add("SUPER + Enter", "kitty — terminal")
add("SUPER + W", "WordCraft — text editor / word processor")
add("SUPER + Z", "Zoiper 5 — SIP softphone")
add("SUPER + E", "Nautilus — file manager")
add("SUPER + B", "GNOME Web — browser")
add("SUPER + D", "wofi — application launcher")

add_section("Window management")
add("SUPER + Q", "Close the focused window")
add("SUPER + F", "Toggle floating / tiled")
add("SUPER + P", "Toggle pseudo-tiling")
add("SUPER + F11", "Fullscreen")
add("SUPER + Arrows", "Move focus between windows")

add_section("Workspaces")
add("SUPER + 1 … 5", "Switch to workspace 1–5")
add("SUPER + Shift + 1 … 5", "Move the focused window to workspace 1–5")

add_section("Screenshots")
add("Print", "Full-screen screenshot (saved to ~/Pictures)")
add("SUPER + Print", "Region screenshot (select with mouse)")

add_section("Media and hardware")
add("Volume keys", "Raise / lower / mute audio")
add("Play / Next / Prev", "Media playback control")
add("Brightness keys", "Backlight brightness up / down")

add_section("Session")
add("SUPER + L", "Lock the screen (hyprlock)")
add("SUPER + Shift + L", "Lock and suspend")
add("SUPER + Shift + E", "Log out of Hyprland")
add("SUPER + Shift + B", "Switch bar: Quickshell neon bar (default) ↔ Waybar — remembered after reboot")

add_section("Quickshell bar — mouse controls")
add("Click TOM OS chip", "Open the app launcher")
add("Click workspace number", "Jump to that workspace (the pink pill is the one you are on)")
add("Click volume", "Open the pavucontrol mixer")
add("Right-click / scroll volume", "Mute / unmute — scroll to change volume in 5% steps")
add("Click network badge", "Open network settings (Wi-Fi bars, “wired” or “offline”)")
add("Tray icon (L / R click)", "Activate the app / open its menu")
add("Click power button", "Power menu: Lock · Suspend · Restart · Shut down · Log out")

add_section("TDM — login screen")
add("Enter (user field)", "Jump to the password field")
add("Enter (password field)", "Sign in to the selected session")
add("Esc", "Cancel a sign-in that is in progress")
add("Eye icon", "Show / hide the password (Caps Lock warning appears automatically)")

add_section("kitty — terminal")
add("Ctrl + Shift + Enter", "New window (same directory)")
add("Ctrl + Shift + T", "New tab (same directory)")
add("Ctrl + Shift + K", "Close tab")
add("Ctrl + Shift + Left / Right", "Previous / next tab")
add("Ctrl + Shift + F2", "Edit the kitty config file")
add("Ctrl + Shift + C / V", "Copy / paste (kitty defaults)")
add("Auto-start", "fastfetch runs each time kitty opens — skip it with TOMOS_NO_FASTFETCH=1")

# build story
story = []

logo = Image(str(ROOT / "assets/logo-tomos-256.png"), width=20*mm, height=20*mm)
logo_chip = Table([[logo]], colWidths=[24*mm], rowHeights=[24*mm])
logo_chip.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#E8E8F2")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
header = Table([[logo_chip, Paragraph("TOM OS<br/><font size=10 color='#9B97B5' name='%s'>Keyboard shortcuts — Hyprland edition</font>" % BODY_FONT, title_style)]],
               colWidths=[27*mm, PAGE_W - M_L - M_R - 27*mm])
header.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
]))
story.append(header)
story.append(Spacer(1, 4*mm))
story.append(Paragraph("SUPER is the Windows / Cmd key. Everything here works out of the box on the live USB and the installed system.", sub_style))
story.append(Spacer(1, 5*mm))

# tables — one per section so each section header is a full-width band
key_w = 62*mm
act_w = PAGE_W - M_L - M_R - key_w
for i, (kind, cells) in enumerate(rows):
    if kind != "section":
        continue
    # collect rows until next section
    j = i + 1
    tbl_rows = [cells]
    while j < len(rows) and rows[j][0] == "row":
        tbl_rows.append(rows[j][1])
        j += 1
    t = Table(tbl_rows, colWidths=[key_w, act_w], repeatRows=1)
    style = [
        ("SPAN", (0, 0), (1, 0)),
        ("BACKGROUND", (0, 0), (-1, 0), MAGENTA),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (0, -1), 6),
        ("LINEBELOW", (0, 1), (-1, -1), 0.5, BORDER),
        ("LINEAFTER", (0, 1), (0, -1), 0.5, BORDER),
    ]
    for r in range(1, len(tbl_rows)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), SURFACE))
    t.setStyle(TableStyle(style))
    story.append(KeepTogether([t, Spacer(1, 4.5*mm)]))

story.append(Spacer(1, 2*mm))
story.append(Paragraph("Live USB login: user <font name='JBM-Bold' color='#FF5FD2'>tom</font>, password <font name='JBM-Bold' color='#FF5FD2'>live</font> — the TDM login screen greets you with “Welcome to Tom OS”.", note_style))
story.append(Paragraph("Full keybind reference: ~/.config/hypr/hyprland.conf and ~/.config/kitty/kitty.conf inside Tom OS.", note_style))

# ---------- background + footer ----------
def paint_bg(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(BG)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    # thin neon top rule
    canvas_obj.setStrokeColor(MAGENTA)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(0, PAGE_H - 3*mm, PAGE_W, PAGE_H - 3*mm)
    canvas_obj.setStrokeColor(CYAN)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(0, PAGE_H - 4.6*mm, PAGE_W, PAGE_H - 4.6*mm)
    # footer
    canvas_obj.setFont("JBM-Med", 7.5)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(M_L, 9*mm, "TOM OS 26.10 — neon punk GNU/Linux")
    canvas_obj.drawRightString(PAGE_W - M_R, 9*mm, "page %d" % doc.page)
    canvas_obj.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4,
                        leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
                        title="Tom OS Keyboard Shortcuts", author="Perplexity Computer")
doc.build(story, onFirstPage=paint_bg, onLaterPages=paint_bg)
print("wrote", OUT)
