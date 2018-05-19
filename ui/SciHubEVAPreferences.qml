import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2
import QtQuick.Controls 2.3
import QtQuick.Window 2.3

import "." as Ui

Window {
    title: qsTr("Preferences")
    modality: Qt.ApplicationModal

    property int margin: 10

    width: columnLayoutPreferences.implicitWidth + 2 * margin
    height: columnLayoutPreferences.implicitHeight + 2 * margin
    minimumWidth: columnLayoutPreferences.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutPreferences.Layout.minimumHeight + 2 * margin

    signal showWindowAddSciHubURL()
    signal removeSciHubURL(int networkPrimarySciHubURLCurrentIndex)

    signal saveFilenamePrefixFormat(string filenamePrefixFormat)

    signal saveNetworkPrimarySciHubURLCurrentIndex(int networkPrimarySciHubURLCurrentIndex)
    signal saveNetworkTimeout(int networkTimeout)
    signal saveNetworkRetryTimes(int networkRetryTimes)

    signal saveProxyEnabled(bool proxyEnabled)
    signal saveProxyType(string proxyType)
    signal saveProxyHost(string proxyHost)
    signal saveProxyPort(int proxyPort)
    signal saveProxyUsername(string proxyUsername)
    signal saveProxyPassword(string proxyPassword)

    function showWindowPreferences() {
        show()
    }

    function saveAllPreference() {
        saveFilenamePrefixFormat(textFieldPreferencesFilenamePrefixFormat.text.trim())

        saveNetworkPrimarySciHubURLCurrentIndex(comboBoxPreferencesNetworkPrimarySciHubURL.currentIndex)
        saveNetworkTimeout(textFieldPreferencesNetworkTimeout.text)

        saveProxyEnabled(checkBoxPreferencesProxyEnabled.checked)

        if (radioButtonPreferencesProxyTypeHTTP.checked) {
            saveProxyType('http')
        } else if (radioButtonPreferencesProxyTypeSocks.checked) {
            saveProxyType('socks')
        }

        saveProxyHost(textFieldPreferencesProxyHost.text.trim())
        saveProxyPort(textFieldPreferencesProxyPort.text.trim())
        saveProxyUsername(textFieldPreferencesProxyUsername.text.trim())
        saveProxyPassword(textFieldPreferencesProxyPassword.text.trim())

        close()
    }

    function setFilenamePrefixFormat(filenameFormat) {
        textFieldPreferencesFilenamePrefixFormat.text = filenameFormat
    }

    function setNetworkPrimarySciHubURLModel(model) {
        comboBoxPreferencesNetworkPrimarySciHubURL.model = model
    }

    function setNetworkPrimarySciHubURLCurrentIndex(currentIndex) {
        comboBoxPreferencesNetworkPrimarySciHubURL.currentIndex = currentIndex
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
        if (proxyType === 'http') {
            radioButtonPreferencesProxyTypeHTTP.checked = true
        } else if (proxyType === 'socks') {
            radioButtonPreferencesProxyTypeSocks.checked = true
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

    function showMessage(title, text, icon, standardButtons) {
        messageDialogPreferencesWindow.setTitle(title)
        messageDialogPreferencesWindow.setText(text)
        messageDialogPreferencesWindow.setIcon(icon)
        messageDialogPreferencesWindow.setStandardButtons(standardButtons)

        messageDialogPreferencesWindow.open()
    }

    function showInfoMessage(title, text) {
        showMessage(title, text, StandardIcon.Information, StandardButton.Ok)
    }

    function showErrorMessage(title, text) {
        showMessage(title, text, StandardIcon.Critical, StandardButton.Ok)
    }

    Ui.SciHubEVAAddSciHubURL {
        id: windowAddSciHubURL
    }

    MessageDialog {
        id: messageDialogPreferencesWindow
        visible: false
        icon: StandardIcon.Information
        standardButtons: StandardButton.Ok
    }

    MessageDialog {
        id: messageDialogPreferencesWindowRemoveSciHubURL
        visible: false
        title: qsTr("Confirm Delete")
        icon: StandardIcon.Question
        standardButtons: StandardButton.Yes | StandardButton.No

        onYes: {
            removeSciHubURL(comboBoxPreferencesNetworkPrimarySciHubURL.currentIndex)
        }
    }

    ColumnLayout {
        id: columnLayoutPreferences
        anchors.fill: parent
        anchors.margins: margin

        GroupBox {
            id: groupBoxPreferencesCommon
            Layout.fillWidth: true
            title: qsTr("Common")

            GridLayout {
                id: gridLayoutPreferencesFile
                rows: 2
                columns: 2
                anchors.fill: parent

                Label {
                    id: labelPreferencesFilenamePrefixFormat
                    text: qsTr("Filename Prefix Format: ")
                }

                TextField {
                    id: textFieldPreferencesFilenamePrefixFormat
                    placeholderText: "{author}_{year}_{title}"
                    validator: RegExpValidator {
                        regExp: /.*[(\{author\})|(\{year\})|(\{title\})]+.*/
                    }
                    Layout.fillWidth: true
                    selectByMouse: true
                }

                Label {
                    id: labelPreferencesFilenameFormatSupportedKeywords
                    text: qsTr("Supported Keywords: ")
                }

                Label {
                    id: labelPreferencesFilenameFormatSupportedKeywordsExplain
                    text: qsTr("{author}: Author, {year}: Year, {title}: Title")
                }
            }
        }

        GroupBox {
            id: groupBoxPreferencesNetwork
            Layout.fillWidth: true
            title: qsTr("Network")

            ColumnLayout {
                id: columnLayoutPreferencesNetwork
                anchors.fill: parent

                RowLayout {
                    id: rowLayoutPreferencesNetworkPrimarySciHubURL
                    Layout.fillWidth: true

                    Label {
                        id: labelPreferencesNetworkPrimarySciHubURL
                        text: qsTr("Primary SciHub URL: ")
                    }

                    ComboBox {
                        id: comboBoxPreferencesNetworkPrimarySciHubURL
                        Layout.minimumWidth: 200
                        Layout.fillWidth: true
                    }

                    RoundButton {
                        id: roundButtonPreferencesNetworkPrimarySciHubURLAdd
                        text: "+"

                        onClicked: {
                            showWindowAddSciHubURL()
                        }
                    }

                    RoundButton {
                        id: roundButtonPreferencesNetworkPrimarySciHubURLRemove
                        text: "-"

                        onClicked: {
                            var text = ""

                            if (comboBoxPreferencesNetworkPrimarySciHubURL.count <= 1) {
                                text = qsTr("Cannot remove the last Sci-Hub URL!")
                                var title = qsTr("Error")
                                showErrorMessage(title, text)
                            } else {
                                text = qsTr("Delete Sci-Hub URL: ") +
                                        comboBoxPreferencesNetworkPrimarySciHubURL.currentText + " ?"
                                messageDialogPreferencesWindowRemoveSciHubURL.setText(text)

                                messageDialogPreferencesWindowRemoveSciHubURL.open()
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
                        horizontalAlignment: Text.AlignHCenter
                        Layout.preferredWidth: 60
                        validator: RegExpValidator {
                            regExp: /[0-9]+/
                        }
                        selectByMouse: true
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
                        horizontalAlignment: Text.AlignHCenter
                        Layout.preferredWidth: 60
                        validator: RegExpValidator {
                            regExp: /[0-9]+/
                        }
                        selectByMouse: true
                    }
                }
            }
        }

        GroupBox {
            id: groupBoxPreferencesProxy
            Layout.fillHeight: false
            Layout.fillWidth: true
            title: qsTr("Proxy")

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
                        id: radioButtonPreferencesProxyTypeSocks
                        text: "Socks"
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
                        Layout.fillWidth: true
                        selectByMouse: true
                    }

                    Label {
                        id: labelPreferencesProxyPort
                        text: qsTr("Proxy Port: ")
                    }

                    TextField {
                        id: textFieldPreferencesProxyPort
                        Layout.fillWidth: true
                        validator: RegExpValidator {
                            regExp: /[0-9]+/
                        }
                        selectByMouse: true
                    }

                    Label {
                        id: labelPreferencesProxyUsername
                        text: qsTr("Proxy Username: ")
                    }

                    TextField {
                        id: textFieldPreferencesProxyUsername
                        Layout.fillWidth: true
                        selectByMouse: true
                    }

                    Label {
                        id: labelPreferencesProxyPassword
                        text: qsTr("Proxy Password: ")
                    }

                    TextField {
                        id: textFieldPreferencesProxyPassword
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
    }
}
