import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Window

ApplicationWindow {
    title: qsTr("Add Sci-Hub URL")

    modality: Qt.ApplicationModal
    flags: Qt.Dialog

    property int margin: 10

    width: columnLayoutAddSciHubURL.implicitWidth + 2 * margin
    height: columnLayoutAddSciHubURL.implicitHeight + 2 * margin
    minimumWidth: columnLayoutAddSciHubURL.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutAddSciHubURL.Layout.minimumHeight + 2 * margin

    signal addSciHubURL(string url)

    function showUIAddSciHubURL() {
        textFieldAddSciHubURL.text = ""
        show()
    }

    ColumnLayout {
        id: columnLayoutAddSciHubURL

        anchors.fill: parent
        anchors.margins: margin

        focus: true

        RowLayout {
            Layout.fillWidth: true

            Label {
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

        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Enter || event.key === Qt.Key_Return) {
                buttonAddSciHubURLConfirm.clicked()
            } else if (event.key === Qt.Key_Escape) {
                buttonAddSciHubURLCancel.clicked()
            }
        }
    }
}
