// ████ Tom OS — Quickshell wallpaper ████
// Draws the Tom OS wallpaper on the background layer of every screen.
// Works on any GPU (also software rendering in VMs). Change the picture by
// putting a path in ~/.config/tomos/wallpaper (e.g. wallpaper.png).
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import QtQuick

PanelWindow {
    id: wall
    required property var modelData
    screen: modelData

    anchors {
        top: true
        bottom: true
        left: true
        right: true
    }
    exclusionMode: ExclusionMode.Ignore
    WlrLayershell.layer: WlrLayer.Background
    WlrLayershell.namespace: "tomos-wallpaper"
    color: "#0a0a12"

    property string path: "/usr/share/backgrounds/tomos/wallpaper-eclipse.png"

    FileView {
        path: Quickshell.env("HOME") + "/.config/tomos/wallpaper"
        watchChanges: true
        onFileChanged: reload()
        onLoaded: {
            const p = text().trim();
            if (p.length > 0) wall.path = p.startsWith("/") ? p : "/usr/share/backgrounds/tomos/" + p;
        }
    }

    Image {
        anchors.fill: parent
        source: "file://" + wall.path
        fillMode: Image.PreserveAspectCrop
        asynchronous: true
        smooth: true
        sourceSize.width: wall.screen ? wall.screen.width : 1920
        sourceSize.height: wall.screen ? wall.screen.height : 1080
    }
}
