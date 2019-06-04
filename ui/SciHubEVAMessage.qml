import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12

Dialog {
    x: (parent.width - width) / 2
    y: (parent.height - height) / 2

    closePolicy: Popup.NoAutoClose

    function setIcon(text) {
        labelMessageIcon.text = text
    }

    function setText(text) {
        labelMessageText.text = text
    }

    FontLoader {
        id: fontMDI
        source: "qrc:/fonts/materialdesignicons-webfont.ttf"
    }

    ColumnLayout {
        id: columnLayoutMessage

        anchors.fill: parent

        RowLayout {
            id: rowLayoutMessageText

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignLeft | Qt.AlignCenter

            spacing: 10

            Label {
                id: labelMessageIcon

                font.family: fontMDI.name
                font.pointSize: labelMessageText.font.pointSize * 3
            }

            Label {
                id: labelMessageText
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

                Layout.fillWidth: true
                Layout.minimumWidth: 200
                Layout.maximumWidth: 300

                textFormat: Text.RichText
                wrapMode: Text.WordWrap
            }
        }
    }
}
