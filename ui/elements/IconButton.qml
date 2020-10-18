import QtQuick 2.14
import QtQuick.Controls 2.14
import QtQuick.Controls.Material 2.14

Button {
    id: button

    property string iconSource
    property real iconSize: labelText.font.pointSize * 1.6

    implicitWidth: leftPadding + rightPadding + rowContent.implicitWidth

    contentItem: Row {
        id: rowContent

        spacing: 6
        anchors.horizontalCenter: parent.horizontalCenter

        AnimatedImage {
            id: animatedImageIcon
            playing: true
            source: iconSource
            height: iconSize
            width: iconSize
            anchors.verticalCenter: parent.verticalCenter
        }

        Label {
            id: labelText
            text: parent.parent.text
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}
