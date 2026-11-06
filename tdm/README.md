# TomOS Display Manager (TDM) 0.1.0

The default login screen of **Tom OS**. TDM is a GTK4 greeter written in Rust
for [greetd](https://sr.ht/~kennylevinsen/greetd/). It runs fullscreen inside
the [cage](https://github.com/cage-kiosk/cage) Wayland kiosk compositor and
uses the Tom OS neon-punk branding (Neon Eclipse wallpaper, TOM OS logo,
pink `#ff2d96` / cyan `#00f0ff` / purple `#c74cff`, JetBrainsMono Nerd Font).

```
systemd ─► greetd.service (display-manager.service, VT 7)
             └─► cage -s -d -m last -- tdm-greeter   (user _greetd)
                    └─ greetd IPC ($GREETD_SOCK) ─► PAM ─► /usr/bin/tomos-session ─► Hyprland
```

## What changed in the 0.1.0 rewrite

| Area | 0.0.6 | 0.1.0 |
|---|---|---|
| Structure | everything in one `greeter.rs` | `tdm` library (`config`, `session`, `users`, `state`, `greetd`) + thin CLI and GUI binaries |
| Sign-in flow | type user → click → wait for prompt → type password → click | user picker + password on one form, Enter to sign in; extra PAM prompts (OTP, password change) appear inline |
| Look | generic dark panel | Tom OS neon theme over the system wallpaper, logo, clock/date, hostname; `dark`, `light`, `high-contrast` still available |
| Users | free-text only | picker from `/etc/passwd` (UID 1000–59999, login shell) plus "Other user…" |
| Memory | none | remembers last user + session in `/var/lib/tdm/state` (no secrets) |
| Sessions | passed `Exec` straight through | exports `XDG_SESSION_TYPE`, `XDG_SESSION_DESKTOP`, `XDG_CURRENT_DESKTOP`; Tom OS sessions listed first; X11 sessions wrapped in `startx` (hidden if xinit is missing) |
| Errors | raw PAM text | "Wrong username or password.", password cleared and refocused, greetd session cancelled cleanly |
| Extras | — | Caps Lock warning, Escape cancels, GTK4 `AlertDialog` power confirmations, polkit rule for power buttons |
| Tests | 11 | 27 (config, users, state, session parsing, full greetd conversations against a mock socket, theme CSS) |

Security properties kept from 0.0.6: session `Exec` lines are tokenised to argv
and never passed to a shell, unsupported `%` field codes are rejected, greetd
frames are length-checked (max 1 MiB), the password is only held for the
current attempt and cleared from the entry immediately.

## Files installed in Tom OS

| Path | Purpose |
|---|---|
| `/usr/bin/tdm-greeter` | the greeter |
| `/usr/bin/tdm` | CLI: `tdm list-sessions`, `tdm list-users`, `tdm config`, `tdm check` |
| `/usr/bin/tomos-dm` | switch login screen: `tomos-dm tdm` (default) / `tomos-dm ly` (fallback) |
| `/etc/greetd/config.toml` | runs `cage … tdm-greeter` as `_greetd` on VT 7 |
| `/etc/tdm/greeter.conf` | theme, background, logo, default session/user, power buttons, clock format |
| `/usr/lib/tmpfiles.d/tdm.conf` | creates `/var/lib/tdm` owned by `_greetd` |
| `/etc/polkit-1/rules.d/50-tdm-greeter.rules` | lets the greeter suspend / restart / shut down |
| `/usr/share/tdm/logo.png` | Tom OS logo |

## Configuration (`/etc/tdm/greeter.conf`)

```ini
theme = neon                 # neon | dark | light | high-contrast
title = TOM OS
subtitle = Welcome to Tom OS
background = /usr/share/backgrounds/tomos/wallpaper-eclipse.png
logo = /usr/share/tdm/logo.png
default_session = Tom OS (Hyprland)
# default_user = tom
remember = true
show_users = true
show_power = true
clock_format = %H:%M
date_format = %A %e %B
```

`TDM_THEME`, `TDM_CONFIG`, `TDM_STATE` and `TDM_WINDOWED=1` override these for testing.

## Build

```sh
sudo apt install cargo rustc pkg-config libgtk-4-dev   # Rust >= 1.83, GTK >= 4.12
cargo test --release
cargo build --release
sudo install -m755 target/release/{tdm,tdm-greeter} /usr/bin/
sudo install -Dm644 data/greetd-config.toml /etc/greetd/config.toml
sudo install -Dm644 data/greeter.conf /etc/tdm/greeter.conf
sudo install -Dm644 data/tdm.tmpfiles /usr/lib/tmpfiles.d/tdm.conf
sudo install -Dm644 data/50-tdm-greeter.rules /etc/polkit-1/rules.d/50-tdm-greeter.rules
sudo systemd-tmpfiles --create /usr/lib/tmpfiles.d/tdm.conf
sudo systemctl enable --force greetd.service
```

Runtime dependencies: `greetd`, `cage`, `libgtk-4-1`.

`examples/greetd_probe.rs` runs the exact login conversation the greeter uses
against a real greetd. It was used to check Tom OS end to end: correct password
starts the session as the user with `XDG_SESSION_TYPE=wayland`, wrong password
starts nothing.

## Recovering if the greeter fails

Press `Ctrl+Alt+F2`, log in on the text console and run `sudo tomos-dm ly`,
then reboot. `sudo tomos-dm tdm` switches back.

MIT licensed — rewrite of https://github.com/Spruhantom/Tomos-display-manager
