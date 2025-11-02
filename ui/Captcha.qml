import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Window

ApplicationWindow {
    id: applicationWindowCaptcha
    title: qsTr("Captcha")

    modality: Qt.ApplicationModal
    flags: Qt.Dialog

    property int margin: 10
    property bool kill: false

    width: columnLayoutCaptcha.implicitWidth + 2 * margin
    height: columnLayoutCaptcha.implicitHeight + 2 * margin
    minimumWidth: columnLayoutCaptcha.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutCaptcha.Layout.minimumHeight + 2 * margin

    signal killCaptcha(bool kill, string captcha)

    function showUICaptcha(captchaImagePath) {
        imageCaptcha.source = captchaImagePath
        textFieldCaptcha.text = ""
        show()
    }

    ColumnLayout {
        id: columnLayoutCaptcha

        anchors.fill: parent
        anchors.margins: margin
        spacing: margin

        focus: true

        Image {
            id: imageCaptcha
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter

            Label {
                text: qsTr("Captcha: ")
            }

            TextField {
                id: textFieldCaptcha

                Layout.minimumWidth: 160

                selectByMouse: true
            }

            Item {
                Layout.fillWidth: true
                Layout.fillHeight: true
            }

            Button {
                id: buttonCaptchaConfirm
                text: qsTr("Confirm")

                onClicked: {
                    applicationWindowCaptcha.kill = true
                    close()
                }
            }

            Button {
                id: buttonCaptchaCancel
                text: qsTr("Cancel")

                onClicked: {
                    applicationWindowCaptcha.kill = false
                    close()
                }
            }
        }

        Keys.onPressed: (event) => {
            if (event.key === Qt.Key_Enter || event.key === Qt.Key_Return) {
                buttonCaptchaConfirm.clicked()
            } else if (event.key === Qt.Key_Escape) {
                buttonCaptchaCancel.clicked()
            }
        }
    }

    onClosing: {
        killCaptcha(kill, textFieldCaptcha.text.trim())
    }
}
