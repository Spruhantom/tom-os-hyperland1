#!/usr/bin/env python3
"""Tom OS — Welcome document (all the perks)."""
import urllib.request
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, Image, PageBreak)
from reportlab.lib.styles import ParagraphStyle

ROOT = Path("/home/user/workspace/neonpunk-os")
FONT_DIR = ROOT / "build/config/includes.chroot/usr/share/fonts/truetype/jetbrains-mono-nerd"
OUT = ROOT / "TomOS-Welcome.pdf"

pdfmetrics.registerFont(TTFont("JBM", str(FONT_DIR / "JetBrainsMonoNerdFont-Regular.ttf")))
pdfmetrics.registerFont(TTFont("JBM-Bold", str(FONT_DIR / "JetBrainsMonoNerdFont-Bold.ttf")))
pdfmetrics.registerFont(TTFont("JBM-Med", str(FONT_DIR / "JetBrainsMonoNerdFont-Medium.ttf")))

inter_path = Path("/tmp/fonts/Inter.ttf")
try:
    if not inter_path.exists():
        urllib.request.urlretrieve(
            "https://github.com/google/fonts/raw/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf",
            inter_path)
    pdfmetrics.registerFont(TTFont("Inter", str(inter_path)))
    BODY_FONT = "Inter"
except Exception:
    BODY_FONT = "Helvetica"

BG      = HexColor("#12101C")
SURFACE = HexColor("#1A1826")
BORDER  = HexColor("#2E2B44")
TEXT    = HexColor("#E8E8F2")
MUTED   = HexColor("#9B97B5")
MAGENTA = HexColor("#FF5FD2")
CYAN    = HexColor("#2DE2E6")
GREEN   = HexColor("#00FF9C")

PAGE_W, PAGE_H = A4
M_L, M_R, M_T, M_B = 16*mm, 16*mm, 16*mm, 20*mm
CW = PAGE_W - M_L - M_R

sec_style = ParagraphStyle("sec", fontName="JBM-Bold", fontSize=11.5, leading=15,
                           textColor=HexColor("#12101C"), backColor=MAGENTA,
                           borderPadding=(3, 6, 3, 6))
item_style = ParagraphStyle("item", fontName=BODY_FONT, fontSize=10, leading=14.5,
                            textColor=TEXT)
title_style = ParagraphStyle("title", fontName="JBM-Bold", fontSize=26, leading=30,
                            textColor=TEXT)
sub_style = ParagraphStyle("sub", fontName=BODY_FONT, fontSize=10.5, leading=14,
                           textColor=MUTED)
note_style = ParagraphStyle("note", fontName=BODY_FONT, fontSize=8.5, leading=12,
                            textColor=MUTED)

def section(title):
    return Paragraph(title, sec_style)

def item(bold, rest):
    return Paragraph(
        f'<font name="JBM-Bold" color="#FF5FD2">{bold}</font>'
        f'<font color="#E8E8F2"> — {rest}</font>', item_style)

def build_table(items):
    t = Table([[it] for it in items], colWidths=[CW])
    style = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("LINEBELOW", (0, 0), (-1, -2), 0.5, BORDER),
    ]
    for r in range(len(items)):
        if r % 2 == 1:
            style.append(("BACKGROUND", (0, r), (-1, r), SURFACE))
    t.setStyle(TableStyle(style))
    return t

story = []

logo = Image(str(ROOT / "assets/logo-tomos-256.png"), width=34*mm, height=34*mm)
logo_chip = Table([[logo]], colWidths=[38*mm], rowHeights=[38*mm])
logo_chip.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), HexColor("#E8E8F2")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
header = Table([[logo_chip, Paragraph(
    "Welcome to Tom OS<br/><font size=10 color='#9B97B5'>everything you get — the neon punk edition</font>",
    title_style)]], colWidths=[41*mm, CW - 41*mm])
header.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
]))
story.append(header)
story.append(Spacer(1, 4*mm))
story.append(Paragraph("A lightweight, Ubuntu-based live operating system with a neon-punk soul — built for Tom. Runs from any USB stick (or Ventoy drive) on x86-64 PCs.", sub_style))
story.append(Spacer(1, 5*mm))

story.append(section("01 · A modern foundation"))
story.append(Spacer(1, 1.5*mm))
story.append(build_table([
    item("Ubuntu 26.04 LTS core", "the resolute release — a huge software catalogue and full Ubuntu repository access."),
    item("Linux kernel 7.2.6", "the newest mainline-stable kernel with ready-built Ubuntu packages, with matching headers for building drivers or modules."),
    item("Firmware to date", "Ubuntu's full firmware stack plus the upstream linux-firmware 20261019 drop — newest Wi-Fi, GPU and Bluetooth blobs included."),
    item("Live and installable", "boots straight from USB with zero install, or installs to disk in a few clicks."),
]))
story.append(Spacer(1, 4.5*mm))

