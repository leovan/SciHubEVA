import QtQuick 2.14
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14
import QtQuick.Window 2.14

ApplicationWindow {
    title: qsTr("Captcha")

    modality: Qt.ApplicationModal

    property int margin: 10

    width: columnLayoutCaptcha.implicitWidth + 2 * margin
    height: columnLayoutCaptcha.implicitHeight + 2 * margin
    minimumWidth: columnLayoutCaptcha.Layout.minimumWidth + 2 * margin
    minimumHeight: columnLayoutCaptcha.Layout.minimumHeight + 2 * margin

    signal killCaptcha(bool kill, string captcha)

    function showWindowCaptcha(captchaImagePath) {
        imageCaptcha.source = captchaImagePath
        textFieldCaptcha.text = ""
        show()
    }

    ColumnLayout {
        id: columnLayoutCaptcha

        anchors.fill: parent
        anchors.margins: margin

        focus: true

        Image {
            id: imageCaptcha
        }

        RowLayout {
            id: rowLayoutCaptchaButtons

            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight | Qt.AlignVCenter

            Label {
                id: labelCaptcha
                text: qsTr("Enter captcha: ")
            }

            TextField {
                id: textFieldCaptcha

                Layout.minimumWidth: 100

                selectByMouse: true
            }

            Button {
                id: buttonCaptchaConfirm
                text: qsTr("Confirm")

                onClicked: {
                    close()
                    killCaptcha(true, textFieldCaptcha.text.trim())
                }
            }

            Button {
                id: buttonCaptchaCancel
                text: qsTr("Cancel")

                onClicked: {
                    close()
                    killCaptcha(false, "")
                }
            }
        }

        Keys.onPressed: {
            if (event.key === Qt.Key_Enter || event.key === Qt.Key_Return) {
                buttonCaptchaConfirm.clicked()
            } else if (event.key === Qt.Key_Escape) {
                buttonCaptchaCancel.clicked()
            }
        }
    }
}
