import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.impl
import QtQuick.Controls.Material
import QtQuick.Controls.Material.impl
import QtQml.Models
import QtQuick.Window

import "." as UI
import "./elements" as UIElements

Window {
    id: applicationWindowPreferences
    title: qsTr("Preferences")

    modality: Qt.ApplicationModal
    flags: Qt.Dialog

    property int margin: 10

    width: columnLayoutPreferences.implicitWidth + 2 * margin
    height: columnLayoutPreferences.implicitHeight + 2 * margin
    minimumWidth: columnLayoutPreferences.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutPreferences.Layout.minimumHeight + 2 * margin

    signal showUIAddSciHubURL()
    signal removeSciHubURL(int networkSciHubURLCurrentIndex)
    signal saveSystemLanguage(string language)
    signal saveSystemTheme(string theme)
    signal saveFileFilenamePrefixFormat(string filenamePrefixFormat)
    signal saveFileOverwriteExistingFile(bool overwrite)
    signal saveNetworkSciHubURLs(variant networkSciHubURLs)
    signal saveNetworkSciHubURL(string networkSciHubURL)
    signal saveNetworkTimeout(int networkTimeout)
    signal saveNetworkRetryTimes(int networkRetryTimes)
    signal saveNetworkProxyEnabled(bool proxyEnabled)
    signal saveNetworkProxyType(string proxyType)
    signal saveNetworkProxyHost(string proxyHost)
    signal saveNetworkProxyPort(string proxyPort)
    signal saveNetworkProxyUsername(string proxyUsername)
    signal saveNetworkProxyPassword(string proxyPassword)

    function saveAll() {
        saveSystemLanguage(comboBoxPreferencesSystemLanguage.currentValue)
        saveSystemTheme(comboBoxPreferencesSystemTheme.currentValue)

        saveFileFilenamePrefixFormat(textFieldPreferencesFileFilenamePrefixFormat.text.trim())
        saveFileOverwriteExistingFile(switchPreferencesFileOverwrite.checked)

        saveNetworkSciHubURLs(comboBoxPreferencesNetworkSciHubURL.model)
        saveNetworkSciHubURL(comboBoxPreferencesNetworkSciHubURL.currentText)
        saveNetworkTimeout(textFieldPreferencesNetworkTimeout.text)
        saveNetworkProxyEnabled(switchPreferencesNetworkEnableProxy.checked)

        if (radioButtonPreferencesNetworkProxyTypeHTTP.checked) {
            saveNetworkProxyType('http')
        } else if (radioButtonPreferencesNetworkProxyTypeSocks5.checked) {
            saveNetworkProxyType('socks5')
        }

        saveNetworkProxyHost(textFieldPreferencesNetworkProxyHost.text.trim())
        saveNetworkProxyPort(textFieldPreferencesNetworkProxyPort.text.trim())
        saveNetworkProxyUsername(textFieldPreferencesNetworkProxyUsername.text.trim())
        saveNetworkProxyPassword(textFieldPreferencesNetworkProxyPassword.text.trim())

        close()
    }

    function setSystemLanguage(language) {
        for (var idx = 0; idx < comboBoxPreferencesSystemLanguage.count; idx ++) {
            if (language === comboBoxPreferencesSystemLanguage.valueAt(idx)) {
                comboBoxPreferencesSystemLanguage.currentIndex = idx
                break
            }
        }
    }

    function setSystemTheme(theme) {
        for (var idx = 0; idx < comboBoxPreferencesSystemTheme.count; idx ++) {
            if (theme === comboBoxPreferencesSystemTheme.valueAt(idx)) {
                comboBoxPreferencesSystemTheme.currentIndex = idx
                break
            }
        }
    }

    function setFileFilenamePrefixFormat(filenameFormat) {
        textFieldPreferencesFileFilenamePrefixFormat.text = filenameFormat
    }

    function setFileOverwriteExistingFile(overwrite) {
        switchPreferencesFileOverwrite.checked = overwrite
    }

    function setNetworkSciHubURLs(urls) {
        comboBoxPreferencesNetworkSciHubURL.model = urls
    }

    function setNetworkSciHubURL(url) {
        for (var idx = 0; idx < comboBoxPreferencesNetworkSciHubURL.count; idx ++) {
            if (url === comboBoxPreferencesNetworkSciHubURL.valueAt(idx)) {
                comboBoxPreferencesNetworkSciHubURL.currentIndex = idx
                break
            }
        }
    }

    function setNetworkTimeout(networkTimeout) {
        textFieldPreferencesNetworkTimeout.text = networkTimeout
    }

    function setNetworkRetryTimes(networkRetryTimes) {
        textFieldPreferencesNetworkRetryTimes.text = networkRetryTimes
    }

    function setNetworkProxyEnabled(proxyEnabled) {
        switchPreferencesNetworkEnableProxy.checked = proxyEnabled
    }

    function setNetworkProxyType(proxyType) {
        if (proxyType === "http") {
            radioButtonPreferencesNetworkProxyTypeHTTP.checked = true
        } else if (proxyType === "socks5") {
            radioButtonPreferencesNetworkProxyTypeSocks5.checked = true
        }
    }

    function setNetworkProxyHost(proxyHost) {
        textFieldPreferencesNetworkProxyHost.text = proxyHost
    }

    function setNetworkProxyPort(proxyPort) {
        textFieldPreferencesNetworkProxyPort.text = proxyPort
    }

    function setNetworkProxyUsername(proxyUsername) {
        textFieldPreferencesNetworkProxyUsername.text = proxyUsername
    }

    function setNetworkProxyPassword(proxyPassword) {
        textFieldPreferencesNetworkProxyPassword.text = proxyPassword
    }

    UI.AddSciHubURL {
        id: windowAddSciHubURL
    }

    UIElements.Message {
        id: dialogPreferencesMessage

        modal: true

        footer: DialogButtonBox {
            Button {
                text: qsTr("OK")

                onClicked: {
                    dialogPreferencesMessage.close()
                }
            }
        }
    }

    UIElements.Message {
        id: dialogPreferencesRemoveSciHubURLConfirmMessage

        modal: true

        footer: DialogButtonBox {
            Button {
                text: qsTr("Yes")

                onClicked: {
                    removeSciHubURL(comboBoxPreferencesNetworkSciHubURL.currentIndex)
                    dialogPreferencesRemoveSciHubURLConfirmMessage.close()
                }
            }

            Button {
                text: qsTr("No")

                onClicked: dialogPreferencesRemoveSciHubURLConfirmMessage.close()
            }
        }
    }

    ColumnLayout {
        id: columnLayoutPreferences

        anchors.fill: parent
        anchors.margins: margin

        Layout.fillHeight: true
        Layout.fillWidth: true

        RowLayout {
            Layout.fillHeight: true
            Layout.fillWidth: true

            ColumnLayout {
                id: columnLayoutPreferenceList

                Layout.fillHeight: true
                Layout.fillWidth: true

                Layout.minimumWidth: 120
                Layout.maximumWidth: 120

                ListModel {
                    id: listModelPreferencesTools

                    ListElement {
                        property string name: qsTr("System")
                        property string iconSource: "qrc:/images/icons/monitor.svg"
                    }

                    ListElement {
                        property string name: qsTr("File")
                        property string iconSource: "qrc:/images/icons/edit_file.svg"
                    }

                    ListElement {
                        property string name: qsTr("Network")
                        property string iconSource: "qrc:/images/icons/ethernet_on.svg"
                    }
                }

                Component {
                    id: itemDelegatePreferencesTools

                    UIElements.ItemDelegate {
                        width: parent.width

                        onClicked: {
                            listViewPreferencesTools.currentIndex = index
                            stackLayoutPreferencesPanel.currentIndex = index
                        }
                    }
                }

                ListView {
                    id: listViewPreferencesTools

                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    model: listModelPreferencesTools
                    delegate: itemDelegatePreferencesTools

                    Component.onCompleted: {
                        listViewPreferencesTools.currentIndex = 0
                        stackLayoutPreferencesPanel.currentIndex = 0
                    }
                }
            }

            ToolSeparator {
                rightPadding: 3
                leftPadding: 3
                bottomPadding: 0
                topPadding: 0

                Layout.fillHeight: true
            }

            StackLayout {
                id: stackLayoutPreferencesPanel

                currentIndex: 0

                Layout.fillHeight: true
                Layout.fillWidth: true

                Layout.minimumWidth: 480
                Layout.minimumHeight: 400

                Item {
                    id: itemPreferencesSystem

                    ScrollView {
                        id: scrollViewPreferencesSystem

                        anchors.fill: parent

                        ColumnLayout {
                            spacing: margin
                            width: Math.max(implicitWidth, scrollViewPreferencesSystem.width)

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Language: ")
                                }

                                ComboBox {
                                    id: comboBoxPreferencesSystemLanguage

                                    Layout.fillWidth: true

                                    textRole: "text"
                                    valueRole: "value"

                                    model: [
                                        { text: "English", value: "en" },
                                        { text: "简体中文", value: "zh_CN" },
                                        { text: "繁體中文", value: "zh_HK" },
                                        { text: "正體中文", value: "zh_TW" },
                                        { text: "Português", value: "pt_PT" }
                                    ]
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Theme: ")
                                }

                                ComboBox {
                                    id: comboBoxPreferencesSystemTheme

                                    Layout.fillWidth: true

                                    textRole: "text"
                                    valueRole: "value"

                                    model: [
                                        { text: qsTr("System"), value: "System" },
                                        { text: qsTr("Light"), value: "Light" },
                                        { text: qsTr("Dark"), value: "Dark" }
                                    ]
                                }
                            }

                            ToolSeparator {
                                Layout.fillWidth: true

                                rightPadding: 0
                                leftPadding: 0
                                orientation: Qt.Horizontal
                            }

                            RowLayout {
                                Layout.fillWidth: true

                                Image {
                                    Layout.alignment: Qt.AlignLeft | Qt.AlignTop

                                    source: "qrc:/images/icons/info.svg"
                                    sourceSize.height: labelAttention.font.pointSize * 1.6
                                    sourceSize.width: labelAttention.font.pointSize * 1.6
                                }

                                Label {
                                    id: labelAttention
                                    text: qsTr("Changes will take effect after restart")
                                }
                            }
                        }
                    }
                }

                Item {
                    id: itemPreferencesFile

                    ScrollView {
                        id: scrollViewPreferencesFile

                        anchors.fill: parent

                        ColumnLayout {
                            spacing: margin
                            width: Math.max(implicitWidth, scrollViewPreferencesFile.width)

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Overwrite Existing File: ")
                                }

                                Switch {
                                    id: switchPreferencesFileOverwrite
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Filename Prefix Format: ")
                                }

                                TextField {
                                    id: textFieldPreferencesFileFilenamePrefixFormat

                                    Layout.fillWidth: true

                                    selectByMouse: true
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Supported Keywords: ")

                                    Layout.alignment: Qt.AlignTop
                                }

                                ColumnLayout {
                                    Label {
                                        text: qsTr("{author}: Author")
                                    }

                                    Label {
                                        text: qsTr("{year}: Year")
                                    }

                                    Label {
                                        text: qsTr("{title}: Title")
                                    }

                                    Label {
                                        text: qsTr("{id}: DOI or PMID")
                                    }
                                }
                            }
                        }
                    }
                }

                Item {
                    id: itemPreferencesNetwork

                    ScrollView {
                        id: scrollViewPreferencesNetwork

                        anchors.fill: parent

                        ColumnLayout {
                            spacing: margin
                            width: Math.max(implicitWidth, scrollViewPreferencesNetwork.width)

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("SciHub URL: ")
                                }

                                ComboBox {
                                    id: comboBoxPreferencesNetworkSciHubURL

                                    Layout.fillWidth: true
                                }

                                RoundButton {
                                    id: roundButtonPreferencesNetworkSciHubURLAdd
                                    text: "+"

                                    onClicked: {
                                        showUIAddSciHubURL()
                                    }
                                }

                                RoundButton {
                                    id: roundButtonPreferencesNetworkSciHubURLRemove
                                    text: "-"

                                    onClicked: {
                                        if (comboBoxPreferencesNetworkSciHubURL.count <= 1) {
                                            dialogPreferencesMessage.messageType = "error"
                                            dialogPreferencesMessage.message = qsTr("Cannot remove the last Sci-Hub URL!")
                                            dialogPreferencesMessage.open()
                                        } else {
                                            var message = qsTr("Delete Sci-Hub URL: ") + comboBoxPreferencesNetworkSciHubURL.currentText + " ?"
                                            dialogPreferencesRemoveSciHubURLConfirmMessage.messageType = "question"
                                            dialogPreferencesRemoveSciHubURLConfirmMessage.message = message
                                            dialogPreferencesRemoveSciHubURLConfirmMessage.open()
                                        }
                                    }
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true


                                Label {
                                    text: qsTr("Timeout: ")
                                }

                                TextField {
                                    id: textFieldPreferencesNetworkTimeout

                                    Layout.fillWidth: true

                                    horizontalAlignment: Text.AlignHCenter
                                    selectByMouse: true
                                    validator: RegularExpressionValidator {
                                        regularExpression: /[0-9]+/
                                    }
                                }

                                Label {
                                    text: "ms"
                                }

                                ToolSeparator {}

                                Label {
                                    text: qsTr("Retry Times: ")
                                }

                                TextField {
                                    id: textFieldPreferencesNetworkRetryTimes

                                    Layout.fillWidth: true

                                    horizontalAlignment: Text.AlignHCenter
                                    selectByMouse: true
                                    validator: RegularExpressionValidator {
                                        regularExpression: /[0-9]+/
                                    }
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Enable Proxy")
                                }

                                Switch {
                                    id: switchPreferencesNetworkEnableProxy
                                }

                                ToolSeparator {}

                                Label {
                                    text: qsTr("Proxy Type: ")
                                }

                                RadioButton {
                                    id: radioButtonPreferencesNetworkProxyTypeHTTP
                                    text: "HTTP"
                                }

                                RadioButton {
                                    id: radioButtonPreferencesNetworkProxyTypeSocks5
                                    text: "SOCKS5"
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Proxy Host: ")
                                }

                                TextField {
                                    id: textFieldPreferencesNetworkProxyHost

                                    Layout.fillWidth: true

                                    selectByMouse: true
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Proxy Port: ")
                                }

                                TextField {
                                    id: textFieldPreferencesNetworkProxyPort

                                    Layout.fillWidth: true

                                    selectByMouse: true
                                    validator: RegularExpressionValidator {
                                        regularExpression: /[0-9]+/
                                    }
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Proxy Username: ")
                                }

                                TextField {
                                    id: textFieldPreferencesNetworkProxyUsername

                                    Layout.fillWidth: true

                                    selectByMouse: true
                                }
                            }

                            RowLayout {
                                Layout.fillHeight: true
                                Layout.fillWidth: true

                                Label {
                                    text: qsTr("Proxy Password: ")
                                }

                                TextField {
                                    id: textFieldPreferencesNetworkProxyPassword

                                    Layout.fillWidth: true

                                    echoMode: TextInput.Password
                                }
                            }
                        }
                    }
                }
            }
        }

        RowLayout {
            Layout.topMargin: 6
            Layout.fillHeight: true

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight | Qt.AlignTop

            Button {
                id: buttonPreferencesConfirm
                text: qsTr("Confirm")

                onClicked: saveAll()
            }

            Button {
                id: buttonPreferencesCancel
                text: qsTr("Cancel")

                onClicked: close()
            }
        }

        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Enter || event.key === Qt.Key_Return) {
                buttonPreferencesConfirm.clicked()
            } else if (event.key === Qt.Key_Escape) {
                buttonPreferencesCancel.clicked()
            }
        }
    }
}
