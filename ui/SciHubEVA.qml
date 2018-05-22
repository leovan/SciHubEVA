import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2
import QtQuick.Controls 2.3
import QtQuick.Controls.Styles 1.4
import QtQuick.Controls.Material 2.3

import Qt.labs.settings 1.0
import Qt.labs.platform 1.0 as Plotform

import "." as Ui

ApplicationWindow {
    id: applicationWindow
    objectName: "applicationWindow"
    visible: true
    title: "Sci-Hub EVA"

    property int margin: 10

    width: columnLayoutMain.implicitWidth + 2 * margin
    height: columnLayoutMain.implicitHeight + 2 * margin
    minimumWidth: columnLayoutMain.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutMain.Layout.minimumHeight + 2 * margin

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

    function showMessage(title, text, icon, standardButtons) {
        messageDialogApplicationWindow.setTitle(title)
        messageDialogApplicationWindow.setText(text)
        messageDialogApplicationWindow.setIcon(icon)
        messageDialogApplicationWindow.setStandardButtons(standardButtons)

        messageDialogApplicationWindow.open()
    }

    function showInfoMessage(title, text) {
        showMessage(title, text, StandardIcon.Information, StandardButton.Ok)
    }

    function showErrorMessage(title, text) {
        showMessage(title, text, StandardIcon.Critical, StandardButton.Ok)
    }

    function setSaveToDir(directory) {
        textFieldSaveToDir.text = directory
    }

    function appendLogs(log) {
        textAreaLogs.append(log)
    }

    Ui.SciHubEVAMenuBar {
        id: menuBar
    }

    Ui.SciHubEVAPreferences {
        id: windowPreferences
    }

    Ui.SciHubEVAAbout {
        id: windowAbout
    }

    Plotform.FolderDialog {
        id: folderDialogSaveTo
        options: Plotform.FolderDialog.ShowDirsOnly

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

    MessageDialog {
        id: messageDialogApplicationWindow
        visible: false
        icon: StandardIcon.Information
        standardButtons: StandardButton.Ok
    }

    ColumnLayout {
        id: columnLayoutMain
        anchors.fill: parent
        anchors.margins: margin

        GridLayout {
            id: gridLayoutQuery
            Layout.fillHeight: true
            Layout.fillWidth: true
            rows: 2
            columns: 3

            Label {
                id: labelQuery
                text: qsTr("Query: ")
                Layout.minimumWidth: 60
            }

            TextField {
                id: textFieldQuery
                selectByMouse: true
                placeholderText: qsTr("URL / DOI / PMID")
                Layout.fillWidth: true
            }

            Button {
                id: buttonRampage
                text: qsTr("RAMPAGE")
                font.bold: false
                Layout.minimumWidth: 100

                onClicked: {
                    if (textFieldSaveToDir.text.trim() === '') {
                        showErrorMessage(qsTr("Error"), qsTr("Please choose save to directory first!"))
                    } else if (textFieldQuery.text.trim() === '') {
                        showErrorMessage(qsTr("Error"), qsTr("Please specify query!"))
                    } else {
                        applicationWindow.rampage(textFieldQuery.text.trim())
                    }
                }
            }

            Label {
                id: labelSaveTo
                text: qsTr("Save to: ")
                Layout.minimumWidth: 60
            }

            TextField {
                id: textFieldSaveToDir
                Layout.fillWidth: true
                readOnly: true
                selectByMouse: true
            }

            Button {
                id: buttonSaveToOpen
                text: qsTr("Open ...")
                font.bold: false
                Layout.minimumWidth: 100

                onClicked: folderDialogSaveTo.open()
            }
        }

        Label {
            id: labelLogs
            text: qsTr("Logs: ")
        }

        RowLayout {
            id: rowLayoutLogs

            Flickable {
                id: flickableLogs
                anchors.fill: parent
                Layout.minimumWidth: 600
                Layout.maximumWidth: 600
                Layout.preferredWidth: 600
                Layout.minimumHeight: 200
                Layout.maximumHeight: 200
                Layout.preferredHeight: 200

                function scrollToBottom() {
                    if (contentHeight > height) {
                        contentY = contentHeight - height
                    }
                }

                TextArea.flickable: TextArea {
                    id: textAreaLogs
                    text: qsTr("Welcome to Sci-Hub EVA")
                    font.pointSize: 12
                    padding: 6
                    textFormat: Text.RichText
                    wrapMode: Text.WordWrap
                    readOnly: true
                    selectByMouse: true

                    onTextChanged: flickableLogs.scrollToBottom()
                }
            }
        }
    }
}
