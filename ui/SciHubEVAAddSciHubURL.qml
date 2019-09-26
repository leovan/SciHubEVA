import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12

ApplicationWindow {
    title: qsTr("Add Sci-Hub URL")

    modality: Qt.ApplicationModal

    property int margin: 10

    width: columnLayoutAddSciHubURL.implicitWidth + 2 * margin
    height: columnLayoutAddSciHubURL.implicitHeight + 2 * margin
    minimumWidth: columnLayoutAddSciHubURL.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutAddSciHubURL.Layout.minimumHeight + 2 * margin

    signal addSciHubURL(string url)

    function showWindowAddSciHubURL() {
        textFieldAddSciHubURL.text = ""
        show()
    }

    ColumnLayout {
        id: columnLayoutAddSciHubURL

        anchors.fill: parent
        anchors.margins: margin

        focus: true

        RowLayout {
            id: rowLayoutAddSciHubURLText

            Layout.fillWidth: true

            Label {
                id: labelAddSciHubURL
                text: qsTr("Sci-Hub URL: ")
            }

            TextField {
                id: textFieldAddSciHubURL

                implicitWidth: 200
                Layout.minimumWidth: 200

                selectByMouse: true
            }
        }

        RowLayout {
            id: rowLayoutAddSciHubURLButtons

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter

            Button {
                id: buttonAddSciHubURLConfirm
                text: qsTr("Confirm")

                onClicked: {
                    if (textFieldAddSciHubURL.text.trim() != "") {
                        addSciHubURL(textFieldAddSciHubURL.text.trim())
                        close()
                    }
                }
            }

            Button {
                id: buttonAddSciHubURLCancel
                text: qsTr("Cancel")

                onClicked: close()
            }
        }

        Keys.onPressed: {
            if (event.key === Qt.Key_Enter || event.key === Qt.Key_Return) {
                buttonAddSciHubURLConfirm.clicked()
            } else if (event.key === Qt.Key_Escape) {
                buttonAddSciHubURLCancel.clicked()
            }
        }
    }
}
