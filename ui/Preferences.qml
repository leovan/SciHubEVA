import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14

import "." as Ui

ApplicationWindow {
    id: preferencesWindow
    title: qsTr("Preferences")

    modality: Qt.ApplicationModal

    property int margin: 10

    width: columnLayoutPreferences.implicitWidth + 2 * margin
    height: columnLayoutPreferences.implicitHeight + 2 * margin
    minimumWidth: columnLayoutPreferences.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutPreferences.Layout.minimumHeight + 2 * margin

    signal showWindowAddSciHubURL()
    signal removeSciHubURL(int networkSciHubURLCurrentIndex)

    signal saveFilenamePrefixFormat(string filenamePrefixFormat)
    signal saveThemeCurrentIndex(int themeCurrentIndex)
    signal saveOverwriteExistingFile(bool overwrite)

    signal saveNetworkSciHubURLCurrentIndex(int networkSciHubURLCurrentIndex)
    signal saveNetworkTimeout(int networkTimeout)
    signal saveNetworkRetryTimes(int networkRetryTimes)

    signal saveProxyEnabled(bool proxyEnabled)
    signal saveProxyType(string proxyType)
    signal saveProxyHost(string proxyHost)
    signal saveProxyPort(int proxyPort)
    signal saveProxyUsername(string proxyUsername)
    signal saveProxyPassword(string proxyPassword)

    property int themeCurrentIndex

    function showWindowPreferences() {
        show()
    }

    function saveAllPreference() {
        saveFilenamePrefixFormat(textFieldPreferencesCommonFilenamePrefixFormat.text.trim())
        saveThemeCurrentIndex(comboBoxPreferencesCommonTheme.currentIndex)
        saveOverwriteExistingFile(switchCommonOverwrite.checked)

        saveNetworkSciHubURLCurrentIndex(comboBoxPreferencesNetworkSciHubURL.currentIndex)
        saveNetworkTimeout(textFieldPreferencesNetworkTimeout.text)

        saveProxyEnabled(switchPreferencesNetworkEnableProxy.checked)

        if (radioButtonPreferencesNetworkProxyTypeHTTP.checked) {
            saveProxyType('http')
        } else if (radioButtonPreferencesNetworkProxyTypeSocks5.checked) {
            saveProxyType('socks5')
        }

        saveProxyHost(textFieldPreferencesNetworkProxyHost.text.trim())
        saveProxyPort(textFieldPreferencesNetworkProxyPort.text.trim())
        saveProxyUsername(textFieldPreferencesNetworkProxyUsername.text.trim())
        saveProxyPassword(textFieldPreferencesNetworkProxyPassword.text.trim())

        if (comboBoxPreferencesCommonTheme.currentIndex != themeCurrentIndex) {
            dialogChangeThemeRestartMessage.setIcon("\uf17d")
            dialogChangeThemeRestartMessage.setText(qsTr("A restart is required for the theme to take effect."))
            dialogChangeThemeRestartMessage.open()
        } else {
            close()
        }
    }

    function setFilenamePrefixFormat(filenameFormat) {
        textFieldPreferencesCommonFilenamePrefixFormat.text = filenameFormat
    }

    function setThemeModel(model) {
        comboBoxPreferencesCommonTheme.model = model
    }

    function setThemeCurrentIndex(currentIndex) {
        themeCurrentIndex = currentIndex
        comboBoxPreferencesCommonTheme.currentIndex = currentIndex
    }

    function setOverwriteExistingFile(overwrite) {
        switchCommonOverwrite.checked = overwrite
    }

    function setNetworkSciHubURLModel(model) {
        comboBoxPreferencesNetworkSciHubURL.model = model
    }

    function setNetworkSciHubURLCurrentIndex(currentIndex) {
        comboBoxPreferencesNetworkSciHubURL.currentIndex = currentIndex
    }

    function setNetworkTimeout(networkTimeout) {
        textFieldPreferencesNetworkTimeout.text = networkTimeout
    }

    function setNetworkRetryTimes(networkRetryTimes) {
        textFieldPreferencesNetworkRetryTimes.text = networkRetryTimes
    }

    function setProxyEnabled(proxyEnabled) {
        switchPreferencesNetworkEnableProxy.checked = proxyEnabled
    }

    function setProxyType(proxyType) {
        if (proxyType === "http") {
            radioButtonPreferencesNetworkProxyTypeHTTP.checked = true
        } else if (proxyType === "socks5") {
            radioButtonPreferencesNetworkProxyTypeSocks5.checked = true
        }
    }

    function setProxyHost(proxyHost) {
        textFieldPreferencesNetworkProxyHost.text = proxyHost
    }

    function setProxyPort(proxyPort) {
        textFieldPreferencesNetworkProxyPort.text = proxyPort
    }

    function setProxyUsername(proxyUsername) {
        textFieldPreferencesNetworkProxyUsername.text = proxyUsername
    }

    function setProxyPassword(proxyPassword) {
        textFieldPreferencesNetworkProxyPassword.text = proxyPassword
    }

    FontLoader {
        id: fontMDI
        source: "qrc:/fonts/materialdesignicons-webfont.ttf"
    }

    Ui.AddSciHubURL {
        id: windowAddSciHubURL
    }

    Ui.Message {
        id: dialogChangeThemeRestartMessage

        modal: true

        footer: DialogButtonBox {
            Button {
                id: buttonDialogChangeThemeRestartMessageOK
                text: qsTr("OK")

                onClicked: {
                    dialogChangeThemeRestartMessage.close()
                    preferencesWindow.close()
                }
            }
        }
    }

    Ui.Message {
        id: dialogRemoveSciHubURLConfirmMessage

        modal: true

        footer: DialogButtonBox {
            Button {
                id: buttonDialogRemoveSciHubURLConfirmMessageYes
                text: qsTr("Yes")

                onClicked: {
                    removeSciHubURL(comboBoxPreferencesNetworkSciHubURL.currentIndex)
                    dialogRemoveSciHubURLConfirmMessage.close()
                }
            }

            Button {
                id: buttonDialogRemoveSciHubURLConfirmMessageNo
                text: qsTr("No")

                onClicked: dialogRemoveSciHubURLConfirmMessage.close()
            }
        }
    }

    ColumnLayout {
        id: columnLayoutPreferences

        anchors.fill: parent
        anchors.margins: margin

        focus: true

        RowLayout {
            id: rowLayoutPreferencesTabs

            spacing: 0

            Layout.fillHeight: true
            Layout.fillWidth: true

            ListModel {
                id: listModelPreferencesTabButtons

                ListElement {
                    name: qsTr("Common")
                    iconText: "\uf61b"
                }

                ListElement {
                    name: qsTr("Network")
                    iconText: "\uf003"
                }
            }

            Component {
                id: itemDelegatePreferencesTabButtons

                ItemDelegate {
                    width: parent.width
                    highlighted: ListView.isCurrentItem

                    RowLayout {
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        anchors.fill: parent
                        Layout.alignment: Qt.AlignCenter | Qt.AlignVCenter

                        Label {
                            text: iconText
                            font.family: fontMDI.name
                            font.bold: true
                            font.pixelSize: 1.2 * buttonDialogRemoveSciHubURLConfirmMessageYes.font.pixelSize

                            Layout.leftMargin: 6
                        }

                        Label {
                            text: name
                            font.bold: true

                            Layout.rightMargin: 6
                        }
                    }

                    onClicked: {
                        listViewPreferencesTabButtons.currentIndex = index
                        stackLayoutPreferencesTabs.currentIndex = index
                    }
                }
            }

            ListView {
                id: listViewPreferencesTabButtons

                Layout.minimumWidth: 100
                Layout.minimumHeight: 100
                Layout.fillHeight: true

                model: listModelPreferencesTabButtons
                delegate: itemDelegatePreferencesTabButtons
            }

            ToolSeparator {
                id: toolSeparatorPreferences

                bottomPadding: 0
                topPadding: 0

                Layout.fillHeight: true
            }

            StackLayout {
                id: stackLayoutPreferencesTabs

                currentIndex: 0

                Layout.minimumHeight: 380
                Layout.minimumWidth: 400
                Layout.fillHeight: true
                Layout.fillWidth: true

                Item {
                    id: itemTabPreferencesCommon

                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    GridLayout {
                        id: gridLayoutPreferencesCommon
                        columnSpacing: 3
                        rowSpacing: 0

                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.top: parent.top

                        rows: 4
                        columns: 2

                        Label {
                            id: labelPreferencesCommonFilenamePrefixFormat
                            text: qsTr("Filename Prefix Format: ")
                        }

                        TextField {
                            id: textFieldPreferencesCommonFilenamePrefixFormat

                            implicitWidth: 200
                            Layout.fillWidth: true

                            placeholderText: "{id}_{year}_{author}_{title}"
                            selectByMouse: true
                        }

                        Label {
                            id: labelPreferencesCommonFilenameFormatSupportedKeywords
                            text: qsTr("Supported Keywords: ")
                        }

                        Label {
                            id: labelPreferencesCommonFilenameFormatSupportedKeywordsExplain
                            text: qsTr("{author}: Author, {year}: Year") +
                                  "<br/>" +
                                  qsTr("{title}: Title, {id}: DOI or PMID")
                            wrapMode: Text.NoWrap
                        }

                        Label {
                            id: labelPreferencesCommonTheme
                            text: qsTr("Theme: ")
                        }

                        ComboBox {
                            id: comboBoxPreferencesCommonTheme

                            Layout.minimumWidth: 200
                            Layout.fillWidth: true
                        }

                        Label {
                            id: labelCommonOverwrite
                            text: qsTr("Overwrite Existing File:")
                        }

                        Switch {
                            id: switchCommonOverwrite
                            text: checked ? qsTr("Yes") : qsTr("No")
                            display: AbstractButton.TextBesideIcon
                        }
                    }
                }

                Item {
                    id: itemTabPreferencesNetwork

                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    GridLayout {
                        id: gridLayoutPreferencesNetwork
                        rowSpacing: 0
                        columnSpacing: 3

                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.top: parent.top

                        rows: 9
                        columns: 2

                        Label {
                            id: labelPreferencesNetworkSciHubURL
                            text: qsTr("SciHub URL: ")
                        }

                        RowLayout {
                            id: rowLayoutPreferencesNetworkSciHubURL

                            Layout.fillWidth: true

                            ComboBox {
                                id: comboBoxPreferencesNetworkSciHubURL

                                Layout.minimumWidth: 160
                                Layout.fillWidth: true
                            }

                            RoundButton {
                                id: roundButtonPreferencesNetworkSciHubURLAdd
                                text: "\uf415"

                                font.family: fontMDI.name

                                onClicked: {
                                    showWindowAddSciHubURL()
                                }
                            }

                            RoundButton {
                                id: roundButtonPreferencesNetworkSciHubURLRemove
                                text: "\uf374"

                                font.family: fontMDI.name

                                onClicked: {
                                    if (comboBoxPreferencesNetworkSciHubURL.count <= 1) {
                                        dialogChangeThemeRestartMessage.setIcon("\uf5de")
                                        dialogChangeThemeRestartMessage.setText(qsTr("Cannot remove the last Sci-Hub URL!"))
                                        dialogChangeThemeRestartMessage.open()
                                    } else {
                                        var text = qsTr("Delete Sci-Hub URL: ") + comboBoxPreferencesNetworkSciHubURL.currentText + " ?"
                                        dialogRemoveSciHubURLConfirmMessage.setIcon("\uf816")
                                        dialogRemoveSciHubURLConfirmMessage.setText(text)
                                        dialogRemoveSciHubURLConfirmMessage.open()
                                    }
                                }
                            }
                        }

                        Label {
                            id: labelPreferencesNetworkTimeout
                            text: qsTr("Timeout: ")
                        }

                        RowLayout {
                            id: rowLayoutPreferencesNetworkTimeout
                            width: 100
                            height: 100

                            TextField {
                                id: textFieldPreferencesNetworkTimeout

                                implicitWidth: 60
                                Layout.fillWidth: false

                                horizontalAlignment: Text.AlignHCenter
                                selectByMouse: true
                                validator: RegExpValidator {
                                    regExp: /[0-9]+/
                                }
                            }

                            Label {
                                id: labelPreferencesNetworkTimeoutUnits
                                text: "ms"
                            }
                        }

                        Label {
                            id: labelPreferencesNetworkRetryTimes
                            text: qsTr("Retry Times: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkRetryTimes

                            implicitWidth: 60
                            Layout.fillWidth: false

                            horizontalAlignment: Text.AlignHCenter
                            selectByMouse: true
                            validator: RegExpValidator {
                                regExp: /[0-9]+/
                            }
                        }

                        Label {
                            id: labelPreferencesNetworkEnableProxy
                            text: qsTr("Enable Proxy")
                        }

                        Switch {
                            id: switchPreferencesNetworkEnableProxy
                            text: checked ? qsTr("Yes") : qsTr("No")
                        }

                        Label {
                            id: labelPreferencesNetworkProxyType
                            text: qsTr("Proxy Type: ")
                        }

                        RowLayout {
                            id: rowLayoutPreferencesNetworkProxyType
                            width: 100
                            height: 100

                            RadioButton {
                                id: radioButtonPreferencesNetworkProxyTypeHTTP
                                text: "HTTP"
                            }

                            RadioButton {
                                id: radioButtonPreferencesNetworkProxyTypeSocks5
                                text: "SOCKS5"
                            }

                        }

                        Label {
                            id: labelPreferencesNetworkProxyHost
                            text: qsTr("Proxy Host: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkProxyHost

                            implicitWidth: 200
                            Layout.fillWidth: true

                            selectByMouse: true
                        }

                        Label {
                            id: labelPreferencesNetworkProxyPort
                            text: qsTr("Proxy Port: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkProxyPort

                            implicitWidth: 200
                            Layout.fillWidth: true

                            selectByMouse: true
                            validator: RegExpValidator {
                                regExp: /[0-9]+/
                            }
                        }

                        Label {
                            id: labelPreferencesNetworkProxyUsername
                            text: qsTr("Proxy Username: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkProxyUsername

                            implicitWidth: 200
                            Layout.fillWidth: true

                            selectByMouse: true
                        }

                        Label {
                            id: labelPreferencesNetworkProxyPassword
                            text: qsTr("Proxy Password: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkProxyPassword

                            implicitWidth: 200
                            Layout.fillWidth: true

                            echoMode: TextInput.Password
                        }
                    }
                }
            }
        }

        RowLayout {
            id: rowLayoutPreferencesButtons
            Layout.topMargin: 6
            Layout.fillHeight: true

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight | Qt.AlignTop

            Button {
                id: buttonPreferencesConfirm
                text: qsTr("Confirm")

                onClicked: saveAllPreference()
            }

            Button {
                id: buttonPreferencesCancel
                text: qsTr("Cancel")

                onClicked: close()
            }
        }

        Keys.onPressed: {
            if (event.key === Qt.Key_Enter || event.key === Qt.Key_Return) {
                buttonPreferencesConfirm.clicked()
            } else if (event.key === Qt.Key_Escape) {
                buttonPreferencesCancel.clicked()
            }
        }
    }
}


