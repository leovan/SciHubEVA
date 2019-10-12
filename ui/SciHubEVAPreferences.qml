import QtQuick 2.12
import QtQuick.Layouts 1.12
import QtQuick.Controls 2.12
import QtQuick.Window 2.12

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
    signal saveOverwriteExistingFile(bool overwrite)
    signal saveThemeCurrentIndex(int themeCurrentIndex)

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
        saveFilenamePrefixFormat(textFieldPreferencesFilenamePrefixFormat.text.trim())
        saveOverwriteExistingFile(switchOverwrite.checked)
        saveThemeCurrentIndex(comboBoxPreferencesTheme.currentIndex)

        saveNetworkSciHubURLCurrentIndex(comboBoxPreferencesNetworkSciHubURL.currentIndex)
        saveNetworkTimeout(textFieldPreferencesNetworkTimeout.text)

        saveProxyEnabled(checkBoxPreferencesProxyEnabled.checked)

        if (radioButtonPreferencesProxyTypeHTTP.checked) {
            saveProxyType('http')
        } else if (radioButtonPreferencesProxyTypeSocks5.checked) {
            saveProxyType('socks5')
        }

        saveProxyHost(textFieldPreferencesProxyHost.text.trim())
        saveProxyPort(textFieldPreferencesProxyPort.text.trim())
        saveProxyUsername(textFieldPreferencesProxyUsername.text.trim())
        saveProxyPassword(textFieldPreferencesProxyPassword.text.trim())

        if (comboBoxPreferencesTheme.currentIndex != themeCurrentIndex) {
            dialogChangeThemeRestartMessage.setIcon("\uf17d")
            dialogChangeThemeRestartMessage.setText(qsTr("A restart is required for the theme to take effect."))
            dialogChangeThemeRestartMessage.open()
        } else {
            close()
        }
    }

    function setFilenamePrefixFormat(filenameFormat) {
        textFieldPreferencesFilenamePrefixFormat.text = filenameFormat
    }

    function setOverwriteExistingFile(overwrite) {
        switchOverwrite.checked = overwrite
    }

    function setThemeModel(model) {
        comboBoxPreferencesTheme.model = model
    }

    function setThemeCurrentIndex(currentIndex) {
        themeCurrentIndex = currentIndex
        comboBoxPreferencesTheme.currentIndex = currentIndex
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
        checkBoxPreferencesProxyEnabled.checked = proxyEnabled
    }

    function setProxyType(proxyType) {
        if (proxyType === "http") {
            radioButtonPreferencesProxyTypeHTTP.checked = true
        } else if (proxyType === "socks5") {
            radioButtonPreferencesProxyTypeSocks5.checked = true
        }
    }

    function setProxyHost(proxyHost) {
        textFieldPreferencesProxyHost.text = proxyHost
    }

    function setProxyPort(proxyPort) {
        textFieldPreferencesProxyPort.text = proxyPort
    }

    function setProxyUsername(proxyUsername) {
        textFieldPreferencesProxyUsername.text = proxyUsername
    }

    function setProxyPassword(proxyPassword) {
        textFieldPreferencesProxyPassword.text = proxyPassword
    }

    FontLoader {
        id: fontMDI
        source: "qrc:/fonts/materialdesignicons-webfont.ttf"
    }

    Ui.SciHubEVAAddSciHubURL {
        id: windowAddSciHubURL
    }

    Ui.SciHubEVAMessage {
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

    Ui.SciHubEVAMessage {
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

        GroupBox {
            id: groupBoxPreferencesCommon
            title: qsTr("Common")

            Layout.fillWidth: true

            GridLayout {
                id: gridLayoutPreferencesFile

                rows: 4
                columns: 2
                anchors.fill: parent

                Label {
                    id: labelPreferencesFilenamePrefixFormat
                    text: qsTr("Filename Prefix Format: ")
                }

                TextField {
                    id: textFieldPreferencesFilenamePrefixFormat

                    implicitWidth: 200
                    Layout.fillWidth: true

                    placeholderText: "{author}_{year}_{title}"
                    selectByMouse: true
                    validator: RegExpValidator {
                        regExp: /.*[(\{author\})|(\{year\})|(\{title\})]+.*/
                    }
                }

                Label {
                    id: labelPreferencesFilenameFormatSupportedKeywords
                    text: qsTr("Supported Keywords: ")
                }

                Label {
                    id: labelPreferencesFilenameFormatSupportedKeywordsExplain
                    text: qsTr("{author}: Author, {year}: Year, {title}: Title") +
                          "<br/>" +
                          qsTr("{id}: DOI or PMID (avaiable only when in such search type)")
                    wrapMode: Text.NoWrap
                }

                Label {
                    id: labelPreferencesTheme
                    text: qsTr("Theme: ")
                }

                ComboBox {
                    id: comboBoxPreferencesTheme

                    Layout.minimumWidth: 200
                    Layout.fillWidth: true
                }

                Label {
                    id: labelOverwrite
                    text: qsTr("Overwrite Existing File:")
                }

                RowLayout {
                    id: rowLayoutOverwrite

                    Label {
                        id: labelOverwriteNo
                        text: qsTr("No")
                    }

                    Switch {
                        id: switchOverwrite
                        display: AbstractButton.IconOnly
                    }

                    Label {
                        id: labelOverwriteYes
                        text: qsTr("Yes")
                    }
                }
            }
        }

        GroupBox {
            id: groupBoxPreferencesNetwork
            title: qsTr("Network")

            Layout.fillWidth: true

            ColumnLayout {
                id: columnLayoutPreferencesNetwork

                anchors.fill: parent

                RowLayout {
                    id: rowLayoutPreferencesNetworkSciHubURL

                    Layout.fillWidth: true

                    Label {
                        id: labelPreferencesNetworkSciHubURL
                        text: qsTr("SciHub URL: ")
                    }

                    ComboBox {
                        id: comboBoxPreferencesNetworkSciHubURL

                        Layout.minimumWidth: 200
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

                RowLayout {
                    id: rowLayoutPreferencesNetworkTimeoutAndRetryTimes

                    Layout.fillWidth: true

                    Label {
                        id: labelPreferencesNetworkTimeout
                        text: qsTr("Timeout: ")
                    }

                    TextField {
                        id: textFieldPreferencesNetworkTimeout

                        implicitWidth: 60
                        Layout.fillWidth: true

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

                    ToolSeparator {
                        id: toolSeparatorPreferencesNetworkTimeoutAndRetryTimes
                    }

                    Label {
                        id: labelPreferencesNetworkRetryTimes
                        text: qsTr("Retry Times: ")
                    }

                    TextField {
                        id: textFieldPreferencesNetworkRetryTimes

                        implicitWidth: 60
                        Layout.fillWidth: true

                        horizontalAlignment: Text.AlignHCenter
                        selectByMouse: true
                        validator: RegExpValidator {
                            regExp: /[0-9]+/
                        }
                    }
                }
            }
        }

        GroupBox {
            id: groupBoxPreferencesProxy
            title: qsTr("Proxy")

            Layout.fillHeight: false
            Layout.fillWidth: true

            ColumnLayout {
                id: columnLayoutPreferencesProxy

                anchors.fill: parent

                RowLayout {
                    id: rowLayoutPreferencesProxyEnabledAndType

                    Layout.fillWidth: true

                    CheckBox {
                        id: checkBoxPreferencesProxyEnabled
                        text: qsTr("Enable Proxy")
                    }

                    ToolSeparator {
                        id: toolSeparatorPreferencesProxyEnabledAndType
                    }

                    Label {
                        id: labelPreferencesProxyType
                        text: qsTr("Proxy Type: ")
                    }

                    RadioButton {
                        id: radioButtonPreferencesProxyTypeSocks5
                        text: "SOCKS5"
                    }

                    RadioButton {
                        id: radioButtonPreferencesProxyTypeHTTP
                        text: "HTTP"
                    }
                }

                GridLayout {
                    id: gridLayoutPreferencesProxy

                    columns: 2

                    Label {
                        id: labelPreferencesProxyHost
                        text: qsTr("Proxy Host: ")
                    }

                    TextField {
                        id: textFieldPreferencesProxyHost

                        implicitWidth: 200
                        Layout.fillWidth: true

                        selectByMouse: true
                    }

                    Label {
                        id: labelPreferencesProxyPort
                        text: qsTr("Proxy Port: ")
                    }

                    TextField {
                        id: textFieldPreferencesProxyPort

                        implicitWidth: 200
                        Layout.fillWidth: true

                        selectByMouse: true
                        validator: RegExpValidator {
                            regExp: /[0-9]+/
                        }
                    }

                    Label {
                        id: labelPreferencesProxyUsername
                        text: qsTr("Proxy Username: ")
                    }

                    TextField {
                        id: textFieldPreferencesProxyUsername

                        implicitWidth: 200
                        Layout.fillWidth: true

                        selectByMouse: true
                    }

                    Label {
                        id: labelPreferencesProxyPassword
                        text: qsTr("Proxy Password: ")
                    }

                    TextField {
                        id: textFieldPreferencesProxyPassword

                        implicitWidth: 200
                        Layout.fillWidth: true

                        echoMode: TextInput.Password
                    }
                }
            }
        }

        RowLayout {
            id: rowLayoutPreferencesButtons

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
