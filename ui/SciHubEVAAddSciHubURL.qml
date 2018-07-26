import QtQuick 2.11
import QtQuick.Layouts 1.4
import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.4
import QtQuick.Window 2.4

Window {
    title: qsTr("Add Sci-Hub URL")
    modality: Qt.ApplicationModal

    property int margin: 10

    width: columnLayoutAddSciHubURL.implicitWidth + 2 * margin
    height: columnLayoutAddSciHubURL.implicitHeight + 2 * margin
    minimumWidth: columnLayoutAddSciHubURL.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutAddSciHubURL.Layout.minimumHeight + 2 * margin

    signal addSciHubURL(string url)

    function showWindowAddSciHubURL() {
        show()
    }

    function showMessage(title, text, icon, standardButtons) {
        messageDialogAddSciHubURL.setTitle(title)
        messageDialogAddSciHubURL.setText(text)
        messageDialogAddSciHubURL.setIcon(icon)
        messageDialogAddSciHubURL.setStandardButtons(standardButtons)

        messageDialogAddSciHubURL.open()
    }

    function showInfoMessage(title, text) {
        showMessage(title, text, StandardIcon.Information, StandardButton.Ok)
    }

    function showErrorMessage(title, text) {
        showMessage(title, text, StandardIcon.Critical, StandardButton.Ok)
    }

    MessageDialog {
        id: messageDialogAddSciHubURL
        visible: false
        icon: StandardIcon.Information
        standardButtons: StandardButton.Ok
    }

    ColumnLayout {
        id: columnLayoutAddSciHubURL
        anchors.fill: parent
        anchors.margins: margin

        RowLayout {
            id: rowLayoutAddSciHubURLText
            Layout.fillWidth: true

            Label {
                id: labelAddSciHubURL
                text: qsTr("Sci-Hub URL: ")
            }

            TextField {
                id: textFieldAddSciHubURL
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
                    if (textFieldAddSciHubURL.text.trim() === '') {
                        showErrorMessage(qsTr("Error"), qsTr("Please input a new Sci-Hub URL!"))
                    } else {
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
    }
}
