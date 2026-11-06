// ████ Tom OS — Quickshell neon bar ████
import Quickshell
import Quickshell.Io
import Quickshell.Wayland
import Quickshell.Hyprland
import Quickshell.Services.Pipewire
import Quickshell.Services.UPower
import Quickshell.Services.SystemTray
import Quickshell.Widgets
import QtQuick
import QtQuick.Layouts

PanelWindow {
    id: bar

    // ---------- neon punk palette (matches waybar + kitty) ----------
    readonly property color bg:       Qt.rgba(10 / 255, 10 / 255, 18 / 255, 0.85)
    readonly property color surface:  Qt.rgba(20 / 255, 20 / 255, 31 / 255, 0.75)
    readonly property color fg:       "#e8e8f0"
    readonly property color muted:    "#8a8aa0"
    readonly property color magenta:  "#ff2d96"
    readonly property color purple:   "#c74cff"
    readonly property color cyan:     "#00f0ff"
    readonly property color yellow:   "#ffe14d"
    readonly property color blue:     "#5c7cff"
    readonly property color green:    "#00ff9c"
    readonly property color red:      "#ff2d78"
    readonly property string fontFamily: "JetBrainsMono Nerd Font"

    anchors {
        top: true
        left: true
        right: true
    }
    margins {
        top: 8
        left: 12
        right: 12
    }
    implicitHeight: 38
    color: "transparent"
    WlrLayershell.namespace: "tomos-bar"

    // ---------- live data ----------
    SystemClock {
        id: clock
        precision: SystemClock.Minutes
    }

    PwObjectTracker {
        objects: [Pipewire.defaultAudioSink]
    }
    readonly property var sink: Pipewire.defaultAudioSink

    // network: nmcli summary — "wifi|SSID|SIGNAL", "eth|IFNAME" or "off"
    property string netKind: "off"
    property string netName: ""
    property int netSignal: 0

    Process {
        id: netProc
        command: ["sh", "-c",
            "w=$(nmcli -t -f ACTIVE,SIGNAL,SSID dev wifi 2>/dev/null | grep '^yes:' | head -1); " +
            "if [ -n \"$w\" ]; then s=${w#yes:}; echo \"wifi|${s#*:}|${s%%:*}\"; " +
            "else e=$(nmcli -t -f TYPE,STATE,DEVICE dev 2>/dev/null | grep '^ethernet:connected' | head -1); " +
            "if [ -n \"$e\" ]; then echo \"eth|${e##*:}\"; else echo off; fi; fi"]
        stdout: StdioCollector {
            onStreamFinished: {
                const p = this.text.trim().split("|");
                bar.netKind = p[0] || "off";
                bar.netName = p[1] || "";
                bar.netSignal = parseInt(p[2] || "0");
            }
        }
    }

    // cpu + memory from /proc
    property real cpuPct: 0
    property real memPct: 0
    property var lastCpu: null

    Process {
        id: sysProc
        command: ["sh", "-c", "head -1 /proc/stat; grep -E '^(MemTotal|MemAvailable):' /proc/meminfo"]
        stdout: StdioCollector {
            onStreamFinished: {
                const lines = this.text.trim().split("\n");
                const f = lines[0].trim().split(/\s+/).slice(1).map(Number);
                const idle = f[3] + (f[4] || 0);
                const total = f.reduce((a, b) => a + b, 0);
                if (bar.lastCpu) {
                    const dt = total - bar.lastCpu.total;
                    const di = idle - bar.lastCpu.idle;
                    if (dt > 0) bar.cpuPct = Math.round(100 * (1 - di / dt));
                }
                bar.lastCpu = { total: total, idle: idle };
                const memTotal = parseInt(lines[1].split(/\s+/)[1]);
                const memAvail = parseInt(lines[2].split(/\s+/)[1]);
                if (memTotal > 0) bar.memPct = Math.round(100 * (1 - memAvail / memTotal));
            }
        }
    }

    Timer {
        interval: 3000
        running: true
        repeat: true
        triggeredOnStart: true
        onTriggered: {
            netProc.running = true;
            sysProc.running = true;
        }
    }

    // ---------- helpers ----------
    function wifiIcon(sig) {
        if (sig >= 75) return "󰤨";
        if (sig >= 50) return "󰤥";
        if (sig >= 25) return "󰤢";
        return "󰤟";
    }

    readonly property var battery: UPower.displayDevice
    readonly property int batteryPct: battery
        ? Math.round(battery.percentage > 1 ? battery.percentage : battery.percentage * 100)
        : 0

    component Chip: Text {
        font.family: bar.fontFamily
        font.pixelSize: 13
        color: bar.fg
        verticalAlignment: Text.AlignVCenter
    }

    // ---------- the bar itself ----------
    // neon frame: pink -> purple -> cyan gradient border (same as kitty / TDM)
    Rectangle {
        anchors.fill: parent
        radius: 13
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0.0; color: bar.magenta }
            GradientStop { position: 0.5; color: bar.purple }
            GradientStop { position: 1.0; color: bar.cyan }
        }
    }

    Rectangle {
        anchors.fill: parent
        anchors.margins: 1.5
        radius: 12
        color: Qt.rgba(10 / 255, 10 / 255, 18 / 255, 0.94)

        // left: logo + workspaces + window title
        RowLayout {
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            spacing: 8

            // Tom OS brand: round logo + lightning bolt + name (matches the TDM login screen)
            Rectangle {
                implicitWidth: brandRow.implicitWidth + 16
                implicitHeight: 26
                radius: 9
                color: Qt.rgba(1, 45 / 255, 150 / 255, 0.12)
                border.width: 1
                border.color: Qt.rgba(1, 45 / 255, 150 / 255, 0.55)

                RowLayout {
                    id: brandRow
                    anchors.centerIn: parent
                    spacing: 6

                    Image {
                        source: "file:///usr/share/tdm/logo.png"
                        sourceSize.width: 20
                        sourceSize.height: 20
                        Layout.preferredWidth: 20
                        Layout.preferredHeight: 20
                        smooth: true
                    }
                    Chip { text: "\uf0e7"; color: bar.yellow }
                    Chip {
                        text: "TOM OS"
                        font.bold: true
                        font.letterSpacing: 2
                        color: bar.magenta
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Quickshell.execDetached(["sh", "-c", "rofi -show drun || wofi --show drun"])
                }
            }

            Repeater {
                model: Hyprland.workspaces

                delegate: Rectangle {
                    required property HyprlandWorkspace modelData
                    visible: modelData.id > 0
                    implicitWidth: modelData.focused ? 32 : 24
                    implicitHeight: 22
                    radius: 7
                    color: modelData.focused ? bar.magenta
                         : modelData.urgent ? Qt.rgba(1, 45 / 255, 120 / 255, 0.35)
                         : bar.surface
                    border.width: modelData.focused ? 0 : 1
                    border.color: Qt.rgba(199 / 255, 76 / 255, 1, 0.35)

                    Behavior on implicitWidth { NumberAnimation { duration: 160; easing.type: Easing.OutCubic } }

                    Chip {
                        anchors.centerIn: parent
                        text: parent.modelData.name
                        font.bold: parent.modelData.focused
                        color: parent.modelData.focused ? "#0a0a12" : bar.muted
                    }

                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        onClicked: parent.modelData.activate()
                    }
                }
            }

            Chip {
                Layout.maximumWidth: 320
                Layout.leftMargin: 6
                elide: Text.ElideRight
                color: bar.muted
                text: ToplevelManager.activeToplevel ? ToplevelManager.activeToplevel.title : ""
            }
        }

        // centre: clock
        Row {
            anchors.centerIn: parent
            spacing: 10
            Chip {
                color: bar.cyan
                font.bold: true
                font.pixelSize: 14
                text: "\uf017  " + Qt.formatDateTime(clock.date, "HH:mm")
            }
            Chip { color: bar.muted; text: "//" }
            Chip {
                color: bar.purple
                text: Qt.formatDateTime(clock.date, "ddd dd MMM")
            }
        }

        // right: audio, network, cpu, memory, battery, tray
        RowLayout {
            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.verticalCenter: parent.verticalCenter
            spacing: 14

            Chip {
                color: bar.purple
                text: !bar.sink || !bar.sink.audio ? "󰝟 --"
                    : bar.sink.audio.muted ? "󰝟 muted"
                    : " " + Math.round(bar.sink.audio.volume * 100) + "%"
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    acceptedButtons: Qt.LeftButton | Qt.RightButton
                    onClicked: mouse => {
                        if (mouse.button === Qt.RightButton && bar.sink && bar.sink.audio)
                            bar.sink.audio.muted = !bar.sink.audio.muted;
                        else
                            Quickshell.execDetached(["pavucontrol"]);
                    }
                    onWheel: wheel => {
                        if (!bar.sink || !bar.sink.audio) return;
                        const step = wheel.angleDelta.y > 0 ? 0.05 : -0.05;
                        bar.sink.audio.volume = Math.max(0, Math.min(1, bar.sink.audio.volume + step));
                    }
                }
            }

            // network: neon signal-bar badge (pink -> cyan bars, lit by strength)
            Rectangle {
                id: netPill
                readonly property bool off: bar.netKind === "off"
                readonly property bool wifi: bar.netKind === "wifi"
                readonly property var thresholds: [1, 30, 55, 80]
                readonly property var barColors: [bar.magenta, bar.purple, "#5ab8ff", bar.cyan]
                implicitHeight: 24
                implicitWidth: netRow.implicitWidth + 16
                radius: 8
                color: off ? Qt.rgba(1, 45 / 255, 120 / 255, 0.10) : Qt.rgba(0, 240 / 255, 1, 0.07)
                border.width: 1
                border.color: off ? Qt.rgba(1, 45 / 255, 120 / 255, 0.65) : Qt.rgba(0, 240 / 255, 1, 0.55)

                RowLayout {
                    id: netRow
                    anchors.centerIn: parent
                    spacing: 7

                    Item {
                        implicitWidth: 18
                        implicitHeight: 14
                        Layout.alignment: Qt.AlignVCenter

                        Repeater {
                            model: 4
                            delegate: Rectangle {
                                required property int index
                                readonly property bool lit: bar.netKind === "eth"
                                    || (netPill.wifi && bar.netSignal >= netPill.thresholds[index])
                                x: index * 5
                                width: 3
                                height: 5 + index * 3
                                y: 14 - height
                                radius: 1.5
                                color: lit ? netPill.barColors[index] : Qt.rgba(1, 1, 1, 0.13)
                                Behavior on color { ColorAnimation { duration: 250 } }
                            }
                        }

                        // offline: pulsing pink slash across the bars
                        Rectangle {
                            visible: netPill.off
                            anchors.centerIn: parent
                            width: 22
                            height: 2
                            radius: 1
                            rotation: -35
                            color: bar.magenta
                            SequentialAnimation on opacity {
                                running: netPill.off
                                loops: Animation.Infinite
                                NumberAnimation { from: 1.0; to: 0.35; duration: 900; easing.type: Easing.InOutSine }
                                NumberAnimation { from: 0.35; to: 1.0; duration: 900; easing.type: Easing.InOutSine }
                            }
                        }
                    }

                    Chip {
                        Layout.maximumWidth: 140
                        elide: Text.ElideRight
                        font.bold: true
                        font.pixelSize: 12
                        color: netPill.off ? bar.magenta : bar.cyan
                        text: netPill.wifi ? bar.netName
                            : bar.netKind === "eth" ? "wired"
                            : "offline"
                    }

                    Chip {
                        visible: netPill.wifi
                        font.pixelSize: 11
                        color: bar.purple
                        text: bar.netSignal + "%"
                    }
                }

                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Quickshell.execDetached(["nm-connection-editor"])
                }
            }

            Chip {
                color: bar.yellow
                text: " " + bar.cpuPct + "%"
            }

            Chip {
                color: bar.blue
                text: "󰍛 " + bar.memPct + "%"
            }

            Chip {
                visible: bar.battery && bar.battery.isLaptopBattery
                color: bar.batteryPct <= 15 ? bar.red : bar.green
                text: (UPower.onBattery ? "󰁹 " : "󰂄 ") + bar.batteryPct + "%"
            }

            Repeater {
                model: SystemTray.items

                delegate: IconImage {
                    id: trayIcon
                    required property SystemTrayItem modelData
                    implicitSize: 16
                    source: modelData.icon

                    MouseArea {
                        anchors.fill: parent
                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        onClicked: mouse => {
                            if (mouse.button === Qt.RightButton && trayIcon.modelData.hasMenu)
                                trayIcon.modelData.display(bar, trayIcon.mapToItem(null, 0, 0).x, bar.implicitHeight);
                            else
                                trayIcon.modelData.activate();
                        }
                    }
                }
            }

            // power button -> neon power menu
            Rectangle {
                id: powerBtn
                implicitWidth: 28
                implicitHeight: 24
                radius: 8
                color: powerMenu.visible ? bar.magenta : Qt.rgba(1, 45 / 255, 150 / 255, 0.15)
                border.width: 1
                border.color: bar.magenta
                Chip {
                    anchors.centerIn: parent
                    text: "\u23fb"
                    font.pixelSize: 14
                    color: powerMenu.visible ? "#0a0a12" : bar.magenta
                }
                MouseArea {
                    anchors.fill: parent
                    cursorShape: Qt.PointingHandCursor
                    onClicked: powerMenu.visible = !powerMenu.visible
                }
            }
        }
    }

    PopupWindow {
        id: powerMenu
        visible: false
        anchor.item: powerBtn
        anchor.rect.x: powerBtn.width - implicitWidth
        anchor.rect.y: powerBtn.height + 12
        implicitWidth: 190
        implicitHeight: menuCol.implicitHeight + 20
        color: "transparent"

        Rectangle {
            anchors.fill: parent
            radius: 12
            gradient: Gradient {
                GradientStop { position: 0.0; color: bar.magenta }
                GradientStop { position: 1.0; color: bar.cyan }
            }
            Rectangle {
                anchors.fill: parent
                anchors.margins: 1.5
                radius: 11
                color: "#14141f"

                Column {
                    id: menuCol
                    anchors.fill: parent
                    anchors.margins: 9
                    spacing: 4

                    Repeater {
                        model: [
                            { icon: "\uf023", label: "Lock",      cmd: "hyprlock",              tint: "#00f0ff" },
                            { icon: "\uf186", label: "Suspend",   cmd: "systemctl suspend",     tint: "#c74cff" },
                            { icon: "\uf2f1", label: "Restart",   cmd: "systemctl reboot",      tint: "#ffe14d" },
                            { icon: "\u23fb", label: "Shut down", cmd: "systemctl poweroff",    tint: "#ff2d96" },
                            { icon: "\uf08b", label: "Log out",   cmd: "hyprctl dispatch exit", tint: "#8a8aa0" }
                        ]
                        delegate: Rectangle {
                            id: item
                            required property var modelData
                            width: menuCol.width
                            height: 30
                            radius: 8
                            color: hover.containsMouse ? Qt.rgba(1, 45 / 255, 150 / 255, 0.18) : "transparent"
                            Row {
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.left: parent.left
                                anchors.leftMargin: 10
                                spacing: 10
                                Chip { width: 16; text: item.modelData.icon; color: item.modelData.tint }
                                Chip { text: item.modelData.label }
                            }
                            MouseArea {
                                id: hover
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    powerMenu.visible = false;
                                    Quickshell.execDetached(["sh", "-c", item.modelData.cmd]);
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
