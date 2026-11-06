# Welcome to Tom OS

*A lightweight, Ubuntu-based live operating system with a neon-punk soul — built for Tom. Runs from any USB stick (or Ventoy drive) on x86-64 PCs.*

## 01 · A modern foundation

- **Ubuntu 26.04 LTS core** — the resolute release — a huge software catalogue and full Ubuntu repository access.
- **Linux kernel 7.2.6** — the newest mainline-stable kernel with ready-built Ubuntu packages, with matching headers for building drivers or modules.
- **Firmware to date** — Ubuntu's full firmware stack plus the upstream linux-firmware 20261019 drop — newest Wi-Fi, GPU and Bluetooth blobs included.
- **Live and installable** — boots straight from USB with zero install, or installs to disk in a few clicks.

## 02 · The desktop

- **TDM login screen** — the TomOS Display Manager — a neon, Tom OS-branded graphical login with your logo, a “Welcome to Tom OS” greeting, user and session pickers, Caps Lock warning and Suspend / Restart / Shut down buttons.
- **Hyprland 0.53.3** — a modern, fast, animated Wayland tiling window manager — eye candy without the bloat.
- **kitty terminal** — GPU-accelerated with a custom neon palette, powerline tabs and 10,000 lines of scrollback.
- **Quickshell neon bar** — the default top bar — TOM OS logo chip, pink workspace pill, cyan clock, live volume / CPU / memory, a redesigned neon network badge (Wi-Fi bars, “wired”, “offline”) and a one-click power menu.
- **Waybar as a backup** — prefer the classic bar? `SUPER+SHIFT+B` swaps between Quickshell and Waybar, and Tom OS remembers your choice.
- **wofi + mako** — an app launcher and pop-up notifications, both themed to match.
- **hyprlock + hypridle** — neon lock screen and idle suspend, so your session stays yours.

## 03 · The look

- **Neon punk everywhere** — custom TomOS theme for both GTK 3 and GTK 4 apps, dark mode with magenta accents system-wide.
- **Two 4K wallpapers** — the Neon Eclipse design (default) and a synthwave city with your logo. Quickshell draws the wallpaper so it works on any GPU, even in VMs — put a different picture path in `~/.config/tomos/wallpaper` to change it.
- **Your branding** — the TOM OS logo on the TDM login screen, the top bar, the terminal, wallpapers, app launcher and installer.
- **JetBrains Mono Nerd Font** — crisp terminal typography with icons and glyphs built in.
- **welcome to TOM OS** — every new kitty window opens with fastfetch, a “welcome to TOM OS” line and a quick shortcuts tip.

## 04 · The apps

- **WordCraft 0.11.0** — an open-source, Word-style editor that handles .docx, Markdown and PDF — `SUPER+W`.
- **Zoiper 5 free** — a full SIP softphone for calls and VoIP accounts — `SUPER+Z`.
- **Files, web, text** — Nautilus file manager, GNOME Web browser and GNOME Text Editor, all GTK-themed.
- **Sound done right** — PipeWire audio with a PulseAudio compatibility layer and pavucontrol mixing.
- **fastfetch** — runs automatically in kitty with a neon ring-T Tom OS logo, showing your kernel, login manager, bar, CPU, GPU, memory and display.

## 05 · Live USB superpowers

- **Calamares installer** — a friendly graphical installer — launch "Install Tom OS" from the app launcher (`SUPER+D`). It writes to the disk you choose, so double-check your target.
- **Persistence** — add a persistence partition to your USB stick and your files and settings survive reboots.
- **Ventoy friendly** — a standard hybrid ISO built for Ventoy, Rufus, dd or Etcher — BIOS and UEFI (Secure Boot off).
- **Nothing to risk** — the live session runs from the USB stick — nothing is written to your disk unless you launch the installer.

## 06 · First five minutes

1. Boot the USB — the TDM login screen says “Welcome to Tom OS”. Sign in as `tom` / `live`.
2. Press `SUPER+ENTER` for a terminal, `SUPER+D` to launch apps.
3. Connect to Wi-Fi by clicking the neon network badge in the top bar.
4. Like it? Run "Install Tom OS" and make it permanent.
5. Keep the Keyboard Shortcuts card nearby — every keybind is on it.

*Tom OS 26.10 · neon punk edition — built with live-build, Hyprland, and a lot of magenta.*
