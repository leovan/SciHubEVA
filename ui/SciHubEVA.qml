import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import Qt.labs.settings
import Qt.labs.platform as Platform

import "." as UI
import "./elements" as UIElements

ApplicationWindow {
    id: applicationWindowSciHubEVA
    title: "Sci-Hub EVA"

    modality: Qt.ApplicationModal

    visible: true

    property int margin: 10
    property int theme: Material.theme

    width: columnLayoutApplication.implicitWidth + 2 * margin
    height: columnLayoutApplication.implicitHeight + 2 * margin
    minimumWidth: columnLayoutApplication.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutApplication.Layout.minimumHeight + 2 * margin
    maximumWidth: columnLayoutApplication.Layout.maximumWidth + 2 * margin
    maximumHeight: columnLayoutApplication.Layout.maximumHeight + 2 * margin

    signal openSaveToDir(string directory)
    signal systemOpenSaveToDir(string directory)
    signal showUIPreference()
    signal systemOpenLogFile()
    signal systemOpenLogDirectory()
    signal rampage(string query)

    function setSaveToDir(directory) {
        textFieldSaveToDir.text = directory
    }

    function appendLog(message) {
        var style = "<style>a { color: " + Material.accent + "; }</style>"
        textAreaLogs.append(style + message)
    }

    function beforeRampage() {
        buttonRampage.enabled = false
        buttonLoadInputQueryList.enabled = false
        buttonOpenSaveToDir.enabled = false
    }

    function afterRampage() {
        buttonRampage.enabled = true
        buttonLoadInputQueryList.enabled = true
        buttonOpenSaveToDir.enabled = true
    }

    UI.About {
        id: dialogAbout
    }

    UIElements.Message {
        id: dialogMessage

        footer: DialogButtonBox {
            Button {
                id: buttonDialogMessageOK
                text: qsTr("OK")

                onClicked: dialogMessage.close()
            }
        }
    }

    Platform.FileDialog {
        id: fileDialogQueryList

        onAccepted: {
            var queryListURI = fileDialogQueryList.file.toString()

            switch (Qt.platform.os) {
            case "windows":
                queryListURI = queryListURI.replace(/^(file:\/{3})/, "")
                break
            default:
                queryListURI = queryListURI.replace(/^(file:\/{2})/, "")
                break
            }

            textFieldQuery.text = queryListURI
        }
    }

    Platform.FolderDialog {
        id: folderDialogSaveTo

        options: Platform.FolderDialog.ShowDirsOnly

        onAccepted: {
            var saveToURI = folderDialogSaveTo.folder.toString()

            switch (Qt.platform.os) {
            case "windows":
                saveToURI = saveToURI.replace(/^(file:\/{3})/, "")
                break
            default:
                saveToURI = saveToURI.replace(/^(file:\/{2})/, "")
                break
            }

            textFieldSaveToDir.text = saveToURI
            openSaveToDir(saveToURI)
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

        focus: true

        GridLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true

            rows: 2
            columns: 5

            Label {
                text: qsTr("Query: ")

                Layout.minimumWidth: 60
            }

            TextField {
                id: textFieldQuery
                placeholderText: qsTr("URL, PMID, DOI, Title or Query List File")

                implicitWidth: 300
                Layout.minimumWidth: 300
                Layout.fillWidth: true

                selectByMouse: true
            }

            Button {
                id: buttonRampage
                text: qsTr("Rampage")

                font.bold: false
                Layout.minimumWidth: implicitWidth
                Layout.minimumHeight: buttonAbout.implicitHeight
                Layout.fillWidth: true

                onClicked: {
                    if (textFieldSaveToDir.text.trim() === "") {
                        dialogMessage.messageType = "error"
                        dialogMessage.message = qsTr("Please choose save to directory first!")
                        dialogMessage.open()
                    } else if (textFieldQuery.text.trim() === "") {
                        dialogMessage.messageType = "error"
                        dialogMessage.message = qsTr("Please specify query!")
                        dialogMessage.open()
                    } else {
                        rampage(textFieldQuery.text.trim())
                    }
                }
            }

            Button {
                id: buttonLoadInputQueryList
                text: qsTr("Load")

                font.bold: false
                Layout.minimumWidth: implicitWidth
                Layout.minimumHeight: buttonAbout.implicitHeight
                Layout.fillWidth: true

                onClicked: fileDialogQueryList.open()
            }

            UIElements.IconButton {
                id: buttonAbout
                iconSource: "qrc:/images/icons/info.svg"

                onClicked: dialogAbout.open()
            }

            Label {
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
                id: buttonOpenSaveToDir
                text: qsTr("Open")

                font.bold: false
                Layout.minimumWidth: implicitWidth
                Layout.minimumHeight: buttonPreferences.implicitHeight
                Layout.fillWidth: true

                onClicked: folderDialogSaveTo.open()
            }

            Button {
                id: buttonShowSaveToDir
                text: qsTr("Show")

                font.bold: false
                Layout.minimumWidth: implicitWidth
                Layout.minimumHeight: buttonPreferences.implicitHeight
                Layout.fillWidth: true

                onClicked: systemOpenSaveToDir(textFieldSaveToDir.text.trim())
            }

            UIElements.IconButton {
                id: buttonPreferences
                iconSource: "qrc:/images/icons/settings.svg"

                onClicked: {
                    showUIPreference()
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

            Layout.minimumHeight: 200
            Layout.fillWidth: true

            ScrollBar.vertical: UIElements.ScrollBar {
                id: scrollBarLogs
            }

            TextArea.flickable: TextArea {
                id: textAreaLogs

                textFormat: Text.RichText
                wrapMode: Text.WordWrap
                readOnly: true
                selectByMouse: true
                horizontalAlignment: Text.AlignLeft

                Layout.fillWidth: true

                onTextChanged: {
                    scrollBarLogs.position = 1.0 - scrollBarLogs.size
                }

                onLinkActivated: (link) => {
                    Qt.openUrlExternally(link)
                }

                MouseArea {
                    id: mouseAreaLogs

                    anchors.fill: parent

                    propagateComposedEvents: true
                    acceptedButtons: Qt.RightButton

                    onClicked: (mouse) => {
                        if (mouse.button === Qt.RightButton) {
                            menuLogs.open()
                        }
                    }

                    Platform.Menu {
                        id: menuLogs

                        Platform.MenuItem {
                            text: qsTr("Open Log File")
                            onTriggered: systemOpenLogFile()
                        }

                        Platform.MenuItem {
                            text: qsTr("Open Log Directory")
                            onTriggered: systemOpenLogDirectory()
                        }
                    }
                }
            }
        }

        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Enter || event.key === Qt.Key_Return) {
                buttonRampage.clicked()
            }
        }
    }
}
