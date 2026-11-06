// ████ Tom OS — Quickshell shell (default desktop shell) ████
// Entry point: Tom OS wallpaper + neon bar on every connected screen.
// Switch between this and waybar with SUPER+SHIFT+B (tomos-bar toggle).
import Quickshell
import QtQuick

ShellRoot {
    Variants {
        model: Quickshell.screens
        Wallpaper {}
    }

    Variants {
        model: Quickshell.screens

        Bar {
            required property var modelData
            screen: modelData
        }
    }
}