story.append(section("02 · The desktop"))
story.append(Spacer(1, 1.5*mm))
story.append(build_table([
    item("TDM login screen", "the TomOS Display Manager — a neon, Tom OS-branded graphical login with your logo, a “Welcome to Tom OS” greeting, user and session pickers, Caps Lock warning and Suspend / Restart / Shut down buttons."),
    item("Hyprland 0.53.3", "a modern, fast, animated Wayland tiling window manager — eye candy without the bloat."),
    item("kitty terminal", "GPU-accelerated with a custom neon palette, powerline tabs and 10,000 lines of scrollback."),
    item("Quickshell neon bar", "the default top bar — TOM OS logo chip, pink workspace pill, cyan clock, live volume / CPU / memory, a redesigned neon network badge (Wi-Fi bars, “wired”, “offline”) and a one-click power menu."),
    item("Waybar as a backup", "prefer the classic bar? SUPER+SHIFT+B swaps between Quickshell and Waybar, and Tom OS remembers your choice."),
    item("wofi + mako", "an app launcher and pop-up notifications, both themed to match."),
    item("hyprlock + hypridle", "neon lock screen and idle suspend, so your session stays yours."),
]))
story.append(Spacer(1, 4.5*mm))

story.append(PageBreak())
story.append(section("03 · The look"))
story.append(Spacer(1, 1.5*mm))
story.append(build_table([
    item("Neon punk everywhere", "custom TomOS theme for both GTK 3 and GTK 4 apps, dark mode with magenta accents system-wide."),
    item("Two 4K wallpapers", "the Neon Eclipse design (default) and a synthwave city with your logo. Quickshell draws the wallpaper so it works on any GPU, even in VMs — put a different picture path in ~/.config/tomos/wallpaper to change it."),
    item("Your branding", "the TOM OS logo on the TDM login screen, the top bar, the terminal, wallpapers, app launcher and installer."),
    item("JetBrains Mono Nerd Font", "crisp terminal typography with icons and glyphs built in."),
    item("welcome to TOM OS", "every new kitty window opens with fastfetch, a “welcome to TOM OS” line and a quick shortcuts tip."),
]))
story.append(Spacer(1, 4.5*mm))

story.append(section("04 · The apps"))
story.append(Spacer(1, 1.5*mm))
story.append(build_table([
    item("Tom OS WordDocEdit", "the Tom OS word processor, a neon-themed edition of WordCraft 0.15.1 for .docx, .odt, .rtf, Markdown and PDF export — SUPER+W."),
    item("Zoiper 5 free", "a full SIP softphone for calls and VoIP accounts — SUPER+Z."),
    item("Files, web, text", "Nautilus file manager, GNOME Web browser and GNOME Text Editor, all GTK-themed."),
    item("Sound done right", "PipeWire audio with a PulseAudio compatibility layer and pavucontrol mixing."),
    item("fastfetch", "runs automatically in kitty with a neon ring-T Tom OS logo, showing your kernel, login manager, bar, CPU, GPU, memory and display."),
]))
story.append(Spacer(1, 4.5*mm))

story.append(section("05 · Live USB superpowers"))
story.append(Spacer(1, 1.5*mm))
story.append(build_table([
    item("Calamares installer", "a friendly graphical installer — launch “Install Tom OS” from the app launcher (SUPER+D). It writes to the disk you choose, so double-check your target."),
    item("Persistence", "add a persistence partition to your USB stick and your files and settings survive reboots."),
    item("Ventoy friendly", "a standard hybrid ISO built for Ventoy, Rufus, dd or Etcher — BIOS and UEFI (Secure Boot off)."),
    item("Nothing to risk", "the live session runs from the USB stick — nothing is written to your disk unless you launch the installer."),
]))
story.append(Spacer(1, 4.5*mm))

story.append(PageBreak())
story.append(section("06 · First five minutes"))
story.append(Spacer(1, 1.5*mm))
story.append(build_table([
    item("1", "boot the USB — the TDM login screen says “Welcome to Tom OS”. Sign in as tom / live."),
    item("2", "press SUPER+ENTER for a terminal, SUPER+D to launch apps."),
    item("3", "connect to Wi-Fi by clicking the neon network badge in the top bar."),
    item("4", "like it? Run “Install Tom OS” and make it permanent."),
    item("5", "keep the Keyboard Shortcuts card nearby — every keybind is on it."),
]))
story.append(Spacer(1, 5*mm))
shot = Image(str(ROOT / "final-iso-kitty-fastfetch.png"), width=CW, height=CW*800/1280)
story.append(shot)
story.append(Spacer(1, 1.5*mm))
story.append(Paragraph("The real Tom OS desktop: Quickshell neon bar on top, kitty with fastfetch below.", note_style))
story.append(Spacer(1, 3*mm))
story.append(Paragraph("Tom OS 26.10 · neon punk edition — built with live-build, Hyprland, and a lot of magenta.", note_style))

def paint_bg(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(BG)
    canvas_obj.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    canvas_obj.setStrokeColor(MAGENTA)
    canvas_obj.setLineWidth(2)
    canvas_obj.line(0, PAGE_H - 3*mm, PAGE_W, PAGE_H - 3*mm)
    canvas_obj.setStrokeColor(CYAN)
    canvas_obj.line(0, PAGE_H - 4.6*mm, PAGE_W, PAGE_H - 4.6*mm)
    canvas_obj.setFont("JBM-Med", 7.5)
    canvas_obj.setFillColor(MUTED)
    canvas_obj.drawString(M_L, 9*mm, "TOM OS 26.10 — welcome")
    canvas_obj.drawRightString(PAGE_W - M_R, 9*mm, "page %d" % doc.page)
    canvas_obj.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4,
                        leftMargin=M_L, rightMargin=M_R, topMargin=M_T, bottomMargin=M_B,
                        title="Welcome to Tom OS", author="Perplexity Computer")
doc.build(story, onFirstPage=paint_bg, onLaterPages=paint_bg)
print("wrote", OUT)
