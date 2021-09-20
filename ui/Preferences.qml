import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Window

import "." as UI
import "./elements" as UIElements

ApplicationWindow {
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

        focus: true

        RowLayout {
            spacing: 0

            Layout.fillHeight: true
            Layout.fillWidth: true

            ListModel {
                id: listModelPreferencesTabButtons

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
                id: itemDelegatePreferencesTabButtons

                ItemDelegate {
                    width: parent.width
                    highlighted: ListView.isCurrentItem

                    RowLayout {
                        Layout.fillHeight: true
                        Layout.fillWidth: true

                        anchors.fill: parent
                        Layout.alignment: Qt.AlignCenter | Qt.AlignVCenter

                        Image {
                            source: iconSource

                            sourceSize.height: labelDelegateToolsItemText.font.pointSize * 1.6
                            sourceSize.width: labelDelegateToolsItemText.font.pointSize * 1.6

                            Layout.leftMargin: 6
                        }

                        Label {
                            id: labelDelegateToolsItemText

                            text: name
                            font.weight: Font.Medium

                            Layout.rightMargin: 6
                            Layout.fillWidth: true
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
                    id: itemTabPreferencesSystem

                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    GridLayout {
                        columnSpacing: 3
                        rowSpacing: 0

                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.top: parent.top

                        columns: 2

                        Label {
                            text: qsTr("Language: ")
                        }

                        ComboBox {
                            id: comboBoxPreferencesSystemLanguage

                            Layout.minimumWidth: 200
                            Layout.fillWidth: true

                            textRole: "text"
                            valueRole: "value"

                            model: [
                                { text: "English", value: "en" },
                                { text: "简体中文", value: "zh_CN" },
                                { text: "繁體中文", value: "zh_HK" },
                                { text: "正體中文", value: "zh_TW" }
                            ]
                        }

                        Label {
                            text: qsTr("Theme: ")
                        }

                        ComboBox {
                            id: comboBoxPreferencesSystemTheme

                            Layout.minimumWidth: 200
                            Layout.fillWidth: true

                            textRole: "text"
                            valueRole: "value"

                            model: [
                                { text: qsTr("System"), value: "System" },
                                { text: qsTr("Light"), value: "Light" },
                                { text: qsTr("Dark"), value: "Dark" }
                            ]
                        }

                        ToolSeparator {
                            rightPadding: 0
                            leftPadding: 0
                            Layout.fillWidth: true
                            Layout.columnSpan: 2
                            orientation: Qt.Horizontal
                        }

                        RowLayout {
                            Layout.fillWidth: true
                            Layout.columnSpan: 2

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

                Item {
                    id: itemTabPreferencesFile

                    Layout.fillHeight: true
                    Layout.fillWidth: true

                    GridLayout {
                        columnSpacing: 3
                        rowSpacing: 0

                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.top: parent.top

                        columns: 2

                        Label {
                            text: qsTr("Filename Prefix Format: ")
                        }

                        TextField {
                            id: textFieldPreferencesFileFilenamePrefixFormat

                            implicitWidth: 200
                            Layout.fillWidth: true

                            placeholderText: "{id}_{year}_{author}_{title}"
                            selectByMouse: true
                        }

                        Label {
                            text: qsTr("Supported Keywords: ") + "<br/>" +
                                  qsTr("{author}: Author, {year}: Year, {title}: Title, {id}: DOI or PMID")
                            Layout.columnSpan: 2
                        }

                        Label {
                            text: qsTr("Overwrite Existing File: ")
                        }

                        Switch {
                            id: switchPreferencesFileOverwrite
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
                        rowSpacing: 0
                        columnSpacing: 3

                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.top: parent.top

                        rows: 9
                        columns: 2

                        Label {
                            text: qsTr("SciHub URL: ")
                        }

                        RowLayout {
                            Layout.fillWidth: true

                            ComboBox {
                                id: comboBoxPreferencesNetworkSciHubURL

                                Layout.minimumWidth: 160
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

                        Label {
                            text: qsTr("Timeout: ")
                        }

                        RowLayout {
                            width: 100
                            height: 100

                            TextField {
                                id: textFieldPreferencesNetworkTimeout

                                implicitWidth: 60
                                Layout.fillWidth: false

                                horizontalAlignment: Text.AlignHCenter
                                selectByMouse: true
                                validator: RegularExpressionValidator {
                                    regularExpression: /[0-9]+/
                                }
                            }

                            Label {
                                text: "ms"
                            }
                        }

                        Label {
                            text: qsTr("Retry Times: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkRetryTimes

                            implicitWidth: 60
                            Layout.fillWidth: false

                            horizontalAlignment: Text.AlignHCenter
                            selectByMouse: true
                            validator: RegularExpressionValidator {
                                regularExpression: /[0-9]+/
                            }
                        }

                        Label {
                            text: qsTr("Enable Proxy")
                        }

                        Switch {
                            id: switchPreferencesNetworkEnableProxy
                            text: checked ? qsTr("Yes") : qsTr("No")
                        }

                        Label {
                            text: qsTr("Proxy Type: ")
                        }

                        RowLayout {
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
                            text: qsTr("Proxy Host: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkProxyHost

                            implicitWidth: 200
                            Layout.fillWidth: true

                            selectByMouse: true
                        }

                        Label {
                            text: qsTr("Proxy Port: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkProxyPort

                            implicitWidth: 200
                            Layout.fillWidth: true

                            selectByMouse: true
                            validator: RegularExpressionValidator {
                                regularExpression: /[0-9]+/
                            }
                        }

                        Label {
                            text: qsTr("Proxy Username: ")
                        }

                        TextField {
                            id: textFieldPreferencesNetworkProxyUsername

                            implicitWidth: 200
                            Layout.fillWidth: true

                            selectByMouse: true
                        }

                        Label {
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


