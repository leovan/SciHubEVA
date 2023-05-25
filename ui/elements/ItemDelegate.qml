import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.impl
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl
import QtQml.Models

ItemDelegate {
    id: control

    readonly property real iconSize: 20

    highlighted: ListView.isCurrentItem

    RowLayout {
        Layout.fillHeight: true
        Layout.fillWidth: true

        anchors.fill: parent
        Layout.alignment: Qt.AlignCenter | Qt.AlignVCenter

        Image {
            source: iconSource

            sourceSize.height: iconSize
            sourceSize.width: iconSize

            Layout.leftMargin: 8
        }

        Label {
            id: labelDelegateToolsItemText

            text: name
            font.weight: Font.Medium

            Layout.rightMargin: 8
            Layout.fillWidth: true
        }
    }

    background: Rectangle {
        implicitHeight: control.Material.delegateHeight
        color: control.highlighted ? control.Material.listHighlightColor : "transparent"
        radius: Material.ExtraSmallScale

        Ripple {
            width: parent.width
            height: parent.height

            clip: visible
            pressed: control.pressed
            anchor: control
            active: enabled && (control.down || control.visualFocus || control.hovered)
            color: control.Material.rippleColor
            clipRadius: Material.ExtraSmallScale
        }
    }
}
