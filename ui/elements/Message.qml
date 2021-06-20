import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window

Dialog {
    x: (parent.width - width) / 2
    y: (parent.height - height) / 2

    modal: true

    closePolicy: Popup.NoAutoClose

    property string message
    property string messageType

    ColumnLayout {
        anchors.fill: parent

        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignLeft

            spacing: 10

            Image {
                Layout.alignment: Qt.AlignLeft | Qt.AlignTop

                source: {
                    switch (messageType.toLowerCase()) {
                    case "question":
                        "qrc:/images/icons/help.svg"
                        break
                    case "warn":
                        "qrc:/images/icons/box_important.svg"
                        break
                    case "error":
                        "qrc:/images/icons/cancel.svg"
                        break
                    default:
                        "qrc:/images/icons/info.svg"
                        break
                    }
                }

                sourceSize.height: 56
                sourceSize.width: 56
            }

            Label {
                text: message

                Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter

                Layout.fillWidth: true
                Layout.minimumWidth: 200
                Layout.maximumWidth: 300

                textFormat: Text.RichText
                wrapMode: Text.WordWrap
            }
        }
    }
}
