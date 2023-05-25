import QtQuick
import QtQuick.Templates as T
import QtQuick.Controls.Material

T.ScrollBar {
    id: control

    implicitWidth: Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding)

    padding: control.interactive ? 1 : 2
    visible: control.policy !== T.ScrollBar.AlwaysOff
    minimumSize: orientation === Qt.Horizontal ? height / width : width / height

    contentItem: Rectangle {
        implicitWidth: control.interactive ? 9 : 4
        implicitHeight: control.interactive ? 9 : 4

        color: control.pressed ? control.Material.scrollBarPressedColor :
               control.interactive && control.hovered ? control.Material.scrollBarHoveredColor : control.Material.scrollBarColor
        opacity: 0.0
        radius: Material.ExtraSmallScale
    }

    background: Rectangle {
        implicitWidth: control.interactive ? 12 : 4
        implicitHeight: control.interactive ? 12 : 4
        color: "#0e000000"
        opacity: 0.0
        radius: Material.ExtraSmallScale
        visible: control.interactive
    }

    states: State {
        name: "active"
        when: control.policy === T.ScrollBar.AlwaysOn || (control.active && control.size < 1.0)
    }

    transitions: [
        Transition {
            to: "active"
            NumberAnimation { targets: [control.contentItem, control.background]; property: "opacity"; to: 1.0 }
        },
        Transition {
            from: "active"
            SequentialAnimation {
                PropertyAction{ targets: [control.contentItem, control.background]; property: "opacity"; value: 1.0 }
                PauseAnimation { duration: 2450 }
                NumberAnimation { targets: [control.contentItem, control.background]; property: "opacity"; to: 0.0 }
            }
        }
    ]
}
