import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import Qt.labs.settings 1.1
import Qt.labs.platform 1.1 as Platform

import "." as Ui

ApplicationWindow {
    id: applicationWindow
    title: "Sci-Hub EVA"

    visible: true

    property int margin: 10

    width: columnLayoutApplication.implicitWidth + 2 * margin
    height: columnLayoutApplication.implicitHeight + 2 * margin
    minimumWidth: columnLayoutApplication.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutApplication.Layout.minimumHeight + 2 * margin
    maximumWidth: columnLayoutApplication.Layout.maximumWidth + 2 * margin
    maximumHeight: columnLayoutApplication.Layout.maximumHeight + 2 * margin

    signal saveToDir(string directory)
    signal showWindowPreference()
    signal showWindowAddSciHubURL()

    signal rampage(string query)

    function beforeRampage() {
        buttonRampage.enabled = false
        buttonSaveToOpen.enabled = false
    }

    function afterRampage() {
        buttonRampage.enabled = true
        buttonSaveToOpen.enabled = true
    }

    function setSaveToDir(directory) {
        textFieldSaveToDir.text = directory
    }

    function appendLogs(log) {
        textAreaLogs.append("<style>a { color: " + Material.accent + "; }</style>" + log)
    }

    FontLoader {
        id: fontMDI
        source: "qrc:/fonts/materialdesignicons-webfont.ttf"
    }

    Ui.SciHubEVAPreferences {
        id: windowPreferences
    }

    Ui.SciHubEVAAbout {
        id: windowAbout
    }

    Ui.SciHubEVAMessage {
        id: dialogMessage

        modal: true

        footer: DialogButtonBox {
            Button {
                id: buttonDialogMessageOK
                text: qsTr("OK")

                onClicked: dialogMessage.close()
            }
        }
    }

    Platform.FolderDialog {
        id: folderDialogSaveTo

        options: Platform.FolderDialog.ShowDirsOnly

        onAccepted: {
            var folderURI = folderDialogSaveTo.folder.toString()

            switch (Qt.platform.os) {
            case "windows":
                folderURI = folderURI.replace(/^(file:\/{3})/, "")
                break
            default:
                folderURI = folderURI.replace(/^(file:\/{2})/, "")
                break
            }

            textFieldSaveToDir.text = folderURI
            applicationWindow.saveToDir(folderURI)
        }
    }

    background: Image {
        source: {
            switch(Material.theme) {
            case Material.Light:
                "qrc:/images/SciHubEVA-background-light.png"
                break
            case Material.Dark:
                "qrc:/images/SciHubEVA-background-dark.png"
                break
            default:
                ""
                break
            }
        }
    }

    ColumnLayout {
        id: columnLayoutApplication

        anchors.fill: parent
        anchors.margins: margin

        GridLayout {
            id: gridLayoutQuery

            Layout.fillHeight: true
            Layout.fillWidth: true

            rows: 2
            columns: 4

            Label {
                id: labelQuery
                text: qsTr("Query: ")

                Layout.minimumWidth: 60
            }

            TextField {
                id: textFieldQuery
                placeholderText: qsTr("URL, PMID / DOI or search string")

                implicitWidth: 300
                Layout.minimumWidth: 300
                Layout.fillWidth: true

                selectByMouse: true
            }

            Button {
                id: buttonRampage
                text: qsTr("RAMPAGE")

                Layout.minimumWidth: 100

                font.bold: false

                onClicked: {
                    if (textFieldSaveToDir.text.trim() === '') {
                        dialogMessage.setIcon("\uf5de")
                        dialogMessage.setText(qsTr("Please choose save to directory first!"))
                        dialogMessage.open()
                    } else if (textFieldQuery.text.trim() === '') {
                        dialogMessage.setIcon("\uf5de")
                        dialogMessage.setText(qsTr("Please specify query!"))
                        dialogMessage.open()
                    } else {
                        applicationWindow.rampage(textFieldQuery.text.trim())
                    }
                }
            }

            Button {
                id: buttonAbout
                text: "\uf2fc"

                font.family: fontMDI.name
                font.pointSize: buttonRampage.font.pointSize * 1.2

                onClicked: windowAbout.open()
            }

            Label {
                id: labelSaveTo
                text: qsTr("Save to: ")

                Layout.minimumWidth: 60
            }

            TextField {
                id: textFieldSaveToDir

                implicitWidth: 300
                Layout.minimumWidth: 300
                Layout.fillWidth: true

                readOnly: true
                selectByMouse: true
            }

            Button {
                id: buttonSaveToOpen
                text: qsTr("Open ...")

                Layout.minimumWidth: 100

                font.bold: false

                onClicked: folderDialogSaveTo.open()
            }

            Button {
                id: buttonPreferences
                text: "\uf493"

                font.family: fontMDI.name
                font.pointSize: buttonSaveToOpen.font.pointSize * 1.2

                onClicked: {
                    applicationWindow.showWindowPreference()
                }
            }
        }

        Label {
            id: labelLogs
            text: qsTr("Logs: ")
        }

        Flickable {
            id: flickableLogs

            flickableDirection: Flickable.VerticalFlick

            Layout.minimumWidth: 600
            Layout.minimumHeight: 200

            function scrollToBottom() {
                if (contentHeight > height) {
                    contentY = contentHeight - height
                }
            }

            TextArea.flickable: TextArea {
                id: textAreaLogs
                text: qsTr("Welcome to Sci-Hub EVA")

                font.pointSize: labelLogs.font.pointSize
                textFormat: Text.RichText
                wrapMode: Text.WordWrap
                readOnly: true
                selectByMouse: true

                onTextChanged: flickableLogs.scrollToBottom()
                onLinkActivated: Qt.openUrlExternally(link)
            }
        }
    }
}
