import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

Button {
    id: button

    property string iconSource

    readonly property real iconSize: 22
    readonly property bool hasIcon: iconSource.toString().length > 0
    readonly property bool hasText: button.text.toString().length > 0
    readonly property bool hasOnlyIcon: hasIcon && !hasText

    topInset: 6
    bottomInset: 6
    verticalPadding: 14
    leftPadding: hasOnlyIcon ? 8 : hasIcon ? 16 : 24
    rightPadding: hasOnlyIcon ? 8 : 24

    implicitWidth: hasIcon ?
                   Math.min(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding) :
                   Math.max(implicitBackgroundWidth + leftInset + rightInset,
                            implicitContentWidth + leftPadding + rightPadding)
    implicitHeight: Math.max(implicitBackgroundHeight + topInset + bottomInset,
                             implicitContentHeight + topPadding + bottomPadding)

    contentItem: Row {
        id: rowContent

        spacing: 8
        anchors.horizontalCenter: parent.horizontalCenter

        AnimatedImage {
            id: animatedImageIcon
            playing: true
            source: iconSource
            height: iconSize
            width: hasIcon ? iconSize : 0
            anchors.verticalCenter: parent.verticalCenter
        }

        Label {
            id: labelText
            text: button.text
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}
